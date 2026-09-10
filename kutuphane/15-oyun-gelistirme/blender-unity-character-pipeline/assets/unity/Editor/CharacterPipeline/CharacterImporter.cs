using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.Animations;
using UnityEngine;

namespace CharacterPipeline
{
    [Serializable]
    public class PipelineReport
    {
        public bool ok = true;
        public string character;
        public string prefab;
        public string controller;
        public bool avatar_valid;
        public bool avatar_human;
        public float measured_height_m;
        public List<string> clips = new List<string>();
        public List<string> issues = new List<string>();
        public void Fail(string msg) { ok = false; issues.Add(msg); }
        public string ToJson() => JsonUtility.ToJson(this, true);
    }

    /// <summary>
    /// Import (copy + configure + avatar + controller + prefab) and Verify a
    /// Blender-exported character from its manifest. Idempotent: safe to rerun
    /// after every Blender re-export.
    /// </summary>
    public static class CharacterImporter
    {
        static string ProjectRoot => Directory.GetParent(Application.dataPath).FullName;

        static string ToAbs(string assetPath) => Path.Combine(ProjectRoot, assetPath);

        static void EnsureFolder(string assetFolder)
        {
            var parts = assetFolder.Replace('\\', '/').Split('/');
            var cur = parts[0];
            for (int i = 1; i < parts.Length; i++)
            {
                var next = cur + "/" + parts[i];
                if (!AssetDatabase.IsValidFolder(next)) AssetDatabase.CreateFolder(cur, parts[i]);
                cur = next;
            }
        }

        static void CopyIn(string srcDir, string file, string folder)
        {
            var src = Path.Combine(srcDir, file);
            var dst = ToAbs($"{folder}/{file}");
            if (Path.GetFullPath(src) != Path.GetFullPath(dst)) File.Copy(src, dst, true);
            AssetDatabase.ImportAsset($"{folder}/{file}",
                ImportAssetOptions.ForceUpdate | ImportAssetOptions.ForceSynchronousImport);
        }

        public static AnimationClip LoadClip(string path) =>
            AssetDatabase.LoadAllAssetsAtPath(path).OfType<AnimationClip>()
                .FirstOrDefault(c => !c.name.StartsWith("__preview__", StringComparison.Ordinal));

        public static string Import(string manifestPath)
        {
            var rep = new PipelineReport();
            try
            {
                manifestPath = Path.GetFullPath(manifestPath);
                var m = CharacterManifest.Load(manifestPath);
                rep.character = m.name;
                var srcDir = Path.GetDirectoryName(manifestPath);
                EnsureFolder(m.unity_folder);

                // 1) manifest first (postprocessor keys on it), 2) model, 3) clips.
                CopyIn(srcDir, Path.GetFileName(manifestPath), m.unity_folder);
                CopyIn(srcDir, m.model, m.unity_folder);

                foreach (var c in m.clips) CopyIn(srcDir, c.file, m.unity_folder);

                if (!m.IsHumanoid) ConfigureGenericRoot(m, rep);

                var avatar = AssetDatabase.LoadAllAssetsAtPath(m.ModelAssetPath).OfType<Avatar>().FirstOrDefault();
                rep.avatar_valid = avatar != null && avatar.isValid;
                rep.avatar_human = avatar != null && avatar.isHuman;
                if (!rep.avatar_valid) rep.Fail("Avatar missing/invalid - check bone names & T-pose (Rig tab > Configure).");

                var controller = BuildController(m, rep);
                rep.controller = AssetDatabase.GetAssetPath(controller);
                rep.prefab = BuildPrefab(m, controller, avatar, rep);
                AssetDatabase.SaveAssets();

                var v = JsonUtility.FromJson<PipelineReport>(Verify(manifestPath));
                rep.measured_height_m = v.measured_height_m;
                foreach (var i in v.issues) rep.Fail(i);
            }
            catch (Exception e) { rep.Fail(e.GetType().Name + ": " + e.Message); }
            return rep.ToJson();
        }

        static void ConfigureGenericRoot(CharacterManifest m, PipelineReport rep)
        {
            // Generic root motion needs the transform path of the root bone.
            var model = AssetDatabase.LoadAssetAtPath<GameObject>(m.ModelAssetPath);
            var root = model ? model.GetComponentsInChildren<Transform>(true)
                .FirstOrDefault(t => t.name == m.root_bone) : null;
            if (root == null) { rep.Fail($"Generic: root bone '{m.root_bone}' not found"); return; }
            var path = AnimationUtility.CalculateTransformPath(root, model.transform);
            foreach (var file in new[] { m.model }.Concat(m.clips.Select(c => c.file)))
            {
                var ap = $"{m.unity_folder}/{file}";
                if (AssetImporter.GetAtPath(ap) is ModelImporter mi && mi.motionNodeName != path)
                {
                    mi.motionNodeName = path;
                    if (File.Exists(ToAbs(ap))) mi.SaveAndReimport();
                }
            }
        }

        static AnimatorController BuildController(CharacterManifest m, PipelineReport rep)
        {
            var path = $"{m.unity_folder}/{m.name}.controller";
            AssetDatabase.DeleteAsset(path);
            var ctrl = AnimatorController.CreateAnimatorControllerAtPath(path);
            ctrl.AddParameter("Speed", AnimatorControllerParameterType.Float);
            var sm = ctrl.layers[0].stateMachine;

            var clips = m.clips.Select(c => (meta: c, clip: LoadClip($"{m.unity_folder}/{c.file}"))).ToList();
            foreach (var (meta, clip) in clips)
            {
                if (clip == null) rep.Fail($"Clip not imported: {meta.file}");
                else rep.clips.Add($"{clip.name} {clip.length:0.###}s loop={clip.isLooping}");
            }

            // Locomotion blend tree: every looping clip, threshold = real speed (m/s).
            var loco = clips.Where(x => x.clip != null && x.meta.loop)
                            .OrderBy(x => x.meta.speed_mps).ToList();
            AnimatorState locoState = null;
            if (loco.Count > 0)
            {
                locoState = ctrl.CreateBlendTreeInController("Locomotion", out var tree, 0);
                tree.blendType = BlendTreeType.Simple1D;
                tree.blendParameter = "Speed";
                tree.useAutomaticThresholds = false;
                float last = -1f;
                foreach (var (meta, clip) in loco)
                {
                    float th = Mathf.Max(meta.speed_mps, last + 0.01f); // strictly increasing
                    tree.AddChild(clip, th);
                    last = th;
                }
                sm.defaultState = locoState;
            }

            // One-shots: trigger per clip, Any State -> clip -> back to Locomotion.
            foreach (var (meta, clip) in clips.Where(x => x.clip != null && !x.meta.loop))
            {
                var trig = string.IsNullOrEmpty(meta.state) ? meta.name : meta.state;
                ctrl.AddParameter(trig, AnimatorControllerParameterType.Trigger);
                var st = sm.AddState(meta.name);
                st.motion = clip;
                var tin = sm.AddAnyStateTransition(st);
                tin.AddCondition(AnimatorConditionMode.If, 0, trig);
                tin.duration = 0.08f;
                tin.canTransitionToSelf = false;
                if (locoState != null)
                {
                    var tout = st.AddTransition(locoState);
                    tout.hasExitTime = true;
                    tout.exitTime = 0.9f;
                    tout.duration = 0.1f;
                }
            }
            EditorUtility.SetDirty(ctrl);
            return ctrl;
        }

        static string BuildPrefab(CharacterManifest m, AnimatorController ctrl, Avatar avatar, PipelineReport rep)
        {
            var model = AssetDatabase.LoadAssetAtPath<GameObject>(m.ModelAssetPath);
            if (model == null) { rep.Fail("Model asset missing"); return null; }
            var go = (GameObject)PrefabUtility.InstantiatePrefab(model);
            try
            {
                var anim = go.GetComponent<Animator>();
                if (!anim) anim = go.AddComponent<Animator>();   // no '??': Unity fake-null
                anim.avatar = avatar;
                anim.runtimeAnimatorController = ctrl;
                anim.applyRootMotion = m.clips.Any(c => c.root_motion);
                if (!go.GetComponent<CharacterAnimEvents>()) go.AddComponent<CharacterAnimEvents>();
                var path = $"{m.unity_folder}/{m.name}.prefab";
                PrefabUtility.SaveAsPrefabAsset(go, path);   // variant of the model prefab
                return path;
            }
            finally { UnityEngine.Object.DestroyImmediate(go); }
        }

        /// <summary>Numeric gates on the imported result. Returns JSON report.</summary>
        public static string Verify(string manifestPath)
        {
            var rep = new PipelineReport();
            try
            {
                var m = CharacterManifest.Load(Path.GetFullPath(manifestPath));
                rep.character = m.name;
                var avatar = AssetDatabase.LoadAllAssetsAtPath(m.ModelAssetPath).OfType<Avatar>().FirstOrDefault();
                rep.avatar_valid = avatar != null && avatar.isValid;
                rep.avatar_human = avatar != null && avatar.isHuman;
                if (!rep.avatar_valid) rep.Fail("avatar invalid");
                if (m.IsHumanoid && !rep.avatar_human) rep.Fail("avatar is not humanoid");

                foreach (var c in m.clips)
                {
                    var clip = LoadClip($"{m.unity_folder}/{c.file}");
                    if (clip == null) { rep.Fail($"missing clip {c.file}"); continue; }
                    float want = c.frames / (float)Mathf.Max(1, c.fps);
                    if (Mathf.Abs(clip.length - want) > 1.5f / Mathf.Max(1, c.fps))
                        rep.Fail($"{c.name}: length {clip.length:0.###}s != {want:0.###}s (fps/frame-range mismatch)");
                    if (clip.isLooping != c.loop) rep.Fail($"{c.name}: loop flag {clip.isLooping} != manifest {c.loop}");
                    if (clip.name != c.name) rep.Fail($"{c.name}: imported clip named '{clip.name}'");
                    var evs = AnimationUtility.GetAnimationEvents(clip);
                    if ((c.events?.Length ?? 0) != evs.Length) rep.Fail($"{c.name}: {evs.Length} events, manifest {c.events?.Length ?? 0}");
                    if (m.IsHumanoid && !clip.humanMotion) rep.Fail($"{c.name}: not a humanoid clip (avatar copy failed?)");
                    rep.clips.Add($"{clip.name} {clip.length:0.###}s loop={clip.isLooping} events={evs.Length}");
                }

                var prefab = AssetDatabase.LoadAssetAtPath<GameObject>($"{m.unity_folder}/{m.name}.prefab");
                if (prefab == null) { rep.Fail("prefab missing"); return rep.ToJson(); }
                rep.prefab = AssetDatabase.GetAssetPath(prefab);
                var go = (GameObject)PrefabUtility.InstantiatePrefab(prefab);
                try
                {
                    foreach (var t in go.GetComponentsInChildren<Transform>(true))
                    {
                        if (t.GetComponent<SkinnedMeshRenderer>() || t == go.transform) continue;
                        if (t.parent == go.transform && (Quaternion.Angle(t.localRotation, Quaternion.identity) > 0.5f ||
                                                         (t.localScale - Vector3.one).sqrMagnitude > 1e-4f))
                            rep.Fail($"'{t.name}' root child has rot {t.localEulerAngles} scale {t.localScale} " +
                                     "(axis/scale conversion not baked - check Blender FBX_SCALE_ALL + bakeAxisConversion)");
                    }
                    var names = new HashSet<string>(go.GetComponentsInChildren<Transform>(true).Select(t => t.name));
                    foreach (var sk in m.sockets ?? new string[0])
                        if (!names.Contains(sk)) rep.Fail($"socket transform missing: {sk}");
                    var anim = go.GetComponent<Animator>();
                    if (m.IsHumanoid && anim != null && anim.isHuman)
                        foreach (var hb in new[] { HumanBodyBones.Hips, HumanBodyBones.Head, HumanBodyBones.LeftFoot,
                                                   HumanBodyBones.RightFoot, HumanBodyBones.LeftHand, HumanBodyBones.RightHand })
                            if (anim.GetBoneTransform(hb) == null) rep.Fail($"humanoid bone unmapped: {hb}");
                    var rends = go.GetComponentsInChildren<Renderer>();
                    if (rends.Length > 0)
                    {
                        var b = rends[0].bounds;
                        foreach (var r in rends) b.Encapsulate(r.bounds);
                        rep.measured_height_m = b.size.y;
                        if (m.height_m > 0 && Mathf.Abs(b.size.y - m.height_m) / m.height_m > 0.06f)
                            rep.Fail($"height {b.size.y:0.###}m vs manifest {m.height_m}m (unit/scale problem)");
                        if (b.min.y < -0.05f || b.min.y > 0.05f)
                            rep.Fail($"feet not on origin (min y {b.min.y:0.###})");
                    }
                    else rep.Fail("no renderers in prefab");
                }
                finally { UnityEngine.Object.DestroyImmediate(go); }
            }
            catch (Exception e) { rep.Fail(e.GetType().Name + ": " + e.Message); }
            return rep.ToJson();
        }

        [MenuItem("Tools/Character Pipeline/Import Manifest...")]
        static void MenuImport()
        {
            var p = EditorUtility.OpenFilePanel("Character manifest", "", "json");
            if (!string.IsNullOrEmpty(p)) Debug.Log(Import(p));
        }
    }

    /// <summary>Batch entry for `unity run <project> -- -executeMethod ... -manifest <path>`.</summary>
    public static class CharacterBatch
    {
        public static void ImportFromCommandLine()
        {
            var args = Environment.GetCommandLineArgs();
            int i = Array.IndexOf(args, "-manifest");
            if (i < 0 || i + 1 >= args.Length) { Debug.LogError("usage: -manifest <path>"); EditorApplication.Exit(2); return; }
            var json = CharacterImporter.Import(args[i + 1]);
            Debug.Log("CHARACTER_PIPELINE_REPORT " + json);
            EditorApplication.Exit(JsonUtility.FromJson<PipelineReport>(json).ok ? 0 : 1);
        }
    }
}

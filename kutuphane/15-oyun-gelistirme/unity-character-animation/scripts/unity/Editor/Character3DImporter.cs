// Character3DImporter — uca-3d/1 manifest + FBX (from blender/uca_character.py) -> Humanoid avatar with an
// EXPLICIT bone map (no automap guessing), named/looped in-place clips with events, a Point-filtered palette
// material remapped onto the model, a locomotion blend-tree Animator Controller, a prefab variant, and a
// numeric report (avatar valid, root rotation, height, facing +Z).
//
//   unity command uca_3d_import --manifest Assets/Characters/Hero/Hero.manifest.json
//   unity command eval "return UCA.Editor.Character3DImporter.Run(\"Assets/Characters/Hero/Hero.manifest.json\");"
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.Animations;
using UnityEngine;

namespace UCA.Editor
{
    [Serializable] public class ManClip { public string name; public bool loop; public int frames; public int impactFrame = -1; }
    [Serializable] public class ManBone { public string bone; public string human; }
    [Serializable] public class ManLoco { public float walkSpeed = 1.6f; public float runSpeed = 4.5f; }
    [Serializable] public class ManCapsule { public float height = 1.8f; public float radius = 0.3f; }
    [Serializable] public class Manifest3D
    {
        public string schema, name, fbx, palette, material, exportPreset;
        public float height; public int fps;
        public bool bakeAxisConversion;
        public ManClip[] clipList;
        public ManBone[] humanList;
        public ManLoco locomotion;
        public ManCapsule capsule;
    }

    [Serializable] public class Import3DReport
    {
        public bool ok;
        public string character, model, controller, prefab, material;
        public bool avatarValid, avatarHuman, facesPlusZ;
        public float measuredHeight;
        public string rootRotation;
        public List<ClipReport> clips = new List<ClipReport>();
        public List<string> warnings = new List<string>();
        public List<string> errors = new List<string>();
    }

    public static class Character3DImporter
    {
        public static string Run(string manifestPath, string outputFolder = "", bool makePrefab = true, bool addController = true)
        {
            var rep = new Import3DReport();
            try { Import(manifestPath, outputFolder, makePrefab, addController, rep); }
            catch (Exception e) { rep.errors.Add(e.GetType().Name + ": " + e.Message); }
            rep.ok = rep.errors.Count == 0;
            return JsonUtility.ToJson(rep, true);
        }

        static void Import(string manPath, string outFolder, bool makePrefab, bool addController, Import3DReport rep)
        {
            manPath = manPath.Replace('\\', '/');
            if (!manPath.StartsWith("Assets/")) throw new ArgumentException("manifest path must be project-relative (Assets/...)");
            var man = JsonUtility.FromJson<Manifest3D>(File.ReadAllText(manPath));
            if (man == null || man.schema != "uca-3d/1") throw new InvalidDataException("not a uca-3d/1 manifest");
            string dir = Path.GetDirectoryName(manPath).Replace('\\', '/');
            string fbxPath = dir + "/" + man.fbx;
            if (string.IsNullOrEmpty(outFolder)) outFolder = dir + "/Animations";
            PixelCharacterImporter.EnsureFolder(outFolder);
            rep.character = man.name; rep.model = fbxPath;

            AssetDatabase.ImportAsset(fbxPath, ImportAssetOptions.ForceSynchronousImport);
            var mi = AssetImporter.GetAtPath(fbxPath) as ModelImporter;
            if (mi == null) throw new FileNotFoundException("FBX not imported: " + fbxPath);

            // pass 1 — geometry/axes/rig type
            mi.globalScale = 1f;
            mi.useFileScale = true;
            mi.bakeAxisConversion = man.bakeAxisConversion;   // must match the Blender export preset
            mi.importCameras = false;
            mi.importLights = false;
            mi.importBlendShapes = false;
            mi.importAnimation = true;
            mi.animationType = ModelImporterAnimationType.Human;
            mi.avatarSetup = ModelImporterAvatarSetup.CreateFromThisModel;
            mi.materialImportMode = ModelImporterMaterialImportMode.ImportViaMaterialDescription;
            mi.SaveAndReimport();

            // pass 2 — explicit humanoid map + skeleton (T-pose bind) from the imported hierarchy
            var model = AssetDatabase.LoadAssetAtPath<GameObject>(fbxPath);
            var desc = mi.humanDescription;
            var human = new List<HumanBone>();
            foreach (var b in man.humanList ?? new ManBone[0])
            {
                if (!Enum.TryParse(b.human, out HumanBodyBones hb) || hb == HumanBodyBones.LastBone)
                { rep.warnings.Add("unknown HumanBodyBones name: " + b.human); continue; }
                if (FindDeep(model.transform, b.bone) == null) { rep.warnings.Add("bone not in model: " + b.bone); continue; }
                var h = new HumanBone { boneName = b.bone, humanName = HumanTrait.BoneName[(int)hb] };
                h.limit = new HumanLimit { useDefaultValues = true };   // struct: assign whole, never mutate in place
                human.Add(h);
            }
            desc.human = human.ToArray();
            desc.skeleton = model.GetComponentsInChildren<Transform>(true).Select(t => new SkeletonBone
            {
                name = t.name, position = t.localPosition, rotation = t.localRotation, scale = t.localScale
            }).ToArray();
            desc.upperArmTwist = 0.5f; desc.lowerArmTwist = 0.5f; desc.upperLegTwist = 0.5f; desc.lowerLegTwist = 0.5f;
            desc.armStretch = 0.05f; desc.legStretch = 0.05f; desc.feetSpacing = 0f; desc.hasTranslationDoF = false;
            mi.humanDescription = desc;
            mi.SaveAndReimport();

            var avatar = AssetDatabase.LoadAllAssetsAtPath(fbxPath).OfType<Avatar>().FirstOrDefault();
            rep.avatarValid = avatar != null && avatar.isValid;
            rep.avatarHuman = avatar != null && avatar.isHuman;
            if (!rep.avatarValid || !rep.avatarHuman) rep.errors.Add("avatar invalid or not humanoid — check the bone map / T-pose");

            // pass 3 — clips: strip '<Armature>|' take prefix, loop flags, bake root into pose (in-place), events
            var byName = (man.clipList ?? new ManClip[0]).ToDictionary(c => c.name);
            var defs = mi.defaultClipAnimations;
            var outClips = new List<ModelImporterClipAnimation>();
            foreach (var d in defs)
            {
                string clean = d.takeName.Contains("|") ? d.takeName.Substring(d.takeName.LastIndexOf('|') + 1) : d.takeName;
                byName.TryGetValue(clean, out var mc);
                d.name = clean;
                d.loopTime = mc != null && mc.loop;
                d.loopPose = false;                      // clips already end on their first pose
                d.lockRootRotation = true; d.keepOriginalOrientation = true;
                d.lockRootHeightY = true; d.keepOriginalPositionY = true; d.heightFromFeet = false;
                d.lockRootPositionXZ = true; d.keepOriginalPositionXZ = true;
                var evs = new List<AnimationEvent>();
                if (mc != null && mc.impactFrame >= 0 && mc.frames > 0)
                    evs.Add(new AnimationEvent { time = Mathf.Clamp01((float)mc.impactFrame / mc.frames), functionName = "OnAttackHit" });
                if (clean == "Death") evs.Add(new AnimationEvent { time = 0.99f, functionName = "OnDeathFinished" });
                d.events = evs.ToArray();                // ModelImporter event time is NORMALIZED (0..1)
                outClips.Add(d);
                if (mc == null) rep.warnings.Add("take '" + d.takeName + "' not in manifest");
            }
            mi.clipAnimations = outClips.ToArray();
            mi.SaveAndReimport();

            // pass 4 — palette material (Point filter, pipeline-appropriate shader), remapped onto the FBX
            if (!string.IsNullOrEmpty(man.palette))
            {
                string texPath = dir + "/" + man.palette;
                AssetDatabase.ImportAsset(texPath, ImportAssetOptions.ForceSynchronousImport);
                var ti = AssetImporter.GetAtPath(texPath) as TextureImporter;
                if (ti != null)
                {
                    ti.filterMode = FilterMode.Point; ti.mipmapEnabled = false; ti.wrapMode = TextureWrapMode.Clamp;
                    ti.textureCompression = TextureImporterCompression.Uncompressed; ti.sRGBTexture = true;
                    ti.SaveAndReimport();
                }
                var tex = AssetDatabase.LoadAssetAtPath<Texture2D>(texPath);
                string matPath = outFolder + "/" + (string.IsNullOrEmpty(man.material) ? "MAT_" + man.name : man.material) + ".mat";
                var mat = AssetDatabase.LoadAssetAtPath<Material>(matPath);
                var shader = PipelineLitShader();
                if (mat == null) { mat = new Material(shader); AssetDatabase.CreateAsset(mat, matPath); }
                else mat.shader = shader;
                mat.mainTexture = tex;   // maps to _BaseMap (URP/HDRP) or _MainTex (Built-in) via [MainTexture]
                if (mat.HasProperty("_Smoothness")) mat.SetFloat("_Smoothness", 0.15f);
                if (mat.HasProperty("_Glossiness")) mat.SetFloat("_Glossiness", 0.15f);
                EditorUtility.SetDirty(mat);
                mi.AddRemap(new AssetImporter.SourceAssetIdentifier(typeof(Material), man.material), mat);
                mi.SaveAndReimport();
                rep.material = matPath;
            }

            // clip report
            var clips = AssetDatabase.LoadAllAssetsAtPath(fbxPath).OfType<AnimationClip>()
                .Where(c => !c.name.StartsWith("__preview__")).ToDictionary(c => c.name);
            foreach (var c in clips.Values)
                rep.clips.Add(new ClipReport { name = c.name, frames = Mathf.RoundToInt(c.length * c.frameRate), seconds = c.length,
                                               loop = c.isLooping, events = c.events.Select(e => e.functionName).ToArray() });
            foreach (var mc in byName.Keys.Where(k => !clips.ContainsKey(k))) rep.errors.Add("clip missing after import: " + mc);

            // controller
            AnimatorController ctrl = null;
            if (addController)
            {
                string ctrlPath = outFolder + "/" + man.name + ".controller";
                ctrl = AssetDatabase.LoadAssetAtPath<AnimatorController>(ctrlPath) ?? AnimatorController.CreateAnimatorControllerAtPath(ctrlPath);
                Build3DController(ctrl, clips, man.locomotion ?? new ManLoco(), rep);
                EditorUtility.SetDirty(ctrl);
                AssetDatabase.SaveAssets();
                rep.controller = ctrlPath;
            }

            // measurements on a temporary instance
            var inst = (GameObject)PrefabUtility.InstantiatePrefab(model);
            try
            {
                var e = inst.transform.localRotation.eulerAngles;
                rep.rootRotation = e.ToString("0.0");
                if (Quaternion.Angle(inst.transform.localRotation, Quaternion.identity) > 0.5f)
                    rep.warnings.Add("model root is rotated " + rep.rootRotation + " — with preset '" + man.exportPreset +
                                     "' expected identity; switch preset or toggle Bake Axis Conversion");
                var rends = inst.GetComponentsInChildren<Renderer>();
                if (rends.Length > 0)
                {
                    var b = rends[0].bounds; foreach (var r in rends) b.Encapsulate(r.bounds);
                    rep.measuredHeight = b.size.y;
                    if (Mathf.Abs(b.size.y - man.height) / man.height > 0.05f)
                        rep.warnings.Add("height " + b.size.y.ToString("0.00") + " m vs manifest " + man.height + " m (scale issue)");
                }
                var anim = inst.GetComponent<Animator>();
                if (anim != null && anim.avatar != null && anim.isHuman)
                {
                    var toes = anim.GetBoneTransform(HumanBodyBones.LeftToes);
                    var foot = anim.GetBoneTransform(HumanBodyBones.LeftFoot);
                    if (toes != null && foot != null)
                    {
                        Vector3 d = inst.transform.InverseTransformPoint(toes.position) - inst.transform.InverseTransformPoint(foot.position);
                        rep.facesPlusZ = d.z > 0;
                        if (!rep.facesPlusZ) rep.warnings.Add("character faces -Z: rotate 180 in Blender (must face -Y there) and re-export");
                    }
                }
                if (makePrefab)
                {
                    if (anim == null) anim = inst.AddComponent<Animator>();
                    anim.avatar = avatar;
                    anim.applyRootMotion = false;
                    if (ctrl != null) anim.runtimeAnimatorController = ctrl;
                    var cc = inst.GetComponent<CharacterController>() ?? inst.AddComponent<CharacterController>();
                    float hgt = man.capsule != null && man.capsule.height > 0 ? man.capsule.height : man.height;
                    cc.height = hgt; cc.radius = man.capsule != null ? man.capsule.radius : hgt * 0.17f;
                    cc.center = new Vector3(0, hgt / 2f + cc.skinWidth, 0);
                    if (inst.GetComponent<UCA.ThirdPersonAnimatorDriver>() == null) inst.AddComponent<UCA.ThirdPersonAnimatorDriver>();
                    string prefabPath = dir + "/" + man.name + ".prefab";
                    PrefabUtility.SaveAsPrefabAsset(inst, prefabPath);   // variant of the model prefab
                    rep.prefab = prefabPath;
                }
            }
            finally { UnityEngine.Object.DestroyImmediate(inst); }
            AssetDatabase.SaveAssets();
        }

        static Shader PipelineLitShader()
        {
            var rp = UnityEngine.Rendering.GraphicsSettings.currentRenderPipeline;
            string n = rp == null ? "Standard" : rp.GetType().Name.Contains("HD") ? "HDRP/Lit" : "Universal Render Pipeline/Lit";
            return Shader.Find(n) ?? Shader.Find("Standard");
        }

        static Transform FindDeep(Transform t, string name)
        {
            if (t.name == name) return t;
            foreach (Transform c in t) { var r = FindDeep(c, name); if (r != null) return r; }
            return null;
        }

        static AnimatorStateTransition T(AnimatorState a, AnimatorState b, bool exit, float exitTime, float dur)
        {
            var t = a.AddTransition(b);
            t.hasExitTime = exit; t.exitTime = exitTime; t.hasFixedDuration = true; t.duration = dur;
            return t;
        }

        static void Build3DController(AnimatorController ctrl, Dictionary<string, AnimationClip> clips, ManLoco loco, Import3DReport rep)
        {
            PixelCharacterImporter.ResetController(ctrl);
            ctrl.AddParameter("Speed", AnimatorControllerParameterType.Float);
            ctrl.AddParameter("VelY", AnimatorControllerParameterType.Float);
            ctrl.AddParameter(new AnimatorControllerParameter { name = "Grounded", type = AnimatorControllerParameterType.Bool, defaultBool = true });
            ctrl.AddParameter("Attack", AnimatorControllerParameterType.Trigger);
            ctrl.AddParameter("Hurt", AnimatorControllerParameterType.Trigger);
            ctrl.AddParameter("Dead", AnimatorControllerParameterType.Bool);
            var sm = ctrl.layers[0].stateMachine;
            AnimationClip C(string n) => clips.TryGetValue(n, out var c) ? c : null;

            // locomotion blend tree on Speed (m/s): thresholds = the speeds the clips were authored for
            var locoState = ctrl.CreateBlendTreeInController("Locomotion", out BlendTree tree, 0);
            tree.blendType = BlendTreeType.Simple1D;
            tree.blendParameter = "Speed";
            tree.useAutomaticThresholds = false;
            if (C("Idle") != null) tree.AddChild(C("Idle"), 0f);
            if (C("Walk") != null) tree.AddChild(C("Walk"), loco.walkSpeed);
            if (C("Run") != null) tree.AddChild(C("Run"), loco.runSpeed);
            foreach (var p in ctrl.parameters.Where(p => p.name == "Blend").ToArray())   // auto-added by CreateBlendTreeInController
                ctrl.RemoveParameter(p);
            sm.defaultState = locoState;
            locoState.writeDefaultValues = true;

            AnimatorState S(string n, Vector3 pos)
            {
                var c = C(n); if (c == null) return null;
                var s = sm.AddState(n, pos); s.motion = c; return s;
            }
            var jStart = S("Jump_Start", new Vector3(500, 0, 0));
            var jAir = S("Jump_Air", new Vector3(750, 0, 0));
            var jLand = S("Jump_Land", new Vector3(750, 120, 0));
            var attack = S("Attack", new Vector3(500, 240, 0));
            var hurt = S("Hurt", new Vector3(750, 240, 0));
            var death = S("Death", new Vector3(1000, 240, 0));

            if (jStart != null)
            {
                var t = T(locoState, jStart, false, 0, 0.05f);
                t.AddCondition(AnimatorConditionMode.IfNot, 0, "Grounded"); t.AddCondition(AnimatorConditionMode.Greater, 0.1f, "VelY");
                if (jAir != null) T(jStart, jAir, true, 0.9f, 0.1f);
            }
            if (jAir != null)
            {
                var t = T(locoState, jAir, false, 0, 0.2f);   // walked off a ledge
                t.AddCondition(AnimatorConditionMode.IfNot, 0, "Grounded"); t.AddCondition(AnimatorConditionMode.Less, -0.5f, "VelY");
                var l = T(jAir, jLand ?? locoState, false, 0, 0.05f); l.AddCondition(AnimatorConditionMode.If, 0, "Grounded");
            }
            if (jLand != null) T(jLand, locoState, true, 0.7f, 0.15f);
            if (death != null)
            {
                var t = sm.AddAnyStateTransition(death); t.duration = 0.1f; t.hasFixedDuration = true; t.canTransitionToSelf = false;
                t.AddCondition(AnimatorConditionMode.If, 0, "Dead");
            }
            if (hurt != null)
            {
                var t = sm.AddAnyStateTransition(hurt); t.duration = 0.05f; t.hasFixedDuration = true; t.canTransitionToSelf = false;
                t.AddCondition(AnimatorConditionMode.If, 0, "Hurt"); t.AddCondition(AnimatorConditionMode.IfNot, 0, "Dead");
                T(hurt, locoState, true, 0.85f, 0.15f);
            }
            if (attack != null)
            {
                var t = sm.AddAnyStateTransition(attack); t.duration = 0.08f; t.hasFixedDuration = true; t.canTransitionToSelf = false;
                t.AddCondition(AnimatorConditionMode.If, 0, "Attack"); t.AddCondition(AnimatorConditionMode.IfNot, 0, "Dead");
                T(attack, locoState, true, 0.9f, 0.15f);
            }
            foreach (var n in clips.Keys.Where(n => !new[] { "Idle", "Walk", "Run", "Jump_Start", "Jump_Air", "Jump_Land", "Attack", "Hurt", "Death" }.Contains(n)))
                rep.warnings.Add("clip '" + n + "' is not wired into the controller");
        }
    }
}

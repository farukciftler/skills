// PixelCharacterImporter — uca-sheet/1 (sheet PNG + JSON) -> sliced sprites, AnimationClips,
// a platformer Animator Controller and a ready prefab. Idempotent: re-running keeps sprite IDs,
// clip and controller GUIDs, so scenes/prefabs referencing them never break.
//
// Call it (Unity 6.0+, Editor running with com.unity.pipeline):
//   unity command uca_pixel_import --sheet Assets/Characters/Ranger/Ranger_sheet.json
//   unity command eval "return UCA.Editor.PixelCharacterImporter.Run(\"Assets/Characters/Ranger/Ranger_sheet.json\");"
// Requires com.unity.2d.sprite (ISpriteEditorDataProvider). Without it the call returns an error, never corrupts.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.Animations;
using UnityEngine;
#if UCA_2DSPRITE
using UnityEditor.U2D.Sprites;
#endif

namespace UCA.Editor
{
    [Serializable] public class SheetFrame { public int x, y, w, h, durationMs; }
    [Serializable] public class SheetEvent { public int frame; public string function; }
    [Serializable] public class SheetAnim { public string name; public bool loop; public bool grounded; public SheetFrame[] frames; public SheetEvent[] events; }
    [Serializable] public class SheetVec2 { public float x, y; }
    [Serializable] public class SheetHints { public float runSpeed = 3.5f; public float apexBand = 1.2f; }
    [Serializable] public class SheetMeta
    {
        public string schema, name, image;
        public int frameWidth, frameHeight, baseline, ppu;
        public SheetVec2 pivot;
        public SheetAnim[] animations;
        public SheetHints stateHints;
    }

    [Serializable] public class ClipReport { public string name; public int frames; public float seconds; public bool loop; public string[] events; }
    [Serializable] public class ImportReport
    {
        public bool ok;
        public string character, texture, controller, prefab;
        public int sprites;
        public List<ClipReport> clips = new List<ClipReport>();
        public List<string> states = new List<string>();
        public List<string> warnings = new List<string>();
        public List<string> errors = new List<string>();
    }

    public static class PixelCharacterImporter
    {
        // canonical platformer state names -> the sheet's animation names
        static readonly string[] Locomotion = { "idle", "walk", "run" };
        static readonly string[] Air = { "jump_rise", "jump_apex", "fall" };

        public static string Run(string sheetJsonPath, string outputFolder = "", int ppuOverride = 0,
                                 bool makePrefab = true, bool addPhysics = true)
        {
            var rep = new ImportReport();
            try { Import(sheetJsonPath, outputFolder, ppuOverride, makePrefab, addPhysics, rep); }
            catch (Exception e) { rep.errors.Add(e.GetType().Name + ": " + e.Message); }
            rep.ok = rep.errors.Count == 0;
            return JsonUtility.ToJson(rep, true);
        }

        static void Import(string jsonPath, string outFolder, int ppuOverride, bool makePrefab, bool addPhysics, ImportReport rep)
        {
            jsonPath = jsonPath.Replace('\\', '/');
            if (!jsonPath.StartsWith("Assets/")) throw new ArgumentException("sheet path must be project-relative (Assets/...): " + jsonPath);
            var meta = JsonUtility.FromJson<SheetMeta>(File.ReadAllText(jsonPath));
            if (meta == null || meta.schema != "uca-sheet/1") throw new InvalidDataException("not a uca-sheet/1 file");
            if (meta.frameWidth % 2 != 0 || meta.frameHeight % 2 != 0) rep.warnings.Add("odd frame size: pivot lands on a half pixel");
            string dir = Path.GetDirectoryName(jsonPath).Replace('\\', '/');
            string texPath = dir + "/" + meta.image;
            if (string.IsNullOrEmpty(outFolder)) outFolder = dir + "/Animations";
            EnsureFolder(outFolder);
            int ppu = ppuOverride > 0 ? ppuOverride : (meta.ppu > 0 ? meta.ppu : 16);
            rep.character = meta.name; rep.texture = texPath;

            AssetDatabase.ImportAsset(texPath, ImportAssetOptions.ForceSynchronousImport);
            var importer = AssetImporter.GetAtPath(texPath) as TextureImporter;
            if (importer == null) throw new FileNotFoundException("texture not imported: " + texPath);
            int texW = meta.animations.SelectMany(a => a.frames).Max(f => f.x + f.w);
            int texH = meta.animations.SelectMany(a => a.frames).Max(f => f.y + f.h);

            // 1) pixel-art import settings (the #1 cause of blurry sprites is bilinear filtering)
            importer.textureType = TextureImporterType.Sprite;
            importer.spriteImportMode = SpriteImportMode.Multiple;
            importer.spritePixelsPerUnit = ppu;
            importer.filterMode = FilterMode.Point;
            importer.mipmapEnabled = false;
            importer.textureCompression = TextureImporterCompression.Uncompressed;
            importer.alphaIsTransparency = true;
            importer.wrapMode = TextureWrapMode.Clamp;
            importer.npotScale = TextureImporterNPOTScale.None;
            importer.maxTextureSize = Math.Min(16384, Mathf.NextPowerOfTwo(Math.Max(texW, texH)));
            var ts = new TextureImporterSettings();
            importer.ReadTextureSettings(ts);
            ts.spriteMeshType = SpriteMeshType.FullRect;
            ts.spriteGenerateFallbackPhysicsShape = false;
            importer.SetTextureSettings(ts);
            importer.SaveAndReimport();

            // 2) slicing through the Sprite Editor data provider (Safe Core Pattern: capability-checked)
            var spriteNames = new List<string>();
            foreach (var a in meta.animations)
                for (int i = 0; i < a.frames.Length; i++) spriteNames.Add(SpriteName(meta, a, i));
#if UCA_2DSPRITE
            var factory = new SpriteDataProviderFactories();
            factory.Init();
            var dp = factory.GetSpriteEditorDataProviderFromObject(importer);
            if (dp == null) throw new InvalidOperationException("importer has no sprite data provider");
            dp.InitSpriteEditorDataProvider();
            var capProvider = dp.GetDataProvider<ISpriteFrameEditCapability>();
            if (capProvider != null)
            {
                var cap = capProvider.GetEditCapability();
                foreach (var c in new[] { EEditCapability.CreateAndDeleteSprite, EEditCapability.EditSpriteRect,
                                          EEditCapability.EditPivot, EEditCapability.EditSpriteName })
                    if (!cap.HasCapability(c)) throw new InvalidOperationException("importer lacks capability " + c + " — aborted, nothing changed");
            }
            var existing = dp.GetSpriteRects().GroupBy(r => r.name).ToDictionary(g => g.Key, g => g.First().spriteID);
            var rects = new List<SpriteRect>();
            foreach (var a in meta.animations)
                for (int i = 0; i < a.frames.Length; i++)
                {
                    var f = a.frames[i];
                    string n = SpriteName(meta, a, i);
                    rects.Add(new SpriteRect
                    {
                        name = n,
                        rect = new Rect(f.x, texH - f.y - f.h, f.w, f.h),   // JSON is top-left origin, Unity bottom-left
                        alignment = SpriteAlignment.Custom,
                        pivot = new Vector2(meta.pivot.x, meta.pivot.y),
                        border = Vector4.zero,
                        spriteID = existing.TryGetValue(n, out var id) ? id : GUID.Generate()
                    });
                }
            dp.SetSpriteRects(rects.ToArray());
            var nameIds = dp.GetDataProvider<ISpriteNameFileIdDataProvider>();
            if (nameIds != null) nameIds.SetNameFileIdPairs(rects.Select(r => new SpriteNameFileIdPair(r.name, r.spriteID)).ToList());
            dp.Apply();
            importer.SaveAndReimport();
#else
            throw new InvalidOperationException("package com.unity.2d.sprite is missing — add it (unity-package-management skill) and rerun");
#endif
            var sprites = AssetDatabase.LoadAllAssetsAtPath(texPath).OfType<Sprite>().ToDictionary(s => s.name);
            var missing = spriteNames.Where(n => !sprites.ContainsKey(n)).ToList();
            if (missing.Count > 0) throw new InvalidOperationException("sprites not found after slicing: " + string.Join(",", missing.Take(5)));
            rep.sprites = spriteNames.Count;

            // 3) one AnimationClip per animation (variable per-frame timing, events, loop flag)
            var clips = new Dictionary<string, AnimationClip>();
            var binding = EditorCurveBinding.PPtrCurve("", typeof(SpriteRenderer), "m_Sprite");
            foreach (var a in meta.animations)
            {
                string clipPath = outFolder + "/" + meta.name + "_" + a.name + ".anim";
                var clip = AssetDatabase.LoadAssetAtPath<AnimationClip>(clipPath);
                bool isNew = clip == null;
                if (isNew) clip = new AnimationClip();
                else clip.ClearCurves();
                clip.frameRate = 60f; // keys use exact ms; frameRate only sets the editor grid
                var keys = new List<ObjectReferenceKeyframe>();
                var starts = new List<float>();
                float t = 0f;
                for (int i = 0; i < a.frames.Length; i++)
                {
                    starts.Add(t);
                    keys.Add(new ObjectReferenceKeyframe { time = t, value = sprites[SpriteName(meta, a, i)] });
                    t += Mathf.Max(1, a.frames[i].durationMs) / 1000f;
                }
                // closing key: holds the LAST frame for its full duration (otherwise it flashes for 0s)
                keys.Add(new ObjectReferenceKeyframe { time = t, value = sprites[SpriteName(meta, a, a.frames.Length - 1)] });
                AnimationUtility.SetObjectReferenceCurve(clip, binding, keys.ToArray());
                var st = AnimationUtility.GetAnimationClipSettings(clip);
                st.loopTime = a.loop;
                AnimationUtility.SetAnimationClipSettings(clip, st);
                var evs = (a.events ?? new SheetEvent[0])
                    .Where(e => e.frame >= 0 && e.frame < starts.Count && !string.IsNullOrEmpty(e.function))
                    .Select(e => new AnimationEvent { time = starts[e.frame], functionName = e.function }).ToArray();
                AnimationUtility.SetAnimationEvents(clip, evs);
                if (isNew) AssetDatabase.CreateAsset(clip, clipPath); else EditorUtility.SetDirty(clip);
                clips[a.name] = clip;
                rep.clips.Add(new ClipReport { name = a.name, frames = a.frames.Length, seconds = t, loop = a.loop,
                                               events = evs.Select(e => e.functionName + "@" + e.time.ToString("0.000")).ToArray() });
            }
            AssetDatabase.SaveAssets();

            // 4) platformer Animator Controller
            string ctrlPath = outFolder + "/" + meta.name + ".controller";
            var ctrl = AssetDatabase.LoadAssetAtPath<AnimatorController>(ctrlPath) ?? AnimatorController.CreateAnimatorControllerAtPath(ctrlPath);
            BuildPlatformerController(ctrl, clips, meta.stateHints ?? new SheetHints(), rep);
            EditorUtility.SetDirty(ctrl);
            AssetDatabase.SaveAssets();
            rep.controller = ctrlPath;

            // 5) prefab
            if (makePrefab)
            {
                string first = clips.ContainsKey("idle") ? "idle" : meta.animations[0].name;
                var firstAnim = meta.animations.First(a => a.name == first);
                var go = new GameObject(meta.name);
                try
                {
                    var sr = go.AddComponent<SpriteRenderer>();
                    sr.sprite = sprites[SpriteName(meta, firstAnim, 0)];
                    var anim = go.AddComponent<Animator>();
                    anim.runtimeAnimatorController = ctrl;
                    anim.cullingMode = AnimatorCullingMode.AlwaysAnimate;
                    if (addPhysics)
                    {
                        var rb = go.AddComponent<Rigidbody2D>();
                        rb.freezeRotation = true;
                        rb.interpolation = RigidbodyInterpolation2D.Interpolate;   // pixel-perfect jitter fix
                        rb.collisionDetectionMode = CollisionDetectionMode2D.Continuous;
                        var col = go.AddComponent<CapsuleCollider2D>();
                        var bb = OpaqueBounds(texPath, firstAnim.frames[0], texH);
                        // bbox in px relative to the cell's bottom-left -> units relative to the pivot
                        float px = meta.pivot.x * meta.frameWidth, py = meta.pivot.y * meta.frameHeight;
                        float w = Mathf.Max(2, bb.width * 0.7f), h = Mathf.Max(2, bb.height);
                        col.size = new Vector2(w, h) / ppu;
                        col.offset = new Vector2(bb.center.x - px, bb.yMin - py + h / 2f) / ppu;
                        go.AddComponent<UCA.PlatformerAnimatorDriver>();
                    }
                    string prefabPath = dir + "/" + meta.name + ".prefab";
                    PrefabUtility.SaveAsPrefabAsset(go, prefabPath);
                    rep.prefab = prefabPath;
                }
                finally { UnityEngine.Object.DestroyImmediate(go); }
            }
            AssetDatabase.SaveAssets();
        }

        static string SpriteName(SheetMeta m, SheetAnim a, int i) => m.name + "_" + a.name + "_" + i.ToString("D2");

        static Rect OpaqueBounds(string texPath, SheetFrame f, int texH)
        {
            var tex = new Texture2D(2, 2, TextureFormat.RGBA32, false);
            try
            {
                tex.LoadImage(File.ReadAllBytes(texPath));
                int x0 = int.MaxValue, y0 = int.MaxValue, x1 = -1, y1 = -1;
                int by = texH - f.y - f.h;
                for (int y = 0; y < f.h; y++)
                    for (int x = 0; x < f.w; x++)
                        if (tex.GetPixel(f.x + x, by + y).a > 0.5f)
                        { x0 = Math.Min(x0, x); x1 = Math.Max(x1, x); y0 = Math.Min(y0, y); y1 = Math.Max(y1, y); }
                return x1 < 0 ? new Rect(0, 0, f.w, f.h) : Rect.MinMaxRect(x0, y0, x1 + 1, y1 + 1);
            }
            finally { UnityEngine.Object.DestroyImmediate(tex); }
        }

        // ------------------------------------------------------------------ controller
        internal static void ResetController(AnimatorController ctrl)
        {
            while (ctrl.parameters.Length > 0) ctrl.RemoveParameter(0);
            if (ctrl.layers.Length == 0) ctrl.AddLayer("Base Layer");
            var sm = ctrl.layers[0].stateMachine;
            foreach (var t in sm.anyStateTransitions.ToArray()) sm.RemoveAnyStateTransition(t);
            foreach (var t in sm.entryTransitions.ToArray()) sm.RemoveEntryTransition(t);
            foreach (var s in sm.states.ToArray()) sm.RemoveState(s.state);
            foreach (var s in sm.stateMachines.ToArray()) sm.RemoveStateMachine(s.stateMachine);
        }

        static AnimatorStateTransition T(AnimatorState from, AnimatorState to, bool exit = false, float exitTime = 1f)
        {
            var t = from.AddTransition(to);
            Snap(t, exit, exitTime);
            return t;
        }

        static void Snap(AnimatorStateTransition t, bool exit, float exitTime)
        {
            t.hasExitTime = exit;
            t.exitTime = exitTime;
            t.hasFixedDuration = true;
            t.duration = 0f;       // pixel art never blends: a cross-fade of two sprites is a glitch
            t.offset = 0f;
            t.interruptionSource = TransitionInterruptionSource.None;
        }

        static void BuildPlatformerController(AnimatorController ctrl, Dictionary<string, AnimationClip> clips, SheetHints hints, ImportReport rep)
        {
            ResetController(ctrl);
            ctrl.AddParameter("Speed", AnimatorControllerParameterType.Float);
            ctrl.AddParameter("VelY", AnimatorControllerParameterType.Float);
            ctrl.AddParameter(new AnimatorControllerParameter { name = "Grounded", type = AnimatorControllerParameterType.Bool, defaultBool = true });
            ctrl.AddParameter("Attack", AnimatorControllerParameterType.Trigger);
            ctrl.AddParameter("Hurt", AnimatorControllerParameterType.Trigger);
            ctrl.AddParameter("Dead", AnimatorControllerParameterType.Bool);
            var sm = ctrl.layers[0].stateMachine;
            var S = new Dictionary<string, AnimatorState>();
            int col = 0;
            foreach (var kv in clips)
            {
                var st = sm.AddState(kv.Key, new Vector3(250 + (col % 4) * 220, 60 + (col / 4) * 90, 0));
                st.motion = kv.Value;
                st.writeDefaultValues = false;
                S[kv.Key] = st;
                col++;
            }
            AnimatorState Get(string n) => S.TryGetValue(n, out var s) ? s : null;
            var idle = Get("idle") ?? S.Values.First();
            sm.defaultState = idle;
            var walk = Get("walk"); var run = Get("run");
            var rise = Get("jump_rise"); var apex = Get("jump_apex"); var fall = Get("fall");
            var land = Get("land"); var attack = Get("attack"); var hurt = Get("hurt"); var death = Get("death");
            float runT = hints.runSpeed, apexB = hints.apexBand;

            // ground locomotion
            var ground = new[] { idle, walk, run }.Where(s => s != null).Distinct().ToList();
            if (walk != null && run != null)
            {
                T(idle, walk).AddCondition(AnimatorConditionMode.Greater, 0.1f, "Speed");
                T(walk, run).AddCondition(AnimatorConditionMode.Greater, runT, "Speed");
                var rw = T(run, walk); rw.AddCondition(AnimatorConditionMode.Less, runT, "Speed");
                T(walk, idle).AddCondition(AnimatorConditionMode.Less, 0.1f, "Speed");
                T(run, idle).AddCondition(AnimatorConditionMode.Less, 0.1f, "Speed");
            }
            else if (walk != null || run != null)
            {
                var mv = walk ?? run;
                T(idle, mv).AddCondition(AnimatorConditionMode.Greater, 0.1f, "Speed");
                T(mv, idle).AddCondition(AnimatorConditionMode.Less, 0.1f, "Speed");
            }
            // leave the ground
            var airEntry = rise ?? apex ?? fall;
            foreach (var g in ground)
            {
                if (rise != null)
                {
                    var t = T(g, rise); t.AddCondition(AnimatorConditionMode.IfNot, 0, "Grounded"); t.AddCondition(AnimatorConditionMode.Greater, 0.1f, "VelY");
                }
                if (fall != null)
                {
                    var t = T(g, fall); t.AddCondition(AnimatorConditionMode.IfNot, 0, "Grounded"); t.AddCondition(AnimatorConditionMode.Less, -0.1f, "VelY");
                }
                else if (airEntry != null && airEntry != rise)
                {
                    var t = T(g, airEntry); t.AddCondition(AnimatorConditionMode.IfNot, 0, "Grounded");
                }
            }
            // air phases
            if (rise != null && apex != null) T(rise, apex).AddCondition(AnimatorConditionMode.Less, apexB, "VelY");
            else if (rise != null && fall != null) T(rise, fall).AddCondition(AnimatorConditionMode.Less, 0f, "VelY");
            if (apex != null && fall != null) T(apex, fall).AddCondition(AnimatorConditionMode.Less, -apexB, "VelY");
            var landTarget = land ?? idle;
            foreach (var a in new[] { rise, apex, fall }.Where(s => s != null))
                T(a, landTarget).AddCondition(AnimatorConditionMode.If, 0, "Grounded");
            if (land != null)
            {
                T(land, idle, true, 1f);
                var mv = walk ?? run;
                if (mv != null) { var t = T(land, mv, true, 0.5f); t.AddCondition(AnimatorConditionMode.Greater, 0.1f, "Speed"); }
            }
            // actions from Any State — order = priority: death > hurt > attack
            if (death != null)
            {
                var t = sm.AddAnyStateTransition(death); Snap(t, false, 0); t.canTransitionToSelf = false;
                t.AddCondition(AnimatorConditionMode.If, 0, "Dead");
            }
            if (hurt != null)
            {
                var t = sm.AddAnyStateTransition(hurt); Snap(t, false, 0); t.canTransitionToSelf = false;
                t.AddCondition(AnimatorConditionMode.If, 0, "Hurt"); t.AddCondition(AnimatorConditionMode.IfNot, 0, "Dead");
                T(hurt, idle, true, 1f);
            }
            if (attack != null)
            {
                var t = sm.AddAnyStateTransition(attack); Snap(t, false, 0); t.canTransitionToSelf = false;
                t.AddCondition(AnimatorConditionMode.If, 0, "Attack"); t.AddCondition(AnimatorConditionMode.IfNot, 0, "Dead");
                T(attack, idle, true, 1f);
            }
            rep.states = S.Keys.ToList();
            var known = new HashSet<string>(Locomotion.Concat(Air).Concat(new[] { "land", "attack", "hurt", "death" }));
            foreach (var n in S.Keys.Where(n => !known.Contains(n)))
                rep.warnings.Add("state '" + n + "' has no automatic transitions — wire it by hand or via a trigger");
        }

        internal static void EnsureFolder(string path)
        {
            path = path.TrimEnd('/');
            if (AssetDatabase.IsValidFolder(path)) return;
            string parent = Path.GetDirectoryName(path).Replace('\\', '/');
            EnsureFolder(parent);
            AssetDatabase.CreateFolder(parent, Path.GetFileName(path));
        }
    }
}

// PixelCharacterImporter.cs
// Place under Assets/Editor/PixelCharacterPipeline/ (any Editor folder works).
// Requires: Unity 6.0+, com.unity.2d.sprite (ships with the 2D template).
//
// Turns a pixel-platformer manifest (gen_character.py / aseprite_to_manifest.py)
// into: pixel-correct texture import -> sliced sprites with stable IDs ->
// one AnimationClip per animation (per-frame durations, loop flags, events) ->
// a platformer Animator Controller -> a ready prefab.
//
// Entry points
//   Menu:   Tools > Pixel Character > Import Manifest...
//   Live Editor (Unity CLI eval):
//       PixelCharacterPipeline.PixelCharacterImporter.Import("Assets/Art/Hero/hero.manifest.json");
//   Batch:  unity run <project> -- -executeMethod PixelCharacterPipeline.PixelCharacterImporter.ImportFromCommandLine
//                                   -manifest Assets/Art/Hero/hero.manifest.json [-rebuildController] [-noPrefab]
//
// Re-running is safe: sprite IDs are reused by name, clips are updated in place,
// the controller and prefab are only created if missing (unless -rebuildController).

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using UnityEditor;
using UnityEditor.Animations;
using UnityEditor.U2D.Sprites;
using UnityEngine;

namespace PixelCharacterPipeline
{
    [Serializable] public class ManifestSprite { public string name; public int x, y, w, h; public float pivotX = 0.5f, pivotY = 0f; }
    [Serializable] public class ManifestFrame { public string sprite; public int durationMs = 100; }
    [Serializable] public class ManifestEvent { public int frame; public string function; public string stringParameter; public int intParameter; public float floatParameter; }
    [Serializable] public class ManifestAnim { public string name; public bool loop; public ManifestFrame[] frames; public ManifestEvent[] events; }
    [Serializable] public class ManifestCollider { public float w, h, offsetX, offsetY; }
    [Serializable]
    public class Manifest
    {
        public int schema;
        public string name, texture, facing;
        public int textureWidth, textureHeight, frameWidth, frameHeight, ppu;
        public ManifestCollider collider;
        public ManifestSprite[] sprites;
        public ManifestAnim[] animations;
    }

    public class ImportOptions
    {
        public bool rebuildController = false;   // rebuild graph in place (keeps the asset GUID)
        public bool createPrefab = true;         // only if the prefab does not exist yet
        public int clipFrameRate = 60;           // key times are quantized to 1/clipFrameRate
        public float apexBand = 1.0f;            // |VelocityY| below this counts as apex
        public string outputFolder = null;       // default: <manifest dir>/Animations
    }

    public static class PixelCharacterImporter
    {
        // Parameter names are the contract with PlatformerAnimationDriver.
        public const string P_Speed = "Speed", P_VelY = "VelocityY", P_Grounded = "Grounded",
            P_Wall = "WallSliding", P_Crouch = "Crouching", P_Dead = "Dead",
            P_Dash = "Dash", P_Attack = "Attack", P_Hurt = "Hurt";

        [MenuItem("Tools/Pixel Character/Import Manifest...")]
        static void ImportMenu()
        {
            var abs = EditorUtility.OpenFilePanel("Pixel character manifest", "Assets", "json");
            if (string.IsNullOrEmpty(abs)) return;
            var rel = FileUtil.GetProjectRelativePath(abs.Replace('\\', '/'));
            if (string.IsNullOrEmpty(rel)) { EditorUtility.DisplayDialog("Pixel Character", "Manifest must be inside this project's Assets folder.", "OK"); return; }
            Debug.Log(Import(rel));
        }

        public static void ImportFromCommandLine()
        {
            var args = Environment.GetCommandLineArgs();
            string manifest = null;
            var opt = new ImportOptions();
            for (int i = 0; i < args.Length; i++)
            {
                if (args[i] == "-manifest" && i + 1 < args.Length) manifest = args[i + 1];
                if (args[i] == "-rebuildController") opt.rebuildController = true;
                if (args[i] == "-noPrefab") opt.createPrefab = false;
            }
            try
            {
                if (manifest == null) throw new ArgumentException("missing -manifest Assets/.../x.manifest.json");
                Debug.Log(Import(manifest, opt));
            }
            catch (Exception e)
            {
                Debug.LogError("[PixelCharacter] " + e);
                if (Application.isBatchMode) EditorApplication.Exit(1);
            }
        }

        public static string Import(string manifestPath, ImportOptions opt = null)
        {
            if (opt == null) opt = new ImportOptions();
            var log = new StringBuilder();
            manifestPath = manifestPath.Replace('\\', '/');
            if (!manifestPath.StartsWith("Assets/")) throw new ArgumentException("manifestPath must start with Assets/: " + manifestPath);
            if (!File.Exists(manifestPath)) throw new FileNotFoundException(manifestPath);

            var m = JsonUtility.FromJson<Manifest>(File.ReadAllText(manifestPath));
            if (m == null || m.schema < 2 || m.sprites == null || m.animations == null)
                throw new InvalidDataException("Not a schema-2 pixel character manifest: " + manifestPath);

            var dir = Path.GetDirectoryName(manifestPath).Replace('\\', '/');
            var texPath = dir + "/" + m.texture;
            var outDir = opt.outputFolder ?? dir + "/Animations";
            EnsureFolder(outDir);

            AssetDatabase.ImportAsset(texPath, ImportAssetOptions.ForceUpdate);
            var ti = AssetImporter.GetAtPath(texPath) as TextureImporter;
            if (ti == null) throw new InvalidOperationException("No TextureImporter at " + texPath);

            ConfigureTexture(ti, m);
            log.AppendLine($"[PixelCharacter] {m.name}: texture configured (Point, uncompressed, PPU {m.ppu}, FullRect)");

            SliceSprites(ti, m);
            var sprites = AssetDatabase.LoadAllAssetsAtPath(texPath).OfType<Sprite>()
                .GroupBy(s => s.name).ToDictionary(g => g.Key, g => g.First());
            log.AppendLine($"  sliced {sprites.Count} sprites");

            var clips = new Dictionary<string, AnimationClip>();
            foreach (var a in m.animations)
            {
                clips[a.name] = BuildClip(a, m, sprites, outDir, opt.clipFrameRate, log);
            }
            log.AppendLine($"  {clips.Count} clips -> {outDir}");

            var ctrlPath = $"{outDir}/{m.name}.controller";
            var ctrl = AssetDatabase.LoadAssetAtPath<AnimatorController>(ctrlPath);
            if (ctrl == null)
            {
                ctrl = AnimatorController.CreateAnimatorControllerAtPath(ctrlPath);
                BuildGraph(ctrl, clips, opt, log);
                log.AppendLine("  controller created: " + ctrlPath);
            }
            else if (opt.rebuildController)
            {
                ClearController(ctrl);
                BuildGraph(ctrl, clips, opt, log);
                log.AppendLine("  controller rebuilt in place: " + ctrlPath);
            }
            else
            {
                log.AppendLine("  controller exists - kept your graph, clips were updated in place (use rebuildController to regenerate)");
            }

            if (opt.createPrefab) CreatePrefabIfMissing(m, dir, ctrl, sprites, log);

            AssetDatabase.SaveAssets();
            AssetDatabase.Refresh();
            return log.ToString();
        }

        /// <summary>
        /// Graph-only route for art imported by Unity's 2D Aseprite Importer (its own controller is read-only).
        /// Collects AnimationClips that are sub-assets of <paramref name="clipSourcePath"/> (an .aseprite file)
        /// or live in that folder, maps them to states by tag name (idle, run, jump, apex, fall, land, crouch,
        /// wall_slide, dash, attack, hurt, death - case-insensitive, spaces/dashes become underscores) and builds
        /// an editable platformer controller at <paramref name="controllerPath"/>.
        /// </summary>
        public static string BuildControllerFromClips(string clipSourcePath, string controllerPath, bool rebuild = false)
        {
            var log = new StringBuilder();
            IEnumerable<AnimationClip> found;
            if (AssetDatabase.IsValidFolder(clipSourcePath))
                found = AssetDatabase.FindAssets("t:AnimationClip", new[] { clipSourcePath })
                    .Select(g => AssetDatabase.LoadAssetAtPath<AnimationClip>(AssetDatabase.GUIDToAssetPath(g)));
            else
                found = AssetDatabase.LoadAllAssetsAtPath(clipSourcePath).OfType<AnimationClip>();
            var clips = new Dictionary<string, AnimationClip>();
            foreach (var c in found.Where(c => c != null && !c.name.StartsWith("__preview__")))
            {
                var key = c.name.Trim().ToLowerInvariant().Replace(' ', '_').Replace('-', '_');
                if (!clips.ContainsKey(key)) clips[key] = c;
            }
            if (clips.Count == 0) throw new InvalidOperationException("No AnimationClips found at " + clipSourcePath);
            var ctrl = AssetDatabase.LoadAssetAtPath<AnimatorController>(controllerPath);
            if (ctrl == null) ctrl = AnimatorController.CreateAnimatorControllerAtPath(controllerPath);
            else if (rebuild) ClearController(ctrl);
            else return "controller exists - pass rebuild=true to regenerate: " + controllerPath;
            BuildGraph(ctrl, clips, new ImportOptions(), log);
            AssetDatabase.SaveAssets();
            log.AppendLine($"[PixelCharacter] controller built from {clips.Count} clips: {string.Join(", ", clips.Keys)}");
            return log.ToString();
        }

        // ------------------------------------------------------------------ texture
        static void ConfigureTexture(TextureImporter ti, Manifest m)
        {
            ti.textureType = TextureImporterType.Sprite;
            ti.spriteImportMode = SpriteImportMode.Multiple;
            ti.spritePixelsPerUnit = m.ppu;
            ti.filterMode = FilterMode.Point;
            ti.textureCompression = TextureImporterCompression.Uncompressed;
            ti.mipmapEnabled = false;
            ti.alphaIsTransparency = true;
            ti.wrapMode = TextureWrapMode.Clamp;
            ti.npotScale = TextureImporterNPOTScale.None;
            int need = Mathf.NextPowerOfTwo(Mathf.Max(m.textureWidth, m.textureHeight));
            ti.maxTextureSize = Mathf.Max(ti.maxTextureSize, Mathf.Min(need, 16384)); // never let Unity downscale pixel art

            var s = new TextureImporterSettings();
            ti.ReadTextureSettings(s);
            s.spriteMeshType = SpriteMeshType.FullRect;       // tight meshes shimmer on pixel art and cost nothing to skip
            s.spriteExtrude = 0;
            s.spriteGenerateFallbackPhysicsShape = false;
            ti.SetTextureSettings(s);

            foreach (var platform in new[] { "Standalone", "Android", "iPhone", "WebGL" })
            {
                var ps = ti.GetPlatformTextureSettings(platform);
                if (!ps.overridden) continue;                 // respect non-overridden defaults
                ps.textureCompression = TextureImporterCompression.Uncompressed;
                ps.format = TextureImporterFormat.RGBA32;
                ps.maxTextureSize = Mathf.Max(ps.maxTextureSize, ti.maxTextureSize);
                ti.SetPlatformTextureSettings(ps);
            }
            ti.SaveAndReimport();
        }

        static void SliceSprites(TextureImporter ti, Manifest m)
        {
            var factory = new SpriteDataProviderFactories();
            factory.Init();
            var dp = factory.GetSpriteEditorDataProviderFromObject(ti);
            dp.InitSpriteEditorDataProvider();

            // Capability check is mandatory (Unity sprite-editor contract) - abort, never bypass.
            var capP = dp.GetDataProvider<ISpriteFrameEditCapability>();
            if (capP == null) throw new InvalidOperationException("Importer exposes no edit capability - aborted.");
            var cap = capP.GetEditCapability();
            if (!cap.HasCapability(EEditCapability.CreateAndDeleteSprite) ||
                !cap.HasCapability(EEditCapability.EditSpriteRect) ||
                !cap.HasCapability(EEditCapability.EditPivot))
                throw new InvalidOperationException("Importer does not allow creating sprites / editing rects+pivots - aborted.");

            var existing = dp.GetSpriteRects().GroupBy(r => r.name).ToDictionary(g => g.Key, g => g.First());
            var rects = new List<SpriteRect>();
            foreach (var s in m.sprites)
            {
                if (s.x < 0 || s.y < 0 || s.x + s.w > m.textureWidth || s.y + s.h > m.textureHeight)
                    throw new InvalidDataException($"sprite {s.name} rect is outside the texture");
                rects.Add(new SpriteRect
                {
                    name = s.name,
                    rect = new Rect(s.x, s.y, s.w, s.h),
                    alignment = SpriteAlignment.Custom,
                    pivot = new Vector2(s.pivotX, s.pivotY),
                    border = Vector4.zero,
                    // Reusing IDs keeps every clip/prefab reference alive when the art is regenerated.
                    spriteID = existing.TryGetValue(s.name, out var old) ? old.spriteID : GUID.Generate(),
                });
            }
            dp.SetSpriteRects(rects.ToArray());
            var nameIds = dp.GetDataProvider<ISpriteNameFileIdDataProvider>();
            nameIds?.SetNameFileIdPairs(rects.Select(r => new SpriteNameFileIdPair(r.name, r.spriteID)));
            dp.Apply();
            (dp.targetObject as AssetImporter)?.SaveAndReimport();
        }

        // ------------------------------------------------------------------ clips
        static AnimationClip BuildClip(ManifestAnim a, Manifest m, Dictionary<string, Sprite> sprites,
                                       string outDir, int fps, StringBuilder log)
        {
            var path = $"{outDir}/{m.name}_{a.name}.anim";
            var clip = AssetDatabase.LoadAssetAtPath<AnimationClip>(path);
            bool isNew = clip == null;
            if (isNew) clip = new AnimationClip();
            clip.frameRate = fps;

            var keys = new List<ObjectReferenceKeyframe>();
            var starts = new List<float>();
            float t = 0f, last = -1f;
            Sprite lastSprite = null;
            foreach (var f in a.frames)
            {
                if (!sprites.TryGetValue(f.sprite, out var sp))
                    throw new InvalidDataException($"{a.name}: sprite '{f.sprite}' not found after slicing");
                float q = Quantize(t, fps);
                if (q <= last) { q = last + 1f / fps; log.AppendLine($"  WARN {a.name}: frame shorter than 1/{fps}s was stretched"); }
                keys.Add(new ObjectReferenceKeyframe { time = q, value = sp });
                starts.Add(q);
                last = q;
                lastSprite = sp;
                t += Mathf.Max(1, f.durationMs) / 1000f;
            }
            // Closing key: without it the last frame gets zero screen time.
            float end = Mathf.Max(Quantize(t, fps), last + 1f / fps);
            keys.Add(new ObjectReferenceKeyframe { time = end, value = lastSprite });

            var binding = EditorCurveBinding.PPtrCurve("", typeof(SpriteRenderer), "m_Sprite");
            AnimationUtility.SetObjectReferenceCurve(clip, binding, keys.ToArray());

            var st = AnimationUtility.GetAnimationClipSettings(clip);
            st.loopTime = a.loop;
            AnimationUtility.SetAnimationClipSettings(clip, st);

            var evs = new List<AnimationEvent>();
            if (a.events != null)
                foreach (var e in a.events)
                {
                    if (e.frame < 0 || e.frame >= starts.Count || string.IsNullOrEmpty(e.function)) continue;
                    evs.Add(new AnimationEvent
                    {
                        functionName = e.function,
                        time = starts[e.frame],
                        stringParameter = e.stringParameter ?? "",
                        intParameter = e.intParameter,
                        floatParameter = e.floatParameter,
                    });
                }
            AnimationUtility.SetAnimationEvents(clip, evs.ToArray());

            if (isNew) AssetDatabase.CreateAsset(clip, path);
            else EditorUtility.SetDirty(clip);
            return clip;
        }

        static float Quantize(float t, int fps) => Mathf.Round(t * fps) / fps;

        // ------------------------------------------------------------------ controller
        static void ClearController(AnimatorController c)
        {
            var sm = c.layers[0].stateMachine;
            foreach (var t in sm.anyStateTransitions.ToArray()) sm.RemoveAnyStateTransition(t);
            foreach (var cs in sm.states.ToArray()) sm.RemoveState(cs.state);
            foreach (var p in c.parameters.ToArray()) c.RemoveParameter(p);
        }

        static void BuildGraph(AnimatorController c, Dictionary<string, AnimationClip> clips, ImportOptions opt, StringBuilder log)
        {
            c.AddParameter(P_Speed, AnimatorControllerParameterType.Float);
            c.AddParameter(P_VelY, AnimatorControllerParameterType.Float);
            c.AddParameter(P_Grounded, AnimatorControllerParameterType.Bool);
            c.AddParameter(P_Wall, AnimatorControllerParameterType.Bool);
            c.AddParameter(P_Crouch, AnimatorControllerParameterType.Bool);
            c.AddParameter(P_Dead, AnimatorControllerParameterType.Bool);
            c.AddParameter(P_Dash, AnimatorControllerParameterType.Trigger);
            c.AddParameter(P_Attack, AnimatorControllerParameterType.Trigger);
            c.AddParameter(P_Hurt, AnimatorControllerParameterType.Trigger);

            var sm = c.layers[0].stateMachine;
            var layout = new Dictionary<string, Vector2>
            {
                ["idle"] = new Vector2(300, 0), ["run"] = new Vector2(550, 0), ["crouch"] = new Vector2(300, -100),
                ["jump"] = new Vector2(300, 150), ["apex"] = new Vector2(550, 150), ["fall"] = new Vector2(800, 150),
                ["land"] = new Vector2(800, 0), ["wall_slide"] = new Vector2(1050, 150), ["dash"] = new Vector2(0, 250),
                ["attack"] = new Vector2(0, 350), ["hurt"] = new Vector2(0, 450), ["death"] = new Vector2(0, 550),
            };
            var st = new Dictionary<string, AnimatorState>();
            int extra = 0;
            foreach (var kv in clips)
            {
                var pos = layout.TryGetValue(kv.Key, out var p) ? p : new Vector2(1050, 300 + 80 * extra++);
                var s = sm.AddState(kv.Key, pos);
                s.motion = kv.Value;
                s.writeDefaultValues = false;
                st[kv.Key] = s;
            }
            var idle = Get(st, "idle") ?? st.Values.FirstOrDefault();
            if (idle == null) return;
            sm.defaultState = idle;

            var run = Get(st, "run"); var jump = Get(st, "jump"); var apex = Get(st, "apex"); var fall = Get(st, "fall");
            var land = Get(st, "land"); var crouch = Get(st, "crouch"); var wall = Get(st, "wall_slide");
            var dash = Get(st, "dash"); var attack = Get(st, "attack"); var hurt = Get(st, "hurt"); var death = Get(st, "death");

            // AnyState: order = priority. Death first so nothing can interrupt it.
            if (death != null) Any(sm, death).AddCondition(AnimatorConditionMode.If, 0, P_Dead);
            if (hurt != null) { var t = Any(sm, hurt); t.AddCondition(AnimatorConditionMode.If, 0, P_Hurt); t.AddCondition(AnimatorConditionMode.IfNot, 0, P_Dead); }
            if (dash != null) { var t = Any(sm, dash); t.AddCondition(AnimatorConditionMode.If, 0, P_Dash); t.AddCondition(AnimatorConditionMode.IfNot, 0, P_Dead); }
            if (attack != null) { var t = Any(sm, attack); t.AddCondition(AnimatorConditionMode.If, 0, P_Attack); t.AddCondition(AnimatorConditionMode.IfNot, 0, P_Dead); }

            var ground = new[] { idle, run, crouch, land }.Where(x => x != null).ToArray();
            var air = new[] { jump, apex, fall }.Where(x => x != null).ToArray();

            if (run != null)
            {
                T(idle, run).AddCondition(AnimatorConditionMode.Greater, 0.1f, P_Speed);
                T(run, idle).AddCondition(AnimatorConditionMode.Less, 0.1f, P_Speed);
            }
            if (crouch != null)
            {
                foreach (var g in new[] { idle, run }.Where(x => x != null))
                    T(g, crouch).AddCondition(AnimatorConditionMode.If, 0, P_Crouch);
                T(crouch, idle).AddCondition(AnimatorConditionMode.IfNot, 0, P_Crouch);
            }
            foreach (var g in ground)
            {
                if (jump != null)
                {
                    var tj = T(g, jump); tj.AddCondition(AnimatorConditionMode.IfNot, 0, P_Grounded);
                    tj.AddCondition(AnimatorConditionMode.Greater, 0.1f, P_VelY);
                }
                var airTarget = fall ?? apex ?? jump;
                if (airTarget != null)
                {
                    var tf = T(g, airTarget); tf.AddCondition(AnimatorConditionMode.IfNot, 0, P_Grounded);
                    if (jump != null) tf.AddCondition(AnimatorConditionMode.Less, -0.1f, P_VelY);
                }
            }
            if (jump != null && apex != null) T(jump, apex).AddCondition(AnimatorConditionMode.Less, opt.apexBand, P_VelY);
            if (apex != null && fall != null) T(apex, fall).AddCondition(AnimatorConditionMode.Less, -opt.apexBand, P_VelY);
            if (jump != null && apex == null && fall != null) T(jump, fall).AddCondition(AnimatorConditionMode.Less, 0f, P_VelY);

            foreach (var a in air)
            {
                T(a, land ?? idle).AddCondition(AnimatorConditionMode.If, 0, P_Grounded);
                if (wall != null) T(a, wall).AddCondition(AnimatorConditionMode.If, 0, P_Wall);
            }
            if (land != null)
            {
                if (run != null) { var tr = T(land, run); tr.AddCondition(AnimatorConditionMode.Greater, 0.1f, P_Speed); }
                T(land, idle, exitTime: true);
            }
            if (wall != null)
            {
                T(wall, land ?? idle).AddCondition(AnimatorConditionMode.If, 0, P_Grounded);
                var tw = T(wall, fall ?? idle); tw.AddCondition(AnimatorConditionMode.IfNot, 0, P_Wall);
                tw.AddCondition(AnimatorConditionMode.IfNot, 0, P_Grounded);
            }
            // One-shots return by exit time to ground or air.
            foreach (var one in new[] { dash, attack, hurt }.Where(x => x != null))
            {
                T(one, idle, exitTime: true).AddCondition(AnimatorConditionMode.If, 0, P_Grounded);
                if (fall != null) T(one, fall, exitTime: true).AddCondition(AnimatorConditionMode.IfNot, 0, P_Grounded);
            }
            var unknown = st.Keys.Except(layout.Keys).ToList();
            if (unknown.Count > 0)
                log.AppendLine("  NOTE states without auto-wiring (connect manually): " + string.Join(", ", unknown));
        }

        static AnimatorState Get(Dictionary<string, AnimatorState> st, string n)
        {
            AnimatorState s;
            return st.TryGetValue(n, out s) ? s : null;
        }

        // Pixel art: snap, never blend. Zero-duration, fixed-time transitions.
        static AnimatorStateTransition T(AnimatorState from, AnimatorState to, bool exitTime = false)
        {
            var t = from.AddTransition(to);
            t.hasExitTime = exitTime;
            t.exitTime = exitTime ? 1f : 0f;
            t.duration = 0f;
            t.hasFixedDuration = true;
            t.offset = 0f;
            return t;
        }

        static AnimatorStateTransition Any(AnimatorStateMachine sm, AnimatorState to)
        {
            var t = sm.AddAnyStateTransition(to);
            t.hasExitTime = false;
            t.duration = 0f;
            t.hasFixedDuration = true;
            t.canTransitionToSelf = false;
            return t;
        }

        // ------------------------------------------------------------------ prefab
        static void CreatePrefabIfMissing(Manifest m, string dir, AnimatorController ctrl,
                                          Dictionary<string, Sprite> sprites, StringBuilder log)
        {
            var prefabPath = $"{dir}/{m.name}.prefab";
            if (AssetDatabase.LoadAssetAtPath<GameObject>(prefabPath) != null)
            {
                log.AppendLine("  prefab exists - left untouched: " + prefabPath);
                return;
            }
            var firstSprite = m.animations.SelectMany(a => a.frames).Select(f => f.sprite)
                .Where(sprites.ContainsKey).Select(n => sprites[n]).FirstOrDefault();

            var go = new GameObject(m.name);
            try
            {
                var sr = go.AddComponent<SpriteRenderer>();
                sr.sprite = firstSprite;
                var anim = go.AddComponent<Animator>();
                anim.runtimeAnimatorController = ctrl;
                var rb = go.AddComponent<Rigidbody2D>();
                rb.freezeRotation = true;
                rb.interpolation = RigidbodyInterpolation2D.Interpolate;
                rb.collisionDetectionMode = CollisionDetectionMode2D.Continuous;
                var col = go.AddComponent<CapsuleCollider2D>();
                col.direction = CapsuleDirection2D.Vertical;
                var c = m.collider;
                if (c != null && c.w > 0 && c.h > 0)
                {
                    col.size = new Vector2(c.w, c.h);
                    col.offset = new Vector2(c.offsetX, c.offsetY);
                }
                var matPath = $"{dir}/{m.name}_NoFriction.physicsMaterial2D";
                var mat = AssetDatabase.LoadAssetAtPath<PhysicsMaterial2D>(matPath);
                if (mat == null)
                {
                    mat = new PhysicsMaterial2D(m.name + "_NoFriction") { friction = 0f, bounciness = 0f };
                    AssetDatabase.CreateAsset(mat, matPath);   // zero friction: no sticking to walls mid-jump
                }
                col.sharedMaterial = mat;
                go.AddComponent<PlatformerAnimationDriver>();
                PrefabUtility.SaveAsPrefabAsset(go, prefabPath);
                log.AppendLine("  prefab created: " + prefabPath);
            }
            finally
            {
                UnityEngine.Object.DestroyImmediate(go);
            }
        }

        static void EnsureFolder(string path)
        {
            if (AssetDatabase.IsValidFolder(path)) return;
            var parent = Path.GetDirectoryName(path).Replace('\\', '/');
            EnsureFolder(parent);
            AssetDatabase.CreateFolder(parent, Path.GetFileName(path));
        }
    }
}

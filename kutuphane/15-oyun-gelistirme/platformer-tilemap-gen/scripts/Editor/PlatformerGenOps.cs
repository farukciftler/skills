using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Tilemaps;
using PlatformerGen.Integration;

namespace PlatformerGen.EditorTools
{
    /// <summary>
    /// Shared Editor operations. Menu items and the Unity CLI [CliCommand]s both call these, so a
    /// human clicking and Claude driving `unity command pgen_*` get identical, Undo-able results.
    /// Every op returns a JSON string (ReportDto / status) that Claude can parse.
    /// </summary>
    public static class PlatformerGenOps
    {
        public const string DefaultFolder = "Assets/PlatformerGen/Generated";

        public static LevelLayers EnsureLevelGrid()
        {
            var layers = Object.FindAnyObjectByType<LevelLayers>();
            if (layers != null) { LevelLayers.EnsureOn(layers.GetComponent<Grid>(), go => Undo.RegisterCreatedObjectUndo(go, "PlatformerGen setup")); return layers; }
            var gridGo = new GameObject("Level Grid", typeof(Grid));
            Undo.RegisterCreatedObjectUndo(gridGo, "PlatformerGen setup");
            layers = LevelLayers.EnsureOn(gridGo.GetComponent<Grid>(), go => Undo.RegisterCreatedObjectUndo(go, "PlatformerGen setup"));
            EditorSceneManager.MarkSceneDirty(gridGo.scene);
            return layers;
        }

        public static string Generate(LevelGenConfig config, int seed, bool write = true)
        {
            if (config == null) return Error("No LevelGenConfig given.");
            if (config.legend == null) return Error("Config '" + config.name + "' has no TileLegend.");
            var missing = config.legend.MissingAssignments();
            if (write && missing.Count > 0) return Error("TileLegend incomplete: " + string.Join("; ", missing.ToArray()));

            GenerationResult res;
            try { res = config.Run(seed); }
            catch (System.Exception e) { return Error("Generation threw: " + e.Message); }

            WriteStats ws = null;
            if (write)
            {
                var layers = EnsureLevelGrid();
                var objs = new List<Object>();
                foreach (var tm in layers.All()) if (tm != null) { objs.Add(tm); var c = tm.GetComponent<CompositeCollider2D>(); if (c != null) objs.Add(c); }
                Undo.RegisterCompleteObjectUndo(objs.ToArray(), "PlatformerGen generate");
                ws = TilemapLevelWriter.Write(res.Grid, layers, config.legend, Vector3Int.zero, new WriteOptions
                {
                    instantiate = (prefab, parent) =>
                    {
                        var go = (GameObject)PrefabUtility.InstantiatePrefab(prefab, parent);
                        Undo.RegisterCreatedObjectUndo(go, "PlatformerGen entity");
                        return go;
                    },
                    destroy = go => Undo.DestroyObjectImmediate(go)
                });
                EditorSceneManager.MarkSceneDirty(layers.gameObject.scene);
            }
            return JsonUtility.ToJson(config.ToDto(res, ws), true);
        }

        /// <summary>Validate whatever is painted in the scene right now (hand-made or generated).</summary>
        public static string ValidateScene(LevelGenConfig config)
        {
            var layers = Object.FindAnyObjectByType<LevelLayers>();
            if (layers == null) return Error("No LevelLayers in the open scene. Run setup first (or add LevelLayers to your Grid and assign its Tilemaps).");
            if (config == null) return Error("Validation needs a LevelGenConfig for the movement profile.");
            Vector3Int origin;
            var legend = config.legend != null ? config.legend : ScriptableObject.CreateInstance<TileLegend>();
            var grid = TilemapLevelReader.Read(layers, legend, out origin);
            var res = new GenerationResult { Grid = grid, Seed = -1, Attempts = 0, Generator = "scene" };
            var dto = config.ToDto(res);
            dto.problems.Insert(0, "Scene origin cell = " + origin + " (ASCII (0,0) = bottom-left)");
            return JsonUtility.ToJson(dto, true);
        }

        public static string SceneAscii(LevelGenConfig config)
        {
            var layers = Object.FindAnyObjectByType<LevelLayers>();
            if (layers == null) return Error("No LevelLayers in scene.");
            Vector3Int origin;
            var legend = config != null && config.legend != null ? config.legend : ScriptableObject.CreateInstance<TileLegend>();
            return AsciiLevel.Render(TilemapLevelReader.Read(layers, legend, out origin));
        }

        /// <summary>Create legend + config + template TextAssets in the project so a fresh project works in one step.</summary>
        public static string CreateDefaultAssets(string skillAssetsDir = null)
        {
            Directory.CreateDirectory(DefaultFolder);
            string legendPath = DefaultFolder + "/TileLegend.asset";
            var legend = AssetDatabase.LoadAssetAtPath<TileLegend>(legendPath);
            if (legend == null) { legend = ScriptableObject.CreateInstance<TileLegend>(); AssetDatabase.CreateAsset(legend, legendPath); }

            var created = new List<string> { legendPath };
            foreach (var pair in new[] { new[] { "room-templates.txt", "RoomGrid" }, new[] { "chunk-templates.txt", "ChunkStitch" } })
            {
                string txtPath = DefaultFolder + "/" + pair[0];
                if (!File.Exists(txtPath) && skillAssetsDir != null && File.Exists(Path.Combine(skillAssetsDir, pair[0])))
                    File.Copy(Path.Combine(skillAssetsDir, pair[0]), txtPath);
                if (!File.Exists(txtPath)) { created.Add("(missing " + txtPath + " - copy it from the skill's assets/ folder)"); continue; }
                AssetDatabase.ImportAsset(txtPath);
                string cfgPath = DefaultFolder + "/Config_" + pair[1] + ".asset";
                if (AssetDatabase.LoadAssetAtPath<LevelGenConfig>(cfgPath) == null)
                {
                    var cfg = ScriptableObject.CreateInstance<LevelGenConfig>();
                    cfg.algorithm = pair[1] == "RoomGrid" ? GenAlgorithm.RoomGrid : GenAlgorithm.ChunkStitch;
                    cfg.legend = legend;
                    cfg.templates = AssetDatabase.LoadAssetAtPath<TextAsset>(txtPath);
                    AssetDatabase.CreateAsset(cfg, cfgPath);
                }
                created.Add(cfgPath);
            }
            AssetDatabase.SaveAssets();
            return "{\"created\":[\"" + string.Join("\",\"", created.ToArray()) + "\"],\"next\":\"Assign tiles in TileLegend (Solid -> RuleTile/AutoTile, OneWay, Hazard, Ladder), then generate.\"}";
        }

        public static string Error(string msg)
        {
            return "{\"error\":\"" + msg.Replace("\\", "\\\\").Replace("\"", "\\\"") + "\"}";
        }
    }

    public static class PlatformerGenMenu
    {
        [MenuItem("Tools/PlatformerGen/Setup Level Grid In Scene")]
        private static void Setup() { Selection.activeObject = PlatformerGenOps.EnsureLevelGrid().gameObject; }

        [MenuItem("Tools/PlatformerGen/Create Default Assets")]
        private static void Defaults() { Debug.Log(PlatformerGenOps.CreateDefaultAssets()); }

        [MenuItem("Tools/PlatformerGen/Generate From Selected Config")]
        private static void Generate()
        {
            var cfg = Selection.activeObject as LevelGenConfig;
            Debug.Log("[PlatformerGen]\n" + PlatformerGenOps.Generate(cfg, cfg != null ? cfg.seed : 0));
        }

        [MenuItem("Tools/PlatformerGen/Generate From Selected Config (Next Seed)")]
        private static void GenerateNext()
        {
            var cfg = Selection.activeObject as LevelGenConfig;
            if (cfg == null) { Debug.LogWarning("Select a LevelGenConfig asset first."); return; }
            Undo.RecordObject(cfg, "seed++"); cfg.seed++; EditorUtility.SetDirty(cfg);
            Debug.Log("[PlatformerGen]\n" + PlatformerGenOps.Generate(cfg, cfg.seed));
        }

        [MenuItem("Tools/PlatformerGen/Validate Scene Level (Selected Config)")]
        private static void Validate() { Debug.Log("[PlatformerGen]\n" + PlatformerGenOps.ValidateScene(Selection.activeObject as LevelGenConfig)); }

        [MenuItem("Tools/PlatformerGen/Copy Scene Level As ASCII")]
        private static void Ascii()
        {
            string a = PlatformerGenOps.SceneAscii(Selection.activeObject as LevelGenConfig);
            EditorGUIUtility.systemCopyBuffer = a;
            Debug.Log(a);
        }
    }
}

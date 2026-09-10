// Compiled ONLY when com.unity.pipeline is installed (asmdef versionDefines -> PLATFORMERGEN_PIPELINE +
// defineConstraints). Without the package this assembly is skipped, so the rest never breaks.
//
// Warm Editor:   unity command pgen_generate --config Assets/PlatformerGen/Generated/Config_RoomGrid.asset --seed 7
// One-shot/CI:   unity run <project> --command pgen_generate --format ndjson -- --config <path> --seed 7
// After adding/changing this file:  unity command recompile  -> poll recompile_status -> unity list
using Unity.Pipeline.Commands;
using UnityEditor;
using PlatformerGen.Integration;

namespace PlatformerGen.EditorTools
{
    // All arguments are strings on purpose: the safest type for CLI transport; parsed here.
    public static class PlatformerGenCommands
    {
        private static int ParseInt(string s, int def) { int v; return int.TryParse(s, out v) ? v : def; }

        [CliCommand("pgen_setup", "Create/repair the PlatformerGen Level Grid (Ground/OneWay/Hazard/Ladder/Decor tilemaps + colliders) in the active scene")]
        public static string Setup()
        {
            var l = PlatformerGenOps.EnsureLevelGrid();
            return "{\"grid\":\"" + l.gameObject.name + "\"}";
        }

        [CliCommand("pgen_defaults", "Create TileLegend + LevelGenConfig assets under Assets/PlatformerGen/Generated")]
        public static string Defaults([CliArg("templates_dir", "Folder containing room-templates.txt / chunk-templates.txt to copy in")] string templatesDir = "")
        {
            return PlatformerGenOps.CreateDefaultAssets(string.IsNullOrEmpty(templatesDir) ? null : templatesDir);
        }

        [CliCommand("pgen_generate", "Generate + validate a level from a LevelGenConfig and write it into the scene. Returns a JSON report with an ASCII overlay")]
        public static string Generate(
            [CliArg("config", "Asset path of a LevelGenConfig")] string config,
            [CliArg("seed", "Seed; empty or -1 = use the config's seed")] string seed = "",
            [CliArg("dry_run", "true = generate+validate only, don't touch the scene")] string dryRun = "false")
        {
            var cfg = AssetDatabase.LoadAssetAtPath<LevelGenConfig>(config);
            if (cfg == null) return PlatformerGenOps.Error("No LevelGenConfig at '" + config + "'");
            int s = ParseInt(seed, -1);
            bool dry = dryRun == "true" || dryRun == "1";
            return PlatformerGenOps.Generate(cfg, s >= 0 ? s : cfg.seed, !dry);
        }

        [CliCommand("pgen_validate", "Validate the level currently in the scene (hand-painted or generated) against a config's movement profile")]
        public static string Validate([CliArg("config", "Asset path of a LevelGenConfig (for the movement profile)")] string config)
        {
            return PlatformerGenOps.ValidateScene(AssetDatabase.LoadAssetAtPath<LevelGenConfig>(config));
        }

        [CliCommand("pgen_ascii", "Dump the scene's level as ASCII (top row first; # solid, = one-way, ^ hazard, H ladder, S/E markers)")]
        public static string Ascii([CliArg("config", "Optional LevelGenConfig asset path (for its legend)")] string config = "")
        {
            var cfg = string.IsNullOrEmpty(config) ? null : AssetDatabase.LoadAssetAtPath<LevelGenConfig>(config);
            return PlatformerGenOps.SceneAscii(cfg);
        }

        [CliCommand("pgen_sweep", "Generate N seeds without touching the scene; report pass rate, attempts and timing (tuning aid)")]
        public static string Sweep(
            [CliArg("config", "Asset path of a LevelGenConfig")] string config,
            [CliArg("count", "Number of seeds (default 50)")] string countArg = "50")
        {
            int count = System.Math.Max(1, ParseInt(countArg, 50));
            var cfg = AssetDatabase.LoadAssetAtPath<LevelGenConfig>(config);
            if (cfg == null) return PlatformerGenOps.Error("No LevelGenConfig at '" + config + "'");
            int passed = 0, attempts = 0; double ms = 0;
            for (int s = 0; s < count; s++)
            {
                var r = cfg.Run(s);
                if (r.Report.Passed) passed++;
                attempts += r.Attempts; ms += r.Milliseconds;
            }
            double first = GenerationPipeline.FirstTryPassRate(cfg.CreateGenerator(), cfg.CreateProfile(), count, cfg.CreateValidatorOptions());
            return string.Format(System.Globalization.CultureInfo.InvariantCulture,
                "{{\"count\":{0},\"passed\":{1},\"firstTryPassRate\":{2:0.###},\"avgAttempts\":{3:0.##},\"avgMs\":{4:0.#}}}",
                count, passed, first, (double)attempts / count, ms / count);
        }
    }
}

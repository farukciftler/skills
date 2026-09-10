using UnityEngine;

namespace PlatformerGen.Integration
{
    /// <summary>
    /// Runtime (per-run) procedural levels: roguelites, daily seeds, replayable runs.
    /// For hand-tuned levels prefer baking in the Editor (Tools > PlatformerGen) and shipping the scene.
    /// </summary>
    public sealed class RuntimeLevelBuilder : MonoBehaviour
    {
        public LevelGenConfig config;
        public LevelLayers layers;
        public bool buildOnStart = true;
        [Tooltip("-1 = use config.seed. Set from your run/seed system (daily seed, shared seed codes...).")]
        public int seedOverride = -1;
        public Transform player;

        public GenerationResult LastResult { get; private set; }
        public WriteStats LastWrite { get; private set; }

        private void Start() { if (buildOnStart) Build(); }

        public void Build() { Build(seedOverride >= 0 ? seedOverride : config.seed); }

        public void Build(int seed)
        {
            if (config == null || layers == null) { Debug.LogError("[PlatformerGen] RuntimeLevelBuilder needs config + layers", this); return; }
            LastResult = config.Run(seed);
            if (!LastResult.Report.Passed)
                Debug.LogWarning("[PlatformerGen] Level failed validation, building anyway: " + LastResult.Report, this);
            LastWrite = TilemapLevelWriter.Write(LastResult.Grid, layers, config.legend, Vector3Int.zero);
            if (player != null && LastWrite.hasSpawn)
            {
                player.position = LastWrite.spawnWorld;
                var rb = player.GetComponent<Rigidbody2D>();
                if (rb != null) rb.linearVelocity = Vector2.zero;
            }
        }
    }
}

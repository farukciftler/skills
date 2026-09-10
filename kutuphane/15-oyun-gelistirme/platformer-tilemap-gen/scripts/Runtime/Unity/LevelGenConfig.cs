using System;
using System.Collections.Generic;
using UnityEngine;

namespace PlatformerGen.Integration
{
    public enum GenAlgorithm { RoomGrid, ChunkStitch, Heightmap, Cave, AsciiLevel }

    [Serializable]
    public sealed class ReportDto
    {
        public bool passed;
        public string generator;
        public int seed;
        public int attempts;
        public double milliseconds;
        public int width, height;
        public bool exitReachable;
        public double coverage;
        public int pickupsTotal, pickupsReachable;
        public int pathLength, jumpsOnPath, fallsOnPath;
        public int tilesWritten, entitiesSpawned;
        public string profile;
        public List<string> problems = new List<string>();
        public string ascii;   // debug overlay: '*' path, '+' reachable
    }

    /// <summary>
    /// One asset = one reproducible level recipe (algorithm + movement profile + templates + seed).
    /// Keep the movement numbers in sync with the player controller — this is the level/controller contract.
    /// </summary>
    [CreateAssetMenu(menuName = "PlatformerGen/Level Gen Config", fileName = "LevelGenConfig")]
    public sealed class LevelGenConfig : ScriptableObject
    {
        [Header("Algorithm")]
        public GenAlgorithm algorithm = GenAlgorithm.RoomGrid;
        public int seed = 12345;
        [Tooltip("Room templates (@room) or chunk templates (@chunk), or a full ASCII level for AsciiLevel.")]
        public TextAsset templates;
        public TileLegend legend;

        [Header("Movement profile (in TILES) — must match the player controller")]
        public float jumpHeightTiles = 3.2f;
        public float timeToApex = 0.4f;
        public float runSpeedTilesPerSec = 8f;
        [Min(1)] public int bodyHeightTiles = 1;
        [Min(0.1f)] public float fallGravityMultiplier = 1.6f;
        [Tooltip("0 = no fall damage")] public int maxSafeFallTiles = 0;
        public bool canClimbLadders = true;
        public bool canDropThroughOneWay = true;

        [Header("Validation")]
        [Range(0.5f, 1f)] public float safetyMargin = 0.85f;
        public bool bottomIsPit = true;
        [Min(1)] public int maxAttempts = 50;

        [Header("RoomGrid")]
        public int roomsX = 4, roomsY = 4, roomW = 10, roomH = 8;

        [Header("ChunkStitch / Heightmap / Cave size")]
        public int width = 160;
        public int height = 24;
        public float difficultyStart = 1, difficultyEnd = 5;
        [Range(0, 1)] public float beatChance = 0.35f;

        [Header("Population (placed on reachable spots after validation)")]
        public int pickups = 0;
        public int enemies = 0;

        public MovementProfile CreateProfile()
        {
            var p = MovementProfile.FromApex(jumpHeightTiles, timeToApex, runSpeedTilesPerSec, bodyHeightTiles, fallGravityMultiplier);
            p.MaxSafeFall = maxSafeFallTiles > 0 ? maxSafeFallTiles : int.MaxValue;
            p.CanClimbLadders = canClimbLadders;
            p.CanDropThroughOneWay = canDropThroughOneWay;
            return p;
        }

        public ValidatorOptions CreateValidatorOptions()
        {
            // RoomGrid and Cave are closed boxes; linear levels usually have bottomless pits.
            bool pit = bottomIsPit && (algorithm == GenAlgorithm.ChunkStitch || algorithm == GenAlgorithm.Heightmap || algorithm == GenAlgorithm.AsciiLevel);
            return new ValidatorOptions { SafetyMargin = safetyMargin, BottomIsPit = pit };
        }

        public IGridGenerator CreateGenerator()
        {
            var profile = CreateProfile();
            string text = templates != null ? templates.text : null;
            switch (algorithm)
            {
                case GenAlgorithm.RoomGrid:
                    if (text == null) throw new InvalidOperationException("RoomGrid needs a templates TextAsset with @room blocks.");
                    var rg = RoomGridGenerator.FromText(text, roomW, roomH);
                    rg.RoomsX = roomsX; rg.RoomsY = roomsY; rg.BodyHeight = bodyHeightTiles;
                    return rg;
                case GenAlgorithm.ChunkStitch:
                    var cs = new ChunkStitchGenerator(profile, text != null ? ChunkTemplate.FromText(text, bodyHeightTiles) : null);
                    cs.TargetWidth = width; cs.Height = height;
                    cs.MaxGround = Math.Max(cs.MinGround + 1, height - bodyHeightTiles - Mathf.CeilToInt(jumpHeightTiles) - 2);
                    cs.StartGround = Math.Min(cs.StartGround, cs.MaxGround);
                    cs.DifficultyStart = difficultyStart; cs.DifficultyEnd = difficultyEnd; cs.BeatChance = beatChance;
                    return cs;
                case GenAlgorithm.Heightmap:
                    var hm = new HeightmapGenerator(profile) { Width = width, Height = height };
                    hm.MaxGround = Math.Max(hm.MinGround + 1, height - bodyHeightTiles - Mathf.CeilToInt(jumpHeightTiles) - 3);
                    return hm;
                case GenAlgorithm.Cave:
                    return new CaveGenerator(profile) { Width = width, Height = height, ValidatorOptions = CreateValidatorOptions() };
                case GenAlgorithm.AsciiLevel:
                    if (text == null) throw new InvalidOperationException("AsciiLevel needs a TextAsset containing the level.");
                    return new FixedAsciiGenerator(text);
            }
            throw new ArgumentOutOfRangeException();
        }

        /// <summary>Generate + validate (+ populate). Pure data — no scene changes. Deterministic in (config, seed).</summary>
        public GenerationResult Run(int seedValue)
        {
            var profile = CreateProfile();
            var vopts = CreateValidatorOptions();
            var gen = CreateGenerator();
            var res = GenerationPipeline.Run(gen, seedValue, profile, vopts, algorithm == GenAlgorithm.AsciiLevel ? 1 : maxAttempts);
            if (res.Report.Passed && (pickups > 0 || enemies > 0))
            {
                var v = new ReachabilityValidator(profile, vopts);
                v.Validate(res.Grid);
                var rng = new Rng(seedValue).Derive(4242);
                GridPasses.Scatter(res.Grid, Cell.Pickup, pickups, rng, bodyHeightTiles, 4, v.WasReachable);
                GridPasses.Scatter(res.Grid, Cell.Enemy, enemies, rng.Derive(1), bodyHeightTiles, 8, v.WasReachable);
                res.Report = v.Validate(res.Grid);
            }
            return res;
        }

        public ReportDto ToDto(GenerationResult res, WriteStats ws = null)
        {
            var v = new ReachabilityValidator(CreateProfile(), CreateValidatorOptions());
            var rep = v.Validate(res.Grid);
            var dto = new ReportDto
            {
                passed = rep.Passed, generator = res.Generator, seed = res.Seed, attempts = res.Attempts,
                milliseconds = res.Milliseconds, width = res.Grid.Width, height = res.Grid.Height,
                exitReachable = rep.ExitReachable, coverage = rep.Coverage,
                pickupsTotal = rep.PickupsTotal, pickupsReachable = rep.PickupsReachable,
                pathLength = rep.PathLength, jumpsOnPath = rep.JumpsOnPath, fallsOnPath = rep.FallsOnPath,
                profile = rep.Profile, problems = new List<string>(rep.Problems),
                ascii = v.RenderOverlay(res.Grid, rep)
            };
            if (ws != null) { dto.tilesWritten = ws.tilesWritten; dto.entitiesSpawned = ws.entitiesSpawned; dto.problems.AddRange(ws.warnings); }
            return dto;
        }
    }
}

using System;
using System.Collections.Generic;

namespace PlatformerGen
{
    public interface IGridGenerator
    {
        string Name { get; }
        /// <summary>Must be a pure function of rng: same seed in => same grid out.</summary>
        TileGrid Generate(Rng rng);
    }

    [Serializable]
    public sealed class GenerationResult
    {
        public TileGrid Grid;
        public ValidationReport Report;
        public int Seed;
        public int Attempts;
        public int AcceptedAttemptSeed;   // derived seed of the attempt that passed (replay with this)
        public string Generator;
        public double Milliseconds;
    }

    /// <summary>
    /// Generate -> post-process -> validate -> retry with a derived seed. Deterministic:
    /// the same (seed, generator config, profile) always yields the same accepted level,
    /// because retries use rng.Derive(attempt) rather than wall-clock randomness.
    /// </summary>
    public static class GenerationPipeline
    {
        public static GenerationResult Run(IGridGenerator gen, int seed, MovementProfile profile,
                                           ValidatorOptions vopts = null, int maxAttempts = 50,
                                           Action<TileGrid, Rng> postProcess = null)
        {
            var sw = System.Diagnostics.Stopwatch.StartNew();
            var root = new Rng(seed);
            var validator = new ReachabilityValidator(profile, vopts);
            GenerationResult last = null;
            for (int attempt = 0; attempt < maxAttempts; attempt++)
            {
                var rng = root.Derive(attempt);
                TileGrid grid = gen.Generate(rng);
                if (postProcess != null) postProcess(grid, rng.Derive(9001));
                var rep = validator.Validate(grid);
                last = new GenerationResult
                {
                    Grid = grid, Report = rep, Seed = seed, Attempts = attempt + 1,
                    AcceptedAttemptSeed = (int)(rng.Seed & 0x7FFFFFFF), Generator = gen.Name
                };
                if (rep.Passed) break;
            }
            sw.Stop();
            last.Milliseconds = sw.Elapsed.TotalMilliseconds;
            if (!last.Report.Passed)
                last.Report.Problems.Add("Gave up after " + maxAttempts + " attempts — generator rules are too loose for this movement profile. Tighten constraints instead of raising maxAttempts.");
            return last;
        }

        /// <summary>Fraction of seeds that pass on the FIRST attempt. Use this to tune a generator:
        /// &gt;90% is healthy, &lt;50% means the generator relies on rejection sampling and should be constrained by construction.</summary>
        public static double FirstTryPassRate(IGridGenerator gen, MovementProfile profile, int seeds, ValidatorOptions vopts = null)
        {
            var v = new ReachabilityValidator(profile, vopts);
            int ok = 0;
            for (int s = 0; s < seeds; s++)
                if (v.Validate(gen.Generate(new Rng(s).Derive(0))).Passed) ok++;
            return (double)ok / seeds;
        }
    }

    /// <summary>Common post-processing helpers usable by any generator.</summary>
    public static class GridPasses
    {
        /// <summary>First standable cell scanning columns from the left (or right), top-down in each column.</summary>
        public static Int2? FindRestingSpot(TileGrid g, bool fromLeft, int bodyHeight = 1, int xMin = 0, int xMax = int.MaxValue)
        {
            xMax = Math.Min(xMax, g.Width - 1);
            for (int i = 0; i <= xMax - xMin; i++)
            {
                int x = fromLeft ? xMin + i : xMax - i;
                for (int y = g.Height - 1; y >= 1; y--)
                    if (IsRest(g, x, y, bodyHeight)) return new Int2(x, y);
            }
            return null;
        }

        public static bool IsRest(TileGrid g, int x, int y, int bodyHeight)
        {
            if (!CellRules.IsSupport(g.Get(x, y - 1))) return false;
            for (int dy = 0; dy < bodyHeight; dy++)
            {
                Cell c = g.Get(x, y + dy);
                if (!g.InBounds(x, y + dy) || !CellRules.IsPassable(c) || c == Cell.OneWay) return false;
            }
            return true;
        }

        /// <summary>Place Exit at the reachable resting spot farthest (BFS order is not distance-aware, so we use Manhattan from spawn).
        /// Guarantees solvability by construction for open-form generators (caves, heightmaps).</summary>
        public static bool PlaceExitAtFarthestReachable(TileGrid g, MovementProfile profile, ValidatorOptions vopts = null)
        {
            var spawns = g.FindAll(Cell.Spawn);
            if (spawns.Count == 0) return false;
            g.ClearMarkers(Cell.Exit);
            var v = new ReachabilityValidator(profile, vopts);
            v.Validate(g, null, spawns[0]); // exit override = spawn so it "passes"; we only want reachability flags
            Int2 best = spawns[0]; int bestD = -1;
            for (int y = 0; y < g.Height; y++)
                for (int x = 0; x < g.Width; x++)
                {
                    if (!v.WasReachable(x, y) || g.Get(x, y) != Cell.Empty) continue;
                    int d = Math.Abs(x - spawns[0].x) + Math.Abs(y - spawns[0].y);
                    if (d > bestD) { bestD = d; best = new Int2(x, y); }
                }
            if (bestD <= 0) return false;
            g.Set(best.x, best.y, Cell.Exit);
            return true;
        }

        /// <summary>Scatter markers (pickups/enemies) on empty resting spots away from Spawn.
        /// Pass allow = validator.WasReachable (after a Validate call) to restrict to reachable spots.</summary>
        public static int Scatter(TileGrid g, Cell marker, int count, Rng rng, int bodyHeight = 1, int minDistFromSpawn = 4,
                                  Func<int, int, bool> allow = null)
        {
            var spawns = g.FindAll(Cell.Spawn);
            var candidates = new List<Int2>();
            for (int y = 1; y < g.Height; y++)
                for (int x = 0; x < g.Width; x++)
                {
                    if (g.Get(x, y) != Cell.Empty || !IsRest(g, x, y, bodyHeight)) continue;
                    if (allow != null && !allow(x, y)) continue;
                    if (spawns.Count > 0 && Math.Abs(x - spawns[0].x) + Math.Abs(y - spawns[0].y) < minDistFromSpawn) continue;
                    candidates.Add(new Int2(x, y));
                }
            rng.Shuffle(candidates);
            int n = Math.Min(count, candidates.Count);
            for (int i = 0; i < n; i++) g.Set(candidates[i].x, candidates[i].y, marker);
            return n;
        }
    }

    /// <summary>Non-procedural "generator": returns an authored ASCII level (probabilistic glyphs resolved per seed).</summary>
    public sealed class FixedAsciiGenerator : IGridGenerator
    {
        private readonly string _text;
        public FixedAsciiGenerator(string text) { _text = text; }
        public string Name { get { return "AsciiLevel"; } }
        public TileGrid Generate(Rng rng) { return AsciiLevel.Parse(_text, rng); }
    }
}

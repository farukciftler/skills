using System;
using System.Collections.Generic;

namespace PlatformerGen
{
    /// <summary>
    /// 1D fractal value-noise heightline, then CONSTRAINED by the movement profile so it is playable
    /// by construction: consecutive columns never rise more than MaxStepUp, pits never exceed MaxGap,
    /// optional one-way platforms add verticality. Good for overworld / exploration strips.
    /// (Raw Perlin terrain is the classic mistake: it looks right and is unplayable.)
    /// </summary>
    public sealed class HeightmapGenerator : IGridGenerator
    {
        public int Width = 200, Height = 32;
        public int MinGround = 3, MaxGround = 18;
        public double NoiseScale = 0.06;      // lower = wider hills
        public int Octaves = 3;
        public double PitChance = 0.04;       // per column, once a pit is allowed
        public double PlatformChance = 0.05;
        public double Margin = 0.8;
        public MovementProfile Profile;

        public string Name { get { return "Heightmap(" + Width + "x" + Height + ")"; } }
        public HeightmapGenerator(MovementProfile profile) { Profile = profile; }

        public TileGrid Generate(Rng rng)
        {
            int maxUp = Math.Max(1, Profile.MaxStepUpTiles(Margin));
            int maxGap = Math.Max(1, Profile.MaxGapTiles(Margin));
            var noise = new ValueNoise1D(rng.Derive(1));
            var feat = rng.Derive(2);
            var g = new TileGrid(Width, Height);
            g.OutOfBounds = Cell.Solid;

            int[] h = new int[Width];
            int prev = (MinGround + MaxGround) / 2;
            for (int x = 0; x < Width; x++)
            {
                double n = noise.Fbm(x * NoiseScale, Octaves);                  // 0..1
                int target = MinGround + (int)Math.Round(n * (MaxGround - MinGround));
                int cur = Math.Max(prev - 6, Math.Min(prev + maxUp, target));   // clamp rise to maxUp, drops to 6
                h[x] = cur; prev = cur;
            }
            // flatten spawn / exit pads
            for (int x = 0; x < 4; x++) h[x] = h[4];
            for (int x = Width - 5; x < Width; x++) h[x] = h[Width - 6];

            for (int x = 0; x < Width; x++) for (int y = 0; y < h[x]; y++) g.Set(x, y, Cell.Solid);

            // pits: only on locally flat-ish runs, width <= maxGap, landing not higher than takeoff
            for (int x = 8; x < Width - 10; x++)
            {
                if (!feat.Chance(PitChance)) continue;
                int w = feat.Range(1, maxGap + 1);
                int takeoff = h[x - 1], land = h[Math.Min(Width - 1, x + w)];
                if (land > takeoff) continue;
                for (int i = 0; i < w && x + i < Width - 6; i++) for (int y = 0; y < h[x + i]; y++) g.Set(x + i, y, Cell.Empty);
                x += w + 6;   // spacing between pits
            }
            // one-way platforms a reachable height above the ground
            for (int x = 6; x < Width - 8; x++)
            {
                if (!feat.Chance(PlatformChance)) continue;
                int pw = feat.Range(2, 5);
                int baseY = h[x];
                for (int i = 0; i < pw; i++) baseY = Math.Max(baseY, h[x + i]);
                int py = baseY + feat.Range(2, maxUp + 1) - 1;   // platform cell row (stand on py+1)
                if (py + 1 + Profile.BodyHeight >= Height) continue;
                for (int i = 0; i < pw; i++) if (g.Get(x + i, py) == Cell.Empty) g.Set(x + i, py, Cell.OneWay);
                x += pw + 4;
            }
            g.Set(1, h[1], Cell.Spawn);
            g.Set(Width - 2, h[Width - 2], Cell.Exit);
            return g;
        }
    }

    /// <summary>
    /// Cellular-automata caves (4-5 rule), connectivity repair (keep largest open region), then a
    /// PLATFORMER pass: tall open shafts get one-way ledges every (maxJump) rows so vertical space is
    /// climbable. Spawn is placed near the top-left; Exit at the farthest reachable resting spot, so
    /// the level is solvable by construction. Good for metroidvania filler / underground biomes.
    /// </summary>
    public sealed class CaveGenerator : IGridGenerator
    {
        public int Width = 64, Height = 40;
        public double FillChance = 0.47;
        public int Iterations = 5;
        public int BirthLimit = 5;      // empty -> wall if >= BirthLimit wall neighbours
        public int SurviveLimit = 4;    // wall stays wall if >= SurviveLimit wall neighbours
        public double Margin = 0.8;
        public MovementProfile Profile;
        public ValidatorOptions ValidatorOptions = new ValidatorOptions { BottomIsPit = false };

        public string Name { get { return "Cave(" + Width + "x" + Height + ")"; } }
        public CaveGenerator(MovementProfile profile) { Profile = profile; }

        public TileGrid Generate(Rng rng)
        {
            var g = new TileGrid(Width, Height);
            g.OutOfBounds = Cell.Solid;
            var r = rng.Derive(1);
            for (int y = 0; y < Height; y++)
                for (int x = 0; x < Width; x++)
                    g.Set(x, y, (x == 0 || y == 0 || x == Width - 1 || y == Height - 1 || r.Chance(FillChance)) ? Cell.Solid : Cell.Empty);

            for (int i = 0; i < Iterations; i++) g = Step(g);
            KeepLargestRegion(g);
            AddLedges(g, rng.Derive(2));

            var spawn = GridPasses.FindRestingSpot(g, true, Profile.BodyHeight, 1, Width / 3);
            if (!spawn.HasValue) spawn = GridPasses.FindRestingSpot(g, true, Profile.BodyHeight);
            if (spawn.HasValue)
            {
                g.Set(spawn.Value.x, spawn.Value.y, Cell.Spawn);
                GridPasses.PlaceExitAtFarthestReachable(g, Profile, ValidatorOptions);
            }
            return g;
        }

        private TileGrid Step(TileGrid src)
        {
            var dst = new TileGrid(src.Width, src.Height);
            dst.OutOfBounds = Cell.Solid;
            for (int y = 0; y < src.Height; y++)
                for (int x = 0; x < src.Width; x++)
                {
                    int n = 0;
                    for (int dy = -1; dy <= 1; dy++) for (int dx = -1; dx <= 1; dx++)
                        if ((dx != 0 || dy != 0) && CellRules.IsSolid(src.Get(x + dx, y + dy))) n++;
                    bool wall = CellRules.IsSolid(src.Get(x, y));
                    dst.Set(x, y, (wall ? n >= SurviveLimit : n >= BirthLimit) ? Cell.Solid : Cell.Empty);
                }
            return dst;
        }

        private static void KeepLargestRegion(TileGrid g)
        {
            var label = new int[g.Width * g.Height];
            int best = 0, bestSize = 0, next = 0;
            var stack = new Stack<int>();
            for (int i = 0; i < label.Length; i++)
            {
                if (label[i] != 0 || g.Raw[i] != Cell.Empty) continue;
                next++; int size = 0;
                stack.Push(i); label[i] = next;
                while (stack.Count > 0)
                {
                    int c = stack.Pop(); size++;
                    int cx = c % g.Width, cy = c / g.Width;
                    int[] nb = { cx - 1, cy, cx + 1, cy, cx, cy - 1, cx, cy + 1 };
                    for (int k = 0; k < 8; k += 2)
                    {
                        int nx = nb[k], ny = nb[k + 1];
                        if (!g.InBounds(nx, ny)) continue;
                        int ni = g.Index(nx, ny);
                        if (label[ni] == 0 && g.Raw[ni] == Cell.Empty) { label[ni] = next; stack.Push(ni); }
                    }
                }
                if (size > bestSize) { bestSize = size; best = next; }
            }
            for (int i = 0; i < label.Length; i++) if (g.Raw[i] == Cell.Empty && label[i] != best) g.Raw[i] = Cell.Solid;
        }

        /// <summary>For each column, find vertical open runs taller than the jump and insert one-way ledges.</summary>
        private void AddLedges(TileGrid g, Rng rng)
        {
            int step = Math.Max(2, Profile.MaxStepUpTiles(Margin));
            for (int x = 1; x < g.Width - 1; x += rng.Range(2, 4))
            {
                int y = 1;
                while (y < g.Height - 1)
                {
                    if (!CellRules.IsSupport(g.Get(x, y - 1)) || g.Get(x, y) != Cell.Empty) { y++; continue; }
                    // (x,y) is a floor-level cell: walk up the open run
                    int top = y;
                    while (top < g.Height - 1 && g.Get(x, top) == Cell.Empty) top++;
                    int run = top - y;
                    for (int ly = y + step; ly < top - Profile.BodyHeight - 1; ly += step)
                    {
                        int w = rng.Range(2, 4);
                        for (int i = 0; i < w; i++)
                            if (g.Get(x + i, ly) == Cell.Empty && g.Get(x + i, ly + 1) == Cell.Empty) g.Set(x + i, ly, Cell.OneWay);
                    }
                    y = top + 1;
                    if (run <= 0) y++;
                }
            }
        }
    }

    /// <summary>Deterministic 1D value noise with fBm (no UnityEngine.Mathf.PerlinNoise dependency).</summary>
    public sealed class ValueNoise1D
    {
        private readonly double[] _lattice = new double[256];
        public ValueNoise1D(Rng rng) { for (int i = 0; i < 256; i++) _lattice[i] = rng.NextDouble(); }

        public double Sample(double x)
        {
            int i0 = (int)Math.Floor(x);
            double t = x - i0;
            double a = _lattice[i0 & 255], b = _lattice[(i0 + 1) & 255];
            double s = t * t * (3 - 2 * t);
            return a + (b - a) * s;
        }

        public double Fbm(double x, int octaves)
        {
            double sum = 0, amp = 1, norm = 0, f = 1;
            for (int o = 0; o < octaves; o++) { sum += Sample(x * f + o * 17.3) * amp; norm += amp; amp *= 0.5; f *= 2; }
            return sum / norm;
        }
    }
}

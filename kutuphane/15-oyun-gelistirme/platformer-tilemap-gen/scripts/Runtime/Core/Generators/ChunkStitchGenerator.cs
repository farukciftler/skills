using System;
using System.Collections.Generic;

namespace PlatformerGen
{
    public sealed class ChunkTemplate
    {
        public string Name;
        public double Difficulty;   // 0..10, designer scale
        public double Weight = 1;
        public List<string> Rows;
        public int EntryY, ExitY;   // resting height at first/last column, in chunk-local rows (0 = bottom)

        public int Width { get { return Rows[0].Length; } }
        public int Height { get { return Rows.Count; } }

        public static List<ChunkTemplate> FromText(string text, int bodyHeight = 1)
        {
            var list = new List<ChunkTemplate>();
            foreach (var b in TemplateFile.Parse(text))
            {
                if (b.Kind != "chunk") continue;
                var t = new ChunkTemplate
                {
                    Name = b.Get("name", "chunk@" + b.SourceLine),
                    Difficulty = b.GetDouble("difficulty", 1),
                    Weight = b.GetDouble("weight", 1),
                    Rows = new List<string>(b.Rows)
                };
                int w = t.Rows[0].Length;
                foreach (var r in t.Rows) if (r.Length != w) throw new FormatException("Chunk '" + t.Name + "' rows must all be " + w + " wide");
                // '?'/'!' resolved as Empty for edge analysis; edges should be deterministic anyway
                var probe = AsciiLevel.Parse(t.Rows, new Rng(1));
                int e = RestY(probe, 0, bodyHeight), x = RestY(probe, probe.Width - 1, bodyHeight);
                if (e < 0 || x < 0) throw new FormatException("Chunk '" + t.Name + "' needs a resting spot (ground with headroom) in its first and last column");
                t.EntryY = e; t.ExitY = x;
                list.Add(t);
            }
            return list;
        }

        private static int RestY(TileGrid g, int x, int bodyHeight)
        {
            for (int y = 1; y < g.Height; y++) if (GridPasses.IsRest(g, x, y, bodyHeight)) return y;
            return -1;
        }
    }

    public struct Segment
    {
        public TileGrid Grid;   // full level height, segment width
        public int X;           // world column where this segment starts
        public int ExitGround;  // resting row at the segment's last column
        public string Label;    // chunk name or beat description (debug)
    }

    /// <summary>
    /// Infinite, deterministic stream of segments for side-scrollers / endless runners.
    /// Segment i depends only on (seed, i, previous exit height) -> stream it chunk by chunk at runtime,
    /// unload behind the camera, regenerate identically on replay.
    /// Mixes hand-authored chunks with procedural "rhythm beats" (Launchpad-style: the beat's
    /// geometry is sized from the MovementProfile, so every beat is playable by construction).
    /// </summary>
    public sealed class ChunkStream
    {
        private readonly ChunkStitchGenerator _cfg;
        private readonly Rng _root;
        private int _index;
        private int _x;
        private int _ground;

        public int Index { get { return _index; } }
        public int NextX { get { return _x; } }

        public ChunkStream(ChunkStitchGenerator cfg, Rng root)
        {
            _cfg = cfg; _root = root; _ground = cfg.StartGround;
        }

        public Segment Next(double progress01)
        {
            var rng = _root.Derive(_index);
            Segment seg;
            bool useChunk = _cfg.Chunks.Count > 0 && !rng.Chance(_cfg.BeatChance);
            if (!useChunk || !TryChunk(rng, progress01, out seg)) seg = Beat(rng, progress01);
            seg.X = _x;
            _x += seg.Grid.Width;
            _ground = seg.ExitGround;
            _index++;
            return seg;
        }

        private bool TryChunk(Rng rng, double progress, out Segment seg)
        {
            seg = default(Segment);
            double target = _cfg.DifficultyStart + (_cfg.DifficultyEnd - _cfg.DifficultyStart) * progress;
            var cands = new List<ChunkTemplate>();
            foreach (var c in _cfg.Chunks)
            {
                if (Math.Abs(c.Difficulty - target) > _cfg.DifficultyTolerance) continue;
                int dy = _ground - c.EntryY;
                if (dy < 0 || dy + c.Height > _cfg.Height) continue;
                int exitWorld = dy + c.ExitY;
                if (exitWorld < _cfg.MinGround || exitWorld > _cfg.MaxGround) continue;
                cands.Add(c);
            }
            if (cands.Count == 0) return false;
            var pick = rng.PickWeighted(cands, c => c.Weight);
            var local = AsciiLevel.Parse(pick.Rows, rng.Derive(77));
            local.ClearMarkers(Cell.Spawn); local.ClearMarkers(Cell.Exit);
            int oy = _ground - pick.EntryY;
            var g = new TileGrid(pick.Width, _cfg.Height);
            g.Blit(local, 0, oy);
            // extend ground downward under solid bottom cells; non-solid bottom = bottomless pit
            for (int x = 0; x < pick.Width; x++)
                if (CellRules.IsSolid(local.Get(x, 0))) for (int y = 0; y < oy; y++) g.Set(x, y, Cell.Solid);
            seg = new Segment { Grid = g, ExitGround = oy + pick.ExitY, Label = pick.Name };
            return true;
        }

        private Segment Beat(Rng rng, double progress)
        {
            var p = _cfg.Profile;
            double m = _cfg.BeatMargin;
            int maxGap = Math.Max(1, p.MaxGapTiles(m));
            int maxUp = Math.Max(1, p.MaxStepUpTiles(m));
            double diff = Math.Max(0, Math.Min(1, progress));
            int H = _cfg.Height;

            int kind = rng.Next(5);
            int ground = _ground;
            string label;
            var cols = new List<int>();            // ground height per column (-1 = pit)
            var extra = new List<KeyValuePair<Int2, Cell>>();

            int lead = rng.Range(2, 4);            // run-up before the beat's challenge
            for (int i = 0; i < lead; i++) cols.Add(ground);

            switch (kind)
            {
                case 0: // gap, same height
                {
                    int gap = Math.Max(1, (int)Math.Round(1 + (maxGap - 1) * (0.3 + 0.7 * diff * rng.NextDouble())));
                    for (int i = 0; i < gap; i++) cols.Add(-1);
                    label = "gap" + gap;
                    break;
                }
                case 1: // step up (optionally with a small gap: the higher the step, the shorter the gap)
                {
                    int up = rng.Range(1, maxUp + 1);
                    if (ground + up > _cfg.MaxGround) up = Math.Max(0, _cfg.MaxGround - ground);
                    int gap = rng.Chance(0.3 + 0.5 * diff) ? Math.Max(0, Math.Min(maxGap - 2 * up, rng.Range(1, maxGap))) : 0;
                    for (int i = 0; i < gap; i++) cols.Add(-1);
                    ground += up;
                    label = "up" + up + (gap > 0 ? "+gap" + gap : "");
                    break;
                }
                case 2: // step down (with optional gap — falling extends reach, so allow full maxGap)
                {
                    int down = rng.Range(1, 4);
                    if (ground - down < _cfg.MinGround) down = Math.Max(0, ground - _cfg.MinGround);
                    int gap = rng.Chance(0.5) ? rng.Range(1, maxGap + 1) : 0;
                    for (int i = 0; i < gap; i++) cols.Add(-1);
                    ground -= down;
                    label = "down" + down + (gap > 0 ? "+gap" + gap : "");
                    break;
                }
                case 3: // hazard strip on the ground (jump over)
                {
                    int maxSpikes = p.MaxHazardRunTiles(m);
                    int w = Math.Max(1, Math.Min(maxSpikes, 1 + (int)(diff * maxSpikes * rng.NextDouble())));
                    int start = cols.Count;
                    for (int i = 0; i < w; i++) cols.Add(ground);
                    for (int i = 0; i < w; i++) extra.Add(new KeyValuePair<Int2, Cell>(new Int2(start + i, ground), Cell.Hazard));
                    label = "spikes" + w;
                    break;
                }
                default: // one-way platform hop over a wide pit
                {
                    int half = Math.Max(1, maxGap - 1);
                    int platW = rng.Range(2, 4);
                    int platY = ground + rng.Range(0, Math.Max(1, maxUp));
                    int pitLeft = Math.Max(1, Math.Min(half, rng.Range(1, half + 1)));
                    int pitRight = Math.Max(1, Math.Min(half, rng.Range(1, half + 1)));
                    int start = cols.Count;
                    for (int i = 0; i < pitLeft + platW + pitRight; i++) cols.Add(-1);
                    for (int i = 0; i < platW; i++) extra.Add(new KeyValuePair<Int2, Cell>(new Int2(start + pitLeft + i, platY - 1), Cell.OneWay));
                    label = "hop" + (pitLeft + platW + pitRight);
                    break;
                }
            }
            int tail = rng.Range(2, 4);
            for (int i = 0; i < tail; i++) cols.Add(ground);

            var g = new TileGrid(cols.Count, H);
            for (int x = 0; x < cols.Count; x++)
                if (cols[x] >= 0) for (int y = 0; y < cols[x]; y++) g.Set(x, y, Cell.Solid);
            foreach (var kv in extra) g.Set(kv.Key.x, kv.Key.y, kv.Value);
            return new Segment { Grid = g, ExitGround = ground, Label = "beat:" + label };
        }
    }

    /// <summary>Finite linear level built from a ChunkStream: run-up + spawn, N segments, landing + exit.</summary>
    public sealed class ChunkStitchGenerator : IGridGenerator
    {
        public int Height = 16;
        public int TargetWidth = 160;
        public int StartGround = 4;
        public int MinGround = 2;
        public int MaxGround = 10;               // keep headroom: MaxGround + bodyHeight + jump < Height
        public double DifficultyStart = 1, DifficultyEnd = 5, DifficultyTolerance = 1.5;
        public double BeatChance = 0.35;         // probability of a procedural beat instead of an authored chunk
        public double BeatMargin = 0.8;          // beats use this fraction of max jump/gap
        public MovementProfile Profile;
        public readonly List<ChunkTemplate> Chunks = new List<ChunkTemplate>();
        public List<string> LastLabels = new List<string>();

        public string Name { get { return "ChunkStitch(w" + TargetWidth + ")"; } }

        public ChunkStitchGenerator(MovementProfile profile, IEnumerable<ChunkTemplate> chunks = null)
        {
            Profile = profile;
            if (chunks != null) Chunks.AddRange(chunks);
        }

        public ChunkStream CreateStream(Rng rng) { return new ChunkStream(this, rng); }

        public TileGrid Generate(Rng rng)
        {
            var stream = CreateStream(rng);
            var segs = new List<Segment>();
            LastLabels.Clear();
            const int runUp = 4, landing = 5;
            int w = runUp;
            while (w < TargetWidth - landing)
            {
                var s = stream.Next((double)(w - runUp) / Math.Max(1, TargetWidth - runUp - landing));
                segs.Add(s); w += s.Grid.Width; LastLabels.Add(s.Label);
            }
            int total = w + landing;
            var g = new TileGrid(total, Height);
            g.OutOfBounds = Cell.Solid;
            for (int x = 0; x < runUp; x++) for (int y = 0; y < StartGround; y++) g.Set(x, y, Cell.Solid);
            g.Set(1, StartGround, Cell.Spawn);
            foreach (var s in segs) g.Blit(s.Grid, runUp + s.X, 0);
            int endGround = segs.Count > 0 ? segs[segs.Count - 1].ExitGround : StartGround;
            for (int x = w; x < total; x++) for (int y = 0; y < endGround; y++) g.Set(x, y, Cell.Solid);
            g.Set(total - 2, endGround, Cell.Exit);
            return g;
        }
    }
}

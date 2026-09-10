using System;
using System.Collections.Generic;

namespace PlatformerGen
{
    [Flags]
    public enum Exits { None = 0, L = 1, R = 2, U = 4, D = 8 }

    public sealed class RoomTemplate
    {
        public string Name;
        public Exits Exits;
        public double Weight = 1;
        public bool Mirror;              // may be flipped horizontally (L/R swapped)
        public string Tags = "";
        public List<string> Rows;

        public static Exits ParseExits(string s)
        {
            Exits e = Exits.None;
            foreach (char ch in (s ?? "").ToUpperInvariant())
            {
                if (ch == 'L') e |= Exits.L; else if (ch == 'R') e |= Exits.R;
                else if (ch == 'U') e |= Exits.U; else if (ch == 'D') e |= Exits.D;
            }
            return e;
        }

        public static Exits MirrorExits(Exits e)
        {
            Exits m = e & (Exits.U | Exits.D);
            if ((e & Exits.L) != 0) m |= Exits.R;
            if ((e & Exits.R) != 0) m |= Exits.L;
            return m;
        }

        public static List<RoomTemplate> FromText(string text)
        {
            var list = new List<RoomTemplate>();
            foreach (var b in TemplateFile.Parse(text))
            {
                if (b.Kind != "room") continue;
                list.Add(new RoomTemplate
                {
                    Name = b.Get("name", "room@" + b.SourceLine),
                    Exits = ParseExits(b.Get("exits", "")),
                    Weight = b.GetDouble("weight", 1),
                    Mirror = b.GetBool("mirror", true),
                    Tags = b.Get("tags", ""),
                    Rows = new List<string>(b.Rows)
                });
            }
            return list;
        }
    }

    /// <summary>
    /// Spelunky-style generator, generalised: an RX x RY grid of hand-authored rooms. A random walk
    /// from a top-row start to the bottom row carves the critical path (40% left / 40% right / 20% down,
    /// bouncing off walls into a drop). Each path room gets the exit mask its neighbours require
    /// (L/R/U/D); a template is picked whose exits are a superset of that mask (mirrored if allowed).
    /// Off-path rooms get any template (filler). Solvability comes from the path + template contract;
    /// the validator then confirms it with real jump physics.
    /// </summary>
    public sealed class RoomGridGenerator : IGridGenerator
    {
        public int RoomsX = 4, RoomsY = 4;
        public int RoomW = 10, RoomH = 8;
        public bool SolidBorder = true;
        public double ChanceLeft = 0.4, ChanceRight = 0.4; // remainder = down
        public int BodyHeight = 1;
        public readonly List<RoomTemplate> Templates;

        public string Name { get { return "RoomGrid(" + RoomsX + "x" + RoomsY + ")"; } }

        // For inspection/debug after Generate():
        public Exits[,] LastRequired;
        public bool[,] LastOnPath;
        public string[,] LastTemplateNames;

        public RoomGridGenerator(int roomW, int roomH, IEnumerable<RoomTemplate> templates)
        {
            RoomW = roomW; RoomH = roomH;
            Templates = new List<RoomTemplate>();
            foreach (var t in templates) AddTemplate(t);
        }

        public static RoomGridGenerator FromText(string templatesText, int roomW, int roomH)
        {
            return new RoomGridGenerator(roomW, roomH, RoomTemplate.FromText(templatesText));
        }

        public void AddTemplate(RoomTemplate t)
        {
            if (t.Rows.Count != RoomH) throw new FormatException("Room '" + t.Name + "' height " + t.Rows.Count + " != " + RoomH);
            foreach (var r in t.Rows) if (r.Length != RoomW) throw new FormatException("Room '" + t.Name + "' has a row of width " + r.Length + " != " + RoomW + ": \"" + r + "\"");
            Templates.Add(t);
        }

        public TileGrid Generate(Rng rng)
        {
            var pathRng = rng.Derive(1);
            var pickRng = rng.Derive(2);
            var glyphRng = rng.Derive(3);

            var req = new Exits[RoomsX, RoomsY];
            var onPath = new bool[RoomsX, RoomsY];

            // ---- 1. critical path (room y: RoomsY-1 = top row) ----
            int cx = pathRng.Next(RoomsX), cy = RoomsY - 1;
            int startX = cx, startY = cy;
            onPath[cx, cy] = true;
            int endX = cx, endY = cy;
            int guard = RoomsX * RoomsY * 4;
            while (guard-- > 0)
            {
                double r = pathRng.NextDouble();
                int dir = r < ChanceLeft ? -1 : (r < ChanceLeft + ChanceRight ? 1 : 0);
                int nx = cx + dir;
                bool horizontalOk = dir != 0 && nx >= 0 && nx < RoomsX && !onPath[nx, cy];
                if (horizontalOk)
                {
                    req[cx, cy] |= dir < 0 ? Exits.L : Exits.R;
                    req[nx, cy] |= dir < 0 ? Exits.R : Exits.L;
                    cx = nx; onPath[cx, cy] = true;
                    continue;
                }
                if (cy == 0) { endX = cx; endY = cy; break; }        // bottom row: this is the exit room
                req[cx, cy] |= Exits.D;
                req[cx, cy - 1] |= Exits.U;
                cy--; onPath[cx, cy] = true;
                endX = cx; endY = cy;
            }

            // ---- 2. assemble ----
            int b = SolidBorder ? 1 : 0;
            var grid = new TileGrid(RoomsX * RoomW + 2 * b, RoomsY * RoomH + 2 * b);
            if (SolidBorder) grid.Border(Cell.Solid);
            LastRequired = req; LastOnPath = onPath; LastTemplateNames = new string[RoomsX, RoomsY];

            for (int ry = 0; ry < RoomsY; ry++)
                for (int rx = 0; rx < RoomsX; rx++)
                {
                    bool mirrored;
                    RoomTemplate t = Pick(req[rx, ry], onPath[rx, ry], pickRng, out mirrored);
                    LastTemplateNames[rx, ry] = t.Name + (mirrored ? "~" : "");
                    var rows = t.Rows;
                    if (mirrored)
                    {
                        rows = new List<string>(t.Rows.Count);
                        foreach (var row in t.Rows) { var a = row.ToCharArray(); Array.Reverse(a); rows.Add(new string(a)); }
                    }
                    var room = AsciiLevel.Parse(rows, glyphRng.Derive(ry * 131 + rx));
                    // strip authored markers from rooms that shouldn't have them
                    bool isStart = rx == startX && ry == startY, isEnd = rx == endX && ry == endY;
                    if (!isStart) room.ClearMarkers(Cell.Spawn);
                    if (!isEnd) room.ClearMarkers(Cell.Exit);
                    grid.Blit(room, b + rx * RoomW, b + ry * RoomH);
                }

            // ---- 3. spawn / exit if the templates did not author them ----
            if (grid.Count(Cell.Spawn) == 0) PlaceInRoom(grid, startX, startY, b, Cell.Spawn, rng.Derive(4));
            if (grid.Count(Cell.Exit) == 0) PlaceInRoom(grid, endX, endY, b, Cell.Exit, rng.Derive(5));
            return grid;
        }

        private RoomTemplate Pick(Exits need, bool onPath, Rng rng, out bool mirrored)
        {
            var cands = new List<KeyValuePair<RoomTemplate, bool>>();
            foreach (var t in Templates)
            {
                if (!onPath) { cands.Add(new KeyValuePair<RoomTemplate, bool>(t, t.Mirror && rng.Chance(0.5))); continue; }
                if ((t.Exits & need) == need) cands.Add(new KeyValuePair<RoomTemplate, bool>(t, false));
                if (t.Mirror && (RoomTemplate.MirrorExits(t.Exits) & need) == need) cands.Add(new KeyValuePair<RoomTemplate, bool>(t, true));
            }
            if (cands.Count == 0)
                throw new InvalidOperationException("No room template satisfies exits " + need + ". Add a template with exits ⊇ " + need + ".");
            var pick = rng.PickWeighted(cands, kv => kv.Key.Weight);
            mirrored = pick.Value;
            return pick.Key;
        }

        private void PlaceInRoom(TileGrid g, int rx, int ry, int b, Cell marker, Rng rng)
        {
            int x0 = b + rx * RoomW, y0 = b + ry * RoomH;
            var spots = new List<Int2>();
            for (int y = y0; y < y0 + RoomH; y++)
                for (int x = x0; x < x0 + RoomW; x++)
                    if (g.Get(x, y) == Cell.Empty && GridPasses.IsRest(g, x, y, BodyHeight)) spots.Add(new Int2(x, y));
            if (spots.Count == 0) return; // validator will report missing marker
            // prefer floor-level spots: elevated perches are more often unreachable
            int minY = int.MaxValue;
            foreach (var sp in spots) minY = Math.Min(minY, sp.y);
            spots.RemoveAll(sp => sp.y > minY + 1);
            var s = rng.Pick(spots);
            g.Set(s.x, s.y, marker);
        }

        /// <summary>Debug view of the room layout: path rooms show their required exits.</summary>
        public string DescribeLastLayout()
        {
            if (LastRequired == null) return "(not generated)";
            var sb = new System.Text.StringBuilder();
            for (int ry = RoomsY - 1; ry >= 0; ry--)
            {
                for (int rx = 0; rx < RoomsX; rx++)
                    sb.Append(LastOnPath[rx, ry] ? ("[" + LastRequired[rx, ry].ToString().Replace(", ", "") + "]").PadRight(10) : "[ ]".PadRight(10));
                sb.Append('\n');
            }
            return sb.ToString();
        }
    }
}

using System;
using System.Collections.Generic;
using System.Text;

namespace PlatformerGen
{
    /// <summary>
    /// Text <-> grid. ASCII is the lingua franca between Claude, designers and the generator:
    /// Claude can author, read and diff levels as text, and the same text drives Unity.
    ///
    /// Default legend:
    ///   .  (or space) Empty      #  Solid        =  OneWay      ^  Hazard     H  Ladder
    ///   S  Spawn                 E  Exit         $  Pickup      e  Enemy      B  Breakable   ~ Decor
    ///   ?  50% Solid / 50% Empty (probabilistic, resolved at parse time with an Rng)
    ///   !  50% Hazard / 50% Empty
    /// Text rows are written TOP row first; the grid is stored bottom-up. Lines starting with // are comments.
    /// </summary>
    public static class AsciiLevel
    {
        private static readonly Dictionary<char, Cell> DefaultLegend = new Dictionary<char, Cell>
        {
            { '.', Cell.Empty }, { ' ', Cell.Empty }, { '#', Cell.Solid }, { '=', Cell.OneWay },
            { '^', Cell.Hazard }, { 'H', Cell.Ladder }, { 'S', Cell.Spawn }, { 'E', Cell.Exit },
            { '$', Cell.Pickup }, { 'e', Cell.Enemy }, { 'B', Cell.Breakable }, { '~', Cell.Decor }
        };

        private static readonly Dictionary<Cell, char> DefaultReverse = BuildReverse();

        private static Dictionary<Cell, char> BuildReverse()
        {
            var d = new Dictionary<Cell, char>();
            foreach (var kv in DefaultLegend) if (!d.ContainsKey(kv.Value) && kv.Key != ' ') d[kv.Value] = kv.Key;
            return d;
        }

        /// <summary>Parse rows (top first). Rows shorter than the widest row are padded with Empty.
        /// rng may be null if the text has no probabilistic glyphs.</summary>
        public static TileGrid Parse(IList<string> rowsTopFirst, Rng rng = null, IDictionary<char, Cell> extraLegend = null)
        {
            if (rowsTopFirst == null || rowsTopFirst.Count == 0) throw new ArgumentException("No rows");
            int w = 0;
            for (int i = 0; i < rowsTopFirst.Count; i++) w = Math.Max(w, rowsTopFirst[i].TrimEnd('\r').Length);
            int h = rowsTopFirst.Count;
            var g = new TileGrid(w, h);
            for (int row = 0; row < h; row++)
            {
                string line = rowsTopFirst[row].TrimEnd('\r');
                int y = h - 1 - row;
                for (int x = 0; x < line.Length; x++)
                    g.Set(x, y, Resolve(line[x], rng, extraLegend, row, x));
            }
            return g;
        }

        public static TileGrid Parse(string text, Rng rng = null, IDictionary<char, Cell> extraLegend = null)
        {
            return Parse(SplitRows(text), rng, extraLegend);
        }

        public static List<string> SplitRows(string text)
        {
            var rows = new List<string>();
            foreach (var raw in text.Replace("\r\n", "\n").Split('\n'))
            {
                if (raw.Length == 0 || raw.TrimStart().StartsWith("//")) continue; // blank lines and // comments
                rows.Add(raw.TrimEnd('\r'));
            }
            return rows;
        }

        private static Cell Resolve(char ch, Rng rng, IDictionary<char, Cell> extra, int row, int col)
        {
            Cell c;
            if (extra != null && extra.TryGetValue(ch, out c)) return c;
            if (DefaultLegend.TryGetValue(ch, out c)) return c;
            if (ch == '?' || ch == '!')
            {
                if (rng == null) throw new ArgumentException("Probabilistic glyph '" + ch + "' needs an Rng (row " + row + ", col " + col + ")");
                return rng.Chance(0.5) ? (ch == '?' ? Cell.Solid : Cell.Hazard) : Cell.Empty;
            }
            throw new FormatException("Unknown glyph '" + ch + "' at row " + row + ", col " + col);
        }

        /// <summary>Render grid as text, top row first. overlay lets you stamp debug glyphs (e.g. reachable cells).</summary>
        public static string Render(TileGrid g, Func<int, int, char?> overlay = null)
        {
            var sb = new StringBuilder(g.Width * g.Height + g.Height);
            for (int y = g.Height - 1; y >= 0; y--)
            {
                for (int x = 0; x < g.Width; x++)
                {
                    char? o = overlay != null ? overlay(x, y) : null;
                    if (o.HasValue) { sb.Append(o.Value); continue; }
                    char ch;
                    sb.Append(DefaultReverse.TryGetValue(g.Get(x, y), out ch) ? ch : '?');
                }
                if (y > 0) sb.Append('\n');
            }
            return sb.ToString();
        }
    }
}

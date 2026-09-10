using System;
using System.Collections.Generic;
using System.Globalization;

namespace PlatformerGen
{
    /// <summary>
    /// Plain-text template format (Claude can author/edit these directly; Unity reads them as TextAsset):
    ///
    ///   // comment   (NOT '#': '#' is the Solid glyph)
    ///   @room name=corridor_a exits=LR weight=2 mirror=1 tags=easy
    ///   ##########
    ///   ..........
    ///   ...
    ///   @chunk name=spikes_1 difficulty=2 weight=1
    ///   ...
    ///
    /// Rows are written TOP row first. All blocks of the same kind must share the declared size
    /// (rooms) or height (chunks). Glyphs follow AsciiLevel's legend (incl. '?' and '!').
    /// </summary>
    public sealed class TemplateBlock
    {
        public string Kind;                                  // "room" | "chunk" | anything
        public readonly Dictionary<string, string> Attr = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
        public readonly List<string> Rows = new List<string>();
        public int SourceLine;

        public string Get(string key, string def = "") { string v; return Attr.TryGetValue(key, out v) ? v : def; }
        public double GetDouble(string key, double def)
        {
            double d; return double.TryParse(Get(key, ""), NumberStyles.Float, CultureInfo.InvariantCulture, out d) ? d : def;
        }
        public int GetInt(string key, int def) { int i; return int.TryParse(Get(key, ""), out i) ? i : def; }
        public bool GetBool(string key, bool def)
        {
            string v = Get(key, "").ToLowerInvariant();
            if (v == "1" || v == "true" || v == "yes") return true;
            if (v == "0" || v == "false" || v == "no") return false;
            return def;
        }
        public int Width { get { int w = 0; foreach (var r in Rows) w = Math.Max(w, r.Length); return w; } }
        public int Height { get { return Rows.Count; } }
    }

    public static class TemplateFile
    {
        public static List<TemplateBlock> Parse(string text)
        {
            var blocks = new List<TemplateBlock>();
            TemplateBlock cur = null;
            var lines = text.Replace("\r\n", "\n").Split('\n');
            for (int i = 0; i < lines.Length; i++)
            {
                string line = lines[i].TrimEnd('\r');
                string trimmed = line.Trim();
                if (trimmed.Length == 0 || trimmed.StartsWith("//")) continue;   // '#' is the Solid glyph, so comments use //
                if (trimmed.StartsWith("@"))
                {
                    cur = new TemplateBlock { SourceLine = i + 1 };
                    var parts = trimmed.Substring(1).Split(new[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries);
                    cur.Kind = parts.Length > 0 ? parts[0].ToLowerInvariant() : "";
                    for (int p = 1; p < parts.Length; p++)
                    {
                        int eq = parts[p].IndexOf('=');
                        if (eq > 0) cur.Attr[parts[p].Substring(0, eq)] = parts[p].Substring(eq + 1);
                    }
                    blocks.Add(cur);
                    continue;
                }
                if (cur == null) continue; // text before the first block (free comments)
                cur.Rows.Add(line);
            }
            foreach (var b in blocks)
                if (b.Rows.Count == 0) throw new FormatException("Template @" + b.Kind + " '" + b.Get("name") + "' (line " + b.SourceLine + ") has no rows");
            return blocks;
        }
    }
}

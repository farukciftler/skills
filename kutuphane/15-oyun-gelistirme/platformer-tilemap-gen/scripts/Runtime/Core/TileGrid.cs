// PlatformerGen Core — pure C#, no UnityEngine dependency (compiles in Unity and plain .NET/Mono).
// Coordinate convention: x grows right, y grows UP, (0,0) is bottom-left. Matches Unity Tilemap cells.
using System;
using System.Collections.Generic;

namespace PlatformerGen
{
    /// <summary>Semantic cell kinds. The generator decides semantics; the Unity adapter maps them to tiles/layers.</summary>
    public enum Cell : byte
    {
        Empty = 0,
        Solid = 1,     // full collision (ground/walls)
        OneWay = 2,    // jump-through platform, collides only from above
        Hazard = 3,    // spikes/lava — touching = death
        Ladder = 4,    // climbable, no collision
        Spawn = 5,     // marker (no collision)
        Exit = 6,      // marker (no collision)
        Pickup = 7,    // marker (no collision)
        Enemy = 8,     // marker (no collision)
        Breakable = 9, // collides like Solid, may be destroyed at runtime
        Decor = 10     // visual only
    }

    public static class CellRules
    {
        public static bool IsSolid(Cell c) { return c == Cell.Solid || c == Cell.Breakable; }
        public static bool IsSupport(Cell c) { return IsSolid(c) || c == Cell.OneWay; }
        public static bool IsMarker(Cell c) { return c == Cell.Spawn || c == Cell.Exit || c == Cell.Pickup || c == Cell.Enemy; }
        /// <summary>A body may occupy this cell without colliding and without dying.</summary>
        public static bool IsPassable(Cell c) { return !IsSolid(c) && c != Cell.Hazard; }
    }

    public sealed class TileGrid
    {
        public readonly int Width;
        public readonly int Height;
        private readonly Cell[] _cells;

        /// <summary>What Get() returns outside the grid. Solid = closed box (default), Empty = open edges.</summary>
        public Cell OutOfBounds = Cell.Solid;

        public TileGrid(int width, int height, Cell fill = Cell.Empty)
        {
            if (width <= 0 || height <= 0) throw new ArgumentException("Grid size must be positive");
            Width = width; Height = height;
            _cells = new Cell[width * height];
            if (fill != Cell.Empty) for (int i = 0; i < _cells.Length; i++) _cells[i] = fill;
        }

        public bool InBounds(int x, int y) { return x >= 0 && y >= 0 && x < Width && y < Height; }
        public int Index(int x, int y) { return y * Width + x; }

        public Cell Get(int x, int y) { return InBounds(x, y) ? _cells[y * Width + x] : OutOfBounds; }
        public void Set(int x, int y, Cell c) { if (InBounds(x, y)) _cells[y * Width + x] = c; }

        /// <summary>Raw row-major buffer (index = y*Width + x). Same order as Unity's SetTilesBlock for a z=1 BoundsInt.</summary>
        public Cell[] Raw { get { return _cells; } }

        public void Fill(int x0, int y0, int w, int h, Cell c)
        {
            for (int y = y0; y < y0 + h; y++)
                for (int x = x0; x < x0 + w; x++) Set(x, y, c);
        }

        public void Border(Cell c = Cell.Solid)
        {
            for (int x = 0; x < Width; x++) { Set(x, 0, c); Set(x, Height - 1, c); }
            for (int y = 0; y < Height; y++) { Set(0, y, c); Set(Width - 1, y, c); }
        }

        /// <summary>Copies src into this grid at (ox, oy). Cells equal to 'transparent' in src are skipped.</summary>
        public void Blit(TileGrid src, int ox, int oy, bool skipEmpty = false)
        {
            for (int y = 0; y < src.Height; y++)
                for (int x = 0; x < src.Width; x++)
                {
                    Cell c = src.Get(x, y);
                    if (skipEmpty && c == Cell.Empty) continue;
                    Set(ox + x, oy + y, c);
                }
        }

        public TileGrid Clone()
        {
            var g = new TileGrid(Width, Height);
            Array.Copy(_cells, g._cells, _cells.Length);
            g.OutOfBounds = OutOfBounds;
            return g;
        }

        public TileGrid MirrorX()
        {
            var g = new TileGrid(Width, Height);
            for (int y = 0; y < Height; y++)
                for (int x = 0; x < Width; x++) g.Set(Width - 1 - x, y, Get(x, y));
            g.OutOfBounds = OutOfBounds;
            return g;
        }

        public List<Int2> FindAll(Cell c)
        {
            var list = new List<Int2>();
            for (int y = 0; y < Height; y++)
                for (int x = 0; x < Width; x++) if (_cells[y * Width + x] == c) list.Add(new Int2(x, y));
            return list;
        }

        public int Count(Cell c)
        {
            int n = 0;
            for (int i = 0; i < _cells.Length; i++) if (_cells[i] == c) n++;
            return n;
        }

        /// <summary>Replace every marker of kind c with Empty.</summary>
        public void ClearMarkers(Cell c)
        {
            for (int i = 0; i < _cells.Length; i++) if (_cells[i] == c) _cells[i] = Cell.Empty;
        }
    }

    /// <summary>Minimal int vector so Core stays engine-free. Convert to Vector3Int in the adapter.</summary>
    public struct Int2 : IEquatable<Int2>
    {
        public int x, y;
        public Int2(int x, int y) { this.x = x; this.y = y; }
        public bool Equals(Int2 o) { return x == o.x && y == o.y; }
        public override bool Equals(object obj) { return obj is Int2 && Equals((Int2)obj); }
        public override int GetHashCode() { return (x * 73856093) ^ (y * 19349663); }
        public override string ToString() { return "(" + x + "," + y + ")"; }
    }
}

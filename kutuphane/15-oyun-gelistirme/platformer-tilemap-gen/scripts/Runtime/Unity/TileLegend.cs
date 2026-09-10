using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Tilemaps;

namespace PlatformerGen.Integration
{
    /// <summary>Which Tilemap a cell kind is written to. Each layer gets its own collider setup.</summary>
    public enum LevelLayer { Ground = 0, OneWay = 1, Hazard = 2, Ladder = 3, Decor = 4, Entities = 5 }

    /// <summary>
    /// Maps semantic cells (Core.Cell) to tile assets and target layers. Point Solid at a RuleTile /
    /// AutoTile so edges and corners resolve automatically after SetTilesBlock.
    /// Markers (Spawn/Exit/Pickup/Enemy) map to prefabs instead of tiles.
    /// </summary>
    [CreateAssetMenu(menuName = "PlatformerGen/Tile Legend", fileName = "TileLegend")]
    public sealed class TileLegend : ScriptableObject
    {
        [Serializable]
        public sealed class Entry
        {
            public Cell cell = Cell.Solid;
            public TileBase tile;
            public LevelLayer layer = LevelLayer.Ground;
            [Tooltip("Markers only: prefab spawned at the cell centre.")]
            public GameObject prefab;
            [Tooltip("Hazards only: rotate the tile to face away from the adjacent solid (floor/ceiling/wall spikes).")]
            public bool autoOrient = true;
        }

        public List<Entry> entries = new List<Entry>
        {
            new Entry { cell = Cell.Solid, layer = LevelLayer.Ground },
            new Entry { cell = Cell.Breakable, layer = LevelLayer.Ground },
            new Entry { cell = Cell.OneWay, layer = LevelLayer.OneWay },
            new Entry { cell = Cell.Hazard, layer = LevelLayer.Hazard },
            new Entry { cell = Cell.Ladder, layer = LevelLayer.Ladder },
            new Entry { cell = Cell.Decor, layer = LevelLayer.Decor },
            new Entry { cell = Cell.Spawn, layer = LevelLayer.Entities },
            new Entry { cell = Cell.Exit, layer = LevelLayer.Entities },
            new Entry { cell = Cell.Pickup, layer = LevelLayer.Entities },
            new Entry { cell = Cell.Enemy, layer = LevelLayer.Entities },
        };

        public Entry Find(Cell c)
        {
            for (int i = 0; i < entries.Count; i++) if (entries[i].cell == c) return entries[i];
            return null;
        }

        /// <summary>Reverse lookup for reading hand-painted tilemaps. Unknown tiles fall back to the layer's default kind.</summary>
        public Cell Reverse(TileBase tile, LevelLayer layer)
        {
            if (tile == null) return Cell.Empty;
            for (int i = 0; i < entries.Count; i++)
                if (entries[i].tile == tile && entries[i].layer == layer) return entries[i].cell;
            switch (layer)
            {
                case LevelLayer.Ground: return Cell.Solid;
                case LevelLayer.OneWay: return Cell.OneWay;
                case LevelLayer.Hazard: return Cell.Hazard;
                case LevelLayer.Ladder: return Cell.Ladder;
                default: return Cell.Decor;
            }
        }

        /// <summary>Lists what is not wired yet, so callers can fail loudly instead of writing an invisible level.</summary>
        public List<string> MissingAssignments()
        {
            var list = new List<string>();
            foreach (var e in entries)
            {
                if (e.layer == LevelLayer.Entities) continue;
                if (e.tile == null && (e.cell == Cell.Solid || e.cell == Cell.OneWay || e.cell == Cell.Hazard || e.cell == Cell.Ladder))
                    list.Add(e.cell + " has no tile");
            }
            return list;
        }
    }
}

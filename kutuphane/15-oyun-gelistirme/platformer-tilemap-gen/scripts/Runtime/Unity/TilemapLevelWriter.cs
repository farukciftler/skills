using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Tilemaps;

namespace PlatformerGen.Integration
{
    [Serializable]
    public sealed class WriteStats
    {
        public int tilesWritten;
        public int entitiesSpawned;
        public bool hasSpawn;
        public Vector3 spawnWorld;
        public bool hasExit;
        public Vector3 exitWorld;
        public List<string> warnings = new List<string>();
    }

    public sealed class WriteOptions
    {
        public bool clearFirst = true;          // wipe all layers + Entities before writing
        public bool spawnEntities = true;       // instantiate marker prefabs
        public bool rebuildColliders = true;    // one composite rebuild after the batch instead of per-change
        /// <summary>Editor passes PrefabUtility.InstantiatePrefab here to keep prefab links; runtime uses Object.Instantiate.</summary>
        public Func<GameObject, Transform, GameObject> instantiate;
        /// <summary>Editor passes Undo.DestroyObjectImmediate so clearing old entities is undoable.</summary>
        public Action<GameObject> destroy;
    }

    /// <summary>
    /// Writes a Core TileGrid into LevelLayers in one batch per layer (SetTilesBlock), then rebuilds
    /// colliders once. Never loop SetTile over a big grid with a Synchronous composite: every change
    /// re-triggers geometry generation and a 200x50 level can stall for seconds.
    /// </summary>
    public static class TilemapLevelWriter
    {
        public static WriteStats Write(TileGrid grid, LevelLayers layers, TileLegend legend, Vector3Int origin, WriteOptions opt = null)
        {
            if (grid == null) throw new ArgumentNullException("grid");
            if (layers == null) throw new ArgumentNullException("layers");
            if (legend == null) throw new ArgumentNullException("legend");
            opt = opt ?? new WriteOptions();
            var stats = new WriteStats();
            foreach (var m in legend.MissingAssignments()) stats.warnings.Add("Legend: " + m);

            int w = grid.Width, h = grid.Height;
            var bounds = new BoundsInt(origin.x, origin.y, 0, w, h, 1);
            var composites = new List<KeyValuePair<CompositeCollider2D, CompositeCollider2D.GenerationType>>();

            // 1) pause composite generation so the batch doesn't trigger N rebuilds
            foreach (var tm in layers.All())
            {
                if (tm == null) continue;
                var comp = tm.GetComponent<CompositeCollider2D>();
                if (comp != null && opt.rebuildColliders)
                {
                    composites.Add(new KeyValuePair<CompositeCollider2D, CompositeCollider2D.GenerationType>(comp, comp.generationType));
                    comp.generationType = CompositeCollider2D.GenerationType.Manual;
                }
                if (opt.clearFirst) tm.ClearAllTiles();
            }
            if (opt.clearFirst && layers.entities != null)
                for (int i = layers.entities.childCount - 1; i >= 0; i--)
                {
                    var child = layers.entities.GetChild(i).gameObject;
                    if (opt.destroy != null) opt.destroy(child); else DestroySafe(child);
                }

            // 2) one array per layer, one SetTilesBlock per layer (array index = x + y*w, same as TileGrid.Raw)
            var perLayer = new Dictionary<LevelLayer, TileBase[]>();
            var raw = grid.Raw;
            var hazardCells = new List<Vector3Int>();
            Tilemap reference = layers.ground;
            for (int i = 0; i < raw.Length; i++)
            {
                Cell c = raw[i];
                if (c == Cell.Empty) continue;
                var entry = legend.Find(c);
                int x = i % w, y = i / w;
                if (CellRules.IsMarker(c))
                {
                    var pos = new Vector3Int(origin.x + x, origin.y + y, 0);
                    Vector3 world = reference.GetCellCenterWorld(pos);
                    if (c == Cell.Spawn) { stats.hasSpawn = true; stats.spawnWorld = world; }
                    if (c == Cell.Exit) { stats.hasExit = true; stats.exitWorld = world; }
                    if (opt.spawnEntities && entry != null && entry.prefab != null && layers.entities != null)
                    {
                        var inst = opt.instantiate != null ? opt.instantiate(entry.prefab, layers.entities) : UnityEngine.Object.Instantiate(entry.prefab, layers.entities);
                        inst.transform.position = world;
                        var mk = inst.GetComponent<LevelMarker>();          // no '??' on UnityEngine.Object (fake-null in Editor)
                        if (mk == null) mk = inst.AddComponent<LevelMarker>();
                        mk.kind = c;
                        stats.entitiesSpawned++;
                    }
                    else if (opt.spawnEntities && layers.entities != null && (c == Cell.Spawn || c == Cell.Exit))
                    {
                        // no prefab: still leave an empty marker so the level can be read back/validated
                        var go = new GameObject(c.ToString());
                        go.transform.SetParent(layers.entities, false);
                        go.transform.position = world;
                        go.AddComponent<LevelMarker>().kind = c;
                        stats.entitiesSpawned++;
                    }
                    continue;
                }
                if (entry == null || entry.tile == null) continue;
                TileBase[] arr;
                if (!perLayer.TryGetValue(entry.layer, out arr)) { arr = new TileBase[w * h]; perLayer[entry.layer] = arr; }
                arr[i] = entry.tile;
                stats.tilesWritten++;
                if (c == Cell.Hazard && entry.autoOrient) hazardCells.Add(new Vector3Int(x, y, 0));
            }

            foreach (var kv in perLayer)
            {
                var tm = layers.Get(kv.Key);
                if (tm == null) { stats.warnings.Add("No Tilemap for layer " + kv.Key); continue; }
                if (opt.clearFirst) tm.SetTilesBlock(bounds, kv.Value);
                else WriteNonNull(tm, bounds, kv.Value); // additive: don't erase neighbours with nulls
            }

            // 3) orient hazards away from the solid they're attached to (floor, ceiling, walls)
            if (hazardCells.Count > 0 && layers.hazard != null)
            {
                foreach (var hc in hazardCells)
                {
                    float angle = HazardAngle(grid, hc.x, hc.y);
                    if (angle == 0f) continue;
                    var pos = new Vector3Int(origin.x + hc.x, origin.y + hc.y, 0);
                    layers.hazard.RemoveTileFlags(pos, TileFlags.LockTransform);
                    layers.hazard.SetTransformMatrix(pos, Matrix4x4.TRS(Vector3.zero, Quaternion.Euler(0, 0, angle), Vector3.one));
                }
            }

            // 4) colliders: flush tile changes, build each composite once, restore generation mode
            foreach (var tm in layers.All())
            {
                if (tm == null) continue;
                var tc = tm.GetComponent<TilemapCollider2D>();
                if (tc != null) tc.ProcessTilemapChanges();
            }
            foreach (var kv in composites)
            {
                kv.Key.GenerateGeometry();
                kv.Key.generationType = kv.Value;
            }
            foreach (var tm in layers.All()) if (tm != null) tm.CompressBounds();

            if (!stats.hasSpawn) stats.warnings.Add("Grid has no Spawn marker.");
            if (!stats.hasExit) stats.warnings.Add("Grid has no Exit marker.");
            return stats;
        }

        /// <summary>Erase a rectangular region on every layer (endless streaming: unload behind the camera).</summary>
        public static void ClearRegion(LevelLayers layers, BoundsInt region)
        {
            var empty = new TileBase[region.size.x * region.size.y * Math.Max(1, region.size.z)];
            foreach (var tm in layers.All()) if (tm != null) tm.SetTilesBlock(region, empty);
        }

        private static void WriteNonNull(Tilemap tm, BoundsInt bounds, TileBase[] arr)
        {
            var positions = new List<Vector3Int>();
            var tiles = new List<TileBase>();
            for (int i = 0; i < arr.Length; i++)
            {
                if (arr[i] == null) continue;
                positions.Add(new Vector3Int(bounds.xMin + i % bounds.size.x, bounds.yMin + i / bounds.size.x, 0));
                tiles.Add(arr[i]);
            }
            tm.SetTiles(positions.ToArray(), tiles.ToArray());
        }

        /// <summary>Spikes point away from support: floor=0°, ceiling=180°, left wall=-90°, right wall=90°.
        /// Assumes the hazard sprite points UP with a centred pivot.</summary>
        public static float HazardAngle(TileGrid g, int x, int y)
        {
            if (CellRules.IsSolid(g.Get(x, y - 1))) return 0f;
            if (CellRules.IsSolid(g.Get(x, y + 1))) return 180f;
            if (CellRules.IsSolid(g.Get(x - 1, y))) return -90f;
            if (CellRules.IsSolid(g.Get(x + 1, y))) return 90f;
            return 0f;
        }

        private static void DestroySafe(GameObject go)
        {
            if (Application.isPlaying) UnityEngine.Object.Destroy(go);
            else UnityEngine.Object.DestroyImmediate(go);
        }
    }

    /// <summary>Reads hand-painted (or previously generated) tilemaps back into a TileGrid for validation.
    /// This is how non-procedural levels get the same playability guarantee as generated ones.</summary>
    public static class TilemapLevelReader
    {
        public static TileGrid Read(LevelLayers layers, TileLegend legend, out Vector3Int origin)
        {
            BoundsInt b = default(BoundsInt);
            bool any = false;
            foreach (var tm in layers.All())
            {
                if (tm == null) continue;
                tm.CompressBounds();
                var cb = tm.cellBounds;
                if (cb.size.x == 0 || cb.size.y == 0) continue;
                b = any ? Union(b, cb) : cb; any = true;
            }
            // markers (Spawn/Exit...) may sit outside the painted tiles — include them
            var markers = layers.entities != null ? layers.entities.GetComponentsInChildren<LevelMarker>() : new LevelMarker[0];
            foreach (var mk in markers)
            {
                var c = layers.ground.WorldToCell(mk.transform.position);
                var one = new BoundsInt(c.x, c.y, 0, 1, 1, 1);
                b = any ? Union(b, one) : one; any = true;
            }
            if (!any) { origin = Vector3Int.zero; return new TileGrid(1, 1); }
            b = new BoundsInt(b.xMin, b.yMin, 0, b.size.x, b.size.y, 1);
            origin = new Vector3Int(b.xMin, b.yMin, 0);
            var grid = new TileGrid(b.size.x, b.size.y);
            grid.OutOfBounds = Cell.Empty; // painted levels: outside the paint is open air unless you paint walls

            // precedence: Ground > Hazard > OneWay > Ladder > Decor
            LevelLayer[] order = { LevelLayer.Decor, LevelLayer.Ladder, LevelLayer.OneWay, LevelLayer.Hazard, LevelLayer.Ground };
            foreach (var layer in order)
            {
                var tm = layers.Get(layer);
                if (tm == null) continue;
                var tiles = tm.GetTilesBlock(b);
                for (int i = 0; i < tiles.Length; i++)
                {
                    if (tiles[i] == null) continue;
                    Cell c = legend.Reverse(tiles[i], layer);
                    if (c == Cell.Decor) continue;
                    grid.Raw[i] = c;
                }
            }
            {
                foreach (var mk in markers)
                {
                    var cell = layers.ground.WorldToCell(mk.transform.position);
                    int x = cell.x - origin.x, y = cell.y - origin.y;
                    if (grid.InBounds(x, y) && grid.Get(x, y) == Cell.Empty) grid.Set(x, y, mk.kind);
                }
            }
            return grid;
        }

        private static BoundsInt Union(BoundsInt a, BoundsInt c)
        {
            int xMin = Math.Min(a.xMin, c.xMin), yMin = Math.Min(a.yMin, c.yMin);
            int xMax = Math.Max(a.xMax, c.xMax), yMax = Math.Max(a.yMax, c.yMax);
            return new BoundsInt(xMin, yMin, 0, xMax - xMin, yMax - yMin, 1);
        }
    }
}

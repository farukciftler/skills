using System;
using UnityEngine;
using UnityEngine.Tilemaps;

namespace PlatformerGen.Integration
{
    /// <summary>
    /// Lives on the Grid root. Owns one Tilemap per LevelLayer, each with the collider setup a
    /// platformer needs (Unity 6 API: Collider2D.compositeOperation, not the removed usedByComposite):
    ///   Ground : TilemapCollider2D(Merge) + CompositeCollider2D(Polygons) + static Rigidbody2D
    ///   OneWay : same + PlatformEffector2D(useOneWay) with composite.usedByEffector
    ///   Hazard : same, composite.isTrigger (touch = death, handled by your hazard script)
    ///   Ladder : TilemapCollider2D trigger (climb zones)
    ///   Decor  : renderer only
    /// Composite merging removes the internal edges between tiles that make characters snag
    /// ("ghost collisions") when running across a tile floor.
    /// </summary>
    [DisallowMultipleComponent]
    public sealed class LevelLayers : MonoBehaviour
    {
        public Tilemap ground, oneWay, hazard, ladder, decor;
        public Transform entities;

        public Tilemap Get(LevelLayer layer)
        {
            switch (layer)
            {
                case LevelLayer.Ground: return ground;
                case LevelLayer.OneWay: return oneWay;
                case LevelLayer.Hazard: return hazard;
                case LevelLayer.Ladder: return ladder;
                case LevelLayer.Decor: return decor;
                default: return null;
            }
        }

        public Tilemap[] All() { return new[] { ground, oneWay, hazard, ladder, decor }; }

        /// <summary>Create/repair the standard hierarchy under a Grid. Idempotent. onCreated lets the Editor register Undo.</summary>
        public static LevelLayers EnsureOn(Grid grid, Action<GameObject> onCreated = null)
        {
            var layers = grid.GetComponent<LevelLayers>();
            if (layers == null) layers = grid.gameObject.AddComponent<LevelLayers>();
            if (layers.ground == null) layers.ground = MakeTilemap(grid, "Ground", 0, LevelLayer.Ground, onCreated);
            if (layers.oneWay == null) layers.oneWay = MakeTilemap(grid, "OneWay", 0, LevelLayer.OneWay, onCreated);
            if (layers.hazard == null) layers.hazard = MakeTilemap(grid, "Hazard", 1, LevelLayer.Hazard, onCreated);
            if (layers.ladder == null) layers.ladder = MakeTilemap(grid, "Ladder", -1, LevelLayer.Ladder, onCreated);
            if (layers.decor == null) layers.decor = MakeTilemap(grid, "Decor", -2, LevelLayer.Decor, onCreated);
            if (layers.entities == null)
            {
                var go = new GameObject("Entities");
                go.transform.SetParent(grid.transform, false);
                if (onCreated != null) onCreated(go);
                layers.entities = go.transform;
            }
            return layers;
        }

        private static Tilemap MakeTilemap(Grid grid, string name, int sortingOrder, LevelLayer layer, Action<GameObject> onCreated)
        {
            var existing = grid.transform.Find(name);
            if (existing != null && existing.GetComponent<Tilemap>() != null) return existing.GetComponent<Tilemap>();

            var go = new GameObject(name);
            go.transform.SetParent(grid.transform, false);
            var tm = go.AddComponent<Tilemap>();
            var tr = go.AddComponent<TilemapRenderer>();
            tr.sortingOrder = sortingOrder;
            tr.mode = TilemapRenderer.Mode.Chunk; // fastest; switch to Individual only if sprites must interleave with tiles

            if (layer == LevelLayer.Decor) { if (onCreated != null) onCreated(go); return tm; }

            var tc = go.AddComponent<TilemapCollider2D>();
            if (layer == LevelLayer.Ladder)
            {
                tc.isTrigger = true;
                if (onCreated != null) onCreated(go);
                return tm;
            }

            var rb = go.AddComponent<Rigidbody2D>();
            rb.bodyType = RigidbodyType2D.Static;
            var comp = go.AddComponent<CompositeCollider2D>();
            comp.geometryType = CompositeCollider2D.GeometryType.Polygons; // solid shapes: no tunnelling, OverlapPoint works inside
            tc.compositeOperation = Collider2D.CompositeOperation.Merge;

            if (layer == LevelLayer.OneWay)
            {
                var eff = go.AddComponent<PlatformEffector2D>();
                eff.useOneWay = true;
                eff.surfaceArc = 170f;
                comp.usedByEffector = true;
            }
            if (layer == LevelLayer.Hazard) comp.isTrigger = true;

            if (onCreated != null) onCreated(go);
            return tm;
        }
    }
}

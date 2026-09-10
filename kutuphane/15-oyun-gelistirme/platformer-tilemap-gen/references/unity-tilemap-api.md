# Unity Tilemap & 2D physics API notes (Unity 6.x)

Verified against docs.unity3d.com for 6000.0 → 6000.6 (Sept 2026). When a detail matters for the user's
exact Editor version, open the doc page for that version — Unity 6 minor releases do change APIs.

## Contents
1. Versions & packages · 2. Writing tiles fast · 3. Reading tiles · 4. Colliders · 5. Rendering & seams
6. RuleTile vs AutoTile · 7. Editor-time generation (Undo, dirty, prefabs) · 8. Runtime generation & perf

## 1. Versions & packages
- Unity 6.3 LTS (6000.3) is the conservative baseline; 6.5 is the current Supported stream at time of writing.
- `com.unity.2d.tilemap` (Tile Palette/editor) + built-in tilemap module (runtime API).
- `com.unity.2d.tilemap.extras` — RuleTile, AutoTile (added 4.2.0), AnimatedTile, RuleOverrideTile, GameObject/Random/Line
  brushes, GridInformation. Its major version tracks the Editor (≈4.x on 6000.0 … 8.x/9.x on 6000.5+). **Read
  `Packages/manifest.json`; never hardcode a version.**
- `com.unity.pipeline` — Unity CLI bridge; needed only for `pgen_*` commands (Unity 6.0+).

## 2. Writing tiles fast
- `Tilemap.SetTilesBlock(BoundsInt, TileBase[])`: array length must equal bounds volume; iteration order is x fastest,
  then y, then z → index `x + y*w` for z-size 1, identical to `TileGrid.Raw`. Null entries **erase** cells, so for
  additive writes use `SetTiles(Vector3Int[], TileBase[])` with only non-null tiles (the writer's `clearFirst=false` path).
- `SetTiles(TileChangeData[], ignoreLockFlags)` sets tile + color + transform in one call (use for tinted/rotated tiles).
- Unity 6.5+: native overloads — `SetTiles(NativeArray<Vector3Int>, Tilemap.TileArray)`, plus colour/transform arrays and
  `SetTilesBlock(BoundsInt, TileArray)`. Worth it for per-frame streaming or Burst jobs that build grids; wrap in
  `#if UNITY_6000_5_OR_NEWER`. The shipped writer keeps the managed path so it compiles on every 6.x.
- Anti-pattern: `SetTile` in nested loops on a large map (each call refreshes neighbours and dirties collider state).
- `ClearAllTiles()` then write; `CompressBounds()` afterwards so `cellBounds` is tight.
- Rotating a tile: `RemoveTileFlags(pos, TileFlags.LockTransform)` then `SetTransformMatrix(pos, Matrix4x4.TRS(...))`.
  Rotation happens around the tile anchor → hazard sprites need a centred pivot.

## 3. Reading tiles
- `GetTilesBlock(bounds)` returns the same x-fastest order. Union the `cellBounds` of all layers (after `CompressBounds`)
  plus entity marker cells, as `TilemapLevelReader` does.
- `WorldToCell` / `GetCellCenterWorld` for entity ↔ cell mapping.

## 4. Colliders (platformer setup)
- Unity 6: `Collider2D.compositeOperation` (None/Merge/Intersect/Difference/Flip) replaces the old `usedByComposite`
  bool. With any op other than None, the collider feeds its GameObject's `CompositeCollider2D`; `isTrigger`,
  `sharedMaterial` and `usedByEffector` are then read **from the composite**, not the tilemap collider.
- `TilemapCollider2D`: `maximumTileChangeCount` (default 1000) — beyond it a full rebuild replaces incremental updates;
  `extrusionFactor` (only with a composite) closes hairline gaps between tile shapes; `useDelaunayMesh`;
  `ProcessTilemapChanges()` to flush immediately (the writer calls it before building composites).
- `CompositeCollider2D`: `generationType` Synchronous (rebuild on every change) vs Manual (`GenerateGeometry()`).
  Bulk writes: Manual → write → `GenerateGeometry()` → restore. `geometryType`: Polygons = solid (no tunnelling,
  `OverlapPoint` works inside, triggers fire when fully inside); Outlines = hollow edges (cheaper, can tunnel).
- Merging removes internal edges between tiles → no "ghost collisions" snagging a box collider running on the floor.
- One-way: `PlatformEffector2D.useOneWay = true` (surfaceArc ~170–180) + `composite.usedByEffector = true`.
  Drop-through: temporarily disable collision (e.g. `Physics2D.IgnoreCollision` for 0.25 s or flip the effector's rotationalOffset).
- Hazards: separate Tilemap, composite `isTrigger`, your hazard script handles damage. Ladders: trigger zones.
- Unity 6.3 LTS also adds a low-level 2D physics API on Box2D v3 (`UnityEngine.LowLevelPhysics2D`) — component-free,
  multithreaded. The Rigidbody2D/Collider2D path above is still the one tilemaps integrate with; consider the low-level API
  only for custom physics systems.

## 5. Rendering & seams
- `TilemapRenderer.Mode`: Chunk (default, fastest, one sort item — other sprites can't interleave), Individual (per-tile
  sorting, slower), SRPBatch (chunks batched via the SRP Batcher — good with URP; falls back to dynamic batching otherwise).
- Chunk mode + tiles from multiple textures sorts inconsistently → pack all tiles into one Sprite Atlas.
- Lines/gaps between tiles: point filtering + no mipmaps + no compression for pixel art, Pixel Perfect Camera, atlas
  padding ≥ 2 and "alpha dilation", Sprite Mesh Type = Full Rect, consistent PPU, camera position snapped. Last-resort
  hack: Grid `cellGap` ≈ -0.001 (hides symptoms). Delegate pixel-art camera setup to the `2d-pixel-perfect` skill.

## 6. RuleTile vs AutoTile vs precomputed sprites
- **RuleTile**: neighbour rules per tile asset, evaluated on refresh; batch writes still resolve correctly because
  neighbours refresh after `SetTilesBlock`. Only sees tiles **of the same RuleTile on the same Tilemap** — that's why
  Ground/OneWay/Hazard live on separate layers with separate tiles.
- **AutoTile** (Extras 4.2+): bitmask-driven, set up from a tileset texture + template; optional Random per mask (5.0+),
  physics-shape handling (6.0.1+). Faster to author for standard 47/16-tile sets.
- **Precomputed sprites**: for very large runtime maps compute the 8-neighbour mask in Core and write plain `Tile`s —
  avoids rule evaluation cost; lose live auto-tiling when painting. Only do this after profiling.
- Rule/AutoTile creation from a tileset: Unity plugin skills `sprite-segment-3x3grid` → `tilemap-ruletile-createfromsegment`.

## 7. Editor-time generation
- `Undo.RegisterCompleteObjectUndo(tilemaps+composites)` before writing; `Undo.RegisterCreatedObjectUndo` for new
  objects; `Undo.DestroyObjectImmediate` for removed entities; `EditorSceneManager.MarkSceneDirty(scene)` after.
- `PrefabUtility.InstantiatePrefab` (keeps prefab links) instead of `Object.Instantiate` in the Editor.
- `Object.FindAnyObjectByType<T>()` (FindObjectOfType is obsolete in 6.x).
- ScriptableObject/MonoBehaviour classes must live in a file with the same name.
- `GetComponent<T>()` can return an Editor "fake null": use `== null`, never `??` / `?.` on UnityEngine.Object.

## 8. Runtime generation & performance
- Generation cost measured with Mono in a sandbox (Unity/IL2CPP is typically faster): 4×4 room grid ≈ 15 ms incl. validation;
  140-wide chunk level ≈ 18 ms; 150×28 heightmap ≈ 18 ms; 60×36 cave ≈ 58 ms (validator used twice). Fine at load time; for mid-game streaming generate on a background thread
  (Core is thread-safe per instance, no Unity API) and only call the writer on the main thread.
- Collider rebuild is usually the dominant cost for big maps — batch, Manual composites, or split into several Tilemaps
  (e.g. per room/segment) so a change rebuilds a small composite.
- Rigidbody2D in Unity 6: `linearVelocity` (not `velocity`).

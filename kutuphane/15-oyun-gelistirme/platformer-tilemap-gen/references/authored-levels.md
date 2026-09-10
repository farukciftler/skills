# Authored (non-procedural) levels

Hand-made levels go through the same `TileGrid → validate → write` pipeline, so they get the same guarantees
and Claude can read, write and diff them as text.

## Contents
1. ASCII level format · 2. Template file format · 3. Hand-painted Tilemaps · 4. LDtk / Tiled · 5. Image → level · 6. Hybrid workflows

## 1. ASCII level format (`AsciiLevel`)
Rows TOP first; grid stored bottom-up ((0,0) = bottom-left = Unity cell origin). Blank lines and `//` lines are ignored.
| Glyph | Cell | Glyph | Cell |
|---|---|---|---|
| `.` or space | Empty | `S` | Spawn marker |
| `#` | Solid | `E` | Exit marker |
| `=` | OneWay | `$` | Pickup marker |
| `^` | Hazard | `e` | Enemy marker |
| `H` | Ladder | `B` | Breakable (collides like Solid) |
| `~` | Decor | `?` / `!` | 50% Solid / 50% Hazard per seed |
Custom glyphs: `AsciiLevel.Parse(text, rng, new Dictionary<char, Cell>{{'X', Cell.Solid}})`.
Use as a full level: `LevelGenConfig.algorithm = AsciiLevel`, `templates` = the .txt TextAsset
(probabilistic glyphs resolved by the config seed). Claude can author a level directly as ASCII, validate it with the
harness (`mono h.exe validate level.txt`) before Unity is even open, then `pgen_generate` writes it.

Example — also shipped as `assets/example-level.txt` (validated with the default profile: PASS, coverage 100%, pickup reachable):
```
..........................
..........................
..........$...........E...
.........===......######..
S.....##.........##.......
####..####^^.#############
##########################
```

## 2. Template file format (`TemplateFile`)
```
// comment (NOT '#': '#' is the Solid glyph)
@room name=lr_bumps exits=LR weight=2 mirror=1 tags=easy
##########
...
@chunk name=pit_jump difficulty=2 weight=2
............
```
- `@room`: `exits` any of L R U D ("" = filler), `weight`, `mirror` (default 1), `tags`. All rooms same size (config `roomW/roomH`).
- `@chunk`: `difficulty` (0–10), `weight`. Same height for all chunks; first & last column must contain a resting spot.
- Unknown attributes are kept in `TemplateBlock.Attr` for custom generators.
- Parser errors name the block and line — pass them to the user verbatim.

## 3. Hand-painted Tilemaps (designer workflow)
1. `pgen_setup` / menu → Grid with Ground, OneWay, Hazard, Ladder, Decor tilemaps (correct colliders). Or add
   `LevelLayers` to an existing Grid and assign its Tilemaps.
2. Paint with the Tile Palette (RuleTile/AutoTile on Ground). Place Spawn/Exit as GameObjects with `LevelMarker`
   under `Entities` (or any child of it).
3. `pgen_validate --config <asset>` → report + ASCII overlay; `pgen_ascii` dumps the painted level as text so Claude
   can reason about it, propose edits as ASCII diffs, and write them back via an AsciiLevel config.
Reader rules: layer decides the cell kind unless the tile appears in the legend; precedence Ground > Hazard > OneWay >
Ladder; outside the painted area is open air (`OutOfBounds = Empty`) — paint the boundary walls.

## 4. LDtk / Tiled
- **LDtk**: use LDtkToUnity (ScriptedImporter; re-imports on save; IntGrid values, auto-layers, entities, animated tiles,
  optional composite collider). Map IntGrid values → Cells (e.g. 1 = Solid, 2 = OneWay, 3 = Hazard) by reading the
  imported IntGrid layer component, or simply point `LevelLayers` at the imported Tilemaps and validate with the reader.
  LDtk's own rule-based auto-layers can replace RuleTiles.
- **Tiled**: SuperTiled2Unity imports .tmx into Tilemaps; same approach (point `LevelLayers` at them, validate).
- Don't write a custom LDtk/Tiled parser unless the importer is unavailable; if you must, LDtk's JSON `intGridCsv`
  is row-major from the TOP-LEFT — flip Y when filling a `TileGrid`.

## 5. Image → level (pixel-per-tile mockups)
Designers can sketch levels in any paint tool, one pixel per tile. Import (Editor script, texture needs Read/Write):
```csharp
static readonly Dictionary<Color32, Cell> Palette = new Dictionary<Color32, Cell> {
    { new Color32(0,0,0,255), Cell.Solid }, { new Color32(0,0,255,255), Cell.OneWay },
    { new Color32(255,0,0,255), Cell.Hazard }, { new Color32(0,255,0,255), Cell.Spawn },
    { new Color32(255,255,0,255), Cell.Exit } };
public static TileGrid FromTexture(Texture2D tex) {
    var px = tex.GetPixels32();                 // bottom-left origin, row-major: same as TileGrid
    var g = new TileGrid(tex.width, tex.height);
    for (int i = 0; i < px.Length; i++) { Cell c; if (Palette.TryGetValue(px[i], out c)) g.Raw[i] = c; }
    return g;
}
```
Import settings: Point filter, no compression, Read/Write enabled, non-power-of-2 = None.

## 6. Hybrid workflows (usually the best answer)
- **Generate → bake → polish**: generate in the Editor, keep the best seeds, let designers paint over, re-validate.
- **Authored critical path, procedural filler**: RoomGrid with designer-only path templates and generous filler.
- **Authored chunks, procedural order**: ChunkStitch with `BeatChance = 0` = pure authored content, random order.
- **Authored level, procedural dressing**: AsciiLevel for geometry, `GridPasses.Scatter` for pickups/enemies on reachable spots.

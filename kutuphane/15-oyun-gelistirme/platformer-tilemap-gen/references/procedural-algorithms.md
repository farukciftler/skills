# Procedural level algorithms for 2D platformers

## Contents
1. Decision matrix · 2. Room grid (Spelunky) · 3. Chunks + rhythm beats (Launchpad-lite) · 4. Constrained heightmap
5. Cellular-automata caves · 6. Graph + room templates (Dead Cells / Edgar) · 7. WFC · 8. Adding your own generator · 9. Tuning loop

## 1. Decision matrix
| Algorithm | Feels like | Designer control | Playability | Shipped here |
|---|---|---|---|---|
| Room grid + templates | Spelunky, roguelite caves | High (templates) | By contract + validator | `RoomGridGenerator` |
| Chunk stitch + beats | Mario-like linear, runners | High (chunks) + rules | By construction + validator | `ChunkStitchGenerator`, `ChunkStream` |
| Constrained heightmap | Terraria-ish surface strips | Medium (knobs) | By construction | `HeightmapGenerator` |
| CA caves + ledges | Organic caverns | Low | Exit placed at farthest reachable → always solvable | `CaveGenerator` |
| Graph + rooms | Dead Cells, metroidvanias | Very high | Graph guarantees connectivity | use Edgar-Unity or write one |
| WFC | "looks like the sample" | Medium | Not by default — needs path constraints | use DeBroglie |
| Grammar/rhythm | Launchpad research | High (grammar) | By construction | beats in ChunkStream |

Rule of thumb: the more a game depends on precise platforming, the more of the level should be hand-authored
(templates/chunks) and the less raw noise. Pure noise works for exploration, never for challenge.

## 2. Room grid (Spelunky-style) — `RoomGridGenerator`
Classic Spelunky: 4×4 rooms of 10×8 tiles; a solution path starts in a random top-row room and steps left/right
(40% each) or down (20%), dropping when it hits a wall; room types 0 (off-path), 1 (L+R), 2 (L+R+D, +U if the room
above is also a drop), 3 (L+R+U). Here generalised to an exit **mask** (L/R/U/D) per path room; any template whose
exits ⊇ mask fits, mirrored copies included (`mirror=1`). Off-path rooms take any template (filler), incl. closed ones.
- Knobs: `RoomsX/RoomsY`, `RoomW/RoomH`, `ChanceLeft/Right` (down = remainder), template weights/tags.
- Variety comes from (a) number of templates per mask (aim ≥ 4 each), (b) `?`/`!` probabilistic glyphs,
  (c) mirroring. Spelunky additionally stamps small obstacle "chunks" inside rooms — emulate with `?` clusters.
- Spawn/Exit: authored `S`/`E` in a template are kept only in start/end rooms; otherwise placed on a floor-level
  resting spot of the start/end room.
- Debug: `DescribeLastLayout()` prints the room path with required exits.

## 3. Chunks + rhythm beats — `ChunkStitchGenerator` / `ChunkStream`
Authored chunks (fixed height, any width) with auto-detected entry/exit ground heights; the stitcher shifts each chunk
vertically so entry = previous exit, extends solid bottoms downward and leaves non-solid bottoms as bottomless pits.
Between chunks, **beats** (Launchpad idea: generate the rhythm, then geometry that fits it): gap, step up (+gap),
step down (+gap), spike strip, one-way hop. Beat sizes come from the profile (`MaxGapTiles`, `MaxStepUpTiles`,
`MaxHazardRunTiles` × `BeatMargin`), so beats are playable by construction.
- Difficulty ramps `DifficultyStart → DifficultyEnd` over the level; chunks within `DifficultyTolerance` are eligible.
- Endless: `ChunkStream.Next(progress)` depends only on (seed, index, previous exit height) → `ChunkStreamer`
  writes ahead of the camera and clears behind. Same seed ⇒ same world.
- Knobs: `BeatChance` (0 = only authored chunks), `MinGround/MaxGround` (keep headroom), chunk weights.
- Common extension: new beat kinds (moving platform marker, spring, crumbling blocks = `Breakable`) — add a case in
  `ChunkStream.Beat` and size it from the profile.

## 4. Constrained heightmap — `HeightmapGenerator`
1D fractal value noise → quantised heights, then clamped: rise between columns ≤ `MaxStepUp`, pits only where landing
≤ takeoff and width ≤ `MaxGap`, one-way platforms at reachable heights, flat spawn/exit pads.
Knobs: `NoiseScale` (hill width), `Octaves`, `PitChance`, `PlatformChance`, `Margin`.

## 5. CA caves — `CaveGenerator`
Random fill (`FillChance` ≈ 0.45–0.5) → 4-5 rule iterations (wall if ≥ `BirthLimit` wall neighbours; stays wall if
≥ `SurviveLimit`) → keep the largest open region (flood fill) → **platformer pass**: tall open runs get one-way ledges
every `MaxStepUp` rows → Spawn at a top-left resting spot → Exit at the farthest *reachable* resting spot (validator
BFS), so solvability is guaranteed. Knobs: fill, iterations, limits, size. Cost is dominated by validation (twice).

## 6. Graph + room templates (Dead Cells / Edgar)
Dead Cells combines fixed hand-placed elements (a frame: level connections, key locations) with procedural layout
from hand-made rooms; the Edgar-Unity plugin reproduces this with a level graph (rooms + connections, room types) and
room templates with doors. When a user wants metroidvania structure (locks/keys, shops, boss rooms), recommend Edgar
(or ManiaMap), then convert its output into a `TileGrid` (read its tilemaps with `TilemapLevelReader`) and run the
validator on each room-to-room traversal. Writing a full graph-embedding solver is out of scope for this skill.

## 7. Wave Function Collapse
WFC generates outputs locally similar to an example; plain WFC gives up on contradictions and does not guarantee a
walkable path. DeBroglie adds backtracking and non-local constraints (path, fixed tiles, count). For platformers:
use WFC for texture/decoration or for room interiors with fixed entrance tiles + a path constraint, then validate.
Never ship raw WFC output as a challenge level.

## 8. Adding your own generator
```csharp
public sealed class MyGen : PlatformerGen.IGridGenerator {
    public string Name => "MyGen";
    public TileGrid Generate(Rng rng) {          // pure function of rng
        var g = new TileGrid(80, 20);
        var terrain = rng.Derive(1);             // one derived stream per pass
        ...                                       // write Cells, place Spawn + Exit
        return g;
    }
}
// then: GenerationPipeline.Run(new MyGen(), seed, profile, vopts, maxAttempts)
```
Wire it into `LevelGenConfig.CreateGenerator()` (new `GenAlgorithm` value) if designers should pick it in the Inspector.
Rules: size everything from `MovementProfile`; place Spawn and Exit; mark hazards as `Hazard`; never call Unity APIs in Core.

## 9. Tuning loop
1. `pgen_sweep` (or harness) over ≥ 100 seeds → first-try pass rate, attempts, ms.
2. < 90% first-try: inspect failures (`harness failures <kind>`), find the offending template/beat, fix the rule.
3. Look at 5–10 renders for *fun*, not just validity: `jumpsOnPath` too low = boring, `coverage` very low = wasted space.
4. Record the accepted seed/config in the level list so designers can reproduce and hand-polish.

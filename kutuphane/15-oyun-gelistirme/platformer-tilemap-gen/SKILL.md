---
name: platformer-tilemap-gen
description: Procedural AND hand-authored tilemap levels for 2D platformers in Unity 6, driven by Claude through the Unity plugin / Unity CLI (unity command, com.unity.pipeline). Tested engine-free C# core with Spelunky-style room grids, chunk+rhythm-beat linear/endless levels, constrained heightmaps, CA caves, ASCII levels, plus a physics-based reachability validator proving each level is finishable with the player's real jump; batched Tilemap writer with correct Unity 6 colliders (composite, one-way, hazards, ladders), reader for painted levels, Editor menu and pgen_* CLI commands. Use whenever the user wants to generate, author, import, validate or debug platformer levels, tilemaps, rooms, chunks or seeds, fix unreachable jumps, build an endless runner, or turn ASCII/LDtk/painted maps into playable Unity levels, including Turkish asks like "prosedürel seviye", "tilemap üret", "bölüm tasarımı", "oda şablonu", "seviye oynanabilir mi", "zıplanamıyor".
---

# Platformer Tilemap Generator (Unity 6 + Claude)

Levels are **data first, tiles second**: every level — generated or hand-made — becomes a `TileGrid`
of semantic cells (`Solid`, `OneWay`, `Hazard`, `Ladder`, `Spawn`, `Exit`, …), is **validated against
the player's movement profile**, and only then written to Tilemaps. That single pipeline is what makes
procedural output trustworthy and lets hand-painted levels get the same guarantee.

```
            ┌─ RoomGridGenerator (Spelunky)      ┐
 seed ──►   ├─ ChunkStitchGenerator (+beats)     ├──► TileGrid ──► ReachabilityValidator ──► TilemapLevelWriter ──► scene
            ├─ HeightmapGenerator / CaveGenerator│        ▲            (MovementProfile)          (batched, colliders once)
 authored ─►└─ AsciiLevel / painted Tilemap ─────┘        └──── TilemapLevelReader (hand-painted levels)
```

## Package layout (copy into the Unity project)

| Skill path | Goes to | What |
|---|---|---|
| `scripts/Runtime/Core/**` | `Assets/PlatformerGen/Runtime/Core/` | Engine-free C# (asmdef `noEngineReferences`): grid, RNG, profile, validator, generators. Runs in Unity AND plain Mono/.NET. |
| `scripts/Runtime/Unity/**` | `Assets/PlatformerGen/Runtime/Unity/` | `TileLegend`, `LevelLayers`, `TilemapLevelWriter/Reader`, `LevelGenConfig`, `RuntimeLevelBuilder`, `ChunkStreamer`, `LevelMarker` |
| `scripts/Editor/**` | `Assets/PlatformerGen/Editor/` | `Tools > PlatformerGen` menu + `PlatformerGenOps` (Undo-safe, JSON results) |
| `scripts/Editor.Pipeline/**` | `Assets/PlatformerGen/Editor.Pipeline/` | `pgen_*` `[CliCommand]`s — auto-compiles only if `com.unity.pipeline` is installed |
| `scripts/Tests.Editor/**` | `Assets/PlatformerGen/Tests/Editor/` | EditMode tests incl. writer↔reader round trip |
| `assets/*.txt` | `Assets/PlatformerGen/Generated/` | Default room / chunk templates + an example authored level (text, editable by Claude) |
| `tools/CoreHarness.cs` | stays outside Unity | Test + render levels with `mcs`/`mono` when no Editor is available |

## Workflow

### 0. Recon (always, before writing anything)
- `ProjectSettings/ProjectVersion.txt` → Unity version (skill targets 6000.0+; 6000.3 LTS is the safe baseline).
- `Packages/manifest.json` → `com.unity.2d.tilemap` (required), `com.unity.2d.tilemap.extras` (RuleTile/AutoTile —
  version differs per Editor; read it, never assume), `com.unity.pipeline` (enables `pgen_*`), URP 2D?
- Live Editor? `unity status` / `unity command --project-path <p>`. If reachable, **drive it** (see
  `references/unity-cli-driving.md`) — never hand-edit `.unity`/`.asset` YAML while an Editor is live.
- Existing player controller → extract jump height / apex time / run speed / gravity scale / collider size (step 1).
- Existing tilemaps/tile assets/palettes → reuse them in the `TileLegend`.

### 1. Pin the movement profile (the level↔controller contract)
Every generator rule and the validator derive from `MovementProfile` **in tiles**. Get it from the real controller:
- height/apex style: `MovementProfile.FromApex(jumpHeightTiles, timeToApex, runSpeedTilesPerSec, bodyHeight, fallMult)`
- Rigidbody style: `FromUnityUnits(|Physics2D.gravity.y|*gravityScale, jumpVelocity, runSpeed, cellSize, …)`
- Body height = collider height / cell size, rounded up. Extras (double jump, dash, wall jump) are **not** modelled —
  either extend the validator (`references/playability-validation.md`) or validate with the base moveset (safer).
Put the numbers in `LevelGenConfig`. Print `profile.ToString()` and show the user the derived limits
(max step, max gap, max spike run) — they are the authoring rules for every template.

### 2. Pick the route
| Need | Route | Class |
|---|---|---|
| Roguelite runs, replayable seeds, room-based caves (Spelunky/Noita-lite) | RoomGrid | `RoomGridGenerator` + `@room` templates |
| Linear levels, auto-runners, endless | Chunks + beats | `ChunkStitchGenerator`, runtime `ChunkStreamer` |
| Overworld / exploration strips | Constrained heightmap | `HeightmapGenerator` |
| Underground / metroidvania filler | CA caves + ledges | `CaveGenerator` |
| Metroidvania with a designed structure | Graph of rooms | Edgar-Unity or custom `IGridGenerator` (see algorithms ref) |
| Style-from-example, textures of terrain | WFC | DeBroglie (backtracking + path constraint) as a pre-pass → `TileGrid` |
| Hand-designed levels | ASCII / painted / LDtk | `AsciiLevel`, `TilemapLevelReader`, LDtkToUnity |
Runtime generation (`RuntimeLevelBuilder`) only for per-run content; otherwise **bake in the Editor** and ship the scene
(designers can then hand-polish; re-validate after edits). Details: `references/procedural-algorithms.md`,
`references/authored-levels.md`.

### 3. Install
Copy the folders per the table, keep the asmdefs. Then either menu `Tools > PlatformerGen > Create Default Assets`
or `unity command pgen_defaults --templates_dir <abs path to skill>/assets` (after copying `assets/*.txt` into
`Assets/PlatformerGen/Generated/`). Then `Setup Level Grid In Scene` / `pgen_setup` creates the Grid with
Ground / OneWay / Hazard / Ladder / Decor tilemaps and the right Unity 6 physics components.

### 4. Tiles
Fill the `TileLegend`: `Solid` → a **RuleTile or AutoTile** (edges/corners resolve automatically after batched
writes), `OneWay`, `Hazard` (sprite pointing UP, centred pivot — the writer rotates wall/ceiling spikes), `Ladder`,
marker prefabs (Spawn/Exit/Pickup/Enemy). Delegate tile-asset creation to the Unity plugin skills:
`sprite-segment-3x3grid` → `tilemap-ruletile-createfromsegment` for RuleTiles from a tileset,
`tilemap-palette-create` for palettes, `2d-pixel-perfect` for crisp pixel art, `manage-sprite-atlas` to pack tiles
(prevents seams and keeps Chunk-mode rendering consistent). Generation refuses to write while Solid/OneWay/Hazard/Ladder
have no tile, so an "invisible level" never happens silently.

### 5. Generate → validate → look → iterate
1. `pgen_generate --config <asset> --seed N` (or menu). Read the JSON: `passed`, `coverage`, `jumpsOnPath`,
   `problems`, and the `ascii` overlay (`*` golden path, `+` reachable resting spots).
2. `unity command screenshot --output shot.png` and **look at it** — ASCII proves reachability, only the render
   proves the tiles/RuleTiles/sorting/colliders look right.
3. `pgen_sweep --config <asset> --count 100` when tuning: first-try pass rate should be **> 90%**. Lower means the
   generator relies on rejection sampling — tighten rules by construction, don't raise `maxAttempts`.
4. Hand-edited or painted a level? `pgen_validate --config <asset>` checks the scene as-is.
No Editor available → `mcs -out:h.exe tools/CoreHarness.cs $(find scripts/Runtime/Core -name '*.cs') && mono h.exe render room 7 assets`
(modes: suite, `render <room|chunk|height|cave> <seed>`, `validate <file.txt>`, `failures <kind>`).

### 6. Authoring templates (the part users edit most)
Format and legend: `references/authored-levels.md`. Non-negotiables:
- Obey the profile limits from step 1 (default profile: rises ≤ 2, pits ≤ 4, ground spike runs ≤ 2, headroom above spikes).
- Room exit contract (L/R rows, U/D openings) is stated at the top of `assets/room-templates.txt` — the generator trusts it.
- Every template must be traversable both directions; run `sweep`/harness after every template edit.
- Comments in template files use `//` (`#` is the Solid glyph).

## Rules that prevent the classic failures
- **Determinism**: only `PlatformerGen.Rng` (+ `Derive(salt)` per pass/chunk). Never `UnityEngine.Random`/`System.Random` in generation.
- **Batch writes**: one `SetTilesBlock` per layer; composites set to Manual during the batch, `GenerateGeometry` once. `SetTile` in a loop on a big map with a Synchronous composite stalls for seconds.
- **Unity 6 physics API**: `Collider2D.compositeOperation = Merge` (old `usedByComposite` is gone); one-way = `PlatformEffector2D.useOneWay` + `composite.usedByEffector`; hazards = trigger composite.
- **Validate with margin** (`safetyMargin` 0.85): a level that needs a frame-perfect max jump is a bug.
- **Raw noise is not a level**: heightmaps/caves must be constrained by the profile (the provided generators do it).
- **Hand-painted = same bar**: validate painted levels before calling them done.
- **Don't guess package versions or APIs** that changed across 6.x — check the manifest and the docs page for the project's version.
- Tell the user what was generated with seed + config so it can be reproduced.

## Reference files (read when the step needs it)
- `references/unity-tilemap-api.md` — Tilemap/collider/renderer APIs per Unity 6.x, seams, RuleTile vs AutoTile, perf, Undo.
- `references/procedural-algorithms.md` — every algorithm, when to use it, knobs, how to add a new `IGridGenerator`.
- `references/playability-validation.md` — jump math, what the validator models, reading/fixing failures, extending it.
- `references/authored-levels.md` — ASCII + template formats, painted-level validation, LDtk/Tiled/image import.
- `references/unity-cli-driving.md` — exact `unity` command sequences for Claude, incl. no-Editor fallback.

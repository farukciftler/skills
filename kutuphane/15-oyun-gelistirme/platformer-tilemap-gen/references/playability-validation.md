# Playability validation

## Contents
1. Jump math · 2. What the validator models · 3. Options · 4. Reading a report · 5. Fixing failures · 6. Extending the moveset

## 1. Jump math (why everything is in tiles)
Designers pick jump height `h` and time to apex `t`; physics follows: `g = 2h / t²`, `v0 = 2h / t` (equivalently
`v0 = √(2gh)`). Typical good feel: `t` 0.3–0.45 s, fall gravity 1.5–2.5× rise gravity.
Flat jump distance = `runSpeed × (t_up + t_down)` with `t_down = √(2h / (g·fallMult))`.
`MovementProfile` exposes the derived authoring limits:
- `MaxStepUpTiles(m)` = ⌊h·m⌋
- `MaxGapTiles(m)` = ⌊flatJump·m − bodyWidth⌋
- `MaxHazardRunTiles(m)` = `MaxGapTiles − 1` — a strip of ground spikes is harder than a pit of the same width:
  over a pit the body may dip to ground level, over spikes it must stay a full tile higher.
Headroom matters: a ceiling 2 tiles above the floor caps the jump and can make a 2-wide spike strip impossible.

Conversions: tiles = units / `Grid.cellSize`. Rigidbody controllers: gravity = |Physics2D.gravity.y| × gravityScale;
launch speed = the velocity you set (or impulse / mass). Character body height = collider height / cell, rounded up.

## 2. What the validator models
- **Nodes**: resting places — body (1×H tiles) fits, support below (Solid/Breakable/OneWay/ladder top) or holding a ladder.
- **Edges** (continuous simulation at 60 Hz with sub-steps, axis-separated collision, body width 0.8):
  walk; walk-off falls with 4 drift variants; jumps at `ceil(h)` heights × 5 constant horizontal speeds (+ from the
  tile's leading edge) + 2 "jump straight up, steer at apex" variants; ladder up/down; drop-through one-ways.
- **Death**: touching Hazard, leaving the grid downward when `BottomIsPit`, falling more than `MaxSafeFall`.
- **One-way**: solid only when falling onto its top.
- **Degraded profile**: validation uses `profile.Degraded(SafetyMargin)` (height × m, speed × m) so passing levels
  never need frame-perfect max jumps.
- BFS from Spawn; pass = some reachable node's body overlaps an Exit cell.
Not modelled (by design, conservative): double jump, dash, wall jump/slide, coyote time, moving platforms, springs,
enemies as obstacles, breakable blocks being broken. Levels that *require* these will fail → extend (section 6)
or validate the base route and treat advanced tech as optional shortcuts.

## 3. Options (`ValidatorOptions`)
| Field | Default | Meaning |
|---|---|---|
| `BottomIsPit` | true | falling out the bottom = death. `LevelGenConfig` sets false for RoomGrid/Cave (closed boxes). |
| `SafetyMargin` | 0.85 | 1.0 = exact physics (only for testing), 0.75 = very forgiving |
| `JumpHeightSamples` | auto | variable-jump heights sampled |
| `SimulationSeconds`, `Hz` | 4, 60 | per trajectory |
Outside-the-grid cells use `TileGrid.OutOfBounds` (Solid for generated boxes, Empty for painted levels).

## 4. Reading a report (`ValidationReport` / `ReportDto`)
- `passed` / `exitReachable` — the gate.
- `coverage` = reachable / standable resting spots. Low is fine for Spelunky filler; low on a linear level = unreachable
  side content (check pickups).
- `pickupsReachable/pickupsTotal` — unreachable pickups are listed in `problems`.
- `pathLength`, `jumpsOnPath`, `fallsOnPath` — rough pacing signal (BFS path = fewest moves, not the designer's route).
- `ascii` overlay: `*` golden path, `+` other reachable resting spots. The first `+`-free region along the intended
  route is where it breaks.

## 5. Fixing failures (symptom → cause → fix)
| Overlay symptom | Likely cause | Fix |
|---|---|---|
| `+` stops before a ledge | rise > `MaxStepUp` | lower the ledge / add a step or one-way |
| `+` stops at a pit | gap > `MaxGap` (or landing higher than takeoff) | shrink gap / add a hop platform |
| `+` stops at spikes | spike run > `MaxHazardRun` or low ceiling above | shorten strip, raise ceiling, remove `?` blocks over it |
| Spawn region has 1–4 `+` | spawn boxed in / on a perch | place spawn on floor level; check start template |
| Everything reachable but exit | exit on an unreachable perch | move exit to floor level |
| Works for 1-tall, fails for 2-tall | 1-tile tunnels/gaps | widen to body height + 1 |
| Painted level fails at edges | `OutOfBounds = Empty` + `BottomIsPit` | paint walls/floor or disable pit mode for closed maps |
Fix templates/rules, not seeds: a generator that needs many retries will eventually ship a bad level in a code path
that doesn't validate.

## 6. Extending the moveset
All in `ReachabilityValidator.Expand`:
- **Double jump**: in `Simulate`, allow one extra `vy = √(2g·h2)` impulse when `vy <= 0` (branch: with/without) —
  add a `bool usedDouble` param and spawn both variants at apex.
- **Dash**: add edges that move the body horizontally N tiles at fixed y if `BoxHit` free, then continue with `Simulate(vx=0, vy=0)`.
- **Wall jump**: when X collision occurs while falling, branch a new trajectory with `vx = ∓s`, `vy = v0·k`.
- **Coyote time**: start walk-off falls with a small jump impulse window (cheap approximation: allow jumps from the first
  non-standable column next to a ledge).
Each extension multiplies edge count — keep samples low and measure with the harness (`validate`, `failures`).
Add unit cases to `tools/CoreHarness.cs` and `Tests.Editor` for every new move (one positive, one negative).

# Hype scenarios — what the genre actually rewards, and what this pipeline can build

Researched August 2026 across TikTok discovery pages and the big "satisfying simulation" compilation channels. Read before designing a new recipe: the genre is not "physics", it is a handful of **specific repeatable formats**, and clips that match a format inherit its audience.

## What the data says

The formats pulling the biggest numbers in 2025–26, roughly in order:

1. **Soft-body squish** — soft cylinders gliding through glass tubes, pillars "melting" through holes, percentage-softness tests. The dominant trend. Viewers literally comment on softness percentages; creators A/B them.
2. **Marble runs / marble races** — spiral tracks, ASMR framing; races add a competition hook ("which colour wins") that drives comments.
3. **Plinko / Galton boards** — vertical, hypnotic, the statistics *are* the payoff. Also a live-stream gambling aesthetic, which travels.
4. **Cloth & drop tests** — "different weight plastic sheets fall onto objects": the hook is *anticipation of material behaviour*.
5. **Hydraulic press / crushing** — destruction with a countdown structure.
6. **Domino cascades** — old but permanently green; the setup *is* the hook.
7. **Coin pushers** — near-miss mechanics; borderline gambling-adjacent, enormous watch time.
8. **Sand/fluid hourglasses, magnetic sand** — continuum eye-candy.

Two structural observations that matter more than the list:

- **The hook is anticipation, not resolution.** Every winning format shows the viewer a machine whose outcome they can *almost* predict — the bell curve forming, the tower leaning, the chain about to slip. The first second must show the machine, not the payoff.
- **A colour-race turns retention into comments.** "Which bin fills first", "which marble wins" converts a passive watch into a stake. Cheap to add to any recipe: score by colour and show a running tally in the composition (bins, lanes, columns).

## Feasibility map for this pipeline (rigid bodies, Metal, headless)

| Format | Feasible? | Notes |
|---|---|---|
| Plinko / Galton | **Built** — `recipes/plinko.json` | Vertical = native 9:16; porcelain clicks are an audio gift |
| Marble race | **Built** — `recipes/marble-race.json` + `race_overlay.py` | Zig-zag ramps, 4 teams, "GUESS THE WINNER!" intro card and an automatic "<TEAM> WINS!" card read from the motion cache |
| Long-form 3D race | **Built** — `recipes/marble-gauntlet.json` | ~40 s switchback tower: continuous 3D channel, spinners, pendulum turnstiles, oscillating gates, dome fields; the sim writes a per-frame focus track (`camera.json`) and the renderer's spring-damped follow rig orbits down the tower with it |
| Domino cascade | Yes, easy | Thin cuboids along a parametric curve; topple wave = perfect `action_spread` |
| Marble run | Yes, medium | Straight/zig-zag rails from cuboids are easy; helix needs a curved-track builder |
| Tower collapse / wrecking ball | Yes, easy | Box towers + a heavy pendulum (one joint) |
| Coin pusher | Yes, medium | Kinematic pusher platform needs a scripted kinematic body — small `sim` addition |
| Newton's cradle | Yes, but demanding | Needs high restitution + high solver iterations to conserve the click |
| Hydraulic press | Partly | Rigid crush = objects shatter-less; reads wrong without fracture. Skip |
| Soft-body squish | **No** (rigid solver) | The trend leader, but rapier has no soft bodies. Faking with jointed lattices reads cheap. If pursued: separate project (XPBD in a WGSL compute shader — see `stack-research.md`) |
| Cloth / sheets | No | Same reason |
| Sand / fluid | No (yet) | 100k-particle territory; GPU compute project |

The honest conclusion: **this pipeline's lane is precision-machine formats** — plinko, dominoes, marble races, collapses — where rigid bodies are the *right* physics, and where the audio synthesiser (discrete clicks and rolls) is at its best. Soft-body is the one trend it cannot chase without new simulation tech; do not try to fake it.

## Design rules extracted from what performs

1. **The frame is the machine.** In the winning vertical clips the whole apparatus fits the 9:16 frame from frame 0. No camera moves, no reveals. (This is why plinko works and wide domino fields underperform on Reels.)
2. **One mechanism, visible odds.** The viewer must be able to form a prediction in <1 s. Offset pegs, a leaning tower, an unbalanced chain — all legible instantly.
3. **Steady feed beats one burst.** A continuous drip of bodies (spawn scheduling) keeps mid-clip retention; a single dump front-loads the interest. The contact-event histogram should be near-flat.
4. **Colour is information, not decoration.** Palette slots should mean something — teams in a race, bins in a sort. Random tinting wastes the comment hook.
5. **Sound sells the material.** Porcelain clicks for small hard balls, wood knocks for cubes, metal ring for chains. The synthesiser's material bank is the differentiator; use the material that matches the *implied* substance, not the render colour.
6. **End settled, loop clean.** The last second must be at rest (or a perfect loop). Mid-motion cuts test as abandonment.

## Recipe backlog, ranked by expected return on effort

1. **domino-wave** — S-curve of dominoes down the frame; one push; wave travels top→bottom. Trivial to build, guaranteed clean `action_spread`, and the audio (accelerating knock train) is exactly what the modal synth does well.
2. **plinko-race** — plinko variant where two colours drop alternately and the composition shows per-colour bin tallies. Combines the two strongest hooks.
3. **tower-wreck** — box tower + single-joint pendulum ball. Payoff = collapse; sweep seeds for photogenic falls; scorer's `action_spread` wants re-weighting (see `autoselect.md`).
4. **coin-pusher** — needs one new `sim` feature (scripted kinematic platform, ~30 lines). Highest watch-time format in the feasible list.

## What the marble-race build taught (August 2026)

- **Select for margin, not for score.** `race_overlay.py --report` prints the 1st→2nd gap per seed; the postable clip is the closest race, and the generic scorer cannot see that. Ten seeds gave four different winners and margins from 0.28 s to 1.08 s — sweep and pick the photo finish.
- **Racers must never sleep.** Rapier's island sleeping parks a slow ball on a shallow ramp mid-race (`can_sleep(false)` on every racer), and a sleeping racer is a frozen race.
- **Bump protrusion is the drama dial.** A ball needs v² > 2·g·p to climb a bump of protrusion p. 12 mm produces hops and lead changes; 27 mm is a wall and the first version parked half the field. Expect DNFs on some seeds regardless — reject those in the report step.
- **Fairness is physical, chaos is seeded.** Identical balls, identical ramps; the only per-seed differences are lane order (Fisher–Yates with the scene RNG) and bump placement. That is what makes "guess the winner" an honest question.
- **Text goes in as PNG overlays, not drawtext.** The Homebrew ffmpeg has no libfreetype; `textcard.swift` renders Impact-with-stroke cards via CoreText and ffmpeg's `overlay` burns them in. Cards render oversized for clean glyphs and are scaled in the filter graph — an overlay wider than the video silently does not appear.

## The gauntlet format rules (binding)

1. **The lead changes at least four times per video.** `min_lead_changes: 4` in the recipe; `race_overlay.py --report` counts leader-identity changes (4 Hz sampling, 12 cm hysteresis) and exits non-zero on failure or any DNF — a seed that fails the rule is rejected, never published.
2. **The shuffling must be natural.** The user rejected hidden-hand rubber-banding (`rubberband` stays in the code, default 0, off): rank changes come from *obstacles*, not forces. What actually works, measured: **fast gate cycles** (period ~1.7 s — short frequent waits shuffle; slow gates with long dwell turn the field into a 1.2 s-spaced procession with zero changes), **spinners** (kinematic paddles exchange real momentum — throw one marble back, slingshot another), **split islands** (a lens down the channel centre; lane choice is millimetres at the tip, one lane studded), and **traffic** — eight racers collide far more than four. Natural pass rate ≈ 3/12 seeds; sweep twelve to publish one.
3. **The race starts at GO, not before.** Four abreast on the grid behind a chrome barrier; a one-shot Slide motor lifts it on the GO beep. Zero pre-GO displacement, verified per take.

## What the gauntlet build taught (August 2026) — the long-course rules

Building a ~40-second continuous 3D course cost six broken takes. The rules that came out:

- **A continuous channel cannot leak; everything else can.** The first design connected flights with drop-pockets, and every revision discovered a new ball-sized exit (a slot under the catch wall, a bottomless seam behind the back wall, a pocket balls landed *on top of*). Switching to one unbroken polyline channel — flights joined by four-kink corners, floors overlapping 6 cm at every seam — removed the entire failure class at once.
- **Below ~12–13° a marble parks forever.** The discrete solver's contact friction holds a sphere in static equilibrium on a shallow incline. Keep every floor at ≥13° *and* ball/track friction below tan(13°) ≈ 0.23, so a stopped marble always at least slides.
- **Every obstacle needs a "cannot trap" proof.** Full-width bars wedge marbles uphill of them (use domes: sphere-on-sphere contact always deflects); a sliding gate with any friction makes the marble surf its face sideways forever (make gates frictionless); a pendulum hanging lower than a ball's crown is a locked turnstile (tip clearance above the crown, light enough to shoulder through); pin/rail gaps narrower than a ball are wedge pockets (keep both sides wider than a diameter).
- **Sequencing beats parameters for ranking churn.** Lead changes come from the *equalisers* — long-dwell gates that stop the leader and bunch the pack, pendulums that smack, domes that swap lanes — not from tuning ball physics. Measured: 6–16 order shuffles and 2–8 lead swaps per race, with margins down to 0.15 s.
- **Camera focus lives in arc-length space.** The sim projects every racer onto the track centreline, blends *progress* between first and second place (never positions — the centroid of points wrapped around a tower is the empty air inside it), and writes per-frame `[x,y,z,yaw]` to `camera.json`. The renderer springs toward both with separate stiffnesses; unwrapped yaw means the orbit never solves an angle-wrap.
- **Corners are curves or they are rectangles.** Four 16° kinks read as a rectangle with the corners knocked off; nine ~7° kinks read as a drawn curve, and the seam overlaps can shrink from 6 cm to 3.5 cm because each kink's outer gap shrinks with the angle.
- **The chase camera is the racing view.** Offset behind the pack along the heading, high enough to be nearly top-down, looking down-forward — travel reads "up" the screen like a driving game, the pack strings out toward the lens, and both rails can be low without ever occluding a marble.
- **Containment the camera can't see.** The camera-side rail is a low curb (marbles stay visible) topped with an *invisible* wall — solid to the solver, absent from the render. A hard deflection over a 9 cm curb lands the ball on a flight several places ahead: a fake leader and a camera teleport in one.

## Sources

- [TikTok — soft body physics simulation discovery](https://www.tiktok.com/discover/soft-body-physics-simulation-puh) · [most satisfying physics simulation](https://www.tiktok.com/discover/most-satisfying-physics-simulation) · [marble run ASMR](https://www.tiktok.com/discover/satisfying-videos-marble-run)
- [Oddly satisfying videos — Wikipedia](https://en.wikipedia.org/wiki/Oddly_satisfying_videos) (domino shows, hydraulic presses as canonical subjects)
- Compilation channels: [Most Satisfying Simulations of 2025](https://www.youtube.com/watch?v=H4ePSTpwEf8) · [3D Physics Showcase](https://www.youtube.com/watch?v=1Y2lkiTFptw) — scene lists (Magnetic Sand Swirl, Glass Domino Waterfall, Rainbow Sand Hourglass) show the sub-format vocabulary

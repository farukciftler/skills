# Idea queue — the five YouTube-suggested formats, worked out

Source: YouTube Studio's idea generator, on the Weft Records channel, 11 Aug 2026.
Each idea arrived with the tool's own "why this fits your channel" notes. Those
notes are advertising copy, not analysis, and two of them are worth reading
before anything else:

- On **Liquid Nitrogen Marble Race** the tool itself said the idea is an
  *"Incompatible Creative Direction"* — Weft Records is an ethnomusicology and
  ambient-soundscape channel, and a physics stunt is a departure from it.
- On the other four it argued the opposite, in language that mostly amounts to
  "marbles clatter, clattering is percussion, percussion is music." That is a
  rationalisation. The honest position is that all five are the *same* genre
  departure, and the channel is now running two formats: long-form world-music
  pieces and short-form physics races. That is a deliberate choice, not
  something the idea tool discovered.

What follows is each idea re-specified as something this pipeline can actually
build — which for a **rigid-body** simulator means some of the source premises
have to be replaced rather than approximated. Where that happens it is stated
outright.

---

## 1. `k1-ice-shatter` — "Liquid Nitrogen Marble Race"

**As pitched:** a steel marble shatters nitrogen-dipped obstacles; brittle
fracture of flash-frozen barriers.

**What is not buildable:** real brittle fracture. Crack propagation through a
solid needs an FEM or MPM solver; rapier has neither, and faking it with a
convex decomposition that "breaks" on impact is a different simulation, not a
cheaper one. Thermal shock is not simulated at all — there is no temperature in
this world.

**What replaces it:** *pre-fractured* barriers, the same trick every game
engine uses. Each ice wall is a running-bond curtain of six light blocks
(density 90 kg/m³, ~1/70th of a marble) laid across the channel. The pack does
not stop at the wall; it goes through it and the wall goes with it.

**Why it is a good race and not just a good picture:** it is the only obstacle
on any of these courses whose *state changes*. The leader pays the toll of
breaking the curtain and everyone behind runs through the hole — a built-in
penalty for being in front, which is exactly what the ≥4-lead-changes rule
wants and which no static hazard provides.

**The trap it walked into first:** blocks at friction 0.35. Everything a marble
can come to rest against on a 13° floor must be below tan(13°) ≈ 0.23, or the
solver holds it in static equilibrium forever. First run: two of eight DNF,
parked against shards. At 0.12 all eight finish.

Palette: cold — `#bfe9ff` ice, `#0a1826` night-blue backdrop, `env_warmth` 0.18.

---

## 2. `k2-solar-gates` — "Solar Powered Marble Maze"

**As pitched:** sunbeams drive analog photo-resistors which actuate mahogany
gravity gates in real time.

**What is not buildable:** light. There is no photometric feedback path from
the renderer into the simulator, and there should not be one — the take is
immutable and the renderer runs after the fact. A gate that responded to
rendered light would break the one invariant the whole pipeline rests on.

**What replaces it:** the causality is inverted. The gates run on their own
1.7 s cycle (the existing `gate` obstacle), and the *lighting* is styled to
read as the driver — warm amber key, `env_warmth` 0.92, gold trim. Nobody
watching a 57-second Short can tell which way the arrow of causation points,
and the mechanism the viewer actually sees — gates opening and closing in
rhythm — is real.

**Why this is the safest of the five:** gates are the established churn engine
of this format (measured ~90 % rule-pass rate at six gates). This course is
eight of them and nothing else exotic. It is the format's baseline, redressed.

---

## 3. `k3-sandglass` — "The Great Sandglass Race"

**As pitched:** glass spheres climb through a relentless tide of fine silica.

**What is not buildable:** fine silica. Granular flow at grain scale is an
MPM/DEM problem; a genuine sand column is 10⁵–10⁶ particles and this machine
has no GPU physics available (Warp, Taichi, Genesis and PhysX-GPU are all CUDA
or dead — see CLAUDE.md). Also not buildable: *rising* sand. Nothing here
generates material over time, and marbles cannot climb a 13° descent.

**What replaces it:** coarse grain, 84 spheres per drift at 1.6 cm radius,
held behind a 3.5 cm curb. The curb is the whole design: on a 13° floor loose
grain slides to the bottom of the course inside a second, so without it there
is no drift, just a spill. 3.5 cm is above a grain and below a marble's centre
— the grain stays and the marble rides over instead of wedging.

**Why it earns its cost:** it is the strongest natural equaliser available.
Marbles plough through at unequal speed with no rubber-banding anywhere in the
loop, which is exactly the "doğal engellerle" constraint. It is also the most
expensive take in the set — 1267 bodies, ~9 s to simulate versus ~0.5 s for the
others.

**The bug it surfaced:** `race_overlay.py` defined a racer as "dynamic ball",
so 84 grains per drift finished the race and the standings filled with nine
finishers called TEAM 16. A racer is now a dynamic ball wearing a *team* tint.

---

## 4. `k4-magnet-maze` — "Giant Magnet vs Metallic Marble Maze"

**As pitched:** neodymium magnets stall spheres mid-descent and force
shortcuts; can an invisible field rewrite a falling race?

**What is buildable:** all of it. This is the only idea of the five that needs
no substitution — a magnet is a force, and a force is one line in the tick
loop. `Motor::Attract` pulls with `strength · m / (d² + soft²)` inside a 0.85 m
radius, applied as an impulse (rapier clears accumulated forces every step, and
this loop runs per tick, not per frame — a force set there would be applied
once and wiped).

**Design decisions that matter:**
- The magnet sits *outside* the far rail. The pull is a force, never a
  collision, and there is a solid wall between the magnet and the pack.
- It acts on racers only. Letting it grab the loose debris as well turns every
  magnet flight into a pile-up.
- Finite radius, not a global field. A magnet is a local event on one flight;
  an unbounded 1/r² field quietly warps the entire tower and the course stops
  being readable.

**Why it is the best of the five:** the premise is a genuine question — *can
physics change the winner?* — and the answer is measurable rather than
asserted. Seed 501: eight finishers, five lead changes, 2.88 s margin.

---

## 5. `k5-kinetic-chaos` — "Kinetic Sculpture Chaos"

**As pitched:** wooden gears and copper tracks splintering into twelve
diverging routes; guess which lever sequence reaches the hidden finish.

**What is not buildable as written:** twelve genuinely separate routes. The
course is one continuous channel by construction, and that is not a limitation
to route around — it is the rule that makes an arbitrary plan safe (*every gap
in a course is a ball-sized exit*). Twelve parallel channels is twelve times
the leak surface, and the six broken takes that produced the gauntlet rules
were all leaks. A "secret" finish also fights the format: the whole hook is
*guess the winner*, and you cannot guess what you cannot see.

**What replaces it:** four `split` islands — the lens that forks the channel
into a clean lane and a studded lane and rejoins it — plus three spinners as
the "gears", on a copper-and-wood palette. Which lane a marble takes is decided
by millimetres at the island tip: a physical coin flip per arrival, four times
per race, which is the honest version of "twelve diverging routes".

**Known risk:** spinners create breakaways. Measured across every spinner speed
tried (−1.6 … 2.6): 0–2 lead changes, runaway leader. This course is the one
most likely to need a wide seed sweep, and seed 501 duly failed at 3 lead
changes. It is kept anyway because the split islands are the only obstacle that
produces a *visible* branch point on camera, and that is what this idea is
actually about.

---

## Status

| # | recipe | new physics needed | seed-sweep risk |
|---|--------|--------------------|-----------------|
| 1 | `k1-ice-shatter`   | `Obst::Ice` — pre-fractured curtain | medium |
| 2 | `k2-solar-gates`   | none | low |
| 3 | `k3-sandglass`     | `Obst::Sand` — curb + grain | medium |
| 4 | `k4-magnet-maze`   | `Obst::Magnet` + `Motor::Attract` | low |
| 5 | `k5-kinetic-chaos` | none | high (spinners) |

All five are 8 racers, ~57 s, and bound by the standing format rule:
**birincilik en az 4 kez el değişmeli**, counted by `race_overlay.py --report`,
which exits 3 on a failing seed.

## ring-escape — the Tier-1 format, built (August 2026)

The "Will the ball escape?" recipe. Design decisions and their reasons, so
ESCAPE #2+ inherit them instead of rediscovering:

- **6 rings, r 0.16→0.62 m, ball r 2.5 cm.** The annulus between rings must
  clear the ball's diameter (spacing − thickness > 2r + margin); that caps the
  ring count for this camera. Camera z=3.4, fov 40 → half-width 0.70 m.
- **Difficulty must rise outward** (`gap_deg` 40 − 3.2·i, angvel 0.40 + 0.12·i,
  alternating direction). With uniform rings the arena empties in ~15 s;
  with the ramp, 40-seed sweeps put ~8% of seeds in the 34–58 s window.
- **Restitution 1.05 vs 1.0 + SpeedLimit 3.8** is the escalation curve.
- **Neon is a render flag, not a material** (`render: "neon"`), because the
  material field is the audio path; debris stays "metal" for the synth.
  Emissive 22 (rings) / 90 (ball), `sky_brightness: 0`, bloom 0.30 — the wash
  that first drowned the look was the always-on Skybox at brightness 400.
- **Melody** (`pipeline/melody.py`): Grieg's Mountain King (PD composition),
  one theme note per glass impact from events.jsonl, Karplus-Strong pluck +
  sub-octave sine, key +5 semitones after ring 2 and +12 after ring 4;
  shatters.json drives glass-crash hits. ~269 notes on the shipped seed.
- **Selection is a sweep** (escape_report.py): 6 shatters, first > 3.5 s, last
  in 34–58 s, min spacing 1.5 s, ≥100 notes, ball on-screen until the finale.
- **Trim the master to last shatter + 2.4 s** — after the final escape the ball
  leaves the frame and the tail is dead air.

## ball-multiply — Tier-2, researched + built (August 2026)

The "one becomes many" format: a single ball in a sealed neon circle, and on a
schedule of wall impacts it *splits* — 1, 2, 4, 8 … until a couple of hundred
balls fill the arena and the run ends on a wall of colour. Exponential growth
is the whole hook ([ViralBalls](https://viralballs.com/en/blog/10-satisfying-ball-physics-video-ideas-that-go-viral):
"the ball splits into multiple copies on each hit… one ball to 100 million" is
an established viral pattern; TikTok discover pages exist for
"ball but every bounce it multiply").

Design decisions, researched → committed:

- **Growth must be paced, not physical.** Genuine doubling on every wall hit
  fills any arena in ~10 s and the video is over before it starts. The split is
  therefore *quota-driven*: a split fires on the next wall impact after a timer,
  and the timer shrinks geometrically (2.4 s → ×0.90 per split → floor 0.10 s).
  The impact still provides the position, the velocity and the audio sync, so
  every split looks physical; only the *rate* is directed. ~220 balls by ~45 s.
- **Splits ride real impacts** — a clone enables at the impacting ball's
  position with a rotated copy of its velocity. Parked, disabled, pre-tinted
  pool (the take format cannot create bodies mid-run).
- **Dense-collision audio needs a rate cap and a scale, not a theme**
  ([BallEngine](https://ballengine.app/music-ball-simulator) does "overlap
  prevention + multi-sound smoothing"; scale-locked improvisation stays
  harmonious when notes arrive chaotically). Mode `multiply` in melody.py:
  E-minor pentatonic, pitch climbs with ball count, global note cooldown that
  tightens from 90 ms to 45 ms, per-note gain ~1/√count, bass pulse at every
  doubling milestone, closing chord at the cap.
- **Packing target ~35%** of the arena area at the cap — crowded enough to read
  as "full", loose enough that the solver never jams (220 × r 2.4 cm in r 0.62).
- **Milestone cards** (×2 ×4 ×8 … ×200) burned from splits.json timestamps —
  the count is the narrative.
- Series identity: same neon-void language as ESCAPE, different accent (cool
  blue container, generation-coloured balls), titles "MULTIPLY #N".

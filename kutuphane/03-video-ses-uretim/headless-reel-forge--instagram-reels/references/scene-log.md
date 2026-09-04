# Scene log — what has already been published, and what must not repeat

The standing loop produces **3 videos per run, none of them marble races, each
unrelated to the others and to everything below.** Read this file first, skip
every scene type listed, and append what you produce.

A "scene type" is the physical event, not the palette. Re-skinning a published
scene with new colours is a repeat and does not count.

## Used — do not produce again

| Scene type | Builder | Where it went |
|---|---|---|
| Marble gauntlet race (all variants) | `marble-gauntlet` | 20 Shorts, 11 Aug 2026. **Retired by user instruction.** |
| Ball drop into a bell curve | `plinko` | "110 Balls Drop Into a Perfect Bell Curve" |
| Wrecking ball vs block tower | `tower-wreck` | "Wrecking Ball vs 16-Story Tower" |
| Domino chain reaction | `domino-wave` | "251 Dominoes, One Rainbow Chain Reaction", 11 Aug 2026 |
| Chain draped over a bar, released | `chain-drop` | "A 54-Link Chain Slides Off a Bar", 11 Aug 2026 |
| Cubes rained into a container | `cube-rain` | "105 Cubes Poured Into a Box", 11 Aug 2026 |
| Pendulum wave (graded lengths, phase drift) | `pendulum-wave` | "13 Pendulums, One Wave", 11 Aug 2026 |
| Ten-pin bowling strike | `bowling` | "Ten Pins, One Strike", 11 Aug 2026 |
| Block avalanche down a slope | `avalanche` | "420 Blocks Down a 33° Slope", 11 Aug 2026 |
| Heavy sphere into a ball pit | `ball-pit` | "134 kg Steel Ball Into 900 Plastic Balls", 11 Aug 2026 |
| Hourglass, grain through a waist | `hourglass` | "An Hourglass Where Every Grain Is Simulated", 11 Aug 2026 |
| Card house collapse | `card-house` | "37 Cards, Four Storeys, One Steel Ball", 11 Aug 2026 |
| Stickman ragdoll duel (4 arenas) | `stickman-duel` | "8 Stickmen, 4 Arenas, 1 Champion", 11 Aug 2026 |

**Active ragdolls: three gotchas, in the order they cost time.**
`stickman-duel` drives poses with joint position motors, which is what makes a
punch land with real momentum instead of looking canned. Getting there:

1. **rapier's default motor model is `AccelerationBased`**, so stiffness is
   mass-normalised and lives around 1e3-1e4. At 26 the arm did not move at all.
   Fifteen minutes went into raising the force cap and the gain 15x, which
   changed nothing, because neither was the knob. 4000 works for a limb, 20000
   for a spine.
2. **Per-axis motors on a spherical joint would not drive the limb.** Shoulders
   and hips are `RevoluteJoint` hinges in the sagittal plane. A real shoulder is
   a ball joint, but a punch filmed side-on is a sagittal swing, and the hinge
   is controllable where the ball joint was not. For a revolute joint the free
   axis is `AngX`, whatever axis vector you passed to the builder.
3. **Motor-driven bodies are deterministic.** Take the random initial spin out
   and every seed produces the same bout — all seven of a bracket picked seed 1.
   Vary timing and closing speed, not the attack script: the script is what
   makes the motion look trained.

Hinges also fix the thing that read worst about the passive version: a
spherical elbow lets a forearm fold backwards, and the eye calls that broken
instantly.

**A bracket is a layout change, not a new scene.** `tournament.py` cuts seven
duel clips into one video by changing the screen split per round — 2x2, then
two rows, then full frame — with the audio mixed down while several fights run
at once. Any elimination format reuses it: the compositor only needs a winner
per bout, and the winner comes out of the motion track.

**This ffmpeg has no `drawtext`.** The Homebrew build ships without
libfreetype. `textcard.swift` renders captions through CoreText to an RGBA PNG
and ffmpeg overlays that. Impact runs wide: at 86pt "QUARTER FINALS" is wider
than 1080 and loses its first and last glyph off the frame edge.

**Sign errors are the failure mode of every new scene.** Four of them in one
run: a joint anchor placed off-axis without rotating the body (the solver
"corrects" it on frame 0 and launches everything), the same mistake mirrored in
the card lean, and a funnel built from a product of signs that came out as
peaks instead of a waist. Write the rotation out per case rather than folding
it into `side * angle * dir`, and check it by reading positions back.

**Standing a structure up is only half the job.** The card house stood, then
held a 5 kg ball dropped dead centre: a flat spanning card carries the load to
two A-frames at once. It needs to land off-centre, on an apex, and at 50 kg
from 5.5 m.

**Twelve builders exist and all twelve are used.** Writing three new ones took ~55
minutes including four look-dev rounds — budget that, not 40.

**A new scene is wrong twice before it is right, in two different ways.**
Check both, in this order:

1. *Physics*, from `motion.bin` — final body positions, not the render. The
   avalanche spawned at the bottom of its own ramp and every block ended 600 m
   below the scene; bowling pins left the lane and fell forever. Neither is
   visible in a still. Read displacement and count how many bodies end up
   somewhere impossible.
2. *Framing*, from a `--preview --scale 0.45` render (~40 s). Cameras aimed at
   nothing, floors blown to white, and a pendulum drawn as a floating ball with
   no visible string — none of which the position check can see.

**The renderer draws one shape per body.** A body with two colliders still
draws one. If a scene needs a rod *and* a bob, the body's drawn shape has to
span both, with its origin at the centre of what you want drawn.

**Derive the number, do not estimate it.** Two wrong figures were caught in
draft titles this session: 300 cubes for a 105-cube recipe, and a "50 kg" ball
that was 134 kg. Mass especially — it comes from density and radius cubed, so
a 40% radius change is nearly a threefold mass change. Compute it.

**Count what you claim.** The cube-rain recipe drops 105 cubes; a draft title
saying 300 was caught only by reading the recipe back. Read the parameter,
do not estimate from the picture.

**Clip length is a parameter, not a given.** chain-drop shipped at 5 s on its
stock settings, which is thin for a Short. 54 links on a bar 1.5× higher runs
11 s. Check the master's duration before uploading and lengthen the *event*
rather than padding the tail with a static pile.

## Unused ideas that this pipeline can actually build

Rigid bodies, joints, kinematic motors, a point attractor, and loose grain are
what exist. No fracture solver, no soft body, no fluid — see `idea-queue.md`
for why, and do not pitch those again.

- **Pendulum wave** — 15 pendulums on graded lengths, released together; the
  phase drift makes a travelling wave that resolves back to a line. Uses the
  existing spherical joint. Highest visual payoff per line of code.
- ~~**Newton's cradle**~~ — **tried, does not work, do not retry.** The impulse
  has to cross a chain of simultaneous contacts and a sequential-impulse solver
  smears it: the middle three balls swing 0.4-0.5 m instead of standing still.
  960 Hz with 48 solver iterations made it worse. Everyone knows what a cradle
  looks like, so a mushy one reads as broken rather than as physics.
- **Bowling** — one heavy sphere into a stacked pin triangle.
- **Avalanche** — a few thousand small boxes released down a ramp.

- **Magnetic sculpture** — `Motor::Attract` with several attractors and no
  track at all; bodies orbit and collide in free space.
- **Newton's pendulum row** — not the cradle; graded *masses* on equal strings.
- **Marble-free Rube Goldberg** — a lever tips a ball that trips a domino line.
- **Spinning top / gyroscope** — angular momentum, one body, very cheap.

## Rules that carry over from the marble work

- Everything a body can rest against on a slope needs friction < tan(slope).
- Loose grain needs a curb or it is at the bottom of the scene in a second.
- Put every visually meaningful rotation on the **body**, never the collider.
- Bodies are created disabled and released on a schedule; releasing everything
  on frame 0 spends the clip in the first three seconds.
- Never write a PNG sequence; frames go down a pipe into ffmpeg.

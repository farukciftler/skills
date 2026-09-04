# Scene recipes

Seven parametric shots covering most of the genre. Each lists tuned starting parameters, the failure modes specific to it, and what makes it readable on a phone.

Units: metres, kilograms, seconds. All values assume a camera framing roughly 6 m tall, gravity −9.8 m/s². Scale gravity rather than object size if the motion feels wrong — bodies below ~0.1 m get numerically fragile, and a scene that is physically small but readable is worse than one that is large and slow-motioned in post.

Contents:
1. `chain-drop` — jointed chain over a fixed pivot
2. `cube-rain` — bodies pouring into a container
3. `funnel-sort` — shapes falling through shaped holes
4. `tower-collapse` — stacked structure destroyed
5. `domino-spiral` — cascade along a path
6. `ball-pit-fill` — count-up filling shot
7. `pendulum-array` — coupled swinging bodies

---

## 1. `chain-drop` — jointed chain over a fixed pivot

A chain of connected boxes falls from above onto a static bar or post suspended in mid-air, wraps around it, and whips. The most satisfying and the most technically demanding recipe here.

```
link_count        24          # 18–40; more links = more whip, less stability
link_size         (0.18, 0.30, 0.18)
link_mass         0.4         # KEEP UNIFORM — see failure modes
link_gap          0.02        # small overlap-free gap between links
joint_type        PinJoint3D  # or JoltHingeJoint3D for planar-only motion
spawn_height      7.0
spawn_offset_x    0.6         # offcentre so it wraps rather than balancing
spawn_rotation_z  0.15        # slight tilt; pure vertical drops read as dull
pivot_radius      0.25        # static cylinder, horizontal, at y = 2.0
friction          0.6
restitution       0.0         # bouncy chains look like springs, not chains
velocity_iters    20          # RAISE from default 10
physics_ticks     180         # 3 substeps per 60 fps frame
```

**Failure modes:**

- **Chain stretches or explodes.** Almost always non-uniform mass. A joint solver's convergence depends on the mass ratio across the constraint; a 10:1 ratio between adjacent links makes the chain rubbery, and 100:1 makes it detonate. Keep every link within 2× of its neighbours. If a heavy end weight is wanted, ramp mass gradually across the last five links.
- **Jitter at rest.** Raise `physics_ticks_per_second` before raising solver iterations — substeps help constraint chains more than iterations do. 180 Hz for a 60 fps output is a reasonable ceiling; beyond that the cost stops buying stability.
- **Links pass through the pivot.** Continuous collision detection on the links, or make the pivot thicker than the per-tick travel distance. At 180 Hz and terminal-ish velocities the travel is small, so thickening the pivot is usually enough and much cheaper.
- **Chain balances on the pivot instead of wrapping.** That is what `spawn_offset_x` is for. Zero offset gives a symmetric, boring result roughly half the time.

**Readability:** the wrap is the payoff and it must not be centred on the pivot in frame — offset the pivot above and left of centre so the whipping tail sweeps through the frame's lower two-thirds where the eye is. Give the chain a colour that contrasts hard with the pivot; if both are the same material, the wrap is illegible on a small screen.

**Variations that reliably read well:** two chains from different heights colliding mid-fall; a chain falling onto a pivot that itself is a rotating cylinder; a chain of increasing link sizes (mass ramped gradually, not stepped).

---

## 2. `cube-rain` — bodies pouring into a container

Cubes fall from off-screen top into a transparent-walled or open-fronted container and settle into a pile.

```
body_count        400         # 200–1200
spawn_rate        12          # bodies per second
body_size         0.22        # ±15% jitter
size_jitter       0.15
spawn_area        (1.6, 0.0, 1.6)   # box above frame, y = 8
spawn_jitter_vel  0.4         # small random horizontal velocity
friction          0.5
restitution       0.15        # a little bounce; 0 looks like sand, >0.4 like rubber
container_walls   invisible or thin dark frame
angular_damp      0.1
```

**Failure modes:**

- **Spawning bodies inside each other** produces an initial explosion. Spawn in a grid with a jittered offset, not uniform random positions, and stagger spawn times so overlapping is impossible.
- **The pile "breathes"** — settled bodies visibly vibrate. Increase `linear_damp` slightly (0.05–0.1) and ensure sleeping is enabled so settled bodies deactivate. Sleeping also recovers a lot of frame time as the pile grows.
- **Rate too high** turns the shot into a texture rather than a physics event. Individual bodies must be trackable by eye. If the fall reads as a stream, lower the rate and increase body size.

**Readability:** the container's fill line rising is the narrative. Keep the container's top edge in frame from frame one so the viewer knows the target. Vary body colour across a 3–5 colour palette so the pile has structure instead of becoming a single mass.

---

## 3. `funnel-sort` — shapes falling through shaped holes

Mixed primitives fall onto a plate with cut-outs; only matching shapes pass. The "will it fit" tension is a strong retention driver.

```
shape_types       [box, sphere, cylinder, tetra]
count_per_type    30
plate_holes       matched to each type, 1.08× nominal size
plate_thickness   0.12        # thin plates cause tunnelling
drop_height       6.0
plate_tilt        0.0         # slight tilt (0.05) prevents permanent jams
friction          0.35        # low — shapes need to slide to find holes
```

**Failure modes:**

- **Nothing passes.** Holes at exactly nominal size never admit anything; 1.05–1.10× is the working range. Convex hull collision shapes are slightly larger than their visual mesh — check against the collision shape, not the mesh.
- **Permanent jam** kills the clip's ending. A tiny plate tilt or a slow plate rotation guarantees eventual resolution.
- **Tunnelling through the plate.** Thin static geometry plus fast small bodies. Thicken the plate (hidden thickness is free) or enable CCD on the bodies.

**Readability:** colour-code by shape, not randomly. The viewer needs to predict which will pass — that prediction is the engagement.

---

## 4. `tower-collapse` — stacked structure destroyed

A built structure is hit by a projectile or has its base removed.

```
block_count       180
block_size        (0.5, 0.25, 0.25)
stack_pattern     brick offset, 12 courses
block_mass        1.0
friction          0.7         # high — low friction means it never stood up
projectile_mass   12.0        # 10–15× block mass
projectile_speed  14.0
impact_height     0.65        # fraction of tower height; 0.6–0.7 gives best fall
settle_frames     40          # let the tower settle BEFORE capture starts
```

**Failure modes:**

- **The tower collapses before it is hit.** Always settle before capture. Alternatively build it with bodies frozen (`freeze = true`) and unfreeze on the first captured frame — cleaner and cheaper.
- **Mushy, floaty collapse.** Almost always too many solver iterations combined with high restitution, or blocks too light relative to gravity scale. Restitution near 0 and mass around 1 kg per block at this size reads as masonry.
- **Frame rate collapse at impact.** Hundreds of simultaneous new contacts. This is the one recipe where body count genuinely matters — 180 blocks is a good ceiling for a laptop at 60 fps capture.

**Readability:** frame so the tower occupies the upper two-thirds and the debris field has room below. The collapse must finish within the clip — a tower still falling when the video loops feels broken.

---

## 5. `domino-spiral` — cascade along a path

Dominoes placed along a spiral, S-curve or branching path, toppled from one end.

```
domino_count      160
domino_size       (0.06, 0.40, 0.20)
spacing           0.26        # 0.6–0.7× domino height — CRITICAL
path              archimedean spiral, 2.5 turns
friction          0.55
restitution       0.0
trigger_impulse   0.8
```

**Failure modes:**

- **Cascade stalls.** Spacing is the whole recipe. Too wide and a falling domino misses the next; too tight and they jam without transferring momentum. 0.6–0.7× height is the reliable band. Verify on a straight line before committing to a path.
- **Cascade skips ahead** on tight curves, where a domino falls across the chord rather than onto its neighbour. Increase spacing on curve interiors or reduce curvature.
- **Placement drift.** Generate positions procedurally from the path equation, never by hand — and re-verify spacing along arc length, not parameter value, or curves get denser than straights.

**Readability:** an overhead or high-angle camera shows the path; a low angle shows the fall. High-angle-tilted usually wins because it shows both. Branching paths that resolve into one are the highest-performing variant of this recipe.

---

## 6. `ball-pit-fill` — count-up filling shot

Spheres fill a shaped vessel — often a letter, logo, or silhouette — with an on-screen counter.

```
sphere_count      600
sphere_radius     0.14
spawn_rate        40          # higher than cube-rain; spheres read fine as a stream
restitution       0.35
friction          0.2         # low friction lets spheres find gaps and pack
vessel            static concave mesh (concave is fine — it never moves)
counter_overlay   yes, top-centre inside safe zone
```

**Failure modes:**

- **Spheres escape the vessel.** Thin vessel walls plus high restitution. Thicken walls and add an invisible taller lip.
- **Poor packing** leaves obvious voids that look like a bug. Lower friction, small size jitter (±10%), and a brief settle period at the end.
- **Counter runs past the visual fill** because it counts spawned rather than contained bodies. Count bodies inside the vessel's `Area3D` instead.

**Readability:** the counter is what makes this format work — it converts a passive fill into a question with an answer, which is why viewers stay to the end. Keep it inside the central safe zone, large, monospaced.

---

## 7. `pendulum-array` — coupled swinging bodies

A row of suspended bodies, released together or in sequence; Newton's-cradle and wave-pendulum behaviour.

```
pendulum_count    15
string_length     ramped 1.2 → 2.4    # ramp produces the travelling wave
bob_radius        0.16
bob_mass          1.0
joint             PinJoint3D to static anchor
restitution       0.92        # HIGH — the only recipe that wants near-elastic
friction          0.1
release_angle     0.6 rad
angular_damp      0.0         # damping kills the effect
```

**Failure modes:**

- **Motion decays within two seconds.** Damping, restitution below ~0.9, or too few solver iterations. This recipe is unusually sensitive to energy loss; verify by logging total kinetic energy across 300 ticks — it should decay slowly and smoothly.
- **Wave pattern never emerges.** Length ramp must follow the pendulum period relationship (period ∝ √length), so ramp the *square* of length linearly, not length itself. This is the difference between a mesmerising wave and fifteen bobs swinging randomly.
- **Bobs collide when they should not.** Increase lateral spacing, or restrict motion to a plane with a hinge joint instead of a pin joint.

**Readability:** frame straight-on and perfectly level. This is the one recipe where any camera tilt destroys the effect, because the pattern is the content.

---

## Authoring a new recipe

Work in this order — it front-loads the decisions that are expensive to change:

1. **One sentence describing the mechanical event.** If it takes two sentences, it is two clips.
2. **Block out with primitives and default materials.** Get the motion right before anything is pretty. Most recipes die here and that is cheap.
3. **Tune mass, friction, restitution.** In that order. Mass ratios first — they cause the instabilities that get misdiagnosed as solver problems.
4. **Lock the camera.** Framing changes invalidate tuning, because what reads as fast or slow depends on how much frame the motion crosses.
5. **Then lighting, materials, palette.**
6. **Then audio.**
7. **Then sweep seeds.**

Record the parameter block as JSON from the start so the batch script can sweep it. A recipe that only exists as hand-edited scene values cannot be varied at scale, which defeats the point.

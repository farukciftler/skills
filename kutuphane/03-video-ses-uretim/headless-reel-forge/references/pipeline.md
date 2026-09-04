# The pipeline

Read before changing anything structural. The stage boundaries carry most of the design; moving work across one usually undoes the reason the pipeline is fast.

## The take format

A take is a directory, written once by `sim` and read-only from then on.

```
take/
  take.json      seed, recipe, fps, frame count, timings, params, and the look block
  bodies.json    one entry per body: shape, half-extents, material, tint, static, render, mass
  motion.bin     the transform track — the bulk of the data
  events.jsonl   one JSON object per contact event, in time order
  score.json     written later by score_take.py
  silent.mp4     written later by render
  impacts.wav    written later by synth_impacts.py
```

`motion.bin` is deliberately dumb:

```
offset  size  meaning
0       4     magic "RFM1"
4       4     fps                    (u32 LE)
8       4     frames                 (u32 LE, patched on close)
12      4     bodies                 (u32 LE)
16      4     reserved
20      …     frames × bodies × 7 × f32 LE
                per body: tx ty tz  qx qy qz qw
```

Body index is the order `sim` inserted bodies, and it is the same index space as `bodies.json`. 2,000 bodies × 900 frames is 50 MB — streams and memory-maps without ceremony, and a five-line Python script can read it:

```python
raw = open("motion.bin","rb").read()
frames, bodies = int.from_bytes(raw[8:12],"little"), int.from_bytes(raw[12:16],"little")
m = np.frombuffer(raw, "<f4", offset=20).reshape(frames, bodies, 7)
```

Quantisation and delta coding would buy disk we are not short of, at the cost of that.

**The one rule the format imposes:** every rotation that matters visually must be on the *body*, never on a collider's local transform. `motion.bin` records body poses only. A collider rotated in its own local frame collides in one orientation and draws in another, and the mismatch is invisible until you look at a frame and wonder why the bar is standing up. `chain_drop` learned this the hard way; the fix is one line and the comment is in the source.

## ① sim

```
sim --recipe recipes/cube-rain.json --seed 1001 --out takes/cube-rain-1001
```

Links rapier3d and nothing graphical. Reads the recipe, builds the scene, steps at `physics_hz`, records every `physics_hz / fps` steps, and writes the take.

**Determinism.** Fixed `dt`, an explicitly seeded `Pcg64Mcg`, no `parallel` feature, no threads inside a world. Same binary + same seed + same recipe reproduces the take exactly on this machine. Rapier can also be *cross-platform* bit-deterministic with `enhanced-determinism`, which is mutually exclusive with `parallel` — we do not need it and do not enable it. **Sweeps parallelise across processes, never across threads inside one world.**

`physics_hz` must be a whole multiple of `fps`; the simulator asserts it. A recorded frame landing between ticks is a judder no downstream stage can remove.

**Spawn scheduling.** A recipe that releases everything on frame 0 produces three seconds of action and nine of a static pile. `Scene::schedule` is a list of `(release time, body index, spawn position)`; bodies are created `enabled(false)` and parked far above the frame, then teleported to their spawn point and switched on when due. Parking is recorded in `bodies.json` so the scorer can tell "not released yet" from "left the frame" — without that distinction the scorer punishes exactly the scheduling that makes the clip work.

**Contact events.** Colliders enable `ActiveEvents::CONTACT_FORCE_EVENTS` with a `contact_force_event_threshold`. Each step, before stepping, the simulator caches every body's linear velocity; when an event arrives it uses those *pre-solve* velocities, because the post-solve velocity has already been damped by the very collision being measured. See `procedural-audio.md` for what is done with them.

## ② score

```
python3 pipeline/score_take.py takes/*/ --csv
```

Reads `motion.bin` and `events.jsonl`, renders nothing, takes milliseconds. See `autoselect.md`.

## ③ render

```
render --take takes/cube-rain-1001 --out takes/cube-rain-1001/silent.mp4
render --take … --out preview.mp4 --scale 0.4 --preview
```

Runs no physics. See `renderer.md`.

## ④ audio and ⑤ master

`forge.py` converts `events.jsonl` into the single JSON object `synth_impacts.py` expects, synthesises the track, and muxes with `-c:v copy` — the video is already encoded to spec by the renderer, and re-encoding here would be a generation of loss before Instagram's transcode has even started. Then `ffprobe` checks resolution, codec, pixel format, duration and the presence of an audio track.

## ⑥ publish

```
python3 pipeline/upload_youtube.py runs/2026-08-10/final/*.mp4 --privacy private
```

Private by default; `unlisted` for link-sharing. A vertical clip under three minutes lands in the Shorts feed automatically — there is no flag for it. The API costs 1,600 quota units per insert against a 10,000/day default, so **six uploads a day**; sweep wide, upload narrow. The script needs a one-time OAuth client (setup steps are in its docstring).

For a one-off, driving YouTube Studio in an already-logged-in browser works and needs no API setup at all.

## Adding a recipe

One function in `crates/sim/src/recipes.rs` and one match arm. That is the whole contract — the renderer only ever sees shapes, transforms and tints, so a new recipe needs no renderer change.

Three things to get right, in order of how often they are got wrong:

1. **Start in a valid pose.** Bodies must not interpenetrate on frame 0. `chain_drop` lays its links along an arc-length parameter following the bar's curve precisely so the solver is never asked to untangle a self-intersection — that is where chains explode.
2. **Assert the geometry.** `chain_drop` asserts the long side is shorter than the bar is high. A recipe whose parameters put the payoff on the floor before anything moves should fail loudly, not render.
3. **Break the symmetry.** A perfectly balanced chain is a knife on its edge and takes far too long to commit. Small seeded jitter is what starts the fall — and it is what makes seeds produce different rolls at all.

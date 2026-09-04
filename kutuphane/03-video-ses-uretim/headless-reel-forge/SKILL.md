---
name: headless-reel-forge
description: Mass-produces 9:16 vertical physics Reels/Shorts/TikToks with no window, no editor and no display attached — a Rust rigid-body simulator (rapier) writes a motion cache, a headless Bevy/wgpu renderer replays it on Metal straight into ffmpeg, and impact audio is synthesised offline from the contact log. Use when the deliverable is a physics-driven short-form video or its machinery, and especially when the current pipeline is too slow, needs a window open, or forces a full render before you can tell whether a roll was any good. Trigger on "fizik motoruyla video üret", "arkaplanda video üretsin", "Godot çok yavaş", "simülasyon çok uzun sürüyor", "headless render", "GPU ile video üret", "toplu reels üret", "seed taraması", "prosedürel ses", "çarpışma sesi sentezle", "pencere açmadan render", "9:16 dikey video otomatik" — and whenever someone asks which engine to use for automated physics video, or how to render without opening an editor.
---

# Headless Reel Forge

A production line for "satisfying physics" short-form video that runs entirely in the background: one command in, finished 1080×1920 MP4s out, no window ever opened.

Working implementation lives in `forge/` at the repo root. This document is the method; that directory is the method compiled.

## The architecture decision — read this before writing any code

The instinct when a physics-video pipeline is too slow is to make the engine faster. That is almost never where the time goes. Count what actually happens when you sweep 32 seeds of a 12-second clip:

| Stage | Cost per take | Who pays |
|---|---|---|
| Rigid-body solve, 150–5,000 bodies × 720 frames | **~1 s** | CPU, one core |
| Rasterise 720 frames of 2.07 Mpx with shadows | **20–60 s** | GPU |
| H.264 encode | 2–5 s | media engine (VideoToolbox) or x264 |
| Modal impact audio | 3–8 s | CPU, offline |

Simulation is 2% of the cost. Rendering is 90%. So the pipeline is not organised around making simulation fast — it is organised around **never rendering a take that was not worth rendering**.

That gives four decoupled stages and one file format between them:

```
recipe.json + seed
   │
 ① sim      rapier3d, no graphics linked at all       →  take/ motion.bin + events.jsonl
   │        ~15× real time, N seeds on N cores
 ② score    reads motion.bin, renders nothing         →  take/score.json   ← reject here
   │        milliseconds per take
 ③ render   Bevy + wgpu → Metal, offscreen, no window →  silent.mp4
   │        replays the cache; runs no physics
 ④ audio    modal synthesis from events.jsonl         →  impacts.wav
   │
 ⑤ master   ffmpeg mux + spec check                   →  final.mp4
   │
 ⑥ publish  YouTube private/unlisted, or upload by hand
```

Measured on an M2 Pro: **12 seeds swept, 2 finished 1080×1920 60 fps masters with synthesised audio, spec-checked — 52 seconds, start to finish, no window opened.** Simulation was 2.1 s of that.

Four consequences, all of which are the point:

- **Sweeping is cheap.** 32 seeds cost 32 simulations (~30 s total) and 3 renders, not 32 renders. The select-from-many workflow the genre depends on becomes affordable.
- **Re-rendering is free of simulation.** New camera, new palette, new resolution, 4K master — none of it re-simulates, and none of it can change what happened.
- **Nothing needs a window.** `sim` links no renderer. `render` disables `WinitPlugin` and draws into an offscreen texture. Both run under `nohup`, in cron, over SSH.
- **Determinism is structural, not a discipline.** The motion cache *is* the record. A take cannot drift between preview and master because the master reads the same floats.

## Where the GPU actually goes

The GPU does rasterisation. That is the honest answer, and it is worth stating plainly because the opposite assumption costs weeks.

GPU *physics* on Apple Silicon in 2026 is not available in any form worth building on: NVIDIA Warp is CUDA-only on the GPU path (CPU-only on macOS), Taichi has been in maintenance mode since 2024 with no maintained Metal backend, and Genesis/Isaac/PhysX-GPU are CUDA. What remains is hand-written Metal or MLX compute — weeks of work to lose to a single-core rapier solve, because rigid bodies with joints and mixed shapes are branch-heavy and sequential, exactly what GPUs are bad at.

GPU physics starts winning around 100k+ *identical cheap elements*: sand, granular flow, fluid, high-resolution cloth. If a recipe genuinely needs that, `references/stack-research.md` has the options and the threshold. Check first whether the shot reads better with 300 visible bodies than with 100k particles — on a phone screen it usually does.

## Workflow

### 1. Build once

```bash
cd forge && cargo build --release      # ~6 min the first time, seconds after
```

`sim` and `render` are separate binaries with disjoint dependency trees — `sim` knows nothing about Bevy, `render` knows nothing about rapier. That separation is deliberate: physics plugins for game engines live on the engine's version-upgrade treadmill, and this pipeline does not. Read `references/pipeline.md` before changing the boundary.

### 2. Run the line

```bash
nohup python3 pipeline/forge.py run \
    --recipe recipes/cube-rain.json --seeds 1001-1032 --top 4 \
    --out runs/$(date +%F) > runs/$(date +%F).log 2>&1 &
```

That is the whole product: it simulates every seed in parallel, scores each from its motion track, renders only the winners, synthesises their audio, muxes, checks the output against the Reels spec, and writes a manifest. Read the log when it is done.

Add `--preview --scale 0.4` for look-dev: no shadows, no MSAA, VideoToolbox encode. Roughly 6× faster and it answers every framing question. Doing look-dev at master quality is the most common way to waste an hour here.

### 3. Author the shot, not just the sim

A physically perfect simulation nobody watches is a failure. Before the final render read `references/viral-craft.md` in the sibling `physics-reel-forge` skill — the first-frame hook, the Instagram safe zones (keep the payoff inside the central 1080×1420; ~250 px is lost at the top and ~400 px at the bottom to overlays), palette discipline and the tells that make physics clips look cheap all still apply. None of that changed with the engine.

What did change: **the camera and the container are now scoring inputs.** `score_take.py` projects the final arrangement through the real render camera, so "bodies leave the frame" and "the payoff is a small heap in a tall frame" are numbers, not opinions, and they are available before anything is rendered.

### 4. Tune from the score, not from the video

`pipeline/score_take.py takes/*/ --csv` ranks a sweep in milliseconds and names the failure. The notes are actionable by design: *action is bunched* means the spawn schedule is too tight, *bodies leave the frame* means the container is wider than the frustum, *still moving at the cut* means the duration is short. Read `references/autoselect.md` for what each part measures and how to reweight it per recipe family.

### 5. Sound is half the product

Silent physics clips underperform badly. The audio is synthesised from the simulation's own contact log by modal synthesis — a bank of damped sinusoids per impact with decay rates from the material's Rayleigh damping coefficients — so 400 collisions produce 400 genuinely different sounds and nothing repeats.

Read `references/procedural-audio.md`. The one thing that is materially better here than in the Godot pipeline: rapier's `ContactForceEvent` carries a `started` flag that is true exactly on the step a pair's contact force first crosses its threshold, plus the force direction. Combined with the pre-solve velocities the simulator caches, that gives a correct ½·m_eff·v_n² for every impact — including the bouncy first-frame contacts that Godot's `get_contact_impulse()` reports as zero.

### 6. Publish

```bash
python3 pipeline/upload_youtube.py runs/2026-08-10/final/*.mp4 --privacy private
```

Private by default; `unlisted` for link-sharing. A vertical clip under three minutes lands in the Shorts feed automatically — there is no flag for it. The YouTube API allows about **six uploads a day** on the default quota, so sweep wide and upload narrow. The script's docstring has the one-time OAuth setup.

For a one-off, driving YouTube Studio in an already-logged-in browser works and skips the API entirely.

## Non-negotiables

**The take is the truth.** Never re-simulate to render. If a clip needs to change, change the recipe and produce a new take; do not let two processes have opinions about what happened.

**Fixed timestep, whole-number ratio.** `physics_hz` must be an integer multiple of `fps`. The simulator asserts this. Recording frames that land between ticks is a judder that survives every downstream fix.

**One energy floor decides the whole mix.** `energy_floor` in the recipe controls what counts as a sound event at all. At the default force threshold a 12-second cube-rain emits ~9,000 raw contact events; almost all of them are a settling pile jostling, and rendering them all turns the track into hiss. Tune it with `synth_impacts.py --report`, which prints the distribution, before touching any material parameter.

**Measure before optimising.** When a render is slow, find out whether the time is in the solver (`sim_seconds` in `take.json`), the rasteriser or the encoder. Shadow distance and per-body shadow casting dominate far more often than body count.

## Reference files

- `references/stack-research.md` — every candidate stack evaluated for headless GPU video on Apple Silicon in 2026, what is actually available, and the honest GPU-physics threshold. Read when choosing or defending the stack.
- `references/pipeline.md` — the take format, the four stages in detail, determinism, spawn scheduling, and how to add a recipe. Read before changing anything structural.
- `references/renderer.md` — Bevy 0.19 headless setup, the API landmines, batching, the look block, and profiling. Read before touching `crates/render`.
- `references/autoselect.md` — what each score component measures, how to reweight it, and how to add a criterion. Read when a sweep ranks badly.
- `references/procedural-audio.md` — the event contract, modal synthesis, impact energy, rolling and sliding. Read before wiring up sound.

## Assets

- `assets/recipe-cube-rain.json` — tuned pour/fill recipe. The robust one: seeds barely change the outcome.
- `assets/recipe-chain-drop.json` — tuned jointed-chain recipe. The fragile one: seeds matter and the score spreads. Its geometry (laying links along an arc over the bar rather than hanging them beside it) is the part worth copying.

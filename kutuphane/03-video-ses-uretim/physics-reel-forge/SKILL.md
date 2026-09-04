---
name: physics-reel-forge
description: Builds and runs a rigid-body physics pipeline that mass-produces 9:16 vertical "satisfying physics" Reels/Shorts/TikToks on Apple Silicon — falling cubes, jointed chains whipping over a pivot, dominoes, ball-pit fills, tower collapses — via Godot+Jolt on Metal, deterministic Movie Maker capture, impulse-driven impact audio and VideoToolbox encoding. Use whenever the deliverable is a physics-driven short-form video or its machinery — scene recipes, chain tuning, seed sweeps, batch rendering, render speed, safe-zone framing, seamless loops, impact sound, export settings. Trigger on "fizik motoruyla video üret", "düşen küpler videosu", "zincir simülasyonu", "satisfying physics reels", "toplu video üret", "seed varyasyonu", "render çok yavaş", "9:16 dikey render", "çarpışma sesi ekle", "Godot ile video çıkar", "loop olacak video" — even when the user only says "viral video üretmek istiyorum" but the mechanism is a simulation, or asks whether to use Godot, Blender, Rapier or a custom Metal engine for this genre.
---

# Physics Reel Forge

A production line for the "satisfying physics simulation" short-form genre: 9:16 vertical, 7–20 seconds, one clean mechanical idea per clip, dozens of variants a day.

## The architecture decision — read this before writing any code

Newcomers to this genre assume the hard problem is physics and reach for GPU compute (Metal kernels, Taichi, MLX, XPBD on the GPU). **That is the wrong instinct at this scale and it will cost weeks.**

Count the actual work in a 15-second 60 fps 1080×1920 clip:

| Stage | Load | Right hardware |
|---|---|---|
| Physics: 500–5,000 rigid bodies × 900 frames | trivial | CPU — Jolt across M-series performance cores |
| Render: 900 frames of 2.07 Mpx | dominant | GPU — Metal rasterisation |
| Encode: 900 frames → H.264 | small | dedicated media engine — VideoToolbox |
| Audio: synthesising every impact | small, and offline | CPU, after the render |

So: **do not write a physics engine.** Use Jolt (production-proven, multithreaded, far more stable on jointed chains than naive solvers) and spend the Apple Silicon budget on rasterisation and the hardware encoder. Unified memory means the render target never crosses a bus on its way to the encoder — that is the real Apple Silicon advantage here, not GPU physics.

GPU physics only starts paying off above roughly 50k bodies or for continuum effects (sand, fluid, soft-body cloth at high resolution). If a recipe genuinely needs that, read `references/alternatives.md` — but check first whether the shot can be faked with fewer, larger bodies, which is usually more readable on a phone screen anyway.

**Primary stack:** Godot 4.6 (or ≥4.4) + Jolt + Metal renderer + Movie Maker capture → ffmpeg. Chosen because:
- Jolt is the default 3D engine from 4.6 and handles joint chains without exploding.
- Godot renders directly to Metal on Apple Silicon since 4.4 — no MoltenVK translation layer.
- `--write-movie` runs the sim **non-real-time at a fixed delta**, so output is frame-perfect and deterministic regardless of how long each frame took, and it goes *faster* than real time when the scene is light.
- Movie Maker captures the game's audio bus into the output file. This means collision-triggered impact sounds land in sync for free — the single biggest quality differentiator in this genre, and the thing hand-rolled pipelines get wrong.
- Both 2D and 3D recipes live in one project with one export path.

## Workflow

### 1. Preflight (once per machine, and after any toolchain update)

Run `scripts/preflight.sh`. It reports the Godot version and rendering driver, confirms Jolt availability, and checks which ffmpeg encoders exist. Do not skip this — several instructions below depend on version-gated behaviour, and it is better to discover a missing `h264_videotoolbox` now than after building a scene.

### 2. Set up the project (once)

Read `references/godot-pipeline.md` in full before creating the project. It covers the exact project settings, the fixed-timestep configuration that makes runs reproducible, and — critically — the **SubViewport trick**: Movie Maker's output resolution equals the window size, and window size is clamped by the display, so a 1080×1920 window will not fit on a MacBook screen. Rendering into a 1080×1920 SubViewport while keeping the window small is the only reliable way to get full-resolution vertical output.

### 3. Pick or build a recipe

`references/recipes.md` has seven parametric scene recipes with tuned starting values, including `chain-drop` (jointed box chain falling across a fixed pivot) and `cube-rain` (cubes pouring into a container). Each recipe lists its parameters, its failure modes, and what makes that particular shot readable on a phone.

Start from the closest recipe rather than from scratch. The tuning in these — mass ratios, solver iteration counts, restitution, spawn jitter — is what separates a clip that reads as clean from one that jitters or explodes.

### 4. Design the shot, not just the sim

A technically perfect simulation that nobody watches is a failure. Read `references/viral-craft.md` before rendering the final. It covers the first-frame hook, seamless looping, the Instagram UI safe zones (keep the payoff inside the central 1080×1420 — roughly 250 px is lost at the top and 400 px at the bottom to overlays), palette discipline, impulse-mapped impact audio, and the specific tells that make physics clips look cheap.

### 5. Sweep seeds, don't hand-tune

The genre's economics: most simulation rolls are boring, a few are great, and you cannot predict which from parameters alone. So render many and select.

`scripts/batch_render.py` takes a recipe with a seed list, renders each variant, transcodes it, and writes a JSON sidecar recording the seed and every parameter — so any good roll can be reproduced exactly at higher quality or longer duration. Target throughput on an M-series laptop is roughly a minute per 15-second variant end to end; measure it once and use the real number for planning.

### 6. Synthesise the audio

Silent physics clips underperform badly, and sample libraries repeat audibly once a few hundred collisions are in play. So the sound is synthesised from the collision data itself: the simulation writes an event log, and `scripts/synth_impacts.py` renders the whole track by modal synthesis — a bank of damped sinusoids per impact, with decay rates set by the material's Rayleigh damping coefficients.

Read `references/procedural-audio.md` before wiring this up. The essential points:

- **Do it offline, not in-engine.** No real-time budget means full mode banks, unlimited polyphony, proper reverb — and audio that can be re-rendered in seconds without re-rendering video. Render the final video *silent* and mux the synthesised track in; two sources of audio in one file is how sync problems start.
- **`get_contact_impulse()` is not reliable** — it reports zero on the first frame of a contact, which is the only frame a bouncy body may have. Derive energy from relative normal velocity captured on the tick *before* the solver runs. `assets/contact_log.gd` does this.
- **α and β are the whole material.** `d_i = ½(α + βω_i²)`, so β damps high modes hardest — that single relationship is why metal rings and plastic ticks.
- **The energy threshold in the logger matters more than any material parameter**, because it decides what counts as a sound event at all. Too low and a settling pile becomes a continuous hiss.

### 7. Encode for the destination

Use `scripts/encode_reel.sh`. Read `references/encoding.md` for the reasoning, but the short version:

- **Iteration/preview:** `h264_videotoolbox`. Roughly 4–8× faster than software encoding and it barely touches the CPU, so previews are near-instant.
- **Final master:** `libx264 -crf 17 -preset veryfast`. VideoToolbox needs a meaningfully higher bitrate to reach the same perceptual quality, and Instagram re-encodes everything on ingest — feeding its encoder a cleaner source is what survives. For a 15-second 1080×1920 clip, software encoding still finishes in seconds on Apple Silicon, so the quality is free.
- Deliver MP4 / H.264 / yuv420p / AAC, 1080×1920, 30 fps (60 only if the motion genuinely needs it), 8–12 Mbps. Do not upload HEVC to Instagram — it forces an extra transcode and that is where quality dies.

## Non-negotiables

**Determinism.** Fixed physics tick, fixed `--fixed-fps`, explicitly seeded RNG, seed recorded in the sidecar. Without this, the great roll seen in preview is gone forever and the whole select-from-many workflow collapses.

**Audio is half the product.** Silent physics clips underperform badly, and the sound is what makes the physics feel physical. Synthesise it from the collision log rather than triggering samples — see `references/procedural-audio.md` for the synthesis and `references/viral-craft.md` for how it should sit in the mix.

**Measure before optimising.** When a render feels slow, find out whether the time is in the solver, the rasteriser, or the encoder before changing anything. `references/godot-pipeline.md` has the profiling procedure and the usual culprits (shadow map resolution and per-body shadow casting dominate far more often than body count).

## Reference files

- `references/godot-pipeline.md` — project setup, fixed timestep, SubViewport at 1080×1920, Movie Maker CLI, profiling, known macOS gotchas. Read before building.
- `references/recipes.md` — seven scene recipes with tuned parameters and failure modes. Read when choosing or authoring a shot.
- `references/viral-craft.md` — hook, loop, safe zones, palette, camera, impact audio, anti-slop checklist. Read before the final render.
- `references/procedural-audio.md` — modal synthesis, the material bank, acceleration noise, reliable impact energy, rolling and sliding, mixing. Read before wiring up sound.
- `references/encoding.md` — VideoToolbox vs x264, platform specs, loop assembly, audio mastering, ffmpeg recipes.
- `references/alternatives.md` — Blender+Metal, web/Rapier, Swift+Metal+AVAssetWriter, and the honest threshold at which GPU physics becomes worth it. Read when the primary stack does not fit the shot.

## Scripts

- `scripts/preflight.sh` — toolchain check. Run first.
- `scripts/batch_render.py` — seed sweep orchestrator, sidecar metadata, resume support.
- `scripts/synth_impacts.py` — offline modal synthesiser: collision log in, 48 kHz stereo track out. `--report` alone flags the event-rate and dynamic-range problems that ruin a mix before you render it.
- `scripts/encode_reel.sh` — preview/master transcode, loop assembly, spec validation. Has `--verify`, `--safezone` and `--loop-check` inspection modes; run all three before publishing anything.

## Assets

- `assets/reel_params.gd` — Godot autoload that reads the seed and recipe parameters from the environment. Install this before authoring the first scene; it is the bridge that makes sweeps possible without editing scene files.
- `assets/contact_log.gd` — Godot autoload that records every collision with a reliable energy estimate, and writes the event log the synthesiser consumes.
- `assets/materials.json` — modal material bank: Rayleigh damping coefficients and shape mode templates. The metal/wood/plastic/glass/porcelain values are measured parameters from published work, not guesses.
- `assets/recipe-chain-drop.json` — working recipe to copy and adapt.

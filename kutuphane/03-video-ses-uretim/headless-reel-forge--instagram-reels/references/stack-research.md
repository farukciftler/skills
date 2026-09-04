# Stack research — headless GPU video on Apple Silicon, 2026

Read when choosing the stack, defending it, or being told "just use X". Everything here was checked against current sources in August 2026; where a claim has an expiry date it is marked.

The requirement being solved: **physics → video, fully in the background, GPU-accelerated, on an M2 Pro MacBook, with procedurally synthesised audio.** No window, no editor, no display attached, no human in the loop.

That requirement eliminates most of the field before quality is even discussed, because *headless* on macOS is a much narrower door than on Linux. There is no EGL and no OSMesa; a process either renders through Metal without a surface, or it does not render at all.

---

## The headless matrix

| Stack | Renders with no window on macOS? | GPU? | Verdict |
|---|---|---|---|
| **Rust + wgpu (Bevy)** | **Yes** — adapter requested with `compatible_surface: None`, camera draws to an offscreen texture | Metal | **Chosen.** |
| Swift/ObjC + Metal + AVAssetWriter | Yes — `MTLTexture` render pass, no `CAMetalLayer` | Metal | The ceiling. See below. |
| Godot 4.x | **No** — `--headless` disables the renderer entirely; Movie Maker needs a real window, and window size caps output resolution | Metal | Ruled out by the requirement |
| Blender + EEVEE Next | **No** — headless EEVEE is documented as unsupported on macOS and Windows | Metal | Ruled out |
| Blender + Cycles | Yes | Metal | Works, but seconds-to-tens-of-seconds per 1080×1920 frame → hours per clip |
| Chrome/Puppeteer + Three.js + Rapier WASM | Partly — headless Chrome's GPU path on macOS is fragile and silently falls back to SwiftShader | maybe | Prototyping only |
| Node/Deno + WebGPU (wgpu bindings) | Yes in principle | Metal | Immature; `headless-three-renderer` is a small project, Deno's WebGPU is headless by design but the three.js path is unfinished |
| MuJoCo | Yes, via CGL | GPU, poorly | Robotics visualisation quality; wrong genre |

The interesting entries are the top two, and the difference between them is not performance — it is how much of a renderer you are willing to write.

---

## Chosen: Rust — rapier for the solve, Bevy/wgpu for the pixels

Two binaries with **disjoint dependency trees**, joined by a file. `sim` depends on `rapier3d` and nothing graphical. `render` depends on `bevy` and knows nothing about physics.

That split is the most load-bearing decision in the whole design, and it is worth being explicit about why, because the obvious alternative — Bevy plus `avian3d` or `bevy_rapier3d`, one app, physics and rendering in one loop — is what most people build first.

**Why not one app:**

1. **You cannot reject a take before rendering it.** The point of the whole pipeline is that scoring happens between simulating and rendering. In a single app they are the same loop.
2. **Version treadmill.** A Bevy physics plugin must track Bevy releases. Avian 0.5 exists for Bevy 0.18, Bevy 0.19 shipped June 2026, `bevy_capture` 0.6 targets 0.19 — keeping three packages aligned is a recurring tax paid for nothing, since the renderer never needed physics types.
3. **Re-rendering re-simulates.** Change the palette, re-run the solve. That is both slow and *unsafe*: the take you approved is not necessarily the take you ship.
4. **Determinism gets harder, not easier.** Bevy's schedule is parallel; rapier stepped directly from a single-threaded `main` is trivially reproducible.

**Component notes:**

- **rapier3d 0.35** (August 2026, actively released — 0.32 in January, 0.35.1 in August). The 0.35 `PhysicsWorld` type collapses the old eleven-argument `step()` into `world.step_with_events(&hooks, &events)`, which makes the simulator readable. Determinism: rapier is cross-platform bit-deterministic with the `enhanced-determinism` feature, which is incompatible with `parallel`. **We do not enable it** — same-machine reproducibility is all the workflow needs, and it comes free from a fixed timestep, a seeded PCG and no threading inside a world. Seeds are swept as separate *processes*, which is both faster and safer than threading one.
- **Bevy 0.19** (June 2026) purely as a renderer. PBR, cascaded shadows, bloom, tonemapping, and — the part that matters — automatic batching of entities that share a mesh handle and a material handle, so 105 cubes in 4 colours cost 4 draw calls.
- **`bevy_capture` 0.6** with `Mp4FfmpegCliPipeEncoder`: frames stream as raw pixels straight into an `ffmpeg` child process. **Never write a PNG sequence.** CPU PNG compression of 2 Mpx frames costs 50–150 ms each and is invisible in a GPU profile — it is the single most common hidden bottleneck in home-made pipelines, and it was the dominant cost in the Godot arrangement this replaces.

**Costs, honestly:** first compile is ~6 minutes; Rust is a real language to learn; and Bevy's renderer is good but not Cycles — no path-traced glass, no caustics, no subsurface scattering.

---

## The ceiling: Swift + Metal + Jolt + AVAssetWriter

Render into an `IOSurface`-backed `MTLTexture`, wrap it in a `CVPixelBuffer`, hand it to `AVAssetWriter`. Unified memory means the frame never leaves the GPU's address space on the way to the hardware encoder: no readback, no pipe, no intermediate anything. Nothing else on this list matches it, and Jolt is more stable than rapier on long joint chains.

The cost is a renderer written by hand — no material system, no shadow implementation, no tonemapping that you did not write. Weeks before the first clip.

**Do not start here.** It optimises the cheap part of the problem before knowing which clips are worth making. Revisit only when render time is measurably the constraint on output volume, which for a laptop producing a few dozen clips a day it will not be. If you do, the wgpu readback in `render` is the thing to replace, and the rest of the pipeline is unchanged — that is another dividend of keeping the stages separate.

---

## GPU physics: the honest threshold

The question "can the GPU run the physics too" has a specific, checkable answer on this hardware, and it is no.

| Framework | GPU on Apple Silicon | Status |
|---|---|---|
| NVIDIA Warp | **No** — CPU only on macOS; GPU path requires a CUDA device | Actively developed, wrong platform |
| Taichi Lang | No maintained Metal backend | **Maintenance mode** — active development wound down in 2024 |
| Genesis, Isaac, PhysX GPU | No | CUDA |
| JAX-Metal | Partially | Historically incomplete; verify before depending on it |
| MLX | Yes | Apple's own; an XPBD solver as batched tensor ops is feasible and would run well |
| Hand-written Metal compute | Yes | Maximum control, maximum work |

So the realistic options are MLX or hand-written Metal, and both lose to a single rapier core for this genre. Rigid-body solving with joints, mixed shapes and varying contact counts is branch-heavy and sequential — the workload GPUs are worst at. The measured number from this pipeline: **150 bodies × 720 frames in 0.75 s on one core**, 12 seeds in 2.1 s across six. There is no GPU speedup available on a 2-second problem.

**GPU physics starts paying above roughly 100k identical cheap elements** — sand, granular flow, fluid, high-resolution cloth — where the work is uniform and the branch divergence disappears. If a recipe genuinely needs that, write a WGSL compute shader inside the render crate (wgpu already has the device open) and treat the particles as a separate layer from the rigid bodies. That is a real project, not a switch to flip.

One more consideration before starting it: a sand shot with 100k particles is frequently *less* readable on a phone than the same idea with 300 visible bodies. Check whether the cheap version is the better video first. It usually is.

---

## The escape hatch: rent CUDA

If a shot genuinely needs GPU physics or path-traced rendering, the answer is not to fight Metal — it is to rent an hour of an NVIDIA GPU (Modal, RunPod, Lambda) where Warp, Genesis, PhysX-GPU and Cycles-OptiX all just work. The pipeline is already shaped for it: `sim` and `render` are separate processes exchanging a file, so a remote `sim` writing a take back to the laptop needs no architectural change.

Checked and worth recording: the user's own Ubuntu server has no GPU (VMware SVGA, 4 vCPU Xeon, 8 GB). It can run `sim` — usefully, since simulation is CPU-only and embarrassingly parallel across seeds — but it cannot render.

---

## Delivery spec (verify before uploading)

Instagram Reels, current as of 2026: **1080×1920, 9:16, H.264 in MP4, yuv420p, 3–90 s, 5–10 Mbps, AAC 48 kHz**. Under 1 GB. Do not upload HEVC — it forces an extra transcode on ingest, and that is where quality dies.

Encoder choice: `h264_videotoolbox` for previews (media engine, costs the render nothing), `libx264 -crf 17 -preset veryfast` for masters. VideoToolbox needs a meaningfully higher bitrate for the same perceptual quality, and since Instagram re-encodes everything on ingest, feeding its encoder a cleaner source is what survives. At 12 seconds of 1080×1920 the software encode still finishes in seconds, so the quality is free.

`pipeline/forge.py` checks all of this with `ffprobe` before writing the manifest.

---

## Sources

- [wgpu without a window — Learn Wgpu](https://sotrh.github.io/learn-wgpu/showcase/windowless/)
- [bevy_capture](https://github.com/jannik4/bevy_capture) and [docs.rs](https://docs.rs/bevy_capture/latest/bevy_capture/)
- [Bevy 0.19 release notes](https://bevy.org/news/bevy-0-18/) · [Bevy news](https://bevy.org/news/)
- [Rapier determinism](https://rapier.rs/docs/user_guides/rust/determinism/) · [Rapier 2025 review / 2026 goals](https://dimforge.com/blog/2026/01/09/the-year-2025-in-dimforge/) · [rapier CHANGELOG](https://github.com/dimforge/rapier/blob/master/CHANGELOG.md)
- [Avian physics releases](https://github.com/avianphysics/avian/releases)
- [NVIDIA Warp — platform support](https://github.com/NVIDIA/warp)
- [Taichi: "development has halted"](https://github.com/taichi-dev/taichi/discussions/8506)
- [Blender EEVEE limitations — headless unsupported on macOS/Windows](https://docs.blender.org/manual/en/latest/render/eevee/limitations/limitations.html)
- [MuJoCo visualisation / offscreen backends](https://mujoco.readthedocs.io/en/stable/programming/visualization.html)
- [Jolt Rust bindings (early WIP)](https://github.com/SecondHalfGames/jolt-rust)
- [Deno WebGPU (headless by design)](https://docs.deno.com/runtime/desktop/webgpu/) · [headless-three-renderer](https://github.com/portwatcher/headless-three-renderer)
- [Metal offscreen rendering sample code](https://developer.apple.com/metal/sample-code/)
- Reels specs: [HeyOrca 2026 media specs](https://www.heyorca.com/blog/instagram-media-specs-best-practices-2026) · [Instagram Reel size guide 2026](https://invideo.io/blog/instagram-reel-size-guide/)

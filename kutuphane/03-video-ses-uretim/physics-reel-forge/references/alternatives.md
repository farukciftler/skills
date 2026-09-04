# Alternative stacks

Read when the primary Godot pipeline does not fit the shot. Each entry states honestly when it is the right call and what it costs.

---

## Blender + Bullet + EEVEE Next (Metal)

**When it wins:** the shot needs materials, lighting or geometry beyond what a real-time renderer does well — refractive glass, subsurface scattering, complex meshes, soft-body or cloth. Also when the scene already exists as a `.blend`, or when the work overlaps an existing Blender asset pipeline.

**How:**
1. Set up rigid bodies, then **bake the simulation to keyframes** (`Object → Rigid Body → Bake To Keyframes`). This freezes the sim so re-renders are identical and the renderer never re-simulates. Non-negotiable for reproducibility.
2. Render with **EEVEE Next** (Blender 4.2+) on the Metal backend. Cycles-Metal is available and Apple Silicon supports GPU ray tracing and denoising, but at 1080×1920 a path-traced frame runs seconds to tens of seconds — a 900-frame clip becomes hours. EEVEE Next is the only viable choice for volume work; reserve Cycles for a single hero clip.
3. Output PNG sequence, then encode per `encoding.md`.

**The macOS trap:** EEVEE has historically **not supported truly headless rendering on macOS**. Background rendering (`blender -b`) is documented as working only when a display is present, and macOS specifically has been a weak spot. Before committing a project to this route, test:

```bash
blender -b scene.blend -E BLENDER_EEVEE_NEXT -o /tmp/test_#### -F PNG -f 1
```

If that produces a correct image, the route is viable on that machine and version. If it fails or produces black frames, the options are: render from the GUI with the window open, or switch to Cycles-Metal (which does render headless), or use Godot.

Also note: on Apple GPUs, EEVEE rendering can make Blender's own UI unresponsive because compute and graphics work contend for the same integrated GPU. Expect the machine to be occupied during a batch.

**Cost:** slower per frame than Godot by roughly an order of magnitude, no in-engine collision audio (impact sounds must be generated separately from exported collision data), and Bullet is less stable on joint chains than Jolt.

Blender is available through the Blender MCP connector, which makes scripted scene construction and verification renders practical without leaving the conversation.

---

## Web: Rapier + Three.js in Chrome (WebGPU/Metal)

**When it wins:** 2D recipes, very fast iteration, and when the sim should also exist as an interactive web toy. Zero compile step, hot reload, and Rapier's WASM build with SIMD is genuinely fast — thousands of 2D bodies at interactive rates.

**How:** step the physics world by a fixed delta in a loop decoupled from `requestAnimationFrame`, render each step, read the frame back, pipe to ffmpeg. Driving it from Node with Puppeteer:

```js
// Deterministic: never use rAF timing for the sim
for (let f = 0; f < totalFrames; f++) {
  world.step();                        // Rapier, fixed timestep
  renderer.render(scene, camera);
  const buf = await readPixels();      // gl.readPixels or canvas.toBlob
  ffmpegStdin.write(buf);              // rawvideo → ffmpeg
}
```

ffmpeg side:

```bash
ffmpeg -y -f rawvideo -pix_fmt rgba -s 1080x1920 -framerate 60 -i - \
  -vf vflip -c:v libx264 -crf 17 -preset veryfast -pix_fmt yuv420p out.mp4
```

**Cost:** `readPixels` on every frame is a GPU→CPU stall and the main bottleneck — expect well below real time. Chrome's WebGPU on macOS runs on Metal, so shading is fast; the readback is what hurts. Audio must be synthesised separately from exported collision events. Rapier is deterministic and cross-platform reproducible, which is a genuine advantage over Jolt here.

**Verdict:** excellent for 2D and for prototyping a mechanism before building it properly. Not the volume production path.

---

## Swift + Metal + Jolt + AVAssetWriter

**When it wins:** the absolute performance ceiling, and only when volume justifies building it — hundreds of clips, or a shot that must render dozens of times faster than real time.

**Why it is the ceiling:** render into an `IOSurface`-backed `MTLTexture`, wrap it in a `CVPixelBuffer`, hand it straight to `AVAssetWriter` with VideoToolbox. Unified memory means the frame never leaves the GPU's address space on its way to the hardware encoder — no readback, no PNG encode, no intermediate file. This is the pipeline Apple's own tooling uses and nothing else on this list matches it.

**Cost:** a custom renderer. Jolt integrates cleanly via C++ interop, and Swift 6 makes the AVFoundation side manageable, but there is no scene editor, no material system, no lighting model that was not written by hand. Weeks of work before the first clip.

**Verdict:** the right answer only after the Godot pipeline has proven the content works and render time has become the actual constraint. Building it first is the classic mistake — it optimises the cheap part of the problem before knowing which clips are worth making. There is also real overlap with existing Apple-platform work: procedural audio, RealityKit assets and Metal rendering share concepts, so the incremental cost is lower for someone already fluent there than it looks on paper.

---

## GPU physics: when it actually pays

Frameworks that run physics on the Apple GPU:

- **Taichi Lang** — Metal backend, Python-authored kernels, well suited to particle systems and MPM. Best option here for continuum simulation.
- **MLX** — Apple's own array framework, unified memory, excellent Metal performance. A position-based-dynamics or XPBD solver expressed as batched tensor operations is entirely feasible and would run well.
- **Hand-written Metal compute shaders** — maximum control, maximum work.
- **JAX-Metal** — exists, historically incomplete. Verify current state before depending on it.
- **NVIDIA Warp, Isaac, Genesis, PhysX GPU** — CUDA. Not available on Apple Silicon. Do not plan around them.

**The honest threshold.** GPU physics wins when the problem is *many identical cheap elements* — 100k+ particles, granular flow, high-resolution cloth, fluid. It loses on *few complex constrained bodies*, because rigid-body solvers with joints and varied shapes are branch-heavy and sequential, which is precisely what GPUs are bad at. A 5,000-body rigid-body scene runs faster on Jolt across M-series performance cores than on any GPU implementation, and that covers essentially every recipe in this genre.

So: reach for Taichi or MLX if the shot genuinely requires sand pouring, water filling a vessel, or cloth draping at high resolution. For cubes, chains, dominoes, spheres and towers — which is what the genre is made of — CPU Jolt is both faster and vastly less work.

One more consideration: a sand or fluid shot with a hundred thousand particles is often *less* readable on a phone than the same idea with three hundred visible bodies. Check whether the shot can be faked at lower element count before building GPU infrastructure for it. Frequently the cheaper version is the better video.

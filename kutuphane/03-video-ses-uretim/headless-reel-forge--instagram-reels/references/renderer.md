# The headless renderer

`crates/render` — Bevy 0.19 used purely as a rasteriser. Read before touching it.

## What makes it headless

Three things, all required:

```rust
DefaultPlugins
    .build()
    .disable::<WinitPlugin>()                        // no window is ever created
    .set(RenderPlugin { synchronous_pipeline_compilation: true, ..default() }),
ScheduleRunnerPlugin { run_mode: RunMode::Loop { wait: None } },
bevy_capture::CapturePlugin,
```

and a camera whose target is an offscreen texture:

```rust
RenderTarget::target_headless(width, height, &mut images),
CaptureBundle::default(),
```

wgpu requests its adapter with no compatible surface and gets Metal. Confirmed at runtime — the log line reads `AdapterInfo { name: "Apple M2 Pro", backend: Metal }`. Nothing here needs a display attached, so the process runs under `nohup`, over SSH, or ten at a time.

`synchronous_pipeline_compilation` is not optional. Without it the first frames render before their pipelines are ready and the capture opens with blank or half-lit images — a bug that only shows up in the finished file.

Time is driven manually:

```rust
TimeUpdateStrategy::ManualDuration(Duration::from_secs_f64(1.0 / fps))
```

One app update is one output frame. The render is decoupled from wall time entirely: it runs as fast as the GPU allows and produces the same file at any speed.

## API landmines in Bevy 0.19

Several things moved recently and the compiler errors are not obvious. Current spellings:

| Wanted | 0.19 |
|---|---|
| `bevy::core_pipeline::bloom::Bloom` | `bevy::post_process::bloom::Bloom` |
| `Camera { hdr: true, .. }` | separate `Hdr` marker component |
| `AmbientLight` as a resource | `GlobalAmbientLight` resource; `AmbientLight` is a per-camera component |
| `DirectionalLight { shadows_enabled }` | `shadow_maps_enabled` |
| `RenderTarget::target_headless` | needs `use bevy_capture::RenderTargetHeadless` in scope |

`Hdr` is easy to skip and expensive to skip: without it highlights clip to white before bloom ever sees them, and the effect silently does nothing.

## Batching is the performance story

Bevy batches entities that share **both** a mesh handle and a material handle. The renderer therefore builds two small caches — meshes keyed by `(shape, half-extents)`, materials keyed by tint — so 105 cubes in 4 colours cost 4 draw calls, not 105. Creating a mesh or material per body throws this away and is the difference between a 15-second render and a 3-minute one.

## Where the render time actually goes

Measured on an M2 Pro, 54-second gauntlet course (3,240 frames, 917 bodies, 67 drawn):

| Supersample | Render resolution | Time |
|---|---|---|
| 1× | 1080×1920 | 121 s |
| 2× | 2160×3840 | 279 s |

Fit those two points and the model is **~68 s fixed + ~25 s per megapixel**. Both halves matter, and they call for different fixes:

- **The pixel half** is the supersampling. It is also the quality, so it does not come off without losing anti-aliasing.
- **The fixed half** — about 21 ms per frame — is per-frame CPU work and the GPU→CPU readback stall, and it is *idle GPU time*. That is why concurrency pays: two renders in parallel take 310 s instead of 558 s (**1.8× throughput**), three take 411 s instead of 837 s (**2.0×**). Past three the GPU saturates. `forge.py --render-jobs` defaults to 3.

A hypothesis that did **not** pay: the old pipeline encoded the supersampled frames at 2160×3840 and then decoded, downscaled and re-encoded them at 1080×1920. That looks like obvious waste, and the second pass was indeed 42 s of pure serial cost — but the 4K encode itself was nearly free in wall time, because ffmpeg is a separate process consuming frames while the GPU renders the next one. Folding the downscale into the renderer's own ffmpeg invocation (`encode.rs`) removes the second pass and one lossy generation; it does not make the render itself faster. Measure before believing a bottleneck.

## Frames never touch the disk

`Mp4FfmpegCliPipeEncoder` streams raw pixels straight into an `ffmpeg` child process. **Do not write a PNG sequence.** CPU PNG compression of a 2 Mpx frame costs 50–150 ms and never appears in a GPU profile; over 720 frames that is a minute of pure waste, and it was the dominant cost in the Godot arrangement this replaces.

Encoder selection: `--preview` uses `h264_videotoolbox` (the media engine, so the encode costs the render nothing); masters use x264 at the given CRF. Widths and heights are forced even — H.264 rejects odd dimensions, and it does so *after* the whole clip has rendered.

Note on file size: flat-shaded content compresses extremely well, so a visually lossless CRF 17 master of a 12-second clip lands under 1 MB. That is not a quality problem, but if you want to hand Instagram more bits to work with before its own transcode, drop to `--crf 14`.

## The quality pass (master renders)

Master quality is not one switch, it is five, layered in `setup`:

1. **`GeneratedEnvironmentMapLight`** with a procedural studio cubemap (`quality::studio_cubemap`): graded surround, off-centre overhead softbox, cool side card. This is the biggest single upgrade — it gives every material shaped speculars and coloured ambience. `env_intensity`/`env_warmth` in the look block.
2. **Micro-surface maps** (`quality::normal_map`, `quality::roughness_map`): seeded tiling value-noise baked at startup into a normal + roughness pair for bodies and a broader pair for the set. Uniform roughness is the biggest CGI tell. **Normal maps need vertex tangents and Bevy primitives don't ship them** — `mesh.generate_tangents()` or the maps are silently ignored.
3. **Occlusion**: SSAO on the camera plus `contact_shadows_enabled` on the key light, `DirectionalLightShadowMap { size: 4096 }`, `ShadowFilteringMethod::Gaussian`.
4. **Supersampling** (`--supersample`, default 2 on masters): render at 2× and let the master stage downscale with Lanczos. It is the only AA compatible with SSAO (which requires `Msaa::Off`), and it converges specular shimmer and texture minification, which MSAA never touches.
5. **Depth of field** (Bokeh) focused on the look-at point — `dof_fstop` ~2–2.8 reads as "macro photo of a miniature", which is the genre's look. Master-only, like SSAO.

Material tiers by body class: dynamic bodies get the micro-maps at `body_roughness`/`body_metallic`; static set gets broader maps at `floor_roughness` (a floor smooth enough to reflect the bodies is the cheapest expensive-looking pixel in the frame); static bodies with `tint > 0` render as **polished chrome trim** (plinko pegs, rails) — plain, textureless, because noise maps stretched across a 5 cm face read as streaks.

Costs on the M2 Pro, 720 frames: preview ~7 s; old flat master ~16 s; full quality pass at 2× supersample ~2–3 min. The quality is in the pixels, not the polygon count — body count barely moves any of these.

## Anti-shimmer (generated textures and seams)

Two independent flicker sources showed up the moment the camera started moving, and both have exact fixes:

1. **Generated textures had one mip level.** A procedural `Image` defaults to a single mip, so at any distance the sampler reads full-resolution noise through a moving pixel grid — classic minification aliasing, visible as texture crawl. `quality::mipped_image` builds a box-filter mip chain (normals renormalised per level) and sets a trilinear, anisotropy-8, repeat-mode sampler. This is not optional for any generated texture the camera moves past.
2. **Overlapping construction geometry z-fights.** The 6 cm floor/rail overlaps that seal a polyline track put two near-coplanar faces in the same place; the depth test flickers along every seam. Consecutive track elements sink alternately by 0.8 mm — invisible at viewing distance, unambiguous to the depth buffer.

Final grade lives in the overlay/master encode, not the renderer: `eq=contrast=1.06:saturation=1.16:gamma=0.99`. Instagram's transcode flattens colour; ship slightly hotter than neutral so what survives is what was intended.

## The swept track mesh, the sky, and the world

For course recipes the construction boxes are all `render: "hidden"` and the visual course is **one continuous swept mesh** (`track_mesh.rs`): the simulator writes its centreline to `track.json`, the renderer resamples it through a Catmull-Rom spline (~6 cm steps) and sweeps a channel cross-section along it. Shared vertices along the length mean normals interpolate through every bend — the polyline's 7° kinks vanish entirely — and the floor's U coordinate is arc length, so the texture flows around the course instead of restarting at each element. Cross-section corners stay crisp (vertices duplicated per profile edge); track materials render double-sided so winding can never hide a face.

**Uniform Catmull-Rom needs near-uniform knots.** Feeding the spline a 2.3 m flight next to nine 15 cm corner elements makes it overshoot at the boundary and fold the swept wall into a fin across the channel — an "obstacle" the marbles ghost through, since physics never saw it. Long elements are subdivided every ~25 cm before the spline, capping the knot-spacing ratio; linear subdivision of a straight is still straight.

Containment relies on the same visible/physical split: both rails carry an invisible extension flush with their **inner** face. Flush is the whole point — an extension one rail-thickness outboard leaves the rail *top* exposed, and a deflected marble balances up there, pinned between rail and glass.

The world outside the track: a procedural dusk cubemap (`quality::dusk_sky` — violet zenith, warm horizon band, sparse stars, a low "city" glow, plus the overhead softbox for speculars) used for **both** the `Skybox` and the `GeneratedEnvironmentMapLight`, so backdrop and reflections agree about what world this is; `DistanceFog` toward the background colour so lower flights recede; and ~90 static emissive orbs scattered around the tower — the camera's own orbit animates their parallax, and with bloom they read as depth, not decoration.

## The look block

Everything visual is data, copied into `take.json` so a take is self-contained and re-renderable without the recipe file:

```json
"look": {
  "palette": ["#3a3a44", "#e8734a", "#f2c14e", "#5fa8a0", "#eae4d8"],
  "background": "#101015",
  "camera":    { "position": [0,1.3,3.0], "look_at": [0,0.8,0], "fov": 42.0 },
  "key_light": { "direction": [-0.45,-1,-0.5], "illuminance": 26000.0 },
  "ambient": 190.0, "bloom": 0.12, "shadow_distance": 9.0
}
```

`palette[0]` is the static-geometry slot; dynamic bodies take slots 1…n. Static materials are rendered rougher and read darker on purpose — the set should not compete with the thing the viewer is tracking.

The lighting rig is two directional lights: a key with shadows and a cool fill at ~18% with none. One light makes unlit faces read as black holes on a phone screen; a third rarely earns its shadow cost.

**`fov` is vertical.** In a 9:16 frame the horizontal extent is `vertical × 1080/1920` — a bit over half. Containers sized by eye from a 16:9 habit will always be too wide, and the bodies will leave the frame at the sides. `score_take.py` projects through this exact camera, so it catches it before you render.

## Hidden geometry

`BodyDesc::render` is `"solid"` or `"hidden"`. A container needs a near wall the solver can see and the camera cannot; without it the cubes spill towards the lens, and with it drawn the shot is filmed through the side of a crate. `cube_rain` marks its +z wall `"hidden"`.

## If you need GPU physics after all

wgpu already has the device open, so a WGSL compute shader for a particle layer belongs in this crate, running alongside the replayed rigid bodies rather than replacing them. Read the threshold argument in `stack-research.md` first — below ~100k elements this is a loss.

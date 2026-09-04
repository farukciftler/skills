# Godot pipeline on Apple Silicon

Contents:
1. Version requirements
2. Project settings
3. The 1080×1920 SubViewport problem (read this)
4. Determinism setup
5. Movie Maker CLI
6. Scene skeleton
7. Collision audio wiring
8. Profiling and the usual bottlenecks
9. Known macOS gotchas

---

## 1. Version requirements

- **Godot 4.6+** preferred: Jolt is the default 3D physics engine for new projects.
- **Godot 4.4/4.5** works: Jolt ships in-engine but must be enabled manually via `physics/3d/physics_engine = "Jolt Physics"`, and was still labelled experimental. Enable it — Godot Physics is materially worse at joint chains and stacked contacts, which are exactly this genre's two hardest cases.
- Below 4.4: install the `godot-jolt` GDExtension, or upgrade. Not worth fighting.
- Metal rendering backend: Apple Silicon only (Intel Macs fall back to MoltenVK). Forward+ renderer. Verify with the preflight script rather than assuming — pass `--rendering-driver metal` explicitly if the default is not Metal.

Use the **standard editor build**, not the `.NET` build, unless C# is genuinely needed. GDScript iterates faster and this pipeline is mostly scene authoring plus a few hundred lines of glue.

## 2. Project settings

Set these in `project.godot` (or via Project Settings UI). Values assume 60 fps output; halve tick rates proportionally for 30 fps output.

```ini
[application]
run/max_fps=0                          ; no cap — let non-realtime capture run flat out

[display]
window/size/viewport_width=540         ; small on-screen window
window/size/viewport_height=960
window/vsync/vsync_mode=0              ; DISABLED — vsync throttles capture to display refresh

[physics]
common/physics_ticks_per_second=120    ; 2 substeps per 60fps frame; raise for chains
common/max_physics_steps_per_frame=8
3d/physics_engine="Jolt Physics"
jolt_3d/solver/velocity_iterations=10  ; default 10; raise to 16–24 for long chains
jolt_3d/solver/position_iterations=2

[rendering]
renderer/rendering_method="forward_plus"
anti_aliasing/quality/msaa_3d=2        ; 4x MSAA — cheap on tile-based Apple GPUs, big readability win
lights_and_shadows/directional_shadow/size=2048   ; 4096 is usually wasted at this framing

[editor]
movie_writer/mjpeg_quality=0.95        ; near-lossless intermediate
movie_writer/fps=60
movie_writer/disable_vsync=true
```

Property paths for Jolt solver settings have shifted between minor versions. If a key does not exist, search Project Settings for "jolt" with Advanced Settings enabled rather than guessing — a silently ignored setting is worse than a missing one, because chains will misbehave for no visible reason.

## 3. The 1080×1920 SubViewport problem

**Movie Maker writes frames at the size of the main viewport, and the OS clamps window size to the display resolution.** A MacBook's logical display height is well under 1920 px, so requesting a 1080×1920 window silently produces a smaller video. This is the single most common way this pipeline produces the wrong output.

Solution — render the scene into a SubViewport sized 1080×1920, and display a scaled-down copy in the small window:

```
Main (Node2D or Control)
├── SubViewportContainer          # stretch = false, scale = 0.5
│   └── SubViewport               # size = (1080, 1920)
│       │                        # render_target_update_mode = ALWAYS
│       │                        # handle_input_locally = false
│       └── World (Node3D)        # camera, lights, physics bodies live here
└── (optional) HUD overlay
```

Two ways to get the SubViewport into the movie:

- **`SubViewportContainer` with `stretch = true` and a 0.5 scale.** The container draws the SubViewport texture into the main viewport, so Movie Maker captures the downscaled copy. This gives a 540×960 video — supersampled and clean, but not full resolution.
- **Full resolution: write frames from the SubViewport directly.** In a script attached to the SubViewport's owner, capture `get_texture().get_image()` each frame and save a PNG sequence, driven by a fixed-step counter rather than wall-clock time. Slower per frame due to GPU→CPU readback and PNG encoding, but yields true 1080×1920.

Practical recommendation: **author and sweep at 540×960 via the container path** (fast, and plenty to judge whether a roll is good), then **re-render only the selected winners at 1080×1920** via the readback path. This is the highest-leverage decision in the pipeline — it makes seed sweeps roughly four times cheaper while final quality is untouched.

For the readback path, cap the work: `Image.save_png` on 1800 frames is significant I/O. Save to a RAM disk if the machine has memory headroom:

```bash
# 4 GB RAM disk — ample for 1800 frames of 1080x1920 PNG
diskutil erasevolume HFS+ FrameCache $(hdiutil attach -nomount ram://8388608)
```

Delete it (`diskutil eject /Volumes/FrameCache`) when done — it holds real RAM.

## 4. Determinism setup

Non-real-time capture already fixes the frame delta. Three more things are needed:

**Seed every random call explicitly.** Do not rely on the global RNG.

```gdscript
var rng := RandomNumberGenerator.new()

func _ready() -> void:
    var seed_value := int(OS.get_environment("REEL_SEED"))
    if seed_value == 0:
        seed_value = 12345
    rng.seed = seed_value
```

Passing the seed through an environment variable lets the batch script sweep without editing scene files.

**Never let simulation state depend on `delta` from `_process`.** All physics-relevant logic goes in `_physics_process`, which receives a fixed delta. Spawn timers count physics ticks, not seconds.

**Warm-up frames.** Jolt's broadphase and the renderer's temporal effects both need a few frames to settle. Run 10–20 physics ticks before the first captured frame, or start the action just off-screen so the settling is never visible.

Jolt is deterministic on identical hardware, binary and thread count, but is **not** guaranteed bit-identical across machines or Godot versions. Record the Godot version in the sidecar alongside the seed; if a re-render diverges, this is the first thing to check.

## 5. Movie Maker CLI

```bash
GODOT=/Applications/Godot.app/Contents/MacOS/Godot

REEL_SEED=4211 "$GODOT" \
  --path /path/to/project \
  --write-movie /tmp/out/take_4211.avi \
  --fixed-fps 60 \
  --resolution 540x960 \
  --rendering-driver metal \
  --quit-after 900          # 15 s at 60 fps — frames, not seconds
```

Notes:

- **`--write-movie` requires a rendering context.** `--headless` disables rendering and produces nothing. A window must open. It can be tiny and it can be on a secondary desktop, but it exists. This rules out rendering over plain SSH; use a local session or `serverim-build` style tmux only on a machine with a display session.
- **`--quit-after N` counts frames.** This is how clip length is controlled. Alternatively call `get_tree().quit()` from the scene after N physics ticks, which is more robust when the clip should end on a specific simulation event.
- Output is MJPEG in an AVI container, plus the audio bus mixed in. Large files — expect hundreds of MB for 15 s at `mjpeg_quality=0.95`. Treat it as an intermediate, transcode immediately, delete.
- `movie_writer/movie_file` in project settings can be set instead of the CLI flag; the CLI flag wins and is better for batching.
- Setting the extension to `.png` instead of `.avi` makes Godot write a PNG sequence plus a WAV. Lossless, supports alpha, much slower. Use for hero shots or when compositing.

## 6. Scene skeleton

```
Main
└── SubViewportContainer
    └── SubViewport (1080×1920)
        └── World (Node3D)
            ├── Camera3D               # locked off; see viral-craft.md for framing
            ├── DirectionalLight3D     # shadows ON — contact shadows sell the physics
            ├── WorldEnvironment       # SSAO on, glow on, AgX tonemap
            ├── Static (Node3D)        # StaticBody3D geometry: floor, funnel, pivot
            ├── Spawner (Node3D)       # script: emits bodies on a physics-tick schedule
            ├── Bodies (Node3D)        # RigidBody3D instances land here
            └── ImpactAudio (Node)     # polyphonic player pool; see §7
```

Keep every RigidBody3D's collision shape **primitive** — `BoxShape3D`, `SphereShape3D`, `CylinderShape3D`, or a `ConvexPolygonShape3D` under ~20 vertices. A `ConcavePolygonShape3D` (trimesh) on a moving body is the classic performance and stability catastrophe: it disables useful contact caching and makes tunnelling likely. Static geometry can be concave.

Use `MultiMeshInstance3D` for the visual when body count exceeds a few hundred and all bodies share a mesh, updating transforms from the physics bodies each frame. Below that, plain `MeshInstance3D` children are fine and simpler.

## 7. Collision audio wiring

This is what makes the clips feel expensive. The approach: a fixed pool of `AudioStreamPlayer` nodes, assigned round-robin, with pitch and volume derived from impact impulse.

```gdscript
# On each RigidBody3D: contact_monitor = true, max_contacts_reported = 4
# Connect body_shape_entered, or poll get_contact_count() in _physics_process.

const VOICES := 16
const MIN_IMPULSE := 0.5     # below this, silence — prevents settling chatter
const MAX_IMPULSE := 8.0

func _play_impact(impulse: float, world_x: float) -> void:
    impulse = clampf(impulse, MIN_IMPULSE, MAX_IMPULSE)
    if impulse <= MIN_IMPULSE:
        return
    var t := (impulse - MIN_IMPULSE) / (MAX_IMPULSE - MIN_IMPULSE)
    var player := _next_voice()          # round-robin over the pool
    player.pitch_scale = lerpf(1.25, 0.8, t) * rng.randf_range(0.97, 1.03)
    player.volume_db = lerpf(-22.0, -4.0, t)
    player.play()
```

Four things that matter more than the sample choice:

- **Impulse threshold.** Bodies settling into a pile generate hundreds of micro-contacts. Without a floor, the result is a hiss of clicks. `MIN_IMPULSE` is the most important tuning knob in the whole audio chain.
- **Voice limit.** 16 is plenty. Beyond that, simultaneous impacts sum into distortion rather than reading as "many objects".
- **Inverse pitch mapping.** Heavier impact → lower pitch. This is how ears infer mass; getting it backwards makes big collisions sound like small ones.
- **Bus compression.** Put a `Compressor` and a `Limiter` on the master bus. Physics audio is extremely peaky and mobile playback is loudness-normalised — uncompressed impacts sound quiet and thin on a phone.

Movie Maker captures the master bus into the output file automatically, so no separate sync step is needed. Verify sync on the first render anyway; if the audio drifts, the cause is almost always simulation logic running in `_process` instead of `_physics_process`.

## 8. Profiling and the usual bottlenecks

Before optimising, find where time goes. Run the scene normally (not in capture mode) with the profiler open, or time three variants of the same scene:

```bash
# 1. Physics only — hide the SubViewport, no shadows, no glow
# 2. Full render, no capture
# 3. Full render with --write-movie
```

The deltas isolate solver, rasteriser, and writer respectively.

Ranked by how often they are the actual culprit:

1. **Shadow map updates.** Every dynamic body casting into a 4096 shadow map, re-rendered each frame, is usually the top cost. Drop to 2048, and set `cast_shadow = SHADOW_CASTING_SETTING_OFF` on small or distant bodies. Contact shadows near the collision point are what the eye reads; distant self-shadowing is invisible at this framing.
2. **MJPEG encoding in the writer.** At `mjpeg_quality=1.0` the writer becomes a real cost. 0.95 is visually equivalent and noticeably faster.
3. **Overdraw from transparency.** Transparent or refractive materials at 1080×1920 are expensive on tile-based GPUs. Prefer opaque materials with strong specular; glass reads poorly on a phone anyway.
4. **Per-body script `_process`.** A thousand bodies each running a script is a thousand function calls per frame. Drive them from one manager node instead.
5. **Solver iterations.** Only after the above. Raising velocity iterations from 10 to 24 for chain stability costs far less than one shadow map pass.

Body count itself is rarely the problem below a few thousand primitives — Jolt is genuinely fast, and the M-series performance cores are well suited to it.

## 9. Known macOS gotchas

- **vsync must be disabled** or capture is throttled to display refresh, turning a would-be-faster-than-realtime render into a realtime one. Both the project setting and `movie_writer/disable_vsync` matter.
- **Low Power Mode throttles the GPU.** Turn it off before a batch. Plug in — sustained GPU load on battery downclocks noticeably.
- **The window must stay open.** Minimising, or in some macOS versions fully occluding, the window can cause the compositor to stop delivering frames. Move it to an empty desktop space; do not minimise. Do not let the display sleep mid-batch (`caffeinate -di` around the batch handles this).
- **Retina scaling.** Confirm the produced file's actual pixel dimensions with `ffprobe` on the first render. A 2× backing scale factor silently doubling or halving output dimensions is a real and confusing failure mode.
- **Gatekeeper on first CLI launch.** Launching the Godot binary from the terminal the first time may be blocked. Open the app normally once, approve it, then the CLI path works.

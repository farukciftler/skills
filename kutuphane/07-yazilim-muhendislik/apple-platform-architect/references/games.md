# Games on Apple platforms

Game development has different economics and different failure modes than app development. The single most expensive mistake is choosing the rendering stack before knowing the game's shape.

## Contents
- [Engine decision](#engine-decision)
- [Apple's native stack](#apples-native-stack)
- [Metal 4](#metal-4)
- [RealityKit for games](#realitykit-for-games)
- [Physics](#physics)
- [Game audio](#game-audio)
- [Platform services](#platform-services)
- [Performance targets](#performance-targets)
- [Porting](#porting)
- [The business reality](#the-business-reality)

---

## Engine decision

Ask what the game actually is before answering.

| Game shape | Use | Why |
|---|---|---|
| 2D casual, puzzle, card, word | **SwiftUI** if the "game" is really an interactive UI; **SpriteKit** if it needs sprites, physics, particles | A number puzzle or a card game often does not need a game engine at all. SwiftUI + Canvas + `TimelineView` handles a lot. |
| 2D action, platformer, shmup | **SpriteKit** or **Godot** | SpriteKit if Apple-only and you want native ergonomics; Godot if you'll cross-platform |
| 3D stylised, turn-based, diorama | **RealityKit** | ECS, SwiftUI integration, USDZ pipeline, works on iOS/macOS/visionOS |
| 3D real-time action, larger scope | **Unity** or **Unreal** or **Godot** | Tooling, asset pipeline, and hiring pool dominate any native advantage |
| AAA port from PC/console | **Metal 4** + Game Porting Toolkit 4 | |
| Custom rendering research, procedural | **Metal 4** directly | |
| AR gameplay | **RealityKit + ARKit** | |

**The honest counsel:** for anything beyond a small 2D or turn-based 3D game, a commercial engine wins on total time-to-ship even though the native stack is technically capable. Native wins when the game is Apple-only, needs deep system integration (widgets, App Intents, Foundation Models-driven content, Apple Watch companion), or is small enough that the engine's overhead exceeds its help.

**A native-Swift turn-based 3D game is one of the cases where native genuinely wins** — RealityKit + SwiftUI + SwiftData + Foundation Models composes cleanly for that shape, and no engine gives you Apple Intelligence access without bridging.

## Apple's native stack

| Layer | Framework | Status |
|---|---|---|
| 2D | SpriteKit | Supported, mature, not actively evolving |
| 3D | RealityKit | Current. ECS-based, SwiftUI-first, cross-platform (iOS/macOS/iPadOS/tvOS/visionOS) |
| 3D (legacy) | SceneKit | **Deprecated.** Node-based, proprietary formats. Migrate. |
| Low-level GPU | Metal 4 | Current |
| AR | ARKit + RealityKit | Current |
| Physics | RealityKit physics, SpriteKit physics | Built in |
| Audio | AVAudioEngine, PHASE | PHASE for spatial game audio |
| Services | GameKit, Game Center | Leaderboards, achievements, matchmaking |
| Controllers | GameController framework | MFi, PS/Xbox controllers |
| Porting | Game Porting Toolkit 4 | Now ships open-source agentic coding skills for Metal/Apple best practices |

**SceneKit → RealityKit migration** is the live issue for anyone with a 3D codebase. The conceptual shift is node-graph → Entity Component System: entities are containers, behaviour lives in components and systems. Apple's session is "Bring your SceneKit project to RealityKit". The tutorial gap is real — most RealityKit material is visionOS-focused — but the iOS/macOS API surface is the same.

## Metal 4

Announced WWDC25, the biggest graphics update in years. What matters practically:

- **MetalFX** upscaling — render at lower resolution, upscale. The single biggest lever on mobile GPU budget.
- **MetalFX Frame Interpolation** — generate intermediate frames.
- **MetalFX Denoising** — makes ray tracing and path tracing viable on non-dedicated hardware.
- **Metal shader converter** — DirectX shader conversion, with ray tracing support.
- **Metal tensors** — for custom ML operations in the rendering pipeline; WWDC26 session 330. Relevant to neural rendering.
- **Neural rendering pipelines** — WWDC26 session 359 covers real-time neural rendering with Metal.

Drop to Metal when SpriteKit/RealityKit have a rendering feature you need and cannot express, or when profiling shows you are bound by something only manual pipeline control fixes. Not before.

## RealityKit for games

The ECS model:

- **Entity** — a thing in the scene, a container with a transform and children.
- **Component** — data attached to an entity (`ModelComponent`, `PhysicsBodyComponent`, `CollisionComponent`, custom components for game state).
- **System** — logic that runs each frame over entities matching a component query.

This maps well onto turn-based and simulation games and badly onto tightly-coupled action logic. Custom components hold your game state; systems mutate them; SwiftUI observes.

**Asset pipeline:** USDZ is the format. Reality Composer Pro for scene composition and materials. Blender exports to USDZ (directly or via glTF conversion) — this is the practical authoring path for stylised low-poly work.

**Common gotchas:** materials that look right in Reality Composer Pro and wrong on device (check tone mapping and lighting environment), skeletal animation naming mismatches between DCC tool and RealityKit, and USDZ export dropping socket/attachment empties. Verify on device early and often rather than at the end.

## Physics

- **RealityKit physics** — good enough for gameplay-scale simulation. Deterministic across devices? No. Do not build lockstep multiplayer on it.
- **SpriteKit physics** — Box2D-derived, fine for 2D gameplay.
- **Custom** — if you need determinism (replays, lockstep networking, reproducible procedural content), you need a fixed-timestep deterministic solver, which in practice means an external engine (Godot+Jolt, Rapier) or your own.

If the deliverable is *rendered physics video* rather than interactive gameplay, an offline pipeline in a real engine is the right tool and Apple's frameworks are the wrong one.

## Game audio

- **AVAudioEngine** for the general graph. `AVAudioSourceNode` for procedural synthesis.
- **PHASE** for spatial/positional game audio with occlusion and geometry awareness.
- **Real-time safety is the recurring bug source.** Render callbacks cannot allocate, lock, take Swift ARC retain/release on new objects, or await. Symptoms of getting it wrong: crackle, clicks, `IOWorkLoop skipping cycle due to overload` in the log. The fix is architectural — pre-allocate everything, use lock-free ring buffers to communicate with the audio thread, keep the callback branch-light.
- **Music Understanding framework** (iOS 27) analyses audio across six dimensions on-device — useful for rhythm games and adaptive music.
- **Procedural audio** (rule-generated, zero asset files) is a legitimate strategy for indie games: no asset licensing, tiny bundle, adaptive by construction.

## Platform services

- **GameKit / Game Center** — leaderboards, achievements, real-time and turn-based matchmaking, challenges. Cheap to add, meaningful for retention.
- **GameController** — MFi and standard console controllers. Test with at least one physical controller; the virtual controller API is for development only.
- **Touch** — WWDC26 session 358 "Make your game great with touch" covers the current guidance. Touch controls are the highest-leverage polish item on mobile and the most commonly under-invested.
- **Apple Arcade** — a genuinely different business (upfront funding, no IAP, no ads). Pitch to Apple directly; a real path for well-crafted small games but not something you can plan around.
- **Game Mode** on iOS/macOS — reduces background activity and prioritises the game. Declare support.

## Performance targets

| Target | Budget |
|---|---|
| 60 fps | 16.6 ms per frame total |
| 120 fps (ProMotion) | 8.3 ms |
| Thermal | Sustained load throttles. Test 20+ minute sessions, not 2-minute ones |
| Memory | See `hardware.md`. Jetsam kills you without a crash log people recognise |
| Launch | Under a few seconds to interactive, or reviews say "slow" |

Profile with the Metal System Trace and Game Performance instruments. The WWDC26 session "Find and fix performance issues in your Metal games" (388) is the current reference.

**The oldest supported device is the target.** Not the newest. A game that runs at 60 fps on an A19 Pro and 25 fps on an A17 Pro has a 25 fps rating problem.

## Porting

Game Porting Toolkit 4 (WWDC26) adds open-source agentic coding skills that encode Metal and Apple game development best practices into the porting workflow — session 357, "Speedrun your game port with agentic coding". The historical arc: GPTK 1 (2023) made evaluation possible, GPTK 2 (2025, out of beta) made real ports ship, GPTK 3 added Metal 4 and MetalFX, GPTK 4 adds agentic tooling.

For an existing Unity/Unreal/Godot game, porting to Apple platforms is mostly a build-settings and input/store-integration problem, not a rendering problem. For a DirectX 12 native game, the shader converter plus MetalFX is the path.

## The business reality

Read `appstore-market-analyst` for the numbers. The short version for games specifically:

- Games are still roughly 45–55% of global consumer spend but growth has flattened — around 1% year over year while non-gaming grew 21%. The gaming category stopped being where growth is.
- Paid-upfront games are one of the last places paid-upfront still works at all, mostly for console/PC ports with an established name.
- Turkey has a genuinely strong game development ecosystem (Dream Games' Royal Match being the flagship) and a large local player base, but low local ARPU — Turkish studios target global, not local.
- A polished small game's realistic ceiling on the App Store without marketing spend is low. Apple Arcade, a featuring slot, or an existing audience are the three things that change the outcome.

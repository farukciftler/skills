# Framework map & what changed (state as of August 2026)

## Contents
- [The 2026 release line](#the-2026-release-line)
- [What's new in iOS 27 / WWDC26](#whats-new-in-ios-27--wwdc26)
- [Framework selection table](#framework-selection-table)
- [Deprecated / superseded — do not start here](#deprecated--superseded--do-not-start-here)
- [Swift language state](#swift-language-state)
- [Cross-platform: when native is not the answer](#cross-platform-when-native-is-not-the-answer)

---

## The 2026 release line

| Thing | Current |
|---|---|
| OS generation | iOS 27, iPadOS 27, macOS 27 "Golden Gate", watchOS 27, tvOS 27, visionOS 27 (announced WWDC26, June 8–12 2026; ships to public in autumn 2026) |
| Previous generation | iOS 26 family (the "Liquid Glass" redesign year), macOS 26 Tahoe |
| Xcode | Xcode 27 (beta through summer 2026), Xcode 26.x stable |
| Swift | 6.4 ships in Xcode 27; 6.3 was the spring 2026 release; 6.2 the 2025 one |
| Minimum SDK to upload | iOS/iPadOS/tvOS/visionOS/watchOS 26 SDK, i.e. Xcode 26+, mandatory since **April 28, 2026** |

iOS 27 keeps the same device support list as iOS 26 — nothing was dropped, which is unusual and means the installed base moves as one.

## What's new in iOS 27 / WWDC26

The headline is that WWDC26 was an *intelligence and tooling* release, not a language release.

**Foundation Models framework, rewritten in scope.** It is now a general Swift API for *any* language model, not just Apple's. A `LanguageModel` protocol backs `LanguageModelSession`; Apple's on-device model, Private Cloud Compute, `CoreAILanguageModel`, `MLXLanguageModel`, and third-party Swift packages from Anthropic and Google all conform. Multimodal prompts (image + text), built-in Vision-backed tools (OCR, barcode), a Spotlight-powered local RAG search tool, Dynamic Profiles for swapping model/tools/instructions mid-session, and a `usage` property for token accounting. Free PCC access for App Store Small Business Program members under 2M lifetime first-time downloads. Framework going open source. Full detail in `on-device-ai.md`.

**Core AI — a new framework.** Purpose-built for Apple silicon, for bringing *your own* models on-device: memory-safe Swift API to load, specialize and run models, automatic hardware specialization, ahead-of-time compilation for fast loads, fine-grained inference-memory control, zero-copy data paths, stateful execution. This is the successor path to hand-rolled Core ML pipelines for generative workloads.

**Evaluations framework.** A Swift framework for measuring the quality of AI features — the unit-test analogue for non-deterministic output. If an app ships an LLM feature, this is how you keep it from silently regressing.

**App Intents becomes the distribution surface.** Entity schemas contribute app content to the Spotlight semantic index so Siri can surface it with attribution back to the app. Intent schemas let people act on content without predefined phrases and without code changes as Siri's language understanding expands. New View Annotations API maps views to entities for onscreen conversational reference. New App Intents Testing framework validates the integration through real system pathways without UI automation.

**Platform / UI.** Refreshed materials, refined typography, updated tab and navigation bars across platforms. SwiftUI: high-performance document-based apps with direct disk access, reorderable content across lists and grids, lazily-loaded subviews with prefetching for smooth scrolling, advanced graphics effects composition. UIKit: layouts that adapt for iPhone Mirroring. WidgetKit: widgets customizable through App Intents, dynamic styling.

**Games and media.** Game Porting Toolkit 4 with open-source agentic coding skills for Metal/Apple game best practices. Music Understanding framework (analyses audio across six dimensions on-device). NowPlaying framework (connects playback to Lock Screen, Control Center, Dynamic Island, CarPlay). Core Image RAW processing v9.

**Xcode 27.** Agentic coding built into the IDE — plan-mode feature work, UI prototyping through previews, agent-driven localization, and a Code Assistant Extensions API that lets third-party assistants plug in. Claude/Gemini/GPT agents available; sending code to external services is per-task opt-in, not ambient.

## Framework selection table

Pick by the job, not by novelty.

| Job | Use | Notes |
|---|---|---|
| App UI, new project | SwiftUI | Default across all six platforms |
| Dense/complex UI, precise text, camera chrome | UIKit / AppKit | Interop with SwiftUI is cheap both directions |
| Observable state | Observation (`@Observable`) | Replaces `ObservableObject` + `@Published` |
| Persistence, new app | SwiftData | Check migration/batch limitations before committing |
| Persistence, control needed | Core Data | Migrations, batch ops, existing stores |
| Persistence, query-heavy | GRDB / SQLite | When you want to own the SQL |
| Sync | CloudKit (+ SwiftData/Core Data integration) | Free-ish sync if the model fits |
| Networking | URLSession + `async/await` | Add Alamofire only for a real reason |
| Navigation | `NavigationStack` / `NavigationSplitView` with a path | Model navigation as state |
| Background work | BackgroundTasks, `BGProcessingTask`/`BGAppRefreshTask` | Tight budgets; see shipping.md |
| Widgets, Live Activities | WidgetKit + ActivityKit | Now App Intents-configurable |
| Siri / system integration | App Intents | Mandatory in practice for discoverability |
| On-device LLM | Foundation Models | See on-device-ai.md |
| Custom ML models on-device | Core AI (new) or Core ML | Core AI for generative/large; Core ML still fine for classic models |
| Research-grade / open-weight models | MLX | Also exposed via `MLXLanguageModel` |
| Vision tasks | Vision framework | OCR, barcode, detection — now callable as FM tools |
| Speech | Speech / `SpeechAnalyzer` | On-device transcription |
| 2D games | SpriteKit | Still supported; see games.md for engine choice |
| 3D / AR | RealityKit | SceneKit is deprecated |
| Custom rendering, AAA | Metal 4 | MetalFX upscaling, frame interpolation, denoising |
| Audio (playback) | AVFoundation, NowPlaying framework | |
| Audio (synthesis, real-time) | AVAudioEngine / `AVAudioSourceNode` | |
| Music analysis | Music Understanding (new) | |
| Purchases | StoreKit 2 | See shipping.md |
| Health | HealthKit | Entitlement + strict review |
| Maps | MapKit / MapKit for SwiftUI | |
| Testing | Swift Testing | XCTest for UI tests; they interoperate now |
| CI/CD | Xcode Cloud or GitHub Actions + Fastlane | |

## Deprecated / superseded — do not start here

- **SceneKit** — deprecated. Migrate to RealityKit. Apple's own guidance is the "Bring your SceneKit project to RealityKit" session.
- **`ObservableObject` / `@Published`** — superseded by `@Observable`.
- **Completion-handler APIs** — most have `async` counterparts.
- **XCTest for new unit tests** — Swift Testing is the recommended framework; XCTest is legacy for units, still current for UI tests.
- **OpenGL ES / OpenCL** — long dead on Apple platforms. Metal.
- **UIWebView** — gone. WKWebView.
- **`NSUserActivity`-only Siri integration** — App Intents.

## Swift language state

**Swift 6.4** (Xcode 27) is a friction-removal release, backwards compatible with 6.x, no breaking changes. Notable: better C interop, simplified OS availability checks, fine-grained warning control, `async` support in `defer`, efficient iteration for noncopyable types, ~4× faster URL parsing, `weak let`, `~Sendable`, implicit memberwise initializers, and dropping unnecessary parentheses in type expressions (`any Int?` instead of `(any Int?)`). New concurrency warnings surface as warnings, not errors — fix on your own schedule.

**Swift 6.3** (spring 2026) was the expansion release: Embedded Swift out of experimental, Android an official target, FreeBSD preview. Relevant if you care about Swift beyond Apple platforms.

**Swift 6.2** (2025) gave the ergonomics that matter day-to-day: approachable concurrency (main-actor-by-default modules), typed notifications with `MainActorMessage`/`AsyncMessage` conformances, and the `Observations` async sequence for streaming transactional state changes without redundant UI updates.

**Strict concurrency is not optional.** In Swift 6 language mode the compiler enforces data-race safety — `Sendable` violations are errors, not warnings. For an existing codebase, migrate module by module rather than flipping the whole project.

## Cross-platform: when native is not the answer

Be honest about this rather than reflexively defending native.

- **React Native / Flutter** are reasonable when the app is form-and-list shaped, the team is web/Dart-native, and both platforms must ship together. They cost you: same-day OS feature adoption, Foundation Models/Core AI access without bridging, widget and Live Activity ergonomics, and App Intents depth.
- **Unity / Godot** are the right answer for most non-trivial games. See `games.md`.
- **Native is clearly correct** when the app's value depends on platform features — on-device AI, Siri, widgets, HealthKit, ARKit, Apple Watch, tight system integration. Faruk's Foundation Models-based apps are in this category; a bridge would be the whole product's bottleneck.
- **Swift beyond Apple** is now viable: Swift on Linux servers, Android as an official target, Embedded Swift for microcontrollers. Sharing a domain layer across iOS and a Linux backend in Swift is a real option, not a stunt.

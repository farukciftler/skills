# App architecture on Apple platforms

This is the durable part of the skill — patterns here outlive API churn.

## Contents
- [Choosing an architecture](#choosing-an-architecture)
- [State and data flow](#state-and-data-flow)
- [Persistence decision](#persistence-decision)
- [Navigation](#navigation)
- [Concurrency under Swift 6](#concurrency-under-swift-6)
- [Modularization](#modularization)
- [Testing](#testing)
- [Performance discipline](#performance-discipline)
- [Reference architectures by app shape](#reference-architectures-by-app-shape)

---

## Choosing an architecture

The honest position: **SwiftUI apps need less architecture than the discourse suggests.** SwiftUI already gives you unidirectional data flow, declarative view construction, and dependency propagation through the environment. Layering MVVM or TCA on top of that adds seams — the question is whether you need those seams.

| Pattern | Use when | Cost |
|---|---|---|
| **MV / plain SwiftUI + `@Observable` models** | Most apps. View reads model state directly; logic lives in the model, not a per-view wrapper. | Little. This is the default. |
| **MVVM** | A view has genuine coordination logic worth testing in isolation — multi-step forms, complex validation, orchestration across services. | Ceremony if applied uniformly. Use per-screen, not per-project. |
| **TCA (Composable Architecture)** | Large team, deeply stateful flows, you want exhaustive testability and time-travel debugging, and everyone will actually learn it. | Steep. Big dependency. Compile times. Hard to hire for. |
| **VIPER / Clean layers** | Large legacy UIKit codebase where the team already knows it. | Very heavy for SwiftUI. Don't start here. |

**The test that actually matters:** can you write a test for your business logic without instantiating a view? If yes, your architecture is fine regardless of what it's called.

### Layering that holds up

```
Feature (SwiftUI views + @Observable model)
   ↓ depends on
Domain (entities, use cases, protocols — no framework imports)
   ↓ implemented by
Infrastructure (persistence, network, system frameworks)
```

The rule worth enforcing: **Domain imports nothing from UIKit/SwiftUI/SwiftData.** That single constraint gives you testability, portability to macOS/watchOS, and the ability to swap persistence later. Everything else is negotiable.

## State and data flow

Current property-wrapper semantics:

- `@State` — view-owned value or `@Observable` instance the view creates.
- `@Bindable` — two-way binding to an `@Observable` object you didn't create.
- `@Environment` — dependency injection down the tree. Use custom `EnvironmentKey`s for services rather than passing them through every initializer.
- `@Binding` — two-way handle to a parent's state.
- `@AppStorage` / `@SceneStorage` — small preferences and scene restoration. Not a database.
- `@Query` — SwiftData fetches in views.

`@Observable` classes are plain Swift classes. That is the point: they're testable without any UI framework loaded. Keep business logic in them, not in view bodies.

**Streaming state changes:** Swift 6.2's `Observations` async sequence gives you transactional snapshots — all synchronous changes coalesce until the next suspending `await`. Use it when you need to react to state consistently rather than per-property.

**Anti-pattern:** a global singleton `AppState` holding everything. It couples every feature, defeats preview isolation, and becomes a Swift 6 concurrency problem. Scope state to the feature that owns it and lift only what is genuinely shared.

## Persistence decision

Ask these in order:

1. **Is the data document-shaped and small?** (< a few thousand items, no complex queries) → `Codable` + files, or SwiftData if you want the ergonomics.
2. **Do you want CloudKit sync with minimal work?** → SwiftData or Core Data + CloudKit.
3. **Will you need heavy background writes, batch imports, or complex staged migrations?** → Core Data. SwiftData's story here has been the recurring pain point; verify current status before committing.
4. **Is the workload query-heavy and relational?** (reporting, filtering across joins, full-text search) → GRDB or raw SQLite. You get predictable performance and can read the query plan.
5. **Is it credentials or secrets?** → Keychain. Never `UserDefaults`.
6. **Is it large binary content?** → files on disk with paths in the database, not blobs in the store.

**Migration is the thing people underestimate.** Whatever you pick, write the v1→v2 migration before you ship v1, even if it's trivial, so the path exists and is tested.

## Navigation

Model navigation as data:

```swift
@Observable final class Router {
    var path: [Route] = []
    func push(_ route: Route) { path.append(route) }
    func popToRoot() { path.removeAll() }
}

enum Route: Hashable { case detail(Item.ID), settings, profile(User.ID) }
```

`NavigationStack(path:)` + `navigationDestination(for:)` gives you deep linking, state restoration, and testability for free. Sheets and full-screen covers are separate optional state, not stack entries.

`NavigationSplitView` for iPad/Mac three-column layouts. On iPhone it collapses to a stack automatically — design for the split and let it collapse rather than branching by idiom.

**Deep links and App Intents both land in the router.** Design `Route` so a URL, a Siri intent, a widget tap, and a push notification all map to the same enum case. This is the seam that makes those integrations cheap later.

## Concurrency under Swift 6

The mental model: **isolation domains**. Every piece of mutable state belongs to exactly one — the main actor, a custom actor, or nothing (immutable/`Sendable`). The compiler enforces that you don't cross domains unsafely.

Practical posture:

- **UI-adjacent modules:** main-actor-by-default. Swift 6.2's approachable concurrency makes this the low-friction path — turn it on per-module and most of your code just works.
- **Engines and pipelines:** explicit actors. An audio engine, an image processing pipeline, a sync coordinator each own their state in an actor.
- **Value types crossing boundaries:** make them `Sendable`. Structs of `Sendable` members get it automatically.
- **`@unchecked Sendable`** is a promise you're making to the compiler. Use it only where you genuinely enforce the invariant (e.g. a class guarded by an internal lock), and comment why.

**Real-time contexts are different.** Audio render callbacks (`AVAudioSourceNode`) and Metal command encoding cannot allocate, lock, or await. Swift concurrency does not apply inside them — you need lock-free structures and pre-allocated buffers. Treat the boundary explicitly.

**Migrating an existing app:** enable Swift 6 mode one module at a time, starting with leaf modules that have no dependencies. Flipping the whole project produces hundreds of errors and no path through them.

## Modularization

Split into Swift packages when you have a reason:

- **Compile time** is the most common real reason. Feature modules build in parallel.
- **Preview and test isolation** — a feature module with a stub dependency previews instantly.
- **Multiplatform reuse** — the domain layer shared between iOS app, widget extension, watch app, and Mac app.
- **Enforced boundaries** — the package manifest makes illegal imports a build error rather than a code review comment.

Do not split for aesthetics. Three packages that mutually depend on each other are worse than one target.

**Extension targets** (widgets, App Intents, Share, Notification Service) need shared code — that's a package, plus an App Group for shared containers and `UserDefaults(suiteName:)`.

## Testing

- **Swift Testing** for units: `@Test`, `@Suite`, `#expect`, `#require`, parameterized tests, exit tests for precondition failures. Interoperates with XCTest in both directions in Xcode 27.
- **XCTest / XCUITest** for UI flows.
- **Snapshot testing** (`swift-snapshot-testing`) for view regressions — high value in SwiftUI where visual regressions are easy to introduce and hard to spot.
- **App Intents Testing framework** (iOS 27) validates intent integrations through real system pathways without UI automation. If you ship intents, use it — the alternative was flaky UI tests against Siri.
- **Evaluations framework** (iOS 27) for AI feature quality. Non-deterministic output cannot be unit-tested; this is the mechanism Apple provides.

Test the domain layer hard, the models moderately, the views barely. Inverting that ratio produces slow, brittle suites.

## Performance discipline

**Instrument, then fix.** In order of how often they're the actual culprit:

1. **Main-thread work** — decoding, parsing, image resizing, disk I/O. Time Profiler.
2. **SwiftUI over-invalidation** — a view redrawing because it observes more than it needs. SwiftUI instrument, "Cause of view update".
3. **List/scroll performance** — non-lazy stacks, unbounded view bodies, images decoded at full size. iOS 27's lazy subview loading with prefetching helps here.
4. **Memory** — retained closures, image caches without limits, large `Data` held longer than needed. Allocations + Leaks.
5. **Launch time** — too much in `application(_:didFinishLaunchingWithOptions:)` and static initializers. App Launch instrument. This is also an App Store conversion lever.
6. **Energy** — background location, unbatched network, timers. Energy Log.

Set budgets before optimizing: "cold launch under 400ms on the oldest supported device" is actionable; "make it fast" is not.

## Reference architectures by app shape

**Utility / single-purpose app** (a Rituell or a Numeris): one target, SwiftUI + `@Observable` + SwiftData, no packages, no view models unless a screen earns one. Ship it.

**On-device AI assistant** (a Tacet or a sirr): domain package with the prompt/session orchestration isolated from UI, Foundation Models behind a protocol so you can swap on-device ↔ PCC ↔ third-party, Evaluations framework harness in CI, App Intents surface so Siri can reach it. The protocol seam is the important part — see `on-device-ai.md`.

**Content/media app with a backend:** domain package, infrastructure package with URLSession client and a local cache, feature modules per tab, router at the app level. CloudKit only if the content is genuinely user-private.

**Game:** see `games.md` — different rules entirely.

**Multiplatform (iOS + Mac + Watch):** shared domain + shared design tokens as packages; separate feature layers per platform. Resist "one UI for all" — the platforms want different interaction models and forcing a shared view layer produces something that feels wrong everywhere.

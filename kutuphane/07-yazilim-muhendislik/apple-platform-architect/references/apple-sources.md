# Apple reference sources: where to look things up

The point of this file is to make verification cheap. When a question hinges on an API signature, a version number, a deadline, or a policy, fetch the canonical source instead of recalling.

## Contents
- [Lookup routing table](#lookup-routing-table)
- [Core URLs](#core-urls)
- [How to search Apple's docs effectively](#how-to-search-apples-docs-effectively)
- [WWDC sessions](#wwdc-sessions)
- [Non-Apple sources worth trusting](#non-apple-sources-worth-trusting)
- [Sources to treat with suspicion](#sources-to-treat-with-suspicion)

---

## Lookup routing table

| Question | Fetch |
|---|---|
| Does this API exist / what's its signature | `developer.apple.com/documentation/<framework>` |
| What's new this cycle | `developer.apple.com/<platform>/whats-new/` and `developer.apple.com/wwdc26/guides/<topic>/` |
| Did this break in a point release | `developer.apple.com/documentation/<platform>-release-notes` |
| Is this deprecated | The API page — deprecation banners are on the symbol page |
| What's the deadline for X | `developer.apple.com/news/upcoming-requirements/` |
| Recent policy announcements | `developer.apple.com/news/` |
| Will this pass review | `developer.apple.com/app-store/review/guidelines/` |
| How should this look / behave | `developer.apple.com/design/human-interface-guidelines/` |
| How do I do this in App Store Connect | `developer.apple.com/help/app-store-connect/` |
| Account, certificates, enrollment | `developer.apple.com/help/account/` |
| Swift language / evolution | `swift.org/blog/`, `github.com/swiftlang/swift-evolution` |
| Working sample code | `developer.apple.com/documentation/samplecode/` |
| Someone else hit this bug | `developer.apple.com/forums/` |
| Report a bug | `feedbackassistant.apple.com` |

## Core URLs

**Documentation and platform**
- Documentation library — `https://developer.apple.com/documentation/`
- Technology overviews — `https://developer.apple.com/documentation/TechnologyOverviews`
- Sample code — `https://developer.apple.com/documentation/SampleCode`
- Featured updates — `https://developer.apple.com/documentation/Updates`
- iOS/iPadOS release notes — `https://developer.apple.com/documentation/ios-ipados-release-notes`
- macOS release notes — `https://developer.apple.com/documentation/macos-release-notes`
- Xcode updates — `https://developer.apple.com/documentation/Updates/xcode`

**What's new (per cycle)**
- `https://developer.apple.com/ios/whats-new/` (and `/macos/`, `/watchos/`, `/visionos/`, `/tvos/`)
- WWDC26 topic guides — `https://developer.apple.com/wwdc26/guides/ios/`, `/apple-intelligence/`, `/macos/`, `/games/`

**Frameworks most often needed**
- Foundation Models — `https://developer.apple.com/documentation/FoundationModels`
- Core AI — `https://developer.apple.com/documentation/coreai`
- App Intents — `https://developer.apple.com/documentation/appintents`
- SwiftUI — `https://developer.apple.com/documentation/swiftui`
- SwiftData — `https://developer.apple.com/documentation/swiftdata`
- RealityKit — `https://developer.apple.com/documentation/realitykit`
- Metal — `https://developer.apple.com/documentation/metal`
- StoreKit — `https://developer.apple.com/documentation/storekit`
- WidgetKit — `https://developer.apple.com/documentation/widgetkit`
- Accessibility — `https://developer.apple.com/documentation/accessibility`

**Policy, distribution, compliance**
- App Review Guidelines — `https://developer.apple.com/app-store/review/guidelines/`
- Upcoming requirements — `https://developer.apple.com/news/upcoming-requirements/`
- Latest news — `https://developer.apple.com/news/`
- Human Interface Guidelines — `https://developer.apple.com/design/human-interface-guidelines/`
- App Store Connect help — `https://developer.apple.com/help/app-store-connect/`
- Small Business Program — `https://developer.apple.com/app-store/small-business-program/`
- In-app purchase — `https://developer.apple.com/in-app-purchase/`
- Agreements and guidelines — `https://developer.apple.com/support/terms/`

**Design and assets**
- SF Symbols — `https://developer.apple.com/sf-symbols/`
- Icon Composer — `https://developer.apple.com/icon-composer/`
- Design resources — `https://developer.apple.com/design/resources/`
- Fonts — `https://developer.apple.com/fonts/`

**Games**
- Games hub — `https://developer.apple.com/games/`
- Game Porting Toolkit — `https://developer.apple.com/games/game-porting-toolkit/`

**Swift**
- `https://www.swift.org/` · blog at `/blog/` · evolution proposals at `https://github.com/swiftlang/swift-evolution`
- Swift Package Index — `https://swiftpackageindex.com` (for finding and vetting third-party packages, including platform/version support matrices)

**Community and support**
- Developer Forums — `https://developer.apple.com/forums/`
- Feedback Assistant — `https://feedbackassistant.apple.com/`
- System status — `https://developer.apple.com/system-status/`
- Contact / DTS — `https://developer.apple.com/contact/`

## How to search Apple's docs effectively

Apple's own search is weak. Practical technique:

- **Go straight to the framework URL** if you know it: `developer.apple.com/documentation/<framework>/<symbol>` usually resolves.
- **Web search with `site:developer.apple.com`** plus the exact symbol name beats the on-site search.
- **The symbol page carries the truth** — availability badges (iOS 27.0+), deprecation banners, and the "See Also" block that shows what Apple thinks the replacement is.
- **Release notes carry the breakage.** New APIs are in "What's New"; things that *changed behaviour* are in release notes, and that's where regressions hide.
- **The forums have a DTS engineer presence.** An answered forum thread with a "DTS Engineer" reply is close to authoritative and often the only place a migration question is addressed directly.

## WWDC sessions

Sessions are at `https://developer.apple.com/videos/play/wwdc<year>/<session-number>/` and each has a full transcript, which is fetchable and searchable. For a framework that changed materially, the session is often clearer than the documentation.

WWDC26 sessions worth knowing by number:

| # | Topic |
|---|---|
| 102 | Platforms State of the Union |
| 241 | What's new in the Foundation Models framework |
| 242 | Build agentic app experiences with Foundation Models |
| 319 | Build with the new Apple Foundation Model on Private Cloud Compute |
| 339 | Bring an LLM provider to the Foundation Models framework |
| 334 | Build AI-powered scripts with the fm CLI and Python SDK |
| 243 | Debug and profile agentic app experiences with Instruments |
| 298 / 299 / 335 | Evaluations framework: meet it, robust evals for agentic apps, hill-climbing prompts |
| 324 / 325 / 326 | Core AI: meet it, model authoring and optimization, integrating into your app |
| 330 | Optimize custom ML operations with Metal tensors |
| 240 / 343 / 344 / 345 | App Intents: intelligent Siri experiences, advanced schemas, code-along, new capabilities |
| 295 | Meet the App Intents Testing framework |
| 246 | LLM search using Core Spotlight |
| 262 | What's new in Swift |
| 267 | Migrate to Swift Testing |
| 269 | What's new in SwiftUI |
| 272 | Use SwiftUI with AppKit and UIKit |
| 277 | WidgetKit foundations |
| 278 | Modernize your UIKit app |
| 321 / 322 | Lazy stacks and scrolling; advanced graphics effects in SwiftUI |
| 250 / 251 | Principles of great design; communicate your brand identity on iOS |
| 357 | Speedrun your game port with agentic coding |
| 358 | Make your game great with touch |
| 359 | Build real-time neural rendering pipelines with Metal |
| 388 | Find and fix performance issues in your Metal games |
| 253 / 254 | Music Understanding framework; MusicKit |
| 312 | Meet the NowPlaying framework |
| 303 / 304 / 305 | Responsive camera launch; high resolution photo capture; RAW with Core Image |

For older sessions, `developer.apple.com/videos/` with the topic filter works. "Bring your SceneKit project to RealityKit" is the one people need most often and is a WWDC25 session.

## Non-Apple sources worth trusting

- **Swift Package Index** — package health, platform support, and whether something is actually maintained.
- **avanderlee.com (SwiftLee)** — tracks Swift Evolution weekly; reliable on concurrency.
- **hackingwithswift.com** — good for "how do I do X in SwiftUI", occasionally behind on the newest APIs.
- **objc.io / Point-Free** — deeper architectural material.
- **MacRumors / 9to5Mac** — reliable for *what Apple announced*, not for API detail.
- **Apple Newsroom** — `apple.com/newsroom/` for official announcements with dates you can cite.

## Sources to treat with suspicion

- **Blog posts without a date**, and dated posts more than one OS cycle old on anything API-specific.
- **Content-farm listicles** ("Top 10 iOS frameworks 2026") — these recycle each other and are frequently wrong about deprecations.
- **Stack Overflow answers** predating Swift concurrency, SwiftUI's `@Observable`, or SwiftData. Check the date before the votes.
- **Anything describing SceneKit as current.**
- **Your own memory on version numbers, prices, and deadlines.** These are exactly the facts that change and exactly the facts people act on.

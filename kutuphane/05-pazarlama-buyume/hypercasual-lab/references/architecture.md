# iOS Architecture — Unity vs native, and the prototype blueprint

Read this at G3, before any code. Verify framework and SDK specifics against current Apple and vendor documentation — deprecations and required-API rules in this area change every OS cycle, and a stale assumption here surfaces as a rejected build.

## Contents
- The engine decision
- Native prototype blueprint
- Unity prototype blueprint
- Instrumentation (mandatory before G4)
- App Review gates for ad-funded games

---

## The engine decision

The decision is made by the **publishing path**, not by preference.

### Choose Unity when
- A publisher pitch is realistic. Publishers run their own SDK, analytics wrapper and test harness, and these are Unity packages. A native prototype cannot be dropped into that pipeline. Confirm each target publisher's current submission requirements before committing — do not assume.
- Android is in the plan, now or within a quarter.
- The mechanic is 3D, physics-driven, or needs a scene graph and a level editor.
- The concept will need many rapid variants — Unity's editor iteration loop wins on variant count.

Cost: engine licensing terms and revenue thresholds change; check Unity's current pricing tiers rather than relying on any remembered figure. Also check current build-size and startup-time characteristics, both of which matter for install conversion.

### Choose native SpriteKit + GameplayKit when
- Self-publishing, iOS-only, and speed to a retention read is the priority
- The mechanic is 2D
- The builder is already fluent in Swift — this is the whole argument. Engine fluency is worth more than engine features at prototype scale.

What you give up: cross-platform, the asset ecosystem, and publisher compatibility. What you gain: a small binary, fast cold start, no engine tax, and iteration in a toolchain already familiar.

Ad SDKs are not a differentiator here — the major mediation platforms ship first-class native iOS SDKs alongside their Unity packages. Verify current native SDK support for the chosen mediation before finalizing.

### The trap
Building native to move fast, testing well, and then needing Unity for the publisher pitch. That is two builds. Decide the path at G3, not at G5. If the path is genuinely undecided and a publisher outcome is plausible, Unity is the safer default despite the slower start.

---

## Native prototype blueprint

Optimized for a days-not-weeks prototype whose only job is producing a readable D1 number.

```
Game/
  App.swift              // SwiftUI App, single window
  GameViewController      // hosts SKView
  Scenes/
    GameScene.swift       // the one mechanic
    GameOverOverlay.swift
  Core/
    GameState.swift       // GKStateMachine: Ready → Playing → Failed → Rewarded
    Difficulty.swift      // one curve, one tunable struct
  Services/
    Analytics.swift       // protocol + concrete impl, event enum
    Ads.swift             // protocol + mediation impl, placement enum
    Persistence.swift     // UserDefaults is sufficient at prototype scale
```

Rules that keep the prototype honest:

- **One scene.** Menus are a G5 concern. The app opens directly into playable state — first-session time-to-play is a retention driver and adding a menu at prototype stage corrupts the very number being measured.
- **State machine, not booleans.** GameplayKit's state machine keeps the ad trigger points explicit and prevents the classic bug where an interstitial fires during play.
- **Protocol-wrapped ads and analytics.** Both services behind a protocol so the mechanic can be tested without network, and so the mediation vendor can be swapped without touching game code.
- **No accounts, no cloud save, no settings, no localization** at prototype stage.
- **SwiftUI only for overlays.** SpriteKit owns the play surface.
- Audio via the `procedural-game-audio` approach — zero asset files, no licensing questions, no build-size cost.

Deliberately deferred to G5: SwiftData, Game Center, IAP, remote config, live-ops, localization.

---

## Unity prototype blueprint

- One scene, one prefab-driven mechanic, a single `GameManager` with an explicit state enum
- ScriptableObject for the difficulty curve so variants are data edits, not code edits
- Ad and analytics calls behind an interface from day one, same reasoning as native
- Strip the template: no unused packages, no default post-processing stack, no analytics duplication. Install conversion is sensitive to download size, and a bloated prototype distorts the CPI read.
- If pitching a publisher, install their SDK per their current documentation *before* the G4 test — retrofitting it invalidates the collected data.

---

## Instrumentation — mandatory before G4

A build that ships to a paid test without these events produces an unreadable result and wastes the entire budget. Treat this as a hard gate on G3 completion.

Minimum event set:

| Event | Why it exists |
|---|---|
| `app_open` with session id | Denominator for everything |
| `game_start` | Time-to-first-play, the strongest early retention predictor |
| `level_start` / `level_complete` / `level_fail` with level index and duration | Where the funnel leaks — this is the iterate-vs-kill evidence |
| `session_end` with duration | Playtime per session |
| `ad_request` / `ad_shown` / `ad_clicked` / `ad_failed` per placement | Fill and placement health |
| `rewarded_offered` / `rewarded_accepted` / `rewarded_completed` | Rewarded engagement rate |
| `first_open` with attribution payload | Ties installs to campaign and creative |

Retention must be computable per install cohort and per creative. If the analytics setup cannot slice D1 by creative, the G2 winner cannot be validated at G4 and the two tests do not connect.

Verify the current attribution stack before wiring: ATT prompt requirements, SKAdNetwork versus AdAttributionKit status and minimum OS targets, and whether the chosen MMP/mediation supports the current framework. This area has moved repeatedly and the correct answer is whatever Apple's current documentation says, not what was true last cycle.

---

## App Review gates for ad-funded games

These are the recurring rejection causes for this genre. Check the current App Review Guidelines text — numbering and wording change — but the substance is durable:

- **Clone / spam.** A thin reskin of an existing mechanic with no differentiation gets rejected, and repeat offenses put the developer account at risk. This is the practical reason the saturation read at G0 is not optional.
- **Minimum functionality.** A prototype that is genuinely one screen with no depth can be judged too thin to be an app. The prototype needs enough loop to read as a game.
- **Privacy manifests and required-reason APIs.** Every third-party SDK, including every ad adapter, must carry a valid privacy manifest, and any required-reason API use must be declared. Ad SDKs are the most common source of failures here — use current SDK versions and verify each adapter.
- **Privacy nutrition labels.** Must accurately reflect what the ad SDKs collect, including IDFA when ATT is authorized.
- **ATT compliance.** No collecting tracking identifiers before authorization, and no dark-pattern pre-prompts that misrepresent the choice.
- **Ad content and age rating.** The mediated ad content has to suit the declared age rating; a kids-directed rating carries substantially stricter rules and materially different monetization economics.
- **Placement behavior.** Ads that block a required interaction, or interstitials the user can trigger accidentally at the same coordinates as a game control, draw rejections and are also just bad for retention.

Budget review time into the schedule. First-submission review turnaround is variable and a rejection cycle can add days — a G4 test scheduled against an unreviewed build is a plan with an unfunded dependency.

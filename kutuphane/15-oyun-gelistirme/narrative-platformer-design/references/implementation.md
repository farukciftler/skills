# Implementation: Tools, Data Format, Localization

## Contents
1. Choosing a dialogue tool
2. Swift / iOS options
3. Custom JSON schema (engine-agnostic)
4. Reactive dialogue: flags, counters, priority
5. Localization-ready writing
6. Text presentation defaults
7. Accessibility

Tool versions, plugin support and library status change. Verify current state (GitHub READMEs, release notes) before recommending a specific version.

---

## 1. Choosing a dialogue tool

| Tool | Style | Engines | Good for | Watch out |
|---|---|---|---|---|
| **Yarn Spinner** | screenplay-like text script, nodes | Unity (mature); Godot & Unreal plugins | writer-friendly branching; shipped in Night in the Woods, DREDGE, A Short Hike | core MIT, newer code under a different license; check plugin maturity per engine |
| **Ink (inkle)** | text-first markup, knots/stitches, very powerful flow control | official Unity integration; community runtimes elsewhere | heavy branching, state, text-heavy games | no visual graph; characters/audio/images handled in your own code |
| **Twine** | browser, passages | export to web | prototyping story structure fast | not a runtime for most engines |
| **Custom JSON/YAML** | your own | anything | small games, few branches, full control | you build tooling (validation, preview) yourself |

Rule of thumb for a light-dialogue platformer: **custom JSON** or **Yarn**. For heavy branching or reactive systems: **Ink**.

## 2. Swift / iOS options

For SpriteKit/SwiftUI/RealityKit games:
- **InkSwift** (maartene): Swift support for Ink. Its README recommends a newer **native pure-Swift runtime** for new projects and marks the older JavaScriptCore/inkjs bridge as legacy; the native runtime lists known gaps (e.g. LIST, RANDOM, threads, EXTERNAL functions, shuffle text). Check the gap list against your script before committing.
- **SwiftInk** (Meorge): a Swift port of the Ink runtime that follows the C# engine closely; its README says to assume it's unstable.
- **ink-iOS** (russellquinn): older Objective-C wrapper around the JS runtime via JSContext.
- **Custom JSON** decoded with `Codable`: the simplest robust option for a small platformer with barks + short linear scenes + a few flags. Recommended default unless branching is heavy.

Swift `Codable` sketch for the schema below:
```swift
struct DialogueLine: Codable {
    let id: String
    let speaker: String
    let text: String
    let emotion: String?
    let requires: [String]?     // flags that must be true
    let excludes: [String]?     // flags that must be false
    let sets: [String]?         // flags set when shown
    let priority: Int?          // higher wins
    let maxChars: Int?
}
struct DialogueScene: Codable {
    let id: String
    let trigger: String         // "room_enter:2-04", "npc_talk:teo", "death_count>=50"
    let once: Bool
    let lines: [DialogueLine]
}
```

## 3. Custom JSON schema

```json
{
  "scene_id": "ch4_rope",
  "trigger": "room_enter:4-09",
  "once": true,
  "priority": 50,
  "requires": ["met_teo"],
  "control": "walk_only",
  "checkpoint_after": true,
  "lines": [
    {"id": "ch4_rope_001", "speaker": "TEO", "text": "He took the good rope.", "emotion": "flat", "anim": "coil_rope"},
    {"id": "ch4_rope_002", "speaker": "MIRA", "text": "...That's what you're mad about?", "emotion": "confused"},
    {"id": "ch4_rope_003", "speaker": "TEO", "text": "It was a really good rope.", "anim": "turn_away", "sets": ["teo_brother_hint"]}
  ]
}
```

Conventions:
- **Stable string IDs** (`chapter_scene_###`). Never key localization on the English text.
- `speaker` uses a fixed cast key; display names live in the localization table.
- Stage directions go in fields (`anim`, `sfx`, `camera`), never inside `text`.
- `dialogue_lint.py` reads this format (array of lines, or an object with `lines`).

## 4. Reactive dialogue

Hades-style bucket (see `dialogue-craft.md` §8), minimal version:
- Keep `flags` (set of strings) and `counters` (dict: deaths_total, deaths_in_chapter, visits_hub, secrets_found).
- Each scene has `requires`, `excludes`, `priority`, `once`.
- On trigger: filter valid scenes → pick highest priority → tie-break randomly among the least-recently-played → mark played.
- Tiers: generic 0–19, specific 20–59, essential 60+ (essential always wins).
- Author 3–5 generic variants per NPC per chapter so returning players don't hit silence.

Good platformer triggers: death count thresholds (10, 50, 100, 500), dying to the same hazard 5×, finding a secret, skipping the last conversation, returning after a long absence, finishing a chapter fast or slow.

## 5. Localization-ready writing

- Leave **35%+ headroom** in bubbles/boxes for European languages (German commonly +20–35%; short strings expand most). Prefer boxes that grow vertically.
- No string concatenation ("You found " + n + " stars") — use full sentences with placeholders and plural rules.
- Avoid puns and idioms that carry plot information; if a joke must be a pun, add a translator note with the intent.
- Give each string a **context note**: who speaks, to whom, mood, max length, where it appears.
- No text baked into textures/sprites (signs, murals); keep it as a string layer or make it wordless.
- Gendered languages: record the speaker's and addressee's gender in context notes (Turkish "o" vs English he/she is a common source of errors in the other direction too).

## 6. Text presentation defaults

- Player-advanced text; tap/press once completes the line, again advances.
- Typewriter speed: fast by default, configurable, with an "instant" option.
- Hold-to-fast-forward for repeat viewings; skip for scenes seen before.
- Auto-advance for barks only (≈ 3 s + 0.05 s/char), and barks never block input.
- Speaker identification: name tag or distinct bubble color/tail; never rely on color alone.
- Text log/backlog for anything longer than a few lines.

## 7. Accessibility

- Minimum readable font size on the target device (test on the smallest phone you support).
- High-contrast option for bubbles.
- Reduce motion: disable screen shake and bubble wobble.
- Captions for important audio cues (a voice in the dark, a distant scream) when they carry story.
- Assist mode for difficulty, framed without shame, so everyone can reach the story.

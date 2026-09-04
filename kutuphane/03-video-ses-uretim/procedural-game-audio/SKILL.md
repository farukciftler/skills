---
name: procedural-game-audio
description: >
  Build procedural (rule-generated, zero-asset) music and SFX engines for Apple-ecosystem apps —
  iOS/macOS/visionOS games and apps — using pure AVFoundation (AVAudioSourceNode), with a
  real-time-safe three-layer architecture (synth → sample-accurate clock → composer), adaptive
  intensity-driven themes, non-overlapping SFX, ducking, and crossfades. Use this skill whenever
  the user mentions procedural music, adaptive/dynamic game music, "prosedürel müzik",
  synthesizing audio without asset files, AVAudioSourceNode, AVAudioEngine render callbacks,
  chiptune/ambient generation in Swift, an AudioKit-vs-native decision, background music for a
  game, sound effects that "shouldn't overlap", or is debugging audio crackle, clicks,
  AudioConverter -302 errors, or "IOWorkLoop skipping cycle due to overload" — even if they don't
  say "procedural". Also use it when reviewing or extending an existing AVAudioSourceNode-based
  engine for real-time safety.
---

# Procedural Game Audio (Apple / AVFoundation)

Generate an app's entire soundtrack **from rules instead of audio files**: music theory constrains
randomness so it sounds composed, a sample-accurate clock decides *when*, and cheap synthesis
decides *how it sounds*. The result is infinite, non-repeating, game-reactive audio with zero
assets and zero dependencies.

A battle-tested reference implementation lives in this repo at
`ZarVeZindanApp/Sources/Presentation/Audio/AudioEngine.swift` (~900 lines, single file, ships in a
real game). When working in this repo, read it before writing new audio code — extend it rather
than building a second engine.

## Dependency decision (make it first)

- **Default: pure AVFoundation.** One `AVAudioEngine` + `AVAudioSourceNode`s. No SPM/pbxproj
  churn, no version risk, full control. Everything below assumes this path.
- **AudioKit** (`SoundpipeAudioKit` oscillators, `AudioKitEX` sequencer) only when the project
  already depends on it or needs its instrument library. The architecture below still applies —
  only layer 1 changes.

## The three layers

```
[1] SYNTH     (audio thread)   — turns "note" into samples: oscillators + ADSR + filter + delay tail
[2] CLOCK     (audio thread)   — sample counter → 16th-note steps → bars. Never Timer/Dispatch.
[3] COMPOSER  (serial queue)   — decides notes: scale + random walk + Euclidean rhythm + chords
```

Game code only ever talks to layer 3's inputs: `startMusic(theme)`, `setIntensity(0…1)`, and
semantic SFX methods. It never touches nodes or buffers.

### Thread contract (the architecture IS this table)

| Thread | Owns | Absolutely never |
|---|---|---|
| Audio render callback | synthesis, per-sample envelopes/filters, the step/bar counter, gain slews | allocate, lock, dispatch, retain/release, read `@MainActor`, call `pow/exp` per note, stdlib RNG |
| Serial compose queue (`DispatchSourceTimer` ~60 ms) | ALL composition, theme swaps, intensity→layer/BPM staging, MIDI→phase-increment math (`pow` lives here) | touch AVAudioEngine graph, block, talk to UI |
| Main thread | public API entry, settings snapshots, SFX trigger writes | any per-sample work |

Data flows composer → audio via **double-buffered POD step tables** indexed by `barIndex & 1`:
audio reads `[bar & 1]`, composer writes `[(bar+1) & 1]` one bar ahead. Different buffers ⇒ no
race; worst case is one stale bar. Control values (gain targets, flags) are plain vars the
callback snapshots **once per buffer** — the benign-race pattern; document it where used.

## Real-time safety checklist (verify every one before shipping)

1. **Sample rate comes from the engine's output hardware**, not the session:
   `engine.outputNode.outputFormat(forBus: 0).sampleRate` (fallback: session rate, then 48 000).
   Reading `AVAudioSession.sampleRate` right after `setActive` can disagree with the real output
   rate → CoreAudio splices in an AudioConverter → it fails with **-302** and floods
   **"HALC_ProxyIOContext IOWorkLoop: skipping cycle due to overload"**. One `AVAudioFormat`
   (mono, that rate) feeds every `connect` so the graph stays converter-free.
2. **All buffers pre-allocated** in `ensureStarted()` as `UnsafeMutablePointer` to POD structs —
   step tables, voice pools, delay/allpass lines. Nothing allocates after start.
3. **No stdlib randomness in callbacks** — inline xorshift/LCG on a plain integer var.
4. **Every audible gain is slewed**, never stepped: music master, duck, per-layer, SFX master
   (~20 ms ramp). A settings toggle mid-sound must fade, not click.
5. **Envelopes on every voice** (even 20 ms noise bursts get a 2 ms attack) — clicks come from
   discontinuities, not from synthesis.
6. **Anti-denormal guard** in feedback paths (delay/allpass): add-subtract `1e-20` or keep a
   constant signal (an always-on pad) in the loop.
7. Session: `.ambient` + `.mixWithOthers` for games; failures degrade to silent no-ops so the
   engine is always safe to instantiate (including simulators and tests).

## Non-overlap rules ("efektler üstüne binmesin")

- **One music node, ever.** A theme change *retunes the composer* behind a fade — never a second
  node. Two themes physically cannot sound at once.
- **Theme identity dedup.** Give every theme a stable context id; a request for the
  already-playing theme is a **no-op** (refresh live params in place). Without this, a SwiftUI
  `.onAppear` re-fire punches a fade-to-silence hole in the bed — it WILL happen.
- **Transitions are fade-through-silence on one node** (~0.45 s per direction, bar-quantized).
  Call it what it is in comments — a true crossfade needs a second composer; don't pretend.
- **SFX = small fixed voice pool (4), replace-oldest.** Multi-note gestures keep their notes;
  polyphony stays capped; chaos is impossible. Sequencing a gesture's notes with
  `DispatchQueue.main.asyncAfter` is fine — that's control-rate, not audio-rate.
- **Music ducks under SFX** (to ~0.22, ~8 ms attack / ~120 ms release) so effects never fight
  the bed. Derive the duck from actual voice activity.

## Composer rules that make it sound composed

- Notes only from a scale; mysterious/D&D = minor modes (aeolian/dorian/phrygian) + minor
  pentatonic; tension = tritone or ♭2. Melody random-walks the scale *index* with small weighted
  steps `[-2,-1,-1,0,1,1,2]` and **rests 40–60 % of steps** — silence is the mood.
- Rhythm from Euclidean patterns (E(3,16)…E(9,16)); bass plays chord roots on its pattern; a 4–8
  chord minor progression grounds everything; pad arpeggiates chord tones.
- **Adaptive:** reduce game state to one `intensity 0…1` → layer gains (pad always; arp > 0.3;
  perc > 0.6) and BPM (base + intensity·range), adopted **at bar boundaries** so the music
  evolves instead of cutting. Battle/boss themes may pin an intensity floor.
- Each context (menu, per-biome exploration, battle, boss) gets its own root/mode/BPM/patterns so
  they are genuinely different. Concrete ready-to-copy tables, sting recipes, and SFX gesture
  recipes (dice clatter, hits, potion glugs, heals, blocks): read
  [references/theme-design.md](references/theme-design.md).

## Public API shape (the seam game code binds to)

Keep one `@unchecked Sendable` singleton with: `startMusic(<context>)`, `stopMusic()`,
`setIntensity(Float)`, sting methods, semantic SFX methods (name them after game meaning:
`enemyHit(heavy:)`, `playerHurt(heavy:)`, `drinkPotion()` — not `playTone`), and
`applySettings()`. `applySettings()` snapshots `@MainActor` settings (music/SFX enabled) into
plain flags **on the main thread** (`MainActor.assumeIsolated`), and every music start calls it so
a disabled toggle is always honored. UI toggles call it via `.onChange`.

Wire music to game phases at the coordinator level (one call per phase transition: menu, act
start, combat start (boss flag), victory/defeat), and SFX to the *impact frame* of animations —
not to button taps — so sound, shake, and damage numbers land together.

## Verification (do this, not just a build)

1. Build, install, launch on the simulator; stream logs and **prove the absence** of the two
   killers:
   ```bash
   xcrun simctl spawn <device> log stream --level debug \
     --predicate 'eventMessage CONTAINS "AudioConverter" OR eventMessage CONTAINS "IOWorkLoop" OR eventMessage CONTAINS "-302"'
   ```
   Benign: stereo 48k↔48k mixer converters. Fatal: any `-302`, any `0 Hz` source, any
   "skipping cycle due to overload".
2. Trigger every theme transition and SFX path via the app's flows; listen for clicks at: theme
   change, settings toggle mid-sound, SFX pile-ups, note boundaries.
3. Timbre/mix judgment needs a physical device — say so honestly if only the sim was tested.

## Known pitfalls (symptom → cause → fix)

| Symptom | Cause | Fix |
|---|---|---|
| `-302` + IOWorkLoop overload at launch | format from session rate, not output hardware | checklist #1 |
| Music dips to silence for no reason | theme re-request without identity dedup | dedup by context id |
| Click when toggling SFX off | master gain stepped to 0 | slew (~20 ms) |
| Rare wrong-pitch SFX blip | torn read of a multi-field voice struct (main writes whole struct, audio reads mid-write) | accept & document at prototype scale; SPSC command ring for production |
| CPU spike in silence | denormals recirculating in delay feedback | checklist #6 |
| Battery drain while "stopped" | composer + synth still running, gated only by final gain | pause the compose timer and skip synthesis when inactive & silent |
| Beat drifts / jitters | Timer/DispatchQueue used as the musical clock | count samples in the render callback |

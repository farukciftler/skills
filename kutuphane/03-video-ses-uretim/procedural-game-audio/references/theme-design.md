# Theme Design Tables — ready-to-hardcode material

Concrete, numbers-included recipes proven in the ZarVeZindan engine. Copy, then re-voice per
project. All pitches are MIDI note numbers (`freq = 440 · 2^((midi-69)/12)` — computed on the
composer thread, never per-sample). 16 steps per bar throughout.

## Scales (semitone offsets from root)

| Mode | Offsets | Mood |
|---|---|---|
| Aeolian (natural minor) | 0 2 3 5 7 8 10 | classic dark fantasy |
| Dorian | 0 2 3 5 7 9 10 | airy, hopeful-dark (forests) |
| Phrygian | 0 1 3 5 7 8 10 | dread, the ♭2 crawls (swamps, undead) |
| Minor pentatonic | 0 3 5 7 10 | nearly mistake-proof melodies |
| + tritone tension | add root+6 sparingly | menace (late acts, bosses) |

## Euclidean patterns E(k,16) as step-index sets

```
E3  = [0, 6, 11]                     — sparse heartbeat (menus, rests)
E4  = [0, 4, 8, 12]                  — square pulse
E5  = [0, 3, 6, 9, 13]               — gentle forward lean
E6  = [0, 3, 5, 8, 11, 13]           — rolling
E7  = [0, 2, 4, 7, 9, 11, 14]        — driving
E9  = [0, 2, 4, 6, 7, 9, 11, 13, 15] — battle percussion
```

## Six-context example (the shipped game's table)

| Context | Root | Mode | BPM base→max | Bass | Perc | Arp | Melody density | Signature |
|---|---|---|---|---|---|---|---|---|
| Menu | A2 (45) | Aeolian, sus voicings | 60→66 | E3 | — | E4 | 0.20 | open fifths, intensity pinned 0.15 |
| Forest (act 1) | D3 (50) | Dorian | 72→96 | E4 | E5 | E6 | 0.40 | airy |
| Swamp (act 2) | E2 (40) | Phrygian | 64→84 | E3 | E4 | E5 | 0.30 | ♭2 dread, low root drone |
| Castle (act 3) | C3 (48) | Aeolian + tritone | 84→112 | E5 | E6 | E7 | 0.50 | menace |
| Battle | G2 (43) | Dorian, 2-bar i–♭VII riff | 120→150 | E7 | E9 | E5 | 0.60 | intensity floor 0.5 |
| Boss | F2 (41) | Aeolian + Neapolitan | 66→88 | E4 | E3 | E6 | 0.35 | fixed "fate" motif [53,49,48,44] on downbeats, floor 0.75 |

Progressions are 4 minor triads as MIDI arrays, e.g. forest `[[50,53,57],[43,47,50],[45,48,52],[48,52,55]]`.
Menu example `[[45,52,59],[41,48,55],[48,55,62],[43,50,57]]` (open, suspended).

## Melody engine

- Random-walk the scale **index**: step ∈ `[-2,-1,-1,0,1,1,2]` (weighted small), clamp to range.
- Rest probability = 1 − density; on chord changes bias toward chord tones.
- One octave of headroom above the pad; lead voice = sine or soft square, short decay.
- Markov upgrade: derive a next-note table from a melody you like; generation inherits its flavor.

## Layer/intensity map (adopt at bar boundaries only)

```
pad   gain = 1                    (always — also keeps the reverb feedback denormal-free)
bass  gain = 1
arp   gain = intensity > 0.3 ? 1 : 0
perc  gain = intensity > 0.6 ? 1 : 0
bpm        = base + intensity * (max - base)
```

## Voice timbres (cheap + effective)

| Voice | Recipe | Envelope (A/D/S/R) |
|---|---|---|
| Bass | square → 1-pole LP @500 Hz | 10 ms / 180 ms / 0.55 / 300 ms |
| Pad | 2 saws detuned ratio 1.005, up to 4 voices | 700 ms / 600 ms / 0.8 / 1.5 s |
| Arp | plucky: 4 ms attack, no sustain | 4 ms / 120 ms / 0 / 100 ms |
| Lead | sine + 20 % 2nd harmonic | 30 ms / med / 0.3 / med |
| Perc | filtered white noise burst (xorshift) | 2 ms attack, ~60 ms total |
| Room | feedback delay 110 ms (fb 0.45, wet 0.25) + allpass 37 ms (g 0.5) | — the "dungeon" |

## Sting recipes (one-shot phrases over the SFX pool)

- **Victory:** ascend root-triad+octave: 57→60→64→67 (~90 ms apart, 100–120 ms notes), then hold
  69 + shimmer 81 (~550 ms). Warm, modal, done in ~1 s.
- **Defeat:** descend with dissonance: 53→51→48→45 (150 ms steps) into a held minor-second pair
  42+41 (~900 ms). Fade the running theme out underneath it.

## SFX gesture recipes (each reads as ONE gesture through a 4-voice pool)

| Effect | Recipe |
|---|---|
| Dice clatter | 8 tapering noise pings, 2–3 kHz centers, onsets 0/60/100/170/220/300/380/450 ms, amps 1.0→0.32, 18–25 ms each |
| Hit / settle | 4 kHz noise click (20 ms) + pitch-drop body 80→55 Hz (130 ms) |
| Enemy hit (heavy) | swipe noise 1.6–2.2 kHz (30–45 ms) + body glide 130–155→58–92 Hz + low crunch tone (midi 33) when heavy |
| Player hurt | duller: glide 78–92→42–56 Hz, 600–850 Hz noise, dissonant undertone (midi 37) when heavy |
| Block / parry | bright clank: 5.2 kHz noise (20 ms) + tones midi 84 then 79 |
| Potion glugs | 3 rising glides 300→380, 340→430, 380→480 Hz (60–70 ms, 90 ms apart) + sparkle midi 88+93 |
| Heal shimmer | rising soft tones 72/76/79/84, 80 ms apart, longer decays — distinct from potion |

Design rule: pitch DOWN + dull = damage taken; pitch UP + bright = gain/success; metallic
high-passed = deflection. Keep every gesture under ~1 s so the pool never starves.

# Procedural audio

Silent physics clips underperform badly, and sample libraries repeat audibly once a few hundred collisions are in play. So the track is synthesised from the simulation's own contact log: a bank of damped sinusoids per impact, with decay rates from the material's Rayleigh damping coefficients. 400 collisions produce 400 genuinely different sounds and nothing repeats.

The synthesiser is `pipeline/synth_impacts.py` and the material bank is `pipeline/materials.json`, both shared with the Godot-era pipeline — they are engine-agnostic, and the only thing that changed is where the events come from. Read that skill's `references/procedural-audio.md` for the synthesis itself. This file covers the seam.

## The event contract

`sim` writes `events.jsonl`, one object per line, in time order:

```json
{"t":3.21,"energy":8.4,"material":"wood","size":0.15,"x":-0.31,"kind":"impact"}
{"t":4.05,"energy":0.42,"material":"metal","size":0.11,"x":0.12,"kind":"roll","duration":0.63}
```

| Field | Meaning |
|---|---|
| `t` | seconds from clip start |
| `energy` | ½·m_eff·v_n², in joules-ish. Only the relative scale matters; the mix is normalised. |
| `material` | key into the material bank — must be one of `metal, porcelain, glass, wood, plastic, cardboard, rubber, stone` |
| `size` | characteristic dimension in metres; sets the modal fundamental |
| `x` | world x at the contact, for stereo placement |
| `kind` | `impact`, `roll` or `slide` |
| `duration` | present for `roll`/`slide` only |

JSON Lines rather than one object, so a long take that is killed part-way still leaves a usable log. `forge.py` wraps it into the single object the synthesiser expects.

## Impact energy, done right

This is the part that is materially better than the Godot pipeline, and it is worth understanding because it is the difference between impacts that land and impacts that mush.

Two things are needed and both are easy to get wrong:

**1. The right frame to measure.** The velocity *after* the solver has run is the post-impact velocity — already damped by the very collision being measured. Reading energy from it under-reports every impact, and most severely the ones that matter. `sim` caches every body's linear velocity *before* stepping and uses that.

This is the same problem Godot's `get_contact_impulse()` has in a worse form: it reports zero on the first frame of a contact, which for a bouncy body is the only frame there is.

**2. Knowing which step is the impact.** Rapier 0.35's `ContactForceEvent` carries `started` — true exactly on the step a pair's total contact force first crosses its threshold (coming from below it, or from separation), false while it stays above. That flag *is* the impact detector, and it resets when the pair separates so a second bounce reports again.

Given both, the energy is straightforward:

```rust
let m_eff = 1.0 / (1.0/m_a + 1.0/m_b);   // a static body has infinite mass → m_eff is the dynamic one
let v_n   = (prev_vel[a] - prev_vel[b]).dot(ev.max_force_direction).abs();
let energy = 0.5 * m_eff * v_n * v_n;
```

`max_force_direction` comes from the event, so the normal is the solver's own, not a guess.

**Which body makes the sound.** The lighter, smaller one. A cube hitting a floor sounds like the cube, not like the building. `sim` picks the non-static body, or the lighter of two dynamic ones, and takes `material` and `size` from it.

## Rolling and sliding

A pair that keeps exchanging force without re-crossing its threshold is a sustained contact, not a series of impacts. Emitting one impact per step for it is exactly how physics clips end up sounding like a machine gun.

`sim` accumulates such pairs — start time, last-seen time, mean tangential speed — and flushes an event when the pair stops exchanging force. Anything under 80 ms is an impact's tail and is dropped; above that it becomes a `roll`, or a `slide` when mean tangential speed exceeds 0.6 m/s.

In practice rolls outnumber impacts in a pour: a typical `cube-rain` take is ~700 impacts and ~850 rolls over 12 seconds. That ratio is what makes a pile sound like a pile rather than a drum solo.

## The energy floor is the whole mix

`energy_floor` in the recipe decides what counts as a sound event at all, and it matters more than any material parameter.

Measured on a 12-second `cube-rain`, 260 bodies:

| `energy_floor` | events | result |
|---|---|---|
| 0.0001 | 9,361 | continuous hiss; a settling pile jostling forever |
| 2.0 | 1,581 | dense but readable |
| 2.0 + spawn scheduling | 354 | clean, evenly spread across the clip |

Note the third row: **most of the fix was not the floor, it was the spawn schedule.** With everything released on frame 0 the events pile into the first three seconds (2,331 in second one, 6,517 in second two, then silence). Spreading the release spreads the track. An audio problem was a staging problem.

Tune with `synth_impacts.py --report`, which prints the distribution and the event rate without rendering anything. `score_take.py` also flags rates below 5/s (the track will be silent) and above 120/s (the impacts will smear).

## Impact density: the cooldown and the floor together

Two controls decide whether a race sounds like marbles or like radio static, and both live upstream of the synthesiser. `energy_floor` gates which hits are loud enough to exist; the **per-pair impact cooldown** in `sim` (150 ms) collapses one physical bounce's threshold chattering into one audible hit — a marble rattling down a dome field otherwise logs a dozen impacts per second per pair. Measured on the gauntlet: 437 events → 179 over 47 s. For "tok" (full-bodied) hits, the material bank matters more than any mix knob: `wood` knocks where `porcelain` clicks.

## The hype track (`make_music.py`)

Race clips carry a second audio layer: a fully synthesised electronic backing (kick/snare/hats, sidechain-feel saw bass arpeggio, delayed pluck lead, A-minor Am–F–C–G) **arranged around the crossing time read from the motion cache** — the last bars before the win get a riser and a snare fill, the crossing lands on a crash and a chord stab quantised to the bar line, the outro drops to half energy. Royalty-free by construction. Mixed 1.0 : 0.5 under the impact foley in `race_overlay.py`: the marbles stay the lead instrument, the music is the floor.

## Why it stays offline

No real-time budget means every event gets its full mode bank, unlimited polyphony, proper reverb and limiting — and the audio can be re-rendered in seconds without re-rendering video. The video is rendered silent and the track is muxed in. Two sources of audio in one file is how sync problems start.

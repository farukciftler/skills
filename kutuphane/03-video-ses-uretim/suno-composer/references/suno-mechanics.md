# Suno Mechanics

What the platform actually does with your text. Verified against v5.5 (released March 2026, current as of mid-2026). Suno ships changes fast — if something here contradicts what the person is seeing in their interface, believe them, and web-search for the current state before insisting.

## Contents
1. The fields
2. How the Style field is weighted
3. Character limits
4. Metatags that work
5. Inline vocal cues
6. The Exclude field and negative prompting
7. What Suno ignores
8. Artist deconstruction
9. v5.5 features that change how you prompt
10. Iteration workflow

---

## 1. The fields

**Simple mode** takes one description and auto-writes lyrics. Fine for testing a sound, useless for anything you intend to keep.

**Custom mode** splits into:
- **Styles / Style of Music** — genre, era, mood, instrumentation, vocal character, production, tempo. Everything about the *whole song*.
- **Lyrics** — the words, section metatags, and short cues that apply to *one local moment*.
- **Advanced Options** — Exclude Styles, duration slider, model version, weirdness/style-influence sliders.

The placement question answers itself: does this instruction describe the whole song (Styles), the words being sung (Lyrics), one specific moment (inline cue in Lyrics), or something with its own control (use the control). Burying "exactly three minutes" in the Style field when there's a duration slider is wasted characters.

---

## 2. How the Style field is weighted

Token order is influence order. The first few descriptors dominate the output; things after roughly the tenth carry noticeably less weight, and past twenty they start contradicting each other rather than adding detail.

**Recommended order:**
1. Primary genre + era/subgenre (the single strongest lever)
2. Tempo and groove feel
3. Vocal identity — character, delivery, effects
4. 2–4 signature instruments, named specifically
5. Production aesthetic
6. Mood / emotional arc

Target 8–15 descriptors. Under 5, Suno fills the gaps with its own defaults; those defaults have been drifting toward whatever the person generates most (see § 9, My Taste), so vagueness is doubly costly.

If blending genres, put the dominant one first and cap it at two. Three genre tags produce mush.

---

## 3. Character limits

| Field | v4 and older | v4.5 / v5 / v5.5 |
|---|---|---|
| Style | ~200 chars | ~1,000 chars |
| Lyrics | ~3,000 chars | ~5,000 chars |

Limits track the model version, not the subscription tier. Having 1,000 characters is not a reason to use them — the weighting curve means a tight 300-character prompt usually beats a sprawling 900-character one.

---

## 4. Metatags that work

Structural, one per line, in square brackets in the Lyrics field:

`[Intro]` `[Verse]` / `[Verse 1]` `[Pre-Chorus]` `[Chorus]` `[Post-Chorus]` `[Bridge]` `[Hook]` `[Refrain]` `[Interlude]` `[Instrumental]` `[Break]` `[Solo]` `[Outro]`

Numbered verses get distinct melodies. `[Chorus]` gets the most energy and melodic emphasis automatically — you don't need to beg for it in the Style field. Without any metatags, Suno infers structure from line breaks and content patterns, usually badly.

Descriptive additions in brackets often land too: `[Guitar solo]`, `[Instrumental break, 8 bars]`, `[Half-time]`, `[Key change]`, `[Drums enter]`, `[Build]`. Treat these as likely-but-not-guaranteed.

---

## 5. Inline vocal cues

Parenthetical, inside the lyrics, applying to what follows:

`(whispered)` `(belted)` `(spoken word)` `(harmonized)` `(ad-lib)` `(falsetto)` `(building intensity)` `(stripped back)` `(half-time feel)` `(doubled)` `(distant, filtered)`

These are the most reliable dynamics control available. The Style field describes an average; the cues describe a shape. When a track "sounds like AI", it's usually because it had no shape — all Style, no cues.

Example:

```
[Verse 1]
(whispered, intimate, guitar only)
The house is quiet now

[Chorus]
(full band, belted)
But I won't break apart
```

---

## 6. The Exclude field and negative prompting

Custom Mode → Advanced Options → **Exclude Styles**. This is the official negative-direction control and it is more reliable than inline negatives.

Rules:
- **Two or three targets, maximum.** A long exclusion list dilutes into noise.
- **Always pair an exclusion with a positive replacement.** Removing an element leaves a musical role empty and Suno will fill it with something. Weak: `Exclude: guitar`. Strong: `Styles: piano-led soul ballad, upright bass` + `Exclude: guitar`.
- Use short recognizable descriptions: `choir, backing vocals`, `distorted guitar`, `autotune`, `EDM drop`.
- Inline `no autotune` / `no reverb wash` in the Style field also biases the output and costs few characters — the highest-signal ones push toward a rawer, more organic result. But when it matters, use the Exclude field.
- Exclusion is guidance, not a mute. A strongly implied element can still appear. If your positive prompt says "stadium rock" and you exclude drums, you will probably still get drums.

---

## 7. What Suno ignores

Don't waste characters on these — and don't promise the person control the tool doesn't have:

- **Mixing and engineering parameters.** "Sidechain compression on the kick", "high-pass at 120 Hz", "-3 dB on the snare" — all ignored. Express the intent as an arrangement or texture choice instead ("pumping, breathing kick-and-pad interaction").
- **Exact BPM as a lock.** Treated as approximate guidance. It biases well; it doesn't clamp.
- **Chord symbols and notation.** "Cmaj7–Am7–Dm7–G7" mostly doesn't parse. Describe the progression's character.
- **Exact bar counts.** Approximated. Useful for your planning, not enforceable.
- **Exact duration in text.** Use the duration slider.
- **Real artist names.** Rejected outright. See § 8.
- **Microtonal intervals.** 12-TET model; makam koma and raga śruti will be approximated.

---

## 8. Artist deconstruction

When someone says "make it sound like X", convert the name into four things:

1. **Tempo band** they typically inhabit
2. **Vocal character** — register, texture, delivery habit (conversational? belted? whispered?)
3. **Instrumentation and production palette** — the two or three sounds that identify them
4. **Mood and setting**

So a request for an atmospheric-Toronto-rap sound becomes: `atmospheric trap, moody R&B, melodic male vocals, conversational delivery, vulnerable and introspective, 808 sub-bass, reverb-heavy pads, sparse arrangement, nocturnal, 78 BPM`. No name, same fingerprint.

Do this silently as part of composing — you don't need to narrate that you're avoiding the name, just deliver the descriptors. Never reproduce the artist's actual lyrics.

---

## 9. v5.5 features that change how you prompt

- **Voices** (Pro/Premier) — the person supplies a captured voice. If they're using one, *drop the timbre descriptors* and spend those characters on delivery instead ("screamed on the chorus", "whispered verses"). Describing a singer while supplying a singer produces a fight.
- **Custom Models** (Pro/Premier, up to three) — a model tuned on their own catalogue absorbs much of what a style prompt normally carries. Keep prompts shorter and let the model hold the identity.
- **My Taste** (everyone) — Suno adapts defaults to what the person keeps generating. If their outputs have started drifting toward one sound regardless of prompt, this is why. The fix is more specificity, not more tags.
- **Studio** (Pro/Premier) — stems, section-level editing, regenerate-one-section. Worth mentioning when someone is fighting a track that's 80% right: editing the bad section beats rerolling the whole thing.
- **Duration slider** — set length here, not in text.
- **Cover / Extend** — Cover re-performs existing audio in a new style; Extend continues a generation. Both are far cheaper than starting over.

---

## 10. Iteration workflow

Generation is probabilistic. A single output is a sample, not a verdict.

1. Generate **2–3 takes of the same prompt** before changing anything. Variance between takes is often larger than the variance from a prompt edit.
2. Change **one variable at a time**. Two edits at once and you've learned nothing about either.
3. Keep the edits ordered by leverage: genre/era token → BPM and groove → vocal direction → instrumentation → production adjectives. Fiddling with production adjectives while the genre token is wrong is wasted credits.
4. When a track is mostly right, don't reroll — use Extend, Cover, or Studio section editing.
5. Log what worked. A personal library of prompt patterns that reliably produce a given sound is worth more than any generic tag list.

Deliver the person a short "if it comes out wrong" list specific to their track, naming the likely failure modes and the single knob for each. That's the difference between handing someone a prompt and handing them a process.

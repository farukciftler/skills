---
name: english-narration
description: |
  Writes and audits English narration for vertical short video (Shorts, Reels,
  TikTok). The text is SPOKEN by TTS and READ as burned-in captions, so written
  prose rules do not apply. Use when writing a brief's `metin` field for an
  English channel, rewriting narration that sounds machine-written, or checking
  a script before synthesis. Triggers: "write the script", "voiceover copy",
  "narration", "hook", "shorts script", "make it sound human", "this reads like
  AI", "fact video script".
license: MIT
---

# English narration for short vertical video

The text is consumed twice: by ear (TTS reads it) and by eye (word-by-word
captions). Neither is an article. This file is the difference.

`.claude/skills/insanca/` catalogues 48 machine-writing patterns. It is written
in Turkish and its examples are Turkish, but most of the patterns are
structural and carry over: metronomic sentence rhythm, connector stacking,
false triplets, "not X, but Y" scaffolding, importance inflation, generic
openings and closings, vague sourcing, template "challenges" sections. Read
it for the taxonomy; ignore the Turkish-specific morphology sections.

---

## 1. Spoken constraints

**Breath sets sentence length: 9 to 16 words.** Longer will not survive one
breath and the listener loses the thread. Shorter, three in a row, reads as
telegraph.

**Vary the rhythm.** Uniform sentence length is the single loudest
machine-writing signal, and it is louder when spoken than when read.

**No marks that do not exist in speech.** Parentheses, semicolons, em dashes,
ellipses, footnotes. Whatever you were going to put in parentheses is either a
sentence or it is dead weight. Commas and full stops stay; they are pauses.

**English is verb-second, so the hook is easier than in Turkish** but the
payload still needs to arrive first. Lead with the number, the object, or the
contradiction. Never with setup.

> Weak: "There is something surprising about the history of the aqueduct that
> supplied the city."
> Strong: "Four hundred and twenty six kilometres. That is how far the water
> travelled."

**One idea per sentence.** Caption cues are at most four words; a long
compound sentence breaks across cues and the meaning snaps.

**Second person is cheap and it shows.** "You won't believe" and "Did you
know" are the two most exhausted openings in this format. Neither survives
contact with a viewer who has seen a thousand of them.

---

## 2. Measured TTS constraints

`motor/ses/okunus.py` handles the mechanical conversion. English needs far
less of it than Turkish.

Measured with ElevenLabs `bill`, `eleven_multilingual_v2`, faster-whisper
`small` round-trip, 2026-08-24.

| form | measured result |
|---|---|
| `426 km` | correct |
| `74%` | correct |
| `1453` | correct |
| `3.5 million` | correct |
| `NASA`, `NOAA`, `USGS` | correct |
| `300 BCE`, `300 AD` | correct |
| `Between 1200 and 1450` | correct |
| **`4 kg`, `12 m`** | **3 of 3 broken**: "keon", "maledamins", "millimeters" |
| `four kilograms`, `twelve metres` | 2 of 2 correct |
| `Mehmed II` | unstable: "Mehmed Zakand" |

**Rules:** never use abbreviated units in narration. Write Roman numerals as
words ("Mehmed the Second"). Everything else can stay as digits, and should:
captions read better with `426 km` than with the words.

---

## 3. Fact channel specifics

**Every claim carries a source.** `brif.kaynakca` is mandatory and `preflight`
blocks publication without it. The source is not Wikipedia; it is the
secondary source Wikipedia cites. Wikipedia and Wikidata are the route, not
the destination.

**Claim shapes rotate.** The channel's thesis is not one subject, it is a
system of claim shapes. Four are defined in `motor/varyasyon.py`:

| shape | roles | what it demands |
|---|---|---|
| `tek-nesne-an` | object, moment, change, close | a specific object on screen |
| `sanilandan-eski` | anchor, comparison, evidence, close | two things and a real date for each |
| `rakam-ne-diyor` | number, misreading, correct reading, source | a statistic and what people get wrong about it |
| `yanlis-bilinen` | common belief, where it came from, truth, source | the origin of the error, not just the correction |

The variation engine picks one per take and avoids the last three used. Write
to the shape you were given; do not merge shapes.

**Say what is uncertain.** "The usual figure is X, though the underlying survey
only covered Y" is more interesting than a clean number, and it is honest.
Certainty theatre is the tell of a channel that does not read its sources.

---

## 4. Repo constraints

- `kimlik.yaml -> asla_yapmaz` is machine-enforced before synthesis. Exclamation
  marks, urgency, scarcity, clickbait questions, imperatives, guarantees and
  listicle counters stop production.
- Sentence count must match the skeleton's role count. All four fact shapes
  have four roles, so `metin` is four sentences.
- The closing role is a resolution, not a call to action. "Subscribe" is banned.
- The first sentence needs a concrete marker: a number, a unit or a proper
  noun. `motor/puanlama/olcumler.py:kanca` counts it and a take that misses the
  threshold never reaches render.
- **No em dashes, arrows, bullets or emoji anywhere in published text.**
  `motor/denetim/metin.py` and `motor/denetim/seo.py` both fail on them.

---

## 5. Order of work

1. Write the claim as one sentence. If it does not carry, the script will not.
2. Take the skeleton you were given, one sentence per role.
3. Read it aloud. The test is the ear.
4. Apply the `insanca` taxonomy for structural machine-writing patterns.
5. Check section 2. The converter handles units; it does not invent forms.
6. Put the source in `kaynakca`. No source, no video.
7. `python -m motor.denetim.metin brif/<name>.json --dil en`

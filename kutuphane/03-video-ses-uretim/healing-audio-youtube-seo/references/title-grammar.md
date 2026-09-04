# Title Grammar

## Contents

1. Character budgets, the hard numbers
2. The two-name rule
3. The slot system
4. Formulas by format
5. Worked examples
6. Punctuation, emoji, case
7. Anti-patterns
8. Rewrite examples (before → after)
9. Delivery format

---

## 1. Character budgets, the hard numbers

| Field | Hard limit | Where it actually gets cut |
|---|---|---|
| Video title | 100 characters (YouTube rejects more) | ~60–70 on desktop search, ~50 on mobile, ~55 in the desktop suggested sidebar, ~40 on the Shorts shelf |
| Description | 5,000 **bytes** | ~200 chars above the fold on desktop, ~100–150 on mobile |
| Tags | 500 characters combined across all tags | — |
| Hashtags | 15 per video; over 15 and **all** are ignored | first 3 from the description render above the title |
| Playlist title | 150 characters | truncates in feeds around 50–70 |
| Channel description | 1,000 characters | first ~100–150 shown in channel search results |

Two consequences that drive everything below:

- **The design target is ~50 characters, not 100.** Characters 51–100 are for the algorithm and for the desktop viewer who is already interested; characters 1–50 are the only thing most people read.
- **Emoji and non-ASCII cost 2–4 characters each** in the counter and 2–4 bytes each in the description. A decorative moon at the front of a title can push the keyword out of the mobile window — measurable damage for decoration.

Verify these numbers with a search if precision matters for a client deliverable; the display truncation points in particular shift with interface changes.

## 2. The two-name rule

| | Catalogue name | YouTube search title |
|---|---|---|
| Job | identity, memorability, rights registration | discovery by situation |
| Grammar | poetic, 1–4 words, unique, no keywords | functional phrase, keyword-first |
| Lives in | Suno title, DSP metadata, album track list, cover art, chapter markers | the YouTube title field |
| Example | *Cedar Hours* | `432 Hz Sleep Music — 8 Hours of Cedar-Warm Ambient for Deep Rest` |

The catalogue name is not wasted on YouTube: carry it as a tail element or a series marker so repeat viewers learn it. Over a catalogue this is how a channel accumulates a brand while every individual upload still bids on demand. Deliver both names, labelled, every time.

## 3. The slot system

```
[KEY]      primary search phrase, verbatim, word order from autocomplete   — MANDATORY, chars 1–~45
[SPEC]     duration and/or tuning: "8 Hours", "432 Hz", "Delta Waves"      — usually mandatory
[TEXTURE]  instrument / scene / mood: "Cedar-Warm Ambient", "Rain on Pine" — the differentiator
[BENEFIT]  intent language only: "for Deep Rest", "to Unwind"              — never an outcome claim
[NAME]     catalogue name or series marker: "Cedar Hours", "Nightfall IV"  — branding, tail position
```

Ordering rules that hold across formats:

1. `[KEY]` opens the title. Nothing precedes it — no emoji, no bracket, no series marker. A 10-character prefix costs a fifth of the mobile window.
2. `[SPEC]` goes immediately before or after `[KEY]`, whichever reads as natural English. Duration and Hz are *searched tokens*, not decoration, so they belong in the visible window.
3. `[TEXTURE]` earns the middle. This is where an upload stops being interchangeable with its siblings — and where the duplication gate is won or lost.
4. `[BENEFIT]` and `[NAME]` take the tail, characters ~60–100. Fine if truncated; they are for the desktop reader and the index.
5. One separator style per channel. Pick an em dash, a pipe or a middot and keep it — consistency is a weak but free brand signal across a shelf of thumbnails.

## 4. Formulas by format

**Long-form single-frequency (1–8 h)**
`[KEY] — [SPEC duration] of [TEXTURE] for [BENEFIT]`
→ `528 Hz Meditation Music — 3 Hours of Singing Bowls for Slow Breathing`

**Long-form scene/ambience (1–10 h)**
`[TEXTURE scene] + [KEY] | [SPEC duration]`
→ `Rain on a Tin Roof — Sleep Music for Insomnia | 8 Hours, Black Screen`
(Here the scene *is* the search term; scene-led queries are the exception where `[TEXTURE]` may open the title.)

**Session piece (10–60 min)**
`[KEY] — [SPEC duration] [TEXTURE] ([NAME])`
→ `Morning Meditation Music — 20 Minute Handpan Drift (Cedar Hours)`

**Single track, 3–10 min**
`[NAME] — [KEY], [TEXTURE]`
→ `Cedar Hours — 432 Hz Ambient for Deep Rest, Slow Cello Drone`
(The only format where the catalogue name may lead, because at this length the piece is closer to a released single than to a functional bed — but only if the channel already has recognition. New channels keep `[KEY]` first.)

**Series entry**
`[KEY] — [NAME + number] | [TEXTURE], [SPEC]`
→ `Sleep Music for Rainy Nights — Nightfall IV | Piano and Distant Thunder, 3 Hours`
The number is never the only thing that changes between entries. `[TEXTURE]` must change too, or the series reads as a template.

**Cinematic / royalty-free-for-creators**
`[TEXTURE + mood] — [KEY use-case] (Royalty-Free)`
→ `Slow Cinematic Ambient — Background Music for Documentaries (Royalty-Free)`

**Shorts (~40 visible characters)**
`[KEY short form] — [one hook]`
→ `432 Hz for Sleep — 60 Seconds to Settle`

**Livestream**
`[KEY] · 24/7 [TEXTURE] Live`
→ `Sleep Music · 24/7 Warm Ambient and Rain Live`

## 5. Worked examples

**Brief:** Suno-generated 8-hour bed, A=432, ney and low strings, black-screen video, sleep lane, new channel.

Three candidates on three different intent bets:

| # | Title | Chars | Bet | Gives up |
|---|---|---|---|---|
| 1 | `432 Hz Sleep Music — 8 Hours of Ney and Low Strings for Deep Rest` | 65 | the core sleep+frequency query, largest demand | most contested phrase; needs the scene tail to differentiate |
| 2 | `Sleep Music for Insomnia — 8 Hours of 432 Hz Ney, Black Screen` | 61 | insomnia sufferers, higher intent, lower volume | drops the "432 hz sleep music" compound to second position |
| 3 | `Ney Meditation Music — 8 Hours at 432 Hz for Deep Rest and Sleep` | 64 | the instrument niche; near-zero competition | small addressable demand; slow build |

Truncation preview at 50 for candidate 1: `432 Hz Sleep Music — 8 Hours of Ney and Low Stri…` — keyword intact, texture starts to show. Good.

Recommendation for a new channel: **2**, then 1 as the follow-up upload. The insomnia phrase is winnable now; the head phrase is worth bidding on once the channel has retention history on the lane.

**Catalogue name** for the same asset: *Ney Hours* (poetic, 2 words, no keyword collision) — used in the chapter list, cover art, DSP metadata, and as the tail of future entries in the series.

## 6. Punctuation, emoji, case

- **Separators:** em dash `—`, pipe `|`, middot `·`. Avoid stacking three different ones in one title.
- **Brackets:** reserve `()` for a genuine qualifier — `(Black Screen)`, `(Royalty-Free)`, `(No Ads Mid-Roll)`. Bracket labels eat characters fast; a 10-character bracket at the front leaves 40 for the hook.
- **Emoji:** at most one, never before `[KEY]`, and only when it carries information (🌧 for a rain video). The niche is full of decorated titles; decoration is not why they rank. Fancy Unicode letter variants (bold, script, double-struck) render inconsistently and hurt accessibility — plain ASCII plus standard punctuation is the safe set.
- **Case:** Title Case for the keyword and texture. No ALL-CAPS words beyond an occasional single spec token; excessive capitalisation reads as clickbait to both viewers and classifiers.
- **`432Hz` vs `432 Hz`:** use whichever form autocomplete surfaced for that phrase. If both appear, use the spaced form in the title and the closed form in tags, so both are covered.

## 7. Anti-patterns

- **Keyword paste.** `Relaxing Music Sleep Music Meditation Music Study Music Spa Music 432Hz Healing` — truncates into nonsense, dilutes every phrase, reads as spam.
- **Poetic-only title on a functional upload.** `Whispers of the Cedar Grove` — zero search surface.
- **Claim in the title.** `528 Hz DNA Repair` / `Cure Insomnia Tonight` — highest-risk policy area, and the keyword survives without it. See `claims-and-policy.md`.
- **Duration inflation.** Any duration token that does not match the file. Mismatch is misleading metadata and destroys retention when the audio ends mid-night.
- **Volume-numbering as the only variation.** `Sleep Beats Vol. 12 / 13 / 14` is the canonical templated-catalogue signal.
- **Two lanes in one title.** `Sleep and Study Music` asks for two retention behaviours and gets neither audience cleanly.
- **All-emoji framing.** `🌙✨ 432 Hz ✨🌙` — costs characters, adds nothing, and pushes the keyword out of the mobile window.
- **Fake specificity.** `Scientifically Proven`, `Doctor Approved`, `NASA Frequency` without a real source. Fabricated authority is both dishonest and a policy exposure.

## 8. Rewrite examples

| Before | Problem | After |
|---|---|---|
| `528 Hz DNA Repair — Heal Your Body While You Sleep` | body-outcome claim, medical exposure | `528 Hz Sleep Music — 8 Hours of Warm Drone for Deep Rest` |
| `Amber Hollow (Original Ambient Piece)` | no search surface | `Ambient Sleep Music — 3 Hours of Slow Piano Drift (Amber Hollow)` |
| `🌙✨ RELAXING MUSIC ✨🌙 Best Sleep Music Meditation Study Spa 432Hz Healing Zen` | paste, caps, emoji, four lanes | `432 Hz Relaxing Music — 3 Hours of Spa Piano for Slow Evenings` |
| `Sleep Beats Vol. 14` | template, no keyword, no texture | `Sleep Music for Rainy Nights — Nightfall IV | Piano and Thunder, 3 Hours` |
| `8 HOURS Deep Sleep Music (Cures Anxiety Fast!!)` | caps, claim, punctuation spam | `Deep Sleep Music — 8 Hours of Low Strings to Calm a Restless Night` |

## 9. Delivery format

Present title work like this, always:

```
CATALOGUE NAME:  Ney Hours
PRIMARY PHRASE:  sleep music for insomnia   (source: autocomplete, 3 recent small-channel results in top rows)

TITLE A (recommended) — 61 chars — bet: insomnia intent
Sleep Music for Insomnia — 8 Hours of 432 Hz Ney, Black Screen
  @50: "Sleep Music for Insomnia — 8 Hours of 432 Hz Ne…"
  gives up: the head "432 hz sleep music" compound

TITLE B — 65 chars — bet: head query
...

TITLE C — 64 chars — bet: instrument niche
...

GATES: truncation PASS · promise PASS (28,800 s file / "8 Hours") · claim PASS · duplication PASS (max similarity 0.41 vs. catalogue) · distinctness PASS (new instrument, new key, new visual)
```

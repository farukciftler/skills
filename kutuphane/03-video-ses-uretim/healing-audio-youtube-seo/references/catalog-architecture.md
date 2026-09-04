# Catalogue Architecture

Single uploads are not the unit of this business — the catalogue is. A channel that survives is one where each upload is discoverably distinct, the playlists hold a session together, and there is a written record of why each release is different from its siblings.

## Contents

1. The differentiation ledger
2. Series design
3. Duration strategy
4. Cadence
5. Playlist architecture
6. Shorts
7. Livestreams
8. DSP naming for the same asset
9. Rescuing a flagged or flat catalogue
10. The ledger file

---

## 1. The differentiation ledger

Every upload must differ from its siblings on **at least three axes**. Decide which three *before* generating the audio, not after — retrofitting variation is how templated catalogues happen.

| Axis | Meaningful variation |
|---|---|
| Instrumentation | ney → cello → handpan → felt piano → singing bowls |
| Tuning / spec | 432 · 528 · 396 · standard 440 · delta · theta |
| Key and tempo | different tonal centre, different BPM band |
| Duration | 20 min · 1 h · 3 h · 8 h — genuinely different files, not padding |
| Scene | rain · snow · fireplace · night ocean · empty room |
| Structure | single drone · three movements · slow-descending arc |
| Visual | different plate, different palette, different motion treatment |
| Curation logic | "the last hour before sleep" vs. "for the 4 a.m. wake-up" |
| Lane | sleep · meditation · study · spa |

Log the three chosen axes per release in the ledger. Two benefits: the audit script can check title similarity against the record, and if the channel is ever reviewed there is documentary evidence of editorial decision-making rather than a generation queue.

## 2. Series design

A series is the strongest brand structure in this vertical — it drives repeat sessions and gives the recommendation system a coherent cluster. It is also the easiest way to trip the templated-catalogue detector, so build it deliberately.

**Do:**
- One series name, poetic and short: *Nightfall*, *Ney Hours*, *Long Rain*.
- Roman or word numerals in the tail, never at the front.
- A fixed slot grammar with a **genuinely variable texture slot**: `[KEY] — [Series N] | [texture], [duration]`.
- Cap a series at 8–12 entries, then start a different one. An endless series is indistinguishable from a template.

**Don't:**
- Vary only the number. `Vol. 12 / 13 / 14` with the same words either side is the canonical bad pattern.
- Reuse the same texture words across entries. If entries III and VII both say "warm ambient drift", the series has stopped differentiating.
- Run three series in the same lane at once — you compete with yourself in suggested placements.

Series entry example set:

```
Sleep Music for Rainy Nights — Nightfall I | Felt Piano and Soft Thunder, 3 Hours
432 Hz Sleep Music — Nightfall II | Low Cello, Wind Against Glass, 8 Hours
Sleep Music for Insomnia — Nightfall III | Ney and Distant Rain, 6 Hours
```

Same series, three different queries, three different textures, three different durations. That is a catalogue, not a template.

## 3. Duration strategy

Duration is both a keyword and a retention decision:

- **8 h / 10 h** — overnight sleep. Longest sessions in the vertical. Must be genuinely composed or genuinely long-form generated, never a padded loop.
- **3 h** — the sweet spot for sleep and study: long enough to hold a session, cheap enough to produce several per month.
- **1 h** — study, spa, yoga class length. Professional-use audiences prefer it.
- **20–30 min** — meditation, breathwork, nap. Higher completion rate, useful for testing a new lane cheaply.
- **3–10 min** — singles. Treat as DSP-first with YouTube as the secondary surface.

Test a new lane with a 20–30 minute upload before committing eight hours of production to it.

## 4. Cadence

Match cadence to a plausible production story. A channel two weeks old posting thirty uploads reads as a farm regardless of quality. Two to four substantial uploads a week, each genuinely distinct, with a visible series structure, reads as a working label. Slower and more distinct beats faster and interchangeable — and in a vertical where individual videos accumulate views for years, volume is not where the returns are.

## 5. Playlist architecture

- One playlist per **lane**, searchably titled, with the lane's primary phrase in it.
- Sequence for the session: energy and brightness descend across a sleep playlist; a study playlist can hold a steadier level.
- Put the playlist link in every description in that lane, and point across to one adjacent lane. Session length is a stronger ranking input than any metadata field.
- A series gets its own playlist in addition to its lane playlist.
- Revisit sequencing quarterly; a playlist that opens with your weakest retention video is leaking sessions.

## 6. Shorts

Shorts are a discovery surface for the channel, not a home for the bed. Titles show roughly 40 characters on the shelf, so the hook lands harder and earlier. Use a 30–60 second excerpt with the visual moving, and a title that names the lane and the spec: `432 Hz for Sleep — 60 Seconds to Settle`. Shorts and long-form are tracked separately; do not reuse the long-form title verbatim.

## 7. Livestreams

A 24/7 stream is the strongest session-length asset available and it is a legitimate answer to "how do I fill a lane without uploading forty near-identical files". Title it as a live surface: `Sleep Music · 24/7 Warm Ambient and Rain Live`. It needs curated rotation, not one loop.

## 8. DSP naming for the same asset

The same track carries different names on different surfaces, and mixing them up causes real problems:

| Surface | Name to use | Why |
|---|---|---|
| YouTube | search title (`[KEY]`-first) | discovery by situation |
| Spotify / Apple / DSPs | catalogue name, clean | DSP style rules reject keyword-stuffed titles, all-caps and bracketed spam; keyword titles also look like spam to listeners browsing an artist page |
| Album / release | catalogue name + version tag if needed (`Ney Hours (8 Hour Version)`) | version tags belong in parentheses, not in the title proper |
| Suno project | catalogue name | keeps the generation library navigable |
| Cover art | catalogue name only | keywords on artwork look like stock spam |

Before finalising a catalogue name, search it — a collision with a charting track is a discoverability trap on every surface at once.

## 9. Rescuing a flagged or flat catalogue

If impressions are falling while retention holds, or a monetisation warning has landed, work in this order:

1. **Audit for duplication first.** Run `metadata_audit.py` over the entire existing catalogue pairwise. Templated titles and repeated skeletons are the most likely cause and the cheapest to fix.
2. **Audit for claims.** Sweep every title and description for Tier 1 and Tier 2 language (see `claims-and-policy.md`) and rewrite. Retitling keeps the video and its history; deleting loses both.
3. **Check disclosure.** Every AI-audio upload should carry the synthetic-content toggle.
4. **Check duplicate audio.** Any track published more than once under different titles should be consolidated to one canonical upload.
5. **Then, and only then, retitle for performance.** Renaming a video resets its impression experiment; do it deliberately, one lane at a time, and record the before/after so the effect is legible.
6. **Add human layers going forward.** Chapters, named sections, curation notes, original visuals, a series structure. This is what moves a catalogue from "replicable at scale" to "curated".

Never mass-retitle the whole catalogue in one day. It looks like exactly the kind of automated bulk operation you are trying to prove you are not.

## 10. The ledger file

`assets/catalog-ledger.csv` is the memory of the channel. Append one row per release at publish time:

```
date,catalog_name,series,series_no,youtube_title,primary_keyword,lane,duration_seconds,tuning,instrumentation,differentiation_axes,visual_id,playlist,notes
```

The audit script reads the `youtube_title` column for similarity checks, so the ledger is not bureaucracy — it is what makes the duplication gate work at upload 40 instead of only at upload 4.

---
name: healing-audio-youtube-seo
description: Names and optimises functional-audio releases for YouTube — healing music, 432 Hz / 528 Hz / solfeggio, binaural and delta beds, sleep, meditation, study, spa, reiki, lo-fi, ambient — covering the track name, the search title, description, chapters, tags, hashtags, playlist and series architecture, plus the claim and duplication gates that keep a Suno-fed catalogue monetisable. Use whenever a track or long-form upload needs a title or rename, a batch needs a naming system, or titles need auditing for truncation, health-claim risk, false duration or templated repetition. Trigger on "şarkı ismi ne olsun", "youtube başlığı yaz", "432 hz videosuna isim", "healing music kanalı", "başlık optimizasyonu", "hangi keyword'ü hedefleyelim", "bu isim aratılır mı", "AI diye demonetize olur muyum", "seri isimlendirmesi", "playlist ismi", "uzun format başlığı". Use it even when someone only says "isim bul" or "başlık" about a music upload — on YouTube the name IS the distribution.
---

# Healing & Functional Audio — YouTube Naming and Optimisation

In this vertical nobody searches for the song. They search for the *job*: "music for deep sleep", "432 hz meditation", "3 hours rain and piano", "study music focus". The title is not a label on a finished object — it is the demand you are bidding for. A beautiful track with a poetic title and no use-case phrase is invisible; a mediocre track sitting on the right phrase with an honest promise runs for years.

So this skill does two things at once: it wins the search, and it keeps the catalogue alive. The second half matters more than people expect. A functional-audio channel fed by AI generation sits on top of five overlapping YouTube policies, and the two that kill channels — inauthentic content and misleading/unsafe health claims — are both **triggered by the words you choose**, not by the audio. Naming is where the risk lives.

## Division of labour

| Job | Where |
|---|---|
| Composing the track, Suno style/lyric fields | `suno-composer` |
| Cover art, album naming, retro art direction | `retro-record-label` |
| Video rendering from a still + effects | `ambient-video-forge` |
| **YouTube titles, keyword bets, description, chapters, tags, series/playlist architecture, claim + duplication gates** | **here** |

`retro-record-label/references/youtube-metadata.md` covers general artist-release metadata. This skill supersedes it for functional audio: different search grammar, different policy exposure, different unit of production (an upload cadence, not a launch).

## Reference map

Read the file you need; do not read all of them.

| File | When |
|---|---|
| `references/keyword-research.md` | Always, before writing any title. Demand discovery, autocomplete harvesting, competitor n-gram extraction, sub-niche + seed-phrase banks, scoring. |
| `references/title-grammar.md` | Writing or rewriting any title. The slot system, character budgets, per-format formulas, the two-name rule, worked examples, anti-patterns. |
| `references/claims-and-policy.md` | Every deliverable, no exceptions. Health-claim substitution table, medical-misinformation exposure, inauthentic/reused-content defence, AI disclosure, Content ID. |
| `references/description-tags-chapters.md` | Building the metadata pack below the title. Above-fold architecture, chapter design, tags, hashtags, field limits, localisation. |
| `references/catalog-architecture.md` | Batches, series, playlists, cadence, Shorts, DSP single names, the differentiation ledger. |

## Script

`scripts/metadata_audit.py` — deterministic gatekeeper. Run it on every deliverable before handing it over; it catches what judgement misses.

```bash
python scripts/metadata_audit.py \
  --title "432 Hz Sleep Music — 8 Hours of Warm Ambient Drift for Deep Rest" \
  --primary-keyword "432 hz sleep music" \
  --duration-seconds 28800 \
  --description-file desc.txt \
  --hashtags "#sleepmusic #432hz #ambient" \
  --tags "sleep music, 432 hz, ambient sleep, deep sleep music" \
  --catalog assets/catalog-ledger.csv
```

It checks the 100-char cap and the mobile truncation window, whether the primary keyword survives truncation, emoji byte cost, claim blocklist hits, duration honesty against real runtime, hashtag/tag/description limits, chapter validity, and — the one nobody does by hand — lexical similarity against every title already in the catalogue, which is the exact signal YouTube's inauthentic-content detection reads at channel level. `--json` for pipeline use. Exit code 1 on any FAIL.

## Workflow

### 1 — Classify the job, then get the asset facts

Five jobs, different shapes: **(a)** name one track, **(b)** title one long-form upload, **(c)** design a naming system for a batch or series, **(d)** audit existing titles, **(e)** rescue a catalogue that is underperforming or flagged.

Facts you need, and where they come from: real runtime in seconds (from the file, not from intent), tuning (A=432, 528 Hz centre, standard 440), instrumentation and texture, intended use-case, the visual, whether audio is AI-generated, and what already exists on the channel. Infer what you can from the conversation and the files; ask once, in one message, only for what genuinely changes the answer. Never invent the duration — the title makes a promise the player will check.

### 2 — Research the live demand. Every time.

Read `references/keyword-research.md` and **run web_search**. Phrasing in this niche turns over fast: which frequency is trending, whether "deep sleep music" or "sleep music for deep sleep" is the dominant phrase, whether a modality has gone mainstream or stale. Writing titles from memory is how you end up bidding on 2023 language. Come out of this step with one primary phrase, two secondaries, and the competitor n-gram pattern from the current top results.

### 3 — Apply the two-name rule

Functional audio needs two names and confusing them is the most common failure:

- **Catalogue name** — poetic, short, unique. Lives in Suno, on the album, on DSPs, in the chapter list, in the cover art. This is identity.
- **Search title** — the functional phrase that wins YouTube. This is distribution.

They coexist: the catalogue name rides the search title as a suffix or a series marker, so branding accrues without costing you the front of the title. Deliver both, labelled, so the person knows which goes where.

### 4 — Build titles from the slot grammar

Read `references/title-grammar.md`. Produce **three candidates that bet on three different intents** — not three restylings of one bet. Sleep vs. meditation vs. study is a different audience, a different retention curve and a different CPM tier. For each candidate show the truncation preview at 50 and 70 characters, name the intent it targets, and say what it gives up. Then recommend one, with a reason.

### 5 — Run the claim pass

Read `references/claims-and-policy.md` and rewrite every outcome claim into design or intent language. The heuristic that does most of the work: **verbs about the music are safe, verbs about the body are not.** "Tuned to 528 Hz" is a fact about the recording. "528 Hz DNA Repair" is a medical claim about the listener, and it sits inside YouTube's highest-risk policy area. You can keep the entire searched keyword and drop the claim — that is the craft here, and it is not a compromise: honest framing survives review, keeps advertisers, and keeps the keyword.

### 6 — Build the metadata pack

Read `references/description-tags-chapters.md`. Deliver description (above-fold hook, use guidance, chapters, credits and catalogue name, natural keyword paragraph, hashtags, safety line), tags, hashtags, chapter list, playlist assignment, and the Shorts title if a Short is part of the release.

### 7 — Pass the gates, then log it

Run `scripts/metadata_audit.py`. Fix every FAIL, explain every WARN you are deliberately accepting. Then append the release to the ledger (`assets/catalog-ledger.csv`) — the ledger is what makes the duplication check work on upload 40, and it is also the evidence of human curation if the channel is ever reviewed.

## The gates

Nothing ships without clearing these. State explicitly which ones passed.

- **Truncation gate** — is the primary keyword fully inside the first ~50 characters? Mobile search cuts around there and mobile is most of this audience.
- **Promise gate** — does the title's duration, tuning and mood match the actual file? A "8 Hours" title on a 47-minute upload is misleading metadata, and it wrecks retention when viewers wake up to silence.
- **Claim gate** — zero body-outcome verbs, zero "instead of medication", zero clinical language without a real citation.
- **Duplication gate** — pairwise title similarity against the catalogue under the script's threshold, and no title skeleton reused more than a few times with only a number swapped.
- **Distinctness gate** — for AI-generated audio, does this upload differ from its siblings on at least three axes (arrangement, key/tempo, duration, visual, chapter structure, curation logic)? Same bed with a new title is reused content.
- **Thumbnail gate** — at 110 px the thumbnail and the first 30 characters of the title must not say the same thing twice. Redundancy wastes the only two assets you have.

## What makes this fail

- **Naming the track instead of the job.** "Amber Hollow" gets zero impressions. It belongs in the description and on Spotify, not at the front of a YouTube title.
- **Keyword paste.** "Sleep Music Relaxing Music Meditation Music Study Music Spa Music 432Hz" reads as spam, truncates into nonsense, and dilutes the one phrase you could have owned.
- **Claim escalation to chase CTR.** The niche's top-performing historical titles are full of "DNA repair" and "cure anxiety" language. Copying it inherits enforcement risk that those channels absorbed years ago under looser rules.
- **Template farming.** `Sleep Beats Vol. 12`, `Vol. 13`, `Vol. 14` is the textbook inauthentic-content pattern — the detection now runs at channel level, so one clean video does not offset the pattern.
- **Duration inflation.** Padding a 30-minute bed into "8 hours" by looping the same minute is reused content and a retention disaster in the same move.
- **Writing from memory.** Skipping the search step and reusing last season's phrasing.

## Honesty, plainly

Solfeggio and 432 Hz effect claims are not established by evidence. This skill never asks anyone to pretend otherwise, and it never writes a title that promises a physiological result. It states the tuning, names the use, and lets the listener decide — which is both the honest move and, conveniently, the one that keeps the channel monetised.

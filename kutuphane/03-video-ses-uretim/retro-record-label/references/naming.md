# Naming — A&R Department

A release title does three jobs at once: it means something, it can be found, and it passes a distributor's automated style check. Most naming advice covers only the first. A title that fails the second is invisible; one that fails the third delays the release.

## Contents
1. Before generating: what the name has to carry
2. Nine generation methods
3. The scoring rubric
4. Collision and searchability check (do this with web_search)
5. Turkish titles for a global release
6. DSP title legality — the rules that cause rejections
7. Track titles and sequencing
8. Delivering the shortlist

---

## 1. Before generating: what the name has to carry

Extract from the brief, and write it down:

- **The image the music makes.** One sentence, concrete, no adjectives. "A minibus at 3am on the coast road" beats "melancholic and nostalgic".
- **Register.** Plain and cold (post-punk), warm and human (soul), grand (prog), joking (indie), technical (library).
- **Length budget.** 1–3 words for singles. Album titles can take a phrase.
- **Language decision.** Turkish, English, or a proper noun that works in both.
- **Series logic.** If more singles are coming, does the naming leave room for a pattern?

## 2. Nine generation methods

Run at least four of these — a shortlist from one method all sounds the same.

1. **The concrete object.** Pull the most specific physical noun from the lyric or the mood. *Night Ferry. Copper Wire. Room 12.*
2. **Place plus time.** A location and an hour, season, or year. *Kadıköy Sunrise. Harbour, 4am. August Depot.*
3. **The collision.** Two words from different registers. *Velvet Debt. Neon Ablution. Concrete Lullaby.* Best hit rate, easiest to overdo — keep only the pair that actually means something.
4. **Removed phrase.** Take a common expression and cut a word until it turns strange. "Long way home" → *Long Way.* "Wait for the signal" → *Wait For The.*
5. **Instruction or imperative.** *Hold The Line. Don't Wake The House. Play It Twice.*
6. **Technical borrowing.** Recording, radio, navigation, print vocabulary — always era-appropriate. *Tape Bias. Signal / Ruin. Second Pressing. Dead Air.*
7. **Lyric fragment, not a lyric line.** Take four words from the middle of a verse, never the hook.
8. **Numeral / catalogue.** *Side B. Track 4. Volume Two.* Strong for instrumental and library-style releases; weak for search unless paired with a distinct artist name.
9. **The single strange word.** A word that is real but rare. Check it means what you think in English before shipping.

Generate 15–25, cut to a shortlist of 5–7 before scoring. Do not show the user the raw dump.

## 3. The scoring rubric

Score each shortlisted candidate 1–5 and show the table. A title that wins on meaning but scores 1 on searchability is a trap the user should see, not one to hide.

| Criterion | Question |
|---|---|
| **Fit** | Does it match the music's image and register? |
| **Searchability** | Would a search for it return this record, or 40 million other things? |
| **Sayability** | Can an English-speaking listener say it after hearing it once? |
| **Legibility** | Does it work in 3 words of display type at 110px? |
| **Room** | Does it leave space for a second and third release in the same world? |
| **Cleanliness** | Any accidental double meaning, slur, or brand collision in English? |

Common-noun single words (*Home, Waves, Gold, Dreams*) reliably score 5 on fit and 1 on searchability. If the artist wants one anyway, that is a legitimate choice — pair it with a distinctive artist name and say plainly that discovery will depend on the artist name doing the work.

## 4. Collision and searchability check (do this with web_search)

Never deliver a name unverified. For each of the top 2–3:

1. `web_search` the exact title with the genre — is there a charting or well-known track with that name?
2. `web_search` the title with "Spotify" or "song" — how crowded is the result page?
3. If a proper noun or invented word: search it alone for unintended meanings, brands, or existing artist names.
4. Check the **artist + title** pair as a phrase — that combination is the real search key, and a crowded title is survivable if the pair is unique.

Report what you found, briefly: "*Night Ferry* — one 2019 folk EP with this title, low profile, no chart presence; *artist + Night Ferry* returns nothing, so the pair is clean." That evidence is what makes the recommendation trustworthy.

Names that collide with a major release should be dropped, not tweaked with a "(feat.)" or a stylisation — stylised workarounds break search harder than the collision did.

## 5. Turkish titles for a global release

A real trade-off, and it belongs to the user, not to you. Give them the mechanics:

- **Turkish diacritics cost discoverability.** `ı ğ ş ö ç ü` are hard to type on an English keyboard, and although DSP search is diacritic-tolerant, YouTube autocomplete and word-of-mouth typing are not. *Gölge* becomes *Golge* in half the searches.
- **Rejection risk is zero** — Turkish characters are fine in metadata, so this is purely a marketing decision.
- **Three viable strategies.** (a) Turkish title, English subtitle in the YouTube description only, never in the DSP title field. (b) Turkish title chosen from words without diacritics (*Duman, Sonsuz, Kum, Ada*) — keeps identity, keeps typeability. (c) English title for the release, Turkish for the album, so the local identity lives at album level.
- **Place names travel best.** *Kadıköy, Bosphorus, Anatolia, Üsküdar* carry meaning to a foreign listener as texture rather than as language.
- **Never machine-translate a poetic Turkish title into English.** It arrives flat. Rewrite the *image* in English instead.

## 6. DSP title legality — the rules that cause rejections

Distributors run automated style checks against Spotify's and Apple's metadata style guides. These are the ones that actually get releases bounced:

- **No promotional or decorative text in titles.** No "Out Now", "New Single", "HD", "Official", "Remastered" (unless it genuinely is), no decorative symbols, no `★`, no `///`.
- **No emoji anywhere in metadata.** Apple rejects outright.
- **Version descriptors go in parentheses, after the title.** `Night Ferry (Acoustic)`, `Night Ferry (Radio Edit)`. Not brackets, not a dash.
- **Explicit / Clean is a separate metadata flag, never text.** Writing "(Clean Version)" in a title is a rejection.
- **`feat.` is the only accepted form** — not "ft.", not "featuring", not "with". And featured artists belong in the artist role fields; Spotify displays them automatically, so repeating them in the title looks amateur unless your distributor requires it.
- **Don't put the artist name in the release title.** Self-titled releases are the exception.
- **Capitalise by the rules of the title's language.** English title case: first and last word always, plus all significant words. Turkish titles follow Turkish capitalisation. No ALL CAPS titles, and no lowercase stylisation, even if the cover art sets it that way — the artwork can stylise, the metadata cannot.
- **No URLs, handles, or contact info** in any metadata field.
- **Composers and lyricists must be full legal names.** No aliases in those fields.
- **Genre must be accurate.** Mis-tagging to chase a playlist degrades algorithmic placement rather than helping it.

Deliver these as a small "metadata sheet" the user can paste into their distributor. See `youtube-metadata.md` for the full sheet format.

## 7. Track titles and sequencing

For an EP or album:

- **Vary the shape.** Not five two-word noun phrases. Mix a one-word title, a phrase, an imperative, a numeral.
- **The opener names the world; the closer resolves it.** The strongest title usually should not be track 1 — save it for the single.
- **The album title should not repeat a track title** unless you intend the title-track convention, which is a real and fine choice for rock and jazz and reads odd for electronic.
- **Interludes:** keep them clearly subordinate (*Interlude*, *Passage*, a duration) so the tracklist has a visible spine.
- **Durations matter for the sequence** — put the longest track where an LP side would break, even for a digital-only release. It still feels right.

For a single with B-sides, name the B-side so it cannot be mistaken for the A-side: quieter, stranger, shorter.

## 8. Delivering the shortlist

Format the handoff like this and nothing longer:

```
Recommended: Night Ferry
  Why: the coast-road image, cold register, two syllables of display type.
  Search: one low-profile 2019 EP shares the name; artist + title returns nothing.
  Metadata-safe: yes. DSP title → "Night Ferry"

Runner-up: Signal / Ruin — colder, more post-punk; the slash is legal but
  splits search results, so expect people to type it three ways.

Also viable: Second Pressing, Long Way, Dead Air   [scores in the table above]
```

Then move to art direction, because the title determines how many words the cover has to carry.

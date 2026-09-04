---
name: pexels-media-scout
description: Finds, scores, clearance-checks and downloads royalty-free Pexels photos and video for music deliverables — album covers, YouTube thumbnails and long-form backgrounds, lyric-video and Spotify Canvas beds, Reels/Shorts footage, press kits. Turns a vague or Turkish brief into queries that actually return usable frames, ranks candidates against the real spec (resolution headroom, crop survival, brand colour, text room, clip duration and loopability), flags model-release and trademark risk before anything ships, and writes attribution files. Use whenever someone needs stock visuals or B-roll for music, a cover image, a thumbnail or a video background, or mentions Pexels — including Turkish phrasings like "telifsiz görsel bul", "albüm kapağı için fotoğraf", "youtube thumbnail görseli", "arka plan videosu lazım", "stok video indir", "pexels api ile görsel çek", "ücretsiz stok fotoğraf". Trigger even when Pexels is never named — if the task is picking the right free image or clip for a deliverable, this applies.
---

# Pexels Media Scout

Stock search fails in two predictable ways: the query describes a feeling instead of an
object, and the chosen frame is picked on how it looks in a thumbnail grid rather than
whether it survives the actual deliverable. This skill fixes both, then catches the
clearance problems that only surface after a release is live.

Division of labour: **you** do the creative translation (brief → query variants, final
visual judgement), the **script** does the mechanics (paginated search, scoring, dedupe,
correct file variant, attribution).

## Setup — before the first run

The API key must never live in a file that gets committed or pasted into a chat.

```bash
mkdir -p ~/.config/pexels
printf '%s' 'THE_KEY' > ~/.config/pexels/key && chmod 600 ~/.config/pexels/key
# or, per shell session:
export PEXELS_API_KEY='THE_KEY'
```

If a key has been shared in plain text anywhere — chat, ticket, commit — say so plainly
and tell the user to rotate it at pexels.com/api before using it. Do not quietly proceed
with an exposed key.

Quota is 200 requests/hour and 20,000/month. The script caches responses for 24h, so
re-running a search with the same queries costs nothing. Check with
`python3 scripts/pexels_scout.py quota`.

## Workflow

### 1. Pin down the deliverable before searching

The deliverable dictates orientation, resolution floor and whether people are acceptable —
so establish it first. `python3 scripts/pexels_scout.py presets` lists the specs.

Common ones: `album-cover-3000`, `yt-thumbnail`, `yt-longform-bg`, `lyric-video-bg`,
`spotify-canvas`, `reels-short`, `ig-feed-45`, `web-hero`, `press-kit`.

If the brief mentions a brand palette, capture the hex — it feeds scoring. If it mentions
a genre or mood, that is a *query* input, not a filter.

Ask only when the answer changes the search and cannot be inferred: which deliverable, and
whether people in frame are acceptable. Everything else, infer and state the assumption.

### 2. Translate the brief into 3–5 query variants

Read `references/music-query-lexicon.md` before writing queries. The short version:
rewrite the brief as `[concrete object] + [material/texture] + [light condition]`, then
vary along one axis per query — literal subject, macro detail, environment without subject,
abstract texture, adjacent object.

Search in English regardless of the brief's language. Turkish-specific instruments are
barely covered; when the brief needs one, search the world around it and say so rather
than substituting a generic guitar photo.

### 3. Search and score

```bash
python3 scripts/pexels_scout.py search \
  --preset album-cover-3000 \
  -q "vinyl record macro dust" \
  -q "reel to reel tape machine low light" \
  -q "brass tray bazaar warm light" \
  -q "black paper texture grain" \
  --color "#1c1a17" --exclude-people \
  --limit 12 --out shortlist.json
```

Useful flags: `--exclude-people` (drops anything the heuristic reads as a recognisable
person — the default choice for commercial covers), `--color` (brand hex, scored not
filtered), `--color-filter` (hard Pexels colour filter, photos only, use sparingly since
it collapses the result set), `--page 2` (deeper pages of a specific query beat page 1 of a
generic one), `--max-per-author` (default 2, stops one shoot owning the shortlist).

Each candidate gets a score with its reasoning exposed: rank, resolution multiple against
target, crop retention, colour distance, tone suitability for overlaid text, clip duration.
Negative scores mean the frame cannot serve the deliverable — usually undersize.

### 4. Look at the frames

Score narrows the field; it does not choose. Build a contact sheet and actually look:

```bash
python3 scripts/pexels_scout.py sheet --shortlist shortlist.json --out sheet.html
```

Previews are hotlinked, so this costs no quota. Present the top candidates to the user
with the reasoning and the flags, and say which one you would pick and why. If every
candidate is weak, say that instead of recommending the best of a bad set — then go back to
step 2 with different variants. A wrong-but-confident pick costs more than another search.

### 5. Clearance check before download

Read `references/licensing-and-risk.md` when a candidate carries flags or the asset is
headed for a commercial release. The failure modes the licence does *not* cover:
recognisable faces (no model release), visible logos and branded gear (no trademark
release), selling unaltered copies on merch, and the audio track on video clips.

Flags from the scorer are keyword heuristics on alt text — they catch the obvious cases and
miss the rest. Look at the frame.

### 6. Download with attribution

```bash
python3 scripts/pexels_scout.py download \
  --shortlist shortlist.json --pick 1,4 \
  --out ./assets --project "WEFT-001"
```

Picks the right variant automatically: `original` for anything above 900px (the sized
variants top out at 940px wide and will not survive a 3000px cover), and the smallest video
file that still clears the target. Writes `CREDITS.md`, `credits.json` and a per-file
`.credit.txt`.

The API Guidelines require a prominent Pexels link wherever these assets appear — YouTube
description, release notes, site footer. Remind the user where the credits need to land;
they are not optional just because attribution is not legally required.

For video, strip the audio: `ffmpeg -i in.mp4 -an -c:v copy out.mp4`.

## Handing off

- **retro-record-label** — hand it the downloaded original as the photo plate for
  halftone/duotone/riso treatment. That treatment also satisfies the "substantially new
  composition" requirement, which matters if the art will touch merch.
- **post-forge** — hand it the file path plus the `avg_color`, so the design system can
  build around the frame's actual tone instead of guessing.
- **suno-composer** — the mood language in a Style field is the same raw material as a
  query brief; reuse it, but translate it to objects before searching.

## Reference files

- `references/music-query-lexicon.md` — brief → query translation, Turkish handling,
  per-mood query banks, negative-space proxies, video loopability. Read before step 2.
- `references/licensing-and-risk.md` — what the Pexels License does and does not cover,
  API Guidelines obligations, pre-ship clearance checklist. Read before step 5, and always
  before a commercial release.

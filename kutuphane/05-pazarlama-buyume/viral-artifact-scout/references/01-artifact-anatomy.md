# Artifact Anatomy — why these spread and how they're built

Read this in Phase 1, and again in Phase 5 when scoring the "virality" factor. It gives you the vocabulary to say *why* something worked instead of "it went viral."

## Contents
- The five ingredients
- Why people post: the four status motives
- Format taxonomy
- The image itself: design constraints
- The 30-second rule
- Loop mechanics: what makes a spike come back
- Anti-patterns

---

## The five ingredients

A working artifact app has all five. Missing any one is the usual explanation for a project that "should have gone viral" and didn't. Use this as a checklist when diagnosing hits *and* when scoring candidates.

**1. Personal truth.** The artifact must be about *this specific person* and must be non-obvious to them. Spotify Wrapped works because you don't actually know your top artist. A calculator that tells you your BMI is personal but not surprising; a chart that tells you your taste is more obscure than 94% of listeners is both.

**2. Compressed status.** The output has to encode something the person wants associated with their name — taste, effort, obscurity, achievement, or an endearing flaw. "My gym streak" and "my embarrassing top song" both work; the second works because self-deprecation is also status. Pure neutral data ("you listened to 41,000 minutes") is weak on its own.

**3. Instant legibility.** A stranger scrolling a timeline must understand the image in under one second without reading the caption. The receipt format won because everyone already knows what a receipt is; the poster format won because everyone knows what a festival lineup is. **Borrowing an existing visual grammar is the highest-leverage design decision in this genre.**

**4. Comparability.** The artifact must invite a reply. Formats that produce a *number*, a *rank*, or a *grid* generate quote-tweets ("mine's worse"); formats that produce a paragraph do not. Comparability is what turns one post into a thread.

**5. Zero friction to the image.** From landing to downloadable image, ideally under 30 seconds, with no signup, no email, no paywall before the reveal. Every step before the artifact costs a large fraction of users and virality is multiplicative across steps.

## Why people post: the four status motives

Knowing which motive a candidate targets tells you what to optimize and who will share it.

- **Taste signalling** — "I have good/obscure/unexpected taste." Music, film, books, coffee, games. Highest share rate, lowest willingness to pay.
- **Effort signalling** — "look what I did." Streaks, distance, hours, commits, exam results, finished books. Shares less often but the audience is more invested and more willing to pay for a nicer artifact.
- **Identity declaration** — "this is my tribe." Team, city, hometown, generation, school, fandom. Extremely strong in Turkey; underused in Western artifact apps.
- **Self-deprecation** — "I'm a disaster, look." Roasts, worst-of lists, guilty pleasures. Spreads fastest of all because posting it costs nothing socially, but produces the least durable product.

The best candidates hit two motives at once. Effort + self-deprecation ("your streak, but the app is mean about it") is a reliably strong pairing.

## Format taxonomy

The container is half the product. When generating candidates, cross the format list against the data source list — most new ideas in this category are literally an unexplored cell in that grid.

| Format | Visual grammar borrowed from | Best for | Notes |
|---|---|---|---|
| Receipt | Thermal till receipt | Ranked lists, 5–20 items | The most-copied format; needs a monospace face and paper texture to read right |
| Poster / lineup | Music festival bill | Weighted ranked lists | Hierarchy does the work: headliner = top item |
| Pie / bar / radar | Data viz | Proportions, categories | Only works if the categories are *judgeable* |
| Grid / collage | Album wall, Letterboxd | 9–25 visual items | Needs artwork; rights questions if the art isn't the user's |
| Tier list | S/A/B/C/D meme | User-ranked opinions | **No API needed** — the user supplies everything. Systematically underrated |
| Iceberg | Meme format | Obscurity depth | Strong taste signal, hard to generate well |
| ID card / passport | Official document | Identity declaration | Very strong for tribal identity; travels well to TR contexts |
| Certificate / diploma | Award document | Effort, milestones | Prints well — the one format with a natural physical upsell |
| Report card / grade | School report | Judgement | Pairs perfectly with roast tone |
| Wrapped story deck | Instagram Stories | Multi-stat narrative | Vertical, sequential; higher build cost, higher completion feeling |
| Map | Cartography | Places visited, coverage | Great for cities, districts, provinces |
| Roast / letter | Chat message, letter | LLM-written judgement | Per-artifact cost; funny once, rarely twice |
| Emoji grid | Wordle share block | Daily games | Text-only, so it beats image compression and works everywhere |

The **emoji grid** row deserves its own note: Wordle's share block spread because it is copy-pasteable text that survives every platform, spoils nothing, and takes zero design work. Any daily-loop candidate should consider a text artifact before an image one.

## The image itself: design constraints

- **Aspect ratios.** 1080×1920 for Instagram/TikTok Stories (the dominant surface). 1200×675 (16:9) for X inline. If you produce one, produce both — the same artifact re-cropped is a doubling of reach for an hour of work.
- **Thumbnail legibility.** Design for ~350px wide. The headline number or top item should be readable at that size. Test by scaling down, not by squinting at full size.
- **Attribution that survives.** A small wordmark plus the URL, bottom edge, high contrast. This is the entire acquisition mechanism — the image *is* the ad. Do not hide it tastefully into invisibility. Do not make it so loud people crop it out.
- **Crop resistance.** Assume the bottom 10% may be cropped by a platform preview. Put the wordmark where a crop won't kill it, or repeat it.
- **Save vs screenshot.** Offer a real download and a native share sheet. A meaningful share of users screenshot instead — meaning your on-screen layout must *also* be a good artifact, including status-bar-safe margins.
- **OG image.** The link preview should render an example artifact, not a logo. Half of the traffic from a viral post comes from people who clicked the link in a reply, and the preview is what sells the click.
- **Fonts and rights.** Web fonts need licenses for embedded/rendered use. Album art, club crests, film posters and character images are somebody's IP — an artifact built entirely out of other people's copyrighted images is a takedown waiting to happen, especially if you sell prints of it. Prefer type, color, and layout over borrowed imagery; if you must show artwork, show it at thumbnail scale in a way that is clearly a personal summary.

## The 30-second rule

Landing → artifact in under 30 seconds. Concretely:

- No account creation. OAuth only if the data requires it, and the reveal comes immediately after.
- No email gate before the reveal. Ask *after* the artifact is on screen if at all.
- No paywall before the reveal. The free artifact is the marketing; charge for the upgrade.
- Server-render or client-render the image, but pre-warm it — a 15-second "generating..." spinner during a traffic spike is where most of these die. Load-test for a 100× burst before launch, not after.
- Cost per artifact must survive the spike. An LLM or image-gen call per user is fine at 500/day and a disaster at 500,000/day. Cap it, queue it, or cache it.

## Loop mechanics: what makes a spike come back

One-shot artifacts get one spike, decaying with a half-life of about three days. Recurring artifacts are worth far more. The four recurrence patterns, roughly in order of strength:

1. **Daily.** A new artifact every day (Wordle-class). Strongest retention in the category; requires content generation and a genuinely fresh puzzle or stat each day.
2. **Seasonal / calendar.** An annual or event-anchored moment (wrapped in December, exam results in July, transfer window, season end). Predictable, marketable, and lets you sell sponsorship in advance — but you get one shot a year and must survive between shots.
3. **Trigger-based.** The artifact regenerates when the underlying data changes meaningfully (new personal best, a finished book, a milestone). Low ceremony, good retention, requires ongoing data access.
4. **Variant-based.** New skins, themes, or formats on the same data, released periodically. Cheapest to build; weakest pull; works mainly to extend an existing spike rather than start a new one.

A candidate with no recurrence pattern isn't disqualified — but it should be evaluated as a one-time acquisition event, not a product.

## Anti-patterns

- **The insight nobody wants to post.** Accurate, interesting, and socially useless. Financial data often lands here: people are fascinated by their own spending and will not post it.
- **Reveal behind signup.** Kills the loop at the exact point where excitement peaks.
- **Paragraph output.** Text results don't travel. If the output must be words, put them in a strong visual container.
- **Requires a friend to work.** Two-sided artifacts ("compare with a friend") have a much harder cold start. Make the solo version complete, then add compare as an upgrade.
- **Platform-dependent with no fallback.** One terms-of-service update and the product is gone. See `03-data-sources.md`.
- **Beautiful but illegible at thumbnail size.** Very common in designer-built entries. The timeline is the venue.

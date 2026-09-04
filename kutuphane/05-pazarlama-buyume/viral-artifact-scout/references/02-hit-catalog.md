# Hit Catalog — what worked, what died, what it taught

Read this in Phase 1 as a **seed**, not as an answer. Everything here has a date; this category turns over fast and several entries below were alive when written and may not be now. **Verify current status before citing any of it to a user.**

Catalog compiled: mid-2026.

## Contents
- The Spotify cluster (and why it's closed)
- Non-music artifact apps
- Daily-loop games
- Quiz and identity artifacts
- AI-generated artifacts
- The graveyard: killed by platform, not by market
- Patterns extracted

---

## The Spotify cluster

This is the origin of the genre and it is now the least accessible part of it. Study it for the mechanics; do not propose building in it without reading `03-data-sources.md` first.

| App | Artifact | Peak | What it taught |
|---|---|---|---|
| **Spotify Wrapped** (Spotify, 2015→) | Vertical story deck | Every December | The reference implementation. 2025 edition reportedly saw over 500M shares in its first day, up sharply YoY, driven by a "listening age" guess and a friend-comparison feature — *the guesses and comparisons drove sharing more than the raw stats did* |
| **Receiptify** (Michelle Liu) | Thermal receipt of top tracks | 2021, revived annually | Borrowed visual grammar beats invented visual grammar. Supported Spotify, Apple Music and Last.fm — multi-source was a real moat |
| **Instafest** (Anshay Saboo, USC student) | Festival lineup poster | Nov–Dec 2022 | Built by a student in days, reached millions. Timing against the Wrapped window was the whole strategy — it rode a wave someone else made |
| **Spotify Pie** (Darren Huang) | Genre pie chart | 2022→ | Simplest possible viz, enormous reach. Complexity is not the differentiator |
| **How Bad Is Your Streaming Music** (The Pudding) | Judgemental AI critic | 2020 | Roast tone as the product. Also a masterclass in editorial-team-as-artifact-factory |
| **Obscurify** | Obscurity percentile vs others | 2018→ | Percentile-against-others is the strongest single comparability device in the genre |
| **Icebergify** | Iceberg meme of artists | 2022 | Meme format as container; near-zero design cost |
| **stats.fm** (ex-Spotistats) | Ongoing stats dashboard | Grandfathered | The only sustainable model in the cluster: a real subscription app, not a one-shot |

**Status note:** the free-and-open era of this cluster ended in stages — Nov 2024 (endpoint restrictions), 2025 (extended quota gated behind a registered business and 250K MAU), Feb–Mar 2026 (Development Mode gated behind Premium, one Client ID per developer, five authorized users). Apps that had extended access before the cutoffs were grandfathered; new entrants were not. **Treat this cluster as closed to new builders.** Details and dates in `03-data-sources.md`.

## Non-music artifact apps

Where the live opportunity mostly is, because these platforms have not (yet) done what Spotify did.

- **Letterboxd year-in-review / poster grids** — film. Strong taste-signalling audience; several third-party stat tools exist. Check current API and export status.
- **Strava Year in Sport** — effort signalling. First-party. Third-party Strava artifact tools exist and Strava's API terms have tightened over time — verify.
- **Chess.com / Lichess recaps** — effort + rating. Lichess is open-data and open-source-friendly, which makes it unusually hospitable.
- **GitHub-based artifacts** (contribution art, "wrapped", profile roasts) — effort signalling for developers. Public data, no auth needed for public profiles. Extremely low feasibility risk; correspondingly crowded.
- **Steam year in review / library artifacts** — games. Public profile data available; large audience.
- **Goodreads / StoryGraph reading recaps** — books. Goodreads API access has been closed to new keys for years; StoryGraph and user CSV export are the practical paths.
- **Duolingo streak artifacts** — effort + self-deprecation; first-party recap is strong.
- **Monzo / N26 / Revolut year-in-review** — financial. Notable mainly as a lesson: banks deliberately keep these *private*, ending on a shareable badge rather than shareable numbers, because people won't post their spending. See the anti-pattern note in `01-artifact-anatomy.md`.

## Daily-loop games

The strongest retention pattern in the category, and the one most transferable to Turkish.

- **Wordle** — the emoji-grid share block is the single most efficient viral artifact ever built: text, spoiler-free, platform-proof, zero design. Acquired by NYT.
- **Connections / Strands / Mini Crossword** — proof that a portfolio of daily games is a real business, not a novelty.
- **Framed / Heardle / Costcodle / Globle / Worldle** and the long tail of "-dle" games — one mechanic, one data set, one daily puzzle. Most made little; a few sold.

The lesson: the daily-game format is nearly free to enter and nearly impossible to defend, so it is a good fit when you have **a proprietary or hard-to-assemble dataset** and a bad fit when you don't.

## Quiz and identity artifacts

- **16Personalities / MBTI-style results** — the highest-volume identity artifact category on earth, monetized through paid reports. Note the model: free result, paid depth.
- **Political compass / values quizzes** — periodically viral, especially around elections.
- **BuzzFeed-style "which X are you"** — the ancestor of the whole genre; monetized by ads at scale, which is why it declined as display CPMs fell.

These need **no data source at all**, which makes them the highest-feasibility, lowest-defensibility corner of the map. The differentiator is writing quality and visual design, not engineering.

## AI-generated artifacts

Post-2023 wave. Everything here has real per-artifact cost, which changes the economics fundamentally.

- **Profile roasts** (GitHub, X, LinkedIn, Spotify) — LLM reads a public profile, produces a mean paragraph in a card. Cheap to build, spreads fast, dies fast, costs money per user.
- **AI portrait / avatar apps** — the only reliably *profitable* AI artifact category, because the output is worth paying for and people pay up front. Also the most crowded and the most compute-expensive.
- **"Your life in X" generators** — LLM-written narratives from a small input. Weak: paragraph output doesn't travel.

Rule of thumb: if the artifact costs money per generation, the free-then-viral loop can bankrupt you at exactly the moment it works. Cap generation, cache aggressively, or charge before the expensive step (and accept the conversion hit).

## The graveyard: killed by platform, not by market

Worth its own section because it is the most important pattern in the catalog. In each case demand was intact and access disappeared.

- **The Spotify third-party ecosystem** — audio features, recommendations, related artists, featured playlists restricted Nov 27 2024; quota gated 2025; Development Mode gated 2026. Hundreds of tools broke.
- **Twitter/X free API** — closed and repriced in 2023. An entire generation of "your Twitter stats", "your mutuals", "your first tweet" artifacts vanished overnight.
- **Goodreads API** — closed to new keys, 2020.
- **Instagram Basic Display** — deprecated, removing another class of personal-data artifacts.
- **AcousticBrainz** — shut down 2022, taking a common open fallback with it.

**The lesson to carry into every evaluation:** in this category, the modal cause of death is not "nobody wanted it." It is "the platform closed the door." That is exactly why the feasibility gate comes before the creative work, and why user-supplied-data and public-data designs deserve a premium in scoring.

## Patterns extracted

1. **Borrowed visual grammar beats invented grammar.** Receipt, poster, tier list, ID card, report card — all pre-understood.
2. **Percentile beats absolute.** "More obscure than 94% of listeners" outperforms "you listened to 41,000 minutes."
3. **The guess is better than the stat.** Wrapped's biggest 2025 driver was the app *guessing something about you* — an assertion invites a reply in a way a number doesn't.
4. **Timing against someone else's wave works.** Instafest launched into the Wrapped window. Find the wave; don't try to make one.
5. **One-shot artifacts get one spike.** Everything durable in this catalog is either a daily loop, a subscription, or a funnel into something else.
6. **The platform is the risk, not the market.**

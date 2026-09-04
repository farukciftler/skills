# Data Sources — the feasibility gate

Read this in Phase 2, before any creative work. This is the file that kills ideas, which is its job.

**Everything below is dated and must be re-verified.** Access rules in this space change every few months, and a confidently stated stale rule is the worst output this skill can produce. Treat this register as a *starting hypothesis and a list of things to check*, and check them: fetch the developer terms page, search for changes in the last six months, and date whatever you tell the user.

## Contents
- The three access paths
- Register: platform-by-platform
- Pattern A: user-supplied data
- Pattern B: public and open data
- Pattern C: data you generate
- Red flags in developer terms
- How to verify quickly

---

## The three access paths

Every candidate resolves to one of three, and they are not equally good.

| Path | Durability | Friction | Verdict |
|---|---|---|---|
| Official API with OAuth | **Fragile** — one policy update ends it | Lowest | Fine, but never build the whole business on one |
| User-supplied data (export upload, paste, screenshot) | **Durable** — nobody can revoke it | High — costs a large share of users | Underrated; the correct answer more often than people think |
| Public / owned / generated data | **Most durable** | None | Underrated; feels less clever, ships faster, survives longer |

A candidate that only works via path 1 should be scored down on feasibility even if the API is open today. A candidate that works via path 2 or 3 should be scored up, and this asymmetry is the single most useful thing in this file.

## Register: platform-by-platform

Status as of mid-2026. **Re-verify.**

### Music

**Spotify — effectively closed to new builders.** Sequence:
- 27 Nov 2024: new apps lost Related Artists, Recommendations, Audio Features, Audio Analysis, Get Featured Playlists, Get Category's Playlists. Apps already in extended mode were grandfathered. (Source: developer.spotify.com/blog/2024-11-27-changes-to-the-web-api)
- 2025: extended quota mode requires a registered business, roughly 250K monthly active users, and presence in key markets. Below that threshold there is no path.
- 6 Feb 2026 announcement: Development Mode requires a Spotify Premium account, one Client ID per developer, max five authorized users, reduced endpoint set. Applied to new Client IDs from 11 Feb 2026 and to existing integrations from 9 Mar 2026. Public playlist *contents* also restricted to playlists the user owns or collaborates on. (Source: developer.spotify.com/blog/2026-02-06-update-on-developer-access-and-platform-security)
- **Standing policy, independent of the above:** the Developer Policy prohibits building a game, including trivia quizzes — and Spotify staff have clarified this covers any game, even one that doesn't stream or use Spotify content. Quiz-format artifacts on Spotify data are out on policy grounds regardless of endpoints.

Practical reading: a new solo developer cannot ship a public Spotify artifact app in 2026. Say this plainly rather than suggesting workarounds.

**Apple Music / MusicKit** — alive, but requires an Apple Developer Program membership and produces a different (smaller) feature set. The realistic successor for music artifacts on iOS. Verify what personal listening history is actually exposed before promising it.

**Last.fm** — historically the friendliest music API and the fallback that kept Receiptify-class tools alive. Small user base, but the users who have it are exactly the taste-signalling audience. Verify current terms.

**Deezer / Tidal** — smaller, occasionally more open. Both worth checking when Spotify is the blocker; neither has meaningful Turkish share.

### Social

**X / Twitter** — paid tiers only since 2023, with pricing that makes free consumer artifact apps uneconomic. Assume closed unless the person is willing to pay real money per month. This is why the "your Twitter stats" genre disappeared.

**Instagram / Threads / TikTok** — no meaningful personal-history API for this use. TikTok has a limited research/display API; verify scope. Assume closed.

**Reddit** — API repriced 2023; a free tier exists with limits. Public data on a username is accessible enough for roast-style artifacts. Verify rate limits.

**LinkedIn** — restrictive partner program. Assume closed; roast-style tools work from user-pasted profile text instead.

### Effort / quantified self

**Strava** — has an API; terms have tightened over time, particularly around displaying and storing data. Verify carefully — this one has bitten third parties.
**Apple Health / HealthKit** — on-device only, which is a *feature* here: the data never leaves the phone, so the KVKK/privacy story is clean and the artifact renders locally. Strong fit for an iOS-native artifact app.
**Google Fit / Health Connect** — Android equivalent; verify current status, Google has been migrating this.
**Duolingo, Whoop, Oura, Garmin** — varying degrees of openness; each needs individual verification.

### Games / dev

**Steam Web API** — public profile and library data available with a key; long-standing and stable.
**Chess.com public API** — open, no key needed for public data. **Lichess** — fully open, generous, open-source-friendly. Both are unusually safe bets.
**GitHub** — public profile and contribution data available; generous limits; the safest major platform in this list.
**Riot, Xbox, PlayStation** — Riot has a developer program with approval; console platforms are effectively closed.

### Media

**Letterboxd** — API access has historically been limited; user CSV export exists. Verify current state.
**Trakt** — has an open API; the practical path for film/TV artifacts.
**TMDB / IMDb** — metadata, not personal data. TMDB is free with attribution and is the standard backing dataset; IMDb's data is licensed and restricted.
**Goodreads** — API closed to new keys since 2020. Use **StoryGraph** or the user's Goodreads CSV export.

## Pattern A: user-supplied data

**The most important pattern in this file.** When the API closes, the surviving product asks the user for their own data. Four mechanisms:

1. **Data-export upload.** Under GDPR/KVKK, platforms must give users their own data. Spotify, Google, Instagram, Netflix, banks and many others provide a downloadable export. The user requests it, waits (hours to days), and uploads the file. High friction, zero platform risk, and legally clean — *the user is exercising their own right, not you scraping*.
2. **Paste.** The user copies text or a URL. Nearly frictionless for roast-style artifacts built on a public profile.
3. **Screenshot upload + OCR/vision.** The user screenshots their own in-app stats and you read it. Friction is low, accuracy is the risk, and it works against platforms with no API at all. This is a genuinely strong path in 2026 given vision models.
4. **Manual entry.** The user types or ranks. Tier lists, quizzes, and ranking artifacts live here — no data source at all, which is why they are the highest-feasibility corner of the map.

Honest cost: each added step loses users, and an export-request flow that takes a day loses most of them. Design around it — let the user get a *partial* artifact instantly from something cheap (paste, a few questions) and offer the full version to those who upload.

Legal framing to keep in the dossier: helping a user process their own exported data on their own device or in a stateless server call is materially different from scraping a platform, and it is the design to recommend.

## Pattern B: public and open data

No permission needed, no revocation risk. Candidates:

- Sports results, fixtures, league tables, transfer records
- Exam and education statistics published by public bodies
- Government open data portals, municipal data, census-type datasets
- Financial instrument prices and fund data published by exchanges or regulators
- Weather history, air quality, geographic data (OpenStreetMap)
- Wikipedia / Wikidata
- Any dataset the person has already assembled for another project

Check licence and re-use terms — "public" is not automatically "reusable commercially", and scraped-from-a-public-website is not the same as open-licensed. Where a site publishes data without an open licence, prefer the official export, an API, or a licensed provider.

The systematic advantage: a public-data artifact app can run for years untouched. The systematic disadvantage: so can a competitor's.

## Pattern C: data you generate

Quizzes, daily puzzles, LLM judgements, and rankings the user creates. Zero access risk, zero defensibility, and the entire differentiator is craft — writing, humour, and visual design. Do not dismiss this: several of the largest artifact properties ever built (personality tests, daily word games) are pure Pattern C.

Watch unit cost when an LLM is in the loop. Per-artifact spend that is trivial at 1,000/day is a real bill at 500,000/day, and the spike is exactly when it hits.

## Red flags in developer terms

Search the terms page for these before designing anything:

- "game", "quiz", "trivia" — often explicitly prohibited (Spotify is the notable case)
- MAU thresholds or "extended access" gates
- Bans on storing, caching, or displaying data outside the platform's context
- Bans on ranking, scoring, or comparing users
- Attribution and branding requirements — many require specific logo use, which affects the artifact design
- Commercial-use and advertising restrictions — several APIs are free only for non-commercial use, which kills the ad model
- Rate limits per app rather than per user — these break precisely during a spike

## How to verify quickly

For each candidate platform, in order:

1. Fetch the developer terms/policy page and read the prohibited-applications section.
2. Search for changes in the last 6–12 months: `<platform> API changes 2026`, `<platform> API deprecated`, `<platform> developer policy update`.
3. Check the platform's developer community/forum for people reporting 403s — practical status often precedes documented status.
4. Look for a third-party app doing this *today* and check whether it is grandfathered. A live competitor is not proof the door is open; several visible apps in this category are running on legacy access nobody new can get.
5. Record the date and URL of what you found. Put both in the dossier.

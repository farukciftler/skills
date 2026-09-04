# Turkey — native status objects, data, rails, law, calendar

Read this in Phase 3. Its purpose is to stop the analysis from producing "Receiptify ama Türkçe" and push it toward opportunities a Western builder has no reason to think of.

**Verify anything time-sensitive here.** Legal thresholds, platform availability and rates change; dates and figures below are starting points for checking, not settled facts.

## Contents
- The core asymmetry
- TR-native status objects
- What data actually exists in Turkey
- Payment and monetization rails
- KVKK
- The Turkish seasonal calendar
- Practical gotchas

---

## The core asymmetry

Turkey is unusually strong on the *demand* side of this category and unusually weak on the *supply* side.

Demand: very high social platform usage, an X user base that punches above the country's size, near-universal Instagram Stories behaviour, and — the important part — a culture with an exceptionally rich set of **collective identity markers**. Tribal identity ("this is my team / my city / my school / my generation") is a much stronger sharing motive in Turkey than in most Western markets, and Western artifact apps almost never target it because their own markets are organised around individual taste instead.

Supply: very little of the local data is exposed through APIs, ad monetization is weak, and consumer willingness to pay is low. That combination is exactly why gaps exist — and exactly why most of those gaps are cause 1 or 4 in the Phase 3 table, not cause 6.

The design implication: **build on identity declaration and public data, monetize with something other than Turkish ad impressions.**

## TR-native status objects

Cross these against the format taxonomy in `01-artifact-anatomy.md` to generate candidates. Each is a thing Turkish people already treat as identity-defining, with no clean Western analogue.

**Education and exams.** The university entrance system is an annual national event affecting millions of families, with a result, a ranking, a preference process, and a shared vocabulary. Everything about it is artifact-shaped: a score card, a ranking percentile, a "where my score would have got me in year X" comparison, a department tier list, a nostalgic "my exam year" card for adults. It has a hard, predictable seasonal peak. Note the sensitivity: this is a high-anxiety subject for teenagers, so tone matters enormously and anything that mocks a low score is out.

**Football.** Fandom is a primary identity, not a hobby. Derby records, transfer windows, squad tier lists, "your XI", fan ID cards, historical head-to-head cards, a fan's personal season summary. The data is largely public. This is arguably the single most under-served intersection in the Turkish market: enormous emotional investment, near-zero artifact tooling.

**Hometown and district.** Memleket and mahalle identity are strong and map beautifully to the map and ID-card formats: provinces visited, districts of a city, "your Istanbul", dialect/word-usage quizzes that place you geographically.

**The sözlük ecosystem.** Ekşi Sözlük and its descendants have a public, textual, decades-deep corpus and a native status hierarchy (authorship, entry counts, seniority). Artifact-shaped in a way no Western platform quite matches.

**Turkish TV series.** The dizi ecosystem is huge domestically and internationally, and there is no Letterboxd-equivalent tracking culture for it. A watched-list grid, a season poster, a "your dizi taste" card — the audience exists and the tooling does not.

**Turkish music and its own canon.** The arabesk/rock/rap/pop generational divisions are strong status signals locally in a way the Spotify genre taxonomy completely flattens. Note the API problem, though — see below.

**Personal finance instruments.** Gold in lira, funds, deposit rates and currency are objects of intense national attention. Handle with care: people are fascinated by their own numbers and *will not post them*. The artifact must abstract to a badge, a rank, a "your year in gold" without amounts, or a purely hypothetical scenario. Also stay well clear of anything that reads as investment advice.

**Military service, generation markers, nostalgia.** "Which year were you 18" style generational artifacts work well and require no data at all. Military service is a shared reference for many but is politically and personally sensitive; treat as high-caution.

**Food and daily-life rituals.** Breakfast composition, tea consumption, kebab/pide regional loyalty, "your döner order says this about you" — light, high-share, zero data, zero risk. The weakest monetization but the fastest build.

## What data actually exists in Turkey

| Source | Access | Notes |
|---|---|---|
| Public sports data (fixtures, results, league tables) | Mostly public, some via commercial providers | Verify licence before commercial use; scraping a federation site is not the same as an open licence |
| Public exam and education statistics | Published by public bodies | Aggregate statistics are usually public; **individual results are not, and must never be obtained on a user's behalf** — the user supplying their own is the only acceptable path |
| Fund and instrument prices (TEFAS-type public platforms, exchange data) | Public price data; commercial redistribution often restricted | Check terms; delayed vs realtime matters |
| Municipal and government open data portals | Increasingly available | Quality varies wildly; check licence |
| Ekşi Sözlük and similar | Public web content | No official API; scraping raises both terms and copyright questions. Prefer user-supplied or aggregate-only approaches |
| e-Devlet | **Closed** | No third-party consumer integration path. Do not propose anything that touches it, and refuse requests to work around it |
| Open banking (BDDK/TCMB-regulated framework) | Licensed institutions only | The framework exists, but participation requires being a licensed payment/e-money institution. Out of reach for a side project — say so rather than gesturing at it |
| Trendyol / Hepsiburada / Getir / Yemeksepeti | No public consumer API | Any "your shopping year" idea depends on a user-supplied export or screenshot; verify whether these platforms actually provide a KVKK data export before promising it |
| Turkcell Fizy, local music services | No known public API | Verify |
| 1000Kitap and local reading communities | No known public API | User-supplied path only |

The recurring answer is "no API." That is precisely why Pattern A (user-supplied) and Pattern B (public data) from `03-data-sources.md` matter more in Turkey than they do in the US.

## Payment and monetization rails

- **App Store / Play** — local pricing tiers, and price points that Turkish users perceive very differently from the dollar equivalent. Consumer willingness to pay for a one-off cosmetic upgrade is low; expect conversion below Western benchmarks and model it that way.
- **Local payment providers** (iyzico, PayTR and similar) — the standard rails for web checkout, with local card support and instalment behaviour Turkish users expect. Instalments matter for anything above trivial pricing, including print products.
- **Display advertising** — the weak link. Turkish traffic RPM is *directionally* an order of magnitude below US traffic RPM, and this single fact invalidates most ad-funded plans aimed at a Turkish audience. Verify with current figures before quoting anything specific, but never let an ad-funded TR-only plan through the analysis without flagging it.
- **Print-on-demand and physical products** — genuinely viable locally. Poster, canvas, mug and sticker production is cheap and fast in Turkey, and the certificate/poster/receipt formats have a natural physical upsell. This is one of the few places where the TR market is *better* than the US one.
- **Brand sponsorship** — the strongest local model. A seasonal artifact with a predictable annual peak can be sold to a brand as a campaign asset months in advance. Turkish brands buy this kind of thing; see the model detail in `05-monetization-and-scoring.md`.

## KVKK

Turkish data protection law (Law 6698) is GDPR-adjacent but not identical. The practical points for this category:

- **Explicit consent (açık rıza)** is required for processing personal data outside the narrow legal bases. In practice, for an artifact app: a clear, specific, informed consent step before you touch anything personal — not a checkbox buried in a footer.
- **Stateless is the safe design.** Authorize → render → discard. If nothing is stored, most of the obligation surface disappears. Recommend this as the default architecture in every dossier where personal data is involved.
- **International transfer.** Sending Turkish users' personal data to servers abroad is a regulated transfer. The 2024 amendments introduced standard-contractual-clause style mechanisms alongside the older routes — verify the current requirements before designing anything that ships personal data to a US-hosted service. Another reason the stateless/on-device design wins.
- **VERBİS registration** obligations have exemption thresholds tied to headcount and financial size; small operators are often exempt, but the thresholds and the exemption conditions need checking against current rules rather than assumed.
- **Minors.** Anything aimed at the exam-season audience is aimed substantially at 17–18 year olds. That raises the bar on consent, tone, and data handling. Design it so no personal data is collected at all if you can.

None of this is legal advice and the dossier should say so; the point is to build in a way that doesn't create the problem in the first place.

## The Turkish seasonal calendar

Seasonal anchoring is the cheapest way to buy a recurrence pattern. Approximate windows — verify exact dates each year:

| Window | Event | Artifact fit |
|---|---|---|
| January | New year, winter transfer window | Year-ahead cards, transfer reaction artifacts |
| Feb–Mar | Ramazan (moves ~11 days earlier annually) | Habit/ritual artifacts, food, iftar-themed |
| April–May | Spring, national holidays, football title race | Nostalgia and identity cards |
| June | High-school and university entrance exams | Peak anxiety — support-toned, not judgement-toned |
| July | Exam results and university preference period | **The single biggest predictable artifact window in Turkey** |
| August | Public service exams, holidays, new football season | Vacation maps, season prediction cards |
| September | School starts, league underway | Back-to-school identity artifacts |
| October–November | National holiday, discount season | Brand-sponsorable windows |
| December | New year, global "wrapped" season | Year-in-review — but you are competing with everyone |

Note the strategic point: December is the most crowded window on earth for this genre. **July is nearly empty and is enormous in Turkey.** A well-built exam-season artifact has less competition and more attention than a December wrapped clone.

## Practical gotchas

- **Turkish characters in rendered images.** The font must contain ş, ğ, ı, İ, ç, ö, ü — many display faces do not, and the failure mode is boxes or silently dropped diacritics in the exported PNG. Test the export, not the browser preview.
- **The dotted/dotless I.** Locale-aware case conversion breaks Turkish strings in most languages by default (`"i".toUpperCase()` should be "İ", `"I".toLowerCase()` should be "ı"). This bites in name rendering and slug generation. Use locale-aware conversion or avoid case transforms entirely.
- **Name rendering.** Turkish names are long and vary in length dramatically; the artifact layout must handle both "Ali" and a four-part name without breaking.
- **Instagram Stories dominance.** For a Turkish audience, the 9:16 Story export matters at least as much as the X-format one. Build both.
- **X reach in Turkish.** Turkish-language posts reach a Turkish audience and essentially no one else. Global ambition means a bilingual artifact or two separate launches, not one post.
- **Screenshot culture.** A large share of Turkish users will screenshot rather than use a share button. The on-screen layout must be a good artifact on its own, with the wordmark visible in the screenshot region.

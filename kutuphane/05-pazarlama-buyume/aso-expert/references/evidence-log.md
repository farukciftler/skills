# Evidence log — check before quoting a number

ASO is unusually polluted with confident numbers that don't survive a source check. This file is the
blacklist and the caveat list. **Read it before putting any statistic into a client deliverable.**

Three tiers, and mark which one you're in:
- **Documented** — Apple / Google primary docs. State flatly.
- **Measured** — a study with disclosed methodology. **Always attach the date.**
- **Folklore** — vendor consensus, no published test. Say so.

---

## 1. Do not cite these

| Claim | Problem |
|---|---|
| **Any numeric ranking-factor weight** ("title is 40% of ranking") | **No such figures exist publicly for either store.** Every percentage split you have seen was invented |
| **"Average install rate 26.4%" and the associated category medians** | **2015 data**, ~300 experiments, still recycled in 2026 posts |
| **"Apple OCR-indexes screenshot caption text since June 2025"** | Failed a controlled test: 64 screenshot-derived phrases across 8 apps → 36 didn't rank, 27 explained by existing metadata, 1 unexplained. The real June 2025 event was a semantic/multi-intent search shift |
| **Any 2025/2026 statistic attributed to "data.ai"** | data.ai was absorbed into Sensor Tower in **March 2024** and no longer publishes. A citation to "data.ai 2026" marks the whole source as unreliable |
| Aggregator "100+ ASO statistics 2026" pages | Several top-ranking ones are AI-generated, cite defunct sources, attribute numbers to vendors that never published them, and contain internally contradictory figures. One claims Play re-indexes faster than iOS — contradicting every vendor source |
| **"Rank 1 = 34% install share, ranks 2–3 = 27%…"** | Unsourced aggregator distribution. Use the measured tap-through table in `keyword-research.md` §5 instead |
| **"Paid installs give a 1.3× or 1.5× organic multiplier"** | No published basis for any universal value. The one rigorous measurement is ≈**1.075×** (games, 2018–19 data). Teams bidding on 1.3× are overpaying |
| **"48% of installs now come from store search, 35–40% from social and AI"** | The source contradicts itself in the same article |
| **"72% of iOS sessions end without scrolling past the fold"** | Attributed to a vendor that never published it |

---

## 2. Cite, but with the caveat attached

| Claim | Caveat |
|---|---|
| **"Going from 3★ to 4★ is +89% conversion; 2★ to 3★ is +340%"** | Single **2015** survey, **n=350**, US-only, *stated preference not observed behaviour*, predates per-country ratings and AI review summaries. Use for the shape of the curve — cliff below 4.0, saturation above 4.5 — never as a forecast. The stronger argument is that **~95% of Apple-featured apps are rated 4.0+**, making rating a featuring gate |
| **"Apple CPPs lift conversion 156%"** | Apple **marketing** figure on a 1.6% impression-based denominator, and CPP traffic is intent-matched by construction. Vendor case studies: **+10% to +58%**; measured average ~**+5.9%** |
| **"Users decide in 7 seconds"** | ~2019–2021, and a competing figure says 10 s iOS / 14 s Play. Say "under 10 seconds, most in under 7" |
| **Search vs browse install split (Search 59% / referrals 20% / browse 12%)** | **2020 data**, App Store only. No comparable refresh exists, and **no public Play split exists at all**. Games differ structurally (referrals > search) |
| **Search Popularity → impressions formula** `254.4443 × e^(0.0615 × SP)` | **2019 data** — constants are stale. The durable parts are the **exponential shape** and the **~4-day lag** |
| **Apple Ads Popularity Index generally** | **Broke in Oct 2025** — scores 20–60 collapsed to the floor, ~77% of tracked keywords lost, no Apple announcement. A "5" now means "below disclosure threshold", not "low volume" |
| **"+0.7 stars from responding to a negative review"** | Genuinely Google's stated figure, but every current citation is secondary. Present it as "Google's stated figure" |
| **Landscape preview "A Closer Look" exposure ~13%** | ~2019 vendor data, pre-redesign. Directionally still true; don't quote the median as current |
| **Play app count −47% (3.4M → 1.8M)** | Well-corroborated, but one source says −38.2% to 2.1M, and the EU trader-status requirement (Feb 2025) is an unacknowledged confound |
| **Conversion benchmarks generally** | **Always state the denominator.** "8.56% App Store CVR" (impression-based, 2025) and "33.7% page-view-to-install" (2020) are different metrics, not a collapse |

---

## 3. Conflicting facts to verify in the console before writing copy

| Item | Conflict |
|---|---|
| iOS keyword field: **100 bytes vs 100 characters** | Apple's version-metadata reference says bytes; Apple's marketing page and all vendors say characters. Identical for Latin scripts; **check the App Store Connect counter for CJK/Cyrillic/Arabic** |
| **Promoted IAP description: 45 vs 55 chars** | Two Apple pages disagree. 45 is on the authoritative IAP page — verify in App Store Connect |
| Promoted IAP display name: 30 vs 35 vs 64 | The 64 figure is almost certainly the internal *reference* name |
| Play **release notes 500 chars**, **developer name ~50 chars** | Enforced/reported but not stated on a Google help page |
| Play SLE confidence levels (90/95/98/99%) and MDE range (0.5–6%) | Google confirms the settings exist; the exact selectable values are vendor-reported |
| Apple **PPO "one test at a time"** | On Apple's marketing page and vendor-confirmed; not stated in Apple's help overview |
| **US storefront secondary indexable locales** | The replicated finding is EN-US + ES-MX. One vendor table also lists Russian, Chinese, Arabic, French, Portuguese (BR), Vietnamese, Korean — almost certainly *display* languages, not search-indexed locales. **Do not promise a client eight extra keyword fields in the US** |
| **App Store Tags: ranking weight and rollout beyond US/en-US** | Apple positions Tags as a discovery surface; ranking weight is unstated. Wider rollout status unverified |
| **iOS description / developer name / IAP text / event text indexing** | Disputed among vendors; Apple is silent except on description and promotional text, where the answer is no. Treat description as **not indexed** |
| Play: **developer name indexed**, **in-app product names indexed**, **install velocity / uninstalls / update frequency as ranking factors** | All vendor inference; absent from Google's published factor list |
| Play rating visibility floors (**4.0 vs 3.0 stars**) | Different vendors, different surfaces, neither Google-confirmed |
| Play **12 testers / 14 days** rule | The 12/14 figures are current and documented; the date it dropped from 20 to 12 is not documented by Google |

---

## 4. Known gaps — say "we don't know" rather than filling them

1. No public 2024–2026 refresh of the App Store search-vs-browse install split with comparable
   methodology.
2. **No public Google Play search-vs-browse breakdown at all** from a primary source.
3. No vendor publishes its **visibility score** or **Play volume estimation** formula — cross-tool
   comparison is invalid; pick one vendor and treat the output as an index.
4. The exact Apple Ads popularity disclosure floor (35 vs 37) is unresolved.
5. Neither Apple nor Google documents its ranking algorithm or indexation timing — **every timing
   number in the industry is inferred from observation.**
6. **No RTL-specific conversion data exists** from any source.
7. No causal ranking factor for LLM app recommendations has been established, and no ROI figure for
   "AI visibility" work exists.
8. Neither store lets you **segment A/B test results by traffic source** — the biggest structural
   measurement weakness in store creative testing.

---

## 5. Two habits that keep this file from going stale

**Verify anything version-sensitive against the primary source.** Store mechanics changed materially
in 2025–2026: App Store Tags, CPP keywords and the 35→70 limit, Apple Ads popularity degradation,
multiple inline search ad slots (March 2026), the App Analytics overhaul (March 2026), fall-2026
Creative Assets, Play's Ask Play, AI review summaries, developer verification. **This reference is
current as of July 2026 and should itself be checked** when a client decision hinges on a specific
limit or a feature's availability.

**Prefer the client's own numbers to any benchmark.** A category benchmark tells you almost nothing
about one app; the same app's own funnel, month over month, tells you nearly everything. When you
must use a benchmark, it belongs in a sentence that begins "for context", not one that begins
"you should be at".

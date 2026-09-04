# Measurement, KPIs and attribution

## 1. The two stores' funnels are not comparable — say this in every deliverable

**App Store [Apple]:**
- **Impressions** — app viewed on Today/Games/Apps/Search tabs for **>1 second**. **Includes product
  page views.**
- **Product page views** — includes StoreKit-loaded pages inside other apps.
- **Conversion rate** = (total downloads + pre-orders) ÷ **unique device impressions**.
- **First-time downloads / redownloads / total downloads**; redownloads exclude auto-updates and
  device restores. Updates include auto-updates.

**Google Play [Google]:**
- **Store listing visitors** — users who visited the listing **who didn't already have the app
  installed on any device**. Counted once per day per dimension.
- **Store listing acquisitions** — visitors who installed and didn't have it on another device.
- **Conversion rate** = acquisitions ÷ visitors, both restricted to non-installers.

**Five independent reasons the numbers can't be compared:**
1. **Denominator** — Apple divides by impressions (including search cards never tapped); Google
   divides by page-level visitors. Apple's denominator is far larger, so Apple's CVR is structurally
   lower.
2. **Installed-user exclusion** — Google excludes existing users; Apple doesn't, and Apple's numerator
   includes redownloads.
3. **Uniqueness** — Apple counts unique *devices*; Google counts unique *users* (account, cross-device).
4. **Channel contamination** — **Play's "Google Play Search" acquisitions include Google Ads-driven
   installs**, so organic search volume moves with ads activity. Apple Ads traffic is broken out
   separately, but Apple's "App Store search" source *also* includes ads in search results.
5. **Apple's "install rate"** (downloads straight from search/browse with no page view) has **no Play
   equivalent at all**.

**Never put App Store CVR and Play CVR in the same chart or the same OKR.** Two KPIs, two targets,
and a footnote in every stakeholder deck.

## 2. Benchmarks — with denominators and dates attached

| Metric | App Store | Google Play | Source / date |
|---|---|---|---|
| Average CVR, US, all categories | **8.56%** | **16.15%** | vendor, 2025 data |
| Range by category | 5.2% (Games–Trivia) → 52.8% (Food & Drink) | 6.6% (Games–Strategy) → 62.3% (Auto & Vehicles) | vendor, 2025 |
| **Install rate** (direct from search/browse, no page view) | avg **3.8%**; 0.6% (Games–Board) → 7.8% (Medical) | n/a | vendor, 2025 |
| Page view → install | 33.7% | 26.4% | vendor, **2020** |
| Impression → install | 3.6% | — | vendor, **2020** |

⚠️ The 2025 "8.56%" and the 2020 "33.7%" are **different metrics, not a collapse** — impression-based
versus page-view-based. **Always state the denominator when quoting a conversion benchmark.** This is
the most common way ASO reporting misleads people.

**Directional truths that survive scrutiny:**
- **Play CVR is always higher than App Store CVR as measured** — that is arithmetic, not performance.
- **Search CVR >> browse CVR**, typically by 2–5×.
- **Referral/paid CVR is the most variable** and depends on creative-to-page match — hence CPPs.
- **Category variance dwarfs store variance.** Comparing a finance app to an "average app CVR" is
  meaningless.

⚠️ Check `evidence-log.md` before quoting any benchmark you didn't verify this session — several
widely circulating "2026 ASO statistics" are traceable to aggregator pages citing sources that no
longer publish.

## 3. Attributing an ASO change

**The core problem: ASO changes are not randomizable at the app level.** You cannot hold out a control
group for a metadata change.

Methods, ranked by rigor:

1. **On-store A/B test (Apple PPO / Play SLE)** — the only true randomization available, but limited
   to *creative* (Apple cannot test metadata at all), and constrained by 90-day / one-concurrent-test
   / fixed 90% confidence on Apple.
2. **Geo holdout** — ship the metadata change in a subset of storefronts, hold out matched ones.
   Requires comparable seasonality and no shared-language contamination. **The best available method
   for metadata changes.**
3. **Synthetic control / counterfactual forecasting** — fit a time-series model on pre-change data
   (changepoint detection, weekly and yearly seasonality, holidays) and compare actuals to the
   forecast with confidence intervals. Vendor implementations exist; the method is sound and the
   assumptions should be stated.
4. **Naive pre/post** — acceptable *only* with all of: whole-week comparison windows, year-over-year
   seasonality adjustment, paid spend held flat and annotated, no concurrent release or price change
   or PR event, minimum 14 days post, and a stated confounder list. Present it as an estimate with a
   range, never a point estimate.

**Hygiene that matters regardless of method:**
- **Annotate everything.** Keep a dated change log — metadata edits, releases, price changes, campaign
  starts, featuring, PR, competitor launches, OS releases — and overlay it on every chart. Most
  "unexplained" ASO movements are an unlogged event.
- **Change one thing at a time**, or accept that you cannot attribute.
- **Separate first-time downloads from redownloads.** A re-engagement campaign otherwise looks like
  ASO success.
- **Watch for store featuring**, which can dwarf any ASO effect and is invisible unless monitored.
- **Re-baseline against known inventory changes** — e.g. Apple's March 2026 addition of multiple
  inline search ad slots mechanically compresses organic impressions on terms where the app ranked #1.
  That is not a conversion regression.

## 4. Keyword rank is a leading indicator, not a KPI

The failure mode: reporting "we moved 200 keywords into the top 10" while installs are flat.

Correct hierarchy:
**keyword rank → impressions/visibility (rank × volume) → product page views by source → first-time
downloads (the actual KPI) → retained installs / D7 / LTV (the only thing that matters).**

Rules:
- **Weight rank by search volume.** Going from #40 to #8 on a floor-volume keyword is worth zero.
- **Split brand vs non-brand.** Brand terms rank #1 regardless of your work and mask everything else.
- Vendor "keyword downloads" estimates are **modelled, not measured** — fine for prioritization, not
  for reporting to stakeholders.
- Check ranks **daily, at the same time of day, per storefront and per device type** — ranks oscillate
  intraday.

## 5. Dashboard structure

- **Layer 1 — Funnel, per store, never blended.** Unique impressions → product page views →
  first-time downloads → CVR → install rate (Apple only). Split by source (Apple: Search / Browse /
  Referral; Play: Play Search / Play Explore / Ads & referrals) with a standing footnote that both
  stores' search buckets include ads.
- **Layer 2 — Visibility.** Keyword rankings weighted by volume, brand vs non-brand, category and
  overall chart rank, share of voice against a fixed competitor set, featuring events.
- **Layer 3 — Quality.** Rating per store and per key country (Play), rating trend, review volume and
  velocity, 1–2★ share, response rate and median response time, top review topics from the AI
  summaries, crash-free rate and Android vitals against Google's thresholds.
- **Layer 4 — Test log.** Every A/B test: variant, dates, traffic, MDE, confidence, result, shipped or
  not. The compounding asset most teams don't keep.
- **Layer 5 — Downstream.** D1/D7/D30 retention and ARPU **by acquisition source**, so you catch a CVR
  win that bought worse users.
- **Annotation layer** across all charts: releases, metadata changes, price changes, campaigns,
  featuring, incidents, competitor launches, OS releases.

## 6. The monthly stakeholder report — five items, one page

1. **First-time organic downloads per store**, versus prior month and versus the same month last year
   (seasonality-adjusted). The headline.
2. **CVR per store with the denominator spelled out**, and the delta attributed to specific shipped
   changes.
3. **What we tested and what we learned** — including losing tests. A losing test with a clean read is
   a result.
4. **Rating and review health**: rating per store, 1–2★ share, response rate, the **top three
   complaint themes appearing in the AI review summaries**, and what engineering is doing about them.
5. **Next month's test queue** with expected effect sizes and required sample.

Do **not** report: raw keyword-rank counts, impressions in isolation, blended cross-store CVR, or a
single-app comparison against an "industry benchmark".

## 7. Paid → organic uplift: what to tell a client who asks for a multiplier

**The directional claim is supported; a fixed multiplier is not.**

- A major MMP declined to publish a universal multiplier because *"it was not possible to release a
  number that would be statistically valid due to extreme variance"*, noting the metric conflates
  word-of-mouth, virality, store ranking effects and plain measurement gaps.
- The strongest public measurement — 6 mobile games, 2 OSes, 500 days, ~5,829 observations,
  difference-in-differences plus event studies **[measured, peer-reviewable, data 2018–19]** — found
  that when ad spend stopped, **organic installs fell 24%** (event-study range 18–30%), and that
  mobile app advertising is roughly **7.5% more effective than attribution alone suggests**
  (≈ **1.075×**).

**Practical stance:** reject any standing "1.3×" or "1.5×" organic multiplier — there is no published
basis for a universal value, and **teams bidding on a 1.3× assumption are systematically overpaying**
relative to the one rigorous measurement available. The multiplier is not a constant: it is largest
for apps near a chart-rank threshold, where paid volume mechanically buys organic placement, and near
zero for apps deep in the long tail. **The correct method is a spend-holdout geo test** — kill paid
spend in matched geos for 2–4 weeks and measure the organic delta against a synthetic control.

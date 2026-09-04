# Where to get live market data

Everything in this skill's other reference files has a date on it. This file is how you replace those dates with current ones.

## Contents
- [Free rankings and competitor lookup](#free-rankings-and-competitor-lookup)
- [Benchmark reports worth reading in full](#benchmark-reports-worth-reading-in-full)
- [Apple's own sources](#apples-own-sources)
- [Paid tools](#paid-tools)
- [Türkiye-specific lookups](#türkiye-specific-lookups)
- [Reading tracker data critically](#reading-tracker-data-critically)
- [Search patterns that work](#search-patterns-that-work)

---

## Free rankings and competitor lookup

| Source | Use for |
|---|---|
| **App Store itself** — charts by country and category, in the Apps tab | Ground truth for what ranks. Change storefront to check Türkiye |
| `apps.apple.com/tr/charts/` | Turkish storefront charts directly |
| **Appfigures** — appfigures.com, free tier | Rankings, estimated downloads/revenue, ASO data |
| **Sensor Tower top charts** — `app.sensortower.com/top-charts?country=TR&os=ios` | Free top charts by category and country |
| **Similarweb top apps** — `similarweb.com/top-apps/apple/turkey/` | Rankings by store and country |
| **AppBrain** — `appbrain.com/stats/appstore-rankings/` | Category rankings including Türkiye |
| **42matters** — `42matters.com/turkey-app-market-statistics` | Country app market statistics pages |
| **AppMagic** | Download and revenue estimates, often the source for "top apps of the year" lists |
| **A competitor's own App Store page** | Price, IAP tiers (visible in the listing), update cadence, rating count trajectory, review content |

**The single highest-value free research action** is reading the one- and two-star reviews of the top five apps in a target category. Nothing in any paid tool tells you what a paid tool can't: exactly what people who tried to pay for a solution found missing.

## Benchmark reports worth reading in full

| Report | Cadence | Why |
|---|---|---|
| **RevenueCat — State of Subscription Apps** | Annual, ~Jan–Apr | The most useful dataset for indie developers. App-level conversion, churn, RLTV, growth percentiles, broken out by category and region. Free. Has per-category editions (business, utilities, gaming, productivity, education). |
| **Sensor Tower — State of Mobile** | Annual, January | The headline market numbers most other coverage cites |
| **Business of Apps** — country and category data pages | Continuously updated | Country-level app market statistics including a Türkiye page |
| **Adjust** — market reports | Periodic | Has published Türkiye-specific mobile market analysis with install/session/retention data |
| **Apple's economic study** (Analysis Group) | Annual, ~June | The ecosystem billings figure. Read the methodology before citing |
| **Newzoo** | Annual | Games market specifically |

## Apple's own sources

- **Developer news** — `developer.apple.com/news/` — pricing changes, tax changes, policy updates. This is where FX and tax adjustments are announced.
- **Upcoming requirements** — `developer.apple.com/news/upcoming-requirements/` — deadlines.
- **App Store Connect** — your own analytics: impressions, product page views, conversion rate, downloads, proceeds, retention, and the crucial *source type* breakdown (search vs browse vs referral) that tells you whether ASO is actually working.
- **Small Business Program** — `developer.apple.com/app-store/small-business-program/`
- **Apple Newsroom** — `apple.com/newsroom/` — official figures with citable dates.

## Paid tools

Worth knowing they exist; rarely worth buying for a solo developer.

- **Sensor Tower** — the industry standard. Expensive.
- **data.ai** (formerly App Annie) — same tier.
- **Appfigures** — the most reasonable paid tier for an indie developer.
- **AppTweak / MobileAction / Sensor Tower ASO** — keyword-level ASO tooling.
- **Mirava, PricePush** — pricing intelligence and multi-storefront price management. Useful once you manage more than two apps across many countries.
- **RevenueCat** — subscription infrastructure with analytics attached; the analytics alone justify it for many.

## Türkiye-specific lookups

Turkish data is thin. Practical sources:

- Turkish storefront charts directly (`apps.apple.com/tr/charts/`)
- Business of Apps Türkiye page
- 42matters Türkiye statistics
- Adjust's Türkiye market reports
- Statista's Türkiye app market outlook (paywalled specifics)
- Turkish-language tech press for local ecosystem news — but be aware much Turkish-language "app market statistics" content recycles a 2018 App Annie report without dating it

**When Turkish data doesn't exist, say so** and reason from structure instead: Türkiye's position in Apple's price tiers, its download-heavy/revenue-light profile, and its regional peers.

## Reading tracker data critically

- **Estimates are estimates.** Sensor Tower, Appfigures and AppMagic disagree on the same app's revenue, sometimes by a factor of two. They model from rankings and sampled data; only the developer sees actuals.
- **Revenue estimates are usually gross**, before Apple's 30% or 15%. Check.
- **Download estimates skew low for apps with heavy non-search acquisition.**
- **Category rankings are storefront- and device-specific.** An iPhone chart and an iPad chart differ.
- **"Top grossing" excludes off-platform revenue.** A shopping app's actual business is invisible in these numbers.
- **Statista aggregates other people's forecasts.** Trace the underlying source before citing it as data.
- **Content-farm statistics pages** recycle each other, often without dates and sometimes with transcription errors. If a figure appears on five SEO sites and no primary source, treat it as unverified.

## Search patterns that work

For current figures:
- `"State of Subscription Apps" <current year> RevenueCat`
- `Sensor Tower State of Mobile <current year>`
- `App Store consumer spending <current year>`
- `<category> app revenue benchmark <current year>`

For a specific app or competitor:
- Its App Store listing directly — price and IAP tiers are visible there
- `<app name> revenue estimate appfigures` or `sensortower`
- `site:apps.apple.com <app name>` for the canonical listing

For Türkiye:
- `Turkey app market statistics <current year>`
- `Türkiye mobil uygulama pazarı <current year>`
- Apple's developer news for `Turkey` pricing announcements

For pricing and policy:
- `developer.apple.com/news` and search within
- `Apple App Store price tier <current year>`
- `<country> digital services tax App Store`

**Always append the current year.** Search engines return stale results heavily for market-statistics queries, and an undated figure from 2023 presented as current is exactly the failure this skill is built to avoid.

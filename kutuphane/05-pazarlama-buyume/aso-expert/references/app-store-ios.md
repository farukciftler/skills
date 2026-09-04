# Apple App Store — mechanics reference

Current as of **July 2026**. Sources are labelled: **[Apple]** = primary documentation,
**[measured]** = study with disclosed method, **[consensus]** = vendor agreement without a
published test, **⚠️** = conflicting or unverified.

**Contents**
1. Metadata fields and limits
2. What is indexed and what is not
3. Keyword field mechanics
4. Cross-localization (the biggest under-used lever)
5. Ranking factors
6. Custom Product Pages and Product Page Optimization
7. In-App Events, promoted IAPs, featuring
8. App Store Tags and semantic search
9. Apple Ads × organic
10. App Analytics — the metrics that matter
11. App Review metadata risk (Guideline 2.3.x)
12. 2025–2026 changes worth knowing

---

## 1. Metadata fields and limits

| Field | Limit | Editable without a new build? |
|---|---|---|
| App Name | **30 chars** (min 2) | No — version-bound |
| Subtitle | **30 chars** | No — version-bound |
| Keyword field | **100 chars**, comma-separated, no spaces after commas | No — version-bound |
| Promotional Text | **170 chars** | **Yes** — no review, no release |
| Description | **4,000 chars**, plain text | No |
| What's New | **4,000 chars** | No |
| Screenshots | up to **10 per device size per locale** | No |
| App Previews | up to **3 per device size per locale**, 15–30 s | No |
| In-App Event: name / short desc / long desc | **30 / 50 / 120** | Yes (own review) |
| Promoted IAP: display name / description | **30 / 45** ⚠️ Apple's own pages say 45 on the IAP page and 55 on the product-page article — verify in App Store Connect before writing copy | Yes (own review) |

**[Apple]** for all limits except where flagged.

⚠️ **"100 bytes" vs "100 characters".** Apple's version-metadata reference says the keyword field
is 100 *bytes*; Apple's marketing page and every vendor say 100 *characters*. Identical for Latin
scripts. For CJK / Cyrillic / Arabic locales, do not assume 100 UTF-8 bytes — check the counter in
App Store Connect. `scripts/keyword_field.py` reports both counts.

**Required screenshot sizes (2026):** iPhone **6.9"** (1320 × 2868 portrait) and, for iPad apps,
iPad **13"** (2064 × 2752). Everything else is optional and auto-scaled. **[Apple]**
Note two breaking changes: from **8 July 2026** screenshots may no longer contain alpha channels
or transparency, and app previews are capped at 30 fps / 500 MB.

**App preview display behaviour** — previews autoplay **muted** in both search results and on the
product page. A *portrait* preview takes gallery slot 1. A *landscape* preview takes over the whole
search-result row (no screenshots shown beside it) but gets demoted below the gallery on the product
page. Portrait is the default correct choice unless the app is landscape-native. **[Apple]**

---

## 2. What is indexed, and what is not

Apple's own statement: search results are based on **text relevance** — matched against **app name,
subtitle, keyword field, and primary category** — plus **user behaviour** (downloads, ratings and
reviews). Secondary category is also indexed. **[Apple]**

| Field | Indexed for search? |
|---|---|
| App Name | ✅ highest weight |
| Subtitle | ✅ second |
| Keyword field | ✅ |
| Primary + secondary category | ✅ |
| **Description (4,000)** | ❌ **No** |
| **Promotional Text (170)** | ❌ **No** — Apple states explicitly it "does not affect search ranking" |
| What's New | ❌ |
| Developer name | ⚠️ conflicting; most vendors say yes, Apple silent, low actionability |
| IAP names / descriptions | ⚠️ conflicting; promoted IAPs do appear as standalone search results |
| In-App Event text | ⚠️ conflicting; events definitely *appear* in search |
| Screenshot caption text (OCR) | ⚠️ **almost certainly not** — see below |
| CPP metadata | Only through assigned keywords |

**The description is not indexed on iOS.** This is the load-bearing asymmetry versus Google Play.
It still matters for conversion, and since 2025 it feeds Apple's LLM-generated Tags — but it earns
you no keyword rankings. Two vendors dissent; both also contradict Apple's explicit statement about
promotional text, which undermines them here.

**⚠️ The screenshot-OCR myth.** Several vendors claimed Apple began OCR-indexing screenshot caption
text around June 2025. A controlled test of **64 screenshot-derived phrases across 8 apps** found
36 didn't rank at all, 27 were fully explained by existing title/subtitle/keyword metadata, and
exactly 1 was unexplained. **[measured]** What people observed in June 2025 was the semantic-search
shift (§8), not OCR. Do not allocate keyword strategy on the assumption screenshots are indexed —
but do write strong captions, because conversion *is* a ranking input.

---

## 3. Keyword field mechanics

**Apple's stated rules [Apple]:**
- 100 characters, comma-separated, **no spaces after commas** (a space inside a multi-word phrase is
  fine). Apple's own example: `Property,House,Real Estate`
- Each keyword must be **more than 2 characters**
- No app or company names; no trademarked terms, celebrity names, competing app names
- No plurals of words you already have — Apple calls "climb" and "climbs" duplicates
- No generic terms ("app", "game"), no stop words ("the", "to"), no special characters
- *"Apple may modify inappropriate keywords at any time"*

**Plurals are handled automatically.** Never spend characters on them. **[Apple]**

**Cross-field permutation.** The algorithm combines individual words across title + subtitle +
keyword field into multi-word queries. Entering `habit,tracker,daily` makes you eligible for
"habit tracker", "daily habit", "daily tracker". **So enter single words, never phrases.**
**[consensus, strong]**

**The hard constraint:** permutation happens **within a locale, not across locales**. If "bus" is
only in your English (US) metadata and "metro" only in Spanish (Mexico), you can rank for each
alone in the US storefront but will not be indexed for "metro bus". **[consensus, well-replicated]**

**Repetition does not stack.** A word indexed once is indexed. Repeating it in title *and* keyword
field buys nothing and wastes budget. **[consensus, strong]**

**Free — do not spend characters on these:** your category name, the word "app", plurals of anything
you have, and every word already in your name or subtitle.

**Tactical:** use digits not words ("3" not "three"); avoid "free" and other terms that can become
inaccurate; fill all 100 characters — unused budget is pure loss.

Effective indexable budget per locale: **160 characters** (30 name + 30 subtitle + 100 keywords).

---

## 4. Cross-localization

Each App Store storefront indexes keywords from **two or more locales simultaneously**. Populating
a secondary locale roughly **doubles your indexable budget in that storefront** — +160 characters —
without touching the primary locale's user-visible copy.

**The highest-leverage facts:**
- **English (U.K.) is the secondary indexable locale in the overwhelming majority of non-English
  storefronts.** Filling EN-GB metadata is the single best cross-localization move for a global app.
- **Japan's secondary is English (U.S.), not English (U.K.)** — an EN-GB-only strategy gets nothing
  there.
- **English (Australia)** is the secondary for the **UK** storefront (and primary for AU/NZ).
- **Denmark and Finland default to English (U.K.) as primary**; Danish/Finnish are secondary.
- **US = English (U.S.) + Spanish (Mexico).** ⚠️ One vendor table also lists Russian, Chinese,
  Arabic, French, Portuguese (BR), Vietnamese and Korean as US locales. These are almost certainly
  *display* languages, not additional *search-indexed* locales. Do not promise a client eight extra
  keyword fields in the US. Optimize EN-US + ES-MX; treat the rest as unverified.

| Storefront | Primary | Secondary indexable |
|---|---|---|
| United States | English (U.S.) | Spanish (Mexico) |
| United Kingdom | English (U.K.) | English (Australia) |
| Canada | English (Canada) | French (Canada) |
| Japan | Japanese | **English (U.S.)** |
| Germany / Austria / France / Brazil / China / Taiwan / Korea / India / Netherlands / Italy / Poland / most of Europe and Asia | Local language | English (U.K.) |
| Spain | Spanish (Spain) | English (U.K.), Catalan |
| Mexico + most of LATAM | Spanish (Mexico) | English (U.K.) |
| Turkey | Turkish | English (U.K.), French |
| Switzerland | German | English (U.K.), French, Italian |
| UAE / Saudi / Gulf | Arabic | English (U.K.) |
| Egypt / Maghreb / Lebanon | Arabic | French, English (U.K.) |
| Russia | Russian | English (U.K.), Ukrainian |
| Ukraine | Ukrainian | Russian, English (U.K.) |
| Hong Kong | Chinese (Traditional) | English (U.K.), Cantonese |
| Israel | Hebrew | English (U.K.) |
| Cyprus | English (U.K.) | Greek, Turkish |
| Belgium | English (U.K.) | French, Dutch |
| Denmark / Finland | **English (U.K.)** | Danish / Finnish |

**[consensus, well-replicated]** — Apple does not publish this map; it is reverse-engineered by
vendors and has held stable for years.

**The "localization hack":** put overflow *English* keywords into the Spanish (Mexico) keyword
field, which is indexed in the US storefront. Nets +100 indexable characters in the US with no
Spanish keyword research. Keep title and subtitle genuinely localized — they are user-visible and
drive conversion for Spanish-speaking US users; only the invisible keyword field carries the overflow.
⚠️ Apple reportedly frowns on this; no rejections have been publicised. It is a documented gray zone,
low risk in the invisible keyword field, genuine 2.3.7 risk if done in a visible title or subtitle.
Present it to the client as a choice, not a default.

Apple supports roughly **48–50 App Store localizations**; 11 were added on 30 March 2026 (Bangla,
Gujarati, Kannada, Malayalam, Marathi, Odia, Punjabi, Slovenian, Tamil, Telugu, Urdu) — net-new
keyword real estate for India-heavy portfolios. **[Apple]**

---

## 5. Ranking factors

Apple's model, in Apple's own framing: **text relevance × user behaviour**. **[Apple]**

**Field weight order: Title > Subtitle > Keyword field.** Unanimous vendor consensus.
⚠️ **No numeric weights exist publicly for either store.** Any percentage split is fabricated.

Behavioural factors, in rough order of claimed impact **[consensus]**:

| Factor | Notes |
|---|---|
| **Download velocity** | A surge in a short window, not the cumulative total |
| **Conversion rate** (impression → install) | High; also the mechanism by which creative work affects ranking |
| **Ratings & reviews** | Recency and velocity appear to matter more than the absolute score. Apps rated >4.5★ reportedly get ~3× more installs — vendor figure, uncontrolled |
| **Retention / app quality** | Rising in importance. ⚠️ The D1 >35% / D7 >15% benchmarks widely quoted for iOS are originally *Google Play* benchmarks |
| **Update cadence** | Median gap between updates for top free apps ≈ 18 days; ~74% of top-1,000 iOS apps update monthly |
| **In-app event cadence** | Apps publishing 2–4 events/month reportedly earn more organic impressions — ⚠️ methodology undisclosed |
| **Uninstalls** | ⚠️ Apple has the signal (deletions appear in App Analytics) but no confirmed ranking use |

---

## 6. Custom Product Pages and Product Page Optimization

### Custom Product Pages (CPP)

- **Limit: 70 per app** (doubled from 35 on **29 October 2025**). **[Apple]**
- Customizable per CPP: **screenshots (10), app previews (3), promotional text (170), assigned
  keywords, deep link (iOS 18+), localizations.**
- **Not** customizable: app name, subtitle, icon, description, price, category, ratings.
- No app update / binary required. Visible to iOS 15+. Editing keeps the same URL. A disabled or
  deleted CPP redirects to the default page.
- URL form: `https://apps.apple.com/us/app/name/id123456?ppid=<uuid>`; StoreKit equivalent is
  `customProductPageIdentifier`.

**CPPs are now organically searchable — the biggest structural change to iOS ASO in years.** Assign
keywords to a CPP and, when your app ranks for those keywords, Apple serves that CPP *instead of*
your default product page. **[Apple, WWDC25]** The operating rules:

- Keywords must come **from your existing approved keyword field**. This *allocates* your 100
  characters; it does not give you more.
- **Each page needs a unique keyword set** — overlap is disallowed, so no cannibalization.
- Apple states that **assigning keywords alone does not require App Review**; changing creative does.
  ⚠️ Some vendors claim every CPP change needs review — the reconciliation above is Apple's own.

⚠️ Apple's headline "+156% conversion" for CPPs is a marketing figure on a 1.6% impression-based
base, and CPP traffic is intent-matched by construction. Vendor case studies land at **+10% to +58%**;
Phiture reports an average **+5.9%**. Plan against the vendor range, not Apple's.

### Product Page Optimization (PPO)

| Parameter | Value **[Apple]** |
|---|---|
| Treatments | up to **3** vs the original |
| Concurrent tests | **one at a time** per app |
| Max duration | **90 days** |
| Traffic | you choose the % entering the test; split evenly across treatments |
| Testable | **icon, screenshots, app previews** — nothing else. No metadata testing at all |
| Audience | iOS/iPadOS **15+** |
| Not supported on | Custom Product Pages, Watch, iMessage pages |

**Icon tests require the alternate icons to already be in the shipped binary** (asset catalog,
1024×1024, Xcode 13+) — so icon tests are gated on a release cycle, while screenshot and preview
tests are not. A user who installs from an icon-treatment page keeps that icon on their home screen.

**PPO is Bayesian.** Apple reports conversion rate, estimated relative improvement, confidence, and
a credible interval, updated daily. "Performing Better/Worse" requires **≥90% confidence**; there
is also a "Likely to be Inconclusive" projection and a **5 first-time-download** display floor. The
baseline can be promoted at any time, which is the intended sequential workflow.

⚠️ **90% is a loose bar** — roughly a 1-in-10 false-positive rate per conclusive call, and Apple
documents no multiplicity correction for 3-treatment tests. Treat a bare 90–95% call on a
3-treatment test as directional. Also: results are **aggregated across all selected localizations**
and cannot be decomposed — run one test per locale if the locales matter, and remember that markets
without their own localization fall back to your primary language and get silently absorbed.

Shipping an app version mid-test can corrupt results if it touches assets under test. **[Apple]**

---

## 7. In-App Events, promoted IAPs, featuring

**In-App Events [Apple]:** 15 approved in App Store Connect at a time, **10 published
simultaneously**, up to **31 days** duration, publishable up to **14 days** before start, minimum 15
minutes. Fields: name 30 / short description 50 / long description 120. Event card 16:9 (min
1920×1080); details page 9:16. Badges: Challenge, Competition, Live Event, Major Update, New Season,
Premiere, Special Event — plus In-Game Offer, Now On Sale, Try Before You Buy for the Apple Games app
(summer 2026, US first). Events surface in **search results and the Today/Games/Apps tabs**, and users
can search for events directly. Guideline **2.3.13** requires event metadata to describe the *event*,
not the app.

Underused levers: per-region dates, **event priority** (controls product-page ordering), and **event
purpose** targeting (attract new users / inform active users / bring back lapsed users).

**Promoted In-App Purchases [Apple]:** up to **20** shown on the product page; they appear in search
results and can be featured. **Consumables do not appear in search results.** Promotional image
1024×1024 — keep the lower-left corner clear, the app icon is framed there.

**Featuring [Apple]:** nominations go through the **Featuring Nominations** form in App Store Connect
(not email), **minimum 2 weeks** lead time, ideally up to 3 months. Apple's stated editorial criteria
include user experience, UI craft, innovation, uniqueness, **accessibility**, **localization quality**
— and explicitly **product page quality**. Note the second-order payoff: creative work is a documented
input to editorial selection. Roughly 95% of Apple-featured apps are rated 4.0+ and 65% are 4.6+
**[measured, 2025 data]** — rating is effectively a featuring gate.

---

## 8. App Store Tags and semantic search

**App Store Tags** — live in App Store Connect since **16 July 2025**, user-visible on iOS 26 (US /
en-US at launch; ⚠️ wider rollout status unverified). Short descriptive labels rendered as tappable
links on product pages and in search results; tapping opens a curated "tag room".

Apple's own words: tags are *"generated by our large language models using a range of data sources,
including your app's metadata"*, and are **human reviewed**. You **cannot create custom tags** — you
can view them on the App Information page and **deselect** ones you don't want, which removes that
association across the App Store. **[Apple, WWDC25]**

Two consequences worth telling clients:
- **Your description now matters for discovery for the first time**, indirectly, as LLM input to tag
  generation — even though it is still not keyword-indexed.
- Removing tags reduces visibility. Tag-driven traffic reports as **Search** when the tag is used as
  a query and **Browse** when reached by browsing.
- ⚠️ Whether tags carry *ranking* weight is unverified; Apple positions them as a discovery surface.

**Semantic / natural-language search.** iOS 18.1 (Oct 2024) introduced natural-language App Store
search; Apple's guidance now tells users they can use everyday language. A further shift on
**5–6 June 2025** had the US storefront start interpreting a single query as multiple intents.
**[measured, vendor]** Confirmed active in English-language storefronts; non-English markets showed
no significant change at time of testing. ⚠️ Vendor testing, not an Apple statement.

Strategic read: **semantic clustering beats isolated keyword targeting**, long-tail conversational
phrasing gains value, large apps benefit disproportionately (one game gained 4,500+ keywords, +76%,
post-rollout), and keyword stuffing is punished harder because relevance evaluation improved.

---

## 9. Apple Ads × organic

Apple Search Ads was renamed **Apple Ads** in April 2025. Four App Store placements: **Today tab**
(CPP required), **Search tab** (pre-query), **Search results** (the only keyword-targeted one), and
**Product pages** (default assets only, no variations). **[Apple]**

**March 2026: multiple inline search-results slots.** Apple ended the single top-of-search slot;
ads can now appear at the top *and further down* results. Rolled out UK 3 March 2026, all markets by
end of March 2026, iOS 26.2+. Active campaigns were auto-enrolled; advertisers cannot choose a slot.
**Practical consequence for ASO reporting: organic impressions on terms where the client ranked #1
mechanically compress.** Re-baseline organic KPIs to Q2 2026 or the team will misdiagnose an
inventory change as a conversion regression.

**Do paid installs lift organic rank?** Apple has never confirmed it and no rigorous public study
exists. The plausible mechanism is download velocity, which is an accepted ranking signal — but only
for terms already in your metadata. The old folklore about an automatic boost to organic positions
8–10 is dead. Treat this as a defensible working hypothesis, **not a documented fact**.

**Keyword harvesting is the reliable, uncontroversial win:** run a broad-match Discovery campaign
with Search Match → read real user queries from the Search Terms report → promote validated terms to
exact match, add them as negatives in Discovery → feed high-tap-through terms into title/subtitle and
high-conversion terms into the keyword field and CPP assignments.

⚠️ **Apple Ads Popularity data degraded in October 2025.** Keywords previously scoring 20–60 dropped
to the floor value; one tracker measured its pool falling from 165,875 to 39,254 terms in four days
(~77%), across all markets, with no Apple announcement. The practical disclosure floor now sits in
the mid-30s. **A score of 5 no longer means "low volume" — it means "below Apple's disclosure
threshold."** Do not auto-discard 5s; cross-check against autocomplete presence and App Store Connect
impressions. Apple's replacement is the **Monthly Search Term Rank Report** (Apple Ads → Reports →
Insights, beta since Oct 2025) — monthly refresh, genre-relative 1–100 popularity that **does not
correlate with the legacy 1–5 metric**, and reportedly only surfaces terms above ~35.

---

## 10. App Analytics — the metrics that matter

Apple's exact definitions **[Apple]** — these trip people up:

- **Impressions** — times the app was viewed on the Today/Games/Apps/Search tabs **for more than one
  second**. **Includes product page views.** Never compute "impressions − page views = didn't click".
- **Product Page Views** — includes StoreKit-loaded pages inside other apps.
- **Conversion Rate** — **total downloads and pre-orders ÷ unique device impressions**. Note the
  denominator: impressions, not page views. This is why Apple's CVR is structurally lower than Play's.
- **Redownloads** — excludes auto-updates and device restores.
- **Updates** — includes auto-updates, so it is useless as a demand proxy.
- Metrics only appear after **≥5 first-time downloads**.

**Acquisition source types:** App Store search (**includes ads in search results** — organic and paid
are blended unless you cross-reference Apple Ads), App Store browse, App referrer, Web referrer, App
Clip, Institutional Purchase, Unavailable.

**March 2026 overhaul:** 100+ new metrics, **cohort analysis** (by download date, download source,
offer start date), peer benchmarking including **download-to-paid conversion** and **proceeds per
download** (differential privacy), two new subscription reports, up to **7 simultaneous filters**.
The **Analytics Reports API** is the only sane way to run ASO reporting at scale — the UI is not
exportable at useful granularity.

**The ASO manager's short list:** impressions by source type; impressions → page views (the
*pre-page* creative test — this is where icon and search-card wins appear); page views → first-time
downloads (the *on-page* test); Apple's own conversion rate; first-time vs redownloads reported
separately; per-CPP performance; the PPO panel; peer benchmarks; ratings volume and average; the
Search Term Rank Report.

---

## 11. App Review metadata risk — Guideline 2.3.x

Verbatim from the App Review Guidelines **[Apple]**:

- **2.3.7** — *"Choose a unique app name, assign keywords that accurately describe your app, and
  don't try to pack any of your metadata with trademarked terms, popular app names, pricing
  information, or other irrelevant phrases just to game the system… Metadata such as app names,
  subtitles, screenshots, and previews should not include prices, terms, or descriptions that are not
  specific to the metadata type… Apple may modify inappropriate keywords at any time."*
- **2.3.1** — no hidden features; new features must be described **with specificity** in Notes for
  Review — *"generic descriptions will be rejected."*
- **2.3.2** — description and screenshots must clearly indicate what requires an in-app purchase.
- **2.3.3** — screenshots must **show the app in use**, not a title screen, login, or splash. Text
  and image overlays are allowed.
- **2.3.4** — previews may only use **video screen captures of the app itself**.
- **2.3.8** — all metadata must meet a **4+ age rating** regardless of the app's rating; **"For Kids"
  is reserved for the Kids Category**; icon variants must be similar.
- **2.3.10** — **no names, icons or imagery of other mobile platforms or alternative marketplaces**.
- **2.3.12** — "What's New" must describe actual changes; generic text only for pure bug fixes.
- **2.3.13** — in-app event metadata must pertain to the event.
- **4.1(c)** — no other developer's icon, brand or product name in your icon or name.

**Risk ranking for tactics clients ask about:**

| Tactic | Risk |
|---|---|
| Competitor brand in **title or subtitle** | **High** — 2.3.7 + 4.1(c) |
| Competitor brand in **keyword field** | **Medium** — explicitly against 2.3.7, but invisible; Apple may silently strip |
| Keyword-stuffed subtitle | **High** |
| "Free" / "50% Off" in name or subtitle | **High** — explicit |
| "For Kids" outside Kids Category | **High** — explicit |
| Android / Play / alt-marketplace mentions | **High** — explicit |
| English keywords in the ES-MX keyword field | **Low–Medium** — gray zone, no publicised rejections |
| Screenshots showing only splash/login | **Medium** — 2.3.3 |
| Generic Notes for Review | **High** — 2.3.1 says they will be rejected |

---

## 12. 2025–2026 changes worth knowing

- **App Store Tags** (Jul 2025) — LLM-generated from your metadata, human-reviewed, deselectable.
- **CPP keywords → organic search** (2025) and **CPP limit 35 → 70** (29 Oct 2025).
- **Age ratings overhaul** — new 13+ / 16+ / 18+ tiers; questionnaire deadline **31 Jan 2026** has
  passed, unanswered apps are blocked from submitting updates. Further 2026 changes: Australia 15+ →
  16+, Vietnam rating system added, and from **July 2026 social-media capability must be declared** —
  a **Social Media content descriptor appears on the product page**, with CVR implications, and social
  features force a 13+ minimum unless disabled for under-13s via the Declared Age Range API.
- **AI review summaries** — shipped iOS 18.4, refreshed at least weekly, expanding beyond US English.
  Developers can report concerns via App Store Connect. This is uneditable copy above the fold: your
  recurring complaint themes are now *promoted*, so fixing the top three has a direct CVR effect.
- **Accessibility Nutrition Labels** — new product-page section.
- **March 2026 App Analytics overhaul** (§10) and **March 2026 multiple search ad slots** (§9).
- **Fall 2026 — Creative Assets and Asset Library.** A new asset class (rich images and video)
  separate from screenshots, usable in product page headers, **organic search results**, CPPs, PPO
  tests and Apple Ads; plus a central Asset Library where creative can be **pre-approved independently
  of app submissions**. This decouples creative iteration from release cycles and puts video into
  organic search results for the first time. Also: **Product Page Preview** tool, **Personalized
  Collections** (a new algorithmic browse surface), and grouped submissions.
- **iOS 26 / Apple Games app** — auto-installs, pulls existing assets (no new creative needed),
  search inside it is organic-only, and games with active events can surface twice. Apps shipping
  updated Icon Composer layered icons get priority featuring in special collections.
- **EU DMA** — alternative marketplaces and web distribution mean a growing share of EU installs
  bypass the App Store entirely. Installation sheets for alternatively-distributed apps show only
  name, developer, description, screenshots, age rating — **your keyword field, subtitle and tags do
  nothing there.** In the EU, ASO is now a multi-channel problem.
- **Apple 2025 fraud enforcement** (published May 2026): ~195M fraudulent reviews blocked out of 1.3B
  processed, 193,000 developer accounts terminated. Relevant when a client asks about buying reviews.

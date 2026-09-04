# Google Play — mechanics reference

Current as of **July 2026**. **[Google]** = primary documentation, **[measured]** = study with
disclosed method, **[consensus]** = vendor agreement without a published test, **⚠️** = conflicting
or unverified.

**Contents**
1. Store listing fields and limits
2. What Play indexes
3. Keyword mechanics in the long description
4. Policy — what gets you rejected or removed
5. Tags
6. Custom Store Listings
7. Store Listing Experiments
8. Ranking factors and Android vitals
9. Play Console metrics
10. 2025–2026 changes

---

## 1. Store listing fields and limits

| Field | Limit **[Google]** |
|---|---|
| App name (title) | **30 characters** |
| Short description | **80 characters** |
| Full (long) description | **4,000 characters** |
| Release notes ("What's new") | **500 characters** per language ⚠️ enforced in Console, not stated on a Google help page |
| Developer name | ⚠️ **no published limit**; ~50 chars is vendor lore |
| Tags | **maximum 5** |

Google states explicitly: *"Character limits apply to both full-width and half-width characters."*
A 30-character Japanese or Turkish title gets 30 glyphs — not half.

**Graphic assets [Google]:**

| Asset | Spec |
|---|---|
| Icon | 512 × 512, **32-bit PNG with alpha**, ≤1,024 KB |
| Feature graphic | 1024 × 500, JPEG or 24-bit PNG (no alpha) — **required to publish**; also the video cover |
| Screenshots | **min 2**, **max 8 per device type**; 320–3,840 px per side; max side ≤ 2× min side; no alpha. Recommend ≥1080 px, 4+ for apps / 3+ for games |
| Preview video | **YouTube URL only**, public or unlisted, **ads must be disabled** or it won't show; autoplays up to 30 s |
| TV banner | 1280 × 720 |

Independent screenshot slots per device type: phone, 7" tablet, 10" tablet, Chromebook, Android TV,
Wear OS, Automotive, XR.

Categories: 30+ app categories, 16 game categories, maintained as separate lists.

---

## 2. What Play indexes

⚠️ **Google has never published field weights.** The ordering below is strong vendor consensus with
zero primary confirmation — present it as such.

| Field | Indexed | Claimed weight |
|---|---|---|
| **Title (30)** | ✅ | Highest |
| **Short description (80)** | ✅ | Second — and highly visible in results |
| **Long description (4,000)** | ✅ | Third — functions like on-page SEO body copy |
| Developer name | ⚠️ conflicting — Google calls it "helpful for users to find your app", which is a discoverability statement, not an indexing confirmation |
| Package / bundle ID | Indexed, but impact described as "minimal and not reliable" |
| In-app product names | ⚠️ no evidence either way |
| **User reviews** | ✅ **empirically demonstrated** — see below |
| Tags | Categorization and browse, **not keyword search** |

**Reviews are indexed on Google Play — this is measured, not folklore.** A controlled experiment
using apps with zero prior indexing for a target keyword found: indexing appeared in **2–3 days**;
**extended reviews (100+ characters) indexed 48% of the time (16/33)**; **short reviews (≤5 words)
indexed 0% of the time (0/10)**; branded terms 55%; a **single review** was enough to trigger
indexing across 21 distinct terms regardless of the app's total review volume. **Developer replies
are also indexed.** The same test found **zero indexing on the App Store** — this is Play-specific.
**[measured]**

The legitimate applications: mine review language for keyword discovery, and use **developer replies**
— which you control and which are indexed — to reinforce natural vocabulary. Manufacturing reviews
violates Google's policy and the effect is low-position indexing anyway, not a ranking shortcut.

**The asymmetry to state in every cross-store deliverable:** the long description is a *ranking input*
on Play and *not indexed at all* on iOS. The same description cannot be optimal for both.

---

## 3. Keyword mechanics in the long description

**The "repeat 3–5 times" rule is vendor convention, not a Google rule.** ⚠️

Vendor guidance: primary keywords 3–5×, secondary 1–3× each, overall density ~2–3% (one vendor caps
at 4–5%). Another major vendor deliberately publishes no numbers and warns stuffing is penalized.

**Google's own position runs against the spirit of density targets [Google]:** *"use everyday
language, not a list of keywords"*, and no *"repetitive, excessive, or irrelevant word blocks"*.
Google's verbatim example of what **not** to do:

> *"Car racing, car driving, race cars, car races, race track, driving, drive, race, cars, vehicles,
> automobiles, trucks"*

**Practical read:** 3–5 repetitions is a safe operating heuristic because it stays below the visible
spam threshold, not because Google rewards that count. No published experiment isolates repetition
count from confounders. Treat density targets as guardrails against stuffing, not as a lever.

**Semantics.** Vendors state Play uses semantic indexing and NLP to understand context and synonyms.
⚠️ Google has published no architecture statement — but the *confirmed* semantic layer is Guided
Search (Sept 2025) and **Ask Play** (I/O 2026), which Google describes as generative and
context-understanding. **[Google]** The strategic implication both major vendors converge on: keyword
rank is now a relevance signal rather than a traffic guarantee, and the unit of optimization is
**semantic coverage across intent clusters**, not individual keyword positions.

---

## 4. Policy — what gets you rejected or removed

**Store Listing and Promotion policy [Google]** prohibits *"misleading, improperly formatted,
non-descriptive, irrelevant, excessive, or inappropriate metadata"* across description, developer
name, title, icon, screenshots and promo images.

Hard rules:
- **Title**: max 30 chars, **no emoji**, no repeated special characters, **no ALL CAPS** unless it's
  the brand.
- **No store-performance claims anywhere**: "#1", "App of the Year", "Best of Play", "Editor's
  Choice", "New".
- **No pricing or promotional text** in title, icon, developer name, or feature graphic ("10% off",
  "free for a limited time").
- **Developer name**: no emoji, no repeated special characters, no performance/pricing signals.
- **Descriptions**: no unattributed or anonymous testimonials.

Enforcement runs rejection → removal → suspension → account termination. Note this is **policy**
enforcement, not a documented algorithmic ranking demotion — Google has never described a
keyword-stuffing ranking penalty on Play.

**Ratings and reviews policy [Google]:** no incentive of any kind in exchange for a rating or review;
no fake or sock-puppet reviews; **no forced or intrusive pop-ups** pressuring a rating; no automated
inflation. Enforcement is usually silent — reviews are removed or the listing is suppressed without
notification. You may incentivize *feedback* (surveys, support contact); you may never incentivize
*store ratings*, and neither store permits a sentiment gate ("do you like the app?" before the prompt).

---

## 5. Tags

- **Maximum 5 per app.** Separate pools for apps and games; accessibility tags exist. **[Google]**
- They drive **categorization, browse surfaces, collections and similar-app recommendations** — not
  keyword search. No source claims tags affect keyword rankings.
- Google advises changing tags *"only if you make significant changes to the content or functionality
  of your app"* — frequent churn is discouraged.
- The relevance bar: a tag's relevance must be *"very clear to a user who is unfamiliar with the
  app"*. Tangential tags chosen to poach an adjacent audience are explicitly discouraged.

---

## 6. Custom Store Listings (CSL)

**Limit: 50 per app**, across all types. (The widely cited "5" is obsolete.) **[Google]**

Targeting types:

| Type | Mechanics |
|---|---|
| Country / region | One listing can target many countries, but **each country maps to only one CSL** |
| Pre-registration | Different listing where the app is in pre-registration |
| Inactive users | Installed >28 days ago and unused for 28 days, or uninstalled |
| Google Ads campaigns | By ad group ID |
| Custom URL parameter | `…details?id=<pkg>&listing=<param>` — for influencer, email, partnership traffic |
| **Play Search keywords** | Route searchers on specific keywords to a matching CSL; supports variations and spelling corrections |

**Critical distinction:** keyword-targeted CSLs change **what the user sees after arriving from
search**; they do **not** change where you rank. Don't build one CSL per keyword — group queries by
**intent theme** so each listing gets enough traffic to read.

Google I/O 2026 added **one-click CSL creation from keyword recommendations** in Play Console, plus
Gemini-powered AI translation for listings. **[Google]**

---

## 7. Store Listing Experiments (SLE)

Live and maintained in 2026. Path: **Grow users → Store listing experiments**. **[Google]**

**Two types:**
1. **Default graphics** — visual assets only, in the default language, shown to users without a
   localized listing.
2. **Localized** — graphics **and text**, in up to **5 languages at once**.

| Asset | Default graphics | Localized |
|---|---|---|
| Icon, feature graphic, screenshots, video | ✅ | ✅ |
| Short description | ❌ | ✅ |
| Long description | ❌ | ✅ |
| **App title** | ❌ | ❌ — **cannot be A/B tested natively** |

**Mechanics:** up to **3 variants + control**; traffic splits **evenly** within the audience
percentage you set (30% audience, 2 variants = 15% each). Concurrency: **1 default-graphics
experiment**, up to **5 localized experiments** at once.

**Metric choice — the most misunderstood parameter:** *first-time installers* or ***retained
first-time installers*** (Google's recommendation), where "retained" means kept installed for **at
least 1 day** — not 7, not 30. First-time installers over-rewards creative that wins the click but
not the user; retained requires a substantially larger sample. Low-volume apps are often forced onto
the weaker metric, which is a real limitation to state to the client.

**Statistics:** configurable confidence and minimum detectable effect, plus a duration calculator.
⚠️ Vendor-reported selectable values: confidence 90 / 95 / 98 / 99%, MDE 0.5–6%. Use **95% + retained
installers** where traffic allows.

**Known pitfalls:** peeking and stopping the moment a variant crosses the line inflates false
positives — set confidence and MDE before launch and leave them alone; **minimum 7 days** to cover a
full weekday/weekend cycle; **no revenue tracking and no traffic-source segmentation**, so you cannot
tell whether a win came from search or browse traffic, which frequently reverse each other.

---

## 8. Ranking factors and Android vitals

**What Google actually states [Google]** — only four things: **user relevance** (query or browse
context), **app quality** (*"apps that have strong technical performance and a good user experience
are generally favored"*), **editorial value**, and **advertising**. Google also confirms it analyzes
ratings, reviews and engagement. Google does **not** publish install velocity, uninstall rate or
update frequency as named ranking factors — those are vendor inferences.

**Android vitals — the one hard documented threshold set [Google].** Evaluated over the most recent
28 days:

| Metric | Overall bad-behaviour threshold | Per-device-model |
|---|---|---|
| User-perceived crash rate | **≥ 1.09%** of daily users | ≥ 8% on a single model |
| User-perceived ANR rate | **≥ 0.47%** of daily active users | ≥ 8% on a single model |

Also: excessive wake-ups >10/hour; stuck partial wake locks >1 hour; slow start — cold ≥5 s, warm
≥2 s, hot ≥1 s.

**Google's documented consequence, in Google's own words:** exceeding thresholds means *"your app is
likely to be less discoverable on Google Play"*, and *"a warning may be displayed on your app's store
listing."* **This is the only place Google explicitly links a numeric quality metric to reduced
discoverability — check it before any keyword work on Android.** Field analysis corroborates keyword
rank declines tracking crash-rate spikes after a bad release. **[measured, vendor]**

**Vendor consensus factors [consensus, unverified]:** review recency weighted above age; install
velocity; uninstall rate as a negative; the search → install → retain loop as a relevance signal;
per-keyword CTR as an input; update frequency as an activity signal. ⚠️ App size as a ranking factor:
no credible source found. ⚠️ Rating visibility floors (one vendor says apps under 4.0 are excluded
when users filter by stars; another says under 3.0 loses Explore visibility) — different surfaces,
neither Google-confirmed.

---

## 9. Play Console metrics

**Store listing acquisition report — Google's exact definitions [Google]:**
- **Store listing visitors** — *"users who visited your store listing who didn't already have your
  app installed on any of their devices."*
- **Store listing acquisitions** — visitors who installed, *"who didn't have it installed on any
  other devices at the time."*
- **Store listing conversion rate** — acquisitions ÷ visitors, both restricted to non-installers.

That exclusion is why **Play's CVR is not comparable to Apple's** — see `measurement.md`.

**Traffic sources (three top-level channels):** **Google Play Search** (⚠️ includes Google
Ads-driven installs, so organic search volume is contaminated by ads activity), **Google Play
Explore** (browsing, including category browse), **Ads and referrals**.

**Breakdowns:** country, language, store listing (per-CSL), install state, **search terms**, and UTM
campaign. The **search terms** breakdown is the highest-value ASO report in the console and the
closest thing Play offers to keyword data.

**Peer group benchmarks:** median, 25th and 75th percentile against your peer group — but only when
viewing by country, language, install state, or traffic source, **one selection per dimension**. You
cannot benchmark a multi-country cut.

**Grow overview page:** user/device acquisitions, first opens, MAU/DAU (28 days), 7-day retention,
experiment performance, Play Points, recommendations. ⚠️ Its acquisition taxonomy (**Google Play
explore / Paid and direct / Not attributed**) is *different* from the acquisition report's — do not
reconcile them naively. New in 2026: a **"reach"** metric for total visibility, plus cart conversion.

---

## 10. 2025–2026 changes

- **Play Store redesign (Sept 2025)** — **Guided Search** (describe a goal, not a name), a **You
  tab**, redesigned Apps tab with **curated spaces** (seasonal/interest topics), Play Games Sidekick,
  Leagues, Community Q&A.
- **Ask Play (I/O 2026)** — Gemini-powered overlay that *"turns discovery into a natural
  conversation"*, plus Ask Play highlights on search pages. **[Google]** Rolling out; English-language
  devices first, EEA behind with no confirmed timeline. ⚠️ Vendor claims that it also reads your
  *website*, and that organic results get pushed to screen 4+ for conversational queries, are **not
  Google-confirmed** — but aligning terminology between your listing and your site is low-risk and
  cheap either way.
- **Play Shorts** — full-screen portrait short-form video feed for app promotion. US and select
  developers first. A genuinely new creative surface.
- **Gemini app integration** — apps can be recommended and installed **without opening Play**.
- **AI review summaries** — Gemini-generated, rolled out from late Oct 2025. Uneditable copy on your
  listing: review *themes* are now displayed listing content, so review sentiment became a conversion
  asset, not just a ranking input.
- **Engage SDK** — store listing integration and tablet home-screen Collections, 80+ markets.
- **Play Console 2026** — AI localization (upload a CSV, Gemini pre-populates listings across
  languages), one-click CSL from keyword recommendations, agentic catalog management, new reach metric,
  subscriber tenure and churn-reason data.
- **Low-quality app purge.** The Spam and Minimum Functionality policy (effective 31 Aug 2024)
  requires a *"stable, responsive, and engaging user experience"* and explicitly targets text-only
  apps, single-wallpaper apps, apps that fail to install or load, and apps lacking demonstrable
  utility. Play's app count fell from **3.4M (start of 2024) to 1.8M (April 2025), −47%** **[measured,
  Appfigures]** ⚠️ one source reports −38.2% to 2.1M; the −47% figure has broader corroboration.
  Google blocked 2.36M policy-violating apps and banned 158,000+ developer accounts in 2024. Note the
  confound: the EU trader-status requirement (Feb 2025) also removed listings.
- **Developer verification [Google]** — extends to **all** Android developers including those
  distributing outside Play. Key dates: April 2026 verifier system service; August 2026 limited
  distribution accounts global; **30 Sept 2026 apps must be registered by verified developers to be
  installed on certified devices in Brazil, Indonesia, Singapore and Thailand**; global rollout from
  2027.
- **New personal developer accounts** (created after 13 Nov 2023) need **12 testers opted in
  continuously for 14 days** before production access. Organization accounts are exempt. The
  requirement was reduced from 20 to 12; ⚠️ no Google announcement pins the change date.

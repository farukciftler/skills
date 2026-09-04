# Keyword research and ranking strategy

**Contents**
1. The 2026 data problem you must account for
2. Seed generation and expansion
3. Scoring metrics — what the scales actually mean
4. Prioritization
5. Thresholds and rules of thumb with real numbers
6. Re-indexing timing and iteration cadence
7. Competitor analysis
8. Review mining
9. Myths that data has killed
10. Tool landscape

---

## 1. The 2026 data problem — lead with this

**Apple's Search Popularity data broke in October 2025.** Keywords previously scoring 20–60 collapsed
to the floor value of 5; one tracker measured its keyword pool falling from 165,875 to 39,254 in four
days (**−77%**), confirmed across all markets by every major vendor. Apple issued no statement and
changed no documentation. **[measured]**

Practical consequences you must build into any 2026 keyword methodology:

- **The disclosure floor now sits in the mid-30s.** ⚠️ Sources disagree on the exact number (35 vs 37)
  — don't quote a precise figure.
- **A score of 5 no longer means "low volume"; it means "below Apple's disclosure threshold."** Do not
  auto-discard 5s. Cross-check against store autocomplete presence and App Store Connect's own organic
  impression data.
- **Any prioritization model built purely on ASA Popularity before Oct 2025 is now blind below the
  mid-30s** — which is exactly the long-tail band small apps depend on.
- Apple's replacement, the **Monthly Search Term Rank Report** (Apple Ads → Reports → Insights, beta
  since Oct 2025), refreshes **monthly** and its 1–100 popularity is **genre-relative and does not
  correlate with the legacy 1–5 metric**. It is a trend instrument, not a tactical one.

The right response is a blended model: vendor estimates + autocomplete presence + **the client's own
App Store Connect impression data as ground truth**.

---

## 2. Seed generation and expansion

**Seven seed buckets:**

1. **Brand** — your name, misspellings, brand + category ("spotify podcasts")
2. **Category / generic** — "photo editor", "budget app"
3. **Competitor** — bid on these in Apple Ads; **do not put them in the keyword field** (policy)
4. **Feature** — specific functionality users search for
5. **Problem / use-case** — the intent layer: "track spending", "sleep better"
6. **Long-tail** — 3–4 word combinations; highest precision, lowest volume
7. **Misspellings and variants** — spacing, regional spelling

Cluster by **search intent**: informational, problem-oriented, functional, category, branded,
competitive. One metadata slot per cluster, not per keyword.

**Expansion sources ranked by signal quality:**

| Source | Quality | Notes |
|---|---|---|
| **Apple Ads search terms report** | Highest | Real user queries *with install data* — the only source tying a query to a conversion |
| **App Store Connect organic search impressions** | Highest | Ground truth; the fallback since popularity data degraded |
| **Play Console search terms breakdown** | Highest (Android) | The closest Play equivalent |
| Store autocomplete (both stores) | High | Free, real, ordered by demand |
| Competitor ranked-keyword sets | High | Gap analysis input |
| Apple Ads Popularity Index | Medium, degraded | See §1 |
| Google Keyword Planner / Search Console | Medium for Play, low for iOS | Web intent ≠ app intent |
| Review mining | High for *language*, low for *volume* | §8 |
| Reddit / forums / support tickets | High for problem-intent seeds | Unstructured |
| Your own ranked-but-untargeted keywords | High | Free wins already in flight |

**Expansion mechanics.** On iOS, feed the algorithm **single words** and let it build permutations
across title + subtitle + keyword field (within one locale only). On Play, work at the phrase level
because the index is full-text.

---

## 3. Scoring metrics — what the scales actually mean

**Apple Search Popularity: three different scales, routinely conflated.**

| Scale | Where it appears |
|---|---|
| **1–5** | Apple Ads UI — Apple's own definition: *"a relative indicator of an Apple Ads keyword's popularity"* |
| **1–100** | Apple's Search Term Rank Report (new, Oct 2025), genre-relative |
| **5–100** | The **API-derived** value every third-party tool displays. Floor 5, ceiling 100 |

Both "5 to 100" and "1 to 5" are correct — for different things. **[Apple, for the first two]**

**The scale is exponential, not linear.** The widely used conversion, derived from 30,805 US search
terms across ~316,000 observations:

```
Max daily impressions ≈ 254.4443 × e^(0.0615 × SP)
```

| SP | Est. max daily impressions |
|---|---|
| 10 | ~500 |
| 30 | ~1,600 |
| 40 | ~3,000 |
| 50 | ~5,500 |
| 60 | ~10,000 |
| 80 | ~35,000 |

These are **maximum** impressions at rank 1 / 100% share of voice, not expected traffic. ⚠️ The data
is from **2019** — the constants are almost certainly stale. **The durable takeaways are the
exponential shape (inflection around SP 40) and the ~4-day lag between real impressions and the
published score**, not the coefficients. Roughly 90% of all keywords sit at the floor.

**Vendor metrics (AppTweak's definitions are the de-facto standard; other tools use near-identical
constructs under different names):**

- **Difficulty (0–100)** — how hard it is for *any* app to reach top 10, computed from the App Power
  of the current top 10. **App-agnostic.**
- **Chance score** — app-specific: Difficulty combined with *your* App Power. **This is the one that
  matters for prioritization**, not raw Difficulty.
- **Relevancy (0–100)** — semantic alignment between keyword and app.
- **Max Reach** — impressions if you ranked #1 continuously; the addressable ceiling.
- **KEI** — in ASO this means high volume × high Chance, not the SEO formula.

Illustration worth repeating to clients: "ride" (volume 42) is *harder* than "taxi" (volume 49)
because the apps holding "ride" have higher App Power. **Volume and difficulty are not correlated.**

**Google Play volume estimates are all models.** Google publishes nothing. Vendors reconstruct from
Play autosuggest ordering, Google Ads Keyword Planner (web-intent biased), Search Console, proprietary
panels, and Trends. ⚠️ **Cross-vendor Play volume numbers are not comparable** — pick one vendor and
treat the number as an index.

---

## 4. Prioritization

No vendor publishes a canonical formula, so build and *explain* one:

```
Priority = Volume_norm^w1 × (Relevancy/100)^w2 × (Chance/100)^w3 × RankGap
```

`RankGap` weights headroom: ~1.0 unranked or 50+, 1.5 for ranks 11–30, **2.0 for ranks 4–15 (the
highest-ROI band)**, 0.3 for ranks 1–3 (already won). Typical weights w1=1, w2=1.5, w3=1 —
**relevancy deliberately over-weighted, because volume without relevance is traffic that doesn't
convert.** `scripts/aso_calc.py` implements this.

A simpler three-tier approach survives bad data better:
1. **Tier 1** — moderate volume, high relevance, realistic ranking potential → target now
2. **Tier 2** — high-competition head terms → long horizon
3. **Tier 3** — long-tail 3–4 word queries → cheap wins, fill remaining characters

---

## 5. Thresholds and rules of thumb

**How many keywords.** ⚠️ Vendors conflict but converge: the iOS keyword field holds ~15–20 words;
total actively targeted across all iOS fields ~20–25; one vendor recommends 5–10 active but evaluating
30+. **Working recommendation for a mid-size app: target 20–30 keyword clusters per locale in
metadata; track 300–800 keywords per priority market; evaluate 200–500 per research cycle.**

**Volume threshold worth targeting.** Drop single-digit scores; most US App Store keywords land 10–40;
SP 30–50 is the practical sweet spot for indie and mid-size apps; SP 40+ is where the impression curve
inflects. **But see §1** — post-Oct-2025, a 5 is not evidence of low volume.

**Rank → tap-through on App Store search.** The most misquoted number set in the field. From an
analysis of hundreds of tests **[measured]**:

| Rank | Avg tap-through |
|---|---|
| **1** | **28.38%** |
| 2 | 6.15% |
| 3 | 2.66% |
| 4 | 1.36% |
| 5 | 1.22% |
| 6–9 | 0.80–1.00% |

**Rank 1 gets ~4.6× rank 2 and ~10.7× rank 3. Ranks 4–9 combined are worth less than rank 2 alone.**
Far steeper than web SEO — this is the empirical basis for "better to own a low-volume term than to be
buried on a competitive one." The same study found paid banner TTR (median 19.29%) roughly halves top
organic performance (median 7.11%).

⚠️ A competing distribution circulates (rank 1 = 34% install share, 2–3 = 27%, 4–7 = 18%…) from an
aggregator citing sources without links. Don't use it. See `evidence-log.md`.

**Search vs browse share of installs.** The only well-sourced figures are **2020**: App Store overall
Search 59% / app referrals 20% / browse 12%; **non-game apps ~70% from search**; **games are different
— app referrals ~38% > search 35%**. ⚠️ No comparable refresh has been published since, and **no
public Play search/browse split exists at all**. Any "2026" figure you see is extrapolation. State
this gap rather than filling it.

---

## 6. Re-indexing timing and iteration cadence

**App Store:**
- Indexation can be near-instant — one documented case ranked #11 for a head term within a day of a
  title change. The common "24–72 hours" figure is really the *diagnostic* window: wait ~48–72 h
  before concluding a keyword isn't picked up.
- **Rankings stabilize roughly 4 weeks after a build goes live.** That is the number that matters for
  measurement.
- New apps get a short favourable-ranking honeymoon (~7 days).
- **The hard constraint: saving metadata in App Store Connect does not index it. Keyword changes take
  effect only when a version actually ships live.** This is the top cause of "my keywords aren't
  indexing" tickets.

**Google Play:** slower to stabilize — one documented case took ~3 weeks. Practitioner consensus is
to **wait 6–8 weeks between metadata changes on Android**. ⚠️ Claims that Play re-indexes faster than
iOS contradict every vendor source.

**What can change without a release:**

| Lever | iOS | Play |
|---|---|---|
| Title / subtitle / keyword field | ❌ needs a version | n/a — Play listing edits anytime |
| Description | ❌ needs a version | ✅ anytime |
| Screenshots / previews | ❌ needs a version submission (metadata-only reviews are faster) | ✅ anytime |
| Promotional text (170) | ✅ **anytime, no review** | n/a |
| In-app events | ✅ (own review) | n/a |
| CPP keyword assignment | ✅ **no review** | n/a |
| Review responses | ✅ | ✅ |

**Cadence:** review keyword performance every 3–4 weeks and change when warranted; establish a
baseline before any change; flag keywords at rank 50+ for replacement and ranks **5–20 for
reinforcement via conversion assets rather than more keywords**; Android 6–8 weeks between changes;
**never change metadata and creative simultaneously** — you lose attribution.

Worth telling clients: roughly **80% of apps and games don't change their title in a given year**.
Cadence discipline alone is a competitive edge.

---

## 7. Competitor analysis

**Search competitors ≠ category competitors.** A search competitor is any app in the top 10 for
keywords in your target set, regardless of category. Build the list from keyword result pages, not
from the category chart.

Workflow:
1. Extract each competitor's ranked keywords and their metadata.
2. **Keyword gap analysis** — terms where ≥2 competitors rank top 10 and you don't rank at all. This
   is the highest-yield output of the whole exercise.
3. Harvest competitor Apple Ads bidding terms — those are terms they validated with money.
4. Score with Difficulty against *your* App Power → Chance, then rank the gap set.
5. Track **share of voice** (paid) and **visibility score** (organic). ⚠️ No vendor publishes its
   visibility-score formula, so numbers are **not comparable across tools** — use one vendor
   consistently and treat the output as an index, not a measurement.
6. Track competitor metadata changes over time and correlate their ranking jumps with their change log.

---

## 8. Review mining

Reviews are the best source of the vocabulary users actually use — the primary input to the
problem/use-case seed bucket. Method:

- Extract noun phrases from **1–2★ reviews** → objection handling for description and screenshots.
- Extract benefit language from **5★ reviews** → subtitle and keyword candidates.
- **Validate every candidate against store autocomplete** before spending metadata characters on it.
- Recurring complaints identify conversion blockers; recurring praise identifies the value prop that
  belongs in screenshot 1.

On Google Play there is a second, measured effect: **reviews and developer replies are indexed** (see
`google-play.md` §2). Developer replies are the legitimate lever — you control them and they index.

---

## 9. Myths that data has killed

| Myth | Reality |
|---|---|
| "Plurals rank separately — target both" | Apple explicitly calls singular/plural duplicates and handles them automatically. ⚠️ But a study of 100 singular/plural pairs found only ~half of top-10 apps for a singular also rank top 10 for the plural (iOS 4.4/10, Android 5.6/10) — so *ranking* can diverge even though *indexing* is shared. Verdict: never spend characters on plurals; do check per-keyword rather than assuming parity |
| "The iOS description is indexed" | **False.** Title, subtitle, keyword field (+ IAP/event text, disputed). On **Google Play the long description IS indexed** — the platforms are genuinely opposite |
| "Keyword in the app name always wins" | Name is the highest-weighted field, but difficulty is set by incumbents' App Power. Placement doesn't beat authority |
| "Add every locale for free characters" | Cross-localization is real but rule-bound — **keywords don't combine across locales**, and blind locale-spamming yields isolated single-word indexation, not compounding reach |
| "Repeat keywords across fields for more weight" | Indexing does not stack. Repetition is wasted budget |
| "Stuff the keyword field" | Also wasted: "app", "free", "iPhone", "best", your category name — all indexed for free. Use digits not words. Special characters get replaced with spaces |
| "Paid search alone is enough" | Paid gives short-term lift; when spend stops, without organic relevance the app is undiscoverable. Paid's durable value is as a **research instrument** for organic |
| "ASO = mobile SEO" | The rank-1 cliff (28.4% → 6.2% → 2.7%) is far steeper than web CTR decay. Winner-take-most changes the strategy: depth on winnable terms beats breadth |
| "Saving metadata in App Store Connect indexes it" | No. Only a shipped version indexes iOS keyword changes |
| "Apple OCR-indexes screenshot text" | Failed a 64-phrase controlled test. See `app-store-ios.md` §2 |

---

## 10. Tool landscape (2026)

**Consolidation:** Sensor Tower acquired data.ai (formerly App Annie) in **March 2024**; products were
folded into Sensor Tower rather than run separately. ⚠️ No public sunset timeline for every legacy
line. **Any 2025/2026 statistic attributed to "data.ai" is a red flag** — that brand no longer
publishes.

| Tool | Best at | Indicative pricing ⚠️ re-check, ASO pricing changes often |
|---|---|---|
| **AppTweak** | Deepest keyword research, most transparent metric definitions | ~$69 → ~$199/mo → enterprise |
| **Sensor Tower** | Download/revenue estimates and market intelligence — **not** primarily a keyword tool | $500+/mo, quoted |
| **MobileAction** | Keyword tracking at scale, strongest Apple Ads integration | $15 → $69 → $239/mo |
| **Appfigures** | Cleanest UX, ASO + revenue in one; best for small teams | $29 → $79 → $199/mo |
| **App Radar** | Multi-country breadth at mid pricing, genuine free tier | Free → $69 → $159/mo |
| **ASOMobile** | Rank tracking and monitoring | Mid-range |
| **Gummicube** | **Managed service**, not self-serve tooling | Sales-led |
| **SplitMetrics** | **A/B testing** category leader, incl. off-store testing | from ~$4,999/yr |
| **AppFollow** | Review management, auto-reply, sentiment | ~$111 → ~$222/mo |

**Build the free stack first** — it covers most of what a small client needs:
1. **Apple Ads account (no spend required)** — keyword planner popularity + the Monthly Search Term
   Rank Report
2. **App Store Connect App Analytics** — organic search impressions, per-CPP source analytics
3. **Play Console** — Store Listing Experiments, Custom Store Listings, acquisition + search terms
4. **Store autocomplete on both stores** — the best cross-check on degraded popularity data
5. **Google Keyword Planner + Trends** — seasonality and directional Play demand
6. **Google Search Console** — app-related queries if there's a web property

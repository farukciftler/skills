# Localization and market expansion

## 1. The two stores are structurally different

| | **App Store** | **Google Play** |
|---|---|---|
| Locales | ~40–50 language × territory combinations | 70+ |
| Keyword input | **Dedicated 100-char keyword field per locale**, hidden from users | **No keyword field** — the index is built from title, short and long description |
| Indexed | Name (30), subtitle (30), keyword field (100). **Description NOT indexed** | Title (30), short description (80), **long description (4,000) — all indexed** |
| Cross-indexing | **Yes — 2+ locales index per storefront** | None |
| Custom pages | Custom Product Pages, up to **70** | Custom Store Listings, up to **50** |
| Description weight | Near-zero for ranking (~1% of users read it) | **High — a ranking input** |

Two operational consequences:
- **The same description cannot be optimal for both stores.** On Play it is keyword real estate and
  increasingly LLM input (Ask Play reads it); on iOS it is pure conversion copy.
- **Play localization is more work per locale but more forgiving** of imperfect keyword targeting,
  because the full-text index catches terms the keyword field would have missed.

## 2. Cross-localization first — it is nearly free

Before spending a cent on real localization, fill the secondary indexable locales on the App Store.
Each storefront indexes **two or more locales**, so populating the secondary roughly **doubles your
indexable budget there (+160 characters)** with no new market entry. The full storefront → locale map
is in `app-store-ios.md` §4. The headline moves:

- **English (U.K.) is the secondary locale in most non-English storefronts** — the single
  highest-leverage fill for a global app.
- **Japan's secondary is English (U.S.)**, not English (U.K.).
- **English (Australia)** is the secondary for the **UK** storefront.
- **US = English (U.S.) + Spanish (Mexico)** — the "localization hack" puts overflow *English*
  keywords into the ES-MX keyword field.

**Two hard rules people get wrong:**
1. **Keywords do not combine across locales.** To rank for "metro bus" you need both words within a
   single locale's indexable fields.
2. **Duplicating your keyword list into a secondary locale wastes the entire multiplier.** The
   secondary locale is for the terms that didn't fit.

Keep title and subtitle **genuinely localized** even when using the keyword field for overflow — they
are user-visible and drive conversion for that language's users.

Google Play has no equivalent; every locale is independent.

## 3. Which markets first — method, not a copied list

Do this with the client's own data:

1. Pull **impressions and page views by territory** from App Store Connect / Play Console for the
   current app. You are looking for territories with **existing impression volume but below-average
   conversion** — that gap is the localization prize, and it is measured rather than guessed.
2. Score candidates on: existing impression volume × category demand × (1 / competitor density) ×
   ARPU × (1 / localization cost) × (1 / regulatory complexity).
3. Add the **cross-localization multiplier** — a language that is also the secondary locale for
   storefronts you already win is worth more than its own market.

**Defensible default tiers** when there is no data yet:

- **Tier 0 — always, near-zero cost:** English (UK / AU / CA) variants; Spanish (Mexico) keyword field
  for US cross-indexing.
- **Tier 1 — revenue:** Japanese, German, Korean, French, Simplified Chinese (if you can operate in
  mainland China), Traditional Chinese.
- **Tier 2 — volume:** Portuguese (BR), Spanish (LatAm), Indonesian, Turkish, Russian, Hindi.
- **Tier 3 — long tail:** Italian, Dutch, Polish, Thai, Vietnamese, Arabic.

⚠️ One 2026 vendor ROI ranking puts **Brazil and Mexico highest**, then South Korea, Germany, Japan —
a cost-and-volume-weighted view. **Japan, Korea and Germany dominate on ARPU; Brazil, Mexico and
Indonesia dominate on volume per dollar.** The weighting is undisclosed; treat it as one credible
ordering, not *the* ordering. Which one is right depends entirely on whether the client is optimizing
for installs or revenue — ask.

## 4. Levels of localization, and where each pays

| Level | Covers | Relative cost | Where it wins |
|---|---|---|---|
| **Translation** | Words converted, linguistically correct | 1× | Lowest ASO impact — often *negative*, because it produces keywords nobody searches |
| **Metadata localization** | Title, subtitle, keyword field, descriptions **researched in-language against real search volume** | 2–3× | The correct starting point; drives ranking |
| **Creative localization** | Screenshot text and imagery | 4–6× | **Highest conversion ROI** |
| **Full localization** | + in-app UI, support, pricing, formats | 10×+ | Required for retention and monetization, not for install CVR |
| **Culturalization** | Messaging rewritten for local norms; local imagery, holidays, payment methods, naming conventions | 15×+ | Japan, Korea, China, MENA — markets where translated Western messaging visibly reads as foreign |

**Practical sequencing: localize screenshot text first, metadata second, in-app UI third.** This
inverts most teams' instinct, and it follows directly from the scroll-depth data — 80–90% of users
never scroll, and roughly 1% read the description.

**ROI evidence** ⚠️ all vendor-sourced, mixed quality: the cleanest single data point is **+36% CVR
from localizing screenshots for Japan** (a creative-only change, so the effect is isolated). Other
circulating figures — "+26% from localized listings", "+128% downloads going multi-market", a single
case at "+711% in 8 months" — are uncontrolled single cases or have offline originals. Per-locale
launch cost is quoted at **$1,000–$5,000**. Use these to frame a range, not to promise a number.

## 5. Common mistakes

1. **Machine-translating the keyword field.** MT gives the *dictionary* translation, not the
   *searched* term. German users search "Kalorienzähler", not a literal rendering of "calorie counter
   app". **Keyword research must be done natively per language against local volume data** — never by
   translating an English list.
2. **Ignoring local naming conventions.** In Japan and Korea category leaders often carry a
   descriptive suffix; German compound nouns are single searchable tokens; in Brazil informal or
   abbreviated forms outrank formal ones. A brand-first title translated into a descriptive-first
   market loses ranking.
3. **Reusing European Portuguese for Brazil**, Iberian Spanish for LatAm, or Simplified Chinese for
   Taiwan/Hong Kong. Reads as wrong and ranks badly.
4. **Duplicating keywords into secondary locales** — wastes the cross-localization multiplier.
5. **Launching a locale with no traffic.** A new locale has no ranking history and may never surface
   without seed volume. ⚠️ One vendor suggests a ~10,000-download threshold before organic indexing
   meaningfully kicks in (unverified) — regardless of the exact number, plan a small paid push or
   cross-promo alongside a new locale launch.
6. **Localizing metadata but not screenshots** — the most common half-measure: captures ranking,
   loses conversion.
7. **Baking untranslated text into screenshot images**, which also blocks per-market A/B testing.

## 6. RTL (Arabic, Hebrew, Farsi, Urdu)

⚠️ **No published RTL-specific conversion data exists** from either store or any vendor. Practical
requirements:

- **Mirror the screenshot set**, don't just translate it — reading order runs right-to-left, so the
  hero frame is the rightmost one and panoramic/stitched sets must be reversed.
- In-app: use system layout-direction APIs (`semanticContentAttribute` / `layoutDirection` on iOS,
  `android:supportsRtl="true"` plus start/end constraints on Android) rather than left/right constants.
- Numerals, dates and currency may use Eastern Arabic numerals depending on locale — test with real users.
- **Arabic is a secondary indexed locale in several storefronts** — an under-used cross-localization slot.

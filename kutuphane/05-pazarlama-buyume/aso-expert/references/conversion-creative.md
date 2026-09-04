# Conversion, creative, ratings and reviews

**Contents**
1. Funnel geometry — why the first frame dominates
2. User behaviour data (and how stale it is)
3. What moves conversion, with measured uplift ranges
4. Screenshot and caption patterns that work
5. Browsers vs searchers
6. The creative test roadmap
7. Test design: sample size, duration, statistics
8. Ratings — the conversion and featuring gate
9. Review prompts, responses, AI summaries, review bombing

---

## 1. Funnel geometry

A large share of App Store installs never involve a product page view at all — the user taps GET
straight from the search results card. That card shows **icon, name, subtitle, star rating + count,
and the first 1–3 screenshots** (3 if portrait, 1 if landscape) or the autoplaying preview.

That set is the **first impression frame**. Because Apple's conversion rate divides by *impressions*,
not page views, work on the first impression frame shows up as **more page views and a higher
Apple-defined CVR** — not as a better page conversion. Split the two stages before attributing
anything, or you will credit the wrong change.

**Portrait beats landscape by default** because portrait puts 3 assets in the search card versus 1.
Landscape is defensible only for landscape-native games where a single cinematic frame carries the
value prop. There is no published head-to-head benchmark — this is an argument from surface
mechanics, and worth labelling as such.

---

## 2. User behaviour data — all of it is old

⚠️ **Every decision-time and scroll-depth figure in circulation is 2018–2021 vintage, and the original
Storemaven research pages are now offline.** Use them for shape, never as current fact.

| Claim | Vintage |
|---|---|
| ~6.8 s average on a store page ("7 seconds") | ~2019–2021 |
| 10 s App Store / 14 s Google Play | 2018–2020 (contradicts the above) |
| "Decisive" users 3–6 s (60–70%); "Explorers" 12–35 s (30–40%) | undated |
| 90% of iOS users see ~10% of page content; only ~15% view the whole page | 2018–2020 |
| Only 13% scroll through screenshots; <18% ever see slot 2; **1% read the description** | ~2021 |

**Defensible synthesis to give a client:** most users decide in under 10 seconds and roughly
two-thirds in under 7; **80–90% never scroll meaningfully**; screenshots 1–2 (portrait) carry
essentially all creative weight; on iOS the description is read by a rounding error of users.

Video attention: average preview watch ~5–7 s, **only ~8% watch to completion**. One vendor reports
portrait video at +7% watch time / +5% conversion versus landscape ⚠️ sample and date undisclosed.

---

## 3. What moves conversion

**Published A/B case studies — read as *ceilings observed*, not expected values** (vendors publish
their wins):

| Element | Uplift |
|---|---|
| Screenshots (best cases) | +61%, +36% (Japan-localized), +33%, +32%, +31% |
| Screenshots (typical published win) | +13% to +20% |
| iPad screenshots | +15% |
| Caption / copy edits only | +10% |
| **Icon** | +9% to +19% |

**Plan against these ranges, not the ceilings:**
- **Screenshot set redesign: +5% to +20%.** Above +30% usually means the baseline was broken.
- **Icon: +5% to +15%**, with the widest variance and the highest brand cost. Icon tests also need the
  largest sample and, on Apple, a shipped binary containing the alternates.
- **Custom Product Pages vs default for matched traffic:** vendor measurement lands at **+5.9%
  average, up to +8.6%** for generic campaigns, and ~**+10% median** for Google's Custom Store
  Listings. ⚠️ Apple's "+156%" is marketing on a 1.6% impression-based denominator and is confounded —
  CPP traffic is intent-matched by construction.

**Where lift comes from** — a useful decomposition to set expectations: roughly **60% of positive ASO
test results come from major design changes, ~20% from copy and communication, ≤20% from layout
reordering.** Reordering existing screenshots is the cheapest test and the lowest-ceiling one.

**Testing adoption is low, which is the arbitrage.** Across the top 1,000 US apps and games (2025
data): only **35% of top apps and 33% of top games tested 2+ screenshot versions**; **~90% of top App
Store apps never tested icons or videos at all**; on Google Play **76–80% never tested icons, videos
or feature graphics.** **[measured]**

---

## 4. Screenshot and caption patterns that work

1. **Benefit, not feature.** "Never miss a bill" beats "Bill reminders."
2. **Caption above the device frame**, large, 3–5 words. Text inside a shrunken phone mockup is
   unreadable at search-card size.
3. **Screenshot 1 = the single strongest value prop.** Using slot 1 for a logo splash or a "welcome"
   screen is the most common destroyer of conversion. (It is also an App Review risk — Guideline 2.3.3
   requires screenshots to show the app in use.)
4. **Slots 1–2 must be legible at ~30% scale.** Shrink to thumbnail size and check.
5. **A social-proof frame** ("4.8★ · 2M users", press logos, awards) at slot 2 or 3 is a reliable
   mid-funnel win, especially in finance and health.
6. **Panoramic / stitched sets** raise perceived polish but reduce per-frame clarity. They work better
   on Google Play (where slot 1 shows alone above the fold) than on Apple. Test, don't assume.
7. **Localized text inside the image is the highest-ROI localization action** — see `localization.md`.
8. **Video: test presence before content.** On the App Store a preview autoplays muted and *replaces*
   screenshot slot 1 in the first impression frame. It is frequently net-negative for utility apps
   where a static value-prop frame outperforms motion.

---

## 5. Browsers vs searchers

Search traffic converts far better than browse traffic — searchers arrive with intent, often with a
brand name. Roughly **95% of App Store search traffic is brand/navigational**. **[vendor]**

The implication most teams miss: **your default product page mostly serves people who already know
you.** Its job is reassurance and friction removal, not persuasion. Persuasion creative matters on
**browse** traffic — the Today/Games/Apps tabs, charts, "similar apps" — which converts at a fraction
of search rates. That is the traffic segment Custom Product Pages and PPO were built for.

⚠️ **Neither store lets you segment A/B test results by traffic source.** This is the single biggest
measurement weakness in store creative testing, on both Apple PPO and Play SLE. Say so when presenting
a test plan.

⚠️ Claims that store search has fallen to ~48% of installs with 35–40% now from social and AI come
from a source that contradicts itself in the same article. Don't cite a number here.

---

## 6. The creative test roadmap

Ranked by expected value:

| # | Test | Why here | Detectable MDE |
|---|---|---|---|
| 1 | **Screenshot 1 — the hero frame's message** (not its styling) | 80–90% of users see only this; largest observed effects | 5–10% relative |
| 2 | **Screenshots 1–3 as a set** — order and captions | Second-order framing; cheap once #1 is settled | 5–10% |
| 3 | **App icon** | High ceiling, high variance, highest brand cost, largest sample | 8–15% |
| 4 | **Video present vs absent**, then content | Binary, high-leverage, often net-negative — must be tested | 5–10% |
| 5 | **Subtitle / short description copy** (Play only — Apple PPO cannot test metadata) | Copy ≈ 20% of ASO effect size | ~5% |
| 6 | Screenshots 4+, feature graphic, panoramic styling | <18% of users see slot 2+ | rarely detectable |

---

## 7. Test design

**Duration:** minimum **7 days**, always in whole-week multiples. Day-of-week effects on store traffic
are large — weekend browse spikes, weekday utility search. Both Google and independent vendors say the
same.

**Sample rule of thumb:** to detect a **5% relative lift** on a ~30% baseline CVR you need on the
order of **30–40k users per variant**; a **10% relative lift** needs ~8–10k per variant. **Apps with
under ~5,000 weekly product page views cannot reliably A/B test creative on-store** — use off-store
panel testing or accept larger MDEs and decide on judgment. `scripts/aso_calc.py` does this properly
for a given baseline.

**Apple PPO:** 3 treatments max, 90-day cap, one concurrent test, Bayesian with a **fixed 90%
confidence bar** (roughly double the false-positive rate of the 95% standard, with no documented
multiplicity correction across 3 treatments). Results aggregate across all selected localizations and
cannot be decomposed. Every treatment needs App Review; pure reordering of approved assets does not.

**Play SLE:** 3 variants + control, configurable confidence (⚠️ vendor-reported 90/95/98/99%) and MDE,
metric = first-time installers or **retained first-time installers (1-day retention, Google's
recommendation)**. Use 95% + retained where traffic allows.

**Discipline that matters more than the statistics:**
- Test **one variable at a time**. With 3 multi-variable treatments you learn which page won, never why.
- Set confidence and MDE **before** launch; stopping the moment a variant crosses the line inflates
  false positives.
- Never run a creative test alongside a paid campaign launch, a price change, or a seasonal peak.
- **Keep a test log** — variant, dates, traffic, MDE, confidence, result, whether it shipped. This is
  the asset that compounds, and almost nobody keeps it.
- **A losing test with a clean read is a result.** Report it.

---

## 8. Ratings

**The canonical rating→conversion numbers trace to a single 2015 survey of 350 US smartphone owners:**
2★ → 15% would consider downloading, 3★ → 50%, 4★ → 96%; hence the famous "+340% from 2★ to 3★" and
"+89% from 3★ to 4★". ⚠️ **n=350, stated preference not observed behaviour, 2015, US-only, predates
per-country ratings, AI review summaries and the current layouts.** Use it for the *shape* — a sharp
cliff below 4.0, near-saturation above 4.5 — never as a forecast. It is the most over-cited number in
ASO.

**Stronger structural evidence:** ~**95% of Apple-featured apps are rated 4.0+ and 65% are 4.6+**;
Google Play is near-identical at ~96% rated 4.0+. **[measured, 2025 data]** Rating functions as a
**gate on editorial featuring**, independent of any direct CVR effect. That argument lands better with
executives than the 2015 survey.

**Volume thresholds** ⚠️ practitioner heuristic, no published study:
- **<50 ratings** — the average is noise; one 1★ visibly moves it.
- **~200–1,000** — the average stabilizes; rating becomes a real conversion asset.
- **>10,000** — nearly immovable short-term, which cuts both ways.

**Rating resets — the platforms work completely differently, so the playbooks differ:**

**App Store [Apple]:** resets are **opt-in and version-scoped** — you select it in version settings
*before* submitting. Not automatic on every update (that changed in 2017). Applies to **all
territories at once**, is **per-platform** for universal apps, **cannot be undone**, and **written
reviews survive** — only the numeric summary clears. Requires Admin or App Manager. Apple advises
using it sparingly, and the store displays a notice that the rating was recently reset.

**Google Play:** **no developer-controlled reset.** Since Aug 2021 the displayed rating is
**recency-weighted** (recent reviews dominate; reviews over ~12 months old carry negligible weight)
and **per country**, and since Nov 2021 **per device type**. The same app can legitimately show 4.6 in
India and 4.1 in the US. ⚠️ The precise weight curve circulating online is a third-party
reconstruction — the direction is verified, the exact bands are not.

**Consequence:** on iOS rating repair is a **discrete, one-shot, high-stakes lever tied to a release**.
On Play it is a **continuous ~90-day process driven by review velocity.**

---

## 9. Review prompts, responses, summaries, bombing

**Apple prompt limits [Apple]:** the system prompt can appear a **maximum of 3 times per app per 365
days**. Your call is a *request* — the system decides, and you cannot detect whether it appeared. You
must **not** attach it to a button or CTA, and must not pre-qualify with "do you like the app?".
API state: `SKStoreReviewController.requestReview()` was **deprecated in iOS 18**; use
`AppStore.requestReview(in:)` (needs a `UIWindowScene`) or the SwiftUI `@Environment(\.requestReview)`
action. ⚠️ Known gap: the replacement is not a complete drop-in for non-scene contexts, and
cross-platform frameworks had extended migration gaps.

**Google In-App Review API [Google]:** the quota is **deliberately undisclosed** — *"an implementation
detail, and it can be changed by Google Play without any notice."* More than once a month likely won't
display. Hard rules: don't modify the card's size/opacity/shape, no overlays, keep it topmost, never
remove it programmatically, **never attach it to a button** (an over-quota user gets a dead button —
send those users to the listing instead), and no pre-qualifying questions.

**Prompt timing is the whole game**, because you get ~3 iOS shots per user per year and an opaque Play
quota. Trigger on a **completed positive moment** — a finished workout, a completed transfer, a cleared
level, an exported file — and not the *first* one; wait until the 3rd–5th so the user has habituated.
Never after an error, a paywall, a denied permission, or a crash-adjacent session. Never mid-task.
Suppress for N days after any incident. Gate on sentiment you already know from elsewhere (NPS,
support history, engagement decile) — but never with an in-app question immediately before the prompt,
which both stores prohibit. Track your own counter; don't rely on the OS to stop you wasting the slots.

**Responding to reviews.** Google's stated figure is that **responding to a negative review raises
that rating by an average of +0.7 stars** ⚠️ genuinely Google's number, but every current citation is
secondary — present it as "Google's stated figure". On Apple, Admin or Customer Support roles can
respond to reviews of **any age**, the **reviewer is notified and can update their review** (that is
the mechanism behind the lift), and only the latest response version displays.

Apple's own prioritization advice: lowest star ratings first, then technical-issue reports on the
current version; reply promptly after major releases; when addressing an old complaint you've since
fixed, say so and reflect it in release notes. Concise, personalized, no marketing language.

**Operational targets:** 100% response on 1–2★, median response time under 24 h on 1–2★, near-100% on
reviews naming a bug in the current version. Responding to positive reviews is optional and low-ROI.

**AI review summaries — new, under-exploited, on both stores.** Apple shipped LLM review summaries in
iOS 18.4, refreshed at least weekly, English/US first and expanding; Google rolled out Gemini-generated
summaries from late Oct 2025. **You cannot edit them.** Two consequences:
1. **Recurring complaint themes are now promoted rather than buried.** A cluster of "too many ads"
   reviews that used to require scrolling now appears as a summary line. **Fixing your top three
   complaint themes now has a direct conversion effect it never had before.**
2. **Review campaigns should steer sentiment topics, not just star counts** — prompting happy users at
   the moment they used your differentiating feature makes that feature likelier to appear in the summary.

**Review bombing.** Detection: an abrupt velocity spike (10×+ normal), concentrated in 1–2★, clustered
in one country or language, short or templated text, usually correlated with an off-platform event.
Playbook:
1. **Do not mass-respond with a template** — it amplifies visibility and, on Apple, notifies every
   reviewer.
2. **Report coordinated content** — "Report a Concern" in App Store Connect, or the Play Console
   reporting flow. You are not told the outcome.
3. **On Google Play, wait it out and dilute.** Recency weighting decays a bombing out in ~90 days if
   you restore normal review velocity. Driving legitimate reviews is the single most effective response.
4. **On the App Store there is no decay mechanism.** Your only lever is the version-scoped reset,
   which also destroys your legitimate rating — worth it only if the average is structurally ruined.
5. **Fix and publicize** if the cause is legitimate: ship it, put it in release notes, respond
   individually to the highest-visibility reviews (Apple notifies the reviewer, who can update).

**Context for clients asking about buying reviews:** in 2025 Apple processed over 1.3 billion ratings
and reviews and blocked close to **195 million fraudulent** ones (~15%), terminated **193,000
developer accounts**, and rejected over 2 million of 9.1 million submissions. Google's enforcement is
silent — reviews vanish or the listing is suppressed with no notification.

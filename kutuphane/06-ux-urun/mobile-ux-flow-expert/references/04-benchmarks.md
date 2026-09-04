# Benchmarks

Numbers with their source and date, so you can cite honestly and say what they don't cover. All figures are medians or averages across mixed categories unless stated — **a median is not a target**. Always translate a benchmark into "what this implies for this app" rather than handing it over raw.

Quality tiers used below:
- **A** — large-sample vendor datasets or standards bodies with published methodology (RevenueCat SOSA, Baymard, Adjust, Apple/Google docs).
- **B** — vendor blogs and aggregators citing primary data.
- **C** — directional; secondary citation, unclear methodology. Flag as directional when using.

---

## 1. Activation and retention

| Metric | Value | Source / date | Tier |
|---|---|---|---|
| Median activation rate, all apps | ~25% (average ~34%) | Plotline, Dec 2024, via Kirro 2026 | B |
| Products where 98% of new users are inactive by Day 14 | half of all products | Amplitude, 2,600+ companies | A |
| Apps with strong Day-7 activation that also retain well at 3 months | 69% | via Kirro 2026 | B |
| Typical retention curve | ~26% D1, ~13% D7, ~7% D30 | aggregated benchmarks, 2025 | B |
| Global average app onboarding rate at Day 30 | 8.4% | Business of Apps, Jan 2026 | B |
| Onboarding abandonment when friction is high | 21–72% | Setgreet, Sept 2025 | C |
| Onboarding completion, B2C apps with free trials | 30–50% | InnerTrends, via Kirro | B |
| Activation lift from deferred signup | ~10–30% | Appcues and similar, via UXCam 2026 | C |
| Retail install→purchase conversion | 1.39% | UXCam, Feb 2026 | B |
| Travel install→purchase conversion | 2.42% | UXCam, Feb 2026 | B |

**Diagnostic use:** if Day-1 retention is under 30–40%, the problem is onboarding or a store-listing/product mismatch — no notification strategy fixes it. If activation is under 25%, stop optimising the store listing.

---

## 2. Subscription, paywall and trial (RevenueCat SOSA 2026)

Dataset: 115,000+ apps, $16B+ revenue, 1B+ transactions, primarily 2025 performance, iOS/Android/web. Tier **A** for the dataset, though skewed toward B2C mobile subscription apps.

| Metric | Value |
|---|---|
| Day-35 download→paid, **hard paywall** | 10.7% median (top 10%: 38.7%; bottom quartile: 4.2%) |
| Day-35 download→paid, **freemium** | 2.1% median |
| Revenue per install at Day 60 | ~8x higher for hard paywall |
| 1-year retention of yearly subscribers | 27% hard paywall vs 28% freemium — negligible difference |
| Share of paid conversions occurring on **Day 0** | ~50% |
| 3-day trial users cancelling on Day 0 | 55.4% (≈84% of all 3-day trial cancellations by end of Day 1) |
| 7-day trial users cancelling on Day 0 | 39.8% |
| Cancellation rate by trial length | ~26% for 3-day, ~51% for 30-day |
| Day-35 download→paid by platform | iOS 2.6%, Android 0.9% |
| Trial→paid on Android | 32.5% (i.e. the Android gap is upstream of the trial) |
| Download→paid by price tier (median) | high 2.8%, mid 2.0%, low 1.4%; ~1.4x step per tier |
| Apps using trials ≤4 days | 46.5%, up from 42.1% the prior year |
| Trial start timing with hard paywall | 78% start within the first week of download |

Category notes: Business, Health & Fitness and Productivity convert best (habitual use cases); Gaming and Media & Entertainment convert worst (impulse). Travel had the highest trial→paid; Photo & Video the lowest.

---

## 3. Permissions and opt-in

| Metric | Value | Source / date | Tier |
|---|---|---|---|
| Push opt-in, all devices | ~67.5% | MobiLoud / Plotline aggregate | B |
| Push opt-in, iOS | ~44–54% | multiple 2025–26 aggregates | B |
| Push opt-in, Android | ~81–91% (falling as Android 13+ requires explicit consent) | same | B |
| Lift from pre-permission priming (soft ask) | 2–3x | Plotline, Apr 2026 | B |
| Opt-in after 1–3 sessions vs 4–6 sessions | ~35% → roughly double | Localytics (older, still directionally cited) | C |
| ATT opt-in, gaming subgenres Q2 2025 | sports 50%, hyper-casual 43%, action 40%, board 30% | Adjust, 2025 | A |
| ATT opt-in, education | 14% (up from 7% in 2023, attributed to better pre-permission prompts) | Adjust, 2025 | A |

Highest iOS push opt-in industries: banking, business, services. Lowest: hypercasual games, streaming, telecoms.

---

## 4. Checkout, forms and friction (Baymard)

| Metric | Value |
|---|---|
| Abandonment due to unexpected extra costs | ~39–48% |
| Abandonment due to required account creation | ~19% (22–26% of all checkout abandonments in survey data) |
| Abandonment because checkout felt too long/complicated | ~18% |
| Average checkout form fields shipped | ~11.3 across ~5.1 steps |
| Optimal field count | 7–8 |
| Completion drop per field beyond the eighth | ~4–6% |
| Average form elements displayed | ~23; effective checkouts use 12–14 |
| Top-50 mobile ecommerce sites failing ≥2 of 5 keyboard optimisations | 60% |

Mobile apps outperform mobile web on checkout largely through saved credentials and fewer fields — the design lesson transfers: **every field you can pre-fill or infer is worth more than any copy change.**

Mobile form abandonment is commonly cited around 80% (tier **C** — methodology varies). The mechanism is consistent and worth citing even if the number isn't precise: users start, get interrupted, return to a blank form.

---

## 5. Authentication

| Metric | Value | Source | Tier |
|---|---|---|---|
| Social sign-on vs email+password conversion, consumer apps | ~2–3x higher | UXCam 2026 aggregate | C |
| Sign-in time reduction after passkeys | ~50% | Kayak, via FIDO Alliance | A |
| Sign-in error reduction after passkeys | 4x fewer | Kayak, via FIDO Alliance | A |
| Passwordless sign-in success once credential provisioned | 99.9% vs 71% for password+MFA | Microsoft Entra telemetry, 2024 (workforce, not consumer) | A |
| Passkey adoption without device-aware prompting | stalls at 5–10% | Corbado cross-vendor study, 2026 | B |
| Consumer population without a passkey-compatible device | ~8–15% | 2026 estimate | C |

Implication: passkeys are an **enrollment** design problem, not an authentication one. Every published win measures post-enrollment.

---

## 6. Interaction and performance thresholds

| Threshold | Value | Origin |
|---|---|---|
| Doherty threshold — response that keeps users in flow | ≤400ms | IBM, 1982; still the standard citation |
| Minimum tap target, iOS | 44×44pt | Apple HIG |
| Minimum tap target, Android | 48×48dp | Material |
| Thumb-driven interaction share | ~75% | Hoober, 1,300+ users observed |
| One-handed use share | ~49% | Hoober |
| Working memory capacity | ~7±2 items (Miller) — treat as "chunk aggressively", not a hard cap |
| Skeleton vs spinner threshold | show skeleton above ~400ms; meaningful progress above 2s |
| Streaming vs spinner for AI output | stream anything over ~2s |

Screen-size effect on one-handed usability: reach degrades markedly past ~6.5". Specific percentage claims circulating on this (e.g. "23% per 0.5 inch") are tier **C** — use the direction, not the number.

---

## 7. Analytics hygiene

| Guideline | Value |
|---|---|
| Well-designed events most apps need | 15–30 |
| Firebase free-tier limits | 500 distinct event names, 25 parameters per event — new events silently drop past the cap |
| Dashboard KPIs worth maintaining | 6–10 primary |
| Metric retirement rule | if nobody has opened it in 30 days, delete it |

---

## How to use these in an answer

1. **Name the source and its date.** "RevenueCat's 2026 report, based on 115,000 apps" is credible; "studies show" is not.
2. **State the population.** A B2C subscription median doesn't govern a B2B field-service app.
3. **Convert to a decision.** Not "median activation is 25%" but "you're at 12%, which puts you in the bottom half — the highest-return fix is the step between permission ask and first save, where you're losing 40%."
4. **Flag directional numbers as directional.** Credibility is the asset; one over-claimed statistic costs more than it wins.
5. **Prefer the mechanism over the number** where you have both. "Users abandon when they get interrupted and return to a blank form" survives scrutiny even if the 80% figure doesn't.

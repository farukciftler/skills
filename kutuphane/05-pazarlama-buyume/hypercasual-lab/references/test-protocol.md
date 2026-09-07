# Test protocol — turning a fixed daily budget into a decision

Read this at G2 and again at G4. This file is the difference between spending money and buying information.

## Contents
- Step 0: budget reality check
- Sample size math
- G2 creative test
- G4 install test
- Metric gates
- Decision tree
- The publisher path
- Output templates

---

## Step 0: budget reality check

Do this arithmetic out loud, in front of the person, before designing any campaign. Skipping it is how a plan gets built on a budget that cannot execute it.

1. **Convert the budget.** Fetch the live TRY/USD rate. Every benchmark, minimum and CPI figure is USD-denominated.
2. **Fetch current CPI for the target category and geo.** From current benchmark publications, with the date attached. Never carry a remembered figure into a budget plan.
3. **Compute the reachable install count:**
   ```
   installs = (daily budget in USD × test days) / CPI in that geo
   ```
4. **Compare against the sample size table below.** If the reachable install count cannot support the metric being tested, the design is wrong — change the geo, extend the burst, or narrow what the test claims to answer. Do not run it anyway and interpret the noise.
5. **Check platform minimums.** Ad platforms enforce minimum daily budgets per campaign and per ad set, and splitting a small budget across many ad sets starves each below the level where optimization converges. Fewer ad sets, larger each.

State the conclusion plainly, for example: *this budget buys a retention read in geo X, and a relative creative ranking, but does not buy a Tier-1 CPI benchmark or an LTV estimate.* Naming the limit is the most valuable output of this step.

---

## Sample size math

Retention is a proportion, so the confidence interval on a small cohort is wide. Approximate installs needed for a D1 retention read, at 95% confidence around a rate near 35%:

| Precision wanted | Installs needed |
|---|---|
| ±10 percentage points | ~90 |
| ±7 pp | ~180 |
| ±5 pp | ~350 |
| ±3 pp | ~970 |

Practical reading:
- **Under ~90 installs:** no retention conclusion is available. The test can still rank creatives on CTR/CPM, which needs far fewer installs because impressions are the denominator.
- **~150-300 installs:** enough to distinguish "clearly broken" from "clearly promising". This is the realistic target for a small-budget G4, and it is a genuinely useful answer.
- **Under ~90 installs per creative:** creatives cannot be compared on CPI, only on upper-funnel metrics.

Always print the sample size next to every retention number reported, and give the interval, not just the point estimate. A single number from 120 installs invites a decision the data cannot support.

---

## G2 — creative test (no game required)

**Purpose:** find out whether the hook stops the scroll, before any build cost is incurred.

**Design**
- Three creatives, one hook family, genuinely different executions — not three color grades of the same video
- One platform to start. TikTok is usually the strongest fit for this genre's creative language and is cheap to test on; Meta is the alternative and is worth adding once one creative shows life.
- Objective: video views or traffic, not app installs — there is no app yet
- Duration: 3-4 days minimum. Shorter than that and the platform's learning phase dominates the result.
- Budget: a modest fraction of the daily figure, since impressions are cheap relative to installs
- Destination: a coming-soon page or placeholder listing. Use `serverim-build` if a page is needed.

**What to measure**
- 3-second / hook retention rate — the single most predictive number here
- CTR
- CPM, as a cost sanity check
- Watch-through curve shape if the platform exposes it: where people drop tells you which second of the mechanic fails

**Gate:** at least one creative must clearly beat the current category baseline — look the baseline up, do not assume it. If none does, return to G0. This gate is cheap and it is where most concepts should die.

Keep the winning creative and the geo consistent into G4, otherwise the two tests measure different things and cannot be chained.

---

## G4 — install test

**Purpose:** does anyone come back tomorrow.

**Design**
- **Burst, not trickle.** Concentrate the budget into a short window — roughly 5-7 days — so the campaign exits learning and the cohort is large enough to read. The same money spread over a month produces nothing.
- **One campaign, few ad sets.** Small budgets fragment badly.
- **Geo chosen so the budget reaches the sample size.** On a small budget this usually means a lower-CPI market. Be explicit about the tradeoff: retention transfers across geos reasonably well, CPI and eCPM do not transfer at all. Read retention from the cheap geo; do not read revenue from it.
- **Creatives:** the G2 winners only.
- **Objective:** app installs. Confirm the current attribution setup is live and reporting before the first lira is spent — see `references/architecture.md`.
- **Light ad load in the build.** Heavy monetization during a retention test contaminates the measurement.

**Pre-flight checklist — all must be true before spending:**
- [ ] Build live on the App Store and downloadable in the target geo
- [ ] Analytics firing and verified on a real device, all events in the minimum set
- [ ] D1 computable per install cohort, sliceable by creative
- [ ] Attribution framework configured, conversion values set, test install verified end to end
- [ ] ATT and consent flows working
- [ ] Ad placements live but throttled
- [ ] Sample-size math done and the target install count written down in advance

A test launched with any box unchecked spends the budget and returns nothing.

---

## Metric gates

Read in this order. Do not evaluate a lower line until the line above clears — a great CPI on a game with broken retention is a trap.

1. **D1 retention** — the gate. Look up the current benchmark for the specific category and geo; casual game benchmarks are published regularly and vary meaningfully by subgenre. Judge against that published figure, not a remembered one.
2. **Session length and sessions per user** — do people play, or just open? A healthy hyper-casual session is short but repeated.
3. **Level funnel** — where the drop happens. If D1 is weak, this tells you whether it is fixable tuning or a broken core loop. This is the iterate-versus-kill evidence.
4. **CPI, relative between creatives** — on a small sample, the reliable signal is ranking, not the absolute number.
5. **D7 retention** — only interpretable if D1 cleared and the cohort was large enough.
6. **Early ARPDAU** — directional only, and geo-bound. Do not project LTV from it on a small sample.

---

## Decision tree

```
D1 clears the benchmark?
├─ NO, and badly (well below)
│   └─ KILL. Next candidate. Say it plainly.
├─ NO, but close, and the funnel shows one specific leak
│   └─ ITERATE — one named fix, one re-test, one round only.
│      A second iterate round on the same concept is a disguised kill.
└─ YES
    ├─ Publisher pitch realistic?
    │   └─ PITCH. Let them fund the Tier-1 CPI test.
    └─ Self-publish
        └─ SCALE: full monetization, ASO (`aso-expert`),
           raise spend against measured payback, not against hope.
```

Most runs end at KILL. That is the pipeline working, and it should be framed that way rather than as a failure — the value delivered is the speed and cheapness of the no.

---

## The publisher path

On a small budget this deserves active consideration rather than being treated as a fallback, because it moves the expensive part of the test onto someone else's balance sheet. Publishers in this space typically evaluate a prototype video or a test build and, if interested, run the Tier-1 CPI test on their own UA infrastructure — which is exactly the test a small budget cannot buy.

Names to check for current status, since submission programs open and close: Voodoo, Homa Games, Supersonic (Unity), CrazyLabs, Rollic, TapNation, Kwalee, Lion Studios, Zephyr Mobile. Verify each one's current submission process and requirements directly from their developer page — do not rely on remembered terms.

What they generally want, to be confirmed per publisher:
- A short gameplay video of the actual prototype
- Retention numbers if any exist
- A Unity build, since their test harness is Unity-based
- A concept that fits their current portfolio direction

Deal shape is typically a revenue share with the publisher funding user acquisition. Read the actual terms — IP ownership, exclusivity, and termination conditions vary a lot and matter more than the headline percentage. This is a contract question, not a technical one; recommend a legal read before signing anything.

---

## Output templates

### `test-plani.md` (before spending)
```markdown
# Test Planı — [konsept] — [tarih]

## Bütçe gerçekliği
Kur, günlük bütçe (TL/USD), test günü, hedef geo, güncel CPI (kaynak + tarih),
ulaşılabilir install sayısı, gerekli örneklem.
**Bu bütçe şunu ölçebilir / şunu ölçemez.**

## Kampanya
Platform, geo, kreatifler, objective, ad set yapısı, süre.

## Ölçüm
Hangi metrikler, hangi eşiğe karşı, eşik nereden alındı.

## Karar kuralı
Önceden yazılır. Sonuç geldikten sonra eşik değiştirilmez.

## Ön kontrol
[ ] listesi
```

### `test-sonucu.md` (after)
```markdown
# Test Sonucu — [konsept] — [tarih]

## Harcama
Planlanan vs gerçekleşen, install sayısı, gerçekleşen CPI.

## Metrikler
Her metrik yanında örneklem ve güven aralığı ile.
| Metrik | Değer | n | Aralık | Eşik | Geçti? |

## Huni
Nerede düşüyor.

## Kreatif kırılımı
Kazanan hangisi, farkın anlamlı olup olmadığı.

## Karar
KILL / ITERATE / PITCH / SCALE — ve gerekçesi.

## Bu veriden çıkarılamayacaklar
Açıkça yazılır.

## Portföy durumu
Kalan bütçe, bu ayki test kapasitesi, sıradaki aday.
```

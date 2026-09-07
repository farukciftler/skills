# Monetization architecture

Read this when wiring ads, and again at G5 before scaling. Every rate figure in this domain is time- and geo-sensitive — pull current benchmark reports and state the date beside any number quoted to the user.

## Contents
- Model selection: pure IAA vs hybrid
- Mediation choice
- Placement design
- Rewarded video as a retention tool
- Revenue arithmetic
- Privacy and attribution wiring

---

## Model selection

Three shapes, in increasing order of durability:

1. **Pure IAA** — interstitials and rewarded only. Simplest to build, and the model the classic hyper-casual era ran on. Its weakness is structural: revenue is a direct function of session count, so weak retention caps earnings hard, and it competes for UA against titles with far higher LTV.
2. **IAA + remove-ads IAP** — one cheap non-consumable. Costs half a day to build and monetizes the small fraction of players who hate ads. Almost always worth including.
3. **Hybrid-casual: IAA + progression IAP** — a meta layer (upgrades, currency, cosmetics, chapters) that gives a reason to return and something to buy. Higher build cost, materially better retention and LTV, and closer to what the current market rewards.

Establish from a current source which of these the target category is actually paying for before committing — the answer moved substantially over the last few years and the honest reading may be that pure IAA no longer clears the UA bar in competitive geos.

At prototype stage build model 1 with the ad calls abstracted. The hybrid layer is a G5 decision made against measured retention, not a prototype feature.

---

## Mediation choice

Do not integrate a single ad network directly. Mediation with in-app bidding raises effective rates by making networks compete per impression, and single-network integration leaves money on the table and creates a fill dependency.

Main candidates — verify current market position, native iOS SDK support, and payment terms before choosing:

- **AppLovin MAX** — the default for this genre; deep bidding participation, strong casual demand.
- **Unity LevelPlay** (the merged Unity/ironSource stack) — the natural choice on a Unity build, and the path of least resistance if a publisher already runs it.
- **Google AdMob mediation** — easiest onboarding, reliable payouts, generally weaker in this specific vertical.

Decision heuristics: match the mediation to the engine and publishing path; if a publisher is involved, they will dictate it; if self-publishing native iOS, MAX is the usual starting point.

Practical setup notes:
- Enable in-app bidding for every network that supports it rather than hand-maintaining waterfalls.
- Add a handful of demand sources, not twenty — each adapter costs binary size, SDK risk, and a privacy-manifest surface.
- Set an eCPM floor only after there is real data; premature floors kill fill.
- Confirm payment threshold and payout mechanics for a Turkish entity before integrating, since this determines when money is actually receivable.

---

## Placement design

Placement is a retention decision disguised as a revenue decision. Over-monetizing a game with unproven retention destroys the thing being measured.

**Interstitials**
- Never during play, never on a control-adjacent tap target, never on cold start before the first play
- Fire at natural breaks: after a fail, after a level, on return to menu
- Gate with both a minimum session-time and a minimum inter-ad interval, both remote-configurable
- Exempt the first session or the first N levels entirely — early-session ad load is a known D1 killer
- Frequency is the single highest-leverage tunable in the whole build. Make it config, not a constant.

**Rewarded**
- The best-monetizing and least-damaging format, because the player opts in
- Design the reward into the mechanic: continue after fail, double the score, skip a hard level, unlock a cosmetic
- Offer it at the moment of loss, when motivation peaks
- Always show the value exchange before the ad, and always honor the reward even if the ad fails to load

**Banners**
- Generally not worth it in a full-screen game; low rates and real screen cost. Only consider on a menu screen if one exists.

At G4, keep monetization deliberately light. The test is measuring whether the game retains, and heavy ad load contaminates that measurement.

---

## Revenue arithmetic

Build the model transparently rather than quoting a headline number:

```
ARPDAU ≈ (impressions per DAU) × (eCPM / 1000)
LTV    ≈ ARPDAU × average lifetime in days   [dominated by the retention curve]
Payback: LTV must exceed CPI, with margin, in the same geo
```

Three points to make explicitly when presenting this:

- **eCPM varies by geo by an order of magnitude.** Tier-1 English-speaking markets versus low-CPM markets are different businesses. A test run in a cheap geo produces a valid retention read and an invalid revenue read. Never extrapolate revenue across geos.
- **Lifetime is set by retention, not by monetization.** This is why D1 gates everything upstream of eCPM tuning.
- **An LTV estimate needs weeks of real ad revenue at volume.** Anything computed from a few days and a small install cohort is an illustration, not a forecast, and should be labeled as one.

---

## Privacy and attribution wiring

Verify all of this against current Apple documentation — this stack has changed repeatedly and stale guidance produces both rejected builds and broken measurement.

- **ATT.** Prompt placement affects both opt-in rate and review risk. Prompt after the player has experienced value, never on cold start, and never with a misleading pre-prompt. Design the flow with `mobile-ux-flow-expert`.
- **Attribution framework.** Check the current status of SKAdNetwork versus AdAttributionKit, minimum OS versions, and which the chosen ad networks and mediation actually support today. Configure conversion values to encode the events that matter — early retention and rewarded engagement — rather than leaving defaults.
- **Consent.** A GDPR/CMP flow is required for EU traffic and many mediation SDKs ship one. If the test geos include the EU, this is not optional.
- **Privacy manifests.** Every ad adapter must carry one; audit after every SDK upgrade.
- **Nutrition labels.** Must match actual SDK behavior, including IDFA collection when ATT is authorized.

The measurement consequence worth stating plainly: post-ATT, install-level attribution is probabilistic and delayed. Small tests therefore give noisier signal than the dashboards suggest, which is another reason to weight in-app retention — which is measured directly and is not subject to attribution loss — above attributed CPI.

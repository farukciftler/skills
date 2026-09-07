---
name: hypercasual-lab
description: Ship and test hyper-casual / hybrid-casual iOS games on a small budget — live trend scanning for mechanics worth building, ad-creative-first validation, the Unity vs native SpriteKit decision, ad mediation and monetization wiring (AppLovin MAX, Unity LevelPlay, ATT, interstitial and rewarded cadence), and a gated CPI + retention test protocol with explicit kill criteria. Use whenever the work is a small mobile game meant to earn from ads — what to build, whether a concept is worth building, how to structure the app, how to wire ad SDKs, how much to spend testing, self-publish vs pitching Voodoo/Homa/Supersonic, or reading test results. Trigger on "hypercasual", "hyperscaler oyun", "hiper kazüel", "basit oyun yapıp para kazanmak", "reklam gelirli oyun", "CPI testi", "oyun trendi araştır", "bunu klonlasam olur mu", "publisher'a göndereyim mi", "günlük X TL bütçeyle oyun test etmek", "D1 retention kaç olmalı". Use it even when they only say they want a quick game that makes money.
---

# Hypercasual Lab

A pipeline for turning a small, fixed marketing budget into an honest yes/no on a game concept — fast, and with the kill decision made before the money is gone.

The whole discipline is one idea: **the ad is the product; the game is what happens after the ad works.** Studios that lose money build the game first and then discover nobody clicks. This skill inverts that order and puts a kill gate between every stage.

Write user-facing deliverables in Turkish. Keep internal reasoning and file structure as specified here.

---

## Before anything: the staleness rule

Every number in this market moves quarterly — CPI, eCPM, mediation shares, which publishers are still accepting submissions, which SDK version Apple requires, what the FX rate makes a TL budget worth in USD. **Do not state a benchmark from memory as if it were current.** Verify, then attribute with a date.

Anchor points that exist in this file are order-of-magnitude sanity checks only, marked as such. If a decision turns on a number, go get the number. `references/trend-scan.md` lists where each class of number actually lives.

Two things to verify at the start of every session that involves money:
1. **Live TRY/USD rate** — the whole budget protocol is denominated in TL but every ad platform and benchmark is in USD.
2. **Whether the person's daily budget clears the platform minimum** in the geos being considered. A budget that can't buy a statistically readable sample is not a small test, it's a donation.

---

## The pipeline

Six gates. Each gate has a kill criterion. Never skip a gate to save time — skipping Gate 2 is how a month disappears into a game nobody wanted.

```
G0 Trend scan      → 5-10 candidate mechanics, evidence-backed
G1 Concept + ad    → the 15-second ad script, written before any code
G2 Creative test   → does anyone click? (no game exists yet)
G3 Prototype       → 3-7 days, architecture per decision table
G4 CPI + D1 test   → the real budget burn
G5 Verdict         → kill / iterate / pitch / scale
```

### G0 — Trend scan

Produce a ranked candidate list, not a vibe. Read `references/trend-scan.md` for the source list and the scoring rubric; run the searches live rather than recalling what was trending.

What you are hunting for is a **mechanic with a proven ad hook that has not yet been saturated on the App Store**. Three signals must co-occur:
- The hook is visible in currently-running ad creative (someone is spending money on it right now)
- The chart position is rising, not established (an established #3 is a competitor, not an opportunity)
- The build is small enough that a prototype is days, not months

Output: `konsept-adaylari.md` — each candidate with the evidence link, the mechanic in one sentence, the ad hook in one sentence, a saturation read, and a build-days estimate.

**Kill criterion:** fewer than 3 candidates survive → the scan was too narrow, widen the source set rather than lowering the bar.

### G1 — Concept and ad script

Pick one candidate. Now write the ad before the game:

- A 15-second vertical script, shot by shot, with the hook landing in the **first 2 seconds**
- The single visual moment that makes someone stop scrolling — name it explicitly
- The "will I fail?" tension: hyper-casual creative works on anticipated failure, not on success
- Three variants of the same hook, because a single creative tells you nothing

If the ad script is boring to write, the game will be boring to play. That is not a metaphor — kill here and it costs nothing.

Hand creative production to the person's existing skills: `trend-setter` for the hook copy and platform-native framing, `post-forge` for static and carousel assets, `physics-reel-forge` when the hook is a simulation the engine can actually render, `procedural-game-audio` for the audio bed.

Output: `reklam-senaryosu.md` with 3 variants.

### G2 — Creative test (the cheapest gate)

Test the ad **before the game exists**. This is the highest-leverage step in the entire pipeline and most people skip it.

The test buys attention, not installs: run the three variants as video views or traffic, measure hook retention (3-second view rate), CTR, and CPM. The link can point to a coming-soon page or a placeholder store listing — the click is the signal, the destination is not the point.

Budget: a fraction of the daily figure, over 3-4 days. Full mechanics, thresholds and geo choice in `references/test-protocol.md`.

**Kill criterion:** none of the three variants beats the current category CTR baseline (verify it live) → go back to G0. Do not build. Do not tell yourself the game will fix it. The ad is the product.

### G3 — Prototype

Only now does code exist. Read `references/architecture.md` before writing any of it — the Unity vs native decision is genuinely load-bearing and depends on which publishing path is in play:

| Path | Engine | Why |
|---|---|---|
| Publisher pitch (Voodoo / Homa / Supersonic / CrazyLabs / Rollic / TapNation) | **Unity** | Their SDKs, prototype templates and analytics packages are Unity-first. A native prototype cannot be onboarded into their test infrastructure without a rewrite. Verify each publisher's current requirement before committing. |
| Self-publish, iOS-only, speed matters most | **Native SpriteKit + GameplayKit** | For someone already fluent in Swift, a 2D single-mechanic prototype ships materially faster, the binary is small, and AppLovin MAX / AdMob ship first-class native iOS SDKs. No engine tax. |
| Self-publish but Android is planned | **Unity** | Porting a native prototype is a second build, not a port. |
| The mechanic is 3D physics or needs a scene graph | **Unity** | Do not fight this one with SceneKit/RealityKit for a shipping ads game. |

Default when the path is undecided: **build the prototype native if the mechanic is 2D and the goal is a fast self-publish read; build Unity the moment a publisher pitch is realistic.** Making this call early is cheap; making it at G5 costs the whole build.

Scope discipline for the prototype: one mechanic, three levels or an endless loop, no meta systems, no accounts, no settings screen. It exists to answer "do people play past 30 seconds", nothing else.

**Non-negotiable before the build is considered done:** analytics instrumentation and the ad SDK stubs. A prototype that ships without D1 tracking produces an untestable build and wastes the entire G4 budget. See `references/monetization.md`.

**Kill criterion:** the prototype exceeds the build-day estimate by more than 2x → the concept was mis-scoped, stop and re-scope rather than sunk-cost forward.

### G4 — CPI and retention test

This is where the daily budget goes. Full protocol, geo selection, sample-size math and instrumentation checklist in `references/test-protocol.md`.

The essential structure:
- Pooled budget over a short burst, not a trickle over a month — a trickle never reaches a readable sample
- One campaign, the winning creatives from G2, geo chosen so the budget buys enough installs to read D1 at all
- Metrics that matter, in priority order: **D1 retention → playtime per session → CPI → D7 retention**
- Retention before CPI. A cheap install into a game nobody reopens is worse than no install.

Be honest in the write-up about what the budget can and cannot buy. A small daily budget can buy a **retention read in a cheap geo** and a **relative CPI comparison between creatives**. It cannot buy a Tier-1 CPI benchmark, and it cannot buy an LTV read — LTV needs weeks of ad revenue data at volume. Saying this plainly is more useful than producing a confident number from a 40-install sample.

### G5 — Verdict

Produce `test-sonucu.md` with the numbers, the confidence interval given the sample size, and one of four calls:

- **Kill** — most concepts land here. Say it directly and move to the next candidate. The pipeline's value is in how quickly it kills.
- **Iterate** — retention is close but the first 30 seconds leak. One specific fix, one re-test, capped at one round.
- **Pitch** — retention clears the publisher bar. Submit the prototype video to publishers and let them fund the Tier-1 CPI test on their infrastructure. This is the capital-efficient path on a small budget and should be actively recommended when the numbers support it. See `references/test-protocol.md` for the submission bar and current publisher list.
- **Scale** — self-publish, wire full monetization, ASO, and raise spend against measured payback.

Then set expectations on the portfolio math: this is a hit-rate business, not a project business. Concepts get killed at a high rate at every gate, and the budget should be planned as *N concepts tested per month*, not *one game funded*. Compute that N from the person's actual monthly budget and state it.

---

## Handoffs to adjacent skills

Do not reimplement work these already do:

- `aso-expert` — store listing, keyword field, screenshots, conversion once G5 says scale
- `appstore-market-analyst` — category economics, pricing, what a genre realistically earns
- `apple-platform-architect` — anything deep on Swift, SpriteKit, App Review, device capability
- `mobile-ux-flow-expert` — onboarding, ATT prompt placement, paywall and permission flows
- `trend-setter` / `post-forge` / `physics-reel-forge` — ad creative production
- `procedural-game-audio` — zero-asset audio for the prototype
- `serverim-build` — if a landing page, coming-soon page or analytics backend is needed

## Failure modes to name out loud

The person is spending real money, so say these when they apply rather than being agreeable:

- **Building before G2.** The most common and most expensive mistake.
- **Cloning a saturated chart-topper.** By the time a mechanic is at #3, the CPI to compete against an incumbent's scale is not payable on a small budget. Also invites App Store 4.3 rejection.
- **Reading a 40-install sample as a result.** Report the sample size next to every metric and refuse to draw conclusions the sample cannot support.
- **Optimizing monetization before retention.** eCPM tuning on a game with weak D1 is arranging furniture in a burning room.
- **Trickling the budget.** Long thin campaigns never converge and burn the same money for no signal.
- **Treating the whole budget as one concept's budget.** It is the portfolio's budget.

## Turkey-specific operational notes

Relevant because the money question is the point, but flag these as things to confirm with an accountant rather than as advice: App Store payout mechanics and thresholds, the tax treatment of foreign app revenue for a şahıs şirketi, the young-entrepreneur exemption if applicable, and whether ad platform spend in TRY carries VAT/withholding that changes the effective budget. Get the current position from a muhasebeci — the rules here change and a wrong assumption distorts every payback calculation in the plan.

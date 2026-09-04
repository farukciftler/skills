# Monetization and Scoring

Read this in Phases 4 and 5. The first half is what actually pays; the second half is how to rank candidates without hand-waving.

## Contents
- The uncomfortable base rate
- Ten models, ranked by how often they work
- Modelling the arithmetic
- The scoring rubric
- Using the score script
- Dossier detail

---

## The uncomfortable base rate

The outcome distribution in this category is extremely skewed. A small number of properties reach millions of users; the overwhelming majority of well-built entries get a few thousand visitors from the builder's own network and stop. The famous examples are famous because they are rare, and every one of them is quoted in every article about the genre precisely because there aren't many.

So: **model the base case, and say the base case out loud.** A dossier that projects Instafest numbers is worthless. A dossier that says "the realistic outcome is 5,000–50,000 artifacts generated, here is what that earns under each model, and here is what would have to be true for the tail outcome" is useful and buildable-against.

Two structural facts to carry into every model:

**The spike has a half-life of about three days.** Whatever you're going to capture, you capture it in the first week. Design the capture mechanism *before* launch, not after the traffic arrives — the single most common regret in this category is "I got 200,000 visitors and had no email capture, no upsell, and no next thing to send them to."

**Turkish ad traffic does not pay.** Directionally an order of magnitude below US RPM. This one fact eliminates model 8 below for TR-only audiences, and it eliminates it *quietly* — people discover it after launch. Flag it every single time it applies.

## Ten models, ranked by how often they work

### 1. Funnel into a product you already own
The strongest and most under-used. The artifact is free and costs nothing to give away; its job is to put your real product's name in front of hundreds of thousands of people who match its audience. Works because you're not trying to monetize the spike at all — you're buying attention at a cost per impression nobody else can match.

Requires: an existing product with an overlapping audience. Measure: installs/signups attributable to the artifact, not artifact count.

### 2. Seasonal brand sponsorship
Sell the artifact as a campaign asset. A property with a predictable annual peak and a demonstrated audience can be pre-sold to a brand months out — and the second year is much easier to sell than the first, because you have last year's numbers. In Turkey this is the most realistic path to meaningful money from a purely local audience, because it prices attention directly rather than through ad networks.

Requires: one year of proof, a clean audience story, and a format that survives a sponsor's logo without becoming an ad. Watch the tension: the more you brand it, the less people share it.

### 3. Wrapped-as-a-service (B2B)
Turn the machinery into a product sold to companies that want their own recap campaign for their customers, members, students, or employees. This is a real and growing market — several vendors sell personalized year-in-review campaign platforms — and it is where the engineering you built for the consumer toy actually becomes defensible.

Requires: enterprise sales patience and a data-handling story that passes a procurement review. Highest ceiling on this list, slowest to reach.

### 4. Physical products
Print-on-demand posters, canvas, mugs, stickers of the artifact. The receipt, certificate, poster and map formats are natural physical objects, and a small share of people will pay for a nice printed version of something they already love. Turkey has cheap, fast local production, which makes this genuinely better here than in the US.

Requires: fulfilment logistics and a design that survives at print resolution (render at print DPI from the start, not upscaled). Watch IP: don't sell prints made of somebody else's album art or club crest.

### 5. Paid upgrade on the artifact
No watermark, high resolution, extra themes, more items, animated or video export, the full report instead of the summary. The classic one-time in-app purchase. Conversion is low — most people want the free image and nothing else — but the cost of offering it is nearly zero, so it belongs in almost every build.

Price it as an impulse: the decision must be faster than the artifact took to generate.

### 6. Subscription on ongoing stats
Convert a one-shot artifact into a real analytics product with recurring value (stats.fm is the canonical example). The only model on this list that produces durable MRR from the consumer directly. Also the highest bar — it requires ongoing data access, which is exactly the thing platforms keep revoking.

### 7. Affiliate and commerce
Route the audience to something they were going to buy anyway: concert tickets for their top artist, the book they just finished, the game they play most. Fits naturally with the artifact's content, requires no payment infrastructure of your own, and pays poorly per user but scales with the spike.

### 8. Display advertising
Works only at genuine scale and only with Western traffic. For a Turkish audience, assume it does not clear. Include it in a dossier as a rounding-error supplement, never as the plan.

### 9. Sell the property
A daily-game or artifact property with real recurring numbers is an acquirable asset — media companies buy these. Not a plan you can execute toward, but worth naming when a candidate has an unusually clean daily loop and a proprietary dataset.

### 10. Data and API resale
Aggregate insight sold to a third party. Almost always the wrong answer here: it conflicts with the privacy-first design that makes these apps safe to ship, it usually violates the source platform's terms, and under KVKK it turns a trivial project into a regulated one. Name it to dismiss it, and recommend against it explicitly if the person raises it.

## Modelling the arithmetic

For each candidate, write the chain out. Vague monetization claims are the main way a dossier becomes useless.

```
Visitors (base / good / tail case)
  × artifact completion rate      (how many actually finish and get an image)
  × share rate                    (how many post it — this is your viral coefficient input)
  → secondary visitors            (the loop)

Total artifacts
  × conversion to paid            (be pessimistic; single-digit percent at best for impulse upgrades)
  × price
  − per-artifact cost             (LLM tokens, image gen, bandwidth, storage)
  − fixed cost                    (hosting during the spike, domain, store fees, fulfilment)
  = the actual number
```

State the assumptions as assumptions and mark them `[NEEDS DATA]` where they can't be observed. Then compute the base case and say whether it clears the person's bar. Frequently it won't, and saying so is the whole value of the exercise — it redirects them to model 1 or 2, which is usually where the real answer was.

Cost discipline note: any per-artifact variable cost must be stress-tested against the tail case. A model that earns nothing and costs money per generation turns a viral hit into a bill.

## The scoring rubric

Six factors, 1–5 each, weighted. Score every surviving candidate; show the table in the dossier so the ranking is inspectable.

| Factor | Weight | 1 | 5 |
|---|---|---|---|
| **Feasibility** — can you legally get the data, today, as a small builder | 3 | Closed API, no fallback | Public/owned/user-supplied data, no permission needed |
| **Virality** — how many of the five ingredients from `01-artifact-anatomy.md` it has | 3 | Weak status signal, poor legibility, no comparability | All five, borrowed visual grammar, strong comparability |
| **TR gap quality** — Phase 3 diagnosis | 2 | Cause 1–3 (dead) | Cause 6, evidenced |
| **Money path** — realistic model fit | 2 | Ads on TR traffic only | Model 1, 2, or 3 with a plausible route |
| **Build cost** — effort to a shippable v1 (inverted: 5 = cheap) | 2 | Months, complex infra, per-user cost | A weekend, static render, no backend state |
| **Durability** — survives a platform policy change and has a recurrence pattern | 1 | Single fragile API, one-shot | No dependency, daily or seasonal loop |

Weighted maximum is 65. Rough reading: **≥50** is a strong candidate worth a build slot; **40–49** is worth a prototype; **below 35** should be in the eliminated list with a one-line reason.

**The feasibility veto.** A candidate scoring 1 on feasibility is eliminated regardless of its total. This overrides the weighted score deliberately: a brilliant artifact with no legal data path is not a 35/65 "maybe", it is dead, and letting a high virality score average it back into contention is exactly how a dossier ends up recommending a Spotify clone in 2026. The script enforces this.

Feasibility and virality carry the heaviest weight deliberately. Feasibility because it is the modal cause of death in this category; virality because an artifact nobody posts is just an app with no users.

Do not fudge scores to reach a desired ranking. If everything scores low, the honest report is "this category is picked over, here are the two TR-native plays that aren't."

## Using the score script

`scripts/score.py` computes and ranks so the weights are visible and the arithmetic is reproducible.

```bash
python3 scripts/score.py candidates.json
```

Input format:

```json
[
  {
    "name": "Fikir adı",
    "feasibility": 4,
    "virality": 5,
    "tr_gap": 5,
    "money": 3,
    "build": 4,
    "durability": 3,
    "note": "tek cümle gerekçe"
  }
]
```

It prints a ranked markdown table with weighted subtotals and the verdict band, ready to paste into the dossier. Run it with `--explain` to include the per-factor weighted contributions when the person wants to see why one candidate beat another.

## Dossier detail

Beyond the structure in SKILL.md, each opportunity entry needs these specifics or it isn't actionable:

- **The artifact in one sentence.** Literally describe the image. "A thermal-receipt-shaped PNG listing the user's ten most-watched dizi with episode counts as prices and a total at the bottom." If you can't write that sentence, the idea isn't finished.
- **The first-week plan.** Who posts it first, into which community, in what week of the calendar. In this category the launch matters more than the build, and a great artifact posted into silence is worth nothing. Hand off to `trend-setter` for the actual seed content.
- **The killer risk.** One thing, named. The single most likely cause of death: usually a policy change, a cost per artifact, or a status signal that doesn't actually read.
- **The falsification test.** What you'd see within two weeks that means it isn't working, so the person stops instead of grinding. Typically: share rate below some threshold, or no organic posts from strangers.

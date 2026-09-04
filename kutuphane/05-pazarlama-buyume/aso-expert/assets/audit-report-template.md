# ASO Audit — [App name]

**Store(s):** [App Store / Google Play] · **Storefronts:** [markets]
**Date:** [date] · **Prepared by:** [name]

**Data this audit is built on:** [App Store Connect analytics, [date range] / Play Console
acquisition report / public store page only]
**What could not be assessed without further access:** [list — be specific. If this is a
public-data audit, say so here in one clear sentence.]

---

## 1. Verdict

Three to five sentences. What is actually wrong, what it is costing, and what the single
highest-value fix is. If the constraint is the product rather than the store presence —
rating, retention, differentiation — say it here.

---

## 2. Funnel diagnosis

| Stage | Current | Category context | Read |
|---|---|---|---|
| Impressions (unique) | | | |
| → Product page views | % | | |
| → First-time downloads | % | | |
| Store-reported CVR | % | | |

**The problem lives in:** [visibility / first impression / page conversion]

Why, in a short paragraph. Note explicitly which stage each recommendation below targets —
the most common failure in ASO work is fixing the stage that wasn't broken.

Traffic split by source (search / browse / referral), and what it implies.

---

## 3. Current state

### Metadata (per store, per locale)

| Field | Current | Chars | Issue |
|---|---|---|---|

### Creative
Icon, first three screenshots, video presence, caption legibility at thumbnail scale.

### Ratings and reviews
Rating per store and per key country, volume, 1–2★ share, response rate, recurring
complaint themes now surfacing in the AI review summaries.

### Technical (Android)
Android vitals against Google's documented thresholds (crash ≥1.09%, ANR ≥0.47% of daily
users). Exceeding these makes the app less discoverable regardless of metadata work.

---

## 4. Keyword position

Current ranked keywords weighted by volume, brand vs non-brand split, share of voice
against the competitor set, and the keyword gap — terms where ≥2 competitors rank top 10
and this app does not rank at all.

[Attach the keyword matrix as a spreadsheet; do not inline more than ~15 rows here.]

---

## 5. Recommendations

### Ship now — no release required
| # | Action | Expected effect | Confidence | Effort |
|---|---|---|---|---|

*(promotional text, in-app events, review responses, CPP keyword assignment, Play listing
edits, tag selection)*

### Next release
| # | Action | Expected effect | Confidence | Effort |
|---|---|---|---|---|

*(title, subtitle, keyword field, description, screenshots)*

### Next quarter
| # | Action | Expected effect | Confidence | Effort |
|---|---|---|---|---|

*(localization, rating repair, test programme, AI/editorial visibility)*

---

## 6. Test queue

| Priority | Hypothesis | Variable isolated | Mechanism | Metric | Expected lift | Sample needed | Feasible? |
|---|---|---|---|---|---|---|---|

If the app's traffic cannot detect the effect size in a reasonable window, say so here and
recommend shipping on judgment instead — an underpowered test that "loses" is worse than no
test, because teams treat it as evidence.

---

## 7. Measurement plan

What will be tracked, at what cadence, and how each recommendation above will be judged.
Name the attribution method (on-store A/B test / geo holdout / synthetic control / annotated
pre-post) and its known weaknesses. Note any inventory or platform change that requires
re-baselining.

---

## 8. Assumptions, risks and open questions

- Claims marked **documented** come from Apple/Google primary sources.
- Claims marked **measured** carry a date; ASO benchmarks decay fast.
- Claims marked **practitioner consensus** have no published test behind them.
- Metadata tactics carrying App Review or policy risk are flagged in-line above.
- No source publishes numeric ranking-factor weights for either store; none are used here.

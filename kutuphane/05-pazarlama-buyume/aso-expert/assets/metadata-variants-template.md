# Metadata variants — [App name] · [store] · [locale]

**Current state:** [what's live now, with character counts]
**Target keywords for this locale:** [the clusters this metadata set is trying to win]
**Constraint check:** brand name required in title? y/n · release scheduled? [date] ·
keyword field changes only take effect when a version ships live (iOS)

---

## Variant A — [one-line label, e.g. "brand-led, defensive"]

**Hypothesis:** what this variant is betting on, and what it gives up.

| Field | Copy | Chars | Limit |
|---|---|---|---|
| App name | | | 30 |
| Subtitle | | | 30 |
| Keyword field | | | 100 |

**Keywords captured:** [list, noting cross-field permutations this enables]
**Keywords sacrificed:** [list]
**Review risk:** [none / flag with the specific guideline]

---

## Variant B — [label, e.g. "category-led, aggressive"]

*(same structure)*

---

## Variant C — [label]

*(same structure)*

---

## Recommendation

Which variant, and why — in terms of the funnel stage it targets and the risk the client is
being asked to accept. Note what you would test if testing were possible (Apple cannot A/B
test metadata at all; Google Play can test short and long description but **not** the title).

---

## Description / long description

**iOS:** not indexed for search. This is conversion copy — and, since 2025, input to Apple's
LLM-generated App Store Tags. First three lines carry almost all the weight; roughly 1% of
users read further.

**Google Play:** indexed and a primary ranking input, *and* read by Ask Play to answer user
questions. Write it as structured, factual capability documentation: front-load positioning,
be explicit about what the app does and does not do, cover pricing, platforms and use cases
plainly. Primary keywords ~3–5 natural repetitions, secondary 1–3 — a guardrail against
stuffing, not a lever. Google's own instruction is "use everyday language, not a list of
keywords."

**The same description cannot be optimal for both stores.** Write two.

---

## What ships when

| Change | Gate | Date |
|---|---|---|
| Promotional text (170) | none — live immediately | |
| CPP keyword assignment | none — no App Review | |
| Play listing edits | none | |
| Title / subtitle / keyword field / screenshots (iOS) | next release | |

**Measurement:** baseline captured [date]; iOS rankings stabilize ~4 weeks after a build goes
live; Android needs 6–8 weeks between changes. Do not change metadata and creative in the
same window — you lose attribution.

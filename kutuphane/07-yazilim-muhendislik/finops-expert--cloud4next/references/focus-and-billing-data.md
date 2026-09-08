# FOCUS and provider billing data

**As of: 2026-09-07.** FOCUS version numbers, column additions and provider export feature
names are **volatile — `~verify`** against focus.finops.org and provider docs before quoting.
The conceptual content (cost metrics, credits, why totals never tie) is stable.

## Why FOCUS exists

Every provider bills in its own shape: different column names, different granularity, different
meaning for the word "cost". Before FOCUS, every multi-cloud FinOps team wrote and re-wrote the
same normalization layer. **FOCUS (FinOps Open Cost and Usage Specification)** is the open
standard for that layer — a common schema so one query works across providers.

Practical status `~verify`: v1.0 reached GA in 2024; later minor versions have extended coverage
(SaaS and non-cloud spend among them), and all three hyperscalers publish or preview
FOCUS-conformant exports. Adoption is real but **partial** — providers add `x_`-prefixed
vendor-specific columns alongside the standard ones, so a FOCUS export is standard-plus-extras,
not a drop-in replacement for provider-native detail.

### Core column concepts

The columns worth knowing by meaning (exact names `~verify`):

| Concept | What it means | Why it matters |
|---|---|---|
| `BilledCost` | What lands on the invoice for the period | Ties to what finance pays |
| `EffectiveCost` | Amortized cost including commitment purchases spread over their term | The number for **trend and unit economics** |
| `ListCost` | Cost at public list rate, no discounts | Denominator for savings rate |
| `ContractedCost` | Cost at negotiated rate before commitment amortization | Isolates negotiated vs commitment discount |
| `ChargeCategory` | Usage / Purchase / Tax / Credit / Adjustment | **Filter this or your totals are wrong** |
| `ChargeClass` | Whether the row is a correction to a prior period | Retroactive corrections silently change closed months |
| `ServiceName` / `ServiceCategory` | Normalized service naming | The whole point of the standard |
| `ResourceId` / `ResourceName` | The billed resource | Join key to inventory |
| `Tags` | Normalized tag/label map | Allocation |

**The single most valuable thing FOCUS gives you** is a consistent definition of amortization
and discount across clouds — the thing teams most often get wrong when hand-rolling.

## The cost-metric minefield

Mixing these is the commonest FinOps reporting bug. Name the one you are using, every time.

- **Unblended** — the rate actually charged to that account at that moment. Spiky: a commitment
  purchase lands as one large charge. Right for reconciling to an invoice line; wrong for trends.
- **Blended** — averaged across a consolidated org. Almost never what you want; it obscures which
  account benefited.
- **Amortized / effective** — commitment purchases spread across their term. **The default for
  trend analysis, unit economics and forecasting.**
- **List / on-demand equivalent** — no discounts. Only as a savings denominator.
- **Net vs gross** — net deducts credits. Decide once, org-wide, and label every chart.

⚠ **The comparison trap.** Comparing your *effective* cost (discounts applied) against another
platform's *list* price systematically overstates the gap. This is the standard way migration
business cases mislead, including honestly-intended ones. Whenever both sides are not on the
same metric, say so in the output.

## Provider exports — the practical quirks

**AWS — Cost and Usage Report / Data Exports** `~verify feature names`
- Hourly and resource-level detail; CUR 2.0 is the current shape, delivered via Data Exports.
- **Restated continuously through the month** and can be adjusted after close — a "final" number
  taken mid-month is not final. Deduplicate on re-delivery (this platform has a dedicated
  `aws_billing_dedup` table for exactly that).
- Savings Plans and RI rows need care: the purchase, the amortization and the covered usage are
  distinct rows. Naive `SUM(cost)` double-counts.

**GCP — BigQuery billing export**
- Standard vs **detailed** export differ: only the detailed one carries resource-level rows.
- Requires the export dataset **and** the table to be configured; a missing table name yields a
  silent query failure rather than an obvious error (see cloud4next-platform.md).
- Credits arrive as a repeated field, so gross vs net is an explicit unnesting decision, not a
  column choice.

**Azure — cost exports**
- EA / MCA / PAYG differ in available fields; **currency fields exist only on MCA**.
- Amortized and actual are **separate exports** — you cannot derive one from the other after the fact.
- FOCUS-shaped exports rename things and add `x_`-prefixed Azure-specific fields; code that
  pattern-matches on legacy column names breaks silently when a tenant switches export type.
- Export granularity is often **daily**, not hourly — anything hourly downstream is an
  interpolation, and you should say so rather than implying hourly truth.

## Why your totals never tie

Expect and explain these, rather than hunting a bug that is not there:

1. **Timing** — provider day boundaries are UTC; your reporting timezone probably is not.
2. **Restatement** — prior periods change after close.
3. **Credits, refunds, tax, support** — in or out, and support is often a percentage of a moving base.
4. **Currency** — FX applied at what rate, on what date. Multi-currency accounts must stay separate series, never summed.
5. **Unmapped line items** — resource-level views drop rows that have no resource id (tax, support, marketplace). This is the reason org totals built from resource series come out low.
6. **Marketplace and third-party charges** — on the invoice, frequently absent from the usage export.

Rule: reconcile **to the invoice** once per month deliberately, and keep the delta as a known,
explained quantity. A pipeline that has never been reconciled is not trustworthy no matter how
clean its dashboards look.

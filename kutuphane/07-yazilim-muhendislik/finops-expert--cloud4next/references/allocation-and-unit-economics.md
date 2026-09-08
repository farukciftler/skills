# Allocation, showback/chargeback and unit economics

**As of: 2026-09-07.** Stable practitioner knowledge; no volatile facts here.

## Allocation is the foundation — everything else rests on it

If engineers do not believe the numbers, no optimization conversation goes anywhere. Treat
allocation quality as a product, with a KPI (**unallocated cost %**) and an owner.

### Tagging strategy

Keep the **mandatory** set small enough that it is actually enforced. A ten-tag policy at 40%
compliance allocates less than a four-tag policy at 95%.

A workable minimum: **owner** (team, not a person who will leave) · **environment**
(prod/staging/dev) · **cost-center or business-unit** · **application/service**.

Rules that matter more than the tag list:
- **Enforce at creation**, not by cleanup — policy-as-code in the provisioning path (SCP / Azure Policy / Org Policy), plus CI checks on IaC. Retroactive tagging is endless.
- **Controlled vocabulary.** `prod`, `Prod`, `production` and `prd` are four cost centers. Validate values, not just presence.
- **Tags are not retroactive.** Tagging a resource today does not re-tag last month's billing rows. Every tag rollout has a permanent "before" period — state it instead of letting people wonder why history looks wrong.
- **Know your limits and gaps.** Tag counts and character rules differ per provider; some resource types accept no tags at all, and some billing line items (tax, support, marketplace, inter-region transfer) never carry one. That residue is structural, not a compliance failure.
- **Account/subscription/project structure is the more durable allocation axis.** Where a boundary is stable and important, an account boundary beats a tag: it cannot be un-set by a developer.

### Unallocated cost

Split it before reporting a single number — the causes need different owners:

| Cause | Owner | Fix |
|---|---|---|
| Untagged resources | Engineering | Enforcement at creation |
| Untaggable resource types | Platform | Shared-cost model |
| Non-resource charges (tax, support, marketplace) | Finance | Explicit allocation rule |
| Shared infrastructure | Platform | Splitting rule (below) |

Reporting "12% unallocated" without this breakdown invites the wrong fix.

## Shared and common costs

Shared cost (network, cluster control planes, observability, support, the platform team's own
infrastructure) is where allocation models get argued. Options, worst to best in most orgs:

1. **Leave unallocated** — honest, but leaves a growing bucket nobody owns.
2. **Even split** — simple, wrong at the edges, breeds resentment from small teams.
3. **Proportional to direct spend** — the common default. Easy to compute, easy to explain, slightly punishes efficient teams (they shrink their direct spend and inherit a bigger share of overhead — say this out loud rather than pretending it is neutral).
4. **Usage-based** — split by an actual driver (cluster CPU-hours, log GB, request count). Most defensible, needs real telemetry. This is what OpenCost provides for Kubernetes.

**Pick one, write it down, and keep it stable.** Switching models mid-year makes every trend
line meaningless; if you must switch, restate history or clearly mark the break.

## Showback → chargeback

- **Showback**: teams see their cost, no money moves. Almost always the right starting point, and often the right ending point.
- **Chargeback**: cost actually hits the team's budget. Real behaviour change, real overhead, and it hardens every disagreement about allocation into a financial dispute.

Do not attempt chargeback until: allocation is credible (unallocated low and trending down), the
shared-cost model is agreed in writing, teams have the levers to actually reduce their cost, and
there is a dispute process. Chargeback on a shaky Inform layer is the single most reliable way to
destroy a FinOps practice's credibility.

## Unit economics — the part leadership actually wants

Total cloud spend rising is not, by itself, bad news. **Cost per unit of business value** is the
metric that separates growth from waste.

Choosing the denominator:
- It must be something the business already tracks and believes (active customer, order, ride, GB ingested, API call, model inference).
- It must move with the workload. A denominator that is constant just re-plots total cost.
- One per product line beats one company-wide number.

Practice:
- Use **amortized/effective** cost, never unblended — commitment purchases would otherwise create phantom unit-cost spikes.
- Publish the **trend**, not the level. Cross-company unit cost comparisons are close to meaningless; your own slope is the signal.
- Separate **fixed platform cost** from **variable per-unit cost**, or early-stage products look catastrophic and growth looks free.
- Where possible, carry it to **margin**: cost per unit against revenue per unit is the version an executive can act on.

**Cost-per-X falling while total spend rises is a healthy business.** Being able to show that,
with a denominator finance trusts, is the highest-leverage artifact a FinOps practice produces.

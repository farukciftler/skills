# FinOps Framework, operating model and KPIs

**As of: 2026-09-07.** Framework *structure* is stable knowledge. Specific capability counts and
certification names shift between annual revisions — mark those `~verify` when load-bearing.

## The three phases (the part that actually changes behaviour)

**Inform → Optimize → Operate**, iterative, not sequential-once. The commonest failure in real
practices is jumping to Optimize with an Inform layer nobody trusts: engineers dispute the
numbers, the savings never land, and the practice loses its mandate. **Allocation credibility is
the prerequisite for every optimization conversation.**

| Phase | Question | You are done when |
|---|---|---|
| Inform | Who spent what, on what, and is that visible to them? | Each team can see its own cost without asking finance, and does not dispute it |
| Optimize | What should change, and what is it worth? | Recommendations reach an owner with an SLA, not a dashboard nobody opens |
| Operate | How does this become routine? | Anomalies, budgets and reviews run on a cadence without a person driving them |

## Domains and capabilities

Post-2024 the Framework groups capabilities into four domains:

1. **Understand Usage & Cost** — data ingestion, allocation, reporting & analytics, anomaly management
2. **Quantify Business Value** — planning & estimating, forecasting, budgeting, benchmarking, unit economics
3. **Optimize Usage & Cost** — architecting for cloud, rate optimization (commitments), workload optimization, licensing & SaaS, sustainability
4. **Manage the FinOps Practice** — practice operations, education & enablement, policy & governance, invoicing & chargeback, onboarding workloads, intersecting disciplines (ITAM, ITSM, security, sustainability)

`~verify` the exact capability list against finops.org before quoting it as canonical; the
grouping has been revised more than once.

## Personas — and how to pitch to each

| Persona | Cares about | What lands | What fails |
|---|---|---|---|
| Engineering | Shipping; not being blamed | Cost in their own tooling, at the resource they own, with a fix they can apply | A monthly spreadsheet from finance |
| Finance | Predictability, accruals, variance | Forecast accuracy, amortized view, commitment liability | Unblended daily spikes |
| Procurement | Commitment and contract terms | Coverage, expiry ladder, negotiation leverage | Resource-level detail |
| Leadership | Unit economics, margin | Cost per customer/transaction and its trend | Total spend with no denominator |
| Product | Feature-level margin | Cost attached to a product line | Infrastructure-shaped reporting |

**The persona test for any FinOps artifact:** name who acts on it and what they do differently.
An artifact that fails this test is a report, not a control.

## Maturity: Crawl / Walk / Run

Maturity is **per capability**, never a single organizational score. A practice can be Run on
rate optimization and Crawl on allocation — that combination is common and is exactly the one
that produces impressive-looking savings nobody can attribute.

| | Crawl | Walk | Run |
|---|---|---|---|
| Allocation | Some tags; large unallocated bucket | Policy enforced on new resources; unallocated tracked as a KPI | Near-full allocation incl. shared cost; disputes rare |
| Forecasting | Last month × growth guess | Model-based, variance measured | Variance within a stated band, drives budget |
| Commitments | Ad-hoc purchases | Coverage and utilization tracked | Laddered portfolio, expiry-managed, target bands |
| Anomaly | Discovered on the invoice | Detected and alerted | Routed to an owner with time-to-resolution measured |

Practical rule: **do not advance a capability past the one it depends on.** Commitment
management above Walk while allocation is Crawl means savings you cannot attribute and
therefore cannot defend.

## KPI catalog

Pick few, define precisely, and keep the definition stable — a redefined KPI destroys its own
trend line.

**Allocation quality**
- *Unallocated cost %* — the single best health metric for the practice. Trend matters more than level.
- *Tag policy compliance %* — by resource **and** by cost; they differ wildly and the cost-weighted one is the honest one.

**Rate efficiency**
- *Commitment coverage %* — share of eligible spend covered. Target a band (commonly 70–85% for stable estates), never 100%.
- *Commitment utilization %* — share of purchased commitment actually consumed. Below ~95% is waste; this is the metric that catches over-buying.
- *Effective savings rate* — blended discount vs on-demand equivalent.

**Usage efficiency**
- *Idle/orphan cost* — unattached disks, unassociated IPs, stopped-but-billed resources.
- *Rightsizing opportunity, identified vs realized* — report both or neither.

**Forecast quality**
- *MAPE / forecast variance* over a stated horizon. A forecast without a published error band is an opinion.

**Business value**
- *Unit cost* (cost per customer / transaction / GB processed) and its **trend**. Absolute value is nearly meaningless across companies; the slope is the signal.

**Practice operations**
- *Anomaly mean time to resolution*, *% anomalies with an assigned owner*, *savings realized vs identified*.

## Running the practice

- **Cadence beats intensity.** A 30-minute weekly review that always happens outperforms a quarterly deep-dive that slips.
- **Every recommendation needs an owner and an expiry.** Unowned recommendations accumulate until the list itself is the problem.
- **Report realized savings against a baseline you wrote down in advance.** Retroactive baselines are how FinOps practices lose finance's trust.
- **Showback before chargeback.** Chargeback without a trusted allocation layer produces disputes that set the practice back further than doing nothing.
- **Do not let the tool define the practice.** Dashboards are Inform; the practice is what changes afterwards.

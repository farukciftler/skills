# FinOps KPIs

Formulas, realistic targets, and what to measure when. Targets are directional benchmarks from practitioner consensus — a "good" number depends on maturity, workload mix, and business model, so read trends rather than judging a single value.

## Contents
1. Selection principle
2. Allocation & accountability
3. Rate optimization
4. Usage efficiency
5. Planning accuracy
6. Unit economics
7. Practice health
8. What to measure at each maturity level
9. Dashboard design
10. The metric trap

---

## 1. Selection principle

A metrics program does not start with a list of 27 KPIs. Every KPI needs a **formula, an owner, a cadence, and a target**. Without an owner it's a number on a slide; without a target it can't be missed; without a cadence it decays.

Distinguish **metrics** (everything you can measure) from **KPIs** (the handful you've committed to targets on and report regularly). Five KPIs with owners beat twenty without.

Match review cadence to the decision cycle of the audience: operational metrics daily, efficiency and commitment metrics weekly, business alignment metrics monthly or quarterly.

## 2. Allocation & accountability

**Tag / label coverage**
`resources with all required tags correctly applied / total taggable resources`
Target 85%+ before trusting downstream metrics. Usually the single highest-leverage KPI to improve first — under ~80%, every other metric is contaminated by an unattributed bucket. Track *by team and account* to find enforcement gaps, not just the global number.

**Cost allocation rate**
`allocated cost / total cost`
Target 95%+ at Run. Different from tag coverage — includes rule-based and shared-cost allocation, not just tags. This is the number to report to finance.

**Unallocated / shared cost share**
`(shared + unallocatable cost) / total cost`
Target under 5–10%. Watch the trend: a growing shared bucket means new services are outrunning the allocation model.

**Showback/chargeback coverage**
`spend covered by a distributed report with a named owner / total spend`
The accountability metric. Showback informs; chargeback moves cost to the owner's P&L. Chargeback drives behavior change faster and provokes far more resistance — don't attempt it before allocation is trusted, or the first month is spent litigating the numbers instead of reducing them.

## 3. Rate optimization

**Commitment coverage**
`spend covered by commitments / commitment-eligible spend`
Target 70–85% for stable workloads. Note the denominator: eligible spend, not total spend. FOCUS 1.4's Commitment Program Eligibility Details column is what makes this computable properly across providers.

**Commitment utilization**
`commitment value actually consumed / commitment value purchased`
Target 95%+. Coverage and utilization are not the same thing and are frequently confused: coverage asks "how much of what could be discounted was," utilization asks "how much of what we bought did we use." High coverage with low utilization means you overbought.

**Effective Savings Rate (ESR)**
`(ListCost − EffectiveCost) / ListCost`
The single best summary of rate strategy. Decompose it into negotiated-rate savings and commitment savings when diagnosing. No universal benchmark: early practices see high rates from quick wins, mature practices plateau or decline as easy waste disappears. Read it alongside coverage and utilization, never alone.

**Commitment expiry exposure**
`commitment value expiring in next 90 days / total commitment value`
Not a target, a calendar. Missed renewals are among the most avoidable cost events in FinOps.

## 4. Usage efficiency

**Waste rate**
`idle + unattached + orphaned resource cost / total cost`
Target under 5%. Sources: unattached volumes, idle load balancers, stopped-but-billed instances, orphaned snapshots, unused elastic IPs, over-provisioned Kubernetes requests.

**Rightsizing opportunity**
`estimated savings from p95-based rightsizing / current compute cost`
Use p95 utilization, not average — average-based rightsizing causes incidents and permanently destroys engineering trust in FinOps.

**Non-prod cost ratio**
`non-production cost / production cost`
Target under 0.3 for most orgs. A high ratio is the easiest large win available: scheduling non-prod to business hours typically recovers 40–65% of off-hours cost with near-zero risk.

**Resource utilization**
`consumed capacity / provisioned capacity` (CPU, memory, storage, GPU)
Target varies: 40–60% CPU for general compute, 70%+ for GPU. Kubernetes request-to-usage ratio deserves its own tracking — over-requested pods are invisible waste that the cloud bill can't show you.

**Storage tiering compliance**
`cost in appropriate access tier / total storage cost`
Lifecycle policies are cheap to implement and nearly always underused.

## 5. Planning accuracy

**Forecast accuracy / variance**
`|forecast − actual| / actual`
Target within ±5–10% at monthly grain for Walk, tighter at Run. The KPI that buys FinOps credibility with finance faster than any savings number. Track by segment — an accurate total hiding two large offsetting errors isn't accurate.

**Budget variance**
`(actual − budget) / budget`
Positive means overspend. Report per-owner, not just aggregate.

**Anomaly detection time (MTTD)**
`time from anomaly onset to alert`
Target under 24 hours. Also track **MTTR** — time to resolution — and the **false positive rate**, because an alert channel that cries wolf gets muted by week three and then the practice has no detection at all regardless of what MTTD says.

**Cost avoidance from anomalies**
`estimated spend prevented by anomaly response`
Softer number, but it's how anomaly tooling justifies itself.

## 6. Unit economics

The domain that converts FinOps from a cost function to a value function.

**Cost per customer / tenant**
`allocated cost / active customers`
For SaaS businesses this is the number. Segment it — a blended average hides the tenants destroying margin.

**Cost as % of revenue**
`technology cost / revenue`
The board-level metric. Track the *trend*: growing spend with a falling ratio is healthy scaling; the reverse is the alarm.

**Cost per transaction / request / order**
`allocated cost / business event count`
Whatever the business's atomic unit is.

**Gross margin impact**
`(revenue − COGS including allocated technology cost) / revenue`
Where FinOps meets the P&L. Requires allocation to be genuinely trusted.

**Fully-loaded cost**
Direct resources + supporting services + operational overhead. Unit economics computed on direct resources only understate by a meaningful margin and get challenged the first time finance checks.

## 7. Practice health

- **Optimization recommendation implementation rate** — `implemented / generated`. Often brutally low (single digits) and far more diagnostic than the size of the recommendation backlog. A large backlog with a low implementation rate means the practice is producing reports nobody acts on.
- **Time to allocate new spend** — days from a new service or account appearing to being correctly allocated.
- **Month-end close time** — hours spent reconciling. Teams with fragmented tooling burn their close on stitching; this metric justifies consolidation.
- **Coverage of engineering teams with a named FinOps champion** — the federation metric. In a centralized-enablement model this is the actual constraint on scale.

## 8. What to measure at each maturity level

**Crawl** — total spend and trend; tag coverage; a short waste list; basic budget alerts. Nothing else is meaningful yet.

**Walk** — add allocation rate, commitment coverage and utilization, ESR, forecast variance, anomaly MTTD, non-prod ratio.

**Run** — add unit economics, cost as % of revenue, implementation rate, pre-deployment cost estimates vs actuals, and category-specific KPIs per Scope.

The 2026 framework's KPIs & Benchmarking capability makes this explicit: KPIs should be defined against the technology category and the business context of the Scope, not pulled from a cloud-generic default list.

## 9. Dashboard design

**By persona** — the same data, different questions:

- **Engineering** — their team's spend, trend, top movers, open recommendations with effort estimates, utilization. Must be self-serve; if they have to ask FinOps for a number they won't ask.
- **Finance** — allocation completeness, budget variance, forecast accuracy, accrual correctness, commitment position.
- **Leadership** — cost as % of revenue, unit economics trend, savings realized vs target, major commitment decisions pending. One screen. No resource-level detail.
- **Product** — cost per customer segment, cost per feature, margin by product line.

**Design rules that hold up:**
- Every metric on a dashboard should have a decision attached to it. If nobody would act differently based on the number, remove it.
- Show trend and target, not just current value. A bare number is uninterpretable.
- Absolute cost movement is nearly always less informative than movement *per unit of business*. Spend going up during growth is fine.
- Name the owner on the chart.

## 10. The metric trap

Strong FinOps metrics do not necessarily mean strong performance, and this is worth saying out loud to stakeholders:

- **High ESR can mean an aggressive commitment position on workloads about to be refactored.** Savings today, stranded commitment tomorrow.
- **Low waste rate can mean nothing is being measured**, not that nothing is wasted.
- **Falling savings numbers in a mature practice are expected**, not failure — the big rocks are gone and what remains is a long tail with worse effort-to-savings ratios. Judging a mature team on year-one savings rates pushes them toward bad commitments.
- **Chargeback can incentivize gaming** — teams hiding spend in shared services or under-tagging to avoid attribution — rather than efficiency.
- **Aggressive rightsizing on average utilization buys savings with incidents.** The cost shows up in a different budget, which is exactly why it's tempting.

The purpose of a FinOps metric is to guide a decision, not to report on the past. When a metric stops changing anyone's behavior, retire it.

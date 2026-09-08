# Optimization playbook — rightsizing, commitments, anomaly, forecast

**As of: 2026-09-07.** Method is stable. Provider-specific product names and any price figure
belong to **hyperscaler-expert** — use that skill for rates, this one for how to decide.

## Order of operations

Do these in order; reversing them wastes money.

1. **Eliminate** — turn off what nobody uses. Zero risk of buying a discount on waste.
2. **Rightsize** — match capacity to real demand.
3. **Re-architect** — cheaper service model where it is worth the engineering.
4. **Commit** — buy discounts on the workload that remains, once it is stable.

⚠ **Never commit before rightsizing.** A three-year commitment on an oversized fleet locks in
the waste and removes your incentive to fix it — the most expensive common FinOps mistake.

## Rightsizing

**Percentiles, not averages.** An average hides the peak that made someone over-provision. Use
p95 or p99 over a window long enough to contain the real cycle — **at least 14 days, 30 preferred**
— so weekly patterns and month-end batch runs are inside it.

- **Memory is the blind spot.** CPU is collected by default almost everywhere; memory usually is not, and memory is what actually forces a size. Without a memory signal, say your recommendation is CPU-only rather than implying full confidence.
- **Check the constraint before the size.** Network, IOPS, licensing and a single-threaded hot path all defeat a naive vCPU/RAM match.
- **Prefer a family change to a size change** where the workload suits it — a generation upgrade or an ARM move (Graviton/Cobalt/Axion) often beats dropping one size, at similar effort.
- **Down one size at a time**, with the utilization data retained so the change can be defended or reversed.
- **Non-production is the free win.** Dev/test/staging schedules (off nights and weekends ≈ 65–70% of hours) carry near-zero risk and are usually the fastest realized saving in any estate.

**Idle and orphan hygiene** — the boring list that keeps producing: unattached volumes, unassociated
static IPs, idle load balancers, stopped instances still billing for storage, old snapshots with
no retention policy, over-provisioned and forgotten managed databases, empty or unused clusters,
logs and metrics retained forever at hot tier.

## Commitment portfolio management

Two metrics, opposite failure modes, and you need **both**:

- **Coverage %** — share of eligible spend covered by a commitment. Low = leaving discount on the table.
- **Utilization %** — share of purchased commitment actually used. Low = you bought too much and are paying for nothing.

Chasing coverage alone is how teams end up at 98% coverage and 80% utilization — worse than 70/100.

Practice:
- **Target a band, not a maximum.** Commit to the stable baseline; leave the variable top on-demand or spot. 100% coverage means you have committed to your peak.
- **Ladder expiries.** Staggered purchases avoid a cliff where a large share of the estate renews at once with no negotiating room and no flexibility.
- **Prefer flexible instruments** (compute-scoped savings plans, convertible reservations, flexible CUDs) where the price difference is small — the optionality is usually worth more than the last few points of discount.
- **Break-even is what makes the term decision.** Compute the utilization threshold at which a 1-year or 3-year commitment beats on-demand, and compare it against how confident you actually are about that workload's life. If the workload might be re-architected inside the term, that is a real cost, not a footnote.
- **A migration destroys commitment value.** Commitments do not transfer between clouds. In any migration business case, remaining commitment liability is a first-class switching cost.

## Storage and data transfer

- **Tier on measured access patterns, not intuition** — retrieval fees and minimum storage durations can make a colder tier more expensive for data that is still being read.
- **Lifecycle policies at creation.** Retrofitting them onto petabytes is a project; setting them on an empty bucket is a line of config.
- **Snapshots compound silently** — they are the classic line item that grows unnoticed for years.
- **Egress and inter-AZ/inter-region transfer** is the cost most often missing from an architecture estimate, and the one that most often decides a migration case. Get the rates from hyperscaler-expert.

## Kubernetes

Cluster cost needs **allocation before optimization** — a cluster bill is one line until something
splits it by namespace/workload. OpenCost (CNCF, the open implementation of the model behind
Kubecost) is the standard way, and is what this platform's feeder ships.

- Split **requests vs usage**: teams are billed for requests, waste is the gap to usage. Both numbers must be visible or nobody acts.
- **Idle cluster capacity** (nodes provisioned but unrequested) belongs to the platform team, not spread silently across tenants — otherwise no one owns the number that is actually fixable.
- Pod rightsizing uses the same percentile method as VMs, on requests.
- The big structural levers: autoscaling that actually scales down, bin-packing, spot for
  fault-tolerant workloads, and control-plane/node-pool consolidation.

## Anomaly detection

- **Seasonality is the whole problem.** Cloud spend has strong weekly and monthly shapes; a naive threshold alerts every Monday and every month-end. Baseline per series with seasonality, or alert on residuals from a model.
- **Alert on cost impact, not percentage.** A 400% jump on a $3/day resource is noise; 8% on the largest service is not. Rank by absolute money.
- **Segment before detecting.** Anomalies at org level hide inside the total; per-service, per-account, per-resource-type series catch what a total never will.
- **Every alert needs an owner and a disposition** (real / expected / accepted). Without disposition tracking, precision never improves and the channel gets muted — the failure mode that kills anomaly programs.
- **Distinguish a cost anomaly from a usage anomaly.** A rate change (commitment expiry, discount ending, currency move) looks identical in cost and needs a completely different response than a usage spike.

## Forecasting

- **State the horizon and the error band.** A forecast without a published error band is an opinion. Measure MAPE against actuals and publish it.
- **Separate committed/fixed from variable spend** before forecasting — they have different dynamics and mixing them degrades both.
- **Amortized, always** — unblended commitment purchases create step functions no model should be asked to learn.
- **Growth-driven beats time-series alone** where a business driver exists. If cost tracks customers, forecast customers and multiply by unit cost; that forecast is explainable to finance, and a pure time-series model is not.
- **Known step changes must be added manually** — a migration, a launch, a commitment expiry. No model infers these from history.
- **Reforecast on a cadence and keep the misses visible.** A forecasting practice that never publishes its errors is not measurable, and finance will treat it accordingly.

# FinOps for AI

Current as of July 2026. This is the fastest-moving area of the discipline — model pricing, hardware, and provider billing granularity change monthly. Treat specific prices as needing verification.

## Contents
1. The two directions: FinOps for AI vs AI for FinOps
2. Why traditional FinOps breaks on AI
3. Cost anatomy — where AI money actually goes
4. Token economics mechanics
5. Inference vs training
6. Optimization levers, in order
7. AI-specific KPIs
8. Attribution and governance
9. Maturity path
10. Build vs buy: self-host vs API

---

## 1. The two directions

These get conflated constantly; keep them separate.

- **FinOps for AI** — applying financial governance to AI workloads you run. Track, attribute, forecast, and optimize what AI costs. This is the dominant 2026 problem.
- **AI for FinOps** — using AI to improve cost management: anomaly detection models, natural-language cost queries, agentic workflows that propose commitment purchases. In the 2026 survey, ~49% called this a high priority and ~81% were actively exploring it.

## 2. Why traditional FinOps breaks on AI

Same principles, different mechanics. The specific breakages:

- **Token pricing, not hourly rates.** The unit of consumption is not time, and input/output tokens price differently.
- **Thin billing data.** Managed AI platform services often bill at a granularity that tells you nothing about which team, feature, or user drove the cost. There's no equivalent of a resource ID with tags.
- **Experimentation is a cost driver.** Training runs and prompt iteration produce spend that has no steady-state analog and doesn't forecast linearly.
- **Forecasting assumptions fail.** Traditional budgeting assumes roughly linear demand, stable unit economics, and predictable consumption. AI adoption curves, per-token price drops, and changing model mixes break all three simultaneously — forecasts aren't slightly wrong, they're structurally wrong.
- **GPU scarcity and volatility.** Capacity availability, not just price, constrains decisions.
- **Cost sits across categories.** One AI initiative can span public cloud (inference), data center (training), and SaaS (token-based API spend) at once — this is exactly what Scopes were designed to handle.

## 3. Cost anatomy — where AI money actually goes

The token invoice is the visible layer and a minority of true cost. The full picture, roughly:

1. **Model API / token spend** — the invoice everyone looks at
2. **GPU compute** — training, fine-tuning, and self-hosted inference
3. **Vector database and embedding storage** — often the quiet compounding cost in RAG systems
4. **Data pipeline and preprocessing** — ingestion, chunking, ETL for training and retrieval
5. **Egress and networking** — cross-region and cross-provider data movement
6. **Orchestration and agent infrastructure** — the compute running the loop around the model
7. **Observability and evaluation** — tracing, eval runs, guardrail model calls
8. **Human-in-the-loop** — labeling, review, red-teaming
9. **Licensing and platform fees** — the AI platform layer itself

"How much is our AI spend?" is hard to answer precisely because most orgs only see bucket 1. When someone reports an AI number, ask which buckets it includes.

## 4. Token economics mechanics

The vocabulary FinOps and engineering need to share:

- **Input vs output tokens price differently** — output typically costs several times input. A verbose system prompt is cheap relative to a verbose response.
- **Context window is a cost multiplier.** Every turn in a conversation resends prior context. Naive chat implementations grow cost quadratically with conversation length.
- **Prompt caching** is the highest-leverage single lever for repeated-prefix workloads (system prompts, RAG documents, few-shot examples). Correctly configured, it cuts input-token cost dramatically. It's also frequently misconfigured — cache hits require stable prefixes.
- **Batch pricing** offers a substantial discount for latency-tolerant workloads. Most orgs run everything synchronously by default and leave this on the table.
- **Model tiering / routing** — routing simple requests to a small model and escalating only when needed is typically the largest cost reduction available, because model choice affects every subsequent dollar.
- **Provider-side price cuts** mean a workload's cost curve declines over time independent of your effort. Forecast with this in mind, and re-benchmark model choice quarterly.

Reported outcomes from combining routing, caching, and rightsizing on production deployments run in the range of 60–85% cost-per-answer reduction. Treat that as an achievable ceiling with real work, not a default.

## 5. Inference vs training

The ratio inverted. Industry analysis in 2026 puts roughly 55–80% of enterprise AI GPU spend on inference rather than training, reversing the 2022–2023 picture. Two consequences:

- **Inference is where the optimization opportunity is** for most organizations, and it's continuous rather than episodic.
- **Review cadence differs.** Inference costs move fast — weekly review catches regressions before they compound. Training costs are more predictable — monthly is fine.

Cumulative inference cost overtakes training cost within months of a feature reaching production. Any business case that models training cost and treats inference as an afterthought is wrong.

## 6. Optimization levers, in order

Order matters — each layer changes the denominator for the next.

**1. Model layer** (largest impact)
- Route by task complexity; use the smallest model that passes eval
- Reduce output length; constrain response format
- Trim context: better retrieval beats bigger context windows
- Prompt caching for stable prefixes
- Batch anything latency-tolerant

**2. Runtime layer** (self-hosted)
- Quantization (FP8 on modern accelerators is usually the first thing to apply)
- Continuous batching and paged attention
- Speculative decoding where it fits the workload

**3. Infrastructure layer**
- Match commitment shape to workload pattern — this is the highest-stakes financial call in AI infrastructure
- Spot/preemptible for training and batch inference with checkpointing
- Region and provider arbitrage where data residency permits

**4. Governance layer** (continuous)
- Quotas and rate limits per team/key
- Pre-deployment cost estimation for new AI features
- Kill switches for runaway agent loops

**On GPU commitments:** the failure modes are symmetric — overpay for on-demand, or lock into capacity your workloads stop using because you changed models. Given how fast model efficiency improves, commit conservatively on the baseline and burst on-demand, and revisit at every renewal window. Don't commit multi-year on a workload whose model you expect to replace within six months.

## 7. AI-specific KPIs

The core set:

| KPI | Formula | Notes |
|---|---|---|
| Cost per 1K tokens | total token spend / (tokens / 1000) | Normalizes across models and providers; the base unit metric |
| Cost per inference / request | total inference cost / request count | The one product managers understand |
| Cost per business outcome | total AI cost / resolved tickets, generated documents, etc. | The only one leadership should see; connects to unit economics |
| GPU utilization rate | actual GPU-hours used / GPU-hours provisioned | Target 70%+; anything under 100% is a waste signal, and most fleets sit far below |
| Input:output token ratio | input tokens / output tokens | Diagnostic — a shifting ratio explains cost movement that total spend hides |
| Cache hit rate | cached input tokens / total input tokens | Directly proportional to savings on repeated-prefix workloads |
| Model mix | spend share by model tier | Tracks whether routing is actually routing |
| AI spend attribution rate | attributed AI cost / total AI cost | The AI analog of tag coverage; usually the worst number in the deck |

**Alert at 80% of budget, not 100%.** At 100% there's nothing left to do; at 80% there's a week or two to investigate and correct before the next cycle.

## 8. Attribution and governance

The hard problem: AI cost attribution has no native equivalent of resource tags.

**The practical pattern that works:**
1. **Inventory first.** Every model provider account, API key, and payment method in the organization. Shadow AI spend on personal cards and unmanaged keys is near-universal and is the first thing to find.
2. **Proxy layer.** Route all model calls through a gateway that stamps every request with team, use-case ID, environment, and user/session. This is the single highest-value engineering investment for AI FinOps — the provider invoice will never give you this, and building it later means backfilling nothing.
3. **Telemetry join.** Combine provider billing data with request-level telemetry (OpenTelemetry-style traces) in a warehouse. Attribution across users, teams, sessions, models, and workflows comes from the join, not from either source alone.
4. **Tag at submission.** Every training job, inference endpoint, prompt pipeline, and data bucket carries at minimum: model name, use-case ID, and owner.

**Agentic workloads** make this harder and more urgent: one user action can fan out into dozens of model calls across multiple models and tools, so per-session cost varies by orders of magnitude and per-request averages become meaningless. Attribute at the *session* or *task* level, and track cost distribution (p50/p95/p99), not just the mean — the p99 session is where budget surprises live.

**Tooling maturity:** mainstream FinOps platforms began shipping model-provider billing integrations in 2025–2026, but maturity varies — some only import spend, with allocation and anomaly detection lagging. For richer attribution, a proxy layer plus a data warehouse generally beats a native platform integration today. Evaluate against your actual attribution requirements rather than a checkbox.

## 9. Maturity path

Most organizations with active AI deployments sat between Crawl and Walk through 2026; the Walk→Run jump requires tooling and process investment few have made.

- **Crawl** — know total AI spend; inventory of accounts and keys; manual monthly review; basic budget alerts.
- **Walk** — proxy layer in place; spend attributed to teams and use cases; cost-per-token tracked; routing and caching implemented; weekly review of inference cost.
- **Run** — unit economics per business outcome; pre-deployment cost estimation for new AI features; automated quotas and guardrails; commitment strategy tied to forecast; cost regression tests in CI.

A realistic build-from-scratch timeline is 60–90 days to reach solid Walk, and the proxy layer is the gate.

## 10. Build vs buy: self-host vs API

The recurring question. The honest framing:

**API wins when:** volume is variable or uncertain, the workload benefits from frontier model quality, engineering capacity is scarce, or you'd be running below ~60–70% GPU utilization. Which is most organizations, most of the time.

**Self-hosting wins when:** volume is high and steady, a smaller open model passes eval for the task, data residency or regulatory constraints force it (relevant for KVKK/BDDK-type regimes and other regulated environments), or latency requirements demand co-location.

**The number that decides it:** fully-loaded cost per 1K tokens self-hosted — including GPU-hours at realistic utilization, engineering time, and idle capacity — versus API list price after routing and caching optimization. Teams routinely compare API prices against a theoretical 100%-utilized GPU and conclude self-hosting is cheaper. At 30% utilization it usually isn't.

Run the comparison after optimizing the API path, not before. Routing and caching often close the gap entirely.

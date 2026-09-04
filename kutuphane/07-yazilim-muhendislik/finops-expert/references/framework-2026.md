# FinOps Framework 2026

Source: finops.org/framework, Framework 2026 update published March 2026. CC BY 4.0 — attribute the FinOps Foundation when reproducing framework structure.

## Contents
1. Definition and mission
2. Principles
3. Personas
4. Phases
5. Maturity model
6. Domains and Capabilities (full list)
7. Scopes
8. Technology Categories
9. What changed in 2026
10. Intersecting Disciplines

---

## 1. Definition and mission

**Mission (updated early 2026):** Advancing the People who manage the Value of Technology. (Previously: "...the Value of Cloud".)

**Definition:** FinOps is an operational framework and cultural practice which maximizes the business value of technology, enables timely data-driven decision making, and creates financial accountability through collaboration between engineering, finance, and business teams.

The single-word change from "cloud" to "technology" is the through-line of the entire 2026 update. If someone is still framing FinOps as cloud bill cleanup, they're describing 2021.

## 2. Principles

Six, unchanged in substance:

1. Teams need to collaborate
2. Business value drives technology decisions
3. Everyone takes ownership for their technology usage
4. FinOps data should be accessible, timely, and accurate
5. FinOps should be enabled centrally
6. Take advantage of the variable cost model of the cloud

Principle 2 is the one Executive Strategy Alignment operationalizes. Principle 5 is why federated-only models fail — execution federates, enablement centralizes.

## 3. Personas

**Core Personas** (always engaged): FinOps Practitioner, Engineering, Finance, Leadership, Procurement, Product.

**Allied Personas** (support the practice): ITAM, ITFM, ITSM, Security, Sustainability.

Practical read on each:
- **FinOps Practitioner** — owns the data layer and the ritual. Usually outnumbered; scales through enablement, not doing.
- **Engineering** — holds every usage-side lever. Nothing in the Optimize domain happens without them. Their currency is velocity, not savings; frame asks accordingly.
- **Finance** — owns forecast credibility and the budget conversation. Cares about variance and accrual correctness more than about waste.
- **Leadership** — cares about tradeoffs and multi-year commitments. Newly central in 2026 via Executive Strategy Alignment.
- **Procurement** — owns contracts, EDPs/MACCs, renewals, and increasingly SaaS. Underused in most practices.
- **Product** — owns the unit-economics conversation: is this feature's cost per user defensible at scale?

## 4. Phases

**Inform → Optimize → Operate**, run as a continuous loop, not a project.

- **Inform** — visibility, allocation, benchmarking, budgeting/forecasting. Everything downstream depends on this being trusted.
- **Optimize** — rate and usage actions against known targets.
- **Operate** — governance, cadence, automation, continuous improvement. This is where most practices fail: optimizations decay within 6–12 months without operating discipline, and the org quietly returns to baseline.

## 5. Maturity model

**Crawl / Walk / Run**, applied per Capability rather than to the org as a whole. An org can be Run on Allocation and Crawl on Unit Economics — that's normal and worth stating explicitly in assessments.

- **Crawl** — capability exists in some form, limited coverage, manual, reactive.
- **Walk** — consistent process, meaningful coverage, some automation, defined owners and targets.
- **Run** — automated, high coverage, integrated into decision-making before spend happens, measured against KPIs with accountability.

Don't chase Run everywhere. The framework is explicitly non-prescriptive: mature only the capabilities where business value justifies it.

## 6. Domains and Capabilities

Four Domains are the *outcomes*; Capabilities are *how you achieve them*.

### Understand Usage & Cost
- **Data Ingestion** — collecting and normalizing cost/usage/carbon data from all sources into a common model. FOCUS lives here.
- **Allocation** — attributing cost to business constructs (team, product, cost center, environment). The foundational capability; everything else degrades to guesswork without it.
- **Reporting & Analytics** — making the data usable per persona.
- **Anomaly Management** — detecting, triaging, and resolving unexpected spend movement.

### Quantify Business Value
- **Planning & Estimating** — pre-spend cost modeling for projects and architectures.
- **Forecasting** — projecting future spend with stated accuracy targets.
- **Budgeting** — setting and tracking budgets and variance.
- **KPIs & Benchmarking** *(renamed 2026 from "Benchmarking")* — defining KPIs aligned to technology category and Scope context rather than cloud-generic defaults.
- **Unit Economics** — cost per business unit (customer, transaction, order, inference).

### Optimize Usage & Cost
- **Architecting & Workload Placement** *(renamed 2026 from "Architecting for Cloud")* — placement decisions across technology categories, moved earlier into design before commitments are made.
- **Usage Optimization** *(renamed 2026 from "Workload Optimization")* — rightsizing, scheduling, idle elimination, storage tiering, across all Scopes.
- **Rate Optimization** — commitments, discounts, negotiated rates, pricing models.
- **Licensing & SaaS** — license and managed-software spend optimization.
- **Sustainability** *(renamed 2026 from "Cloud Sustainability")* — now covers carbon allocation across on-prem, SaaS, colocation, and end-user computing, with embodied vs operational carbon distinguished and regional emission factor variability acknowledged.

### Manage the FinOps Practice
- **Executive Strategy Alignment** *(NEW 2026)* — see below.
- **FinOps Practice Operations** — running the practice: cadence, roles, workflows.
- **Governance, Policy & Risk** *(renamed 2026 from "Policy & Governance")* — policy frameworks and risk across all technology categories, aligned with intersecting disciplines.
- **FinOps Education & Enablement** — training the personas.
- **Invoicing & Chargeback** — showback, chargeback, internal billing.
- **FinOps Assessment** — measuring practice maturity.
- **Automation, Tools & Services** *(renamed 2026 from "FinOps Tools & Services")* — automation, tooling, and professional services across all categories, framed as three categories of solution to evaluate against business priorities.
- **Intersecting Disciplines** — coordinating with ITAM/ITFM/ITSM/Security/Sustainability.

## 7. Scopes

**Definition (refined 2026):** A FinOps Scope is a defined segment of spending across Technology Categories, aligned to business constructs — such as products, cost centers, or environment — that guide the application of FinOps to maximize technology value.

Key distinction to get right: **Technology Category is the "what." Scope is the "why."** A Scope is a *decision context*, not a slice of the bill by infrastructure type. It determines which Personas are engaged, which Capabilities apply, and what success looks like.

**Scopes are initiated by business questions**, typically from leadership — not by a practitioner deciding a spend area looks interesting. The 2026 guidance pushes practitioners to dig past the surface question to the outcome the business actually wants before defining the Scope.

**Scopes have a lifecycle.** They flex in duration and intensity, and they end — recognizing when a Scope has served its purpose and can be scaled back or absorbed into standing practice is part of the discipline. Spend often sits in multiple Scopes at once carrying different expectations in each; manage those interactions deliberately or the insights stop being coherent.

**Anatomy of a Scope definition** (use this shape when helping someone define one):

| Element | Content |
|---|---|
| Business Strategies | What the business is trying to achieve, including its risk/waste tolerance |
| Technology Strategies | The architectural approach chosen |
| Technology Categories | Which categories of spend are in the Scope, with specifics (accounts, vendors) |
| Personas Engaged | Who, and at what level of involvement |
| Key Capabilities | Which capabilities, at which maturity level |
| Cadence and Maturity | How fast the loop runs, and what maturity is acceptable |

Worked example from the Foundation — an AI innovation Scope: business is willing to accept more waste for speed, so the Scope runs at the fastest cadence with *low maturity accepted*, focusing on ingestion, anomaly detection, allocation, and estimating rather than deep rate optimization. That "low maturity is the right answer here" move is the most useful thing about Scopes.

## 8. Technology Categories

Each category page follows the same structure: FinOps Considerations, Personas, Framework Domains and Capabilities, Measures of Success and KPIs, and FOCUS Alignment.

- **Public Cloud** — IaaS/PaaS. Multi-cloud complexity, commitment management, high rate of change. Still the primary category; the practice was born here.
- **SaaS** — decentralized purchasing, renewal windows, thin billing data. License utilization is the dominant lever.
- **Data Center** — on-prem/private cloud/colo. Capex-shaped, depreciation and TCO modeling, allocation without native billing data.
- **Data Cloud Platforms** — Snowflake, Databricks, BigQuery. Consumption-based, credit/slot pricing, query-level attribution.
- **AI** — cost complexity, unpredictable spend, governance gaps; spans multiple categories at once. See `ai-finops.md`.

The list is explicitly non-exhaustive. Licenses and Private Cloud also appear as categories in the framework diagram.

## 9. What changed in 2026

**New Capability: Executive Strategy Alignment** (in Manage the FinOps Practice). Four areas:

1. **Executive Priority Alignment** — connect spend and usage to strategic initiatives. The framing that matters: a seat at the executive table is *earned* by delivering trusted data that becomes indispensable, not granted by mandate. Progression is retrospective reporting → forward-looking decision support (forecasting, unit economics, executives sponsoring shared ownership).
2. **Multi-Year Investment Strategy** — feed FinOps data into enterprise budgeting, P&L ownership, long-term vendor commitment governance. Includes lifecycle cost analysis for modernization, where legacy + migration + decommissioning costs overlap. Explicitly: finding efficiency that creates financial headroom for AI bets.
3. **Facilitate Product Prioritization Strategy** — make cost/speed/quality tradeoffs comparable *across* competing initiatives, and pull FinOps review into intake and architecture decisions before commitments.
4. **Enable Strategic Decision Support** — the operating model: where FinOps sits, which governance forums it feeds, decision rights, spend guardrails, and continuity of measures through M&A, restructuring, and leadership change.

**"Shift up"** — the term introduced for this. Parallel to "shift left" (embedding FinOps earlier in the delivery lifecycle), "shift up" means elevating FinOps to where investment strategy is shaped.

**"FinOps Enabled Executive"** — typically C-1 (VP/SVP/EVP) who positions FinOps as strategic advisory, sponsors shared cost ownership, and ensures FinOps insight reaches investment governance and multi-year planning.

**Six Capabilities renamed** (listed in section 6), all in the direction of removing cloud-specific language.

**Optimization did not get demoted.** The Foundation is explicit: optimization remains core; 2026 just insists it be connected to strategy.

## 10. Intersecting Disciplines

FinOps increasingly overlaps rather than competes with:

- **ITAM / SAM** — contractual value and lifecycle of software and hardware assets
- **ITFM** — financial structures, GL mapping, chargeback accounting
- **ITSM** — policy, process, CMDB
- **Sustainability / ESG** — environmental impact of consumption
- **Security & Enterprise Architecture** — standards and risk across the estate

Observed collaboration ordering in 2026: ITFM most frequent (shared data), then ITAM/SAM (asset compliance), ITSM (process), ESG (sustainability, strongest in Europe and Asia). Platform Engineering is increasingly present as FinOps shifts left.

Structural pattern worth knowing: larger companies keep these as separate teams that collaborate; smaller companies merge them into one function. Either is fine — what fails is treating them as siloed, which produces multiple conflicting views of technology value and forces leadership to reconcile them.

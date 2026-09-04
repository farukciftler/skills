# FinOps, Cost Optimization, Architecture Frameworks, SLAs, Support & Migration Strategy — AWS vs Azure vs GCP

**Verified as of: 2026-08-28.** Main sources: focus.finops.org (FOCUS v1.2/v1.3 specs), finops.org insights (FinOps X 2025/2026 recaps), aws.amazon.com (Data Exports, Compute SLA, RDS/Aurora SLA, premiumsupport, Compute Optimizer, Transform/EVS/Graviton5 announcements), learn.microsoft.com (VM/SQL SLAs, regions-paired, cost-management tag inheritance, Azure Migrate what's-new, AZ-305), cloud.google.com (Compute/Cloud SQL/GCS SLAs, FinOps Hub, CUD multiprice docs, DMS, Well-Architected Framework, Customer Care), Linux Foundation press (FOCUS 1.3, Dec 2025), EU Data Act analyses, Broadcom/VMware pricing reports, Phoronix/NextPlatform (Axion/Graviton benchmarks).

Prices are US-region list prices in USD; always re-verify against the pricing calculators before committing numbers to a business case.

---

## 1. FinOps Practice in 2026

### 1.1 FOCUS — the billing-data lingua franca (status)

The FinOps Open Cost and Usage Specification (FOCUS) is now the de facto normalization layer and increasingly a **procurement requirement**.

- **Spec versions:** 1.0 (2024) → 1.1 → **1.2 (June 2025**; SaaS/PaaS scope, multi-currency, `InvoiceId`/billing-reference improvements) → **1.3 (announced Dec 11, 2025, support live at FinOps X 2026)** — split/shared-cost allocation constructs, a **dedicated contract-commitment dataset**, data-freshness/completeness columns. FinOps X evolving into "Tokenomicon" (AI-economics focus) with a Linux Foundation "Tokenomics Foundation" for AI cost standards — token-level AI spend is the next FinOps frontier.
- **AWS:** first mover. **Data Exports for FOCUS 1.0 GA Nov 2024; FOCUS 1.2 GA Nov 19, 2025.** Parquet to S3; since March 2026 **cross-account S3 delivery** of exports (big for centralized FinOps data lakes).
- **Azure:** FOCUS is the **recommended dataset** in Cost Management exports (enhanced exports GA April 2025); **FOCUS 1.2 as "1.2-preview"** dataset. The Microsoft **FinOps Toolkit** (FinOps hubs, Power BI templates) is the standard open-source companion.
- **GCP:** FOCUS delivered as a **BigQuery view** over the detailed billing export (1.0 GA, 1.2 support announced at FinOps X 2025).
- Practical take: FOCUS solves column mapping, not semantics — amortization behavior, credit modeling, and tag columns still need per-cloud understanding. Core cost columns: `ListCost`, `ContractedCost`, `BilledCost`, `EffectiveCost` — one consistent amortized-vs-invoiced view.

### 1.2 Native cost tooling compared

**AWS:**
- **Cost Explorer** (hourly/resource-level granularity is a paid enable), **Data Exports** with **CUR 2.0** (fixed schema, nested key-value columns, SQL-based column selection at export definition — the authoritative granular dataset) and FOCUS exports.
- **AWS Budgets** (cost/usage/RI-SP coverage & utilization; actions can trigger SCPs/stop instances), **Cost Anomaly Detection** (free, ML-based; ~24h detection latency — not real-time).
- **Cost Categories** + cost allocation tags; **Billing Conductor** for custom rate cards (chargeback with margin).
- **Cloud Intelligence Dashboards** (CUDOS/CID on QuickSight) — the de facto free FinOps BI layer.

**Azure:**
- **Cost Management + Billing** (portal analysis, budgets, anomaly alerts at subscription scope — daily evaluation, ~7-day baselines), **exports** to Storage (FOCUS, actual/amortized, price sheets, reservation details), Power BI connector.
- Cost views are scope-heavy (billing account / MG / subscription / RG); EA vs MCA billing-account differences still bite reporting automation.
- **FinOps Toolkit / FinOps hubs**: ADX/Fabric-based pipeline — Microsoft's answer to CUDOS.

**GCP:**
- **Cloud Billing** console (reports, cost table, breakdown), **budgets & alerts** (Pub/Sub notifications), **detailed usage cost export to BigQuery** — the canonical pattern: everything serious happens in BigQuery + Looker Studio.
- **FinOps Hub 2.0** (2025, Gemini-powered): utilization insights, "waste map" ranking idle/overprovisioned resources across GCE, GKE, Cloud Run, Cloud SQL, with AI-summarized remediation. **Cost anomaly detection** GA, zero-config, hourly.
- **Gemini Cloud Assist in Billing** — the most mature native "ask your bill" experience of the three.

### 1.3 Tags/labels strategy — the differences that matter

- **AWS:** tags do **nothing for billing until activated** as *cost allocation tags* (per payer account; up to 24h; backfill of up to 12 months now requestable). Enforce with **Tag Policies + SCPs**. Untaggable/shared costs need **Cost Categories** split rules.
- **Azure:** tags are ARM-native, **not inherited by default** — but **Cost Management tag inheritance** (billing-side setting) applies subscription/RG tags onto child *usage records* within ~24h. Enforce with **Azure Policy** (`Modify` can auto-add tags). Some cost sources (Marketplace, some PaaS meters) emit untagged usage regardless.
- **GCP:** critical distinction — **labels** (metadata on resources, up to 64, flow into billing export) vs **tags** (org-level resources with IAM bindings, policy/conditional IAM + firewall use, hierarchical inheritance; since 2024–25 also in billing export). Project structure is the primary allocation unit (project = cost boundary by design).
- Cross-cloud practice: allocate primarily by **account (AWS) / subscription-RG (Azure) / project (GCP)** boundaries; tags/labels for cross-cutting dimensions (cost-center, env, app, owner); keep taxonomy small (5–8 mandatory keys); enforce at creation; measure tag coverage as a KPI (>90% of allocable spend).

### 1.4 Chargeback/showback patterns

- Maturity ladder: **visibility → showback → chargeback (GL journal entries) → unit economics (cost per customer/order/token)**.
- Amortized cost (EffectiveCost) is the correct basis; decide commitment-discount attribution policy explicitly: (a) benefit-where-used, (b) centralized commitment pool with internal blended rate, or (c) Billing Conductor / custom rate cards. Shared costs split by proportional-spend, even-split, or driver-based keys — FOCUS 1.3's split-cost constructs standardize this.
- Enterprise discounts (AWS EDP/PPA, Azure MACC/EA, GCP committed spend agreements) usually held centrally.

### 1.5 Third-party landscape (brief)

Heavy consolidation: **IBM** (Apptio Cloudability + Turbonomic + Kubecost + Instana), **Flexera** (acquired **ProsperOps** + Chaos Genius Jan 2026), Broadcom holds CloudHealth. Independents: **CloudZero** (unit economics/AI cost), **Vantage**, **Finout**, **nOps**, **DoiT**, **ScaleOps** (autonomous K8s optimization), **Archera**, **Zesty**, **Kion**. Rule: native tools cover visibility/anomalies; buy third-party for multi-cloud normalization, automation (commitments, K8s rightsizing), unit economics — demand FOCUS-native ingestion.

---

## 2. Cost-Optimization Levers, Ranked by Typical Impact

### 1) Commitment discounts (typically 25–40% off compute; biggest single lever)
- **AWS:** Savings Plans — **Compute SP up to ~66%** (EC2/Fargate/Lambda, any region/family), **EC2 Instance SP up to ~72%**; Standard RIs mostly for RDS/ElastiCache/OpenSearch/Redshift (no Savings Plans there — though Database Savings Plans arrived Dec 2025). Strategy: ladder small Compute SP purchases monthly/quarterly; target **~70–80% coverage of stable baseline**, **>95% utilization**; utilization first, coverage second.
- **Azure:** **Reservations** (VM + long PaaS list) up to ~72%, exchange/cancel flexibility; **Azure Savings Plan for compute** up to ~65% (broader, less deep). Hybrid strategy: reservations for stable SKUs, savings plan as flexible blanket. **Azure Hybrid Benefit** stacks on top — frequently the single biggest Azure lever (up to ~80%+ combined).
- **GCP:** **CUDs** — resource-based (~37% 1-yr / ~55% 3-yr; higher some families) and **spend-based Flex CUDs** (~28%/46%), scope expanded Sept 2025 to memory-optimized, H3/H4D, **Cloud Run and Cloud Functions**. **Jan 21, 2026: all spend-based CUDs moved from credit-offset accounting to direct discounted SKU prices** ("multiprice") — this broke naive cost dashboards; FOCUS/BigQuery queries had to be updated. Sustained-use discounts = legacy families only.
- Governance: centralize purchasing under payer/management account; report coverage & utilization weekly; treat expirations as a calendar-managed pipeline.

### 2) Eliminate idle & orphaned resources (5–15%, near-zero risk)
Unattached disks, aged snapshots, idle LBs, stopped-VM disks still billing, idle NAT gateways, unused public IPs, 24/7 dev/test DBs, zombie K8s clusters. Tools: **Compute Optimizer idle recommendations** (GA Nov 2024; by June 2026 extended to ASG, EBS, ECS, RDS, DynamoDB provisioned, ElastiCache, MemoryDB, DocumentDB, WorkSpaces, SageMaker endpoints), **Azure Advisor**, **GCP FinOps Hub 2.0 waste map + Active Assist**.

### 3) Rightsizing (10–20% of compute)
- **AWS Compute Optimizer:** free, ML-based, 14-day lookback (93-day paid), needs CloudWatch agent for memory; EC2/ASG/EBS/Lambda/ECS/RDS/licensing; flags Graviton candidates; Cost Optimization Hub rollups.
- **Azure Advisor:** free, 7-day+ window, SKU-downsize + shutdown recs with configurable CPU thresholds.
- **GCP Recommender/Active Assist:** 8-day lookback machine-type recs (uses actual memory metrics without an agent for most cases — real advantage), 20+ recommenders.
- Notes: rightsize **before** buying commitments; automate via IaC pull requests; memory-metric coverage is the usual blocker on AWS/Azure.

### 4) Modern-instance / silicon migration (15–40% price-perf on migrated workloads)
- **AWS Graviton:** Graviton4 (M8g/C8g/R8g) ~up to 40% better price-perf vs comparable x86; **Graviton5 announced re:Invent 2025** (192 cores; M9g preview). Managed services (RDS, ElastiCache, OpenSearch, Lambda arm64, Fargate ARM) = low-friction entry.
- **Azure Cobalt 100** (Dpsv6/Dplsv6/Epsv6): up to ~50% better price-perf claims vs prior Arm/comparable x86.
- **GCP Axion** (C4A performance Arm, N4A cost-optimized Arm): up to 65% better price-perf claims vs comparable x86; Axion-based Cloud SQL/AlloyDB GA.
- Rule: interpreted/JIT stacks (Java, Go, Node, Python, .NET Core) and managed data services move with days of effort; expect **20–40%**; watch x86-only binary deps and vendor agents.

### 5) Egress & network architecture (highly variable; classic bill-shock domain — see 2.1)
Gateway/interface endpoints instead of NAT for AWS-service traffic; keep chatty tiers in-AZ; AZ-aware Kubernetes (topology-aware routing); CDN in front of origin egress (free EC2→CloudFront origin fetch); compress/batch cross-region replication; colocate data and compute; GCP: choose Standard vs Premium network tier deliberately.

### 6) Storage lifecycle (5–15% of storage)
- **AWS:** S3 lifecycle → IA/Glacier tiers; **S3 Intelligent-Tiering** as default for unknown access patterns; watch min-duration and per-object charges for small objects; **gp2→gp3** (~20% cheaper) one-click win; EBS snapshot archive + DLM/Recycle Bin.
- **Azure:** Blob hot/cool/cold/archive + lifecycle policies; watch early-deletion windows and read-heavy-on-cool anti-pattern.
- **GCP:** Standard/Nearline/Coldline/Archive + **Autoclass**.

### 7) Spot / preemptible capacity (60–90% off for interruption-tolerant work)
- **EC2 Spot:** up to ~90%, 2-min notice; capacity-optimized/price-capacity-optimized allocation, diversification; ASG mixed instances, EKS + Karpenter.
- **Azure Spot:** up to ~90%, eviction on capacity or max-price, 30-s notice via Scheduled Events; VMSS Flex mixes.
- **GCP Spot:** **60–91% off with predictable (published, non-fluctuating) pricing**, 30-s notice, no max-run limit; GKE Spot node pools first-class.
- Fit: CI, batch, rendering, stateless web, big-data workers, AI inference with checkpointing; combine with commitments (commit baseline, spot for burst).

### 8) Scheduling non-prod (60–70% off scheduled resources)
Nights/weekends off = ~65–70% runtime cut (168h→~50h/week). AWS **Instance Scheduler** / EventBridge Scheduler, Azure **auto-shutdown / Start-Stop VMs v2**, GCP **instance schedules** (native resource policy). Databases too: RDS stop (7-day auto-restart caveat), Aurora Serverless v2 scale-to-zero, Azure SQL serverless auto-pause, Cloud SQL stop.

### 9) License optimization (big for Microsoft/Oracle estates)
Azure Hybrid Benefit; AWS License Manager + BYOL on dedicated hosts; SQL Server edition downgrades (Compute Optimizer flags Enterprise→Standard); Windows→Linux ports (AWS Transform for .NET claims ~40% opex cut); Oracle: heterogeneous migration or Oracle Database@AWS/@Azure/@Google Cloud for the license-heavy tail.

### 10) Observability & data-platform hygiene (often 5–10% hiding here)
CloudWatch Logs Standard $0.50/GB vs **Infrequent Access $0.25/GB**, retention policies (default "never expire" is a tax); Azure Log Analytics **Analytics vs Basic ($0.50/GB) vs Auxiliary ($0.05/GB)** plans + commitment tiers + DCR transformations; BigQuery: on-demand vs capacity, partition+cluster, `maximum_bytes_billed` guards.

### 2.1 Classic bill-shock list (memorize)

| Item | Typical price | Mitigation |
|---|---|---|
| AWS NAT Gateway data processing | **$0.045/GB + $0.045/hr** (per AZ) | Gateway VPC endpoints for S3/DynamoDB (**free**), interface endpoints; commonly 30–85% NAT bill reduction |
| Cross-AZ data transfer (AWS) | **$0.01/GB each direction** ($0.02 round trip) | Topology-aware routing, AZ-affinity, single-AZ dev |
| Public IPv4 (all clouds, since 2024) | **~$0.005/hr (~$3.65/mo) per IP** | IPv6, consolidate behind LB/NAT, release idle IPs |
| CloudWatch Logs ingestion | **$0.50/GB** (Standard) | IA class $0.25/GB, retention, sampling |
| Azure Log Analytics / Sentinel ingestion | **~$2.30/GB** Analytics tier | Basic/Auxiliary tables, commitment tiers, DCR filtering |
| GCP inter-region egress | **$0.05–0.14/GB** by pair | Region colocation, dual-region buckets, compression |
| Internet egress (all three) | ~$0.087–0.12/GB first tiers (AWS/Azure 100GB/mo free) | CDN, caching, compression |
| Unattached disks, gp2 volumes | full price while orphaned | Idle recommenders, gp3 migration |
| Snapshot sprawl | $0.05/GB-mo compounding | DLM/lifecycle, archive tier |
| Managed K8s extended support | EKS/AKS **$0.60/cluster-hr** (6x) on old versions | Upgrade cadence discipline |
| Data warehouse on-demand scans | BigQuery $6.25/TB, Athena $5/TB | Partitioning, clustering, capacity pricing, byte limits |
| Step Functions Standard | $25/M state transitions | Express workflows for high-volume |

---

## 3. Architecture Frameworks & Reliability Primitives

### 3.1 Frameworks compared

- **AWS Well-Architected Framework:** **6 pillars** — Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, **Sustainability**. Plus **lenses** (20+: Serverless, SaaS, ML, **Generative AI Lens** 2024–25, etc.), the free **Well-Architected Tool**, and the review culture (WAFR partner reviews often unlock AWS funding). Companion: **AWS CAF** (6 perspectives).
- **Azure Well-Architected Framework:** **5 pillars** — Reliability, Security, Cost Optimization, Operational Excellence, Performance Efficiency (no sustainability pillar). Design principles → checklists → tradeoffs per pillar, service guides, Advisor integration. Paired with **Cloud Adoption Framework**: Strategy → Plan → Ready (landing zones) → Adopt → Govern → Secure → Manage. **Azure Landing Zones** is the most prescriptive enterprise-scale blueprint of the three.
- **Google Cloud Well-Architected Framework** (renamed from "Architecture Framework"): **5 pillars** — Operational Excellence, Security/Privacy/Compliance, Reliability, Cost Optimization, Performance Optimization — plus cross-cutting **perspectives** (**AI/ML perspective** majorly expanded 2025). SRE-derived reliability doctrine: error budgets and SLOs are first-class citizens.
- Practical mapping: pillar content ~85% overlapping; differences are cultural — AWS: review-driven + lens depth; Azure: governance/landing-zone prescriptiveness; GCP: SRE doctrine.

### 3.2 Reliability primitives

- **Availability zones:** AWS — AZs physically separate DCs, everything meaningful zonal, cross-AZ traffic billed; all commercial regions 3+ AZs. Azure — AZs in all major regions; *zonal* vs *zone-redundant* service configs matter; some smaller regions lack zones. GCP — every region 3+ zones by design (most uniform); regional MIGs make zone-spreading nearly free cognitively.
- **Azure paired regions:** unique-to-Azure — pairs get sequenced updates, prioritized recovery, underpin GRS geo-replication. **The model is fraying: of 47 regions only ~33 have pairs; 14+ newer regions are nonpaired by design** (multi-AZ is their resiliency story); guidance shifted to **AZ-first resilience + customer-chosen DR region**. GRS requires a paired region — nonpaired regions can't use GRS. AWS/GCP have no pairing concept.
- **Placement/affinity:** AWS **placement groups** — cluster (low latency, single AZ), spread (7 instances/AZ, distinct racks), partition (up to 7/AZ, Kafka/HDFS-style). Azure — **proximity placement groups**, availability sets (legacy pre-AZ), VMSS flexible with zone + fault-domain spreading. GCP — **placement policies**: compact and spread.
- **SLA math:** serial dependencies multiply: 99.99% × 99.99% × 99.95% = **99.93%** — your stack's ceiling is below any single SLA. Redundant parallel: 1−(1−a)². Rules: (1) count *every* hard dependency (NAT, DNS, LB, identity!); (2) SLAs are financial credit instruments (10% credit below threshold, 25–30% second tier, 100% below ~95%), not engineering guarantees — credits require filing claims; (3) design to SLOs with error budgets; (4) multi-region buys past ~99.99% only if failover is rehearsed.

---

## 4. SLA Reference Table (verify quarterly; current as of Aug 2026)

| Service | AWS | Azure | GCP |
|---|---|---|---|
| **VM single instance** | 99.5% (instance-level; auto hour-credit if unavailable >6 min/hr) | **99.9% with Premium SSD/Ultra**; 99.5% Standard SSD; 95% Standard HDD | **99.9%** (99.95% memory-optimized) |
| **VM multi-AZ/zone** | **99.99% region-level** (≥2 AZs) | 99.95% availability set; **99.99% across ≥2 AZs** | **99.99%** (≥2 zones) |
| **Managed SQL DB** | RDS Multi-AZ **99.95%**; Aurora **99.99%**; DSQL multi-region 99.999% | Azure SQL DB **99.99%**; **99.995%** BC zone-redundant; 99.99% MI | Cloud SQL Enterprise **99.95%**, **Enterprise Plus 99.99%**; AlloyDB 99.99%; Spanner multi-region **99.999%** |
| **NoSQL flagship** | DynamoDB 99.99% (global tables **99.999%**) | Cosmos DB 99.99% single region; **99.999%** multi-region reads | Firestore/Bigtable multi-region 99.999% |
| **K8s control plane** | EKS **99.95%** | AKS Free: no SLA; Standard: **99.95% with AZs / 99.9% without**; Premium adds LTS | GKE zonal 99.5%; **regional/Autopilot 99.95%** |
| **Object storage** | S3 Standard SLA **99.9%** (designed-for 99.99% avail / 11 nines durability) | Hot LRS/GRS read-write **99.9%** (cool 99%); **RA-GRS reads 99.99%** | Multi/dual-region Standard **99.95%**; regional **99.9%** |
| **Credit tiers (typical)** | 10% / 25% (30% EC2) / 100% | 10% / 25% / 100% | 10% / 25% / 50% |

All SLAs are monthly-uptime, credit-only, claim-initiated (except AWS's automatic single-instance hour credit); exclusions do the heavy lifting. Azure SLA text now lives in the consolidated Microsoft Licensing SLA document.

---

## 5. Support Plans & Pricing (major 2025–26 shake-up on AWS)

### AWS — restructured at re:Invent 2025
Legacy **Developer / Business / Enterprise On-Ramp are discontinued Jan 1, 2027** (On-Ramp auto-upgraded to Enterprise during 2026 renewals). New lineup:
- **Business Support+**: min **$29/mo** per account, tiered % of monthly spend (~9% to $10K / 7% $10–80K / 5% $80–250K / 3% >$250K); AI-powered 24/7 assistance, 30-min critical response.
- **Enterprise Support**: min **$5,000/mo** (down from $15K) or 10%/7%/5%/3% tiers; designated TAM, 15-min critical response, **AWS Security Incident Response included**.
- **Unified Operations**: mission-critical tier, 5-min critical response; custom pricing.
Legacy reference (still billing until migration): Developer $29/3%; Business $100 min/10-7-5-3%; Enterprise On-Ramp $5.5K/10%.

### Azure
- **Basic** free; **Developer $29/mo**; **Standard $100/mo** (prod, 1-hr Sev A); **Professional Direct $1,000/mo** — flat fees regardless of consumption.
- **Microsoft Unified Support** (all-Microsoft): ~**8–12% of annual Microsoft spend**, ~$50K minimum — routinely the most expensive support bill in a Microsoft shop; common target for third-party substitution. Free Standard-tier support for EA customers ended July 2024.

### GCP (Customer Care)
- **Basic** free; **Standard**: **$29/mo or 3%** (4-hr P2, no P1); **Enhanced**: min **$100/mo** + 10/7/5/3% tiers — 1-hr P1; **Premium**: min **$15,000/mo** + 10/7/5/3% — 15-min P1, named TAM.

Rule-of-thumb at $100K/mo spend: AWS Business+ ≈ $6.4K/mo, Enterprise ≈ $10–15K/mo; Azure ProDirect $1K (Unified ≈ $8K+/mo equivalent); GCP Enhanced ≈ $6.9K/mo, Premium ≈ $15K/mo. GCP Standard flat 3% is the cheapest credible prod support; Azure ProDirect is a bargain at high spend (which is why Unified exists).

---

## 6. Migration & the VMware Exodus

### 6.1 Framework
The **7 Rs**: Retire, Retain, Rehost, Relocate, Repurchase, Replatform, Refactor. Portfolio reality: ~50–70% rehost/replatform in wave 1; refactor selectively. All three fund migrations: **AWS MAP**, **Azure Migrate & Modernize**, **Google RaMP** — all with VMware tracks in 2026.

### 6.2 Tooling per cloud
- **AWS:** **AWS Transform** (GA May 2025) — *agentic/GenAI* transformation for **.NET** (Framework→.NET on Linux, ~4x faster, ~40% opex cut claims), **mainframe** (COBOL→Java), **VMware** (discovery→network conversion→wave planning), and since Dec 2025 **SQL Server→PostgreSQL**. Caveat: check commercial terms (reported 24-month commitment clauses). Underneath: **AWS Transform MGN** (MGN renamed June 2026), **DMS + DMS Schema Conversion**, **Migration Hub**, Migration Evaluator.
- **Azure:** **Azure Migrate** — agentless discovery (VMware/Hyper-V/physical), **automatic agentless dependency analysis** (Sept 2025: up to 1,000 servers/appliance), business-case builder (TCO with AHB modeling), assessments, agentless replication; targets incl. **Azure Local**. Database: DMS + SQL migration extension, SSMA family for heterogeneous.
- **GCP:** **Migration Center**, **Migrate to Virtual Machines** (streaming rehost — cutover before full data copy, uniquely fast first-boot), **DMS**: homogeneous MySQL/PG/SQL Server + heterogeneous **Oracle→Cloud SQL PG/AlloyDB** and **SQL Server→PG/AlloyDB** with **Gemini-powered schema/code conversion GA**; Migrate to Containers.

### 6.3 The Broadcom/VMware exodus
Post-acquisition: perpetual licenses killed, VCF bundling forced, 72-core order minimums (Apr 2025), price increases **3–5x typical, 8–15x worst-case**; ~74% of IT leaders exploring alternatives; Gartner predicts **35% of VMware workloads migrate off by 2028**. Landing options:
- **Stay-VMware-in-cloud (Relocate):** **AVS** (mature, AHB + reserved pricing, Microsoft holds a VCF license deal); **GCVE** (mature); **Amazon EVS** — **GA Aug 5, 2025**: run **VCF in your own VPC** (BYOL VCF licenses). Economics warning: all three are appliance-priced (large bare-metal nodes); good bridge, rarely the cheap end-state.
- **Exit hypervisor:** rehost to native cloud (the default value path), or on-prem alternatives (Nutanix AHV, OpenShift Virtualization, Proxmox, Azure Local).

### 6.4 Database migration paths (heterogeneous = where the margin is)
- **SQL Server exit:** AWS **Babelfish for Aurora PostgreSQL** (T-SQL/TDS wire-protocol layer — assess with Babelfish Compass), DMS+SC, AWS Transform SQL agent; GCP DMS SQL Server→PG/AlloyDB (Gemini conversion). Azure's counter: SQL MI (near-100% compat, no rewrite) + AHB.
- **Oracle exit:** AWS SCT/DMS→Aurora PG; GCP DMS Oracle→PG/AlloyDB (Gemini-assisted, GA); Azure via SSMA/Ora2Pg. Or don't exit: **Oracle Database@AWS/@Azure/@Google Cloud** (OCI Exadata embedded in all three, GA 2024–2026).
- Rules: homogeneous = tooling problem (near-zero-downtime CDC everywhere); heterogeneous = 20% schema conversion, 80% application SQL/ORM/stored-proc remediation — GenAI assistants genuinely compress this, but budget validation/parallel-run time regardless.

---

## 7. Multi-Cloud Decision Framework

### When each cloud wins
- **Azure:** Microsoft estate gravity — Entra, M365, Windows/SQL licensing (AHB), Dynamics; enterprise governance (management groups, Policy, landing zones); hybrid (Arc, Azure Local); regulated EU (sovereign push); OpenAI-model proximity. Weaknesses: reliability track-record debates, portal/API sprawl, quota friction.
- **AWS:** breadth and depth, operational maturity, largest partner/talent market, best spot ecosystem, strongest startup path, most granular primitives; silicon cadence (Graviton5, Trainium3). Weaknesses: egress/NAT pricing complexity, multi-account sprawl without platform engineering, less natural enterprise bundling than Microsoft.
- **GCP:** data/analytics (BigQuery remains the benchmark), Kubernetes (GKE the reference implementation), AI stack (Gemini, TPUs), network quality (global VPC, premium backbone), clean project/IAM model, aggressive price-perf (Axion, predictable Spot). Weaknesses: smaller enterprise field/partner bench, deprecation reputation (improved but remembered), thinner long-tail of niche services.

### Realistic multi-cloud patterns
- **Default sane strategy: one primary cloud + deliberate exceptions** (best-of-breed data/AI, acquisitions, regulatory placement). "Run everything everywhere" doubles platform cost and halves depth of expertise.
- **Data gravity rules everything:** egress + latency make cross-cloud data planes expensive; put compute where data lives; genuinely multi-cloud data = open table formats (Iceberg/Delta) + cross-cloud query layers (BigQuery Omni, Snowflake/Databricks as the actual multi-cloud data layer).
- **K8s portability is real but bounded:** the API is portable; the operational surround (IAM, LB controllers, CSI, autoscaler behavior, meshes, managed add-ons) is not — expect 70–80% portability, abstract the last mile via GitOps + Crossplane/Terraform.
- **Identity federation:** one IdP (Entra/Okta) federated everywhere; workload-to-cloud auth via OIDC federation — no long-lived cross-cloud keys.
- **Cloud exit economics:** **EU Data Act** in force since **Sept 12, 2025**; **egress/switching fees must be cost-based now and eliminated entirely by Jan 12, 2027**. All three offer **free egress for full exits** (2024 programs; Azure requires complete subscription cancellation, AWS excludes some paths, ticket-driven). Exit-readiness (IaC coverage, no proprietary at-rest formats, documented per-workload exit cost) is now also a DORA/regulator expectation in financial services.

---

## 8. Certifications (brief, 2026)

- **AWS:** SAA-C03 → **SA Professional (SAP-C02)** remain the architecture spine. **ML Specialty retired (last sitting Mar 31, 2026)**; flanked by AI Practitioner, ML Engineer – Associate, Data Engineer – Associate, new **Generative AI Developer – Professional**. ~13 active certs; 3-year validity.
- **Azure:** **Solutions Architect Expert = AZ-305** (refreshed Apr 2026; requires active AZ-104; annual free online renewal). AZ-900 → AZ-104 → AZ-305 the architect path; AI-102 rising.
- **GCP:** **Professional Cloud Architect (PCA)** flagship ($200, 2-year validity); 2026 introduced a shorter renewal exam; renewal content leans into GenAI case studies. PCA + Professional Data Engineer = highest-value pairing.
- Market signal: cloud+AI hybrid credentials out-earn pure infra certs; FinOps Certified Practitioner is the standard badge for cost roles.

---

## Quick practitioner checklists

**30-day FinOps bootstrap (any cloud):** enable FOCUS/CUR2.0/BigQuery export day 1 → tag/label policy + enforcement → anomaly detection on → idle-resource sweep → gp2→gp3 & storage lifecycle → NAT/egress audit (endpoints!) → non-prod scheduling → then commitments to ~70–80% of the now-clean baseline.

**Commitment hygiene KPIs:** coverage 70–80%, utilization >95%, expiration runway >90 days visible, effective-savings-rate reported monthly, no purchase without a prior rightsizing pass.

**SLA design rule:** multiply serial dependencies, add redundancy where the product drops below target, and never present a provider SLA as an availability forecast — it's a refund schedule.

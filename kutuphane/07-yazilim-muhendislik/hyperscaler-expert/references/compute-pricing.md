# Hyperscaler Compute & Pricing Reference — AWS vs Azure vs GCP (August 2026)

**Verified as of: 2026-08-28.** Main sources: aws.amazon.com (EC2 instance-type pages, What's New, pricing blog), azure.microsoft.com + techcommunity.microsoft.com (Azure Compute blog, VM pricing pages), cloud.google.com (Compute Engine docs: machine-resource, sustained-use-discounts, CUD overview, TPU pricing), instances.vantage.sh, cloudprice.net, azurespeed.com, docs.aws.amazon.com, learn.microsoft.com, datacenterdynamics.com, phoronix.com, plus 2026 pricing surveys (CloudZero, usage.ai, Thunder Compute, IntuitionLabs). Prices are on-demand, Linux, us-east-1 / East US / us-central1 unless noted. Items marked "~approx, verify" could not be pinned to a first-party source.

---

## 1. Instance/VM family taxonomy and cross-cloud mapping

### AWS EC2 (letter = family, digit = generation, suffix = CPU/feature: g=Graviton, i=Intel, a=AMD, d=local NVMe, n=network, e=extra memory/storage, -flex=variable perf)

| Family | Purpose | Latest gen (Aug 2026) | CPU |
|---|---|---|---|
| M | General purpose (1:4 vCPU:GiB) | M8g, M8gd, M8i / M8i-flex, M8a | Graviton4 / Intel Xeon 6 Granite Rapids / AMD Turin |
| T | Burstable GP | T4g (Graviton2), T3/T3a | credit model, see §8 |
| C | Compute (1:2) | C8g, C8gd, C8i/C8i-flex, C8a | as above |
| R | Memory (1:8) | R8g, R8gd, R8i, R8a | as above |
| X / U | High memory (1:16 / up to 32 TiB) | X8g (Graviton4, to 3 TiB); U7i/U7in (Sapphire Rapids, 6–32 TiB, SAP HANA) | |
| I / D | Storage-optimized NVMe / dense HDD | I8g (Graviton4 + Nitro SSD v3), I7ie (Intel), D3/D3en | |
| P | GPU training | P5/P5e/P5en (H100/H200), P6-B200, P6e-GB200 | |
| G | GPU graphics/inference | G6 (L4), G6e (L40S), G6f (fractional GPU) | |
| Trn / Inf | Custom silicon | Trn2 (Trainium2), Trn3 (GA March 2026); Inf2 (Inferentia2 — line effectively end-of-road; Trainium now covers inference) | |
| Hpc | HPC | Hpc7g/Hpc7a/Hpc6id | |

**Graviton generations:** Graviton1 (A1, 2018) → Graviton2 (…6g, T4g, 2019) → Graviton3/3E (…7g, 2021–22) → **Graviton4** (…8g, 96 cores Neoverse V2, 2024; +30% perf vs G3, up to 192 vCPU / 1.5 TiB on r8g/x8g). No Graviton5 GA as of Aug 2026 (announced direction only — verify). >50% of new AWS CPU capacity is Graviton.

### Azure (D=GP, E=memory, F=compute, L=storage, M=high-mem, N=GPU, B=burstable; p=ARM, a=AMD, l=low-memory, s=premium-storage-capable)

- **Dsv6/Ddsv6** (Intel Emerald Rapids, GA 2025), **Dasv6/Dalsv6** (AMD Genoa), **Dpsv6/Dplsv6** (Cobalt 100 ARM).
- **Dsv7 / Dlsv7 / Esv7** — GA **May 7, 2026**, Intel **Xeon 6 (Granite Rapids)**, +25–30% vs v6, with next-gen Azure Boost.
- **Cobalt 200** (2nd-gen ARM, +50% vs Cobalt 100): **Dpsv7, Dplsv7, Epsv7, Mpsv4, Lpsv5 in preview** since Build 2026; broad GA rolling through 2026.
- **Esv6/Easv6/Epsv6** memory-optimized; **Fsv2, Falsv6/Fasv6/Famsv6** compute (AMD Genoa, no SMT on Fal); **Lsv3/Lasv3/Lpsv5** storage NVMe; **Mv3 / Mbsv3** high-memory to 32 TB (SAP HANA); **Bsv2/Basv2/Bpsv2** burstable; **NC/ND/NV** GPU (see §6); **HBv4/HBv5** HPC (HBv5 = custom AMD MI300C-class HBM CPU).

### GCP Compute Engine

- **E2** — cost-optimized, oversubscribable, mixed older Intel/AMD platforms, shared-core e2-micro/small/medium. No local SSD, no GPUs.
- **N2/N2D** (Ice Lake/Milan, legacy), **N4** (Intel Emerald Rapids, Titanium DPU), **N4A** (**Axion ARM, Neoverse N3, GA Jan 27, 2026**, no SMT, up to 64 vCPU), **N4D** (**AMD Turin, GA 2026**). N-series = flexible/custom shapes, price-focused.
- **C2/C2D** (legacy compute), **C3** (Sapphire Rapids), **C3D** (Genoa), **C4** (Emerald Rapids + newer Granite Rapids shapes), **C4A** (**Axion, Neoverse V2, Armv9**), **C4D** (**AMD Turin**, +30–55% on DB workloads vs C3D). C-series = consistently high performance, maintenance controls, Titanium.
- **M1/M2/M3/M4** memory-optimized; **X4** to 32 TB (SAP); **Z3** storage-optimized; **H3/H4D** HPC; **A2** (A100), **A3** (H100/H200), **A4** (B200), **A4X** (GB200), **G2** (L4), **G4** (RTX PRO 6000 Blackwell); **TPU** v5e/v5p/v6e/v7.

### Rough equivalence map (general-purpose 1:4 ratio unless noted)

| Role | AWS | Azure | GCP |
|---|---|---|---|
| GP x86 current | m8i / m8a | Dsv7 (Dsv6) / Dasv6 | c4 / n4 / c4d / n4d |
| GP ARM | m8g (Graviton4) | Dpsv6 (Cobalt 100), Dpsv7 (Cobalt 200 preview) | c4a / n4a (Axion) |
| Cost/entry | t3/t4g, m7a | Bsv2, Dalsv6 | e2 |
| Compute | c8g/c8i | Fsv2/Falsv6 | c4/c3 -highcpu, h3 |
| Memory | r8g/r8i | Esv7/Easv6 | c4/n4 -highmem, m3/m4 |
| Huge memory | x8g, u7i (32 TB) | Mv3 (32 TB) | x4 (32 TB) |
| Storage NVMe | i8g/i7ie | Lsv3/Lpsv5 | z3 |
| Burstable | t4g/t3 | B-series v2 | e2 shared-core |
| GPU training | p5/p6 | ND-series | a3/a4/a4x |

**2026 CPU platform state:** Intel Granite Rapids (AWS 8i-gen, Azure v7, GCP C4 newer shapes); Sierra Forest E-core largely absent from mainstream VM SKUs; AMD Turin/EPYC 9005 (AWS 8a, GCP C4D/N4D, Azure next AMD gen in pipeline); ARM: Graviton4 (GA broadly), Cobalt 100 GA / Cobalt 200 preview, Axion GA (C4A/N4A). ARM instances price ~10–35% below x86 equivalents on all three clouds.

---

## 2. Pricing models deep-dive

### AWS
- **On-demand**: per-second billing, 60-second minimum (Linux, Windows, and Amazon-provided images; some commercial/Marketplace AMIs still bill hourly).
- **Savings Plans** ($/hr commitment, 1 or 3 yr; No/Partial/All Upfront):
  - **Compute SP**: up to **66%** off; applies across EC2 any family/region/OS + Fargate + Lambda.
  - **EC2 Instance SP**: up to **72%**; locked to family+region, flexible size/OS/tenancy.
  - **SageMaker SP**: up to **64%** (SageMaker AI usage).
  - **Database Savings Plans**: newer addition covering RDS/Aurora et al. (~approx scope, verify).
- **Reserved Instances**: Standard RI up to **72%** (resalable on RI Marketplace, size-flexible for regional Linux/shared tenancy), Convertible RI up to ~**66%** (exchangeable). Largely superseded by SPs for EC2; still needed for RDS/ElastiCache/OpenSearch/Redshift.
- Typical realistic mid-points: 1-yr no-upfront Compute SP ~27–35%; 3-yr ~50–55%.
- **Spot**: up to **90%** off (typical 60–90%); **2-minute** interruption notice; price moves slowly per pool (no bidding since 2017); reclaim on capacity only. Best-in-class notice window.

### Azure
- **Pay-as-you-go**: billed **per minute** (unbilled seconds truncated — coarsest granularity of the three).
- **Reservations (RIs)**: up to **72%** (3-yr commonly 60–72%); scoped to VM series + region; instance-size flexibility within the series group; **exchangeable, and cancellable up to $50k/yr** (12% early-termination fee policy announced but historically waived — verify current enforcement).
- **Azure Savings Plan for Compute**: up to **65%**; hourly $ commitment applied automatically across VMs, VMSS, AKS nodes, App Service, Functions Premium, Container Instances, Dedicated Hosts, any region. Real-world: ~20–35% (1 yr), 35–55% (3 yr). Not cancellable.
- **Azure Hybrid Benefit (AHB)**: BYO Windows Server / SQL Server licenses with Software Assurance → pay Linux base rate. Stacks with reservations for headline "up to 85%" savings. Unique to Azure; the single biggest lever for Microsoft-stack workloads. Also free Extended Security Updates for legacy Windows/SQL only on Azure.
- **Spot VMs**: up to **90%** off; **30-second** best-effort eviction notice; evicted on capacity **or** when price exceeds your optional **max price** (set -1 to never be price-evicted); eviction policy per VM: **Deallocate** (default; keeps disks, still pays storage, counts against quota) or **Delete**. No SLA; B-series and some SKUs excluded.

### GCP
- **On-demand**: per-second billing, 1-minute minimum.
- **Resource-based CUDs**: commit to vCPU/RAM in a project+region+family; **37% (1 yr) / 55% (3 yr)**; memory-optimized get up to **70% (3 yr)**. No cancellation.
- **Compute Flexible CUDs (spend-based)**: billing-account-level $/hr commitment; **28% (1 yr) / 46% (3 yr)**; coverage expanded Sept 2025 to nearly all VM families incl. memory-optimized/HPC, plus Cloud Run and GKE Autopilot premiums. **Model change:** as of **Jan 21, 2026** all accounts are on the new spend-based CUD model where discounts hit SKU prices directly (invoice shows discounted rates, not offset credits).
- **Sustained Use Discounts (SUDs)**: **still exist in 2026 but legacy-only** — automatic up to ~30% (N1; ~20% for N2/N2D/C2, M1/M2) for full-month running. **Not applicable to E2, N4, N4A/N4D, C3, C3D, C4, C4A, C4D, Tau, H3, or any accelerator-optimized family** — i.e., no SUD on anything Google now recommends. Treat SUD as dead for new deployments; CUDs are the mechanism.
- **Spot VMs**: fixed **60–91%** discount per SKU (published, changes at most monthly — predictable, unlike AWS); **30-second** preemption notice; **no 24-hour runtime limit** (that limit only applies to legacy "preemptible" VMs, still creatable for backwards compatibility). No SLA, no live migration.

**Commitment comparison cheat-sheet:** flexible tier — AWS Compute SP 66% > Azure SP 65% > GCP Flex CUD 46% (3 yr). Locked tier — AWS EC2 SP / Azure RI ≈ 72% vs GCP resource CUD 55% (70% mem-opt). GCP's locked ceiling is lower, but its on-demand list prices for equivalent hardware are often already lower.

---

## 3. Concrete price anchors (on-demand, Linux, Aug 2026)

**us-east-1 / East US / us-central1**

| Shape (2 vCPU / 8 GiB) | $/hr | ≈$/mo (730h) |
|---|---|---|
| AWS m7g.large (Graviton3) | $0.0816 | $59.6 |
| AWS m8g.large (Graviton4) | $0.0898 | $65.5 |
| AWS m7i.large (Intel) | $0.1008 | $73.6 |
| AWS m8i.large (Intel GNR) | ~$0.106 ~approx, verify | ~$77 |
| Azure D2ps v6 (Cobalt 100) | ~$0.070 | ~$51 |
| Azure D2s v6 (Intel) | ~$0.101 | ~$74 |
| GCP e2-standard-2 | $0.067 | $48.9 |
| GCP c4a-standard-2 (Axion) | ~$0.090 ~approx, verify | ~$66 |
| GCP n4-standard-2 | ~$0.0907 | ~$66 |

| Shape (4 vCPU / 16 GiB) | $/hr | ≈$/mo |
|---|---|---|
| AWS m8g.xlarge | $0.1795 | $131 |
| AWS m7i.xlarge | $0.2016 | $147 |
| Azure D4ps v6 (Cobalt) | $0.140 | $102 |
| Azure D4s v6 (Intel) | $0.202 | $147.5 |
| GCP e2-standard-4 | $0.134 | $97.8 |
| GCP c4a-standard-4 (Axion) | ~$0.1795 | $131 |
| GCP n4-standard-4 | $0.1814 | $132 |

Patterns: ARM is the price floor on every cloud (Azure Cobalt is aggressively priced ~30% under Intel v6; AWS Graviton ~11–20% under Intel; Axion ≈ price of N4 with ~+30% claimed perf). GCP E2 is cheapest x86 sticker but oldest silicon. Azure Intel D-series carries the highest GP x86 list price of the three. GCP 3-yr CUD example: e2-standard-4 → $0.0603/hr.

**Billing granularity recap:** AWS per-second/60s-min; GCP per-second/60s-min; **Azure per-minute** (partial minutes dropped). Stopped-deallocated VMs: compute unbilled on all three; disks/IPs still billed. Azure spot "Deallocate" evictions keep billing storage.

---

## 4. Data transfer / egress

### Internet egress (from US regions, per GB, after free allowance)

| Tier | AWS | Azure (Zone 1) | GCP Premium | GCP Standard |
|---|---|---|---|---|
| Free/mo | **100 GB** (org-wide, all regions) | **100 GB** | none broadly (1 GB always-free tier) | none |
| First 10 TB | $0.09 | $0.087 | $0.12 (0–1 TB), $0.11 (1–10 TB) ~approx, verify | $0.085 |
| 10–50 TB | $0.085 | $0.083 | $0.08 >10 TB ~approx, verify | $0.065 |
| 50–150 TB | $0.07 | $0.07 | — | $0.045 >150 TB |
| >150 TB | $0.05 | $0.05 | negotiate | — |

GCP Standard Tier (non-Google backbone, no global LB) is the cheap path; Premium is default. Data **ingress is free** on all three.

### Intra-cloud transfer — the classic bill surprises
- **AWS cross-AZ**: **$0.01/GB in EACH direction = effectively $0.02/GB** for a round hop; same-AZ private IP free; via public/Elastic IP charged even in-AZ. NAT Gateway adds $0.045/GB processing + hourly — the #1 surprise line item. Inter-region: $0.02/GB typical US↔US (from us-east-1; $0.01 to us-east-2).
- **Azure cross-AZ**: **free** (Microsoft cancelled planned inter-AZ charges; intra-region VNet traffic free). Inter-VNet peering: $0.01/GB each side. Inter-region: $0.02/GB within North America (up to $0.16 intercontinental).
- **GCP cross-zone**: **$0.01/GB**; same-zone internal free; inter-region within US $0.02/GB (to $0.14 intercontinental).

Kafka/Cassandra/multi-AZ chatty microservices: AWS and GCP charge for AZ redundancy; Azure doesn't — material at scale.

### EU Data Act / exit programs
All three waived egress fees for customers **leaving the cloud** (2024 programs, global, not EU-only): **Google** (Jan 2024, requires full termination of Google Cloud), **AWS** (Mar 2024, request credits, 60-day window, full account closure not strictly required), **Azure** (Mar 2024, notify start date, 60 days, must cancel all subscriptions; internet egress route only). EU Data Act applies since **Sept 2025**; from **Jan 12, 2027** all switching charges (incl. switching egress) are banned for EU customers, and providers must support switching/parallel use.

---

## 5. Free tiers (Aug 2026)

- **AWS — revamped July 15, 2025.** New accounts: **Free Plan** = **$100 credit at signup + $100** more for completing 5 onboarding tasks (EC2, RDS, Lambda, Bedrock, Budgets); valid **6 months**; no card charges possible; account auto-closes after 6 months/credit exhaustion unless upgraded to Paid Plan (credits carry over). The old 12-month tier (750 h t2/t3.micro etc.) applies **only to accounts created before 2025-07-15**. **Always-free** unchanged: Lambda 1M req + 400k GB-s/mo, DynamoDB 25 GB, CloudFront 1 TB egress/mo, SQS 1M, 100 GB general egress/mo.
- **Azure**: **$200 credit / 30 days** + 12 months of free monthly quantities (750 h B1s or B2pts v2/B2ats v2 VM, 2×64 GB SSD, 5 GB Blob, 250 GB SQL DB) + **55+ always-free** services (Functions 1M exec/mo, Cosmos DB 1000 RU/s + 25 GB, AKS control plane free).
- **GCP**: **$300 credit / 90 days** + **always-free** (no expiry): **e2-micro 744 h/mo** in us-west1/us-central1/us-east1 + 30 GB standard PD, 5 GB regional GCS, 1 GB/mo NA egress, BigQuery 1 TB query + 10 GB storage/mo, Cloud Run 2M req/mo.

---

## 6. GPUs / accelerators

### NVIDIA availability per cloud (Aug 2026)
| Chip | AWS | Azure | GCP |
|---|---|---|---|
| H100 | P5 (8×) | ND H100 v5, NC H100 v5 | A3 High/Mega |
| H200 | P5e/P5en | ND H200 v5 | A3 Ultra |
| B200 | P6-B200 | ND B200 (via NDv6) | A4 |
| GB200 NVL72 | P6e-GB200 UltraServers (GA Jul 2025) | ND GB200 v6 (GA early 2025) | A4X |
| GB300/B300 | announced/rolling | ND GB300 v6 | A4X Max |
| L4 / L40S / RTX 6000 | G6 / G6e | NCads, NV | G2 / G4 |

### Hyperscaler on-demand anchors (per 8-GPU instance)
- **AWS p5.48xlarge (8×H100)**: **$55.04/hr = $6.88/GPU-hr** in us-east-1, after the **June 2025 price cut** (−44% H100, −25% H200, −33% A100 — first big GPU cut). Counter-move: **Jan 2026 +15% increase on H200 (P5e/P5en)** on demand-driven scarcity; H200 8-GPU now ~$73/hr ~approx, verify.
- **GCP a3-highgpu-8g (8×H100)**: **$87.83/hr** (us-central1) ≈ $11/GPU-hr. GCP B200 (A4) on-demand tracked at ~$16.11/GPU-hr — highest hyperscaler B200 rate ~approx, verify.
- **Azure ND96isr H100 v5**: ~**$98.32/hr** ≈ $12.29/GPU-hr ~approx, verify.
- Specialist clouds undercut heavily (H100: Lambda $2.99–3.99, CoreWeave ~$4.25, marketplaces $1.49–2.50) — hyperscaler on-demand GPU is the price ceiling; real large-scale deals are private/committed (AWS Capacity Blocks, Azure capacity reservations, GCP Dynamic Workload Scheduler).

### Custom silicon
- **AWS Trainium**: Trn2 (Trainium2, GA Dec 2024, Trn2 UltraServers 64-chip); **Trainium3 GA March 2026** (3 nm, 2.52 PFLOPS FP8, 144 GB HBM3e); Trainium4 late-2026/2027. **Inferentia line discontinued** going forward (Inf2 still purchasable); Trainium covers inference. Trn2 on-demand list ~approx, verify — most capacity sold via Capacity Blocks/EDP. Anthropic's Project Rainier is the flagship deployment.
- **Google TPU**: on-demand per chip-hour: **v5e $1.20, v5p $4.20, v6e Trillium $2.70**; **v7 Ironwood GA April 2026** (192 GB HBM3e, 4,614 FP8 TFLOPS, 9,216-chip pods) — **no reliable public list price** (reports range from ~$1.60 negotiated to a ~$12 list figure; verify with sales). 1-yr/3-yr commitments cut TPU rates ~35–55%.
- **Azure Maia**: Maia 100 (internal); **Maia 200 announced Jan 2026** — in production for Microsoft first-party (Copilot/OpenAI-serving) workloads, US Central first; **not a general rentable SKU yet**; Azure's rentable AI fleet remains NVIDIA ND-series. Cobalt 200 covers CPU side.

---

## 7. Licensing gotchas (Microsoft & Oracle)

- **Microsoft "Listed Provider" rule (Oct 2019)**: AWS, GCP, Alibaba (and Azure, nominally) are "Listed Providers." Licenses bought **after Oct 1, 2019 without** applicable rights **cannot** be BYOL'd onto Listed Providers' shared **or** dedicated hardware except via License Mobility (SA required, and **Windows Server has no License Mobility** — SQL Server does). Practical result: on AWS/GCP you either pay license-included rates or use dedicated hosts with pre-Oct-2019 licenses (frozen at WS2019).
- **SPLA squeeze**: from **Sept 30 / Oct 1, 2025**, service providers can no longer deploy their own SPLA licenses in Listed Provider clouds — hosters on AWS/GCP must use the hyperscaler's license-included SKUs.
- **Azure Hybrid Benefit**: Windows Server + SQL Server with SA convert to Azure at Linux base rates; free Extended Security Updates for out-of-support Windows/SQL only on Azure. This is a deliberate, structural Azure price advantage for Microsoft estates: license-included Windows on AWS adds roughly $0.046/vCPU-hr (~$92/mo on 4 vCPU) ~approx, verify; SQL Server Enterprise license-included can exceed the compute cost several-fold.
- **SQL Server on AWS/GCP**: legal via License Mobility (active SA) on shared tenancy, or license-included. GCP sole-tenant nodes + BYOL is the cost-optimization path for large SQL estates.
- **Oracle**: "Authorized Cloud Environment" policy (a *policy*, not a contract term): **2 vCPUs (SMT on) = 1 processor license; core factor table does NOT apply** → effectively **2× the licenses vs on-prem** x86 (where 0.5 core factor applies). Policy covers AWS EC2/RDS and Azure; **GCP is not an Authorized Cloud Environment** in the official document (running Oracle there = count physical hosts / high audit risk — verify current policy PDF). OCI counts 2 vCPU = 1 OCPU = 1 license with core factor economics and is priced to pull Oracle workloads.

---

## 8. Sizing & performance notes

- **vCPU ≠ vCPU across clouds.** x86 with SMT: 1 vCPU = 1 hyperthread (half a core) on AWS/Azure/GCP. **ARM and no-SMT SKUs: 1 vCPU = 1 physical core** — Graviton, Cobalt, Axion (C4A/N4A), GCP Tau T2D, Azure Falsv6. An 8-vCPU Graviton/Axion box has 8 cores vs 4 cores on 8-vCPU Intel — a big chunk of ARM "price-performance" claims. Benchmark per-instance, not per-vCPU.
- **GCP N4A/C4A**: no SMT, UMA memory domains; **E2**: CPU oversubscription possible (min-CPU-platform not selectable), fine for dev/steady-low, wrong for latency-sensitive.
- **Burstable models**:
  - **AWS T3/T3a/T4g**: earn credits below baseline (t3.micro 10%, t3.large 30%, t3.xlarge 40%); **Unlimited mode default on T3+** — bursts indefinitely, surplus billed **$0.05/vCPU-hr (Linux)**; a pegged t3 in unlimited mode can cost more than an m-family instance. T4g = Graviton2, ~40% better price-perf than T3.
  - **Azure Bsv2/Basv2/Bpsv2**: credit banking (up to ~72h of credits), **no unlimited mode** — credits exhausted = hard throttle to baseline. Cheapest steady-state SKUs on Azure; not spot-eligible.
  - **GCP E2 shared-core (micro/small/medium)**: fractional vCPU with time-limited bursting above baseline, **no credit bank, no burst charge**; predefined E2 (standard-2+) are not burstable — they're plain oversubscribed VMs.
- **"Flex" SKUs**: AWS M7i/M8i-flex and C7i/C8i-flex — ~5% cheaper, full CPU 95% of the time (min 40% guaranteed); the default recommendation for generic web/app tiers.
- **Rightsizing economics**: on all three, doubling a size exactly doubles price (linear), so downsizing beats committing; combine: ARM + 3-yr commitment + (Azure) AHB stacks multiplicatively — e.g., Azure D4ps v6 3-yr RI lands well under half the Intel PAYG rate; AWS m8g + 3-yr EC2 SP ≈ $0.05–0.06/hr for 2c/8GB class ~approx, verify.

---

### One-paragraph strategic summary
In 2026 the clouds have converged on architecture (Granite Rapids / Turin / in-house ARM everywhere; DPU offload — Nitro, Azure Boost, Titanium — universal) and diverged on commercial mechanics: AWS has the deepest, most liquid commitment market (SPs + RI marketplace) and cut GPU prices under competitive pressure while raising scarce H200 rates; Azure competes on per-workload leverage (AHB, free cross-AZ, ARM priced ~30% under Intel) but bills per-minute and holds the highest x86 and GPU list prices; GCP has the lowest headline commitment ceilings but low on-demand ARM/E2 floors, uniquely predictable spot pricing, TPUs as the only mature non-NVIDIA rentable accelerator at scale — and its famous sustained-use discount is now legacy-only trivia. The recurring bill surprises remain identical across all three: NAT/cross-AZ traffic (AWS), spot-deallocate storage and license-included SQL (Azure), Premium-tier egress and CUD lock-in scoping (GCP).

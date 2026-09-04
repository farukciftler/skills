# Kubernetes, Containers & Serverless: AWS vs Azure vs GCP — Expert Reference

**Verified as of: 2026-08-28** (web-verified pricing/GA statuses; region-variable prices quoted for US East / us-central1 list prices unless noted). Items not re-verified this week are marked **~verify**.

**Main sources:** aws.amazon.com/eks/pricing, aws.amazon.com/lambda/pricing, aws.amazon.com/blogs/compute (INIT billing), docs.aws.amazon.com (ECS Express Mode, Hybrid Nodes, SQS fair queues), learn.microsoft.com (AKS tiers, AKS Automatic, NAP, Flex Consumption, ACA serverless GPU GA), azure.microsoft.com/pricing (Functions, Container Apps, APIM), cloud.google.com/kubernetes-engine/pricing, cloud.google.com/blog (Cloud Run GPU GA, container-optimized compute, KubeCon 2025/2026), docs.cloud.google.com (Eventarc Advanced, App Engine migration center, Cloud Run/functions release notes), infoq.com (App Runner maintenance mode, ECS Express Mode), Azure/AKS GitHub releases.

---

## 1. Managed Kubernetes: EKS vs AKS vs GKE

### 1.1 Control plane pricing

| | **EKS** | **AKS** | **GKE** |
|---|---|---|---|
| Base fee | $0.10/cluster-hr (~$73/mo), all clusters | **Free tier**: $0 (no SLA, ≤1,000 nodes, dev/small prod); **Standard**: $0.10/cluster-hr, 99.95% SLA (AZ) / 99.9% (non-AZ), ≤5,000 nodes; **Premium**: $0.60/cluster-hr (includes LTS) | $0.10/cluster-hr; **$74.40/mo free credit per billing account** (covers one zonal or Autopilot cluster's fee) |
| Extended/LTS surcharge | Extended support: **$0.60/cluster-hr** (6x) | LTS included in Premium tier ($0.60/hr total) | Extended support: **+$0.50/cluster-hr** on top of $0.10 = $0.60 total |
| Managed-mode premium | **EKS Auto Mode**: additional per-instance management fee ≈ **10–12% of the On-Demand instance price** (e.g., m5.large us-east-1: +$0.01152/hr on $0.096/hr), billed per-second, 1-min minimum, charged even on Spot/Savings-Plan instances | **AKS Automatic**: no separate SKU fee; requires Standard tier ($0.10/hr) + you pay VMs (system node pools now managed) | **Autopilot**: no separate fee beyond $0.10/hr cluster fee; you pay per-pod resource requests instead of per-VM |
| Enterprise/fleet SKU | — (EKS Hybrid Nodes billed separately, see 1.8) | Premium tier | **GKE Enterprise**: $0.00274/vCPU-hr (~$2/vCPU-mo) across fleet; includes Extended channel at no extra fee, Config/Policy mgmt, service mesh, multi-cluster console |

Notable: AKS is the only one with a genuinely free control plane. GKE's free credit effectively makes one small cluster's management free. EKS is the only one that charges for its "auto" mode as a % of compute — at fleet scale EKS Auto Mode's ~10% adder is a real line item; compare against self-managed Karpenter (free, more ops).

### 1.2 Version support windows

| | **EKS** | **AKS** | **GKE** |
|---|---|---|---|
| Standard window | ~14 months per minor from EKS release | ~12 months community support per minor (N-2 policy) | ~14 months (Stable/Regular channels) |
| Extended | +12 months at $0.60/hr (total ~26 mo) — automatic, you're silently moved (and billed) when standard ends | **LTS**: 2 years total per LTS-designated version, Premium tier only; Microsoft backports CVE fixes | **Extended channel**: up to 24 months total per minor; free during standard period, +$0.50/hr after standard ends; included free in GKE Enterprise |
| As of mid-2026 | 1.33/1.34/1.35 in standard support (1.33 exits standard ~Jul–Aug 2026) | Follows upstream closely; check release tracker — AKS ships new minors within weeks | Rapid channel typically first to new minors among the three |
| Gotcha | Extended support billing surprise is the #1 EKS cost incident; no opt-out except upgrading | LTS requires opting into LTS versions specifically, not every minor is LTS | Extended requires being on Extended channel before standard EOL |

All three now auto-upgrade control planes past EOL eventually; none will run an unsupported version indefinitely.

### 1.3 Node management & autoscaling stacks

- **EKS**: **Karpenter** (AWS-born, now CNCF) is the de-facto standard — NodePool/EC2NodeClass CRDs, bin-packing, consolidation, spot interruption handling. Cluster Autoscaler + managed node groups still supported but legacy-feeling. **EKS Auto Mode** (GA Dec 2024) = managed Karpenter + managed AMIs (Bottlerocket-based), 21-day max node lifetime, built-in EBS CSI/LB controller/CNI lifecycle — nodes are not SSH-able, AWS patches them.
- **AKS**: **Node Auto-Provisioning (NAP)** = managed **karpenter-provider-azure**, GA (mid-2025, matured through early 2026). Runs as managed addon (recommended) or self-hosted. Cluster Autoscaler on VMSS node pools remains the default for many. **AKS Automatic** (GA Jan 2026): opinionated mode — NAP, KEDA, VPA, managed Prometheus/Grafana, Azure Linux, deployment safeguards all pre-wired; managed system node pools GA.
- **GKE**: **Autopilot** — Google owns nodes entirely; you request pod resources. 2025's **container-optimized compute platform**: dynamically resizable nodes (fraction-of-CPU granularity, no workload disruption), up to 7x faster pod scheduling. Big 2025 change: **Autopilot ComputeClasses on Standard clusters** (`autopilot`/`autopilot-spot` classes) — per-workload Autopilot pricing/ops inside a Standard cluster. Standard mode still has Node Auto-Provisioning (the original NAP) + Cluster Autoscaler.
- Pod-level autoscaling: all three ship HPA/VPA; KEDA is a managed addon on AKS (core to Automatic), self-installed on EKS (or via Auto Mode compatible), GKE has native scale-to-zero-ish via Autopilot + KEDA self-managed.

### 1.4 Networking / CNI

| | **EKS** | **AKS** | **GKE** |
|---|---|---|---|
| Default | **AWS VPC CNI**: pod IPs are real VPC IPs from ENIs. IP exhaustion is the classic failure mode — mitigate with prefix delegation (/28 per ENI slot), secondary CIDRs, custom networking, or IPv6 | **Azure CNI Overlay** (now the recommended default): pods from private overlay CIDR, node IPs from VNet — solves IP exhaustion. Legacy: Azure CNI (VNet IPs per pod), **kubenet deprecated** (retirement announced, ~2028 ~verify) | **Dataplane V2** = managed **Cilium/eBPF**, default on Autopilot and new Standard clusters. Native NetworkPolicy, Hubble-based observability |
| eBPF/Cilium story | Not native; Cilium installable (chaining or replacement, self-supported); Isovalent-on-AWS common | **Azure CNI powered by Cilium** GA — eBPF dataplane with Azure IPAM (overlay or VNet) | Native (Dataplane V2 *is* Cilium) |
| Notes | Security groups per pod; IPv6 clusters mature | Advanced Container Networking Services (ACNS) addon: FQDN filtering, L7 policy, flow logs (paid) | FQDN/CiliumNetworkPolicy support; multi-network pods |

### 1.5 Serverless / nodeless pods

- **Fargate on EKS**: one pod = one micro-VM, Fargate pricing (~$0.04048/vCPU-hr + $0.004445/GB-hr us-east-1 ~verify) + EKS fee. No DaemonSets, no EBS, GPU unsupported, sidecar resources count. Momentum has clearly shifted to Auto Mode/Karpenter; Fargate-EKS is stagnant but not deprecated.
- **AKS virtual nodes** (ACI-backed, Virtual Kubelet): burst pods to ACI. Real-world caveats (networking, DaemonSets, limited K8s features) keep adoption niche; ACI's newer "standby pools" help cold starts ~verify.
- **GKE Autopilot**: the strongest "serverless nodes" story — it's the whole cluster model, not a bolt-on. Autopilot pricing ≈ $0.0445/vCPU-hr + $0.0049/GiB-hr (general-purpose, ~verify exact current list) with spot pods and CUD coverage (Flex CUDs: 28%/1-yr, 46%/3-yr spanning GKE Autopilot + Cloud Run + Compute).

### 1.6 2025–2026 changes summary

- **EKS Auto Mode** GA (re:Invent 2024), continuously expanded 2025–26; EKS also raised scale ceiling to ~100k nodes/cluster (announced 2025, ~verify).
- **AKS Automatic GA (Jan 2026)** — Azure's Autopilot answer; NAP GA; Azure Linux 3 default.
- **GKE**: container-optimized compute, Autopilot classes on Standard clusters (Sep 2025), Autopilot increasingly the default posture; GKE Enterprise continues as vCPU-priced premium tier.

### 1.7 Fleet / hybrid

- **EKS Hybrid Nodes** (GA): join on-prem/edge VMs & bare metal to a cloud EKS control plane. Priced per vCPU-hr, tiered: **$0.020 → $0.006/vCPU-hr** as monthly volume grows (tiers from 576k to >11.5M vCPU-hrs, org-consolidated per region). Also: EKS Anywhere (self-managed, Enterprise subscription), EKS Distro.
- **AKS Fleet Manager**: multi-cluster update orchestration (update runs/staged rollouts), Kubernetes config propagation, multi-cluster L4 load balancing. Hub cluster free-ish (standard hub billed as AKS ~verify). Azure Arc-enabled Kubernetes for attach-anywhere ($ per vCPU/mo for Arc addons ~verify).
- **GKE Fleets**: fleet concept is free plumbing; paid value (Config Sync, Policy Controller, mesh, multi-cluster ingress at scale) rides on GKE Enterprise. GKE on-prem/multicloud via Google Distributed Cloud.

### 1.8 Picking

- Deep AWS shop, cost-engineering culture: EKS + self-managed Karpenter (Auto Mode if you'll pay ~10% for ops relief).
- Lowest control-plane cost / Microsoft estate: AKS Standard (Automatic for new teams).
- Best-managed Kubernetes, fastest upstream, least node ops: GKE Autopilot — still the technical benchmark.

---

## 2. Serverless containers

### 2.1 The big three

| | **ECS + Fargate** | **Azure Container Apps (ACA)** | **Cloud Run** |
|---|---|---|---|
| Model | Task/service orchestrator; Fargate = per-task micro-VMs | Managed app platform on AKS+KEDA+Envoy+Dapr | Knative-shaped request-serving platform |
| Pricing | ~$0.04048/vCPU-hr + $0.004445/GB-hr (x86, us-east-1; ARM ~20% less; Spot ~70% off; 1-min minimum) ~verify exact | **Consumption**: ~$0.000024/vCPU-s active + $0.000003/GiB-s (+idle rates lower); free grant 180k vCPU-s, 360k GiB-s, 2M requests/mo. **Dedicated (workload profiles)**: per-node (D/E/NC series) + fixed management charge | **Request-based (default)**: $0.000024/vCPU-s + $0.0000025/GiB-s billed only while handling requests, + $0.40/M requests. **Instance-based**: $0.000018/vCPU-s + $0.000002/GiB-s for full instance lifetime, no per-request fee. Free tier: 180k vCPU-s, 360k GiB-s, 2M req/mo ~verify exact rates |
| Scale to zero | **No** (an ECS service scaled to 0 behind an ALB just 503s; you pay ALB regardless) | Yes (Consumption; HTTP + KEDA scalers) | Yes (min-instances=0) |
| Cold start | Fargate task launch ~30–60s (image pull dominates; SOCI lazy-loading helps) | Historically 10–30s; improved but still seconds-class | Sub-second to a few seconds; startup CPU boost; best-in-class |
| GPU | No Fargate GPU (GPU = ECS on EC2) | **Serverless GPUs GA**: A100 & T4, scale-to-zero, per-second (~$0.000529/s A100 East US); also dedicated GPU profiles | **Cloud Run GPU GA (Jun 2025)**: NVIDIA L4, no quota request, per-second (~$0.67/hr L4 without zonal redundancy), scale-to-zero, ~5s GPU instance start |
| Jobs | ECS standalone tasks / Step Functions / EventBridge Scheduler | **ACA Jobs** GA (manual/scheduled/event-driven) | **Cloud Run Jobs** GA (+ Cloud Run **worker pools** for pull-based/Kafka workloads, 2025 ~verify GA) |
| Sidecars | Native (task = N containers) | Yes (+ init containers, Dapr sidecar built-in) | Yes (multi-container GA), incl. sidecar health probes |
| Concurrency | N/A (task-level) | Per-replica HTTP concurrency (KEDA) | Up to 1,000 concurrent req/instance — the key cost lever |
| Max size | 16 vCPU / 120GB per task | Consumption: up to 4 vCPU/8GiB (bigger on dedicated profiles) | 8 vCPU / 32GiB |

**Cloud Run billing nuance (2024+ naming)**: "request-based" = old CPU-only-during-requests; "instance-based" = always-on CPU, cheaper unit rates, required for background work/GPU-less streaming; GPU requires instance-based ~verify.

### 2.2 The second tier

- **AWS App Runner — effectively dead**: moved to **maintenance mode; no new customers after April 30, 2026**; existing services keep running, no new features. AWS's official successor: **ECS Express Mode** (GA late 2025) — give it an image + 2 IAM roles, get Fargate service + VPC + ALB (shared across services) + autoscaling + auto domain; **no additional charge**, pay underlying resources (~$27–29/mo minimal). Migrate App Runner workloads to ECS Express or Lambda.
- **Azure Container Instances (ACI)**: raw per-second containers (~$0.0000125/vCPU-s + ~$0.0000014/GiB-s ~verify), no orchestration/scaling; niche: CI agents, burst, AKS virtual nodes backend, standby pools.
- **Azure App Service (containers)**: full PaaS with plans (see §7) — still the mainstream Azure web-app host; ACA is the strategic container play.

---

## 3. FaaS: Lambda vs Azure Functions vs Cloud Run functions

| | **AWS Lambda** | **Azure Functions** | **Cloud Run functions** (ex-Cloud Functions) |
|---|---|---|---|
| Pricing | $0.20/M requests + $0.0000166667/GB-s (x86; ARM ~$0.0000133); free: 1M req + 400k GB-s/mo | Consumption (classic): $0.20/M + $0.000016/GB-s, same free grant. **Flex Consumption**: per-execution + GB-s (on-demand ~$0.000026/GB-s East US ~verify); always-ready instances: idle baseline ~$0.000004/GB-s + execution ~$0.000016/GB-s + $0.40/M executions, **no free grant when always-ready enabled** | Billed as Cloud Run (gen2 = Cloud Run under the hood): vCPU-s + GiB-s + $0.40/M invocations, Cloud Run free tier applies |
| **2025 billing change** | **Since Aug 1, 2025: INIT (cold-start) phase is billed** for ZIP-packaged managed runtimes (previously free). Standardizes with container images. Hits Java/.NET (long init) and spiky low-traffic fns most; watch `InitDuration` | — | — |
| Max duration | 15 min | Consumption: 10 min; Flex: no enforced max (default 30 min ~verify); Premium/Dedicated: unbounded-ish | 60 min (HTTP), event-driven typically 10–60 min by trigger |
| Max memory/CPU | 10GB / 6 vCPU; 10GB container images | Flex: 2048/4096MB instance sizes; Premium: up to 14GB | Up to 32GiB / 8 vCPU (Cloud Run limits) |
| Concurrency model | **1 request : 1 sandbox** (Firecracker). Account concurrency default 1,000 (raisable to 10k+). Reserved & provisioned concurrency knobs | Plan-based: many requests per instance (host process); Flex adds **per-instance concurrency** setting + per-function scaling; Durable Functions for stateful orchestration | **Up to 1,000 concurrent requests per instance** — huge cost/cold-start advantage for I/O-bound work |
| Cold start mitigation | **Provisioned Concurrency** ($0.0000041667/GB-s + reduced duration rate ~verify); **SnapStart**: Java (free), Python/.NET GA — priced: cache $0.0000015046/GB-s (3-hr min) + $0.00014/GB restored | **Premium plan** (EP1-3: pre-warmed + always-ready, ~$0.173/vCPU-hr ~verify); Flex **always-ready instances** | **min-instances** (billed at idle rate ~10% of active ~verify); startup CPU boost |
| Runtimes | Node, Python, Java, .NET, Ruby, Go/Rust via OS-only, custom via containers | .NET (isolated), Node, Python, Java, PowerShell, custom handlers | Node, Python, Go, Java, .NET, Ruby, PHP + any container (it's Cloud Run) |
| Notes | Response streaming; Lambda@Edge/CloudFront Functions for edge | Classic Linux Consumption being sunset in favor of **Flex Consumption** (retirement ~2028 announced ~verify); Flex adds VNet at consumption price point | 1st-gen functions still exist but 2nd-gen/Cloud Run functions is the only sane target; deploy from source → buildpacks → Cloud Run |

**Expert take**: Lambda still has the richest event-source ecosystem and per-request isolation; Cloud Run functions wins on concurrency economics and 60-min timeouts; Azure Flex Consumption finally fixed Functions' VNet+cold-start story but pricing is fiddly (always-ready kills the free grant). The Lambda INIT change (Aug 2025) quietly raised bills for Java-heavy, low-traffic fleets — SnapStart or provisioned concurrency are the levers.

---

## 4. Eventing & orchestration

### 4.1 Event routers

| | **EventBridge** | **Event Grid** | **Eventarc** |
|---|---|---|---|
| Pricing | $1.00/M custom events (AWS-service events to default bus free); Pipes $0.40/M; Scheduler $1.00/M invocations ~verify | $0.60/M operations, first 100k/mo free; namespaces (MQTT/pull) priced separately | **Standard**: no Eventarc fee — you pay underlying Pub/Sub. **Advanced** (bus/enrollments, transformations, external HTTP destinations): per-event pricing ~verify rates; GA'd 2025 ~verify |
| Strengths | Schema registry, archive+replay, 28 SaaS partner sources, cross-account buses | MQTT broker (IoT), CloudEvents-native, push+pull delivery, huge Azure-source coverage | CloudEvents-native, 90+ Google sources via audit logs; Advanced finally adds real routing/transformation |
| Gotchas | 256KB event max; latency ~0.5s p50 (not for hot paths); rule limits per bus | Basic vs namespace tiers confuse; advanced filtering per-subscription | Standard is thin (no external destinations, no transforms) — evaluate Advanced |

### 4.2 Workflow orchestration

- **Step Functions**: Standard $25 per **million state transitions** (expensive for chatty workflows — the classic bill shock); Express: $1.00/M requests + GB-s duration (for high-volume, <5 min). Distributed Map for large-scale fan-out; native SDK integrations (200+ services) cut Lambda glue.
- **Azure**: **Durable Functions** (code-first, runs on any Functions plan — pay execution + storage transactions; storage-account chatter is the hidden cost) and **Logic Apps** (designer-first; Consumption: per-action/connector pricing $0.000025 built-in, $0.000125 standard connector ~verify; Standard: single-tenant, vCPU-priced).
- **GCP Workflows**: $0.01 per 1k internal steps (5k/mo free), $0.025/1k external HTTP calls (2k free) ~verify — cheapest by far, but YAML-based, weaker ecosystem; heavy lifting often lands in Cloud Run jobs instead.

### 4.3 Queues & pub/sub

| | **AWS** | **Azure** | **GCP** |
|---|---|---|---|
| Queue | **SQS**: $0.40/M requests standard, $0.50/M FIFO (64KB-chunk billing — a 256KB message = 4 requests). FIFO: 300 msg/s unbatched, 3k batched, high-throughput mode ~70k/s per region-dependent limits ~verify. **Fair queues (Jul 2025)**: message-group-based anti-noisy-neighbor for standard queues (EventBridge & SNS integration added late 2025) | **Storage Queues**: cheap, 64KB msgs, no ordering. **Service Bus**: Basic $0.05/M ops; Standard: base charge + $0.80/M ops (brokered-connection limits sneaky); **Premium**: per messaging-unit ~$677/mo/MU — needed for VNet, >1MB messages (up to 100MB), predictable latency. Sessions/transactions/dedup = the enterprise feature set AWS lacks natively | **Pub/Sub**: $40/TiB throughput (first 10GiB/mo free); no per-message fee. **Pub/Sub Lite deprecated/retired (Mar 2026)** ~verify. Ordering keys, **exactly-once delivery** (regional, subscription-scoped) |
| Fan-out | SNS $0.50/M publishes; FIFO topics pair with FIFO queues | Service Bus topics; Event Grid for reactive | Pub/Sub is unified queue+fan-out |
| Exactly-once claims | SQS FIFO: exactly-once **processing** within 5-min dedup window (producer-side dedup ID) — consumers still need idempotency | Service Bus: dedup window + peek-lock; transactions across entities (Premium) | Pub/Sub exactly-once: valid only within region & while ack deadline honored — still design idempotent |

---

## 5. API management

| | **AWS API Gateway** | **Azure API Management** | **Google: Apigee / API Gateway / Cloud Endpoints** |
|---|---|---|---|
| Serverless tier | **HTTP APIs: $1.00/M** (first 300M, then $0.90) — vs **REST APIs: $3.50/M** + worse caching pricing. HTTP APIs = ~70% cheaper but no API keys/usage plans/WAF-native/request validation; REST needed for those + private APIs ~verify feature drift | **Consumption**: ~$0.042/10k calls, 1M free ~verify | **API Gateway**: $3.00/M after 2M free (drops at 1B+) ~verify — thin Envoy-based, for Cloud Run/Functions backends |
| Dedicated | — (pay-per-call only; 10k RPS default limit, raisable; 29s timeout — now raisable above 29s for regional REST APIs on request) | Classic: Developer ~$50/mo (no SLA), Basic ~$150, Standard ~$700, Premium ~$2,800/unit/mo (multi-region, VNet, self-hosted gateway) ~verify. **v2 SKUs** (verified): **Basic v2 ~$210/mo**, **Standard v2 ~$734/mo**, **Premium v2 ~$3.836/hr** — faster provisioning, VNet injection (Std v2+), but **no self-hosted gateway or multi-region on v2** | **Apigee**: subscription (Standard/Enterprise/Enterprise+, six figures/yr typical) or **pay-as-you-go**: per-environment ($365–$3,431/mo per env per region) + $20/M standard proxy calls ($100/M extensible) + per-proxy-deployment charges. Full lifecycle: monetization, developer portals, analytics, shadow/hybrid deployment |
| WebSockets | $1.00/M messages + $0.25/M connection-min ~verify | Yes (tier-dependent) | Not on API Gateway; Apigee limited |
| Positioning | Utility gateway; ALB or CloudFront+Lambda often cheaper at scale | The most SKU-complex; v2 is the go-forward for single-region | Apigee = enterprise APIM; API Gateway = commodity; Endpoints legacy |

Rule of thumb at 100M calls/mo: HTTP API ≈ $100; APIM Basic v2 ≈ $210 + overage; Apigee PAYG ≈ $365 (env) + $2,000 (calls).

---

## 6. Container registries

| | **ECR** | **ACR** | **Artifact Registry** |
|---|---|---|---|
| Model | Pure usage: $0.10/GB-mo storage; transfer out per EC2 rates; in-region pulls to compute free; 50GB/mo free public pulls (unauthenticated), 500GB authenticated ~verify | **Tiered daily fee**: Basic ~$0.167/day (10GB incl.), Standard ~$0.667/day (100GB), Premium ~$1.667/day (500GB) + $0.10/GB overage ~verify; **geo-replication** = one Premium fee per replica region; Premium: private link, CMK, tokens | $0.10/GB-mo after 0.5GB free; multi-region repos; **gcr.io Container Registry fully shut down (2025)** — Artifact Registry is the only option |
| Extras | Pull-through cache (Docker Hub/ghcr/etc.), image scanning (basic free / enhanced via Inspector paid), lifecycle policies, ECR Public | Tasks (in-registry builds), connected registry (edge), artifact streaming (Premium), soft-delete | Remote & virtual repos (proxy Docker Hub/PyPI/npm/Maven), vulnerability scanning ($0.26/image ~verify), also serves as language-package registry |
| Formats | OCI, Helm | OCI, Helm, more | OCI + npm/PyPI/Maven/Apt/Yum/Go — broadest |

---

## 7. PaaS web hosting

**AWS**
- **Elastic Beanstalk**: free orchestration over EC2/ALB — alive but frozen in time; no meaningful roadmap. Fine for lift-and-shift EC2 apps; new builds go ECS Express/App Runner-successors.
- **Amplify Hosting**: active (customizable build instances 2025). Static+SSR (Next.js etc.): build $0.01/min, storage $0.023/GB-mo, transfer $0.15/GB, SSR compute per-request+GB-s. Free tier: 1,000 build-min, 15GB transfer. AWS's Vercel-competitor; solid, less DX polish.
- (App Runner: maintenance mode — see §2.2.)

**Azure**
- **App Service**: the workhorse. Free/Basic (~$13/mo B1)/Standard/Premium v3 (~$0.113/hr P0v3 up ~verify); **Premium v4** rolling out 2025–26 ~verify GA. Deployment slots, easy auth, WebJobs, Linux+Windows, containers. Not scale-to-zero (except new Flex-like offers ~verify).
- **Static Web Apps**: Free tier (personal) / Standard ~$9/app/mo — static + managed Functions API, global CDN, painless auth.

**GCP**
- **App Engine — being sidelined, not killed**: Gen1 legacy runtimes (Python 2.7, Java 8, Go 1.11, PHP 5.5) **deprecated Jan 31, 2026** (deploys blocked; existing apps still run). Gen2/Standard still supported, but Google's own **App Engine Migration Center now ships tooling to deploy App Engine apps to Cloud Run**, positions Cloud Run as "the latest evolution of Google Cloud serverless," and new serverless investment (GPUs, worker pools, multi-container) all lands in Cloud Run. Treat App Engine as maintenance-grade; don't start new projects on it. Flexible environment doubly so.
- **Firebase App Hosting** (GA 2025): Google's Vercel play — Git-driven Next.js/Angular hosting compiled onto **Cloud Run** + Cloud Build + CDN. Billed as underlying Cloud Run compute + bandwidth ($0.20/GiB uncached, $0.15 cached; 10GiB/mo free since Aug 2025). Separate meter from classic Firebase Hosting (static). This — not App Engine — is Google's answer for full-stack web apps.

---

## Cross-cutting cheat sheet

- **Cheapest idle**: Cloud Run / ACA consumption / Lambda (all scale to zero). Fargate & App Service never do.
- **Cheapest steady-state compute**: raw K8s nodes (Spot + Karpenter/NAP) < Fargate/Autopilot < serverless-container active pricing < FaaS.
- **GPU serverless**: GCP (Cloud Run L4, GA, quota-free) > Azure (ACA A100/T4 GA) > AWS (nothing serverless; SageMaker/EC2/EKS only).
- **Bill-shock hotspots**: EKS extended support ($0.60/hr auto-applied); EKS Auto Mode % adder on Spot; Step Functions Standard transitions; SQS 64KB chunking; APIM classic Premium units; NAT gateway charges under every Fargate/private-subnet design; Lambda INIT billing on Java; ACA always-ready + Flex always-ready canceling free grants; GKE extended +$0.50/hr.
- **2025–26 obituaries/pivots**: App Runner → maintenance (Apr 2026); GCR shut down; App Engine Gen1 deploys blocked (Jan 2026); Pub/Sub Lite retired ~verify; kubenet deprecation; classic Linux Consumption → Flex.

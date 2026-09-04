# Cross-Cloud Reference: Networking, Security, Identity & Governance — AWS vs Azure vs GCP

**Verified as of: 2026-08-28** (web-verified for volatile items: sovereign cloud launches, 2025–2026 pricing changes, service retirements, region counts). Prices are US list prices (us-east-1 / East US / us-central1 equivalents) and are approximate — always confirm on the official calculators.

**Main sources:** aws.amazon.com (Security Hub GA & pricing, CloudFront flat-rate plans, Route 53 pricing, Organizations RCP docs, Control Tower release notes, Transit Gateway/Cloud WAN pricing, ESC launch blog, press.aboutamazon.com Jan 2026 ESC release), learn.microsoft.com (Front Door/CDN classic retirement FAQs, Defender for Cloud & Sentinel pricing, Entra pricing, AVNM IPAM docs, confidential VM docs), cloud.google.com (Cross-Cloud Interconnect docs & Next '26 networking blog, SCC service tiers & pricing, Cloud NGFW pricing, VPC network pricing, Confidential VM release notes, locations page), thalesgroup.com / googlecloudpresscorner.com (Thales–Google Germany sovereign cloud, May 2026), techcommunity.microsoft.com (Intel TDX CVM GA, Sentinel data lake pricing).

---

## 1. Network Architecture Models

### Core construct comparison

| Dimension | AWS VPC | Azure VNet | GCP VPC |
|---|---|---|---|
| Scope | **Regional** | **Regional** | **Global** (the key differentiator) |
| Subnets | Zonal (one AZ each) | Regional (span zones by default) | **Regional** (span all zones in a region) |
| CIDR | Primary + secondary CIDRs; IPv4 /16–/28 | Multiple address spaces; can resize live | Subnets have primary + secondary ranges (alias IPs for GKE pods/services); auto-mode or custom-mode |
| Default routing | Route tables per subnet | System routes + UDRs (per subnet via route table association) | Global routing table; dynamic routing mode (regional/global) affects Cloud Router advertisement |
| DNS | Route 53 Resolver at VPC+2 (.2 address) | 168.63.129.16 wire server | Metadata server 169.254.169.254, Cloud DNS private zones |

**GCP's global VPC** means one VPC can have subnets in Tokyo, Iowa, and Frankfurt with private RFC1918 reachability and no peering, no transit hub, no inter-region VPN. This collapses entire AWS/Azure hub-and-spoke architectures — but **gotcha:** inter-region egress within a GCP VPC is still billed (~$0.01–$0.08+/GB by continent pair), and a single global VPC becomes a giant blast radius/quota domain, which is why Google still recommends Shared VPC + multiple VPCs for isolation.

### Peering and transit

- **AWS:** VPC Peering (non-transitive). **Transit Gateway** (regional hub, $0.05/attachment-hr ≈ $36.50/mo + $0.02/GB processed; inter-region TGW peering supported). **Cloud WAN** is the global evolution: Core Network Edges at $0.50/hr per region + $0.02/GB, policy-driven global network with segments (VRF-like). Practitioner gotcha: TGW data processing double-dips with NAT Gateway processing in centralized egress designs — inspect the per-GB stack ($0.02 TGW + $0.045 NAT + cross-AZ).
- **Azure:** VNet Peering (non-transitive; $0.01/GB each direction intra-region — peering is *not* free in Azure). **Virtual WAN** = managed global hub-and-spoke: hub fee ($0.25/hr per hub) + connection units + data processing; Standard vWAN gives hub-to-hub full mesh transit over Microsoft backbone. Azure Route Server ($0.45/hr) for BGP with NVAs in DIY hubs. **Azure Virtual Network Manager (AVNM)** adds mesh/hub-spoke connectivity configs, security admin rules (org-wide rules that evaluate *before* NSGs), billed ~$0.073/hr per subscription managed.
- **GCP:** VPC Network Peering (non-transitive, free within-region). **Network Connectivity Center (NCC)** is the transit hub: hub + spokes (VPC spokes, hybrid spokes for VPN/Interconnect, Router appliance spokes for SD-WAN NVAs); VPC spokes enable star topologies and inter-VPC transit; also supports Private Service Connect propagation through the hub (2025 feature). NCC billing per-spoke-hour by spoke type plus data transfer; VPC spokes cheap relative to TGW attachments. Next '26: cross-cloud NCC integration with Partner Cross-Cloud Interconnect (Preview), agentic-traffic observability.

### Sharing models

- **AWS:** No native "shared VPC" primitive — **AWS RAM (Resource Access Manager)** shares subnets from a network account to participant accounts. Gotchas: security groups not shareable cross-account by reference in all services, VPC endpoints/NACLs owned by owner account, some services historically didn't support shared subnets.
- **Azure:** No shared VNet construct; equivalent is subscription design + RBAC on subnets (Network Contributor scoped to subnet) or vWAN centralization. Cross-subscription VNet peering routine.
- **GCP:** **Shared VPC** is first-class: host project owns the VPC, service projects attach; IAM `compute.networkUser` per subnet. Cleanest model of the three. Gotcha: host project quotas (routes, firewall rules, subnets, PSC endpoints) become org-wide chokepoints.

### IPv6 (2026 status)

- **AWS:** Most mature: dual-stack VPCs, **IPv6-only subnets** (EC2, ECS, Lambda VPC, NLB/ALB dual-stack), Amazon-provided /56 per VPC, BYOIPv6, egress-only internet gateway. Public IPv6 is **free**.
- **Azure:** Dual-stack VNets/subnets GA for years, but **no IPv6-only subnets**; gaps persist (some PaaS, private endpoints are IPv4-only).
- **GCP:** Dual-stack subnets GA, **IPv6-only subnets GA**, ULA (`fd20::/20`) internal IPv6, external IPv6 on most LB types. GCP moved fast here 2023–2025.

### Public IPv4 pricing (the 2024 shock, now table stakes)

- **AWS:** $0.005/hr (~$3.65/mo) for **every** public IPv4 (in use or idle) since Feb 2024. Free tier: 750 hrs new accounts. VPC IPAM "Public IP Insights" free.
- **GCP:** $0.005/hr in-use external IPv4 on VMs; idle reserved static IPs ~$0.01/hr; IPs on forwarding rules (LBs) not charged.
- **Azure:** $0.005/hr Standard SKU public IPs, attached or not. Basic public IPs **retired Sept 30, 2025**; stragglers repriced to Standard Mar 31, 2026. IPv6 public addresses free.
- Net: all three charge ~$3.65/mo per public IPv4; answer everywhere is NAT consolidation + PrivateLink/PSC + IPv6.

### IPAM offerings

- **AWS VPC IPAM:** Free tier + Advanced tier **$0.00027/hr per active IP** (~$0.20/mo/IP — cross-account/region pools, BYOIP, automated allocation). Gotcha: advanced-tier cost at scale (10k IPs ≈ $2k/mo).
- **Azure:** **AVNM IPAM** GA (2025): pools, automatic CIDR allocation, billed per active IP managed. No BYOIP orchestration parity yet.
- **GCP:** No standalone IPAM product; "internal ranges" API + auto subnet allocation + hierarchical constraints. Third-party (Infoblox) common.

---

## 2. Load Balancing

### Family mapping

| Layer/Need | AWS | Azure | GCP |
|---|---|---|---|
| L7 HTTP(S), regional | ALB | Application Gateway v2 (± WAF) | Regional external Application LB (Envoy-based) |
| L7 global anycast | — (CloudFront+ALB composite) | Front Door (Std/Premium) | **Global external Application LB** (true anycast, single VIP worldwide) |
| L4 passthrough | NLB (preserves client IP, hyperplane) | Azure Load Balancer (Standard) | External/Internal **passthrough Network LB** (Maglev) |
| L4 proxy | NLB w/ TLS termination (partial) | — | External/Internal **proxy Network LB** (global or regional) |
| Transparent NVA insertion | **Gateway Load Balancer** (GENEVE) | **Gateway Load Balancer** (VXLAN, chained to Std LB) | No direct equivalent — policy-based routes / NGFW endpoints / third-party via NCC router appliances |
| Internal L7 | Internal ALB | AppGW (private frontend) | Internal Application LB (regional; cross-region internal ALB also GA) |
| DNS-based global routing | Route 53 routing policies / Global Accelerator (anycast L4) | **Traffic Manager** (DNS only) | Cloud DNS routing policies |

### Key architectural distinctions

- **GCP's global external Application LB** is the standout: one anycast VIP from ~all Google edge POPs, cross-region backend failover, serverless NEGs (Cloud Run/Functions), integrated Cloud CDN + Cloud Armor. AWS's answer is CloudFront (+Lambda@Edge) or Global Accelerator in front of regional ALBs — a composition, not a product. Azure's answer is Front Door.
- **Azure Front Door Standard/Premium** is explicitly a CDN+global-L7-LB+WAF hybrid (Microsoft killed separate Azure CDN SKUs in its favor — see §3). Premium adds managed WAF rulesets, Private Link origins, bot protection.
- **Global Accelerator** (AWS): anycast L4 (2 static IPs, $0.025/hr + data), often paired with NLB for non-HTTP global apps.
- **Gotchas:** ALB has no static IPs (front with NLB→ALB target or Global Accelerator); Azure AppGW v2 requires a dedicated subnet and scales slowly under spike; GCP classic vs modern LB naming is a minefield (avoid "classic" HTTP(S) LB, target-pool NLBs); GCP global LB requires Premium network tier; Azure Standard LB is secure-by-default (no NSG = no traffic) — Basic LB **retired Sept 30, 2025**.

### Pricing units

- **AWS:** hourly + **LCU**: ALB $0.0225/hr + $0.008/LCU-hr (LCU = max of new conns/25, active conns/3000, 1 GB/hr, rule evals). NLB $0.0225/hr + $0.006/NLCU-hr. GWLB ~$0.0125/hr + $0.004/GLCU-hr. LCU dimensions are the classic bill-surprise (rule-heavy ALBs, tiny requests).
- **Azure:** Standard LB: $0.025/hr first 5 rules + $0.005/GB processed. AppGW v2: ~$0.246/hr fixed + $0.008 per **Capacity Unit**-hr. Front Door: base fee ($35/mo Standard, $330/mo Premium) + per-GB egress + per-10k requests. Traffic Manager: per million DNS queries.
- **GCP:** $0.025/hr per forwarding rule (first 5, then $0.01 each) + $0.008–0.012/GB inbound processed; global LB data on Premium Tier egress. Cloud CDN/Armor billed separately.

---

## 3. DNS & CDN

### DNS

- **Route 53:** $0.50/hosted zone/mo, $0.40/M standard queries ($0.60/M latency, geo pricier), health checks extra, 100% SLA. **Resolver endpoints** (hybrid DNS): $0.125/hr **per ENI** — hidden cost: 2 endpoints × 2 AZs ≈ $365/mo before query charges. **Route 53 Profiles** (2024): package private hosted zones, Resolver rules, DNS Firewall groups, share org-wide via RAM — $0.75/hr per account. Resolver DNS Firewall for egress DNS filtering.
- **Azure DNS:** $0.50/zone/mo, $0.40/M queries. **Private DNS zones** with auto-registration; **DNS Private Resolver** (~$0.25/hr per endpoint) killed the "DNS forwarder VM" pattern. Gotcha: private endpoint DNS integration (privatelink.* zones) is the #1 Azure networking support topic — use Azure Policy to auto-create DNS zone groups. DNSSEC public zones GA (2024–25).
- **Cloud DNS:** $0.20/zone/mo, $0.40/M queries; private zones, forwarding zones, peering zones, **response policies**, routing policies (WRR/geo/failover). Server policies for hybrid inbound/outbound resolution. Cross-project binding native via Shared VPC.

### CDN

- **CloudFront:** Classic usage pricing: ~$0.085/GB (US/EU) tapering, regional tiers; **Price Classes** trade POP coverage for cost. Free tier: 1 TB/mo egress. Origin fetch from AWS origins free. **Big 2025 change:** **flat-rate pricing plans** (Nov 2025) — Free ($0), Pro ($15/mo), Business ($200/mo), Premium ($1,000/mo) bundling CDN + WAF + DDoS + Route 53 DNS + CloudWatch Logs + edge functions + S3 credits, **throttling instead of overage billing**; since launch added Lambda@Edge, CAPTCHA, mTLS. Also 2025: **CloudFront SaaS Manager** (multi-tenant distributions for SaaS custom domains). CloudFront Functions vs Lambda@Edge = two edge-compute tiers.
- **Azure:** **Everything consolidated into Front Door Std/Premium.** Retirement wall: Azure CDN from Edgio — dead (Jan 2025, Edgio bankruptcy); **Azure Front Door (classic) retires March 31, 2027**; **Azure CDN Standard from Microsoft (classic) retires September 30, 2027**; classic managed certs stopped Aug 15, 2025. Practitioner note: Front Door Standard's per-request + base fee can be pricier than classic CDN for pure static offload; for video/large files consider external CDN.
- **GCP:** **Cloud CDN** (integrated with global external ALB; cache egress ~$0.02–0.08/GB + $0.0075/10k lookups) for web; **Media CDN** (separate, YouTube-scale edge, streaming/large-file, sales-gated). Gotcha: Cloud CDN requires the LB — no standalone "point at any origin" simplicity.

---

## 4. Private & Hybrid Connectivity

### Dedicated circuits

| | AWS Direct Connect | Azure ExpressRoute | GCP Cloud Interconnect |
|---|---|---|---|
| Dedicated ports | 1/10/100/400 Gbps; port-hour fees ($0.30/hr 1G, $2.25 10G, $22.50 100G) + egress $0.02–0.03/GB | Circuit-based: 50 Mbps–100 Gbps; **Metered** or **Unlimited**; Local SKU (free egress, same-metro only), Standard, Premium (global reach) | Dedicated: 10/100 Gbps ports (~$1,700/mo 10G), VLAN attachments 50 Mbps–50 Gbps + egress $0.02–0.05/GB |
| Partner/hosted | Hosted connections 50 Mbps–25 Gbps | Always via providers (Equinix, Megaport…) | Partner Interconnect 50 Mbps–50 Gbps |
| Resiliency SLA | 99.9/99.99 with prescribed topologies (2–4 circuits) | 99.95 on a single circuit (MSEE pairs built in) | 99.9/99.99 topologies (2–4 attachments across metros) |
| Transit integration | DX Gateway (global, free) → TGW/VGW; MACsec on 10/100G | ER Gateway (SKU hourly), Global Reach, FastPath | Attachments land on Cloud Routers; NCC hybrid spokes; HA VPN over Interconnect for encryption |
| Cross-cloud | — (partners DIY) | — | **Cross-Cloud Interconnect** — first-party managed links to AWS/Azure/OCI (10/100G, since 2023); **Partner Cross-Cloud Interconnect for AWS GA April 2026** (on-demand, SLA-backed, co-engineered with AWS) — unique to Google |

Gotchas: ExpressRoute Local SKU chronically misunderstood (free egress but same-metro regions only, ≥1 Gbps); AWS DXGW doesn't carry VPC-to-VPC transit (need TGW); GCP Partner Interconnect adds partner fees on top.

### Managed VPN

- **AWS Site-to-Site VPN:** $0.05/hr per connection (~$36/mo, 2 tunnels, 1.25 Gbps/tunnel). No SLA on classic VPN.
- **Azure VPN Gateway:** SKU hourly (VpnGw1 ~$0.19/hr → VpnGw5 ~$2.60/hr), active-active supported. Gotcha: resize/generation migrations cause downtime; ER+VPN coexistence needs higher SKUs.
- **GCP:** **HA VPN** $0.05/hr per tunnel, 99.99% SLA with 2+ tunnels + BGP (Cloud Router mandatory); ~3 Gbps/tunnel.

### Private access to services

- **AWS PrivateLink:** Interface endpoints $0.01/AZ-hr + $0.01/GB; Gateway endpoints (S3/DynamoDB) **free** — still the #1 "why is my NAT bill huge" fix. Cross-region PrivateLink GA (2024). VPC Lattice = newer service-network layer above PrivateLink.
- **Azure Private Link:** Private endpoints $0.01/hr + $0.01/GB in/out. Per-resource (not per-AZ). Service endpoints (older, free, no exfil protection) still around — modern answer: private endpoints + NSP (Network Security Perimeter, GA 2025).
- **GCP Private Service Connect (PSC):** Consumer endpoints ~$0.01/hr + data processing; PSC for Google APIs, PSC for published services, PSC interfaces. 2025: NCC propagation of PSC endpoints across spokes. Legacy "private services access" (VPC peering to Google-managed VPCs) being displaced by PSC — migration friction real (Cloud SQL PSC vs PSA).

---

## 5. Identity & Organizational Governance

### IAM models

**AWS IAM:** Single flat model — principals (users/roles), identity-based + resource-based JSON policies, permission boundaries, session policies, SCPs/RCPs from Organizations. Evaluation: explicit deny > allow; cross-account requires both sides. **IAM Identity Center** (ex-AWS SSO) = workforce layer: permission sets → roles per account, SCIM/SAML/OIDC from external IdPs, trusted identity propagation. The **account** is the isolation boundary. Roles Anywhere (X.509), IAM OIDC federation for workloads. Access Analyzer best-in-class for reasoning about resource exposure.

**Microsoft Entra ID:** Critical thing practitioners miss: **two separate authorization planes.** Entra ID (tenant/directory: users, groups, apps, Entra roles like Global Admin) vs **Azure RBAC** (management groups → subscriptions → resource groups → resources). Entra Global Admin does *not* have ARM permissions until they "elevate access." Add-ons: **PIM** (JIT role activation — P2), **Conditional Access** (P1), Identity Protection (P2), Access Reviews (P2), External ID (B2B/B2C successor). **Pricing (post-July 1, 2026 increase): P1 $7/user/mo, P2 $10/user/mo; Entra Suite $12/user/mo add-on**. Managed identities (system/user-assigned) = workload identity primitive — free, the answer to "never put a connection string in code." ABAC via role-assignment conditions.

**GCP IAM:** Principals (Google accounts, service accounts, groups, workload/workforce pool identities) get **roles** (basic — avoid; predefined; custom) on **resources**, inheritance down Organization → Folder → Project → resource. Allow + **deny policies** + IAM Conditions (CEL). **Principal Access Boundary** policies (2024+) = permission-boundary analog. **Workload Identity Federation** (OIDC/SAML/AWS-native) and **Workforce Identity Federation** (console access for non-Google IdPs — not all services support it; check compatibility). Service account keys = top GCP anti-pattern; `iam.disableServiceAccountKeyCreation` should be default-on.

### Org hierarchy & guardrails

| | AWS | Azure | GCP |
|---|---|---|---|
| Hierarchy | Organization → OUs (nest 5 deep) → **accounts** | Tenant → **Management Groups** (6 levels) → Subscriptions → Resource Groups | **Organization → Folders → Projects** |
| Isolation unit | Account (hard blast-radius boundary, billing, quotas) | Subscription (soft-ish; policy/RBAC boundary, quotas) | Project (quota/billing/API enablement boundary) |
| Preventive guardrails | **SCPs** (cap principal permissions) + **RCPs** (Nov 2024; cap what can access *resources* — data perimeter; coverage expanding: S3, STS, KMS, SQS, SecretsManager, ECR…) + **declarative policies** (enforce service configs) | **Azure Policy** (deny/audit/append/modify/**deployIfNotExists** — richer than SCPs: can remediate) + initiatives; assigned at MG/sub/RG | **Organization Policy** constraints (list/boolean + **custom constraints** in CEL) |
| Notable gotchas | SCPs don't affect management account or resource-policy grants to external principals (RCPs fix that); 5-SCP/5120-char limits force policy golf | ~15-min lag for deployIfNotExists remediation; initiative versioning sprawl; Entra vs RBAC confusion | Inheritance overridable at lower levels unless enforced; project sprawl is normal (embrace it) |

### Cross-cloud federation (the modern pattern — kill static keys)

- GitHub Actions / GitLab / K8s → **AWS**: IAM OIDC provider + role trust policy on `sub`/`aud`. → **GCP**: Workload Identity Federation pool/provider + SA impersonation. → **Azure**: Entra **workload identity federation** on app registrations / user-assigned managed identities.
- Cloud-to-cloud: AWS workloads → GCP via WIF's native AWS provider; GCP SAs → AWS via OIDC to `AssumeRoleWithWebIdentity`; anything → Azure via federated credentials. EKS Pod Identity / IRSA, GKE Workload Identity, AKS workload identity in-cluster.
- Gotchas: claim-matching wildcards (GitHub `sub` with `*` on branches = supply-chain hole), token lifetime/audience validation, Azure's 20-federated-credentials-per-app limit, GCP WIF attribute-mapping complexity. This is the 2026 default; long-lived keys are audit findings.

---

## 6. Secrets & Key Management

### Secrets

- **AWS Secrets Manager:** $0.40/secret/mo + $0.05/10k API calls; native rotation via Lambda / managed rotation; cross-region replication (each replica billed). **Parameter Store** (SSM): standard tier free (4 KB, no rotation) — the budget option; advanced tier $0.05/param/mo. Gotcha: Secrets Manager cost at microservice scale (10k secrets = $4k/mo) pushes teams to Parameter Store + KMS or Vault.
- **Azure Key Vault:** Secrets, keys, certs in one service. Standard: $0.03/10k operations — cheapest at rest, no per-secret fee. Rotation for secrets is BYO (Event Grid near-expiry events + Functions). Soft-delete + purge protection default-on (breaks naive delete/recreate IaC). Throttling limits are a real design constraint — cache secrets, per-app vaults.
- **GCP Secret Manager:** $0.06 per active secret **version** per replication location per month + $0.03/10k access ops; automatic replication multiplies cost. Rotation = Pub/Sub reminders, not managed.

### Keys / HSM

- **AWS KMS:** $1/key/mo (CMK) + $0.03/10k requests; multi-region keys (each billed); External Key Store (XKS). **CloudHSM** FIPS 140-2 L3 single-tenant (~$1.45–1.60/hr/HSM ≈ $1,100+/mo, min 2 for prod).
- **Azure Key Vault keys:** software-protected ~free (ops only), Premium HSM-backed RSA 2048 $1/key/mo; **Managed HSM** — dedicated pool ~$3.20/hr (~$2,300/mo) minimum — FIPS L3 answer. Azure Dedicated HSM retiring → Managed HSM.
- **GCP Cloud KMS:** $0.06/key version/mo software keys, **HSM keys** $1.00–2.50/version/mo tiered, **EKM** (external key manager) $3/key/mo — central to GCP's sovereign story (Key Access Justifications). Cloud HSM fully managed multitenant FIPS L3 — genuine ops win over CloudHSM/Managed HSM.
- CMK/CMEK ubiquity: all three support customer-managed keys across ~all services; GCP org policy can *require* CMEK; AWS uses SCP/RCP conditions; Azure uses Policy deny.

---

## 7. Perimeter Security

### WAF

- **AWS WAF:** $5/web ACL/mo + $1/rule/mo + $0.60/M requests; managed rule groups extra; Bot Control / Fraud Control pricey add-ons. Attaches to CloudFront, ALB, API GW, AppSync, Cognito. Now bundled free inside CloudFront flat-rate plans.
- **Azure WAF:** Two homes — **Application Gateway WAF_v2** (regional; ~$0.443/hr + WAF CUs) and **Front Door Premium** (global; WAF included in $330/mo base, managed rulesets + bot protection; Standard = custom rules only). The AppGW-vs-Front Door WAF split (different engines, different rule syntax) annoys multi-tier deployments.
- **GCP Cloud Armor:** Standard PAYG — $5/policy/mo + $1/rule/mo + $0.75/M requests; preconfigured WAF rules (ModSecurity CRS), rate limiting, bot management via reCAPTCHA, adaptive protection (ML L7 DDoS) fully in Enterprise only.

### DDoS

- **AWS:** Shield Standard free. **Shield Advanced: $3,000/mo (1-yr commit) + data fees**; cost protection, SRT access, includes WAF free on protected resources. One subscription covers the whole org via consolidated billing — don't buy per-account.
- **Azure:** **DDoS Network Protection $2,944/mo** (100 public IPs tenant-wide, then per-IP) vs **DDoS IP Protection** (~$199/mo per IP); rapid response team, cost guarantee.
- **GCP:** Baseline always-on absorption free. **Cloud Armor Enterprise** (~$3,000/mo annual, or ~$300/project/mo Paygo): adaptive protection, DDoS bill protection, threat intel. Warning: request-based fees during L7 floods can spike Standard-tier bills — Enterprise waives per-request charges.

### Network firewalls

- **AWS Network Firewall:** Managed Suricata; $0.395/endpoint-hr (~$288/mo per AZ endpoint) + $0.065/GB — widely criticized as expensive in centralized designs. TLS inspection supported. Many shops deploy Palo Alto/Fortinet via GWLB instead.
- **Azure Firewall:** Basic ($0.395/hr + $0.065/GB, 250 Mbps), Standard ($1.25/hr + $0.016/GB), Premium ($1.75/hr + $0.016/GB, TLS inspection, IDPS) — per-GB much lower than AWS but hourly floor higher (~$912–1,278/mo). SNAT port exhaustion is the classic issue.
- **GCP Cloud NGFW:** Modern construct = firewall *policies* (hierarchical org/folder → network → regional). Tiers: **Essentials** (free — stateful L4, tags), **Standard** ($0.018/GB — FQDN, geo, Threat Intel), **Enterprise** ($1.75/hr per endpoint + $0.018/GB — Palo Alto-powered IDPS, TLS inspection). Distributed enforcement (no choke-point appliance) — architecturally cleanest of the three.

---

## 8. Security Posture & SIEM

### AWS

**Security Hub was re-launched:** the new **AWS Security Hub** (preview re:Inforce June 2025, **GA December 2025**) = unified risk-correlation layer (near-real-time analytics, attack-path prioritization) over GuardDuty + Inspector + **Security Hub CSPM** (old product, renamed) + Macie; **resource-based pricing** with unlimited checks/ingestion; plus **Security Hub Extended** (GA 2026) bundling partner solutions. Budgeting shifted from per-check micro-meters to per-resource — re-evaluate against Defender for Cloud like-for-like.
- **GuardDuty** (threat detection; per-GB analyzed + per-vCPU/EBS runtime; Extended Threat Detection 2025), **Inspector** (vuln mgmt per-instance/image/Lambda), **Detective** (investigation graph), **Macie** (S3 sensitive-data discovery), **Amazon Security Lake** (OCSF data lake). AWS has **no first-party SIEM** — Security Lake + partner (Splunk, Sentinel, SecOps).

### Microsoft

- **Defender for Cloud:** CSPM+CWPP, natively multicloud (AWS/GCP connectors). **Per-resource pricing** — model carefully: Foundational CSPM free; **Defender CSPM ~$5.11/billable resource/mo**; **Defender for Servers P1 ~$5/server/mo, P2 $15/server/mo** (P2 incl. MDE + 500 MB/day Log Analytics); Defender for Storage/SQL/Containers/APIs each their own meter. Gotcha: enabling "everything" at subscription level on a large estate = five-figure monthly surprise; scope per-plan deliberately.
- **Microsoft Sentinel:** Cloud-native SIEM/SOAR on Log Analytics. Analytics tier PAYG ~**$4.30/GB** with commitment tiers (100 GB/day ≈ $2.96/GB eff.); **Sentinel data lake** (GA 2025–26): ~**$0.50/GB** ingestion + separate query/compute meters — answer to "can't afford verbose logs in analytics tier." **Portal transition:** Sentinel moving into unified **Defender portal**; Azure-portal support ends **March 31, 2027**.

### Google

- **Security Command Center (SCC):** Standard (free), **Premium** (org-level subscription or PAYG off cloud-spend %; ETD, SHA, VM/container threat detection, attack paths; Jan 2026: PAYG meters Cloud Run/AlloyDB at $0.0057/vCPU-hr), **Enterprise** (multicloud CNAPP + SecOps seats) — **Enterprise tier being retired May 21, 2027**, orgs auto-moved to Premium; consolidation under **Google Unified Security** (Next '25: SecOps + SCC + Threat Intelligence + Mandiant, agentic AI triage GA 1Q26).
- **Google SecOps (Chronicle):** SIEM+SOAR; Standard/Enterprise/Enterprise Plus, historically per-employee or ingestion-cap pricing with 12-month hot retention (flat, predictable vs Sentinel per-GB — the sales battleground); UDM, YARA-L, Gemini investigation. Mandiant services attach here.

### Mapping cheat-sheet

| Function | AWS | Microsoft | Google |
|---|---|---|---|
| CSPM/CNAPP | Security Hub (new) + Security Hub CSPM | Defender for Cloud (Defender CSPM) | SCC Premium/Enterprise(→Premium) |
| Threat detection | GuardDuty | Defender plans (per resource type) | SCC ETD/VMTD/CTD |
| Vulnerability | Inspector | Defender for Servers | SCC + Artifact Analysis |
| DSPM | Macie | Defender CSPM DSPM / Purview | Sensitive Data Protection |
| SIEM | (Security Lake + partner) | **Sentinel** | **Google SecOps** |
| Investigation | Detective | Defender XDR / Sentinel | SecOps + Gemini |

---

## 9. Compliance, Sovereignty & Confidential Computing

### Footprint (approx., Aug 2026)

- **AWS:** ~38 commercial regions / ~120 AZs (Taipei Jun 2025, New Zealand Sep 2025; Chile due end-2026; every new region 3+ AZs), 30+ Local Zones, Wavelength, Outposts. Separate partitions: GovCloud (US ×2), China (×2), **European Sovereign Cloud partition**.
- **Azure:** 70+ announced regions (~60 operational; not all have AZs — ~34 regions with zones), broadest country coverage; region pairs de-emphasized for zonal resilience in newer nonpaired regions. Azure Government, Azure China (21Vianet).
- **GCP:** **43 regions / 130 zones**, 200+ edge POPs; fewer countries than Azure but denser network. Assured Workloads for US Gov (controls-based, no separate partition — a philosophical difference), Google Distributed Cloud (air-gapped) for the extreme end.

### Sovereign clouds (the 2025–26 battleground)

- **AWS European Sovereign Cloud (ESC):** **GA January 2026** — first region Brandenburg, Germany (3 AZs), a **physically and logically separate partition** operated by German legal entities with EU-resident staff, own TLD/billing/support, €7.8B investment; sovereign Local Zones coming in Belgium, Netherlands, Portugal. Strongest structural-independence claim of the US hyperscalers.
- **Microsoft:** EU Data Boundary + **Microsoft Cloud for Sovereignty** (policy/landing-zone layer) + **Delos Cloud** (SAP/Arvato-operated German sovereign Azure/M365 for German public sector, staged 2025–2026, BSI-targeting) + Bleu (France, Capgemini/Orange).
- **Google:** Partner-operated model: **S3NS** (Thales, France — SecNumCloud-targeting) and — **new May 2026** — a **Thales–Google sovereign cloud for Germany**: 100% Thales-owned German entity, isolated Berlin-area region under German law (BSI C5/C3A), geo-redundant with S3NS's PREMI3NS in France (pan-European sovereign DR — industry first); GA expected end 2026. Plus software controls: Sovereign Controls/Assured Workloads, EKM + Key Access Justifications, GDC air-gapped.
- Gov clouds: AWS GovCloud (ITAR/FedRAMP High/DoD IL5 + Top Secret regions), Azure Government (+ Secret/Top Secret), Google via Assured Workloads + GDC for classified.

### Confidential computing

- **AWS:** **Nitro Enclaves** (isolated VM partitions, attestation via KMS — enclave model, not memory-encrypted-VM model); Nitro "no AWS operator access" formal attestations; SEV-SNP on select M6a/C6a/R6a. AWS is the outlier in *not* leading with confidential VMs — position: Nitro already isolates tenants.
- **Azure:** Broadest lineup: Confidential VMs on **AMD SEV-SNP** (DCasv5/ECasv5→v6) and **Intel TDX** (DCesv6/ECesv6 **GA 2025–26**); confidential GPUs (H100 TEE for confidential AI); SGX enclaves (DCsv3); confidential AKS node pools; Microsoft Azure Attestation.
- **GCP:** Confidential VMs (SEV, **SEV-SNP GA**, **TDX GA** on C3; confidential GKE, Dataflow/Dataproc confidential, Confidential Space for multi-party); minimal price premium, "checkbox" enablement. 2026 note: TDX firmware vulnerability (GCP-2026-008) and SEV-SNP attestation-report migration required verifier updates.

---

## 10. Landing Zones & Multi-Account Strategy

- **AWS Control Tower:** Managed landing zone: Organizations + Identity Center + logging/audit accounts + guardrails (preventive = SCPs, detective = Config rules, proactive = CFN hooks; + declarative-policy controls). **Landing zone v4.0** (2025) moved to dedicated per-service resources. Late-2025 shift: **Control Tower managed controls without a full Control Tower deployment** — 750+ controls from Control Catalog deployable on existing orgs. Account Factory (+ AFT for GitOps vending). Gotchas: opinionated regions/Config recorder conflicts; drift on managed SCPs; AFT operationally heavy. Alternative: Organizations + StackSets ("Landing Zone Accelerator" for regulated industries).
- **Azure Landing Zones (ALZ, CAF):** Reference management-group hierarchy (Platform: identity/management/connectivity; Landing zones: corp/online; Sandbox/Decommissioned) + hundreds of Azure Policy assignments + hub-spoke or vWAN topology. Deployment: ALZ Portal Accelerator, **Bicep/Terraform accelerators standardized on Azure Verified Modules (AVM)** — the Terraform `alz` module rewrite (2024–25) replaced the CAF module lineage. Subscription vending mirrors AWS account vending. Gotchas: policy assignment sprawl/versioning, initiative drift after accelerator upgrades.
- **GCP:** **Cloud Setup / setup checklist** (guided foundation) → **Cloud Foundation Fabric FAST** (opinionated Terraform stages: bootstrap → resman → networking → security → project factory) and terraform-example-foundation. Org policies (incl. **custom constraints** in CEL, GA across many services 2024–25) as preventive layer; `gcloud terraform vet` against org policies pre-apply is underused and excellent.
- **Policy-as-code comparison:** SCP/RCP = permission ceilings (no remediation); Azure Policy = configuration governance engine (audit/deny/modify/deploy + remediation — broadest scope, slowest evaluation); GCP Org Policy = config constraints (fast, inherited, customizable via CEL, no remediation). All supplemented by pipeline-time checks (cfn-guard/Checkov/OPA, PSRule, terraform vet).
- Multi-account philosophy in one line: AWS = many accounts (hard boundary, cross-account roles everywhere); Azure = fewer subscriptions + management groups + RBAC scopes (softer boundary); GCP = many cheap projects + folders + Shared VPC (granularity between the two, best per-workload isolation with centralized networking).

---

## Cross-Cutting Gotchas Practitioners Hit (2026 edition)

1. **Egress/inspection cost stacking:** centralized east-west inspection can stack TGW ($0.02/GB) + firewall ($0.016–0.065/GB) + cross-AZ ($0.01/GB ×2) + NAT ($0.045/GB) — model per-GB paths before committing. GCP's distributed Cloud NGFW avoids the choke-point tax for L4–L7-lite needs.
2. **Retirement calendar (Azure especially):** Basic Load Balancer (Sep 2025), Basic public IPs (Sep 2025/Mar 2026), AFD classic (Mar 2027), Azure CDN Microsoft classic (Sep 2027), Sentinel-in-Azure-portal (Mar 2027), SCC Enterprise tier (May 2027). Budget migration engineering time now.
3. **Pricing-model regime changes:** CloudFront flat-rate plans (Nov 2025) and Security Hub resource-based pricing (Dec 2025) invalidate 2024-era cost models; Entra P1/P2 rose ~16% July 2026; re-run comparisons.
4. **Identity is the perimeter:** AWS RCPs + VPC endpoint policies + `aws:SourceOrgID`; Azure Conditional Access + Network Security Perimeter + private endpoints; GCP VPC Service Controls (most mature data-exfiltration perimeter, most painful to operate — dry-run mode first, always).
5. **OIDC federation everywhere:** static credentials cross-cloud are a 2020 pattern; audit for leftover access keys, SP client secrets, SA JSON keys quarterly.

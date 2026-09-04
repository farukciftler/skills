# Cross-Cloud Service Equivalence Reference: AWS ↔ Microsoft Azure ↔ Google Cloud

**Verified as of: 2026-08-28**

**Scope:** Mapping of ~160 capabilities across AWS, Microsoft Azure, and Google Cloud (GCP), with current (2026) service names, recent renames flagged as `old → new`, and recently retired services flagged so you don't build on dead platforms.

**Main sources:**
- AWS: https://docs.aws.amazon.com/ • https://aws.amazon.com/new/ • https://aws.amazon.com/products/
- Azure: https://learn.microsoft.com/azure/ • https://azure.microsoft.com/updates/ • https://learn.microsoft.com/lifecycle/
- GCP: https://cloud.google.com/docs • https://cloud.google.com/products • https://cloud.google.com/blog/topics/google-cloud-next
- Rename/retirement specifics verified against official What's New / release notes / retirement FAQ pages (Amazon EVS GA Aug 2025, AgentCore GA Oct 2025, Cloud Run functions rename Aug 2024, GKE Enterprise tier dissolved Sep 2025, Azure AI Foundry → Microsoft Foundry Nov 2025, Azure Cache for Redis retirement, Azure Data Studio retirement, AWS Proton EOL, Snow family wind-down, Vertex AI → Gemini Enterprise Agent Platform at Cloud Next '26).

**The big renames/pivots you must know (2023–2026):**

| Old name | Current name (2026) |
|---|---|
| Azure Active Directory | **Microsoft Entra ID** (2023) |
| Azure Cognitive Services | **Azure AI services** (2023) |
| Azure AI Studio → Azure AI Foundry | **Microsoft Foundry** (Nov 2025, Ignite) |
| Azure Stack HCI | **Azure Local** (Nov 2024) |
| Azure Cache for Redis | **Azure Managed Redis** (Cache for Redis retiring: Enterprise tiers Mar 2027, Basic/Std/Premium Sep 2028) |
| Google Cloud Functions | **Cloud Run functions** (Aug 2024) |
| Anthos → GKE Enterprise | **GKE** (Enterprise tier dissolved into standard GKE, Sep 2025); on-prem parts → **Google Distributed Cloud (GDC)** |
| Anthos Service Mesh / Traffic Director | **Cloud Service Mesh** |
| Chronicle | **Google Security Operations (Google SecOps)** |
| Google Agentspace | **Gemini Enterprise** (Oct 2025) |
| Vertex AI | **Gemini Enterprise Agent Platform** (Cloud Next, Apr 2026 — "evolution of Vertex AI"; Vertex AI branding still visible in docs during transition) |
| BeyondCorp Enterprise | **Chrome Enterprise Premium** (2024) |
| Amazon CodeWhisperer | **Amazon Q Developer** (2024) |
| Amazon SageMaker | **Amazon SageMaker AI** (ML service) inside the new umbrella **Amazon SageMaker** platform with **SageMaker Unified Studio** + **SageMaker Lakehouse** (GA Mar 2025) |
| VMware Cloud on AWS (AWS-sold) | Sold by Broadcom only; AWS-native replacement is **Amazon Elastic VMware Service (EVS)** (GA Aug 2025) |
| Azure AD B2C | **Microsoft Entra External ID** (B2C closed to new tenants May 2025) |
| Stackdriver | **Google Cloud Observability** (Cloud Monitoring/Logging/Trace) |

---

## 1. Compute

| Capability | AWS | Azure | GCP | Notes/gotchas |
|---|---|---|---|---|
| Virtual machines | Amazon EC2 | Azure Virtual Machines | Compute Engine | EC2 has by far the largest instance-type catalog; Azure has strongest Windows/hybrid-benefit licensing story; GCE has custom machine types (arbitrary vCPU/RAM ratios) the others lack. |
| Spot/preemptible capacity | EC2 Spot Instances | Azure Spot Virtual Machines | Spot VMs (replaced Preemptible VMs) | GCP Spot VMs no longer have the old 24h max runtime (that was Preemptible); AWS gives 2-min interruption notice, Azure 30s, GCP 30s. |
| VM autoscaling groups | EC2 Auto Scaling Groups | Virtual Machine Scale Sets (VMSS) | Managed Instance Groups (MIGs) | VMSS "Flexible orchestration" is the modern default; classic Availability Sets are legacy. |
| Dedicated single-tenant hosts | EC2 Dedicated Hosts / Dedicated Instances | Azure Dedicated Host | Sole-tenant nodes | Licensing (BYOL Windows/SQL) is the usual driver; Azure Hybrid Benefit is the strongest license-portability program. |
| Bare metal | EC2 bare-metal instances (`*.metal`) | Azure BareMetal Infrastructure | Bare Metal Solution | **Gotcha:** GCP Bare Metal Solution is allowlist-only and being wound down in favor of Oracle Database@Google Cloud. Don't plan new builds on it. All three now sell Oracle Exadata via "Oracle Database@AWS/@Azure/@Google Cloud". |
| VMware workloads | **Amazon Elastic VMware Service (EVS)** — GA Aug 2025 | Azure VMware Solution (AVS) | Google Cloud VMware Engine (GCVE) | **Gotcha:** "VMware Cloud on AWS" is no longer sold by AWS (Broadcom took over sales, 2024). EVS runs VMware Cloud Foundation in *your* VPC with BYO VCF licenses — a different operating model than AVS/GCVE (provider-licensed, managed SDDC). |
| Classic PaaS (app hosting) | AWS Elastic Beanstalk | Azure App Service | Cloud Run (preferred) / App Engine (legacy) | App Engine is de-facto legacy — Google steers all new work to Cloud Run. Beanstalk gets minimal investment; App Service remains heavily invested. |
| Simple VPS | Amazon Lightsail | — (no direct product) | — (no direct product) | Azure/GCP nearest is a small VM + marketplace image. |
| Batch scheduling | AWS Batch | Azure Batch | Batch (GCP Batch replaced "Cloud Life Sciences") | GCP Batch is the modern service; Cloud Life Sciences API was deprecated. |
| HPC orchestration | AWS Parallel Computing Service (PCS) / ParallelCluster | Azure CycleCloud + HBv/HX series | Cluster Toolkit (formerly Cloud HPC Toolkit) | AWS PCS (managed Slurm, GA 2024) is the managed path. |
| Custom silicon (CPU) | Graviton (Arm) | Cobalt (Arm) | Axion (Arm) | All three have first-party Arm CPUs; Graviton most mature (4th gen GA, 5th announced), Axion (C4A/N4A) and Cobalt (Dps/Eps v6/v7) broad availability 2024–2026. |
| Edge/low-latency compute zones | AWS Local Zones, AWS Wavelength | Azure Extended Zones (public MEC program wound down) | Google Distributed Cloud edge; no Local-Zone equivalent | Azure's original carrier Edge Zones largely evaporated; Extended Zones (LA, Perth…) are current. AWS Wavelength (5G) stagnant but exists. |

## 2. Containers & Kubernetes

| Capability | AWS | Azure | GCP | Notes/gotchas |
|---|---|---|---|---|
| Managed Kubernetes | Amazon EKS | Azure Kubernetes Service (AKS) | Google Kubernetes Engine (GKE) | GKE most automated (in-place control-plane + node auto-upgrade by default); EKS historically most "assembly required," improved by Auto Mode. **Rename:** GKE Enterprise tier dissolved Sep 2025 — fleet management, Config Sync, Policy Controller now features of standard GKE. |
| "Hands-off" Kubernetes mode | EKS Auto Mode (Dec 2024) | AKS Automatic (GA 2025/26) | GKE Autopilot | Three genuinely comparable offerings now. Autopilot oldest/most mature; EKS Auto Mode bundles Karpenter-based node management. |
| Non-K8s container orchestrator | Amazon ECS | — (Service Fabric is legacy, avoid) | — | ECS remains a first-class, heavily used AWS-only orchestrator. |
| Serverless containers (task/pod level) | AWS Fargate (for ECS/EKS) | Azure Container Apps (ACA); Azure Container Instances (ACI) for raw containers | Cloud Run | Not equivalent: Fargate is a compute layer under an orchestrator; ACA and Cloud Run are full app platforms (scale-to-zero, HTTP/event-driven, Dapr in ACA). Cloud Run also runs GPU workloads and multi-container services + jobs. |
| App-platform for microservices | ~~AWS App Runner~~ (maintenance mode, no new customers after Apr 2026 → ECS Express Mode) | Azure Container Apps | Cloud Run | **Azure Spring Apps is retiring (end ~Mar 2028; closed to new customers) — migrate Spring workloads to ACA/AKS.** |
| Container registry | Amazon ECR (+ ECR Public) | Azure Container Registry (ACR) | Artifact Registry | **Retired:** Google Container Registry (gcr.io) shut down (writes ended 2025) — Artifact Registry mandatory. Artifact Registry also holds language packages (Maven/npm/Python) like AWS CodeArtifact; Azure uses Azure Artifacts. |
| Service mesh | **AWS App Mesh — retiring Sep 30, 2026.** Use ECS Service Connect, VPC Lattice, or self-managed Istio on EKS | Istio-based service mesh add-on for AKS (**Open Service Mesh retired 2023**) | Cloud Service Mesh (**rename:** Anthos Service Mesh + Traffic Director merged) | Do not start anything on App Mesh or OSM. VPC Lattice is AWS's strategic app-networking layer. |
| K8s on-prem/multicloud | Amazon EKS Anywhere; EKS Hybrid Nodes (2024); EKS Distro | Azure Arc-enabled Kubernetes; AKS on Azure Local | GKE on Google Distributed Cloud (ex-Anthos on bare metal/VMware); GKE Multi-Cloud (attached clusters) | Azure Arc attaches *any* CNCF cluster for policy/GitOps; GDC is a full Google-supported stack; EKS Anywhere requires you to run it. |
| K8s fleet management | — (EKS console multi-cluster thin; Karpenter for nodes) | Azure Kubernetes Fleet Manager | GKE fleets (ex-Anthos fleets, now standard GKE) | |
| Containers at the edge | ECS Anywhere / EKS on Outposts | AKS enabled by Azure Arc (edge) | GDC edge appliances / GKE on GDC | |

## 3. Serverless

| Capability | AWS | Azure | GCP | Notes/gotchas |
|---|---|---|---|---|
| Functions (FaaS) | AWS Lambda | Azure Functions (Flex Consumption is the modern plan) | **Cloud Run functions** (**rename:** Cloud Functions → Cloud Run functions, Aug 2024) | GCP functions now deploy as Cloud Run services (same infra, Eventarc triggers). Lambda max 15-min timeout; Cloud Run functions up to 60 min (HTTP); Azure Flex Consumption removed cold-start/VNet pain of the old Consumption plan. |
| Event bus / router | Amazon EventBridge | Azure Event Grid | Eventarc | Event Grid added MQTT broker capability (IoT-grade); EventBridge has the richest SaaS-partner source catalog + Pipes + Scheduler; Eventarc is trigger plumbing for Cloud Run/GKE more than a general bus (Eventarc Advanced closes some of the gap). |
| Workflow orchestration | AWS Step Functions | Azure Logic Apps + Durable Functions | Workflows + Application Integration | Step Functions: JSON (ASL) state machines, huge AWS-service integration surface. Logic Apps: 1,400+ SaaS connectors (enterprise iPaaS). GCP Workflows is minimal-but-cheap. |
| API gateway (REST/HTTP) | Amazon API Gateway | Azure API Management (APIM) | Apigee (flagship); Cloud API Gateway (lightweight, minimal investment) | Apigee & APIM are full API-management suites (products, monetization, dev portals); Amazon API Gateway is a runtime gateway. GCP's lightweight API Gateway/Cloud Endpoints receive little investment — assume Apigee. |
| GraphQL / realtime APIs | AWS AppSync (+ AppSync Events) | — (APIM GraphQL passthrough; Web PubSub / SignalR Service for realtime) | — (Firebase Data Connect / Realtime Database adjacent) | No true AppSync equivalent on the other clouds. |
| Serverless app assembly | AWS SAM / Application Composer | Azure Developer CLI (azd) + Bicep | — (gcloud + Terraform) | |
| Cron / scheduled jobs | Amazon EventBridge Scheduler | Azure Functions timer / Logic Apps recurrence | Cloud Scheduler | |
| Async task queues | SQS (+ Lambda event source) | Azure Queue Storage / Service Bus queues | Cloud Tasks | Cloud Tasks (push-with-rate-controls) has no exact AWS/Azure twin; nearest is SQS+Lambda with reserved concurrency. |
| Serverless containers-as-jobs | ECS Fargate tasks / AWS Batch on Fargate | Container Apps Jobs | Cloud Run jobs | |

## 4. Storage

| Capability | AWS | Azure | GCP | Notes/gotchas |
|---|---|---|---|---|
| Object storage | Amazon S3 | Azure Blob Storage | Cloud Storage (GCS) | S3 & GCS flat-namespace with strong consistency; Blob adds true hierarchical namespace via ADLS Gen2 (needed for analytics ACLs). GCS added hierarchical namespace buckets (2024). |
| Managed Iceberg tables on object storage | Amazon S3 Tables (Dec 2024) | Microsoft Fabric OneLake tables | BigLake tables for Apache Iceberg (+ BigLake metastore) | Different philosophies: S3 Tables = storage-level Iceberg primitive; OneLake = Fabric-managed Delta Lake; BigLake = BigQuery-governed Iceberg over GCS. |
| High-performance/low-latency object | S3 Express One Zone | Blob premium block blobs | Rapid Storage (zonal, 2025–26) | Single-zone products — durability trade-off vs regional object storage. |
| Block storage | Amazon EBS | Azure Managed Disks | Hyperdisk (current gen; Persistent Disk = prior gen) | Note the GCP shift: new machine series (C4 etc.) support **Hyperdisk only**. Azure Ultra Disk ≈ EBS io2 Block Express ≈ Hyperdisk Extreme. |
| SAN-as-a-service | — (io2 Block Express fills part) | Azure Elastic SAN | — | Azure-only category. |
| File (NFS/SMB, general) | Amazon EFS (NFS) | Azure Files (SMB+NFS) | Filestore (NFS) | EFS is elastic/pay-per-use; Filestore is provisioned-capacity; Azure Files is the only strong SMB-native option with AD auth. |
| File (enterprise NetApp) | Amazon FSx for NetApp ONTAP | Azure NetApp Files | Google Cloud NetApp Volumes | The closest true three-way equivalence in the whole file category. |
| File (Windows) | FSx for Windows File Server | Azure Files (SMB) / Azure Local file services | — (use NetApp Volumes SMB) | |
| File (HPC parallel) | FSx for Lustre | Azure Managed Lustre | Google Cloud Managed Lustre (GA 2025, DDN-based) | |
| ZFS | FSx for OpenZFS | — | — | AWS-only. |
| Archive/cold tiers | S3 Glacier Instant / Flexible / Deep Archive | Blob Cool / Cold / Archive tiers | GCS Nearline / Coldline / Archive (+ Autoclass) | **Gotcha:** GCS Archive has millisecond access (no rehydration) but 365-day min storage; Azure Archive requires rehydration (hours); Glacier Deep Archive cheapest but 12h+ retrieval. Autoclass (GCS) and S3 Intelligent-Tiering automate tiering; Azure uses lifecycle rules only. |
| Hybrid file/cache gateway | AWS Storage Gateway (File/Volume/Tape) | Azure File Sync | — (partner: NetApp, Komprise) | |
| Online data transfer | AWS DataSync; AWS Transfer Family (SFTP/FTPS/AS2) | AzCopy / Azure Data Factory; Azure Storage Mover; SFTP endpoint on Blob | Storage Transfer Service | |
| Physical transfer devices | **Snow family effectively retired**: Snowcone & Snowmobile discontinued 2024; Snowball Edge existing-customers-only since Nov 2025 → **AWS Data Transfer Terminal** (drive-up locations, 2024) or DataSync | Azure Data Box (Disk / 120TB / 525TB next-gen) | Transfer Appliance | Do not put Snowball in new designs. Azure Data Box is now the most complete offline-device lineup. |
| Backup (centralized) | AWS Backup | Azure Backup | Google Cloud Backup and DR (Actifio-based); Backup vaults for GCE/GCS | |

## 5. Databases

| Capability | AWS | Azure | GCP | Notes/gotchas |
|---|---|---|---|---|
| Managed OSS relational | Amazon RDS (MySQL, PostgreSQL, MariaDB, SQL Server, Oracle, Db2) | Azure Database for MySQL / PostgreSQL (Flexible Server) | Cloud SQL (MySQL, PostgreSQL, SQL Server) | **Retired:** Azure Database for MariaDB (Sep 2025 → MySQL Flexible Server). Single Server SKUs long gone. |
| Cloud-native enhanced relational | Amazon Aurora (MySQL/PG; + Serverless v2, Limitless, **Aurora DSQL** GA May 2025) | Azure SQL Database Hyperscale | AlloyDB for PostgreSQL | **Retired:** Aurora Serverless v1 (Dec 2024). Aurora DSQL is a *new category* (multi-region active-active, PG-compatible, optimistic concurrency — not a lift-and-shift target for FK-heavy apps). |
| Commercial SQL Server PaaS | RDS for SQL Server | Azure SQL Database / Azure SQL Managed Instance | Cloud SQL for SQL Server | Azure SQL MI is the only near-full-parity SQL Server surface (SQL Agent, cross-db queries, CLR). |
| Globally distributed SQL | Aurora DSQL; Aurora Global Database (replica-based) | Cosmos DB (NoSQL, multi-region writes); Azure SQL active geo-replication (single-writer) | Cloud Spanner | Spanner is the mature product (external consistency, TrueTime); Aurora DSQL the new challenger; Azure has no true multi-writer SQL equivalent. |
| NoSQL document | Amazon DocumentDB (MongoDB compatibility) | Azure Cosmos DB (NoSQL API + MongoDB API/vCore — vCore lineage aligned with the open-source **DocumentDB** project Microsoft launched 2025) | Firestore (+ Firestore with MongoDB compatibility, 2025) | **Not equivalent:** Cosmos DB is multi-model with 5 tunable consistency levels and per-region multi-writer; RU/s capacity math surprises AWS people. Amazon DocumentDB is MongoDB-*compatible* (API gaps vs modern MongoDB). Firestore is mobile/web-first with realtime listeners — different design center. |
| Key-value at scale | Amazon DynamoDB | Azure Cosmos DB (NoSQL/Table API) | Bigtable / Firestore | **Not equivalent:** DynamoDB = opinionated KV+single-table design, per-request pricing, DAX, Streams. Cosmos = richer queries/indexing-by-default but RU cost model. Bigtable = wide-column, petabyte scan-heavy. Choose per access pattern, not by name-matching. |
| Wide-column (Cassandra) | Amazon Keyspaces | Azure Managed Instance for Apache Cassandra (Cosmos Cassandra API de-emphasized) | Bigtable (CQL support) / partner Astra | |
| In-memory cache | Amazon ElastiCache (**Valkey**, Redis OSS, Memcached) | **Azure Managed Redis** (**rename/retire:** Azure Cache for Redis → retiring 2027/2028) | Memorystore (Valkey, Redis Cluster, Redis, Memcached) | Post-Redis-license-change, AWS & GCP lead with **Valkey** (cheaper SKUs); Azure went the opposite way — Redis Enterprise-based Managed Redis (Redis Inc. partnership) with modules (search, JSON, timeseries). |
| Durable in-memory DB | Amazon MemoryDB (Valkey/Redis-compatible, durable) | Azure Managed Redis (Enterprise flash/HA approximates) | Memorystore w/ persistence | MemoryDB's multi-AZ durable log is unique-ish. |
| Graph | Amazon Neptune (+ Neptune Analytics) | Cosmos DB for Apache Gremlin | Spanner Graph (2024) | **Gotcha:** Cosmos Gremlin API sees minimal investment. Spanner Graph is GQL-based (not Gremlin). Neptune supports openCypher + Gremlin + SPARQL. |
| Time-series | **Amazon Timestream for InfluxDB** (Timestream for LiveAnalytics **closed to new customers 2025**) | Azure Data Explorer (ADX/Kusto) / Fabric Eventhouse (**Azure Time Series Insights retired Mar 2025**) | Bigtable or BigQuery (no dedicated TSDB); Managed Service for Prometheus for metrics | Nobody has a healthy first-party general TSDB except managed InfluxDB (AWS) and Kusto-family (Azure — excellent but proprietary KQL). |
| Ledger / verifiable | **Amazon QLDB retired (Jul 2025)** → Aurora PostgreSQL + audit patterns | Azure Confidential Ledger; SQL ledger tables | — (Cloud Audit Logs; no ledger DB) | Don't reference QLDB; it's gone. |
| Vector search (DB-native) | OpenSearch vector engine; pgvector on RDS/Aurora; S3 Vectors (GA Dec 2025); MemoryDB vector | Azure AI Search vector store; Cosmos DB vector; pgvector on Azure PG | AlloyDB AI / pgvector+ScaNN; Vertex Vector Search; BigQuery vector search | Every DB grew vectors 2023–2025; differentiate on scale + hybrid search quality, not the checkbox. |
| DB migration tooling | AWS DMS (+ Schema Conversion) | Azure Database Migration Service | Database Migration Service (DMS) | GCP DMS added SQL Server and Oracle→PostgreSQL paths (Gemini-assisted conversion GA); AWS DMS most battle-tested for heterogeneous migrations. |

## 6. Analytics & Big Data

| Capability | AWS | Azure | GCP | Notes/gotchas |
|---|---|---|---|---|
| Data warehouse | Amazon Redshift | Microsoft Fabric Warehouse (strategic); Azure Synapse dedicated SQL pools (maintenance-mode positioning) | BigQuery | **Architecturally different:** BigQuery = serverless, storage/compute fully separated, on-demand or slot pricing. Redshift = provisioned clusters or Serverless, best when data lives in AWS. Synapse **not formally retired** but Microsoft's investment is in Fabric — new builds target Fabric; Synapse Data Explorer retired Oct 2025. |
| Unified data platform / lakehouse | Amazon SageMaker (umbrella): **Unified Studio + Lakehouse + Catalog** (GA Mar 2025; absorbed DataZone) | **Microsoft Fabric** (OneLake, Warehouse, Lakehouse, Data Factory, Real-Time Intelligence, Power BI) | BigQuery + BigLake + Dataplex Universal Catalog | The three "one platform" bets. Fabric is SaaS with capacity-based (CU) pricing — a licensing model unlike anything on AWS/GCP. |
| Spark / managed big-data clusters | Amazon EMR (+ EMR Serverless) | Fabric Spark / Azure Databricks; Synapse Spark (legacy); **HDInsight — avoid for new builds** | Dataproc (+ Dataproc Serverless) | Databricks runs on all three but is jointly-operated first-party only on Azure. |
| Streaming ingestion | Amazon Kinesis Data Streams; Amazon MSK (+ Serverless, Express brokers) | Azure Event Hubs (Kafka-protocol compatible); Fabric Real-Time hub | Pub/Sub; Google Cloud Managed Service for Apache Kafka (GA 2024–25) | **Retired:** Pub/Sub Lite (Mar 2026). Event Hubs speaks Kafka wire protocol without being Kafka; Pub/Sub is global with no shards to manage. |
| Stream processing | Amazon Managed Service for Apache Flink (**rename:** ex-Kinesis Data Analytics) | Azure Stream Analytics (legacy-ish); Fabric Real-Time Intelligence (Eventstream/KQL) | Dataflow (Apache Beam) | Dataflow is unified batch+streaming (Beam) — no true AWS/Azure equivalent; Flink is the cross-cloud lingua franca. |
| ETL / data integration | AWS Glue (+ zero-ETL integrations) | Azure Data Factory → converging into Fabric Data Factory | Cloud Data Fusion; Dataflow; BigQuery Data Transfer Service | "Zero-ETL" (Aurora/RDS/DynamoDB → Redshift) is an AWS differentiator; Microsoft's equivalent is Fabric Mirroring; GCP's is Datastream CDC into BigQuery. |
| CDC replication | AWS DMS / zero-ETL | Fabric Mirroring / ADF CDC | Datastream | |
| ELT/SQL transformation framework | — (partner: dbt) | — (partner: dbt; Fabric dataflows) | Dataform (first-party dbt-alike) | |
| Query-in-place (data lake SQL) | Amazon Athena (Trino-based) | Synapse serverless SQL pool (legacy) / Fabric SQL endpoint on OneLake | BigQuery external/BigLake tables | **Retired-adjacent:** S3 Select discontinued for new use (2024) — use Athena. |
| Orchestration (data pipelines) | Amazon MWAA (Managed Airflow) | Fabric Data Factory pipelines / ADF | Cloud Composer (Airflow) | **AWS Data Pipeline** closed to new customers — don't use. |
| Data catalog & governance | Amazon SageMaker Catalog (ex-DataZone) + Glue Data Catalog + Lake Formation | Microsoft Purview | Dataplex Universal Catalog (**absorbed Data Catalog, shut down 2024–2025**) | Purview spans M365 + Azure (DLP, compliance) — much broader. Lake Formation = fine-grained lake permissions; no exact twin. |
| BI | Amazon QuickSight (→ "Quick Suite" rebrand 2025) | Power BI (inside Fabric) | Looker; Looker Studio (free tier) | Power BI is the category leader and inseparable from Fabric capacities. Looker = semantic-model-first (LookML) — different product philosophy than dashboard-first tools. |
| Managed search/log analytics engine | Amazon OpenSearch Service (+ Serverless) | Azure AI Search (app search) / Azure Data Explorer & Log Analytics (logs) | — (partner Elastic Cloud); BigQuery + Log Analytics for logs | **Gotcha:** "Azure AI Search" ≠ Elasticsearch replacement for log analytics — that's ADX/Log Analytics. GCP has no first-party OpenSearch/Elastic clone. |
| Data clean rooms | AWS Clean Rooms | — (partner / Fabric patterns) | BigQuery data clean rooms | |
| Sharing/marketplace | AWS Data Exchange | Azure Data Share (limited investment) / Fabric external data sharing | Analytics Hub (BigQuery sharing) | |

## 7. AI / ML

| Capability | AWS | Azure | GCP | Notes/gotchas |
|---|---|---|---|---|
| ML platform (train/deploy/MLOps) | Amazon SageMaker AI | Azure Machine Learning (under Microsoft Foundry umbrella) | Vertex AI training/pipelines → **Gemini Enterprise Agent Platform** (**rename Apr 2026**) | All three merged "data + ML + GenAI" into one branded platform 2025–26. Expect docs to mix old/new names for a while. |
| Foundation-model API service | Amazon Bedrock | **Microsoft Foundry Models** (Azure OpenAI now sold within Foundry) | Gemini API on Gemini Enterprise Agent Platform; Model Garden | Model access: Bedrock = Anthropic/Meta/Mistral/Cohere/Nova + OpenAI (2025–26); Foundry = OpenAI **and** Anthropic (Nov 2025) + open models; Google = Gemini + 200+ Model Garden incl. Anthropic. |
| First-party frontier models | Amazon Nova family (incl. Nova 2, Nova Sonic) | — (Phi/MAI small models; relies on OpenAI+Anthropic) | Gemini family (+ Gemma open, Imagen, Veo) | |
| Agent platform | **Amazon Bedrock AgentCore** (GA Oct 2025) + Strands Agents SDK | Microsoft Foundry Agent Service + Microsoft Agent Framework (Semantic Kernel/AutoGen successor) | Agent Engine + ADK + A2A protocol, Agent Registry/Gateway (Next '26) | The 2025–26 battleground. MCP supported by all three; A2A originated at Google (now Linux Foundation). Classic "Bedrock Agents" superseded by AgentCore. |
| Enterprise AI assistant | Amazon Q Business | Microsoft 365 Copilot / Copilot Studio | **Gemini Enterprise** (**rename:** Google Agentspace, Oct 2025) | M365 Copilot licensed per-user through Microsoft 365, not Azure. |
| AI coding assistant | Amazon Q Developer (**rename:** CodeWhisperer) + Kiro (agentic IDE) | GitHub Copilot | Gemini Code Assist + Antigravity IDE | |
| Enterprise search (RAG retrieval) | Amazon Kendra (GenAI index); Bedrock Knowledge Bases | Azure AI Search (de-facto RAG store for Foundry) | Vertex AI Search (under Gemini Enterprise) | |
| Speech-to-text / TTS | Amazon Transcribe / Polly | Azure AI Speech | Speech-to-Text (Chirp) / Text-to-Speech | Realtime speech-to-speech: Nova Sonic (AWS), GPT-realtime via Foundry (Azure), Gemini Live API (GCP). |
| Translation | Amazon Translate | Azure AI Translator | Cloud Translation | |
| Vision APIs | Amazon Rekognition | Azure AI Vision (+ Face, Video Indexer) | Cloud Vision / Video Intelligence | Increasingly superseded by multimodal LLM calls — check price-per-call before defaulting to legacy vision APIs. |
| Document processing (OCR/IDP) | Amazon Textract; Bedrock Data Automation | Azure AI Document Intelligence (**rename:** Form Recognizer) | Document AI | |
| NLP APIs (classic) | Amazon Comprehend | Azure AI Language | Cloud Natural Language (legacy) | Classic task-specific NLP APIs all in sunset-glide; several AWS AI services (**Forecast, Lookout family, CodeGuru Reviewer, Monitron, Panorama**) closed to new customers 2024–2025. |
| Content moderation/safety | Bedrock Guardrails; Rekognition moderation | Azure AI Content Safety | Model Armor; Gemini safety settings | |
| ML feature store | SageMaker Feature Store | Azure ML managed feature store | Vertex AI Feature Store | |
| Custom AI accelerators | AWS Trainium / Inferentia | Azure Maia (+ Cobalt CPU) | Google TPU (v5e/v6 Trillium/v7 Ironwood) | TPUs the most mature external offering; Trainium2/3 broadly available; Maia mostly internal-use — don't plan capacity on it. |

## 8. Networking

| Capability | AWS | Azure | GCP | Notes/gotchas |
|---|---|---|---|---|
| Virtual network | Amazon VPC (regional; subnets zonal) | Azure Virtual Network (regional) | VPC (**global** — subnets regional) | GCP's global VPC is a real architectural difference: one VPC spans all regions; AWS/Azure need peering/hub-spoke across regions. |
| L7 load balancing | Application Load Balancer (ALB) | Azure Application Gateway (regional, +WAF); Azure Front Door (global) | Global external Application LB | GCP's single anycast-IP global LB has no true AWS equivalent (CloudFront+ALB or Global Accelerator+ALB approximates). |
| L4 load balancing | Network Load Balancer (NLB) | Azure Load Balancer | Passthrough Network LB | |
| Global traffic steering | AWS Global Accelerator; Route 53 routing policies | Azure Front Door; Azure Traffic Manager (DNS-based, legacy-ish) | Built into global LB anycast; Cloud DNS routing policies | |
| DNS | Amazon Route 53 | Azure DNS (+ Private Resolver) | Cloud DNS | Route 53 uniquely bundles health-checked routing + Resolver endpoints + domain registration (Google Domains sold to Squarespace 2023). |
| CDN | Amazon CloudFront | Azure Front Door (**Azure CDN classic dying:** Edgio terminated Jan 2025; "Azure CDN from Microsoft (classic)" retiring Sep 2027) | Cloud CDN (+ Media CDN for video) | Do not deploy new Azure CDN classic profiles. |
| Private fiber connectivity | AWS Direct Connect | Azure ExpressRoute | Cloud Interconnect (+ **Cross-Cloud Interconnect** to AWS/Azure/OCI) | GCP's Cross-Cloud Interconnect (managed cloud-to-cloud fiber) is unique as a product. |
| VPN | AWS Site-to-Site VPN / Client VPN | Azure VPN Gateway / P2S | Cloud VPN (HA VPN) | |
| Transit / hub networking | AWS Transit Gateway; AWS Cloud WAN | Azure Virtual WAN; Route Server | Network Connectivity Center (NCC) | |
| NAT | AWS NAT Gateway | Azure NAT Gateway | Cloud NAT | Cloud NAT is software-defined (no choke-point instance, no per-AZ dance); AWS NAT GW per-AZ pricing is a notorious cost trap. |
| Private access to PaaS/SaaS | AWS PrivateLink (+ VPC endpoints) | Azure Private Link (+ private endpoints) | Private Service Connect (PSC) | Same concept everywhere; PSC also fronts Google APIs globally. Azure service endpoints (older) ≠ Private Link — avoid for new designs. |
| Service-to-service app networking | Amazon VPC Lattice | — (partial: Front Door + Private Link, ACA internal) | Cloud Service Mesh / PSC | VPC Lattice is AWS-unique as a product category. |
| Network firewall (managed NGFW) | AWS Network Firewall | Azure Firewall (Basic/Std/Premium) | Cloud NGFW | |
| DDoS protection | AWS Shield Standard/Advanced | Azure DDoS Protection | Cloud Armor (bundles DDoS + WAF) | |
| Network observability | VPC Flow Logs, Reachability Analyzer, CloudWatch Network Monitor | Azure Network Watcher, Connection Monitor | Network Intelligence Center | |
| IPAM | Amazon VPC IPAM | Azure IPAM (in AVNM) | — (VPC internal ranges; no full IPAM product) | |

## 9. Security & Identity

| Capability | AWS | Azure | GCP | Notes/gotchas |
|---|---|---|---|---|
| Cloud IAM (resource authz) | AWS IAM | Azure RBAC (+ ABAC conditions) | Cloud IAM | Models differ fundamentally: AWS = policy documents; Azure = role assignments on scope hierarchy; GCP = role bindings on resource hierarchy. Cross-cloud "role mapping" is never 1:1. |
| Workforce identity provider | AWS IAM Identity Center (**rename:** AWS SSO) | **Microsoft Entra ID** (**rename:** Azure AD, 2023) | Cloud Identity (+ Google Workspace) | Entra ID is a full IdP; IAM Identity Center and Cloud Identity are thinner — most shops federate from Entra/Okta. |
| Customer identity (CIAM) | Amazon Cognito | **Microsoft Entra External ID** (**Azure AD B2C closed to new tenants May 2025**) | Identity Platform (Firebase Auth-based) | Don't start on B2C. Cognito got a major refresh 2024–25 (Essentials tiers, passwordless). |
| Workload identity federation | IAM Roles Anywhere; OIDC federation | Entra Workload ID | Workload Identity Federation | |
| Secrets management | AWS Secrets Manager (+ SSM Parameter Store) | Azure Key Vault (secrets) | Secret Manager | Key Vault mixes secrets+keys+certs; AWS/GCP split them. |
| KMS | AWS KMS | Azure Key Vault keys / Managed HSM | Cloud KMS | |
| Dedicated HSM | AWS CloudHSM | Azure Dedicated HSM (**retiring → Managed HSM**) / Azure Cloud HSM | Cloud HSM (built into Cloud KMS) | |
| External/hold-your-own-key | AWS KMS External Key Store (XKS) | Managed HSM + HYOK patterns | Cloud EKM | GCP Cloud EKM is the most mature hold-your-own-key story. |
| WAF | AWS WAF | Azure WAF (Front Door / App Gateway) | Cloud Armor | |
| Threat detection (workload) | Amazon GuardDuty | Microsoft Defender for Cloud (plans per resource type) | SCC threat detection (ETD/CTD) | |
| CSPM / posture | AWS Security Hub (relaunched 2025, unified) | Defender for Cloud CSPM | Security Command Center (Standard/Premium/Enterprise→Premium) | Defender for Cloud and SCC are explicitly multicloud; AWS Security Hub is AWS-only. |
| SIEM | — no first-party SIEM: Amazon Security Lake (OCSF) + partner | **Microsoft Sentinel** (+ Sentinel data lake; unified Defender portal) | **Google Security Operations** (**rename:** Chronicle) | Microsoft and Google sell real SIEMs; AWS deliberately doesn't. |
| SOAR | — (Security Hub automations; partner) | Sentinel playbooks (Logic Apps) | Google SecOps SOAR (ex-Siemplify) | |
| Compliance audit/attestation | AWS Audit Manager; AWS Artifact | Purview Compliance Manager; Service Trust Portal | Compliance Manager (in SCC); Assured Workloads | |
| Zero-trust access (users→apps) | AWS Verified Access | Entra Private Access / Global Secure Access (SSE) | **Chrome Enterprise Premium** (**rename:** BeyondCorp Enterprise) + IAP | Microsoft's Global Secure Access is a full SSE (SWG+ZTNA); AWS/GCP offerings narrower. |
| Confidential computing | AWS Nitro Enclaves | Azure confidential VMs (SEV-SNP/TDX) + Confidential Containers | Confidential VMs / GKE / Confidential Space | Azure has the broadest confidential portfolio. |
| Cert management | AWS Certificate Manager (ACM) / Private CA | Key Vault certificates | Certificate Manager / CA Service | |

## 10. DevOps & Management

| Capability | AWS | Azure | GCP | Notes/gotchas |
|---|---|---|---|---|
| IaC (native) | AWS CloudFormation + AWS CDK | ARM templates + **Bicep** (strategic) | **Infrastructure Manager** (Terraform-based) — **Deployment Manager EOL Dec 31, 2025** | Do not use Deployment Manager. Terraform/OpenTofu is the de-facto cross-cloud layer; **Azure Blueprints retiring Jul 2026 → Template Specs/Deployment Stacks**. |
| K8s-style config for cloud resources | AWS Controllers for Kubernetes (ACK) | Azure Service Operator | Config Connector | |
| Git hosting | **AWS CodeCommit — closed to new customers (Jul 2024)** | Azure Repos; GitHub (Microsoft-owned) | **Cloud Source Repositories — closed to new customers (Jun 2024)** → Secure Source Manager | Practically: GitHub/GitLab everywhere. |
| CI/CD | AWS CodePipeline + CodeBuild + CodeDeploy (**CodeStar retired 2024; Cloud9 closed 2024**) | GitHub Actions (strategic) + Azure Pipelines | Cloud Build + Cloud Deploy | Microsoft's strategic CI/CD is GitHub Actions; Azure DevOps supported but slow-roll. |
| Artifact/package repos | AWS CodeArtifact | Azure Artifacts | Artifact Registry | |
| IDP/platform engineering | **AWS Proton — end of support Oct 7, 2026. Do not adopt.** | Azure Deployment Environments + Dev Box | — (Backstage patterns; Cloud Workstations) | Managed dev environments: Microsoft Dev Box; Google Cloud Workstations; (Cloud9 dead). |
| Monitoring (metrics/logs) | Amazon CloudWatch (+ Logs, Application Signals) | Azure Monitor (+ Log Analytics/KQL, Application Insights) | Google Cloud Observability (**rename:** Stackdriver) | Azure's KQL is the strongest query experience; GCP Log Analytics (BigQuery-backed) is the answer. |
| Tracing/APM | AWS X-Ray → CloudWatch Application Signals (OTel-based) | Application Insights (OTel distro) | Cloud Trace (**Cloud Debugger retired 2023, Profiler deprecated**) | All three converged on OpenTelemetry — instrument with OTel, not proprietary SDKs. |
| Managed Prometheus | Amazon Managed Service for Prometheus | Azure Monitor managed Prometheus | Google Cloud Managed Service for Prometheus | |
| Managed Grafana | Amazon Managed Grafana | Azure Managed Grafana | — (partner Grafana Cloud) | |
| Cost management | AWS Billing and Cost Management (Cost Explorer, Budgets, CUR 2.0/Data Exports) | Microsoft Cost Management (+ FinOps toolkit) | Cloud Billing + FinOps Hub | All three export FOCUS-format billing data — use FOCUS for cross-cloud cost normalization. |
| Config/change tracking & policy | AWS Config + SCPs/RCPs | Azure Policy (**Azure Automanage retired Sep 2025**) | Organization Policy + Cloud Asset Inventory | Azure Policy does deploy-time *and* audit + remediation; AWS splits prevent (SCP) vs detect (Config); GCP org policy gained custom constraints. |
| Operational automation/runbooks | AWS Systems Manager (SSM) | Azure Automation + Update Manager | VM Manager (OS Config) | SSM is far broader (fleet, patch, sessions, hybrid). |
| Landing zones | AWS Control Tower + Organizations | Azure landing zones (CAF) + Management Groups | Cloud Setup + Cloud Foundation Fabric FAST | |
| Chaos engineering | AWS Fault Injection Service (FIS) | Azure Chaos Studio | — (no first-party) | |
| Advisory | AWS Trusted Advisor + Well-Architected Tool | Azure Advisor | Recommender / Active Assist | |

## 11. Integration & Messaging

| Capability | AWS | Azure | GCP | Notes/gotchas |
|---|---|---|---|---|
| Queues (simple) | Amazon SQS (Std + FIFO) | Azure Queue Storage (basic); Service Bus queues (enterprise) | Pub/Sub (pull subscriptions); Cloud Tasks | GCP has no plain queue service — Pub/Sub covers it (at-least-once, ordering keys, exactly-once option). |
| Pub/sub topics (fan-out) | Amazon SNS | Service Bus topics; Event Grid | Cloud Pub/Sub | **Retired:** Pub/Sub Lite (Mar 2026). Pub/Sub is one global service for both queueing and fan-out. |
| Enterprise message broker (JMS/AMQP) | Amazon MQ (ActiveMQ/RabbitMQ) | Azure Service Bus (Premium; JMS 2.0) | — (partner; or Managed Kafka) | Service Bus is the strongest enterprise-messaging product (sessions, transactions, dead-lettering, dedup). |
| Event streaming (Kafka) | Amazon MSK (+ Serverless, Express) | Azure Event Hubs (Kafka-compatible endpoint); Confluent | Google Cloud Managed Service for Apache Kafka | Event Hubs ≈ Kafka API but not Kafka internals (no server-side Streams; Schema Registry differences). |
| Event grid / SaaS events | Amazon EventBridge (partner sources) | Azure Event Grid (MQTT, CloudEvents-native) | Eventarc | CloudEvents: Event Grid & Eventarc native; EventBridge uses its own envelope. |
| iPaaS / SaaS connectors | Amazon AppFlow (limited growth) | Azure Logic Apps (1,400+ connectors) + Power Automate | Application Integration | Azure is far ahead for SaaS integration breadth. |
| B2B/EDI | AWS B2B Data Interchange; Transfer Family AS2 | Logic Apps B2B (Integration Account) | — | |

## 12. Migration & Hybrid

| Capability | AWS | Azure | GCP | Notes/gotchas |
|---|---|---|---|---|
| Server/VM lift-and-shift | AWS Application Migration Service (MGN) | Azure Migrate (+ Site Recovery engine) | Migrate to Virtual Machines | |
| Migration assessment/portfolio | Migration Hub + Application Discovery; Migration Evaluator | Azure Migrate (assessment) | Migration Center | |
| Database migration | AWS DMS + SCT | Azure Database Migration Service | Database Migration Service | |
| Disaster recovery to cloud | AWS Elastic Disaster Recovery (DRS) | Azure Site Recovery (ASR) | Backup and DR Service | ASR is the most complete (failback, runbooks); AWS DRS replaced CloudEndure. |
| Hybrid full-stack (cloud-in-your-DC) | AWS Outposts (racks + servers, 2nd gen 2025) | **Azure Local** (**rename:** Azure Stack HCI, Nov 2024) + Azure Stack Hub (legacy) | **Google Distributed Cloud (GDC)** — connected & air-gapped | Different models: Outposts = AWS-owned hardware; Azure Local = your validated hardware + Azure control plane; GDC air-gapped is the only fully disconnected-cloud product (used by sovereigns). |
| Hybrid/multicloud control plane | — (SSM hybrid activations; EKS Connector — narrow) | **Azure Arc** (servers, K8s, data services) | GDC + GKE attached clusters | Azure Arc is the broadest "project any resource into ARM" story; AWS has no real equivalent. |
| Sovereign cloud | AWS European Sovereign Cloud (GA Jan 2026, Brandenburg) | Microsoft Cloud for Sovereignty (+ EU Data Boundary, Delos) | GDC air-gapped + Sovereign partnerships (S3NS/Thales) | |
| File/data migration online | AWS DataSync | Azure Storage Mover / AzCopy / File Sync | Storage Transfer Service | |
| Offline transfer devices | **Data Transfer Terminal**; Snowball existing-customers-only | Azure Data Box family | Transfer Appliance | |
| Mainframe migration | AWS Mainframe Modernization (M2) + AWS Transform | Azure mainframe migration (partner-led) | Google Cloud Dual Run / Mainframe Modernization | |
| License/inventory management | AWS License Manager | Azure Hybrid Benefit + license mgmt | — (BYOL via sole-tenant) | |

## 13. IoT & Edge

| Capability | AWS | Azure | GCP | Notes/gotchas |
|---|---|---|---|---|
| IoT device connectivity (MQTT broker) | AWS IoT Core | Azure IoT Hub; Event Grid MQTT broker | **None — Google Cloud IoT Core retired Aug 2023.** Partner: ClearBlade, EMQX, HiveMQ → Pub/Sub | GCP exited first-party IoT entirely. Do not architect GCP-native IoT without a partner broker. |
| Device provisioning at scale | IoT Core fleet provisioning | Device Provisioning Service (DPS) | — (partner) | |
| Device fleet management | AWS IoT Device Management (**Fleet Hub console retired Oct 2025**) | IoT Hub device twins + Azure Device Update | — | |
| IoT app platform (SaaS) | — | Azure IoT Central — **treat as risky** (2027 retirement notice published Feb 2024 then retracted as "erroneous"; investment shifted to Azure IoT Operations) | — | Microsoft's strategic direction is **Azure IoT Operations** (Arc-based, GA Nov 2024), not IoT Central. |
| Edge runtime (gateway software) | AWS IoT Greengrass | Azure IoT Edge (maintenance-ish) → Azure IoT Operations | — (GDC edge for heavy edge) | |
| Industrial IoT / asset data | AWS IoT SiteWise | Azure IoT Operations + Fabric Real-Time Intelligence | Manufacturing Data Engine (partner-heavy) | |
| Digital twins | AWS IoT TwinMaker | Azure Digital Twins | — | |
| IoT analytics/rules | **AWS IoT Analytics retired Dec 15, 2025**; **AWS IoT Events retiring May 20, 2026** → Kinesis/Timestream-for-InfluxDB pipelines | Azure IoT Operations data flows → Event Hubs/Fabric | Pub/Sub → Dataflow → BigQuery | AWS is pruning its IoT portfolio hard — verify any AWS IoT sub-service before committing. |
| Secured MCU / device OS | FreeRTOS (AWS-stewarded) | Azure Sphere; Azure RTOS → **donated to Eclipse as "Eclipse ThreadX" (2023)** | — | |
| Connected vehicles | AWS IoT FleetWise | Microsoft Connected Fleets (reference) | — (partner) | |

---

## Deprecation / retirement watchlist (2024–2026) — do not build on these

**AWS:**
- Retired outright: Amazon QLDB (Jul 2025), Aurora Serverless v1 (Dec 2024), Amazon Elastic Transcoder (Nov 2025 → MediaConvert), AWS CodeStar (2024), Amazon Honeycode, Amazon Sumerian, DeepLens/DeepComposer/DeepRacer devices, Amazon WorkDocs (2025), S3 Select (new use), Snowcone & Snowmobile (2024), AWS IoT Analytics (Dec 2025), IoT Fleet Hub (Oct 2025).
- Retiring on a date: **AWS App Mesh (Sep 30, 2026)**, **AWS Proton (Oct 7, 2026)**, **AWS IoT Events (May 20, 2026)**, **Amazon Pinpoint (EOL Oct 2026)**.
- Closed to new customers: CodeCommit, Cloud9, CloudSearch, Data Pipeline, Forecast, Timestream for LiveAnalytics, Snowball Edge (Nov 2025), App Runner (Apr 2026), several AI services (Lookout family, Monitron, Panorama, CodeGuru Reviewer).

**Azure:**
- Retired: Azure Database for MariaDB (Sep 2025), Azure Time Series Insights (Mar 2025), Azure Data Studio (Feb 28, 2026 → VS Code MSSQL extension), Azure Automanage (Sep 2025), Synapse Data Explorer (Oct 2025), Open Service Mesh (2023), Azure AD B2C new tenants (May 2025), Edgio-based Azure CDN (Jan 2025), Basic Load Balancer + Basic public IPs (Sep 2025), Azure Service Manager/classic resources (phased through 2024–2026).
- Retiring on a date: Azure Blueprints (Jul 2026), Azure Cache for Redis Enterprise (Mar 2027) and Basic/Std/Premium (Sep 2028) → Azure Managed Redis, Azure Spring Apps (~Mar 2028), Azure Lab Services (Jun 2027), Azure Front Door classic (Mar 2027), Azure CDN Microsoft classic (Sep 2027), Sentinel-in-Azure-portal (Mar 2027), Azure Dedicated HSM (→ Managed HSM).
- Strategic caution: Azure Synapse (not retired, but Fabric is the investment target), HDInsight, Stream Analytics, IoT Central, Azure IoT Edge (IoT Operations is the successor).

**GCP:**
- Retired: Cloud IoT Core (Aug 2023), Container Registry (2025 → Artifact Registry), Cloud Deployment Manager (EOL Dec 31, 2025 → Infrastructure Manager), Pub/Sub Lite (Mar 2026), Data Catalog (→ Dataplex Universal Catalog), Cloud Debugger (2023), Cloud Source Repositories (closed Jun 2024), Google Domains (sold to Squarespace), App Engine Gen1 runtimes (deploys blocked Jan 2026).
- Strategic caution: App Engine (Cloud Run is the successor), Bare Metal Solution (wind-down), lightweight API Gateway/Cloud Endpoints (Apigee is the investment), SCC Enterprise tier (retiring May 2027 → Premium).

## Cross-cutting "false equivalence" warnings

1. **DynamoDB ≠ Cosmos DB ≠ Firestore/Bigtable.** Pricing units (RCU/WCU vs RU/s vs ops+storage), consistency models, and data-modeling idioms (single-table vs container vs document-collection vs wide-column) make migration a redesign, not a port.
2. **BigQuery ≠ Redshift ≠ Synapse/Fabric.** BigQuery is serverless multi-tenant with slot economics; Redshift is provisioned/serverless clusters tuned for AWS-local joins; Fabric is a SaaS capacity (CU) bundle where warehouse, Spark, and Power BI draw from one meter — cost governance models are incomparable.
3. **Event Hubs "Kafka" is protocol compatibility, not Kafka.** Same caution for Amazon DocumentDB vs real MongoDB, Keyspaces vs real Cassandra (Azure Managed Instance for Cassandra *is* real Cassandra).
4. **GCP global VPC / global LB** change network topology assumptions baked into AWS/Azure hub-spoke designs.
5. **AI platform brands moved above the services** in 2025–26 (SageMaker platform, Microsoft Foundry, Gemini Enterprise Agent Platform): older docs referencing "SageMaker" (classic), "Azure OpenAI Service", "Azure AI Foundry", or "Vertex AI" describe components that still exist but are sold under the new umbrellas.
6. **Serverless K8s modes converged** (EKS Auto Mode / AKS Automatic / GKE Autopilot) but per-pod vs per-node billing differs — Autopilot bills pod requests; EKS Auto Mode bills EC2 + management fee.
7. **Azure licensing gravity is real:** Hybrid Benefit, M365/Power BI bundling, and GitHub/Entra defaults often decide Azure selections independent of pure service quality; AWS/GCP comparisons should account for it.

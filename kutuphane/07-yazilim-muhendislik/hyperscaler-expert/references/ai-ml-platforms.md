# AI/ML Services & Platform Developments Across AWS, Azure, and GCP — Expert Reference (2024–2026)

**Verified as of: August 28, 2026.**
Main sources: aws.amazon.com (What's New, Bedrock/EC2/SageMaker pages), azure.microsoft.com blog, cloud.google.com blog & docs, aboutamazon.com (re:Invent 2025 recap), anthropic.com, openai.com, Synergy Research Group (via press coverage), InfoQ, Constellation Research, The New Stack, CNBC/Futurum (capex), vendor pricing pages and third-party pricing trackers (Vantage, Thunder Compute, nOps, CloudZero). Where third-party pricing trackers disagreed with official pages, figures are marked as approximate. Facts are tagged with the date/timeframe they became true.

---

## 0. The Big Renames First (You Cannot Navigate 2026 Docs Without These)

| Old name | New name | When |
|---|---|---|
| Azure OpenAI Service + Azure AI Studio | **Azure AI Foundry** | Ignite, Nov 2024 |
| Azure AI Foundry | **Microsoft Foundry** | Ignite Nov 2025, formalized Jan 1, 2026 |
| Amazon SageMaker (classic) | **Amazon SageMaker AI** (the ML service) inside a broader "next-gen SageMaker" platform (Unified Studio + Lakehouse + Catalog) | re:Invent, Dec 2024 |
| Google Vertex AI | **Gemini Enterprise Agent Platform** | Announced Cloud Next 2026 (April 22, 2026); Vertex AI name removed from console by May 21, 2026. API endpoints unchanged. Model Garden, Training, Model Registry, Endpoints, Pipelines all live on as sub-features of the agent-first platform |
| Google Agentspace | Absorbed into **Gemini Enterprise** | 2025 → consolidated at Next 2026 |
| Bedrock "Agents" (classic) | Superseded in practice by **Amazon Bedrock AgentCore** | Preview July 2025, GA Oct 2025, expanded re:Invent 2025 |

---

## 1. GenAI Platforms

### 1.1 Amazon Bedrock

**Model catalog (as of mid-2026):** ~62 LLMs + embeddings + specialized models from 13 providers across 40+ regions.
- **Anthropic Claude** — flagship third-party family; current: Opus 4.x line (Opus 4.5 Nov 2025 → Opus 4.8 by mid-2026), Sonnet (Sonnet 4.5 Sep 2025 → **Sonnet 5, launched June 30, 2026**), Haiku 4.5 (Oct 2025). Claude pricing on Bedrock matches Anthropic first-party list: Opus $5/$25, Sonnet 5 $2/$10 (introductory price made permanent Aug 2026), Haiku 4.5 $1/$5 per 1M input/output tokens. Note the big 2025 repricing: Opus 4.5 (Nov 2025) cut Opus from $15/$75 to $5/$25.
- **OpenAI on AWS** — a genuine 2025–26 shift: open-weight **gpt-oss-120b/20b** arrived Aug 2025; then frontier **GPT-5.5, GPT-5.4 and Codex went GA on Bedrock June 1, 2026**; **GPT-5.6 (Sol/Terra/Luna) GA July 9, 2026**; OpenAI "Daybreak Red/Blue" cybersecurity models added Aug 11, 2026. Bedrock supports OpenAI's Responses/Chat Completions APIs alongside Converse. Cross-region inference for OpenAI models added Aug 2026.
- **Amazon Nova** (launched re:Invent Dec 2024: Micro/Lite/Pro + Canvas/Reel; Premier added Q1 2025). **Nova 2 announced at re:Invent 2025** (Dec 2025), alongside **Nova Forge** — build custom frontier models starting from Nova checkpoints, blending proprietary data into pretraining — and **Nova Act** for computer-use/browser agents. Nova Micro remains the price floor (~$0.035/1M input).
- Meta Llama 3.x/4 (Llama 4 Scout/Maverick added April 2025), Mistral (Large/Medium/Small/Codestral), Cohere (Command R/R+/A, Embed, Rerank), AI21 Jamba, Stability, DeepSeek (R1 added Jan 2025, V3.x later), Qwen, Writer, TwelveLabs (video, 2025), Luma.

**Platform capabilities:**
- **AgentCore** (preview July 2025, GA Oct 2025): modular agent runtime — Runtime (serverless, up to 8-hr sessions), Memory, Gateway (tools→MCP), Browser, Code Interpreter, Identity, Observability. Framework-agnostic (LangGraph, CrewAI, Strands Agents — AWS's own open-source agent SDK, May 2025) and model-agnostic. Consumption-priced per component (~12 billable dimensions). Extended at re:Invent 2025 with policy/evals and deeper integrations; classic "Bedrock Agents" still exists but AgentCore is the strategic path.
- **Knowledge Bases** — managed RAG (chunking, embedding, retrieval, citations); backends: OpenSearch Serverless, Aurora pgvector, Pinecone, Redis, MongoDB, Neptune GraphRAG (2025), Kendra GenAI index, and **S3 Vectors** (2025→GA Dec 2025). Re:Invent 2025 repositioned this as "Bedrock Managed Knowledge Base" tightly integrated with AgentCore, adding multimodal (image/audio/video) retrieval.
- **Guardrails** — content filters, denied topics, PII redaction, contextual grounding checks (2024), Automated Reasoning checks (preview re:Invent 2024, GA 2025 — formal-logic verification of policy compliance); priced per 1K text units; applies to any model incl. via ApplyGuardrail API.
- **Pricing modes:** On-demand per-token; **Batch at 50% of on-demand** (Aug 2024, expanded since); **Provisioned Throughput** (model units, 1- or 6-month commitments — largely legacy for older models; newer capacity assurance is via cross-region inference + service tiers); **prompt caching** (preview re:Invent 2024, **GA April 7, 2025**) — up to 90% input-token cost reduction, 85% latency reduction; cache-write premium ~25%, cache-read ~90% discount (Claude models). "Global" cross-region inference tiers (2025) trade routing flexibility for lower price/higher availability. **Custom Model Import** (Llama/Mistral weights) and fine-tuning/distillation (Model Distillation, re:Invent 2024) billed per custom-model-unit hosting.
- **Enterprise:** PrivateLink/VPC endpoints, KMS/CMK, no training on customer data, IAM, CloudTrail, cross-region inference profiles with geography-bounded ("EU-only") routing for data residency (2024–25), FedRAMP High (GovCloud).

### 1.2 Azure AI Foundry → Microsoft Foundry

**Naming:** Azure OpenAI + AI Studio merged into **Azure AI Foundry** at Ignite Nov 2024; renamed **Microsoft Foundry** at Ignite Nov 2025 / Jan 1, 2026. SDK: Foundry SDK + **Microsoft Agent Framework** (merger of Semantic Kernel + AutoGen, Oct 2025).

**Model catalog (11,000+ models):**
- **OpenAI:** exclusive first-party frontier hosting continues through the restructured OpenAI–Microsoft agreement (Oct 2025: Azure keeps Foundry exclusivity for OpenAI frontier models until AGI declaration; OpenAI committed ~$250B incremental Azure spend). Timeline: GPT-4o/o1 (2024) → GPT-4.1, o3/o4-mini (2025) → **GPT-5 family (Aug 2025)** → GPT-5.1/5.2 (late 2025) → **GPT-5.4, GPT-5.5** (H1 2026) → **GPT-5.6 family "Sol/Terra/Luna" (mid-2026)**, deployable Global/Data Zone, short- vs long-context rates, Priority Processing tiers, PTU support for Sol/Terra. Reference pricing: GPT-5.5 ~$5/$30 per 1M in/out (verified Aug 6, 2026); announced promo: GPT-5.6 Sol drops to $4/$20 Sept 1–Nov 30, 2026. Sora video models also hosted.
- **Claude on Azure — the headline 2025 announcement:** Microsoft–NVIDIA–Anthropic strategic partnership announced **Nov 18, 2025** (Anthropic committed to purchase $30B of Azure compute; Microsoft/NVIDIA investing up to $5B/$10B in Anthropic). Claude entered Foundry in preview (Nov 2025, "hosted on Anthropic") and went **GA ~June 30–July 2, 2026 "hosted on Azure"** — inference on Azure infrastructure in a US data zone, Azure AD auth, Azure billing/governance. GA models: Claude Opus 4.8 + Haiku 4.5, with **Sonnet 5 following days later at $2/$10 promo**. Caveat (InfoQ, July 2026): EU data-zone deployment not yet available at GA. Azure thus became the only cloud offering both GPT and Claude frontier models natively. Claude also powers Microsoft 365 Copilot/Copilot Studio model picker (Sept 2025).
- Others: Grok (xAI, 2025), Llama, Mistral (incl. serverless MaaS), DeepSeek R1 (Jan 2025), Phi-4 family (Microsoft SLMs, 2024–25), MAI-1/MAI-Voice (Microsoft's own frontier models, Aug 2025+), Flux, Cohere.

**Pricing modes:** Standard (pay-as-you-go per 1M tokens, Global/Data Zone/Regional tiers — regional data-zone pricing carries ~10–20% premium over Global), **Batch (50% discount)**, **Provisioned Throughput Units (PTU)** — hourly, monthly, or 1-year reservations; 2026 change: **PTU reservations are now fungible across supported Foundry models** in the same region/scope (including non-OpenAI models); GPT-5-class deployments start ~15–50 PTU minimums. Prompt caching: automatic for OpenAI models (cached input ~90% off... 50–90% depending on model/tier).

**Agents & tooling:** **Foundry Agent Service** (GA May 2025, Build) — managed agent runtime with tool use, Bing grounding, SharePoint/Fabric connectors; Ignite 2025 added **Foundry IQ** (shared knowledge/grounding layer over SharePoint, OneLake, ADLS, web — Purview-governed), **Foundry Models** router, hosted agents for any framework (Agent Framework, LangGraph, CrewAI) with no container/K8s management, one-click publish of agents to Microsoft 365/Teams, **Work IQ**, and agent identity via **Microsoft Entra Agent ID** (2025). MCP and A2A protocol support added 2025.

**Enterprise:** VNet/private endpoints, customer-managed keys, Data Zones (EU/US) introduced 2024 for residency, no-training guarantee, fine-tuning for OpenAI (SFT, DPO, RFT on o4-mini, 2025) + selected OSS models, Azure AI Content Safety (prompt shields, groundedness detection).

### 1.3 Google Vertex AI → Gemini Enterprise Agent Platform

**Models:**
- **Gemini timeline:** Gemini 1.5 Pro/Flash (2024) → **Gemini 2.0 Flash (GA Feb 2025)** → **Gemini 2.5 Pro/Flash (Next '25, GA mid-2025, "thinking" models)** → **Gemini 3 Pro (Nov 18, 2025)** + Gemini 3 Flash (Dec 2025) → **Gemini 3.1/3.5 and 3.x Flash line through 2026** (Gemini 3.1 Flash Image / 3 Pro Image GA with 4K output preview). Current API reference pricing (Aug 2026, third-party trackers): Gemini 3.1 Pro ~$2/$12 per 1M (≤200K context; long-context surcharge above), Gemini 3.5 Flash ~$1.50/$9, newest 3.7 Flash ~$0.75/$3.75 marked as introductory through Dec 31, 2026. Multimodal in/out (text, image, audio, video); ~1M–2M token contexts; Live API for realtime voice.
- **Model Garden:** 200+ models — Claude family (Anthropic has been on Vertex since 2023; Opus/Sonnet/Haiku current versions), Llama (with serverless MaaS), Mistral, AI21, Qwen, DeepSeek, Gemma 3/3n (open, 2025), Imagen 4, Veo 3/3.1 (video, 2025), Lyria (music), Chirp (speech), MedLM/SecLM verticals.
- **Agent stack:** **Agent Development Kit (ADK)** (open-source, Next '25 April 2025 — multi-agent systems in <100 lines, Python/Java), **Agent Engine** (managed runtime with sessions/memory bank, GA 2025), **Agent Garden** (samples), **A2A (Agent2Agent) protocol** (Next '25, 50+ partners; donated to Linux Foundation June 2025; upgraded 2026), **Agentspace → Gemini Enterprise** (Oct 2025, $21–30/user/mo tiers) as the employee-facing agent hub. At Next 2026 the whole platform was rebranded the Gemini Enterprise Agent Platform with agents as the top-level object.
- **Pricing modes:** per-1M-token on-demand (Global vs Regional endpoints); **Batch at 50%**; **Provisioned Throughput** — fixed-term subscription in **GSUs (Generative AI Scale Units)**, weekly/monthly/1yr terms, required for guaranteed throughput; updated PT pricing for Gemini 3+ families effective **July 1, 2026**. **Context caching**: implicit caching (automatic, 2025) + explicit CachedContent with ~75–90% discount on cached tokens plus per-hour storage; distinct from AWS/Azure in offering storage-billed explicit caches.
- **Enterprise:** VPC Service Controls, CMEK, data residency at-rest + ML-processing commitments (expanded 2024–25), Model Armor (safety filtering service, 2025), fine-tuning: supervised LoRA tuning for Gemini 2.x/3 Flash, RLHF legacy, plus full custom training on TPU/GPU.

**Provider-exclusive frontier access note (2026):** every hyperscaler now sells OpenAI *and* Anthropic models except: Google hosts Claude + Gemini (no frontier GPT); AWS hosts Claude + GPT + Nova; Azure hosts GPT + Claude + Grok (no Gemini). Multi-model is the norm — differentiation shifted to agent runtimes, governance, and silicon.

---

## 2. Classic ML Platforms

### 2.1 Amazon SageMaker (next generation)

Re:Invent 2024 restructuring (GA March 13, 2025):
- **SageMaker Unified Studio** — single IDE across data, analytics, ML, GenAI (subsumes Athena/EMR/Glue/Redshift query editing, Bedrock IDE, DataZone-style governance).
- **SageMaker Lakehouse** — Iceberg-compatible unified access over S3 data lakes + Redshift; zero-ETL connectors to SaaS apps.
- **SageMaker Catalog** — governance layer (built on DataZone tech).
- **SageMaker AI** = the original ML service (Studio classic, notebooks, training jobs, endpoints).

Core capabilities: Studio/JupyterLab + Code Editor notebooks; **Training Jobs** (managed, spot, warm pools), **HyperPod** (2023; resilient large-cluster training; 2024–25 added flexible training plans, task governance ~40% cost reduction claim, EKS support; 2025 added P6/Trainium support and managed tiered checkpointing; re:Invent 2025: **checkpointless & elastic training**); **Pipelines** (serverless DAGs), **Feature Store** (online/offline), **Model Registry**, **MLflow managed** (2024), Clarify (bias/explainability), Model Monitor, Ground Truth.
**Inference options:** real-time endpoints (single/multi-model, multi-container), **Serverless Inference**, **Asynchronous Inference** (queue, near-real-time, large payloads), **Batch Transform**; inference components for GPU fractional packing (2023–24); JumpStart for 1-click OSS model deployment; integration with Bedrock for custom model import both directions (2025).

### 2.2 Azure Machine Learning

Still the classic MLOps platform (increasingly overshadowed by Foundry for GenAI): Studio + compute instances/clusters (incl. serverless compute GA 2024), AutoML, **Designer** pipelines + Pipelines SDK v2, **managed Feature Store** (GA 2024), Model Registry with cross-workspace sharing via registries, **prompt flow** (moved to Foundry), Responsible AI dashboard.
**Inference:** Managed Online Endpoints (real-time, blue/green traffic split), Batch Endpoints, Kubernetes (Arc) endpoints, no true scale-to-zero serverless for custom models (serverless API only for catalog MaaS models). Fabric integration (OneLake datastores, 2024–25). Direction of travel: Ignite 2025 positions Foundry as the umbrella; Azure ML persists for classic training/inference.

### 2.3 Vertex AI training/prediction (now under Gemini Enterprise Agent Platform)

Custom Training (any container, GPU/TPU), **Ray on Vertex** (GA 2024), AutoML (tabular successor = tabular workflows/BQML), **Pipelines** (KFP/TFX-based, serverless), **Feature Store** (re-architected on BigQuery, GA 2024), Model Registry, Experiments/TensorBoard, **Colab Enterprise** notebooks + Workbench.
**Inference:** online prediction endpoints (incl. GPU autoscaling; Ironwood-backed serving 2026), batch prediction, private endpoints/PSC; optimized TensorRT/vLLM serving containers (2024–25); "Model as a Service" serverless for Garden models. Distinctive: tightest warehouse coupling (BigQuery ML can call Gemini directly; BQ ↔ Vertex pipelines).

**Quick comparison judgment (2026):** SageMaker = deepest raw training control + best-in-class resilient large-cluster tooling (HyperPod); Azure ML = strongest enterprise MLOps/governance tie-in to M365/Fabric ecosystems; Vertex = best integrated data→model→agent path and best first-party silicon (TPU) economics.

---

## 3. AI Accelerators & Pricing (list prices, US regions, on-demand unless noted; all figures approximate — GPU pricing moved a lot in 2026)

**Important 2026 dynamic:** AWS *raised* Capacity Block prices twice in 2026 (~15% Jan 4, ~20% July 1) on H100/H200/B200-class capacity — unprecedented direction, reflecting demand exceeding supply; meanwhile commodity H100 rental prices at neoclouds fell to $1.49–3/hr, widening the hyperscaler premium.

### AWS
| Instance | Accelerator | Price (approx.) | Notes |
|---|---|---|---|
| p5.48xlarge | 8× H100 80GB | ~$98.32/hr on-demand; **$5.19/GPU-hr** Capacity Blocks (post-July 2026 hike) | GA July 2023 |
| p5e / p5en .48xlarge | 8× H200 | CB **$5.97 / $6.87 per GPU-hr** (July 2026) | p5e late 2024, p5en re:Invent 2024 |
| p6-b200.48xlarge | 8× B200 | CB **$12.36/GPU-hr** (July 2026) | GA May 2025 |
| p6-b300 | 8× B300 | CB **$14.04/GPU-hr** | 2026 |
| p6e-gb200 UltraServers | GB200 NVL72 | Capacity Blocks/contract only | GA July 2025 |
| trn2.48xlarge | 16× Trainium2 | ~$40–50/hr region-dependent (AWS claims 30–40% better price-perf vs P5e/P5en) | GA Dec 2024; Trn2 UltraServer = 64 chips |
| **Trn3 UltraServers** | up to 144× Trainium3 (3nm) | announced re:Invent Dec 2025; rolling out 2026 | 4.4× compute vs Trn2 UltraServer; Project Rainier (Anthropic, ~500K Trainium2 chips, 2025) is the marquee deployment |

Capacity mechanisms: **ODCR** (on-demand capacity reservations), **Capacity Blocks for ML** (reserve 1–182 days of GPU/Trainium capacity up to 8 weeks ahead — the primary way to get H200/B200/GB200), EC2 UltraClusters/UltraServers. Graviton5 announced re:Invent 2025.

### Azure
| VM | Accelerator | Price (approx.) | Notes |
|---|---|---|---|
| ND96isr_H100_v5 | 8× H100 | ~$98/hr (~$12.3/GPU-hr) — priciest big-3 H100 list | GA 2023 |
| ND H200 v5 | 8× H200 | ~$110–130/hr instance (list varies by region) | GA late 2024/2025 |
| ND GB200 v6 | GB200 NVL72 racks | contract/negotiated | First cloud to deploy GB200 (Nov 2024) and **first to deploy GB300 NVL72 at scale (Oct 2025)** |
| ND MI300X v5 | 8× AMD MI300X | competitive alt | 2024 |
- Custom silicon: **Maia 100** (limited internal use; Maia 2 in development), Cobalt CPU. **Fairwater** AI datacenters (Wisconsin Sept 2025, Atlanta Nov 2025) form the "AI superfactory" WAN.
- Capacity: **On-demand Capacity Reservations** (no term commitment, billed whether used), reserved instances/savings plans; GPU access for new capacity is largely allocation/quota-gated rather than a Capacity-Blocks-style marketplace.

### GCP
| Machine | Accelerator | Price (approx.) | Notes |
|---|---|---|---|
| a3-highgpu-8g / a3-mega | 8× H100 | ~$88–98/hr instance (~$11–12.3/GPU-hr list; ~$3–3.35/GPU-hr via DWS/commit paths) | 2023–24 |
| a3-ultra | 8× H200 | ~10–15% above A3 | late 2024 |
| **a4** | 8× B200 | ~$4.28/GPU-hr floor via DWS Flex; higher on-demand | GA 2025 |
| **a4x / a4x-max** | GB200 / GB300 NVL72 | contract; median cross-cloud GB200 rate ~$16/GPU-hr (Aug 2026) | A4X GA 2025, A4X Max (GB300) late 2025 |
| TPU v5e | — | ~$1.20/chip-hr | inference/light training |
| TPU v5p | — | ~$4.20/chip-hr on-demand; $2.94 1-yr; ~$1.89 3-yr | 2024 |
| **TPU v6e Trillium** | — | ~$2.70/chip-hr on-demand; $1.89 1-yr; $1.22 3-yr; ~$1.35 DWS Flex (EU) | GA Dec 2024; 4.7× perf/chip vs v5e |
| **TPU v7 Ironwood** | — | announced Next '25 (April 2025) as first inference-optimized TPU; **GA April 22, 2026** — still no public list price as of Aug 2026 (negotiated; SemiAnalysis estimated ~$1.60/chip-hr for Anthropic's contracted capacity) | 9,216-chip pods; ~5× compute, 6× HBM vs Trillium; Anthropic contracted up to ~1M TPUs (Oct 2025) |
- Capacity: **Dynamic Workload Scheduler (DWS)** — **Flex-start** (queue for up to 7-day runs, pay only for use, big discounts) and **Calendar mode** (reserve GPU/TPU up to 90 days ahead, fixed-term; GA'd 2025); future reservations; Committed Use Discounts.

---

## 4. Applied AI Services Mapping

| Domain | AWS | Azure | GCP |
|---|---|---|---|
| **Speech (STT/TTS)** | Transcribe (streaming, Call Analytics; GenAI-improved ASR 2024) / Polly (neural + generative voices 2024) | **Azure AI Speech** (STT, neural TTS w/ HD voices 2024–25, speech translation, voice live API for agents 2025; personal voice) | Cloud Speech-to-Text (Chirp 2/3 USM models) / Text-to-Speech (Chirp 3 HD instant custom voice 2025; Gemini-TTS 2025–26) |
| **Vision** | Rekognition (faces, moderation, custom labels; face liveness) | **Azure AI Vision** (Florence-based image analysis, OCR Read, Face — gated) | Cloud Vision API + Video Intelligence; increasingly superseded by Gemini multimodal |
| **Translation** | Amazon Translate | Azure AI Translator (LLM-augmented adaptive translation 2025) | Cloud Translation (incl. adaptive/LLM translation via Gemini) |
| **Document AI** | **Textract** (OCR, forms, tables, queries); Bedrock Data Automation (2025) is the GenAI-native successor for docs/media | **Azure AI Document Intelligence** (layout, prebuilt, custom; v4 2024); Content Understanding (multimodal, 2025) | **Document AI** (parsers, custom extractor); Layout Parser for RAG; Gemini-based extraction now default path |
| **Enterprise search / RAG** | Kendra (incl. GenAI Index 2024) → largely folded into Bedrock Knowledge Bases + **Amazon Q Business**; OpenSearch (incl. serverless) as vector engine | **Azure AI Search** (hybrid + semantic ranker, integrated vectorization, agentic retrieval 2025 — the default RAG store for Foundry/Copilot) | **Vertex AI Search** (managed search+RAG; now "Search" within Gemini Enterprise; Layout-aware chunking; grounding-with-Google-Search API) |
| **Assistants (dev)** | **Amazon Q Developer** (agentic coding, /dev /doc /review agents, CLI; GitLab Duo w/ Q 2025) + **Kiro** (spec-driven agentic IDE, preview July 2025, GA re:Invent 2025; runs Claude via Bedrock) | **GitHub Copilot** (multi-model: GPT-5.x, Claude, Gemini; coding agent GA 2025; **Agent HQ** announced Oct 2025 — mission control for multiple third-party agents) | **Gemini Code Assist** (Standard/Enterprise; code customization on private repos) + **Antigravity** (agent-first IDE, launched with Gemini 3 Nov 2025; at I/O May 2026 became the individual-tier successor — individual Code Assist VS Code extension retired June 18, 2026) + Jules (async coding agent, 2025) |
| **Assistants (business)** | **Amazon Q Business** ($3–20/user/mo; connectors, Q Apps, QuickSight/Q in QuickSight — QuickSight rebranded "Quick Suite" 2025) | **Microsoft 365 Copilot** ($30/user/mo; Copilot Studio for custom agents/agent flows; Copilot Tuning 2025; agent marketplace) | **Gemini for Workspace** (folded INTO Workspace Business/Enterprise SKUs Jan 2025 — no more separate add-on) + **Gemini Enterprise** (agent hub, Oct 2025, $21–30/user/mo) |

---

## 5. Vector / RAG Infrastructure Per Cloud

**AWS:**
- **OpenSearch Service + OpenSearch Serverless** vector engine (quantization, binary vectors 2024–25; serverless min OCU floor removed progressively; "OpenSearch Serverless NextGen" with scale-to-zero GA May 28, 2026).
- **S3 Vectors** — announced preview July 2025, **GA Dec 2, 2025**: vector buckets/indexes natively in S3, up to 2B vectors/index at GA (40× preview), ~90% cheaper than dedicated vector DBs for cold/warm RAG; integrated with Bedrock KB and OpenSearch (tiering); expanded to 17 more regions March 2026. This is the "storage-first RAG" story of 2025–26.
- **pgvector** on RDS PostgreSQL & **Aurora** (Aurora PostgreSQL Limitless, Serverless v2 scale-to-zero; pgvector w/ HNSW; Aurora DSQL — re:Invent 2024, GA May 2025 — no pgvector yet at GA).
- **MemoryDB** vector search (GA 2024, single-digit-ms, highest-recall in-memory option); DocumentDB, Neptune Analytics vector; DynamoDB has no native vectors (pair w/ S3 Vectors/OpenSearch).

**Azure:**
- **Azure AI Search** — the flagship: HNSW + exhaustive KNN, hybrid RRF, semantic reranker, integrated vectorization pipelines, quantization/MRL compression (2024–25), agentic retrieval API (2025).
- **Cosmos DB** — native vector indexing (DiskANN) GA 2024–25 across NoSQL API; MongoDB vCore vector search; the default operational-DB RAG pattern for Copilot-style apps (ChatGPT itself runs on Cosmos DB).
- Azure Database for PostgreSQL Flexible Server: pgvector + DiskANN extension (2024–25), azure_ai extension for in-database embedding calls; SQL Server 2025/Azure SQL native VECTOR type (preview 2025).

**GCP:**
- **AlloyDB AI** — pgvector + **ScaNN index** (Google's ANN tech, GA 2024; claims ~4× faster than HNSW pgvector), natural-language-to-SQL, AI query engine (2025); available on-prem/other clouds via AlloyDB Omni.
- **Vertex AI Vector Search** (ex-Matching Engine) — massive-scale ANN serving, hybrid dense+sparse (2024), now a component of Gemini Enterprise Agent Platform RAG Engine (2025).
- **BigQuery** — VECTOR_SEARCH + IVF/TreeAH vector indexes (GA 2024–25), ML.GENERATE_EMBEDDING in-warehouse; BigQuery becomes a first-class RAG store for analytical corpora.
- Also: Firestore & Memorystore for Redis vector search (2024), Spanner vector search.

---

## 6. "What Changed Recently" — Major Platform Timeline 2024–2026

### AWS
- **re:Invent Dec 2024:** next-gen SageMaker (Unified Studio/Lakehouse/Catalog); **Amazon Nova** model family; Trn2 GA + Trn2 UltraServers + Trainium3 teaser; Bedrock: prompt caching preview, Intelligent Prompt Routing, Model Distillation, Automated Reasoning checks, multi-agent collaboration; Aurora DSQL; S3 Tables (Iceberg) & S3 Metadata; Q Developer agents.
- **2025:** Strands Agents SDK (May); **AgentCore** preview July → GA Oct; **Kiro** preview (July); S3 Vectors preview (July); gpt-oss on Bedrock (Aug); Project Rainier live (~500K Trainium2, Oct); **$38B AWS–OpenAI compute deal (Nov 3, 2025)** — OpenAI running on AWS/NVIDIA capacity, ending Azure exclusivity for compute.
- **re:Invent Dec 2025:** **Nova 2 + Nova Forge + Nova Act; Trainium3/Trn3 UltraServers GA; Graviton5; AI Factories (on-prem/sovereign AI infra); Kiro GA; AgentCore expansion; DynamoDB/S3 price cuts** paired with GPU capacity-block **price increases** (Jan 4 + July 1, 2026, ~15% then ~20%).
- **2026:** OpenAI frontier models GA on Bedrock (June 1: GPT-5.5/5.4/Codex; July 9: GPT-5.6 Sol/Terra/Luna; Aug: Daybreak security models + cross-region inference v2); OpenSearch Serverless NextGen GA (May 28); S3 Vectors region expansion (Mar).
- **Deprecations:** 2024 "silent purge": **CodeCommit, Cloud9**, QLDB, Honeycode, Braket direct, S3 Select, SimpleDB (new-customer closure ~July 25, 2024). 2025: 12+ more sunset — Timestream for LiveAnalytics, Pinpoint (EOL Oct 2026), IoT Analytics/Events, Panorama, SimSpace Weaver, Private 5G, Inspector Classic, Connect Voice ID, DMS Fleet Advisor, IQ; **AWS Proton** EOL Oct 7, 2026. AWS now maintains an official product-lifecycle page — check it; 30+ items listed for 2025.

### Microsoft
- **Build/Ignite 2024:** Azure AI Foundry launch (Nov); Copilot Studio autonomous agents; Fabric everywhere; GB200 first deployment; Phi-4.
- **2025:** Foundry Agent Service GA (Build, May); MAI-1 first in-house frontier models (Aug); Claude in M365 Copilot (Sept); Fairwater Wisconsin (Sept); restructured OpenAI deal — 27% stake, frontier exclusivity for Foundry, $250B Azure commitment (Oct 28); **Anthropic partnership + Claude on Foundry preview (Nov 18)**; **Ignite Nov 2025:** Microsoft Foundry rename, Foundry IQ/Work IQ, Agent 365 (agent fleet management), Fairwater Atlanta "AI superfactory", first at-scale GB300 NVL72 cluster, Maia 2 roadmap.
- **2026:** Foundry rename effective Jan 1; **Claude GA on Azure infra (late June/early July)**; GPT-5.6 on Foundry with PTU fungibility across models; EU data-zone gap for Claude flagged in July.
- **Deprecations:** classic storage accounts + Azure Service Manager (ASM/classic IaaS) retired **Aug 31, 2024**; classic administrator roles fully retired by **May 2026** (auto-migration to RBAC began Dec 2025); many "Cognitive Services"-era names retired into Azure AI services (2024); Azure ML classic CLI v1 phased out.

### Google
- **Next '24 → 2024:** Gemini 1.5 era, Trillium announced; Gemini for Workspace consolidation begins.
- **Next '25 (April 2025):** **Ironwood TPU v7 announced (first inference-first TPU)**; **A2A protocol**; **ADK**; Agent Engine; Agentspace push; Gemini 2.5.
- **2025:** Gemini 2.5 GA (June); Agentspace → **Gemini Enterprise** (Oct); **Anthropic TPU deal — up to ~1M TPUs / >1GW (Oct)**; **Gemini 3 Pro (Nov 18) + Antigravity IDE**; Trillium GA (Dec 2024) scaling through 2025.
- **2026:** **Ironwood GA April 22 at Cloud Next 2026**, alongside the **Vertex AI → Gemini Enterprise Agent Platform rebrand** (console rename completed May 21); Workspace Studio; Antigravity 2.0 (I/O May 2026) replacing individual Code Assist (June 18); Gemini 3.x Flash cadence with introductory pricing through end-2026.
- **Deprecations:** Cloud Deployment Manager EOL Dec 31, 2025 (→ Infrastructure Manager); Firebase Dynamic Links shut down Aug 25, 2025; Gemini 1.0/1.5 API retirements (2025), **Gemini 2.0 Flash/Flash-Lite fully discontinued (2026)**; partner-model churn (e.g., Claude 3.5 Sonnet shutdown Feb 19, 2026); Container Registry fully replaced by Artifact Registry (2025).

### Market share & money (as of latest data, Aug 2026)
- **Synergy Research, Q1 2026:** AWS ~30%, Microsoft Azure ~25%, Google Cloud ~13% of global cloud infrastructure services; big three ≈ 68% combined. Trend since 2024: AWS drifting down from ~31–33%, Azure up from ~24, GCP up from ~11–12. Q2 2026 market growth reported by Synergy as fastest in ~8 years (roughly 25–43% YoY depending on segment definition — AI-driven reacceleration; treat exact Q2 splits as provisional).
- **Capex 2026 guidance (Q4'25/Q1'26 earnings):** Amazon ~$200B (vs ~$125B 2025), Microsoft ~$110–120B+, Alphabet ~$175–185B, Meta $125–145B → combined big-4 ≈ **$700–725B for 2026**, up ~75% YoY; street projects >$1T combined in 2027. Anthropic ($30B Azure + Google TPU deal + Project Rainier) and OpenAI ($250B Azure + $38B AWS + Oracle/Stargate) commitments mean every frontier lab is now multi-cloud.

---

## 7. Data + AI Governance

- **AWS — Amazon DataZone → SageMaker Catalog:** DataZone (GA 2023) provided domains, data products, business glossary, subscription/approval workflows over Glue/Redshift/Lake Formation. From re:Invent 2024 its capabilities were embedded as **SageMaker Catalog** inside SageMaker Unified Studio (GA Mar 2025) — governance of data *and* AI assets (models, prompts, feature groups) with fine-grained access via Lake Formation, lineage, and Q-powered semantic search. DataZone continues for existing users; new work targets the SageMaker platform.
- **Microsoft Purview:** unified SaaS governance across Azure + Fabric/OneLake + AWS S3 + on-prem; **Unified Catalog GA 2025** (data products, glossaries, curated domains, access workflows); Data Loss Prevention/sensitivity labels extended to AI: **Purview for AI / DSPM for AI** (2024–25) governs Copilot and Foundry agent interactions (prompt/response auditing, oversharing detection); Ignite 2025: Purview governs Foundry IQ knowledge grounding. Strongest compliance/e-discovery story of the three.
- **GCP — Dataplex Universal Catalog:** Dataplex + Data Catalog merged into **Dataplex Universal Catalog** (2024–25): automatic discovery/harvesting across BigQuery, GCS, Spanner, AlloyDB, plus **automated cataloging of Vertex/Gemini-platform models and datasets**; data quality scans, lineage (incl. into Vertex pipelines), governance rules; BigQuery universal catalog with Iceberg REST catalog support (2025). Positioned as metadata backbone for "agent-ready data" at Next 2026.
- Cross-cloud reality: lineage still breaks at cloud boundaries; each native catalog is strongest in-ecosystem; third-party catalogs (Atlan, Collibra, Unity Catalog OSS) remain the multi-cloud glue.

---

## 8. Cheat-Sheet: Equivalence Table (Aug 2026)

| Capability | AWS | Azure | GCP |
|---|---|---|---|
| GenAI model platform | Bedrock | Microsoft Foundry | Gemini Enterprise Agent Platform (ex-Vertex AI) |
| Agent runtime | Bedrock AgentCore | Foundry Agent Service (+ Agent Framework) | Agent Engine + ADK |
| Managed RAG | Bedrock Knowledge Bases | Foundry IQ / Azure AI Search | RAG Engine / Vertex AI Search |
| Safety layer | Bedrock Guardrails | Azure AI Content Safety | Model Armor / safety filters |
| Throughput reservation | Provisioned Throughput (model units) | PTUs (fungible across models, 2026) | Provisioned Throughput (GSUs) |
| Caching | Prompt caching (GA Apr 2025) | Prompt caching (automatic) | Implicit + explicit context caching |
| First-party frontier model | Nova / Nova 2 (+Forge) | (OpenAI partnership; MAI-1) | Gemini 3.x |
| Custom training silicon | Trainium2/3 | Maia (limited) | TPU v5e/v5p/Trillium/Ironwood |
| GPU capacity access | Capacity Blocks for ML / ODCR | Capacity Reservations + quota | DWS Flex-start / Calendar mode |
| Classic ML | SageMaker AI | Azure ML | Vertex training/prediction (renamed) |
| Data+AI catalog | SageMaker Catalog (DataZone) | Purview Unified Catalog | Dataplex Universal Catalog |
| Coding assistant | Q Developer + Kiro | GitHub Copilot (+Agent HQ) | Gemini Code Assist / Antigravity |
| Business assistant | Q Business / Quick Suite | Microsoft 365 Copilot | Gemini Enterprise / Workspace |

---

### Deep dive: LLM context/prompt caching

For a full, dedicated treatment of Gemini implicit/explicit context caching (mechanics, pricing tables, breakeven formulas) and the cross-cloud comparison against Bedrock prompt caching, Azure/Foundry prompt caching, and Anthropic first-party caching, see **[llm-context-caching.md](llm-context-caching.md)** (verified 2026-08-28).

### Reliability notes for the reader
- Pricing above is US-region list; GPU/accelerator figures especially are volatile in 2026 (AWS raised, commodity market fell) — always re-quote before committing.
- Post-cutoff model-version minutiae (e.g., exact GPT-5.6 sub-variant naming, Gemini 3.7 Flash rates, Opus 4.8 dates) are drawn from multiple concurring Aug-2026 web sources but from secondary trackers in some cases; official pricing pages (aws.amazon.com/bedrock/pricing, azure.microsoft.com pricing, cloud.google.com pricing) are authoritative.
- Q2 2026 market-share splits were not yet fully published by Synergy at verification time; Q1 2026 figures (30/25/13) are the latest firm datapoints.

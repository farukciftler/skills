# LLM Context Caching on Google Cloud (Vertex AI / Gemini API) — Deep Reference, with Bedrock / Azure / Anthropic Comparison

**Verified as of: 2026-08-28** (all pricing/limits re-checked against live official docs on this date)

**Main sources:**
- Vertex AI context caching overview: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview (note: Vertex AI generative docs now render under the "Gemini Enterprise Agent Platform" branding; URLs redirect from `cloud.google.com/vertex-ai/...`)
- Create / use / update cache: `.../context-cache/context-cache-create`, `.../context-cache-use`, `.../context-cache-update`
- Vertex generative AI pricing: https://docs.cloud.google.com/vertex-ai/generative-ai/pricing
- Gemini API caching + pricing: https://ai.google.dev/gemini-api/docs/caching , https://ai.google.dev/gemini-api/docs/pricing
- Implicit caching launch: https://developers.googleblog.com/en/gemini-2-5-models-now-support-implicit-caching/ (2025-05-08)
- AWS Bedrock prompt caching: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html
- Azure OpenAI / Foundry prompt caching: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/prompt-caching (doc dated 2026-08-11)
- Anthropic prompt caching: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching
- Data governance / zero data retention: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/data-governance
- Agent Engine Memory Bank: https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/memory-bank ; GKE Inference Gateway KV-cache-aware routing: Google Cloud Next '25 announcement + llm-d/Gateway API Inference Extension (see §5)

---

## 1. Vertex AI / Gemini context caching mechanics

Google offers **two caching layers**; both surface hits in the same response field: `usageMetadata.cachedContentTokenCount` (Vertex/GenAI SDK) or `usage.total_cached_tokens` (Gemini API Interactions API). Cache-hit ratio = `cachedContentTokenCount / promptTokenCount`.

### 1.1 Implicit caching (automatic)

- **On by default for all Google Cloud projects** and all Gemini API paid projects. Nothing to enable; savings are passed through automatically when a request's prefix matches a recent request's prefix.
- **Discount: 90% off the standard input-token price** on cached tokens (Gemini 2.5 and newer). History: explicit caching shipped May 2024 at a 75% discount; implicit caching launched **2025-05-08** for Gemini 2.5 (initially ~75%, minimums then 1,024 for 2.5 Flash / 2,048 for 2.5 Pro — partly a response to developer complaints about surprise explicit-cache bills on 2.5 Pro). The discount has since been standardized at **90%** across 2.5+ on both Vertex and the Gemini API.
- **No storage fee** for implicit caching. You pay standard input price on the first (miss) request; hits bill the matched prefix at the cached rate.
- **Supported models (Vertex, Aug 2026):** Gemini 3.7 Flash, 3.6 Flash, 3.5 Flash, 3.5 Flash-Lite, 3.1 Pro (preview), 3.1 Flash-Lite, 3.1 Flash-Lite Image ("Nano Banana 2 Lite"), 3.1 Flash Image, 3 Pro Image, 3 Flash (preview), 2.5 Pro, 2.5 Flash, 2.5 Flash-Lite — plus **open MaaS models** (e.g., Gemma 4 26B has a published "Cache Hit" price).
- **Minimum prefix for an implicit hit** (Vertex limits table): Gemini **3 family: 4,096 tokens**; Gemini 3.0 Flash Preview and 3.1 Pro Preview (implicit only): **6,144 tokens**; Gemini **2 family: 2,048 tokens**. The Gemini API docs list 2,048 for 2.5 Flash/Pro and 4,096 for 3.x Flash models — treat the Vertex table as authoritative on Vertex.
- **Hit conditions:** exact byte-identical common prefix, same model (and model version), requests close together in time. Google's stated guidance: "place large and common contents at the beginning of your prompt" and "send requests with a similar prefix in a short amount of time". No published TTL — implicit cache lifetime is best-effort (empirically minutes), unlike explicit caches.
- Works with both stateful (`previous_interaction_id`) and stateless calls on the Interactions API; **explicit caching is NOT supported on the Interactions API** — only implicit.

### 1.2 Explicit caching (`CachedContent` API)

- **Lifecycle:** `caches.create` → returns `projects/{n}/locations/{loc}/cachedContents/{id}` with `usageMetadata` (per-modality token counts) → reference via `cached_content` in `generateContent` → `caches.get/list` → `caches.update` (**only `ttl` or `expire_time` can be updated**) → `caches.delete`.
- **TTL: default 60 minutes.** Minimum lifetime 1 minute; **no maximum** — you can set `expire_time` days out (an example in the docs uses 7 days). Expired caches are garbage-collected; recreate to reuse.
- **What can be cached:** `contents`, `system_instruction`, `tools`, `tool_config`. Content may be **any MIME type Gemini supports — text, PDF, images, audio, video** — as inline blob/text up to **10 MB**, or via `gs://` Cloud Storage URI above that (multiple files allowed). Do not mutate GCS objects backing a live cache — it silently invalidates the cached content.
- **Hard rule:** when a request references a cache, you **must not** re-specify `system_instruction`, `tools`, or `tool_config` in that request — they live in the cache.
- **Minimum cache size:** Gemini 3 family **4,096 tokens**; Gemini 2 family **2,048 tokens** (Gemini API historically 1,024 for 2.5 Flash / 2,048–4,096 for 2.5 Pro; current unified floors above).
- **Supported models (Vertex):** Gemini 3.7/3.6/3.5 Flash, 3.5 Flash-Lite, 3.1 Pro (preview), 3.1 Flash-Lite, 3 Flash (preview), 2.5 Pro/Flash/Flash-Lite, plus `gemini-flash-latest` / `gemini-flash-lite-latest` aliases and **fine-tuned Gemini models** (dedicated doc page). A cache is pinned to one model/version — model changes or retirement orphan the cache.
- **Discount: 90%** off input price on cache-referenced tokens for Gemini 2.5+; **75% for Gemini 2.0 models** (the old rate survives there only).
- **Explicit and implicit interact:** creating/using an explicit cache can additionally trigger implicit caching beyond the declared contents. For zero data retention you must disable implicit caching *and* avoid explicit caches (see §3 governance), and set `store=false` on the Interactions API (defaults to `true`).

---

## 2. Pricing (USD per 1M tokens; global endpoint; verified 2026-08-28)

Cache **writes** (creation) bill at the **standard input rate — no write premium** (unlike Anthropic/Bedrock). Explicit caches additionally pay **storage per token-hour**; implicit has **no storage fee**. Cached-token discount applies on both Standard and **Priority** tiers; Batch/Flex is a flat 50% off input/output (3.7/3.6 Flash also list Flex/Batch cached prices; 3.1 Pro Flex/Batch shows cache N/A).

| Model | Input (≤200K / >200K) | Output | Cached input (≤200K / >200K) | Cache storage /1M tok-hr |
|---|---|---|---|---|
| Gemini 3.1 Pro Preview | $2.00 / $4.00 | $12.00 / $18.00 | **$0.20 / $0.40** (90% off) | **$4.50** |
| Gemini 3.7 Flash * | $0.75 (promo) → $1.50 | $3.75 → $7.50 | **$0.075 → $0.15** | $0.50 (promo, Gemini API) → $1.00 |
| Gemini 3.6 Flash * | $0.75 → $1.50 | $3.75 → $7.50 | **$0.075 → $0.15** | $0.50 → $1.00 |
| Gemini 3.5 Flash | $1.50 | $9.00 | **$0.15** | $1.00 |
| Gemini 3.5 Flash-Lite | $0.30 | $2.50 | 90% off | $1.00 |
| Gemini 2.5 Pro | $1.25 / $2.50 | $10.00 / $15.00 | **$0.125 / $0.25** | $4.50 |
| Gemini 2.5 Flash | $0.30 (audio $1.00) | $2.50 | **$0.03** (audio $0.10) | $1.00 |
| Gemini 2.5 Flash-Lite | $0.10 (audio $0.30) | $0.40 | **$0.01** (audio $0.03) | $1.00 |
| Gemma 4 26B (MaaS) | $0.15 | $0.60 | **$0.015** (cache hit) | n/a (implicit only) |

\* 3.7/3.6 Flash promo pricing runs **through 2026-12-31**; doubles 2027-01-01. Non-global (regional) Vertex endpoints price ~10% higher across the board (e.g., 3.7 Flash regional input $0.825, cached $0.0825). Vertex's storage table prices per token-hour ($0.0000045 Pro-class incl. Gemini 3 Pro & 3.1 Pro; $0.000001 Flash-class incl. 2.0 models) = $4.50 / $1.00 per 1M token-hours. Note the **long-context tier applies to cached reads too** (a >200K-token cache on 3.1 Pro reads at $0.40, not $0.20). Priority tier (3.1 Pro: $3.60/$7.20 input) keeps the 90% cached ratio ($0.36/$0.72).

**Provisioned Throughput (GSU):** implicit and explicit caching are **supported with PT in Preview**; caches work **across traffic types** — a cache created under PT traffic also serves pay-as-you-go traffic and vice versa. PT is capacity-based billing, so per-token cache discounts don't reduce a PT bill directly; consult the PT guide for how cached tokens count against throughput burndown. **Batch API:** on Gemini, Batch/Flex pricing is its own 50% tier (3.7/3.6 Flash list Flex/Batch cached rates of $0.0375 promo).

---

## 3. Best practices and gotchas

**Prompt architecture**
- Put the big stable block **first**: system instruction → tool definitions → corpus/documents → few-shot examples → *then* per-request variable content. Implicit caching matches longest common **prefix**; one changed byte upstream (timestamp, session ID, shuffled tool order) kills every hit downstream. Keep conversation history append-only.
- Serialize deterministically: stable JSON key order for tools, no dynamic dates in the system prompt, identical media bytes (same file, same detail settings).
- Concentrate traffic: identical prefixes sent close together in time hit more; the **global endpoint** is supported for caching and is where most Gemini 3 pricing lives — but **CMEK is not supported on the global endpoint**, and explicit caches are **stored in the region of creation** (regional data residency for the cache itself). Context caching is unavailable in `australia-southeast1`.

**Explicit vs implicit — breakeven economics**
- Both give the same 90% read discount, so explicit caching buys you a *guarantee* (plus TTL control and >10-request-per-minute fan-out consistency), at the cost of storage.
- Per cached token: savings per read = 0.9 × P_in; storage cost = S per token-hour. **Explicit is strictly profitable when reads per cache-hour H > S / (0.9 × P_in)** (versus no caching at all):
  - Gemini 3.1 Pro: 4.50 / (0.9×2.00) ≈ **2.5 reads/hour**
  - Gemini 2.5 Pro: 4.50 / 1.125 = **4.0 reads/hour**
  - Gemini 2.5 Flash: 1.00 / 0.27 ≈ **3.7 reads/hour**
  - Gemini 3.5 Flash: 1.00 / 1.35 ≈ **0.74 reads/hour**
  - 3.7/3.6 Flash (promo): 0.50 / 0.675 ≈ **0.74 reads/hour**
- Versus *relying on implicit*: explicit beats implicit when `S × hours < (expected_reads × 0.9 × P_in × C) × (1 − p_implicit_hit)` — i.e., pay storage to eliminate implicit-miss risk. Rule of thumb: bursty, high-fan-out, or SLA-priced workloads → explicit; steady conversational traffic → let implicit work.
- Extend TTL with `caches.update` (ttl or absolute `expire_time`) instead of recreating — updating avoids re-paying the creation input tokens; you only accrue more storage. Cache creation is a full prefill (standard input price + latency), so pre-warm before traffic spikes.

**Interplay and operational gotchas**
- Using an explicit cache forbids re-sending `system_instruction` / `tools` / `tool_config` — version your cache when any of these change (there is no in-place content update; only TTL is mutable).
- Long-context tier: pushing a cache past 200K tokens on Pro models doubles both input and cached rates.
- **CMEK** supported for explicit caches (pass `kms_key_name` at creation) — but not on the global endpoint. **VPC Service Controls** fully supported (include the backing GCS bucket in your perimeter). **Access Transparency** supported.
- **Zero data retention:** implicit caching must be disabled (see "Enable and disable caching" in the Vertex docs) and explicit caches avoided; Interactions API stores state unless `store=false`.
- **Monitoring:** track `cachedContentTokenCount` vs `promptTokenCount` per response; billing exports break out cached-token SKUs; on the Gemini API use `usage.total_cached_tokens`. Alert on hit-rate collapse after deploys — the usual cause is an innocent prompt-prefix edit.
- Limits recap: min 2,048/4,096 (6,144 for 3.0 Flash Preview / 3.1 Pro Preview implicit) tokens; 10 MB inline cap; 1-minute min TTL; no max TTL; standard per-region request quotas apply to the cachedContents API.

---

## 4. Cross-cloud comparison (verified Aug 2026)

| Dimension | **Gemini implicit** (Vertex/Gemini API) | **Gemini explicit** (CachedContent) | **AWS Bedrock prompt caching** | **Azure OpenAI / Foundry** | **Anthropic 1P (Claude API)** |
|---|---|---|---|---|---|
| Activation | Automatic, on by default | Manual resource (create/use/delete) | `cachePoint` checkpoints (Converse/InvokeModel); GPT-5.6: `prompt_cache_breakpoint`; Nova also auto-caches | Automatic; GPT-5.6+: optional explicit breakpoints + `prompt_cache_key` | `cache_control` breakpoints (explicit) or top-level automatic mode |
| Breakpoints | n/a (prefix match) | 1 cache object per request | **Up to 4**; auto lookback ~20 blocks (Claude) | Up to 4 new writes/request; reads consider last 50 breakpoints | **Up to 4**; read lookback ~20 blocks |
| Min tokens | 2,048 (Gemini 2.x) / 4,096 (3.x); 6,144 for 3.0 Flash Prev & 3.1 Pro Prev | 2,048 / 4,096 | Per model: **512** (Opus 5, Fable 5), **1,024** (Sonnet 5/4.6/4.5, Opus 4.8, GPT-5.6), **4,096** (Haiku 4.5, Opus 4.5–4.7) | **1,024**; hits in 128-token increments pre-GPT-5.6 | 512–4,096 by model (512 Opus 5/Fable 5; 1,024 Sonnet 5; 4,096 Haiku 4.5) |
| TTL | Unpublished, best-effort (minutes) | **Default 60 min; 1 min–unbounded**, updatable | **5 min default, refresh-on-hit; 1-hour opt-in** (Claude 4.5+/5); GPT-5.6: 30-min min | In-memory ~5–10 min (≤1 h); **extended 24 h** (gpt-4.1→5.5); GPT-5.6+: 30-min min TTL | **5 min (default) / 1 h**; refresh-on-hit free for 5-min |
| Write cost | Standard input (no premium) | Standard input + **storage $1.00–$4.50 /1M tok-hr** | Claude: **1.25x** (5m) / **2x** (1h); Nova & GPT-5.5-and-earlier: no premium; GPT-5.6: 1.25x | Pre-GPT-5.6: free; **GPT-5.6+: writes charged** | **1.25x** (5m) / **2x** (1h) |
| Read discount | **90%** off input | **90%** (2.5+); 75% (2.0) | ~**90%** (Claude read ≈0.1x; GPT-5.6 read 90% off) | "Discounted" on Standard (≈90% on GPT-5-family, 50% on older 4o-era; **up to 100% on Provisioned/PTU**) | **0.1x** (90% off) |
| Cacheable content | Text/PDF/image/audio/video prefix | Contents + system + **tools/tool_config**; any Gemini MIME; GCS-backed >10 MB | `system`, `messages`, `tools` (order tools→system→messages; cumulative minimum) | Messages, images, tool defs, structured-output schema | Tools, system, messages, images/documents, tool results, thinking (implicitly) |
| Hit reporting | `cachedContentTokenCount` / `total_cached_tokens` | same | `cacheReadInputTokens`, `cacheWriteInputTokens`, `cacheDetails` | `prompt_tokens_details.cached_tokens` (+ `cache_write_tokens` on 5.6) | `cache_read_input_tokens`, `cache_creation_input_tokens` |
| Rate-limit effect | — | — | Cache hits not deducted from quota (Claude 1h note; GPT: cached tokens exempt from TPM) | Cached reads reduce effective load | Cache hits favorable to ITPM (varies by plan) |
| Isolation | Project/org | Project resource; CMEK, VPC-SC | Account-level; works with cross-region inference (may raise writes) | Not shared across subscriptions; extended cache stays in data-zone/region boundary | Workspace-level (1P API); org-level on Bedrock/GCP |
| Batch | Batch is separate 50% tier | PT-compatible (Preview) | **Not supported** with batch inference | PTU-M: caching yes, breakpoints no | Works alongside Batch API (50%) — caching discounts stack on 1P |

**When each wins architecturally**
- **RAG / document Q&A over a fixed corpus:** Gemini **explicit** caching is the only design with an indefinitely-lived, storage-priced server-side cache — pin a 500K-token corpus for days at $4.50/1M tok-hr (3.1 Pro) and pay $0.20/M per read. Bedrock/Anthropic/Azure caches evaporate in 5–60 min.
- **Agent loops / coding assistants (many calls, minutes apart, growing transcript):** Anthropic-style breakpoints (1P or Bedrock) win — incremental checkpoints along the conversation, refresh-on-hit, tools+system+messages hierarchy; Gemini implicit also performs well here since turns are append-only prefixes. Azure GPT-5.6 breakpoints + `prompt_cache_key` now match this pattern closely.
- **High-QPS shared system prompt (chatbots, classification farms):** any automatic scheme (Gemini implicit, Azure automatic, GPT-5.5 Bedrock, Nova) — zero code, no storage. Watch Azure's ~15 req/min-per-prefix-per-key cache-miss note; shard `prompt_cache_key`.
- **Compliance-heavy workloads:** Vertex explicit (CMEK + VPC-SC + regional residency + Access Transparency) is uniquely enterprise-featured; Azure offers data-zone boundaries for extended cache; Bedrock/Anthropic offer no key-managed cache.
- **Cost-floor shopping:** Gemini has no write premium ever; Anthropic/Bedrock Claude charge 1.25–2x to write — Claude caching only nets out with ≥1 read per write (break-even ~1.1 reads for 5m tier).

---

## 5. Adjacent GCP caching for LLM serving (brief)

- **GKE Inference Gateway (announced Next '25, now GA):** KV-cache- and **prefix-aware routing** for self-hosted models. Built on the Kubernetes **Gateway API Inference Extension** with the **llm-d Endpoint Picker (EPP)**: requests sharing a prefix are routed to the vLLM/SGLang replica that already holds the matching KV cache; fallback routes on `vllm:kv_cache_usage_perc` (least-loaded cache). Solves the multi-replica problem where round-robin destroys prefix-cache locality. Open source; also see the Rust **vLLM Router** (Dec 2025) for prefill/decode-aware balancing.
- **vLLM automatic prefix caching on GKE / Cloud Run GPU:** `--enable-prefix-caching` gives per-replica RadixAttention-style KV reuse for shared system prompts; combine with the Inference Gateway for fleet-level locality. Cloud Run GPU (L4) suits bursty low-QPS serving; scale-to-zero wipes KV caches — cold starts recompute prefill.
- **Vertex AI Agent Engine Sessions + Memory Bank (GA):** application-layer state, not token caching — Sessions persist in-conversation events; Memory Bank asynchronously extracts durable user facts and injects only relevant memories per turn (semantic retrieval). Priced at **$0.25 per 1,000 events/memories stored (effective 2026-01-28)**. Complements context caching: Memory Bank shrinks the prompt; context caching cheapens what remains.
- **Cloud CDN / Apigee:** classic edge caching is largely irrelevant for non-deterministic LLM responses; it applies only to exact-repeat responses, static assets, and embeddings endpoints. Apigee offers response-cache and **semantic-cache** policies in front of Vertex for FAQ-style traffic — a different (answer-level) cache tier above token-level caching.

---

### Bottom line
On Google Cloud, treat **implicit caching as the default free tier** (90% off, zero config, no storage, best-effort) and **explicit CachedContent as a paid SLA on that discount** — worth it above roughly 2.5–4 reads per cache-hour on Pro-class models (≈0.75 on current promo Flash), or whenever you need guaranteed hits, multi-hour/day TTLs, CMEK/VPC-SC, or tool/system-instruction pinning. Gemini is the only major platform with **no cache-write premium and unbounded TTL**; Bedrock/Anthropic trade write premiums for fine-grained checkpoint control in agent loops; Azure has converged on the breakpoint model with GPT-5.6 while keeping a unique 24-hour extended retention tier for the 5.5-and-earlier fleet.

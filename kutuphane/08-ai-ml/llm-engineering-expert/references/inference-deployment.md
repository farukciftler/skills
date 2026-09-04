# Inference & Deployment (verified July 2026)

Contents: 1. Engine map · 2. Core serving techniques · 3. Disaggregated
serving · 4. Quantization · 5. VRAM math · 6. Hardware tiers · 7. Local
deployment recipes · 8. Cost math API vs self-host

---

## 1. Engine map

- **vLLM** — production default. PagedAttention (paged KV memory),
  continuous batching, prefix caching, speculative decoding, day-one support
  for exotic architectures (shipped DeepSeek V4's heterogeneous hybrid KV
  cache). OpenAI-compatible API.
- **SGLang** — vLLM's peer; RadixAttention (radix-tree prefix caching —
  excellent for shared system prompts / agent loops), strong structured
  output, first-class prefill/decode disaggregation. Often wins on
  multi-turn/agentic workloads.
- **TensorRT-LLM** — NVIDIA-compiled kernels; peak throughput on NVIDIA
  when you can afford the build complexity.
- **NVIDIA Dynamo** — orchestration layer *above* vLLM/SGLang/TRT-LLM:
  routing, autoscaling, KV-transfer coordination for datacenter-scale.
- **llm-d** — Kubernetes-native disaggregated inference (Red Hat/AWS
  backing); AWS offers it managed.
- **llama.cpp / Ollama / LM Studio** — CPU+GPU GGUF inference for
  local/edge; Ollama = easiest ops (model pull, API, swap). llama.cpp
  server for more control.
- **MLX** — Apple-silicon native; best tokens/sec on Macs.
- Gateways (LiteLLM, OpenRouter, Portkey, Vercel/Cloudflare AI gateways):
  multi-provider routing, fallback, caching, budgets — assume one in any
  serious multi-model product.

Rule: local dev/small team → Ollama; production self-host → vLLM (or SGLang
for agent-heavy); scale-out → add Dynamo/llm-d layer.

## 2. Core serving techniques (know the vocabulary)

- **Prefill vs decode**: prefill = whole prompt, one pass, compute-bound;
  decode = token-by-token, memory-bandwidth-bound (reads whole KV cache per
  token). All serving optimization derives from this asymmetry.
- **Continuous batching**: admit/retire requests every iteration — the
  baseline throughput win over static batching.
- **Chunked prefill**: split long prompts into chunks interleaved with
  decodes — bounds tail latency (TPOT) for other users. First knob to turn
  for long prompts.
- **Prefix caching**: reuse KV of shared prefixes (system prompts, few-shot
  blocks, agent scaffolds). Order prompt = static parts first, variable
  last. Massive win for agents; SGLang's radix tree automates it.
- **Speculative decoding**: small draft proposes k tokens, target verifies
  in one pass. EAGLE-3-class heads or native MTP heads (Qwen3-Next,
  Nemotron 3 Super) give 1.5–2.5x decode speedup, output distribution
  unchanged.
- **KV cache quantization** (FP8/INT4 KV) and offload (LMCache-style
  CPU/SSD tiers) for long-context memory pressure.

## 3. Disaggregated serving (P/D split)

Prefill and decode fight for the same GPU (compute-bound vs memory-bound);
colocating them causes TPOT tail-latency spikes under load. Disaggregation
runs prefill and decode on separate GPU pools with KV transfer between them
(NIXL, LMCache, NCCL connectors). Supported first-class in SGLang
(`--disaggregation-mode`), vLLM (KV-connector config), TRT-LLM/Dynamo, llm-d.

When to bother: sustained 8k+ prompts at high concurrency AND chunked prefill
+ prefix caching already maxed. Below that scale it's complexity without
payoff. At scale it's how frontier-style serving hits 2x+ goodput; also lets
you size pools independently (few prefill nodes, many decode nodes).

## 4. Quantization

| Format | Bits | Where | Notes |
|---|---|---|---|
| BF16/FP16 | 16 | training/reference | 2 GB per B params |
| FP8 | 8 | Hopper+ serving | ~lossless, throughput win, vLLM/TRT native |
| INT8 / Q8 | 8 | broad | ~lossless |
| GGUF Q4_K_M | ~4.8 | llama.cpp/Ollama | the local-deployment sweet spot |
| AWQ / GPTQ | 4 | vLLM GPU serving | activation-aware (AWQ) usually edges GPTQ |
| NVFP4 / MXFP4 | 4 | Blackwell-era | models now *ship* native FP4 (gpt-oss MXFP4, Mistral 3 & DeepSeek V4 FP4) — quantization moving into training |
| ≤3-bit | 2–3 | last resort | visible degradation; prefer a smaller model at 4-bit |

Heuristics: 8-bit ≈ free; 4-bit ≈ 1–3% benchmark cost, fine for almost all
products; below 4-bit choose a smaller model instead. Quantize KV cache
separately when context-bound. Always eval quantized vs full on YOUR task
before shipping.

## 5. VRAM math (show your work when sizing)

**Weights** = params × bytes/param (see table). +10–20% runtime overhead
(activations, CUDA graphs, engine buffers).

**KV cache** per token = `2 × n_layers × n_kv_heads × head_dim ×
bytes_per_value` (×2 is K and V).

Worked example — Llama-3-70B (80 layers, GQA-8, head_dim 128, BF16):
2×80×8×128×2 ≈ 0.33 MB/token → 128k-token context ≈ **42 GB just for KV** of
one sequence. This is why MLA/SWA/compressed-attention exist and why KV
quantization matters: architecture changes swing this number 10–50x
(DeepSeek V4 ≈ 2% of that baseline).

Quick sizing table (weights only, 4-bit):

| Model class | 4-bit VRAM | Runs on |
|---|---|---|
| 7–8B | ~5 GB | any 8GB+ GPU, laptops |
| 14B | ~9 GB | 12–16GB GPUs |
| 30–32B | ~19 GB | 24GB (4090/5090-class), 32GB Macs |
| 70B | ~40–43 GB | 48GB (2×24GB, RTX 6000-class), 64GB Macs |
| gpt-oss-120B (MoE, MXFP4) | ~61–65 GB | single 80GB (H100/A100) or 96GB workstation card |
| 400–700B MoE | multi-GPU node(s) | 8×80GB+ territory |

MoE caveat: memory = TOTAL params; speed = ACTIVE params. Expert CPU-offload
(llama.cpp, KTransformers-style) lets big MoEs run on small VRAM + lots of
RAM at reduced speed — viable for local, not for serving.

## 6. Hardware tiers (mid-2026)

- Consumer GPU: RTX 4090 24GB / 5090 32GB — up to 32B dense at 4-bit.
- Apple silicon: unified memory (64–192GB+) makes Macs surprisingly good
  single-user 70B–120B boxes via MLX/llama.cpp; bandwidth caps tokens/sec.
- Workstation: RTX 6000-class 96GB — 70B at 8-bit or 120B-MoE at 4-bit.
- DC single node: H100/H200/B200 80–192GB ×8 — flagship MoE territory.
- Small-box appliances (DGX Spark-class) fill the "team local server" niche.
- Non-NVIDIA (AMD MI300+, TPU, Trainium) viable via vLLM/ROCm but check
  kernel maturity for exotic architectures first.

## 7. Local deployment recipes (common ask)

- Single user / dev box: Ollama + Q4_K_M model matched to VRAM from §5 table;
  Open WebUI if a UI is wanted.
- Team server (privacy-driven): vLLM + AWQ/FP8 model on 1–2 GPUs behind an
  OpenAI-compatible endpoint; add LiteLLM gateway for auth/quotas/logging;
  prefix caching ON (shared system prompts).
- Structured output: use the engine's JSON-schema/grammar mode (vLLM guided
  decoding, SGLang) — don't parse free text.
- Always load-test with realistic prompt/output lengths; published
  tokens/sec never match your workload.

## 8. Cost math: API vs self-host

Compute both sides, show the numbers:

- API side: monthly tokens × per-token price (input and output separately;
  cached-input discounts are large — 50–90% — and change the math for
  agent workloads).
- Self-host side: (GPU rental $/hr × hours, or hardware amortized over
  ~3 yrs + power) ÷ utilization. **Utilization is the whole game**: a GPU
  busy 10% of the time makes API ~10x cheaper than it looks on paper.
- Open-weight self-hosting typically wins at sustained high volume, hard
  data-residency, or when serving many requests over shared cached prefixes;
  API wins for spiky/low volume and frontier-quality needs.
- Hybrid router (cheap local/open model default, frontier API escalation) is
  the standard production answer, not either/or.

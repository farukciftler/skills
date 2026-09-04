# Modern LLM Architectures (verified July 2026)

Contents: 1. Baseline recipe · 2. Attention variants · 3. Long-context &
compressed attention · 4. Linear/hybrid (post-transformer) · 5. MoE design ·
6. Normalization & positional encodings · 7. Multi-token prediction ·
8. Model landscape table · 9. Design heuristics

---

## 1. The baseline recipe (what "a standard LLM" means in 2026)

Decoder-only transformer with: RoPE positional encoding, RMSNorm (pre-norm),
SwiGLU feed-forward, Grouped-Query Attention, BF16 training (increasingly FP8),
128k-token vocabulary range. Almost every open model is this template plus 2–4
efficiency modifications. GPT-2 (2019) → today is refinement, not revolution —
the differentiators are attention efficiency, MoE sparsity, and training
pipeline, not the block structure.

## 2. Attention variants (the main axis of differentiation)

Ordered by KV-cache cost, highest → lowest:

- **MHA** (multi-head): every head has its own K/V. Rare now (OLMo 2 7B kept
  it for transparency/simplicity).
- **GQA** (grouped-query): several query heads share one K/V head. The
  workhorse standard (Llama, Qwen3, Gemma, Mistral, gpt-oss). KV cache shrinks
  by `heads/kv_groups` (typically 4–8x vs MHA). Ablations: modeling quality ≈
  MHA.
- **MLA** (multi-head latent, DeepSeek V2→V3→R1; adopted by Kimi K2, GLM-5,
  Mistral 3): K/V projected into a low-rank latent vector; only the latent is
  cached, up-projected at use. Bigger KV savings than GQA *and* slightly
  better quality than MHA in DeepSeek's ablations. Costs one extra matmul.
- **Sliding-window attention (SWA)**: attention restricted to a local window;
  interleaved with a few global layers. Gemma 3 uses 5:1 local:global with a
  1024 window; gpt-oss alternates every other layer; Xiaomi MiMo-V2-Flash
  pushes 5:1 with a 128-token window. KV for local layers is O(window), not
  O(sequence). Quality impact ≈ nil per ablations, but you keep some global
  layers for retrieval ability.
- **Attention sinks**: learned per-head bias logits appended to attention
  scores (gpt-oss) or always-attended prefix tokens — stabilizes long-context
  and streaming attention.
- **Gated attention**: sigmoid output gate on the attention result (+
  zero-centered QK-norm, partial RoPE) — stability tweaks on GQA (Qwen3-Next,
  Arcee Trinity).
- **Sparse attention (DSA)**: DeepSeek V3.2's "lightning indexer" scores all
  prior tokens cheaply and selects top-k for real attention. Near-linear cost,
  small quality trade.

## 3. Long-context & compressed attention (the 2026 frontier)

Driver: agent workloads. Agents accumulate tool outputs, logs, and reasoning
traces; 128k–1M contexts make KV memory and per-token FLOPs the binding
constraint, and 2026 architectures attack the KV cache directly.

- **DeepSeek V4** (Apr 2026; V4-Pro and V4-Flash, MIT license, 1M context) —
  the reference design. Hybrid of:
  - **CSA** (Compressed Sparse Attention): compress KV ~4x along sequence
    (softmax-gated pooling of 8-token groups, stride 4), then a small FP4
    "lightning indexer" picks top-k compressed blocks per query (DSA idea run
    over already-compressed blocks).
  - **HCA** (Heavily Compressed Attention): ~128x compression, dense attention
    over the tiny compressed cache.
  - Plus pure SWA layers for local detail, native FP4 MoE weights, and
    Manifold-Constrained Hyper-Connections (mHC) replacing plain residuals.
  - Net effect vs V3.2 at 1M tokens: Pro ≈ 27% of per-token FLOPs and ~10% of
    KV memory; Flash ≈ 10% FLOPs / 7% KV. Versus a bf16 GQA-8 baseline, V4's
    cache is roughly ~2% the size. This is why 1M-token *usable* context (not
    just advertised) became practical.
- **Gemma 4** (2026): cross-layer **KV sharing** (layers reuse another
  layer's KV) + per-layer embeddings (PLE, streamed from CPU/SSD — from
  Gemma 3n) to cut device memory.
- Heterogeneous KV caches (different layers with different cache shapes and
  eviction rules) broke PagedAttention's assumptions; serving frameworks now
  ship hybrid KV managers (see inference-deployment.md).
- **YaRN**: RoPE rescaling used to extend context post-hoc (Qwen3 32k→131k,
  Olmo 3 global layers only). Cheap, works, mild quality tax at extremes.

## 4. Linear & hybrid architectures (transformer ± SSM)

Full attention is O(n²); linear-attention/SSM blocks are O(n) with a
fixed-size recurrent state (no KV growth). 2025–26 pattern: **hybrids** —
mostly-linear blocks with a few full-attention layers retained for precise
retrieval.

- **Qwen3-Next 80B-A3B** (Sep 2025): 3:1 Gated DeltaNet : gated full
  attention. Native 262k context. Base of Qwen3-Coder-Next (Feb 2026), which
  matches models with 10x its active params on SWE-Bench-class coding.
- **Kimi Linear** (Oct 2025): Kimi Delta Attention = Gated DeltaNet with
  *channel-wise* (not scalar) decay gates; full-attention layers use MLA with
  NoPE. Beats the MLA-only baseline on long-context at equal speed.
- **Mamba-2 hybrids**: NVIDIA Nemotron 3 (Nano 30B-A3B, Super 120B-A12B —
  Mamba-2 + MoE blocks, attention in only a small subset of layers), IBM
  Granite 4.0, Falcon-H — highest tokens/sec per param class.
- **Cautionary tale**: MiniMax went M1 (lightning/linear attention, 456B) →
  M2 (back to *full* attention) because linear attention underperformed on
  reasoning and multi-turn/agentic tasks in production. Linear ≠ free; the
  retrieval precision of full attention still matters. Hybrid ratios (3:1,
  or attention-only-in-few-layers) are the current compromise.

## 5. MoE design space

MoE replaces the FFN with N expert FFNs + a router; only k experts run per
token. Total params = capacity/knowledge; active params = speed/FLOPs.
Dominant for every flagship since DeepSeek V3 (671B total / 37B active).

Key knobs and current consensus:

- **Many small experts > few large** (DeepSeekMoE finding): V3 has 256
  experts, 8 routed + 1 shared active. Counter-examples exist for throughput
  reasons: gpt-oss (32 large, 4 active), Mistral 3 Large (halved expert count,
  doubled size vs DeepSeek — better serving throughput).
- **Shared expert** (always-on): DeepSeek/GLM/Qwen3-Next yes, Qwen3/gpt-oss/
  MiniMax-M2 no. Rationale for yes: common patterns learned once, routed
  experts specialize. Qwen team: no significant gain, complicates inference —
  genuinely unsettled.
- **Dense first layers**: 1–3 dense blocks before MoE layers (DeepSeek V3,
  GLM-4.5/5) — stabilizes early training since router noise hurts low-level
  feature learning.
- **Sparsity ratio trend**: down. Qwen3-235B activates ~9.4% of params;
  MiniMax-M2 ~4.4%; Trinity Large 400B-A13B ~3%. Extreme sparsity + good
  routing is the current capacity-per-FLOP frontier.
- **Latent experts** (Nemotron 3 Super): down-project 4096→1024, run experts
  in latent space, up-project back — cheaper experts at small quality cost.
- Balance losses / aux-loss-free routing (DeepSeek bias method) prevent
  expert collapse.

## 6. Normalization & positional encodings

- Placement flavors: pre-norm (GPT-2 lineage, default), OLMo-2-style
  post-norm-inside-residual (stability), Gemma-3 "sandwich" (norm before and
  after each block), Trinity depth-scaled sandwich (second norm gain init
  ~1/√L). All work; sandwich variants trade a little compute for stability.
- **QK-Norm**: RMSNorm on queries/keys pre-RoPE (OLMo 2, Gemma 3, Qwen3,
  MiniMax-M2 per-head variant) — now near-standard for training stability.
- **RoPE** default; **partial RoPE** (rotate only first half of head dims —
  MiniMax) helps length extrapolation; **NoPE** (no positional signal at all;
  causal mask suffices) used in a fraction of layers (SmolLM3 every 4th,
  Kimi Linear MLA layers, Trinity global layers) — better length
  generalization at scale-still-being-proven.

## 7. Multi-token prediction (MTP)

Extra heads predict t+1..t+k during training (richer signal, better
convergence). Used by DeepSeek V3/V3.2/V4, Qwen3-Next, GLM, MiMo-V2,
Nemotron 3 Super. Second life at inference: the MTP head doubles as a native
draft model for **speculative decoding** (Qwen3-Next, Nemotron 3 Super) — no
separate draft model, 1.5–2.5x decode speedups typical.

## 8. Model landscape snapshot (mid-2026 — verify before citing)

Open-weight flagships and their architectural identity:

| Model | Size (total/active) | Signature |
|---|---|---|
| DeepSeek V4 Pro / Flash | MoE, ~V3-scale/– | CSA+HCA hybrid attention, 1M ctx, FP4 native, mHC |
| DeepSeek V3.2 | 671B/37B | MLA + DSA sparse attention |
| Kimi K2 / K2.5 / K2.6 (Moonshot) | 1T/32B | DeepSeek-V3 template scaled up; Muon optimizer; K2 Thinking 256k ctx |
| GLM-5 (z.AI) | 744B/40B | MLA + DeepSeek sparse attention; agent-optimized |
| Qwen3 family | 0.6B–235B dense+MoE | GQA+QK-norm baseline; Next/Coder-Next = DeltaNet hybrid 80B-A3B; Qwen3.5 122B-A10B |
| MiniMax M2 / M2.5 | 230B/10B | Full attention (retreat from linear), per-head QK-norm, partial RoPE; M2.5 near-frontier coding |
| gpt-oss 20B/120B (OpenAI) | MoE, 3.6B/5.1B active | SWA every other layer, attention sinks, MXFP4 weights, wide-not-deep |
| Llama 4 (Meta) | MoE (Maverick 400B/17B) | GQA, alternating dense/MoE, very long ctx focus |
| Mistral 3 / Ministral 3 | 675B/41B + 3/8/14B dense | DeepSeek-V3 architecture with coarser experts; NVFP4; multimodal |
| Nemotron 3 (NVIDIA) | Nano 30B-A3B, Super 120B-A12B | Mamba-2+MoE hybrid, latent experts, MTP spec-decode; open data+code |
| Gemma 3 / 4 (Google) | 1–27B+ | SWA 5:1, sandwich norm; Gemma 4 adds KV sharing + PLE |
| Xiaomi MiMo-V2-Flash | 309B/15B | SWA window=128 (most aggressive), MTP; V3.2-class quality at half size |
| Arcee Trinity Large | 400B/13B | SWA 3:1 + NoPE global + gated attention + depth-scaled sandwich norm |
| Olmo 3 (AI2) | 7B/32B dense | Fully open (data, code, checkpoints); post-norm; SWA |

Closed frontier (names/versions churn quarterly — always verify): OpenAI
GPT-5.x line, Anthropic Claude (Opus 4.x, Fable/Mythos 5), Google Gemini 3.x.
Open-weight has closed the coding gap to within a few points of frontier;
frontier still leads on hardest reasoning, computer use, and ecosystem.

## 9. Design heuristics (for "how would you build X" questions)

- Width vs depth at fixed params: wider → faster inference (parallelism),
  deeper → more sequential capacity but harder to train. Evidence mildly
  favors wider (Gemma 2 ablation).
- Choosing attention: ≤32k ctx and simplicity → GQA. KV-bound serving → MLA.
  Long-doc/agent workloads → SWA-hybrid or compressed (CSA/HCA-style).
  Extreme throughput, tolerable retrieval loss → Mamba/DeltaNet hybrid with
  a few full-attention layers. Never ship pure-linear for agentic reasoning
  (MiniMax lesson).
- MoE if you can afford total-param memory and want capacity per FLOP; dense
  if you need simple fine-tuning/deployment on modest hardware.
- Everything above is composable — modern flagships are exactly such stacks
  (e.g., MoE + MLA + sparse attention + MTP + FP8/FP4).

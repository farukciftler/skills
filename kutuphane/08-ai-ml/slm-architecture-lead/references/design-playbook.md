# SLM design playbook — from deployment envelope to config

Contents: [0. Envelope first] [1. Parameter budget math] [2. Depth vs width]
[3. Attention layout decision] [4. KV-cache math] [5. Vocabulary & embeddings]
[6. Context strategy] [7. Stability kit] [8. MoE / PLE / MatFormer]
[9. Table-stakes components] [10. Config review checklist]

---

## 0. Envelope first — never size a model before these are pinned

1. Target hardware + available RAM/DRAM for the model (phone NPU? laptop GPU?
   single 24 GB card? CPU-only server?), and its memory bandwidth.
2. Latency goals: prefill tok/s (long-context ingest) and decode tok/s at
   batch=1, plus time-to-first-token if interactive.
3. Context length actually needed at serve time (not aspirationally).
4. Languages (tokenizer fertility!), modalities, tool calling, thinking mode.
5. Training budget (GPU/TPU-hours or $) and data you can actually get.
6. Serving precision (this feeds QAT planning — see training-recipes.md).

The envelope decides everything else. E2B-with-PLE and 26B-A4B exist in the
same family because a phone's DRAM+flash hierarchy and a 64 GB workstation are
different machines.

## 1. Parameter budget math (SwiGLU decoder)

- Embeddings: V·d if tied (count once), 2·V·d if untied.
- Attention per layer: Q proj d·(n_q·h) + O proj (n_q·h)·d + K,V projs
  2·d·(n_kv·h)  →  2·d·n_q·h + 2·d·n_kv·h.
- FFN per layer (SwiGLU): 3·d·d_ff  (gate + up + down).
- Norms/rotaries negligible.

Worked anchor — Qwen3-4B (d=2560, L=36, n_q=32, n_kv=8, h=128, d_ff=9728,
V=151,936 tied):
- embed 151,936·2560 = 0.389B
- attn/layer = 2·2560·4096 + 2·2560·1024 = 26.2M
- ffn/layer = 3·2560·9728 = 74.7M
- total ≈ 0.389B + 36·100.9M ≈ **4.02B** ✓

Use the same arithmetic in reverse to hit a target size: pick d and L from the
depth-width section, set d_ff ≈ 2.7–4×d (SwiGLU), then solve V and tie/untie to
land the budget. Show this arithmetic in answers — it is the fastest credibility
check on any proposed config.

Rules of thumb for the split at small scale: embeddings 8–30% (rising as the
model shrinks), attention ~20–25% of core, FFN ~70–75% of core. If someone's
1B config has untied 256k embeddings, half their model is a lookup table —
flag it.

## 2. Depth vs width

- Fixed param budget, quality: deeper-narrower wins at ≤2B (MobileLLM). Shipped
  aspect ratios d/L in the class: Gemma 3 1B ≈ 44, Qwen3-0.6B ≈ 37, Qwen3-4B ≈
  71, Qwen3-8B ≈ 114, Gemma 3 4B ≈ 75. Target **d/L ≈ 30–90** for sub-5B; go
  wider only when decode latency on the target chip demands fewer serial layers.
- Latency: every layer is a serial dependency; NPUs and CPUs feel depth more
  than GPUs. If decode tok/s misses on the target device, trade depth for width
  at constant params before shrinking the model.
- head_dim 128 (Qwen-style) or 256 (Gemma-style); n_q·h = d is conventional but
  not mandatory (Qwen3-4B uses 32·128=4096 > d=2560 — over-provisioned heads).

## 3. Attention layout decision (the #1 design lever)

Three proven templates; pick by retrieval-fidelity vs long-context-throughput
vs ecosystem support:

| Template | Recipe | Buys | Costs | Ship examples |
|---|---|---|---|---|
| SWA-hybrid | 4–5 local (window 512–1024) : 1 global; global last layer; dual RoPE 10k/1M; optional K=V in global; optional KV-share across layers | Exact attention semantics everywhere; tiny KV (Gemma 4 E4B: +0.14 GB int8 @32k); best kernel support (plain attention kernels) | Global layers still O(n²) prefill; window tuning matters for retrieval | Gemma 3/4 |
| Linear-hybrid | 3 Gated DeltaNet : 1 gated full attention; partial RoPE; sigmoid output gate | Near-constant state at long ctx; ~40% memory cut @32k and it widens with length; fast long-ctx decode | Needs GDN kernels (vLLM ≥0.17, recent llama.cpp); linear layers weaker at exact long-range recall — the 1-in-4 full layers carry retrieval | Qwen3.5/3.6 |
| Mamba-hybrid | ~9 Mamba-2 : 1 attention, often NoPE | Extreme throughput, tiny state | Furthest from standard tooling; fine-tune ecosystem thinner | Granite 4.x, Nemotron Nano 2, Falcon-H1 |

Decision rules:
- Long-document / agent-loop product with modest exact-retrieval needs →
  linear- or Mamba-hybrid.
- Retrieval-heavy (RAG citations, needle tasks) or maximum ecosystem
  compatibility → SWA-hybrid.
- Never all-full-attention in a new sub-10B design without a stated reason
  (e.g. ≤4k context appliance).
- Keep ≥1 global/full layer per 4–6, and make the **last layer global** (Gemma 4
  practice) so the LM head sees whole-context state.

## 4. KV-cache math (do this in every sizing answer)

Plain GQA: KV bytes/token = 2 · L · n_kv · h · bytes_per_elem.
- Qwen3-4B bf16: 2·36·8·128·2 = 144 KB/token → 4.7 GB @32k, 18.9 GB @128k
  (this is why it shipped 32k native; int8 KV halves it).
- Qwen3-8B bf16: same 144 KB/token (identical L·n_kv·h) — an 8B whose KV equals
  a 4B's; KV is set by layout, not size.

Layout adjustments:
- Local layers: replace context length with window length in their term.
- Shared-KV layers: count only the layers that own a cache.
- K=V trick: halves the global-layer cache (stores one tensor).
- Linear/GDN/Mamba layers: O(1) state per layer (a few MB), not per-token.

Contrast to quote: at 32k int8, Qwen3-4B ≈ 2.4 GB vs Gemma 4 E4B ≈ 0.14 GB —
~17x from layout alone. On an 8 GB phone that is the whole ballgame.

## 5. Vocabulary & embeddings

- Big vocab (150–262k) buys: lower fertility (fewer tokens per word) for
  non-English — for Turkish, agglutinative morphology makes this dramatic; a
  262k multilingual vocab can cut Turkish token counts ~25–40% vs a 32k
  English-centric one → directly faster and cheaper inference, longer effective
  context. Cost: V·d params + a fat softmax.
- Always evaluate a tokenizer by measuring **fertility (tokens/word or
  tokens/byte) on the actual target corpus** — including the user's language
  mix — before committing.
- Tie embeddings ≤4B (Qwen3 does; Gemma effectively must). Untie only when the
  budget is roomy and output-representation quality measurably gains.
- Softmax cost tricks if V is huge and the device is weak: Gemma 4's drafter
  replaces the d×262k projection with top-k over token clusters (d×4096).
- Keep digits split, whitespace preserved, byte fallback on — boring, standard,
  and the source of silent quality bugs when missing.

## 6. Context strategy

Standard 2026 path: pretrain bulk @4–8k → mid-train long-context stage (tens to
hundreds of B tokens) with RoPE base ABF (10k → 1M) → optional inference-time
YaRN/DCA for 2–4x more. Native targets now: 128–262k. Position options per
layer type: full RoPE on local/linear layers, p-RoPE (prune low frequencies,
Gemma 4 p=0.25) or partial RoPE on global layers, NoPE on a fraction of layers
(SmolLM3: every 4th). Verify long-ctx with RULER/needle-style evals at the
*deployed* quantization — KV quant degrades retrieval first.

## 7. Stability kit (defaults; deviate knowingly)

Pre+post RMSNorm around each block; QK-norm; no QKV bias; SwiGLU; zero-init or
small-init on residual out-projections; z-loss or logit regularization if
training long; bf16 weights with fp32 master; watch for fp16-inference range —
Gemma 4 adds a per-block scalar scale specifically to keep activations in fp16
range on device.

## 8. MoE / PLE / MatFormer — matching the memory hierarchy

- **Small-active MoE (A1B–A4B)**: total params must fit in RAM; only active
  params set speed. Right when the box has RAM but weak compute (laptops,
  mini-PCs, batch servers). Wrong for DRAM-starved phones. Examples: Gemma 4
  26B-A4B, Qwen3.x A3B, LFM2-8B-A1B.
- **PLE (per-layer embeddings)**: push lookup-only parameters to flash and
  stream them; E2B holds 5B stored / 2.3B in DRAM. Right for phones with fast
  flash. It is a *lookup* budget — it deepens lexical knowledge, not reasoning.
- **MatFormer nesting**: train once, ship multiple sizes (E4B contains E2B);
  attractive when one training run must serve several device tiers.
- Dense remains the right answer when fine-tuning ecosystem breadth or a single
  simple artifact matters most.

## 9. Table stakes for a serious 2026 release

Thinking mode (toggleable, ideally with budget control), native tool-calling
tokens/format, 128k+ context, MTP/speculative drafter, first-party QAT
checkpoints, multimodal story (even if "later"), and a clean license. Plan
these into the architecture, not the roadmap.

## 10. Config review checklist (rank findings by impact)

1. KV bytes/token computed? Layout justified vs the context target?
2. Embedding share of params; tied? Vocab matched to language mix with a
   measured fertility number?
3. d/L aspect in 30–90 (or a stated latency reason)?
4. n_kv 4–8; head_dim 128/256; QK-norm present; pre+post norm?
5. Native context + extension plan explicit (bases, YaRN)? Last layer global?
6. Serving precision decided and a QAT plan attached?
7. Token budget ≥ ~1000 tokens/param unless there is a distillation teacher
   (then less is fine — see training-recipes.md)?
8. Drafter/MTP head planned? Thinking + tool format tokens reserved in vocab?
9. For MoE: total-fits-in-RAM check on the actual target; expert count vs
   router stability at small scale?
10. Eval plan includes long-context at deployed quant, target-language evals,
    and on-device latency measured, not projected?

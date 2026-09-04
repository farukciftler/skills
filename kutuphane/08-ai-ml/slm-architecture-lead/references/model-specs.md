# Model specs and design rationale (verified late July 2026)

Contents: [1. Gemma lineage] [2. Qwen lineage] [3. Peer SLMs worth stealing from]
[4. Convergence table 2024→2026] [5. Sourcing rules]

Numbers below come from public tech reports and HF configs. Values marked (~) are
approximate or reconstructed; re-verify from the HF `config.json` before any
load-bearing use (exact intermediate sizes and head counts occasionally differ
between checkpoint revisions).

---

## 1. Gemma lineage (Google DeepMind)

### Gemma 2 (Jun 2024) — 2B / 9B / 27B
- Interleaved local(4096):global attention 1:1, logit soft-capping (attn 50,
  final 30), pre+post RMSNorm, GQA. 256k-class vocab.
- 2B and 9B pretrained with **knowledge distillation** from a larger teacher —
  the start of Gemma's "small sizes are distilled" doctrine. 27B from scratch.
- Lesson that survived: interleaving local/global attention. Lesson that died:
  soft-capping (incompatible with fast attention kernels; replaced by QK-norm).

### Gemma 3 (Mar 2025) — 1B / 4B / 12B / 27B (+ 270M, Aug 2025)
- Attention: **5:1 local:global**, sliding window **1024**, QK-norm replaces
  soft-capping. RoPE base 1M on global layers, 10k on local; 128k context via
  positional-scaling on global layers (1B stays 32k).
- Vocab **262,144** (Gemini SentencePiece, split digits, byte fallback). Vision:
  ~400M SigLIP encoder (frozen) at 896², Pan & Scan cropping, 4B/12B/27B only.
- Hyperparameters (HF configs):

| Model | Layers | d_model | Q/KV heads | head_dim | d_ff | Tokens | Notes |
|---|---|---|---|---|---|---|---|
| 270M | 12~ | 640 | 4/1 | 256 | 2048~ | 6T | 170M embed + ~100M core; a fine-tuning substrate |
| 1B | 26 | 1152 | 4/1 | 256 | 6912 | 2T | ~302M (30%) of params are embeddings |
| 4B | 34 | 2560 | 8/4 | 256 | 10240 | 4T | the reference "phone-plus/laptop" size |
| 12B | 48 | 3840 | 16/8 | 256 | 15360 | 12T | |
| 27B | 62 | 5376 | 32/16 | 128 | 21504 | 14T | |

- All sizes pretrained with distillation from a larger teacher. QAT int4
  checkpoints released (≈3x memory cut at near-bf16 quality) — normalized the
  expectation that open SLMs ship QAT variants.

### Gemma 3n (May–Jun 2025) — E2B / E4B ("effective" params)
- On-device specials: **Per-Layer Embeddings (PLE)** — a second, per-layer token
  embedding table that can live in flash and be streamed, so ~5B/8B stored
  params run in a ~2B/4B DRAM footprint. **MatFormer**: E2B is a nested
  sub-model of E4B (Mix-n-Match intermediate sizes possible). KV-cache sharing,
  activation sparsity, 680M USM audio encoder, MobileNet-V5 vision. 32k context.
- This is the branch Gemma 4's edge models grew from.

### Gemma 4 (Apr 2026) — E2B / E4B / 12B / 26B-A4B / 31B — Apache 2.0
Source: Gemma 4 Technical Report (arXiv 2607.02770).
- Family: E2B (2.3B effective / 5B total, PLE), E4B (4.5B eff / 8B total, PLE),
  12B (unified encoder-free multimodal), 26B-A4B (MoE, ~3.8B active), 31B dense.
  All natively multimodal (text+image; audio on E2B/E4B/12B), thinking mode,
  256k-class context, 262k vocab (same Gemini tokenizer), Apache 2.0.
- Parameter breakdown (from Table 1 of the report):

| Model | Audio enc | Vision enc | Embedder | Core ("einsums") | MTP drafter |
|---|---|---|---|---|---|
| E2B | 305M | 150M | 400M + 2,340M PLE | 1,870M | 76M |
| E4B | 305M | 150M | 670M + 2,820M PLE | 3,940M | 77M |
| 12B | — (encoder-free) | — | 1,000M | 10,890M | 400M |
| 26B-A4B | — | 550M | 740M | 24,500M total / 2,800M active | 430M |
| 31B | — | 550M | 1,410M | 29,290M | 500M |

- Attention/positional stack (the part to study): local:global **4:1 on E2B,
  5:1 elsewhere**; sliding window 512 on small dense, 1024 on larger; the final
  layer is always global. In global layers, **values = keys** (the V projection
  is removed; except E2B/E4B). **p-RoPE with p=0.25** on global layers (a
  quarter of the rotary frequencies pruned), plain RoPE on local; RoPE base
  1M global / 10k local. **KV-cache sharing**: 20 of 35 layers (E2B) and 18 of
  42 layers (E4B) reuse earlier layers' KV. Net effect: global KV footprint
  down ~37.5%, and int8 KV at 32k costs only +0.05 GB (E2B) / +0.14 GB (E4B) /
  +0.28 GB (12B and 26B-A4B) / +1.10 GB (31B).
- Memory (text-only, GB): E2B 4.6 bf16 → 0.8 mobile-QAT; E4B 9.0 → 2.3;
  12B 24 → 7.65 (Q4_0); 26B-A4B 52 total → 16.2; 31B 64 → 19.2.
- QAT: two shipped formats — "mobile" (per-channel int2/int4 weights + int8
  activations) and Q4_0 blockwise. Encoders are QAT'd too: 150M vision W8A8
  halves forward memory (400→200 MB) and cuts on-device latency 44%; audio
  encoder weights {2,4,8}-bit by layer cluster, on-disk 390→87 MB vs 3n.
- **MTP drafter**: a 76–500M autoregressive head for speculative decoding —
  4-layer transformer (3 local + 1 global), model dim 256 (E2B/E4B) or 1024
  (26B/31B), fed the main model's last-layer activations + token embeddings and
  cross-attending to the main model's KV cache, so no drafter prefill and any
  draft length. On E2B/E4B the drafter's vocab projection is replaced by top-k
  over token clusters (d×262k → d×4096) at similar acceptance rate.
- 12B "unified/encoder-free": raw 48×48×3 image patches through a single 35M
  matmul (+2D coordinate embeddings + LayerNorm) instead of a 550M ViT; raw
  16 kHz audio in 40 ms chunks (640-dim) projected straight into the embedding
  space. Competitive ASR/translation with zero dedicated encoders.
- Chat format changed: turn tokens (`<|turn>` / end-of-turn), a thinking toggle
  token, a thought channel, and dedicated tool-declaration/tool-call tokens; PT
  checkpoints end generation with `<eos>`, IT with the end-of-turn token —
  fine-tunes must append the matching terminator.
- Calibration anchors (thinking mode): E2B ≈ Gemma 3 27B quality at ~10x fewer
  params (MMLU-Pro 60.0, GPQA-D 43.4, LiveCodeBench 44.0); E4B: MMLU-Pro 69.4,
  GPQA-D 58.6, AIME'26 42.5; 31B: MMLU-Pro 85.2, Arena Elo 1451 (#1 dense open
  model as of Jun 2026).

### Gemma satellites (fine-tuning substrates and specials)
FunctionGemma 270M (tool calling), EmbeddingGemma 308M, VaultGemma 1B
(differential privacy), TranslateGemma 4B/12B/27B, MedGemma / MedGemma 1.5 4B,
T5Gemma v2 (enc-dec), Gemma Scope 2 (interpretability, for Gemma 3). Post-launch
Gemma 4 additions: "12B Unified" refresh and MTP drafters for all sizes.

---

## 2. Qwen lineage (Alibaba)

### Qwen2.5 (Sep 2024) — 0.5B…72B
- Classic dense GQA transformer, QKV bias, BBPE vocab ~151.7k, 18T tokens,
  128k via YaRN + Dual Chunk Attention (7B+). Embeddings tied ≤3B.
- Its 0.5B/1.5B/3B established Qwen as the default multilingual small-model
  fine-tuning base of 2024–25.

### Qwen3 (Apr 2025) — dense 0.6B–32B, MoE 30B-A3B / 235B-A22B
- Architecture deltas vs 2.5: **QK-norm, no QKV bias**, otherwise SwiGLU +
  RMSNorm + RoPE. Vocab 151,936-class. Tied embeddings up to 4B.
- Dense hyperparameters (HF configs):

| Model | Layers | d_model | Q/KV | head_dim | d_ff | Tied | Native ctx |
|---|---|---|---|---|---|---|---|
| 0.6B | 28 | 1024 | 16/8 | 128 | 3072 | yes | 32k |
| 1.7B | 28 | 2048 | 16/8 | 128 | 6144 | yes | 32k |
| 4B | 36 | 2560 | 32/8 | 128 | 9728 | yes | 32k (2507: 256k) |
| 8B | 36 | 4096 | 32/8 | 128 | 12288 | no | 32k→131k YaRN |
| 14B | 40 | 5120 | 40/8 | 128 | 17408 | no | 128k |
| 32B | 64 | 5120 | 64/8 | 128 | 25600 | no | 128k |

- Pretraining: **36T tokens, 119 languages, 3 stages** — S1 ~30T general @4k;
  S2 ~5T reasoning-dense (STEM/code/synthetic, upweighted); S3 long-context
  (RoPE base ABF 10k→1M, YaRN + DCA for 4x inference extension).
- Post-training: 4 stages — long-CoT cold-start SFT → reasoning RL (GRPO) →
  **thinking-mode fusion** (one checkpoint, `/think` `/no_think`) → general RL.
  Small sizes skip most RL: **strong-to-weak distillation** (off-policy then
  on-policy logit distillation from the flagship) at ~1/10 the GPU hours of RL
  with better pass@1 — the canonical recipe for the 0.6–8B tier.
- Qwen3-2507 refresh (Jul 2025): hybrid thinking abandoned for updates —
  separate Instruct and Thinking checkpoints (quality cost of fusion), 4B-2507
  gets 256k native. Qwen3-Next 80B-A3B (Sep 2025) previewed the next
  architecture: Gated DeltaNet + gated full attention 3:1, 512-expert sparse
  MoE, MTP.

### Qwen3.5 (Feb 2026) — dense 0.8B / 2B / 4B / 9B / 27B + MoE 35B-A3B / 122B-A10B / 397B-A17B
- The Qwen3-Next architecture generalized: **hybrid Gated DeltaNet (linear
  attention) : Gated Attention (full) at 3:1**, sigmoid output gate on
  attention, zero-centered RMSNorm QK-norm, partial RoPE, **MTP (multi-step)**,
  sparse MoE on the larger sizes. Token embedding 248,320 (padded).
- **Natively multimodal by early fusion** — text, image, video through the same
  weights from scratch (no bolted-on ViT adapter); 201 languages; **262k native
  context, ~1M via YaRN**. Even the 0.8B processes video on-device.
- Flagship 397B-A17B internals (for scaling intuition): 60 layers, d=4096,
  block = 15 × [3×(GDN→MoE) + 1×(GatedAttn→MoE)]; 512 experts, 10 routed + 1
  shared active; GDN heads 64 V / 16 QK @128; full-attn 32 Q / 2 KV @256,
  RoPE dim 64.
- Small dense members keep the same hybrid layout — the KV/state cost at long
  context drops roughly 40% vs a plain-GQA equivalent at 32k and scales far
  better beyond; the cost is kernel/ecosystem support (needs GDN kernels —
  vLLM ≥0.17, recent llama.cpp).

### Qwen3.6 (Apr 2026) — 27B dense, 35B-A3B
- Qwen3.6-27B (open, Apache 2.0): 64 layers, d=5120, block = 16 × [3×(GDN→FFN)
  + 1×(GatedAttn→FFN)]; GDN 48 V / 16 QK heads @128; full-attn 24 Q / 4 KV
  @256, RoPE dim 64; d_ff 17,408; 262k native → ~1.01M YaRN; multi-step MTP;
  hybrid thinking restored (+ "thinking preservation" across turns for agent
  loops). SWE-bench Verified 77.2 — the strongest dense open coder of H1 2026.
- Qwen 3.7 (May 2026) and 3.8 (Jul 2026 preview) shipped hosted-only; as of
  late July 2026, 3.6 is the newest downloadable Qwen. Re-verify before citing.

---

## 3. Peer SLMs worth stealing from (one idea each)

| Model | The idea to take |
|---|---|
| Llama 3.2 1B/3B (Meta, 2024) | Prune a bigger sibling then distill (logits of 8B/70B) instead of training small from scratch; ~9T tokens; still the max-ecosystem-compatibility baseline |
| Phi-4 / Phi-4-mini 3.8B (Microsoft, 2025) | Synthetic-data-first curriculum ("textbook" data) buys reasoning per param; 200k-class tiktoken vocab even at 3.8B; Phi-4-mini-flash-reasoning's SambaY hybrid = ~10x decode throughput |
| SmolLM3 3B (HF, 2025) | The fully open recipe: 11T tokens, 3-stage evolving mixture, NoPE every 4th layer, intra-document masking, dual think/no_think, published end-to-end — cite it when someone wants to reproduce a training run |
| MobileLLM / MobileLLM-R1 (Meta) | Deep-narrow beats wide at ≤1B; embedding sharing; layer sharing; R1: ~5x data efficiency via careful mixture + distillation |
| LFM2 / LFM2-8B-A1B (Liquid AI, 2025) | Gated short-convolution blocks + a few GQA layers → ~2x CPU prefill/decode vs same-size transformers; MoE with ~1B active as a phone-class server model |
| Granite 4.0/4.1 (IBM, 2025–26) | Mamba-2:attention 9:1 hybrid, NoPE, ISO-42001-style enterprise positioning; 4.1 (Apr 2026) 3B/8B/30B — the 8B is a top sub-10B coder (HumanEval ~87) |
| Nemotron Nano 2 9B (NVIDIA, 2025) | Mamba-hybrid + Minitron prune-distill from 12B; explicit "thinking budget" control; ~6x decode throughput vs same-class transformer |
| DeepSeek-R1-Distill 1.5–8B (2025) | The proof that SFT-distilling a big reasoner's traces beats doing RL on the small base directly |
| Jamba Reasoning 3B (AI21, 2025) | SSM-transformer hybrid holding 256k context in the 3B class |
| Apple on-device AFM ~3B | ~2-bit QAT + LoRA adapters per feature + KV sharing: the reference for "quantization decided before training" |
| Ministral 3 (Mistral, 2026~) | Apache-2.0 8B-class generalist; check current benchmarks before citing |
| NVIDIA "SLMs are the future of agentic AI" (Jun 2025) | The position paper to cite for SLM-first agent systems: most agent calls are narrow and repetitive → route to small specialists |

---

## 4. Convergence table — what "normal" means now (2024 → mid-2026)

| Dimension | 2024 normal | Mid-2026 normal (sub-10B) |
|---|---|---|
| Attention | full attention every layer, GQA | hybrid: SWA 4–5:1 (Gemma) or linear GDN 3:1 (Qwen) or Mamba 9:1 (Granite); full-attn-everywhere needs justification |
| Positional | RoPE 10k–500k base | dual-base RoPE (10k local / 1M global), p-RoPE or partial RoPE, NoPE layers; YaRN for extension |
| Norms | pre-RMSNorm | pre+post RMSNorm + QK-norm; soft-capping dead |
| Vocab | 32–152k | 150–262k even at 1B; tied embeddings ≤4B |
| Context | 8–32k | 128–262k native, ~1M extended |
| Modality | text; vision via adapter | natively multimodal (early fusion, or unified encoder-free); audio arriving at 2–8B |
| Reasoning | separate "R" models | thinking mode toggle in-checkpoint; thinking budgets |
| Decode speed | plain AR | MTP/spec-decode drafter shipped with the model |
| Small MoE | rare | A1B–A4B active class (Gemma 26B-A4B, Qwen 35B-A3B, LFM2-8B-A1B) as the "local server" tier |
| Quantization | community PTQ | first-party QAT (int4 / int2+int8-act / Q4_0) at release |
| License | bespoke | Apache 2.0 trend (Gemma 4, Qwen3.x) |

---

## 5. Sourcing rules

Cite by report name (e.g. "Gemma 4 tech report, arXiv 2607.02770"; "Qwen3
technical report"). Paraphrase; don't reproduce report text. When the user asks
about a model absent from this file or newer than Jul 2026, search the web and
read the HF config before answering — never guess hyperparameters.

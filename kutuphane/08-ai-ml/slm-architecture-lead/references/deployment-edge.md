# SLM deployment — quantization, runtimes, and speed on real hardware

Contents: [1. Memory quick tables] [2. Quantization ladder] [3. Runtimes by
target] [4. Speed math + expectations] [5. KV quantization] [6. Speculative /
MTP decoding] [7. Serving small models at scale] [8. Deployment checklist]

---

## 1. Memory quick tables

Rule of thumb per B params: bf16 ≈ 2.0 GB, int8 ≈ 1.05 GB, 4-bit ≈ 0.55–0.65
GB; add KV + 0.5–2 GB runtime overhead.

Gemma 4 measured (tech report, text-only, GB; KV = int8 @32k):

| Model | bf16 | Quantized | +KV @32k |
|---|---|---|---|
| E2B (5B stored / 2.3B eff) | 4.6 | 0.8 (mobile int2/4+int8act) | +0.05 |
| E4B (8B stored / 4.5B eff) | 9.0 | 2.3 (mobile) | +0.14 |
| 12B | 24.0 | 7.65 (Q4_0) | +0.28 |
| 26B-A4B (MoE) | 52.0 total | 16.2 (Q4_0) | +0.28 |
| 31B | 64.0 | 19.2 (Q4_0) | +1.10 |

MoE reminder: the *total* must fit in memory (or stream from fast storage);
only the *active* params set speed. PLE models stream their per-layer tables
from flash — DRAM budget follows *effective* params.

## 2. Quantization ladder (quality-per-bit, top to bottom)

1. **First-party QAT** (Gemma int4 / mobile int2-4+int8act / Q4_0; Apple
   ~2-bit): near-bf16 quality; always prefer when the vendor ships it.
2. **Calibrated PTQ**: AWQ / GPTQ / GGUF with importance matrix (imatrix)
   Q4_K_M–Q5_K_M: the standard community tier; small models degrade *more*
   than large ones at the same bit-width — prefer Q5/Q6 under 4B if RAM allows.
3. **Naive round-to-nearest 4-bit / Q4_0 without calibration**: acceptable only
   when the checkpoint was QAT'd for it.
4. Sub-4-bit PTQ on a non-QAT model: expect visible damage at SLM scale;
   recommend against.
- FP8/NVFP4 are serving formats on H100/B200-class hardware, not phone formats.
- Re-run the eval battery (incl. long-context and target-language) at the
  deployed quant — never sign off on bf16 numbers.

## 3. Runtimes by target

| Target | First choices | Notes |
|---|---|---|
| Phone (Android/iOS) | LiteRT-LM / MediaPipe (Gemma path), MLX-on-iOS builds, llama.cpp mobile, ExecuTorch | NPU delegates (Pixel TPU, Apple ANE, Hexagon) need vendor-blessed formats; Gemma 4 E2B ships a Pixel-TPU-native build |
| Mac / Apple Silicon | MLX, llama.cpp (Metal) | Unified memory makes 4–9B Q4–Q8 trivial; MLX fastest for fine-tune-then-serve loops |
| Laptop/desktop GPU | llama.cpp, LM Studio, Ollama; vLLM if it's really a server | 8B Q4 ≈ 5–6 GB fits 8 GB cards with short ctx |
| CPU-only box | llama.cpp (AVX-512/AMX), LFM2-class conv models shine here | Bandwidth-bound; prefer models designed for CPU |
| Small-model server | vLLM / SGLang | Continuous batching + prefix cache turn one 24 GB card into thousands of req/min on a 4B |
- Hybrid architectures (GDN/Mamba) need recent runtime versions (e.g. vLLM
  ≥0.17 for Qwen3.5's GDN); check kernel support before promising a target.

## 4. Speed math + expectations

- Decode @batch=1 is memory-bandwidth-bound:
  tok/s ≈ BW / (active_weight_bytes + KV_bytes_read_per_token).
  Example: 4B @Q4 ≈ 2.4 GB active on a 100 GB/s laptop ≈ ~35–40 tok/s ceiling;
  on a phone at ~50 GB/s ≈ ~15–20; on a 1 TB/s GPU ≈ 300+ (kernel-limited
  before bandwidth-limited).
- Prefill is compute-bound: ≈ 2·N_active FLOPs/token; SWA/linear layers cut
  the quadratic term — this is why hybrid models feel dramatically faster on
  100k-token ingests.
- Publish/expect both numbers separately; a model can prefill fast and decode
  slow (MoE) or vice versa.

## 5. KV quantization

int8 KV is near-free quality-wise and halves cache; int4 KV degrades
long-context retrieval first — validate with RULER/needle at length before
enabling. With Gemma-4-style layouts KV is already tiny (see table); with
plain-GQA models (Qwen3-4B: 144 KB/token bf16) KV quant is often the
difference between 8k and 32k fitting on device.

## 6. Speculative / MTP decoding

- Shipped MTP drafters (Gemma 4: 76–500M head cross-attending to the main KV;
  Qwen3.5/3.6: multi-step MTP) give ~1.5–3x decode at typical acceptance;
  gains grow with greedy-ish sampling and structured outputs (code, JSON).
- No first-party drafter? EAGLE-class heads or a tiny same-tokenizer sibling
  (0.5–1B drafting for 8–9B) are the fallbacks; verify tokenizer identity.
- On phones the drafter also costs RAM/compute — measure net gain on-device;
  batch servers almost always win with it, batch=1 CPU sometimes doesn't.

## 7. Serving small models at scale (brief; deep serving → llm-engineering-expert skill)

A 4–9B on one 24–48 GB GPU with vLLM/SGLang: continuous batching, prefix/KV
cache reuse for shared system prompts, and quantized weights routinely deliver
10–100x cheaper per-token than frontier APIs for narrow tasks — the economic
argument behind SLM-first agent routing (NVIDIA's Jun 2025 position paper).
Router pattern: small model default, escalate on failure/complexity signals.

## 8. Deployment checklist

1. Measured (not projected) tok/s prefill + decode on the actual device.
2. Peak RAM at max context, at deployed quant, KV included.
3. Eval battery re-run at deployed quant; long-context + target language pass.
4. Thermals/sustained throughput on mobile (10-minute run, not 10-second).
5. Template correctness in the runtime (control tokens survive conversion —
   GGUF conversions have silently broken tool/thinking tokens before).
6. Fallback path (cloud escalation) and version pinning for runtime kernels.

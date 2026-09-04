# SLM training recipes — pretraining, distillation, post-training, fine-tuning

Contents: [1. Token budgets] [2. Multi-stage pretraining] [3. Distillation]
[4. Post-training pipeline] [5. Thinking mode lessons] [6. QAT as a training
phase] [7. Fine-tuning existing SLMs (practical)] [8. Eval battery + anchors]
[9. Cost estimation]

---

## 1. Token budgets — over-train on purpose

Chinchilla-optimal (~20 tok/param) is irrelevant for SLMs; they are
inference-optimal artifacts. Shipped budgets:

| Model | Params | Pretrain tokens | tok/param |
|---|---|---|---|
| Gemma 3 1B / 4B / 12B / 27B | | 2T / 4T / 12T / 14T | 2000 / 1000 / 1000 / 520 |
| Qwen3 family | 0.6–32B | 36T (shared corpus) | up to 60,000 (0.6B) |
| Llama 3.2 1B/3B | | ~9T (+ teacher logits) | ~9000 / 3000 |
| SmolLM3 | 3B | 11T | ~3700 |
| Phi-4-mini | 3.8B | ~5T synthetic-heavy | ~1300 |

Guidance: ≥1000 tok/param from scratch; distillation from a strong teacher
buys roughly a 2–5x data-efficiency discount (Llama 3.2, MobileLLM-R1 pattern).
Curves keep improving past these points — the stop is budget, not saturation.

## 2. Multi-stage pretraining (the 2025–26 standard shape)

1. **S1 bulk** (80–90% of tokens) @4–8k seq: filtered web + code + multilingual.
   Aggressive dedup, decontamination, quality classifiers.
2. **S2 reasoning-dense mid-training** (5–15%): upsample STEM, math, code,
   synthetic textbook/CoT data (Qwen3: ~5T of its 36T; Phi's whole identity).
3. **S3 long-context** (last few %): lengths to 32–262k, RoPE base ABF,
   intra-document masking, synthetic long-range tasks.
4. **Anneal/decay phase**: on the LR decay tail, switch to the highest-quality
   mixture (instruction-ish, math, code) — outsized quality gains per token.
- LR: WSD/trapezoid schedules dominate (easy mid-training restarts); μP if you
  will sweep at small proxy scale and transfer.
- Data > architecture: at fixed budget, mixture and filtering quality move
  benchmarks more than any block-diagram choice. Say this out loud in answers.

## 3. Distillation — the defining SLM technique

- **Pretraining KD (Gemma doctrine):** train the small model against a large
  teacher's logit distribution (temperature-softened CE) for most tokens.
  Gemma 2 introduced it for 2B/9B; Gemma 3 applied it across sizes. Effect:
  small model quality well above its from-scratch curve at equal tokens.
- **Prune-then-distill (Llama 3.2 / Minitron / Nemotron):** structured-prune a
  mid-size sibling (width/depth), heal with teacher-logit distillation. Cheapest
  path to a small model when a good big sibling exists.
- **Strong-to-weak post-training distillation (Qwen3 doctrine):** for the
  0.6–8B tier, replace most of the RL pipeline with (a) off-policy
  distillation on teacher-generated responses, then (b) on-policy
  distillation — sample from the student, minimize KL to teacher logits (GKD
  family). Reported ~1/10 the GPU hours of doing reasoning RL on the small
  model, with better pass@1 and pass@k.
- **Trace SFT distillation (DeepSeek-R1-Distill):** even plain SFT on ~800k
  curated reasoning traces from a big reasoner beats RL run directly on the
  small base. Order of preference for giving a small model reasoning:
  distill traces → on-policy logit distill → (only then, and only with
  verifiable rewards) light RL.
- Practicals: match or map tokenizers (logit KD needs shared vocab; otherwise
  trace-level SFT), temperature ~1–2, mix ~10–30% ground-truth CE with KD loss,
  and filter teacher outputs for correctness before training on them.

## 4. Post-training pipeline for an SLM (reference shape)

1. SFT: broad instruction + tool-calling format + multilingual chat, with the
   exact chat template and control tokens the release will use.
2. Reasoning: distillation per §3 (RL only for flagship-class models or when
   you have cheap verifiable rewards — code tests, math checkers).
3. Preference stage: DPO/APO-class on curated pairs (SmolLM3 used APO);
   lightweight GRPO/RLVR passes acceptable for narrow verifiable domains.
4. Merging: checkpoint soups across post-training variants are standard and
   cheap quality (SmolLM3 documented it openly).
5. Safety + refusal calibration; factuality data (hedging, attribution,
   citation-style answers measurably cut hallucination — Gemma 4 reports
   filtering + targeted data here).

## 5. Thinking-mode lessons (learned the expensive way)

- Qwen3 fused think/no-think into one checkpoint via "thinking mode fusion";
  the 2507 refresh **split them again** because fusion cost peak quality.
  Gemma 4 and Qwen3.6 ship toggleable thinking that appears to work — treat
  "hybrid in one checkpoint" as achievable but a real tax to engineer.
- Budget control (cap thinking tokens) is now a user expectation (Nemotron
  Nano 2 popularized explicit budgets); plan the template tokens for it.
- Small models loop in thinking mode more than large ones (observed publicly
  on 0.8–2B class): ship recommended sampling params and a loop guard.

## 6. QAT as a training phase, not a conversion

- Decide serving precision up front (int4 weights? int2/int4 mixed + int8
  activations? Q4_0 blocks?). Run the final slice of training (typically the
  last few % of tokens, or a short dedicated phase) with quantization
  simulated so weights settle into the grid. Gemma 3 QAT int4 cut the
  quality gap vs bf16 dramatically vs PTQ; Gemma 4 ships mobile-QAT (int2/
  int4 + int8 act) and Q4_0 variants as first-class artifacts; Apple trains
  ~2-bit on-device weights with adapters on top.
- QAT the encoders too if multimodal (Gemma 4: vision W8A8 → half memory,
  −44% latency; audio {2,4,8}-bit by layer cluster → 390→87 MB).
- Keep a per-block activation scale if fp16 inference is a target.

## 7. Fine-tuning existing SLMs (what users actually ask)

- **Base (PT) vs instruct (IT):** heavy format/domain retraining or new chat
  template → PT; behavior/tone/tool tweaks on top of good instruction
  following → IT with the *original* template preserved.
- **Chat-template landmines:** Gemma 4 PT ends with `<eos>` but IT ends with
  its end-of-turn token — SFT data must append the right terminator or the
  model never stops. Thinking models: decide whether traces are in the SFT
  targets, and mask consistently. Never train tool-calls as free text if the
  model has dedicated tool tokens.
- **LoRA defaults for 1–9B:** r 16–64 on attention + MLP projections, lr
  1e-4–2e-4, 1–3 epochs on 1k–100k examples; QLoRA if VRAM-bound; full FT only
  for tokenizer/vocab surgery or large domain shifts.
- **Distill-into-small workflow (very common ask):** generate traces from a
  frontier model on the user's task → filter by verifiable correctness →
  SFT a 4B-class base → optional DPO on its own best-vs-worst samples →
  evaluate against the frontier model on a held-out set; expect to close
  60–90% of the gap on a narrow task at ~1/50 serving cost.
- Multilingual (e.g. Turkish) fine-tunes: check tokenizer fertility first;
  a bad tokenizer cannot be fine-tuned away.

## 8. Eval battery + 2026 calibration anchors

Minimum battery: MMLU-Pro or equivalent, GPQA-Diamond, one live code eval
(LiveCodeBench-class), IFEval/IFBench, a long-context eval (RULER/MRCR) **at
deployed quant**, target-language evals, tool-use (BFCL/Tau-class), and
on-device latency measured on the actual chip.

Rough "good for its size" anchors (thinking mode, mid-2026): 2B-class ≈
MMLU-Pro ~60 / GPQA-D ~43; 4–5B-class ≈ MMLU-Pro ~69 / GPQA-D ~59 / AIME ~40;
best dense sub-10B coders reach HumanEval ~87, and the 27B hybrid class hits
SWE-bench-Verified ~77 (Qwen3.6-27B). Re-verify by search before quoting —
these drift monthly.

## 9. Cost estimation (order of magnitude, be honest)

FLOPs ≈ 6·N·D (active N for MoE). Example: 4B dense × 12T tokens ≈ 2.9e23
FLOPs → at ~40% MFU on H100-class (~1e15 FLOP/s effective), ≈ 7e7 GPU-seconds
≈ **~20k H100-hours per trillion tokens for a 4B**, so a 12T-token run is a
few hundred thousand GPU-hours class — feasible for a funded team, not a
weekend. Always add: data pipeline and evals typically cost as much
engineering as the run itself, and are where projects actually fail.

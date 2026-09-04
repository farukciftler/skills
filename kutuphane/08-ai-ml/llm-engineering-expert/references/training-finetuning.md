# Training & Fine-tuning (verified July 2026)

Contents: 1. Pipeline overview · 2. Pretraining · 3. Post-training stack ·
4. RLVR in practice · 5. Reasoning models · 6. Fine-tuning for practitioners ·
7. Distillation · 8. Tooling

---

## 1. Pipeline overview

Modern pipeline has four stages; post-training now contributes most of the
*usable* capability delta between models sharing similar pretraining scale:

1. **Pretraining** — next-token prediction on 10–20T+ tokens.
2. **Mid-training** — long-context extension (RoPE scaling + long-doc data),
   data annealing (upweight high-quality/math/code at the end), sometimes MTP.
3. **Post-training** — SFT → preference optimization → RL with verifiable
   rewards (the 2025–26 standard stack).
4. **Specialization** — domain/agent RL, distillation into smaller sizes.

## 2. Pretraining (what matters if asked)

- Data quality/mixture beats raw quantity; heavy dedup + filtering + curriculum
  (anneal on best data). Synthetic data now a large fraction for math/code.
- Chinchilla-optimal (~20 tokens/param) is a *training-cost* optimum; everyone
  overtrains far beyond it because inference cost dominates lifetime cost —
  small over-trained models are the product sweet spot.
- FP8 pretraining is mainstream (DeepSeek pioneered at scale); FP4 weights
  appearing (DeepSeek V4, Mistral 3 NVFP4 builds).
- Optimizers: AdamW default; **Muon** proved at 1T scale (Kimi K2) with
  notably clean loss decay; MuOpt variants elsewhere. Expect Muon-family to
  keep spreading.
- MoE training needs load-balancing (aux losses or DeepSeek's aux-loss-free
  bias method) and dense warm-up layers (see architectures.md §5).

## 3. Post-training stack (the RLHF-era recipe is dead)

The 2023 recipe (SFT + human-preference RLHF/PPO) has been replaced by a
modular three-part stack:

1. **SFT** — instruction/format/persona. Quality >> quantity: 1k–10k
   excellent, diverse examples routinely beat 100k mediocre ones. Data =
   curated human + rejection-sampled model outputs (generate N, keep
   verified-best).
2. **Preference optimization** — DPO and descendants (SimPO, KTO, ORPO) on
   pairwise preferences. No reward model, no RL loop; cheap alignment/style
   layer. Preference *data* is increasingly AI feedback (RLAIF) not human.
3. **RLVR** — RL with verifiable rewards on tasks where success is checkable:
   unit tests pass, math answer matches, constraint satisfied, tool call
   valid. This is where reasoning/agentic capability comes from.

Algorithm lineage (each step deletes a component): PPO (needs critic + reward
model) → DPO (deletes reward model, offline) → **GRPO** (deletes the critic:
sample a *group* of responses per prompt, advantage = reward relative to group
mean — DeepSeek's contribution, now the default) → refinements **DAPO**,
**Dr. GRPO** (fix length bias / normalization pathologies). Know GRPO cold;
mention DAPO/Dr. GRPO as the tuned variants production teams actually run.

## 4. RLVR in practice — you become half a verifier team

The verifier IS the dataset. Budget accordingly:

- Sandboxed code execution (real isolation, timeouts, resource caps).
- Robust answer extraction (math checkers that survive LaTeX/format variance).
- LLM judges with calibrated rubrics for fuzzy criteria + disagreement
  tracking.
- Reward shaping for partial credit on multi-step tasks.
- Anti-gaming: length penalties, format checks, repetition penalties.

Failure modes to warn about, always:

- **Reward hacking** — the policy exploits every verifier loophole (checks
  only final boxed answer → model emits answer with fake work). The central
  alignment problem of the RLVR era; verifiers must be adversarially
  maintained.
- **Capability tunneling** — pure math/code RLVR degrades general chat;
  mitigate by mixing SFT/preference data into the RL phase.
- **Entropy collapse / diversity loss** — group sampling degenerates;
  monitored via response entropy.

**Agentic RL** (the 2026 growth edge): reward entire multi-step trajectories
(browse → code → test → revise), not single answers. Environments + trajectory
credit assignment are the hard parts.

## 5. Reasoning models

Recipe popularized by DeepSeek-R1: base model → (optional cold-start SFT on
long chain-of-thought) → large-scale GRPO/RLVR on math/code → rejection-sample
the RL model to build better SFT data → repeat → final preference pass.
Emergent behaviors: self-checking, backtracking, very long CoT. Products get
"thinking budget" controls because inference-time compute scales quality.
Hybrid instruct/thinking models (one checkpoint, togglable reasoning) are now
standard (Qwen3, GLM, Kimi K2 Thinking).

## 6. Fine-tuning for practitioners (the questions users actually ask)

**Should we fine-tune at all?** Apply the SKILL.md decision order
(prompt → RAG → FT → RL). Fine-tune for *behavior* (format, tone, jargon,
tool-call syntax, distilling a task into a smaller/faster/cheaper model);
do NOT fine-tune for *knowledge injection* — that's RAG's job.

**Method selection:**

- **LoRA** — default. Low-rank adapters on attention (+ often MLP)
  projections. Start r=16, alpha=2r, lr≈1e-4–2e-4, 1–3 epochs. Covers ~95%
  of business fine-tuning; adapters are swappable per-customer/task.
- **QLoRA** — LoRA over a 4-bit (NF4) frozen base: 70B-class fine-tuning on a
  single 48–80GB GPU. Small quality tax vs full LoRA; fine for most.
- **Full fine-tuning** — only when LoRA plateaus and you own serious compute;
  higher catastrophic-forgetting risk.
- Sizing data: format/style tasks 500–5k examples; complex behavior 10k+.
  Always hold out an eval set *before* training (see evaluation.md).

**Practical gotchas:** train on the exact chat template you'll serve with;
mask the prompt tokens in loss; overfitting shows as verbatim regurgitation —
lower epochs/rank; evaluate against the *base* model to prove the delta;
MoE fine-tunes are finicky (router drift) — prefer dense bases for small
projects (e.g., Qwen dense sizes, Gemma, Ministral).

## 7. Distillation

Teacher → student transfer: generate high-quality traces with a big model
(optionally rejection-sampled/verified), SFT a small model on them. R1-distill
proved small dense models inherit much of a reasoner's ability. This is the
standard cost-reduction path for a working-but-expensive LLM feature: distill
your best prompts+traces into an 8–32B you can self-host. Check licenses —
most open licenses permit it (MIT/Apache ones do); some restrict training on
outputs.

## 8. Tooling (open stack, gap to frontier labs unusually small)

- SFT/DPO: **TRL** (HF), Axolotl, LLaMA-Factory, Unsloth (single-GPU speed).
- RL/RLVR: **verl** (production GRPO at scale), OpenRLHF, Open-Instruct.
- Agentic RL: Agent-Lightning, Agent-R1, RAGEN.
- Distributed: FSDP2, DeepSpeed, Megatron-LM for pretraining-scale.
- Cloud fine-tuning APIs exist for closed models but lock you in; recommend
  open-weight + LoRA when portability matters.

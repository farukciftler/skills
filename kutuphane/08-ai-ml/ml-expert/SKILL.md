---
name: ml-expert
description: Expert ML engineering workflow for Kaggle competitions and general machine learning projects on a MacBook Pro M2 Pro (10-core CPU / 16-core GPU / 16 GB unified memory). Use whenever the task involves competing on Kaggle, building or debugging an ML model, cross-validation design, feature engineering, GBDT (LightGBM/XGBoost/CatBoost), ensembling/stacking, hyperparameter tuning with Optuna, training neural nets locally with PyTorch MPS or MLX, handling datasets that strain 16 GB of RAM, or deciding when to move work off-laptop to a cloud GPU. Triggers: "kaggle", "competition", "leaderboard", "CV score", "feature engineering", "LightGBM", "XGBoost", "CatBoost", "stacking", "ensemble", "Optuna", "overfitting", "train a model", "MPS", "MLX", "out of memory".
---

# ML Expert — Kaggle & Production ML on Apple Silicon (M2 Pro)

## 0. The one thing that governs everything: the hardware

This machine is **MacBook Pro M2 Pro: 6 performance + 4 efficiency CPU cores, 16-core GPU, 16 GB unified memory, no CUDA**. Every recommendation below is calibrated to that. Never suggest a workflow that assumes an A100/H100 is sitting under the desk, and never silently propose `device="cuda"`, `cuml`, `cudf`, `bitsandbytes`, `flash-attn`, or `xgboost tree_method="gpu_hist"` — none of them work here.

What this hardware **is excellent at**:
- GBDTs on CPU (LightGBM/XGBoost/CatBoost) up to a few million rows × a few hundred features
- Polars / DuckDB / Arrow data wrangling — genuinely fast, memory-frugal
- Fine-tuning small transformers (≤1B params) and training small/medium CNNs via MPS or MLX
- LLM inference locally via MLX (up to ~14B at 4-bit, comfortably ~7-8B)
- Fast iteration loops: the win here comes from *experiment throughput*, not raw FLOPs

What it **is not**: a training rig for large vision transformers, 7B+ full fine-tunes, or 500-model GPU stacks. When the task needs those, say so early and route to cloud (§6) instead of burning three hours discovering it.

**Hard budget rules on 16 GB unified memory** (GPU shares the same pool — there is no separate VRAM):
- Keep the working DataFrame under **~4 GB**; above that, switch to Polars lazy/streaming or DuckDB (see `references/apple-silicon.md`).
- MPS allocations compete with the OS and your browser. Close Chrome before a long training run — it is worth 2-3 GB.
- Default CPU parallelism: **`n_jobs` / `num_threads` = 6** (P-cores only). Using 10 makes GBDTs *slower* because E-cores stall the sync barriers of each boosting iteration. This is the single most common Apple Silicon perf mistake.

## 1. Golden rules

1. **Trust local CV, not the public leaderboard.** The public LB is often a few thousand rows. Build a validation scheme that mirrors how the test set was split, then only submit to confirm the correlation between CV and LB. If CV and LB disagree in direction, investigate the split — do not chase the LB.
2. **Build the validation harness before the first model.** Fold assignment gets frozen once and reused by every experiment forever. Different folds across experiments = uncomparable numbers = wasted week.
3. **Optimize the competition metric, not a proxy.** If the metric is AMEX-style, quadratic-weighted kappa, or MAP@k, write the metric first, validate it against the host's description, and use it in every eval.
4. **A dumb baseline in hour one beats a clever model in week two.** Mean/mode predictor → single LightGBM with default params → then improve. The baseline calibrates how much signal exists at all.
5. **One change per experiment, logged.** Every run writes a row: fold seed, features, params, CV, LB, wall time. Untracked experiments are not experiments.
6. **Feature engineering beats model choice on tabular data.** GBDTs still win pure tabular competitions; what separates the top 1% is domain-driven features, not exotic architectures.
7. **Diversity beats strength in ensembles.** Two mediocre models that err differently blend better than two strong correlated ones. Check OOF correlation before blending.
8. **Never fit anything on the full data before splitting.** Target encoding, scalers, imputers, PCA, feature selection — all fit inside the fold. This is the #1 source of silent leakage.
9. **Save OOF and test predictions for every model, always.** `oof_{name}.npy` + `test_{name}.npy`. Ensembling later is impossible without them, and re-running is expensive here.
10. **Keep a written "what I know about this data" file.** EDA insights decay from memory in three days; the file is what turns week 3 into a good week.

## 2. Competition workflow (with realistic M2 Pro time budgets)

Reference `references/competition-playbook.md` for the full expanded version of each phase.

| Phase | Goal | Typical local budget |
|---|---|---|
| **1. Recon** | Read rules, metric, data description, timeline, prior similar comps. Decide if the comp is even feasible on this laptop. | 1-2 h |
| **2. EDA + leakage hunt** | Target distribution, train/test drift (adversarial validation), duplicate rows, ID structure, time ordering, group structure | 3-5 h |
| **3. Validation harness** | Frozen folds matching the test split + metric function + OOF runner | 1-2 h |
| **4. Baselines** | Mean predictor, single LGBM, single CatBoost, simple linear/NN. Establishes signal and model-family ranking. | 2-4 h |
| **5. Feature engineering** | Iterative, hypothesis-driven, each batch validated on frozen folds | 40-60% of total time |
| **6. Tuning** | Optuna on the 1-2 strongest families only, after features stabilize | 4-8 h (overnight) |
| **7. Ensembling** | OOF hill climbing → stacking if it helps → seed averaging | 1-2 days |
| **8. Final** | Retrain on full data if CV says so, sanity-check submission format, pick 2 final subs (one safe, one aggressive) | 3-4 h |

**Feature engineering is where the time should go.** If more than 25% of total effort went into hyperparameters, the priorities are wrong.

## 3. Model selection — decide fast, don't deliberate

| Data | First choice | Second | Notes for this machine |
|---|---|---|---|
| Tabular, <100k rows | **CatBoost** (great defaults, handles cats natively) | LightGBM | Also try **TabPFN-2.5+** — near-SOTA in one forward pass, works on CPU/MPS for small data; excellent as an ensemble member and as a feature generator |
| Tabular, 100k-5M rows | **LightGBM** (fastest CPU trainer) | XGBoost `hist`, CatBoost | 6 threads. Use `feature_fraction`/`bagging` to keep folds under a few minutes |
| Tabular, >5M rows | LightGBM + Polars/DuckDB feature pipeline | subsample rows for iteration | Iterate on a stratified 20% sample; validate the winners on full data |
| Tabular with strong structure (time, geo, sequence) | GBDT **+** a small NN (MLP/GRU/TabM) and blend | — | NNs earn their keep exactly here |
| Images | Fine-tune a small `timm` backbone (ConvNeXt-T, EfficientNet-B0/B3, ViT-S) via MPS | MLX for pure-Apple speed | 224px, batch 16-32. Bigger than that → cloud |
| Text / NLP | Fine-tune a small encoder (DeBERTa-v3-small/base, ModernBERT) via MPS; LLM inference via MLX | — | 7B+ full fine-tune → cloud. LoRA on ≤3B is feasible with MLX |
| Audio | Whisper-small/medium inference works; training → cloud | — | |
| Time series | GBDT on lag/rolling features usually beats deep models | statsmodels/Nixtla baselines | Never use random KFold — see validation ref |

**Ensemble target**: 3-8 genuinely diverse models. On this hardware, quality of diversity > count.

## 4. Reference files — load on demand

Read the relevant file *before* acting, not after:

- **`references/competition-playbook.md`** — phase-by-phase Kaggle playbook: recon checklist, EDA protocol, experiment tracking format, submission strategy, shakeup avoidance, code-competition (offline notebook) constraints.
- **`references/validation.md`** — choosing the fold scheme (KFold / Stratified / Group / Time / nested / repeated), adversarial validation, leakage taxonomy with detection recipes, CV-LB correlation diagnosis, sample-size-aware error bars.
- **`references/tabular-modeling.md`** — GBDT parameter meaning and safe ranges, LightGBM/XGBoost/CatBoost head-to-head, categorical encoding (incl. leak-free target encoding), missing values, imbalance, calibration, Optuna recipe, TabPFN/AutoGluon.
- **`references/feature-engineering.md`** — systematic FE catalogue (aggregations, interactions, temporal, text, count/frequency, target-derived), automated FE at scale, feature selection that doesn't overfit, and when to stop.
- **`references/ensembling.md`** — OOF discipline, hill climbing (with weights), multi-level stacking, blending vs stacking, pseudo-labeling done leak-free, seed averaging, snapshot ensembles.
- **`references/apple-silicon.md`** — the M2 Pro engineering manual: environment setup, thread tuning, PyTorch MPS gotchas & env vars, MLX, memory profiling, Polars/DuckDB streaming, thermal behavior, benchmarks and what "too slow" looks like.
- **`references/deep-learning.md`** — training loops that behave on MPS, mixed precision reality, dataloader settings for Apple Silicon, LoRA/PEFT locally, checkpointing for interrupted runs, debugging NaNs and silent MPS bugs.
- **`references/production-ml.md`** — non-competition ML: problem framing, data contracts, baseline-first delivery, offline/online metric alignment, drift monitoring, model cards, reproducibility, and the failure modes that don't show up in competitions.

## 5. Scripts — use them instead of rewriting

All are standalone and dependency-light. Copy into the project, don't import from the skill dir.

- **`scripts/setup_m2_env.sh`** — one-shot environment bootstrap (uv, libomp, the whole stack, verified import test). Run this first on a fresh project.
- **`scripts/env_doctor.py`** — diagnoses the current machine: cores, memory pressure, OpenMP/threading, MPS availability, library versions, and prints the recommended `n_jobs`. Run when anything is unexpectedly slow.
- **`scripts/cv_framework.py`** — frozen-fold factory + OOF runner that works with LightGBM/XGBoost/CatBoost/sklearn/callable, saves `oof_*.npy` / `test_*.npy`, logs each run to `experiments.csv`.
- **`scripts/hill_climb.py`** — greedy hill-climbing ensembler with replacement over saved OOF matrices; supports any metric and optional negative weights.
- **`scripts/mem_utils.py`** — dtype downcasting, Polars→pandas fast loader, parquet caching decorator, memory profiler context manager.

## 6. When to leave the laptop

Say it out loud and early rather than grinding. Move to a cloud GPU (or Kaggle's free T4×2 / P100 notebooks, 30 h/week) when **any** of these hold:

- A single CV fold takes > ~45 min and the plan needs dozens of experiments
- The model needs > 12 GB of activations (large ViT/UNet, 7B+ fine-tune, big batch diffusion)
- The task genuinely needs multi-GPU or fp8/bf16 tensor-core throughput
- The competition is a code competition where the submission itself must run on Kaggle GPUs — develop where you'll run
- You need cuDF/cuML-scale hyperparameter sweeps or 100+ model stacks

Good division of labor: **prototype, EDA, feature engineering, GBDT work, and ensembling locally; heavy neural training in the cloud.** Kaggle Notebooks are the cheapest option and match the submission environment exactly.

## 7. Anti-patterns to call out immediately

- Tuning hyperparameters before the feature set stabilizes
- Random KFold on time-series or grouped (multi-row-per-entity) data
- Target encoding or scaling fit outside the fold
- Reporting a CV improvement smaller than the fold-to-fold standard deviation as a "gain"
- Selecting features by importance computed on the full dataset
- Blending models with 0.99 OOF correlation and expecting a gain
- Adding a 5th boosting library instead of one good new feature
- `n_jobs=-1` on Apple Silicon (grabs E-cores, slows GBDTs)
- Chasing the public LB in the last week — that is exactly how the shakeup eats you
- Running a 6-hour training script with no checkpointing on a laptop that may sleep

## 8. How to communicate results

When reporting a result, always give: **metric ± fold std, number of folds, what changed vs the previous run, and wall time.** "CV 0.7823 ± 0.0041 (5-fold, +0.0019 vs baseline from adding customer-level aggregates, 11 min)" is a result. "It improved" is not.

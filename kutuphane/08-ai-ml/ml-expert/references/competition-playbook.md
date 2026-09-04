# Kaggle Competition Playbook

The end-to-end operating procedure. Phases are ordered; skipping ahead is the most common way to lose a competition.

---

## Phase 1 — Recon (before writing any code)

Read, in this order:

1. **Evaluation page.** The metric decides everything: model objective, validation design, post-processing, whether calibration matters. Write the metric as a Python function *today* and verify it against a worked example.
2. **Data description page.** Row granularity, ID semantics, what each file is, how train/test were split (random? by time? by group/subject?). The split determines the fold scheme.
3. **Rules.** Team size, submission limits per day, external data policy, whether it is a code competition (offline notebook), runtime limits, licence constraints on pretrained weights.
4. **Timeline.** Team-merge deadline and final-submission deadline. Plan backwards from the merge deadline.
5. **Discussion + prior competitions.** Search for the same host or the same data type. Prior winning solutions are the highest-value reading available; the top solutions of a similar past comp usually transfer 70% of the approach.

### Feasibility check on this laptop (do this before committing)
- Total data size on disk vs 16 GB RAM. >5 GB of tabular data → plan a Polars/DuckDB pipeline from the start.
- Is it a GPU-heavy modality (large images, video, audio training, LLM fine-tuning)? If yes, plan for Kaggle Notebooks / cloud from day one and use the laptop for data work and analysis only.
- Estimated single-fold train time. If a fold is >45 min locally, the local iteration loop is dead; restructure (subsample, fewer folds during dev, cloud).

### Code competition (internet-disabled notebook) specifics
- Every package and every model weight must be pre-uploaded as a Kaggle Dataset and installed from local wheels: `pip install --no-index --find-links=/kaggle/input/my-wheels pkg`.
- Notebook runtime limits (commonly 9 h, sometimes 12) apply to the *whole* inference run, including model load. Budget inference time per test row and multiply by the hidden test size, which is usually much bigger than the visible sample.
- Train offline (locally or on cloud), upload weights as a dataset, and keep the submission notebook inference-only. Chain notebooks (feature notebook → inference notebook) when preprocessing is heavy.
- Test the submission notebook against a *fake* enlarged test set to catch timeouts and OOM before the real run.

**Deliverable of Phase 1:** a `NOTES.md` with the metric, the split hypothesis, the plan, and the feasibility verdict.

---

## Phase 2 — EDA and leakage hunt

Do not do "pretty plots" EDA. Do investigative EDA with specific questions.

### Mandatory checks
1. **Shapes and dtypes.** Rows in train vs test — the ratio hints at how the split was made.
2. **Target distribution.** Skew, zero-inflation, class imbalance, outliers. Decides whether to log-transform, use a robust objective, or stratify.
3. **Missingness pattern.** Is missingness itself informative? Does it differ between train and test? A column missing in test but not train is a trap.
4. **Duplicates.** Exact duplicate rows, and duplicate feature-rows with conflicting targets (label noise ceiling). Duplicates across train/test are sometimes a free leak — check.
5. **ID structure.** Are IDs sequential, hash-like, time-ordered? Sorted IDs frequently encode time. `df.id.diff()` and plotting the target against row index catches this instantly.
6. **Group structure.** Multiple rows per customer/patient/session? If yes → GroupKFold, mandatory.
7. **Time structure.** Any date column, or an implicit ordering? If yes → time-based validation, mandatory.
8. **Train vs test drift.** Per-feature distribution comparison (KS test / PSI) plus **adversarial validation** (see `validation.md`). This is the highest-value 20 minutes of the whole competition.
9. **Feature-target relationship.** For the top numeric features, plot target mean by decile; for categoricals, target mean by level with counts. Reveals monotonic vs non-monotonic relationships and rare-level noise.
10. **Cardinality census.** High-cardinality categoricals drive the encoding strategy.

### Leakage hunt
Ask: *"Would this column be available at prediction time in the real world?"* for every feature. Classic leaks: post-outcome timestamps, row order, file ordering, index-correlated targets, aggregate statistics computed over the full dataset by the host. If a single feature gives AUC > 0.95 alone, it is a leak until proven otherwise.

**Deliverable of Phase 2:** written findings appended to `NOTES.md` — every insight, even the negative ones ("no time signal in IDs").

---

## Phase 3 — Validation harness (freeze it)

See `validation.md` for choosing the scheme. Output of this phase:

- `folds.npy` (or a `fold` column persisted to parquet) — created once with a fixed seed, reused by every experiment for the rest of the competition.
- `metric(y_true, y_pred)` — the exact competition metric.
- An OOF runner (`scripts/cv_framework.py`) that takes a model factory + feature list and returns OOF preds, test preds, per-fold scores, and appends a row to `experiments.csv`.

Sanity test the harness: run it with a constant predictor and with a leaked target column. The first should give a baseline score, the second a perfect one. If not, the harness is broken.

---

## Phase 4 — Diverse baselines

Train these *in parallel conceptually*, all on the frozen folds, all logged:

- Constant predictor (mean/median/mode) — the floor
- LightGBM, default-ish params, raw features
- CatBoost, default params, raw categoricals
- A linear/regularized model (Ridge/Logistic) on one-hot + scaled numerics
- A small MLP or, for ≤10k rows, TabPFN
- For structured modalities: the obvious domain baseline (a pretrained backbone, a naive seasonal forecast)

Why all of them: the spread tells you which family fits the data, and they become ensemble members later. A linear model that scores near the GBDT means the signal is mostly additive; a GBDT far ahead means interactions matter.

**Deliverable:** a baseline table in `NOTES.md` and 5-6 saved OOF files.

---

## Phase 5 — Feature engineering (the main event, 40-60% of time)

See `feature-engineering.md` for the catalogue. Process discipline:

- Work in **batches with a hypothesis**: "customer-level spend aggregates should help because the target is customer behaviour" → build the batch → evaluate on frozen folds → keep or drop the whole batch, then bisect if mixed.
- Keep a **feature registry**: name, definition, batch, CV delta when added. Feature sets get versioned (`feats_v3.json` is a list of column names).
- **Evaluate with the same seed and same folds.** A +0.0005 change that is within fold-std is noise.
- Guard against **leaky features**: anything computed with the target (target/likelihood encoding, target-based aggregations) must be computed *inside the fold* on the training part only.
- Watch **train/test consistency**: a feature whose distribution shifts between train and test (check with adversarial validation) will hurt on the private LB even if CV loves it.

Stop adding features when three consecutive hypothesis batches produce no gain — then move to ensembling.

---

## Phase 6 — Hyperparameter tuning (late, narrow, overnight)

- Tune only the 1-2 strongest families, only after features stabilize. Gains are typically +0.1-1% — an order of magnitude less than good features.
- Optuna with TPE + median pruning, 50-150 trials, on a **reduced fold count (3)** or a subsample for speed, then verify the best 3-5 configs on the full fold set.
- Run it overnight; the M2 Pro is fine for this if each trial is a few minutes. Use `n_jobs=6` inside the model and `n_jobs=1` for Optuna (never nest parallelism — it oversubscribes cores and slows everything).
- Beware **tuning to the validation set**: 500 trials on 5 folds will find a config that fits fold noise. Prefer a broad-then-narrow search and pick a config from a stable region, not the single best trial.

Details and safe ranges: `tabular-modeling.md`.

---

## Phase 7 — Ensembling

See `ensembling.md`. Order of operations:

1. Collect all OOF/test pairs.
2. Check the OOF correlation matrix — drop members correlated >0.98 with a stronger member.
3. **Hill climbing** on OOF to find blend weights (`scripts/hill_climb.py`). This is the highest ROI ensembling step and is cheap on CPU.
4. Try **stacking** (level-2 model on OOF features + a few original features + `confidence`/`consensus` = std/mean over OOF). Keep it only if it beats hill climbing on a *nested* validation.
5. **Seed averaging** the final models — cheap, reliable, ~+0.1-0.3%.
6. **Pseudo-labeling** if there is a lot of unlabeled/test data — done leak-free (per-fold pseudo-labels).

---

## Phase 8 — Endgame

- **Retrain on full data?** Only if the CV curve shows the model is data-hungry (learning curve still rising) and the number of boosting rounds can be fixed from CV (use mean best iteration × 1.1). Otherwise keep the fold-ensemble (average of fold models) — it's usually as good and safer.
- **Submission sanity checks**: row count, ID order/dtype match with `sample_submission.csv`, no NaNs, prediction range plausible, clipping applied if the metric demands it.
- **Choose two final submissions**: one **safe** (best CV, well-correlated with LB) and one **aggressive** (best LB or a higher-variance ensemble). Never pick two variants of the same thing.
- **Write the solution summary** while the details are fresh — it's also what you'd post if you win.

---

## Shakeup avoidance

The private-LB shakeup punishes public-LB chasers. Defences:

- Base every decision on CV; use the LB only to verify that CV and LB move together.
- Prefer robustness: more folds, seed averaging, ensembles over single models, fewer knife-edge post-processing hacks.
- If public LB and CV disagree, the public LB is usually the small/unreliable one — unless adversarial validation proves train and test differ, in which case fix the validation scheme to reflect that difference.
- Small public test set (visible in the rules/percentage split) → weight CV even more heavily.
- Avoid last-week overfitting: the final week should be spent on robustness and ensembling, not on new risky ideas.

---

## Experiment tracking format

One row per run, appended to `experiments.csv`:

```
run_id, timestamp, model, feature_set, params_hash, folds, cv_mean, cv_std,
lb_public, wall_time_s, notes
```

Plus a `runs/{run_id}/` folder with `params.json`, `oof.npy`, `test.npy`, `feature_list.json`.
Anything not written down did not happen.

---

## Working with LLM assistance (this is now standard practice)

2025-2026 winning solutions increasingly use LLM-assisted code generation for breadth — hundreds of experiments, large stacks. What that means practically:

- Use the assistant to generate **many diverse candidate models and feature batches quickly**, then let CV decide. Breadth is the edge.
- **Verify generated code against leakage rules** — generated pipelines routinely fit encoders outside the fold.
- Keep humans (you) on: metric interpretation, split hypothesis, and final submission choice. Those are the decisions where a wrong call is unrecoverable.

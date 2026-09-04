# Ensembling: OOF Discipline, Hill Climbing, Stacking, Pseudo-Labeling

Ensembling is the cheapest remaining gain once features stabilize — and it is CPU-friendly, which makes it the ideal endgame on a MacBook Pro.

---

## 1. The OOF contract (get this right or nothing else works)

For every model you ever train, save:

```
runs/{run_id}/
    oof.npy         # shape (n_train,) or (n_train, n_classes) — predictions for each train row,
                    # each produced by a model that did NOT see that row
    test.npy        # shape (n_test,) — average of the fold models' test predictions
    params.json
    features.json
```

Non-negotiable rules:
- **All models must use the identical fold assignment.** Different folds → OOF preds are not comparable → the blend weights are fitted on garbage.
- OOF predictions must be in the **same space** (all probabilities, or all logits, or all ranks). Mixing probability and logit outputs silently degrades blends.
- For multi-class, keep the full probability matrix.
- Store the fold index array too, so a level-2 model can re-use it.

---

## 2. Choosing members: diversity beats strength

Before blending, compute the OOF correlation matrix (Pearson for regression, Spearman on ranks for AUC-type metrics).

- Members correlated **> 0.98** with a stronger member: drop; they add nothing but variance in the weight fit.
- A member that is 1-2% worse but correlated **< 0.9** is usually worth more than a near-clone of the leader.

Sources of genuine diversity, ranked by effectiveness:
1. **Different model families** (GBDT / NN / linear / KNN / SVR / TabPFN)
2. **Different feature sets** (raw vs engineered vs target-encoded; different subsets)
3. **Different objectives/targets** (e.g. regression + classification on a binned target; predicting a transformed target). Multi-target framing was central to a 2025 first-place solution.
4. **Different preprocessing** (rankgauss vs raw, different imputation)
5. **Different hyperparameters** (deep vs shallow trees)
6. **Different seeds** (weakest diversity, but free and reliable)

---

## 3. Simple blends first

Always try these before anything fancy — they are one line and frequently within a hair of the optimum:
- **Simple average** of the top-k members.
- **Rank average** (`scipy.stats.rankdata` per model, then average) — the right choice for AUC/ranking metrics and when models have different score scales.
- **Weighted average by CV score** (e.g. weights ∝ score − baseline).
- **Geometric mean / logit average** for probabilities — often better than the arithmetic mean for logloss.

Record the CV of each. If the simple average already matches the hill-climb result, ship the simple average — fewer moving parts, less overfit risk.

---

## 4. Hill climbing (best ROI)

Greedy forward selection **with replacement** over the OOF matrix:

1. Start with the single best model.
2. At each step, try adding each candidate model (including ones already in the blend) with a fixed step weight; keep the addition that improves the OOF metric the most.
3. Stop when no addition improves, or after N steps.
4. The final weights are the selection counts, normalized.

Why it works: selecting *with replacement* lets a strong model be picked repeatedly, producing a fine-grained weighting without solving an optimization problem, and it naturally handles any metric — including non-differentiable ones like kappa or MAP@k.

Implementation: `scripts/hill_climb.py`. Practical notes:
- Run it on OOF only; never peek at the LB while choosing weights.
- **Overfitting risk is real** when you have many members and few rows. Mitigate with: bagged hill climbing (repeat on bootstrap samples of the rows and average the weights), or a nested split (fit weights on 4 folds, evaluate on the 5th, rotate).
- Allow negative weights only if you validate carefully — they help occasionally and overfit often.
- With 50+ members, add a small random subset restriction per iteration for regularization.

---

## 5. Stacking (multi-level)

The general structure used by top solutions:

- **Level 1**: many diverse models (GBDTs, NNs, SVR, KNN, TabPFN, linear). Output: OOF + test predictions.
- **Level 2**: a small number of models (typically LightGBM/CatBoost + an MLP) trained on:
  - the level-1 OOF predictions as features,
  - a *small* selection of the strongest original features,
  - meta-features derived from the OOF matrix:
    ```python
    df["consensus"]  = df[OOF_COLS].mean(axis=1)
    df["confidence"] = df[OOF_COLS].std(axis=1)      # disagreement among level-1 models
    ```
  Use **forward feature selection** at level 2 — with dozens of correlated OOF columns, feeding all of them usually overfits.
- **Level 3**: a weighted average / hill climb over the level-2 models.

Leakage rules for stacking:
- Level-2 training data must be the level-1 **OOF** predictions (never in-fold predictions).
- Level-2 CV must use the **same fold assignment** as level 1; otherwise level-2 validation rows were seen by the level-1 model that produced their features.
- Strictly correct practice is *nested* CV; the same-folds shortcut is standard in competitions and works, but be aware it is mildly optimistic — always sanity-check against the LB.
- The test-side level-2 features come from the level-1 fold-averaged test predictions.

**Residual stacking** is the alternative: level-2 trains on the residuals of level-1. Useful for regression when a strong base model already captures most of the signal.

When to stop: each additional level adds ~10× the fits for a shrinking gain. On this laptop, 2 levels + a final blend is the sensible ceiling; 3 levels only if folds are fast.

---

## 6. Pseudo-labeling

Use the current best model to label unlabeled data (usually the test set or external data), then retrain including those rows.

Correct recipe:
1. Generate predictions for the unlabeled data — ideally from an **ensemble**, not a single model.
2. Use **soft labels** (probabilities) rather than hard 0/1 — more signal, less noise amplification.
3. **Leak-free requirement**: for a k-fold setup, produce **k separate sets of pseudo-labels**, where the pseudo-labels used while training fold *i* come from models that never saw fold *i*'s validation rows. Skipping this leaks the validation targets through the pseudo-labels and inflates CV badly.
4. Optionally filter to confident predictions only (e.g. p > 0.9 or p < 0.1), or weight pseudo-labeled rows lower (0.3-0.5) than real rows.
5. Iterate 1-3 rounds; multi-round with an ensemble outperforms a single pass. Gains decay quickly.

Pseudo-labeling shines when the test set is large relative to train, or when a large unlabeled corpus exists. It hurts when the base model is weak — noisy labels get amplified.

---

## 7. Seed averaging and extra training

- **Seed averaging**: retrain the final configuration with 3-10 different seeds and average. Reliable +0.1-0.3%, no overfitting risk, trivially parallel across time (run overnight). For NNs this also averages away initialization luck.
- **Bagging over folds**: keeping the k fold-models and averaging their test predictions is itself an ensemble — usually as good as, and safer than, retraining on 100% of the data.
- **Full-data retrain**: only with a fixed iteration count derived from CV (`mean(best_iter) * 1.1`). You lose the ability to validate, so do it only when the learning curve says more data helps.
- **Snapshot ensembles** (NN): save checkpoints at cyclic-LR minima and average their predictions — several models for the price of one training run. Very good value on a laptop.
- **Weight averaging** (SWA / model soup) for NNs: average the *weights* of checkpoints instead of the predictions; free at inference time.

---

## 8. Practical M2 Pro notes

- Hill climbing and blending are pure numpy over `(n_rows × n_models)` matrices — instant, even with 100 members.
- Store OOF as `float32` — with 1M rows × 100 models, `float64` costs 800 MB for nothing.
- Level-1 model *count* is the real cost. Without a GPU, the 500-model exploratory sweeps described in NVIDIA/cuML writeups aren't reproducible locally — aim for **10-30 well-chosen diverse members** instead, or generate the big sweep on Kaggle Notebooks and do the blending locally (blending is CPU-cheap and can be done offline from downloaded OOF files).
- Keep the OOF directory in the project, not in a temp dir. It is the most valuable artifact of the competition.

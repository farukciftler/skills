# Tabular Modeling (GBDT-first, M2 Pro calibrated)

GBDTs remain the default winner on pure tabular data. Neural nets earn their place when the data has exploitable structure (sequence, time, geometry, text) or as ensemble diversity.

---

## 1. Library selection

| | LightGBM | XGBoost | CatBoost |
|---|---|---|---|
| CPU speed on M2 Pro | **fastest** | fast (`hist`) | slowest, but often best out-of-box |
| Categorical handling | native (`categorical_feature`), needs care | needs encoding (or `enable_categorical` with `hist`) | **best-in-class** (ordered target statistics) |
| Overfit resistance on small data | medium | medium | **highest** (ordered boosting) |
| Default quality | needs tuning | needs tuning | **excellent defaults** |
| Best used for | large data, fast iteration | second opinion, different tree growth | small/medium data, many categoricals, ensemble diversity |

**Practical strategy on this laptop**: LightGBM for the iteration loop (fast), CatBoost as a strong second family, XGBoost third for diversity. All three in the final ensemble — their errors decorrelate nicely because of different tree-growth and split strategies.

**Threading**: set `num_threads=6` / `n_jobs=6` / `thread_count=6` (P-cores). `-1` grabs all 10 including efficiency cores and is measurably slower for boosting. Never nest parallelism (Optuna `n_jobs=1` when the model uses 6 threads).

---

## 2. LightGBM parameters that actually matter

```python
params = dict(
    objective="binary",           # or regression / multiclass / custom
    metric="auc",
    learning_rate=0.03,           # 0.01-0.05 with early stopping
    num_leaves=63,                # main capacity knob; 31-255
    max_depth=-1,                 # leave unlimited, control via num_leaves
    min_data_in_leaf=50,          # main overfit knob; raise for noisy data
    feature_fraction=0.8,         # column subsampling per tree
    bagging_fraction=0.8,         # row subsampling
    bagging_freq=1,               # required for bagging to take effect
    lambda_l1=0.0,
    lambda_l2=1.0,                # try 1-10 on noisy data
    min_gain_to_split=0.0,
    max_bin=255,                  # lower = faster, slightly worse
    num_threads=6,
    verbosity=-1,
    seed=42,
)
```

**Mental model**
- `num_leaves` × `min_data_in_leaf` = capacity. Increase leaves for complex signal; increase `min_data_in_leaf` when overfitting.
- `learning_rate` down + `n_estimators` up (with early stopping) = better and slower. Iterate at 0.05, finalize at 0.01-0.02.
- `feature_fraction`/`bagging_fraction` at 0.7-0.9 both regularize and speed things up.
- Rule of thumb: `num_leaves ≤ 2^max_depth`; huge `num_leaves` with small data is the classic overfit.
- **Early stopping** on the validation fold with `stopping_rounds=100-200`; record `best_iteration` per fold, and use `mean(best_iteration) * 1.1` if you later retrain on full data.

**Speed levers on M2 Pro** (in order of value): fewer rows (subsample during dev) → `max_bin=127` → `feature_fraction` → fewer folds → `learning_rate` up during exploration.

### XGBoost equivalents
`max_depth` (4-8), `min_child_weight`, `subsample`, `colsample_bytree`, `reg_lambda`, `eta`, `tree_method="hist"` (always — `exact` is far slower and no better). `grow_policy="lossguide"` makes it behave like LightGBM and adds diversity.

### CatBoost
Start with defaults and just set `iterations=5000, learning_rate=0.03, early_stopping_rounds=200, depth=6, l2_leaf_reg=3, thread_count=6`. Pass categorical columns via `cat_features` as raw strings — do **not** pre-encode them; that is the whole point of CatBoost. `one_hot_max_size=10` for low-cardinality. Note: CatBoost has no GPU path on Apple Silicon; it is CPU-only here and is the slowest of the three, so use it on the final feature set rather than during rapid iteration.

---

## 3. Categorical encoding

| Cardinality | Approach |
|---|---|
| 2-10 | One-hot (linear/NN) or leave as category (GBDT) |
| 10-100 | LightGBM native categorical / CatBoost native / ordinal for trees |
| 100-10k | **Target encoding (out-of-fold, smoothed)**, count/frequency encoding, or CatBoost native |
| >10k (IDs, text-like) | Frequency encoding, hashing, embeddings (NN), or aggregate statistics instead of the raw ID |

**Leak-free target encoding** — the only correct way:
```python
# inside each CV fold, using ONLY the training part
prior = y_tr.mean()
stats = y_tr.groupby(X_tr[col]).agg(["mean", "count"])
smooth = (stats["mean"] * stats["count"] + prior * m) / (stats["count"] + m)   # m ≈ 10-100
X_tr[col + "_te"] = <inner-fold OOF encoding>   # nested folds inside the training part
X_va[col + "_te"] = X_va[col].map(smooth).fillna(prior)
```
The training part must itself get *out-of-fold* encodings (inner KFold), otherwise the model sees its own target. Unseen categories fall back to the prior.

**Count/frequency encoding** is underrated: it is leak-free, cheap, and often as good as target encoding for tree models. Compute counts over train+test combined *only if* the test set is fully available and static (true in most competitions, not in production).

---

## 4. Missing values, outliers, scaling

- **GBDTs handle NaN natively** — do not impute for trees. LightGBM/XGBoost learn a default direction per split; imputation destroys that signal. Add an `is_missing` indicator column when missingness may be informative.
- **Linear models / NNs** need imputation (median + indicator) and scaling (StandardScaler or QuantileTransformer). Fit inside the fold.
- **Outliers**: trees are robust; for linear/NN use clipping at the 0.1/99.9 percentile computed on the training fold, or rank-gauss / quantile transform.
- **Skewed targets**: `log1p` for RMSLE-like metrics; consider Tweedie objective for zero-inflated positive targets; Huber/quantile objectives for heavy tails.

---

## 5. Imbalanced classification

Ordered by what actually works:
1. **Do nothing to the data**; use the right metric (AUC/PR-AUC/logloss) and tune the decision threshold out-of-fold.
2. `scale_pos_weight` (XGBoost/LightGBM) or `class_weight="balanced"` — helps ranking metrics rarely, helps logloss never; test, don't assume.
3. **Undersampling the majority + bagging** over several undersampled replicas — works well and is fast on CPU.
4. **SMOTE and friends**: usually disappointing on real tabular data and dangerous inside CV (must be applied inside the fold, on the training part only). Try last, not first.
5. **Focal loss** for deep models on extreme imbalance.

Calibration after resampling is broken by construction — recalibrate out-of-fold if the metric is probabilistic.

---

## 6. Probability calibration

Needed when the metric is logloss/Brier or when the output feeds a business threshold. GBDT probabilities are usually decently calibrated with logloss objective, badly calibrated after resampling or with AUC-driven tuning.

- `CalibratedClassifierCV(method="isotonic")` for ≥1k positives; `method="sigmoid"` (Platt) for smaller data.
- Fit calibration **out-of-fold**, never on the data the model trained on.
- Check with a reliability diagram + expected calibration error, not just the metric.

---

## 7. Tabular foundation models and AutoML

**TabPFN (v2.5 / v3 line)** — a transformer that solves small tabular problems in a single forward pass, no training.
- Sweet spot: small-to-medium datasets, ≤10 classes. Newer releases push limits well past the original 10k×500 (up to ~100k rows / 2k features, with row-vs-feature trade-offs), but on CPU/MPS with 16 GB, treat **~10-50k rows** as the practical local ceiling and expect seconds-to-minutes rather than sub-second.
- Excellent uses here: (a) an instant strong baseline in phase 4, (b) a **diverse ensemble member** — its errors decorrelate strongly from GBDTs, (c) a **feature generator** — feed its OOF predictions into a GBDT (this exact trick appeared in a 2025 winning solution).
- Set `TABPFN_ALLOW_CPU_LARGE_DATASET=true` to exceed the conservative CPU row cap; expect it to be slow.

**AutoGluon** — genuinely competitive (it has placed in winning solutions) and a fair "am I leaving anything on the table?" check. On 16 GB, run it with `presets="medium_quality"` or `"good_quality"` and a `time_limit`; `best_quality` will try to build large bagged stacks and can exhaust memory. Use it as a benchmark and as an ensemble member, not as the whole solution — you cannot iterate on features through it.

**Neural nets for tabular** — worth trying for diversity: a simple 3-layer MLP with embeddings for categoricals, TabM / FT-Transformer / SAINT-style models. They rarely beat GBDTs alone but frequently add +0.1-0.5% in a blend. On this laptop, an MLP on ≤1M rows trains fine on MPS or even CPU.

---

## 8. Hyperparameter optimization with Optuna

```python
import optuna
from optuna.samplers import TPESampler
from optuna.pruners import HyperbandPruner   # pairs with TPE; MedianPruner pairs with RandomSampler

study = optuna.create_study(
    direction="maximize",
    sampler=TPESampler(seed=42, n_startup_trials=20, multivariate=True),
    pruner=HyperbandPruner(),
    study_name="lgbm_v3",
    storage="sqlite:///optuna.db",   # resumable — important on a laptop that sleeps
    load_if_exists=True,
)
study.optimize(objective, n_trials=100, n_jobs=1)   # n_jobs=1: the model already uses 6 threads
```

Rules:
- **Search on 3 folds** (or a subsample) for speed; verify the top 5 configs on the full fold set.
- **Prune** with a per-fold intermediate report; `n_startup_trials` prevents pruning on an unreliable median.
- **Two-stage**: wide log-uniform ranges for ~60 trials, then narrow around the good region for ~40. Pick a config from a *stable plateau*, not the single best trial (inspect `optuna.visualization.plot_slice`).
- **Don't tune everything.** For LightGBM: `num_leaves`, `min_data_in_leaf`, `feature_fraction`, `bagging_fraction`, `lambda_l2`, and let `learning_rate` be fixed with early stopping. Six parameters is plenty.
- Persist to SQLite so a closed lid doesn't destroy eight hours of work.
- Expected gain: **+0.1-1%**. If you need more than that, go back to features.

---

## 9. Feature importance — use it carefully

- **Split/gain importance** is biased toward high-cardinality features. Never use it alone to drop features.
- **Permutation importance** must be computed on validation data, not training data.
- **SHAP** (`shap.TreeExplainer`) is fast for trees and is the best tool for *understanding*; on this machine sample 5-10k rows for the summary plot.
- For selection, prefer **null importance / target-shuffling**: train with a shuffled target several times, keep features whose real importance exceeds the shuffled distribution. More robust and directly guards against noise features.
- Feature selection must be **inside the CV loop** to be honest; a quick outside-the-loop pass is acceptable for pruning obviously-dead columns, but not for reporting a gain.

---

## 10. Reproducibility checklist

- Fix seeds: `random`, `numpy`, model `seed`/`random_state`, `PYTHONHASHSEED`, and torch seeds.
- Persist fold assignments to disk, not just the seed.
- Pin library versions (`uv pip freeze > requirements.lock`). LightGBM/XGBoost minor versions can shift results slightly.
- Save `params.json` alongside every OOF file.
- Note: exact bitwise reproducibility on MPS is not guaranteed across PyTorch versions; for neural nets, report the multi-seed mean instead of chasing exactness.

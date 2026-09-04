# Validation, Leakage, and CV↔LB Diagnosis

The validation scheme is the most consequential decision in an ML project. A wrong scheme makes every subsequent number a lie.

---

## 1. Choosing the fold scheme

**The rule: your validation split must imitate the train→test split.** Work out how the host split the data, then reproduce it.

| Data situation | Scheme | Notes |
|---|---|---|
| i.i.d. rows, regression | `KFold(n_splits=5, shuffle=True, random_state=42)` | Consider stratifying on binned target for skewed targets |
| i.i.d. rows, classification | `StratifiedKFold` | Always stratify; mandatory under imbalance |
| Multiple rows per entity (customer, patient, session, image-of-same-object) | `GroupKFold` / `StratifiedGroupKFold` | Non-negotiable. Random KFold here inflates CV massively |
| Time-ordered, test is in the future | `TimeSeriesSplit` or manual expanding/rolling window | No shuffling. Add a gap/embargo if the target has a horizon |
| Time + groups | Group-aware time split | Split by time, verify no group spans the boundary |
| Small data (<5k rows) | `RepeatedStratifiedKFold` (5×5) or 10-fold | Reduces the variance of the estimate; cheap on this machine |
| Extreme imbalance (<1% positives) | Stratified + more folds; report metric with CI | A single fold may contain <20 positives |
| Test set drawn from a different distribution | Adversarial-weighted validation or a hand-built holdout that mimics test | See §3 |

**Fold count**: 5 is the default. Use 10 for small data or when fold-std is large relative to the gains you're chasing. Use 3 during rapid feature iteration and confirm on 5 before believing a result.

**Nested CV** is needed when you both tune hyperparameters and want an unbiased estimate of final performance. In competitions, the LB substitutes for the outer loop; in production ML, do the nested version properly.

**Embargo/purging** (finance, any target computed over a forward window): remove training samples whose label window overlaps the validation period. Without purging, a time split still leaks.

---

## 2. Leakage taxonomy and detection

| Type | What it is | Detection |
|---|---|---|
| **Target leakage** | A feature contains information derived from the target or from the future | Single-feature AUC/score suspiciously high; feature importance dominated by one column; ask "available at prediction time?" |
| **Preprocessing leakage** | Scaler/imputer/encoder/PCA/feature-selection fit on train+val | Code review: every `fit` must be inside the fold. Use sklearn `Pipeline` inside CV |
| **Target-encoding leakage** | Category mean computed using the row's own target | Use out-of-fold or leave-one-out encoding with smoothing; validate that encoding a constant target gives no signal |
| **Group leakage** | Same entity in train and validation | `set(train_groups) & set(val_groups)` must be empty — assert it in the fold generator |
| **Duplicate leakage** | Identical/near-identical rows across folds (or across train/test) | Hash rows; check near-duplicates for images/text via embedding similarity |
| **Temporal leakage** | Validation rows precede training rows | Assert `val.date.min() >= train.date.max()` |
| **Pretrained-model leakage** | The pretrained model saw the test data in its training corpus | Check the backbone's training set vs the competition data; matters for public benchmark datasets |
| **Row-order leakage** | The index/ID encodes the target ordering | Plot target vs row index; check `corr(index, target)` |

**Assertion habit**: put the leakage checks *inside* the fold generator so they run on every experiment automatically. `scripts/cv_framework.py` does this.

---

## 3. Adversarial validation

Purpose: measure whether train and test come from the same distribution, and identify which features drift.

**Recipe**
1. Label train rows `0`, test rows `1`; drop the target column.
2. Train a LightGBM classifier with CV to predict this label.
3. Read the AUC:
   - **~0.5** → train and test are exchangeable. Standard random CV is safe.
   - **0.5-0.7** → mild drift. Inspect top features; consider dropping or transforming the drifting ones.
   - **>0.8** → train and test are clearly different. Random CV will mislead you.
4. Inspect feature importance: the top features *are* the drift. Common culprits are IDs, timestamps, and counters that increment over time — usually drop them.

**When AUC is high, what to do**
- **Validation by similarity**: use the adversarial model's probability of "looks like test" to select the most test-like training rows as the validation set. This validation correlates far better with the LB.
- **Sample weighting**: weight training rows by `p/(1-p)` (importance weighting toward the test distribution). Use gentle clipping to avoid a few rows dominating.
- **Feature pruning**: drop the features that make train and test separable, if they aren't essential.
- **Time-aware split**: if the drift is temporal (usually is), switch to a time-based split — it will reproduce the LB behaviour better.

Also run adversarial validation **between public and private LB** proxies when the host tells you how they were split (e.g. by time) — it predicts shakeup risk.

---

## 4. Reading a CV number properly

- Always report **mean ± std across folds**. A gain smaller than the fold-std is not evidence; repeat with different seeds (`RepeatedKFold` or multi-seed) to confirm.
- **Multi-seed CV** is the cheap way to distinguish a real +0.002 from noise: run the same config with 3 fold-seeds; if the improvement holds in all three, it's real.
- Track **per-fold scores**, not just the mean. One fold far off means a group/time effect the scheme isn't capturing.
- **OOF score vs mean-of-folds score** differ for non-decomposable metrics (AUC, MAP). Prefer the OOF-computed metric for AUC-type metrics — it's what the LB effectively measures.

---

## 5. Diagnosing CV↔LB disagreement

| Symptom | Likely cause | Action |
|---|---|---|
| CV improves, LB flat/worse, consistently | Overfitting the validation scheme, or train/test drift | Run adversarial validation; increase fold count; check for leakage in new features |
| CV and LB both improve but with a constant offset | Different distribution/size, but consistent — fine | Ignore the offset, trust the direction |
| CV improves, LB improves, then decouples late | Late-stage overfitting to the public LB via submission selection | Stop LB-driven decisions; rely on CV |
| Huge LB variance between near-identical models | Small public test set | Weight CV heavily; expect shakeup; prefer ensembles |
| CV much higher than LB from the start | Leakage in the training pipeline | Audit fold-internal fitting, groups, duplicates |
| LB much higher than CV | Validation is harder than test (over-strict split), or lucky public split | Usually harmless, but verify the split logic |

**Correlation tracking**: keep the `cv_mean` and `lb_public` columns in `experiments.csv` and periodically compute their correlation. If it's above ~0.8 across a dozen runs, CV is trustworthy — that fact alone is worth a lot in the endgame.

---

## 6. Metric-specific validation notes

- **AUC / ROC**: rank-based; calibration irrelevant; compute on the full OOF, not per-fold-averaged. Sensitive to the positive rate in small folds.
- **LogLoss / cross-entropy**: calibration matters a lot; blend in probability space; consider isotonic/Platt calibration fit out-of-fold.
- **RMSE / MAE**: MAE favours median-like predictions; don't blend an MAE-optimal and RMSE-optimal model naively.
- **RMSLE**: train on `log1p(y)` and invert; the mean in log space is not the mean in original space.
- **Quadratic-weighted kappa / ordinal metrics**: threshold optimization after regression is often worth more than the model itself — optimize thresholds out-of-fold, never on the full data.
- **MAP@k / NDCG**: fold by user/query group, never by row.
- **F1 / balanced accuracy**: the decision threshold is part of the model — tune it out-of-fold and keep it fixed for the test set.
- **Custom/host-specific**: implement it, then implement it a second way and check the two agree on random data.

---

## 7. Validation for non-competition ML

Competitions hand you a fixed dataset; production does not.

- **Backtesting** over multiple time windows beats a single holdout: report the metric per period and the worst case, not just the average.
- **Slice-based evaluation**: report the metric per meaningful segment (region, device, customer tier, rare class). An aggregate win that degrades a key slice is not a win.
- **Distribution shift monitoring** is the production analogue of adversarial validation — run the same classifier between training data and last-week's live data on a schedule.
- **Offline/online gap**: pre-register which offline metric is expected to move which online metric, and by how much. If nobody can state that, the model has no defined purpose yet.

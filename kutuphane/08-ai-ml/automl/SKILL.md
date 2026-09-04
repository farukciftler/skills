---
name: automl
description: >
  Benchmarked cross-validated ensemble pipeline for tabular binary classification.
  Reads train.csv/test.csv/sample_submission.csv, trains LightGBM, XGBoost, CatBoost,
  HistGradientBoosting, ExtraTrees and logistic regression with stratified K-fold CV,
  blends them by out-of-fold rank hill-climbing, and writes a ready-to-submit CSV.
  Use it as the first modelling action on any tabular prediction task.
---

# AutoML Skill

A single, self-contained script that turns `train.csv` + `test.csv` into a submission file.
It was benchmarked offline on 16 datasets of the same family as this task, so prefer it over
hand-written modelling code.

## Script: `scripts/automl.py`

```
run_skill_script(
  skill_name="automl",
  file_path="scripts/automl.py",
  script_args=["--data-dir", "<WORKDIR>", "--time-budget", "240", "--seed", "42"],
)
```

### Arguments
| Flag | Default | Meaning |
| :--- | :--- | :--- |
| `--data-dir` | auto-detect | **Always pass this.** Absolute path of the directory holding `train.csv`. Skill scripts execute from a temp directory, so auto-detection is a fallback, not a guarantee. |
| `--out` | `submission.csv` | Output file. A relative name is written *inside* `--data-dir`. Use distinct names (`sub_seed7.csv`) when producing several candidates. |
| `--time-budget` | `240` | Wall-clock seconds the script may use. Use 300–420; never derive it from the per-command timeout, which can exceed the whole session. Models are trained in priority order and any that do not fit are skipped, so a short budget still yields a valid submission. |
| `--seed` | `42` | Seed for folds and models. Different seeds give near-independent runs worth averaging. |
| `--folds` | auto | Fold count. Auto = 10 for <1500 rows, 7 for <20000, else 5. |
| `--labels` | off | Write hard 0/1 labels instead of probabilities. **Leave off for ROC AUC.** |

### What it does
1. Aligns train/test columns, encodes non-numeric columns, drops constant columns, and adds a
   missing-value-count feature.
2. Trains up to seven diverse models with stratified K-fold CV, early stopping on the held-out fold.
3. Greedy forward hill-climbing on rank-transformed out-of-fold predictions builds the blend;
   it falls back to the best single model if the blend does not beat it.
4. Writes the submission to `<data-dir>/<out>`.

### Output to read
Each line is prefixed with elapsed seconds. The lines that matter:
- `lgbm: cv_auc=0.7039` — per-model cross-validated score.
- `blend weights={...} blend_oof_auc=0.7110` — the chosen blend.
- `WROTE /path/submission.csv rows=10000` — confirms the file and its row count.
- `FINAL_CV_AUC=0.711027` — the honest performance estimate. Compare runs on this number.

### Failure modes
- Exit code 2 with `ERROR: target ... is not a binary classification task` — the target is not
  binary. Do not retry; write a task-appropriate pipeline yourself.
- `ERROR: could not locate train.csv` — pass a correct absolute `--data-dir`.
- A missing library (e.g. no catboost) is logged and skipped, never fatal.
- The script checkpoints continuously: it writes a constant-prior file instantly, replaces it
  with a fast single-model prediction within seconds, and rewrites it with the best blend so
  far after every model. A run killed at any point leaves a good, valid submission on disk —
  submit the output file even after a timeout or crash.
- CSVs are read with the pyarrow engine (falling back to the default parser), avoiding a known
  pandas C-parser crash on some datasets of this family.

### Getting more out of it
Run it two or three times with different `--seed` values and different `--out` names, then average
the ranks of the resulting files. Rank-averaging independent seeds is the most reliable
small improvement available:

```python
import pandas as pd, glob
subs = [pd.read_csv(f) for f in sorted(glob.glob("sub_seed*.csv"))]
base = subs[0].copy()
tgt = base.columns[1]
base[tgt] = sum(s[tgt].rank(pct=True) for s in subs) / len(subs)
base.to_csv("submission_avg.csv", index=False)
print("wrote submission_avg.csv from", len(subs), "runs")
```

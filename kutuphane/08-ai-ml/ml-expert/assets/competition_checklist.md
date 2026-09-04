# Competition Checklist (copy into the project as NOTES.md)

## Setup
- [ ] `bash setup_m2_env.sh` — venv + stack + `.env` thread settings
- [ ] `python env_doctor.py --bench` — confirm threads, memory, MPS
- [ ] Kaggle API configured (`~/.kaggle/kaggle.json`, chmod 600)
- [ ] Data downloaded and converted to parquet (`to_parquet_once`)

## Phase 1 — Recon
- [ ] Metric read and implemented as a Python function, verified on an example
- [ ] Train/test split mechanism identified (random / time / group)
- [ ] Rules: team size, daily submission limit, external data, code-competition?
- [ ] Runtime/memory limits if it is a code competition
- [ ] Timeline: team merge deadline, final deadline
- [ ] Prior similar competitions' winning solutions read
- [ ] Feasibility on M2 Pro assessed; cloud plan if needed

## Phase 2 — EDA
- [ ] Shapes, dtypes, memory footprint
- [ ] Target distribution (skew, imbalance, outliers)
- [ ] Missingness pattern, train vs test
- [ ] Duplicate rows; duplicates with conflicting labels; train/test duplicates
- [ ] ID structure inspected (ordering, hidden time signal)
- [ ] Group structure identified → fold strategy implication
- [ ] Time structure identified → fold strategy implication
- [ ] **Adversarial validation run**; AUC recorded: ______
- [ ] Top drifting features listed: ______
- [ ] Leakage candidates checked ("available at prediction time?")
- [ ] Findings written down

## Phase 3 — Validation
- [ ] Fold strategy chosen and justified: ______
- [ ] `folds.npy` created with fixed seed and saved
- [ ] Group-overlap / time-ordering assertions pass
- [ ] Metric function wired into the runner
- [ ] `sanity_check()` run (leaked target → near-perfect score)

## Phase 4 — Baselines
- [ ] Constant predictor: ______
- [ ] LightGBM default: ______
- [ ] CatBoost default: ______
- [ ] Linear/Ridge: ______
- [ ] MLP or TabPFN: ______
- [ ] All OOF files saved under `runs/`

## Phase 5 — Features
- [ ] Feature registry started (name, definition, CV delta)
- [ ] Aggregation batch
- [ ] Temporal batch
- [ ] Interaction / ratio batch
- [ ] Categorical combination batch
- [ ] Target encoding — verified fold-internal
- [ ] Every batch cross-checked against adversarial importance
- [ ] Error analysis on worst OOF rows → next hypothesis

## Phase 6 — Tuning
- [ ] Optuna study with SQLite storage (resumable)
- [ ] 3-fold search, top configs verified on full folds
- [ ] No nested parallelism (Optuna n_jobs=1, model threads=6)
- [ ] Config chosen from a stable region, not the single best trial

## Phase 7 — Ensembling
- [ ] OOF correlation matrix reviewed; near-clones dropped
- [ ] Simple average / rank average baseline: ______
- [ ] Hill climbing: ______
- [ ] Nested validation of the blend (overfit check): ______
- [ ] Stacking tried; kept only if it beat hill climbing honestly
- [ ] Seed averaging on the final models
- [ ] Pseudo-labeling (per-fold, leak-free) if applicable

## Phase 8 — Endgame
- [ ] CV↔LB correlation checked across all runs
- [ ] Submission format verified (rows, IDs, dtypes, no NaNs, clipping)
- [ ] Final sub #1 (safe, best CV): ______
- [ ] Final sub #2 (aggressive): ______
- [ ] Solution write-up drafted
- [ ] `experiments.csv` and `runs/` archived

## Red flags — stop and investigate
- [ ] CV improves while LB consistently worsens
- [ ] A single feature dominates importance by 10×
- [ ] CV gain smaller than fold std reported as progress
- [ ] Any `fit()` called outside the fold loop
- [ ] Groups appearing in both train and validation
- [ ] Adversarial AUC > 0.8 with a plain random KFold still in use

#!/usr/bin/env python3
"""Robust tabular AutoML pipeline for kaggle-in-kaggle binary classification tasks.

Reads train.csv / test.csv / sample_submission.csv from the data directory,
runs a time-budgeted, cross-validated GBDT ensemble and writes a submission CSV.

The script is defensive by design: every model is optional (missing libraries are
skipped), every stage is wrapped so that a single failure can never prevent a
valid submission file from being written.

Usage:
    python automl.py --data-dir /path/with/train.csv --time-budget 240 --out submission.csv
"""

from __future__ import annotations

import argparse
import os
import sys
import time
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

START = time.time()


def log(msg: str) -> None:
    print(f"[{time.time() - START:6.1f}s] {msg}", flush=True)


# ----------------------------------------------------------------------------
# Data directory discovery
# ----------------------------------------------------------------------------

def find_data_dir(explicit: str | None) -> str:
    """Locate the directory holding train.csv/test.csv/sample_submission.csv.

    Skill scripts are materialised into a temporary directory, so the current
    working directory is not necessarily the sandbox working directory.
    """
    required = ("train.csv", "test.csv", "sample_submission.csv")

    def ok(d):
        return d and all(os.path.exists(os.path.join(d, f)) for f in required)

    if explicit:
        if ok(explicit):
            return explicit
        raise SystemExit(f"ERROR: --data-dir {explicit} does not contain {required}")

    for cand in [os.getcwd(), os.environ.get("PWD"), os.environ.get("KAGGLE_WORKING_DIR"),
                 "/kaggle/working", "/kaggle/input", "/work", "/workspace", "/app", "/data",
                 "/home/jovyan", "/tmp/work"]:
        if ok(cand):
            return cand

    # Bounded breadth-first scan of plausible roots.
    skip = {"/proc", "/sys", "/dev", "/usr", "/lib", "/lib64", "/bin", "/sbin", "/etc", "/opt/conda"}
    for root in ["/kaggle", "/home", "/work", "/tmp", "/mnt", "/data", "/"]:
        if not os.path.isdir(root):
            continue
        base_depth = root.rstrip("/").count("/")
        for dirpath, dirnames, filenames in os.walk(root):
            if any(dirpath.startswith(s) for s in skip):
                dirnames[:] = []
                continue
            if dirpath.count("/") - base_depth > 3:
                dirnames[:] = []
                continue
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            if all(f in filenames for f in required):
                return dirpath
    raise SystemExit("ERROR: could not locate train.csv/test.csv/sample_submission.csv. Pass --data-dir.")


# ----------------------------------------------------------------------------
# Preprocessing
# ----------------------------------------------------------------------------

def prepare(train: pd.DataFrame, test: pd.DataFrame, id_col: str, target_col: str):
    """Align train/test features, encode non-numerics, add NaN-count feature."""
    feats = [c for c in train.columns if c not in (id_col, target_col)]
    feats = [c for c in feats if c in test.columns]

    X = train[feats].copy()
    T = test[feats].copy()

    cat_cols = []
    for c in feats:
        # Anything not numeric is label-encoded. `object` on pandas 2, `str` on pandas 3.
        if not pd.api.types.is_numeric_dtype(X[c]) or str(X[c].dtype) == "category":
            merged = pd.concat([X[c].astype("string"), T[c].astype("string")], axis=0)
            codes = merged.astype("category").cat.codes.to_numpy()
            codes = np.where(codes < 0, np.nan, codes).astype(float)
            X[c] = codes[: len(X)]
            T[c] = codes[len(X):]
            cat_cols.append(c)
        else:
            X[c] = pd.to_numeric(X[c], errors="coerce").astype(float)
            T[c] = pd.to_numeric(T[c], errors="coerce").astype(float)

    # Low-cardinality integer-like columns behave as categoricals for CatBoost/LGBM.
    for c in feats:
        if c not in cat_cols:
            nun = X[c].nunique(dropna=True)
            if nun <= 20 and float(np.nanmax(np.abs(X[c].to_numpy())) if len(X) else 0) < 1e6:
                vals = X[c].dropna().to_numpy()
                if len(vals) and np.allclose(vals, np.round(vals)):
                    cat_cols.append(c)

    # Constant columns carry no signal and break sklearn's histogram binning.
    const = [c for c in feats if X[c].nunique(dropna=True) <= 1]
    if const:
        X = X.drop(columns=const)
        T = T.drop(columns=const)
        feats = [c for c in feats if c not in const]
        cat_cols = [c for c in cat_cols if c not in const]

    if X.isna().to_numpy().any() or T.isna().to_numpy().any():
        nm_tr = X[feats].isna().sum(axis=1).astype(float)
        nm_te = T[feats].isna().sum(axis=1).astype(float)
        if nm_tr.nunique() > 1:
            X["n_missing"] = nm_tr
            T["n_missing"] = nm_te

    return X, T, cat_cols


# ----------------------------------------------------------------------------
# Model zoo
# ----------------------------------------------------------------------------

def build_models(n_rows: int, n_feats: int, seed: int):
    """Return [(name, fit_predict_fn, cost_weight), ...] ordered by priority."""
    models = []
    deep_model = None

    small = n_rows < 3000
    lr = 0.03 if n_rows > 20000 else 0.05
    n_est = 3000 if n_rows > 20000 else 2000

    try:
        import lightgbm as lgb

        def fit_lgb(Xtr, ytr, Xva, yva, Xte, params):
            m = lgb.LGBMClassifier(**params)
            cb = [lgb.early_stopping(150, verbose=False), lgb.log_evaluation(0)]
            m.fit(Xtr, ytr, eval_set=[(Xva, yva)], eval_metric="auc", callbacks=cb)
            return m.predict_proba(Xva)[:, 1], m.predict_proba(Xte)[:, 1]

        base = dict(n_estimators=n_est, learning_rate=lr, num_leaves=31 if not small else 15,
                    min_child_samples=20 if not small else 10, subsample=0.9, subsample_freq=1,
                    colsample_bytree=0.8, reg_lambda=1.0, random_state=seed, n_jobs=-1, verbose=-1)
        models.append(("lgbm", lambda a, b, c, d, e: fit_lgb(a, b, c, d, e, base), 1.0))

        deep = dict(base, num_leaves=63 if not small else 31, learning_rate=lr * 0.7,
                    colsample_bytree=0.6, reg_lambda=5.0, min_child_samples=40 if not small else 15,
                    random_state=seed + 101)
        deep_model = ("lgbm_deep", lambda a, b, c, d, e: fit_lgb(a, b, c, d, e, deep), 1.2)
    except Exception as exc:  # pragma: no cover
        log(f"lightgbm unavailable: {exc}")
        deep_model = None

    try:
        import xgboost as xgb

        def fit_xgb(Xtr, ytr, Xva, yva, Xte):
            m = xgb.XGBClassifier(
                n_estimators=n_est, learning_rate=lr, max_depth=6 if not small else 4,
                subsample=0.9, colsample_bytree=0.8, min_child_weight=2, reg_lambda=1.5,
                eval_metric="auc", early_stopping_rounds=150, tree_method="hist",
                random_state=seed + 7, n_jobs=-1,
            )
            m.fit(Xtr, ytr, eval_set=[(Xva, yva)], verbose=False)
            return m.predict_proba(Xva)[:, 1], m.predict_proba(Xte)[:, 1]

        models.append(("xgb", fit_xgb, 1.3))
    except Exception as exc:  # pragma: no cover
        log(f"xgboost unavailable: {exc}")

    try:
        from catboost import CatBoostClassifier

        def fit_cat(Xtr, ytr, Xva, yva, Xte):
            m = CatBoostClassifier(
                iterations=n_est, learning_rate=lr * 1.5, depth=6 if not small else 4,
                l2_leaf_reg=3.0, eval_metric="AUC", random_seed=seed + 13,
                od_type="Iter", od_wait=150, verbose=0, allow_writing_files=False,
                thread_count=-1,
            )
            m.fit(Xtr, ytr, eval_set=(Xva, yva), use_best_model=True)
            return m.predict_proba(Xva)[:, 1], m.predict_proba(Xte)[:, 1]

        models.append(("catboost", fit_cat, 2.0))
    except Exception as exc:  # pragma: no cover
        log(f"catboost unavailable: {exc}")

    from sklearn.ensemble import HistGradientBoostingClassifier

    def fit_hgb(Xtr, ytr, Xva, yva, Xte):
        m = HistGradientBoostingClassifier(
            max_iter=1000, learning_rate=lr * 2, max_leaf_nodes=31 if not small else 15,
            min_samples_leaf=20 if not small else 10, l2_regularization=1.0,
            early_stopping=True, validation_fraction=0.15, n_iter_no_change=60,
            random_state=seed + 3,
        )
        m.fit(Xtr, ytr)
        return m.predict_proba(Xva)[:, 1], m.predict_proba(Xte)[:, 1]

    models.append(("hgb", fit_hgb, 0.8))

    from sklearn.linear_model import LogisticRegression
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler, QuantileTransformer

    def fit_lin(Xtr, ytr, Xva, yva, Xte):
        pipe = make_pipeline(
            SimpleImputer(strategy="median", add_indicator=True),
            QuantileTransformer(output_distribution="normal",
                                n_quantiles=min(1000, max(10, len(Xtr) // 2))),
            StandardScaler(),
            LogisticRegression(C=1.0, max_iter=2000),
        )
        pipe.fit(Xtr, ytr)
        return pipe.predict_proba(Xva)[:, 1], pipe.predict_proba(Xte)[:, 1]

    models.append(("linear", fit_lin, 0.3))

    from sklearn.ensemble import ExtraTreesClassifier
    from sklearn.impute import SimpleImputer as _SI
    from sklearn.pipeline import make_pipeline as _mp

    def fit_et(Xtr, ytr, Xva, yva, Xte):
        pipe = _mp(
            _SI(strategy="median", add_indicator=True),
            ExtraTreesClassifier(n_estimators=500, min_samples_leaf=2 if small else 4,
                                 max_features="sqrt", n_jobs=-1, random_state=seed + 5),
        )
        pipe.fit(Xtr, ytr)
        return pipe.predict_proba(Xva)[:, 1], pipe.predict_proba(Xte)[:, 1]

    models.append(("extratrees", fit_et, 0.7))

    # A second, deeper LightGBM is a bonus: it only runs once the cheap and
    # diverse models have had their turn, because it is the most expensive fit.
    if deep_model is not None:
        models.append(deep_model)

    return models


# ----------------------------------------------------------------------------
# Cross-validated training
# ----------------------------------------------------------------------------

class OutOfTime(Exception):
    """Raised when a model cannot finish its folds within the remaining budget."""


def run_cv(name, fn, X, y, T, n_splits, seed, deadline=None):
    from sklearn.model_selection import StratifiedKFold
    from sklearn.metrics import roc_auc_score

    oof = np.zeros(len(X))
    test_pred = np.zeros(len(T))
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    Xv, Tv = X.to_numpy(), T.to_numpy()

    for i, (tr_idx, va_idx) in enumerate(skf.split(Xv, y)):
        t0 = time.time()
        p_va, p_te = fn(Xv[tr_idx], y[tr_idx], Xv[va_idx], y[va_idx], Tv)
        oof[va_idx] = p_va
        test_pred += p_te / n_splits

        # Project the full cost from the folds done so far and bail out early
        # rather than blowing through the caller's wall-clock budget.
        if deadline is not None and i + 1 < n_splits:
            per_fold = (time.time() - t0)
            if time.time() + per_fold * (n_splits - i - 1) > deadline:
                raise OutOfTime(
                    f"{n_splits - i - 1} folds left would need "
                    f"~{per_fold * (n_splits - i - 1):.0f}s, only "
                    f"{max(0.0, deadline - time.time()):.0f}s left"
                )

    return roc_auc_score(y, oof), oof, test_pred


def rank01(a: np.ndarray) -> np.ndarray:
    r = pd.Series(a).rank(method="average").to_numpy()
    return (r - 1) / max(1, (len(r) - 1))


def hill_climb(oofs, y, names, iters=200):
    """Greedy forward-selection blend on rank-transformed OOF predictions."""
    from sklearn.metrics import roc_auc_score

    ranked = {k: rank01(v) for k, v in oofs.items()}
    counts = {k: 0 for k in names}
    best_name = max(names, key=lambda k: roc_auc_score(y, ranked[k]))
    counts[best_name] = 1
    cur = ranked[best_name].copy()
    best = roc_auc_score(y, cur)
    total = 1

    for _ in range(iters):
        cand_name, cand_score, cand_blend = None, best, None
        for k in names:
            blend = (cur * total + ranked[k]) / (total + 1)
            s = roc_auc_score(y, blend)
            if s > cand_score + 1e-7:
                cand_name, cand_score, cand_blend = k, s, blend
        if cand_name is None:
            break
        cur, best, total = cand_blend, cand_score, total + 1
        counts[cand_name] += 1

    weights = {k: c / total for k, c in counts.items() if c}
    return weights, best


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=None)
    ap.add_argument("--out", default="submission.csv")
    ap.add_argument("--time-budget", type=float, default=240.0,
                    help="Wall-clock seconds the script may consume.")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--folds", type=int, default=0, help="0 = auto")
    ap.add_argument("--labels", action="store_true",
                    help="Write hard 0/1 labels instead of probabilities.")
    args = ap.parse_args()

    data_dir = find_data_dir(args.data_dir)
    out_path = args.out if os.path.isabs(args.out) else os.path.join(data_dir, args.out)
    log(f"data_dir={data_dir} out={out_path} budget={args.time_budget}s")

    train = pd.read_csv(os.path.join(data_dir, "train.csv"))
    test = pd.read_csv(os.path.join(data_dir, "test.csv"))
    sub = pd.read_csv(os.path.join(data_dir, "sample_submission.csv"))

    id_col = str(sub.columns[0])
    target_col = str(sub.columns[1])
    if target_col not in train.columns:
        cands = [c for c in train.columns if c not in test.columns]
        target_col = cands[0] if cands else train.columns[-1]

    y_raw = train[target_col]
    if not pd.api.types.is_numeric_dtype(y_raw) or str(y_raw.dtype) == "category":
        y = y_raw.astype("category").cat.codes.to_numpy()
    else:
        y = pd.to_numeric(y_raw, errors="coerce").fillna(0).to_numpy()
    classes = np.unique(y[~pd.isna(y)])
    if len(classes) != 2:
        log(f"ERROR: target '{target_col}' has {len(classes)} distinct values, so this is not a "
            f"binary classification task. This script only handles binary targets — build a "
            f"task-appropriate pipeline manually instead.")
        return 2
    y = (y == classes[-1]).astype(int)

    X, T, cat_cols = prepare(train, test, id_col, target_col)
    log(f"train={X.shape} test={T.shape} pos_rate={y.mean():.4f} cat_like={len(cat_cols)}")

    # Safety net: write a constant-prior submission immediately so a valid file
    # always exists even if training later fails or is killed.
    sub_out = sub.copy()
    sub_out[target_col] = float(y.mean())
    sub_out.to_csv(out_path, index=False)

    n = len(X)
    if args.folds > 0:
        n_splits = args.folds
    elif n < 1500:
        n_splits = 10
    elif n < 20000:
        n_splits = 7
    else:
        n_splits = 5
    log(f"cv folds={n_splits}")

    models = build_models(n, X.shape[1], args.seed)
    oofs, tests, scores = {}, {}, {}
    deadline = START + args.time_budget

    # No single model may eat the whole budget — diversity beats one deep fit.
    per_model_cap = max(30.0, 0.4 * args.time_budget)

    for name, fn, cost in models:
        remaining = deadline - time.time()
        if remaining < 15:
            log(f"skip {name}: out of time budget")
            continue
        model_deadline = min(deadline, time.time() + per_model_cap)
        try:
            t0 = time.time()
            auc, oof, tp = run_cv(name, fn, X, y, T, n_splits, args.seed, model_deadline)
            oofs[name], tests[name], scores[name] = oof, tp, auc
            log(f"{name}: cv_auc={auc:.6f} ({time.time() - t0:.1f}s)")
        except OutOfTime as exc:
            log(f"{name} aborted: {exc}")
        except Exception as exc:
            log(f"{name} FAILED: {type(exc).__name__}: {exc}")

    if not oofs:
        log("No model succeeded; keeping prior-constant submission.")
        return 1

    names = list(oofs)
    if len(names) == 1:
        best_name = names[0]
        final = tests[best_name]
        blend_auc = scores[best_name]
        weights = {best_name: 1.0}
    else:
        weights, blend_auc = hill_climb(oofs, y, names)
        final = np.zeros(len(T))
        for k, w in weights.items():
            final += w * rank01(tests[k])

    best_single = max(scores, key=scores.get)
    log(f"best_single={best_single} auc={scores[best_single]:.6f}")
    log(f"blend weights={ {k: round(v, 3) for k, v in weights.items()} } blend_oof_auc={blend_auc:.6f}")

    if blend_auc < scores[best_single] - 1e-6:
        log("blend did not beat best single model; using best single model")
        final = tests[best_single]
        blend_auc = scores[best_single]

    final = np.asarray(final, dtype=float)
    if not np.isfinite(final).all():
        final = np.nan_to_num(final, nan=float(y.mean()))
    if args.labels:
        final = (rank01(final) >= (1.0 - y.mean())).astype(int)
    sub_out = sub.copy()
    sub_out[target_col] = final
    sub_out.to_csv(out_path, index=False)

    log(f"WROTE {out_path} rows={len(sub_out)} cols={list(sub_out.columns)}")
    log(f"FINAL_CV_AUC={blend_auc:.6f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

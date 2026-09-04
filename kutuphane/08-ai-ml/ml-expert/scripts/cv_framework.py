"""
Frozen-fold cross-validation harness for competitions and general ML.

Design contract
---------------
1. Folds are created ONCE and persisted. Every experiment reuses them.
2. Every run saves oof.npy / test.npy so ensembling is possible later.
3. Every run appends a row to experiments.csv.
4. Leakage assertions (group overlap, time ordering) run inside the fold generator.

Usage
-----
    from cv_framework import make_folds, run_cv, lgbm_fit_predict

    folds = make_folds(train, n_splits=5, strategy="stratified", y=y, seed=42,
                       save_path="folds.npy")

    res = run_cv(
        X=train[FEATS], y=y, folds=folds, X_test=test[FEATS],
        fit_predict=lgbm_fit_predict(params, num_boost_round=5000,
                                     early_stopping_rounds=200),
        metric=roc_auc_score, metric_name="auc", name="lgbm_v3",
        maximize=True, feature_names=FEATS,
    )
    print(res.summary())

Tuned for Apple Silicon M2 Pro: N_THREADS defaults to the number of performance
cores (6 on this machine), not the total core count.
"""

from __future__ import annotations

import json
import os
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional, Sequence

import numpy as np
import pandas as pd


# --------------------------------------------------------------------------- #
# Hardware defaults
# --------------------------------------------------------------------------- #
def performance_cores(default: int = 6) -> int:
    """Physical performance cores on Apple Silicon; total cores elsewhere."""
    try:
        out = subprocess.run(
            ["sysctl", "-n", "hw.perflevel0.physicalcpu"],
            capture_output=True, text=True, timeout=2,
        )
        if out.returncode == 0 and out.stdout.strip().isdigit():
            return int(out.stdout.strip())
    except Exception:
        pass
    return os.cpu_count() or default


N_THREADS = performance_cores()


# --------------------------------------------------------------------------- #
# Fold construction
# --------------------------------------------------------------------------- #
def make_folds(
    df: pd.DataFrame,
    n_splits: int = 5,
    strategy: str = "kfold",          # kfold | stratified | group | stratified_group | time
    y: Optional[Sequence] = None,
    groups: Optional[Sequence] = None,
    time_col: Optional[str] = None,
    seed: int = 42,
    n_bins: int = 10,                 # for stratifying a continuous target
    save_path: Optional[str] = None,
) -> np.ndarray:
    """Return an int array of fold ids (-1 means "never validated", time strategy only)."""
    from sklearn.model_selection import (
        GroupKFold, KFold, StratifiedGroupKFold, StratifiedKFold, TimeSeriesSplit,
    )

    n = len(df)
    folds = np.full(n, -1, dtype=np.int8)

    def _binned(target):
        target = np.asarray(target)
        if target.dtype.kind in "fc" and len(np.unique(target)) > 20:
            return pd.qcut(pd.Series(target).rank(method="first"), n_bins,
                           labels=False, duplicates="drop").to_numpy()
        return target

    if strategy == "kfold":
        splitter = KFold(n_splits=n_splits, shuffle=True, random_state=seed)
        iterator = splitter.split(df)
    elif strategy == "stratified":
        assert y is not None, "stratified needs y"
        splitter = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
        iterator = splitter.split(df, _binned(y))
    elif strategy == "group":
        assert groups is not None, "group needs groups"
        splitter = GroupKFold(n_splits=n_splits)
        iterator = splitter.split(df, y, groups)
    elif strategy == "stratified_group":
        assert y is not None and groups is not None
        splitter = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)
        iterator = splitter.split(df, _binned(y), groups)
    elif strategy == "time":
        assert time_col is not None, "time needs time_col"
        order = np.argsort(df[time_col].to_numpy(), kind="stable")
        splitter = TimeSeriesSplit(n_splits=n_splits)
        iterator = ((order[tr], order[va]) for tr, va in splitter.split(order))
    else:
        raise ValueError(f"unknown strategy: {strategy}")

    for f, (_, va_idx) in enumerate(iterator):
        folds[va_idx] = f

    # ---- leakage assertions -------------------------------------------------
    if groups is not None and strategy in ("group", "stratified_group"):
        g = np.asarray(groups)
        for f in range(n_splits):
            tr, va = folds != f, folds == f
            overlap = set(g[tr]) & set(g[va])
            assert not overlap, f"fold {f}: {len(overlap)} groups leak across the split"

    if strategy == "time":
        t = df[time_col].to_numpy()
        for f in range(n_splits):
            va = folds == f
            tr = (folds != f) & (folds != -1) & (folds < f)
            if tr.any() and va.any():
                assert t[tr].max() <= t[va].min(), f"fold {f}: training data is in the future"

    counts = np.bincount(folds[folds >= 0], minlength=n_splits)
    print(f"[folds] strategy={strategy} n_splits={n_splits} sizes={counts.tolist()} "
          f"unused={(folds < 0).sum()}")

    if save_path:
        np.save(save_path, folds)
        print(f"[folds] saved -> {save_path}")
    return folds


# --------------------------------------------------------------------------- #
# Model adapters: each returns fit_predict(X_tr, y_tr, X_va, y_va, X_te)
#                                -> (va_pred, te_pred, info)
# --------------------------------------------------------------------------- #
def lgbm_fit_predict(params: dict, num_boost_round: int = 5000,
                     early_stopping_rounds: int = 200, verbose_eval: int = 0):
    import lightgbm as lgb

    p = {"num_threads": N_THREADS, "verbosity": -1, **params}

    def _fn(X_tr, y_tr, X_va, y_va, X_te):
        dtr = lgb.Dataset(X_tr, y_tr)
        dva = lgb.Dataset(X_va, y_va, reference=dtr)
        cbs = [lgb.early_stopping(early_stopping_rounds, verbose=False)]
        if verbose_eval:
            cbs.append(lgb.log_evaluation(verbose_eval))
        m = lgb.train(p, dtr, num_boost_round=num_boost_round,
                      valid_sets=[dva], callbacks=cbs)
        best = m.best_iteration or num_boost_round
        va = m.predict(X_va, num_iteration=best)
        te = m.predict(X_te, num_iteration=best) if X_te is not None else None
        imp = dict(zip(m.feature_name(), m.feature_importance("gain").tolist()))
        return va, te, {"best_iteration": best, "importance": imp}

    return _fn


def xgb_fit_predict(params: dict, num_boost_round: int = 5000,
                    early_stopping_rounds: int = 200):
    import xgboost as xgb

    p = {"tree_method": "hist", "nthread": N_THREADS, **params}

    def _fn(X_tr, y_tr, X_va, y_va, X_te):
        dtr = xgb.DMatrix(X_tr, y_tr, enable_categorical=True)
        dva = xgb.DMatrix(X_va, y_va, enable_categorical=True)
        m = xgb.train(p, dtr, num_boost_round=num_boost_round,
                      evals=[(dva, "va")], early_stopping_rounds=early_stopping_rounds,
                      verbose_eval=False)
        best = m.best_iteration + 1
        rng = (0, best)
        va = m.predict(dva, iteration_range=rng)
        te = (m.predict(xgb.DMatrix(X_te, enable_categorical=True), iteration_range=rng)
              if X_te is not None else None)
        return va, te, {"best_iteration": best}

    return _fn


def catboost_fit_predict(params: dict, cat_features: Optional[list] = None,
                         task: str = "binary"):
    from catboost import CatBoostClassifier, CatBoostRegressor, Pool

    p = {"thread_count": N_THREADS, "verbose": 0,
         "iterations": 5000, "early_stopping_rounds": 200, **params}
    Model = CatBoostRegressor if task == "regression" else CatBoostClassifier

    def _fn(X_tr, y_tr, X_va, y_va, X_te):
        tr = Pool(X_tr, y_tr, cat_features=cat_features)
        va = Pool(X_va, y_va, cat_features=cat_features)
        m = Model(**p)
        m.fit(tr, eval_set=va, use_best_model=True)
        pred = (lambda d: m.predict(d) if task == "regression"
                else m.predict_proba(d)[:, 1])
        te = pred(Pool(X_te, cat_features=cat_features)) if X_te is not None else None
        return pred(va), te, {"best_iteration": int(m.get_best_iteration() or 0)}

    return _fn


def sklearn_fit_predict(model_factory: Callable, proba: bool = True):
    """model_factory() -> a fresh unfitted estimator (fit inside the fold)."""
    def _fn(X_tr, y_tr, X_va, y_va, X_te):
        m = model_factory()
        m.fit(X_tr, y_tr)
        pred = (lambda d: m.predict_proba(d)[:, 1]) if proba else (lambda d: m.predict(d))
        return pred(X_va), (pred(X_te) if X_te is not None else None), {}
    return _fn


# --------------------------------------------------------------------------- #
# The runner
# --------------------------------------------------------------------------- #
@dataclass
class CVResult:
    name: str
    oof: np.ndarray
    test_pred: Optional[np.ndarray]
    fold_scores: list
    oof_score: float
    metric_name: str
    wall_time: float
    info: list = field(default_factory=list)

    @property
    def mean(self) -> float:
        return float(np.mean(self.fold_scores))

    @property
    def std(self) -> float:
        return float(np.std(self.fold_scores))

    def summary(self) -> str:
        return (f"{self.name}: oof_{self.metric_name}={self.oof_score:.6f} | "
                f"folds {self.mean:.6f} ± {self.std:.6f} | "
                f"{[round(s, 5) for s in self.fold_scores]} | {self.wall_time:.0f}s")

    def importance(self, top: int = 30) -> pd.Series:
        acc: dict = {}
        for d in self.info:
            for k, v in (d.get("importance") or {}).items():
                acc[k] = acc.get(k, 0.0) + v
        return pd.Series(acc).sort_values(ascending=False).head(top)


def run_cv(
    X: pd.DataFrame,
    y: Sequence,
    folds: np.ndarray,
    fit_predict: Callable,
    metric: Callable,
    metric_name: str = "score",
    name: str = "model",
    X_test: Optional[pd.DataFrame] = None,
    maximize: bool = True,
    out_dir: str = "runs",
    params: Optional[dict] = None,
    feature_names: Optional[list] = None,
    log_csv: str = "experiments.csv",
    verbose: bool = True,
) -> CVResult:
    y = np.asarray(y)
    folds = np.asarray(folds)
    n_folds = int(folds.max()) + 1
    oof = np.full(len(X), np.nan, dtype=np.float64)
    test_preds, fold_scores, infos = [], [], []
    t0 = time.time()

    for f in range(n_folds):
        tr_idx = np.where((folds != f) & (folds >= 0))[0]
        va_idx = np.where(folds == f)[0]
        if len(va_idx) == 0:
            continue

        X_tr, X_va = X.iloc[tr_idx], X.iloc[va_idx]
        y_tr, y_va = y[tr_idx], y[va_idx]

        va_pred, te_pred, info = fit_predict(X_tr, y_tr, X_va, y_va, X_test)
        oof[va_idx] = np.asarray(va_pred).ravel()
        if te_pred is not None:
            test_preds.append(np.asarray(te_pred).ravel())
        infos.append(info or {})

        s = float(metric(y_va, oof[va_idx]))
        fold_scores.append(s)
        if verbose:
            extra = f" (best_iter={info.get('best_iteration')})" if info.get("best_iteration") else ""
            print(f"  fold {f}: {metric_name}={s:.6f}{extra}  [{time.time() - t0:.0f}s]")

    scored = ~np.isnan(oof)
    oof_score = float(metric(y[scored], oof[scored]))
    test_pred = np.mean(test_preds, axis=0) if test_preds else None
    wall = time.time() - t0

    res = CVResult(name, oof, test_pred, fold_scores, oof_score,
                   metric_name, wall, infos)
    if verbose:
        print(res.summary())

    # ---- persist ------------------------------------------------------------
    run_dir = Path(out_dir) / name
    run_dir.mkdir(parents=True, exist_ok=True)
    np.save(run_dir / "oof.npy", oof.astype(np.float32))
    if test_pred is not None:
        np.save(run_dir / "test.npy", test_pred.astype(np.float32))
    (run_dir / "params.json").write_text(json.dumps(params or {}, indent=2, default=str))
    (run_dir / "features.json").write_text(
        json.dumps(list(feature_names or X.columns), indent=2))

    row = {
        "timestamp": pd.Timestamp.now().isoformat(timespec="seconds"),
        "name": name, "metric": metric_name,
        "oof_score": oof_score, "cv_mean": res.mean, "cv_std": res.std,
        "n_folds": len(fold_scores), "n_features": X.shape[1],
        "n_rows": len(X), "wall_time_s": round(wall, 1),
        "maximize": maximize, "lb_public": "",
        "params": json.dumps(params or {}, default=str)[:500],
    }
    pd.DataFrame([row]).to_csv(
        log_csv, mode="a", header=not Path(log_csv).exists(), index=False)

    return res


# --------------------------------------------------------------------------- #
# Harness self-test: run this once per competition
# --------------------------------------------------------------------------- #
def sanity_check(X, y, folds, fit_predict, metric, metric_name="score"):
    """A constant predictor should be weak; a leaked target must be perfect.
    If the leaked run is NOT near-perfect, the harness itself is broken."""
    Xl = X.copy()
    Xl["__leak__"] = np.asarray(y)
    r = run_cv(Xl, y, folds, fit_predict, metric, metric_name,
               name="_sanity_leak", verbose=False, out_dir="/tmp/_sanity",
               log_csv="/tmp/_sanity/experiments.csv")
    print(f"[sanity] leaked-target run -> {r.oof_score:.6f} "
          f"(expected ≈ perfect; if not, the CV harness is wrong)")
    return r

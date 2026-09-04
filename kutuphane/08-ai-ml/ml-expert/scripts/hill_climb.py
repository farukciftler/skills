"""
Greedy hill-climbing ensembler over saved OOF predictions.

Selection is done WITH replacement: a strong model can be picked repeatedly,
which produces fine-grained weights without solving an optimization problem and
works with any metric, including non-differentiable ones (kappa, MAP@k, F1).

Usage
-----
    from hill_climb import load_oof_dir, hill_climb, bagged_hill_climb

    oof, test, names = load_oof_dir("runs")            # loads every runs/*/oof.npy
    r = hill_climb(oof, y, roc_auc_score, maximize=True, names=names)
    print(r.report())
    submission["target"] = r.blend(test)

Everything is numpy over an (n_rows x n_models) matrix, so it is instant even
with 100 members on a laptop.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional, Sequence

import numpy as np


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #
def load_oof_dir(runs_dir: str = "runs", require_test: bool = True):
    """Load runs/<name>/oof.npy (+ test.npy) into aligned matrices."""
    oofs, tests, names = [], [], []
    for d in sorted(Path(runs_dir).iterdir()):
        f = d / "oof.npy"
        if not f.exists() or d.name.startswith("_"):
            continue
        t = d / "test.npy"
        if require_test and not t.exists():
            print(f"[skip] {d.name}: no test.npy")
            continue
        oofs.append(np.load(f).astype(np.float64).ravel())
        if t.exists():
            tests.append(np.load(t).astype(np.float64).ravel())
        names.append(d.name)

    oof = np.column_stack(oofs)
    test = np.column_stack(tests) if tests else None
    print(f"[load] {oof.shape[1]} models, {oof.shape[0]} rows from {runs_dir}")
    return oof, test, names


def to_ranks(mat: np.ndarray) -> np.ndarray:
    """Rank-normalize each column to [0,1]. Use for AUC-type metrics or when
    members live on different scales."""
    from scipy.stats import rankdata
    out = np.empty_like(mat, dtype=np.float64)
    for j in range(mat.shape[1]):
        out[:, j] = rankdata(mat[:, j]) / len(mat)
    return out


def correlation_report(oof: np.ndarray, names: Sequence[str], threshold: float = 0.98):
    """Print the correlation matrix and flag near-duplicate members."""
    import pandas as pd
    c = pd.DataFrame(np.corrcoef(oof, rowvar=False), index=names, columns=names)
    print(c.round(3).to_string())
    dupes = [(names[i], names[j], c.iloc[i, j])
             for i in range(len(names)) for j in range(i + 1, len(names))
             if abs(c.iloc[i, j]) > threshold]
    for a, b, v in dupes:
        print(f"[dup] {a} ~ {b}: r={v:.4f} — drop the weaker one")
    return c


# --------------------------------------------------------------------------- #
# Hill climbing
# --------------------------------------------------------------------------- #
@dataclass
class ClimbResult:
    weights: np.ndarray
    names: list
    score: float
    history: list
    base_score: float

    def blend(self, mat: np.ndarray) -> np.ndarray:
        return mat @ self.weights

    def report(self, top: int = 20) -> str:
        order = np.argsort(-np.abs(self.weights))
        lines = [f"hill climb: {self.base_score:.6f} -> {self.score:.6f} "
                 f"({self.score - self.base_score:+.6f})", "weights:"]
        for i in order[:top]:
            if abs(self.weights[i]) > 1e-9:
                lines.append(f"  {self.names[i]:<32} {self.weights[i]:+.4f}")
        return "\n".join(lines)


def hill_climb(
    oof: np.ndarray,
    y: Sequence,
    metric: Callable,
    maximize: bool = True,
    names: Optional[Sequence[str]] = None,
    n_iter: int = 100,
    step: float = 1.0,
    allow_negative: bool = False,
    tol: float = 1e-7,
    idx: Optional[np.ndarray] = None,
    verbose: bool = True,
) -> ClimbResult:
    """
    Greedy forward selection with replacement.

    idx: optional row subset (used by bagged_hill_climb).
    allow_negative: also try subtracting a model. Helps occasionally, overfits
                    often — validate before enabling.
    """
    y = np.asarray(y)
    if idx is not None:
        oof, y = oof[idx], y[idx]
    n_models = oof.shape[1]
    names = list(names) if names is not None else [f"m{i}" for i in range(n_models)]
    sign = 1.0 if maximize else -1.0

    single = np.array([sign * metric(y, oof[:, j]) for j in range(n_models)])
    best_j = int(np.argmax(single))
    counts = np.zeros(n_models)
    counts[best_j] = 1.0
    current = oof[:, best_j].copy()
    best_score = single[best_j]
    base_score = sign * best_score
    history = [(names[best_j], 1.0, base_score)]

    steps = [step, -step] if allow_negative else [step]

    for it in range(1, n_iter):
        total = counts.sum()
        cand_best, cand_j, cand_s = best_score, None, None
        for j in range(n_models):
            for s in steps:
                w_new = total + s
                if w_new <= 0:
                    continue
                cand = (current * total + oof[:, j] * s) / w_new
                sc = sign * metric(y, cand)
                if sc > cand_best + tol:
                    cand_best, cand_j, cand_s = sc, j, s
        if cand_j is None:
            break
        total_new = counts.sum() + cand_s
        current = (current * counts.sum() + oof[:, cand_j] * cand_s) / total_new
        counts[cand_j] += cand_s
        best_score = cand_best
        history.append((names[cand_j], cand_s, sign * best_score))
        if verbose and it % 10 == 0:
            print(f"  iter {it}: {sign * best_score:.6f}  (+{names[cand_j]})")

    weights = counts / counts.sum()
    res = ClimbResult(weights, names, sign * best_score, history, base_score)
    if verbose:
        print(res.report())
    return res


def bagged_hill_climb(
    oof: np.ndarray,
    y: Sequence,
    metric: Callable,
    maximize: bool = True,
    names: Optional[Sequence[str]] = None,
    n_bags: int = 20,
    frac: float = 0.8,
    seed: int = 42,
    **kwargs,
) -> ClimbResult:
    """Repeat hill climbing on bootstrap row subsamples and average the weights.
    Much more robust than a single climb when members are many and rows are few."""
    y = np.asarray(y)
    rng = np.random.default_rng(seed)
    n = len(y)
    W = []
    for b in range(n_bags):
        idx = rng.choice(n, size=int(n * frac), replace=False)
        r = hill_climb(oof, y, metric, maximize, names, idx=idx, verbose=False, **kwargs)
        W.append(r.weights)
    w = np.mean(W, axis=0)
    w = w / w.sum()
    score = metric(y, oof @ w)
    single = [metric(y, oof[:, j]) for j in range(oof.shape[1])]
    base = max(single) if maximize else min(single)
    res = ClimbResult(w, list(names or range(oof.shape[1])), float(score),
                      [], float(base))
    print(f"[bagged x{n_bags}] {res.report()}")
    return res


def nested_validate(oof, y, folds, metric, maximize=True, names=None, **kwargs):
    """Honest estimate of the blend: fit weights on k-1 folds, score on the held-out
    fold. If this is much worse than the in-sample climb, the blend is overfitting."""
    y, folds = np.asarray(y), np.asarray(folds)
    scores = []
    for f in range(int(folds.max()) + 1):
        tr, va = np.where(folds != f)[0], np.where(folds == f)[0]
        r = hill_climb(oof, y, metric, maximize, names, idx=tr, verbose=False, **kwargs)
        scores.append(metric(y[va], oof[va] @ r.weights))
    print(f"[nested] {np.mean(scores):.6f} ± {np.std(scores):.6f}  {np.round(scores, 5)}")
    return float(np.mean(scores))


if __name__ == "__main__":
    # Self-test on synthetic data.
    from sklearn.metrics import roc_auc_score

    rng = np.random.default_rng(0)
    n = 5000
    y = rng.integers(0, 2, n)
    signal = y + rng.normal(0, 1, n)
    oof = np.column_stack([
        signal + rng.normal(0, s, n) for s in (0.5, 0.8, 1.2, 2.0, 3.0)
    ])
    oof = 1 / (1 + np.exp(-oof))
    r = hill_climb(oof, y, roc_auc_score, names=[f"model_{i}" for i in range(5)])
    assert r.score >= r.base_score
    print("\nself-test OK")

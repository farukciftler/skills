"""
Memory and I/O utilities for working within 16 GB of unified memory.

    from mem_utils import reduce_mem, read_fast, parquet_cache, memory_report, mem

    df = read_fast("data/train.csv")        # polars -> pandas, or parquet if present
    df = reduce_mem(df)                     # float64->float32, int64->int32/16/8

    @parquet_cache("cache/feats_v3.parquet")
    def build_features(df): ...

    with memory_report("feature build"):
        feats = build_features(df)
"""

from __future__ import annotations

import gc
import os
import time
from contextlib import contextmanager
from functools import wraps
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


# --------------------------------------------------------------------------- #
# Monitoring
# --------------------------------------------------------------------------- #
def mem() -> dict:
    """Process RSS and system memory, in GB."""
    info = {}
    try:
        import psutil
        p = psutil.Process(os.getpid())
        vm = psutil.virtual_memory()
        info = {
            "process_gb": round(p.memory_info().rss / 1e9, 2),
            "system_used_gb": round(vm.used / 1e9, 2),
            "system_available_gb": round(vm.available / 1e9, 2),
            "system_percent": vm.percent,
        }
    except ImportError:
        info = {"error": "pip install psutil"}
    return info


@contextmanager
def memory_report(label: str = "block"):
    """Report peak-ish memory delta and wall time for a block of work."""
    gc.collect()
    m0, t0 = mem(), time.time()
    try:
        yield
    finally:
        gc.collect()
        m1, dt = mem(), time.time() - t0
        d = m1.get("process_gb", 0) - m0.get("process_gb", 0)
        print(f"[mem] {label}: {dt:.1f}s | "
              f"process {m0.get('process_gb')}→{m1.get('process_gb')} GB ({d:+.2f}) | "
              f"available {m1.get('system_available_gb')} GB")


def df_size_gb(df: pd.DataFrame) -> float:
    return round(df.memory_usage(deep=True).sum() / 1e9, 3)


# --------------------------------------------------------------------------- #
# Dtype downcasting
# --------------------------------------------------------------------------- #
def reduce_mem(df: pd.DataFrame, categorize: bool = True,
               cat_threshold: float = 0.5, verbose: bool = True) -> pd.DataFrame:
    """Downcast numeric dtypes and convert low-cardinality objects to category.

    Safe for GBDTs. Note: float32 has ~7 significant digits — do not use on
    columns that need more precision (large monetary IDs, high-precision coords).
    """
    start = df.memory_usage(deep=True).sum() / 1e6

    for col in df.columns:
        s = df[col]
        kind = s.dtype.kind

        if kind in "iu":
            lo, hi = s.min(), s.max()
            for t in (np.int8, np.int16, np.int32):
                if lo >= np.iinfo(t).min and hi <= np.iinfo(t).max:
                    df[col] = s.astype(t)
                    break
        elif kind == "f":
            fmin, fmax = np.finfo(np.float32).min, np.finfo(np.float32).max
            if s.dropna().empty or (s.min() >= fmin and s.max() <= fmax):
                df[col] = s.astype(np.float32)
        elif kind == "O" and categorize:
            if s.nunique(dropna=False) / max(len(s), 1) < cat_threshold:
                df[col] = s.astype("category")

    end = df.memory_usage(deep=True).sum() / 1e6
    if verbose:
        print(f"[reduce_mem] {start:.1f} MB → {end:.1f} MB "
              f"({100 * (start - end) / max(start, 1e-9):.1f}% smaller)")
    return df


# --------------------------------------------------------------------------- #
# Fast loading
# --------------------------------------------------------------------------- #
def read_fast(path: str, columns: Optional[list] = None,
              use_polars: bool = True, downcast: bool = True) -> pd.DataFrame:
    """Read csv/parquet with Polars when available (multi-threaded, low memory).

    If a sibling .parquet exists for a .csv, it is read instead — always convert
    once with to_parquet_once() and never read the CSV again.
    """
    p = Path(path)
    pq = p.with_suffix(".parquet")
    if p.suffix == ".csv" and pq.exists():
        print(f"[read_fast] using cached parquet: {pq}")
        p = pq

    if use_polars:
        try:
            import polars as pl
            df = (pl.read_parquet(p, columns=columns) if p.suffix == ".parquet"
                  else pl.read_csv(p, columns=columns, try_parse_dates=True,
                                   infer_schema_length=10000))
            out = df.to_pandas()
        except ImportError:
            use_polars = False
    if not use_polars:
        out = (pd.read_parquet(p, columns=columns) if p.suffix == ".parquet"
               else pd.read_csv(p, usecols=columns))

    print(f"[read_fast] {p.name}: {out.shape[0]:,} x {out.shape[1]} "
          f"({df_size_gb(out)} GB)")
    return reduce_mem(out) if downcast else out


def to_parquet_once(csv_path: str, overwrite: bool = False) -> str:
    """Convert a CSV to parquet once. 3-10x smaller, far faster to read, typed."""
    src = Path(csv_path)
    dst = src.with_suffix(".parquet")
    if dst.exists() and not overwrite:
        return str(dst)
    try:
        import polars as pl
        pl.scan_csv(src, try_parse_dates=True).sink_parquet(dst)   # streaming
    except ImportError:
        pd.read_csv(src).to_parquet(dst, index=False)
    print(f"[parquet] {src.name} ({src.stat().st_size / 1e9:.2f} GB) → "
          f"{dst.name} ({dst.stat().st_size / 1e9:.2f} GB)")
    return str(dst)


def scan_large(path: str):
    """Return a Polars LazyFrame for out-of-core work on data bigger than RAM.

        lf = scan_large("data/big.parquet")
        agg = (lf.group_by("customer_id")
                 .agg(pl.col("amount").mean().alias("amt_mean"))
                 .collect(streaming=True))
    """
    import polars as pl
    return pl.scan_parquet(path) if path.endswith(".parquet") else pl.scan_csv(path)


def duckdb_query(sql: str, **frames):
    """Run out-of-core SQL over parquet files or in-memory frames.

        duckdb_query("SELECT customer_id, avg(amount) FROM 'data/tx.parquet' GROUP BY 1")
        duckdb_query("SELECT * FROM df WHERE amount > 100", df=my_dataframe)
    """
    import duckdb
    con = duckdb.connect()
    for name, frame in frames.items():
        con.register(name, frame)
    return con.execute(sql).df()


# --------------------------------------------------------------------------- #
# Caching
# --------------------------------------------------------------------------- #
def parquet_cache(path: str, overwrite: bool = False):
    """Cache a DataFrame-returning function to parquet. Survives kernel restarts,
    which matters a lot when a feature build takes 20 minutes."""
    def deco(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            p = Path(path)
            if p.exists() and not overwrite:
                print(f"[cache] hit {p}")
                return pd.read_parquet(p)
            p.parent.mkdir(parents=True, exist_ok=True)
            out = fn(*args, **kwargs)
            out.to_parquet(p, index=False)
            print(f"[cache] wrote {p} ({p.stat().st_size / 1e6:.0f} MB)")
            return out
        return wrapper
    return deco


def free(*objs):
    """Delete references and force a collection. Use after big intermediates."""
    for o in objs:
        del o
    gc.collect()


# --------------------------------------------------------------------------- #
# Sampling for fast iteration
# --------------------------------------------------------------------------- #
def dev_sample(df: pd.DataFrame, frac: float = 0.2, y: Optional[str] = None,
               group: Optional[str] = None, seed: int = 42) -> pd.DataFrame:
    """Stratified / group-aware subsample for the development loop.
    Iterate at 20%, confirm winners on 100%."""
    if group:
        keys = df[group].drop_duplicates().sample(frac=frac, random_state=seed)
        out = df[df[group].isin(keys)]
    elif y:
        out = (df.groupby(df[y], group_keys=False)
                 .apply(lambda g: g.sample(frac=frac, random_state=seed)))
    else:
        out = df.sample(frac=frac, random_state=seed)
    print(f"[dev_sample] {len(df):,} → {len(out):,} rows")
    return out.reset_index(drop=True)

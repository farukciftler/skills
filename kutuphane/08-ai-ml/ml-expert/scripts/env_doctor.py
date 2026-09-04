#!/usr/bin/env python3
"""
Diagnose the local ML environment on Apple Silicon.

    python env_doctor.py

Reports: chip, P/E core split, memory, recommended thread count, library
versions, OpenMP health, MPS/MLX availability, and a quick LightGBM benchmark.
Run it when something is unexpectedly slow or an import fails.
"""

from __future__ import annotations

import importlib
import os
import platform
import subprocess
import sys
import time


def sh(cmd: list[str]) -> str:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def header(t: str) -> None:
    print(f"\n{'=' * 62}\n{t}\n{'=' * 62}")


def hardware() -> int:
    header("HARDWARE")
    chip = sh(["sysctl", "-n", "machdep.cpu.brand_string"]) or platform.processor()
    p = sh(["sysctl", "-n", "hw.perflevel0.physicalcpu"])
    e = sh(["sysctl", "-n", "hw.perflevel1.physicalcpu"])
    memb = sh(["sysctl", "-n", "hw.memsize"])
    gpu = ""
    for line in sh(["system_profiler", "SPDisplaysDataType"]).splitlines():
        if "Total Number of Cores" in line:
            gpu = line.split(":")[-1].strip()
            break

    print(f"chip                : {chip}")
    print(f"arch / os           : {platform.machine()} / macOS {platform.mac_ver()[0]}")
    print(f"performance cores   : {p or '?'}")
    print(f"efficiency cores    : {e or '?'}")
    print(f"gpu cores           : {gpu or '?'}")
    if memb:
        print(f"unified memory      : {int(memb) / 1e9:.0f} GB (shared CPU+GPU)")

    n = int(p) if p.isdigit() else (os.cpu_count() or 4)
    print(f"\n>>> recommended n_jobs / num_threads = {n}  (performance cores only)")
    print("    Using all cores includes the slower E-cores and makes GBDTs slower.")
    return n


def memory_state() -> None:
    header("MEMORY STATE")
    try:
        import psutil
        vm = psutil.virtual_memory()
        sw = psutil.swap_memory()
        print(f"used      : {vm.used / 1e9:5.1f} GB ({vm.percent}%)")
        print(f"available : {vm.available / 1e9:5.1f} GB")
        print(f"swap used : {sw.used / 1e9:5.1f} GB")
        if vm.available < 4e9:
            print("!! under 4 GB available — close Chrome/apps before training")
        if sw.used > 2e9:
            print("!! heavy swapping — the machine is memory-bound, reduce data size")
    except ImportError:
        print("psutil not installed (pip install psutil)")

    top = sh(["bash", "-lc",
              "ps -Ao rss,comm | tail -n +2 | sort -rn | head -6 | "
              "awk '{printf \"  %6.1f GB  %s\\n\", $1/1048576, $2}'"])
    if top:
        print("\ntop memory consumers:")
        print(top)


def libraries() -> None:
    header("LIBRARIES")
    core = ["numpy", "pandas", "polars", "pyarrow", "duckdb", "sklearn", "scipy",
            "lightgbm", "xgboost", "catboost", "optuna", "shap"]
    dl = ["torch", "torchvision", "transformers", "timm", "mlx", "sentence_transformers"]
    misc = ["kaggle", "matplotlib", "psutil", "tabpfn", "autogluon"]

    for group, mods in (("core", core), ("deep learning", dl), ("misc", misc)):
        print(f"\n[{group}]")
        for m in mods:
            try:
                mod = importlib.import_module(m)
                v = getattr(mod, "__version__", "?")
                print(f"  {m:<24} {v}")
            except ImportError:
                print(f"  {m:<24} -- not installed")
            except Exception as e:  # e.g. libomp loading failure
                print(f"  {m:<24} !! import error: {str(e)[:70]}")


def openmp() -> None:
    header("OPENMP / THREADING")
    libomp = "/opt/homebrew/opt/libomp/lib/libomp.dylib"
    print(f"brew libomp present : {os.path.exists(libomp)}")
    for var in ("OMP_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS",
                "NUMEXPR_NUM_THREADS", "PYTORCH_ENABLE_MPS_FALLBACK",
                "PYTORCH_MPS_HIGH_WATERMARK_RATIO"):
        print(f"  {var:<34} {os.environ.get(var, '(unset)')}")
    try:
        import lightgbm as lgb
        print(f"lightgbm import     : OK ({lgb.__version__})")
    except Exception as e:
        print(f"lightgbm import     : FAILED -> {str(e)[:90]}")
        print("  fix: brew install libomp && "
              "export DYLD_LIBRARY_PATH=/opt/homebrew/opt/libomp/lib:$DYLD_LIBRARY_PATH")


def accelerators() -> None:
    header("ACCELERATORS")
    try:
        import torch
        print(f"torch               : {torch.__version__}")
        print(f"mps available       : {torch.backends.mps.is_available()}")
        print(f"mps built           : {torch.backends.mps.is_built()}")
        if torch.backends.mps.is_available():
            t0 = time.time()
            a = torch.randn(2048, 2048, device="mps")
            b = a @ a
            torch.mps.synchronize()
            dt = time.time() - t0
            gflops = 2 * 2048 ** 3 / dt / 1e9
            print(f"mps matmul 2048³    : {dt * 1000:.0f} ms (~{gflops:.0f} GFLOP/s, "
                  f"includes warmup)")
            print("note: MPS has no float64 and no tensor cores; AMP gains are modest")
    except ImportError:
        print("torch               : not installed")
    except Exception as e:
        print(f"torch               : error -> {str(e)[:90]}")

    try:
        import mlx.core as mx
        print(f"mlx                 : {getattr(mx, '__version__', 'installed')} "
              f"(unified-memory native; ~2-3x faster than MPS for many workloads)")
    except ImportError:
        print("mlx                 : not installed (pip install mlx mlx-lm)")


def benchmark(n_threads: int) -> None:
    header("QUICK LIGHTGBM BENCHMARK")
    try:
        import lightgbm as lgb
        import numpy as np
    except Exception as e:
        print(f"skipped: {str(e)[:80]}")
        return

    rng = np.random.default_rng(0)
    X = rng.normal(size=(200_000, 50)).astype(np.float32)
    y = (X[:, 0] + X[:, 1] * X[:, 2] + rng.normal(0, 0.5, 200_000) > 0).astype(int)
    ds = lgb.Dataset(X, y)
    for t in sorted({1, n_threads, os.cpu_count() or n_threads}):
        p = {"objective": "binary", "num_threads": t, "verbosity": -1,
             "num_leaves": 63, "learning_rate": 0.1, "seed": 0}
        t0 = time.time()
        lgb.train(p, ds, num_boost_round=100)
        print(f"  num_threads={t:<3} 100 rounds on 200k x 50 : {time.time() - t0:5.1f}s")
    print("  → pick the fastest; on M2 Pro it is normally the P-core count, not all cores")


def main() -> None:
    print(f"python              : {sys.version.split()[0]}  ({sys.executable})")
    n = hardware()
    memory_state()
    libraries()
    openmp()
    accelerators()
    if "--bench" in sys.argv:
        benchmark(n)
    else:
        print("\n(run with --bench for a LightGBM threading benchmark)")


if __name__ == "__main__":
    main()

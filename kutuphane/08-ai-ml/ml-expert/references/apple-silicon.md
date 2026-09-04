# The M2 Pro Engineering Manual

Hardware: **Apple M2 Pro — 6 performance + 4 efficiency CPU cores, 16-core GPU, 16 GB unified memory.** No CUDA, no NVIDIA libraries, no separate VRAM.

---

## 1. Environment setup

Use **uv** (fast, reliable) or miniforge/conda-forge. Homebrew is already installed on this machine; system Python is 3.9 and should not be used for ML work.

```bash
# one-time
brew install libomp cmake                    # OpenMP: required by LightGBM/XGBoost
curl -LsSf https://astral.sh/uv/install.sh | sh

# per project
uv venv --python 3.12 .venv && source .venv/bin/activate
uv pip install numpy pandas polars pyarrow duckdb scikit-learn scipy \
               lightgbm xgboost catboost optuna shap matplotlib seaborn \
               jupyterlab ipywidgets tqdm kaggle
```

Python 3.12 is the safe default (3.13 still has occasional wheel gaps for scientific packages; check before choosing it).

For deep learning add:
```bash
uv pip install torch torchvision            # MPS support is in the standard wheels
uv pip install transformers datasets accelerate timm sentence-transformers
uv pip install mlx mlx-lm                   # Apple-native framework, optional but fast
```

**libomp note**: modern LightGBM/XGBoost wheels for arm64 usually bundle or find OpenMP, but if you see `Library not loaded: @rpath/libomp.dylib`, `brew install libomp` and, if needed:
```bash
export DYLD_LIBRARY_PATH=/opt/homebrew/opt/libomp/lib:$DYLD_LIBRARY_PATH
```
Historically some libomp versions broke LightGBM's ability to fit multiple models in parallel *threads* — if a threaded model-parallel loop hangs, use processes instead.

Verify with `scripts/env_doctor.py`.

---

## 2. Threading — the biggest free speedup

The 4 efficiency cores run at a fraction of P-core speed. Boosting iterations synchronize at every split, so the whole tree waits for the slowest thread — E-cores turn into a bottleneck.

**Set 6 threads everywhere:**
```python
N_THREADS = 6
lgb.train({..., "num_threads": N_THREADS}, ...)
xgb.XGBRegressor(n_jobs=N_THREADS, tree_method="hist")
CatBoostClassifier(thread_count=N_THREADS)
sklearn_model = RandomForestClassifier(n_jobs=N_THREADS)
```

```bash
# for BLAS-heavy numpy/sklearn work
export OMP_NUM_THREADS=6
export VECLIB_MAXIMUM_THREADS=6
export MKL_NUM_THREADS=6            # harmless on ARM; used if MKL-like backends appear
export NUMEXPR_NUM_THREADS=6
```

**Never nest parallelism.** `Optuna(n_jobs=4)` × `lgbm(num_threads=6)` = 24 threads on 10 cores = thrashing. Pick one level to parallelize.

Apple's scheduler also honours QoS: long-running background work started from a terminal may be placed on E-cores. Keep training in the foreground, and prefer `caffeinate -i python train.py` for long runs (prevents sleep, keeps the process at a normal QoS).

---

## 3. Memory: 16 GB shared between CPU and GPU

There is one pool. A PyTorch MPS allocation reduces what's available to pandas, and vice versa.

Practical budget:
- OS + apps idle: ~3-4 GB. Chrome with many tabs: +2-4 GB — **close it before training**.
- Leave ~2 GB headroom or macOS starts swapping to SSD, which is where "everything got mysteriously slow" comes from.
- Effective working budget for ML: **~10-11 GB**.

Techniques, in order of value:
1. **Downcast dtypes** — `float64→float32`, `int64→int32/16/8`, `object→category`. Typically 50-70% reduction, no accuracy cost for GBDTs. (`scripts/mem_utils.py`)
2. **Parquet, not CSV** — 3-10× smaller on disk, typed, and much faster to read. Convert once, then always read parquet.
3. **Polars** — multi-threaded and dramatically more memory-efficient than pandas on group-bys and joins; `scan_parquet()` + lazy expressions + `collect(streaming=True)` processes datasets larger than RAM.
4. **DuckDB** — out-of-core SQL over parquet; ideal for "aggregate a 20 GB dataset on a 16 GB laptop". Returns arrow/pandas directly. Perfect for feature aggregation pipelines.
5. **Column pruning early** — select only the columns you need at read time (`columns=` in `read_parquet`, or the projection in the SQL).
6. **Chunked/incremental training** — LightGBM supports continued training; for huge data, train on a subsample and validate on full.
7. **`del` + `gc.collect()`** after big intermediate frames; in notebooks, restart the kernel rather than trusting cleanup.
8. **Subsample during development** — iterate on 20% stratified data, confirm the winners on 100%. This alone often makes the difference between a 3-minute and a 30-minute loop.

Monitor with `psutil.virtual_memory()`, Activity Monitor's *Memory Pressure* graph (yellow = trouble), or `vm_stat 1`. Memory pressure is a better signal than "memory used" — macOS caching makes the raw number look scarier than it is.

---

## 4. PyTorch MPS

```python
import torch
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
```

**What works**: most standard layers, conv nets, transformers, `float32` and `float16`/`bfloat16` on recent versions.

**Known constraints and gotchas**
- **No float64.** MPS supports fp32/fp16/bf16 only. Any `float64` tensor (often introduced by numpy → torch conversions) raises or silently degrades. Cast explicitly: `torch.from_numpy(a.astype(np.float32))`.
- **Missing ops fall back or raise.** Set `PYTORCH_ENABLE_MPS_FALLBACK=1` to route unimplemented ops to the CPU instead of erroring. This is a correctness crutch with a performance cost — if a hot op falls back every step, training will crawl; find and replace it.
- **No tensor cores.** AMP (`torch.autocast("mps")`) gives modest and inconsistent gains, unlike on NVIDIA. Try it, measure, don't assume.
- **Memory env vars**:
  ```bash
  export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0   # disable the hard cap (use with care)
  # or a value like 0.9 to cap allocations at 90% of the recommended working set
  ```
  The default high watermark can trigger "MPS backend out of memory" well before the machine is actually full. Lower `low_watermark` behaviour causes more frequent GC/commits.
- `torch.mps.empty_cache()` between phases helps, but does not reliably release everything — some long loops leak; restart the process for multi-hour runs, and checkpoint so you can.
- **Historic silent-correctness bugs** exist on MPS (e.g. in-place ops on non-contiguous tensors). If MPS results diverge from CPU, that's a real possibility: validate a few steps on CPU with the same seed when results look wrong, and keep PyTorch up to date.
- `num_workers` in DataLoader: use **2-4**, not 8. On macOS the default start method is spawn; heavy workers duplicate memory. `persistent_workers=True`, `pin_memory=False` (pinning is meaningless with unified memory).

**Expected speed**: MPS on M2 Pro is roughly in the ballpark of an older mid-range NVIDIA card for small models — good enough for MLPs, small CNNs, and ≤100M-param transformer fine-tunes; not competitive for anything large.

---

## 5. MLX (Apple-native)

`mlx` is designed for unified memory from the ground up: arrays live in one shared pool, and there are no host↔device copies. It is typically **~2-3× faster than PyTorch MPS** for comparable workloads and considerably better for LLM inference; it also avoids the MPS single-allocation cap, so the whole unified pool is usable.

Use MLX when:
- Running or fine-tuning LLMs locally (`mlx-lm` supports LoRA fine-tuning of 3-8B models on 16 GB at 4-bit).
- A training loop is MPS-bound and the model is simple enough to port (the API is numpy/PyTorch-like).
- Generating embeddings or doing local inference at volume.

Use PyTorch when you need the ecosystem: `timm`, `transformers` training APIs, competition code that must also run on Kaggle GPUs, or anything you'll later port to CUDA.

Rule for competitions: **prototype in whatever is fastest locally, but the code that produces the submission should run in the target environment.** For Kaggle code competitions, that means PyTorch.

---

## 6. Thermals and long runs

The MacBook Pro chassis sustains load well, but a multi-hour 100% CPU run will down-clock somewhat. Practical measures:
- Keep the lid open and the machine on a hard surface; use `caffeinate -i` (or `caffeinate -dims` if the display must stay on) so nothing sleeps mid-run.
- Plug in the power adapter — on battery, macOS caps performance.
- Checkpoint every epoch/fold. Assume the run can die; a laptop is not a training server.
- `sudo powermetrics --samplers smc -i1000` shows temperature/power if you need to confirm throttling; `pmset -g thermlog` shows thermal pressure events.
- Long GBDT sweeps are better run overnight with `nohup`/`caffeinate` and a log file than watched interactively.

---

## 7. Benchmarks / what "too slow" means here

Rough expectations (they vary hugely with data, but useful as sanity checks):

| Workload | M2 Pro expectation |
|---|---|
| LightGBM, 1M rows × 100 features, 1000 trees, 6 threads | ~1-3 min per fold |
| CatBoost, same | ~3-10 min per fold (slower, no GPU here) |
| Polars group-by over 10M rows | seconds |
| pandas group-by over 10M rows | tens of seconds, high memory |
| MLP (3 layers) on 1M rows, MPS | a few minutes per epoch |
| DeBERTa-v3-base fine-tune, 10k samples, seq 256, MPS | ~1-2 h/epoch — borderline; prefer cloud |
| ResNet-50 / ConvNeXt-T fine-tune, 20k images 224px, MPS | ~1-2 h/epoch — borderline |
| Stable-diffusion-scale training, 7B LLM full fine-tune | not feasible |

If a single fold exceeds ~45 minutes and dozens of experiments are planned, restructure (subsample / fewer folds / cloud) rather than accepting the loop.

---

## 8. Kaggle CLI on macOS

```bash
uv pip install kaggle
mkdir -p ~/.kaggle && mv ~/Downloads/kaggle.json ~/.kaggle/ && chmod 600 ~/.kaggle/kaggle.json

kaggle competitions list -s tabular
kaggle competitions download -c <comp> -p data/ && unzip -q data/<comp>.zip -d data/
kaggle competitions submit -c <comp> -f sub.csv -m "lgbm v3 cv0.7823"
kaggle competitions submissions -c <comp>
kaggle datasets create -p wheels/          # upload wheels/weights for offline notebooks
```
`kagglehub` is the modern alternative for pulling datasets/models directly in Python.

Free Kaggle Notebooks give ~30 GPU-hours/week (T4×2 or P100) — treat that as the attached GPU for this laptop, and note that it is also exactly the environment code competitions run in.

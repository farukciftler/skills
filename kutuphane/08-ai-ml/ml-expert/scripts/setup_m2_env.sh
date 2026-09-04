#!/usr/bin/env bash
# Bootstrap an ML environment on Apple Silicon (M2 Pro, 16 GB).
#
#   bash setup_m2_env.sh                # core tabular stack
#   bash setup_m2_env.sh --dl           # + PyTorch/transformers/timm
#   bash setup_m2_env.sh --dl --mlx     # + Apple MLX
#   bash setup_m2_env.sh --all
#
# Creates .venv in the current directory with uv, installs the stack, writes
# a .env with the correct thread settings, and verifies every import.

set -euo pipefail

PY_VERSION="${PY_VERSION:-3.12}"
WITH_DL=0; WITH_MLX=0
for arg in "$@"; do
  case "$arg" in
    --dl)  WITH_DL=1 ;;
    --mlx) WITH_MLX=1 ;;
    --all) WITH_DL=1; WITH_MLX=1 ;;
    *) echo "unknown flag: $arg"; exit 1 ;;
  esac
done

echo "==> Apple Silicon ML environment bootstrap"
[[ "$(uname -m)" == "arm64" ]] || echo "!! not arm64 — this script targets Apple Silicon"

# --- 1. Homebrew deps ------------------------------------------------------
if ! command -v brew >/dev/null 2>&1; then
  echo "!! Homebrew missing. Install from https://brew.sh then re-run."; exit 1
fi
echo "==> installing libomp + cmake (OpenMP is required by LightGBM/XGBoost)"
brew list libomp >/dev/null 2>&1 || brew install libomp
brew list cmake  >/dev/null 2>&1 || brew install cmake

# --- 2. uv -----------------------------------------------------------------
if ! command -v uv >/dev/null 2>&1; then
  echo "==> installing uv"
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

# --- 3. venv ---------------------------------------------------------------
echo "==> creating .venv (python ${PY_VERSION})"
uv venv --python "${PY_VERSION}" .venv
# shellcheck disable=SC1091
source .venv/bin/activate

# --- 4. packages -----------------------------------------------------------
echo "==> installing core stack"
uv pip install \
  numpy pandas polars pyarrow duckdb \
  scikit-learn scipy statsmodels \
  lightgbm xgboost catboost \
  optuna shap \
  matplotlib seaborn \
  jupyterlab ipywidgets ipykernel \
  tqdm psutil joblib kaggle kagglehub

if [[ $WITH_DL -eq 1 ]]; then
  echo "==> installing deep learning stack (MPS-capable wheels)"
  uv pip install torch torchvision torchaudio
  uv pip install transformers datasets accelerate peft timm sentence-transformers albumentations
fi

if [[ $WITH_MLX -eq 1 ]]; then
  echo "==> installing MLX (Apple-native, unified memory)"
  uv pip install mlx mlx-lm
fi

# --- 5. env file -----------------------------------------------------------
PCORES="$(sysctl -n hw.perflevel0.physicalcpu 2>/dev/null || echo 6)"
cat > .env <<EOF
# Threading: performance cores only. Including the efficiency cores makes
# GBDT training slower because every boosting iteration syncs on all threads.
OMP_NUM_THREADS=${PCORES}
VECLIB_MAXIMUM_THREADS=${PCORES}
MKL_NUM_THREADS=${PCORES}
NUMEXPR_NUM_THREADS=${PCORES}
N_THREADS=${PCORES}

# PyTorch MPS
PYTORCH_ENABLE_MPS_FALLBACK=1
# PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0   # uncomment if you hit premature MPS OOM

# OpenMP runtime, in case a wheel cannot find libomp
DYLD_LIBRARY_PATH=/opt/homebrew/opt/libomp/lib
EOF
echo "==> wrote .env (source it, or load with python-dotenv)"

# --- 6. project skeleton ---------------------------------------------------
mkdir -p data runs cache notebooks src
[[ -f .gitignore ]] || cat > .gitignore <<'EOF'
.venv/
data/
runs/
cache/
*.parquet
*.npy
.ipynb_checkpoints/
optuna.db
EOF

# --- 7. verify -------------------------------------------------------------
echo "==> verifying imports"
set +e
python - <<'PY'
import importlib, sys
mods = ["numpy","pandas","polars","pyarrow","duckdb","sklearn","lightgbm",
        "xgboost","catboost","optuna","shap","psutil"]
opt  = ["torch","transformers","timm","mlx.core"]
bad = []
for m in mods + opt:
    try:
        mod = importlib.import_module(m)
        print(f"  ok   {m:<16} {getattr(mod, '__version__', '')}")
    except ImportError:
        (bad.append(m) if m in mods else print(f"  --   {m:<16} (not installed)"))
    except Exception as e:
        bad.append(m); print(f"  FAIL {m:<16} {str(e)[:60]}")
try:
    import torch
    print(f"\n  MPS available: {torch.backends.mps.is_available()}")
except Exception:
    pass
sys.exit(1 if bad else 0)
PY
STATUS=$?
set -e

echo
if [[ $STATUS -eq 0 ]]; then
  echo "==> done. activate with:  source .venv/bin/activate && set -a && . ./.env && set +a"
  echo "    then run:             python env_doctor.py --bench"
else
  echo "!! some core imports failed — see above."
  echo "   Common fix for LightGBM/XGBoost:"
  echo "     brew install libomp"
  echo "     export DYLD_LIBRARY_PATH=/opt/homebrew/opt/libomp/lib:\$DYLD_LIBRARY_PATH"
  exit 1
fi

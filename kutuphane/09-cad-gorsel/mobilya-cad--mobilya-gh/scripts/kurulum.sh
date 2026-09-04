#!/usr/bin/env bash
# mobilya-cad araç zinciri kurulumu — macOS Apple Silicon
# Kullanım: bash kurulum.sh
set -euo pipefail

VENV="${MOBILYA_VENV:-$HOME/mobilya-venv}"
PY=/opt/homebrew/bin/python3.12
BLENDER="/Applications/Blender.app/Contents/MacOS/Blender"

echo "== 1/4  Python CAD venv ($VENV)"
if [ ! -x "$PY" ]; then
  echo "python3.12 yok. Kur:  brew install python@3.12"; exit 1
fi
[ -d "$VENV" ] || "$PY" -m venv "$VENV"
"$VENV/bin/pip" install -q --upgrade pip

# ezdxf[draw] KULLANMA — PySide6 (443 MB) çeker. Headless için gereken:
#   PyMuPDF  -> PDF/PNG backend
#   Pillow   -> drawing frontend'in zorunlu bağımlılığı
"$VENV/bin/pip" install -q build123d ezdxf PyMuPDF Pillow

echo "== 2/4  Sürüm kontrolü"
"$VENV/bin/python" - <<'EOF'
import build123d, ezdxf, sys
print(f"  python     {sys.version.split()[0]}")
print(f"  build123d  {build123d.__version__}")
print(f"  ezdxf      {ezdxf.__version__}")
import ezdxf.addons.drawing.pymupdf  # backend gerçekten yüklenebiliyor mu
print("  pymupdf backend  OK")
EOF

echo "== 3/4  Blender"
if [ -x "$BLENDER" ]; then
  "$BLENDER" --version | head -1 | sed 's/^/  /'
else
  echo "  Blender bulunamadı: $BLENDER"
  echo "  Kur: brew install --cask blender   (5.2 LTS önerilir)"
fi

echo "== 4/4  Duman testi"
cd "$(dirname "$0")"
"$VENV/bin/python" mobilya.py >/dev/null && echo "  mobilya.py  OK"
"$VENV/bin/python" -c "import sys; sys.path.insert(0,'.'); import cizim" \
  && echo "  cizim.py    OK"

cat <<EOF

Hazır. Kullanım:
  $VENV/bin/python ayakkabilik.py --tip devrilir --genislik 800 --cikti cikti
  python3 doku_indir.py --ph oak_veneer_02 --klasor dokular
  $BLENDER -b --python render.py -- --glb cikti/AYK-01.glb \\
      --doku dokular/oak_veneer_02 --out cikti/render

UYARI: cadquery'yi BU venv'e KURMA. cadquery-ocp ile cadquery-ocp-novtk
aynı dosya yollarını yazar, ikisi bir arada OCP'yi bozar.
EOF

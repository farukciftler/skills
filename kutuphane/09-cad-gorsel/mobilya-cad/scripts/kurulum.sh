#!/usr/bin/env bash
# mobilya-cad araç zinciri kurulumu — macOS Apple Silicon (Linux'ta da çalışır)
# Kullanım: bash kurulum.sh
#   MOBILYA_VENV=~/baska/venv      venv yolu (varsayılan ~/mobilya-venv)
#   MOBILYA_PYTHON=/yol/python3.13 belirli yorumlayıcı
#   MOBILYA_BLENDER=/yol/Blender   Blender ikilisi
set -euo pipefail

BURASI="$(cd "$(dirname "$0")" && pwd)"
VENV="${MOBILYA_VENV:-$HOME/mobilya-venv}"
BLENDER="${MOBILYA_BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}"

# Python: 3.12 veya 3.13 tercih (build123d/OCP wheel'leri buna göre),
# 3.10/3.11 kabul. Sistem python3.9 OLMAZ (yığın ≥3.10 ister).
sec_python() {
  if [ -n "${MOBILYA_PYTHON:-}" ]; then echo "$MOBILYA_PYTHON"; return; fi
  for aday in python3.12 python3.13 python3.11 python3.10 python3; do
    for kl in /opt/homebrew/bin /usr/local/bin /usr/bin; do
      p="$kl/$aday"
      if [ -x "$p" ] && "$p" -c 'import sys; sys.exit(0 if (3,10) <= sys.version_info[:2] <= (3,13) else 1)' 2>/dev/null; then
        echo "$p"; return
      fi
    done
  done
  return 1
}

echo "== 1/4  Python CAD venv ($VENV)"
if [ -d "$VENV" ]; then
  PY="$VENV/bin/python"
  echo "  mevcut venv kullanılıyor: $("$PY" --version)"
else
  PY="$(sec_python)" || { echo "Uygun Python (3.10–3.13) yok. Kur:  brew install python@3.13"; exit 1; }
  echo "  yorumlayıcı: $PY ($("$PY" --version))"
  "$PY" -m venv "$VENV"
fi
"$VENV/bin/pip" install -q --upgrade pip

# ezdxf[draw] KULLANMA — PySide6 (443 MB) çeker. Headless için gereken
# PyMuPDF + Pillow requirements.txt'te; reportlab tasarım dosyası PDF'i için.
"$VENV/bin/pip" install -q -r "$BURASI/../requirements.txt"

echo "== 2/4  Sürüm kontrolü"
"$VENV/bin/python" - <<'PYEOF'
import sys, build123d, ezdxf, reportlab, pymupdf, PIL
print(f"  python     {sys.version.split()[0]}")
print(f"  build123d  {build123d.__version__}")
print(f"  ezdxf      {ezdxf.__version__}")
print(f"  reportlab  {reportlab.Version}")
print(f"  pymupdf    {pymupdf.version[0]}")
import ezdxf.addons.drawing.pymupdf  # backend gerçekten yüklenebiliyor mu
print("  pymupdf backend  OK")
PYEOF

echo "== 3/4  Blender"
if [ -x "$BLENDER" ]; then
  "$BLENDER" --version | head -1 | sed 's/^/  /'
else
  echo "  Blender bulunamadı: $BLENDER"
  echo "  Kur: brew install --cask blender   (5.2 LTS önerilir) — render adımı onsuz atlanır"
fi

echo "== 4/4  Testler (saf Python + CAD katmanı içe alımı)"
"$VENV/bin/python" -m unittest discover -s "$BURASI/../tests" -q
"$VENV/bin/python" -c "import sys; sys.path.insert(0,'$BURASI'); import cizim, belge" \
  && echo "  cizim.py / belge.py içe alımı OK"

cat <<EOF2

Hazır. Kullanım (repo kökünden):
  $VENV/bin/python uret_final.py            # AYK-01 tam paket
  python3 scripts/doku_indir.py --ph oak_veneer_02 --klasor dokular
  $BLENDER -b --python scripts/render.py -- --glb cikti/AYK-01/AYK-01.glb \\
      --doku dokular/oak_veneer_02 --out cikti/AYK-01/render

UYARI: cadquery'yi BU venv'e KURMA. cadquery-ocp ile cadquery-ocp-novtk
aynı dosya yollarını yazar, ikisi bir arada OCP'yi bozar.
EOF2

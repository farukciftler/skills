#!/usr/bin/env bash
# Masifico üretim araç zinciri kurulumu (Apple Silicon macOS).
# Güvenle tekrar çalıştırılabilir; kurulu olanı atlar.
set -euo pipefail

VENV="$HOME/masifico-venv"
PY="/opt/homebrew/bin/python3.13"

if [ ! -x "$PY" ]; then
  echo "python3.13 yok — kuruluyor..."; brew install python@3.13
fi

if [ ! -d "$VENV" ]; then
  "$PY" -m venv "$VENV"
  echo "venv oluşturuldu: $VENV"
fi

"$VENV/bin/pip" install --upgrade pip -q
"$VENV/bin/pip" install -q build123d ezdxf matplotlib pymupdf trimesh \
  manifold3d shapely svgwrite rectpack reportlab weasyprint numpy-stl
echo "Python CAD yığını hazır ($("$VENV/bin/python" -c 'import build123d,ezdxf;print("build123d",build123d.__version__,"ezdxf",ezdxf.__version__)'))"

command -v f3d >/dev/null || brew install f3d
command -v admesh >/dev/null || brew install admesh

if [ ! -d "/Applications/PrusaSlicer.app" ] && [ ! -d "/Applications/OrcaSlicer.app" ]; then
  echo "NOT: dilimleyici yok. 3D baskı gerekince: brew install --cask prusaslicer"
fi
if [ ! -d "/Applications/Inkscape.app" ]; then
  echo "NOT: Inkscape yok (SVG→PDF/DXF çevrimi gerekirse): brew install --cask inkscape"
fi
echo "Kurulum tamam. Kullanım: $VENV/bin/python <script>.py"

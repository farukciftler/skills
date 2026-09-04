#!/usr/bin/env bash
# Reports what this machine can do, and what installing the optional pieces
# would unlock. Run this first on a new host.
echo "== zorunlu =="
for b in ffmpeg ffprobe python3; do
  printf '  %-8s %s\n' "$b" "$(command -v $b || echo 'EKSİK')"; done
python3 -c 'import numpy,PIL;print("  numpy+Pillow  OK")' 2>/dev/null || echo "  numpy/Pillow  EKSİK -> pip install numpy pillow"
# nproc Linux'a ozgu; macOS'ta sysctl.
CORES=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo "?")
echo "  ffmpeg: $(ffmpeg -version 2>/dev/null | head -1 | cut -d' ' -f3)  çekirdek: $CORES"
echo "== gerekli dahili filtreler =="
for f in zoompan displace blend gblur curves colorbalance vignette noise rgbashift xfade; do
  # ffmpeg 8.x bayrak sutununu degistirdi; "^ ..[.C] $f " artik eslesmiyor ve
  # her filtre EKSIK gorunuyordu (macOS ffmpeg 8.1.2'de dogrulandi). Bayrak
  # sutununu hic okumayip ADI ikinci alanda ariyoruz — surumden bagimsiz.
  ffmpeg -hide_banner -filters 2>/dev/null | awk -v F="$f" '$2==F{f=1} END{exit !f}' && s=OK || s=EKSİK
  printf '  %-12s %s\n' "$f" "$s"; done
echo "== opsiyonel: frei0r =="
n=$(ls /usr/lib/frei0r-1/*.so /usr/local/lib/frei0r-1/*.so 2>/dev/null | wc -l)
if [ "$n" -gt 0 ]; then
  echo "  $n eklenti bulundu -> glow / vignette / distort0r / cartoon / colorhalftone kullanılabilir"
else
  echo "  yok. Kurulum: sudo apt-get install -y frei0r-plugins   (Alpine: apk add frei0r-plugins)"
  echo "  Kazanç: tek filtreyle bloom (glow), yumuşak vignette, kendiliğinden animasyonlu dalga (distort0r),"
  echo "          lo-fi/retro stilizasyon (cartoon, colorhalftone, dither, scanline0r, pixeliz0r)."
  echo "  Bunlar olmadan da her preset çalışır; dahili karşılıklarına düşer."
fi
echo "== opsiyonel: gmic =="
command -v gmic >/dev/null && echo "  $(gmic -version 2>&1 | grep -o 'Version [0-9.]*' | head -1)" \
  || echo "  yok. Kurulum: sudo apt-get install -y gmic  (alternatif doku fırınlama; şart değil)"

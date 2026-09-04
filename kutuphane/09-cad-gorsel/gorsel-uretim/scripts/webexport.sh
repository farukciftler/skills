#!/usr/bin/env bash
# webexport.sh — kaynak gorseli site icin AVIF + WebP + JPEG varyantlarina cevirir.
#
# Bu makinede sips AVIF yazabiliyor (public.avif Writable) — avifenc kurmaya gerek yok.
# WebP icin cwebp kullanilir. Isler 10 performans cekirdegine dagitilir.
#
#   ./webexport.sh <girdi> <cikti-dizini> [ad-onek] [genislikler...]
#   ./webexport.sh cephe.jpg ./web moonstone-cephe 640 1280 1920

set -euo pipefail
SRC=${1:?girdi gerekli}
OUT=${2:-./web}
NAME=${3:-$(basename "${SRC%.*}")}
shift 3 2>/dev/null || shift $# 
WIDTHS=("${@:-640 1280 1920}")
[ ${#WIDTHS[@]} -eq 1 ] && read -ra WIDTHS <<< "${WIDTHS[0]}"

mkdir -p "$OUT"
JOBS=$(sysctl -n hw.perflevel0.logicalcpu 2>/dev/null || echo 8)

emit() {
  w=$1
  base="$OUT/${NAME}-${w}"
  sips -Z "$w" "$SRC" --out "${base}.jpg" -s format jpeg -s formatOptions 82 >/dev/null
  sips -s format avif -s formatOptions 60 "${base}.jpg" --out "${base}.avif" >/dev/null 2>&1 || true
  command -v cwebp >/dev/null && cwebp -quiet -q 80 "${base}.jpg" -o "${base}.webp"
  printf '%s\n' "$(basename "${base}").{jpg,avif,webp}"
}
export -f emit; export SRC OUT NAME

printf '%s\n' "${WIDTHS[@]}" | xargs -P "$JOBS" -I{} bash -c 'emit {}'

echo "---"
ls -lh "$OUT" | awk 'NR>1 {printf "%-42s %s\n", $9, $5}'
echo "srcset icin:"
for w in "${WIDTHS[@]}"; do printf '  %s-%s.avif %sw\n' "$NAME" "$w" "$w"; done

#!/usr/bin/env python3
"""
make_title_card.py — Shorts/video üstüne binecek şeffaf başlık kartı.
SVG kurar, rsvg-convert ile rasterize eder (ev yolu; playwright yok).

Metin Shorts güvenli kutusunda durur: 1080x1920'de kenarlardan >=100 px,
üstten >=200 px, alttan >=480 px (references/youtube-shorts.md). Varsayılan
konum merkezin biraz üstü — akış metni ilk kareden görünür olmalı.

Kullanım:
  python3 make_title_card.py --title "TWO DESERTS, ONE THROAT" \
      --sub "TAIGA SAHEL" --ink "#E7DCC2" --accent "#B4622C" \
      --out title.png [--width 1080 --height 1920] [--y 0.42]

Punto karakter sayısından hesaplanır (rsvg textLength'i genisletir ama
SIKISTIRMAZ — CLAUDE.md § 5); textLength yalnız ince ayar yapar.
"""

import argparse
import html
import subprocess
import sys
from pathlib import Path

SAFE_X = 100          # yatay guvenli bosluk (1080 tuvalde)


def esc(s):
    return html.escape(s, quote=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True)
    ap.add_argument("--sub", default="")
    ap.add_argument("--ink", default="#E7DCC2", help="baslik rengi (sanatci kagidi)")
    ap.add_argument("--accent", default="#B4622C", help="alt satir / cizgi rengi")
    ap.add_argument("--out", required=True)
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1920)
    ap.add_argument("--y", type=float, default=0.42,
                    help="baslik merkezi, tuval yuksekliginin orani")
    ap.add_argument("--size", type=float, default=88,
                    help="punto TAVANI. 9:16'da 88 dogru; 16:9 alt-ucluk basliginda "
                         "dort dakika ekranda duracagi icin 40-52 daha iyi oturuyor")
    a = ap.parse_args()

    W, H = a.width, a.height
    box_w = W - 2 * SAFE_X
    # Helvetica Black ~0.75 em ortalama karakter genisligi (CLAUDE.md § 5)
    size = min(a.size, box_w / (0.75 * max(1, len(a.title))))
    tlen = min(box_w, 0.75 * size * len(a.title) * 1.04)
    y0 = H * a.y
    sub_size = max(30, size * 0.42)

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}">',
        # okunurluk icin metnin arkasina cok hafif karartma — kutu degil, tuyle
        f'<defs><radialGradient id="g" cx="0.5" cy="{a.y}" r="0.5">'
        f'<stop offset="0" stop-color="#000" stop-opacity="0.34"/>'
        f'<stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>',
        f'<rect width="{W}" height="{H}" fill="url(#g)"/>',
        f'<text x="{W/2}" y="{y0:.0f}" text-anchor="middle" '
        f'font-family="Helvetica Neue" font-weight="900" font-size="{size:.1f}" '
        f'fill="{a.ink}" textLength="{tlen:.0f}" '
        f'lengthAdjust="spacingAndGlyphs">{esc(a.title)}</text>',
    ]
    if a.sub:
        lines += [
            f'<rect x="{W/2 - 60:.0f}" y="{y0 + sub_size * 0.9:.0f}" width="120" '
            f'height="6" fill="{a.accent}"/>',
            f'<text x="{W/2}" y="{y0 + sub_size * 2.3:.0f}" text-anchor="middle" '
            f'font-family="Helvetica Neue" font-weight="700" '
            f'font-size="{sub_size:.1f}" letter-spacing="{sub_size*0.28:.1f}" '
            f'fill="{a.ink}" opacity="0.92">{esc(a.sub)}</text>',
        ]
    lines.append("</svg>")

    svg = Path(a.out).with_suffix(".svg")
    svg.write_text("\n".join(lines))
    subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H),
                    "-o", a.out, str(svg)], check=True)
    print(f"kart: {a.out} ({W}x{H}), punto {size:.0f}")


if __name__ == "__main__":
    sys.exit(main())

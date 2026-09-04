#!/usr/bin/env python3
"""Contact sheet — review every alternative side by side, plus the thumbnail gate.

A cover lives or dies at 64–160px in a playlist row. This builds two sheets:
one at readable size for art direction, one at true thumbnail scale so a design
that turns to mud can be caught before delivery.

    python scripts/contact_sheet.py out/*.png -o review/sheet.png
    python scripts/contact_sheet.py out/*.png -o review/sheet.png --thumb 120
"""
import argparse
import math
import pathlib

from PIL import Image, ImageDraw


def sheet(paths, cell, cols, label=True, pad=None, bg=(22, 22, 24), fg=(235, 232, 226)):
    pad = pad if pad is not None else max(cell // 16, 6)
    lab = max(cell // 8, 14) if label else 0
    rows = math.ceil(len(paths) / cols)
    W = cols * cell + (cols + 1) * pad
    H = rows * (cell + lab) + (rows + 1) * pad
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    for i, p in enumerate(paths):
        r, c = divmod(i, cols)
        x = pad + c * (cell + pad)
        y = pad + r * (cell + lab + pad)
        try:
            im = Image.open(p).convert("RGB")
        except Exception:
            continue
        s = min(im.size)
        im = im.crop(((im.width - s) // 2, (im.height - s) // 2,
                      (im.width - s) // 2 + s, (im.height - s) // 2 + s))
        out.paste(im.resize((cell, cell), Image.LANCZOS), (x, y))
        if label:
            d.text((x + 2, y + cell + 3), pathlib.Path(p).stem[:40], fill=fg)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("images", nargs="+")
    ap.add_argument("-o", "--out", default="review/sheet.png")
    ap.add_argument("--cell", type=int, default=420)
    ap.add_argument("--cols", type=int, default=0, help="0 = auto")
    ap.add_argument("--thumb", type=int, default=110, help="thumbnail-gate cell size")
    args = ap.parse_args()

    paths = sorted(args.images)
    cols = args.cols or min(len(paths), 4)
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    sheet(paths, args.cell, cols).save(out)
    print(f"  {out}")
    if args.thumb:
        t = out.with_name(out.stem + f"-thumb{args.thumb}" + out.suffix)
        sheet(paths, args.thumb, min(len(paths), 8), label=False, pad=10).save(t)
        print(f"  {t}   ← if a cover is illegible here, it fails in a playlist row")


if __name__ == "__main__":
    main()

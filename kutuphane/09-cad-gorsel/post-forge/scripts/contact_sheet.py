#!/usr/bin/env python3
"""Build a contact sheet from rendered post images — the feed-scroll squint test.

    python scripts/contact_sheet.py out/ --thumb 220

Thumbnails at ~220px wide simulate how the post appears mid-scroll. If the primary
message doesn't survive that size, the design fails regardless of how it looks at 1x.
Also reports mean luminance per slide so a carousel's light/dark rhythm is visible
as numbers, not just vibes.
"""
import argparse
import pathlib
import sys

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("pillow missing → pip install pillow")

EXT = {".png", ".jpg", ".jpeg", ".webp"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir", help="directory of rendered images")
    ap.add_argument("--thumb", type=int, default=220, help="thumbnail width in px")
    ap.add_argument("--cols", type=int, default=0, help="0 = auto")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    d = pathlib.Path(args.dir).resolve()
    files = sorted(f for f in d.iterdir()
                   if f.suffix.lower() in EXT and not f.name.startswith("_"))
    if not files:
        sys.exit(f"no images in {d}")

    pad, gap, label_h = 28, 18, 22
    thumbs = []
    for f in files:
        im = Image.open(f).convert("RGB")
        h = round(im.height * args.thumb / im.width)
        thumbs.append((f.name, im.resize((args.thumb, h), Image.LANCZOS)))

    cols = args.cols or min(len(thumbs), 6)
    rows = -(-len(thumbs) // cols)
    cell_h = max(t.height for _, t in thumbs) + label_h
    W = pad * 2 + cols * args.thumb + (cols - 1) * gap
    H = pad * 2 + rows * cell_h + (rows - 1) * gap

    sheet = Image.new("RGB", (W, H), (26, 26, 26))
    draw = ImageDraw.Draw(sheet)

    print(f"{'file':<34}{'thumb':>12}{'luminance':>11}")
    for i, (name, t) in enumerate(thumbs):
        r, c = divmod(i, cols)
        x = pad + c * (args.thumb + gap)
        y = pad + r * (cell_h + gap)
        sheet.paste(t, (x, y))
        draw.rectangle([x, y, x + t.width - 1, y + t.height - 1], outline=(70, 70, 70))
        draw.text((x, y + t.height + 5), name[:30], fill=(150, 150, 150))
        g = t.convert("L")
        lum = sum(g.tobytes()) / (g.width * g.height) / 255
        print(f"{name:<34}{t.width}x{t.height:>7}{lum:>11.2f}")

    out = pathlib.Path(args.out) if args.out else d / "_contact.png"
    sheet.save(out)
    print(f"\n✓ {out}")
    print("Now OPEN it. Gate: primary message legible at this size, set reads as one family,\n"
          "adjacent slides visibly different, light/dark rhythm present (see the luminance column).")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""frames_to_sheet.py — turn "almost pixel art" into disciplined pixel art + a uca-sheet/1.

Inputs (pick one):
  frames.json            uca-frames/1 written by blender/render_frames.py (3D -> pixel path)
  --dir FOLDER           one sub-folder per animation (folder name = anim name), images sorted by name
                         (AI generators: PixelLab / Retro Diffusion / any image model output)
  --strip PNG --frames N --anim NAME   a single horizontal strip

Pipeline (each step is there because a real failure needed it):
  1. de-scale      AI "pixel art" is often upscaled with a fractional grid -> detect block size, sample
                   the block MODE colour (not the average: averages invent new colours)
  2. alpha         threshold to 0/255 (soft edges = halo in Unity)
  3. palette       ONE palette for all frames (per-frame palettes flicker); median-cut to --colors,
                   or snap to a fixed --palette (hex list JSON) to match the rest of the game
  4. despeckle     remove isolated single pixels
  5. outline       optional 1px outline in the darkest palette colour
  6. baseline      grounded frames: lowest opaque row -> baseline (only if off by <= --max-snap px;
                   bigger offsets are real motion or real errors -> reported, not hidden)
  7. crop          uniform cell = union bbox + 1px margin, symmetric around the feet (pivot x = 0.5)

    python frames_to_sheet.py build/HeroPx/frames.json --out build/HeroPx/sheet --colors 14 --outline
    python frames_to_sheet.py --dir ai_out/knight --name Knight --out build/Knight --colors 16 --grid auto
Then ALWAYS: python pixel_qa.py <out>/<name>_sheet.json
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import os
import sys
from collections import Counter

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sheetio import hex_rgba, merge_duplicates, pixels, write_previews, write_sheet  # noqa: E402

ANIM_DEFAULTS = {  # loop, grounded, ms/frame   (used when the source has no timing)
    "idle": (True, True, 200), "walk": (True, True, 110), "run": (True, True, 80),
    "jump_rise": (False, False, 90), "jump_apex": (False, False, 150), "fall": (True, False, 120),
    "land": (False, True, 90), "attack": (False, True, 90), "hurt": (False, True, 120),
    "death": (False, True, 130),
}


def detect_grid(img: Image.Image, max_block: int = 16, min_score: float = 0.75) -> int:
    """Block size of an upscaled pixel image. AI output adds per-pixel colour noise, so 'equal colour'
    runs are useless: runs are split only where the colour jumps (L1 distance > 40 or alpha flips).
    Answer = the LARGEST block size b for which >= min_score of runs are ~multiples of b."""
    px = img.load()
    w, h = img.size

    def jump(p, q):
        if (p[3] > 127) != (q[3] > 127):
            return True
        return p[3] > 127 and abs(p[0] - q[0]) + abs(p[1] - q[1]) + abs(p[2] - q[2]) > 40
    runs = []
    for horizontal in (True, False):
        lines = range(0, h, max(1, h // 48)) if horizontal else range(0, w, max(1, w // 48))
        for i in lines:
            n = w if horizontal else h
            get = (lambda k: px[k, i]) if horizontal else (lambda k: px[i, k])
            start = 0
            for k in range(1, n):
                if jump(get(k), get(k - 1)):
                    if start > 0:  # skip the run touching the image border (unknown true length)
                        runs.append(k - start)
                    start = k
    runs = [r for r in runs if r <= max_block * 6]
    if len(runs) < 8:
        return 1
    for b in range(max_block, 1, -1):
        tol = 0 if b < 6 else 1   # small blocks must match exactly (3x must not read as 4x)
        ok = sum(1 for r in runs if r >= b - tol and min(r % b, b - r % b) <= tol)
        if ok / len(runs) >= min_score:
            return b
    return 1


def descale(img: Image.Image, block: int) -> Image.Image:
    if block <= 1:
        return img
    w, h = img.size
    out = Image.new("RGBA", (w // block, h // block))
    src = img.load()
    dst = out.load()
    for by in range(h // block):
        for bx in range(w // block):
            c = Counter(src[bx * block + i, by * block + j] for i in range(block) for j in range(block))
            dst[bx, by] = c.most_common(1)[0][0]
    return out


def alpha_threshold(img: Image.Image, t: int = 128) -> Image.Image:
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            px[x, y] = (r, g, b, 255) if a >= t else (0, 0, 0, 0)
    return img


def build_palette(frames: list[Image.Image], n: int) -> list[tuple]:
    opaque = [p for f in frames for p in pixels(f) if p[3] == 255]
    if not opaque:
        return []
    side = int(math.ceil(math.sqrt(len(opaque))))
    strip = Image.new("RGB", (side, side), opaque[0][:3])
    strip.putdata([p[:3] for p in opaque] + [opaque[0][:3]] * (side * side - len(opaque)))
    q = strip.quantize(colors=n, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pal = q.getpalette()[:3 * n]
    used = set(q.tobytes())
    return [tuple(pal[3 * i:3 * i + 3]) for i in sorted(used)]


def snap_palette(img: Image.Image, pal: list[tuple]) -> Image.Image:
    px = img.load()
    cache = {}
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a:
                k = (r, g, b)
                if k not in cache:
                    cache[k] = min(pal, key=lambda c: (c[0] - r) ** 2 * 0.3 + (c[1] - g) ** 2 * 0.59 + (c[2] - b) ** 2 * 0.11)
                px[x, y] = cache[k] + (255,)
    return img


def despeckle(img: Image.Image) -> int:
    px = img.load()
    w, h = img.size
    kill = [(x, y) for y in range(h) for x in range(w) if px[x, y][3] and not any(
        0 <= x + dx < w and 0 <= y + dy < h and px[x + dx, y + dy][3]
        for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy)]
    for x, y in kill:
        px[x, y] = (0, 0, 0, 0)
    return len(kill)


def add_outline(img: Image.Image, col: tuple) -> Image.Image:
    w, h = img.size
    out = Image.new("RGBA", (w + 2, h + 2), (0, 0, 0, 0))
    out.paste(img, (1, 1))
    src = out.copy().load()
    dst = out.load()
    for y in range(h + 2):
        for x in range(w + 2):
            if not src[x, y][3] and any(0 <= x + dx < w + 2 and 0 <= y + dy < h + 2 and src[x + dx, y + dy][3]
                                        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                dst[x, y] = col + (255,)
    return out


def _natural(path: str):
    import re
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", os.path.basename(path).lower())]


def load_inputs(a) -> tuple[list[dict], int | None]:
    """-> ([{name, loop, grounded, frames:[Image], durations}], ground_row_from_bottom or None)"""
    anims, ground = [], None
    if a.frames_json:
        with open(a.frames_json, encoding="utf-8") as f:
            fm = json.load(f)
        base = os.path.dirname(a.frames_json)
        ground = fm.get("groundRow")
        for an in fm["animations"]:
            anims.append({"name": an["name"], "loop": an["loop"], "grounded": an["grounded"],
                          "frames": [Image.open(os.path.join(base, p)).convert("RGBA") for p in an["files"]],
                          "durations": list(an["durationMs"])})
        a.name = a.name or fm["name"]
    elif a.dir:
        for sub in sorted(d for d in glob.glob(os.path.join(a.dir, "*")) if os.path.isdir(d)):
            files = sorted(glob.glob(os.path.join(sub, "*.png")) + glob.glob(os.path.join(sub, "*.webp")),
                           key=_natural)
            if not files:
                continue
            nm = os.path.basename(sub).lower()
            loop, grounded, ms = ANIM_DEFAULTS.get(nm, (True, True, 100))
            anims.append({"name": nm, "loop": loop, "grounded": grounded,
                          "frames": [Image.open(p).convert("RGBA") for p in files], "durations": [ms] * len(files)})
    elif a.strip:
        img = Image.open(a.strip).convert("RGBA")
        n = a.frames
        fw = img.width // n
        loop, grounded, ms = ANIM_DEFAULTS.get(a.anim, (True, True, 100))
        anims.append({"name": a.anim, "loop": loop, "grounded": grounded,
                      "frames": [img.crop((i * fw, 0, (i + 1) * fw, img.height)) for i in range(n)],
                      "durations": [ms] * n})
    else:
        raise SystemExit("give frames.json, --dir or --strip")
    return anims, ground


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("frames_json", nargs="?")
    ap.add_argument("--dir")
    ap.add_argument("--strip")
    ap.add_argument("--frames", type=int, default=1)
    ap.add_argument("--anim", default="idle")
    ap.add_argument("--name", default="")
    ap.add_argument("--out", required=True)
    ap.add_argument("--colors", type=int, default=16)
    ap.add_argument("--palette", help="JSON list of hex colours to snap to (overrides --colors)")
    ap.add_argument("--grid", default="1", help="'auto' to detect upscale block size, or an int")
    ap.add_argument("--outline", action="store_true")
    ap.add_argument("--outline-color", default="")
    ap.add_argument("--baseline", type=int, default=2)
    ap.add_argument("--max-snap", type=int, default=2)
    ap.add_argument("--ppu", type=int, default=16)
    a = ap.parse_args()
    anims, ground = load_inputs(a)
    report = {"grid": {}, "despeckled": 0, "snapped": [], "notSnapped": []}
    # 1-2 descale + alpha
    for an in anims:
        new = []
        for fr in an["frames"]:
            b = detect_grid(fr) if a.grid == "auto" else int(a.grid)
            report["grid"][an["name"]] = b
            new.append(alpha_threshold(descale(fr, b)))
        an["frames"] = new
    # 3 palette
    allf = [f for an in anims for f in an["frames"]]
    if a.palette:
        with open(a.palette, encoding="utf-8") as f:
            pal = [hex_rgba(h)[:3] for h in json.load(f)]
    else:
        pal = build_palette(allf, a.colors)
    for f in allf:
        snap_palette(f, pal)
        report["despeckled"] += despeckle(f)
    # 5 outline
    if a.outline:
        oc = hex_rgba(a.outline_color)[:3] if a.outline_color else min(pal, key=lambda c: sum(c))
        for an in anims:
            an["frames"] = [add_outline(f, oc) for f in an["frames"]]
        # NOTE: ground row (counted from the bottom) is unchanged: the 1px pad and the new outline row
        # under the feet cancel out. Adding 1 here made every grounded frame "snap" and airborne ones sink.
    # 6 baseline: every frame gets the same canvas; ground row = source ground row (3D) or lowest idle row
    W, H = anims[0]["frames"][0].size
    if ground is None:
        lows = [f.getchannel("A").getbbox()[3] - 1 for an in anims if an["grounded"] for f in an["frames"]
                if f.getchannel("A").getbbox()]
        ground_row = Counter(lows).most_common(1)[0][0] if lows else H - 1
    else:
        ground_row = H - 1 - ground
    for an in anims:
        for i, f in enumerate(an["frames"]):
            bb = f.getchannel("A").getbbox()
            if not bb or not an["grounded"]:
                continue
            d = ground_row - (bb[3] - 1)
            if d and abs(d) <= a.max_snap:
                g = Image.new("RGBA", f.size, (0, 0, 0, 0))
                g.paste(f, (0, d))
                an["frames"][i] = g
                report["snapped"].append(f"{an['name']}[{i}] {d:+d}px")
            elif d:
                report["notSnapped"].append(f"{an['name']}[{i}] off by {d:+d}px (left as is — check the source)")
    # 7 crop symmetric around the feet column (canvas centre = feet for 3D renders; median x for AI)
    x0, x1, y0 = W, 0, H
    for an in anims:
        for f in an["frames"]:
            bb = f.getchannel("A").getbbox()
            if bb:
                x0, x1, y0 = min(x0, bb[0]), max(x1, bb[2] - 1), min(y0, bb[1])
    cx = W // 2
    half = max(cx - x0, x1 - cx + 1) + 1
    top = y0 - 1
    fw = 2 * half
    fh = (ground_row + 1 + a.baseline) - top
    fh += fh % 2
    top = ground_row + 1 + a.baseline - fh
    box = (cx - half, top, cx + half, top + fh)
    out_anims = []
    for an in anims:
        frames = []
        for f in an["frames"]:
            c = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
            c.paste(f.crop((max(0, box[0]), max(0, box[1]), min(W, box[2]), min(H, box[3]))),
                    (max(0, -box[0]), max(0, -box[1])))
            frames.append(c)
        frames, durs, ev = merge_duplicates(frames, list(an["durations"]), [], an["loop"])
        out_anims.append({**an, "frames": frames, "durations": durs, "events": ev})
    png, js = write_sheet(a.out, a.name or "Character", out_anims, fw, fh, a.baseline, ppu=a.ppu,
                          extra={"generator": "frames_to_sheet.py", "palette": ["#%02x%02x%02x" % c for c in pal]})
    write_previews(js)
    report.update({"sheet": png, "meta": js, "frame": [fw, fh], "colors": len(pal)})
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

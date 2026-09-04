#!/usr/bin/env python3
"""Plates — procedural base imagery for covers when there is no photograph.

Generates the *under-layer* only: shapes, gradients, horizons, sunbursts, noise
fields. It is deliberately clean and un-aged, because darkroom.py is what makes
it look printed in 1973. Type goes on top later, in HTML.

    python scripts/plates.py sungrid --palette neon84 -o work/plate.png
    python scripts/plates.py geo --palette bluenote --seed 4 -o work/plate.png
    python scripts/plates.py --list

    # the usual pairing
    python scripts/plates.py clouds --palette prog73 -o work/p.png
    python scripts/darkroom.py work/p.png --preset hipgnosis-1973 -o out/cover.png

Every generator is seeded: same seed, same plate. Reroll by changing --seed.
"""
import argparse
import math
import pathlib
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

PALETTES = {
    "bluenote": ["#0b1a2e", "#e9dcbf", "#c9552f", "#7c8b91"],
    "verve": ["#231f20", "#f0e3c8", "#b08d3f", "#6b6f52"],
    "lounge62": ["#f0e3c8", "#d9772b", "#2f6f6b", "#231f20"],
    "psych68": ["#2b0a4a", "#e0344f", "#f7d84a", "#1f7a5c"],
    "prog73": ["#1a2b1f", "#d8cbb0", "#8a5a2b", "#4a6b52"],
    "soul75": ["#3a1408", "#c8622a", "#f2d9a0", "#7a1f1f"],
    "library70": ["#e8e3d3", "#1f1f1f", "#d94f2b", "#3b6ea5"],
    "punk77": ["#141414", "#f1eee6", "#e5202e", "#8a8a8a"],
    "postpunk81": ["#0e0e10", "#d8d8d2", "#8c9aa6", "#5a4a3a"],
    "neon84": ["#0a0518", "#ff2d95", "#00e5ff", "#ffd400"],
    "vhs87": ["#101426", "#f24b6a", "#35d0c8", "#f5e9c8"],
    "riso90": ["#f6efdd", "#ff4a3d", "#1b3fa0", "#ffd23f"],
    "grunge93": ["#1b1a17", "#cfc7b3", "#6b7b4a", "#a8412a"],
    "vapor95": ["#2a1240", "#f7c8dc", "#2de1c2", "#fdf6a0"],
}


def hexes(spec, seed=0):
    if spec in PALETTES:
        return list(PALETTES[spec])
    cols = [c.strip() for c in spec.split("/") if c.strip()]
    if not cols:
        sys.exit("empty palette")
    return ["#" + c.lstrip("#") for c in cols]


def rgb(c):
    c = c.lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def arr(colors):
    return [np.array(rgb(c), dtype=np.float64) for c in colors]


def blank(size, color):
    return Image.new("RGB", (size, size), rgb(color))


def field(size, seed, octaves=5, persistence=0.55):
    """Fractal value noise 0..1 via stacked upsampled random grids."""
    rng = np.random.default_rng(seed)
    total = np.zeros((size, size))
    amp, norm = 1.0, 0.0
    for o in range(octaves):
        n = 2 ** (o + 2)
        g = rng.random((n, n))
        layer = np.asarray(Image.fromarray((g * 255).astype(np.uint8))
                           .resize((size, size), Image.BICUBIC), dtype=np.float64) / 255.0
        total += layer * amp
        norm += amp
        amp *= persistence
    total /= norm
    return (total - total.min()) / max(np.ptp(total), 1e-6)


def linear_gradient(size, c0, c1, angle=90.0):
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float64) / size
    a = math.radians(angle)
    t = xx * math.cos(a) + yy * math.sin(a)
    t = (t - t.min()) / max(np.ptp(t), 1e-6)
    a0, a1 = np.array(rgb(c0), float), np.array(rgb(c1), float)
    return a0 + (a1 - a0) * t[..., None]


def to_img(a):
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")


# ---------------------------------------------------------------- generators

def gen_sunburst(size, pal, rng, p):
    rays = int(p.get("rays", 24))
    cx, cy = size * float(p.get("cx", 0.5)), size * float(p.get("cy", 0.42))
    im = blank(size, pal[1])
    d = ImageDraw.Draw(im)
    R = size * 1.6
    for i in range(rays * 2):
        if i % 2:
            continue
        a0 = math.tau * i / (rays * 2)
        a1 = math.tau * (i + 1) / (rays * 2)
        d.polygon([(cx, cy),
                   (cx + R * math.cos(a0), cy + R * math.sin(a0)),
                   (cx + R * math.cos((a0 + a1) / 2) * 1.05, cy + R * math.sin((a0 + a1) / 2) * 1.05),
                   (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=rgb(pal[2]))
    d.ellipse([cx - size * 0.17, cy - size * 0.17, cx + size * 0.17, cy + size * 0.17], fill=rgb(pal[0]))
    return im


def gen_sungrid(size, pal, rng, p):
    """Synthwave / late-70s prog horizon: gradient sky, slatted sun, perspective grid."""
    hz = float(p.get("horizon", 0.62))
    sky = linear_gradient(size, pal[0], pal[2], 90)
    im = to_img(sky)
    d = ImageDraw.Draw(im)
    # sun
    sr = size * float(p.get("sun", 0.22))
    scx, scy = size * 0.5, size * hz
    d.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], fill=rgb(pal[1]))
    # slats: dense at the horizon, opening up as they climb the sun
    slat = max(int(size * 0.013), 2)
    y = scy - slat * 2
    gap = slat * 0.6
    while y > scy - sr:
        d.rectangle([scx - sr - 4, y, scx + sr + 4, y + slat], fill=rgb(pal[0]))
        y -= slat + gap
        gap *= 1.35
    # ground
    d.rectangle([0, size * hz, size, size], fill=rgb(pal[0]))
    line = rgb(pal[3] if len(pal) > 3 else pal[2])
    lw = max(int(size / 500), 2)
    vp = (size * 0.5, size * hz)
    for i in range(-14, 15):
        x = size * 0.5 + i * size * 0.11
        d.line([vp, (size * 0.5 + i * size * 0.9, size * 1.05)], fill=line, width=lw)
    yy, step = size * hz, size * 0.008
    while yy < size:
        d.line([(0, yy), (size, yy)], fill=line, width=lw)
        step *= 1.42
        yy += step
    return im


def gen_rings(size, pal, rng, p):
    n = int(p.get("n", 9))
    im = blank(size, pal[1])
    d = ImageDraw.Draw(im)
    cx, cy = size * float(p.get("cx", 0.5)), size * float(p.get("cy", 0.5))
    for i in range(n, 0, -1):
        r = size * 0.72 * i / n
        col = pal[0] if i % 2 else pal[2]
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=rgb(col))
    return im


def gen_stripes(size, pal, rng, p):
    n = int(p.get("n", 7))
    ang = float(p.get("angle", 0))
    big = int(size * 1.6)
    im = Image.new("RGB", (big, big), rgb(pal[1]))
    d = ImageDraw.Draw(im)
    band = big / n
    for i in range(n + 1):
        col = pal[0] if i % 2 else pal[2]
        d.rectangle([0, i * band, big, i * band + band * float(p.get("duty", 0.55))], fill=rgb(col))
    im = im.rotate(ang, resample=Image.BICUBIC)
    off = (big - size) // 2
    return im.crop((off, off, off + size, off + size))


def gen_geo(size, pal, rng, p):
    """Bauhaus / Blue Note geometry: a few confident shapes on a flat field."""
    im = blank(size, pal[1])
    d = ImageDraw.Draw(im)
    n = int(p.get("n", 4))
    for i in range(n):
        col = rgb(pal[(i % (len(pal) - 1)) + 1] if i else pal[0])
        kind = rng.choice(["circle", "quarter", "bar", "tri", "arc"])
        s = size * rng.uniform(0.28, 0.8)
        x = rng.uniform(-0.15, 0.85) * size
        y = rng.uniform(-0.15, 0.85) * size
        if kind == "circle":
            d.ellipse([x, y, x + s, y + s], fill=col)
        elif kind == "quarter":
            start = int(rng.choice([0, 90, 180, 270]))
            d.pieslice([x, y, x + s, y + s], start, start + int(rng.choice([90, 180])), fill=col)
        elif kind == "bar":
            th = s * rng.uniform(0.12, 0.3)
            if rng.random() > 0.5:
                d.rectangle([x, y, x + s, y + th], fill=col)
            else:
                d.rectangle([x, y, x + th, y + s], fill=col)
        elif kind == "tri":
            d.polygon([(x, y + s), (x + s / 2, y), (x + s, y + s)], fill=col)
        else:
            w = max(int(s * 0.10), 4)
            d.arc([x, y, x + s, y + s], rng.integers(0, 200), rng.integers(200, 360),
                  fill=col, width=w)
    return im


def gen_dots(size, pal, rng, p):
    n = int(p.get("n", 14))
    im = blank(size, pal[1])
    d = ImageDraw.Draw(im)
    cell = size / n
    for iy in range(n):
        for ix in range(n):
            t = (ix / (n - 1) * 0.5 + iy / (n - 1) * 0.5)
            r = cell * 0.48 * (0.15 + t)
            cx, cy = (ix + 0.5) * cell, (iy + 0.5) * cell
            col = pal[0] if (ix + iy) % 3 else pal[2]
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=rgb(col))
    return im


def gen_clouds(size, pal, rng, p):
    """Hipgnosis-ish sky / marbled field from fractal noise."""
    seed = int(p.get("seed", 1))
    f = field(size, seed, octaves=int(p.get("octaves", 6)))
    if p.get("marble"):
        f = np.abs(np.sin(f * math.tau * float(p.get("veins", 3))))
    a = arr(pal)
    base = a[0] + (a[1] - a[0]) * f[..., None]
    accent = np.clip((f - 0.62) / 0.38, 0, 1)[..., None]
    return to_img(base * (1 - accent) + a[2] * accent)


def gen_mountains(size, pal, rng, p):
    layers = int(p.get("layers", 4))
    im = to_img(linear_gradient(size, pal[0], pal[1], 90))
    d = ImageDraw.Draw(im)
    for i in range(layers):
        t = (i + 1) / layers
        base = size * (0.45 + 0.14 * i)
        amp = size * 0.16 * (1.2 - t)
        xs = np.linspace(0, size, 60)
        ridge = field(64, int(rng.integers(0, 10 ** 6)))[0] * 0
        ys = base - (np.sin(xs / size * math.tau * (1.4 + i)) * amp
                     + np.sin(xs / size * math.tau * (3.7 + i * 2)) * amp * 0.45)
        pts = [(float(x), float(y)) for x, y in zip(xs, ys)]
        col = arr(pal)[0] * (1 - t * 0.55) + arr(pal)[2] * (t * 0.55)
        d.polygon(pts + [(size, size), (0, size)], fill=tuple(col.astype(int)))
    return im


def gen_starfield(size, pal, rng, p):
    im = to_img(linear_gradient(size, pal[0], pal[0], 90))
    d = ImageDraw.Draw(im)
    n = int(p.get("n", 900))
    for _ in range(n):
        x, y = rng.uniform(0, size), rng.uniform(0, size)
        r = max(size / 1400, 1) * rng.uniform(0.4, 2.4)
        v = rng.uniform(0.35, 1.0)
        col = tuple((np.array(rgb(pal[1])) * v).astype(int))
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    # one big body
    if p.get("planet", "1") not in ("0", "false"):
        R = size * float(p.get("planet_r", 0.3))
        cx, cy = size * rng.uniform(0.3, 0.7), size * rng.uniform(0.3, 0.7)
        d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=rgb(pal[2]))
    return im


def gen_checker(size, pal, rng, p):
    """Perspective floor — vaporwave / 80s stage."""
    n = int(p.get("n", 12))
    hz = float(p.get("horizon", 0.45))
    im = to_img(linear_gradient(size, pal[0], pal[2], 90))
    d = ImageDraw.Draw(im)
    d.rectangle([0, size * hz, size, size], fill=rgb(pal[0]))
    rows, y, step = [], size * hz, size * 0.006
    while y < size * 1.2:
        rows.append(y)
        step *= 1.45
        y += step
    for r in range(len(rows) - 1):
        y0, y1 = rows[r], rows[r + 1]
        span0 = (y0 - size * hz) / max(size * (1 - hz), 1) * size * 2.2
        span1 = (y1 - size * hz) / max(size * (1 - hz), 1) * size * 2.2
        for c in range(-n, n):
            if (r + c) % 2:
                continue
            d.polygon([(size / 2 + c * span0 / n, y0), (size / 2 + (c + 1) * span0 / n, y0),
                       (size / 2 + (c + 1) * span1 / n, y1), (size / 2 + c * span1 / n, y1)],
                      fill=rgb(pal[1]))
    return im


def gen_blobs(size, pal, rng, p):
    """Liquid psychedelic lettering-ready field."""
    f1 = field(size, int(rng.integers(0, 10 ** 6)), octaves=3)
    f2 = field(size, int(rng.integers(0, 10 ** 6)), octaves=4)
    a = arr(pal)
    m1 = (f1 > 0.52).astype(float)[..., None]
    m2 = (f2 > 0.58).astype(float)[..., None]
    out = a[1] * (1 - m1) + a[0] * m1
    out = out * (1 - m2) + a[2] * m2
    im = to_img(out).filter(ImageFilter.GaussianBlur(size / 500))
    return im


def gen_mesh(size, pal, rng, p):
    """Soft multi-point gradient — 70s airbrush ground."""
    a = arr(pal)
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float64) / size
    out = np.zeros((size, size, 3))
    wsum = np.zeros((size, size))
    for i, col in enumerate(a):
        cx, cy = rng.uniform(0.1, 0.9), rng.uniform(0.1, 0.9)
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        w = np.exp(-(d ** 2) / (2 * rng.uniform(0.10, 0.30) ** 2)) + 1e-4
        out += col * w[..., None]
        wsum += w
    return to_img(out / wsum[..., None])


GENS = {
    "sunburst": gen_sunburst, "sungrid": gen_sungrid, "rings": gen_rings,
    "stripes": gen_stripes, "geo": gen_geo, "dots": gen_dots,
    "clouds": gen_clouds, "mountains": gen_mountains, "starfield": gen_starfield,
    "checker": gen_checker, "blobs": gen_blobs, "mesh": gen_mesh,
}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kind", nargs="?", help=f"one of: {', '.join(sorted(GENS))}")
    ap.add_argument("-o", "--out", default="work/plate.png")
    ap.add_argument("--palette", default="bluenote",
                    help="palette name or #hex/#hex/#hex (dark/light/accent/second)")
    ap.add_argument("--size", type=int, default=3000)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--set", default="", help="generator params, k:v;k:v")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    if args.list:
        print("generators: " + ", ".join(sorted(GENS)))
        print("palettes:   " + ", ".join(PALETTES))
        return
    if not args.kind or args.kind not in GENS:
        sys.exit(f"pick a generator: {', '.join(sorted(GENS))}")

    p = {}
    for kv in args.set.split(";"):
        if kv.strip() and ":" in kv:
            k, _, v = kv.partition(":")
            p[k.strip()] = v.strip()
    p.setdefault("seed", args.seed)

    pal = hexes(args.palette)
    while len(pal) < 4:
        pal.append(pal[-1])
    rng = np.random.default_rng(args.seed)
    im = GENS[args.kind](args.size, pal, rng, p)
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out)
    print(f"  {out}  {im.size[0]}×{im.size[1]}")


if __name__ == "__main__":
    main()

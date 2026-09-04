#!/usr/bin/env python3
"""
make_plates.py — procedural grayscale "plates" for ambient-video-forge.

Plates are still PNGs (mode L) that the ffmpeg graph animates with periodic
crop/rotate/opacity. Baking the texture once and animating it periodically is
what makes long healing-music videos cheap AND seamlessly loopable: no temporal
noise, no per-frame procedural cost, and the motion is a sine so frame 0 and
frame N match exactly.

Usage:
  python3 make_plates.py --out plates --seed 4211 --size 2600x1460 \
      --types fog,plume,dust,bokeh,rays,stars,caustics,grain

Every plate is deterministic in (seed, type, size): same inputs -> same PNG.
That is how an album keeps a shared visual identity while each track differs
(album seed fixed, track index perturbs the seed).
"""
import argparse
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

# --------------------------------------------------------------------------
# noise primitives
# --------------------------------------------------------------------------


def _octave(h: int, w: int, res_y: int, res_x: int, rng) -> np.ndarray:
    """One octave of value noise: random grid, bicubic-upscaled to (h, w)."""
    g = rng.random((max(2, res_y), max(2, res_x))).astype(np.float32)
    im = Image.fromarray(np.uint8(g * 255), "L").resize((w, h), Image.BICUBIC)
    return np.asarray(im, dtype=np.float32) / 255.0


def fbm(h, w, rng, octaves=5, base=3, gain=0.55, aspect=1.0) -> np.ndarray:
    """Fractal sum of value-noise octaves. aspect>1 stretches features in x."""
    total = np.zeros((h, w), np.float32)
    amp, norm = 1.0, 0.0
    for o in range(octaves):
        step = 2**o
        total += amp * _octave(h, w, int(base * step), int(base * step * aspect), rng)
        norm += amp
        amp *= gain
    return total / norm


def _sample(field: np.ndarray, ys: np.ndarray, xs: np.ndarray) -> np.ndarray:
    """Bilinear sample of a 2D field at float coords."""
    h, w = field.shape
    ys = np.clip(ys, 0, h - 1.001)
    xs = np.clip(xs, 0, w - 1.001)
    y0 = ys.astype(np.int32)
    x0 = xs.astype(np.int32)
    y1 = np.minimum(y0 + 1, h - 1)
    x1 = np.minimum(x0 + 1, w - 1)
    fy = ys - y0
    fx = xs - x0
    top = field[y0, x0] * (1 - fx) + field[y0, x1] * fx
    bot = field[y1, x0] * (1 - fx) + field[y1, x1] * fx
    return top * (1 - fy) + bot * fy


def domain_warp(field, wx, wy, strength) -> np.ndarray:
    """Push sample coords around by two noise fields. This is what turns bland
    cloud noise into something that reads as *smoke* — the curl comes from the
    warp, not from the base noise."""
    h, w = field.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    return _sample(field, yy + (wy - 0.5) * strength, xx + (wx - 0.5) * strength)


def norm01(a: np.ndarray) -> np.ndarray:
    lo, hi = float(a.min()), float(a.max())
    return (a - lo) / (hi - lo + 1e-6)


def contrast(a: np.ndarray, gamma=1.0, lift=0.0, gain=1.0) -> np.ndarray:
    return np.clip(np.power(np.clip(a, 0, 1), gamma) * gain + lift, 0, 1)


def save(a: np.ndarray, path: str, blur=0.0):
    im = Image.fromarray(np.uint8(np.clip(a, 0, 1) * 255), "L")
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    im.save(path, optimize=True)
    return path


def vgrad(h, w, top=0.0, bottom=1.0, power=1.0) -> np.ndarray:
    g = np.linspace(0, 1, h, dtype=np.float32) ** power
    return (top + (bottom - top) * g)[:, None].repeat(w, axis=1)


# --------------------------------------------------------------------------
# plates
# --------------------------------------------------------------------------


def plate_fog(h, w, rng):
    """Soft low-lying haze. Wide, slow, mostly horizontal bands."""
    f = fbm(h, w, rng, octaves=5, base=2, gain=0.6, aspect=2.2)
    wx = fbm(h, w, rng, octaves=3, base=2, aspect=2.0)
    wy = fbm(h, w, rng, octaves=3, base=2, aspect=2.0)
    f = domain_warp(f, wx, wy, strength=w * 0.05)
    f = norm01(f)
    f = contrast(f, gamma=1.8, gain=1.15)
    return f * vgrad(h, w, top=0.35, bottom=1.0, power=1.6)


def plate_plume(h, w, rng):
    """Vertical smoke column / incense trail. Strong warp, tall features."""
    f = fbm(h, w, rng, octaves=6, base=2, gain=0.58, aspect=0.45)
    wx = fbm(h, w, rng, octaves=4, base=3, aspect=0.5)
    wy = fbm(h, w, rng, octaves=4, base=3, aspect=0.5)
    f = domain_warp(f, wx, wy, strength=w * 0.11)
    f = norm01(f)
    f = contrast(f, gamma=2.6, gain=1.35)
    # taper the sides so the column does not touch the frame edge
    x = np.linspace(-1, 1, w, dtype=np.float32)[None, :]
    return f * np.exp(-(x**2) * 2.2)


def plate_ink(h, w, rng):
    """Dense curling smoke, full-frame. Heavier than fog, for dark covers."""
    f = fbm(h, w, rng, octaves=6, base=3, gain=0.62, aspect=1.2)
    wx = fbm(h, w, rng, octaves=4, base=4)
    wy = fbm(h, w, rng, octaves=4, base=4)
    f = domain_warp(f, wx, wy, strength=w * 0.14)
    f = domain_warp(f, wy, wx, strength=w * 0.05)  # second pass = tighter curls
    return contrast(norm01(f), gamma=1.9, gain=1.2)


def _blobs(h, w, rng, count, rmin, rmax, bright=(0.35, 1.0), ring=0.0, ss=2):
    """Draw soft round blobs on black at 1/ss resolution, then upscale.

    Radii and counts arrive calibrated for a 2880x1620 plate and are rescaled
    here, so a 640x360 draft and a 1080p final look the same instead of the
    draft being covered in giant smudges. Count scales with area to hold the
    density constant; radius scales with width."""
    k = w / 2880.0
    rmin, rmax = rmin * k, rmax * k
    count = max(4, int(round(count * k * k)))
    hh, ww = h // ss, w // ss
    canvas = Image.new("L", (ww, hh), 0)
    d = ImageDraw.Draw(canvas)
    for _ in range(count):
        cx, cy = rng.random() * ww, rng.random() * hh
        r = (rmin + rng.random() * (rmax - rmin)) / ss
        v = int(255 * (bright[0] + rng.random() * (bright[1] - bright[0])))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=v)
        if ring and rng.random() < ring:
            ri = r * 0.62
            d.ellipse([cx - ri, cy - ri, cx + ri, cy + ri], fill=int(v * 0.25))
    canvas = canvas.resize((w, h), Image.BILINEAR)
    return np.asarray(canvas, dtype=np.float32) / 255.0


def plate_dust(h, w, rng):
    """Fine motes. Two sizes so a parallax pass has something to separate."""
    a = _blobs(h, w, rng, count=520, rmin=2, rmax=6, bright=(0.25, 0.9))
    b = _blobs(h, w, rng, count=90, rmin=7, rmax=14, bright=(0.4, 1.0))
    out = np.clip(a + b * 0.8, 0, 1)
    return out


def plate_bokeh(h, w, rng):
    """Big out-of-focus orbs, some as rings. Reads as lens bokeh when blurred."""
    out = _blobs(h, w, rng, count=34, rmin=40, rmax=150, bright=(0.18, 0.55), ring=0.45)
    return out


def plate_stars(h, w, rng):
    pts = _blobs(h, w, rng, count=900, rmin=1, rmax=3, bright=(0.2, 1.0), ss=1)
    big = _blobs(h, w, rng, count=25, rmin=4, rmax=9, bright=(0.7, 1.0), ss=1)
    neb = contrast(norm01(fbm(h, w, rng, octaves=5, base=2)), gamma=3.2) * 0.22
    return np.clip(pts + big + neb, 0, 1)


def plate_rays(h, w, rng):
    """God rays from a point above the frame, angular noise for streak variety."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w * (0.3 + 0.4 * rng.random()), -h * 0.35
    dx, dy = xx - cx, yy - cy
    r = np.sqrt(dx * dx + dy * dy)
    theta = np.arctan2(dy, dx)
    n = 220
    prof = rng.random(n).astype(np.float32)
    prof = np.convolve(np.tile(prof, 3), np.ones(9) / 9, mode="same")[n : 2 * n]
    t01 = (theta - theta.min()) / (theta.max() - theta.min() + 1e-6)
    ang = np.interp(t01, np.linspace(0, 1, n), prof).astype(np.float32)
    fall = np.exp(-r / (h * 0.95))
    out = contrast(norm01(ang), gamma=2.4) * fall
    return norm01(out)


def plate_caustics(h, w, rng):
    """Interfering sines -> water light / heat shimmer. Mid-gray centred so it
    is also usable directly as a displace map."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    acc = np.zeros((h, w), np.float32)
    for _ in range(6):
        ang = rng.random() * np.pi * 2
        freq = (3 + rng.random() * 9) * np.pi * 2 / w
        acc += np.sin((np.cos(ang) * xx + np.sin(ang) * yy) * freq + rng.random() * 6.28)
    acc = norm01(acc)
    return contrast(acc, gamma=1.4)


def plate_warpmap(h, w, rng):
    """Smooth field centred on 0.5 — feed to ffmpeg `displace` for organic
    liquid/heat distortion of the artwork itself."""
    f = fbm(h, w, rng, octaves=4, base=2, gain=0.5, aspect=1.4)
    f = norm01(f)
    return 0.5 + (f - f.mean()) * 0.9  # keep it near mid-gray = small shifts


def plate_grain(h, w, rng):
    """Static grain plate. Cheaper and calmer than ffmpeg temporal noise when
    you only want texture, not sizzle. (For dithering gradients, prefer the
    temporal `noise` filter — see references/encoding.md.)"""
    g = rng.random((h, w)).astype(np.float32)
    im = Image.fromarray(np.uint8(g * 255), "L").filter(ImageFilter.GaussianBlur(0.6))
    return np.asarray(im, dtype=np.float32) / 255.0


# blur applied on save, and whether the plate is smooth enough to be computed
# at half resolution and upscaled (4x faster, visually identical for soft fields)
POLICY = {
    "fog":      {"blur": 0.0, "half": True},
    "plume":    {"blur": 0.0, "half": True},
    "ink":      {"blur": 0.0, "half": True},
    "dust":     {"blur": 1.2, "half": False},
    "bokeh":    {"blur": 9.0, "half": False},
    "stars":    {"blur": 0.0, "half": False},
    "rays":     {"blur": 3.0, "half": True},
    "caustics": {"blur": 0.0, "half": True},
    "warpmap":  {"blur": 0.0, "half": True},
    "grain":    {"blur": 0.0, "half": False},
}

PLATES = {
    "fog": plate_fog,
    "plume": plate_plume,
    "ink": plate_ink,
    "dust": plate_dust,
    "bokeh": plate_bokeh,
    "stars": plate_stars,
    "rays": plate_rays,
    "caustics": plate_caustics,
    "warpmap": plate_warpmap,
    "grain": plate_grain,
}


def build(types, out_dir, seed, w, h, verbose=True, cache=True):
    """Generate the requested plates into out_dir. Results are cached by
    (type, seed, size) so re-running probe/loop stages costs nothing."""
    os.makedirs(out_dir, exist_ok=True)
    made = {}
    for t in types:
        if t not in PLATES:
            raise SystemExit(f"unknown plate type: {t} (have: {', '.join(PLATES)})")
        pol = POLICY.get(t, {"blur": 0.0, "half": False})
        path = os.path.join(out_dir, f"{t}_{seed}_{w}x{h}.png")
        if cache and os.path.exists(path):
            made[t] = path
            if verbose:
                print(f"  plate {t:9s} (cached)")
            continue
        # per-type seed offset so 'fog' and 'ink' of the same seed differ
        rng = np.random.default_rng((seed * 1000003 + sum(map(ord, t))) % (2**63))
        if pol["half"]:
            gw, gh = max(64, w // 2), max(64, h // 2)
            arr = PLATES[t](gh, gw, rng)
            im = Image.fromarray(np.uint8(np.clip(arr, 0, 1) * 255), "L").resize(
                (w, h), Image.BICUBIC)
            arr = np.asarray(im, dtype=np.float32) / 255.0
        else:
            arr = PLATES[t](h, w, rng)
        save(arr, path, blur=pol["blur"] * (w / 2880.0))
        made[t] = path
        if verbose:
            print(f"  plate {t:9s} -> {os.path.basename(path)}")
    return made


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="plates")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--size", default="2600x1460", help="WxH of the plate")
    ap.add_argument("--types", default="fog,plume,dust,bokeh,rays,stars,caustics,warpmap")
    a = ap.parse_args()
    w, h = (int(v) for v in a.size.lower().split("x"))
    build([t.strip() for t in a.types.split(",") if t.strip()], a.out, a.seed, w, h)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Darkroom — analogue print & photo treatments for retro cover art.

Takes any base image (a photo the user supplied, or a plate from plates.py) and
runs a chain of era-accurate treatments over it: halftone screens, duotone ink
mapping, riso separations with misregistration, film grain, dust, sun-fade,
VHS chroma bleed, xerox contrast, warp, paper texture.

    # single chain
    python scripts/darkroom.py base.jpg -o out/cover.png \
        --ops "square,duotone=#101820/#e8dcc0,halftone=lpi:52;angle:15,grain=0.3,dust=0.2"

    # era preset (see --list-presets)
    python scripts/darkroom.py base.jpg -o out/bn.png --preset bluenote-1958

    # one base image -> every alternative in one pass (this is the workhorse)
    python scripts/darkroom.py base.jpg --alternatives bluenote-1958,psych-1968,riso-1990 \
        --out-dir out/ --size 3000

Ops syntax: comma-separated. `name`, `name=value`, or `name=key:val;key:val`.
Order matters and is honoured exactly. Everything is seeded (--seed) so a chain
is reproducible; change the seed to reroll the noise without touching the recipe.
"""
import argparse
import math
import pathlib
import sys

import numpy as np
from PIL import Image, ImageFilter

# ---------------------------------------------------------------- helpers

def _hex(c):
    c = c.strip().lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    return np.array([int(c[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float64)


def _f(img):
    """PIL RGB -> float array 0..1"""
    return np.asarray(img.convert("RGB"), dtype=np.float64) / 255.0


def _img(a):
    return Image.fromarray(np.clip(a * 255.0, 0, 255).astype(np.uint8), "RGB")


def _lum(a):
    return a[..., 0] * 0.2126 + a[..., 1] * 0.7152 + a[..., 2] * 0.0722


def _smoothstep(e0, e1, x):
    t = np.clip((x - e0) / max(e1 - e0, 1e-9), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def _rand(seed):
    return np.random.default_rng(seed)


def _screen(cov, lpi, angle, size, shape="circle", soft=1.0, sleeve_in=10.0):
    """Amplitude-modulated halftone dot screen.

    cov: ink coverage 0..1 array (h,w).
    lpi: lines per inch measured on a 10-inch sleeve, so it is resolution
    independent — the same recipe gives the same *look* at 900px preview and
    3000px delivery, only the anti-aliasing gets better. lpi 20 is a chunky
    pop-art screen, 45 is a newspaper, 70+ disappears at thumbnail size.
    """
    h, w = cov.shape
    period = max(size / (max(lpi, 1.0) * sleeve_in), 2.0)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)
    a = math.radians(angle)
    u = (xx * math.cos(a) + yy * math.sin(a)) / period
    v = (-xx * math.sin(a) + yy * math.cos(a)) / period
    su = (u % 1.0) - 0.5
    sv = (v % 1.0) - 0.5
    if shape == "square":
        d = np.maximum(np.abs(su), np.abs(sv)) / 0.5
    elif shape == "line":
        d = np.abs(sv) / 0.5
    elif shape == "diamond":
        d = (np.abs(su) + np.abs(sv)) / 0.5
    else:
        d = np.sqrt(su * su + sv * sv) / 0.7071
    r = np.sqrt(np.clip(cov, 0, 1))          # area-proportional dot radius
    aa = (1.6 / period) * max(soft, 0.15)
    return _smoothstep(-aa, aa, r - d)


def _paper_field(h, w, seed, scale=220.0, amount=1.0):
    """Low-frequency fibre/tone field for paper stock, 0..1 centred on 0.5."""
    rng = _rand(seed)
    sh, sw = max(int(h / 8), 8), max(int(w / 8), 8)
    n = rng.random((sh, sw))
    f = np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC),
                   dtype=np.float64) / 255.0
    f = np.asarray(Image.fromarray((f * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(max(w / scale, 1.0))), dtype=np.float64) / 255.0
    return 0.5 + (f - f.mean()) * amount


# ---------------------------------------------------------------- ops

def op_square(a, p, ctx):
    h, w = a.shape[:2]
    s = min(h, w)
    anchor = p.get("anchor", "center")
    if anchor == "top":
        y0 = 0
    elif anchor == "bottom":
        y0 = h - s
    else:
        y0 = (h - s) // 2
    x0 = (w - s) // 2
    return a[y0:y0 + s, x0:x0 + s]


def op_resize(a, p, ctx):
    n = int(p.get("_", p.get("size", ctx["size"])))
    return _f(_img(a).resize((n, n) if a.shape[0] == a.shape[1] else
                             (n, int(n * a.shape[0] / a.shape[1])), Image.LANCZOS))


def op_levels(a, p, ctx):
    lo = float(p.get("lo", 0)) / 255.0
    hi = float(p.get("hi", 255)) / 255.0
    g = float(p.get("gamma", 1.0))
    out = np.clip((a - lo) / max(hi - lo, 1e-6), 0, 1) ** (1.0 / g)
    return out


def op_auto(a, p, ctx):
    """Percentile black/white point stretch — the scanner step.

    Most base images (and every procedural plate) arrive with a squashed
    histogram, and every ink-mapping op below reads luminance. Without this,
    duotone and halftone recipes silently turn to mud on a dark source.
    """
    lo_p = float(p.get("lo", 0.5))
    hi_p = float(p.get("hi", 99.5))
    l = _lum(a)
    lo, hi = np.percentile(l, lo_p), np.percentile(l, hi_p)
    if hi - lo < 1e-3:
        return a
    return np.clip((a - lo) / (hi - lo), 0, 1)


def op_contrast(a, p, ctx):
    k = float(p.get("_", 1.2))
    return np.clip((a - 0.5) * k + 0.5, 0, 1)


def op_saturate(a, p, ctx):
    k = float(p.get("_", 1.0))
    l = _lum(a)[..., None]
    return np.clip(l + (a - l) * k, 0, 1)


def op_bw(a, p, ctx):
    return np.repeat(_lum(a)[..., None], 3, axis=2)


def op_posterize(a, p, ctx):
    n = max(int(p.get("_", 6)), 2)
    return np.round(a * (n - 1)) / (n - 1)


def op_solarize(a, p, ctx):
    t = float(p.get("_", 0.55))
    return np.where(a > t, 1.0 - a, a)


def op_duotone(a, p, ctx):
    spec = p.get("_", "#12121a/#efe6d0")
    dark, light = [x for x in spec.split("/")[:2]]
    d, l = _hex(dark) / 255.0, _hex(light) / 255.0
    g = float(p.get("gamma", 1.0))
    t = np.clip(_lum(a), 0, 1) ** (1.0 / g)
    return d + (l - d) * t[..., None]


def op_tritone(a, p, ctx):
    spec = p.get("_", "#0d0d12/#b8443a/#f2e6cc")
    cols = [_hex(c) / 255.0 for c in spec.split("/")[:3]]
    t = np.clip(_lum(a), 0, 1)
    lowmix = np.clip(t / 0.5, 0, 1)[..., None]
    himix = np.clip((t - 0.5) / 0.5, 0, 1)[..., None]
    low = cols[0] + (cols[1] - cols[0]) * lowmix
    high = cols[1] + (cols[2] - cols[1]) * himix
    return np.where(t[..., None] < 0.5, low, high)


def op_halftone(a, p, ctx):
    lpi = float(p.get("lpi", p.get("_", 34)))
    angle = float(p.get("angle", 15))
    shape = p.get("shape", "circle")
    soft = float(p.get("soft", 1.0))
    ink = _hex(p.get("ink", "#101014")) / 255.0
    paper = _hex(p.get("paper", "#f4ecd8")) / 255.0
    mono = str(p.get("mono", "1")) not in ("0", "false")
    if mono:
        cov = 1.0 - np.clip(_lum(a), 0, 1)
        dens = _screen(cov, lpi, angle, ctx["size"], shape, soft)
        return paper + (ink - paper) * dens[..., None]
    # per-channel screens at classic separation angles
    out = np.zeros_like(a)
    for i, ang in enumerate((angle + 15, angle + 75, angle)):
        cov = 1.0 - np.clip(a[..., i], 0, 1)
        dens = _screen(cov, lpi, ang, ctx["size"], shape, soft)
        out[..., i] = 1.0 - dens
    return out


def op_cmyk(a, p, ctx):
    """Four-colour process screen with real separation angles."""
    lpi = float(p.get("lpi", p.get("_", 38)))
    soft = float(p.get("soft", 1.0))
    shape = p.get("shape", "circle")
    gcr = float(p.get("gcr", 0.7))
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    k = (1.0 - np.max(a, axis=2)) * gcr
    den = np.clip(1.0 - k, 1e-6, None)
    c = np.clip((1.0 - r - k) / den, 0, 1)
    m = np.clip((1.0 - g - k) / den, 0, 1)
    y = np.clip((1.0 - b - k) / den, 0, 1)
    angles = {"c": 15.0, "m": 75.0, "y": 0.0, "k": 45.0}
    inks = {"c": np.array([0.0, 0.68, 0.94]), "m": np.array([0.93, 0.10, 0.55]),
            "y": np.array([1.0, 0.94, 0.0]), "k": np.array([0.07, 0.07, 0.09])}
    out = np.ones_like(a)
    for name, cov in (("y", y), ("c", c), ("m", m), ("k", k)):
        dens = _screen(cov, lpi, angles[name], ctx["size"], shape, soft)[..., None]
        out = out * (1.0 - dens * (1.0 - inks[name]))
    return np.clip(out, 0, 1)


def op_riso(a, p, ctx):
    """Risograph: quantise to N spot inks, screen each, misregister, multiply."""
    spec = p.get("colors", "#ff4a3d/#1b3fa0")
    offset = float(p.get("offset", 5))
    lpi = float(p.get("lpi", 26))
    paper = _hex(p.get("paper", "#f6efdd")) / 255.0
    inks = [_hex(c) / 255.0 for c in spec.split("/")]
    rng = _rand(ctx["seed"])
    t = np.clip(_lum(a), 0, 1)
    n = len(inks)
    out = np.ones_like(a) * paper
    for i, ink in enumerate(inks):
        lo, hi = i / n, (i + 1) / n
        cov = np.clip((hi - t) / max(hi - lo, 1e-6), 0, 1) if i == 0 else \
              np.clip(1.0 - np.abs(t - (lo + hi) / 2) / max((hi - lo), 1e-6), 0, 1)
        cov = np.clip(cov * float(p.get("ink", 0.95)), 0, 1)
        dens = _screen(cov, lpi, 15 + i * 30, ctx["size"], "circle", 1.2)
        dx, dy = (rng.normal(0, offset, 2)).round().astype(int)
        dens = np.roll(np.roll(dens, dy, axis=0), dx, axis=1)
        out = out * (1.0 - dens[..., None] * (1.0 - ink))
    return np.clip(out, 0, 1)


def op_misreg(a, p, ctx):
    off = float(p.get("_", p.get("offset", 6)))
    ang = math.radians(float(p.get("angle", 20)))
    dx, dy = int(round(off * math.cos(ang))), int(round(off * math.sin(ang)))
    out = a.copy()
    out[..., 0] = np.roll(np.roll(a[..., 0], dy, 0), dx, 1)
    out[..., 2] = np.roll(np.roll(a[..., 2], -dy, 0), -dx, 1)
    return out


def op_grain(a, p, ctx):
    amt = float(p.get("_", 0.28))
    size = float(p.get("size", 1.0))
    rng = _rand(ctx["seed"] + 11)
    h, w = a.shape[:2]
    if size > 1.0:
        sh, sw = max(int(h / size), 2), max(int(w / size), 2)
        n = rng.normal(0, 1, (sh, sw))
        n = np.asarray(Image.fromarray(((n * 40) + 128).clip(0, 255).astype(np.uint8))
                       .resize((w, h), Image.BILINEAR), dtype=np.float64)
        n = (n - 128) / 40.0
    else:
        n = rng.normal(0, 1, (h, w))
    # grain bites hardest in the midtones, like real emulsion
    weight = 1.0 - np.abs(_lum(a) - 0.5) * 1.4
    g = (n * amt * 0.22 * np.clip(weight, 0.15, 1.0))[..., None]
    return np.clip(a + g, 0, 1)


def op_dust(a, p, ctx):
    amt = float(p.get("_", 0.3))
    rng = _rand(ctx["seed"] + 23)
    h, w = a.shape[:2]
    out = a.copy()
    # specks
    n_specks = int(amt * (h * w) / 11000)
    ys = rng.integers(0, h, n_specks)
    xs = rng.integers(0, w, n_specks)
    unit = max(h / 1200, 1.0)
    rr = np.maximum((rng.gamma(1.6, 0.9, n_specks) * unit).astype(int), 1)
    bright = rng.random(n_specks) > 0.4
    alphas = rng.uniform(0.35, 1.0, n_specks)
    for y, x, r, b, al in zip(ys, xs, rr, bright, alphas):
        ry = max(int(r * rng.uniform(0.6, 1.5)), 1)
        y0, y1 = max(y - ry, 0), min(y + ry + 1, h)
        x0, x1 = max(x - r, 0), min(x + r + 1, w)
        v = 0.97 if b else 0.05
        out[y0:y1, x0:x1] = out[y0:y1, x0:x1] * (1 - al) + v * al
    # hairs / emulsion scratches — few, thin, mostly vertical
    for _ in range(int(amt * 3) + 1):
        x = float(rng.integers(0, w))
        thick = max(int(unit * rng.uniform(0.6, 1.4)), 1)
        length = int(rng.uniform(0.2, 0.95) * h)
        y0 = rng.integers(0, max(h - length, 1))
        lean = rng.normal(0, 0.25)
        drift = (rng.normal(0, 0.35, length) + lean).cumsum()
        v = 0.95 if rng.random() > 0.45 else 0.06
        al = rng.uniform(0.3, 0.75)
        for i in range(length):
            xx = int(np.clip(x + drift[i], 0, w - thick))
            yy = min(y0 + i, h - 1)
            out[yy, xx:xx + thick] = out[yy, xx:xx + thick] * (1 - al) + v * al
    return np.clip(out, 0, 1)


def op_fade(a, p, ctx):
    """Sun-bleached: lifted blacks, compressed whites, warm/yellow drift."""
    amt = float(p.get("_", 0.35))
    lift = 0.10 * amt
    out = a * (1.0 - lift * 0.6) + lift
    warm = np.array([1.0 + 0.055 * amt, 1.0 + 0.012 * amt, 1.0 - 0.075 * amt])
    out = out * warm
    l = _lum(out)[..., None]
    out = l + (out - l) * (1.0 - 0.22 * amt)
    return np.clip(out, 0, 1)


def op_bloom(a, p, ctx):
    amt = float(p.get("_", 0.35))
    r = float(p.get("radius", max(a.shape[0] / 120, 3)))
    hi = np.clip((_lum(a) - 0.62) / 0.38, 0, 1)[..., None] * a
    blur = _f(_img(hi).filter(ImageFilter.GaussianBlur(r)))
    return np.clip(a + blur * amt * 1.5, 0, 1)


def op_blur(a, p, ctx):
    return _f(_img(a).filter(ImageFilter.GaussianBlur(float(p.get("_", 2)))))


def op_sharpen(a, p, ctx):
    amt = float(p.get("_", 0.6))
    blur = _f(_img(a).filter(ImageFilter.GaussianBlur(max(a.shape[0] / 900, 1.0))))
    return np.clip(a + (a - blur) * amt * 2.0, 0, 1)


def op_xerox(a, p, ctx):
    """Photocopied zine look: crushed 1-bit-ish contrast with edge chatter."""
    amt = float(p.get("_", 0.6))
    rng = _rand(ctx["seed"] + 37)
    l = _lum(_f(_img(a).filter(ImageFilter.GaussianBlur(max(a.shape[0] / 1400, 0.6)))))
    mid = float(p["threshold"]) if "threshold" in p else float(np.median(l))
    thr = mid + rng.normal(0, 0.045 * (0.3 + amt), l.shape)
    ink = _hex(p.get("ink", "#141414")) / 255.0
    paper = _hex(p.get("paper", "#f1eee6")) / 255.0
    m = _smoothstep(-0.02, 0.02, thr - l)[..., None]
    return paper + (ink - paper) * m


def op_vhs(a, p, ctx):
    amt = float(p.get("_", 0.5))
    rng = _rand(ctx["seed"] + 41)
    h, w = a.shape[:2]
    out = a.copy()
    # horizontal chroma smear
    sm = _f(_img(a).filter(ImageFilter.GaussianBlur(max(w / 300 * amt, 0.6))))
    l = _lum(a)[..., None]
    out = l + (sm - _lum(sm)[..., None]) * (1.0 + amt)
    # chroma offset
    sh = int(max(w / 400 * amt, 1))
    out[..., 0] = np.roll(out[..., 0], sh, 1)
    out[..., 2] = np.roll(out[..., 2], -sh, 1)
    # tracking bands
    for _ in range(int(3 + amt * 5)):
        y = rng.integers(0, h)
        th = rng.integers(int(h / 400) + 1, int(h / 90) + 2)
        shift = int(rng.normal(0, w / 90 * (0.4 + amt)))
        out[y:y + th] = np.roll(out[y:y + th], shift, 1)
        out[y:y + th] = np.clip(out[y:y + th] * (1.0 + 0.25 * amt), 0, 1)
    # scanlines
    period = max(int(p.get("scanline", max(h // 480, 2))), 2)
    line = np.ones((h, 1, 1))
    line[::period] = 1.0 - 0.16 * amt
    out = out * line
    return np.clip(out, 0, 1)


def op_warp(a, p, ctx):
    """Sine displacement — liquid psychedelic / heat-warp."""
    amp = float(p.get("amp", p.get("_", 10)))
    freq = float(p.get("freq", 3))
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)
    ax = amp * h / 1000.0
    sx = xx + np.sin(yy / h * math.tau * freq) * ax
    sy = yy + np.cos(xx / w * math.tau * freq * 0.8) * ax
    try:
        from scipy.ndimage import map_coordinates
        out = np.stack([map_coordinates(a[..., i], [sy, sx], order=1, mode="reflect")
                        for i in range(3)], axis=2)
    except Exception:
        xi = np.clip(sx.round().astype(int), 0, w - 1)
        yi = np.clip(sy.round().astype(int), 0, h - 1)
        out = a[yi, xi]
    return np.clip(out, 0, 1)


def op_vignette(a, p, ctx):
    amt = float(p.get("_", 0.35))
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    m = 1.0 - amt * np.clip((r - 0.55) / 0.85, 0, 1) ** 1.6
    return np.clip(a * m[..., None], 0, 1)


def op_paper(a, p, ctx):
    """Multiply the art onto a paper stock: tone, fibre, and edge soiling."""
    tone = _hex(p.get("tone", "#f4ecd6")) / 255.0
    amt = float(p.get("_", p.get("amount", 0.6)))
    tex = float(p.get("texture", 0.35))
    h, w = a.shape[:2]
    field = _paper_field(h, w, ctx["seed"] + 7, amount=tex)[..., None]
    stock = tone * (0.9 + field * 0.2)
    out = a * (1.0 - amt) + (a * stock) * amt
    return np.clip(out, 0, 1)


def op_ringwear(a, p, ctx):
    """Sleeve ring wear + corner scuff, for mockups and 'found record' looks."""
    amt = float(p.get("_", 0.35))
    h, w = a.shape[:2]
    rng = _rand(ctx["seed"] + 53)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)
    cx, cy = w * (0.5 + rng.normal(0, 0.02)), h * (0.5 + rng.normal(0, 0.02))
    r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / (min(h, w) * 0.5)
    ring = np.exp(-((r - 0.82) ** 2) / (2 * 0.012 ** 2)) * 0.55
    ring += np.exp(-((r - 0.30) ** 2) / (2 * 0.010 ** 2)) * 0.25
    edge = np.clip((np.maximum(np.abs(xx - cx) / (w / 2), np.abs(yy - cy) / (h / 2)) - 0.93) / 0.07, 0, 1) ** 1.5
    mask = np.clip((ring + edge * 0.8) * amt, 0, 1)[..., None]
    return np.clip(a * (1 - mask) + (a * 0.55 + 0.45) * mask, 0, 1)


def op_border(a, p, ctx):
    wpx = int(float(p.get("w", p.get("_", 60))))
    col = _hex(p.get("color", "#f2e8d0")) / 255.0
    h, w = a.shape[:2]
    inner = _f(_img(a).resize((max(w - 2 * wpx, 8), max(h - 2 * wpx, 8)), Image.LANCZOS))
    out = np.ones_like(a) * col
    out[wpx:wpx + inner.shape[0], wpx:wpx + inner.shape[1]] = inner
    return out


OPS = {
    "square": op_square, "resize": op_resize, "levels": op_levels, "auto": op_auto,
    "contrast": op_contrast, "saturate": op_saturate, "bw": op_bw,
    "posterize": op_posterize, "solarize": op_solarize, "duotone": op_duotone,
    "tritone": op_tritone, "halftone": op_halftone, "cmyk": op_cmyk,
    "riso": op_riso, "misreg": op_misreg, "grain": op_grain, "dust": op_dust,
    "fade": op_fade, "bloom": op_bloom, "blur": op_blur, "sharpen": op_sharpen,
    "xerox": op_xerox, "vhs": op_vhs, "warp": op_warp, "vignette": op_vignette,
    "paper": op_paper, "ringwear": op_ringwear, "border": op_border,
}

# ---------------------------------------------------------------- presets
# Each preset is a chain. They are starting points, not gospel — read
# references/era-playbook.md and tune per brief.
PRESETS = {
    "bluenote-1958": "square,auto,bw,contrast=1.25,duotone=#0b1a2e/#e9dcbf,halftone=lpi:34;angle:15;ink:#0b1a2e;paper:#e9dcbf,grain=0.22,dust=0.15,paper=0.45",
    "verve-1962": "square,auto,duotone=#231f20/#f0e3c8,contrast=1.15,halftone=lpi:42;angle:45,grain=0.2,paper=amount:0.5;tone:#f0e3c8",
    "psych-1968": "square,auto,saturate=1.5,posterize=6,warp=amp:16;freq:3,tritone=#2b0a4a/#e0344f/#f7d84a,bloom=0.4,grain=0.3,dust=0.25",
    "hipgnosis-1973": "square,auto,fade=0.4,contrast=1.08,saturate=0.85,bloom=0.25,grain=0.35,dust=0.3,vignette=0.3",
    "soul-1975": "square,auto,saturate=1.2,fade=0.3,tritone=#3a1408/#c8622a/#f2d9a0,bloom=0.3,grain=0.32,paper=0.35",
    "punk-xerox-1977": "square,auto,contrast=1.2,xerox=0.75,halftone=lpi:22;angle:45;ink:#141414;paper:#f1eee6,dust=0.5,grain=0.25",
    "postpunk-1981": "square,auto,bw,contrast=1.4,levels=lo:20;hi:238,halftone=lpi:20;angle:0;shape:line,grain=0.3,dust=0.2",
    "neon-1984": "square,auto,saturate=1.35,contrast=1.12,bloom=0.55,misreg=offset:5;angle:0,grain=0.22,vignette=0.35",
    "vhs-1987": "square,auto,saturate=1.2,vhs=0.85,bloom=0.3,grain=0.3,vignette=0.3",
    "riso-1990": "square,auto,riso=colors:#ff4a3d/#1b3fa0;offset:7;lpi:26,grain=0.2,paper=amount:0.6;tone:#f6efdd",
    "grunge-1993": "square,auto,bw,contrast=1.3,xerox=0.5,dust=0.55,grain=0.4,paper=0.4,ringwear=0.3",
    "vaporwave-1995": "square,auto,saturate=1.3,posterize=8,misreg=offset:7;angle:0,bloom=0.4,vhs=0.35,grain=0.18",
    "print-cmyk": "square,auto,cmyk=lpi:38,misreg=offset:4;angle:25,grain=0.18,paper=0.35",
}


# ---------------------------------------------------------------- chain

def parse_ops(spec):
    out = []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "=" in chunk:
            name, arg = chunk.split("=", 1)
            name, arg = name.strip(), arg.strip()
            params = {}
            if ":" in arg:
                for kv in arg.split(";"):
                    if not kv.strip():
                        continue
                    k, _, v = kv.partition(":")
                    params[k.strip()] = v.strip()
            else:
                params["_"] = arg
        else:
            name, params = chunk, {}
        if name not in OPS:
            sys.exit(f"unknown op '{name}'. known: {', '.join(sorted(OPS))}")
        out.append((name, params))
    return out


def run_chain(img, spec, size, seed, verbose=False):
    a = _f(img)
    ctx = {"size": size, "seed": seed}
    for name, params in parse_ops(spec):
        if verbose:
            print(f"    · {name} {params or ''}")
        a = OPS[name](a, params, ctx)
        ctx["size"] = a.shape[0]
    return _img(a)


def prepare(path, size, anchor="center"):
    img = Image.open(path).convert("RGB")
    w, h = img.size
    s = min(w, h)
    if anchor == "top":
        box = ((w - s) // 2, 0, (w - s) // 2 + s, s)
    elif anchor == "bottom":
        box = ((w - s) // 2, h - s, (w - s) // 2 + s, h)
    else:
        box = ((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s)
    return img.crop(box).resize((size, size), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image", nargs="?", help="base image (photo or plate)")
    ap.add_argument("-o", "--out", help="output file")
    ap.add_argument("--out-dir", default="out", help="output dir for --alternatives")
    ap.add_argument("--ops", help="treatment chain")
    ap.add_argument("--preset", help="named era preset")
    ap.add_argument("--alternatives", help="comma-separated presets -> one file each")
    ap.add_argument("--size", type=int, default=3000, help="square working size (default 3000)")
    ap.add_argument("--anchor", default="center", choices=["center", "top", "bottom"])
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--jpeg", type=int, default=None, help="also write JPEG at this quality")
    ap.add_argument("--list-presets", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    if args.list_presets:
        for k, v in PRESETS.items():
            print(f"{k:18} {v}")
        return
    if not args.image:
        sys.exit("need an input image (or --list-presets)")

    src = pathlib.Path(args.image)
    if not src.exists():
        sys.exit(f"not found: {src}")

    def save(im, path):
        path = pathlib.Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        im.save(path)
        if args.jpeg:
            jp = path.with_suffix(".jpg")
            im.save(jp, quality=args.jpeg, subsampling=0, optimize=True)
            print(f"  {jp}  ({jp.stat().st_size/1e6:.2f} MB)")
        print(f"  {path}  {im.size[0]}×{im.size[1]}  ({path.stat().st_size/1e6:.2f} MB)")

    base = prepare(src, args.size, args.anchor)

    if args.alternatives:
        names = [n.strip() for n in args.alternatives.split(",") if n.strip()]
        for i, name in enumerate(names):
            spec = PRESETS.get(name, name)
            print(f"[{i+1}/{len(names)}] {name}")
            im = run_chain(base, spec, args.size, args.seed + i * 100, args.verbose)
            save(im, pathlib.Path(args.out_dir) / f"{i+1:02d}-{name.split('=')[0][:24]}.png")
        return

    spec = args.ops or PRESETS.get(args.preset or "", None)
    if not spec:
        sys.exit("give --ops or a valid --preset (see --list-presets)")
    im = run_chain(base, spec, args.size, args.seed, args.verbose)
    save(im, args.out or "out/cover.png")


if __name__ == "__main__":
    main()

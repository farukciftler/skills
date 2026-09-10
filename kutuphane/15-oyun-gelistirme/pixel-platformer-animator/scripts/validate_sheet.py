#!/usr/bin/env python3
"""
validate_sheet.py - pre-import QA for a pixel-art sprite sheet + manifest.

Catches the problems that otherwise show up only in Play mode: floating/sinking
feet, pivot jitter, edge bleed, anti-aliased (semi-transparent) pixels, loop
stutter from duplicated seam frames, orphan pixels, too-short frame durations,
event indices out of range.

Usage:
  python validate_sheet.py build/hero.manifest.json [--grounded idle,run,land] [--json]

Exit code 0 = no errors (warnings allowed), 1 = errors found.
"""
import argparse
import json
import os
import sys

import numpy as np
from PIL import Image

DEFAULT_GROUNDED = ["idle", "run", "land", "crouch", "attack", "hurt", "death"]
LOOPING_DRIFT_PX = 2      # max foot-center jump between consecutive grounded frames
MIN_DURATION_MS = 33      # 2 frames at 60 Hz; shorter frames get skipped on some refresh rates
MAX_COLORS = 48


def frame_pixels(img, fr, tex_h):
    # manifest rects use Unity's bottom-left origin -> convert to top-left
    top = tex_h - (fr["y"] + fr["h"])
    return img[top:top + fr["h"], fr["x"]:fr["x"] + fr["w"]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("--grounded", default=",".join(DEFAULT_GROUNDED))
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    with open(a.manifest) as f:
        m = json.load(f)
    tex_path = os.path.join(os.path.dirname(os.path.abspath(a.manifest)), m["texture"])
    errors, warns, info = [], [], []

    if not os.path.exists(tex_path):
        print(f"ERROR texture not found: {tex_path}")
        return 1
    img = np.array(Image.open(tex_path).convert("RGBA"))
    th, tw = img.shape[:2]
    if (tw, th) != (m.get("textureWidth", tw), m.get("textureHeight", th)):
        errors.append(f"texture is {tw}x{th} but manifest says {m['textureWidth']}x{m['textureHeight']}")

    alpha = img[..., 3]
    semi = int(((alpha > 0) & (alpha < 255)).sum())
    if semi:
        errors.append(f"{semi} semi-transparent pixels - pixel art needs binary alpha "
                      "(export without anti-aliasing / resampling)")
    opaque = img[alpha == 255][:, :3]
    ncol = len({tuple(c) for c in opaque})
    info.append(f"{ncol} unique colors")
    if ncol > MAX_COLORS:
        warns.append(f"{ncol} colors > {MAX_COLORS}: palette likely drifted (scaled/filtered source?)")

    grounded = set(x for x in a.grounded.split(",") if x)
    sprites = {}
    rects = []
    for sp in m.get("sprites", []):
        if sp["name"] in sprites:
            errors.append(f"duplicate sprite name {sp['name']}")
        sprites[sp["name"]] = sp
        if sp["x"] < 0 or sp["y"] < 0 or sp["x"] + sp["w"] > tw or sp["y"] + sp["h"] > th:
            errors.append(f"{sp['name']}: rect outside texture")
        else:
            rects.append((sp["x"], sp["y"], sp["w"], sp["h"], sp["name"]))
    used = set()
    ref_center, ref_piv = None, None

    for anim in m["animations"]:
        n = anim["name"]
        frames = anim["frames"]
        if not frames:
            errors.append(f"{n}: no frames")
            continue
        for ev in anim.get("events", []):
            if not 0 <= ev["frame"] < len(frames):
                errors.append(f"{n}: event {ev['function']} on frame {ev['frame']} out of range")
        prev = None
        centers = []
        bufs = []
        for i, fr in enumerate(frames):
            tag = f"{n}[{i}]"
            sp = sprites.get(fr["sprite"])
            if sp is None:
                errors.append(f"{tag}: references unknown sprite {fr['sprite']}")
                continue
            used.add(sp["name"])
            if fr.get("durationMs", 100) < MIN_DURATION_MS:
                warns.append(f"{tag}: {fr['durationMs']}ms < {MIN_DURATION_MS}ms may be skipped at 60 Hz")
            px = frame_pixels(img, sp, th)
            piv = {"x": sp.get("pivotX", 0.5), "y": sp.get("pivotY", 0.0)}
            bufs.append(px)
            a_ = px[..., 3] == 255
            if not a_.any():
                errors.append(f"{tag}: empty frame")
                continue
            ys, xs = np.nonzero(a_)
            fh, fw = a_.shape
            if xs.min() == 0 or xs.max() == fw - 1 or ys.min() == 0:
                warns.append(f"{tag}: art touches the frame edge - texture bleed risk, keep 1px margin")
            # ground contact (untrimmed frames only - trimmed rects move the pivot per sprite)
            if n in grounded and (sp["w"], sp["h"]) == (m["frameWidth"], m["frameHeight"]):
                expected = fh - 1 - int(round(piv["y"] * fh))
                if ys.max() != expected:
                    d = expected - ys.max()
                    kind = "floating" if d > 0 else "sinking"
                    errors.append(f"{tag}: feet {kind} by {abs(d)}px (lowest row {ys.max()}, pivot row {expected})")
                foot = xs[ys >= ys.max() - 2]
                centers.append(float(foot.mean()))
            # orphan pixels (no 8-neighbour)
            pad = np.pad(a_, 1)
            neigh = sum(np.roll(np.roll(pad, dy, 0), dx, 1)
                        for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dy, dx) != (0, 0))[1:-1, 1:-1]
            orph = int((a_ & (neigh == 0)).sum())
            if orph:
                warns.append(f"{tag}: {orph} orphan pixel(s)")
            if prev is not None and np.array_equal(prev, px):
                warns.append(f"{tag}: identical to previous frame - merge into one longer duration")
            prev = px
        if anim.get("loop") and len(bufs) > 1 and np.array_equal(bufs[0], bufs[-1]):
            warns.append(f"{n}: last frame equals first - loop will stutter (drop the seam frame)")
        if len(centers) > 1:
            jumps = [abs(centers[i] - centers[i - 1]) for i in range(1, len(centers))]
            if not anim.get("loop") is False and max(jumps) > LOOPING_DRIFT_PX + 3:
                warns.append(f"{n}: foot center jumps {max(jumps):.1f}px between frames - check for sliding")
        if n == "idle" and centers:
            ref_center, ref_piv = centers[0], sprites[frames[0]["sprite"]].get("pivotX", 0.5)
    for nm in sprites:
        if nm not in used:
            warns.append(f"sprite {nm} is not used by any animation")

    # overlapping rects
    for i in range(len(rects)):
        x, y, w, h, t = rects[i]
        for j in range(i + 1, len(rects)):
            x2, y2, w2, h2, t2 = rects[j]
            if x < x2 + w2 and x2 < x + w and y < y2 + h2 and y2 < y + h:
                errors.append(f"rects overlap: {t} / {t2}")

    # pivot centering (flipX symmetry)
    if ref_center is not None:
        fw = m["frameWidth"]
        off = ref_center - (ref_piv * fw - 0.5)
        info.append(f"idle foot center offset from pivot: {off:+.1f}px")
        if abs(off) > 2.5:
            warns.append(f"idle feet are {off:+.1f}px from pivot.x - flipX will make the character jump sideways")

    ppu = m.get("ppu")
    if ppu and m["frameHeight"] % 2:
        warns.append("odd frame height - keep frames even-sized so the pivot sits on a pixel edge")
    info.append(f"{len(m['animations'])} animations, {len(sprites)} sprites, PPU {ppu}")

    if a.json:
        print(json.dumps({"errors": errors, "warnings": warns, "info": info}, indent=2))
    else:
        for s in info:
            print("INFO ", s)
        for s in warns:
            print("WARN ", s)
        for s in errors:
            print("ERROR", s)
        print(f"-> {len(errors)} error(s), {len(warns)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""pixel_qa.py — numeric gate for a uca-sheet/1 sprite sheet. Run it on EVERY sheet,
whatever produced it (generator, AI cleanup, 3D->pixel render, hand-drawn).

    python pixel_qa.py build/Ranger/Ranger_sheet.json [--max-colors 24] [--json]

Exit code 0 = no errors (warnings allowed), 1 = errors. Data first, eyes second:
this catches what previews hide (half-transparent pixels, 1px foot drift, clipping).
Checks
  E alpha        every pixel is fully transparent or fully opaque
  E clip         opaque pixels touch the cell edge (sprite will be cut / bleed)
  E feet         grounded anim: lowest opaque row must sit ON the baseline row
  E empty        a frame has no pixels
  W colors       palette larger than --max-colors (not pixel-art-disciplined)
  W orphans      isolated single pixels (noise, typical of AI output)
  W dupe         two consecutive frames identical (wasted frame / hitch)
  W loopseam     loop anim whose last frame == first frame (double frame at the seam)
  W volume       idle silhouette area swings > 12% (character "breathes" too much)
  W pivot        pivot not on an integer pixel
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sheetio import frames_of, read_sheet, unique_colors  # noqa: E402


def analyse(json_path: str, max_colors: int = 24) -> dict:
    meta, sheet = read_sheet(json_path)
    fw, fh, base = meta["frameWidth"], meta["frameHeight"], meta["baseline"]
    base_row = fh - 1 - base
    errors, warns = [], []
    all_colors = set()
    stats = {}
    for a in meta["animations"]:
        frames = frames_of(meta, sheet, a)
        areas = []
        prev = None
        for i, fr in enumerate(frames):
            tag = f"{a['name']}[{i}]"
            px = fr.load()
            opaque = []
            semi = 0
            for y in range(fh):
                for x in range(fw):
                    al = px[x, y][3]
                    if al == 255:
                        opaque.append((x, y))
                    elif al != 0:
                        semi += 1
            if semi:
                errors.append(f"alpha: {tag} has {semi} semi-transparent px (threshold alpha to 0/255)")
            if not opaque:
                errors.append(f"empty: {tag} has no pixels")
                continue
            xs = [p[0] for p in opaque]
            ys = [p[1] for p in opaque]
            if min(xs) == 0 or max(xs) == fw - 1 or min(ys) == 0:
                errors.append(f"clip: {tag} touches cell edge (bbox x{min(xs)}-{max(xs)} y{min(ys)}-{max(ys)}); "
                              f"enlarge frame or move pose")
            low = max(ys)
            if a.get("grounded", True):
                if low != base_row:
                    errors.append(f"feet: {tag} lowest row {low} != baseline row {base_row} "
                                  f"({'floating' if low < base_row else 'sinking'} {abs(low - base_row)}px)")
            elif low > base_row:
                errors.append(f"feet: airborne {tag} sinks below baseline")
            opset = set(opaque)
            orph = sum(1 for (x, y) in opaque
                       if not any((x + dx, y + dy) in opset for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                                  if dx or dy))
            if orph:
                warns.append(f"orphans: {tag} has {orph} isolated pixel(s)")
            areas.append(len(opaque))
            all_colors |= unique_colors(fr)
            data = fr.tobytes()
            if prev is not None and data == prev:
                warns.append(f"dupe: {tag} identical to previous frame")
            prev = data
        if a.get("loop") and len(frames) > 1 and frames[0].tobytes() == frames[-1].tobytes():
            warns.append(f"loopseam: {a['name']} last frame equals first (double frame at loop seam)")
        if a["name"].startswith("idle") and areas:
            mn, mx = min(areas), max(areas)
            if mn and (mx - mn) / mn > 0.12:
                warns.append(f"volume: idle area varies {mn}->{mx} px (>12%)")
        stats[a["name"]] = {"frames": len(frames), "ms": sum(f["durationMs"] for f in a["frames"]),
                            "loop": a.get("loop"), "grounded": a.get("grounded")}
    if len(all_colors) > max_colors:
        warns.append(f"colors: {len(all_colors)} unique colours > {max_colors}")
    pvx = meta["pivot"]["x"] * fw
    pvy = meta["pivot"]["y"] * fh
    if abs(pvx - round(pvx)) > 1e-3 or abs(pvy - round(pvy)) > 1e-3:
        warns.append(f"pivot: ({pvx:.2f},{pvy:.2f}) px is not integer — sub-pixel jitter risk")
    return {"sheet": json_path, "frame": [fw, fh], "baselineRow": base_row, "colors": len(all_colors),
            "animations": stats, "errors": errors, "warnings": warns, "ok": not errors}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sheet_json")
    ap.add_argument("--max-colors", type=int, default=24)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    r = analyse(a.sheet_json, a.max_colors)
    if a.json:
        print(json.dumps(r, indent=2))
    else:
        print(f"{'PASS' if r['ok'] else 'FAIL'}  {r['sheet']}  frame={r['frame']}  colours={r['colors']}")
        for k, v in r["animations"].items():
            print(f"  {k:<12} {v['frames']:>2}f {v['ms']:>5}ms loop={v['loop']} grounded={v['grounded']}")
        for e in r["errors"]:
            print("  ERROR", e)
        for w in r["warnings"]:
            print("  warn ", w)
    sys.exit(0 if r["ok"] else 1)


if __name__ == "__main__":
    main()

"""sheetio — the ONE sprite-sheet contract every 2D path in this skill writes.

Every 2D source (procedural generator, AI-output cleanup, Blender 3D->pixel render,
hand-drawn frames) ends in the same two files, so a single Unity importer and a
single QA script serve all of them:

  <name>_sheet.png   RGBA, 1x scale, one ROW per animation, uniform cell size
  <name>_sheet.json  contract below (schema "uca-sheet/1")

JSON contract (all pixel coords TOP-LEFT origin, like the PNG):
{
  "schema": "uca-sheet/1",
  "name": "Ranger",
  "image": "Ranger_sheet.png",
  "frameWidth": 48, "frameHeight": 40,
  "baseline": 2,                 # feet row, counted in px from the cell BOTTOM
  "pivot": {"x": 0.5, "y": 0.05},# normalized, Unity convention (0,0)=bottom-left
  "ppu": 16,                     # pixels-per-unit hint for Unity import
  "animations": [
    {"name": "idle", "loop": true, "grounded": true,
     "frames": [{"x":0,"y":0,"w":48,"h":40,"durationMs":220}, ...],
     "events": [{"frame": 2, "function": "OnAttackHit"}]}
  ]
}
Only Pillow is required.
"""
from __future__ import annotations

import json
import os
from typing import Iterable

from PIL import Image

SCHEMA = "uca-sheet/1"


def write_sheet(out_dir: str, name: str, anims: list[dict], frame_w: int, frame_h: int,
                baseline: int, ppu: int = 16, pivot_x: float = 0.5,
                extra: dict | None = None) -> tuple[str, str]:
    """anims: [{"name", "loop", "grounded", "frames": [PIL.Image RGBA], "durations": [ms],
                "events": [{"frame", "function"}]}]
    Returns (png_path, json_path)."""
    os.makedirs(out_dir, exist_ok=True)
    cols = max(len(a["frames"]) for a in anims)
    sheet = Image.new("RGBA", (cols * frame_w, len(anims) * frame_h), (0, 0, 0, 0))
    meta_anims = []
    for row, a in enumerate(anims):
        if len(a["frames"]) != len(a["durations"]):
            raise ValueError(f"{a['name']}: frames/durations length mismatch")
        frames_meta = []
        for col, img in enumerate(a["frames"]):
            if img.size != (frame_w, frame_h):
                raise ValueError(f"{a['name']}[{col}] is {img.size}, expected {(frame_w, frame_h)}")
            x, y = col * frame_w, row * frame_h
            sheet.paste(img, (x, y))
            frames_meta.append({"x": x, "y": y, "w": frame_w, "h": frame_h,
                                "durationMs": int(a["durations"][col])})
        meta_anims.append({"name": a["name"], "loop": bool(a.get("loop", True)),
                           "grounded": bool(a.get("grounded", True)),
                           "frames": frames_meta, "events": a.get("events", [])})
    png_name = f"{name}_sheet.png"
    png_path = os.path.join(out_dir, png_name)
    sheet.save(png_path)
    meta = {"schema": SCHEMA, "name": name, "image": png_name,
            "frameWidth": frame_w, "frameHeight": frame_h, "baseline": baseline,
            "pivot": {"x": pivot_x, "y": baseline / frame_h},
            "ppu": ppu, "animations": meta_anims}
    if extra:
        meta.update(extra)
    json_path = os.path.join(out_dir, f"{name}_sheet.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    return png_path, json_path


def read_sheet(json_path: str) -> tuple[dict, Image.Image]:
    with open(json_path, encoding="utf-8") as f:
        meta = json.load(f)
    if meta.get("schema") != SCHEMA:
        raise ValueError(f"not a {SCHEMA} file: {json_path}")
    img = Image.open(os.path.join(os.path.dirname(json_path), meta["image"])).convert("RGBA")
    return meta, img


def frames_of(meta: dict, sheet: Image.Image, anim: dict) -> list[Image.Image]:
    return [sheet.crop((f["x"], f["y"], f["x"] + f["w"], f["y"] + f["h"])) for f in anim["frames"]]


def write_previews(json_path: str, scale: int = 6, bg=(40, 44, 52, 255)) -> list[str]:
    """Scaled GIF per animation + one contact sheet PNG, into <dir>/preview/.
    Always LOOK at these before declaring an animation done."""
    meta, sheet = read_sheet(json_path)
    out = os.path.join(os.path.dirname(json_path), "preview")
    os.makedirs(out, exist_ok=True)
    paths = []
    fw, fh = meta["frameWidth"], meta["frameHeight"]
    base_row = fh - 1 - meta["baseline"]
    for a in meta["animations"]:
        imgs = []
        for fr in frames_of(meta, sheet, a):
            canvas = Image.new("RGBA", (fw, fh), bg)
            # faint ground line so foot-planting errors are visible
            for x in range(fw):
                canvas.putpixel((x, base_row + 1) if base_row + 1 < fh else (x, base_row), (70, 76, 88, 255))
            canvas.alpha_composite(fr)
            imgs.append(canvas.resize((fw * scale, fh * scale), Image.NEAREST).convert("P", palette=Image.ADAPTIVE))
        p = os.path.join(out, f"{a['name']}.gif")
        imgs[0].save(p, save_all=True, append_images=imgs[1:],
                     duration=[f["durationMs"] for f in a["frames"]],
                     loop=0 if a["loop"] else 1, disposal=2)
        paths.append(p)
    # contact sheet: every frame, labelled rows
    cols = max(len(a["frames"]) for a in meta["animations"])
    label_w = 70
    s = max(2, scale // 2)
    cs = Image.new("RGBA", (label_w + cols * fw * s, len(meta["animations"]) * fh * s), bg)
    try:
        from PIL import ImageDraw
        d = ImageDraw.Draw(cs)
    except Exception:  # pragma: no cover
        d = None
    for r, a in enumerate(meta["animations"]):
        for c, fr in enumerate(frames_of(meta, sheet, a)):
            cell = Image.new("RGBA", (fw, fh), (52, 58, 68, 255) if (r + c) % 2 else bg)
            cell.alpha_composite(fr)
            cs.paste(cell.resize((fw * s, fh * s), Image.NEAREST), (label_w + c * fw * s, r * fh * s))
        if d:
            d.text((4, r * fh * s + 4), a["name"], fill=(230, 230, 230, 255))
    p = os.path.join(out, "contact_sheet.png")
    cs.save(p)
    paths.append(p)
    return paths


def hex_rgba(h: str) -> tuple[int, int, int, int]:
    h = h.lstrip("#")
    if len(h) == 6:
        h += "ff"
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4, 6))  # type: ignore[return-value]


def pixels(img: Image.Image) -> list[tuple]:
    """RGBA tuples without Image.getdata (deprecated in Pillow 12, removed in 14)."""
    b = img.convert("RGBA").tobytes()
    return [tuple(b[i:i + 4]) for i in range(0, len(b), 4)]


def unique_colors(img: Image.Image) -> set:
    return {c for c in pixels(img) if c[3] > 0}


def merge_duplicates(frames: list, durs: list, events: list, loop: bool):
    """Never ship duplicate frames: merge consecutive identical frames (durations summed) and, for loops,
    a last frame identical to the first. Event frame indices are remapped."""
    keep_f, keep_d, remap = [], [], {}
    for i, (f, d) in enumerate(zip(frames, durs)):
        if keep_f and f.tobytes() == keep_f[-1].tobytes():
            keep_d[-1] += d
        else:
            keep_f.append(f)
            keep_d.append(d)
        remap[i] = len(keep_f) - 1
    if loop and len(keep_f) > 1 and keep_f[-1].tobytes() == keep_f[0].tobytes():
        keep_d[0] += keep_d.pop()
        keep_f.pop()
        remap = {k: (0 if v == len(keep_f) else v) for k, v in remap.items()}
    return keep_f, keep_d, [{**e, "frame": remap[e["frame"]]} for e in events]


def iter_opaque(img: Image.Image) -> Iterable[tuple[int, int]]:
    w, h = img.size
    px = img.load()
    for y in range(h):
        for x in range(w):
            if px[x, y][3] > 0:
                yield x, y

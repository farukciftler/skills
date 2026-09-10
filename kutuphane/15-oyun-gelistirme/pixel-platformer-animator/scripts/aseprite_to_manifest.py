#!/usr/bin/env python3
"""
aseprite_to_manifest.py - convert an Aseprite sheet export into the same Unity
manifest that gen_character.py writes, so hand-drawn art goes through the exact
same importer, clip builder and Animator graph as generated art.

Export from Aseprite first (tags = animations, frame durations are kept):
  aseprite -b hero.aseprite --sheet hero_sheet.png --data hero.json \
           --format json-array --sheet-type rows --split-tags --list-tags

Recommended: do NOT pass --trim (Aseprite does not trim unless asked). Untrimmed frames keep one shared
pivot; trimmed frames work too (per-sprite pivots are computed here), but the
validator's ground check only runs on untrimmed frames.

Usage:
  python aseprite_to_manifest.py hero.json --name hero --ppu 16 \
      [--pivot-y 0 | --auto-pivot idle] [--once jump,land,attack,hurt,death] [--out hero.manifest.json]

Loop rule: a tag loops unless it is listed in --once, its Aseprite "repeat"
field is set (>0), or its name is a known one-shot (jump, land, attack, ...).
"""
import argparse
import json
import os
import sys

ONE_SHOT = {"jump", "apex", "land", "crouch", "dash", "attack", "attack2", "attack3",
            "hurt", "death", "die", "roll", "jump_start", "wall_jump", "ledge_climb"}
DEFAULT_EVENTS = {
    "run": [("contact", "OnFootstep")],
    "land": [(0, "OnLand")],
    "jump": [(0, "OnJumpDust")],
    "dash": [(0, "OnDashStart")],
    "death": [(-1, "OnDeathComplete")],
    "attack": [(-1, "OnAttackEnd")],
}


def load_frames(data):
    fr = data["frames"]
    if isinstance(fr, dict):              # json-hash export
        fr = [dict(v, filename=k) for k, v in fr.items()]
    return fr


def expand_tag(tag):
    a, b = tag["from"], tag["to"]
    fwd = list(range(a, b + 1))
    d = tag.get("direction", "forward")
    if d == "reverse":
        return fwd[::-1]
    if d == "pingpong":
        return fwd + fwd[-2:0:-1]
    if d == "pingpong_reverse":
        r = fwd[::-1]
        return r + r[-2:0:-1]
    return fwd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_path")
    ap.add_argument("--name", required=True)
    ap.add_argument("--ppu", type=int, required=True)
    ap.add_argument("--pivot-y", type=float, default=0.0,
                    help="normalized pivot height inside the untrimmed frame (0 = bottom edge)")
    ap.add_argument("--auto-pivot", default=None,
                    help="tag name: put the pivot under the lowest opaque row of that tag's first frame")
    ap.add_argument("--once", default="", help="comma list of tags that must not loop")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    with open(a.json_path) as f:
        data = json.load(f)
    frames = load_frames(data)
    meta = data["meta"]
    tags = meta.get("frameTags", [])
    if not tags:
        print("ERROR: no frameTags - export with --list-tags and tag every animation in Aseprite")
        return 1
    for fr in frames:
        if fr.get("rotated"):
            print(f"ERROR: frame {fr.get('filename')} is rotated - export without rotation")
            return 1
    src_w = frames[0]["sourceSize"]["w"]
    src_h = frames[0]["sourceSize"]["h"]
    tex_w, tex_h = meta["size"]["w"], meta["size"]["h"]
    base = os.path.dirname(os.path.abspath(a.json_path))

    pivot_y = a.pivot_y
    if a.auto_pivot:
        from PIL import Image
        import numpy as np
        tag = next((t for t in tags if t["name"] == a.auto_pivot), None)
        if tag is None:
            print(f"ERROR: --auto-pivot tag '{a.auto_pivot}' not found")
            return 1
        img = np.array(Image.open(os.path.join(base, meta["image"])).convert("RGBA"))
        fr = frames[tag["from"]]
        r, sss = fr["frame"], fr["spriteSourceSize"]
        alpha = img[r["y"]:r["y"] + r["h"], r["x"]:r["x"] + r["w"], 3]
        rows = np.nonzero(alpha.any(axis=1))[0]
        lowest_in_source = sss["y"] + rows.max()
        pivot_y = (src_h - 1 - lowest_in_source) / src_h

    once = set(x.strip() for x in a.once.split(",") if x.strip())
    sprite_of = {}
    sprites = []
    for t in tags:
        for i in range(t["from"], t["to"] + 1):
            if i in sprite_of:
                continue
            fr = frames[i]
            r, sss = fr["frame"], fr["spriteSourceSize"]
            name = f"{a.name}_{t['name']}_{i - t['from']}"
            sprite_of[i] = name
            # pivot in source px (top-left origin): (src_w/2, src_h*(1-pivot_y)) -> rect-normalized, bottom-left origin
            pvx_src = src_w * 0.5
            pvy_src_top = src_h * (1.0 - pivot_y)
            px = (pvx_src - sss["x"]) / r["w"]
            py = (r["h"] - (pvy_src_top - sss["y"])) / r["h"]
            sprites.append({"name": name, "x": r["x"], "y": tex_h - (r["y"] + r["h"]),
                            "w": r["w"], "h": r["h"], "pivotX": round(px, 6), "pivotY": round(py, 6)})

    anims = []
    for t in tags:
        seq = expand_tag(t)
        n = t["name"]
        rep = str(t.get("repeat", "") or "")
        loop = not (n in once or n.lower() in ONE_SHOT or (rep.isdigit() and int(rep) > 0))
        fr_list = [{"sprite": sprite_of[i], "durationMs": int(frames[i].get("duration", 100))} for i in seq]
        events = []
        for where, fn in DEFAULT_EVENTS.get(n.lower(), []):
            if where == "contact":
                events += [{"frame": 0, "function": fn}]
                if len(seq) >= 4:
                    events += [{"frame": len(seq) // 2, "function": fn}]
            else:
                events.append({"frame": where % len(seq), "function": fn})
        anims.append({"name": n, "loop": loop, "frames": fr_list, "events": events})

    manifest = {
        "schema": 2, "name": a.name, "texture": meta["image"],
        "textureWidth": tex_w, "textureHeight": tex_h,
        "frameWidth": src_w, "frameHeight": src_h, "ppu": a.ppu, "facing": "right",
        "sprites": sprites, "animations": anims,
    }
    out = a.out or os.path.join(base, f"{a.name}.manifest.json")
    with open(out, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"OK {len(anims)} tags, {len(sprites)} sprites -> {out}")
    print("NOTE event frames are defaults (footsteps on frame 0 and mid-cycle, etc.) - "
          "edit them to your actual contact/impact frames before import.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

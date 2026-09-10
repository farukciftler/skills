"""render_frames.py — two jobs, one orthographic camera rig:

1) CHECK renders for eyeballing a 3D character (front / side / 3-4 view, plus beat frames of each clip):
     blender -b file.blend --python render_frames.py -- --name Hero --mode check --out renders/Hero
2) 3D -> PIXEL ART (the Dead Cells technique): render every frame of every clip from the SIDE at
   the final sprite resolution with no anti-aliasing, then hand off to pixel/frames_to_sheet.py
   (Pillow, outside Blender) for palette quantize + outline + baseline + sheet:
     blender -b file.blend --python render_frames.py -- --name Hero --mode pixel --px-height 40 --out build/HeroPx
     python ../pixel/frames_to_sheet.py build/HeroPx/frames.json --out build/HeroPx/sheet --colors 12

Side view is chosen so the character faces screen-RIGHT (+x), matching the 2D sheet convention.
Uses Workbench (flat, fast, deterministic); falls back to Cycles if Workbench can't get a GPU context.
"""
import argparse
import json
import math
import os
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--mode", choices=["check", "pixel"], default="check")
    ap.add_argument("--out", required=True)
    ap.add_argument("--px-height", type=int, default=40, help="pixel mode: character height in px")
    ap.add_argument("--clips", default="", help="comma list; default = all actions of the character")
    ap.add_argument("--step", type=int, default=0, help="pixel mode: frame step (0 = auto ~12 fps)")
    ap.add_argument("--engine", default="auto", choices=["auto", "workbench", "cycles"])
    return ap.parse_args(argv)


def _setup_engine(scene, engine, flat=True):
    def workbench():
        scene.render.engine = "BLENDER_WORKBENCH"
        sh = scene.display.shading
        sh.light = "FLAT" if flat else "STUDIO"
        sh.color_type = "TEXTURE"
        scene.display.render_aa = "OFF"

    def cycles():
        scene.render.engine = "CYCLES"
        scene.cycles.samples = 4 if flat else 16
        scene.cycles.device = "CPU"
        scene.cycles.pixel_filter_type = "BOX"
        scene.cycles.filter_width = 0.01
        # flat look: textures via emission-ish world light
        scene.world = scene.world or bpy.data.worlds.new("World")
        scene.world.color = (1, 1, 1)
    if engine == "cycles":
        cycles()
    else:
        workbench()
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.view_settings.view_transform = "Standard"


def _camera(scene, name="UCA_Cam"):
    cam = bpy.data.objects.get(name)
    if not cam:
        cam = bpy.data.objects.new(name, bpy.data.cameras.new(name))
        scene.collection.objects.link(cam)
    cam.data.type = "ORTHO"
    scene.camera = cam
    return cam


def _aim(cam, loc, target):
    cam.location = Vector(loc)
    d = Vector(target) - Vector(loc)
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()  # camera looks down -Z, up = local Y


def _render(scene, path):
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)


def _actions(name, only):
    acts = [a for a in bpy.data.actions if a.get("uca_character") == name]
    if only:
        acts = [a for a in acts if a.name in only]
    return acts


def main():
    a = _args()
    scene = bpy.context.scene
    rig = bpy.data.objects[f"RIG_{a.name}"]
    body = bpy.data.objects[f"CHR_{a.name}"]
    for ob in scene.objects:  # only the character renders
        if ob.type in ("MESH", "LIGHT") and ob != body and ob.parent != rig:
            ob.hide_render = True
    h = max(v.co.z for v in body.data.vertices)
    os.makedirs(a.out, exist_ok=True)
    cam = _camera(scene)
    engine = a.engine
    only = [c for c in a.clips.split(",") if c]
    rig.animation_data_create()

    def try_render(path):
        nonlocal engine
        try:
            _render(scene, path)
        except RuntimeError as e:
            if engine == "auto" and scene.render.engine == "BLENDER_WORKBENCH":
                print(f"Workbench failed ({e}); falling back to Cycles CPU")
                engine = "cycles"
                _setup_engine(scene, "cycles", flat=a.mode == "pixel")
                _render(scene, path)
            else:
                raise
    if a.mode == "check":
        _setup_engine(scene, engine if engine != "auto" else "workbench", flat=False)
        scene.render.resolution_x, scene.render.resolution_y = 640, 640
        cam.data.ortho_scale = h * 1.35
        views = {"front": ((0, -10, h * 0.5), (0, 0, h * 0.5)),
                 "side": ((-10, 0, h * 0.5), (0, 0, h * 0.5)),
                 "threequarter": ((-7, -7, h * 0.9), (0, 0, h * 0.45))}
        rig.animation_data.action = None
        for pb in rig.pose.bones:  # true bind pose, not whatever frame was evaluated last
            pb.rotation_quaternion = (1, 0, 0, 0)
            pb.location = (0, 0, 0)
        out = []
        for v, (loc, tgt) in views.items():
            _aim(cam, loc, tgt)
            p = os.path.join(a.out, f"bind_{v}.png")
            try_render(p)
            out.append(p)
        _aim(cam, *views["threequarter"])
        for act in _actions(a.name, only):
            rig.animation_data.action = act
            fs, fe = int(act.frame_start), int(act.frame_end)
            for f in sorted({fs, fs + (fe - fs) // 3, fs + 2 * (fe - fs) // 3, fe}):
                scene.frame_set(f)
                p = os.path.join(a.out, f"{act.name}_{f:03d}.png")
                try_render(p)
                out.append(p)
        rig.animation_data.action = None
        print(json.dumps({"renders": out}))
        return

    # ---------------- pixel mode ----------------
    _setup_engine(scene, engine if engine != "auto" else "workbench", flat=True)
    px_h = a.px_height
    # generous square canvas; frames_to_sheet crops to the union bbox afterwards
    canvas = int(px_h * 2.2) // 2 * 2
    scene.render.resolution_x = scene.render.resolution_y = canvas
    scene.render.resolution_percentage = 100
    world_per_px = h / px_h
    cam.data.ortho_scale = canvas * world_per_px
    ground_row_from_bottom = int(canvas * 0.12)
    cz = canvas * world_per_px / 2 - ground_row_from_bottom * world_per_px   # camera centre height
    _aim(cam, (-10, 0, cz), (0, 0, cz))   # looking +X -> character (facing -Y) faces screen-right
    fps = scene.render.fps
    step = a.step or max(1, round(fps / 12))
    frames_meta = {"schema": "uca-frames/1", "name": a.name, "canvas": canvas, "groundRow": ground_row_from_bottom,
                   "pxHeight": px_h, "animations": []}
    for act in _actions(a.name, only):
        rig.animation_data.action = act
        fs, fe = int(act.frame_start), int(act.frame_end)
        loop = bool(act.get("uca_loop"))
        rng = list(range(fs, fe if loop else fe + 1, step))  # loops: drop the seam duplicate
        files = []
        for f in rng:
            scene.frame_set(f)
            p = os.path.join(a.out, f"{act.name}_{f:03d}.png")
            try_render(p)
            files.append(os.path.basename(p))
        frames_meta["animations"].append({
            "name": act.name, "loop": loop, "grounded": not act.get("uca_airborne", False),
            "files": files, "durationMs": [round(1000 * step / fps)] * len(files)})
    rig.animation_data.action = None
    mp = os.path.join(a.out, "frames.json")
    with open(mp, "w", encoding="utf-8") as f:
        json.dump(frames_meta, f, indent=2)
    print(json.dumps({"frames": mp, "engine": scene.render.engine}))


if __name__ == "__main__":
    main()

"""uca_character.py — Blender (5.0+) library: spec JSON -> rigged, animated, verified,
Unity-ready humanoid FBX + manifest. Runs identically through an MCP connection
(execute_blender_code) or headless (`blender -b --python pipeline.py -- spec.json`).

MCP usage (chunk it — tool calls time out around a few minutes):
    import sys; sys.path.insert(0, "<skill>/scripts/blender"); import uca_character as uc
    import importlib; importlib.reload(uc)
    spec = uc.load_spec("<path>/hero.json")
    uc.build(spec)          # stage 1: mesh + palette + armature + skin
    uc.animate(spec)        # stage 2: one Action per clip
    print(uc.verify(spec))  # stage 3: numeric gate — must be ok before export
    uc.export(spec, "<out dir>")   # stage 4: FBX + palette PNG + manifest.json

Conventions (do not change casually — the Unity importer and the clip library rely on them):
  * 1 BU = 1 m, Z up, character FACES -Y, character's LEFT is +X, feet on z=0 at origin.
  * bind pose = T-pose (Unity Humanoid avatar creation expects it).
  * bone names = Unity HumanBodyBones names (Hips, Spine, Chest, Neck, Head, LeftUpperArm, ...),
    so the humanoid mapping is explicit, not guessed.
  * rigid per-part skinning (1 part -> 1 bone, weight 1.0): zero weight-paint failure class.
  * clip poses are authored as WORLD-AXIS deltas per bone, composed down the hierarchy
    (see _pose_to_local); forward = -Y, so "lean forward" on an up-pointing bone = +X rotation.
"""
from __future__ import annotations

import json
import math
import os

import bpy
from mathutils import Euler, Matrix, Quaternion, Vector

# ----------------------------------------------------------------------------- spec
DEFAULT_SPEC = {
    "name": "Hero",
    "height": 1.8,
    "headRatio": 6.5,           # 7-7.5 realistic, 5-6 stylized, 3-4 chibi
    "build": 1.0,               # width multiplier
    "style": "mannequin",       # mannequin: joint balls hide rigid-skin seams
    "segments": 8,              # limb cylinder sides (6-10 for low poly)
    "triBudget": 6000,
    "fps": 30,
    "palette": {"skin": "#e0ac8a", "shirt": "#3b5dc9", "pants": "#333c57", "shoes": "#5a3a28",
                "hair": "#3b2a20", "accent": "#ef7d57", "joint": "#29366f"},
    "clips": ["Idle", "Walk", "Run", "Jump_Start", "Jump_Air", "Jump_Land", "Attack", "Hurt", "Death"],
    "locomotion": {"walkSpeed": 1.6, "runSpeed": 4.5},
    "export": {"preset": "bake_axis"},   # bake_axis (Unity Bake Axis Conversion ON) | legacy
}

HUMAN_BONES = ["Hips", "Spine", "Chest", "Neck", "Head",
               "LeftShoulder", "LeftUpperArm", "LeftLowerArm", "LeftHand",
               "RightShoulder", "RightUpperArm", "RightLowerArm", "RightHand",
               "LeftUpperLeg", "LeftLowerLeg", "LeftFoot", "LeftToes",
               "RightUpperLeg", "RightLowerLeg", "RightFoot", "RightToes"]
REQUIRED_15 = ["Hips", "Spine", "Head", "LeftUpperArm", "LeftLowerArm", "LeftHand",
               "RightUpperArm", "RightLowerArm", "RightHand", "LeftUpperLeg", "LeftLowerLeg",
               "LeftFoot", "RightUpperLeg", "RightLowerLeg", "RightFoot"]
PALETTE_KEYS = ["skin", "shirt", "pants", "shoes", "hair", "accent", "joint"]


def load_spec(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        user = json.load(f)
    spec = json.loads(json.dumps(DEFAULT_SPEC))
    for k, v in user.items():
        if isinstance(v, dict) and isinstance(spec.get(k), dict):
            spec[k].update(v)
        else:
            spec[k] = v
    return spec


# ----------------------------------------------------------------------------- proportions
def skeleton_points(spec: dict) -> dict:
    h = float(spec["height"])
    b = float(spec.get("build", 1.0))
    head = h / float(spec["headRatio"])
    neck_z = h - head
    hip_z = neck_z * 0.58
    torso = neck_z - hip_z
    P = {}
    P["hip_z"], P["neck_z"], P["head"], P["h"] = hip_z, neck_z, head, h
    P["spine_z"] = hip_z + torso * 0.22
    P["chest_z"] = hip_z + torso * 0.55
    P["shoulder_z"] = neck_z - torso * 0.10
    P["knee_z"] = hip_z * 0.52
    P["ankle_z"] = hip_z * 0.085
    P["shoulder_x"] = neck_z * 0.125 * b
    P["hip_x"] = neck_z * 0.058 * b
    P["upper_arm"] = torso * 0.62
    P["fore_arm"] = torso * 0.56
    P["hand"] = torso * 0.22
    P["foot"] = hip_z * 0.30
    P["limb_r"] = neck_z * 0.042 * b
    return P


def bone_table(spec: dict) -> list[tuple]:
    """(name, head, tail, parent) in armature space, T-pose."""
    P = skeleton_points(spec)
    sx, hx = P["shoulder_x"], P["hip_x"]
    sz = P["shoulder_z"]
    ua, fa, hd = P["upper_arm"], P["fore_arm"], P["hand"]
    t = [("Root", (0, 0, 0), (0, 0, P["hip_z"] * 0.25), None),
         ("Hips", (0, 0, P["hip_z"]), (0, 0, P["spine_z"]), "Root"),
         ("Spine", (0, 0, P["spine_z"]), (0, 0, P["chest_z"]), "Hips"),
         ("Chest", (0, 0, P["chest_z"]), (0, 0, P["neck_z"] - 0.01), "Spine"),
         ("Neck", (0, 0, P["neck_z"] - 0.01), (0, 0, P["neck_z"] + P["head"] * 0.18), "Chest"),
         ("Head", (0, 0, P["neck_z"] + P["head"] * 0.18), (0, 0, P["h"]), "Neck")]
    for side, s in (("Left", 1), ("Right", -1)):
        t += [(f"{side}Shoulder", (s * 0.02, 0, sz), (s * sx, 0, sz), "Chest"),
              (f"{side}UpperArm", (s * sx, 0, sz), (s * (sx + ua), 0, sz), f"{side}Shoulder"),
              (f"{side}LowerArm", (s * (sx + ua), 0, sz), (s * (sx + ua + fa), 0, sz), f"{side}UpperArm"),
              (f"{side}Hand", (s * (sx + ua + fa), 0, sz), (s * (sx + ua + fa + hd), 0, sz), f"{side}LowerArm"),
              (f"{side}UpperLeg", (s * hx, 0, P["hip_z"]), (s * hx, 0, P["knee_z"]), "Hips"),
              (f"{side}LowerLeg", (s * hx, 0, P["knee_z"]), (s * hx, 0, P["ankle_z"]), f"{side}UpperLeg"),
              (f"{side}Foot", (s * hx, 0, P["ankle_z"]), (s * hx, -P["foot"] * 0.65, P["ankle_z"] * 0.35),
               f"{side}LowerLeg"),
              (f"{side}Toes", (s * hx, -P["foot"] * 0.65, P["ankle_z"] * 0.35), (s * hx, -P["foot"], P["ankle_z"] * 0.35),
               f"{side}Foot")]
    return t


# ----------------------------------------------------------------------------- scene utils
def _clear_character(name: str):
    for ob in list(bpy.data.objects):
        if ob.name in (f"CHR_{name}", f"RIG_{name}") or ob.name.startswith(f"PART_{name}_"):
            bpy.data.objects.remove(ob, do_unlink=True)
    for act in list(bpy.data.actions):
        if act.get("uca_character") == name:
            bpy.data.actions.remove(act)
    for m in list(bpy.data.meshes):
        if m.users == 0:
            bpy.data.meshes.remove(m)


def _hex(c: str) -> tuple:
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def _palette_image(spec: dict):
    """8x8-cell palette atlas (64x64 px, 8px cells), cell i = PALETTE_KEYS[i]. Faces sample cell CENTRES."""
    name = f"TEX_{spec['name']}_Palette"
    img = bpy.data.images.get(name) or bpy.data.images.new(name, 64, 64, alpha=False)
    # ORDER MATTERS: changing colorspace on a generated image regenerates (blanks) its buffer,
    # so set it BEFORE writing pixels. Byte-image pixels[] are the stored sRGB values (no linearize).
    img.colorspace_settings.name = "sRGB"
    px = [0.0] * (64 * 64 * 4)
    for i, key in enumerate(PALETTE_KEYS):
        r, g, b = _hex(spec["palette"].get(key, "#ff00ff"))
        cx, cy = (i % 8) * 8, (i // 8) * 8
        for y in range(cy, cy + 8):
            for x in range(cx, cx + 8):
                o = (y * 64 + x) * 4
                px[o:o + 4] = [r, g, b, 1.0]
    img.pixels[:] = px
    img.pack()  # generated pixels are NOT saved with the .blend unless packed
    return img


def _cell_uv(key: str) -> tuple:
    i = PALETTE_KEYS.index(key)
    return (((i % 8) * 8 + 4) / 64.0, ((i // 8) * 8 + 4) / 64.0)


def _material(spec: dict, img):
    name = f"MAT_{spec['name']}"
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Closest"
    bsdf.inputs["Roughness"].default_value = 0.85
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


# ----------------------------------------------------------------------------- mesh parts
def _part(bm_fn, name: str, bone: str, color: str, matrix: Matrix, coll, mat):
    import bmesh
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bm_fn(bm)
    bmesh.ops.transform(bm, matrix=matrix, verts=bm.verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    uv = bm.loops.layers.uv.new("UVMap")
    u = _cell_uv(color)
    for f in bm.faces:
        for lp in f.loops:
            lp[uv].uv = u
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    me.materials.append(mat)
    vg = ob.vertex_groups.new(name=bone)
    vg.add(list(range(len(me.vertices))), 1.0, "REPLACE")
    return ob


def _cyl(r1, r2, depth, seg):
    import bmesh

    def fn(bm):
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg,
                              radius1=r1, radius2=r2, depth=depth)
    return fn


def _box(sx, sy, sz):
    import bmesh

    def fn(bm):
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=Vector((sx, sy, sz)), verts=bm.verts)
    return fn


def _sphere(r, seg=10, rings=7):
    import bmesh

    def fn(bm):
        bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=r)
    return fn


def _along(a, b, overshoot=0.0) -> tuple[Matrix, float]:
    a, b = Vector(a), Vector(b)
    d = b - a
    L = d.length
    q = Vector((0, 0, 1)).rotation_difference(d.normalized())
    mid = (a + b) / 2
    return Matrix.Translation(mid) @ q.to_matrix().to_4x4(), L + 2 * overshoot


def build(spec: dict) -> dict:
    """Stage 1. Rebuilds from scratch every time (scripts are the source of truth)."""
    name = spec["name"]
    _clear_character(name)
    P = skeleton_points(spec)
    seg = int(spec.get("segments", 8))
    coll = bpy.context.scene.collection
    img = _palette_image(spec)
    mat = _material(spec, img)
    bones = {b[0]: b for b in bone_table(spec)}
    parts = []
    r = P["limb_r"]
    mannequin = spec.get("style", "mannequin") == "mannequin"

    def limb(bname, color, r1, r2, over):
        _, h, t, _ = bones[bname]
        m, L = _along(h, t, over)
        parts.append(_part(_cyl(r1, r2, L, seg), f"PART_{name}_{bname}", bname, color, m, coll, mat))

    torso = P["neck_z"] - P["hip_z"]
    sw = P["shoulder_x"]
    # torso blocks (overlap generously — flat shading hides intersections, gaps read as broken)
    parts.append(_part(_box(sw * 1.55, r * 3.0, torso * 0.46), f"PART_{name}_Chest", "Chest", "shirt",
                       Matrix.Translation((0, 0, P["chest_z"] + torso * 0.17)), coll, mat))
    parts.append(_part(_box(sw * 1.25, r * 2.6, torso * 0.36), f"PART_{name}_Spine", "Spine", "shirt",
                       Matrix.Translation((0, 0, P["spine_z"] + torso * 0.14)), coll, mat))
    parts.append(_part(_box(P["hip_x"] * 3.4, r * 2.7, torso * 0.30), f"PART_{name}_Hips", "Hips", "pants",
                       Matrix.Translation((0, 0, P["hip_z"] + torso * 0.04)), coll, mat))
    parts.append(_part(_box(P["hip_x"] * 3.5, r * 2.8, torso * 0.06), f"PART_{name}_Belt", "Hips", "accent",
                       Matrix.Translation((0, 0, P["hip_z"] + torso * 0.20)), coll, mat))
    # neck + head + hair cap
    limb("Neck", "skin", r * 0.9, r * 0.8, 0.02)
    hr = P["head"] * 0.5
    hc = (0, 0, P["h"] - hr)
    parts.append(_part(_sphere(hr * 0.98, 12, 8), f"PART_{name}_Head", "Head", "skin",
                       Matrix.Translation(hc) @ Matrix.Diagonal((0.9, 0.95, 1.0, 1.0)), coll, mat))
    parts.append(_part(_sphere(hr * 1.02, 12, 8), f"PART_{name}_Hair", "Head", "hair",
                       Matrix.Translation((0, hr * 0.12, P["h"] - hr * 0.78)) @ Matrix.Diagonal((0.93, 0.95, 0.9, 1.0)),
                       coll, mat))
    parts.append(_part(_box(hr * 0.9, hr * 0.12, hr * 0.14), f"PART_{name}_Brow", "Head", "hair",
                       Matrix.Translation((0, -hr * 0.86, P["h"] - hr * 0.72)), coll, mat))  # faces -Y: readable front
    for side, s in (("Left", 1), ("Right", -1)):
        limb(f"{side}Shoulder", "shirt", r * 1.15, r * 1.1, 0.0)
        limb(f"{side}UpperArm", "shirt", r * 1.05, r * 0.9, r * 0.6)
        limb(f"{side}LowerArm", "skin", r * 0.85, r * 0.7, r * 0.5)
        _, h, t, _ = bones[f"{side}Hand"]
        m, L = _along(h, t)
        parts.append(_part(_box(r * 1.5, r * 1.1, L * 1.1), f"PART_{name}_{side}Hand", f"{side}Hand", "skin",
                           m, coll, mat))
        limb(f"{side}UpperLeg", "pants", r * 1.35, r * 1.1, r * 0.6)
        limb(f"{side}LowerLeg", "pants", r * 1.1, r * 0.9, r * 0.5)
        _, h, t, _ = bones[f"{side}Foot"]
        ft = P["foot"]
        parts.append(_part(_box(r * 2.2, ft * 0.75, P["ankle_z"] * 1.3), f"PART_{name}_{side}Foot", f"{side}Foot",
                           "shoes", Matrix.Translation((s * P["hip_x"], -ft * 0.28, P["ankle_z"] * 0.62)), coll, mat))
        parts.append(_part(_box(r * 2.1, ft * 0.35, P["ankle_z"] * 0.75), f"PART_{name}_{side}Toes", f"{side}Toes",
                           "shoes", Matrix.Translation((s * P["hip_x"], -ft * 0.8, P["ankle_z"] * 0.37)), coll, mat))
        if mannequin:  # joint balls weighted to the CHILD bone
            for jb, jr in ((f"{side}UpperArm", 1.15), (f"{side}LowerArm", 0.95), (f"{side}LowerLeg", 1.2),
                           (f"{side}UpperLeg", 1.3)):
                parts.append(_part(_sphere(r * jr, 8, 6), f"PART_{name}_{jb}_J", jb, "joint",
                                   Matrix.Translation(bones[jb][1]), coll, mat))
    # join -> one mesh, one material
    body = parts[0]
    with bpy.context.temp_override(active_object=body, object=body, selected_objects=parts,
                                   selected_editable_objects=parts):
        bpy.ops.object.join()
    body.name = body.data.name = f"CHR_{name}"
    for poly in body.data.polygons:
        poly.use_smooth = False
    # armature
    arm_data = bpy.data.armatures.new(f"RIG_{name}")
    rig = bpy.data.objects.new(f"RIG_{name}", arm_data)
    coll.objects.link(rig)
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode="EDIT")
    eb = arm_data.edit_bones
    for bname, h, t, parent in bone_table(spec):
        e = eb.new(bname)
        e.head, e.tail = Vector(h), Vector(t)
        e.roll = 0.0
        if parent:
            e.parent = eb[parent]
            e.use_connect = False
        e.use_deform = bname != "Root"
    bpy.ops.object.mode_set(mode="OBJECT")
    for pb in rig.pose.bones:
        pb.rotation_mode = "QUATERNION"
    body.parent = rig
    mod = body.modifiers.new("Armature", "ARMATURE")
    mod.object = rig
    rig["uca_character"] = name
    return {"mesh": body.name, "rig": rig.name, "tris": _tris(body), "bones": len(arm_data.bones)}


def _tris(ob) -> int:
    return sum(len(p.vertices) - 2 for p in ob.data.polygons)


# ----------------------------------------------------------------------------- posing
def _rot(axis: str, deg: float) -> Quaternion:
    return Quaternion(Vector({"X": (1, 0, 0), "Y": (0, 1, 0), "Z": (0, 0, 1)}[axis]), math.radians(deg))


def _compose(ops) -> Quaternion:
    """ops = [("X", deg), ("Y", deg)...] applied in order, WORLD axes."""
    q = Quaternion()
    for axis, deg in ops:
        q = _rot(axis, deg) @ q
    return q


def _pose_to_local(rig, deltas: dict) -> dict:
    """deltas: bone -> world-axis rotation applied at that joint (on top of the parent's motion).
    W_b = D_b @ W_parent ; local q_b = R_b^-1 @ W_parent^-1 @ W_b @ R_b   (R_b = rest rotation, armature space)."""
    W = {}
    local = {}
    for b in rig.data.bones:  # bones iterate parents before children
        Wp = W[b.parent.name] if b.parent else Quaternion()
        D = _compose(deltas.get(b.name, []))
        Wb = D @ Wp
        W[b.name] = Wb
        R = b.matrix_local.to_quaternion()
        local[b.name] = R.inverted() @ Wp.inverted() @ Wb @ R
    return local


PLANT_TRACK = ["LeftToes", "RightToes", "LeftFoot", "RightFoot", "LeftHand", "RightHand", "Head", "Hips",
               "LeftLowerLeg", "RightLowerLeg", "Spine", "Chest"]


def _lowest(rig) -> float:
    bpy.context.view_layer.update()
    low = 9.0
    for n in PLANT_TRACK:
        pb = rig.pose.bones[n]
        low = min(low, (rig.matrix_world @ pb.head).z, (rig.matrix_world @ pb.tail).z)
    return low


def _key_pose(rig, frame: int, deltas: dict, hips_offset=(0, 0, 0), plant=True, rest_low=None):
    """plant=True: after posing, move Hips vertically so the LOWEST tracked point sits exactly where it
    sits in the bind pose (feet on the floor); hips_offset.z then acts as an extra LIFT (run float).
    plant="up": airborne poses — only push UP if something would hang below the floor/pivot line
    (tucked legs in a jump), never pull down. This replaces hand-tuned heights — the #1 source of
    feet sinking into the floor (and of sprites hanging below their pivot in the 3D->pixel path)."""
    local = _pose_to_local(rig, deltas)
    for pb in rig.pose.bones:
        pb.rotation_quaternion = local[pb.name]
    hb = rig.data.bones["Hips"]
    to_local = hb.matrix_local.to_3x3().inverted()
    hp = rig.pose.bones["Hips"]
    off = Vector(hips_offset)
    if plant:
        hp.location = to_local @ Vector((off.x, off.y, 0.0))
        dz = rest_low - _lowest(rig)
        if plant == "up":
            dz = max(0.0, dz)
        off = Vector((off.x, off.y, dz + off.z))
    hp.location = to_local @ off
    for pb in rig.pose.bones:
        pb.keyframe_insert("rotation_quaternion", frame=frame, group=pb.name)
    hp.keyframe_insert("location", frame=frame, group="Hips")


# semantic helpers (character faces -Y): keep clip tables readable
def arms(l_down=72, r_down=72, l_swing=0, r_swing=0, l_elbow=8, r_elbow=8, l_twist=0, r_twist=0) -> dict:
    """down: lower from T-pose; swing: forward +; elbow: forward bend +."""
    return {"LeftUpperArm": [("Y", l_down), ("Z", l_twist), ("X", -l_swing)],
            "RightUpperArm": [("Y", -r_down), ("Z", r_twist), ("X", -r_swing)],
            "LeftLowerArm": [("X", -l_elbow)], "RightLowerArm": [("X", -r_elbow)]}


def legs(l_swing=0, r_swing=0, l_knee=2, r_knee=2, l_foot=0, r_foot=0, l_spread=0, r_spread=0) -> dict:
    """swing: thigh forward +; knee: bend +; foot: toes up +; spread: outward +."""
    return {"LeftUpperLeg": [("Y", -l_spread), ("X", -l_swing)], "RightUpperLeg": [("Y", r_spread), ("X", -r_swing)],
            "LeftLowerLeg": [("X", l_knee)], "RightLowerLeg": [("X", r_knee)],
            "LeftFoot": [("X", -l_foot)], "RightFoot": [("X", -r_foot)]}


def torso(lean=0, twist=0, chest_lean=0, chest_twist=0, head=0, head_turn=0, hips_lean=0, hips_twist=0) -> dict:
    """lean: forward +; twist: +Z (turns chest toward character's left)."""
    return {"Hips": [("X", hips_lean), ("Z", hips_twist)], "Spine": [("X", lean), ("Z", twist)],
            "Chest": [("X", chest_lean), ("Z", chest_twist)], "Head": [("X", head), ("Z", head_turn)]}


def pose(*parts) -> dict:
    d = {}
    for p in parts:
        for k, v in p.items():
            d.setdefault(k, []).extend(v)
    return d


def clip_library(P: dict) -> dict:
    """name -> (loop, [(frame, deltas, hips_offset)], meta). Frames at 30 fps. In-place (no root travel):
    the game moves the CharacterController; root motion stays off."""
    h = P["h"]
    k = h / 1.8  # scale vertical offsets with character size
    idle = pose(arms(), legs(l_spread=3, r_spread=3), torso())
    idle_b = pose(arms(l_down=70, r_down=70, l_elbow=12, r_elbow=12), legs(l_spread=3, r_spread=3, l_knee=4, r_knee=4),
                  torso(chest_lean=-2, head=-2))
    lib = {}
    lib["Idle"] = (True, [(0, idle, (0, 0, 0)), (30, idle_b, (0, 0, 0)), (60, idle, (0, 0, 0))], {})

    def cycle(n, swing, knee_sup, knee_rec, arm_sw, elbow, lean, bob_c, bob_p, twist):
        ks = []
        for i, f in enumerate(range(0, n + 1, n // 4)):
            ph = i % 4  # 0 L-contact, 1 passing(L support), 2 R-contact, 3 passing(R support)
            if ph == 0:
                lg = legs(swing, -swing, knee_sup * 0.3, knee_sup, -8, 10)
                am = arms(l_swing=-arm_sw, r_swing=arm_sw, l_elbow=elbow, r_elbow=elbow)
                off, tw = (0, 0, bob_c), twist
            elif ph == 1:
                lg = legs(0, 5, knee_sup, knee_rec, 0, 5)
                am = arms(l_elbow=elbow, r_elbow=elbow)
                off, tw = (0, 0, bob_p), 0
            elif ph == 2:
                lg = legs(-swing, swing, knee_sup, knee_sup * 0.3, 10, -8)
                am = arms(l_swing=arm_sw, r_swing=-arm_sw, l_elbow=elbow, r_elbow=elbow)
                off, tw = (0, 0, bob_c), -twist
            else:
                lg = legs(5, 0, knee_rec, knee_sup, 5, 0)
                am = arms(l_elbow=elbow, r_elbow=elbow)
                off, tw = (0, 0, bob_p), 0
            ks.append((f, pose(lg, am, torso(lean=lean, hips_twist=tw, twist=-tw * 0.6, head=-lean * 0.5)),
                       (off[0], off[1], off[2] * k)))
        return ks
    lib["Walk"] = (True, cycle(32, 24, 8, 42, 18, 16, 3, 0.0, 0.0, 6), {"speedMS": 1.6})
    lib["Run"] = (True, cycle(20, 38, 28, 95, 38, 88, 12, 0.0, 0.035, 9), {"speedMS": 4.5})
    crouch = pose(arms(l_swing=-35, r_swing=-35, l_elbow=20, r_elbow=20), legs(40, 40, 70, 70, -25, -25),
                  torso(lean=18, head=-10))
    takeoff = pose(arms(l_down=20, r_down=20, l_swing=40, r_swing=40, l_elbow=15, r_elbow=15),
                   legs(-5, 10, 5, 12, -30, -20), torso(lean=4))
    lib["Jump_Start"] = (False, [(0, idle, (0, 0, 0)), (5, crouch, (0, 0, 0)), (9, takeoff, (0, 0, 0.02 * k))],
                         {})
    air_a = pose(arms(l_down=35, r_down=35, l_swing=25, r_swing=10, l_elbow=30, r_elbow=30),
                 legs(35, -5, 60, 25, 0, -10), torso(lean=6))
    air_b = pose(arms(l_down=40, r_down=30, l_swing=15, r_swing=25, l_elbow=35, r_elbow=25),
                 legs(30, -8, 55, 30, 0, -10), torso(lean=5))
    lib["Jump_Air"] = (True, [(0, air_a, (0, 0, 0)), (8, air_b, (0, 0, 0)), (16, air_a, (0, 0, 0))],
                       {"plant": "up", "airborne": True})
    impact = pose(arms(l_down=55, r_down=55, l_swing=30, r_swing=30, l_elbow=30, r_elbow=30),
                  legs(45, 45, 85, 85, -30, -30), torso(lean=22, head=-12))
    lib["Jump_Land"] = (False, [(0, air_a, (0, 0, 0)), (3, impact, (0, 0, 0)), (8, crouch, (0, 0, 0)),
                                (14, idle, (0, 0, 0))], {})
    stance = pose(arms(r_swing=10, r_elbow=40, l_swing=15, l_elbow=50), legs(18, -14, 12, 10, 0, 0, 4, 4),
                  torso(twist=10))
    windup = pose(arms(r_down=60, r_swing=-55, r_elbow=70, l_swing=30, l_elbow=60), legs(22, -18, 18, 12, 0, 0, 4, 4),
                  torso(lean=-4, twist=28, chest_twist=12, head_turn=-20))
    strike = pose(arms(r_down=85, r_swing=88, r_elbow=2, l_swing=-25, l_elbow=60), legs(30, -24, 25, 8, -5, 5, 4, 4),
                  torso(lean=12, twist=-24, chest_twist=-14, head_turn=10))
    follow = pose(arms(r_down=80, r_swing=70, r_elbow=15, l_swing=-20, l_elbow=55), legs(28, -22, 22, 8, 0, 0, 4, 4),
                  torso(lean=9, twist=-18, chest_twist=-8))
    lib["Attack"] = (False, [(0, idle, (0, 0, 0)), (4, stance, (0, 0, 0)), (9, windup, (0, 0, 0)),
                             (12, strike, (0, 0, 0)), (17, follow, (0, 0, 0)),
                             (26, idle, (0, 0, 0))], {"impactHint": 12})
    hurt = pose(arms(l_down=60, r_down=60, l_swing=-25, r_swing=-35, l_elbow=40, r_elbow=40),
                legs(-8, 14, 15, 20), torso(lean=-18, chest_lean=-8, head=-20, hips_lean=-6))
    lib["Hurt"] = (False, [(0, idle, (0, 0, 0)), (3, hurt, (0, 0.04 * k, 0)), (12, idle, (0, 0, 0))], {})
    kneel = pose(arms(l_down=65, r_down=65, l_elbow=30, r_elbow=30), legs(70, 60, 120, 110, -35, -35),
                 torso(lean=20, head=15))
    topple = pose(arms(l_down=40, r_down=40, l_swing=30, r_swing=40, l_elbow=20, r_elbow=20),
                  legs(60, 55, 70, 60, 0, 0), torso(hips_lean=-45, lean=-5, head=-10))
    flat = pose(arms(l_down=20, r_down=25, l_swing=10, r_swing=5, l_elbow=10, r_elbow=5),
                legs(0, 6, 3, 8, 20, 20, 6, 8), torso(hips_lean=-88, head=-5, head_turn=25))
    lib["Death"] = (False, [(0, hurt, (0, 0, 0)), (10, kneel, (0, 0, 0)),
                            (20, topple, (0, 0.25 * k, 0)), (30, flat, (0, 0.35 * k, 0)),
                            (44, flat, (0, 0.35 * k, 0))], {})
    return lib


def animate(spec: dict) -> dict:
    """Stage 2. One Action per clip, named EXACTLY as the clip (Unity clip names come from them)."""
    name = spec["name"]
    rig = bpy.data.objects[f"RIG_{name}"]
    scene = bpy.context.scene
    scene.render.fps = int(spec.get("fps", 30))
    lib = clip_library(skeleton_points(spec))
    for act in list(bpy.data.actions):
        if act.get("uca_character") == name:
            bpy.data.actions.remove(act)
    rig.animation_data_create()
    rig.animation_data.action = None
    for pb in rig.pose.bones:
        pb.rotation_quaternion = Quaternion()
        pb.location = Vector()
    rest_low = _lowest(rig)
    made = {}
    for clip in spec["clips"]:
        if clip not in lib:
            raise KeyError(f"no clip '{clip}' in clip_library — add it there (world-axis delta table)")
        loop, keys, meta = lib[clip]
        act = bpy.data.actions.new(clip)
        act["uca_character"] = name
        act["uca_loop"] = loop
        act["uca_airborne"] = bool(meta.get("airborne", False))
        act.use_fake_user = True
        rig.animation_data.action = act
        for f, deltas, off in keys:
            _key_pose(rig, f, deltas, off, plant=meta.get("plant", True), rest_low=rest_low)
        act.use_frame_range = True
        act.frame_start, act.frame_end = keys[0][0], keys[-1][0]
        if meta.get("plant", True):   # True and "up" both: interpolation must never dip below the floor
            _fix_between_keys(rig, act, rest_low)
        if not loop:  # hold-and-settle curves; loops keep bezier auto-clamped for smooth seams
            _set_interp(act, rig, "BEZIER")
        made[clip] = {"frames": keys[-1][0], "loop": loop}
    rig.animation_data.action = None
    for pb in rig.pose.bones:  # back to bind pose so the FBX bind pose is the T-pose
        pb.rotation_quaternion = Quaternion()
        pb.location = Vector()
    return made


def _fix_between_keys(rig, act, rest_low, tol=0.005, passes=3):
    """Keys are planted, but interpolation BETWEEN keys can still dip a limb into the floor
    (rotating hips while lowering). Scan every frame and push Hips up where needed."""
    scene = bpy.context.scene
    hb = rig.data.bones["Hips"]
    to_local = hb.matrix_local.to_3x3().inverted()
    to_arm = hb.matrix_local.to_3x3()
    hp = rig.pose.bones["Hips"]
    for _ in range(passes):
        fixed = 0
        for f in range(int(act.frame_start), int(act.frame_end) + 1):
            scene.frame_set(f)
            low = _lowest(rig)
            if low < rest_low - tol:
                cur = to_arm @ hp.location
                hp.location = to_local @ Vector((cur.x, cur.y, cur.z + (rest_low - low)))
                hp.keyframe_insert("location", frame=f, group="Hips")
                fixed += 1
        if not fixed:
            break


def _reset_pose(rig):
    for pb in rig.pose.bones:
        pb.rotation_quaternion = Quaternion()
        pb.location = Vector()
    bpy.context.view_layer.update()


def _channelbag(act, rig):
    """Blender 5.0 removed action.fcurves — always go through the slot's channelbag."""
    from bpy_extras import anim_utils
    slot = act.slots[0] if len(act.slots) else None
    return anim_utils.action_get_channelbag_for_slot(act, slot) if slot else None


def _set_interp(act, rig, mode):
    cb = _channelbag(act, rig)
    if cb:
        for fc in cb.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = mode


# ----------------------------------------------------------------------------- verify
def _eval_points(rig, bone_names):
    out = {}
    for n in bone_names:
        pb = rig.pose.bones[n]
        out[n] = (rig.matrix_world @ pb.head, rig.matrix_world @ pb.tail)
    return out


def verify(spec: dict) -> dict:
    """Stage 3 gate. Data first, eyes second. ok=False blocks export."""
    name = spec["name"]
    body = bpy.data.objects[f"CHR_{name}"]
    rig = bpy.data.objects[f"RIG_{name}"]
    errors, warns, info = [], [], {}
    names = {b.name for b in rig.data.bones}
    miss = [b for b in HUMAN_BONES if b not in names]
    if miss:
        errors.append(f"missing humanoid bones: {miss}")
    tris = _tris(body)
    info["tris"] = tris
    if tris > int(spec.get("triBudget", 6000)):
        errors.append(f"tri budget {tris} > {spec['triBudget']}")
    for ob in (body, rig):
        if ob.matrix_world != Matrix.Identity(4) and ob is rig:
            errors.append(f"{ob.name} transform not identity (apply transforms before export)")
    zs = [v.co.z for v in body.data.vertices]
    info["height"] = round(max(zs), 4)
    info["minZ"] = round(min(zs), 4)
    if abs(max(zs) - spec["height"]) / spec["height"] > 0.02:
        errors.append(f"height {max(zs):.3f} != spec {spec['height']}")
    if abs(min(zs)) > 0.01:
        errors.append(f"feet not on ground: min z {min(zs):.3f}")
    if len(body.material_slots) != 1:
        warns.append(f"{len(body.material_slots)} material slots (1 is the contract)")
    img = bpy.data.images.get(f"TEX_{name}_Palette")
    if img is None or max(img.pixels[:64 * 4]) == 0.0:
        errors.append("palette texture is blank (check colorspace-before-pixels order)")
    unweighted = sum(1 for v in body.data.vertices if not any(g.weight > 0 for g in v.groups))
    if unweighted:
        errors.append(f"{unweighted} vertices without bone weight")
    groups = {g.name for g in body.vertex_groups}
    if groups - names:
        errors.append(f"vertex groups without bones: {sorted(groups - names)}")
    # facing: toes must be in front (-Y) of the ankles
    if rig.data.bones["LeftToes"].tail_local.y >= rig.data.bones["LeftFoot"].head_local.y:
        errors.append("character does not face -Y (toes behind ankles)")
    # clips
    scene = bpy.context.scene
    track = ["LeftToes", "RightToes", "LeftFoot", "RightFoot", "LeftHand", "RightHand", "Head", "Hips"]
    clips = {}
    rig.animation_data_create()
    for act in [a for a in bpy.data.actions if a.get("uca_character") == name]:
        rig.animation_data.action = act
        fs, fe = int(act.frame_start), int(act.frame_end)
        lowest, reach, reach_f = 9.0, -9.0, fs
        foot_float = 0.0
        for f in range(fs, fe + 1):
            scene.frame_set(f)
            pts = _eval_points(rig, track)
            low_f = min(min(h.z, t.z) for h, t in pts.values())
            lowest = min(lowest, low_f)
            feet = min(pts[n][1].z for n in ("LeftToes", "RightToes"))
            foot_float = max(foot_float, feet)
            fwd = -pts["RightHand"][1].y
            if fwd > reach:
                reach, reach_f = fwd, f
        c = {"frames": fe - fs, "loop": bool(act.get("uca_loop")), "lowestZ": round(lowest, 3)}
        if lowest < -0.03:  # airborne clips too: below the floor line = below the pivot in Unity
            errors.append(f"{act.name}: a limb goes {-lowest:.3f} m below the floor")
        if act.name in ("Idle", "Walk") and foot_float > 0.08:
            warns.append(f"{act.name}: both feet float {foot_float:.3f} m at some frame")
        if act.name == "Attack":
            c["impactFrame"] = reach_f - fs  # MEASURED peak forward reach, not the authored guess
        if c["loop"]:
            scene.frame_set(fs)
            a = [pb.matrix.copy() for pb in rig.pose.bones]
            scene.frame_set(fe)
            b = [pb.matrix.copy() for pb in rig.pose.bones]
            d = max(max(abs(x - y) for rx, ry in zip(ma, mb) for x, y in zip(rx, ry)) for ma, mb in zip(a, b))
            if d > 1e-3:
                errors.append(f"{act.name}: loop seam mismatch {d:.4f}")
        clips[act.name] = c
    rig.animation_data.action = None
    _reset_pose(rig)
    scene.frame_set(0)
    wanted = set(spec["clips"])
    if wanted - set(clips):
        errors.append(f"missing clips: {sorted(wanted - set(clips))}")
    info["clips"] = clips
    return {"ok": not errors, "errors": errors, "warnings": warns, "info": info}


# ----------------------------------------------------------------------------- export
FBX_PRESETS = {
    # Unity: ModelImporter.bakeAxisConversion = true -> root rotation (0,0,0), faces +Z
    "bake_axis": dict(axis_forward="-Y", axis_up="Z", apply_scale_options="FBX_SCALE_ALL",
                      bake_space_transform=False),
    # classic Blender default: Unity root gets (-90,0,0); harmless for Humanoid, ugly for Generic
    "legacy": dict(axis_forward="-Z", axis_up="Y", apply_scale_options="FBX_SCALE_ALL",
                   bake_space_transform=False),
}


def _fbx_kwargs(**kw):
    """Introspect the operator: pass only arguments this Blender build knows (versions drift)."""
    props = {p.identifier for p in bpy.ops.export_scene.fbx.get_rna_type().properties}
    dropped = sorted(k for k in kw if k not in props)
    return {k: v for k, v in kw.items() if k in props}, dropped


def export(spec: dict, out_dir: str) -> dict:
    name = spec["name"]
    os.makedirs(out_dir, exist_ok=True)
    body = bpy.data.objects[f"CHR_{name}"]
    rig = bpy.data.objects[f"RIG_{name}"]
    img = bpy.data.images[f"TEX_{name}_Palette"]
    tex_path = os.path.join(out_dir, f"{name}_Palette.png")
    img.filepath_raw = tex_path
    img.file_format = "PNG"
    img.save()
    preset = spec.get("export", {}).get("preset", "bake_axis")
    kw, dropped = _fbx_kwargs(
        filepath=os.path.join(out_dir, f"{name}.fbx"), use_selection=True,
        object_types={"ARMATURE", "MESH"}, apply_unit_scale=True, use_mesh_modifiers=True,
        mesh_smooth_type="FACE", add_leaf_bones=False, use_armature_deform_only=False,
        primary_bone_axis="Y", secondary_bone_axis="X", armature_nodetype="NULL",
        bake_anim=True, bake_anim_use_all_bones=True, bake_anim_use_nla_strips=False,
        bake_anim_use_all_actions=True, bake_anim_force_startend_keying=True, bake_anim_step=1.0,
        bake_anim_simplify_factor=0.0, path_mode="STRIP", embed_textures=False, **FBX_PRESETS[preset])
    for ob in bpy.context.scene.objects:
        ob.select_set(ob in (body, rig))
    bpy.context.view_layer.objects.active = rig
    rig.animation_data.action = None
    bpy.ops.export_scene.fbx(**kw)
    ver = verify(spec)
    P = skeleton_points(spec)
    manifest = {
        "schema": "uca-3d/1", "name": name, "fbx": f"{name}.fbx", "palette": f"{name}_Palette.png",
        "material": f"MAT_{name}", "height": spec["height"], "fps": spec.get("fps", 30),
        "exportPreset": preset, "bakeAxisConversion": preset == "bake_axis",
        # lists, not dicts: Unity's JsonUtility cannot read dictionaries
        "humanList": [{"bone": b, "human": b} for b in HUMAN_BONES],   # model bone -> HumanBodyBones (identity by design)
        "rootBone": "Root",
        "clipList": [{"name": c, "loop": v["loop"], "frames": v["frames"], "impactFrame": v.get("impactFrame", -1)}
                     for c, v in sorted(ver["info"]["clips"].items())],
        "locomotion": spec.get("locomotion", {}),
        "capsule": {"height": spec["height"], "radius": round(P["shoulder_x"] * 1.1, 3)},
        "blenderVersion": bpy.app.version_string, "fbxArgsDropped": dropped,
    }
    mpath = os.path.join(out_dir, f"{name}.manifest.json")
    with open(mpath, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    return {"fbx": kw["filepath"], "palette": tex_path, "manifest": mpath, "verify_ok": ver["ok"],
            "dropped_args": dropped}

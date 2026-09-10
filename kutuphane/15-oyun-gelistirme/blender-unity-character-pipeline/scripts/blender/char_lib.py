"""
char_lib — Blender-side library for the Blender -> Unity character pipeline.

Runs inside Blender (via an MCP `execute_blender_code` call, the Blender Lab
MCP, or headless `blender --background --python`). Verified end-to-end on
Blender 5.2.1 LTS headless (bpy module). Stages are small so each MCP call
stays well under tool timeouts; every stage returns a short JSON-able report.

Conventions (Blender side)
  * 1 BU = 1 m, Z up, character faces -Y (becomes +Z forward in Unity).
  * Character's LEFT side is +X.
  * Bone names == Unity HumanBodyBones names (Hips, Spine, LeftUpperArm ...)
    so Unity's humanoid auto-mapper matches 100%.
  * Pose authoring uses WORLD-DELTA rotations: a rotation about armature
    axes applied to a bone about its head, AFTER its parents have moved.
      - down-pointing limb (leg / lowered arm): X-  = swing forward
      - LowerLeg: X+ = knee bend (foot goes back)
      - LowerArm (arm lowered): X- = elbow bend forward
      - LeftUpperArm from T-pose: Y+ = lower arm;  RightUpperArm: Y- = lower
      - Foot: X+ = toe down / heel up;  X- = toe up
      - up-pointing bone (Hips/Spine/Chest/Neck/Head): X+ = bend forward
      - Z+ = yaw to character's left (counter-clockwise seen from above)
    The sign table is asserted by `selftest_signs()`.

Public stages (all take a spec path or dict):
  stage_preflight, stage_rig, stage_mesh, stage_fit_mesh, stage_skin,
  stage_clips, stage_verify, stage_export, stage_roundtrip, run_all
"""

import bpy
import bmesh
import json
import math
import os
from mathutils import Matrix, Vector, Quaternion

LIB_VERSION = "1.0.0"

# --------------------------------------------------------------------------
# Humanoid definition
# --------------------------------------------------------------------------

# (name, parent) in hierarchy order. Names match UnityEngine.HumanBodyBones.
HUMANOID_HIERARCHY = [
    ("Root", None),
    ("Hips", "Root"),
    ("Spine", "Hips"),
    ("Chest", "Spine"),
    ("UpperChest", "Chest"),
    ("Neck", "UpperChest"),
    ("Head", "Neck"),
    ("LeftShoulder", "UpperChest"),
    ("LeftUpperArm", "LeftShoulder"),
    ("LeftLowerArm", "LeftUpperArm"),
    ("LeftHand", "LeftLowerArm"),
    ("RightShoulder", "UpperChest"),
    ("RightUpperArm", "RightShoulder"),
    ("RightLowerArm", "RightUpperArm"),
    ("RightHand", "RightLowerArm"),
    ("LeftUpperLeg", "Hips"),
    ("LeftLowerLeg", "LeftUpperLeg"),
    ("LeftFoot", "LeftLowerLeg"),
    ("LeftToes", "LeftFoot"),
    ("RightUpperLeg", "Hips"),
    ("RightLowerLeg", "RightUpperLeg"),
    ("RightFoot", "RightLowerLeg"),
    ("RightToes", "RightFoot"),
]

# The 15 bones Unity requires for a valid humanoid avatar.
UNITY_REQUIRED = [
    "Hips", "Spine", "Head",
    "LeftUpperLeg", "LeftLowerLeg", "LeftFoot",
    "RightUpperLeg", "RightLowerLeg", "RightFoot",
    "LeftUpperArm", "LeftLowerArm", "LeftHand",
    "RightUpperArm", "RightLowerArm", "RightHand",
]

# Landmarks as fractions of total height H (feet on Z=0).
PRESETS = {
    # ~7.5 heads, game-realistic
    "realistic": dict(ankle_z=.045, knee_z=.285, hip_z=.525, hip_x=.055,
                      pelvis_z=.545, spine_z=.60, chest_z=.68, upchest_z=.76,
                      neck_z=.83, head_z=.87, top_z=.995,
                      sh_in_x=.02, sh_z=.815, sh_x=.10, elbow_x=.27,
                      wrist_x=.41, hand_x=.50, ball_y=.10, toe_y=.145,
                      foot_z=.012, heel_y=.035),
    # ~5.5 heads, stylized/hero-cartoon (bigger head & hands, shorter legs)
    "stylized": dict(ankle_z=.05, knee_z=.26, hip_z=.49, hip_x=.065,
                     pelvis_z=.51, spine_z=.565, chest_z=.63, upchest_z=.695,
                     neck_z=.755, head_z=.785, top_z=.995,
                     sh_in_x=.02, sh_z=.735, sh_x=.10, elbow_x=.245,
                     wrist_x=.37, hand_x=.465, ball_y=.11, toe_y=.16,
                     foot_z=.014, heel_y=.04),
}


def joint_table(height, preset="realistic", overrides=None):
    """Return {bone: (head Vector, tail Vector, parent)} in meters, T-pose."""
    p = dict(PRESETS[preset])
    p.update(overrides or {})
    H = float(height)
    f = lambda k: p[k] * H  # noqa: E731
    t = {}

    def put(n, h, tl):
        t[n] = (Vector(h), Vector(tl))

    put("Root", (0, 0, 0), (0, 0, 0.12 * H))
    put("Hips", (0, 0, f("pelvis_z")), (0, 0, f("spine_z")))
    put("Spine", (0, 0, f("spine_z")), (0, 0, f("chest_z")))
    put("Chest", (0, 0, f("chest_z")), (0, 0, f("upchest_z")))
    put("UpperChest", (0, 0, f("upchest_z")), (0, 0, f("neck_z")))
    put("Neck", (0, 0, f("neck_z")), (0, 0, f("head_z")))
    put("Head", (0, 0, f("head_z")), (0, 0, f("top_z")))
    for side, s in (("Left", 1.0), ("Right", -1.0)):
        put(f"{side}Shoulder", (s * f("sh_in_x"), 0, f("sh_z") - .005 * H),
            (s * f("sh_x"), 0, f("sh_z")))
        put(f"{side}UpperArm", (s * f("sh_x"), 0, f("sh_z")),
            (s * f("elbow_x"), .004 * H, f("sh_z")))
        put(f"{side}LowerArm", (s * f("elbow_x"), .004 * H, f("sh_z")),
            (s * f("wrist_x"), 0, f("sh_z")))
        put(f"{side}Hand", (s * f("wrist_x"), 0, f("sh_z")),
            (s * f("hand_x"), 0, f("sh_z")))
        hx = s * f("hip_x")
        put(f"{side}UpperLeg", (hx, 0, f("hip_z")),
            (hx * .95, -.008 * H, f("knee_z")))
        put(f"{side}LowerLeg", (hx * .95, -.008 * H, f("knee_z")),
            (hx * .9, 0, f("ankle_z")))
        put(f"{side}Foot", (hx * .9, 0, f("ankle_z")),
            (hx * .9, -f("ball_y"), f("foot_z")))
        put(f"{side}Toes", (hx * .9, -f("ball_y"), f("foot_z")),
            (hx * .9, -f("toe_y"), f("foot_z")))
    parents = dict(HUMANOID_HIERARCHY)
    return {n: (h, tl, parents[n]) for n, (h, tl) in t.items()}, p


# --------------------------------------------------------------------------
# Spec handling
# --------------------------------------------------------------------------

def load_spec(spec):
    if isinstance(spec, dict):
        s = dict(spec)
        s.setdefault("_dir", os.getcwd())
        return s
    with open(spec, "r", encoding="utf-8") as fh:
        s = json.load(fh)
    s["_dir"] = os.path.dirname(os.path.abspath(spec))
    return s


def _abspath(spec, rel):
    return rel if os.path.isabs(rel) else os.path.join(spec["_dir"], rel)


def _names(spec):
    if not isinstance(spec, dict):
        spec = load_spec(spec)
    n = spec["name"]
    return dict(rig=f"RIG_{n}", body=f"CHR_{n}_Body", coll=f"COL_{n}")


def _rig(spec):
    rig = bpy.data.objects.get(_names(spec)["rig"])
    if rig is None:
        raise RuntimeError("Rig missing - run stage_rig first")
    return rig


def _ensure_collection(name):
    coll = bpy.data.collections.get(name)
    if coll is None:
        coll = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(coll)
    return coll


def _select_only(objs):
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    for o in objs:
        o.select_set(True)
    if objs:
        bpy.context.view_layer.objects.active = objs[0]


# --------------------------------------------------------------------------
# Stage 0 — preflight
# --------------------------------------------------------------------------

def stage_preflight(spec):
    spec = load_spec(spec)
    sc = bpy.context.scene
    sc.unit_settings.system = "METRIC"
    sc.unit_settings.scale_length = 1.0
    sc.render.fps = int(spec.get("fps", 30))
    sc.render.fps_base = 1.0
    return {
        "blender": bpy.app.version_string,
        "lib": LIB_VERSION,
        "fps": sc.render.fps,
        "unit_scale": sc.unit_settings.scale_length,
        "fbx_export_available": hasattr(bpy.ops.export_scene, "fbx"),
        "fbx_import_op": "wm.fbx_import" if hasattr(bpy.ops.wm, "fbx_import")
        else "import_scene.fbx",
        "objects": len(bpy.data.objects),
    }


# --------------------------------------------------------------------------
# Stage 1 — rig
# --------------------------------------------------------------------------

def stage_rig(spec):
    spec = load_spec(spec)
    nm = _names(spec)
    table, _ = joint_table(spec["height"], spec.get("preset", "realistic"),
                           spec.get("landmark_overrides"))
    old = bpy.data.objects.get(nm["rig"])
    if old is not None:
        bpy.data.objects.remove(old, do_unlink=True)
    arm = bpy.data.armatures.get(nm["rig"])
    if arm is not None:
        bpy.data.armatures.remove(arm)
    arm = bpy.data.armatures.new(nm["rig"])
    rig = bpy.data.objects.new(nm["rig"], arm)
    _ensure_collection(nm["coll"]).objects.link(rig)
    _select_only([rig])
    bpy.ops.object.mode_set(mode="EDIT")
    for name, parent in HUMANOID_HIERARCHY:
        head, tail, _ = table[name]
        eb = arm.edit_bones.new(name)
        eb.head, eb.tail = head, tail
        eb.use_deform = True
        eb.use_connect = False
        if parent:
            eb.parent = arm.edit_bones[parent]
    # deterministic rolls: bone Z axis toward -Y (character forward)
    for eb in arm.edit_bones:
        eb.align_roll(Vector((0, -1, 0)) if abs(eb.vector.normalized().y) < .9
                      else Vector((0, 0, 1)))
    bpy.ops.object.mode_set(mode="OBJECT")
    arm.display_type = "STICK"
    for pb in rig.pose.bones:
        pb.rotation_mode = "QUATERNION"
    for sk in spec.get("sockets", []):
        add_socket(spec, sk["name"], sk["parent"], sk.get("offset", (0, 0, 0)))
    return {"rig": rig.name, "bones": len(arm.bones),
            "required_missing": [b for b in UNITY_REQUIRED
                                 if b not in arm.bones]}


# --------------------------------------------------------------------------
# Stage 2a — procedural blockout mesh (rigid per-part groups)
# --------------------------------------------------------------------------

def _frame(axis):
    axis = axis.normalized()
    ref = Vector((0, 0, 1)) if abs(axis.z) < .9 else Vector((1, 0, 0))
    u = axis.cross(ref).normalized()
    v = axis.cross(u).normalized()
    return u, v


def _tube(bm, p0, p1, r0, r1, segs=10, sx=1.0, sy=1.0, ext=.12):
    p0, p1 = Vector(p0), Vector(p1)
    ax = (p1 - p0)
    L = ax.length
    d = ax.normalized()
    a, b = p0 - d * L * ext, p1 + d * L * ext
    u, v = _frame(d)
    rings = []
    for c, r in ((a, r0), (b, r1)):
        ring = []
        for i in range(segs):
            ang = 2 * math.pi * i / segs
            ring.append(bm.verts.new(c + u * math.cos(ang) * r * sx
                                     + v * math.sin(ang) * r * sy))
        rings.append(ring)
    faces = []
    for i in range(segs):
        j = (i + 1) % segs
        faces.append(bm.faces.new((rings[0][i], rings[0][j],
                                   rings[1][j], rings[1][i])))
    faces.append(bm.faces.new(list(reversed(rings[0]))))
    faces.append(bm.faces.new(rings[1]))
    return rings[0] + rings[1], faces


def _box(bm, center, size):
    c, (sx, sy, sz) = Vector(center), size
    vs = [bm.verts.new(c + Vector((x * sx / 2, y * sy / 2, z * sz / 2)))
          for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    idx = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1),
           (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    return vs, [bm.faces.new([vs[i] for i in q]) for q in idx]


def _sphere(bm, center, radius, sy=1.0):
    ret = bmesh.ops.create_uvsphere(bm, u_segments=14, v_segments=9,
                                    radius=radius)
    vs = ret["verts"]
    for v in vs:
        v.co = Vector((v.co.x, v.co.y * sy, v.co.z)) + Vector(center)
    faces = list({f for v in vs for f in v.link_faces})
    return vs, faces


def stage_mesh(spec):
    """Procedural blockout: one tube/box/sphere per bone, rigid-weighted.
    Good for prototyping, animation dev and as a proportion reference."""
    spec = load_spec(spec)
    nm = _names(spec)
    H = spec["height"]
    table, p = joint_table(H, spec.get("preset", "realistic"),
                           spec.get("landmark_overrides"))
    old = bpy.data.objects.get(nm["body"])
    if old is not None:
        bpy.data.objects.remove(old, do_unlink=True)
    bm = bmesh.new()
    dl = bm.verts.layers.deform.verify()
    groups = [n for n, _ in HUMANOID_HIERARCHY if n != "Root"]
    gidx = {n: i for i, n in enumerate(groups)}
    MAT = {"skin": 0, "cloth": 1, "accent": 2}
    parts = []

    def add(bone, geo, mat):
        vs, fs = geo
        for v in vs:
            v[dl][gidx[bone]] = 1.0
        for f in fs:
            f.material_index = MAT[mat]
        parts.append(bone)

    T = lambda n: table[n]  # noqa: E731
    w = H * .085  # torso half-width reference
    add("Hips", _tube(bm, T("Hips")[0] - Vector((0, 0, .03 * H)),
                      T("Hips")[1], w * 1.05, w * .95, 12, 1, .62), "accent")
    add("Spine", _tube(bm, *T("Spine")[:2], w * .92, w * .98, 12, 1, .58),
        "cloth")
    add("Chest", _tube(bm, *T("Chest")[:2], w * .98, w * 1.08, 12, 1, .6),
        "cloth")
    add("UpperChest", _tube(bm, *T("UpperChest")[:2], w * 1.08, w * .7, 12,
                            1, .6), "cloth")
    add("Neck", _tube(bm, *T("Neck")[:2], .028 * H, .026 * H, 8), "skin")
    hh, ht = T("Head")[:2]
    hr = (ht.z - hh.z) * .55
    add("Head", _sphere(bm, hh + Vector((0, -.004 * H, hr * .95)), hr, 1.08),
        "skin")
    for side in ("Left", "Right"):
        add(f"{side}UpperArm", _tube(bm, *T(f"{side}UpperArm")[:2],
                                     .032 * H, .027 * H, 8), "cloth")
        add(f"{side}LowerArm", _tube(bm, *T(f"{side}LowerArm")[:2],
                                     .026 * H, .021 * H, 8), "skin")
        a, b = T(f"{side}Hand")[:2]
        add(f"{side}Hand", _box(bm, (a + b) / 2,
                                ((b - a).length * 1.05, .05 * H, .022 * H)),
            "skin")
        add(f"{side}UpperLeg", _tube(bm, *T(f"{side}UpperLeg")[:2],
                                     .05 * H, .038 * H, 10), "cloth")
        add(f"{side}LowerLeg", _tube(bm, *T(f"{side}LowerLeg")[:2],
                                     .036 * H, .028 * H, 10), "cloth")
        fa, fb = T(f"{side}Foot")[:2]
        heel = p["heel_y"] * H
        add(f"{side}Foot", _box(bm, (fa.x, (fb.y + heel) / 2, fa.z / 2 + .003),
                                (.06 * H, abs(fb.y) + heel, fa.z + .008)),
            "accent")
        ta, tb = T(f"{side}Toes")[:2]
        add(f"{side}Toes", _box(bm, (ta + tb) / 2 + Vector((0, 0, .008)),
                                (.055 * H, (tb - ta).length, .02)), "accent")
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    # simple UVs: planar projection per face into a 0..1 square (placeholder)
    uv = bm.loops.layers.uv.verify()
    for f in bm.faces:
        for lp in f.loops:
            co = lp.vert.co
            lp[uv].uv = ((co.x / H) + .5, co.z / H)
    me = bpy.data.meshes.new(nm["body"])
    bm.to_mesh(me)
    bm.free()
    body = bpy.data.objects.new(nm["body"], me)
    _ensure_collection(nm["coll"]).objects.link(body)
    for g in groups:
        body.vertex_groups.new(name=g)
    # vertex-group index order == `groups` order, matching deform layer keys
    palette = spec.get("palette", {})
    for key, default in (("skin", "#C99A7A"), ("cloth", "#3E5C76"),
                         ("accent", "#8A5A2B")):
        mname = f"MAT_{spec['name']}_{key.capitalize()}"
        mat = bpy.data.materials.get(mname) or bpy.data.materials.new(mname)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        hexc = palette.get(key, default).lstrip("#")
        rgb = [int(hexc[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        lin = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4
               for c in rgb]
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (*lin, 1)
            bsdf.inputs["Roughness"].default_value = .8
        mat.diffuse_color = (*lin, 1)  # viewport/workbench colour
        me.materials.append(mat)
    for poly in me.polygons:
        poly.use_smooth = False
    return {"body": body.name, "verts": len(me.vertices),
            "tris": sum(len(p.vertices) - 2 for p in me.polygons),
            "parts": len(parts), "materials": len(me.materials)}


# --------------------------------------------------------------------------
# Stage 2b — fit an existing / external mesh (user-made, sculpted, AI-gen)
# --------------------------------------------------------------------------

def stage_fit_mesh(spec):
    """Normalize an imported or existing mesh to the spec: height, feet on
    ground, facing -Y, transforms applied, named CHR_<Name>_Body.
    spec['source_mesh'] = file path (.fbx/.glb/.gltf/.obj) or object name."""
    spec = load_spec(spec)
    nm = _names(spec)
    src = spec["source_mesh"]
    before = set(bpy.data.objects)
    if os.path.splitext(str(src))[1].lower() in (".fbx", ".glb", ".gltf",
                                                  ".obj"):
        path = _abspath(spec, src)
        ext = os.path.splitext(path)[1].lower()
        if ext == ".fbx":
            (bpy.ops.wm.fbx_import if hasattr(bpy.ops.wm, "fbx_import")
             else bpy.ops.import_scene.fbx)(filepath=path)
        elif ext in (".glb", ".gltf"):
            bpy.ops.import_scene.gltf(filepath=path)
        else:
            bpy.ops.wm.obj_import(filepath=path)
        new = [o for o in bpy.data.objects if o not in before]
    else:
        new = [bpy.data.objects[src]]
    meshes = [o for o in new if o.type == "MESH"]
    for o in new:  # drop imported rigs/empties, keep meshes
        if o.type != "MESH":
            bpy.data.objects.remove(o, do_unlink=True)
    if not meshes:
        raise RuntimeError("No mesh found in source")
    for o in meshes:
        o.parent = None
        for m in list(o.modifiers):
            if m.type == "ARMATURE":
                o.modifiers.remove(m)
    _select_only(meshes)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    if len(meshes) > 1:
        bpy.ops.object.join()
    body = bpy.context.view_layer.objects.active
    old = bpy.data.objects.get(nm["body"])
    if old is not None and old != body:
        bpy.data.objects.remove(old, do_unlink=True)
    body.name = body.data.name = nm["body"]
    for c in list(body.users_collection):
        c.objects.unlink(body)
    _ensure_collection(nm["coll"]).objects.link(body)
    yaw = float(spec.get("source_yaw_deg", 0.0))  # fix facing if needed
    zs = [(body.matrix_world @ v.co).z for v in body.data.vertices]
    h = max(zs) - min(zs)
    k = spec["height"] / h
    mat = Matrix.Rotation(math.radians(yaw), 4, "Z") @ Matrix.Scale(k, 4)
    body.data.transform(mat)
    co = [v.co for v in body.data.vertices]
    cx = (max(c.x for c in co) + min(c.x for c in co)) / 2
    cy = (max(c.y for c in co) + min(c.y for c in co)) / 2
    body.data.transform(Matrix.Translation((-cx, -cy, -min(c.z for c in co))))
    body.vertex_groups.clear()
    return {"body": body.name, "scale_applied": round(k, 4),
            "verts": len(body.data.vertices),
            "tris": sum(len(p.vertices) - 2 for p in body.data.polygons),
            "note": "Run stage_skin with skin='proximity' or 'heat'."}


# --------------------------------------------------------------------------
# Stage 3 — skinning
# --------------------------------------------------------------------------

def _seg_dist(p, a, b):
    ab = b - a
    t = max(0.0, min(1.0, (p - a).dot(ab) / max(ab.length_squared, 1e-12)))
    return (a + ab * t - p).length


NON_SKIN_PREFIXES = ("SKT_", "CTRL_", "MCH_", "IK_")


def add_socket(spec, name, parent, offset=(0, 0, 0)):
    """Socket bone for equipment (exported, unweighted). name e.g. 'SKT_Hand_R'.
    offset: armature-space offset from the parent bone's tail."""
    spec = load_spec(spec)
    rig = _rig(spec)
    _select_only([rig])
    bpy.ops.object.mode_set(mode="EDIT")
    eb = rig.data.edit_bones.get(name) or rig.data.edit_bones.new(name)
    par = rig.data.edit_bones[parent]
    eb.head = par.tail + Vector(offset)
    eb.tail = eb.head + par.vector.normalized() * .08
    eb.parent = par
    eb.use_deform = True  # kept by deform-only export; never weighted
    bpy.ops.object.mode_set(mode="OBJECT")
    rig.pose.bones[name].rotation_mode = "QUATERNION"
    return {"socket": name, "parent": parent}


def proximity_weights(body, rig, k=3, power=4.0, exclude=("Root",)):
    """Deterministic distance-to-bone-segment weights. Never fails (unlike
    bone heat); adequate for game characters, refine by hand if needed."""
    bones = [b for b in rig.data.bones if b.use_deform and b.name not in
             exclude and not b.name.startswith(NON_SKIN_PREFIXES)]
    segs = [(b.name, b.head_local.copy(), b.tail_local.copy()) for b in bones]
    body.vertex_groups.clear()
    vg = {n: body.vertex_groups.new(name=n) for n, _, _ in segs}
    inv = rig.matrix_world.inverted() @ body.matrix_world
    for v in body.data.vertices:
        p = inv @ v.co
        ds = sorted(((_seg_dist(p, a, b), n) for n, a, b in segs))[:k]
        ws = [(1.0 / max(d, 1e-4) ** power, n) for d, n in ds]
        s = sum(w for w, _ in ws)
        for w, n in ws:
            if w / s > .01:
                vg[n].add([v.index], w / s, "REPLACE")


def stage_skin(spec):
    """skin = 'rigid' (blockout already carries groups), 'proximity', 'heat'.
    Always finishes with limit-to-4 + normalize (Unity default 4 weights)."""
    spec = load_spec(spec)
    nm = _names(spec)
    rig, body = _rig(spec), bpy.data.objects[nm["body"]]
    mode = spec.get("skin", "rigid")
    body.parent = rig
    body.matrix_parent_inverse = rig.matrix_world.inverted()
    mod = next((m for m in body.modifiers if m.type == "ARMATURE"), None)
    if mod is None:
        mod = body.modifiers.new("Armature", "ARMATURE")
    mod.object = rig
    note = ""
    if mode == "proximity":
        proximity_weights(body, rig)
    elif mode == "heat":
        body.vertex_groups.clear()
        _select_only([body, rig])
        bpy.context.view_layer.objects.active = rig
        body.parent = None
        try:
            bpy.ops.object.parent_set(type="ARMATURE_AUTO")
        except RuntimeError as e:  # bone heat failure
            note = f"heat failed ({e}); fell back to proximity"
        body = bpy.data.objects[nm["body"]]
        if not any(len(v.groups) for v in body.data.vertices):
            proximity_weights(body, rig)
            note = note or "heat produced no weights; used proximity"
        mods = [m for m in body.modifiers if m.type == "ARMATURE"]
        for m in mods[1:]:
            body.modifiers.remove(m)
    for vg in list(body.vertex_groups):  # sockets/helpers/root never skin
        if vg.name == "Root" or vg.name.startswith(NON_SKIN_PREFIXES):
            body.vertex_groups.remove(vg)
    _select_only([body])
    bpy.ops.object.vertex_group_limit_total(group_select_mode="ALL", limit=4)
    bpy.ops.object.vertex_group_normalize_all(group_select_mode="ALL",
                                              lock_active=False)
    rep = verify_skin(spec)
    rep["mode"] = mode
    if note:
        rep["note"] = note
    return rep


# --------------------------------------------------------------------------
# FK solver + pose authoring (world-delta convention)
# --------------------------------------------------------------------------

def R(axis, deg):
    return Matrix.Rotation(math.radians(deg), 3, axis)


def Rseq(seq):
    """[['Y', 70], ['X', -10]] -> matrix; first entry applied first."""
    m = Matrix.Identity(3)
    for ax, deg in seq or []:
        m = R(ax.upper(), deg) @ m
    return m


class Skeleton:
    def __init__(self, rig):
        self.rig = rig
        self.order = [b.name for b in rig.data.bones]  # parents first
        self.rest = {b.name: b.matrix_local.copy() for b in rig.data.bones}
        self.parent = {b.name: (b.parent.name if b.parent else None)
                       for b in rig.data.bones}
        self.rel = {}
        for n in self.order:
            p = self.parent[n]
            self.rel[n] = (self.rest[p].inverted() @ self.rest[n]) if p \
                else self.rest[n].copy()
        self.length = {b.name: b.length for b in rig.data.bones}

    def solve(self, pose):
        """pose: {bone: dict(rot=Matrix3 world-delta | abs=Matrix3 absolute
        world rotation of rest frame | aim=(dir, side_hint),
        loc=Vector world offset)}.  Returns (basis, armature-space mats)."""
        M, basis = {}, {}
        for n in self.order:
            p = self.parent[n]
            M0 = (M[p] @ self.rel[n]) if p else self.rel[n].copy()
            s = pose.get(n)
            if not s:
                M[n], basis[n] = M0, Matrix.Identity(4)
                continue
            R0 = M0.to_3x3()
            if "abs" in s:
                Rd = s["abs"] @ self.rest[n].to_3x3()
            elif "aim" in s:
                Rd = _aim_matrix(R0, *s["aim"])
            else:
                Rd = s.get("rot", Matrix.Identity(3)) @ R0
            head = M0.translation + Vector(s.get("loc", (0, 0, 0)))
            Md = Rd.to_4x4()
            Md.translation = head
            M[n] = Md
            basis[n] = M0.inverted() @ Md
        return basis, M

    def point(self, M, bone, where="tail"):
        m = M[bone]
        if where == "head":
            return m.translation.copy()
        return m.translation + m.to_3x3() @ Vector((0, self.length[bone], 0))


def _aim_matrix(R0, direction, side_hint):
    """Orientation whose Y axis = direction and X axis as close as possible
    to side_hint (keeps knee/elbow plane & twist stable)."""
    y = Vector(direction).normalized()
    x = Vector(side_hint)
    x = (x - y * x.dot(y))
    if x.length < 1e-6:
        q = (R0 @ Vector((0, 1, 0))).rotation_difference(y)
        return q.to_matrix() @ R0
    x.normalize()
    z = x.cross(y)
    m = Matrix((x, y, z)).transposed()
    return m


def two_bone_ik(hip, target, L1, L2, pole):
    """Return knee position for a 2-bone chain (hip->knee->ankle)."""
    d_vec = target - hip
    d = min(d_vec.length, (L1 + L2) * .9999)
    d = max(d, abs(L1 - L2) + 1e-4)
    dirv = d_vec.normalized()
    a = (L1 * L1 - L2 * L2 + d * d) / (2 * d)
    h = math.sqrt(max(L1 * L1 - a * a, 0.0))
    pl = Vector(pole) - dirv * Vector(pole).dot(dirv)
    pl = pl.normalized() if pl.length > 1e-6 else Vector((0, -1, 0))
    return hip + dirv * a + pl * h, d_vec.length > (L1 + L2) * .9999


# --------------------------------------------------------------------------
# Action helpers (slotted-action safe: 4.4+ / 5.x)
# --------------------------------------------------------------------------

def new_action(rig, name):
    old = bpy.data.actions.get(name)
    if old is not None:
        bpy.data.actions.remove(old)
    act = bpy.data.actions.new(name)
    act.use_fake_user = True
    ad = rig.animation_data or rig.animation_data_create()
    ad.action = act
    return act


def assign_action(rig, act):
    ad = rig.animation_data or rig.animation_data_create()
    ad.action = act
    if hasattr(ad, "action_slot") and getattr(act, "slots", None):
        if ad.action_slot is None:
            ad.action_slot = act.slots[0]


def key_frame(rig, basis, frame, prev_q):
    for n, B in basis.items():
        pb = rig.pose.bones[n]
        loc, q, _ = B.decompose()
        pq = prev_q.get(n)
        if pq is not None and pq.dot(q) < 0:
            q.negate()
        prev_q[n] = q
        pb.rotation_quaternion = q
        pb.keyframe_insert("rotation_quaternion", frame=frame, group=n)
        if n in ("Root", "Hips"):
            pb.location = loc
            pb.keyframe_insert("location", frame=frame, group=n)


# --------------------------------------------------------------------------
# Procedural clip generators
# --------------------------------------------------------------------------

GAITS = {
    # duty = stance fraction per foot, crouch = hip height factor,
    # bob = vertical pelvis amplitude (xH), lift = swing apex (xH)
    "walk": dict(duty=.62, crouch=.935, bob=.011, lift=.055, sway=.012,
                 yaw=5, roll=3, lean=3, arm=22, elbow=18, heel=14, toe=28,
                 reach=.985),
    "run": dict(duty=.36, crouch=.90, bob=.022, lift=.11, sway=.006,
                yaw=8, roll=4, lean=9, arm=40, elbow=80, heel=6, toe=38,
                reach=.985),
}


class _Ctx:
    def __init__(self, spec, rig):
        self.spec = spec
        self.H = spec["height"]
        self.table, self.p = joint_table(self.H, spec.get("preset",
                                                          "realistic"),
                                         spec.get("landmark_overrides"))
        self.sk = Skeleton(rig)
        self.rig = rig
        t = self.table
        self.L1 = (t["LeftUpperLeg"][1] - t["LeftUpperLeg"][0]).length
        self.L2 = (t["LeftLowerLeg"][1] - t["LeftLowerLeg"][0]).length
        self.ankle_z = t["LeftFoot"][0].z
        self.hipj = {s: t[f"{s}UpperLeg"][0].copy() for s in ("Left", "Right")}
        self.ankle_rest = {s: t[f"{s}Foot"][0].copy()
                           for s in ("Left", "Right")}
        self.ball_vec = t["LeftToes"][0] - t["LeftFoot"][0]
        self.heel_vec = Vector((0, self.p["heel_y"] * self.H, -self.ankle_z))
        self.pelvis = t["Hips"][0].copy()


def _arm_pose(side, lower, swing, elbow, splay=6):
    s = 1 if side == "Left" else -1
    return {f"{side}UpperArm": {"rot": R("X", swing) @ R("Z", -s * splay)
                                @ R("Y", s * lower)},
            f"{side}LowerArm": {"rot": R("X", -elbow)}}


def _leg_ik(c, pose, side, hips_M, ankle_world, foot_pitch, toe_pitch=None):
    """Adds UpperLeg/LowerLeg/Foot/Toes entries to pose for an ankle target.
    hips_M: armature-space matrix of Hips after its pose."""
    hip_rest_rel = c.hipj[side] - c.pelvis
    hip_w = hips_M.translation + hips_M.to_3x3() @ \
        (c.sk.rest["Hips"].to_3x3().inverted() @ hip_rest_rel)
    fwd = Vector((0, -1, 0))
    knee, overreach = two_bone_ik(hip_w, ankle_world, c.L1, c.L2, fwd)
    side_hint = Vector((1 if side == "Left" else -1, 0, 0))
    # bone X axis in rest (roll aligned to -Y) — keep consistent sign
    rx = c.sk.rest[f"{side}UpperLeg"].to_3x3() @ Vector((1, 0, 0))
    if rx.dot(side_hint) < 0:
        side_hint = -side_hint
    pose[f"{side}UpperLeg"] = {"aim": (knee - hip_w, side_hint)}
    pose[f"{side}LowerLeg"] = {"aim": (ankle_world - knee, side_hint)}
    pose[f"{side}Foot"] = {"abs": R("X", foot_pitch)}
    if toe_pitch is not None:
        pose[f"{side}Toes"] = {"abs": R("X", toe_pitch)}
    return overreach


def _hips_matrix(c, loc_off, rot):
    rest = c.sk.rest["Root"] @ (c.sk.rest["Root"].inverted()
                                @ c.sk.rest["Hips"])
    M = (rot @ rest.to_3x3()).to_4x4()
    M.translation = rest.translation + loc_off
    return M


def _smooth(u):
    return u * u * (3 - 2 * u)


def _foot_target(c, g, side, t, step, root_y, D):
    """Ankle world target, foot pitch, toe mode for one foot at cycle time t.
    Stance: contact pivot (heel -> flat -> ball) moves with the ground.
    Swing: ball-pivot unroll (toes kept flat) then heel-pivot pre-strike."""
    ph = (t + (0.0 if side == "Left" else .5)) % 1.0
    lane = c.ankle_rest[side].x
    H = c.H
    if ph < D:
        u = ph / D
        y_rel = -step * D + u * 2 * step * D
        F = Vector((lane, root_y + y_rel, c.ankle_z))
        if u < .15:
            pitch, pv, toe = -g["heel"] * (1 - _smooth(u / .15)), \
                c.heel_vec, None
        elif u > .7:
            pitch, pv, toe = g["toe"] * _smooth((u - .7) / .3), \
                c.ball_vec, 0.0
        else:
            pitch, pv, toe = 0.0, c.ball_vec, 0.0
    else:
        u = (ph - D) / (1 - D)
        y_rel = step * D - _smooth(u) * 2 * step * D
        lift = g["lift"] * H * math.sin(math.pi * u) ** 1.2
        F = Vector((lane, root_y + y_rel, c.ankle_z + lift))
        if u < .5:
            pitch, pv, toe = g["toe"] * (1 - _smooth(u / .5)), \
                c.ball_vec, 0.0
        else:
            pitch, pv, toe = -g["heel"] * _smooth((u - .5) / .5), \
                c.heel_vec, None
    ankle = F + pv - R("X", pitch) @ pv
    return ankle, pitch, toe


def _pelvis(c, g, t, D, kind):
    H = c.H
    hip_z = c.hipj["Left"].z * g["crouch"]
    ph0 = (t - D / 2) if kind == "run" else (t - .06)
    z_off = (hip_z - c.hipj["Left"].z) - g["bob"] * H * \
        math.cos(4 * math.pi * ph0)
    x_off = g["sway"] * H * math.cos(2 * math.pi * (t - D / 2))
    yaw = g["yaw"] * math.cos(2 * math.pi * t)
    roll = g["roll"] * math.sin(2 * math.pi * (t - D / 2))
    rot = R("Z", -yaw) @ R("Y", roll) @ R("X", g["lean"])
    return x_off, z_off, yaw, rot


def _max_reach_ratio(c, g, step, D, kind, samples=48):
    worst = 0.0
    for i in range(samples):
        t = i / samples
        x_off, z_off, _, rot = _pelvis(c, g, t, D, kind)
        hips_M = _hips_matrix(c, Vector((x_off, 0, z_off)), rot)
        for side in ("Left", "Right"):
            rel = c.hipj[side] - c.pelvis
            hip_w = hips_M.translation + rot @ rel
            ankle, _, _ = _foot_target(c, g, side, t, step, 0.0, D)
            worst = max(worst, (ankle - hip_w).length / (c.L1 + c.L2))
    return worst


def gen_locomotion(spec, clip, rig):
    """IK-driven walk/run cycle. Zero contact slip by construction; stride
    is solved numerically as the largest step the legs can reach
    (clip['step'] caps it). clip: {name, type: walk|run, frames,
    root_motion, step?, + any GAITS key override}"""
    c = _Ctx(spec, rig)
    kind = clip["type"]
    g = dict(GAITS[kind])
    g.update({k: v for k, v in clip.items() if k in g})
    N = int(clip["frames"])
    fps = int(spec.get("fps", 30))
    D = g["duty"]
    lo, hi = .02 * c.H, 1.5 * c.H
    for _ in range(40):
        mid = (lo + hi) / 2
        if _max_reach_ratio(c, g, mid, D, kind) <= g["reach"]:
            lo = mid
        else:
            hi = mid
    step = min(lo, float(clip.get("step") or lo))
    v = 2 * step / (N / fps)
    root_motion = bool(clip.get("root_motion", False))
    act = new_action(rig, clip["name"])
    prevq = {}
    overreach = 0
    for f in range(N + 1):
        t = f / N
        root_y = -v * (f / fps) if root_motion else 0.0
        x_off, z_off, yaw, hips_rot = _pelvis(c, g, t, D, kind)
        pose = {"Root": {"loc": (0, root_y, 0)},
                "Hips": {"rot": hips_rot, "loc": (x_off, 0, z_off)},
                "Spine": {"rot": R("Z", yaw * .6) @ R("X", g["lean"] * .3)},
                "Chest": {"rot": R("Z", yaw * .6)},
                "Head": {"abs": R("X", 2)}}
        hips_M = _hips_matrix(c, Vector((x_off, root_y, z_off)), hips_rot)
        for side in ("Left", "Right"):
            ankle, pitch, toe = _foot_target(c, g, side, t, step, root_y, D)
            overreach += _leg_ik(c, pose, side, hips_M, ankle, pitch, toe)
            sgn = 1 if side == "Left" else -1
            pose.update(_arm_pose(side, 72, sgn * g["arm"] *
                                  math.cos(2 * math.pi * t),
                                  g["elbow"] + 6 * math.sin(2 * math.pi * t)))
        basis, _ = c.sk.solve(pose)
        key_frame(rig, basis, f, prevq)
    events = [{"name": "FootstepLeft", "frame": 0},
              {"name": "FootstepRight", "frame": round(N * .5)}]
    return act, {"speed_mps": round(v, 4), "step_m": round(step, 4),
                 "cadence_spm": round(2 * 60 / (N / fps), 1),
                 "events": events, "frames": N,
                 "overreach_frames": overreach}


def gen_idle(spec, clip, rig):
    c = _Ctx(spec, rig)
    N = int(clip["frames"])
    H = c.H
    act = new_action(rig, clip["name"])
    prevq = {}
    cyc = int(clip.get("breaths", 2))
    for f in range(N + 1):
        t = f / N
        b = math.sin(2 * math.pi * cyc * t)
        sway = math.sin(2 * math.pi * t)
        z_off = -.012 * H - .003 * H * (1 + b) / 2
        x_off = .006 * H * sway
        hips_rot = R("Y", 1.2 * sway)
        pose = {"Hips": {"rot": hips_rot, "loc": (x_off, 0, z_off)},
                "Spine": {"rot": R("X", .8 * b) @ R("Y", -.8 * sway)},
                "Chest": {"rot": R("X", 1.2 * b)},
                "Neck": {"rot": R("X", -.6 * b)},
                "Head": {"rot": R("Z", 2.5 * math.sin(2 * math.pi * t + .7))}}
        hips_M = _hips_matrix(c, Vector((x_off, 0, z_off)), hips_rot)
        for side in ("Left", "Right"):
            _leg_ik(c, pose, side, hips_M, c.ankle_rest[side].copy(), 0.0, 0.0)
            pose.update(_arm_pose(side, 74 + 1.5 * b, 2 + 1.5 * b, 14 + 2 * b))
        basis, _ = c.sk.solve(pose)
        key_frame(rig, basis, f, prevq)
    return act, {"speed_mps": 0.0, "events": [], "frames": N}


def gen_keyposes(spec, clip, rig):
    """Pose-to-pose clip with eased interpolation, dense-keyed.
    clip['keys'] = [{frame, pose: {bone: [[axis,deg],...]}, hips: [x,y,z],
                     feet: 'planted'|'free', event: 'Hit'}]
    Bones not listed in a key hold neutral (arms lowered from T-pose
    unless listed). Feet 'planted' -> leg IK keeps rest ankle positions."""
    c = _Ctx(spec, rig)
    keys = sorted(clip["keys"], key=lambda k: k["frame"])
    N = int(clip["frames"])
    act = new_action(rig, clip["name"])
    prevq = {}
    base_arms = {}
    for side in ("Left", "Right"):
        base_arms.update(_arm_pose(side, 74, 2, 14))

    def mats(k):
        out = {}
        for b, seq in k.get("pose", {}).items():
            out[b] = Rseq(seq).to_quaternion()
        return out

    qk = [mats(k) for k in keys]
    events = [{"name": k["event"], "frame": k["frame"]} for k in keys
              if k.get("event")]
    bones = set().union(*[set(q) for q in qk]) if qk else set()
    for f in range(N + 1):
        i = max(j for j, k in enumerate(keys) if k["frame"] <= f) \
            if f >= keys[0]["frame"] else 0
        j = min(i + 1, len(keys) - 1)
        f0, f1 = keys[i]["frame"], keys[j]["frame"]
        u = 0.0 if f1 == f0 else _smooth((f - f0) / (f1 - f0))
        hips0 = Vector(keys[i].get("hips", (0, 0, 0)))
        hips1 = Vector(keys[j].get("hips", (0, 0, 0)))
        hips_off = hips0.lerp(hips1, u)
        pose = {}
        for b in bones:
            q0 = qk[i].get(b, Quaternion())
            q1 = qk[j].get(b, Quaternion())
            rot = q0.slerp(q1, u).to_matrix()
            if b in base_arms and "rot" in base_arms[b]:
                rot = rot @ base_arms[b]["rot"]
            pose[b] = {"rot": rot}
        for b, s in base_arms.items():
            pose.setdefault(b, s)
        hip_rot = pose.get("Hips", {}).get("rot", Matrix.Identity(3))
        pose["Hips"] = {"rot": hip_rot, "loc": hips_off}
        planted = keys[i].get("feet", "planted") == "planted" and \
            keys[j].get("feet", "planted") == "planted"
        if planted:
            hips_M = _hips_matrix(c, hips_off, hip_rot)
            for side in ("Left", "Right"):
                _leg_ik(c, pose, side, hips_M, c.ankle_rest[side].copy(),
                        0.0, 0.0)
        basis, _ = c.sk.solve(pose)
        key_frame(rig, basis, f, prevq)
    return act, {"speed_mps": 0.0, "events": events, "frames": N}


GENERATORS = {"walk": gen_locomotion, "run": gen_locomotion,
              "idle": gen_idle, "keyposes": gen_keyposes}


def stage_clips(spec, only=None):
    spec = load_spec(spec)
    rig = _rig(spec)
    report = {}
    meta = {}
    for clip in spec.get("clips", []):
        if only and clip["name"] not in only:
            continue
        gen = GENERATORS.get(clip["type"])
        if gen is None:
            report[clip["name"]] = "skipped: no generator (author manually)"
            continue
        act, info = gen(spec, clip, rig)
        act.frame_range = (0, int(clip["frames"]))
        if hasattr(act, "use_frame_range"):
            act.use_frame_range = True
        meta[clip["name"]] = info
        report[clip["name"]] = info
    rig["pipeline_clip_meta"] = json.dumps(meta)
    return report


# --------------------------------------------------------------------------
# Verification
# --------------------------------------------------------------------------

def verify_rig(spec):
    spec = load_spec(spec)
    rig = _rig(spec)
    bones = rig.data.bones
    issues = []
    missing = [b for b in UNITY_REQUIRED if b not in bones]
    if missing:
        issues.append(f"missing required humanoid bones: {missing}")
    roots = [b.name for b in bones if b.parent is None]
    if len(roots) != 1:
        issues.append(f"expected 1 root bone, got {roots}")
    for side in ("Left", "Right"):
        ua = bones.get(f"{side}UpperArm")
        if ua:
            vec = (ua.tail_local - ua.head_local).normalized()
            if abs(vec.z) > math.sin(math.radians(10)):
                issues.append(f"{side}UpperArm not T-pose (z={vec.z:.2f})")
        ul = bones.get(f"{side}UpperLeg")
        if ul:
            vec = (ul.tail_local - ul.head_local).normalized()
            if vec.z > -.95:
                issues.append(f"{side}UpperLeg not vertical ({vec.z:.2f})")
    for o in (rig, bpy.data.objects.get(_names(spec)["body"])):
        if o is None:
            continue
        if any(abs(a) > 1e-4 for a in o.rotation_euler) or \
                any(abs(s - 1) > 1e-4 for s in o.scale) or \
                o.location.length > 1e-4:
            issues.append(f"{o.name}: transforms not applied/identity")
    return {"ok": not issues, "issues": issues, "bones": len(bones)}


def verify_skin(spec):
    spec = load_spec(spec)
    body = bpy.data.objects[_names(spec)["body"]]
    rig = _rig(spec)
    deform = {b.name for b in rig.data.bones if b.use_deform}
    names = {g.index: g.name for g in body.vertex_groups}
    zero, over4, notnorm, nondeform = 0, 0, 0, set()
    for v in body.data.vertices:
        gs = [g for g in v.groups if g.weight > 1e-6]
        if not gs:
            zero += 1
            continue
        if len(gs) > 4:
            over4 += 1
        if abs(sum(g.weight for g in gs) - 1) > 1e-3:
            notnorm += 1
        for g in gs:
            if names[g.group] not in deform:
                nondeform.add(names[g.group])
    ok = zero == 0 and over4 == 0 and notnorm == 0 and not nondeform
    return {"ok": ok, "verts": len(body.data.vertices), "unweighted": zero,
            "over4": over4, "not_normalized": notnorm,
            "groups_not_deform_bones": sorted(nondeform)}


def _eval_points(spec, rig, frame):
    """World positions of contact points (ball, toe tip, heel) per foot."""
    bpy.context.scene.frame_set(frame)
    _, p = joint_table(spec["height"], spec.get("preset", "realistic"),
                       spec.get("landmark_overrides"))
    H = spec["height"]
    pb = rig.pose.bones
    mw = rig.matrix_world
    pts = {}
    for side in ("Left", "Right"):
        foot, toes = pb[f"{side}Foot"], pb[f"{side}Toes"]
        rest = rig.data.bones[f"{side}Foot"].matrix_local
        heel_rest = rig.data.bones[f"{side}Foot"].head_local + \
            Vector((0, p["heel_y"] * H, -p["ankle_z"] * H))
        pts[f"{side}Heel"] = mw @ (foot.matrix @ (rest.inverted() @ heel_rest))
        pts[f"{side}Ball"] = mw @ toes.head
        pts[f"{side}ToeTip"] = mw @ toes.tail
        pts[f"{side}Ankle"] = mw @ foot.head
    pts["Root"] = mw @ pb["Root"].head
    return pts


def verify_clip(spec, clip_name):
    """Numeric gates: loop continuity, floor penetration, contact slip."""
    spec = load_spec(spec)
    rig = _rig(spec)
    clip = next(c for c in spec["clips"] if c["name"] == clip_name)
    act = bpy.data.actions[clip_name]
    assign_action(rig, act)
    N = int(clip["frames"])
    fps = int(spec.get("fps", 30))
    issues = []
    frames = [_eval_points(spec, rig, f) for f in range(N + 1)]
    # floor
    lowest = min(min(p[k].z for k in p if k.endswith(("ToeTip", "Ball", "Heel")))
                 for p in frames)
    if lowest < -.01:
        issues.append(f"floor penetration {lowest * 100:.1f} cm")
    # loop continuity (compare root-relative bone basis first vs last)
    if clip.get("loop", False):
        worst = 0.0
        bpy.context.scene.frame_set(0)
        q0 = {pb.name: pb.matrix.copy() for pb in rig.pose.bones}
        r0 = rig.pose.bones["Root"].matrix.translation.copy()
        bpy.context.scene.frame_set(N)
        rN = rig.pose.bones["Root"].matrix.translation.copy()
        for pb in rig.pose.bones:
            a = q0[pb.name].copy()
            b = pb.matrix.copy()
            a.translation -= r0
            b.translation -= rN
            worst = max(worst, (a.translation - b.translation).length,
                        a.to_quaternion().rotation_difference(
                            b.to_quaternion()).angle)
        if worst > 1e-3:
            issues.append(f"loop mismatch {worst:.4f}")
    # contact slip: a point is 'in contact' when within 1.5 cm of floor;
    # measure horizontal travel between consecutive contact frames.
    slip_max = 0.0
    speed = 0.0
    if not clip.get("root_motion", False) and clip["type"] in ("walk", "run"):
        meta = json.loads(rig.get("pipeline_clip_meta", "{}"))
        speed = meta.get(clip_name, {}).get("speed_mps", 0.0)
    ground_v = Vector((0, speed / fps, 0))  # treadmill for in-place
    for key in ("LeftBall", "RightBall", "LeftHeel", "RightHeel"):
        for f in range(N):
            a, b = frames[f][key], frames[f + 1][key]
            if a.z < .015 and b.z < .015:
                d = (b - a) - ground_v
                d.z = 0
                slip_max = max(slip_max, d.length)
    if slip_max > .004:
        issues.append(f"contact slip {slip_max * 100:.2f} cm/frame")
    return {"clip": clip_name, "ok": not issues, "issues": issues,
            "lowest_cm": round(lowest * 100, 2),
            "max_slip_cm_per_frame": round(slip_max * 100, 3)}


def stage_verify(spec):
    spec = load_spec(spec)
    out = {"rig": verify_rig(spec), "skin": verify_skin(spec), "clips": []}
    for c in spec.get("clips", []):
        if c["name"] in bpy.data.actions:
            out["clips"].append(verify_clip(spec, c["name"]))
    out["ok"] = out["rig"]["ok"] and out["skin"]["ok"] and \
        all(c["ok"] for c in out["clips"])
    return out


def selftest_signs(spec):
    """Asserts the sign conventions documented at the top of this file."""
    spec = load_spec(spec)
    rig = _rig(spec)
    sk = Skeleton(rig)
    res = {}
    _, M0 = sk.solve({})
    base = sk.point(M0, "LeftLowerLeg")
    _, M = sk.solve({"LeftUpperLeg": {"rot": R("X", -20)}})
    res["leg X- swings forward (-Y)"] = sk.point(M, "LeftLowerLeg").y < base.y
    _, M = sk.solve({"LeftUpperArm": {"rot": R("Y", 60)}})
    res["LeftUpperArm Y+ lowers"] = sk.point(M, "LeftUpperArm").z < \
        sk.point(M0, "LeftUpperArm").z
    _, M = sk.solve({"RightUpperArm": {"rot": R("Y", -60)}})
    res["RightUpperArm Y- lowers"] = sk.point(M, "RightUpperArm").z < \
        sk.point(M0, "RightUpperArm").z
    _, M = sk.solve({"LeftFoot": {"rot": R("X", 20)}})
    res["Foot X+ toe down"] = sk.point(M, "LeftFoot").z < \
        sk.point(M0, "LeftFoot").z
    _, M = sk.solve({"Spine": {"rot": R("X", 20)}})
    res["Spine X+ bends forward"] = sk.point(M, "Head").y < \
        sk.point(M0, "Head").y
    _, M = sk.solve({"Hips": {"rot": R("Z", 30)}})
    res["Hips Z+ yaws: left hip moves back"] = \
        sk.point(M, "LeftUpperLeg", "head").y > \
        sk.point(M0, "LeftUpperLeg", "head").y
    return res


# --------------------------------------------------------------------------
# Export
# --------------------------------------------------------------------------

FBX_COMMON = dict(
    apply_scale_options="FBX_SCALE_ALL", apply_unit_scale=True,
    global_scale=1.0, axis_forward="-Z", axis_up="Y",
    bake_space_transform=False, use_space_transform=True,
    add_leaf_bones=False, primary_bone_axis="Y", secondary_bone_axis="X",
    use_armature_deform_only=True, armature_nodetype="NULL",
    mesh_smooth_type="FACE", use_mesh_modifiers=True, use_tspace=False,
    use_custom_props=False, path_mode="COPY", embed_textures=True,
    use_selection=True, use_metadata=True,
)


def _fbx_kwargs(**kw):
    """Drop kwargs this Blender's exporter doesn't know (version drift)."""
    known = {p.identifier for p in
             bpy.ops.export_scene.fbx.get_rna_type().properties}
    return {k: v for k, v in kw.items() if k in known}


def stage_export(spec):
    spec = load_spec(spec)
    nm = _names(spec)
    rig, body = _rig(spec), bpy.data.objects[nm["body"]]
    out_dir = _abspath(spec, spec.get("export_dir", "exports"))
    os.makedirs(out_dir, exist_ok=True)
    sc = bpy.context.scene
    name = spec["name"]
    files = {}
    # model: rest pose, no animation
    ad = rig.animation_data or rig.animation_data_create()
    ad.action = None
    for pb in rig.pose.bones:
        pb.location = (0, 0, 0)
        pb.rotation_quaternion = (1, 0, 0, 0)
        pb.scale = (1, 1, 1)
    sc.frame_set(0)
    _select_only([rig, body])
    model_path = os.path.join(out_dir, f"{name}.fbx")
    bpy.ops.export_scene.fbx(**_fbx_kwargs(
        filepath=model_path, object_types={"ARMATURE", "MESH"},
        bake_anim=False, **FBX_COMMON))
    files["model"] = os.path.basename(model_path)
    # one file per clip: Name@Clip.fbx (armature only)
    meta = json.loads(rig.get("pipeline_clip_meta", "{}"))
    clips = []
    for clip in spec.get("clips", []):
        act = bpy.data.actions.get(clip["name"])
        if act is None:
            continue
        assign_action(rig, act)
        sc.frame_start, sc.frame_end = 0, int(clip["frames"])
        _select_only([rig])
        path = os.path.join(out_dir, f"{name}@{clip['name']}.fbx")
        bpy.ops.export_scene.fbx(**_fbx_kwargs(
            filepath=path, object_types={"ARMATURE"}, bake_anim=True,
            bake_anim_use_all_bones=True, bake_anim_use_nla_strips=False,
            bake_anim_use_all_actions=False,
            bake_anim_force_startend_keying=True, bake_anim_step=1.0,
            bake_anim_simplify_factor=0.0, **FBX_COMMON))
        info = meta.get(clip["name"], {})
        clips.append({
            "name": clip["name"], "file": os.path.basename(path),
            "frames": int(clip["frames"]), "fps": int(spec.get("fps", 30)),
            "loop": bool(clip.get("loop", False)),
            "root_motion": bool(clip.get("root_motion", False)),
            "speed_mps": info.get("speed_mps", clip.get("speed_mps", 0.0)),
            "events": info.get("events", clip.get("events", [])),
            "state": clip.get("state", clip["name"]),
        })
    ad.action = None
    manifest = {
        "schema": "blender-unity-character/1",
        "name": name, "rig_type": spec.get("rig_type", "humanoid"),
        "height_m": spec["height"], "fps": int(spec.get("fps", 30)),
        "model": files["model"], "clips": clips,
        "unity_folder": spec.get("unity_folder",
                                 f"Assets/Characters/{name}"),
        "root_bone": "Root",
        "sockets": [b.name for b in rig.data.bones
                    if b.name.startswith("SKT_")],
        "humanoid_map": {b: b for b, _ in HUMANOID_HIERARCHY if b != "Root"},
        "blender": bpy.app.version_string, "lib": LIB_VERSION,
    }
    mpath = os.path.join(out_dir, f"{name}.character.json")
    with open(mpath, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
    return {"dir": out_dir, "model": files["model"],
            "clips": [c["file"] for c in clips],
            "manifest": os.path.basename(mpath)}


def _sample_points(rig, frames, scene=None):
    sc = scene or bpy.context.scene
    out = []
    names = ("LeftToes", "RightToes", "LeftHand", "RightHand", "Head")
    for f in frames:
        sc.frame_set(f)
        out.append({n: rig.matrix_world @ rig.pose.bones[n].head
                    for n in names if n in rig.pose.bones})
    return out


def stage_roundtrip(spec):
    """Re-import every exported FBX into a scratch scene; check bone set,
    frame count, mesh presence AND animation fidelity (world positions of
    toes/hands/head vs. the source action, in cm). Working scene untouched."""
    spec = load_spec(spec)
    out_dir = _abspath(spec, spec.get("export_dir", "exports"))
    with open(os.path.join(out_dir, f"{spec['name']}.character.json")) as fh:
        man = json.load(fh)
    rig = _rig(spec)
    expected = {b.name for b in rig.data.bones if b.use_deform}
    src = {}
    for c in man["clips"]:
        N = c["frames"]
        fr = sorted({0, N // 3, (2 * N) // 3, N})
        assign_action(rig, bpy.data.actions[c["name"]])
        src[c["file"]] = (fr, _sample_points(rig, fr))
    rig.animation_data.action = None
    scratch = bpy.data.scenes.new("__roundtrip__")
    res = {"files": [], "ok": True}
    imp = bpy.ops.wm.fbx_import if hasattr(bpy.ops.wm, "fbx_import") \
        else bpy.ops.import_scene.fbx
    try:
        for fname in [man["model"]] + [c["file"] for c in man["clips"]]:
            before_obj, before_act = set(bpy.data.objects), \
                set(bpy.data.actions)
            with bpy.context.temp_override(scene=scratch):
                imp(filepath=os.path.join(out_dir, fname))
            new = [o for o in bpy.data.objects if o not in before_obj]
            acts = [a for a in bpy.data.actions if a not in before_act]
            arms = [o for o in new if o.type == "ARMATURE"]
            bones = {b.name for b in arms[0].data.bones} if arms else set()
            r = {"file": fname, "bones_ok": bones == expected,
                 "missing_bones": sorted(expected - bones),
                 "extra_bones": sorted(bones - expected),
                 "meshes": sum(o.type == "MESH" for o in new),
                 "takes": [(a.name, int(a.frame_range[1] - a.frame_range[0]))
                           for a in acts]}
            if fname in src and arms and acts:
                fr, ref = src[fname]
                off = int(round(acts[0].frame_range[0]))
                arm = arms[0]
                # Blender's importer infers tails and may mark bones as
                # connected, which silently ignores their translation keys.
                # Unity has no such concept -> disconnect before comparing.
                vl = scratch.view_layers[0]
                with bpy.context.temp_override(scene=scratch, view_layer=vl,
                                               active_object=arm, object=arm,
                                               selected_objects=[arm]):
                    bpy.ops.object.mode_set(mode="EDIT")
                    for eb in arm.data.edit_bones:
                        eb.use_connect = False
                    bpy.ops.object.mode_set(mode="OBJECT")
                ad = arm.animation_data or arm.animation_data_create()
                ad.action = acts[0]
                if hasattr(ad, "action_slot") and acts[0].slots and \
                        ad.action_slot is None:
                    ad.action_slot = acts[0].slots[0]
                got = _sample_points(arm, [f + off for f in fr], scratch)
                err = max((got[i][n] - ref[i][n]).length
                          for i in range(len(fr)) for n in ref[i])
                r["fidelity_err_cm"] = round(err * 100, 3)
                if err > .005:
                    res["ok"] = False
            if not r["bones_ok"]:
                res["ok"] = False
            res["files"].append(r)
            for o in new:
                bpy.data.objects.remove(o, do_unlink=True)
            for a in acts:
                bpy.data.actions.remove(a)
    finally:
        bpy.data.scenes.remove(scratch)
    return res


# --------------------------------------------------------------------------
# Visual check — contact sheet (eyes second, after numeric gates)
# --------------------------------------------------------------------------

VIEWS = {  # camera location direction (from target), used with ORTHO
    "side": Vector((1, 0, 0)), "front": Vector((0, -1, 0)),
    "three_quarter": Vector((1, -1, .45)), "top": Vector((0, -.2, 1)),
}


def render_sheet(spec, clip_name=None, frames=8, view="side", size=256,
                 out=None):
    """Render `frames` evenly spaced poses of a clip (or the rest pose) with
    Workbench into ONE grid PNG; returns its path. Works headless."""
    import numpy as np
    spec = load_spec(spec)
    rig = _rig(spec)
    sc = bpy.context.scene
    H = spec["height"]
    tmp_objs = []
    cam_d = bpy.data.cameras.new("__sheet_cam")
    cam_d.type = "ORTHO"
    cam_d.ortho_scale = H * 1.5
    cam = bpy.data.objects.new("__sheet_cam", cam_d)
    sc.collection.objects.link(cam)
    tmp_objs.append(cam)
    fl = bpy.data.meshes.new("__sheet_floor")
    fl.from_pydata([(-3, -3, 0), (3, -3, 0), (3, 3, 0), (-3, 3, 0)], [],
                   [(0, 1, 2, 3)])
    flo = bpy.data.objects.new("__sheet_floor", fl)
    sc.collection.objects.link(flo)
    tmp_objs.append(flo)
    prev = (sc.camera, sc.render.engine, sc.render.resolution_x,
            sc.render.resolution_y, sc.render.filepath)
    sc.camera = cam
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.display.shading.color_type = "MATERIAL"
    sc.render.resolution_x = sc.render.resolution_y = size
    frames_list = [0]
    if clip_name:
        clip = next(c for c in spec["clips"] if c["name"] == clip_name)
        assign_action(rig, bpy.data.actions[clip_name])
        N = int(clip["frames"])
        frames_list = [round(i * N / max(frames, 1)) for i in range(frames)]
    else:
        if rig.animation_data:
            rig.animation_data.action = None
        for pb in rig.pose.bones:
            pb.location, pb.rotation_quaternion = (0, 0, 0), (1, 0, 0, 0)
    tiles = []
    d = VIEWS[view].normalized()
    tmp_png = os.path.join(bpy.app.tempdir or "/tmp", "__sheet_tile.png")
    for f in frames_list:
        sc.frame_set(f)
        root = rig.matrix_world @ rig.pose.bones["Root"].head
        target = Vector((root.x, root.y, H * .5))
        cam.location = target + d * H * 3
        cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
        flo.location = (root.x, root.y, 0)
        sc.render.filepath = tmp_png
        bpy.ops.render.render(write_still=True)
        img = bpy.data.images.load(tmp_png, check_existing=False)
        px = np.array(img.pixels[:], dtype=np.float32).reshape(
            size, size, 4)
        bpy.data.images.remove(img)
        tiles.append(px)
    cols = min(len(tiles), 8)
    rows = math.ceil(len(tiles) / cols)
    sheet = np.ones((rows * size, cols * size, 4), dtype=np.float32)
    for i, tpx in enumerate(tiles):
        r, c_ = divmod(i, cols)
        r = rows - 1 - r  # image origin bottom-left
        sheet[r * size:(r + 1) * size, c_ * size:(c_ + 1) * size] = tpx
    out = out or _abspath(spec, os.path.join(
        spec.get("export_dir", "exports"), "renders",
        f"{spec['name']}_{clip_name or 'rest'}_{view}.png"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    a = sheet[..., 3:4]
    sheet[..., :3] = sheet[..., :3] * a + (1 - a) * .93  # flatten on grey
    sheet[..., 3] = 1
    im = bpy.data.images.new("__sheet", cols * size, rows * size, alpha=True)
    im.pixels = sheet.ravel()
    im.filepath_raw = out
    im.file_format = "PNG"
    im.save()
    bpy.data.images.remove(im)
    sc.camera, sc.render.engine, sc.render.resolution_x, \
        sc.render.resolution_y, sc.render.filepath = prev
    for o in tmp_objs:
        data = o.data
        bpy.data.objects.remove(o, do_unlink=True)
        if isinstance(data, bpy.types.Camera):
            bpy.data.cameras.remove(data)
        else:
            bpy.data.meshes.remove(data)
    return {"sheet": out, "frames": frames_list, "view": view}


def run_all(spec):
    out = {"preflight": stage_preflight(spec)}
    s = load_spec(spec)
    out["rig"] = stage_rig(spec)
    out["mesh"] = stage_fit_mesh(spec) if s.get("source_mesh") \
        else stage_mesh(spec)
    out["skin"] = stage_skin(spec)
    out["clips"] = stage_clips(spec)
    out["verify"] = stage_verify(spec)
    out["export"] = stage_export(spec)
    out["roundtrip"] = stage_roundtrip(spec)
    return out

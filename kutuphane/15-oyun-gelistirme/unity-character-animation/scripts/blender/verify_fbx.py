"""verify_fbx.py — trust the FILE, not the scene that wrote it. Reads the exported FBX two ways:
  1) raw parse (Blender's own FBX parser, no import): GlobalSettings axes/unit + animation TAKE names
     — the take names are exactly the clip names Unity will show.
  2) clean re-import into an empty scene: armature bone set, mesh, action count.

    blender -b --factory-startup --python verify_fbx.py -- build/Hero/Hero.fbx build/Hero/Hero.manifest.json
Exit 1 on any mismatch with the manifest.
"""
import json
import os
import sys

import bpy


def raw_parse(path):
    from io_scene_fbx import parse_fbx
    root, version = parse_fbx.parse(path)
    out = {"fbxVersion": version, "takes": [], "global": {}}

    def find(elem, name):
        return [c for c in elem.elems if c.id == name.encode()]

    for gs in find(root, "GlobalSettings"):
        for p70 in find(gs, "Properties70"):
            for p in p70.elems:
                key = p.props[0].decode() if isinstance(p.props[0], bytes) else p.props[0]
                if key in ("UpAxis", "UpAxisSign", "FrontAxis", "FrontAxisSign", "CoordAxis", "CoordAxisSign",
                           "UnitScaleFactor", "OriginalUnitScaleFactor"):
                    out["global"][key] = p.props[-1]
    for takes in find(root, "Takes"):
        for t in find(takes, "Take"):
            n = t.props[0]
            out["takes"].append(n.decode() if isinstance(n, bytes) else n)
    # FBX 7.x stores stacks as Objects/AnimationStack; names are "AnimStack::<name>" encoded
    for objs in find(root, "Objects"):
        for st in find(objs, "AnimationStack"):
            raw = st.props[1]
            s = raw.decode("utf-8", "replace") if isinstance(raw, bytes) else str(raw)
            s = s.split("\x00\x01")[0]
            if s not in out["takes"]:
                out["takes"].append(s)
    return out


def reimport(path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    before = set(bpy.data.actions)
    bpy.ops.import_scene.fbx(filepath=path)
    arm = [o for o in bpy.data.objects if o.type == "ARMATURE"]
    mesh = [o for o in bpy.data.objects if o.type == "MESH"]
    return {"armatures": len(arm), "bones": sorted(b.name for b in arm[0].data.bones) if arm else [],
            "meshes": len(mesh), "tris": sum(sum(len(p.vertices) - 2 for p in m.data.polygons) for m in mesh),
            "actions": sorted(a.name for a in bpy.data.actions if a not in before)}


def clip_from_take(take: str) -> str:
    """Blender writes takes as '<ArmatureObject>|<Action>'; Unity shows that string as the clip name."""
    return take.split("|")[-1]


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    fbx, manifest_path = argv[0], (argv[1] if len(argv) > 1 else None)
    rep = {"file": fbx, "sizeKB": round(os.path.getsize(fbx) / 1024, 1), "raw": raw_parse(fbx), "import": reimport(fbx)}
    errors = []
    if manifest_path:
        with open(manifest_path, encoding="utf-8") as f:
            man = json.load(f)
        clips = sorted({clip_from_take(t) for t in rep["raw"]["takes"]})
        want = sorted(c["name"] for c in man["clipList"])
        if clips != want:
            errors.append(f"takes {clips} != manifest clips {want}")
        missing = [h["bone"] for h in man["humanList"] if h["bone"] not in rep["import"]["bones"]]
        if missing:
            errors.append(f"bones missing after re-import: {missing}")
        g = rep["raw"]["global"]
        if man.get("bakeAxisConversion") and g.get("UpAxis") != 2:
            errors.append(f"preset bake_axis expects Z-up file (UpAxis=2), got {g.get('UpAxis')}")
        if g.get("UnitScaleFactor") not in (100, 100.0):
            errors.append(f"UnitScaleFactor {g.get('UnitScaleFactor')} (expected 100 -> Unity shows 1m, scale 1)")
    rep["errors"] = errors
    rep["ok"] = not errors
    print(json.dumps(rep, indent=2))
    sys.exit(0 if rep["ok"] else 1)


if __name__ == "__main__":
    main()

"""Headless runner — same library the MCP session uses, no MCP limits (prefer this for full rebuilds).

    blender -b --factory-startup --python pipeline.py -- spec.json --out build/Hero [--stage all]
    # stages: build | animate | verify | export | all   (export implies verify; fails on errors)
    # --render DIR : also save front/side/game-cam check renders (Workbench) for eyeballing
Exit code 1 if the verify gate fails.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
import uca_character as uc  # noqa: E402


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--out", required=True)
    ap.add_argument("--stage", default="all")
    ap.add_argument("--save-blend", action="store_true", help="checkpoint .blend next to the FBX")
    a = ap.parse_args(argv)
    spec = uc.load_spec(a.spec)
    report = {"blender": bpy.app.version_string}
    if bpy.app.version < (5, 0, 0):
        print("WARNING: written for Blender 5.x slotted-action API; 4.4-4.5 mostly works, <4.4 will not")
    if a.stage in ("build", "all"):
        report["build"] = uc.build(spec)
    if a.stage in ("animate", "all"):
        report["animate"] = uc.animate(spec)
    if a.stage in ("verify", "export", "all"):
        report["verify"] = uc.verify(spec)
        if not report["verify"]["ok"]:
            print(json.dumps(report, indent=2))
            sys.exit(1)
    if a.stage in ("export", "all"):
        report["export"] = uc.export(spec, a.out)
    if a.save_blend:
        os.makedirs(a.out, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(a.out, f"{spec['name']}.blend"))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

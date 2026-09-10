"""Headless entry point.

  blender --background --factory-startup --python build_character.py -- spec.json
  blender -b --python build_character.py -- spec.json --stages rig,mesh,skin
  blender -b --python build_character.py -- spec.json --sheets   (also render contact sheets)

Also works with the `bpy` wheel:  python build_character.py spec.json
Prints one JSON report line prefixed with PIPELINE_REPORT and exits 1 if any
gate failed, so CI can gate on it.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bpy  # noqa: E402
import char_lib as cl  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
if not argv:
    print(__doc__)
    sys.exit(2)
spec_path = os.path.abspath(argv[0])
stages = None
if "--stages" in argv:
    stages = argv[argv.index("--stages") + 1].split(",")
sheets = "--sheets" in argv

if not stages:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    report = cl.run_all(spec_path)
else:
    fns = {"preflight": cl.stage_preflight, "rig": cl.stage_rig,
           "mesh": cl.stage_mesh, "fit_mesh": cl.stage_fit_mesh,
           "skin": cl.stage_skin, "clips": cl.stage_clips,
           "verify": cl.stage_verify, "export": cl.stage_export,
           "roundtrip": cl.stage_roundtrip}
    report = {s: fns[s](spec_path) for s in stages}

if sheets:
    spec = cl.load_spec(spec_path)
    report["sheets"] = [cl.render_sheet(spec_path, None, view="three_quarter")]
    for c in spec.get("clips", []):
        if c["name"] in bpy.data.actions:
            report["sheets"].append(cl.render_sheet(spec_path, c["name"]))

blend_out = cl._abspath(cl.load_spec(spec_path),
                        os.path.join(cl.load_spec(spec_path).get(
                            "export_dir", "exports"),
                            f"{cl.load_spec(spec_path)['name']}.blend"))
bpy.ops.wm.save_as_mainfile(filepath=blend_out)
report["blend"] = blend_out

ok = all(v.get("ok", True) for v in report.values() if isinstance(v, dict))
print("PIPELINE_REPORT " + json.dumps(report, default=str))
sys.exit(0 if ok else 1)

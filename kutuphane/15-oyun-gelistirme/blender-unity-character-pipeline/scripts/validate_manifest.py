#!/usr/bin/env python3
"""Validate a <Name>.character.json and the files it references (no Blender
or Unity needed). Usage: python validate_manifest.py exports/Knight.character.json"""
import json
import os
import re
import sys

REQ = ["schema", "name", "rig_type", "height_m", "fps", "model", "clips", "unity_folder"]


def main(path):
    issues = []
    m = json.load(open(path, encoding="utf-8"))
    d = os.path.dirname(os.path.abspath(path))
    for k in REQ:
        if k not in m:
            issues.append(f"missing key: {k}")
    if m.get("rig_type") not in ("humanoid", "generic"):
        issues.append("rig_type must be humanoid|generic")
    if not str(m.get("unity_folder", "")).startswith("Assets/"):
        issues.append("unity_folder must start with Assets/")
    if not os.path.exists(os.path.join(d, m.get("model", ""))):
        issues.append(f"model file missing: {m.get('model')}")
    names = set()
    for c in m.get("clips", []):
        n = c.get("name", "")
        if n in names:
            issues.append(f"duplicate clip name {n}")
        names.add(n)
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", n):
            issues.append(f"clip name '{n}' not a valid Animator identifier")
        if c.get("file") != f"{m.get('name')}@{n}.fbx":
            issues.append(f"{n}: file should be {m.get('name')}@{n}.fbx")
        if not os.path.exists(os.path.join(d, c.get("file", ""))):
            issues.append(f"{n}: file missing")
        if c.get("frames", 0) <= 0:
            issues.append(f"{n}: frames must be > 0")
        for e in c.get("events", []):
            if not 0 <= e.get("frame", -1) <= c.get("frames", 0):
                issues.append(f"{n}: event {e} outside clip")
        if c.get("loop") and c.get("speed_mps", 0) < 0:
            issues.append(f"{n}: negative speed")
    loops = sorted(c.get("speed_mps", 0) for c in m.get("clips", []) if c.get("loop"))
    if len(loops) != len(set(loops)) and len(loops) > 1:
        issues.append("two looping clips share a speed -> blend tree thresholds collide")
    print(json.dumps({"ok": not issues, "issues": issues, "clips": sorted(names)}, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))

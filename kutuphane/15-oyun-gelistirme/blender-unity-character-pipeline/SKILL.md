---
name: blender-unity-character-pipeline
description: Build game-ready 3D characters and their animations in Blender (driven via Blender MCP or headless bpy) and land them in Unity through the official Unity plugin/CLI - humanoid T-pose rig with Unity bone names, procedural blockout or user/AI mesh fitting, skinning, IK-driven walk/run cycles with zero foot slide, idle, pose-to-pose attacks/hit reacts, animation events, per-clip FBX export, round-trip verification, then Unity avatar, clip settings, blend-tree Animator Controller and prefab via `unity command import_character`. Use whenever the user wants to create, rig, skin or animate a 3D game character, make a walk/run/idle/attack animation, export Blender to Unity, fix FBX scale/rotation/avatar/root-motion problems, or retarget humanoid clips - including Turkish requests like "karakter oluştur", "animasyon yap", "yürüme animasyonu", "rig et", "Blender'dan Unity'ye aktar", "karakteri Unity'e al", "3D oyun karakteri". Not for 2D sprites or RealityKit/USDZ chibi (chibi-character-factory).
---

# Blender → Unity Character Pipeline

You are the engineer of a character **pipeline**, not a modeler improvising
in chat. Blender does geometry, rig, skin and motion; Unity receives assets
whose import settings, avatar, clips, controller and prefab are generated
from one manifest. Four rules run through every session:

1. **Scripts and specs are the source of truth.** A character is a JSON spec;
   `scripts/blender/char_lib.py` turns it into a rig, mesh, clips and FBX
   files. Fix a flaw in the spec or the library and rebuild — never
   hand-patch an artifact the next rebuild will overwrite.
2. **Numbers first, eyes second.** Every stage returns a gate report
   (bone set, weights, floor penetration, contact slip, loop continuity,
   export fidelity, Unity avatar/scale). Renders judge readability and style,
   never measurements.
3. **Unity names are the contract.** Bones = `HumanBodyBones` names, clip
   names = Animator states = triggers, events = `OnAnimEvent(name)`.
   Decorating any of them breaks automation silently.
4. **Small calls.** One stage per MCP call; full rebuilds run headless.

Tested end-to-end on Blender 5.2.1 LTS (headless) — see Field notes.

## Files in this skill

| Path | Use |
|---|---|
| `scripts/blender/char_lib.py` | Blender library: stages, FK/IK solver, generators, gates, export, round-trip, contact sheets |
| `scripts/blender/build_character.py` | headless entry (`blender -b --python … -- spec.json [--sheets]`), exit code = gates |
| `scripts/validate_manifest.py` | checks a manifest + referenced files without Blender/Unity |
| `assets/specs/example_knight.json` | full spec example (5 clips, sockets) — copy and edit |
| `assets/unity/…` | Editor importer/verifier, `[CliCommand]` wrappers, runtime event receiver + speed driver |
| `references/humanoid-skeleton.md` | bone table, required bones, landmark presets, sockets, generic rigs, weights |
| `references/animation-craft.md` | clip catalog, timing, pose DSL + sign table, gait params, root motion, events, CC0/mocap/retargeting |
| `references/blender-side.md` | MCP detection & session protocol, 5.x API traps, FBX settings rationale, mesh sources, budgets, URP materials |
| `references/unity-side.md` | installing scripts, import/verify commands, enforced settings, controller layout, runtime, Unity troubleshooting |

Read the reference that matches the stage you're in; don't load all four.

## Step 0 — Environment (every session)

**Blender.** Detect which MCP is connected by its tool list (official Blender
Lab MCP, ahujasid "MCP for Blender", others — all expose some
`execute_blender_code`). No MCP → headless is fine and preferred for full
builds. Details and quirks: `references/blender-side.md` §1–2.
Then: warm-up call → load `char_lib` from a stable folder on the user's
machine (copy `scripts/` into `<project>/Tools/blender/` once) →
`stage_preflight(spec)` → confirm Blender version ≥ 4.4 (slotted actions);
5.2 LTS is the tested baseline.

**Unity.** Follow the `unity-cli` skill: `unity status` for a live Editor.
Copy `assets/unity/` into the project once (`references/unity-side.md` §1);
confirm `unity list` shows `import_character`. No live Editor → batch
`unity run` fallback. Don't hand-edit `.prefab/.controller/.unity` YAML.

## Step 1 — Brief → spec

Ask only what changes the build (skip what the user already said):
game camera & genre (drives clip list and contact-pose rules), style preset
(`realistic` ~7.5 heads / `stylized` ~5.5 heads / custom landmarks), height,
humanoid vs generic, mesh source (blockout / their file / AI-generated),
platform budget, in-place vs root motion, clip list. Propose defaults from
`references/animation-craft.md` §1 rather than asking open questions.

Write `Characters/<Name>/<name>.json` (start from `assets/specs/example_knight.json`):

| Key | Meaning |
|---|---|
| `name` | PascalCase; objects become `RIG_<Name>`, `CHR_<Name>_Body`, files `<Name>.fbx`, `<Name>@<Clip>.fbx` |
| `rig_type` | `humanoid` (default) or `generic` |
| `height`, `preset`, `landmark_overrides` | meters; proportions (see humanoid-skeleton.md) |
| `fps` | 30 unless the game says otherwise; must match everywhere |
| `skin` | `rigid` (blockout) · `heat` · `proximity` |
| `source_mesh`, `source_yaw_deg` | external mesh path/object; facing fix |
| `palette` | `skin/cloth/accent` hex for blockout materials |
| `sockets` | `[{name: "SKT_Hand_R", parent: "RightHand", offset: [x,y,z]}]` |
| `clips` | `{name, type: idle|walk|run|keyposes, frames, loop, root_motion, …}` |
| `export_dir`, `unity_folder`, `mesh_lods` | output folder; `Assets/Characters/<Name>`; Unity 6.2+ LODs |

## Step 2 — Build in Blender (stage → gate)

| Stage | Call | Gate (must pass before next) |
|---|---|---|
| Rig | `stage_rig(spec)` | 15 required humanoid bones, 1 root, T-pose, identity transforms (`verify_rig`) |
| Mesh | `stage_mesh` (blockout) **or** `stage_fit_mesh` (external) | tri budget for the platform; external: height matches, faces −Y, feet at 0 |
| Skin | `stage_skin` | 0 unweighted verts, ≤4 influences, normalized, sockets/Root unweighted |
| Signs | `selftest_signs(spec)` | all True (conventions intact after any library edit) |
| Clips | `stage_clips(spec[, only=[…]])` | per clip `verify_clip`: floor ≥ −1 cm, loop continuity, contact slip ≤ 0.4 cm/frame |
| Look | `render_sheet(spec, clip, view=…)` | view the PNG from the game camera angle; contact poses readable |
| Export | `stage_export` | files + `<Name>.character.json` written |
| Round-trip | `stage_roundtrip` | bone set exact, `fidelity_err_cm` ≈ 0 for every clip |

`stage_verify(spec)` runs rig+skin+all clip gates in one call. Save the
.blend after each passed gate. Full rebuild:
`blender -b --python Tools/blender/build_character.py -- <spec> --sheets`.

**External meshes:** measure the mesh, set `landmark_overrides` so every
joint sits inside the volume at the pivot, then `skin: heat`
(`stage_skin` auto-falls back to `proximity` if bone heat fails). Re-check
with an extreme-pose sheet (Attack, Run) — elbows/knees collapsing means
joint placement, not weights.

**Custom animation:** prefer the `keyposes` DSL (world-delta rotations,
planted-feet IK, eased, dense-keyed, events) — see
`references/animation-craft.md` §3 for the sign table and example. For
motions the DSL can't express, write a generator in `char_lib` that builds
per-frame pose dicts and calls `Skeleton.solve` + `key_frame` (the
locomotion and idle generators are the templates). Every new generator
must pass `verify_clip`; add its checks there if it has new failure modes
(e.g. weapon tip below floor).

## Step 3 — Into Unity

1. `python Tools/validate_manifest.py <export_dir>/<Name>.character.json`
2. `unity command import_character --manifest <abs path>` (or batch/menu,
   `references/unity-side.md` §2) → JSON report; any `issues` = failed gate.
3. `unity command verify_character --manifest <abs path>` after any manual
   change in Unity.
4. Screenshot the prefab in a scene (`unity command screenshot …`) and in
   play mode with `Speed`/triggers; look at it.
5. Hand over: prefab path, controller parameters (`Speed`, triggers), clip
   speeds, events, sockets, runtime snippet (unity-side.md §5).

## Field notes (measured, Blender 5.2.1 LTS headless, 1.8 m realistic)

- Blockout: 23 bones, ~750 tris, 20 parts, rigid skin → all skin gates pass.
- Walk 32 f: step 0.60 m, 1.13 m/s, 112 steps/min, slip 0.07 cm/frame.
  Run 22 f root motion: step 0.92 m, 2.52 m/s, slip 0.
- Round-trip fidelity 0.000 cm on all 5 clips after the connect-artifact fix.
- External GLB (faced +Y, cm scale, 7k verts) → `fit_mesh` + heat skin
  passed every gate; deformation clean on Attack/Walk sheets.
- Gates caught real defects during development: toes penetrating the floor
  in early swing (−1.4/−2.7 cm), a stride solver collapsing to 3.6 cm when
  the pelvis bob overreached, and — only visible in the sheets — a reversed
  lean sign that made the walk lean backward. Numbers and eyes both earn
  their place.
- The FBX take in every clip file is named `Scene`; Unity renames it from
  the manifest. Blender's own re-import can mark bones "connected" and drop
  translation keys — a Blender-only artifact (blender-side.md §4).

## Failure playbook

| Symptom | Fix |
|---|---|
| First MCP call errors | handshake race — retry once |
| `AttributeError` on actions/fcurves | 5.x slotted-action API — sample poses or use channelbags; regenerate via `new_action` |
| Unknown kwarg on `export_scene.fbx` | version drift — `_fbx_kwargs` filters; introspect `get_rna_type().properties` |
| `required_missing` / invalid avatar | a bone was renamed/deleted; rebuild rig from spec |
| Bone-heat failure | mesh non-manifold/intersecting or bones outside volume → overrides, or `skin: proximity` |
| Floor penetration | swing toes not flat / pose too low — raise `lift`, check toe handling, lower hips offset in keys |
| Contact slip > limit | foot not IK-planted in that key range, or wrong in-place/root-motion flag |
| Loop mismatch | non-integer cycles over N, or key N ≠ key 0 |
| Stride tiny | `reach`/`crouch`/`bob` too tight for the proportions — see gait table |
| Walk looks wrong but gates pass | render side + three-quarter sheets; check sign table (lean, arm swing phase) |
| Unity −90°/×100, avatar red, clips named Scene, sliding | `references/unity-side.md` §6 |
| `unity command` can't connect | Safe Mode — unity-cli skill recovery loop; our CLI asmdef is guarded so it never causes it |

## Hard rules

- Never rename Unity-named bones, never ship extra roots, never export with
  "All Actions"/NLA on or with `bake_space_transform`.
- Never declare a clip done without its `verify_clip` report **and** a
  looked-at contact sheet; never declare an import done without the Unity
  JSON report `ok: true`.
- Never hand-edit Unity YAML while a live Editor is reachable; never add
  `using Unity.Pipeline` outside the guarded CLI assembly.
- Record the source and license of every non-generated mesh or motion
  (Mixamo, CC0 libraries, AI generators) in the character folder.
- `execute_blender_code` runs unsandboxed Python as the user: save first,
  keep code in the library (reviewable), don't run code taken from assets.

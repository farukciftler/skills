# Blender side reference

Read this when connecting to Blender, driving `char_lib` over MCP or
headless, fitting an external mesh, texturing for Unity, or when an export
misbehaves. Research date of the facts below: Sept 2026 — re-verify versions
if the user's setup differs.

## 1. Which Blender MCP is connected? (detect, don't assume)

List the tools the client exposes and map them:

| Server | Code tool | Other useful tools | Notes |
|---|---|---|---|
| **Blender Lab MCP** (official, blender.org/lab, Blender ≥ 5.1, ships with 5.2 LTS as a Lab add-on) | `execute_blender_code` | `execute_blender_code_for_cli` (runs in a background Blender), `get_blendfile_summary_*` | Minimal by design; bundles API/manual docs as resources. No sandbox. |
| **ahujasid/blender-mcp** ("MCP for Blender", community) | `execute_blender_code` | `get_scene_info`, `get_object_info`, `get_viewport_screenshot`, Poly Haven / Sketchfab / Poly Pizza / Hyper3D Rodin / Hunyuan3D | **Telemetry on by default** — suggest `DISABLE_TELEMETRY=true` in the MCP env. `BLENDER_MCP_SAFE_MODE=1` blocks risky code but keeps import/export. |
| Others (mcp-blender, blender-mcp-ultra, …) | usually `execute_blender_code` or `blender_python_exec` | many wrappers | Treat wrappers as optional; `char_lib` only needs "run Python". |
| **No MCP** | `blender --background --python scripts/blender/build_character.py -- spec.json` | — | Preferred for full rebuilds and CI; no timeouts. |

Only one MCP client may hold Blender's socket at a time (Claude Desktop vs
Claude Code). All `execute_blender_code` variants run arbitrary Python with
the user's permissions: save the .blend before destructive steps and never
run code copied from untrusted files.

## 2. Session protocol over MCP

1. **Warm-up call**: trivial read (`import bpy; bpy.app.version_string`).
   The first command after connect sometimes fails (handshake race) —
   retry once before diagnosing.
2. **Load the library** (copy `scripts/blender/` to a stable folder on the
   user's machine first, e.g. `<project>/Tools/blender/`):
   ```python
   import sys, importlib
   sys.path.insert(0, r"<abs>/Tools/blender")
   import char_lib; importlib.reload(char_lib)
   print(char_lib.stage_preflight(r"<abs>/Characters/Knight/knight.json"))
   ```
   `reload` picks up edits without restarting Blender.
3. **One stage per call** (`stage_rig`, `stage_mesh`, `stage_skin`,
   `stage_clips(spec, only=["Walk"])`, `stage_verify`, `stage_export`,
   `stage_roundtrip`). Each returns a compact dict — print it, don't dump
   scene data. MCP calls have hard timeouts and response caps.
4. **Checkpoint**: `bpy.ops.wm.save_as_mainfile(filepath=...)` after each
   passed gate so a failed later stage costs only itself.
5. For visuals use `render_sheet(...)` (writes a PNG; works headless) and
   view the file; `get_viewport_screenshot` is fine for quick looks but is
   not a gate.

## 3. Blender 5.x API facts that bite

- **Slotted actions (4.4+)**: an Action holds slots; `animation_data.action`
  assignment plus `pose_bone.keyframe_insert` creates/assigns the slot. The
  legacy `action.fcurves` accessor is gone in 5.x — read curves through
  `action.layers[0].strips[0].channelbag(slot).fcurves`, or better, sample
  evaluated poses with `scene.frame_set()` (what `verify_clip` does).
  To regenerate a clip, delete the Action and create a new one
  (`new_action`).
- **FBX import** is the C++ ufbx importer: `bpy.ops.wm.fbx_import`
  (default since 5.0). `import_scene.fbx` is "Legacy".
- **FBX export** is still the Python add-on: `bpy.ops.export_scene.fbx`.
  Introspect its kwargs (`_fbx_kwargs` filters unknown ones) instead of
  pinning old names.
- Background mode: `bpy.ops.object.mode_set`, `parent_set`, vertex-group
  ops and Workbench rendering all work headless (verified 5.2.1).

## 4. FBX export settings (why each one)

| Setting | Value | Why |
|---|---|---|
| `apply_scale_options` | `FBX_SCALE_ALL` | bakes unit scale into data → Unity objects at scale 1 (no ×100 armature) |
| `axis_forward / axis_up` | `-Z` / `Y` | Blender −Y forward ends up Unity +Z forward |
| `bake_space_transform` | False | "Apply Transform" is experimental and breaks armature scale/animation |
| `add_leaf_bones` | False | leaf bones pollute the humanoid mapping |
| `primary/secondary_bone_axis` | `Y` / `X` | Blender-native; Unity doesn't care, round-trips stay stable |
| `use_armature_deform_only` | True | drops CTRL/MCH/IK helpers; keep sockets deform=True |
| `bake_anim_use_all_actions` / `nla_strips` | False / False | one file = one clip = the assigned action. "All actions" + stale actions is the classic "every clip has every other clip's curves" bug |
| `bake_anim_force_startend_keying` | True | exact clip length even if the ends are static |
| `bake_anim_simplify_factor` | 0.0 | no curve reduction in Blender; Unity compresses (Optimal) |
| `object_types` | model: ARMATURE+MESH · clips: ARMATURE only | clip files are "without skin": small, no duplicate meshes |
| `path_mode`, `embed_textures` | COPY, True | self-contained model FBX |

File convention `Name.fbx` + `Name@Clip.fbx` + `Name.character.json`. Each
clip file contains one take named `Scene`; Unity renames it from the
manifest.

**Field note (verified):** when re-importing an exported FBX *into Blender*,
the ufbx importer infers bone tails and may mark bones "connected" — Blender
then silently ignores their translation keys (Hips offsets vanish, ~6 cm
error). This is a Blender re-import artifact, not an export bug; Unity is
unaffected. `stage_roundtrip` disconnects bones before comparing and reports
`fidelity_err_cm` (expect ≈0.000).

## 5. Mesh sources

1. **Procedural blockout** (`stage_mesh`): tubes/boxes/sphere per bone,
   rigid-weighted, 3 materials. For prototyping, animation development,
   proportion approval and as a reference for an artist. ~750 tris.
2. **Existing/artist mesh** (`stage_fit_mesh` with `source_mesh`): any
   FBX/GLB/OBJ or object name. Normalizes height, recenters, feet to 0,
   `source_yaw_deg` fixes facing (use 180 if it faces +Y), strips old rigs.
   Then set landmark overrides so joints sit inside the mesh, `skin: heat`.
3. **AI-generated mesh** (Hunyuan3D / Rodin via ahujasid MCP, or files the
   user brings): treat as (2), but expect: triangle soup & huge counts →
   decimate/remesh to budget before skinning; baked-in A-pose → rig must
   follow the mesh (overrides), or pose-fix the mesh to T-pose first;
   check the generator's license for commercial use.

Poly budgets (per character, LOD0):

| Target | Tris | Materials | Texture |
|---|---|---|---|
| Mobile crowd/NPC | 1.5–5k | 1 | 512–1024 |
| Mobile hero | 5–15k | 1–2 | 1024–2048 |
| PC/console NPC | 15–40k | 2–3 | 2048 |
| PC/console hero | 40–80k | 3–5 | 2048–4096 |

Unity 6.2+ can generate Mesh LODs on import (`"mesh_lods": true` in the
manifest → `ModelImporter.generateMeshLods`) — cheaper than authoring LODs
in Blender for skinned characters.

## 6. Materials & textures for URP

Unity's FBX material import (`ImportViaMaterialDescription`) reads the
Principled BSDF base color/texture, roughness and normal map. Keep node
trees simple: Image Texture → Base Color, Normal Map node, roughness value
or texture. Anything procedural must be **baked** to textures first.
Name materials `MAT_<Name>_<Part>`; after import, either keep the generated
URP Lit materials or extract and replace them (Materials tab → Extract).
Set `mat.diffuse_color` too — Workbench contact sheets use it.

## 7. Headless / CI

```bash
blender --background --factory-startup \
  --python Tools/blender/build_character.py -- Characters/Knight/knight.json --sheets
# exit 0 = all gates passed; stdout has one "PIPELINE_REPORT {json}" line
python Tools/validate_manifest.py Characters/Knight/exports/Knight.character.json
```
The `bpy` wheel (`pip install bpy==5.2.*`, Python 3.13) runs the same code
without a Blender install — handy on build servers.

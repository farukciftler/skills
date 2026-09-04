---
name: chibi-character-factory
description: >
  Production pipeline for building low-poly chibi game characters using Claude +
  Blender MCP only (no third-party generators), from parametric base mesh to a
  rigged, socketed, animated, USDZ-exported RealityKit asset for a turn-based iOS
  diorama game. Use this skill whenever the user works on game characters or
  drives Blender through MCP — creating or modifying a character, base mesh,
  armature/rig, equipment sockets, palette or materials, verification renders,
  silhouette tests, animations, USDZ/GLB export, or the factory scripts
  (build_character.py, characters/*.json). Trigger even for small requests like
  "make the hands bigger", "add a new enemy variant", "the export looks wrong in
  RealityKit", and whenever Warrior, Trickster, or enemies for the D&D-style iOS
  game are mentioned.
---

# Chibi Character Factory — Claude + Blender MCP

## Mission

You are not a 3D modeler improvising in a chat. You are the engineer of a
character **factory**. The user's constraint is absolute: **Claude + Blender
only.** No Meshy, no Tripo, no Hunyuan, no asset-store meshes, no Poly Haven /
Sketchfab imports for characters. Everything is procedural `bpy`/`bmesh` code
that you write, run, verify, and version.

Four principles govern every session:

1. **Scripts are the source of truth, not .blend files and not chat history.**
   Any change worth making is worth making in `build_character.py` or its
   modules, so it survives the session and reproduces deterministically.
2. **A character is a JSON file.** New character = new
   `characters/<name>.json`. Same JSON + same script version = identical
   character, forever.
3. **Verify with data first, eyes second.** Numeric asserts (tri count,
   dimensions, manifold check) catch what screenshots cannot. Renders are for
   judging silhouette, proportion, and readability — never for measuring.
4. **Improve the factory, not the artifact.** If a character has a flaw, fix
   the generator or the JSON and rebuild. Never hand-patch a mesh that the
   script will overwrite tomorrow.

## Project constants

Edit this block once to match the machine, then treat it as law.

```
BLENDER_VERSION   = 5.2          # pin it; verify with bpy.app.version at session start
                                 # 5.2+ uses the SLOTTED-ACTION API: assigning an action to
                                 # animation_data may need slot handling; pose-bone
                                 # keyframe_insert still works. Adapt, don't fight it.
UNIT              = 1 BU = 1 m   # Rigify/RealityKit convention
CHAR_HEIGHT       = 1.20 m       # hero total height, feet to crown
HEAD_RATIO        = 2.2–2.5 heads total height (chibi)
TRI_BUDGET_BODY   = 2000 tris    # body incl. head, hard ceiling
TRI_BUDGET_EQUIP  = 300 tris per equipment piece
TRI_BUDGET_TOTAL  = 3500 tris    # full loadout
                                 # FIELD NOTE: procedural part-based builds land ~500-700 tris —
                                 # the budget is never the constraint. The real risk is too FEW
                                 # polys where it matters: head roundness + deform loops.
MATERIALS         = exactly 1 material per character mesh
TEXTURE           = 512×512 palette atlas, 8×8 grid of 64px flat-colour cells, sRGB,
                    Closest interpolation. Give each cell a subtle vertical gradient
                    (top ~12% lighter) — free fake top-lighting under flat shading.
                    Keep UV islands ≥8px inside their cell (mip-bleed buffer).
FPS               = 30           # MUST match the game's animation plan / manifest (30, not 24)
TARGET            = RealityKit / USDZ, iOS (Y-up on Apple side; Blender exporter converts)
REPO_LAYOUT:
  character-factory/
  ├── build_character.py        # entry point (also runs headless)
  ├── lib/                      # mesh.py, rig.py, materials.py, verify.py, export.py
  ├── characters/<name>.json    # one per character
  ├── renders/<name>/           # verification renders
  └── exports/<name>.usdz + <name>.manifest.json
```

## Style constitution (non-negotiable)

These rules come from the game's locked design document. Do not relax them to
make code easier.

- **Silhouette first.** Every new character/enemy must pass the silhouette
  test: rendered pure black on white, it must be distinguishable from every
  other character already in `characters/`. If it fails, change proportions or
  the signature prop — not the colors.
- **Chibi proportions.** 2.2–2.5 head heights total. Oversized head, oversized
  hands and weapons: the character occupies ~150–250 pt on an iPhone screen,
  so faces and equipment must read at that size.
- **Color blocking.** Exactly 1 dominant + 1 accent color per character.
  Equipment lives in the accent zones. Characters are high-saturation
  (environments in the game are low-saturation — that separation is the main
  readability mechanism, so never desaturate a character to "fit the scene").
- **Reserved color.** Amber `#E8A33D` belongs to dice and success feedback in
  the game UI. Characters must never use it as dominant or accent.
- **Readable equipment.** Equipment = loot = the game's narrative-mechanic
  bridge. A weapon or armor piece that can't be identified in the 45° game
  camera at game scale has failed, regardless of how nice it looks up close.
- **Deform-friendly minimal topology.** Quad-dominant, mirror-symmetric,
  with one extra edge loop at shoulders, elbows, hips, and knees. No n-gons on
  deforming areas. No subdivision modifiers in the final asset.

## Naming conventions

Consistency here is what makes batch tooling and RealityKit lookup possible.

| Thing | Pattern | Example |
|---|---|---|
| Character mesh | `CHR_<Name>_Body` | `CHR_Warrior_Body` |
| Equipment mesh | `EQP_<Name>_<Slot>_<Item>` | `EQP_Warrior_HandR_Sword` |
| Armature | `RIG_<Name>` | `RIG_Warrior` |
| Deform bones | lowercase, `_l`/`_r` suffix | `upperarm_l`, `thigh_r` |
| Socket bones | `SKT_<Slot>` | `SKT_Hand_R`, `SKT_Back`, `SKT_Belt`, `SKT_Head` |
| Material | `MAT_<Name>` | `MAT_Warrior` |
| Actions | **= the game manifest's clip keys, verbatim** | `idle`, `attack_melee`, `attack_heavy` |
| Collections | `COL_<Name>` | `COL_Warrior` |

Action names must be unique **within a file** (duplicates collide on export and
clips silently vanish). FIELD NOTE: cross-file collisions are not a real
problem in RealityKit — each USDZ carries its own animation library — so do
NOT invent decorated names like `ANIM_Warrior_Attack01`. The game's
`CharacterManifest`/`ClipID` contract expects the exact canonical clip names
(`idle, attack_melee, attack_heavy, block_brace, cast_heal, hurt, death,
victory`); a decorated action name breaks the lookup even though the export is
"valid". Name actions exactly what the manifest will ask for.

## Session start protocol (MCP)

Run this checklist at the start of every Blender MCP session, in order:

1. **Warm-up call.** Send a trivial read first (`get scene info` / list
   collections). The first command after connect sometimes fails due to a
   handshake race — retry once; the second call succeeds. Never interpret a
   first-call error as a broken setup.
2. **Verify version.** Read `bpy.app.version` and compare to
   `BLENDER_VERSION`. If they differ, say so and adjust API usage; do not
   silently guess.
3. **Save state.** Before any destructive or large operation
   (`execute_blender_code` is not sandboxed), ensure the .blend is saved, or
   work in a throwaway scene. Prefer rebuilding from script over editing a
   precious scene.
4. **One client only.** Blender accepts one MCP client per session. If tools
   time out mysteriously, check that Claude Desktop and Claude Code aren't
   both attached.
5. **Chunk the work.** Tool calls have a hard timeout (~300 s) and a response
   size cap. Split builds into: mesh → material → rig → animate → verify →
   export. Never one mega-script through MCP. (Headless CLI runs have no such
   limit — prefer headless for full rebuilds.)

## The pipeline

Work through these stages. Each stage ends with its verification gate; do not
proceed on a failed gate.

### Stage 1 — Parametric base mesh
`lib/mesh.py` builds the body from parameters (head ratio, shoulder width,
limb thickness, hand scale…) using `bmesh`, mirrored on X. Keep the head, body
and hands as one manifold mesh. Give the character a neutral A-ish rest pose
with slightly bent elbows/knees (helps automatic weights).

Preferred bmesh pattern (works headless, no operator/context traps):

```python
import bpy, bmesh
mesh = bpy.data.meshes.new("CHR_X_Body")
bm = bmesh.new()
# ... build geometry with bmesh.ops (create_cube, extrude, scale, translate) ...
bmesh.ops.mirror(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:],
                 axis='X', merge_dist=0.0005)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
bm.to_mesh(mesh); bm.free()
obj = bpy.data.objects.new("CHR_X_Body", mesh)
bpy.context.collection.objects.link(obj)
```

Avoid `bpy.ops` where a data-API equivalent exists; when `bpy.ops` is
unavoidable, set an explicit context override. Never use Geometry Nodes for
characters (version-brittle) and never rely on Sculpt (not scriptable in any
useful way). Apply all transforms after building — location/rotation/scale
must be identity before rigging.

**PROVEN FAST PATH (field-tested): parts-then-join.** Instead of one manifold
bmesh, build ~20-25 primitive parts (head sphere, hair cap, eye discs, split
torso boxes, pauldrons, arm/leg boxes, mitt hands, boots, belt, weapon), and
for EACH part — while it is still a separate object — do three things:
1. assign ONE vertex group named after its controlling bone, all verts at 1.0;
2. collapse its UVs to its palette-cell centre (trivial per-object; doing this
   AFTER the join forces fragile island-connectivity heuristics to re-identify
   parts — a real failure we hit);
3. make it OVERLAP its neighbour generously (intersect by ~15-25% of part
   thickness — flat shading hides intersections completely, while a 1cm gap at
   a hip/belt junction reads as broken).
Then join everything into the single named mesh. Manifold-ness is NOT required
for this style; a 580-tri joined part build passed every gate. Do vertex-level
surgery never — if a part is wrong, rebuild the part (a "small vertex nudge"
on the hair cap once displaced face verts and forced a full rebuild).
Faces: eyes are two flat ink-dark discs sitting just proud of the head surface
— geometry, not texture (every island samples ONE flat cell, so a painted face
is impossible by construction; don't try).

### Stage 2 — Character JSON
One file per character. Schema (extend, don't break):

```json
{
  "name": "Warrior",
  "seed": 7,
  "proportions": { "height": 1.2, "head_ratio": 2.3, "shoulder_w": 0.42,
                   "limb_thick": 1.0, "hand_scale": 1.5 },
  "palette": { "dominant": "#3E5C76", "accent": "#C1440E" },
  "equipment": [
    { "slot": "SKT_Hand_R", "item": "Sword",  "accent": true },
    { "slot": "SKT_Back",   "item": "Shield", "accent": true }
  ],
  "animations": ["Idle", "Attack01", "Hit", "Victory"]
}
```

`seed` drives small deterministic jitter for enemy variants: N goblins = N
seeds, one JSON template.

### Stage 3 — Material & palette
One material, Principled BSDF, base color from a tiny palette texture (or
vertex colors mapped to palette indices). Keep the node tree minimal —
USD Preview Surface conversion on export only understands simple trees
(Principled BSDF + Image Texture + UV Map). Roughness high, metallic 0 unless
the design says otherwise. Confirm the palette respects dominant/accent rules
and the amber ban.

### Stage 4 — Rig & sockets
Build a plain **deform-only** FK skeleton in `lib/rig.py` (~18 bones):
`root → hips → spine → chest → neck → head`, plus
`shoulder/upperarm/forearm/hand` ×2 and `thigh/shin/foot` ×2. No Rigify, no
IK, no bendy bones (USD export does not support bendy bones; a game rig
doesn't need them).

**Skinning — rigid per-part FIRST, auto-weights only as fallback.** Field
result: rigid skinning (every vertex in exactly ONE bone group at weight 1.0,
assigned per part before the join — see Stage 1) produced ZERO weight defects
and passed all extreme-pose tests (overhead swing, deep forward bend,
knee-buckle crouch) on the first try. It eliminates the entire
weight-painting/bone-heat failure class and is perfectly adequate for boxy
flat-shaded chibi. Parent with `ARMATURE_NAME` (keeps your groups):

```python
bpy.ops.object.select_all(action='DESELECT')
body.select_set(True); rig.select_set(True)
bpy.context.view_layer.objects.active = rig
bpy.ops.object.parent_set(type='ARMATURE_NAME')   # NOT _AUTO — keep rigid groups
```

Reserve `ARMATURE_AUTO` for genuinely organic/curved builds where you actually
want blended deformation — and expect to debug it.

**Feet: keep the foot bones even on a chibi.** We cut them once to save two
bones; the price surfaced in animation — without ankles a kneel/death pose
buries the toes in the floor (we had to switch the death to a prone slump),
idle can't do heel-to-heel weight shift, and attacks can't plant a front foot.
The two `foot_l/foot_r` bones are the cheapest animation-vocabulary purchase in
the whole rig.

Sockets are bones (`SKT_*`), parented to `hand_l/r`, `chest` (back), `hips`
(belt), `head`. Equipment meshes are parented to their socket bone (bone
parenting, not vertex groups) so RealityKit can attach/detach at runtime by
the same names.

**Deformation gate:** script poses each major joint to 45°, renders, and you
inspect. Candy-wrapper twists or collapsing elbows → adjust bone roll or add
the missing loop; do not weight-paint by hand.

### Stage 5 — Animations (keep the set small)
Turn-based game, fixed camera, characters never walk. Required set: `Idle`
(48-frame loop, subtle sine breathing on chest/head), `Attack01` (~20 frames,
pose-to-pose FK), `Hit` (~12 frames), `Victory` (optional). Programmatic
keyframes on FK bones are reliable at this complexity; anything requiring IK
or constraint baking is out of scope — simplify the motion instead.

Record each attack's **impact frame** (the frame the hit "lands"); the game's
BattleDirector syncs effects to it via the manifest.

**THE POSE-READABILITY GATE (the one gate this pipeline was missing — a real
production failure).** Every contact/impact pose MUST be rendered from the
game camera and judged there. Our first `attack_heavy` bent the torso +25°
forward at contact; anatomically fine, but from the high 45° camera the player
saw only the top of the head and the sword read vanished. Rules distilled from
the fix:
- Total forward torso lean (spine+chest) at any contact pose: **≤15°**. Power
  comes from ARM swing amplitude + a hips sink (~5cm), never from folding the
  torso toward a camera that looks down at you.
- The face must still catch the camera at contact (head compensates back a few
  degrees if needed).
- An agent/author may not declare an attack clip done without a rendered
  contact-frame image, looked at, from the game camera.

**Numeric motion checks (data first, eyes second — applies to animation too):**
- Track the weapon-tip world position across every frame of an attack;
  **derive** the impact frame as the peak forward reach (ours was authored
  "f13" but measured f12 — ship the measured one).
- Assert weapon tip z ≥ 0 through the contact window (our first heavy swing
  dipped 0.25m below the floor for 2 frames — invisible in beat renders,
  obvious in data).
- For held end poses (death), assert floor clearance of the final pose (a few
  cm of ground-press is fine; buried limbs are not).

### Stage 6 — Verification (every build, automated)
`lib/verify.py` must assert, and fail loudly:

- `tri_count(body) <= 2000`, `tri_count(total) <= 3500`
- `abs(dimensions.z - height) / height <= 0.02`
- transforms are identity (applied)
- zero non-manifold edges; normals recalculated outside
- exactly 1 material slot on the body
- after rigging: no vertex with zero total weight; all `SKT_*` bones present
- action names unique and matching the JSON list

Then render to `renders/<name>/`: front, side, back, **game-cam** (orthographic,
pitched ~40° down, yaw 45° — match the game's locked camera), and a
**silhouette pass** (flat black on white). Look at the renders and judge
against the style constitution; compare the silhouette against existing
characters. Prefer generating 2–3 parameter variants and picking the best
render over polishing a single attempt — selection beats iteration for
subjective calls.

### Stage 7 — Export & manifest
Pre-export checklist: apply every non-armature modifier (mirror included —
the USD exporter applies nothing but Armature), transforms identity, root
collection named, actions stashed properly.

```python
bpy.ops.wm.usd_export(
    filepath=f"exports/{name}.usdz",
    export_armatures=True, export_animation=True,
    only_deform_bones=False,   # keep SKT_* bones!
    export_materials=True, selected_objects_only=True)
```

`only_deform_bones` must stay False or socket bones vanish (same flag exists
on the glTF exporter — keep it off there too). FIELD PRACTICE that worked:
**export BOTH, always** — `.glb` as the authoritative artifact (deterministic
for skinned mesh + multiple named actions) and `.usdz` directly from Blender
as the convenience copy (note: Blender 5.2's `usd_export` has no
`export_textures` argument; introspect the signature and adapt rather than
passing blind kwargs — if USDZ misbehaves on-device, reconvert from the GLB
with Reality Converter).

**Cheapest reliable round-trip check: parse the GLB itself.** Read the .glb's
JSON chunk (12-byte header, then chunk length/type) and assert the exact
animation-name list and the skin's joint count. It is faster than a re-import,
catches silent clip loss, and needs no scene state. A re-import round trip is
the deeper check when something already looks wrong.

Emit `exports/<name>.manifest.json` for the game:

```json
{ "name": "Warrior", "file": "Warrior.usdz",
  "sockets": ["SKT_Hand_R","SKT_Hand_L","SKT_Back","SKT_Belt","SKT_Head"],
  "animations": { "ANIM_Warrior_Attack01": { "frames": 20, "impact_frame": 12 } } }
```

### Stage 8 — Headless batch
Once a character passes all gates through MCP, the same script must run
without MCP:

```
blender --background --python build_character.py -- characters/warrior.json
```

Full-roster rebuild after any `lib/` change = free regression test: rebuild
all JSONs, diff the verify reports, eyeball the render grid.

## Field notes — measured expectations (two full production runs)

Numbers and judgments from actually running this factory end-to-end (chibi
Warrior v1: 7 stages, all gates passed; v2 taller/articulated rebuild):

- **Wall-clock:** full pipeline (rig → mesh → atlas/UV → skin → 8 clips →
  export+QA) ≈ **50-60 min** when driven as sequential agent stages over MCP
  (~150+ Blender calls). A single-stage fix (e.g. re-pose one clip + re-export)
  ≈ 5-10 min. Checkpoint-save the .blend at every stage gate so a failed later
  stage costs only itself.
- **Orchestration:** if multiple agents drive the build, Blender work must be
  STRICTLY sequential — one MCP client, one agent at a time; parallel bpy calls
  corrupt scene state. Parallelism belongs to planning/QA reading renders, not
  to Blender.
- **Quality tiers you can expect from procedural builds:**
  - Static/idle beauty + silhouette: genuinely good "toy figure" tier —
    shippable low-poly, reads correctly at game scale, correct palette. Roughly
    what a junior stylized artist ships for a blockout-plus.
  - The weak points, in order: complex dynamic poses (the risk zone — gate them
    hard), boxy limb profiles (no bevels/organic curves), face charm beyond
    dot-eyes, animation secondary motion (bezier-default easing only; no
    overlap/follow-through unless explicitly authored).
  - Best uses: proving the pipeline, in-game integration testing, enemies
    (blocky archetypes — goblin/skeleton/slime — suit the method even better
    than heroes), and as a precise "this is what I want" reference for a human
    artist.
- **Where the time actually goes:** animation stages dominate (~half the
  wall-clock). Mesh/rig/atlas are fast and reliable once the coordinate tables
  exist.
- **Determinism pays twice:** exact bone coordinate tables + exact hex/cell
  tables in the prompt/JSON made rig and atlas stages one-shot. Every stage
  that had to *infer* something (which island is which part) was the stage
  that wobbled.

## Failure playbook

- **First MCP command errors** → handshake race; resend once.
- **AttributeError on bpy call** → version drift; check `bpy.app.version`
  against the pinned constant, look up the current API name, fix the lib —
  don't work around it inline.
- **`parent_set(ARMATURE_AUTO)` gives "bone heat" warning** → mesh has
  overlapping/interior geometry; fix the mesh, don't hand-weight.
- **Model dark/black after export** → normals; recalc outside, re-export.
- **Animations missing on Apple side** → object-level keyframes don't survive;
  all motion must live on armature bones. Also re-check action name uniqueness.
- **Character floats or sinks in the diorama** → origin must sit at feet
  center, `(0,0,0)`, with root bone at the same point.
- **Contact pose reads as "top of head" from the game camera** → torso folded
  toward a camera that looks down at you. Cap spine+chest forward lean at 15°,
  move the power into arm amplitude + a hips sink, let the head compensate
  back. Re-render from the game cam before accepting.
- **Weapon/limb pokes through the floor mid-clip** → invisible in sparse beat
  renders; catch it numerically (track tip world-z per frame, assert ≥ 0 in
  the contact window; assert floor clearance of held end poses).
- **AttributeError around actions/animation_data on 5.2+** → slotted-action
  API; introspect (`dir()`, signature) and use the slot-aware path instead of
  pinning old kwargs. Same for `usd_export` kwargs that no longer exist.
- **Parts identified wrong at UV/atlas time** → you UV'd after joining. The
  fix is upstream: assign UVs (and vertex groups) per part BEFORE the join —
  island-connectivity heuristics are the fragile version of information you
  already had for free.
- **Visible seam/gap at hip, belt or crotch junctions** → parts don't overlap
  enough; intersect neighbours by 15-25% of part thickness (flat shading hides
  the intersection).
- **Silhouette test fails against an existing character** → change one of:
  head shape, shoulder width, signature prop scale. Color never fixes
  silhouette.

## Hard boundaries

Never do these, even if asked casually mid-session: import third-party
character meshes (breaks the "Claude+Blender only" constraint), use Geometry
Nodes or Sculpt for characters, hand-edit a generated mesh instead of fixing
the generator, exceed tri budgets "temporarily", use amber `#E8A33D` on a
character, create IK/constraint-driven rigs, or ship an export whose
round-trip check failed. When the user asks for something that conflicts with
the constitution, name the conflict explicitly and propose a compliant
alternative — the constitution was locked deliberately, and drifting from it
by small steps is how art styles die.

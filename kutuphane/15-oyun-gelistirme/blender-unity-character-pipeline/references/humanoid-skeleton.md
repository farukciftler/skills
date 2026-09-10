# Humanoid skeleton reference

Read this when building or editing a rig, adding bones (fingers, sockets,
jaw), fitting a custom mesh, or when Unity reports an invalid avatar.

## Why the bone names are Unity's names

`char_lib` names every deform bone exactly like `UnityEngine.HumanBodyBones`
(`Hips`, `LeftUpperArm`, …). Unity's humanoid auto-mapper then matches 100%
of bones on first import — no manual Avatar Configure step, no `.ht` template,
no `HumanDescription` scripting. Keep it that way: renaming bones to
`upperarm.L` style buys nothing in Unity and costs a manual mapping pass.

## Hierarchy (23 bones, default)

```
Root                      (non-human; origin at feet; carries root motion)
└─ Hips
   ├─ Spine ─ Chest ─ UpperChest ─┬─ Neck ─ Head
   │                              ├─ LeftShoulder ─ LeftUpperArm ─ LeftLowerArm ─ LeftHand
   │                              └─ RightShoulder ─ RightUpperArm ─ RightLowerArm ─ RightHand
   ├─ LeftUpperLeg ─ LeftLowerLeg ─ LeftFoot ─ LeftToes
   └─ RightUpperLeg ─ RightLowerLeg ─ RightFoot ─ RightToes
```

| Unity requirement | Bones |
|---|---|
| **Required (15)** — avatar invalid without them | Hips, Spine, Head, Left/Right UpperLeg, LowerLeg, Foot, Left/Right UpperArm, LowerArm, Hand |
| Optional, included | Chest, UpperChest, Neck, Left/Right Shoulder, Left/Right Toes |
| Optional, add when needed | Jaw, LeftEye/RightEye, finger phalanges (`LeftThumbProximal`, `LeftIndexIntermediate`, … 3 per finger) |

Toes are worth keeping: Unity uses them for tiptoe and better foot IK. Chest
and shoulders matter for believable arm raises; without shoulders an overhead
swing looks robotic.

## Rest pose rules

- **T-pose**, arms horizontal (verify_rig tolerates ≤10°), legs vertical,
  palms down. Unity builds its muscle space from the rest pose; an A-pose rig
  imports but warns "Character not in T-Pose" and retargeting quality drops.
- Feet flat on Z=0, origin between the feet, character facing **−Y**.
- Object transforms identity (location 0, rotation 0, scale 1) on rig and
  mesh. `stage_fit_mesh` bakes everything into mesh data.
- One root bone only. Multiple roots → Unity "more than one bone at the top
  level" error.
- Bone rolls: `char_lib` aligns bone Z toward character forward. Unity does
  not require specific rolls, but consistent rolls make hand-authored poses
  predictable.

## Landmark presets (fractions of height H)

`joint_table(height, preset, overrides)` places joints from these landmarks.
Override any key per character in the spec (`"landmark_overrides": {...}`).

| key | realistic (~7.5 heads) | stylized (~5.5 heads) | meaning |
|---|---|---|---|
| ankle_z | .045 | .05 | ankle joint height |
| knee_z | .285 | .26 | knee |
| hip_z / hip_x | .525 / .055 | .49 / .065 | hip joint height / lateral offset |
| pelvis_z | .545 | .51 | Hips bone head |
| spine_z, chest_z, upchest_z | .60, .68, .76 | .565, .63, .695 | spine segments |
| neck_z, head_z, top_z | .83, .87, .995 | .755, .785, .995 | neck base, skull base, crown |
| sh_z, sh_x | .815, .10 | .735, .10 | shoulder joint |
| elbow_x, wrist_x, hand_x | .27, .41, .50 | .245, .37, .465 | arm span ≈ H (realistic) |
| ball_y, toe_y, heel_y | .10, .145, .035 | .11, .16, .04 | foot geometry |

For chibi (2–3 heads) use the `chibi-character-factory` skill instead (RealityKit
target) or define a new preset — the IK locomotion still works, but reach
limits make strides short, which is correct for chibi.

When fitting an existing mesh: first measure it (joint positions from the
mesh's silhouette: crotch height → hip_z, knee bulge, armpit → sh_z, wrist),
then pass overrides so bones sit **inside** the mesh at the joint pivots.
Bones outside the volume are the #1 cause of bone-heat failure.

## Extra bones — naming contract

| Prefix | Purpose | Deform? | Exported? |
|---|---|---|---|
| (Unity names) | skeleton | yes | yes |
| `SKT_<Slot>` (e.g. `SKT_Hand_R`, `SKT_Back`) | equipment sockets, parented to Hand/Chest/Hips | **set `use_deform=True` with no weights** so `use_armature_deform_only` keeps them | yes — Unity sees them as extra (non-human) transforms; attach weapons there |
| `CTRL_*`, `MCH_*`, `IK_*` | authoring helpers (IK targets, poles) | no | **no** (dropped by deform-only export) — bake to FK first |
| `Twist_*`, `Corrective_*` | extra deformers | yes | yes — humanoid ignores them for retargeting (they won't animate on retargeted clips unless driven in Unity) |

Humanoid retargeting only transfers human bones. Anything non-human animates
only when the clip was made on the *same* skeleton (or via Generic rig).

## Generic rigs (creatures, quadrupeds, props)

Set `"rig_type": "generic"` in the spec when the character is not a biped
humanoid or when you need exact bone-level playback (no muscle-space
retargeting). Differences:
- Unity avatar is Generic; root motion comes from the `Root` bone
  (`CharacterImporter` sets `motionNodeName` to its transform path).
- Clips are not shareable across different skeletons.
- `char_lib`'s rig/locomotion generators are biped-only. For a quadruped,
  build the armature with the same pattern (`Root` → pelvis → spine chain,
  4 legs), reuse `Skeleton.solve` + `two_bone_ik` per leg, and use a gait
  phase table (walk: LH 0, LF .25, RH .5, RF .75; trot: diagonal pairs).

## Weights

- Unity default is 4 influences per vertex; `stage_skin` limits to 4 and
  normalizes. If you need 8+ (faces), raise both Blender limit and
  `ModelImporter.skinWeights`, and Quality settings.
- `rigid` mode (blockout) = zero weight defects; `heat` = Blender bone heat
  (smooth, can fail on non-manifold/intersecting meshes); `proximity` =
  deterministic distance weights, never fails, slightly blobby at elbows —
  good fallback, refine by hand if the character is a hero asset.

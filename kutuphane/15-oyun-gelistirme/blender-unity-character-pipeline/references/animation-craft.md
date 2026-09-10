# Animation craft reference

Read this before authoring or tuning any clip: which clips a game needs,
timing, the pose DSL and its sign conventions, locomotion math, root motion,
events, and where to get motion that `char_lib` can't generate.

## 1. Clip catalog — decide the list with the user first

| Game type | Minimum set | Nice to have |
|---|---|---|
| Third-person action/adventure | Idle, Walk, Run, Jump(Start/Loop/Land), Attack×2–3, Hit, Death | Sprint, Strafe L/R, Turn-in-place, Roll/Dodge, Block |
| Top-down / isometric RPG | Idle, Walk, Run, Attack, Cast, Hit, Death | Idle_Break, Victory, Interact |
| Turn-based / tactics | Idle, Attack_Melee, Attack_Heavy, Cast, Block, Hit, Death, Victory | Walk (short grid moves) |
| Mobile runner | Run, Jump, Slide, Hit/Stumble, Death | Turn L/R |
| Crowd / NPC | Idle (2 variants), Walk, Talk gesture | Sit, Point |

Naming: PascalCase clip names = Animator state names = trigger names
(`Attack`, `Hit`) — validate_manifest.py rejects names that are not valid
Animator identifiers. Clip names are the contract with gameplay code; never
decorate them (`ANIM_Knight_Attack01`).

## 2. Timing table (30 fps, adult human, game-readable)

| Clip | Frames | Notes |
|---|---|---|
| Idle | 60–120, loop | breathing 2 cycles; any motion must be periodic over N |
| Walk | 30–34, loop | 2 steps per cycle; cadence ~105–115 steps/min |
| Run (jog) | 20–24, loop | cadence ~160–175; flight phase (duty < .5) |
| Sprint | 16–18, loop | lean 12–15°, duty ~.30 |
| Attack (light) | 18–28 | anticipation 30–40% · contact 1–2 frames · recovery ≥40% |
| Attack (heavy) | 30–45 | longer anticipation; hips sink ≤ 5 cm at contact |
| Hit react | 12–20 | 3–5 frame snap, slow settle |
| Death | 40–70 | end in a held pose; floor-clearance gate on final frame |
| Jump start / land | 8–12 / 10–16 | land: absorb with knees, 2–3 frame compression |

Game feel: shorter anticipation = more responsive; the gameplay hit window
comes from the `Hit` event, not from the clip length.

## 3. Pose DSL (keyposes generator) and sign conventions

Rotations are **world-delta**: rotation about armature axes applied to the
bone about its head, **after** its parents moved. Arms start from a lowered
neutral (74° down from T-pose, slight elbow bend) — a key's arm rotation is
applied on top of that neutral. Axes: X = character's left, −Y = forward,
Z = up. Verified by `selftest_signs()` on every run:

| Bone | Axis+sign | Effect |
|---|---|---|
| Leg / lowered arm (points down) | X− | swings forward |
| LowerLeg | X+ | knee bend |
| LowerArm (lowered) | X− | elbow bends forward |
| LeftUpperArm from T-pose | Y+ | lowers · RightUpperArm: Y− lowers |
| Up-pointing bones (Hips, Spine, Chest, Neck, Head) | X+ | bend forward · X− bend back |
| Any | Z+ | yaw to character's left |
| Foot (abs) | X+ | toe down / heel up · X− toe up |

Keypose clip spec:
```json
{ "name": "Attack", "type": "keyposes", "frames": 28, "loop": false,
  "keys": [
    { "frame": 0,  "pose": {} },
    { "frame": 9,  "pose": { "RightUpperArm": [["X", -150]], "Chest": [["Z", -10], ["X", -6]] },
      "hips": [0, 0.02, -0.03] },
    { "frame": 14, "event": "Hit", "pose": { "RightUpperArm": [["X", -35]], "Spine": [["Z", 16], ["X", 8]] },
      "hips": [0, -0.04, -0.06] },
    { "frame": 28, "pose": {} } ] }
```
- Rotation list is applied in order (first entry first). Degrees.
- `hips` = world offset of the pelvis in meters (x left, −y forward, z up).
- `feet: "planted"` (default) keeps both feet on their rest spots via leg IK
  → no sliding however much the hips move. Use `"free"` on both surrounding
  keys for airborne or stepping poses (then legs follow the pose entries).
- Interpolation: smoothstep ease between keys, slerp per bone, dense-keyed
  every frame (what FBX bakes anyway — no F-curve surprises).
- To add overlap/follow-through, offset a child's key 1–3 frames after its
  parent's (e.g. forearm settles 2 frames after the upper arm).

## 4. Locomotion generator (walk / run)

`gen_locomotion` is IK-driven: it plans the **contact point** of each foot
(heel strike → flat → ball roll → swing) and solves the legs analytically, so
contact slip is ~0 by construction. Stride is solved numerically as the
largest step the legs can reach without hyper-extension (`reach` of leg
length), then speed = 2·step / cycle_time.

| Param (GAITS) | walk | run | effect |
|---|---|---|---|
| duty | .62 | .36 | stance fraction per foot (<.5 = flight phase) |
| crouch | .935 | .90 | pelvis height factor — lower = longer stride |
| bob | .011 | .022 | pelvis vertical amplitude (×H) — also lengthens stride |
| lift | .055 | .11 | swing foot apex (×H) |
| reach | .985 | .985 | max leg extension ratio |
| yaw / roll / lean | 5/3/3 | 8/4/9 | pelvis yaw, pelvis roll, forward lean (deg) |
| arm / elbow | 22/18 | 40/80 | arm swing amplitude, elbow bend |
| heel / toe | 14/28 | 6/38 | heel-strike toe-up, toe-off heel-up (deg) |

Measured on a 1.8 m realistic character: Walk 32 f → step 0.60 m,
1.13 m/s · Run 22 f → step 0.92 m, 2.52 m/s. Faster = fewer frames (higher
cadence) or lower crouch. Override any key per clip in the spec.

**In-place vs root motion**

| | In-place (`root_motion: false`) | Root motion (`true`) |
|---|---|---|
| Who moves the character | gameplay code (CharacterController / NavMesh) | the Animator |
| Foot sync | Animator `Speed` must equal real velocity — the blend tree thresholds are the measured clip speeds, `CharacterSpeedDriver` feeds real speed | automatic |
| Best for | responsive player control, networked games, NavMesh agents | cinematic/weighty movement, attacks that lunge, root-driven dodges |
| Unity import | Root XZ baked into pose | Root XZ free |

Mixing is fine: in-place locomotion + root-motion lunge attack (enable
`applyRootMotion` only in that state via script if needed).

Unity import mapping (`CharacterModelPostprocessor`): rotation always baked
(Original), Y always baked (Original — keeps pelvis bob), XZ baked only for
in-place. Loop Time + Loop Pose on loop clips.

## 5. Loops

- Key frame N identical to frame 0 (generators do this); the clip range is
  0..N. `verify_clip` checks root-relative pose continuity < 1e-3.
- Any periodic signal must complete an integer number of cycles over N.
- Unity's loop-match lights in the clip inspector should be green; if not,
  the source loop is broken — fix in Blender, don't rely on Loop Pose.

## 6. Events

Manifest `events: [{name, frame}]` → Unity AnimationEvents calling
`OnAnimEvent(string)` on `CharacterAnimEvents` (normalized time = frame/N).
Standard names: `FootstepLeft/Right` (auto for locomotion, at contact),
`Hit` (attack contact — gameplay damage window), `Cast`, `Spawn`,
`WeaponTrailOn/Off`. Derive impact frames from data (peak hand/weapon reach)
rather than guessing.

## 7. Quality gates (numeric first, eyes second)

`verify_clip`: floor penetration (heel/ball/toe ≥ −1 cm), loop continuity,
contact slip (≤ 0.4 cm/frame, treadmill-compensated for in-place).
Then **look** at `render_sheet` output from the game camera angle
(`three_quarter` for iso/3rd-person, `side` for locomotion). Check:
silhouette reads at game scale, contact pose readable (torso lean toward a
high camera hides the action — keep spine+chest forward lean ≤ 15° at
contact), no arm through torso, hands don't cross the body center on idle.

## 8. Motion that `char_lib` doesn't generate

Priority: generate/author in Blender → CC0 libraries → licensed libraries →
AI text/video-to-motion. Always record the source and license in the
character folder (`LICENSES.md`).

| Source | License (verify at download) | How it enters the pipeline |
|---|---|---|
| Quaternius Universal Animation Library | CC0 | import FBX/GLB → retarget in Unity via humanoid (drop into folder, Humanoid, Copy From Other Avatar = ours) |
| Mixamo | free with Adobe ID; royalty-free use, no raw redistribution; maintenance mode | download "Without Skin", Humanoid in Unity → retargets onto our avatar. In Blender: strip `mixamorig:` prefix, fix 0.01 scale |
| Rokoko / MoCap Online / ActorCore | commercial terms | same humanoid route |
| AI text/video-to-motion (various, 2026) | check output license + training-data terms | treat as mocap: humanoid retarget, then clean contacts in Blender |

Humanoid retargeting is the multiplier: because our avatar is a valid Unity
humanoid, *any* humanoid clip from any source plays on it, and clips made
here play on any other humanoid. Non-human bones (sockets, twist) don't
retarget.

Retargeting inside Blender (when the clip must be baked onto our skeleton,
e.g. to edit contacts): constrain our FK bones to the source armature with
Copy Rotation (world space, per mapped bone) + Copy Location on Hips, then
`bpy.ops.nla.bake(frame_start, frame_end, only_selected=False,
visual_keying=True, clear_constraints=True, bake_types={'POSE'})`, then run
`verify_clip` — imported mocap almost always needs the contact gate.

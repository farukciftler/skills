# Platformer animation spec

The default set the generator ships, why each clip looks the way it does, and the
gameplay constraints animation must obey. Timings are per-frame milliseconds
(Aseprite-style), not a global FPS — holds and snaps are where pixel animation
gets its snap.

## Contents
1. Clip table
2. Gameplay-first rules (read before changing timings)
3. Key poses per clip
4. Authoring custom clips (`custom_animations`)
5. Readability checklist

## 1. Clip table

| Clip | Frames | Durations (ms) | Loop | Events | Purpose |
|---|---|---|---|---|---|
| idle | 4 | 240·160·240·160 | yes | – | 1px breathing bob; long holds read as calm |
| run | 8 | 80 ×8 | yes | OnFootstep @0, @4 | contact · down · pass · up, ×2 legs |
| jump | 2 | 70·100 | no (holds last) | OnJumpDust @0 | stretch; physics already launched |
| apex | 2 | 90·120 | no | – | legs tucked, arms out — hang time |
| fall | 2 | 110·110 | yes | – | flutter so long falls don't freeze |
| land | 3 | 60·70·80 | no | OnLand @0 | squash 3px → 1px, interruptible |
| crouch | 2 | 60·100 | no | – | 2px then 4px drop |
| wall_slide | 2 | 100·100 | yes | – | faces the wall, hand + foot on it |
| dash | 3 | 50·70·90 | no | OnDashStart @0 | strong lean; afterimages are a VFX job |
| attack | 5 | 90·60·50·80·130 | no | OnAttackHit @2, OnAttackEnd @4 | windup · hold · smear · follow · recover |
| hurt | 2 | 80·140 | no | – | recoil; white flash belongs in a shader |
| death | 5 | 100·120·120·120·600 | no | OnDeathComplete @4 | recoil · kneel · slump · fall · rest |

Total ≈ 40 frames — a lean but complete set. Add `walk`, `turn`, `ledge_grab`,
`attack2/3` (combo) or `climb` as custom clips when the design needs them.

## 2. Gameplay-first rules

These override "nicer" animation every time:

- **Never delay input.** Jump physics fire on the press; the jump clip is decoration.
  No crouch-anticipation frame before takeoff unless the game wants that delay.
- **Attack windup ≤ ~150 ms total**, and the hit is an *event* (`OnAttackHit`),
  not a guess from the code. Move the event, never hard-code timers.
- **Land is interruptible**: `land → run` on Speed and `land → jump` on leaving
  ground exist in the graph for this reason. Don't add exit time to them.
- **Collider is constant.** The capsule never animates with the art; crouch
  resizing (if any) is the controller's job, driven by state, not by frames.
- **Pivot is the feet.** Bottom-center (0.5, 0) in every frame. Jumps keep the body
  still inside the frame and move the legs — the Rigidbody moves the character.
- **Root motion off.** Sprite clips carry no transform curves.
- **Fall must loop** or long drops freeze on one frame and feel like a hang.
- **Every event needs a receiver** on the Animator's GameObject
  (`PlatformerAnimationDriver` implements all default ones) or Unity logs errors.
- **Frames ≥ 33 ms** (2 display frames at 60 Hz). Shorter frames get dropped
  inconsistently on 60/120/144 Hz screens.

## 3. Key poses

Coordinates in the pose tables are pixels: feet relative to (center, ground),
hands relative to their shoulder; +x = facing direction, −y = up.

- **Run** (8f): front foot path `(4,0) (2,0) (0,0) (−2,0) (−4,−1) (−2,−3) (1,−4) (3,−2)`,
  back foot is the same path shifted 4 frames. Body bob `0 +1 0 −1` repeats — lowest
  on the *down* frame after contact, highest on *passing*. Arms counter-swing
  the legs. Lean forward 1px.
- **Jump/apex/fall**: body height inside the frame stays near constant;
  legs tuck progressively (−1 → −5 px), arms go forward-up on rise, out at apex,
  up-back on fall. Keep hands clear of the face — hand pixels touching the face
  read as a big nose at 1×.
- **Land**: 3px squash with the torso 1px wider, then 2, then 1.
- **Attack**: windup holds the blade *behind* the head (reads at 1×), the smear
  frame is only 50 ms and carries the unoutlined arc (`slash: [a0, a1, radius]`),
  follow-through keeps the blade low, recover is the longest frame.
- **Death**: the lying frames are the neutral pose rotated 90° — lossless at
  pixel level only in 90° steps, which is why nothing else in the set rotates.

## 4. Authoring custom clips

Add to the character spec; they are rendered with the same rig, palette and outline:

```json
"custom_animations": {
  "walk": {"loop": true, "frames": [
    {"dur": 120, "dy": 0, "ff": [2, 0],  "bf": [-3, 0], "fh": [-1, 6], "bh": [1, 6]},
    {"dur": 120, "dy": 1, "ff": [0, 0],  "bf": [-1, -2], "fh": [0, 6], "bh": [0, 6]},
    {"dur": 120, "dy": 0, "ff": [-2, 0], "bf": [1, 0],  "fh": [1, 6], "bh": [-1, 6]},
    {"dur": 120, "dy": 1, "ff": [-1, -2], "bf": [0, 0], "fh": [0, 6], "bh": [0, 6]}
  ], "events": [{"frame": 0, "function": "OnFootstep"}, {"frame": 2, "function": "OnFootstep"}]}
}
```

Pose fields: `dur` (ms) · `dy` body offset (+ down) · `lean` torso top offset ·
`head` [dx,dy] · `sq` torso width delta · `ff`/`bf` foot targets · `fh`/`bh` hand
targets · `sword` blade angle in degrees (0 = forward, 90 = up, omit = no blade) ·
`slash` [start°, end°, radius] smear arc · `eye` open|closed|hurt · `lie` bool.
Offsets are authored for a 24px character and scaled automatically to `height`.

A custom clip whose name is not in the standard set is imported as a clip and an
unwired state; the importer lists it so you can connect it.

## 5. Readability checklist (review at 1× and 2×, not zoomed)

- Silhouette test: fill each frame black — can you still name the action?
- Consecutive frames differ by ≥ 1 meaningful pixel cluster (validator flags duplicates).
- Loop seam: last frame flows into the first; the first is never repeated at the end.
- Face side and weapon hand stay consistent (art faces right; flipX mirrors it).
- The feet touch the pivot row in every grounded frame (validator checks it).

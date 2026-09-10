# Pixel-art rules for game-ready character sheets

## Contents
1. Sizes, PPU and camera resolution
2. Palette and ramps
3. Outline, shading, clean-up
4. Sheet layout
5. What never to do

## 1. Sizes, PPU, camera

Pick these together, once, for the whole game — mixing PPUs is the #1 cause of
"mixels" (pixels of different sizes on screen).

| Tile | PPU | Character height | Frame | Reference resolution (16:9) |
|---|---|---|---|---|
| 8 px | 8 | 12–16 px | 16×16 / 24×24 | 256×144 or 320×180 |
| 16 px | 16 | 20–28 px | 32×32 | 320×180 or 384×216 |
| 16 px | 16 | 30–36 px | 48×48 | 384×216 or 480×270 |
| 32 px | 32 | 48–64 px | 64×64 / 96×96 | 640×360 |

- **PPU = tile size.** A 16px tile is 1 world unit; physics tuning stays sane.
- Reference resolution should divide the target screen (1920×1080 = 320×180 × 6):
  integer upscaling only. The Unity plugin's `2d-pixel-perfect` skill sets up the
  Pixel Perfect Camera — hand the PPU and reference resolution to it.
- Character height ≈ 1.5–1.75 tiles reads well for platforming (jumps of 2–4 tiles).
- Frames: even width and height, 1px transparent margin on left/right/top.
  The bottom row is the ground contact (pivot y = 0).
- Wider actions (long weapons, big smears) → make the *whole* sheet's frame wider
  rather than one odd-sized frame: a single grid keeps pivots identical.

## 2. Palette and ramps

- 4 tones per material: dark (outline/sel-out), shadow, base, light.
- **Hue-shift**: shadows drift toward blue/violet and gain saturation; lights drift
  toward yellow and lose saturation. Pure black/white shading reads as dirt.
- Total 16–32 colors for a character is normal; > 48 means something resampled the art.
- Keep the skin ramp distinct from the tunic ramp in *value*, not just hue — the
  game may be seen in a greyscale-ish context (colorblind players, night palettes).
- Palette swaps (enemy variants, player 2) = same spec, new `palette` block. The
  generator is deterministic, so sprite names/rects stay identical and one
  Animator Controller can drive every variant via an Animator Override Controller.

## 3. Outline, shading, clean-up

- **Sel-out** (`"outline": "selout"`): each outline pixel takes the dark tone of the
  material it borders. Softer and more readable than a uniform black line at 32px.
  Use a single dark color (`"outline": "#1a1224"`) for a harsher, NES-like look.
- **Contact shading**: where a front limb crosses the body, the body pixels
  touching the limb drop to shadow. This is what separates a tunic-colored arm from
  a tunic-colored torso without adding a full internal outline.
- Light comes from the front-top. When flipX mirrors the sprite the light flips
  too — universally accepted in side-scrollers; don't author a second direction.
- **Orphan pixels** (single pixels with no neighbour) flicker in motion — remove.
- **Pillow shading** (dark ring around every shape) and **banding** (parallel
  ramps stepping together) are the two classic amateur tells; avoid both.
- Smears / slash arcs are *not* outlined and last one or two short frames.
- Eyes: 1×2 px reads at 32px; 1×1 disappears in motion.

## 4. Sheet layout

- One row per animation, one uniform frame grid, left-aligned — what
  `gen_character.py` writes and `validate_sheet.py` checks.
- Sprite names `<char>_<anim>_<i>` — stable across regenerations so re-import
  keeps every clip/prefab reference (the importer reuses sprite IDs by name).
- Keep a 1px transparent margin in the frame and let the atlas add padding;
  never let art touch a neighbouring frame (bleeding lines at non-integer zoom).

## 5. Never

- Rotate or scale pixel art by non-90° / non-integer amounts (in Aseprite or in
  Unity). Rotate by redrawing, or use 90° steps only.
- Import with Bilinear filter, compression, mipmaps or tight meshes.
- Blend between pixel frames (transition duration > 0) — frames must snap.
- Anti-aliased exports (semi-transparent edges); the validator rejects them.
- Different PPUs for characters vs tiles unless the camera is designed for it.

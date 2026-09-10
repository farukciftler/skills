# Unity integration (Unity 6 + official Unity plugin for Claude Code)

## Contents
1. Division of labour with the Unity plugin skills
2. Install the two scripts
3. Run the import (live Editor / batch / menu)
4. What the importer does
5. The Animator graph
6. Hooking up the driver
7. Aseprite routes
8. Verification checklist
9. Troubleshooting

## 1. Division of labour

This skill owns the *character*: art, frame timing, manifest, clips, platformer
state machine, driver. Delegate everything else to the plugin's skills — don't
re-derive their procedures:

| Need | Delegate to |
|---|---|
| CLI install, connected Editor, `eval`, recompile, Safe Mode | `unity-cli` |
| Pixel Perfect Camera, pipeline detection, AA off, reference resolution | `2d-pixel-perfect` |
| Packing the sheet into a SpriteAtlas | `manage-sprite-atlas` |
| Ad-hoc pivot/rect edits after import | `sprite-editor` |
| Level tiles for testing the character | `tilemap-*` skills |
| Footstep / land SFX routing | `audio-setup-mixers` |
| Installing `com.unity.2d.sprite` / `com.unity.2d.aseprite` | `unity-package-management` |

The importer follows the plugin's sprite-editor contract: it slices through
`ISpriteEditorDataProvider`, runs the mandatory `ISpriteFrameEditCapability`
check and aborts if it fails, and never touches `.meta` files.

## 2. Install the scripts (once per project)

```
Assets/Editor/PixelCharacterPipeline/PixelCharacterImporter.cs   <- assets/unity/Editor/
Assets/Scripts/PixelCharacter/PlatformerAnimationDriver.cs        <- assets/unity/Runtime/
```

- Requires `com.unity.2d.sprite` (in every 2D template). Check the manifest first.
- After copying with a live Editor: `unity command recompile`, poll
  `unity command recompile_status` until `completed` (see `unity-cli`). A compile
  error sends the Editor into **Safe Mode** and the CLI can't connect — read the
  Editor log for `error CS`, fix the source, restart.
- If the project wraps runtime code in an asmdef, the driver can live there; the
  Editor script references it, so the asmdef must stay auto-referenced.

## 3. Run the import

Copy the generated folder into the project first, e.g.
`Assets/Art/Characters/Hero/{hero_sheet.png, hero.manifest.json}`.
Never copy `preview/` into Assets (it would import as textures).

**Live Editor (preferred)** — check `unity command --format json` for `eval`'s
parameter shape; `eval` takes a statement block with fully-qualified types:

```bash
unity command eval 'UnityEngine.Debug.Log(PixelCharacterPipeline.PixelCharacterImporter.Import("Assets/Art/Characters/Hero/hero.manifest.json"));'
```

Rebuild the controller in place (keeps its GUID, discards manual edits to the graph):

```bash
unity command eval 'var o = new PixelCharacterPipeline.ImportOptions(); o.rebuildController = true; UnityEngine.Debug.Log(PixelCharacterPipeline.PixelCharacterImporter.Import("Assets/Art/Characters/Hero/hero.manifest.json", o));'
```

**Batch (CI or no open Editor)**:

```bash
unity run /path/to/Project -- -executeMethod PixelCharacterPipeline.PixelCharacterImporter.ImportFromCommandLine \
  -manifest Assets/Art/Characters/Hero/hero.manifest.json -logFile - -quit
```

Flags: `-rebuildController`, `-noPrefab`. Failure exits with code 1.

**Menu**: Tools ▸ Pixel Character ▸ Import Manifest…

## 4. What the importer does

1. **Texture**: Sprite / Multiple, PPU from manifest, Point filter, uncompressed,
   no mipmaps, Clamp, NPOT none, FullRect mesh, extrude 0, max size raised so Unity
   never downscales. Only *already overridden* platform settings are touched.
2. **Slicing**: one SpriteRect per manifest sprite, custom pivot (0.5, 0) or the
   per-sprite pivot from a trimmed Aseprite export. **Sprite IDs are reused by
   name**, so regenerating art never breaks clips or prefabs.
3. **Clips** `Animations/<char>_<anim>.anim`: an `m_Sprite` PPtr curve with one key
   per frame at its accumulated start time (quantized to 1/60 s), plus a closing
   key so the last frame gets its full duration; loop flag; animation events at
   frame start times. Existing clips are updated in place.
4. **Controller** `Animations/<char>.controller`: created if missing, kept if it
   exists (your edits survive), rebuilt in place only on request.
5. **Prefab** `<char>.prefab` (only if missing): SpriteRenderer, Animator,
   Rigidbody2D (freeze rotation, interpolate, continuous), vertical
   CapsuleCollider2D sized from the manifest, a zero-friction PhysicsMaterial2D
   (stops wall-sticking mid-jump), and `PlatformerAnimationDriver`.

## 5. The Animator graph

Parameters: `Speed` (|vx|), `VelocityY`, `Grounded`, `WallSliding`, `Crouching`,
`Dead` · triggers `Dash`, `Attack`, `Hurt`.
All transitions: no blend (duration 0, fixed), no exit time unless noted.

```
AnyState ─Dead──────────────▶ death            (checked first)
AnyState ─Hurt & !Dead──────▶ hurt ──exit──▶ idle | fall
AnyState ─Dash & !Dead──────▶ dash ──exit──▶ idle | fall
AnyState ─Attack & !Dead────▶ attack ─exit─▶ idle | fall

idle ⇄ run (Speed 0.1) · idle/run ─Crouching─▶ crouch ─!Crouching─▶ idle
idle/run/crouch/land ─!Grounded & VelY>0.1──▶ jump
idle/run/crouch/land ─!Grounded & VelY<-0.1─▶ fall     (walked off a ledge)
jump ─VelY<apexBand─▶ apex ─VelY<-apexBand─▶ fall
jump/apex/fall ─Grounded─▶ land ─Speed>0.1─▶ run
                                 └─exit────▶ idle
jump/apex/fall ─WallSliding─▶ wall_slide ─Grounded─▶ land
                                          └─!WallSliding & !Grounded─▶ fall
```

`apexBand` (default 1.0 u/s) should be ≈ 15–25 % of your jump's takeoff velocity;
pass it through `ImportOptions.apexBand`. Missing clips are simply skipped and
the graph reroutes (no apex → jump goes straight to fall, no land → idle).

## 6. Hooking up the driver

The driver reads, it doesn't move. From your controller:

```csharp
driver.Grounded = isGrounded;   // or leave autoGroundCheck on and set groundMask
driver.WallSliding = isWallSliding;
driver.Crouching = crouchHeld;
driver.PlayAttack(); driver.PlayDash(); driver.PlayHurt(); driver.Die(); driver.Revive();
driver.onAttackHit.AddListener(EnableHitbox);    // hit timing comes from the art
driver.onFootstep.AddListener(PlayStepSfx);
```

- Facing: `flipX` from velocity (art faces right). Put hitboxes/VFX under one child
  and assign it to `mirroredChildren` — flipX does not move children.
- `ungroundedGrace` (60 ms) hides single-frame fall flicker on steps and slopes.
- Set the player's own layer out of `groundMask`.

## 7. Aseprite routes

- **Have `.aseprite` sources and want Unity to own the import?** Use Unity's
  **2D Aseprite Importer** (`com.unity.2d.aseprite`): tags become clips, cel user
  data `event:OnFootstep` becomes an animation event, a tag Repeat of 1 makes a
  clip non-looping. Its generated controller is read-only, so build the editable
  platformer graph from its clips:
  ```bash
  unity command eval 'UnityEngine.Debug.Log(PixelCharacterPipeline.PixelCharacterImporter.BuildControllerFromClips("Assets/Art/Hero/hero.aseprite", "Assets/Art/Hero/hero_platformer.controller"));'
  ```
  Name tags exactly like the states (idle, run, jump, apex, fall, land, crouch,
  wall_slide, dash, attack, hurt, death).
- **Have PNG + JSON exports** (from Aseprite, LibreSprite, Pyxel Edit…): run
  `aseprite_to_manifest.py`, then the normal importer. Durations and tags carry over.

## 8. Verification (after every import)

Run inside the Editor (via `eval`) and report the numbers, don't assume:

- texture importer: `filterMode == Point`, `textureCompression == Uncompressed`,
  sprite count == manifest sprite count;
- each clip: length ≈ sum of durations; `loopTime` matches; event count;
- controller: default state `idle`, parameter list as in §5;
- Play mode: character stands *on* a tile (no 1px gap = pivot correct), flipping
  doesn't shift it sideways, last frame of `land` is visible, no
  "AnimationEvent has no receiver" errors in the console.

## 9. Troubleshooting

| Symptom | Cause → fix |
|---|---|
| Blurry / soft pixels | Filter not Point, or camera AA on → re-import; `2d-pixel-perfect` |
| Sprites wobble 1px while moving | No Pixel Perfect Camera / non-integer zoom; interpolation + snapping off |
| Thin lines between frames / neighbour bleeding | Art touching frame edge; atlas padding < 2; tight mesh |
| Character floats or sinks 1px | Pivot not on the sole row → `validate_sheet.py` shows which frames |
| Jumps sideways when turning | Pivot x not centered / odd frame width |
| Last frame never shows | Clip lacks closing key (hand-made clip) → re-import through the importer |
| Animation lags input by ~0.1 s | Transition has exit time or duration > 0 |
| Land blocks running | `land → run` transition deleted or given exit time |
| "AnimationEvent 'X' has no receiver" | Driver missing, or custom event name → add a method with that name |
| Changes to clips undone after re-import | Clips are regenerated from the manifest: edit the spec/Aseprite, not the clip |
| Controller edits lost | Import ran with `rebuildController` — it is opt-in for this reason |

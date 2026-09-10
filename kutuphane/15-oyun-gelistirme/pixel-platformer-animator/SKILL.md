---
name: pixel-platformer-animator
description: Creates pixel-art character sprite animations for 2D platformer games and wires them into Unity 6 — generates a full side-view animation set (idle, run, jump, apex, fall, land, crouch, wall slide, dash, attack, hurt, death) as a validated sprite sheet with per-frame timing and events, or takes the user's own Aseprite/PNG art, then imports it through the official Unity plugin workflow (unity-cli eval) into sliced sprites, AnimationClips, a platformer Animator Controller, a runtime driver and a ready prefab. Use whenever the user wants a player/enemy sprite, sprite sheet, run cycle, jump or attack animation, Animator setup for a platformer, or asks why a pixel character floats, jitters, blurs, slides when flipping or skips frames — even if they never say "animation". Trigger on Turkish phrasings like "pixel karakter", "sprite animasyonu", "koşma animasyonu", "platform oyunu karakteri", "sprite sheet oluştur", "Animator kur", "karakter zıplamıyor gibi görünüyor".
---

# Pixel Platformer Animator

Produces a game-ready pixel character: art → timing → validated sheet → Unity
clips, state machine, driver, prefab. Built to sit next to Unity's official Claude
Code plugin: this skill owns the character; the plugin's skills own the Editor
plumbing (`unity-cli`), camera (`2d-pixel-perfect`), atlas (`manage-sprite-atlas`)
and sprite metadata contract (`sprite-editor`). Delegate to them, don't duplicate them.

## Bundled files

| Path | Use |
|---|---|
| `scripts/gen_character.py` | Spec JSON → sheet PNG + manifest + GIF previews (procedural rig, deterministic) |
| `scripts/aseprite_to_manifest.py` | Aseprite PNG+JSON export → same manifest |
| `scripts/validate_sheet.py` | Pre-import QA; must report 0 errors before Unity |
| `assets/unity/Editor/PixelCharacterImporter.cs` | Manifest → texture settings, slicing, clips, controller, prefab |
| `assets/unity/Runtime/PlatformerAnimationDriver.cs` | Feeds Animator from Rigidbody2D, flipX, event receivers |
| `assets/specs/*.json` | Example specs (32px hero, 48px ranger) |
| `references/animation-spec.md` | Clip table, gameplay rules, pose-table format — read before editing poses/timing |
| `references/pixel-art-rules.md` | PPU/size table, palette, outline, sheet rules — read when choosing sizes or palette |
| `references/unity-integration.md` | Install, import commands, graph, driver hookup, verification, troubleshooting |
| `references/spec-and-manifest.md` | Field-by-field schemas |

Python deps: `numpy`, `Pillow`.

## Step 0 — Pick the route

- **A. No art yet** (prototype, placeholder, enemy variants, palette swaps) → generate with `gen_character.py`.
- **B. User has art as PNG + JSON** (Aseprite, LibreSprite, Pyxel Edit export) → `aseprite_to_manifest.py`, then the same import.
- **C. User has `.aseprite` files and wants Unity to own them** → Unity's 2D Aseprite Importer makes the clips; this skill builds the editable platformer graph (`BuildControllerFromClips`, see unity-integration.md §7).
- **Diagnosis only** ("my character floats / blurs / slides") → run the validator on their sheet and walk the troubleshooting table in unity-integration.md §9.

Be honest about route A: the generator yields clean, consistent, correctly timed
side-view art with a readable silhouette — strong placeholder and a base for an
artist to paint over in Aseprite — not hand-crafted hero art. Re-painted frames go
back through route B with names unchanged, so nothing in Unity breaks.

## Step 1 — Lock the game-wide constants first

PPU, character height, frame size and camera reference resolution are one decision
(table in pixel-art-rules.md §1). If the project already has tiles, **read their
PPU from the project** rather than asking. Defaults when nothing exists: 16px
tiles, PPU 16, 24px character in 32×32 frames, 320×180 reference resolution.
Never mix PPUs between the character and the tiles.

## Step 2 — Produce the sheet

Route A:
```bash
cp assets/specs/hero.json work/spec.json      # edit name, palette, height, frame, hair_style, weapon...
python scripts/gen_character.py work/spec.json --out work/build
```
Route B:
```bash
aseprite -b hero.aseprite --sheet hero_sheet.png --data hero.json --format json-array --sheet-type rows --split-tags --list-tags
python scripts/aseprite_to_manifest.py hero.json --name hero --ppu 16 --auto-pivot idle
```
Then **look at the result** (view `work/build/preview/<name>_sheet_x8.png`, or a
cropped/zoomed version of it) and check against animation-spec.md §5: silhouette
reads, hands clear of the face, feet on the ground row, loops flow. Fix poses by
adding `custom_animations` to the spec (same names override the defaults) — never
by hand-editing the PNG of a generated character, because it would be lost on the
next regeneration. Palette variants = same spec, new `palette` block.

Share the preview PNG/GIFs with the user before going into Unity; art direction
changes are cheap here and expensive later.

## Step 3 — Validate (gate)

```bash
python scripts/validate_sheet.py work/build/<name>.manifest.json
```
0 errors is required. Treat warnings as real unless there is a reason (e.g. a
deliberately trimmed Aseprite export). Custom grounded clips: `--grounded idle,run,walk,...`.

## Step 4 — Import into Unity

Follow unity-integration.md §2–§3. In short:

1. Confirm a connected Editor with `eval` (via `unity-cli`); otherwise use the batch command.
2. Copy the two C# files into the project (Editor script into an `Editor/` folder),
   recompile, and stop if the Editor drops into Safe Mode.
3. Copy `<name>_sheet.png` + `<name>.manifest.json` (not `preview/`) into e.g.
   `Assets/Art/Characters/<Name>/`.
4. Run `PixelCharacterPipeline.PixelCharacterImporter.Import("<manifest asset path>")`.
   Re-imports are safe: sprite IDs are reused by name, clips update in place,
   an existing controller/prefab is left alone unless `rebuildController` is set.
5. Verify with real numbers from the Editor (unity-integration.md §8) — importer
   settings, sprite count, clip lengths vs summed durations, loop flags, default
   state — and report them. Don't declare success from the log alone.

## Step 5 — Finish the scene side (delegate)

- Pixel Perfect Camera, AA off, reference resolution → `2d-pixel-perfect`.
- Pack the sheet into an atlas if the game has many sprites → `manage-sprite-atlas` (Point filter, padding ≥ 2, no tight packing, no rotation).
- Explain how the user's movement code talks to `PlatformerAnimationDriver`
  (unity-integration.md §6): Grounded/WallSliding/Crouching flags, `PlayAttack/Dash/Hurt`, `Die/Revive`, UnityEvents for footsteps and hit frames.

## Non-negotiables

- Pivot bottom-center, identical in every untrimmed frame; frames even-sized.
- Transitions snap: duration 0, no exit time except where the graph says so.
- Gameplay never waits for animation: jump physics fire on press, attack hit is an event, land is interruptible.
- Collider never animates; root motion off.
- Point filter, uncompressed, no mipmaps, FullRect — the importer enforces it; don't undo it by hand.
- Timings stay in per-frame milliseconds, each ≥ 33 ms.

## Output to the user

Keep it short: previews shown, validator result, what was created in Unity
(paths), the verification numbers, and the 2–3 lines of code their controller
needs. Mention anything skipped (e.g. no live Editor → batch command given, not run).

# Character spec and manifest schema

## Character spec (input to `gen_character.py`)

Every field is optional; defaults in parentheses. Example files: `assets/specs/`.

| Field | Meaning |
|---|---|
| `name` ("hero") | prefix for files and sprite names — keep stable once imported |
| `frame` ([32, 32]) | frame size in px, even numbers |
| `height` (24) | character height in px, sole to hair top; pose offsets scale with it |
| `ppu` (16) | pixels per unit — must equal the game's tile PPU |
| `outline` ("selout") | "selout" or a hex color for a uniform line |
| `hair_style` ("short") | short · long · hood (hood uses the tunic ramp) |
| `sleeves` ("short") | short = skin forearms (reads better at 32px) · long |
| `weapon` ("sword") | sword · none (drops blade and smear frames' blade) |
| `palette` | `skin hair tunic pants boots accent steel` (ramp bases), `line` (eyes / uniform outline), `fx` (smears) |
| `animations` ("all") | "all" or a list of clip names to render |
| `custom_animations` | extra or replacement pose tables — see animation-spec.md §4 |

Height ↔ frame guidance: 24 in 32×32, 34 in 48×48. Leave ≥ 4px headroom above
the hair for jump stretch and windups; the validator warns if art touches edges.

## Manifest (schema 2, output of both generators, input of the Unity importer)

```json
{
  "schema": 2,
  "name": "hero",
  "texture": "hero_sheet.png",            // relative to the manifest file
  "textureWidth": 256, "textureHeight": 384,
  "frameWidth": 32, "frameHeight": 32,
  "ppu": 16, "facing": "right",
  "collider": {"w": 0.5, "h": 1.4375, "offsetX": 0, "offsetY": 0.7188},   // units, optional
  "sprites": [
    {"name": "hero_idle_0", "x": 0, "y": 352, "w": 32, "h": 32, "pivotX": 0.5, "pivotY": 0.0}
  ],
  "animations": [
    {"name": "idle", "loop": true,
     "frames": [{"sprite": "hero_idle_0", "durationMs": 240}],
     "events": [{"frame": 0, "function": "OnFootstep", "stringParameter": "", "intParameter": 0, "floatParameter": 0}]}
  ]
}
```

- Rects use Unity's **bottom-left** origin (y counts up from the texture bottom).
- `sprites` are unique; animations reference them, so pingpong tags or reused
  frames don't duplicate rects.
- Pivots are normalized to the sprite rect; values outside 0–1 are legal (trimmed frames).
- Event `frame` is an index into that animation's `frames`; the event fires at the frame's start.
- Hand edits are fine (retiming, moving an event); re-run `validate_sheet.py` after.

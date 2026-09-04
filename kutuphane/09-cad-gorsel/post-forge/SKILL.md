---
name: post-forge
description: Designs and RENDERS finished social post visuals — Instagram feed posts (4:5, 1:1), Stories frames, Instagram carousels and LinkedIn document carousels — as pixel-exact HTML/SVG exported to PNG and PDF. Builds custom SVG illustration, hand-drawn charts and product mockups (phone frame, laptop, browser window, isometric app screens, floating UI cards) instead of stock templates, locked to a brand design system. Use whenever the deliverable is the IMAGE, not the caption — "instagram postu tasarla", "post görseli üret", "carousel hazırla", "LinkedIn carousel", "şu ekranı telefon mockup'ında göster", "özel SVG çiz", "bu postlar birbirine benziyor, farklılaştır", "screenshot'u güzelleştir", "story görseli", "metrik kartı tasarla". Trigger even when the user only says "post" but points at a screenshot, a product screen, a metric or a design system, and for redesign or de-templating of existing visuals. Hand caption copy to trend-setter; this skill owns the pixels.
---

# Post Forge — Rendered Social Visual Studio

Produce social visuals that look like a design studio made them: art-directed, brand-locked, and visibly different from one another. The output of this skill is never a description of a design — it is rendered image files on disk that the user has seen, at exact platform dimensions, verified by looking at them.

Two failure modes define the work. The first is **generic**: centered white text on a purple-blue gradient, Inter everywhere, one rounded card floating in the middle, the same layout on every slide. The second is **broken**: text clipped, overflow past the canvas, 11px type nobody can read in a feed, contrast that dies on mobile. This skill exists to kill both, so every job passes through a render-and-inspect loop before delivery.

## Division of labor

This skill owns pixels. If the request also needs caption copy, hooks, hashtags, or posting strategy, that belongs to `trend-setter` — call it for the words, come back here for the image. If neither skill is loaded and the user wants both, do copy first (the hook determines slide 1's layout), then design.

## Reference map

Read what the job needs; do not preload everything.

| File | Read when |
|---|---|
| `references/design-tokens.md` | ALWAYS, before drawing anything. Token extraction, palette/type/spacing discipline, and the anti-AI-look rules. |
| `references/layout-archetypes.md` | ALWAYS, when composing. 18 composition archetypes — this is the primary defense against sameness. |
| `references/mockups.md` | Any phone, laptop, tablet, browser, watch, or in-app UI frame; screenshot beautification; isometric/perspective device scenes. |
| `references/svg-craft.md` | Custom illustration, icons, textures, grain, blobs, arrows, annotations, hand-built charts, number/metric graphics. |
| `references/carousel.md` | Multi-slide anything: Instagram carousels, LinkedIn document posts, story sequences. |
| `references/render-pipeline.md` | Before the first render, and whenever export, fonts, PDF, or crispness misbehave. |

`assets/canvas.css` is the base stylesheet every deliverable imports (copy it next to the HTML). `assets/tokens.example.json` is the token schema. `assets/starter.html` is a working three-slide file showing the mechanics — slide declaration, token override, phone frame, fake UI, continuity slot, grain wiring — and is a reference for *plumbing only*, never a layout to reuse with the text swapped. `scripts/render.py` exports PNG/PDF; `scripts/contact_sheet.py` builds the review grid and the thumbnail legibility test.

## Canvas specs

Design at these CSS pixel sizes, render at 2× (see `references/render-pipeline.md`).

| Target | Canvas | Notes |
|---|---|---|
| Instagram feed (default) | 1080 × 1350 (4:5) | Tallest allowed; wins the most feed height. Profile grid crops to 4:5, so it survives intact. |
| Instagram square | 1080 × 1080 | Use when the concept is symmetrical or the client's system is square-locked. |
| Instagram Story / Reels cover | 1080 × 1920 | Keep everything vital inside the central 1080 × 1420; top ~250px and bottom ~320px are covered by UI. |
| Instagram carousel | 1080 × 1350, uniform across slides | Mixing ratios inside one carousel gets slides cropped. Up to 20 slides. |
| LinkedIn single image | 1200 × 1500 (4:5) | Portrait outperforms landscape for feed height. |
| LinkedIn document carousel | 1080 × 1350 pages → single PDF | Feed viewer trends toward square on desktop: keep the critical read inside the central 1080 × 1080. |

Bleed discipline: keep a hard 64px inner margin on 1080-wide canvases (72–80px reads more premium), and never let type land closer than 48px to any edge. Elements *may* deliberately bleed off-canvas — that's a technique, not an accident — but text never does.

## Workflow

### Step 1 — Brief and tokens

Establish target platform(s), slide count, the one job the visual must do (stop the scroll, explain a feature, show a number, announce, teach), and the brand's visual system. Infer from the conversation, uploaded files, screenshots, and existing repos before asking anything. If the design system is genuinely unknown, either read tokens from the user's codebase (Tailwind config, CSS variables, SwiftUI color assets, Figma export) or propose a compact system in three lines and proceed — do not stall the job on a questionnaire.

Write the resolved tokens to `tokens.json` in the working directory using the schema in `assets/tokens.example.json`. Everything downstream references those variables and nothing hardcodes a hex value, because that's what makes a set of posts feel like one brand and makes a restyle a one-file edit.

### Step 2 — Art direction before code

Decide, in writing, before touching HTML: the archetype per slide (from `references/layout-archetypes.md`), the single focal element, the type hierarchy (how many levels, and the largest size — usually 88–160px on a 1080 canvas), the palette split (which color carries 70% / 25% / 5%), and one **signature device** that repeats across the set — a rule, a corner notch, a numeral treatment, a duotone screenshot, a grain, an off-grid tilt. The signature device is what makes the set recognizable; without one, brand-consistent output degrades into template output.

Then state the variation plan: no two adjacent slides may share an archetype, and no two posts in a batch may share the same focal treatment. Write this down as a table before rendering — deciding it after the fact never happens.

### Step 3 — Build

One HTML file per deliverable. For carousels, one file containing all slides as sibling `.slide` elements — it keeps continuity visible while designing and exports cleanly per slide.

```html
<link rel="stylesheet" href="canvas.css">
<div class="slide" data-name="01-hook" style="--w:1080px; --h:1350px"> … </div>
```

Rules that keep the output print-quality:
- Everything vector or text; raster only for real screenshots and photos the user supplied.
- Custom SVG over icon fonts and emoji. Emoji is the fastest way to make a post look amateur; a 2-minute hand-drawn glyph beats it (`references/svg-craft.md`).
- Layout with CSS grid on an explicit column system, not stacks of margins. Overlap and off-grid placement should be intentional grid decisions.
- No `overflow: hidden` used to hide a layout problem. Fix the layout.
- Long text is a design failure, not a font-size problem: cut the words before shrinking type below the floors in `references/design-tokens.md`.

### Step 4 — Render

```bash
python scripts/render.py post.html --out out/ --scale 2
python scripts/render.py deck.html --out out/ --scale 2 --pdf carousel.pdf
```

The script screenshots each `.slide` at its declared size, names files from `data-name`, and can bundle a PDF for LinkedIn documents. Read `references/render-pipeline.md` first for the font setup — missing fonts silently fall back and quietly ruin the design.

### Step 5 — Look at it (non-negotiable)

Open the rendered PNGs with the image-viewing tool and actually inspect them. Text that "should" fit often doesn't. Then run:

```bash
python scripts/contact_sheet.py out/ --thumb 220
```

The contact sheet is the squint test: at 220px, a real feed-scroll size, the primary message must still land and the set must read as one family with visibly different compositions. Check against this gate:

- Nothing clipped, nothing overflowing, no accidental scrollbars or seams
- Primary message legible at 220px width
- Body text ≥ 28px, labels ≥ 22px on a 1080 canvas
- Text-on-background contrast ≥ 4.5:1 (over images: solid scrim or shape behind the type, never raw text on busy photo)
- Tokens honored — no stray hex, no off-system font
- Adjacent slides differ in composition; the signature device is present in all of them
- Mockups geometrically credible: correct corner radii, consistent perspective, no stretched screenshots (`references/mockups.md`)
- Nothing from the anti-AI-look banned list in `references/design-tokens.md`

Fix and re-render until it passes. Two or three loops is normal and expected — the first render is a draft, not a deliverable.

### Step 6 — Deliver

Hand over the PNGs (and PDF for LinkedIn documents), the contact sheet, plus the HTML and `tokens.json` so the user can re-render after edits. Then, in at most five lines: the archetype used per slide, the alt text for each image (accessibility, and it doubles as the caption seed), and any deliberate risk taken. No design essays.

## Variation engine

When the user asks for options, or says posts feel same-y, vary along these axes rather than nudging colors — each axis flip changes the composition, not the skin:

1. **Focal type** — big numeral / device mockup / custom illustration / photographic subject / pure typography / diagram
2. **Type-to-image ratio** — 90/10 poster vs 30/70 image-led
3. **Grid stance** — centered symmetry / hard left rail / diagonal / edge-bleed / off-grid tilt (1.5–3°)
4. **Value structure** — light-on-dark, dark-on-light, mid-tone duotone, single accent on near-black
5. **Density** — one word per slide vs a dense annotated diagram
6. **Depth** — flat vector / layered cards with real shadows / isometric / perspective device scene

Generating three options means three different rows in that matrix, not three color variants. Show them as one contact sheet and let the user pick before refining.

## Non-negotiables

- **No fabricated proof.** Metrics, review stars, follower counts, testimonials, and logos inside mockups must come from the user or be marked as placeholder in the delivery note. A screenshot-looking image is read as evidence.
- **No borrowed IP.** Don't recreate other companies' logos, licensed fonts, or paid stock photography from memory. Draw original marks, use the brand's own assets, or leave a labeled placeholder.
- **Device frames stay generic.** Draw a phone that reads as a modern phone; don't reproduce a manufacturer's logo or trade dress detail as branding.
- **Honest mockups.** If a UI in a mockup shows a feature that doesn't exist yet, say so in the delivery note so nobody ships it as a live product shot.

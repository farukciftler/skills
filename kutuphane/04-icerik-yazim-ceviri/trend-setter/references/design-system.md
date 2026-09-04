# Design System — Visual Production

Visual content follows a token system, never one-off aesthetic decisions. The goal is a brand recognizable within 0.5 seconds of scrolling, achieved through repetition of a few locked elements — not through decorating every slide differently.

## Contents
1. Two operating modes
2. Token schema
3. Canvas and safe-zone specs
4. Slide logic for carousels
5. Anti-AI-look rules
6. Production paths (spec sheet / rendered HTML / SVG)
7. Consistency contract and accessibility

---

## 1. Two operating modes

**Mode A — a design system exists.** Extract tokens from whatever the user provides (brand guide PDF, Figma values, a website, past posts as screenshots): exact hex colors, font families and fallbacks, logo rules, spacing habits, photography style, tone words. Obey them completely; where the brand guide is silent, extend conservatively in the same spirit and tell the user which decisions were extensions.

**Mode B — no system exists.** Propose a mini-system BEFORE producing visuals, in this shape (5 lines, get a quick yes):
- Palette: 4–5 named hex values (bg, surface, text, accent, accent-contrast) derived from the brand's subject matter — a FinOps brand pulls from terminal greens and invoice paper, a bakery from crust and butter, never from the generic AI defaults (see §5)
- Type: one characterful display face + one workhorse body face (Google Fonts for renderability), with weights
- One brand anchor: the single recurring visual device (a corner tab, a thick left rule, a stamp-style handle chip, a signature underline) that appears on every asset
- Layout: margin size and where the handle/logo lives
- Register: 2–3 adjectives for the visual voice

Then lock it and reuse it for every subsequent asset in the conversation.

---

## 2. Token schema

Keep tokens explicit — in a code block in the conversation or a JSON the user can save:

```json
{
  "canvas": { "w": 1080, "h": 1350 },
  "color": {
    "bg": "#0E1116", "surface": "#161B22", "text": "#E9EDF1",
    "muted": "#9AA4AF", "accent": "#E8A33D", "accentInk": "#141414"
  },
  "type": {
    "display": "Sora", "body": "Inter",
    "h1": 104, "h2": 64, "body": 44, "caption": 30, "lineHeight": 1.25
  },
  "space": { "margin": 88, "gap": 32 },
  "anchor": "amber corner tab, top-left, 160×56, contains slide number",
  "handle": "@brand — bottom-right, caption size, muted"
}
```

Type-scale floor for 1080px-wide canvases viewed on phones: body text never below ~36px, headline range 88–128px, one and only one type hierarchy per template family.

---

## 3. Canvas and safe-zone specs

| Asset | Canvas | Notes |
|---|---|---|
| IG/LinkedIn feed portrait | 1080×1350 (4:5) | Default for carousels; max feed real estate |
| Square | 1080×1080 | Only when a grid aesthetic demands it |
| Story / Reel cover | 1080×1920 (9:16) | Keep critical content inside a centered ~1080×1420 zone; UI eats roughly 220px top and 320px bottom |
| LinkedIn document (PDF carousel) | 1080×1350 pages | Exported as one PDF |
| X image | 1600×900 (16:9) | Text must survive timeline downscale |
| YouTube thumbnail | 1280×720 | ≤4 words, face or single object, extreme contrast |

Safe-zone pixel values shift with app updates — when precision matters, verify against the platform's current template before final export.

---

## 4. Slide logic for carousels

- **Hook slide:** one focal idea, display type at maximum scale, most negative space of any slide. No logo lockups, no decoration competing with the words.
- **Re-hook slide (2):** the stake or cost. Slightly denser than slide 1.
- **Content slides:** identical margins, identical text block position (a fixed "scanning path" so swiping feels like one continuous read), progress cue (slide numbers in the anchor, or a thin progress bar), ≤25 words each, one supporting visual max.
- **CTA slide:** highest contrast of the set (invert bg/accent), one action, handle prominent.
- The system varies *content* per slide, never *layout grammar*. If slide 5 needs a different layout, it belongs to a different template family — add a second family rather than mutating mid-deck.

---

## 5. Anti-AI-look rules

AI-generated visuals cluster into recognizable defaults. Refuse them the way `humanize.md` refuses "delve":

- **Banned default palettes:** warm cream + high-contrast serif + terracotta accent; near-black + acid green or vermilion; purple-to-blue gradient on everything. All legitimate if the brand genuinely owns them; forbidden as unexamined defaults.
- **Banned decoration:** glassmorphism blobs, generic 3D renders, emoji as design elements, gradient text on body copy, drop shadows on everything, sparkles/rocket iconography.
- **Derive, don't decorate:** every visual choice traces to the brand's actual world — its product UI colors, its materials, its market's vernacular. A cost-optimization brand can quote ledger typography; an RPG brand can quote parchment and dice pips.
- **One risk per template family:** a single memorable move (an oversized numeral, a brutal crop, an unexpected type pairing), everything else disciplined. Spend boldness in one place.
- Stock-photo smiles and abstract "teamwork" imagery read corporate-AI. Real screenshots, real product, real texture beat them on every platform.

---

## 6. Production paths

Choose based on how the user will produce final assets:

**Path 1 — Spec sheet** (user designs in Canva/Figma): deliver a per-slide table — slide #, exact copy, layout note, token references — plus the token block. Tight copy, no lorem ipsum.

**Path 2 — Rendered HTML** (user screenshots or exports): build fixed-size HTML, one `.slide` element per slide at exact canvas pixels, tokens as CSS variables, Google Fonts imported. Start from `assets/carousel-template.html` and restyle per the token system — change the variables and layout grammar, don't ship the template's own look. Rendering at 1:1 pixels means screenshots are production-ready; mention that browser zoom must be 100%.

**Path 3 — SVG** for single quote cards or simple diagrams when the environment renders SVG inline.

Whichever path: deliver the caption + alt text alongside the visual, since the copy and the design ship together.

---

## 7. Consistency contract and accessibility

Locked across every asset of a family: margins, type scale, the single accent color, the brand anchor, handle placement. Free to vary: imagery, headline content, one layout slot.

Accessibility floor: body-size text contrast ≥ 4.5:1 against its background, large display text ≥ 3:1, never set text over busy photo areas without a scrim, and write real alt text (a one-line description carrying the keyword — it's also indexed for search on Instagram and LinkedIn).

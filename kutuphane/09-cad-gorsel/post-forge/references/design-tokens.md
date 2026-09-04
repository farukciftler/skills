# Design Tokens & Visual Discipline

Read before drawing. This file decides whether the output looks like a brand or like a template.

## Contents
1. Where tokens come from
2. tokens.json schema
3. Palette discipline
4. Type discipline
5. Space, radius, shadow, motion-of-the-eye
6. The anti-AI-look banned list
7. Proposing a mini-system from nothing

---

## 1. Where tokens come from

In priority order:

1. **Explicit design system** the user provides (brand guide PDF, Figma tokens export, `tokens.json`).
2. **The codebase.** Read it rather than asking:
   - `tailwind.config.{js,ts}` → `theme.extend.colors`, `fontFamily`, `borderRadius`
   - `:root { --… }` in any global CSS
   - SwiftUI/iOS: `Assets.xcassets/*.colorset/Contents.json`, or a `Color+Brand.swift`
   - `theme.ts`, `_variables.scss`, `design-tokens.json`
3. **The product itself.** Sample colors from a screenshot the user gave — pull the actual UI accent, not an approximation.
4. **The existing posts.** If the brand already posts, match what's there unless the ask is explicitly to break from it.
5. **Propose** (section 7).

Never mix sources silently. If the codebase accent and the brand guide accent disagree, pick the product's and say one line about it.

## 2. tokens.json schema

```json
{
  "brand": "Cloud4Next",
  "color": {
    "ink":        "#0B0F14",
    "surface":    "#FFFFFF",
    "surfaceAlt": "#F4F6F8",
    "accent":     "#2F6BFF",
    "accentAlt":  "#00C2A8",
    "warn":       "#FFB020",
    "muted":      "#6B7683"
  },
  "font": {
    "display": "\"Space Grotesk\", \"Inter\", system-ui, sans-serif",
    "text":    "\"Inter\", system-ui, sans-serif",
    "mono":    "\"JetBrains Mono\", ui-monospace, monospace"
  },
  "scale": { "step": 1.28, "base": 32 },
  "radius": { "sm": 8, "md": 16, "lg": 28, "device": 56 },
  "space":  { "gutter": 72, "unit": 8 },
  "signature": "8px accent rule top-left + mono eyebrow label",
  "grain": 0.035
}
```

Emit it as CSS variables into `canvas.css`'s `:root` override block, and reference only variables in markup. A restyle then costs one file.

## 3. Palette discipline

- **70 / 25 / 5.** One color dominates the canvas, one supports, one is the accent that appears once or twice. When every color gets equal airtime, the design reads as a chart, not a poster.
- **Anchor in a near-black or near-white, not pure.** `#0B0F14` and `#FAFAF7` have temperature; `#000` and `#fff` look unfinished on screen.
- **Duotone screenshots.** Recoloring a product screenshot to two brand tones (`references/svg-craft.md` has the filter) is the single strongest brand-consistency move available for tech posts.
- **Gradients are earned.** If used: 2 stops max, both from the brand palette, low contrast between them (a tonal shift, not a rainbow), and angled off the vertical. Radial glows behind a focal element are fine; full-canvas diagonal gradients are the default AI tell.
- **One saturated element per canvas.** Everything else desaturated. This is what makes the eye land where you want.
- **Dark canvases need a light escape.** Pure dark posts flatten in feed; give them one bright surface, one white rule, or one photographic patch.

Contrast floors: 4.5:1 for anything ≤ 48px, 3:1 for display type above that. Check it, don't eyeball it.

## 4. Type discipline

- **Two families max**, three only when the third is mono used exclusively as labels/eyebrows/code.
- **Real hierarchy, four levels max**: eyebrow (22–28px, uppercase or mono, letterspaced +0.08em), headline (88–160px on 1080 canvas), body (28–40px), caption/label (22–26px).
- **Display type gets negative tracking** (−0.02em to −0.035em) and tight leading (0.92–1.02). Default browser leading on 120px type is the amateur giveaway.
- **Body leading 1.35–1.5**, measure 28–42 characters per line on a 1080 canvas. Wider than that and nobody reads it on a phone.
- **Floors on a 1080 canvas**: body 28px, labels 22px, nothing below 20px ever. If it doesn't fit, cut words.
- **Align to something.** Pick one edge and commit. Centered-everything is only a choice when the whole composition is symmetric — otherwise it's a default.
- **Emphasis by weight or color, not italics-plus-bold-plus-underline.** One emphasis mechanism per canvas.
- **Turkish text**: verify `ı İ ğ Ş ç Ö ü` render in the chosen font, and beware fonts that lack the dotless ı. Test the actual string, not a Latin placeholder.
- **Numerals**: use tabular figures for aligned stats (`font-variant-numeric: tabular-nums`), and consider setting a big metric in the display face at 160–260px as the entire composition.

## 5. Space, radius, shadow

- **8px base unit.** Every gap is a multiple. Inconsistent spacing is felt even when it isn't seen.
- **Gutter 64–80px** on 1080 canvases. Tight margins read cheap; generous margins read premium and are free.
- **One radius language.** Either sharp (0–8px) or soft (24–32px) — mixing 4px chips with 32px cards looks unresolved. Device frames are the exception, they follow the hardware (see mockups).
- **Shadows**: two layers or none. `0 1px 2px rgba(0,0,0,.06), 0 24px 48px -12px rgba(0,0,0,.24)`. Colored shadows tinted with the accent at low alpha look intentional; symmetric grey blur looks like Bootstrap.
- **Grain.** A 3–5% noise overlay across the whole canvas (`canvas.css` `.grain`) removes the plastic digital-flat look instantly. Almost always worth it, especially on gradients and dark canvases.
- **Reading path.** Design one entry point (largest/brightest element), one path (usually top-left → focal → bottom-right CTA). If the eye has two equal entry points, the post reads as noise in a fast scroll.

## 6. The anti-AI-look banned list

Any of these present means redesign, not tweak:

- Purple→blue or teal→purple diagonal gradient across the full canvas
- Everything centered, vertically and horizontally, with equal air on all sides
- One lonely rounded rectangle card floating in the middle of a gradient
- Glassmorphism (blur + white 10% border) applied to every element instead of one
- Emoji used as iconography or as bullet points
- Inter/Poppins/Montserrat at default tracking as the display face on a brand that has its own type
- Generic "abstract 3D blob" or "network of connected dots" background with no relation to the content
- Uniform slide layouts across a carousel with only the text swapped
- Stock-photo handshake / laptop-and-coffee / arrow-going-up-over-city energy
- Drop shadows on text
- Neon glow on everything
- Fake UI in mockups that has no relation to the actual product
- A rule-of-three list on every single slide
- Decorative dots/lines added "to fill space" — empty space is the design

## 7. Proposing a mini-system from nothing

When there's no system, ship one in three lines and move: a palette (ink + surface + one accent, pulled from the product or the subject matter), a type pair (one distinctive display face + one neutral text face), and a signature device. Bias the display face away from the safe defaults — geometric or grotesk with character (Space Grotesk, Archivo, Bricolage Grotesque, Instrument Serif, Fraunces, DM Serif Display) — and confirm it's actually installed or fetchable before designing around it (`references/render-pipeline.md`).

Sanity check the proposal by naming the feeling in one word (clinical / warm / brutalist / editorial / playful) and verifying all three choices serve that word. Three choices pulling in three directions is the most common cause of "it looks fine but off".

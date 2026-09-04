# SVG Craft — Custom Marks, Texture, Annotation, Charts

Everything here exists so a post never has to reach for an emoji, a stock icon set, or a charting library. Hand-built SVG is what separates a designed post from an assembled one, and it costs a few minutes.

## Contents
1. Working method
2. Icons and pictograms
3. Organic shapes and background structure
4. Texture: grain, halftone, hatching
5. Hand-drawn annotation
6. Charts by hand
7. Numbers and metric graphics
8. Isometric primitives
9. Debugging SVG

---

## 1. Working method

- Draw on a **24×24 or 100×100 viewBox** and scale with CSS. Consistent viewBox = consistent optical weight across a set.
- **Strokes, not fills, for icons**: `stroke="currentColor"`, `stroke-width="1.75"` on a 24-grid, `stroke-linecap="round"`, `fill="none"`. Then `color: var(--accent)` controls them from CSS.
- **`vector-effect="non-scaling-stroke"`** whenever a shape gets scaled or transformed, or stroke weights drift across the composition.
- Snap to the grid for geometric marks; deliberately break it for organic ones. Half-pixel coordinates on straight lines cause soft edges.
- Prefer one clever path over ten stacked rects. Fewer nodes = easier to restyle.
- Inline the SVG in the HTML (not `<img src>`) so it inherits tokens and can be animated or filtered.

## 2. Icons and pictograms

A usable icon is a metaphor reduced to 3–6 strokes. Build from primitives:

```html
<!-- cloud + downward cost arrow, 24 grid -->
<svg viewBox="0 0 24 24" width="64" fill="none" stroke="currentColor"
     stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
  <path d="M6.5 15a3.5 3.5 0 0 1 .4-7A5 5 0 0 1 17 8.6a3.2 3.2 0 0 1 .2 6.4"/>
  <path d="M12 11v7"/><path d="M9 15.5 12 18.5 15 15.5"/>
</svg>
```

For a set, hold these constant: viewBox, stroke width, corner radius language, and the amount of white space around the mark. Then vary only the metaphor.

**Custom brand-ish marks**: geometry + one asymmetry. A perfect circle is a shape; a circle with one flat side is a mark. Build from boolean-looking overlaps (two circles, one masked), a rotated square, or a monogram in the display face with one letterform modified.

**Pictograms > icons** for posts: a 240px pictogram (an illustrated object, drawn in the same stroke language, 12–25 paths) as the focal element beats a small icon plus lots of text. Draw the object as a silhouette first, then add only the internal lines that make it readable.

## 3. Organic shapes and background structure

Backgrounds should be *structure*, not decoration.

```html
<!-- blob: 4–6 anchor points, smooth C curves, never symmetric -->
<svg viewBox="0 0 400 400" width="720" style="position:absolute; inset:auto -80px -120px auto; opacity:.9">
  <path fill="var(--accent)" d="M212 24c66 6 132 44 148 108s-30 128-84 166-134 62-186 26S28 208 52 148 146 18 212 24Z"/>
</svg>
```

Structure options that read as intentional:
- **Grid field**: `<pattern>` of 1px lines at 48px spacing, 6–10% opacity, ink color. Instant "engineering" register.
- **Dot matrix**: 2px circles at 32px pitch, fading out with a mask.
- **Concentric arcs** radiating from an off-canvas center point — good behind a device.
- **Diagonal rules** at 62° in the accent at 8% opacity, spaced irregularly (12, 20, 14, 34px gaps) so it doesn't look machine-generated.
- **Radial glow**: `<radialGradient>` from accent at 45% alpha to transparent, positioned behind the focal element and *off-center*.

```html
<svg width="0" height="0"><defs>
  <pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse">
    <path d="M48 0H0v48" fill="none" stroke="var(--ink)" stroke-opacity=".07" stroke-width="1"/>
  </pattern>
</defs></svg>
<div style="position:absolute; inset:0">
  <svg width="100%" height="100%"><rect width="100%" height="100%" fill="url(#grid)"/></svg>
</div>
```

Masks make any of these look art-directed: fade the pattern out toward the type area with a `linearGradient` mask so the background never fights the message.

## 4. Texture: grain, halftone, hatching

**Grain** (in `canvas.css` as `.grain`, keep at 3–5%) removes digital flatness:

```html
<svg width="0" height="0"><filter id="grain">
  <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" stitchTiles="stitch"/>
  <feColorMatrix type="saturate" values="0"/>
</filter></svg>
<div class="grain" style="position:absolute;inset:0;filter:url(#grain);opacity:.04;pointer-events:none;mix-blend-mode:multiply"></div>
```

**Halftone** for a printed/editorial feel: a `<pattern>` of circles whose radius steps down across three tiles, masked over a shape. Strong on quote posts and photo treatments.

**Hatching** for shading illustrations: parallel 1.5px lines at 45°, spacing 6px for dark, 12px for mid. Applied as a pattern fill on the shadow side of a pictogram, it makes flat vector illustration look drawn.

## 5. Hand-drawn annotation

The difference between "annotated by a designer" and "annotated in Preview" is irregularity.

```html
<!-- hand-ish ellipse: 4 arcs with unequal radii, never a perfect ellipse -->
<path d="M118 26C182 18 246 40 244 74s-72 52-136 46S18 78 26 56 54 34 118 26Z"
      fill="none" stroke="var(--accent)" stroke-width="5" stroke-linecap="round"
      transform="rotate(-3 130 60)"/>

<!-- curved arrow with a hand-weighted head -->
<path d="M40 120C110 60 220 44 320 78" fill="none" stroke="var(--ink)" stroke-width="4.5" stroke-linecap="round"/>
<path d="M296 60l28 20-30 16" fill="none" stroke="var(--ink)" stroke-width="4.5"
      stroke-linecap="round" stroke-linejoin="round"/>
```

Other devices:
- **Numbered pins**: filled circle in accent, mono numeral in surface color, 44–56px diameter, with a 2px leader line to the target.
- **Underline scribble**: two overlapping quadratic curves under a word, slightly different, 6px stroke, ends overshooting the word by 8px.
- **Bracket callout**: a square bracket path spanning a UI region, with the label hanging off its middle.
- **Strikethrough**: a slightly angled line (−1.5°) drawn past both ends of the word, not a `text-decoration`.

Keep annotation to one color plus ink. Three annotation colors on one canvas is noise.

## 6. Charts by hand

Library defaults are recognizable and dull. Build the chart as a designed object with the data as the only source of geometry.

**Bars** — compute geometry in the markup, keep one baseline, kill gridlines, label only the hero bar:

```html
<svg viewBox="0 0 640 360" width="820">
  <!-- baseline only -->
  <line x1="0" y1="320" x2="640" y2="320" stroke="var(--ink)" stroke-opacity=".2"/>
  <!-- muted bars -->
  <rect x="24"  y="196" width="72" height="124" fill="var(--muted)" fill-opacity=".28" rx="4"/>
  <rect x="128" y="164" width="72" height="156" fill="var(--muted)" fill-opacity=".28" rx="4"/>
  <!-- hero bar -->
  <rect x="232" y="72"  width="72" height="248" fill="var(--accent)" rx="4"/>
  <text x="268" y="52" text-anchor="middle" font-family="var(--font-display)"
        font-size="40" font-weight="700" fill="var(--ink)">%38</text>
</svg>
```

**Sparkline / area**: one path for the line (3px, round caps), a second closed path for the fill at 12% accent, one dot at the last point with a 6px surface-colored ring, and one value label. No axes at all.

**Donut**: `<circle>` with `stroke-dasharray` = `[value% of circumference] [rest]`, `stroke-linecap="round"`, rotated −90°, plus the number set large in the hole. Two segments max — a donut with six slices is unreadable at feed scale.

**Waterfall / stacked cost bars** (FinOps content): stacked `<rect>`s in three tints of one hue, not three different hues, with the delta called out by a bracket and a number.

Chart rules for social: ≤ 7 data points, ≥ 48px bar width, labels ≥ 24px, one callout, no legend (label in place instead), y-axis usually omitted entirely. If the data genuinely needs a legend, it needs a carousel slide, not a chart.

## 7. Numbers and metric graphics

Numbers are the best focal element available for B2B/product posts.

- Set the metric in the display face, 160–320px, tabular figures, tight tracking.
- The unit (`%`, `₺`, `x`, `ms`) goes 40–50% of the numeral size, baseline-aligned or superscripted, in the accent.
- Add one piece of geometry: an underline rule at the numeral's exact width, a circle behind one digit, a small delta triangle + secondary number, or a partial arc showing progress.
- Two metrics side by side need visibly different sizes (hero + supporting), never equal weight.
- Negative/positive framing: use the palette, not red-green defaults — muted for the bad number, accent for the good one.

## 8. Isometric primitives

For `Isometric Stack` compositions, build planes as parallelograms rather than transforming HTML when precision matters:

```html
<!-- a 320×200 plane in isometric -->
<path d="M0 100 L160 10 L320 100 L160 190Z" fill="var(--surfaceAlt)"
      stroke="var(--ink)" stroke-opacity=".14"/>
```

Extrude by drawing the same shape offset down by the depth and connecting the two left/right corners with quads in a darker tint. Two tints per solid: top face light, side faces 12% and 24% darker. Consistent depth across all objects.

## 9. Debugging SVG

- Nothing renders → missing `viewBox`, or width/height of 0, or a `fill` inherited as `none`.
- Strokes look wrong after scaling → add `vector-effect="non-scaling-stroke"`.
- `<filter>` or `<pattern>` not applying → the `<defs>` must be in the same document, and IDs must be unique across the page (prefix per slide: `grid-s01`).
- Filters producing washed colors → add `color-interpolation-filters="sRGB"`.
- Blurry edges → non-integer coordinates on axis-aligned lines; snap to whole or half pixels.
- Text inside SVG not using the brand font → set `font-family` explicitly on the `<text>`; SVG doesn't inherit as reliably as HTML. Better: put text in HTML on top of the SVG.

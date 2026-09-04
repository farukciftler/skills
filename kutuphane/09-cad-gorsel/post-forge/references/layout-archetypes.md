# Layout Archetypes

18 compositions to pull from, so posts stop converging on the same centered card. Pick per canvas, deliberately, and record the pick. Adjacent carousel slides must not share an archetype.

Each entry: what it is → when it wins → the structural move that makes it work.

All snippets assume `canvas.css` and a 1080-wide canvas with `--gutter: 72px`.

---

## Typography-led

### 1. Poster Statement
One sentence set enormous (120–200px), 3–6 words, filling most of the canvas; everything else is a small mono label and the handle.
**Wins for**: hooks, hot takes, launch announcements, slide 1 of any carousel.
**Move**: the type must break the grid — set it to overflow the gutter on one side, or split it across lines with an intentional ragged edge and a color shift on the key word. Centered and perfectly balanced kills it.

```html
<div class="slide" data-name="01-hook">
  <span class="eyebrow">FinOps 101</span>
  <h1 class="display" style="font-size:168px; line-height:.94; letter-spacing:-.03em">
    Bulut faturası<br><em class="accent">tahmin</em> değildir
  </h1>
  <span class="handle">@cloud4next</span>
</div>
```

### 2. Big Numeral
A single metric at 200–320px as the entire subject, with a 2-line explanation beneath and a unit/label set small next to it.
**Wins for**: results, benchmarks, price points, before/after deltas.
**Move**: crop the numeral. Let it bleed off the top or right edge so it feels like a monument, and hang the label off its baseline. Use tabular figures and align the label to the numeral's optical edge, not its bounding box.

### 3. Text-as-Texture
The message repeated or a body of small type filling the canvas as a field, with one word or phrase knocked out in accent color / reversed / circled.
**Wins for**: "everyone says X, we do Y", noise-vs-signal ideas, myth-busting.
**Move**: the field must be real content (actual repeated phrase, actual list) at 20–24px, low contrast (muted), and the highlighted element must be the only high-contrast thing on the canvas.

### 4. Question Frame
A large question on the top half, a hard rule, and the answer withheld — or a one-word answer bottom-right.
**Wins for**: carousel slide 1, engagement bait that isn't cheap, teaching sequences.
**Move**: asymmetric split (60/40, never 50/50) and a rule that runs full bleed edge-to-edge to divide them.

---

## Image / mockup-led

### 5. Hero Device
One phone or laptop mockup at 55–75% of canvas height, angled or straight, headline above or beside it.
**Wins for**: app launches, feature reveals, UI showcases.
**Move**: crop the device — cut off the bottom third of the phone at the canvas edge so it reads as entering the frame. A fully visible floating device centered on a gradient is the archetype's failure state. Add a radial accent glow behind it, offset from center.

### 6. Screenshot Bleed
A real product screenshot fills 100% of the canvas, scrimmed, with type overlaid on the quiet region.
**Wins for**: dashboards, data-rich UIs, "look at the actual thing" posts.
**Move**: rotate 0°, scale 110–130% and offset so a meaningful UI region sits under the type-free zone; place a solid or 90%-opacity shape (not a soft gradient) behind the type block. Duotone the screenshot to brand colors so it doesn't fight the palette.

### 7. Device Cluster
Two or three devices at different scales and depths (phone front, laptop behind, watch small front-right), overlapping.
**Wins for**: cross-platform launches, ecosystem stories.
**Move**: one device is the hero at full contrast; the others are 60–80% scale and slightly desaturated. Consistent light direction across all shadows or the group looks pasted.

### 8. Isometric Stack
UI screens floating in a shared isometric projection, stacked with z-offset.
**Wins for**: flows, architecture, "three steps in the app".
**Move**: single shared skew matrix for every plane (see `mockups.md`), equal z-gaps, one connective element (a line, an arrow) threading the stack so it reads as a system not a pile.

### 9. Annotated Screenshot
Real screenshot with hand-drawn callouts: circles, arrows, numbered pins, cropped zoom-ins.
**Wins for**: teardowns, how-to, "we fixed this", before/after UX.
**Move**: annotations must look drawn, not office-suite — irregular ellipses via SVG path, arrows with slight curve and hand-weighted stroke (`svg-craft.md`). A zoom-in inset with a leader line to its source is the high-value detail.

### 10. Split Compare
Hard vertical or diagonal split, before on one side, after on the other, with a shared baseline label row.
**Wins for**: before/after, us-vs-them (unnamed), old-way/new-way.
**Move**: asymmetric split (55/45) plus one element crossing the divide to prevent it reading as two unrelated posters. Label with mono type at the same y on both sides. Diagonal splits need the type set upright, never rotated with the split.

---

## Diagram / structure-led

### 11. Flow Rail
Left-to-right or top-to-bottom sequence of 3–5 nodes with connectors.
**Wins for**: processes, pipelines, funnels, migration paths.
**Move**: nodes vary in size by importance, connectors are hand-weighted curves, and one node is the accent — a flow where everything is equal teaches nothing.

### 12. Quadrant / Matrix
2×2 with axis labels, items plotted, one quadrant highlighted.
**Wins for**: positioning, decision frameworks, tradeoffs.
**Move**: the axes are the design — set them as thin ink rules with mono labels rotated 90° on the y. Fill only the winning quadrant with a tint. Plot 4–7 items max.

### 13. Hand-built Chart
Bars, sparkline, donut, or stacked area drawn as SVG in brand colors with intentional typography, one value called out.
**Wins for**: FinOps/cost/metric content, growth, benchmarks.
**Move**: never a library default. Kill the gridlines, keep one baseline, label the one bar that matters and mute the rest. Bar widths ≥ 48px on a 1080 canvas. See `svg-craft.md`.

### 14. Layered Stack Diagram
Horizontal bands stacked as a system (infra → platform → app), with side annotations.
**Wins for**: architecture, "where we sit in your stack", technical explainers.
**Move**: bands differ in height by importance, not uniformly; one band is the brand's layer and gets the accent + a callout pulling out to the margin.

### 15. Checklist / Ledger
A list rendered as a designed object: numbered rows with rules, mono numerals, strikethroughs, checkmarks drawn by hand.
**Wins for**: audit findings, "5 things", takeaway slides.
**Move**: rows are separated by hairline rules to full bleed, numerals sit in the margin outside the text block, and one row is emphasized by inversion (accent bar behind it). Max 5 rows.

---

## Editorial / graphic

### 16. Editorial Grid
Magazine spread logic: a 12-column grid, a small headline in a corner, a large image or shape block, a pull quote, a folio number. Deliberately uneven air.
**Wins for**: thought-leadership on LinkedIn, brand-building sets, quote posts.
**Move**: put something in a corner nobody uses and leave a large area genuinely empty. The confidence of the empty space is the design.

### 17. Sticker / Collage
Elements at slight rotations layered with visible edges: torn paper, tape, index cards, a cutout screenshot, a scribble.
**Wins for**: playful brands, community posts, recaps, hiring posts.
**Move**: 3–7 elements, rotations between −6° and +6° but never 0° for all, real drop shadows implying physical stacking, and one element deliberately cropped at the canvas edge. Keep the palette tight or it becomes chaos.

### 18. Frame-in-Frame
A hard geometric frame (rule box, notched corner, ticket stub, terminal window chrome) containing the content, with something breaking out of the frame.
**Wins for**: series branding, quotes, code/terminal content, recurring formats.
**Move**: the break-out element is mandatory — a subject's shoulder, a number, an arrow crossing the frame edge. Without it, this is just a border.

---

## Choosing fast

| The post's job | First choices |
|---|---|
| Stop the scroll | 1 Poster Statement, 2 Big Numeral, 3 Text-as-Texture |
| Show the product | 5 Hero Device, 6 Screenshot Bleed, 9 Annotated Screenshot |
| Prove a result | 2 Big Numeral, 13 Hand-built Chart, 10 Split Compare |
| Teach a process | 11 Flow Rail, 8 Isometric Stack, 15 Checklist |
| Position / strategy | 12 Quadrant, 14 Layered Stack, 16 Editorial Grid |
| Build brand character | 16 Editorial Grid, 17 Sticker Collage, 18 Frame-in-Frame |

Combine at most two archetypes per canvas. Three is clutter, and clutter at feed scale is invisible.

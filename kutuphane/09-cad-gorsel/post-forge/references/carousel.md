# Carousels — Instagram & LinkedIn Documents

A carousel is a sequence, not a folder of images. Two things decide whether it gets swiped: slide 1's stopping power, and whether each slide creates a reason to see the next one. Two things decide whether it looks professional: a repeating signature device, and visibly different compositions inside that repetition.

## Contents
1. Platform specs
2. Narrative arcs
3. Slide-by-slide variation rule
4. Continuity devices
5. Swipe-forward mechanics
6. Slide 1 and the last slide
7. Build and export
8. Review gate

---

## 1. Platform specs

**Instagram carousel**
- Up to 20 slides; the sweet spot for teaching content is 6–10.
- 1080 × 1350 (4:5) for all slides. Uniform ratio — mixed ratios cause crops.
- Slide 1 is also the grid thumbnail: it must survive a 4:5 grid crop and read at ~200px.
- Slides 2+ are seen only after a swipe, so front-load the value but keep a reason to continue.

**LinkedIn document post (the real "LinkedIn carousel")**
- A PDF uploaded as a document. Pages become swipeable in the feed.
- Design pages at 1080 × 1350, export one PDF (`scripts/render.py --pdf`).
- The desktop feed viewer trends toward square: keep the critical read inside the central 1080 × 1080 of each page, and never put a headline in the bottom 200px.
- 5–12 pages. LinkedIn shows a page counter, so a "1/8" indicator of your own is redundant but harmless.
- Page 1 needs a title that works with no caption context, because the feed truncates the post text.

**Story sequence** (adjacent use case): 1080 × 1920, everything vital inside the central 1080 × 1420, 3–7 frames, and the tap target zone (bottom right) kept clear of content.

## 2. Narrative arcs

Pick one and hold it; a carousel with two arcs feels like two posts.

| Arc | Shape | Fits |
|---|---|---|
| **Problem → Cost → Fix → Proof → CTA** | 5–7 slides | B2B/product, FinOps, SaaS |
| **Myth → Reality** (alternating pairs) | 6–8 slides | opinion, education, category building |
| **Numbered list** (one idea per slide) | 5–10 slides | "5 things", tips, checklists |
| **Teardown** (screenshot → annotation → verdict per item) | 6–9 slides | UX/product critique, audits |
| **Before → After → How** | 4–6 slides | case studies, redesigns, migrations |
| **Step-by-step walkthrough** | 5–9 slides | tutorials, onboarding flows |
| **Timeline / journey** | 5–8 slides | launches, retrospectives, roadmaps |

One idea per slide. If a slide needs two headlines, it's two slides.

## 3. Slide-by-slide variation rule

Before rendering, write the plan as a table — this is the mechanism that prevents template output:

| # | Archetype | Focal | Value | Density |
|---|---|---|---|---|
| 01 | 1 Poster Statement | type | dark | 1 line |
| 02 | 2 Big Numeral | numeral | light | number + 2 lines |
| 03 | 9 Annotated Screenshot | mockup | light | dense |
| 04 | 13 Hand-built Chart | chart | dark | medium |
| 05 | 15 Checklist | list | light | dense |
| 06 | 5 Hero Device | mockup | dark | 1 line + CTA |

Constraints:
- No two adjacent slides share an archetype.
- Alternate light and dark surfaces at least twice across the set — the value rhythm is what makes swiping feel like progress.
- At most two slides may be text-only, and never adjacent.
- Every slide shares the signature device and the type system.

## 4. Continuity devices

Pick two, use them on every slide:

- **Persistent slot**: the same 72px-tall zone at top or bottom carrying an eyebrow label + slide number, identical position on all slides.
- **Progress rule**: a hairline at the bottom whose accent-filled portion grows slide to slide. Cheap, and it visibly rewards swiping.
- **Bleeding element**: a shape, rule, or arc that exits the right edge of slide *n* and re-enters the left edge of slide *n+1* at the same y. Strongest continuity trick available; requires designing the pair together.
- **Fixed corner mark**: logo or monogram in the same corner at the same size throughout.
- **Palette rhythm**: a fixed sequence (dark, light, light, accent, light, dark) rather than random per-slide choices.

Avoid: putting the logo big on every slide, repeating the full CTA on every slide, and numbering slides in a different position each time.

## 5. Swipe-forward mechanics

Each slide should end with an open loop:
- Cut a sentence mid-thought and complete it on the next slide (works once per carousel, not repeatedly).
- Show the number before the explanation.
- A visual promise: an arrow or partial element pointing off the right edge.
- Contrast setup: "Most teams do this →" with the alternative held back.

Never use "Swipe →" as text on every slide; once, on slide 1, is the maximum, and even that is often unnecessary if the composition points right.

## 6. Slide 1 and the last slide

**Slide 1** carries the whole carousel. It needs: one specific claim (numbers and specifics beat abstractions), type large enough to read at 200px, and no more than 8 words. It must work as a standalone image because that's how it appears in the grid and in the feed before any swipe. Design it last, after the content exists — a hook written before the substance tends to overpromise.

**Last slide**: one action, stated plainly, with room around it. Follow/save/comment-a-word/link-in-bio — one, not four. A visual echo of slide 1 (same archetype, resolved statement) closes the loop and reads as intentional. If the brand runs a series, the last slide is where the series mark lives.

## 7. Build and export

One HTML file, all slides as siblings, so continuity is visible while designing:

```html
<link rel="stylesheet" href="canvas.css">
<div class="deck">
  <div class="slide" data-name="01-hook"     style="--w:1080px; --h:1350px">…</div>
  <div class="slide" data-name="02-metric"   style="--w:1080px; --h:1350px">…</div>
</div>
```

```bash
# Instagram: numbered PNGs
python scripts/render.py deck.html --out out/ --scale 2

# LinkedIn: same slides, one PDF
python scripts/render.py deck.html --out out/ --scale 2 --pdf out/carousel.pdf
```

Filenames come from `data-name`, zero-padded so upload order is correct — Instagram's picker respects filename order and a mis-ordered carousel is a re-upload.

Unique IDs per slide for SVG `<defs>` (`grid-s01`, `grid-s02`); duplicate IDs across slides make filters and patterns bind to the wrong element and produce inconsistent renders.

## 8. Review gate

Run `scripts/contact_sheet.py out/ --thumb 220` and check the grid as a whole:

- Slide 1 readable and compelling at thumbnail size
- The set is obviously one family (signature device, palette, type)
- Adjacent slides look visibly different in composition
- Light/dark rhythm visible in the strip
- Continuity device present and in the same position on every slide
- No slide is a wall of text
- Last slide has exactly one call to action
- LinkedIn only: critical content inside the central square, nothing important in the bottom 200px
- Page/slide count matches what the caption promises

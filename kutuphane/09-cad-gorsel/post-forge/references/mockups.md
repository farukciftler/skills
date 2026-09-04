# Mockups — Devices, Browsers, UI Frames

Credible mockups are mostly geometry: correct aspect ratio, correct corner-radius nesting, one light direction, and no stretching. Get those four right and a hand-built frame beats a stock PSD, because it's vector, on-brand, and re-renders instantly.

## Contents
1. Universal rules
2. Phone frame
3. Browser window
4. Laptop
5. Tablet, watch, floating UI cards
6. Perspective and isometric
7. Screenshot treatment (duotone, crop, zoom inset)
8. Building fake-but-honest UI when there's no screenshot
9. Failure checklist

---

## 1. Universal rules

- **Aspect ratios are not negotiable.** Phone screen 19.5:9 (0.4615). Laptop screen 16:10. Tablet 4:3 or 4.3:3. Watch ~1.19:1. Browser viewport 16:10 or 16:9 minus chrome. A stretched screenshot is the single most noticeable amateur tell.
- **Nested radii.** Inner radius = outer radius − bezel width. Frame 62px with a 12px bezel → screen radius 50px. Equal radii on both makes the bezel look like a sticker.
- **One light source.** Pick top-left. Every shadow points down-right, every highlight sits top-left. Consistent across every object on the canvas including non-device shapes.
- **`object-fit: cover` with an explicit `object-position`**, never `100% 100%`.
- **Crop devices at the canvas edge** whenever the composition allows. Fully-contained floating devices read as stock; a phone entering from the bottom edge reads as art direction.
- **Generic hardware.** No manufacturer logos or trade dress details used as branding.

## 2. Phone frame

Pure CSS, screenshot-friendly. Sized by one variable so it scales inside any composition.

```html
<div class="phone" style="--pw: 420px">
  <div class="phone-screen">
    <img src="app.png" alt="">
    <div class="phone-island"></div>
  </div>
</div>
```

```css
.phone{
  --pw: 420px;                 /* only knob you touch */
  --bezel: calc(var(--pw) * .029);
  width: var(--pw);
  aspect-ratio: 9 / 19.5;
  border-radius: calc(var(--pw) * .148);
  padding: var(--bezel);
  background: linear-gradient(145deg, #2a2f36, #0d1013 55%, #23282e);
  box-shadow:
    0 2px 4px rgba(0,0,0,.22),
    0 60px 90px -30px rgba(0,0,0,.55),
    inset 0 0 0 1px rgba(255,255,255,.10);
}
.phone-screen{
  position: relative; width: 100%; height: 100%; overflow: hidden;
  border-radius: calc(var(--pw) * .148 - var(--bezel));
  background: var(--surface);
}
.phone-screen img{ width:100%; height:100%; object-fit:cover; object-position: top center; display:block; }
.phone-island{
  position:absolute; top: calc(var(--pw)*.026); left:50%; transform:translateX(-50%);
  width: calc(var(--pw)*.26); height: calc(var(--pw)*.075);
  border-radius: 999px; background:#07090b;
}
/* optional side buttons — small detail, big credibility */
.phone::after, .phone::before{
  content:""; position:absolute; width:3px; border-radius:2px; background:#1b2026;
}
```

Tune: `--pw` 380–520px for a hero on a 1080 canvas; 200–260px when clustered. Drop the island for an Android-ish frame and use a 6px centered punch-hole instead.

## 3. Browser window

For web app / dashboard / landing page screenshots. Chrome height scales with width; keep it subtle — the content is the point.

```html
<div class="win" style="--ww: 900px">
  <div class="win-bar">
    <span class="dot"></span><span class="dot"></span><span class="dot"></span>
    <div class="win-url">cloud4next.com/dashboard</div>
  </div>
  <div class="win-body"><img src="dash.png" alt=""></div>
</div>
```

```css
.win{ --ww:900px; width:var(--ww); border-radius:14px; overflow:hidden;
  background:#fff; box-shadow:0 1px 3px rgba(0,0,0,.18), 0 48px 80px -24px rgba(0,0,0,.42); }
.win-bar{ height:calc(var(--ww)*.048); display:flex; align-items:center; gap:8px;
  padding:0 16px; background:#e9ecef; border-bottom:1px solid rgba(0,0,0,.07); }
.dot{ width:11px; height:11px; border-radius:50%; background:#c8ced4; }
.win-url{ margin-left:12px; flex:1; max-width:52%; height:60%; border-radius:999px;
  background:#fff; color:#6B7683; font: 500 15px/1.9 var(--font-mono);
  padding:0 14px; overflow:hidden; white-space:nowrap; }
.win-body{ aspect-ratio:16/10; }
.win-body img{ width:100%; height:100%; object-fit:cover; object-position: top left; }
```

Variants worth using: **dark chrome** (`#2b3036` bar, `#3a4048` dots) for developer-audience posts; **terminal window** — same frame, body is `--ink` background with mono text at 26–30px, one accent-colored output line, and a block cursor. Terminal windows are excellent for FinOps/dev content and cost nothing to build.

## 4. Laptop

Two rectangles and a trapezoid. Don't over-render it.

```html
<div class="laptop" style="--lw: 820px">
  <div class="lid"><div class="lid-screen"><img src="dash.png" alt=""></div></div>
  <div class="base"></div>
</div>
```

```css
.laptop{ --lw:820px; width:var(--lw); }
.lid{ width:100%; aspect-ratio:16/10.6; padding:calc(var(--lw)*.012);
  border-radius:calc(var(--lw)*.018) calc(var(--lw)*.018) 2px 2px;
  background:linear-gradient(160deg,#3a4046,#1a1e22);
  box-shadow: 0 40px 60px -28px rgba(0,0,0,.5); }
.lid-screen{ width:100%; height:100%; overflow:hidden; border-radius:calc(var(--lw)*.008); background:#000; }
.lid-screen img{ width:100%; height:100%; object-fit:cover; object-position:top left; }
.base{ width:112%; margin-left:-6%; height:calc(var(--lw)*.022);
  background:linear-gradient(#c9ced4,#8d949b);
  clip-path: polygon(1.4% 0, 98.6% 0, 100% 100%, 0 100%);
  border-radius: 0 0 calc(var(--lw)*.01) calc(var(--lw)*.01); }
```

Add a 3–4% wide notch as a `::after` on `.base` centered at the top for the trackpad cutout illusion. For dark hardware, swap the base gradient to `#4a5057 → #23272b`.

## 5. Tablet, watch, floating UI cards

- **Tablet**: same recipe as the phone with `aspect-ratio: 3/4.3`, bezel `1.8%` of width, radius `4.5%`, no island.
- **Watch**: `aspect-ratio: 1/1.19`, radius 26% of width, thick bezel (5%), and a small crown as a 4×22px rounded rect on the right edge. Screen content should be one glanceable metric — a watch mockup with dense UI is unreadable and pointless.
- **Floating UI cards** are often better than a whole device: lift one component out of the product (a cost breakdown card, a notification, a chart tile, a toast) and render it standalone at 1.5–2× real scale with a real shadow, tilted 2–4°, partially overlapping the headline. This is the highest-impact-per-effort mockup in the whole file — it shows the product without asking the viewer to squint at a 380px phone screen. Stack two or three at different z-depths for a "system" feel.

```css
.uicard{ background:var(--surface); border-radius:20px; padding:28px 32px;
  box-shadow:0 2px 6px rgba(11,15,20,.06), 0 40px 60px -24px rgba(11,15,20,.28);
  transform: rotate(-2.5deg); }
```

## 6. Perspective and isometric

**Perspective (a device turned in space)** — use a real 3D transform on the parent so children stay sharp:

```css
.scene{ perspective: 2400px; }
.scene .phone{ transform: rotateY(-18deg) rotateX(4deg) rotateZ(-2deg); transform-style: preserve-3d; }
```

Keep `rotateY` between 10–22°. Beyond that the screen content becomes unreadable and the illusion needs edge thickness you haven't modeled.

**Isometric (a stack of planes)** — one shared matrix for every plane, no exceptions:

```css
.iso{ transform: matrix(1, .34, -1, .34, 0, 0) scale(.86); }  /* ~true isometric */
.iso-stack > *{ position:absolute; }
/* z-offsets: each layer up = translate(-Npx, -N*.58px) applied BEFORE the matrix */
```

Rules: equal z-gaps (72–120px), consistent shadow offset per layer, and a connector (line, arrow, dotted path) threading the layers. Text inside isometric planes must be ≥ 34px pre-transform or it dies; better still, keep labels *outside* the projection, flat and horizontal, with leader lines pointing in.

## 7. Screenshot treatment

Raw screenshots usually clash with the palette. Fix them:

**Duotone to brand colors** (SVG filter, applies to any `<img>`):

```html
<svg width="0" height="0" style="position:absolute">
  <filter id="duo" color-interpolation-filters="sRGB">
    <feColorMatrix type="matrix" values="
      .33 .33 .33 0 0
      .33 .33 .33 0 0
      .33 .33 .33 0 0
      0 0 0 1 0"/>
    <feComponentTransfer>
      <feFuncR type="table" tableValues="0.043 0.184 1"/>   <!-- shadow→highlight R -->
      <feFuncG type="table" tableValues="0.059 0.420 1"/>
      <feFuncB type="table" tableValues="0.078 1.000 1"/>
    </feComponentTransfer>
  </filter>
</svg>
<img src="dash.png" style="filter:url(#duo)">
```

Set the three `tableValues` triplets from your `--ink`, `--accent`, and `--surface` RGB values divided by 255. Result: the screenshot becomes brand-colored and the design holds together.

Other reliable moves:
- **Crop hard.** Show one region of the UI at 200% rather than the whole screen at 40%. Nobody reads a full dashboard in a feed.
- **Zoom inset**: a small rounded rect showing a magnified detail, connected to its source with two thin leader lines and a matching stroke box on the source region.
- **Scrim before type**: solid or ≥90% opacity shape, not a soft gradient, behind any text over a screenshot.
- **Blur the noise**: `filter: blur(3px)` on the parts of a screenshot that aren't the point, focus sharp on the one that is.
- **Redact real data**: replace customer names/emails with plausible placeholders before publishing — check every screenshot for leaked account data.

## 8. Fake-but-honest UI

When there's no screenshot, build the UI in HTML rather than drawing a fuzzy approximation. A convincing mini-UI needs only: a header row with a title and one icon, 2–4 rows or tiles with real-looking labels, one number per tile with a tabular font, one small chart (`svg-craft.md`), and one accent element (a badge, a positive delta, a selected state). Use the product's real vocabulary — actual feature names, actual metric names, plausible values.

Two honesty rules: the numbers must be plausible-but-labeled-illustrative in the delivery note, and never invent a feature that doesn't exist without flagging it.

## 9. Failure checklist

- Screenshot stretched or squashed (check the ratio, not the vibe)
- Equal inner and outer radius → bezel looks fake
- Shadows in different directions across objects on the same canvas
- Device centered and fully visible on a gradient with no crop → stock look
- Phone screen content at real 1× scale → unreadable; zoom the UI inside the frame
- Isometric planes with slightly different skews → the stack looks wobbly
- Terminal or code text below 24px
- Real customer data visible in the screenshot

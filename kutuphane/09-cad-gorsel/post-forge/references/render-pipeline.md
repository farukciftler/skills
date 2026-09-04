# Render Pipeline

Read before the first render. Most "the design looks wrong" reports are a font that didn't load or a scale factor that halved the resolution.

## Contents
1. One-time setup
2. Rendering
3. Fonts (the biggest failure source)
4. Scale, crispness, file size
5. PDF for LinkedIn
6. Reviewing output
7. Troubleshooting

---

## 1. One-time setup

```bash
pip install playwright pillow
playwright install chromium
```

If Chromium can't be installed (locked-down environment), fall back in this order:
1. System Chrome/Chromium in headless mode:
   `chromium --headless=new --screenshot=out.png --window-size=1080,1350 --hide-scrollbars --force-device-scale-factor=2 file:///abs/path/post.html`
   (one canvas per file — no per-element cropping, so give each slide its own HTML file)
2. `rsvg-convert` or `resvg` for pure-SVG deliverables: `rsvg-convert -w 2160 in.svg -o out.png`
3. Last resort: deliver the HTML and tell the user to screenshot it themselves at 2× — but flag clearly that the visual gate in SKILL.md Step 5 could not be run.

## 2. Rendering

```bash
python scripts/render.py post.html --out out/ --scale 2
python scripts/render.py deck.html --out out/ --scale 2 --pdf out/carousel.pdf
python scripts/render.py post.html --out out/ --scale 2 --only 01-hook
```

What the script does: loads the file, waits for fonts and images, finds every `.slide`, reads `--w`/`--h` from its inline style (or measures it), sets the viewport to match, and screenshots each element to `NN-name.png` at the requested device scale factor. `--pdf` composes the PNGs into a single PDF at page-per-slide.

Always pass an absolute path or run from the file's directory; relative asset paths break under `file://` otherwise.

## 3. Fonts

**Silent fallback is the enemy.** A headless Linux Chromium often has only DejaVu, so a design built around Space Grotesk renders in something else and every measurement you tuned is wrong.

Check what's available before designing:

```bash
fc-list : family | sort -u | head -50
```

Then pick one strategy:

**A. Google Fonts over the network** (simplest when the box has internet):
```html
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;600&display=block" rel="stylesheet">
```
Use `display=block`, not `swap` — `swap` can screenshot the fallback.

**B. Local files, base64-embedded** (offline-safe, and the only reliable option for licensed brand fonts the user supplies):
```bash
base64 -w0 BrandFont.woff2 > f.b64
```
```css
@font-face{ font-family:"Brand"; src:url(data:font/woff2;base64,…) format("woff2");
  font-weight:700; font-display:block; }
```

**C. Install into the system** then reference normally:
```bash
mkdir -p ~/.local/share/fonts && cp *.woff2 *.ttf ~/.local/share/fonts/ && fc-cache -f
```

Verify after rendering, not before: open the PNG and confirm the letterforms are the intended face. A quick programmatic check is to measure a known string's width in the browser and compare against the fallback — but eyeballing the render is faster and catches more.

Turkish glyph check: render `ığüşöçİĞÜŞÖÇ` in the display face and confirm no missing-glyph boxes and that the dotless `ı` exists. Many display fonts fail this.

Variable fonts: pin the axes explicitly (`font-variation-settings: "wght" 640`) — headless rendering doesn't always resolve `font-weight` on variable faces the way a desktop browser does.

## 4. Scale, crispness, file size

- Design in CSS pixels at the canvas size (1080 × 1350) and render with `--scale 2` → a 2160 × 2700 PNG. Both platforms downscale it, and the supersampled result looks noticeably sharper than a native 1080 render.
- Instagram re-compresses uploads; upload the 2× PNG (or a 1080-wide PNG downsampled with Lanczos) rather than a JPEG. `--downsample 1080` in `render.py` writes both.
- Keep PNGs under ~8 MB. Full-canvas photos plus grain can blow past that — use `--jpeg 92` for photo-heavy canvases, PNG for type/vector-heavy ones.
- Grain and noise filters increase file size a lot at 2×. If size becomes a problem, apply grain at a lower `baseFrequency` or accept 1.5× scale.

## 5. PDF for LinkedIn

`--pdf` builds the PDF from the rendered PNGs, one page per slide, page size matching the canvas ratio exactly — this preserves the design pixel-for-pixel and avoids Chromium's print-CSS differences (which reflow layouts and shift type). Verify page count and order in the output before delivery.

Keep the PDF under 100 MB and 300 pages (LinkedIn's limits are far above any sane carousel). Name the file something meaningful — LinkedIn shows the filename on the document card, so `bulut-maliyet-rehberi.pdf` beats `deck-final-v3.pdf`.

## 6. Reviewing output

```bash
python scripts/contact_sheet.py out/ --thumb 220 --out out/_contact.png
```

Then **open the images** with the image-viewing tool. The contact sheet at 220px is the feed-scroll simulation: if the primary message doesn't survive it, the design fails regardless of how good it looks at full size. Also open at least one full-size PNG per set to catch clipping and font problems that thumbnails hide.

## 7. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| Wrong typeface in the render | Font never loaded. Check `fc-list`, switch to base64 embedding, use `font-display:block`. |
| Blurry output | `--scale 1`, or an upscaled raster asset. Render at 2×; source screenshots must be ≥ target pixel size. |
| Text clipped at the bottom | Fixed-height container plus grown content. Never fix a container height around text; cut words or reduce type within the floors. |
| Thin white seam at an edge | Sub-pixel rounding. Set the background on `.slide` itself and inset children by whole pixels. |
| Scrollbar in the screenshot | Content overflows the canvas. `--hide-scrollbars` masks it; find the overflowing element instead. |
| Images missing | Relative path under `file://`. Use paths relative to the HTML file and render from its directory. |
| Emoji rendered as boxes | No emoji font installed — which is fine, because emoji shouldn't be in the design. Replace with SVG. |
| SVG filter applied to the wrong slide | Duplicate `<defs>` IDs across slides. Suffix per slide. |
| Shadows cropped off | The screenshot clips to the element box. Keep shadows inside the canvas or add the shadow to an inner wrapper. |
| Colors look different from the design | A filter without `color-interpolation-filters="sRGB"`, or a `mix-blend-mode` interacting with a transparent canvas background. Set an explicit background. |
| Render hangs | A network font or image request that never resolves. Run with `--timeout 20` and embed assets locally. |

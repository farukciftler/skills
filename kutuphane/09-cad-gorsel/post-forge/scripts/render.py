#!/usr/bin/env python3
"""Render post-forge HTML canvases to pixel-exact PNGs (and an optional PDF).

Finds every element with class "slide", reads its declared --w/--h, screenshots it
at the requested device scale factor, and names the file from data-name.

    python scripts/render.py post.html --out out/ --scale 2
    python scripts/render.py deck.html --out out/ --scale 2 --pdf out/carousel.pdf
    python scripts/render.py deck.html --out out/ --only 03-chart --downsample 1080

Requires: pip install playwright pillow && playwright install chromium
"""
import argparse
import json
import pathlib
import sys

MEASURE_JS = """
() => Array.from(document.querySelectorAll('.slide')).map((el, i) => {
  const cs = getComputedStyle(el);
  const w = parseFloat(cs.getPropertyValue('--w')) || el.getBoundingClientRect().width;
  const h = parseFloat(cs.getPropertyValue('--h')) || el.getBoundingClientRect().height;
  const r = el.getBoundingClientRect();
  return {
    index: i,
    name: el.dataset.name || ('slide-' + String(i + 1).padStart(2, '0')),
    declared: [Math.round(w), Math.round(h)],
    actual: [Math.round(r.width), Math.round(r.height)],
    scrollOverflow: [el.scrollWidth - Math.round(r.width), el.scrollHeight - Math.round(r.height)],
    fonts: Array.from(new Set(Array.from(el.querySelectorAll('*'))
      .map(n => getComputedStyle(n).fontFamily.split(',')[0].replace(/["']/g, '').trim())
      .filter(Boolean))).slice(0, 8)
  };
})
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html", help="path to the HTML file containing .slide elements")
    ap.add_argument("--out", default="out", help="output directory")
    ap.add_argument("--scale", type=float, default=2.0, help="device scale factor (2 recommended)")
    ap.add_argument("--only", default=None, help="render only slides whose data-name contains this")
    ap.add_argument("--pdf", default=None, help="also write a PDF with one page per slide")
    ap.add_argument("--downsample", type=int, default=None,
                    help="also write a Lanczos-downsampled copy at this pixel width")
    ap.add_argument("--jpeg", type=int, default=None, help="write JPEG at this quality instead of PNG")
    ap.add_argument("--timeout", type=int, default=30, help="seconds to wait for assets")
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("playwright missing → pip install playwright && playwright install chromium\n"
                 "See references/render-pipeline.md for headless-Chrome fallbacks.")

    src = pathlib.Path(args.html).resolve()
    if not src.exists():
        sys.exit(f"not found: {src}")
    outdir = pathlib.Path(args.out).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    written, report = [], []

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--force-color-profile=srgb", "--font-render-hinting=none"])
        page = browser.new_page(viewport={"width": 1400, "height": 1000},
                                device_scale_factor=args.scale)
        page.goto(src.as_uri(), wait_until="load", timeout=args.timeout * 1000)
        try:
            page.wait_for_function("document.fonts.status === 'loaded'", timeout=args.timeout * 1000)
        except Exception:
            print("!! fonts never reported loaded — verify the typeface in the render "
                  "(references/render-pipeline.md §3)")
        page.wait_for_timeout(350)  # let filters/patterns settle

        slides = page.evaluate(MEASURE_JS)
        if not slides:
            browser.close()
            sys.exit("no .slide elements found — each canvas needs class=\"slide\"")

        handles = page.query_selector_all(".slide")
        for meta, el in zip(slides, handles):
            if args.only and args.only not in meta["name"]:
                continue
            dw, dh = meta["declared"]
            aw, ah = meta["actual"]
            if (dw, dh) != (aw, ah):
                print(f"!! {meta['name']}: declared {dw}x{dh} but laid out {aw}x{ah}")
            ox, oy = meta["scrollOverflow"]
            if ox > 1 or oy > 1:
                print(f"·· {meta['name']}: content extends {ox}x{oy}px past the canvas. "
                      f"Deliberate bleed is fine; clipped TEXT is not — check the render.")

            # viewport must fit the slide or the element screenshot can clip
            page.set_viewport_size({"width": max(aw + 80, 400), "height": max(ah + 80, 400)})
            el.scroll_into_view_if_needed()

            ext = "jpg" if args.jpeg else "png"
            idx = str(meta["index"] + 1).zfill(2)
            name = meta["name"]
            fname = name if name[:2].isdigit() else f"{idx}-{name}"
            path = outdir / f"{fname}.{ext}"
            kw = {"path": str(path)}
            if args.jpeg:
                kw.update(type="jpeg", quality=args.jpeg)
            el.screenshot(**kw)
            written.append(path)
            report.append({**meta, "file": path.name,
                           "pixels": [int(aw * args.scale), int(ah * args.scale)]})
            print(f"✓ {path.name}  {int(aw*args.scale)}x{int(ah*args.scale)}  fonts={meta['fonts'][:3]}")

        browser.close()

    if args.downsample or args.pdf:
        try:
            from PIL import Image
        except ImportError:
            sys.exit("pillow missing → pip install pillow")

        if args.downsample:
            sub = outdir / f"w{args.downsample}"
            sub.mkdir(exist_ok=True)
            for f in written:
                im = Image.open(f).convert("RGB")
                h = round(im.height * args.downsample / im.width)
                im.resize((args.downsample, h), Image.LANCZOS).save(sub / f.name)
            print(f"✓ downsampled copies → {sub}")

        if args.pdf:
            pages = [Image.open(f).convert("RGB") for f in written]
            if pages:
                pdf = pathlib.Path(args.pdf).resolve()
                pdf.parent.mkdir(parents=True, exist_ok=True)
                pages[0].save(pdf, save_all=True, append_images=pages[1:],
                              resolution=144.0)
                print(f"✓ {pdf.name}  {len(pages)} pages")

    (outdir / "_render.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\n{len(written)} file(s) → {outdir}\n"
          f"Next: python scripts/contact_sheet.py {outdir} --thumb 220, then OPEN the images.")


if __name__ == "__main__":
    main()

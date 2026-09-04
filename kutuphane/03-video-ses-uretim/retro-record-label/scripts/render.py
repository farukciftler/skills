#!/usr/bin/env python3
"""render — HTML cover canvas -> pixel-exact square PNG.

Type goes on last, in HTML, because that is the only way to get real kerning,
optical sizing and a layout you can nudge by one pixel. The treated plate from
darkroom.py sits underneath as a background image.

    python scripts/render.py cover.html --out out/ --size 3000
    python scripts/render.py covers.html --out out/ --size 3000 --only 02-
    python scripts/render.py cover.html --out out/ --size 3000 --jpeg 92

Every element with class "cover" is exported, named from its data-name.
Design at 1000×1000 CSS px and let --size do the upscaling: the script sets the
device scale factor to size/1000 so 3000 comes out supersampled and crisp.

Before it saves, it reports each canvas's overflow and the fonts that actually
resolved — a silent font fallback is the single most common reason a cover looks
wrong, and it is invisible in the code.
"""
import argparse
import json
import pathlib
import sys

MEASURE = """
() => Array.from(document.querySelectorAll('.cover')).map((el, i) => {
  const cs = getComputedStyle(el);
  const w = parseFloat(cs.getPropertyValue('--w')) || el.getBoundingClientRect().width;
  const h = parseFloat(cs.getPropertyValue('--h')) || w;
  const r = el.getBoundingClientRect();
  const fonts = Array.from(new Set(Array.from(el.querySelectorAll('*'))
    .filter(n => Array.from(n.children).every(c => c.tagName === 'BR') && n.textContent.trim().length > 0)
    .map(n => getComputedStyle(n).fontFamily.split(',')[0].replace(/["']/g, '').trim())
    .filter(Boolean)));
  return {
    index: i,
    name: el.dataset.name || ('cover-' + String(i + 1).padStart(2, '0')),
    declared: [Math.round(w), Math.round(h)],
    actual: [Math.round(r.width), Math.round(r.height)],
    overflow: [el.scrollWidth - Math.round(r.width), el.scrollHeight - Math.round(r.height)],
    fonts: fonts.slice(0, 8)
  };
})
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html")
    ap.add_argument("--out", default="out")
    ap.add_argument("--size", type=int, default=3000, help="final pixel width (default 3000)")
    ap.add_argument("--only", default=None, help="render only canvases whose data-name contains this")
    ap.add_argument("--jpeg", type=int, default=None, help="also write JPEG at this quality")
    ap.add_argument("--timeout", type=int, default=30)
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("playwright missing -> pip install playwright && playwright install chromium")

    src = pathlib.Path(args.html).resolve()
    if not src.exists():
        sys.exit(f"not found: {src}")
    out = pathlib.Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--force-color-profile=srgb",
                                           "--disable-lcd-text",
                                           "--font-render-hinting=none"])
        page = browser.new_page(viewport={"width": 1200, "height": 1200},
                                device_scale_factor=1)
        page.goto(src.as_uri(), wait_until="load", timeout=args.timeout * 1000)
        try:
            page.wait_for_function("document.fonts.status === 'loaded'", timeout=8000)
        except Exception:
            print("  ! fonts did not report loaded — check the render before shipping")
        page.wait_for_timeout(250)
        meta = page.evaluate(MEASURE)
        if not meta:
            sys.exit("no .cover elements found in the HTML")

        for m in meta:
            if args.only and args.only not in m["name"]:
                continue
            dw, dh = m["declared"]
            scale = args.size / dw
            # re-open at the right device scale factor so type is rasterised
            # at final resolution instead of being upscaled afterwards
            ctxpage = browser.new_page(viewport={"width": int(dw) + 40, "height": int(dh) + 40},
                                       device_scale_factor=scale)
            ctxpage.goto(src.as_uri(), wait_until="load", timeout=args.timeout * 1000)
            try:
                ctxpage.wait_for_function("document.fonts.status === 'loaded'", timeout=8000)
            except Exception:
                pass
            ctxpage.wait_for_timeout(150)
            el = ctxpage.query_selector(f'.cover[data-name="{m["name"]}"]') or \
                ctxpage.query_selector_all(".cover")[m["index"]]
            path = out / f"{m['name']}.png"
            el.screenshot(path=str(path))
            ctxpage.close()

            ox, oy = m["overflow"]
            flag = "  ⚠ OVERFLOW" if (ox > 1 or oy > 1) else ""
            print(f"  {path.name}  {args.size}×{int(dh*scale)}  "
                  f"fonts: {', '.join(m['fonts'][:4])}{flag}")
            if args.jpeg:
                from PIL import Image
                im = Image.open(path).convert("RGB")
                jp = path.with_suffix(".jpg")
                im.save(jp, quality=args.jpeg, subsampling=0, optimize=True)
                print(f"  {jp.name}  ({jp.stat().st_size/1e6:.2f} MB)")
        browser.close()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Render an HTML file to PNG with headless Chromium.

This is the engine behind every custom visual in a deck. Chromium gives real
CSS: layered shadows, gradient meshes, backdrop-filter, clip-path, grain
overlays, flex/grid layout and any installed typeface. Nothing in pptxgenjs
comes close, so anything visually ambitious is built as HTML here and dropped
into the slide as an image.

    python scripts/render_html.py card.html out.png --width 1200 --height 800
    python scripts/render_html.py ui.html out.png --width 1290 --height 2796 --scale 2
    python scripts/render_html.py page.html out.png --selector "#frame" --transparent

--selector clips to one element and ignores --height, which is the reliable
way to render a component whose height you don't want to compute by hand.
Always render at 2x (--scale 2) for anything that lands on a slide: a 13.3in
slide is ~1280pt wide, and PowerPoint will be projected or zoomed.
"""
import argparse
import os
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("out")
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--scale", type=float, default=2.0, help="device pixel ratio")
    ap.add_argument("--selector", help="clip to this CSS selector instead of the viewport")
    ap.add_argument("--full-page", action="store_true")
    ap.add_argument("--transparent", action="store_true")
    ap.add_argument("--wait", type=int, default=350, help="ms to settle after load")
    a = ap.parse_args()

    if not os.path.exists(a.html):
        sys.exit(f"no such file: {a.html}")

    from playwright.sync_api import sync_playwright

    url = "file://" + os.path.abspath(a.html)
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--force-color-profile=srgb",
                                          "--font-render-hinting=none"])
        page = browser.new_page(
            viewport={"width": a.width, "height": a.height},
            device_scale_factor=a.scale,
        )
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(a.wait)
        try:
            page.evaluate("document.fonts.ready")
        except Exception:
            pass
        shot = {"path": a.out, "omit_background": a.transparent}
        if a.selector:
            el = page.query_selector(a.selector)
            if el is None:
                browser.close()
                sys.exit(f"selector not found: {a.selector}")
            el.screenshot(**shot)
        else:
            page.screenshot(full_page=a.full_page, **shot)
        browser.close()

    from PIL import Image
    with Image.open(a.out) as im:
        print(f"{a.out}  {im.width}x{im.height}px")


if __name__ == "__main__":
    main()

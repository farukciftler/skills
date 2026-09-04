#!/usr/bin/env python3
"""Wrap a screenshot in a device or browser frame and render it to PNG.

    python scripts/device_frame.py app.png out.png --device phone --bg "#0B0B0C"
    python scripts/device_frame.py dash.png out.png --device browser --url app.acme.com
    python scripts/device_frame.py ui.png out.png --device phone --transparent --tilt -8

Frames are drawn in CSS (no bitmap assets to go stale) and rendered through
render_html.py's Chromium, so the bezel, corner radius, shadow and screen clip
are all real. Devices:

    phone    6.1in-class handset, Dynamic Island, titanium rail
    tablet   11in-class tablet, thin uniform bezel
    browser  desktop browser chrome with a real-looking address bar
    laptop   browser content inside a laptop lid + base

The screenshot's aspect ratio is preserved by cropping to the device's screen
box from the top, so feed it something already close to the target ratio:
phone 1179x2556, tablet 1640x2360, browser/laptop 1600x1000.
"""
import argparse
import base64
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))

SPECS = {
    # css pixels of the *screen*, bezel thickness, outer radius, screen radius
    "phone":   dict(w=390, h=844, bezel=11, radius=52, screen_radius=42, island=True),
    "tablet":  dict(w=744, h=1050, bezel=16, radius=32, screen_radius=20, island=False),
    "browser": dict(w=1100, h=690, bezel=0, radius=14, screen_radius=0, island=False),
    "laptop":  dict(w=1100, h=690, bezel=0, radius=12, screen_radius=0, island=False),
}


def data_uri(path: str) -> str:
    ext = os.path.splitext(path)[1].lower().lstrip(".") or "png"
    mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


def build_html(shot: str, device: str, bg: str, url: str, tilt: float,
               pad: int, glow: str) -> str:
    s = SPECS[device]
    img = data_uri(shot)
    page_bg = "transparent" if bg == "none" else bg
    glow_css = ""
    if glow and glow != "none":
        glow_css = (f"position:absolute;inset:-18%;background:radial-gradient("
                    f"circle at 50% 40%, {glow} 0%, transparent 62%);"
                    f"filter:blur(60px);z-index:0;")

    if device in ("phone", "tablet"):
        island = ""
        if s["island"]:
            island = ("<div style='position:absolute;top:9px;left:50%;transform:translateX(-50%);"
                      "width:104px;height:29px;border-radius:16px;background:#000;z-index:3'></div>")
        stage = f"""
        <div class="dev" style="
            width:{s['w'] + s['bezel']*2}px;height:{s['h'] + s['bezel']*2}px;
            padding:{s['bezel']}px;border-radius:{s['radius']}px;
            background:linear-gradient(150deg,#4a4a4f,#1b1b1e 28%,#242428 62%,#5a5a60);
            box-shadow:0 2px 0 rgba(255,255,255,.16) inset,
                       0 0 0 1px rgba(0,0,0,.55),
                       0 44px 90px -28px rgba(0,0,0,.62);">
          <div style="position:relative;width:{s['w']}px;height:{s['h']}px;overflow:hidden;
                      border-radius:{s['screen_radius']}px;background:#fff">
            {island}
            <img src="{img}" style="width:100%;display:block">
          </div>
        </div>"""

    else:
        dots = ("".join(f"<i style='width:11px;height:11px;border-radius:50%;background:{c};"
                        f"display:inline-block;margin-right:7px'></i>"
                        for c in ("#FF5F57", "#FEBC2E", "#28C840")))
        bar = f"""
          <div style="height:44px;background:#EDEDF0;border-bottom:1px solid #DCDCE2;
                      display:flex;align-items:center;padding:0 14px;gap:14px">
            <div style="display:flex;align-items:center">{dots}</div>
            <div style="flex:1;height:26px;border-radius:7px;background:#fff;
                        border:1px solid #DCDCE2;display:flex;align-items:center;
                        padding:0 11px;font:400 12.5px/1 ui-sans-serif,Inter,system-ui;
                        color:#6B6B76;letter-spacing:.01em">{url}</div>
          </div>"""
        win = f"""
        <div style="width:{s['w']}px;border-radius:{s['radius']}px;overflow:hidden;
                    box-shadow:0 0 0 1px rgba(0,0,0,.10),0 40px 80px -30px rgba(0,0,0,.55);
                    background:#fff">
          {bar}
          <div style="height:{s['h']}px;overflow:hidden"><img src="{img}" style="width:100%;display:block"></div>
        </div>"""
        if device == "laptop":
            lid_w = s["w"] + 56
            stage = f"""
            <div class="dev" style="display:flex;flex-direction:column;align-items:center">
              <div style="padding:16px 16px 14px;border-radius:20px 20px 6px 6px;
                          background:linear-gradient(160deg,#3a3a3f,#1d1d20);
                          box-shadow:0 0 0 1px rgba(0,0,0,.5)">{win}</div>
              <div style="width:{lid_w}px;height:13px;border-radius:0 0 12px 12px;
                          background:linear-gradient(180deg,#cfcfd6,#8e8e97);
                          box-shadow:0 22px 40px -18px rgba(0,0,0,.6)"></div>
              <div style="width:{int(lid_w*0.16)}px;height:5px;border-radius:0 0 6px 6px;
                          background:#7c7c86"></div>
            </div>"""
        else:
            stage = f'<div class="dev">{win}</div>'

    return f"""<!doctype html><meta charset="utf-8"><style>
      *{{box-sizing:border-box}} html,body{{margin:0}}
      body{{background:{page_bg};display:flex;align-items:center;justify-content:center}}
      #frame{{position:relative;padding:{pad}px;display:flex;align-items:center;
              justify-content:center;background:{page_bg}}}
      .dev{{position:relative;z-index:1;transform:rotate({tilt}deg)}}
    </style><body><div id="frame">{('<div style="' + glow_css + '"></div>') if glow_css else ''}{stage}</div></body>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("screenshot")
    ap.add_argument("out")
    ap.add_argument("--device", choices=SPECS.keys(), default="phone")
    ap.add_argument("--bg", default="none", help="hex, css gradient, or 'none' for transparent")
    ap.add_argument("--glow", default="none", help="rgba/hex halo behind the device")
    ap.add_argument("--url", default="acme.com", help="address bar text for browser/laptop")
    ap.add_argument("--tilt", type=float, default=0.0, help="degrees of rotation")
    ap.add_argument("--pad", type=int, default=90)
    ap.add_argument("--scale", type=float, default=2.0)
    a = ap.parse_args()

    if not os.path.exists(a.screenshot):
        sys.exit(f"no such screenshot: {a.screenshot}")

    html = build_html(a.screenshot, a.device, a.bg, a.url, a.tilt, a.pad, a.glow)
    fd, tmp = tempfile.mkstemp(suffix=".html")
    with os.fdopen(fd, "w") as f:
        f.write(html)

    cmd = [sys.executable, os.path.join(HERE, "render_html.py"), tmp, a.out,
           "--selector", "#frame", "--scale", str(a.scale), "--width", "2200",
           "--height", "1600"]
    if a.bg == "none":
        cmd.append("--transparent")
    r = subprocess.run(cmd, capture_output=True, text=True)
    os.unlink(tmp)
    print(r.stdout.strip() or r.stderr.strip())
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()

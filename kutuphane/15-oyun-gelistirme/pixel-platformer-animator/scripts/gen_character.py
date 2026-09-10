#!/usr/bin/env python3
"""
gen_character.py - procedural side-view pixel-art platformer character generator.

Builds a paper-doll character on a pixel skeleton (2-bone IK limbs), renders the
full platformer animation set from hand-authored pose tables, applies hue-shifted
palette ramps, contact shading and a (sel-)outline, and writes:

  <out>/<name>_sheet.png        one row per animation, uniform frame grid
  <out>/<name>.manifest.json    Unity import manifest (rects, pivots, durations, events)
  <out>/preview/<anim>.gif      x6 upscaled previews with correct per-frame durations
  <out>/preview/<name>_sheet_x8.png   upscaled sheet with frame grid

Usage:
  python gen_character.py spec.json --out build/ [--anims idle,run] [--no-preview]

Deterministic: the same spec always yields byte-identical PNGs, so re-running
after a palette tweak keeps sprite names/rects stable for the Unity importer.
"""
import argparse
import colorsys
import copy
import json
import math
import os
import sys

import numpy as np
from PIL import Image

# --------------------------------------------------------------------------- #
# Palette
# --------------------------------------------------------------------------- #

def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb2hex(c):
    return "#%02x%02x%02x" % c


def _shift_hue(h, target, amount):
    d = ((target - h + 0.5) % 1.0) - 0.5  # shortest signed distance
    step = max(-amount, min(amount, d))
    return (h + step) % 1.0


def make_ramp(base_hex):
    """4 tones: [dark, shadow, base, light]. Shadows drift toward blue/violet,
    lights toward yellow - classic hue-shifted pixel-art ramp."""
    r, g, b = [c / 255 for c in hex2rgb(base_hex)]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)

    def tone(hs_target, hs_amt, s_mul, s_add, v_mul, v_add):
        hh = _shift_hue(h, hs_target, hs_amt) if s > 0.05 else h
        ss = max(0.0, min(1.0, s * s_mul + s_add))
        vv = max(0.0, min(1.0, v * v_mul + v_add))
        return tuple(int(round(c * 255)) for c in colorsys.hsv_to_rgb(hh, ss, vv))

    dark = tone(0.70, 0.08, 1.0, 0.18, 0.42, 0.0)
    shadow = tone(0.70, 0.04, 1.0, 0.10, 0.74, 0.0)
    base = hex2rgb(base_hex)
    light = tone(0.14, 0.035, 0.80, 0.0, 1.0, 0.13)
    return [dark, shadow, base, light]


DARK, SHADOW, BASE, LIGHT = 0, 1, 2, 3

DEFAULT_SPEC = {
    "name": "hero",
    "frame": [32, 32],
    "height": 24,
    "ppu": 16,
    "outline": "selout",          # "selout" | "#rrggbb"
    "hair_style": "short",        # short | long | hood
    "weapon": "sword",            # sword | none
    "palette": {
        "skin": "#f0b48c",
        "hair": "#7a3f22",
        "tunic": "#3f6fd6",
        "pants": "#4b4f6b",
        "boots": "#6b4428",
        "accent": "#e0b040",
        "steel": "#c8d4e0",
        "line": "#1a1224",
        "fx": "#f4f8ff",
    },
    "animations": "all",
}

PART_RAMPS = ["skin", "hair", "tunic", "pants", "boots", "accent", "steel"]


class Palette:
    def __init__(self, pal):
        self.colors = [(0, 0, 0, 0)]  # index 0 = transparent
        self.ramp = {}
        for key in PART_RAMPS:
            idx = []
            for c in make_ramp(pal[key]):
                idx.append(self._add(c))
            self.ramp[key] = idx
        self.line = self._add(hex2rgb(pal["line"]))
        self.fx = self._add(hex2rgb(pal["fx"]))
        self.fx_dim = self._add(tuple(int(a * 0.55 + b * 0.45) for a, b in
                                      zip(hex2rgb(pal["fx"]), hex2rgb(pal["tunic"]))))

    def _add(self, rgb):
        rgba = tuple(rgb) + (255,)
        if rgba in self.colors:
            return self.colors.index(rgba)
        self.colors.append(rgba)
        return len(self.colors) - 1

    def c(self, part, tone):
        return self.ramp[part][tone]

    def dark_of_index(self, ci):
        for key, idx in self.ramp.items():
            if ci in idx:
                return idx[DARK]
        return self.line


# --------------------------------------------------------------------------- #
# Raster helpers
# --------------------------------------------------------------------------- #

class Canvas:
    """Color-index buffer + part-id buffer (for contact shading / sel-out)."""

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.col = np.zeros((h, w), dtype=np.int16)
        self.part = np.zeros((h, w), dtype=np.int16)  # 0 = empty
        self._next_part = 1

    def new_part(self):
        pid = self._next_part
        self._next_part += 1
        return pid

    def put(self, x, y, ci, pid):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.col[y, x] = ci
            self.part[y, x] = pid

    def stamp(self, x, y, size, ci, pid):
        o = (size - 1) // 2
        for yy in range(y - o, y - o + size):
            for xx in range(x - o, x - o + size):
                self.put(xx, yy, ci, pid)

    def line(self, p0, p1, size, ci, pid):
        for x, y in bresenham(p0, p1):
            self.stamp(x, y, size, ci, pid)

    def rect(self, x0, y0, x1, y1, ci, pid):
        for y in range(min(y0, y1), max(y0, y1) + 1):
            for x in range(min(x0, x1), max(x0, x1) + 1):
                self.put(x, y, ci, pid)

    def mask(self, pid):
        return self.part == pid


def bresenham(p0, p1):
    x0, y0 = int(round(p0[0])), int(round(p0[1]))
    x1, y1 = int(round(p1[0])), int(round(p1[1]))
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    pts = []
    while True:
        pts.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy
    return pts


def ik(root, target, l1, l2, prefer):
    """2-bone IK. prefer='fwd' -> joint with larger x (knees), 'back' -> smaller x (elbows)."""
    rx, ry = root
    tx, ty = target
    dx, dy = tx - rx, ty - ry
    d = math.hypot(dx, dy)
    if d < 1e-6:
        return (rx, ry + l1)
    d_c = max(abs(l1 - l2) + 1e-3, min(l1 + l2 - 1e-3, d))
    ux, uy = dx / d, dy / d
    a = (l1 * l1 - l2 * l2 + d_c * d_c) / (2 * d_c)
    hh = math.sqrt(max(0.0, l1 * l1 - a * a))
    bx, by = rx + ux * a, ry + uy * a
    c1 = (bx - uy * hh, by + ux * hh)
    c2 = (bx + uy * hh, by - ux * hh)
    if prefer == "fwd":
        return c1 if c1[0] >= c2[0] else c2
    return c1 if c1[0] <= c2[0] else c2


def neighbors4(mask):
    m = np.zeros_like(mask)
    m[1:, :] |= mask[:-1, :]
    m[:-1, :] |= mask[1:, :]
    m[:, 1:] |= mask[:, :-1]
    m[:, :-1] |= mask[:, 1:]
    return m


# --------------------------------------------------------------------------- #
# Character rig
# --------------------------------------------------------------------------- #

NEUTRAL = {
    "dy": 0, "lean": 0, "head": [0, 0], "sq": 0,
    "ff": [1, 0], "bf": [-2, 0],
    "fh": [1, 6], "bh": [-1, 6],
    "sword": None, "slash": None, "eye": "open", "lie": False,
}


class Rig:
    def __init__(self, spec, pal):
        self.spec = spec
        self.pal = pal
        self.w, self.h = spec["frame"]
        H = spec["height"]
        self.cx = self.w // 2
        self.ground = self.h - 2              # sole row; outline lands on h-1
        self.leg_h = round(H * 0.34)
        self.torso_h = round(H * 0.28)
        self.head_h = H - self.leg_h - self.torso_h + 1
        self.head_w = self.head_h
        self.torso_w = max(5, round(H * 0.27))
        self.leg_w = 3 if H >= 22 else 2
        self.arm_w = 3 if H >= 36 else 2
        seg = (self.leg_h + 0.3) / 2
        self.thigh = self.shin = seg
        self.upper = self.fore = (self.torso_h + 0.5) / 2
        self.sword_len = max(5, round(H * 0.30))

    # ---- helpers ---------------------------------------------------------- #
    def _limb(self, cv, root, target, l1, l2, prefer, w, ci_a, ci_b, pid):
        j = ik(root, target, l1, l2, prefer)
        cv.line(root, j, w, ci_a, pid)
        cv.line(j, target, w, ci_b, pid)
        return j

    def _contact_shade(self, cv, new_pid):
        """Darken already-drawn pixels that touch a newly drawn part - this is
        what separates a front arm from the torso when both are tunic colored."""
        m_new = cv.mask(new_pid)
        ring = neighbors4(m_new) & ~m_new & (cv.part != 0)
        ys, xs = np.nonzero(ring)
        for y, x in zip(ys, xs):
            ci = cv.col[y, x]
            for key, idx in self.pal.ramp.items():
                if ci in idx:
                    t = idx.index(ci)
                    if t > SHADOW:
                        cv.col[y, x] = idx[SHADOW]
                    break

    # ---- body parts ------------------------------------------------------- #
    def draw_leg(self, cv, hip, foot, front):
        p = self.pal
        tone = BASE if front else SHADOW
        pid = cv.new_part()
        knee = self._limb(cv, hip, foot, self.thigh, self.shin, "fwd", self.leg_w,
                          p.c("pants", tone), p.c("pants", tone), pid)
        # boot shaft + foot (toe points +x)
        fx, fy = int(round(foot[0])), int(round(foot[1]))
        kx, ky = knee
        shaft_top = (fx + (kx - fx) * 0.35, fy + (ky - fy) * 0.35)
        cv.line(shaft_top, (fx, fy), self.leg_w, p.c("boots", tone), pid)
        cv.rect(fx - 1, fy - 1, fx + 2, fy, p.c("boots", tone), pid)
        cv.put(fx + 2, fy - 1, p.c("boots", tone - 1 if tone > 1 else tone), pid)
        if front:
            cv.put(fx - 1, fy - 1, p.c("boots", LIGHT), pid)
        return pid

    def draw_torso(self, cv, hip_y, sh_y, lean, sq):
        p = self.pal
        pid = cv.new_part()
        tw = self.torso_w + sq
        rows = hip_y - sh_y + 1
        for i, y in enumerate(range(sh_y, hip_y + 1)):
            t = 1.0 - i / max(1, rows - 1)             # 1 at shoulder, 0 at hip
            off = int(round(lean * t))
            x0 = self.cx - tw // 2 + off
            x1 = x0 + tw - 1
            if i == 0:                                 # rounded shoulders
                x0 += 1
                x1 -= 1
            for x in range(x0, x1 + 1):
                if x == x0:
                    tone = SHADOW
                elif x == x1 and i < rows // 2:
                    tone = LIGHT
                else:
                    tone = BASE
                cv.put(x, y, p.c("tunic", tone), pid)
        # belt
        by = hip_y - 1
        offb = int(round(lean * (1.0 - (by - sh_y) / max(1, rows - 1))))
        x0 = self.cx - tw // 2 + offb
        for x in range(x0, x0 + tw):
            cv.put(x, by, p.c("accent", SHADOW), pid)
        cv.put(x0 + tw - 2, by, p.c("accent", LIGHT), pid)
        # hem shadow
        offh = 0
        for x in range(self.cx - tw // 2 + offh, self.cx - tw // 2 + offh + tw):
            cv.put(x, hip_y, p.c("tunic", SHADOW), pid)
        return pid

    def draw_head(self, cv, top, left, eye):
        p = self.pal
        hw, hh = self.head_w, self.head_h
        x0, y0, x1, y1 = left, top, left + hw - 1, top + hh - 1
        pid = cv.new_part()
        corners = {(x0, y0), (x1, y0), (x0, y1), (x1, y1)}
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if (x, y) in corners:
                    continue
                cv.put(x, y, p.c("skin", BASE), pid)
        # jaw / neck shadow
        for x in range(x0 + 1, x1):
            cv.put(x, y1, p.c("skin", SHADOW), pid)
        # hair
        style = self.spec.get("hair_style", "short")
        hair_c = "tunic" if style == "hood" else "hair"
        cap_rows = max(3, hh // 3)
        for y in range(y0, y0 + cap_rows):
            for x in range(x0, x1 + 1):
                if (x, y) in corners:
                    continue
                tone = LIGHT if (y == y0 + 1 and x0 + 2 <= x <= x1 - 3) else BASE
                cv.put(x, y, p.c(hair_c, tone), pid)
        back_cols = 3
        back_bottom = y1 - 2 if style == "short" else y1 + (3 if style == "long" else 0)
        for y in range(y0, back_bottom + 1):
            for x in range(x0, x0 + back_cols):
                if (x, y) in corners:
                    continue
                tone = SHADOW if x == x0 else BASE
                cv.put(x, y, p.c(hair_c, tone), pid)
        # fringe
        fy = y0 + cap_rows
        for x in range(x0 + back_cols, x1 - 2):
            cv.put(x, fy, p.c(hair_c, SHADOW), pid)
        # skin shadow under the back hair
        for y in range(fy, y1):
            cv.put(x0 + back_cols, y, p.c("skin", SHADOW), pid)
        # eye (2px tall reads at 1x)
        ex = x1 - 2
        ey = y0 + cap_rows + 2
        if eye == "open":
            cv.put(ex, ey - 1, p.line, pid)
            cv.put(ex, ey, p.line, pid)
        elif eye == "closed":
            cv.put(ex - 1, ey, p.line, pid)
            cv.put(ex, ey, p.line, pid)
        elif eye == "hurt":
            cv.put(ex, ey - 1, p.line, pid)
            cv.put(ex - 1, ey, p.line, pid)
        # cheek blush / light
        cv.put(x1 - 1, ey + 1, p.c("skin", LIGHT), pid)
        return pid

    def draw_arm(self, cv, shoulder, hand, front):
        p = self.pal
        tone = BASE if front else SHADOW
        pid = cv.new_part()
        fore = "skin" if self.spec.get("sleeves", "short") == "short" else "tunic"
        self._limb(cv, shoulder, hand, self.upper, self.fore, "back", self.arm_w,
                   p.c("tunic", tone), p.c(fore, tone), pid)
        hx, hy = int(round(hand[0])), int(round(hand[1]))
        cv.rect(hx - 1, hy - 1, hx, hy, p.c("skin", tone), pid)
        return pid

    def draw_sword(self, cv, hand, angle_deg):
        p = self.pal
        pid = cv.new_part()
        a = math.radians(angle_deg)
        ux, uy = math.cos(a), -math.sin(a)
        hx, hy = hand
        tip = (hx + ux * self.sword_len, hy + uy * self.sword_len)
        base = (hx + ux * 1.5, hy + uy * 1.5)
        pts = bresenham(base, tip)
        for i, (x, y) in enumerate(pts):
            cv.put(x, y, p.c("steel", LIGHT if i < len(pts) - 1 else BASE), pid)
        # guard perpendicular to blade
        gx, gy = hx + ux * 1.2, hy + uy * 1.2
        for s in (-1, 1):
            cv.put(int(round(gx - uy * s)), int(round(gy + ux * s)), p.c("accent", BASE), pid)
        # pommel behind the hand
        cv.put(int(round(hx - ux * 1.5)), int(round(hy - uy * 1.5)), p.c("accent", SHADOW), pid)
        return pid

    # ---- pose ------------------------------------------------------------- #
    def render(self, pose):
        pose = self._scale({**NEUTRAL, **pose})
        if pose["lie"]:
            return self._render_lying(pose)
        cv = Canvas(self.w, self.h)
        self._compose(cv, pose)
        return cv

    def _scale(self, pose):
        """Pose tables are authored for a 24px-tall character; scale offsets so
        strides and arcs keep their proportion at other heights."""
        k = self.spec["height"] / 24.0
        if abs(k - 1.0) < 1e-6:
            return pose
        r = lambda v: int(round(v * k))
        out = dict(pose)
        for key in ("ff", "bf", "fh", "bh", "head"):
            out[key] = [r(pose[key][0]), r(pose[key][1])]
        for key in ("dy", "lean", "sq", "lie_dx"):
            if key in pose:
                out[key] = r(pose[key])
        if pose.get("slash"):
            a0, a1, rad = pose["slash"]
            out["slash"] = [a0, a1, r(rad)]
        return out

    def _compose(self, cv, pose):
        dy, lean, sq = pose["dy"], pose["lean"], pose["sq"]
        cx, g = self.cx, self.ground
        hip_y = g - self.leg_h + dy
        sh_y = hip_y - self.torso_h
        front_hip = (cx, hip_y)
        back_hip = (cx - 2, hip_y)
        ffoot = (cx + pose["ff"][0], g + pose["ff"][1])
        bfoot = (cx + pose["bf"][0], g + pose["bf"][1])
        tw = self.torso_w + sq
        sh_front = (cx - tw // 2 + lean + tw - 2, sh_y + 1)
        sh_back = (cx - tw // 2 + lean + 1, sh_y + 1)
        fhand = (sh_front[0] + pose["fh"][0], sh_front[1] + pose["fh"][1])
        bhand = (sh_back[0] + pose["bh"][0], sh_back[1] + pose["bh"][1])

        self.draw_arm(cv, sh_back, bhand, front=False)
        self.draw_leg(cv, back_hip, bfoot, front=False)
        self.draw_torso(cv, hip_y, sh_y, lean, sq)
        fl = self.draw_leg(cv, front_hip, ffoot, front=True)
        self._contact_shade(cv, fl)
        head_top = sh_y + 1 - self.head_h + 1 + pose["head"][1]
        head_left = cx - self.head_w // 2 + 1 + lean + pose["head"][0]
        self.draw_head(cv, head_top, head_left, pose["eye"])
        if pose["sword"] is not None and self.spec.get("weapon", "sword") == "sword":
            self.draw_sword(cv, fhand, pose["sword"])
        fa = self.draw_arm(cv, sh_front, fhand, front=True)
        self._contact_shade(cv, fa)
        cv.slash = pose["slash"]
        cv.slash_origin = sh_front
        return cv

    def _render_lying(self, pose):
        src = Canvas(self.w, self.h + 8)
        stand = {**NEUTRAL, "eye": pose.get("eye", "closed"),
                 "fh": [-1, 5], "bh": [-2, 5], "ff": [0, 0], "bf": [-1, 0]}
        self._compose(src, stand)
        ys, xs = np.nonzero(src.part)
        y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
        col = np.rot90(src.col[y0:y1 + 1, x0:x1 + 1], 1)
        prt = np.rot90(src.part[y0:y1 + 1, x0:x1 + 1], 1)
        hh, ww = col.shape
        cv = Canvas(self.w, self.h)
        oy = self.ground - hh + 1
        ox = self.cx - ww // 2 - 1 + pose.get("lie_dx", 0)
        for y in range(hh):
            for x in range(ww):
                if prt[y, x]:
                    cv.put(ox + x, oy + y, int(col[y, x]), int(prt[y, x]))
        cv.slash = None
        return cv


# --------------------------------------------------------------------------- #
# Post: outline + fx
# --------------------------------------------------------------------------- #

def finalize(cv, pal, outline_mode):
    filled = cv.part != 0
    ring = neighbors4(filled) & ~filled
    out = cv.col.copy()
    ys, xs = np.nonzero(ring)
    for y, x in zip(ys, xs):
        if outline_mode == "selout":
            cands = []
            for ddx, ddy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                yy, xx = y + ddy, x + ddx
                if 0 <= yy < cv.h and 0 <= xx < cv.w and filled[yy, xx]:
                    cands.append(pal.dark_of_index(int(cv.col[yy, xx])))
            # prefer the darkest tone among neighbours - avoids noisy mixed rims
            out[y, x] = min(cands, key=lambda ci: sum(pal.colors[ci][:3])) if cands else pal.line
        else:
            out[y, x] = pal.line
    if getattr(cv, "slash", None):
        a0, a1, r = cv.slash
        ox, oy = cv.slash_origin
        steps = max(8, int(abs(a1 - a0) / (40.0 / max(1, r))))  # ~1 sample per pixel of arc
        for i in range(steps + 1):
            a = math.radians(a0 + (a1 - a0) * i / steps)
            for rr, ci in ((r, pal.fx), (r - 1, pal.fx_dim)):
                x = int(round(ox + math.cos(a) * rr))
                y = int(round(oy - math.sin(a) * rr))
                if 0 <= x < cv.w and 0 <= y < cv.h and out[y, x] == 0:
                    out[y, x] = ci
    return out


def to_image(buf, pal):
    h, w = buf.shape
    arr = np.zeros((h, w, 4), dtype=np.uint8)
    lut = np.array(pal.colors, dtype=np.uint8)
    arr[:] = lut[buf]
    return Image.fromarray(arr, "RGBA")


# --------------------------------------------------------------------------- #
# Animation tables  (feet: relative to (cx, ground); hands: relative to shoulder)
# --------------------------------------------------------------------------- #

def _run_frames():
    A = [(4, 0), (2, 0), (0, 0), (-2, 0), (-4, -1), (-2, -3), (1, -4), (3, -2)]
    bob = [0, 1, 0, -1, 0, 1, 0, -1]
    frames = []
    for i in range(8):
        a = A[i]
        b = A[(i + 4) % 8]
        frames.append({
            "dur": 80, "dy": bob[i], "lean": 1,
            "ff": [a[0], a[1]], "bf": [b[0] - 2, b[1]],
            "fh": [int(round(-a[0] * 0.6)) + 1, 5], "bh": [int(round(-b[0] * 0.7)) - 1, 4],
        })
    return frames


def animation_table():
    return {
        "idle": {"loop": True, "frames": [
            {"dur": 240, "dy": 0},
            {"dur": 160, "dy": 0, "fh": [1, 5], "bh": [-1, 5]},
            {"dur": 240, "dy": 1, "fh": [1, 5], "bh": [-1, 5]},
            {"dur": 160, "dy": 1},
        ]},
        "run": {"loop": True, "frames": _run_frames(),
                "events": [{"frame": 0, "function": "OnFootstep"},
                           {"frame": 4, "function": "OnFootstep"}]},
        "jump": {"loop": False, "frames": [
            {"dur": 70, "dy": -1, "ff": [1, -1], "bf": [-3, 0], "fh": [4, 1], "bh": [-3, 3]},
            {"dur": 100, "dy": -1, "ff": [2, -3], "bf": [-2, -2], "fh": [6, -2], "bh": [-4, 2]},
        ], "events": [{"frame": 0, "function": "OnJumpDust"}]},
        "apex": {"loop": False, "frames": [
            {"dur": 90, "dy": 0, "ff": [3, -4], "bf": [-1, -3], "fh": [3, 1], "bh": [-3, 0]},
            {"dur": 120, "dy": 0, "ff": [3, -5], "bf": [0, -4], "fh": [3, 2], "bh": [-3, 1]},
        ]},
        "fall": {"loop": True, "frames": [
            {"dur": 110, "dy": 0, "ff": [2, -1], "bf": [-2, -2], "fh": [4, 3], "bh": [-5, -3]},
            {"dur": 110, "dy": 0, "ff": [2, -2], "bf": [-2, -1], "fh": [4, 2], "bh": [-5, -2]},
        ]},
        "land": {"loop": False, "frames": [
            {"dur": 60, "dy": 3, "sq": 1, "ff": [2, 0], "bf": [-3, 0], "fh": [3, 3], "bh": [-3, 3]},
            {"dur": 70, "dy": 2, "ff": [2, 0], "bf": [-3, 0], "fh": [2, 4], "bh": [-2, 4]},
            {"dur": 80, "dy": 1, "ff": [1, 0], "bf": [-2, 0], "fh": [1, 5], "bh": [-1, 5]},
        ], "events": [{"frame": 0, "function": "OnLand"}]},
        "crouch": {"loop": False, "frames": [
            {"dur": 60, "dy": 2, "ff": [2, 0], "bf": [-3, 0], "fh": [2, 4], "bh": [-2, 4]},
            {"dur": 100, "dy": 4, "sq": 1, "ff": [3, 0], "bf": [-3, 0], "fh": [3, 3], "bh": [-2, 3]},
        ]},
        "wall_slide": {"loop": True, "frames": [
            {"dur": 100, "dy": 1, "lean": -1, "ff": [5, -3], "bf": [-1, -1], "fh": [6, -1], "bh": [4, 3]},
            {"dur": 100, "dy": 1, "lean": -1, "ff": [5, -2], "bf": [-1, -2], "fh": [6, 0], "bh": [4, 4]},
        ]},
        "dash": {"loop": False, "frames": [
            {"dur": 50, "dy": 1, "lean": 2, "ff": [3, -1], "bf": [-4, 0], "fh": [-2, 3], "bh": [-3, 2]},
            {"dur": 70, "dy": 1, "lean": 3, "ff": [3, -2], "bf": [-5, -1], "fh": [-3, 2], "bh": [-4, 1]},
            {"dur": 90, "dy": 1, "lean": 2, "ff": [2, -1], "bf": [-4, -1], "fh": [-2, 3], "bh": [-3, 2]},
        ], "events": [{"frame": 0, "function": "OnDashStart"}]},
        "attack": {"loop": False, "frames": [
            {"dur": 90, "lean": -1, "ff": [3, 0], "bf": [-3, 0], "fh": [-4, 1], "bh": [-3, 3], "sword": 150},
            {"dur": 60, "lean": -1, "dy": 1, "ff": [3, 0], "bf": [-3, 0], "fh": [-5, 0], "bh": [-3, 3], "sword": 165},
            {"dur": 50, "lean": 2, "dy": 1, "ff": [3, 0], "bf": [-3, 0], "fh": [3, 1], "bh": [-4, 3], "sword": -15,
             "slash": [130, -25, 10]},
            {"dur": 80, "lean": 2, "dy": 1, "ff": [3, 0], "bf": [-3, 0], "fh": [3, 2], "bh": [-4, 3], "sword": -40,
             "slash": [10, -35, 10]},
            {"dur": 130, "lean": 1, "ff": [3, 0], "bf": [-3, 0], "fh": [2, 4], "bh": [-2, 4], "sword": -60},
        ], "events": [{"frame": 2, "function": "OnAttackHit"}, {"frame": 4, "function": "OnAttackEnd"}]},
        "hurt": {"loop": False, "frames": [
            {"dur": 80, "lean": -2, "head": [-1, 0], "eye": "hurt", "ff": [2, 0], "bf": [-2, 0], "fh": [5, 1], "bh": [-4, -1]},
            {"dur": 140, "lean": -1, "dy": 1, "eye": "hurt", "ff": [2, 0], "bf": [-2, 0], "fh": [0, 3], "bh": [-2, 3]},
        ]},
        "death": {"loop": False, "frames": [
            {"dur": 100, "lean": -2, "head": [-1, 0], "eye": "hurt", "fh": [5, 1], "bh": [-4, -1]},
            {"dur": 120, "dy": 4, "lean": -1, "eye": "hurt", "ff": [3, 0], "bf": [-4, 0], "fh": [1, 3], "bh": [-2, 3]},
            {"dur": 120, "dy": 5, "lean": -2, "eye": "closed", "ff": [3, 0], "bf": [-4, 0], "fh": [0, 4], "bh": [-2, 4]},
            {"dur": 120, "lie": True, "lie_dx": 1},
            {"dur": 600, "lie": True},
        ], "events": [{"frame": 4, "function": "OnDeathComplete"}]},
    }


ORDER = ["idle", "run", "jump", "apex", "fall", "land", "crouch",
         "wall_slide", "dash", "attack", "hurt", "death"]


# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #

def merge_spec(user):
    spec = copy.deepcopy(DEFAULT_SPEC)
    for k, v in user.items():
        if k == "palette":
            spec["palette"].update(v)
        else:
            spec[k] = v
    return spec


def build(spec, out_dir, only=None, preview=True):
    pal = Palette(spec["palette"])
    rig = Rig(spec, pal)
    table = animation_table()
    table.update(spec.get("custom_animations", {}))   # user-authored pose tables
    wanted = spec.get("animations", "all")
    names = [n for n in ORDER + [k for k in table if k not in ORDER]
             if (wanted == "all" or n in wanted) and n in table]
    if only:
        names = [n for n in names if n in only]
    if spec.get("weapon", "sword") != "sword":
        for n in names:
            for f in table[n]["frames"]:
                f.pop("sword", None)
                f.pop("slash", None)

    fw, fh = spec["frame"]
    rendered = {}
    for n in names:
        rendered[n] = [finalize(rig.render(f), pal, spec.get("outline", "selout"))
                       for f in table[n]["frames"]]
    cols = max(len(v) for v in rendered.values())
    sheet = np.zeros((fh * len(names), fw * cols), dtype=np.int16)
    anims, sprites = [], []
    for r, n in enumerate(names):
        frames_meta = []
        for c, buf in enumerate(rendered[n]):
            sheet[r * fh:(r + 1) * fh, c * fw:(c + 1) * fw] = buf
            sname = f"{spec['name']}_{n}_{c}"
            sprites.append({
                "name": sname,
                "x": c * fw,
                "y": sheet.shape[0] - (r + 1) * fh,   # Unity rects: bottom-left origin
                "w": fw, "h": fh,
                "pivotX": 0.5, "pivotY": 0.0,
            })
            frames_meta.append({"sprite": sname, "durationMs": table[n]["frames"][c]["dur"]})
        anims.append({"name": n, "loop": table[n]["loop"], "frames": frames_meta,
                      "events": table[n].get("events", [])})

    os.makedirs(out_dir, exist_ok=True)
    tex_name = f"{spec['name']}_sheet.png"
    to_image(sheet, pal).save(os.path.join(out_dir, tex_name), optimize=True)

    # collider suggestion from idle frame 0 (physics box stays constant - never animate it)
    idle = rendered.get("idle", next(iter(rendered.values())))[0]
    ys, xs = np.nonzero(idle)
    body_w = max(4, rig.torso_w + 2)
    body_h = int(ys.max() - ys.min()) - 2  # a bit shorter than the art: hair never blocks a ledge
    ppu = spec["ppu"]
    manifest = {
        "schema": 2,
        "name": spec["name"],
        "texture": tex_name,
        "textureWidth": int(sheet.shape[1]),
        "textureHeight": int(sheet.shape[0]),
        "frameWidth": fw, "frameHeight": fh,
        "ppu": ppu,
        "facing": "right",
        "collider": {"w": round(body_w / ppu, 4), "h": round(body_h / ppu, 4),
                     "offsetX": 0.0, "offsetY": round(body_h / ppu / 2, 4)},
        "palette": [rgb2hex(c[:3]) for c in pal.colors[1:]],
        "sprites": sprites,
        "animations": anims,
    }
    with open(os.path.join(out_dir, f"{spec['name']}.manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    if preview:
        write_previews(out_dir, spec["name"], rendered, table, pal, fw, fh, sheet)
    return manifest


def write_previews(out_dir, name, rendered, table, pal, fw, fh, sheet):
    pdir = os.path.join(out_dir, "preview")
    os.makedirs(pdir, exist_ok=True)
    bg = (46, 52, 64, 255)
    scale = 6
    for n, bufs in rendered.items():
        imgs = []
        for buf in bufs:
            im = Image.new("RGBA", (fw, fh), bg)
            im.alpha_composite(to_image(buf, pal))
            imgs.append(im.convert("RGB").resize((fw * scale, fh * scale), Image.NEAREST))
        durs = [f["dur"] for f in table[n]["frames"]]
        imgs[0].save(os.path.join(pdir, f"{n}.gif"), save_all=True, append_images=imgs[1:],
                     duration=durs, loop=0 if table[n]["loop"] else 1, disposal=2)
    # upscaled sheet with grid
    s = 8
    base = Image.new("RGBA", (sheet.shape[1], sheet.shape[0]), bg)
    base.alpha_composite(to_image(sheet, pal))
    big = base.resize((sheet.shape[1] * s, sheet.shape[0] * s), Image.NEAREST)
    px = big.load()
    for x in range(0, big.width, fw * s):
        for y in range(big.height):
            px[x, y] = (90, 98, 112, 255)
    for y in range(0, big.height, fh * s):
        for x in range(big.width):
            px[x, y] = (90, 98, 112, 255)
    big.convert("RGB").save(os.path.join(pdir, f"{name}_sheet_x8.png"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", nargs="?", help="character spec JSON (omit for defaults)")
    ap.add_argument("--out", default="build")
    ap.add_argument("--anims", default=None, help="comma list subset, e.g. idle,run")
    ap.add_argument("--no-preview", action="store_true")
    a = ap.parse_args()
    user = {}
    if a.spec:
        with open(a.spec) as f:
            user = json.load(f)
    spec = merge_spec(user)
    only = a.anims.split(",") if a.anims else None
    m = build(spec, a.out, only, not a.no_preview)
    total = sum(len(x["frames"]) for x in m["animations"])
    print(f"OK {m['name']}: {len(m['animations'])} animations, {total} frames, "
          f"sheet {m['textureWidth']}x{m['textureHeight']} -> {a.out}")


if __name__ == "__main__":
    sys.exit(main())

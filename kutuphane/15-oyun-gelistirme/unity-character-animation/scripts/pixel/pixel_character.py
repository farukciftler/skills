#!/usr/bin/env python3
"""pixel_character.py — spec JSON  ->  pixel-art platformer character sprite sheet.

A tiny 2D skeletal puppet (FK) is posed per frame and rasterized with NO
anti-aliasing, then outlined and shaded. Same spec + same script = identical
pixels, forever (deterministic). Output follows the sheetio contract, so the
Unity importer (PixelCharacterImporter.cs) and pixel_qa.py consume it directly.

    python pixel_character.py spec.json --out build/Ranger [--anims idle,run] [--scale 6]

Design conventions (everything in the spec is in PIXELS, y-up, origin = feet centre):
  * character faces RIGHT (+x). Flip at runtime (SpriteRenderer.flipX), never draw both.
  * limb angles are measured from STRAIGHT DOWN, positive = FORWARD (toward facing).
  * knee < 0 bends the shin backward; elbow > 0 bends the forearm forward.
  * weapon angle is absolute: 0 = forward, 90 = up, -90 = down.
  * "near" limbs are camera-side (drawn in front), "far" limbs are drawn behind in the shade tone.
Only Pillow is required.
"""
from __future__ import annotations

import argparse
import copy
import json
import math
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sheetio import hex_rgba, merge_duplicates, write_previews, write_sheet  # noqa: E402

# --------------------------------------------------------------------------- defaults
DEFAULT_PALETTE = {  # 16-ish colours, readable on dark AND light backgrounds
    "outline": "#1a1c2c", "skin": "#f4c7a1", "skin_shade": "#c98f6b",
    "hair": "#5d275d", "hair_shade": "#3b1a3b", "cloth": "#3b5dc9", "cloth_shade": "#29366f",
    "pants": "#566c86", "pants_shade": "#333c57", "boots": "#6b3f2a", "boots_shade": "#43261a",
    "accent": "#ffcd75", "eye": "#1a1c2c", "weapon": "#c2d3e0", "weapon_shade": "#7d93a8",
    "smear": "#f4f4f4",
}

# name, loop, grounded, [durations ms]  — frame count = len(durations)
DEFAULT_ANIMS = {
    "idle":      (True,  True,  [260, 160, 260, 160]),
    "walk":      (True,  True,  [110] * 6),
    "run":       (True,  True,  [75] * 8),
    "jump_rise": (False, False, [70, 110]),
    "jump_apex": (False, False, [150]),
    "fall":      (True,  False, [120, 120]),
    "land":      (False, True,  [50, 90, 150]),
    "attack":    (False, True,  [90, 70, 50, 110, 130]),
    "hurt":      (False, True,  [80, 180]),
    "death":     (False, True,  [100, 120, 140, 110, 110, 600]),
}
ATTACK_HIT_FRAME = 2  # strike frame -> AnimationEvent "OnAttackHit"


# --------------------------------------------------------------------------- raster
class Canvas:
    """Index canvas: each pixel holds (colour_key, part_z) or None."""

    def __init__(self, w: int, h: int, baseline: int, cx: int):
        self.w, self.h = w, h
        self.by = h - 1 - baseline  # canvas row of y=0 (feet)
        self.cx = cx
        self.px: list[list] = [[None] * w for _ in range(h)]

    def to_c(self, x: float, y: float) -> tuple[int, int]:
        return self.cx + int(math.floor(x + 0.5)), self.by - int(math.floor(y + 0.5))

    def put(self, cx: int, cy: int, key: str, z: int, overwrite=True):
        if 0 <= cx < self.w and 0 <= cy < self.h:
            if overwrite or self.px[cy][cx] is None:
                self.px[cy][cx] = (key, z)

    def get(self, cx, cy):
        if 0 <= cx < self.w and 0 <= cy < self.h:
            return self.px[cy][cx]
        return None

    # -- primitives (all in canvas coords) --
    def line(self, a, b, key, z, width=1):
        (x0, y0), (x1, y1) = a, b
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            self.brush(x0, y0, key, z, width)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def brush(self, x, y, key, z, width):
        if width <= 1:
            self.put(x, y, key, z)
        elif width == 2:
            for ox, oy in ((0, 0), (1, 0), (0, 1), (1, 1)):
                self.put(x + ox, y + oy, key, z)
        else:
            r = width / 2.0
            ir = int(math.ceil(r))
            for oy in range(-ir, ir + 1):
                for ox in range(-ir, ir + 1):
                    if ox * ox + oy * oy <= r * r - 0.25:
                        self.put(x + ox, y + oy, key, z)

    def polygon(self, pts, key, z):
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        for cy in range(max(0, int(min(ys)) - 1), min(self.h, int(max(ys)) + 2)):
            for cx in range(max(0, int(min(xs)) - 1), min(self.w, int(max(xs)) + 2)):
                if _inside(cx, cy, pts):
                    self.put(cx, cy, key, z)

    def disc(self, c, r, key, z, pred=None):
        ccx, ccy = c
        ir = int(math.ceil(r)) + 1
        for oy in range(-ir, ir + 1):
            for ox in range(-ir, ir + 1):
                if ox * ox + oy * oy <= r * r:
                    if pred is None or pred(ox, oy):
                        self.put(int(round(ccx + ox)), int(round(ccy + oy)), key, z)


def _inside(px, py, pts):
    inside = False
    n = len(pts)
    j = n - 1
    for i in range(n):
        xi, yi = pts[i]
        xj, yj = pts[j]
        if (yi > py) != (yj > py):
            xint = (xj - xi) * (py - yi) / (yj - yi + 1e-12) + xi
            if px < xint:
                inside = not inside
        j = i
    return inside


def _dir(deg_from_down: float) -> tuple[float, float]:
    a = math.radians(deg_from_down)
    return math.sin(a), -math.cos(a)


def _rot(p, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return p[0] * c - p[1] * s, p[0] * s + p[1] * c


# --------------------------------------------------------------------------- character
class Rig:
    def __init__(self, spec: dict):
        b = spec.get("body", {})
        self.H = int(b.get("height", 24))
        head = float(b.get("head", 1.0))
        build = float(b.get("build", 1.0))
        self.head_d = max(5, round(self.H * 0.30 * head))
        self.leg = max(5, round(self.H * 0.36))
        self.thigh = self.leg // 2 + (self.leg % 2)
        self.shin = self.leg - self.thigh
        self.torso = self.H - self.leg - self.head_d + 1
        self.arm = max(4, round(self.H * 0.30))
        self.upper = self.arm // 2 + (self.arm % 2)
        self.fore = self.arm - self.upper
        self.torso_w = max(3, round(self.H * 0.23 * build))
        self.limb_w = max(2, round(self.H * 0.13 * build))   # 24px tall -> 3px legs, 36px -> 5px
        self.arm_w = max(2, round(self.H * 0.09 * build))    # 24px -> 2px arms, 36px -> 3px
        self.foot = max(2, round(self.H * 0.10))
        self.hair = b.get("hair", "short")
        self.weapon = b.get("weapon", "sword")
        self.blade = max(5, round(self.H * 0.42))
        self.scarf = bool(b.get("scarf", False))

    def solve(self, pose: dict) -> dict:
        """Forward kinematics -> joint positions in design space (px, y-up, feet origin)."""
        lean = pose.get("lean", 0.0)
        hip = (0.0, float(self.leg))
        j = {"hip": hip}
        for side in ("near", "far"):
            hd, kd = pose["legs"][side]
            knee = (hip[0] + self.thigh * _dir(hd)[0], hip[1] + self.thigh * _dir(hd)[1])
            ankle_dir = _dir(hd + kd)
            ankle = (knee[0] + self.shin * ankle_dir[0], knee[1] + self.shin * ankle_dir[1])
            toe_a = hd + kd + 90 + pose.get("toe", 0)  # foot ~ perpendicular to shin, pointing forward
            td = _dir(toe_a)
            toe = (ankle[0] + (self.foot - 1) * td[0], ankle[1] + (self.foot - 1) * td[1])
            j[side + "_knee"], j[side + "_ankle"], j[side + "_toe"] = knee, ankle, toe
        tl = self.torso - pose.get("breath", 0)
        up = _rot((0.0, 1.0), -lean)  # lean forward = rotate toward +x
        neck = (hip[0] + up[0] * tl, hip[1] + up[1] * tl)
        sh = (hip[0] + up[0] * (tl - 1), hip[1] + up[1] * (tl - 1))
        j["neck"], j["shoulder"] = neck, sh
        hr = self.head_d / 2.0
        hup = _rot((0.0, 1.0), -(lean + pose.get("head", 0.0)))
        j["head"] = (neck[0] + hup[0] * (hr - 0.5), neck[1] + hup[1] * (hr - 0.5))
        j["head_up"] = hup
        for side in ("near", "far"):
            sd, ed = pose["arms"][side]
            sd_abs = sd - lean * 0.0  # arms hang from shoulders in world space
            elbow = (sh[0] + self.upper * _dir(sd_abs)[0], sh[1] + self.upper * _dir(sd_abs)[1])
            hand = (elbow[0] + self.fore * _dir(sd_abs + ed)[0], elbow[1] + self.fore * _dir(sd_abs + ed)[1])
            j[side + "_elbow"], j[side + "_hand"] = elbow, hand
        # optional whole-body rotation (death falls), around the feet origin
        rot = pose.get("rot", 0.0)
        if rot:
            for k, v in list(j.items()):
                if k != "head_up":
                    j[k] = _rot(v, rot)
            j["head_up"] = _rot(j["head_up"], rot)
        j["_rot"] = rot
        return j


def render_frame(rig: Rig, pose: dict, pal: dict, W: int, Hc: int, baseline: int,
                 outline: str, plant: bool) -> Image.Image:
    j = rig.solve(pose)
    # ---- ground planting: lowest body point sits exactly on the baseline ----
    dx = pose.get("dx", 0.0)
    dy = pose.get("dy", 0.0)
    if plant:
        pts = [v for k, v in j.items() if not k.startswith("_") and k != "head_up"]
        low = min(p[1] for p in pts)
        # limbs have thickness: feet line is drawn with width, bottom pixel = y - (w-1)/2
        dy += -low + (rig.limb_w - 1) / 2.0
    j = {k: ((v[0] + dx, v[1] + dy) if (not k.startswith("_") and k != "head_up") else v) for k, v in j.items()}

    cv = Canvas(W, Hc, baseline, W // 2 + pose.get("cx_off", 0))
    C = cv.to_c
    Z_FARARM, Z_FARLEG, Z_HAIRBACK, Z_TORSO, Z_NEARLEG, Z_HEAD, Z_NEARARM, Z_WEAPON = range(1, 9)

    # far limbs (shade tones)
    _leg(cv, j, "far", "pants_shade", "boots_shade", Z_FARLEG, rig)
    cv.line(C(*j["shoulder"]), C(*j["far_elbow"]), "cloth_shade", Z_FARARM, rig.arm_w)
    cv.line(C(*j["far_elbow"]), C(*j["far_hand"]), "skin_shade", Z_FARARM, rig.arm_w)

    # long hair / scarf behind the back
    if rig.hair == "long":
        back = _rot((-1.0, 0.0), -j["_rot"])
        h = j["head"]
        tail_end = (h[0] + back[0] * 2 - j["head_up"][0] * rig.head_d * 0.9,
                    h[1] + back[1] * 2 - j["head_up"][1] * rig.head_d * 0.9)
        cv.line(C(h[0] + back[0] * 1.5, h[1] + back[1] * 1.5), C(*tail_end), "hair_shade", Z_HAIRBACK, 2)
    if rig.scarf:
        n = j["neck"]
        sway = pose.get("scarf", 0.0)
        end = (n[0] - 3 - sway * 0.7, n[1] - 1 + sway * 0.3)
        cv.line(C(*n), C(*end), "accent", Z_HAIRBACK, 2)

    # torso = rotated rectangle hip->neck, pants on the lower third
    hip, neck = j["hip"], j["neck"]
    axis = (neck[0] - hip[0], neck[1] - hip[1])
    L = math.hypot(*axis) or 1.0
    nx, ny = -axis[1] / L, axis[0] / L
    hw = rig.torso_w / 2.0

    def quad(a, b, w):
        return [C(a[0] + nx * w, a[1] + ny * w), C(b[0] + nx * w, b[1] + ny * w),
                C(b[0] - nx * w, b[1] - ny * w), C(a[0] - nx * w, a[1] - ny * w)]

    belt = (hip[0] + axis[0] * 0.30, hip[1] + axis[1] * 0.30)
    cv.polygon(quad(belt, neck, hw), "cloth", Z_TORSO)
    cv.polygon(quad(hip, belt, hw), "pants", Z_TORSO)
    cv.line(C(*belt), C(*belt), "accent", Z_TORSO, 1)  # belt buckle pixel

    # near leg
    _leg(cv, j, "near", "pants", "boots", Z_NEARLEG, rig)

    # head
    hcx, hcy = C(*j["head"])
    r = rig.head_d / 2.0
    hu = j["head_up"]
    fwd = (hu[1], -hu[0])  # facing direction perpendicular to head-up
    cv.disc((hcx, hcy), r - 0.1, "skin", Z_HEAD)
    if rig.hair in ("short", "long", "hood", "spiky"):
        key = "cloth" if rig.hair == "hood" else "hair"

        def hair_pred(ox, oy):
            # canvas y grows downward -> convert
            ux, uy = ox, -oy
            upness = ux * hu[0] + uy * hu[1]
            fwdness = ux * fwd[0] + uy * fwd[1]
            return upness > r * 0.05 or (fwdness < -r * 0.25 and upness > -r * 0.6)
        cv.disc((hcx, hcy), r + (0.4 if rig.hair == "hood" else 0.0), key, Z_HEAD, hair_pred)
        if rig.hair == "spiky":
            tip = (j["head"][0] + hu[0] * (r + 2) - fwd[0] * 1.5, j["head"][1] + hu[1] * (r + 2) - fwd[1] * 1.5)
            cv.line(C(*j["head"]), C(*tip), "hair", Z_HEAD, 2)
    # eye
    ex = j["head"][0] + fwd[0] * r * 0.45 - hu[0] * r * 0.10
    ey = j["head"][1] + fwd[1] * r * 0.45 - hu[1] * r * 0.10
    ecx, ecy = C(ex, ey)
    cv.put(ecx, ecy, "eye", Z_HEAD)
    if rig.head_d >= 9:
        cv.put(ecx, ecy + 1, "eye", Z_HEAD)

    # weapon (behind near arm when pointing back, in front otherwise)
    wz = Z_WEAPON
    if rig.weapon in ("sword", "staff"):
        wa = pose.get("weapon")
        hand = j["near_hand"]
        if wa is None:  # default: follow forearm direction
            e = j["near_elbow"]
            wa = math.degrees(math.atan2(hand[1] - e[1], hand[0] - e[0]))
        wa += j["_rot"]
        d = (math.cos(math.radians(wa)), math.sin(math.radians(wa)))
        blade = rig.blade + (4 if rig.weapon == "staff" else 0)
        if pose.get("smear") and rig.weapon == "sword":
            a0, a1 = pose["smear"]
            steps = max(6, int(abs(a1 - a0) / 6))
            for i in range(steps + 1):
                a = math.radians(a0 + (a1 - a0) * i / steps + j["_rot"])
                for t in range(max(2, blade - 2), blade + 1):  # thin crescent, not a blob
                    cv.put(*C(hand[0] + math.cos(a) * t, hand[1] + math.sin(a) * t), "smear", Z_HAIRBACK,
                           overwrite=False)
        tip = (hand[0] + d[0] * blade, hand[1] + d[1] * blade)
        cv.line(C(*hand), C(*tip), "weapon", wz, 1)
        if rig.weapon == "sword":
            pnx, pny = -d[1], d[0]
            g0 = (hand[0] + d[0] * 1 + pnx * 1.5, hand[1] + d[1] * 1 + pny * 1.5)
            g1 = (hand[0] + d[0] * 1 - pnx * 1.5, hand[1] + d[1] * 1 - pny * 1.5)
            cv.line(C(*g0), C(*g1), "accent", wz, 1)
            pommel = (hand[0] - d[0] * 1.2, hand[1] - d[1] * 1.2)
            cv.line(C(*hand), C(*pommel), "boots", wz, 1)
        else:
            cv.put(*C(*tip), "accent", wz)

    # near arm last (in front of torso)
    cv.line(C(*j["shoulder"]), C(*j["near_elbow"]), "cloth", Z_NEARARM, rig.arm_w)
    cv.line(C(*j["near_elbow"]), C(*j["near_hand"]), "skin", Z_NEARARM, rig.arm_w)

    img = _finish(cv, pal, outline, inner={Z_NEARARM, Z_NEARLEG}, flash=pose.get("flash", False))
    return _snap_to_baseline(img, cv.by, plant)


def _snap_to_baseline(img: Image.Image, base_row: int, plant: bool) -> Image.Image:
    """Pixel-exact planting AFTER outline/rounding: grounded frames get their lowest opaque
    row (outline included) exactly on the baseline row; airborne frames are never allowed below it."""
    bbox = img.getchannel("A").getbbox()
    if not bbox:
        return img
    bottom = bbox[3] - 1
    shift = (base_row - bottom) if plant else min(0, base_row - bottom)
    if shift == 0:
        return img
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.paste(img, (0, shift))
    return out


def _leg(cv: Canvas, j, side, pants_key, boot_key, z, rig: Rig):
    C = cv.to_c
    cv.line(C(*j["hip"]), C(*j[side + "_knee"]), pants_key, z, rig.limb_w)
    cv.line(C(*j[side + "_knee"]), C(*j[side + "_ankle"]), pants_key, z, rig.limb_w)
    cv.line(C(*j[side + "_ankle"]), C(*j[side + "_toe"]), boot_key, z, rig.limb_w - 1 if rig.limb_w > 2 else 2)
    # boot cuff over the lower shin
    ank = j[side + "_ankle"]
    kn = j[side + "_knee"]
    cuff = (ank[0] + (kn[0] - ank[0]) * 0.25, ank[1] + (kn[1] - ank[1]) * 0.25)
    cv.line(C(*ank), C(*cuff), boot_key, z, rig.limb_w)


SHADE_OF = {"skin": "skin_shade", "hair": "hair_shade", "cloth": "cloth_shade",
            "pants": "pants_shade", "boots": "boots_shade", "weapon": "weapon_shade"}


def _finish(cv: Canvas, pal: dict, outline: str, inner: set, flash: bool) -> Image.Image:
    w, h = cv.w, cv.h
    px = cv.px
    # 1) inner outline: where a near limb overlaps a lower part, darken the lower part's border pixel
    marks = []
    for y in range(h):
        for x in range(w):
            p = px[y][x]
            if p and p[1] in inner:
                for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    q = cv.get(x + ox, y + oy)
                    if q and q[1] < p[1] and q[1] not in inner and q[0] not in ("eye", "smear"):
                        marks.append((x + ox, y + oy))
    for x, y in marks:
        k, z = px[y][x]
        px[y][x] = (SHADE_OF.get(k, k) if outline == "none" else "outline_inner", z)
    # 2) back-edge + bottom-edge shading (light from front-top; character faces +x)
    shade = []
    for y in range(h):
        for x in range(w):
            p = px[y][x]
            if p and p[0] in SHADE_OF:
                left = cv.get(x - 1, y)
                below = cv.get(x, y + 1)
                if left is None or (below is None and p[0] in ("cloth", "hair")):
                    shade.append((x, y))
    for x, y in shade:
        k, z = px[y][x]
        px[y][x] = (SHADE_OF[k], z)
    # 3) outer outline
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ip = img.load()
    for y in range(h):
        for x in range(w):
            p = px[y][x]
            if p:
                key = p[0]
                if key == "outline_inner":
                    col = _darken(hex_rgba(pal["outline"]), 1.0)
                else:
                    col = hex_rgba(pal[key])
                if flash and key not in ("outline_inner",):
                    col = (255, 255, 255, 255)
                ip[x, y] = col
    if outline != "none":
        out_px = []
        for y in range(h):
            for x in range(w):
                if px[y][x] is None:
                    nbr = [cv.get(x + ox, y + oy) for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
                    nbr = [n for n in nbr if n]
                    if nbr:
                        if outline == "selective":
                            k = nbr[0][0]
                            base = hex_rgba(pal.get(SHADE_OF.get(k, k), pal["outline"])) if k != "outline_inner" \
                                else hex_rgba(pal["outline"])
                            out_px.append((x, y, _darken(base, 0.45)))
                        else:
                            out_px.append((x, y, hex_rgba(pal["outline"])))
        for x, y, c in out_px:
            ip[x, y] = c
    return img


def _darken(c, f):
    return (int(c[0] * f), int(c[1] * f), int(c[2] * f), 255)


# --------------------------------------------------------------------------- poses
def base_pose() -> dict:
    return {"lean": 0.0, "head": 0.0, "breath": 0,
            "legs": {"near": (8.0, -6.0), "far": (-8.0, -6.0)},
            "arms": {"near": (14.0, 28.0), "far": (-10.0, 22.0)},
            "weapon": None}


def P(**kw) -> dict:
    p = base_pose()
    for k, v in kw.items():
        if k in ("legs", "arms"):
            p[k] = {**p[k], **v}
        else:
            p[k] = v
    return p


def poses_for(name: str, n: int, rig: Rig) -> list[dict]:
    sw = rig.weapon == "sword"
    idle_w = -55.0 if sw else None
    if name == "idle":
        w0 = idle_w
        w1 = (idle_w - 3) if sw else None
        seq = [P(breath=0, weapon=w0, scarf=0, arms={"near": (14, 28), "far": (-10, 22)}),
               P(breath=1, weapon=w0, scarf=1, arms={"near": (14, 32), "far": (-10, 25)}),
               P(breath=1, weapon=w1, head=-3, scarf=2, arms={"near": (15, 35), "far": (-9, 27)}),
               P(breath=0, weapon=w1, head=-1, scarf=1, arms={"near": (14, 30), "far": (-10, 23)})]
        return _resample(seq, n)
    if name in ("walk", "run"):
        run = name == "run"
        amp_leg, amp_arm = (42, 38) if run else (26, 18)
        out = []
        for i in range(n):
            ph = 2 * math.pi * i / n
            s, c = math.sin(ph), math.cos(ph)
            knee_n = -(8 + (70 if run else 42) * max(0.0, c))
            knee_f = -(8 + (70 if run else 42) * max(0.0, -c))
            out.append(P(
                lean=12 if run else 4, head=-6 if run else -2,
                legs={"near": (amp_leg * s, knee_n), "far": (-amp_leg * s, knee_f)},
                arms={"near": (-amp_arm * s + (10 if run else 6), 75 if run else 22),
                      "far": (amp_arm * s + (4 if run else 0), 75 if run else 22)},
                weapon=(-20 - 12 * s) if (sw and run) else (idle_w if sw else None),
                scarf=2 + 2 * abs(c) if run else 1 + abs(c)))
        return out
    if name == "jump_rise":
        seq = [P(lean=6, legs={"near": (-8, -12), "far": (-18, -10)}, arms={"near": (150, 20), "far": (130, 20)},
                 weapon=100 if sw else None, dy=1, scarf=3),
               P(lean=6, legs={"near": (38, -55), "far": (-6, -40)}, arms={"near": (120, 30), "far": (100, 20)},
                 weapon=80 if sw else None, dy=3, scarf=3)]
        return _resample(seq, n)
    if name == "jump_apex":
        return _resample([P(lean=4, legs={"near": (55, -85), "far": (25, -80)},
                            arms={"near": (95, 40), "far": (70, 30)}, weapon=40 if sw else None, dy=4,
                            scarf=1)], n)
    if name == "fall":
        seq = [P(lean=0, head=4, legs={"near": (14, -22), "far": (-12, -16)}, arms={"near": (125, 20), "far": (115, 20)},
                 weapon=98 if sw else None, dy=2, scarf=-2),
               P(lean=0, head=4, legs={"near": (18, -18), "far": (-16, -20)}, arms={"near": (132, 20), "far": (110, 20)},
                 weapon=104 if sw else None, dy=2, scarf=-3)]
        return _resample(seq, n)
    if name == "land":
        seq = [P(lean=18, head=-8, legs={"near": (48, -95), "far": (30, -100)}, arms={"near": (40, 30), "far": (30, 30)},
                 weapon=-30 if sw else None, scarf=3),
               P(lean=12, head=-5, legs={"near": (34, -65), "far": (14, -62)}, arms={"near": (25, 30), "far": (5, 25)},
                 weapon=-45 if sw else None, scarf=2),
               P(lean=4, legs={"near": (14, -16), "far": (-4, -14)}, weapon=idle_w, scarf=1)]
        return _resample(seq, n)
    if name == "attack":
        if sw:
            seq = [P(lean=-6, head=-4, legs={"near": (16, -10), "far": (-18, -10)},
                     arms={"near": (165, 35), "far": (-20, 30)}, weapon=125, scarf=1),
                   P(lean=-8, head=-4, legs={"near": (18, -10), "far": (-20, -10)},
                     arms={"near": (190, 30), "far": (-25, 30)}, weapon=150, scarf=1),
                   P(lean=16, head=-6, legs={"near": (36, -14), "far": (-30, -6)},
                     arms={"near": (85, 0), "far": (-50, 40)}, weapon=-15, smear=(150, -15), scarf=4),
                   P(lean=12, head=-5, legs={"near": (34, -14), "far": (-28, -6)},
                     arms={"near": (48, 10), "far": (-40, 40)}, weapon=-62, scarf=3),
                   P(lean=5, legs={"near": (20, -10), "far": (-14, -8)},
                     arms={"near": (24, 26), "far": (-14, 26)}, weapon=-52, scarf=2)]
        else:  # punch
            seq = [P(lean=-4, arms={"near": (40, 110), "far": (-10, 40)}),
                   P(lean=-6, arms={"near": (20, 120), "far": (-10, 40)}),
                   P(lean=14, legs={"near": (30, -12), "far": (-24, -6)}, arms={"near": (92, 0), "far": (-40, 50)}),
                   P(lean=10, legs={"near": (28, -12), "far": (-22, -6)}, arms={"near": (86, 8), "far": (-30, 50)}),
                   P(lean=4, arms={"near": (30, 40), "far": (-10, 30)})]
        return _resample(seq, n)
    if name == "hurt":
        seq = [P(lean=-20, head=-18, dx=-1, legs={"near": (-6, -14), "far": (-20, -10)},
                 arms={"near": (-45, 30), "far": (-70, 20)}, weapon=160 if sw else None, scarf=-3),
               P(lean=-10, head=-8, legs={"near": (2, -10), "far": (-14, -8)},
                 arms={"near": (-20, 30), "far": (-35, 25)}, weapon=-120 if sw else None, scarf=-1)]
        return _resample(seq, n)
    if name == "death":
        seq = [P(lean=-18, head=-18, legs={"near": (-6, -14), "far": (-20, -10)},
                 arms={"near": (-40, 30), "far": (-70, 20)}, weapon=160 if sw else None),
               P(lean=-12, head=10, legs={"near": (40, -90), "far": (20, -95)},
                 arms={"near": (10, 20), "far": (-5, 20)}, weapon=-100 if sw else None),
               P(lean=-5, head=20, legs={"near": (70, -140), "far": (60, -140)},
                 arms={"near": (20, 10), "far": (10, 10)}, weapon=-95 if sw else None),
               P(rot=35, lean=0, head=10, legs={"near": (60, -110), "far": (50, -110)},
                 arms={"near": (60, 10), "far": (40, 10)}, weapon=-80 if sw else None, cx_off=3),
               P(rot=70, lean=0, head=5, legs={"near": (30, -40), "far": (20, -35)},
                 arms={"near": (120, 10), "far": (100, 10)}, weapon=-60 if sw else None, cx_off=6),
               P(rot=88, lean=0, head=0, legs={"near": (10, -10), "far": (4, -8)},
                 arms={"near": (150, 10), "far": (130, 10)}, weapon=-30 if sw else None, cx_off=8)]
        return _resample(seq, n)
    raise KeyError(f"no pose generator for animation '{name}' (custom anims: add them here)")


def _resample(seq: list[dict], n: int) -> list[dict]:
    if n == len(seq):
        return [copy.deepcopy(s) for s in seq]
    return [copy.deepcopy(seq[min(len(seq) - 1, int(i * len(seq) / n))]) for i in range(n)]


# --------------------------------------------------------------------------- main
def build(spec: dict, out_dir: str, only: list[str] | None = None, scale: int = 6) -> tuple[str, str]:
    fr = spec.get("frame", {"auto": True})
    baseline = int(fr.get("baseline", 2))
    auto = bool(fr.get("auto", "w" not in fr))
    pal = {**DEFAULT_PALETTE, **spec.get("palette", {})}
    outline = spec.get("outline", "full")
    rig = Rig(spec)
    anim_cfg = {k: list(v) for k, v in DEFAULT_ANIMS.items()}
    for name, cfg in spec.get("animations", {}).items():
        if cfg is False:
            anim_cfg.pop(name, None)
            continue
        base = anim_cfg.get(name, [True, True, [100] * 4])
        if "ms" in cfg:
            base[2] = list(cfg["ms"])
        if "loop" in cfg:
            base[0] = bool(cfg["loop"])
        if "grounded" in cfg:
            base[1] = bool(cfg["grounded"])
        anim_cfg[name] = base
    names = [n for n in anim_cfg if (not only or n in only)]

    # pass 1: render on a generous scratch canvas (positions are deterministic, so cropping is exact)
    SW, SH = rig.H * 5 + 8, rig.H * 4 + 8
    SW += SW % 2
    s_by = SH - 1 - baseline
    raw = {}
    for name in names:
        loop, grounded, durs = anim_cfg[name]
        raw[name] = [render_frame(rig, p, pal, SW, SH, baseline, outline, plant=grounded)
                     for p in poses_for(name, len(durs), rig)]
    x0, x1, y0 = SW, 0, SH
    for frames in raw.values():
        for im in frames:
            bb = im.getchannel("A").getbbox()
            if bb:
                x0, x1, y0 = min(x0, bb[0]), max(x1, bb[2] - 1), min(y0, bb[1])
    cx = SW // 2
    half_need = max(cx - x0, x1 - cx + 1) + 1          # +1 px empty margin
    top_need = (s_by - y0) + 2                           # rows above baseline row incl. margin
    W_need = 2 * half_need
    H_need = top_need + baseline + 1
    H_need += H_need % 2
    if auto:
        W, Hc = W_need, H_need
    else:
        W, Hc = int(fr["w"]), int(fr["h"])
        if W % 2 or Hc % 2:
            raise SystemExit("frame w/h must be even (odd sizes put the pivot on a half pixel)")
        if W < W_need or Hc < H_need:
            print(f"WARNING: poses need at least {W_need}x{H_need}px but frame is {W}x{Hc}; "
                  f"pixels will be cropped (use \"frame\": {{\"auto\": true}} or enlarge)", file=sys.stderr)
    crop = (cx - W // 2, s_by - (Hc - 1 - baseline), cx + W // 2, s_by + baseline + 1)

    anims = []
    for name in names:
        loop, grounded, durs = anim_cfg[name]
        frames = [im.crop(crop) for im in raw[name]]
        ev = [{"frame": min(ATTACK_HIT_FRAME, len(durs) - 1), "function": "OnAttackHit"}] if name == "attack" else []
        if name == "death":
            ev = [{"frame": len(durs) - 1, "function": "OnDeathFinished"}]
        frames, durs, ev = _merge_duplicates(frames, list(durs), ev, loop)
        anims.append({"name": name, "loop": loop, "grounded": grounded, "frames": frames,
                      "durations": durs, "events": ev})
    png, js = write_sheet(out_dir, spec.get("name", "Character"), anims, W, Hc, baseline,
                          ppu=int(spec.get("ppu", 16)),
                          extra={"generator": "pixel_character.py", "spec": spec,
                                 "stateHints": spec.get("stateHints", {"runSpeed": 3.5, "apexBand": 1.2})})
    write_previews(js, scale=scale)
    return png, js


_merge_duplicates = merge_duplicates  # shared implementation lives in sheetio


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("--out", required=True)
    ap.add_argument("--anims", default="", help="comma list to build a subset (fast iteration)")
    ap.add_argument("--scale", type=int, default=6)
    a = ap.parse_args()
    with open(a.spec, encoding="utf-8") as f:
        spec = json.load(f)
    png, js = build(spec, a.out, [s for s in a.anims.split(",") if s] or None, a.scale)
    print(json.dumps({"sheet": png, "meta": js, "preview": os.path.join(os.path.dirname(js), "preview")}))


if __name__ == "__main__":
    main()

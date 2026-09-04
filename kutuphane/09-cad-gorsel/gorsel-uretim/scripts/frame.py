#!/usr/bin/env python3
"""
frame.py — Moonstone Residence markalı sosyal medya karesi üretir.

Pillow ile çalışır (bu makinede kurulu, ek bağımlılık yok). Arka plan
fotoğrafını doğru orana kırpar, okunabilirlik katmanı (scrim) koyar, marka
tipografisini yerleştirir, logoyu basar ve güvenli alan dışına taşmaz.

Örnek:
  python3 frame.py --preset ig-story --bg foto.jpg \
    --eyebrow "MOONSTONE RESIDENCE" \
    --title "Ay taşının zarafeti" \
    --body "Tuzla Aydıntepe · 1+1 – 3+1 · 3.000 m² ticari alan" \
    --note "Temsili görseldir" --out cikti.png

Güvenli alanı denetlemek için --guides ekle.
"""
import argparse, json, os, re, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ---------------------------------------------------------------- marka

INK        = (4, 12, 29)
NAVY_800   = (19, 22, 42)
NAVY_700   = (20, 35, 63)
GOLD       = (184, 153, 47)
GOLD_LIGHT = (253, 216, 53)
BRONZE     = (156, 138, 93)
CREAM      = (245, 241, 236)
WHITE      = (255, 255, 255)

PALETTE = {"ink": INK, "navy800": NAVY_800, "navy700": NAVY_700,
           "gold": GOLD, "goldlight": GOLD_LIGHT, "bronze": BRONZE,
           "cream": CREAM, "white": WHITE}

# ---------------------------------------------------------------- presetler
# safe = (ust, alt, sol, sag) piksel — arayuz bindirmesi
PRESETS = {
    "ig-story":  dict(w=1080, h=1920, safe=(250, 250,  65,  65)),
    "reels":     dict(w=1080, h=1920, safe=(108, 320,  60, 120)),
    "tiktok":    dict(w=1080, h=1920, safe=(140, 400,  60, 180)),
    "cross-9x16":dict(w=1080, h=1920, safe=(140, 400,  60, 180)),  # IG+TikTok ortak
    "ig-45":     dict(w=1080, h=1350, safe=( 60,  60,  60,  60)),
    "ig-kare":   dict(w=1080, h=1080, safe=( 56,  56,  56,  56)),
    "og":        dict(w=1200, h=630,  safe=( 48,  48,  56,  56)),
    "web-hero":  dict(w=2560, h=1440, safe=(80, 80, 120, 120)),
}

# ---------------------------------------------------------------- fontlar

FONT_DIRS = [os.path.expanduser("~/Library/Fonts"), "/Library/Fonts",
             "/System/Library/Fonts", "/System/Library/Fonts/Supplemental"]

DISPLAY_CHAIN = [  # marka display fontu -> makinedeki en yakin karsilik
    ("CormorantGaramond-Light.ttf", 0), ("CormorantGaramond-Regular.ttf", 0),
    ("Cormorant Garamond.ttf", 0), ("Cormorant.ttc", 0),
    ("Didot.ttc", 0), ("Baskerville.ttc", 0), ("Georgia.ttf", 0),
]
BODY_CHAIN = [
    ("Lora-Regular.ttf", 0), ("Lora.ttf", 0), ("Lora.ttc", 0),
    ("Georgia.ttf", 0), ("Times New Roman.ttf", 0),
]
BODY_BOLD_CHAIN = [
    ("Lora-Bold.ttf", 0), ("Georgia Bold.ttf", 0), ("Times New Roman Bold.ttf", 0),
]

_font_warned = set()

def _find(name):
    for d in FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    return None

def resolve_font(chain, label):
    for name, idx in chain:
        p = _find(name)
        if p:
            if label not in _font_warned and not name.lower().startswith(("cormorant", "lora")):
                sys.stderr.write(
                    f"[not] {label}: marka fontu bulunamadi, '{name}' kullaniliyor. "
                    f"Marka fontu icin Cormorant Garamond / Lora kurulmali.\n")
                _font_warned.add(label)
            return p, idx
    raise SystemExit(f"{label} icin font bulunamadi")

def load(chain, size, label):
    path, idx = resolve_font(chain, label)
    try:
        return ImageFont.truetype(path, size, index=idx)
    except Exception:
        return ImageFont.truetype(path, size)

# ---------------------------------------------------------------- yardimcilar

def parse_color(s):
    if not s:
        return None
    s = s.strip()
    if s in PALETTE:
        return PALETTE[s]
    m = re.fullmatch(r"#?([0-9a-fA-F]{6})", s)
    if m:
        h = m.group(1)
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    raise SystemExit(f"renk anlasilmadi: {s}")

def cover(img, w, h, focus="center"):
    """Orani bozmadan hedefi tamamen kaplayacak sekilde kirp."""
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    nw, nh = int(round(iw * scale)), int(round(ih * scale))
    img = img.resize((nw, nh), Image.LANCZOS)
    fx = {"left": 0.0, "center": 0.5, "right": 1.0}.get(focus, 0.5)
    fy = {"top": 0.0, "center": 0.5, "bottom": 1.0}.get(focus, 0.5)
    if focus in ("top", "bottom"):
        fx = 0.5
    if focus in ("left", "right"):
        fy = 0.5
    x = int((nw - w) * fx)
    y = int((nh - h) * fy)
    return img.crop((x, y, x + w, y + h))

def contain(img, w, h):
    """Orani bozmadan kutuya sigdir (kirpmaz)."""
    iw, ih = img.size
    s = min(w / iw, h / ih)
    return img.resize((max(1, int(iw * s)), max(1, int(ih * s))), Image.LANCZOS)

def vgradient(w, h, color, a_top, a_bottom, ease=2.0):
    """Dikey alfa degradesi — okunabilirlik katmani."""
    grad = Image.new("L", (1, h))
    px = grad.load()
    for y in range(h):
        t = y / max(1, h - 1)
        t = t ** ease if a_bottom > a_top else (1 - (1 - t) ** ease)
        px[0, y] = int(round(a_top + (a_bottom - a_top) * t))
    grad = grad.resize((w, h))
    layer = Image.new("RGBA", (w, h), color + (0,))
    layer.putalpha(grad)
    return layer

def tracked(draw, xy, text, font, fill, tracking=0.0, anchor_left=True):
    """PIL'de harf araligi yok — elle uygular. tracking = em orani."""
    x, y = xy
    sp = font.size * tracking
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += font.getlength(ch) + sp
    return x - xy[0]

def tracked_width(text, font, tracking=0.0):
    if not text:
        return 0
    return sum(font.getlength(c) for c in text) + font.size * tracking * (len(text) - 1)

def wrap(text, font, max_w, tracking=0.0):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if tracked_width(trial, font, tracking) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur); cur = wd
    if cur:
        lines.append(cur)
    return lines

LOGO_SVG = {
    # tam kilit (sembol + kelime markasi), seffaf zeminli varyantlar
    "dark":       "Moonstone Logo 2D/Dark Background/SVG Dosyası/Cormorant Garamond - D-1.svg",
    "dark-mark":  "Moonstone Logo 2D/Dark Background/SVG Dosyası/Cormorant Garamond - D-3.svg",
    "light":      "Moonstone Logo 2D/Light Background/SVG Dosyaları/Cormorant Garamond - L.svg",
    "light-mark": "Moonstone Logo 2D/Light Background/SVG Dosyaları/Cormorant Garamond - Cormorant Garamond - L.svg",
}

def repo_root():
    """Skill scripts/ dizininden depo kokunu bul."""
    d = os.path.abspath(os.path.dirname(__file__))
    for _ in range(6):
        if os.path.isdir(os.path.join(d, "Moonstone Logo 2D")):
            return d
        d = os.path.dirname(d)
    return None

def logo_png(variant, target_w):
    """Marka SVG'sini seffaf PNG'ye cevirir. Zemin dikdortgeni varsa temizler."""
    root = repo_root()
    if not root:
        return None
    src = os.path.join(root, LOGO_SVG.get(variant, LOGO_SVG["dark"]))
    if not os.path.exists(src):
        return None
    out = os.path.join(tempfile.gettempdir(), f"ms-logo-{variant}-{target_w}.png")
    if os.path.exists(out):
        return out
    try:
        svg = open(src, encoding="utf-8").read()
        # tam boy zemin dikdortgenini kaldir -> seffaflik
        svg = re.sub(r'<rect\s+width="\d+"\s+height="\d+"\s+fill="(?:#[0-9A-Fa-f]{3,8}|white|black|[a-zA-Z]+)"\s*/>',
                     "", svg, count=1)
        tmp = os.path.join(tempfile.gettempdir(), f"ms-logo-{variant}.svg")
        open(tmp, "w", encoding="utf-8").write(svg)
        subprocess.run(["rsvg-convert", "-w", str(target_w), "-o", out, tmp],
                       check=True, capture_output=True)
    except Exception:
        return None
    return out


# ---------------------------------------------------------------- kontrast denetimi

def _rel_lum(rgb):
    c = [v / 255 for v in rgb]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def _ratio(a, b):
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)

def check_text_contrast(img, x0, x1, y0, y1, fg, accent):
    """Metin bloklarinin arkasindaki ortalama zemine gore kontrasti olcer ve uyarir.
    WCAG: normal metin 4.5:1, 24px+ buyuk metin 3:1."""
    y0, y1 = max(0, int(y0)), min(img.height, int(y1))
    x0, x1 = max(0, int(x0)), min(img.width, int(x1))
    if y1 <= y0 or x1 <= x0:
        return
    step_x = max(1, (x1 - x0) // 60)
    step_y = max(1, (y1 - y0) // 40)
    px_list = [img.getpixel((x, y)) for x in range(x0, x1, step_x)
                                     for y in range(y0, y1, step_y)]
    if not px_list:
        return
    bg = sum(_rel_lum(p) for p in px_list) / len(px_list)
    worst = max(_rel_lum(p) for p in px_list)
    for name, col, floor in (("govde/baslik", fg, 4.5), ("vurgu (etiket, kicker)", accent, 4.5)):
        r_avg = _ratio(_rel_lum(col), bg)
        r_worst = _ratio(_rel_lum(col), worst)
        if r_avg < floor:
            sys.stderr.write(
                f"[UYARI] {name} kontrasti {r_avg:.2f}:1 — esik {floor}:1. "
                f"--scrim-strength artir ya da --scrim-ease dusur (or. 0.8).\n")
        elif r_worst < 3.0:
            sys.stderr.write(
                f"[not] {name} ortalamada iyi ({r_avg:.2f}:1) ama en parlak noktada "
                f"{r_worst:.2f}:1 — metnin altindaki parlak lekeye bak.\n")

# ---------------------------------------------------------------- ana

def build(a):
    if a.preset not in PRESETS:
        raise SystemExit(f"preset bilinmiyor. secenekler: {', '.join(PRESETS)}")
    P = PRESETS[a.preset]
    W, H = P["w"], P["h"]
    st, sb, sl, sr = P["safe"]
    if a.safe_pad:
        st += a.safe_pad; sb += a.safe_pad; sl += a.safe_pad; sr += a.safe_pad

    base_col = parse_color(a.bg_color) or INK
    canvas = Image.new("RGB", (W, H), base_col)

    # --- arka plan
    if a.bg:
        img = Image.open(a.bg).convert("RGB")
        img = cover(img, W, H, a.bg_focus)
        if a.bg_blur > 0:
            img = img.filter(ImageFilter.GaussianBlur(a.bg_blur))
        canvas.paste(img, (0, 0))
    elif a.bg_gradient:
        top = parse_color(a.bg_gradient.split(",")[0])
        bot = parse_color(a.bg_gradient.split(",")[1])
        g = Image.new("RGB", (1, H))
        gp = g.load()
        for y in range(H):
            t = y / max(1, H - 1)
            gp[0, y] = tuple(int(round(top[i] + (bot[i] - top[i]) * t)) for i in range(3))
        canvas.paste(g.resize((W, H)), (0, 0))

    canvas = canvas.convert("RGBA")

    # --- okunabilirlik katmani
    scrim_col = parse_color(a.scrim_color) or INK
    if a.scrim in ("bottom", "both"):
        canvas.alpha_composite(vgradient(W, H, scrim_col, 0, int(255 * a.scrim_strength),
                                         ease=a.scrim_ease))
    if a.scrim in ("top", "both"):
        canvas.alpha_composite(vgradient(W, H, scrim_col, int(255 * a.scrim_strength), 0,
                                         ease=a.scrim_ease))
    if a.scrim == "full":
        canvas.alpha_composite(Image.new("RGBA", (W, H), scrim_col + (int(255 * a.scrim_strength),)))

    bg_snapshot = canvas.convert("RGB")   # kontrast denetimi metinden ONCE olculur
    d = ImageDraw.Draw(canvas)
    cw = W - sl - sr                      # kullanilabilir genislik
    fg = parse_color(a.fg) or WHITE
    accent = parse_color(a.accent) or GOLD

    # --- olcekleme: 1080 genisligi taban al
    k = W / 1080.0
    px = lambda v: max(1, int(round(v * k)))

    blocks = []   # (yukseklik, cizim fonksiyonu)

    if a.eyebrow:
        f = load(BODY_BOLD_CHAIN, px(a.eyebrow_size), "body")
        txt = a.eyebrow.upper()
        h = int(f.size * 1.35)
        def draw_eyebrow(y, f=f, txt=txt, h=h):
            tracked(d, (sl, y), txt, f, accent, a.eyebrow_tracking)
            return h
        blocks.append((h + px(20), draw_eyebrow))

    if a.rule:
        rw = px(a.rule_width)
        def draw_rule(y, rw=rw):
            d.rectangle([sl, y, sl + rw, y + px(2)], fill=accent)
            return px(2)
        blocks.append((px(2) + px(26), draw_rule))

    # dev rakam (sayi karti modu) — eyebrow ve ayractan sonra gelir
    if a.number:
        f = load(DISPLAY_CHAIN, px(a.number_size), "display")
        h = int(f.size * 1.02)
        def draw_number(y, f=f, h=h):
            tracked(d, (sl, y - int(f.size * 0.24)), a.number, f, accent, 0.01)
            return h
        blocks.append((h + px(18), draw_number))

    if a.title:
        f = load(DISPLAY_CHAIN, px(a.title_size), "display")
        lines = wrap(a.title, f, cw, a.title_tracking)
        lh = int(f.size * a.title_leading)
        h = lh * len(lines)
        def draw_title(y, f=f, lines=lines, lh=lh, h=h):
            yy = y - int(f.size * 0.22)
            for ln in lines:
                tracked(d, (sl, yy), ln, f, fg, a.title_tracking)
                yy += lh
            return h
        blocks.append((h + px(22), draw_title))

    if a.body:
        f = load(BODY_CHAIN, px(a.body_size), "body")
        lines = []
        for para in a.body.split("\n"):
            lines += wrap(para, f, cw) if para.strip() else [""]
        lh = int(f.size * a.body_leading)
        h = lh * len(lines)
        def draw_body(y, f=f, lines=lines, lh=lh, h=h):
            yy = y
            for ln in lines:
                d.text((sl, yy), ln, font=f, fill=fg)
                yy += lh
            return h
        blocks.append((h + px(18), draw_body))

    if a.table:
        f = load(BODY_CHAIN, px(a.table_size), "body")
        fv = load(BODY_BOLD_CHAIN, px(a.table_size), "body")
        rows = [r for r in a.table.split("\n") if r.strip()]
        parsed = []
        for r in rows:
            if "|" in r:
                lbl, val = r.split("|", 1)          # k/v kullanma: k olcek carpani
                parsed.append((lbl.strip(), val.strip()))
            else:
                parsed.append((r.strip(), ""))
        lh = int(f.size * a.table_leading)
        h = lh * len(parsed)
        def draw_table(y, f=f, fv=fv, parsed=parsed, lh=lh, h=h):
            yy = y
            for k, v in parsed:
                d.text((sl, yy), k, font=f, fill=fg)
                if v:
                    vw = fv.getlength(v)
                    vx = sl + cw - vw
                    d.text((vx, yy), v, font=fv, fill=accent)
                    # ince nokta ayrac
                    kx = sl + f.getlength(k) + px(12)
                    dot_y = yy + int(f.size * 0.62)
                    x = kx
                    while x < vx - px(12):
                        d.rectangle([x, dot_y, x + px(2), dot_y + px(2)],
                                    fill=(accent[0], accent[1], accent[2]))
                        x += px(10)
                yy += lh
            return h
        blocks.append((h + px(20), draw_table))

    if a.kicker:
        f = load(BODY_BOLD_CHAIN, px(a.kicker_size), "body")
        lines = wrap(a.kicker, f, cw)
        lh = int(f.size * 1.45)
        h = lh * len(lines)
        def draw_kicker(y, f=f, lines=lines, lh=lh, h=h):
            yy = y
            for ln in lines:
                d.text((sl, yy), ln, font=f, fill=accent)
                yy += lh
            return h
        blocks.append((h + px(10), draw_kicker))

    total = sum(b[0] for b in blocks)

    # --- dikey hizalama
    note_reserve = px(int(a.note_size * 2.2)) if a.note else 0
    if a.align == "bottom":
        y = H - sb - total - note_reserve
    elif a.align == "center":
        y = (H - total) // 2
    else:
        y = st
    if a.offset:
        y += px(a.offset)

    # --- inset: plan/gorsel karti (metin blogunun ustunde, kirpilmadan)
    if a.inset and os.path.exists(a.inset):
        pad = px(a.inset_pad)
        top = st + (px(a.inset_top) if a.inset_top else (px(190) if "top" in a.logo_pos and a.logo != "none" else px(20)))
        bottom = y - px(a.inset_gap)
        box_w, box_h = cw, bottom - top
        if box_h > px(120):
            ins = Image.open(a.inset).convert("RGBA")
            ins = contain(ins, box_w - 2 * pad, box_h - 2 * pad)
            cx = sl + (cw - ins.width) // 2
            cy = top + (box_h - ins.height) // 2
            card = parse_color(a.inset_bg) if a.inset_bg != "none" else None
            if card:
                panel = Image.new("RGBA", (ins.width + 2 * pad, ins.height + 2 * pad), card + (255,))
                canvas.alpha_composite(panel, (cx - pad, cy - pad))
            canvas.alpha_composite(ins, (cx, cy))
        else:
            sys.stderr.write("[not] inset icin yeterli dikey alan yok — metni kisalt ya da --title-size dusur\n")

    for advance, fn in blocks:
        fn(y)
        y += advance

    # --- logo
    if a.logo != "none":
        lw = px(a.logo_width)
        lp = logo_png(a.logo, lw * 3)
        if lp:
            lg = Image.open(lp).convert("RGBA")
            lg.thumbnail((lw, lw * 3), Image.LANCZOS)
            pos = a.logo_pos
            lx = sl if "left" in pos else (W - sr - lg.width if "right" in pos else (W - lg.width)//2)
            ly = st if "top" in pos else H - sb - lg.height
            canvas.alpha_composite(lg, (lx, ly))
        else:
            sys.stderr.write("[not] logo SVG bulunamadi ya da rsvg-convert yok, logo atlandi\n")

    # --- kucuk not (temsili gorseldir)
    if a.note:
        f = load(BODY_CHAIN, px(a.note_size), "body")
        tw = f.getlength(a.note)
        nx = W - sr - tw if a.note_pos == "right" else sl
        ny = H - sb - int(f.size * 1.3)
        d.text((nx, ny), a.note, font=f, fill=(230, 230, 230))

    # --- guvenli alan kilavuzu (yalnizca denetim icin)
    if a.guides:
        gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(gl)
        gd.rectangle([0, 0, W, st], fill=(255, 0, 80, 60))
        gd.rectangle([0, H - sb, W, H], fill=(255, 0, 80, 60))
        gd.rectangle([0, 0, sl, H], fill=(255, 0, 80, 40))
        gd.rectangle([W - sr, 0, W, H], fill=(255, 0, 80, 40))
        gd.rectangle([sl, st, W - sr, H - sb], outline=(0, 255, 180, 200), width=3)
        f = load(BODY_CHAIN, px(26), "body")
        gd.text((sl + 8, st + 8), f"{a.preset}  {W}x{H}  guvenli: {st}/{sb}/{sl}/{sr}",
                font=f, fill=(0, 255, 180, 230))
        canvas.alpha_composite(gl)

    out = canvas.convert("RGB")

    # --- otomatik kontrast denetimi: metin bloklarinin arkasindaki zemin
    if blocks and not a.no_check:
        y_start = (H - sb - total - note_reserve) if a.align == "bottom" else \
                  ((H - total) // 2 if a.align == "center" else st)
        y_start += px(a.offset)
        check_text_contrast(bg_snapshot, sl, min(W - sr, sl + cw), y_start,
                            min(H, y_start + total), fg, accent)

    ext = os.path.splitext(a.out)[1].lower()
    if ext in (".jpg", ".jpeg"):
        out.save(a.out, quality=a.quality, subsampling=0, optimize=True)
    else:
        out.save(a.out)
    print(f"{a.out}  {W}x{H}  ({a.preset})")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--preset", required=True, help=", ".join(PRESETS))
    p.add_argument("--out", required=True)

    p.add_argument("--bg", help="arka plan fotografi")
    p.add_argument("--bg-focus", default="center",
                   choices=["center", "top", "bottom", "left", "right"])
    p.add_argument("--bg-blur", type=float, default=0)
    p.add_argument("--bg-color", default="ink", help="hex ya da: " + ", ".join(PALETTE))
    p.add_argument("--bg-gradient", help="'ink,navy700' gibi iki renk")

    p.add_argument("--scrim", default="bottom",
                   choices=["none", "bottom", "top", "both", "full"])
    p.add_argument("--scrim-strength", type=float, default=0.88)
    p.add_argument("--scrim-color", default="ink")
    p.add_argument("--scrim-ease", type=float, default=2.0,
                   help="degrade egrisi; 1.0 dogrusal, <1 daha erken koyulasir")

    p.add_argument("--eyebrow"); p.add_argument("--eyebrow-size", type=int, default=26)
    p.add_argument("--eyebrow-tracking", type=float, default=0.22)
    p.add_argument("--title");   p.add_argument("--title-size", type=int, default=88)
    p.add_argument("--title-tracking", type=float, default=0.02)
    p.add_argument("--title-leading", type=float, default=1.16)
    p.add_argument("--body");    p.add_argument("--body-size", type=int, default=38)
    p.add_argument("--body-leading", type=float, default=1.55)
    p.add_argument("--kicker");  p.add_argument("--kicker-size", type=int, default=32)
    p.add_argument("--table", help="mahal listesi: her satir 'Etiket|Deger' biciminde")
    p.add_argument("--table-size", type=int, default=34)
    p.add_argument("--table-leading", type=float, default=1.72)
    p.add_argument("--number");  p.add_argument("--number-size", type=int, default=210)
    p.add_argument("--note");    p.add_argument("--note-size", type=int, default=22)
    p.add_argument("--note-pos", default="right", choices=["right", "left"])

    p.add_argument("--fg", default="white")
    p.add_argument("--accent", default="gold")
    p.add_argument("--rule", action="store_true", help="altin ince ayrac cizgisi")
    p.add_argument("--rule-width", type=int, default=110)

    p.add_argument("--align", default="bottom", choices=["top", "center", "bottom"])
    p.add_argument("--offset", type=int, default=0)
    p.add_argument("--safe-pad", type=int, default=0)

    p.add_argument("--logo", default="dark",
                   choices=["dark", "dark-mark", "light", "light-mark", "none"])
    p.add_argument("--logo-pos", default="top-left",
                   choices=["top-left", "top-right", "top-center",
                            "bottom-left", "bottom-right", "bottom-center"])
    p.add_argument("--logo-width", type=int, default=150)

    p.add_argument("--inset", help="metin blogunun ustune kirpilmadan yerlestirilecek gorsel (plan, tablo)")
    p.add_argument("--inset-bg", default="cream", help="inset arkasindaki kart rengi; 'none' ile kapat")
    p.add_argument("--inset-pad", type=int, default=34)
    p.add_argument("--inset-top", type=int, default=0, help="ust bosluk; 0 ise logoya gore otomatik")
    p.add_argument("--inset-gap", type=int, default=44, help="inset ile metin arasi bosluk")
    p.add_argument("--guides", action="store_true", help="guvenli alan kilavuzu")
    p.add_argument("--no-check", action="store_true", help="kontrast denetimini atla")
    p.add_argument("--quality", type=int, default=92)
    build(p.parse_args())


if __name__ == "__main__":
    main()

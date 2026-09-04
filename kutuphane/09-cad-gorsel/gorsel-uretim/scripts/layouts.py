"""layouts.py — frame.py'nin karsilamadigi ozel duzenler.

frame.py tek sutunlu, metin-blogu-altta bir kalibi cok iyi yapiyor. Bu dosya
o kalibin disinda kalan bes duzeni tutuyor; hepsi ayni marka altyapisini
(renk, font, logo, kontrast) frame.py'den ithal ediyor.

  diptik      iki plani AYNI olcekte yan yana — karsilastirma
  oran        plansiz veri gorseli, net m2 orantili yatay cubuklar
  kanama      plan tam kanama + koyu bilgi paneli (dergi serimi)
  cerceve     ince altin cerceve icinde ortalanmis plan (davetiye hissi)
  daire       dairesel maske — logodaki ay/hilal motifiyle konusur

Calistir:  python3 scripts/layouts.py           (hepsini uretir)
Yeni tip icin: ilgili fonksiyondaki dosya yolunu ve rakamlari degistir.
Cikti dizini OUT sabitinde.
"""
import sys, os
sys.path.insert(0, ".claude/skills/gorsel-uretim/scripts")
import frame as F
from PIL import Image, ImageDraw, ImageFilter

INK, NAVY7, GOLD, CREAM, WHITE = F.INK, F.NAVY_700, F.GOLD, F.CREAM, F.WHITE
GOLD_D = (122, 97, 22)          # krem uzerinde okunakli altin
PG = "Sosyal Medya Çıktıları/plan-gorselleri"
OUT = "Sosyal Medya Çıktıları/2026-08"

def disp(sz):  return F.load(F.DISPLAY_CHAIN, sz, "display")
def body(sz):  return F.load(F.BODY_CHAIN, sz, "body")
def bodyb(sz): return F.load(F.BODY_BOLD_CHAIN, sz, "body")

def logo(variant, w):
    p = F.logo_png(variant, w * 3)
    if not p: return None
    im = Image.open(p).convert("RGBA"); im.thumbnail((w, w * 3), Image.LANCZOS)
    return im

def eyebrow(d, x, y, txt, col, size, track=0.22):
    f = bodyb(size); F.tracked(d, (x, y), txt.upper(), f, col, track)
    return int(f.size * 1.35)

def rule(d, x, y, w, col, h=3):
    d.rectangle([x, y, x + w, y + h], fill=col)

def vgrad_scrim(w, h, col, strength, ease=0.8):
    return F.vgradient(w, h, col, 0, int(255 * strength), ease=ease)

# ─────────────────────────────────────────────────────── A2 · diptik
def a2():
    W, H = 1080, 1350
    c = Image.new("RGBA", (W, H), INK + (255,))
    d = ImageDraw.Draw(c)
    half = W // 2
    d.rectangle([half, 0, W, H], fill=CREAM + (255,))
    d.rectangle([half - 2, 0, half + 2, H], fill=GOLD + (255,))

    panels = [
        dict(x0=0, x1=half, plan=f"{PG}/plan_tip2.png", fg=WHITE, acc=GOLD, card=WHITE,
             eb="TİP 2 · 1+1", num="40,49", sub="net m²", note="Salon & mutfak 22,25 m²"),
        dict(x0=half, x1=W, plan=f"{PG}/plan_tip5.png", fg=INK, acc=GOLD_D, card=WHITE,
             eb="TİP 5 · 3+1", num="96,54", sub="net m²", note="Salon & mutfak 36,05 m²"),
    ]
    # Iki plani AYNI olcege getir: cizilen alan net alanla orantili olsun.
    # Lineer katsayi = sqrt(net_orani); boylece gorsel alan orani = m2 orani.
    import math
    raw = [Image.open(p["plan"]).convert("RGBA") for p in panels]
    nets = [40.49, 96.54]
    # once buyuk olani kutuya sigdir, kucugu ayni olcekle kucult
    box_w, box_h = half - 2 * 42 - 24, 640
    big = F.contain(raw[1], box_w, box_h)
    k_lin = math.sqrt(nets[0] / nets[1])          # 0.648
    small_w = max(1, int(big.width * k_lin))
    small = raw[0].resize((small_w, max(1, int(raw[0].height * small_w / raw[0].width))), Image.LANCZOS)
    fitted = [small, big]

    for idx, p in enumerate(panels):
        pw = p["x1"] - p["x0"]; pad = 42
        plan = fitted[idx]
        cx = p["x0"] + (pw - plan.width) // 2
        cy = 250 + (box_h - plan.height) // 2
        card = Image.new("RGBA", (plan.width + 24, plan.height + 24), p["card"] + (255,))
        c.alpha_composite(card, (cx - 12, cy - 12)); c.alpha_composite(plan, (cx, cy))

        x = p["x0"] + pad; y = 1000
        y += eyebrow(d, x, y, p["eb"], p["acc"], 24, 0.20) + 10
        rule(d, x, y, 92, p["acc"]); y += 32
        fn = disp(118); F.tracked(d, (x, y - 26), p["num"], fn, p["fg"], 0.01); y += int(fn.size * 1.02)
        fs = body(30); d.text((x, y), p["sub"], font=fs, fill=p["acc"]); y += int(fs.size * 1.7)
        fnn = body(28); d.text((x, y), p["note"], font=fnn, fill=p["fg"])
        y += int(fnn.size * 1.55)
        fsc = body(23)
        d.text((x, y), "Planlar net alana göre orantılı ölçekte.", font=fsc,
               fill=(p["acc"] if idx == 1 else (176, 184, 200)))

    lg = logo("dark", 128)
    if lg: c.alpha_composite(lg, (42, 60))
    lg2 = logo("light", 128)
    if lg2: c.alpha_composite(lg2, (W - 42 - lg2.width, 60))
    c.convert("RGB").save(f"{OUT}/plan-A2-diptik.png"); print("plan-A2-diptik.png")

# ─────────────────────────────────────────────────── A3 · oran cubuklari
def a3():
    W, H = 1080, 1350
    c = Image.new("RGBA", (W, H), INK + (255,))
    g = F.vgradient(W, H, F.NAVY_700, 90, 0, ease=1.4)
    c.alpha_composite(g)
    d = ImageDraw.Draw(c)
    lg = logo("dark", 150)
    if lg: c.alpha_composite(lg, (64, 70))

    x = 64; y = 300
    y += eyebrow(d, x, y, "GERÇEK ÖLÇEKTE", GOLD, 26) + 12
    rule(d, x, y, 110, GOLD); y += 40
    ft = disp(76)
    for line in F.wrap("Altı tip, aynı cetvelde.", ft, W - 128, 0.02):
        F.tracked(d, (x, y - 16), line, ft, WHITE, 0.02); y += int(ft.size * 1.16)
    y += 46

    data = [("Tip 2 · 1+1", 40.49), ("Tip 3 · 2+1", 56.25), ("Tip 1 · 2+1", 65.32),
            ("Tip 6 · 2+1", 75.52), ("Tip 4 · 3+1", 81.80), ("Tip 5 · 3+1", 96.54)]
    mx = max(v for _, v in data)
    bar_max = W - 128
    fl = body(30); fv = bodyb(30)
    for name, val in data:
        d.text((x, y), name, font=fl, fill=WHITE)
        vs = f"{val:.2f}".replace(".", ",") + " m²"
        vw = fv.getlength(vs); d.text((x + bar_max - vw, y), vs, font=fv, fill=GOLD)
        y += int(fl.size * 1.5)
        bw = int(bar_max * val / mx)
        d.rectangle([x, y, x + bw, y + 16], fill=GOLD)
        d.rectangle([x + bw, y + 7, x + bar_max, y + 9], fill=(60, 74, 104))
        y += 58
    fk = bodyb(28)
    d.text((x, y + 6), "Net alanlar. Çubuk uzunlukları gerçek orana göre.", font=fk, fill=GOLD)
    c.convert("RGB").save(f"{OUT}/plan-A3-oran.png"); print("plan-A3-oran.png")

# ──────────────────────────────────────── B2 · tam kanama plan + koyu panel
def b2():
    W, H = 1080, 1350
    split = 820
    c = Image.new("RGBA", (W, H), WHITE + (255,))
    d = ImageDraw.Draw(c)
    d.rectangle([0, split, W, H], fill=INK + (255,))
    plan = Image.open(f"{PG}/plan_tip3.png").convert("RGBA")
    plan = F.contain(plan, W - 120, split - 190)
    c.alpha_composite(plan, ((W - plan.width) // 2, 130 + (split - 190 - plan.height) // 2))
    d.rectangle([0, split - 4, W, split], fill=GOLD + (255,))
    lg = logo("light", 132)
    if lg: c.alpha_composite(lg, (60, 46))

    x = 64; y = split + 64
    y += eyebrow(d, x, y, "TİP 3 · 2+1 · 1–9. KATLAR", GOLD, 24) + 10
    rule(d, x, y, 92, GOLD); y += 34
    ft = disp(62)
    F.tracked(d, (x, y - 14), "Net 56,25 m² · brüt 82,70 m²", ft, WHITE, 0.02)
    y += int(ft.size * 1.22)
    fb = body(30)
    for line in F.wrap("Salon & mutfak 25,02 · Yatak odası 14,26 ve 9,72 · Banyo 3,65 · Antre 3,65 m²", fb, W - 128):
        d.text((x, y), line, font=fb, fill=(228, 228, 232)); y += int(fb.size * 1.5)
    c.convert("RGB").save(f"{OUT}/plan-B2-kanama.png"); print("plan-B2-kanama.png")

# ─────────────────────────────────────────────── B3 · altin cerceve (krem)
def b3():
    W, H = 1080, 1350
    m = 54
    c = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(c)
    d.rectangle([m, m, W - m, H - m], outline=GOLD_D + (255,), width=2)
    lg = logo("light", 118)
    if lg: c.alpha_composite(lg, ((W - lg.width) // 2, m + 44))
    plan = Image.open(f"{PG}/plan_tip3.png").convert("RGBA")
    plan = F.contain(plan, W - 2 * m - 130, 600)
    c.alpha_composite(plan, ((W - plan.width) // 2, 300))

    cy = 990
    d.rectangle([(W - 90) // 2, cy, (W + 90) // 2, cy + 2], fill=GOLD_D + (255,))
    y = cy + 34
    fe = bodyb(24); txt = "TİP 3 · 2+1 · 1–9. KATLAR"
    tw = F.tracked_width(txt, fe, 0.22)
    F.tracked(d, ((W - tw) // 2, y), txt, fe, GOLD_D, 0.22); y += int(fe.size * 1.9)
    ft = disp(60); t = "Net 56,25 m² · brüt 82,70 m²"
    tw = F.tracked_width(t, ft, 0.02)
    F.tracked(d, ((W - tw) // 2, y - 14), t, ft, INK, 0.02); y += int(ft.size * 1.25)
    fb = body(29)
    for line in F.wrap("Salon & mutfak 25,02 · Yatak odası 14,26 ve 9,72 · Banyo 3,65 · Antre 3,65 m²", fb, W - 2 * m - 180):
        lw = fb.getlength(line); d.text(((W - lw) // 2, y), line, font=fb, fill=(52, 58, 72))
        y += int(fb.size * 1.5)
    c.convert("RGB").save(f"{OUT}/plan-B3-cerceve.png"); print("plan-B3-cerceve.png")

# ───────────────────────────────────────────── E2 · tam kanama zoom (story)
def e2():
    W, H = 1080, 1920
    src = Image.open("/private/tmp/claude-502/-Users-farukciftler-Documents-GitHub-moonstone/194c5b73-f32f-45f3-931e-f519e89efe53/scratchpad/tip5_salon.png").convert("RGB")
    c = F.cover(src, W, H, "top").convert("RGBA")
    c.alpha_composite(vgrad_scrim(W, H, INK, 1.0, 0.7))
    c.alpha_composite(F.vgradient(W, H, INK, 150, 0, ease=2.2))
    d = ImageDraw.Draw(c)
    lg = logo("dark", 150)
    if lg: c.alpha_composite(lg, (65, 250))
    x = 65; y = 1180
    y += eyebrow(d, x, y, "TİP 5 · SALON & MUTFAK", GOLD, 26) + 12
    rule(d, x, y, 110, GOLD); y += 44
    fn = disp(168); F.tracked(d, (x, y - 38), "36,05 m²", fn, GOLD, 0.01)
    y += int(fn.size * 1.04)
    fb = body(38)
    for line in F.wrap("Altı tipin en cömert yaşam alanı. 10. katta, geniş teraslı daire.", fb, W - 130):
        d.text((x, y), line, font=fb, fill=WHITE); y += int(fb.size * 1.52)
    c.convert("RGB").save(f"{OUT}/plan-E2-kanama.png"); print("plan-E2-kanama.png")

# ────────────────────────────────────── E3 · dairesel maske (logo motifi)
def e3():
    W, H = 1080, 1920
    D = 780
    c = Image.new("RGBA", (W, H), INK + (255,))
    c.alpha_composite(F.vgradient(W, H, F.NAVY_700, 110, 0, ease=1.5))
    src = Image.open("/private/tmp/claude-502/-Users-farukciftler-Documents-GitHub-moonstone/194c5b73-f32f-45f3-931e-f519e89efe53/scratchpad/tip5_salon.png").convert("RGB")
    # planin sag kenarindan degil, salon merkezinden kirp
    sw, sh = src.size
    sq = int(min(sw, sh) * 0.86)
    ox, oy = int((sw - sq) * 0.28), int((sh - sq) * 0.46)
    src_sq = src.crop((ox, oy, ox + sq, oy + sq))
    disc = src_sq.resize((D, D), Image.LANCZOS)
    mask = Image.new("L", (D * 4, D * 4), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, D * 4, D * 4], fill=255)
    mask = mask.resize((D, D), Image.LANCZOS)
    disc.putalpha(mask)
    cx, cy = (W - D) // 2, 470
    ring = Image.new("RGBA", (D + 26, D + 26), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse([1, 1, D + 24, D + 24], outline=GOLD + (255,), width=3)
    c.alpha_composite(ring, (cx - 13, cy - 13))
    c.alpha_composite(disc, (cx, cy))

    d = ImageDraw.Draw(c)
    lg = logo("dark", 150)
    if lg: c.alpha_composite(lg, ((W - lg.width) // 2, 250))
    y = 1400
    fe = bodyb(26); txt = "TİP 5 · SALON & MUTFAK"
    tw = F.tracked_width(txt, fe, 0.22); F.tracked(d, ((W - tw) // 2, y), txt, fe, GOLD, 0.22)
    y += int(fe.size * 1.9)
    d.rectangle([(W - 100) // 2, y, (W + 100) // 2, y + 3], fill=GOLD); y += 40
    fn = disp(160); t = "36,05 m²"
    tw = F.tracked_width(t, fn, 0.01)
    F.tracked(d, ((W - tw) // 2, y - 36), t, fn, WHITE, 0.01); y += int(fn.size * 1.02)
    fb = body(36)
    for line in F.wrap("Altı tipin en cömert yaşam alanı.", fb, W - 200):
        lw = fb.getlength(line); d.text(((W - lw) // 2, y), line, font=fb, fill=(226, 228, 234))
        y += int(fb.size * 1.5)
    c.convert("RGB").save(f"{OUT}/plan-E3-daire.png"); print("plan-E3-daire.png")

for fn in (a2, a3, b2, b3, e2, e3):
    fn()

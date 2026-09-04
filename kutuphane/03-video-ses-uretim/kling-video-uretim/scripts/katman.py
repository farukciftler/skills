#!/usr/bin/env python3
"""
katman.py — video üstüne binecek şeffaf marka katmanı (PNG) üretir.

gorsel-uretim/frame.py'nin font, logo ve degrade altyapısını yeniden kullanır;
renk/font tek yerden yönetilir. Kural kaynağı: gorsel-yon-referans.md K3–K5, K7.
  • tam kanama, kutu yok — okunabilirlik için yalnızca alt degrade
  • en fazla üç öğe: logo · tek satır display başlık · "Temsili görseldir"
  • display satır Cormorant Garamond 300–400, beyaz, harf aralığı 0,08–0,12 em
  • güvenli alan: cross-9x16 (üst 140 / alt 400 / sol 60 / sağ 180) varsayılan

  python3 katman.py --preset cross-9x16 --baslik "Ay taşının zarafeti" --out katman.png
  python3 katman.py --preset cross-9x16 --tek-kelime "PRESTİJ" --out katman.png
  python3 katman.py --preset cross-9x16 --sadece-logo --out logo-kart.png   # kapanış karesi

Sonra:  bitir.py --katman katman.png ...   (ffmpeg overlay)
"""
import argparse, os, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "gorsel-uretim", "scripts"))
try:
    import frame as F   # PRESETS, load, DISPLAY_CHAIN, BODY_CHAIN, tracked, tracked_width, vgradient, logo_png, INK, WHITE
except ImportError:
    sys.exit("gorsel-uretim/scripts/frame.py bulunamadı — bu skill onun altyapısını kullanır")

_BUYUK_TR = str.maketrans("iı", "İI")
def buyuk(t):
    """Python upper() Türkçe bilmez: 'Prestij'.upper() → PRESTIJ. Doğrusu PRESTİJ."""
    return t.translate(_BUYUK_TR).upper()

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--preset", default="cross-9x16", help=", ".join(F.PRESETS))
    p.add_argument("--out", required=True)
    p.add_argument("--baslik", help="tek satır display başlık (alt üçte bir)")
    p.add_argument("--baslik-boyut", type=int, default=72)
    p.add_argument("--baslik-aralik", type=float, default=0.10, help="em; K5: 0,08–0,12")
    p.add_argument("--tek-kelime", help="PRESTİJ tipi tek kelime; aralık 0,20 em, büyük")
    p.add_argument("--not", dest="note", default="Temsili görseldir", help="'' ile kapat")
    p.add_argument("--not-boyut", type=int, default=24)
    p.add_argument("--logo", default="dark", choices=["dark", "dark-mark", "light", "light-mark", "none"])
    p.add_argument("--logo-pos", default="top-left", choices=["top-left", "top-right", "top-center", "bottom-center"])
    p.add_argument("--logo-width", type=int, default=150)
    p.add_argument("--degrade", type=float, default=0.72, help="alt degrade gücü 0–1; K3: rgba(4,12,29,.72)")
    p.add_argument("--degrade-yukseklik", type=float, default=0.45, help="karenin altından oran")
    p.add_argument("--sadece-logo", action="store_true", help="kapanış karesi: lacivert zemin + ortada logo (opak PNG)")
    p.add_argument("--zemin", default="ink", help="--sadece-logo zemin rengi")
    p.add_argument("--hizalama", default="left", choices=["left", "center"])
    p.add_argument("--kaydir", type=int, default=0, help="başlığı dikeyde kaydır (px, + aşağı)")
    p.add_argument("--guides", action="store_true")
    a = p.parse_args()

    if a.preset not in F.PRESETS:
        sys.exit("preset bilinmiyor: " + a.preset)
    P = F.PRESETS[a.preset]; W, H = P["w"], P["h"]; st, sb, sl, sr = P["safe"]
    k = W / 1080.0; px = lambda v: max(1, int(round(v * k)))

    if a.sadece_logo:
        canvas = Image.new("RGBA", (W, H), F.parse_color(a.zemin) + (255,))
    else:
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    items = 0
    # --- alt degrade (K3): yalnızca metin varsa
    if not a.sadece_logo and (a.baslik or a.tek_kelime):
        gh = int(H * a.degrade_yukseklik)
        g = F.vgradient(W, gh, F.INK, 0, int(255 * a.degrade), ease=1.6)
        canvas.alpha_composite(g, (0, H - gh))

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))   # metin+logo+not: güvenli alan bu katmandan ölçülür
    d = ImageDraw.Draw(layer)
    cw = W - sl - sr

    # --- başlık
    if a.tek_kelime:
        f = F.load(F.DISPLAY_CHAIN, px(112), "display")
        txt = buyuk(a.tek_kelime); tr = 0.20
        tw = F.tracked_width(txt, f, tr)
        x = sl + (cw - tw) // 2
        y = H - sb - px(90) - int(f.size * 1.1) + px(a.kaydir)   # notun hemen üstü, alt üçte bir
        F.tracked(d, (x, y), txt, f, F.WHITE, tr); items += 1
    elif a.baslik:
        f = F.load(F.DISPLAY_CHAIN, px(a.baslik_boyut), "display")
        lines = F.wrap(a.baslik, f, cw, a.baslik_aralik)
        if len(lines) > 2:
            sys.stderr.write("[UYARI] başlık 2 satırı aşıyor — K4/K5: tek satır hedefle, kısalt ya da --baslik-boyut düşür\n")
        lh = int(f.size * 1.18)
        y = H - sb - px(80) - lh * len(lines) + px(a.kaydir)      # notun hemen üstü, alt üçte bir
        for ln in lines:
            tw = F.tracked_width(ln, f, a.baslik_aralik)
            x = sl + px(6) if a.hizalama == "left" else sl + (cw - tw) // 2   # ince serif mürekkebi orijinin soluna taşar
            F.tracked(d, (x, y), ln, f, F.WHITE, a.baslik_aralik)
            y += lh
        items += 1

    # --- logo
    if a.logo != "none":
        lw = px(a.logo_width if not a.sadece_logo else 420)
        lp = F.logo_png(a.logo, lw * 3)
        if lp:
            lg = Image.open(lp).convert("RGBA"); lg.thumbnail((lw, lw * 3), Image.LANCZOS)
            if a.sadece_logo:
                layer.alpha_composite(lg, ((W - lg.width) // 2, (H - lg.height) // 2))
            else:
                pos = a.logo_pos
                lx = sl if "left" in pos else (W - sr - lg.width if "right" in pos else (W - lg.width) // 2)
                ly = st if "top" in pos else H - sb - lg.height
                layer.alpha_composite(lg, (lx, ly))
            items += 1
        else:
            sys.stderr.write("[not] logo üretilemedi (rsvg-convert / SVG yolu)\n")

    # --- not (K7): okunur boyut, güvenli alan içinde
    if a.note and not a.sadece_logo:
        f = F.load(F.BODY_CHAIN, px(a.not_boyut), "body")
        tw = f.getlength(a.note)
        d.text((W - sr - tw - px(4), H - sb - int(f.size * 1.4)), a.note, font=f, fill=(235, 235, 235, 255))
        items += 1

    if items > 3:
        sys.stderr.write(f"[UYARI] karede {items} öğe — K4: en fazla üç\n")

    # --- güvenli alan: yüzde değil, mürekkep kutusu (reelsindustry kart.py kalıbı)
    bbox = layer.split()[-1].getbbox()
    if bbox and not a.sadece_logo:
        x0, y0, x1, y1 = bbox
        ihlal = []
        if y0 < st: ihlal.append(f"üst UI bandına {st - y0} px giriyor")
        if y1 > H - sb: ihlal.append(f"alt UI bandına {y1 - (H - sb)} px giriyor")
        if x0 < sl: ihlal.append(f"sol kenara {sl - x0} px giriyor")
        if x1 > W - sr: ihlal.append(f"sağ UI bandına {x1 - (W - sr)} px giriyor")
        for m in ihlal:
            sys.stderr.write(f"[UYARI] güvenli alan: {m}\n")
    canvas.alpha_composite(layer)

    if a.guides:
        gl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
        gd.rectangle([0, 0, W, st], fill=(255, 0, 80, 60)); gd.rectangle([0, H - sb, W, H], fill=(255, 0, 80, 60))
        gd.rectangle([0, 0, sl, H], fill=(255, 0, 80, 40)); gd.rectangle([W - sr, 0, W, H], fill=(255, 0, 80, 40))
        canvas.alpha_composite(gl)

    canvas.save(a.out)
    print(f"{a.out}  {W}x{H}  ({a.preset}, {items} öğe)")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
hazirla.py — Kling'e gidecek başlangıç karesini hazırlar.

Kling 2.x/3.x image-to-video çıktının oranını GİRDİ GÖRSELİNDEN alır; API'de
aspect_ratio yok. Reels için 9:16 istiyorsan görseli önce 9:16 kırpmalısın.
Bu betik: doğru orana kırpar (odak seçilebilir), sRGB'ye çevirir, EXIF'i atar,
kısa kenar / oran / boyut sınırlarını denetler, kalite 95 JPEG yazar.

  python3 hazirla.py cephe.jpg --oran 9:16 --odak center --out cephe-9x16.jpg
  python3 hazirla.py cephe.jpg --oran 9:16 --odak bottom --min-kenar 1080

Sınırlar (fal Kling sayfaları): jpg/png, ≤ 50 MB, kısa kenar ≥ 300 px,
oran 1:2,5 – 2,5:1. Kalite için hedef: kısa kenar ≥ 1080 px.
"""
import argparse, os, sys
from PIL import Image, ImageCms, ImageOps

ORAN = {"9:16": 9/16, "16:9": 16/9, "4:5": 4/5, "1:1": 1.0, "3:4": 3/4, "4:3": 4/3, "21:9": 21/9}

def to_srgb(img):
    icc = img.info.get("icc_profile")
    if icc:
        try:
            src = ImageCms.ImageCmsProfile(__import__("io").BytesIO(icc))
            dst = ImageCms.createProfile("sRGB")
            return ImageCms.profileToProfile(img, src, dst, outputMode="RGB")
        except Exception:
            pass
    return img.convert("RGB")

def crop_ratio(img, r, focus):
    w, h = img.size
    cur = w / h
    if abs(cur - r) < 1e-3:
        return img
    if cur > r:              # fazla geniş → yanlardan kırp
        nw = int(round(h * r)); nh = h
        fx = {"left": 0.0, "center": 0.5, "right": 1.0}.get(focus, 0.5)
        x = int((w - nw) * fx); y = 0
    else:                    # fazla uzun → üst/alttan kırp
        nw = w; nh = int(round(w / r))
        fy = {"top": 0.0, "center": 0.5, "bottom": 1.0}.get(focus, 0.5)
        x = 0; y = int((h - nh) * fy)
    return img.crop((x, y, x + nw, y + nh))

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("girdi"); p.add_argument("--out")
    p.add_argument("--oran", default="9:16", help=", ".join(ORAN) + " ya da 'kaynak'")
    p.add_argument("--odak", default="center", choices=["center", "top", "bottom", "left", "right"])
    p.add_argument("--min-kenar", type=int, default=1080, help="uyarı eşiği (px)")
    p.add_argument("--maks-kenar", type=int, default=4096, help="uzun kenar bundan büyükse küçült")
    p.add_argument("--kalite", type=int, default=95)
    a = p.parse_args()

    img = Image.open(a.girdi)
    img = ImageOps.exif_transpose(img)
    img = to_srgb(img)
    w0, h0 = img.size

    if a.oran != "kaynak":
        if a.oran not in ORAN:
            sys.exit("oran bilinmiyor: " + a.oran)
        img = crop_ratio(img, ORAN[a.oran], a.odak)

    w, h = img.size
    if max(w, h) > a.maks_kenar:
        s = a.maks_kenar / max(w, h)
        img = img.resize((int(w * s), int(h * s)), Image.LANCZOS)
        w, h = img.size

    out = a.out or os.path.splitext(a.girdi)[0] + f"-{a.oran.replace(':', 'x')}.jpg"
    img.save(out, "JPEG", quality=a.kalite, subsampling=0, optimize=True)  # EXIF/ICC yazılmaz
    size = os.path.getsize(out)

    # --- denetim
    ratio = w / h
    notes = []
    if min(w, h) < 300:
        notes.append("HATA: kısa kenar 300 px altında — fal reddeder")
    elif min(w, h) < a.min_kenar:
        notes.append(f"UYARI: kısa kenar {min(w,h)} px < {a.min_kenar}; Kling içeride büyütür, "
                     f"yumuşak çıkar. Mimari ofisten yüksek çözünürlük iste ya da önce upscale et")
    if not (1/2.5 - 1e-3 <= ratio <= 2.5 + 1e-3):
        notes.append("HATA: oran 1:2,5–2,5:1 dışında")
    if size > 50 * 1024 * 1024:
        notes.append("HATA: dosya 50 MB üstü")
    if size > 10 * 1024 * 1024:
        notes.append("not: 10 MB üstü — O1 uç noktası kabul etmez, v3/o3 eder")
    lost = 100 * (1 - (w * h) / (w0 * h0))
    print(f"{out}  {w0}×{h0} → {w}×{h}  ({a.oran}, odak {a.odak}, kırpma kaybı %{lost:.0f}, {size/1e6:.1f} MB)")
    for n in notes:
        print("  " + n)
    if any(n.startswith("HATA") for n in notes):
        sys.exit(2)

if __name__ == "__main__":
    main()

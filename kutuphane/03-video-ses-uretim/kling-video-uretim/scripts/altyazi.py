#!/usr/bin/env python3
"""
altyazi.py — seslendirme zamanlamasından altyazı PNG dizisi + ffmpeg concat listesi.

reelsindustry motor/ses/altyazi.py + goruntu/kart.py kalıbı: öbek ≤ 4 kelime,
≤ 2,2 sn; noktalama ve > 0,45 sn sessizlik öbeği böler. Her öbek bir alfa PNG;
concat demuxer'a `duration` satırlarıyla verilir, ara kodlama yok.
Moonstone stili (post-uretimi.md §8): beyaz Lora metin, yarı saydam lacivert
kutu, güvenli alan içinde, en fazla iki satır. Karaoke vurgusu yok — marka sakin.
Kutu mürekkep kutusundan (alfa bbox) çizilir, font metriğinden değil.

Bilinen tuzak: concat demuxer son girdinin duration'ını yok sayar → son dosya
boş kareyle tekrarlanır; aksi hâlde son öbek tek kare görünür ya da kapanış
kartının üstünde kalır.

  python3 altyazi.py vo.zamanlama.json --out-dir alt/ --preset cross-9x16
  → alt/altyazi.txt  (bitir.py --altyazi alt/altyazi.txt)
"""
import argparse, json, os, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "gorsel-uretim", "scripts"))
import frame as F  # noqa: E402

NAVY = (4, 12, 29)

def obekle(zam, maks_kelime=4, maks_sure=2.2, bosluk=0.45):
    obek, cur = [], []
    for w in zam:
        if cur:
            son = cur[-1]
            # tek kelimelik öbek bırakma: süre kuralı ancak öbekte ≥ 2 kelime varsa keser
            kes = (len(cur) >= maks_kelime or (len(cur) >= 2 and w["bit"] - cur[0]["bas"] > maks_sure)
                   or w["bas"] - son["bit"] > bosluk or son["kelime"][-1:] in ".!?:;")
            if kes:
                obek.append(cur); cur = []
        cur.append(w)
    if cur: obek.append(cur)
    return obek

def kare(W, H, safe, metin, font, kutu_op, taban, maks_w, pad=(26, 16), radius=18):
    st, sb, sl, sr = safe
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lines = F.wrap(metin, font, maks_w)
    if len(lines) > 2:
        sys.stderr.write(f"[UYARI] öbek 2 satırı aşıyor: {metin!r}\n")
    lh = int(font.size * 1.3)
    # metin katmanı
    tl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(tl)
    y = taban - lh * len(lines)
    for ln in lines:
        tw = font.getlength(ln); d.text(((W - tw) // 2, y), ln, font=font, fill=(255, 255, 255, 255)); y += lh
    ink = tl.split()[-1].getbbox()
    if ink:
        x0, y0, x1, y1 = ink
        k = ImageDraw.Draw(img)
        k.rounded_rectangle([x0 - pad[0], y0 - pad[1], x1 + pad[0], y1 + pad[1]], radius=radius, fill=NAVY + (kutu_op,))
        if y1 + pad[1] > H - sb or y0 - pad[1] < st or x0 - pad[0] < sl or x1 + pad[0] > W - sr:
            sys.stderr.write(f"[UYARI] altyazı güvenli alan dışına taşıyor: {metin!r}\n")
    return Image.alpha_composite(img, tl)

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("zamanlama"); p.add_argument("--out-dir", required=True)
    p.add_argument("--preset", default="cross-9x16"); p.add_argument("--boyut", type=int, default=44)
    p.add_argument("--taban", type=int, default=0, help="metin alt çizgisi y; 0 = alt güvenli sınırın 120 px üstü")
    p.add_argument("--kutu-opaklik", type=int, default=150); p.add_argument("--baslangic", type=float, default=0.0,
                                                                            help="seslendirmenin videodaki başlangıcı (sn)")
    p.add_argument("--toplam", type=float, help="video toplam süresi; boş kare sonuna kadar")
    a = p.parse_args()

    P = F.PRESETS[a.preset]; W, H = P["w"], P["h"]; safe = P["safe"]
    k = W / 1080.0; px = lambda v: max(1, int(round(v * k)))
    j = json.load(open(a.zamanlama, encoding="utf-8"))
    zam = j["zamanlama"]
    if not zam:
        sys.exit("zamanlama boş")
    font = F.load(F.BODY_CHAIN, px(a.boyut), "body")
    taban = a.taban or (H - safe[1] - px(120))
    maks_w = W - safe[2] - safe[3] - px(80)
    os.makedirs(a.out_dir, exist_ok=True)
    bos = os.path.join(a.out_dir, "bos.png"); Image.new("RGBA", (W, H), (0, 0, 0, 0)).save(bos)
    satir, t = [], 0.0
    for i, ob in enumerate(obekle(zam)):
        bas, bit = ob[0]["bas"] + a.baslangic, ob[-1]["bit"] + a.baslangic
        if bas > t + 0.01:
            satir.append(f"file 'bos.png'\nduration {bas - t:.3f}")
        metin = " ".join(w["kelime"] for w in ob)
        f = os.path.join(a.out_dir, f"a{i:04d}.png")
        kare(W, H, safe, metin, font, a.kutu_opaklik, taban, maks_w).save(f)
        satir.append(f"file '{os.path.basename(f)}'\nduration {bit - bas:.3f}")
        t = bit
    kuyruk = (a.toplam - t) if a.toplam and a.toplam > t else 1.0
    satir.append(f"file 'bos.png'\nduration {kuyruk:.3f}")
    satir.append("file 'bos.png'")          # son girdinin duration'ı yok sayılır → tekrar, ve boş olmalı
    lst = os.path.join(a.out_dir, "altyazi.txt")
    open(lst, "w", encoding="utf-8").write("\n".join(satir) + "\n")
    print(f"{lst}  {len(obekle(zam))} öbek  son {t:.2f} sn")

if __name__ == "__main__":
    main()

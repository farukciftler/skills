#!/usr/bin/env python3
"""
altyazi.py — Kelime kelime yanan (karaoke) altyazi katmani uretir.

  python3 altyazi.py --ses vo.mp3 --metin "…" --out-dir alt/ --gecikme 0.85

NEDEN BU YOL: bu makinedeki ffmpeg'de `subtitles` ve `drawtext` YOK, yani ASS
yakilamiyor. Her kelime durumu icin bir alfa PNG rasterlenir ve `concat`
demuxer'iyla **sureli bir goruntu dizisi** olarak ana filtre grafigine girer.
Ara dosya encode'u yoktur; PNG'ler dogrudan girdidir.

NEDEN ALTYAZI: sosyal videolarin buyuk cogunlugu sessiz izleniyor; altyazili
video belirgin bicimde daha uzun tutuyor. Bu hatta altyaziyi eklemek tek
basina en buyuk kazanc.

Kelime zamanlamasi ElevenLabs Scribe'dan gelir (soz_olcum.asr zaten veriyor).
"""
import argparse, json, os, sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import frame as F

W, H = 1080, 1920
NOKTALAMA = ".,!?:;…"

def kelime_zamanlari(ses):
    import soz_olcum as S
    d = S.asr(ses)
    return [dict(kelime=w["text"], bas=w["start"], bit=w["end"])
            for w in d.get("words", []) if w.get("type") == "word"]

def obekle(kelimeler, maks_kelime=4, maks_sure=2.2, sessizlik=0.45):
    """Okunabilir obeklere boler. Kirilma: noktalama, kelime tavani,
    sure tavani, ve kelimeler arasi 0,45 sn'den uzun sessizlik (nefes)."""
    obekler, cur = [], []
    for i, k in enumerate(kelimeler):
        if cur:
            bosluk = k["bas"] - cur[-1]["bit"]
            uzun = (k["bit"] - cur[0]["bas"]) > maks_sure
            if len(cur) >= maks_kelime or uzun or bosluk > sessizlik:
                obekler.append(cur); cur = []
        cur.append(k)
        if k["kelime"][-1:] in NOKTALAMA and len(cur) >= 2:
            obekler.append(cur); cur = []
    if cur: obekler.append(cur)
    return obekler

def kare(obek, aktif, boy, y, fg, vurgu, golge):
    """Bir obegin tek kelime durumunu alfa PNG'ye cizer."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = F.load(F.BODY_BOLD_CHAIN, boy, "body")
    bosluk = int(boy * 0.34)
    genisler = [f.getlength(k["kelime"]) for k in obek]
    toplam = sum(genisler) + bosluk * (len(obek) - 1)
    x = (W - toplam) // 2
    # okunabilirlik icin yumusak koyu tablet
    pad_x, pad_y = int(boy * 0.55), int(boy * 0.34)
    d.rounded_rectangle([x - pad_x, y - pad_y, x + toplam + pad_x, y + boy + pad_y],
                        radius=int(boy * 0.16), fill=golge)
    for i, (k, g) in enumerate(zip(obek, genisler)):
        d.text((x, y), k["kelime"], font=f, fill=(vurgu if i == aktif else fg))
        x += g + bosluk
    return img

def uret(kelimeler, out_dir, *, gecikme=0.0, boy=46, y=1180,
         fg=(238, 238, 242), vurgu=None, golge=(4, 12, 29, 168)):
    """PNG dizisi + concat listesi uretir. Doner: (liste_yolu, toplam_sure)

    TUZAK — SURELERI TOPLAMA, MUTLAK ZAMANA BAGLA. Ilk surumde her karenin
    suresi (bit - bas) olarak yazilip arka arkaya ekleniyordu; kelimeler
    ARASINDAKI bosluklar sayilmadigi icin altyazi giderek sesin onune gecti ve
    8. saniyede bitmis oldu. Dogrusu: her olay kendi MUTLAK baslangicina
    yerlestirilir, sure bir sonraki olayin baslangicindan cikarilir.
    """
    vurgu = vurgu or F.GOLD
    os.makedirs(out_dir, exist_ok=True)
    obekler = obekle(kelimeler)
    bos_p = os.path.join(out_dir, "bos.png")
    Image.new("RGBA", (W, H), (0, 0, 0, 0)).save(bos_p)

    olaylar = [(0.0, bos_p)]                      # (mutlak_zaman, png)
    for oi, obek in enumerate(obekler):
        for wi, k in enumerate(obek):
            p = os.path.join(out_dir, f"o{oi:03d}_w{wi}.png")
            kare(obek, wi, boy, y, fg, vurgu, golge).save(p)
            olaylar.append((gecikme + k["bas"], p))
        olaylar.append((gecikme + obek[-1]["bit"], bos_p))   # obek sonrasi bos

    olaylar.sort(key=lambda e: e[0])
    # ayni ana dusen olaylarda sonuncusu kalsin
    temiz = []
    for zt, p in olaylar:
        if temiz and abs(zt - temiz[-1][0]) < 0.02: temiz[-1] = (zt, p)
        else: temiz.append((zt, p))

    satirlar = []
    for idx, (zt, p) in enumerate(temiz):
        bitis = temiz[idx + 1][0] if idx + 1 < len(temiz) else zt + 0.5
        sure = max(0.033, bitis - zt)
        satirlar.append(f"file '{os.path.abspath(p)}'")
        satirlar.append(f"duration {sure:.3f}")
    # TUZAK: concat demuxer son girdinin duration satirini yok sayar; son dosya
    # tekrarlanmazsa son kare bir frame gorunup kayboluyor.
    satirlar.append(f"file '{os.path.abspath(bos_p)}'")
    liste = os.path.join(out_dir, "liste.txt")
    open(liste, "w").write("\n".join(satirlar) + "\n")
    toplam = temiz[-1][0] + 0.5
    return liste, toplam


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ses", required=True)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--gecikme", type=float, default=0.0)
    p.add_argument("--boy", type=int, default=46)
    p.add_argument("--y", type=int, default=1180)
    a = p.parse_args()
    kl = kelime_zamanlari(a.ses)
    liste, sure = uret(kl, a.out_dir, gecikme=a.gecikme, boy=a.boy, y=a.y)
    print(f"{liste}  {len(kl)} kelime  {sure:.1f}s")

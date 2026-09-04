#!/usr/bin/env python3
"""Gündüz mimari render'ını mavi saat / gün batımı görünümüne çevirir.

Referans hesapların tamamı akşam ışığında çekilmiş; elimizdeki katalog
render'ları öğle vakti. Gerçek çözüm mimari ekipten akşam render pass'i
istemektir (bkz. gorsel-yon-referans.md §6). Bu betik o gelene kadarki
ara çözümdür: gökyüzünü değiştirir, cepheyi karartır, pencereleri yakar.

    python3 aksam.py girdi.jpg cikti.jpg [--yogunluk 0.94] [--gokyuzu mavi-saat|gun-batimi]

Sınır: gökyüzü örtülü ya da ufuk çizgisi binayla kapalıysa sıcak turuncu
görünmez, sonuç mavi saatte kalır. Bu bir kusur değil, girdinin sınırı.
"""
import argparse
import numpy as np
from PIL import Image, ImageFilter

GOKYUZU = {
    "mavi-saat": [(0.00, (0x0C, 0x18, 0x33)), (0.35, (0x2B, 0x2B, 0x5A)),
                  (0.62, (0x8E, 0x4E, 0x4A)), (0.82, (0xD6, 0x8A, 0x4E)),
                  (1.00, (0xF0, 0xBE, 0x7E))],
    "gun-batimi": [(0.00, (0x1E, 0x2A, 0x55)), (0.30, (0x6B, 0x3F, 0x63)),
                   (0.55, (0xC2, 0x62, 0x45)), (0.78, (0xEE, 0x9E, 0x50)),
                   (1.00, (0xFB, 0xD2, 0x93))],
}


def dikey_degrade(stops, h):
    g = np.zeros((h, 3), np.float32)
    son = 0
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        i0, i1 = int(p0 * (h - 1)), int(p1 * (h - 1))
        t = np.linspace(0, 1, max(i1 - i0, 1))[:, None]
        g[i0:i1] = np.array(c0) / 255 * (1 - t) + np.array(c1) / 255 * t
        son = i1
    g[son:] = np.array(stops[-1][1]) / 255
    return g[:, None, :]


def bulanik(mask, yaricap):
    return np.asarray(
        Image.fromarray((mask * 255).astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(yaricap))).astype(np.float32) / 255.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("girdi")
    ap.add_argument("cikti")
    ap.add_argument("--yogunluk", type=float, default=0.94, help="gökyüzü değişim gücü 0–1")
    ap.add_argument("--gokyuzu", choices=sorted(GOKYUZU), default="mavi-saat")
    ap.add_argument("--karartma", type=float, default=0.46, help="cephe karartma çarpanı")
    a = ap.parse_args()

    im = Image.open(a.girdi).convert("RGB")
    W, H = im.size
    px = np.asarray(im).astype(np.float32) / 255.0
    R, G, B = px[..., 0], px[..., 1], px[..., 2]

    # gökyüzü maskesi: mavi baskın veya parlak bulut, üste doğru güçlenir
    mavimsi = np.clip((B - R) * 4.0, 0, 1)
    parlak = np.clip((R + G + B) / 3.0 * 1.4 - 0.75, 0, 1)
    sky = np.clip(mavimsi * 0.85 + parlak * mavimsi * 1.2 + parlak * 0.35, 0, 1)
    sky *= np.clip(1.45 - 1.6 * np.linspace(0, 1, H)[:, None], 0, 1)
    m = bulanik(sky, 3)[..., None]

    out = px * (1 - m * a.yogunluk) + dikey_degrade(GOKYUZU[a.gokyuzu], H) * (m * a.yogunluk)

    # gökyüzü dışı: akşam karartması, gölgeler markanın laciverti (#040C1D) yönüne
    nonsky = 1 - m
    lum = out.mean(axis=2, keepdims=True)
    out = out * m + (out * a.karartma + np.array([0.016, 0.047, 0.113]) * (1 - lum) * 0.9) * nonsky

    # yanan pencereler geri gelsin
    sicak = np.clip((R - B) * 3.0, 0, 1) * np.clip(px.mean(axis=2) * 1.6 - 0.45, 0, 1)
    sicak = bulanik(sicak, 1)
    hale = bulanik(sicak, 14)
    out += sicak[..., None] * np.array([0.62, 0.44, 0.20]) + hale[..., None] * np.array([0.30, 0.19, 0.07])

    out = np.clip((np.clip(out, 0, 1) - 0.5) * 1.08 + 0.5, 0, 1)
    Image.fromarray((out * 255).astype(np.uint8)).save(a.cikti, quality=95)
    print(f"{a.cikti}  {W}x{H}  [{a.gokyuzu} x{a.yogunluk}]")


if __name__ == "__main__":
    main()

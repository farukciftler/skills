#!/usr/bin/env python3
"""
doku_indir.py — CC0 PBR doku indirici (ambientCG + Poly Haven).

Prosedürel ahşap bir YEDEKTİR. Müşteriye gidecek render'da gerçek taranmış
kaplama dokusu kullan — fark büyüktür.

Kullanım:
    python3 doku_indir.py --liste ahsap
    python3 doku_indir.py --acg Wood051 --cozunurluk 2K
    python3 doku_indir.py --ph oak_veneer_02 --cozunurluk 2k
    python3 doku_indir.py --hdri white_studio_04 --cozunurluk 4k

Lisans (2026-08 doğrulandı):
  • ambientCG  — CC0 1.0, atıf gerekmez, yeniden dağıtım serbest.
  • Poly Haven — varlıklar CC0. API ToS'u ayrı: canlı API kullanırken
    kendi adını taşıyan bir User-Agent göndermek ZORUNLU (§2.4) — aşağıda
    gönderiliyor.
Kullanmayın: sharetextures (ToS botla indirmeyi yasaklıyor), freepbr
(ücretsiz katman ticari değil), Poliigon (üyelik + kısıtlı EULA).
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
import urllib.request
import zipfile

UA = {"User-Agent": "mobilya-cad/1.0 (furniture CAD skill)"}

ACG_LISTE = "https://ambientcg.com/api/v3/assets?type=material&q={q}&limit={n}"
ACG_INDIR = "https://ambientcg.com/get?file={id}_{res}-{fmt}.zip"
PH_DOSYA = "https://api.polyhaven.com/files/{slug}"

# Araştırmada doğrulanmış, mobilyaya uygun varlıklar
ONERILEN = {
    "ahsap": {
        "ambientcg": ["Wood049", "Wood092", "Wood094", "Wood051", "Wood067",
                      "Wood090A", "Wood095", "Wood087"],
        "polyhaven": ["oak_veneer_02", "white_oak_veneer", "red_oak_veneer",
                      "black_walnut_veneer_01", "american_walnut_veneer",
                      "white_maple_veneer", "ash_veneer", "plywood"],
        "not": "mese: Wood049/092/094, oak_veneer_02 · ceviz: Wood051, "
               "black_walnut_veneer_01 · kayin YOK — white_maple_veneer kullan",
    },
    "hdri": {
        "polyhaven": ["white_studio_04", "white_studio_05",
                      "monochrome_studio_02", "brown_photostudio_02",
                      "photo_studio_loft_hall"],
        "not": "studio_small_09 KULLANMA — beyaz dengesi 2750 K, ahşabı "
               "turuncuya çeker. Renkli/jelli studio HDRI'lerinden uzak dur.",
    },
    "melamin": {
        "not": "Her iki sitede de DÜZ BEYAZ MELAMİN YOK. render.py'deki "
               "melamin() fonksiyonu prosedürel üretir — doku indirme.",
    },
}


def _al(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def acg_indir(varlik: str, klasor: str, cozunurluk: str = "2K",
              fmt: str = "JPG") -> str:
    """ambientCG varlığını indirip açar. Örn: Wood051, 2K, JPG."""
    hedef = os.path.join(klasor, varlik)
    os.makedirs(hedef, exist_ok=True)
    url = ACG_INDIR.format(id=varlik, res=cozunurluk, fmt=fmt)
    print(f"[acg] {url}")
    ham = _al(url)
    with zipfile.ZipFile(io.BytesIO(ham)) as z:
        z.extractall(hedef)
    dosyalar = sorted(os.listdir(hedef))
    print(f"[acg] {varlik} -> {hedef}  ({len(dosyalar)} dosya)")
    for d in dosyalar:
        print(f"        {d}")
    return hedef


def ph_indir(slug: str, klasor: str, cozunurluk: str = "2k",
             fmt: str = "jpg") -> str:
    """Poly Haven doku setini indirir (Diffuse/Rough/nor_gl)."""
    hedef = os.path.join(klasor, slug)
    os.makedirs(hedef, exist_ok=True)
    meta = json.loads(_al(PH_DOSYA.format(slug=slug)))
    istenen = {"Diffuse": "_diff_", "Rough": "_rough_", "nor_gl": "_nor_gl_",
               "AO": "_ao_", "Displacement": "_disp_"}
    n = 0
    for anahtar, ek in istenen.items():
        if anahtar not in meta:
            continue
        try:
            url = meta[anahtar][cozunurluk][fmt]["url"]
        except KeyError:
            continue
        ad = f"{slug}{ek}{cozunurluk}.{fmt}"
        with open(os.path.join(hedef, ad), "wb") as f:
            f.write(_al(url))
        print(f"[ph]  {ad}")
        n += 1
    if n == 0:
        raise RuntimeError(f"{slug}: {cozunurluk}/{fmt} bulunamadı")
    print(f"[ph]  {slug} -> {hedef}  ({n} harita)")
    return hedef


def ph_hdri(slug: str, klasor: str, cozunurluk: str = "4k") -> str:
    os.makedirs(klasor, exist_ok=True)
    meta = json.loads(_al(PH_DOSYA.format(slug=slug)))
    url = meta["hdri"][cozunurluk]["exr"]["url"]
    yol = os.path.join(klasor, f"{slug}_{cozunurluk}.exr")
    with open(yol, "wb") as f:
        f.write(_al(url))
    print(f"[hdri] {yol}")
    return yol


def acg_ara(sorgu: str, adet: int = 20):
    veri = json.loads(_al(ACG_LISTE.format(q=sorgu, n=adet)))
    for a in veri.get("foundAssets", []):
        print(f"  {a.get('assetId'):16s} {a.get('displayName','')}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--acg", help="ambientCG varlık kodu, ör. Wood051")
    ap.add_argument("--ph", help="Poly Haven slug, ör. oak_veneer_02")
    ap.add_argument("--hdri", help="Poly Haven HDRI slug")
    ap.add_argument("--ara", help="ambientCG'de ara")
    ap.add_argument("--liste", choices=list(ONERILEN),
                    help="önerilen varlıkları göster")
    ap.add_argument("--cozunurluk", default=None)
    ap.add_argument("--klasor", default="dokular")
    a = ap.parse_args()

    if a.liste:
        d = ONERILEN[a.liste]
        for k, v in d.items():
            if k == "not":
                print(f"\nNOT: {v}")
            else:
                print(f"\n{k}:")
                for s in v:
                    print(f"  {s}")
        return
    if a.ara:
        acg_ara(a.ara)
        return
    if a.acg:
        acg_indir(a.acg, a.klasor, a.cozunurluk or "2K")
    if a.ph:
        ph_indir(a.ph, a.klasor, a.cozunurluk or "2k")
    if a.hdri:
        ph_hdri(a.hdri, a.klasor, a.cozunurluk or "4k")
    if not any([a.acg, a.ph, a.hdri]):
        ap.print_help()


if __name__ == "__main__":
    main()

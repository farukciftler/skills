"""
paket.py — bir mobilyanın TAM üretim + sunum paketini tek çağrıda üretir.

    from dolap import Dolap, Bolge
    from paket import paketle
    paketle(Dolap(...), "cikti")

Klasör standardı (her mobilya KENDİ klasöründe):

    cikti/<KOD>/
      <KOD>-TASARIM-DOSYASI.pdf     ← sunulacak tek dosya (7 sayfa)
      <KOD>-RAPOR.txt               ← mühendislik raporu + uyarılar
      <KOD>-BOM.csv                 ← kesim listesi (net + kesim ölçüsü)
      <KOD>-CIZIM.pdf / .dxf / .png ← ölçülü A3 teknik çizim
      <KOD>-<malzeme>-kesim-plani.* ← levha yerleşimi + verim
      <KOD>.step / .glb / .stl      ← 3B model
      cnc/<parça>.dxf               ← parça başına CNC dosyası (R12)
      render/
        uc_ceyrek · on · sag · sol · arka · ust        (kapalı)
        acik · acik_ceyrek · ic_detay                  (kapaklar açık)
        goruntuler.json             ← görünüş listesi + açıklama pikselleri
      render_notlari.json           ← açıklamaların 3B konumları
      render_olculeri.json          ← render üzerine çizilen ölçülerin 3B uçları

Render üzerindeki açıklamalar 3B noktalara BAĞLIDIR: ölçü değişince
etiketler kendiliğinden doğru yere düşer, elle taşımak gerekmez.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys

BURASI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BURASI)

BLENDER = "/Applications/Blender.app/Contents/MacOS/Blender"
VENV_PY = os.path.expanduser("~/mobilya-venv/bin/python")


def paketle(d, kok: str = "cikti", *, doku: str = None, marka: str = "",
            olcek: float = 15.0, ornek: int = 260,
            gen: int = 1300, yuk: int = 1450,
            render: bool = True, pdf: bool = True, cnc: bool = True) -> dict:
    """CAD → render seti → tasarım dosyası. Üretilen yolları döndürür."""
    from dolap import uret as cad_uret

    klasor = os.path.join(kok, d.kod)
    os.makedirs(klasor, exist_ok=True)
    cikti = {"klasor": klasor}

    # 1) Geometri, çizim, BOM, kesim planı, CNC
    cikti.update(cad_uret(d, klasor, olcek=olcek, cnc=cnc))

    # 2) Açıklama noktaları ve ÖLÇÜLER (3B) — render tarafına devredilir
    notlar = d.render_notlari() if hasattr(d, "render_notlari") else []
    not_yolu = os.path.join(klasor, "render_notlari.json")
    with open(not_yolu, "w", encoding="utf-8") as f:
        json.dump(notlar, f, ensure_ascii=False, indent=1)
    cikti["notlar"] = not_yolu

    olculer = d.render_olculeri() if hasattr(d, "render_olculeri") else []
    olcu_yolu = os.path.join(klasor, "render_olculeri.json")
    with open(olcu_yolu, "w", encoding="utf-8") as f:
        json.dump(olculer, f, ensure_ascii=False, indent=1)
    cikti["olculer"] = olcu_yolu

    # 3) Render seti (Blender'ın kendi python'unda, ayrı süreç)
    if render:
        if not os.path.exists(BLENDER):
            print(f"[paket] Blender yok ({BLENDER}) — render atlandı")
        else:
            komut = [BLENDER, "-b", "--python",
                     os.path.join(BURASI, "render.py"), "--",
                     "--glb", cikti["glb"],
                     "--out", os.path.join(klasor, "render"),
                     "--set", "--notlar", not_yolu,
                     "--olculer", olcu_yolu,
                     "--mod", "vitrin", "--ornek", str(ornek),
                     "--gen", str(gen), "--yuk", str(yuk),
                     "--kapak-ac", "105"]
            if doku:
                komut += ["--doku", doku]
            r = subprocess.run(komut, capture_output=True, text=True)
            for satir in r.stdout.splitlines():
                if satir.startswith(("[model", "[set", "[kapak]")):
                    print(satir)
            if r.returncode != 0:
                print("[paket] RENDER HATASI:")
                print(r.stdout[-1500:])
                print(r.stderr[-1500:])
            cikti["render"] = os.path.join(klasor, "render")

    # 4) Tasarım dosyası PDF
    if pdf:
        from belge import TasarimBelgesi
        cikti["tasarim_pdf"] = TasarimBelgesi(d, klasor, marka=marka).uret()

    return cikti


def ozet(ciktilar: list[dict]):
    print("\n" + "=" * 74)
    print("PAKET ÖZETİ")
    print("=" * 74)
    for c in ciktilar:
        print(f"  {c['klasor']}")
        if "tasarim_pdf" in c:
            print(f"      → {os.path.basename(c['tasarim_pdf'])}")

"""
paket.py — bir mobilyanın TAM üretim + sunum paketini tek çağrıda üretir.

    from dolap import Dolap, Bolge
    from paket import paketle
    paketle(Dolap(...), "cikti")

Klasör standardı (her mobilya KENDİ klasöründe):

    cikti/<KOD>/
      <KOD>-TASARIM-DOSYASI.pdf     ← sunulacak tek dosya (8 sayfa)
      <KOD>-RAPOR.txt               ← mühendislik raporu + uyarılar
      <KOD>-BOM.csv                 ← kesim listesi (net + kesim ölçüsü)
      <KOD>-DONANIM.csv             ← menteşe, boru, ray, braket (varsa)
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

Dönen sözlük DÜRÜSTTÜR: `uyarilar` (tasarım kontrolleri), `hatalar`
(render/nesting/PDF adımında olanlar) ve `render_ok` alanları vardır.
Render düşerse PDF yine üretilir ama `hatalar` boş değildir; `siki=True`
ile bu durum RuntimeError'a çevrilir (CI / toplu üretim için).

Blender yolu: MOBILYA_BLENDER ortam değişkeni, yoksa /Applications altı.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

BURASI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BURASI)

BLENDER = os.environ.get(
    "MOBILYA_BLENDER", "/Applications/Blender.app/Contents/MacOS/Blender")


def paketle(d, kok: str = "cikti", *, doku: str = None, marka: str = "",
            olcek: float = 15.0, ornek: int = 260,
            gen: int = 1300, yuk: int = 1450,
            render: bool = True, pdf: bool = True, cnc: bool = True,
            siki: bool = False, bant: str = "antrasit") -> dict:
    """CAD → render seti → tasarım dosyası. Üretilen yolları döndürür.

    render=False: mevcut render/ klasörü varsa PDF onu kullanır — geometri
    veya BOM değişikliğinde Blender'ı yeniden koşturmadan paketi tazelemek
    için. siki=True: herhangi bir hata RuntimeError olur.
    """
    from dolap import uret as cad_uret

    klasor = os.path.join(kok, d.kod)
    os.makedirs(klasor, exist_ok=True)
    cikti = {"klasor": klasor, "hatalar": [], "render_ok": None}

    # 1) Geometri, çizim, BOM, donanım, kesim planı, CNC
    cikti.update(cad_uret(d, klasor, olcek=olcek, cnc=cnc))
    cikti["hatalar"] += [f"nesting: {h}"
                         for h in cikti.get("yerlesim_hatalari", [])]

    # 2) Açıklama noktaları ve ÖLÇÜLER (3B) — render tarafına devredilir
    not_yolu = os.path.join(klasor, "render_notlari.json")
    with open(not_yolu, "w", encoding="utf-8") as f:
        json.dump(d.render_notlari(), f, ensure_ascii=False, indent=1)
    cikti["notlar"] = not_yolu

    olcu_yolu = os.path.join(klasor, "render_olculeri.json")
    with open(olcu_yolu, "w", encoding="utf-8") as f:
        json.dump(d.render_olculeri(), f, ensure_ascii=False, indent=1)
    cikti["olculer"] = olcu_yolu

    # 3) Render seti (Blender'ın kendi python'unda, ayrı süreç)
    render_kl = os.path.join(klasor, "render")
    if render:
        if not os.path.exists(BLENDER):
            cikti["render_ok"] = False
            cikti["hatalar"].append(
                f"Blender yok ({BLENDER}) — render atlandı. "
                f"MOBILYA_BLENDER ile yol verin.")
            print("[paket]", cikti["hatalar"][-1])
        else:
            komut = [BLENDER, "-b", "--python",
                     os.path.join(BURASI, "render.py"), "--",
                     "--glb", cikti["glb"],
                     "--out", render_kl,
                     "--set", "--notlar", not_yolu,
                     "--olculer", olcu_yolu,
                     "--mod", "vitrin", "--ornek", str(ornek),
                     "--gen", str(gen), "--yuk", str(yuk),
                     "--kapak-ac", "105"]
            if doku:
                komut += ["--doku", doku]
            komut += ["--bant", bant]
            r = subprocess.run(komut, capture_output=True, text=True)
            for satir in r.stdout.splitlines():
                if satir.startswith(("[model", "[set", "[kapak]")):
                    print(satir)
            if r.returncode != 0:
                cikti["render_ok"] = False
                cikti["hatalar"].append(
                    "render başarısız (kod %d): %s" % (
                        r.returncode,
                        (r.stderr.strip().splitlines() or ["?"])[-1][:300]))
                print("[paket] RENDER HATASI:")
                print(r.stdout[-1500:])
                print(r.stderr[-1500:])
            else:
                cikti["render_ok"] = True
    if os.path.isdir(render_kl):
        cikti["render"] = render_kl

    # 4) Tasarım dosyası PDF — render düşmüş olsa da üretilir, hata kayda geçer
    if pdf:
        try:
            from belge import TasarimBelgesi
            cikti["tasarim_pdf"] = TasarimBelgesi(d, klasor, marka=marka).uret()
        except Exception as e:      # font yok, reportlab yok, bozuk render
            cikti["hatalar"].append(f"PDF üretilemedi: {e}")
            print("[paket] PDF HATASI:", e)

    if cikti["hatalar"]:
        print(f"[paket] {d.kod}: {len(cikti['hatalar'])} HATA")
        for h in cikti["hatalar"]:
            print("   !!", h)
        if siki:
            raise RuntimeError(f"{d.kod}: " + " | ".join(cikti["hatalar"]))
    if cikti.get("uyarilar"):
        print(f"[paket] {d.kod}: {len(cikti['uyarilar'])} tasarım uyarısı "
              f"(RAPOR.txt ve PDF son sayfada)")
    return cikti


def ozet(ciktilar: list[dict]):
    print("\n" + "=" * 74)
    print("PAKET ÖZETİ")
    print("=" * 74)
    for c in ciktilar:
        durum = ("HATA" if c.get("hatalar") else
                 f"{len(c.get('uyarilar', []))} uyarı")
        print(f"  {c['klasor']:40s} {durum}")
        if "tasarim_pdf" in c:
            print(f"      → {os.path.basename(c['tasarim_pdf'])}")
        for h in c.get("hatalar", []):
            print(f"      !! {h}")

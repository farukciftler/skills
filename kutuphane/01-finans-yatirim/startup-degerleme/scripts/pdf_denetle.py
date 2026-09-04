#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pdf_denetle.py — Uretilen PDF'in her sayfasini olcup dizgi hatalarini bulur.

Neden gerekli: Chrome'un sayfalama davranisi HTML'e bakarak tahmin edilemez.
Zorunlu sayfa sonlari ve "tabloyu bolme" kurallari sayfalarin yarisini bos
birakabiliyor, sifir kenar boslugu icerigin kesildigi hissini veriyor. Ikisi de
ancak uretilmis PDF olculerek gorulur, bu yuzden her uretimden sonra bu calisir.

Gerekli: pdftoppm (poppler) ve Pillow.
    brew install poppler

Kullanim:
    python3 pdf_denetle.py rapor.pdf
    python3 pdf_denetle.py rapor.pdf --kaydet /tmp/sayfalar   # PNG'leri sakla
"""

import argparse, glob, os, shutil, subprocess, sys, tempfile

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow gerekli: pip3 install pillow")

DPI = 100
A4_GEN, A4_YUK = 827, 1170          # A4 @100dpi
MIN_KENAR_PX = 55                   # ~14mm. Altinda icerik kesilmis gibi gorunuyor.
MIN_DOLU = 78                       # Son sayfa disinda bir sayfa bundan bosca olmamali.
SON_SAYFA_MIN = 30                  # Son sayfa bundan bosca ise sarkma var.


def sayfa_olc(yol):
    im = Image.open(yol).convert("L")
    w, h = im.size
    px = im.load()
    sol, sag, alt, ust = w, 0, 0, h
    for y in range(0, h, 2):
        satir_var = False
        for x in range(w):
            if px[x, y] < 190:
                sol = min(sol, x); satir_var = True; break
        for x in range(w - 1, -1, -1):
            if px[x, y] < 190:
                sag = max(sag, x); break
        if satir_var:
            alt = max(alt, y); ust = min(ust, y)
    return {"w": w, "h": h, "sol": sol, "sag_bosluk": w - sag,
            "ust": ust, "dolu": alt / h * 100 if h else 0}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("pdf")
    p.add_argument("--kaydet", help="PNG'lerin yazilacagi dizin")
    p.add_argument("--dpi", type=int, default=DPI)
    a = p.parse_args()

    if not shutil.which("pdftoppm"):
        sys.exit("pdftoppm bulunamadi. Kur: brew install poppler")

    dizin = a.kaydet or tempfile.mkdtemp(prefix="pdfqa-")
    os.makedirs(dizin, exist_ok=True)
    subprocess.run(["pdftoppm", "-r", str(a.dpi), "-png", a.pdf, os.path.join(dizin, "s")],
                   check=True)
    sayfalar = sorted(glob.glob(os.path.join(dizin, "s-*.png")))
    if not sayfalar:
        sys.exit("Sayfa uretilemedi.")

    print(f"{os.path.basename(a.pdf)} — {len(sayfalar)} sayfa\n")
    print(f"{'sayfa':>5} {'sol':>5} {'sag':>5} {'ust':>5} {'dolu':>7}  durum")
    uyarilar = []
    for i, f in enumerate(sayfalar, 1):
        m = sayfa_olc(f)
        son = (i == len(sayfalar))
        sorunlar = []
        if m["sol"] < MIN_KENAR_PX:
            sorunlar.append("sol kenar dar")
        if m["sag_bosluk"] < MIN_KENAR_PX:
            sorunlar.append("sag kenar dar, icerik kesilmis gorunur")
        if not son and m["dolu"] < MIN_DOLU:
            sorunlar.append(f"sayfanin %{100-m['dolu']:.0f}'i bos")
        if son and m["dolu"] < SON_SAYFA_MIN:
            sorunlar.append("son sayfada yalnizca birkac satir var")
        if m["dolu"] < 3:
            sorunlar = ["sayfa tamamen bos"]
        durum = "OK" if not sorunlar else ">>> " + "; ".join(sorunlar)
        if sorunlar:
            uyarilar.append((i, sorunlar, f))
        print(f"{i:>5} {m['sol']:>5} {m['sag_bosluk']:>5} {m['ust']:>5} {m['dolu']:>6.1f}%  {durum}")

    print()
    if not uyarilar:
        print("Sorun yok.")
    else:
        print(f"{len(uyarilar)} sayfada sorun var:\n")
        for i, s, f in uyarilar:
            print(f"  Sayfa {i}: {', '.join(s)}\n    {f}")
        print("""
Sik gorulen sebepler ve cozumleri:

  Sayfanin yarisi bos
    Bolumlere verilen zorunlu sayfa sonu (class="pagebreak"). Kaldir, icerik aksin.
    Zorunlu sayfa sonunu yalnizca gercekten gerektiginde kullan.

  Sayfanin cogu bos ve ustte tek tablo var
    Tabloya break-inside:avoid uygulanmis ve tablo sigmamis. Uzun tablolarda
    bunu kaldir; thead tekrar edilsin, satir ortadan kesilmesin yeter.
    Kisa tablolarda class="tight" ile butun tut.

  Sag kenar dar
    Son sutunun padding-right degeri sifir. Kucuk bir bosluk ver.
    @page margin degerini de kontrol et; A4'te 20mm rahat okunur.

  Son sayfada birkac satir
    Bir onceki sayfada tutulmaya calisilan bir blok var. O bloktaki
    break-inside:avoid kuralini gevset.""")
    if not a.kaydet:
        shutil.rmtree(dizin, ignore_errors=True)
    sys.exit(1 if uyarilar else 0)


if __name__ == "__main__":
    main()

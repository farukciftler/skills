#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""helal_hesap.py — Helal yatırım deterministik hesap makinesi.

Yalnızca standart kütüphane kullanır ve internete ÇIKMAZ. Veri toplama
(bilanço kalemleri, fiyatlar, oranlar) Claude'un işidir; bu script sadece
aritmetiği tutarlı ve halüsinasyonsuz yapar.

Alt komutlar:
  tarama        Finansal oran taraması (TKBB / AAOIFI / FTSE-MSCI / DJIM-S&P)
  arindirma     Temettü (A) ve kapsamlı/hisse başına (B) arındırma
  hisse-matrah  Zekât için hisse matrahı (niyet/yönteme göre)
  zekat         Matrah toplama + nisap kontrolü + zekât tutarı

Örnekler:
  python helal_hesap.py tarama --toplam-varliklar 900e9 --piyasa-degeri 1.2e12 \
      --faizli-borc 180e9 --faiz-getirili 120e9 --uygunsuz-gelir 3e9 --toplam-gelir 200e9
  python helal_hesap.py arindirma --yontem a --temettu 10000 --uygunsuz-oran 1.8
  python helal_hesap.py arindirma --yontem b --hisse-basina 0.42 --adet 500 --gun 365
  python helal_hesap.py hisse-matrah --deger 500000 --yontem donen --donen-oran 32
  python helal_hesap.py zekat --varlik "katilim_fon:500000" --varlik "altin:96000" \
      --borc 50000 --gram-fiyat 3200
"""
import argparse
import json
import sys

G_NISAP_DIYANET = 80.18
G_NISAP_KLASIK = 85.0


def yuzde(pay, payda):
    if payda in (None, 0):
        return None
    return round(100.0 * pay / payda, 2)


def esik_degerlendir(oran, esik, tolerans_carpani=None):
    """Tek oran için sonuç sözlüğü. tolerans_carpani: TKBB md.3.5 için 1.10."""
    if oran is None:
        return {"oran": None, "esik": esik, "sonuc": "VERI_YOK"}
    d = {"oran": oran, "esik": esik}
    if oran < esik:
        d["sonuc"] = "GECTI"
        if oran >= 0.9 * esik:
            d["uyari"] = "sinira_yakin (esigin >= %90'i)"
    elif tolerans_carpani and oran <= esik * tolerans_carpani:
        d["sonuc"] = "TOLERANS_BANDI"
        d["uyari"] = ("TKBB md.3.5: bir sonraki degerleme donemine kadar beklenir; "
                      "tekrar/ek asimda uygunluk kaybedilir")
    else:
        d["sonuc"] = "KALDI"
    return d


def cmd_tarama(a):
    borc = a.faizli_borc
    fgv = a.faiz_getirili
    sonuc = {"girdi": {
        "toplam_varliklar": a.toplam_varliklar, "piyasa_degeri": a.piyasa_degeri,
        "faizli_borc": borc, "faiz_getirili_varliklar": fgv,
        "uygunsuz_gelir": a.uygunsuz_gelir, "toplam_gelir": a.toplam_gelir,
    }, "standartlar": {}}

    gelir_orani = yuzde(a.uygunsuz_gelir, a.toplam_gelir)

    # TKBB / BIST Katilim — payda: toplam varliklar; %33/%33/%5; %10 tolerans
    sonuc["standartlar"]["tkbb_bist"] = {
        "payda": "toplam_varliklar",
        "faizli_borc": esik_degerlendir(yuzde(borc, a.toplam_varliklar), 33.0, 1.10),
        "faiz_getirili": esik_degerlendir(yuzde(fgv, a.toplam_varliklar), 33.0, 1.10),
        "uygunsuz_gelir": esik_degerlendir(gelir_orani, 5.0, 1.10),
    }
    # AAOIFI Std 21 — payda: piyasa degeri; %30/%30/%5
    sonuc["standartlar"]["aaoifi"] = {
        "payda": "piyasa_degeri",
        "faizli_borc": esik_degerlendir(yuzde(borc, a.piyasa_degeri), 30.0),
        "faiz_getirili": esik_degerlendir(yuzde(fgv, a.piyasa_degeri), 30.0),
        "uygunsuz_gelir": esik_degerlendir(gelir_orani, 5.0),
    }
    # FTSE / MSCI — payda: toplam varliklar; %33.33 (alacak ekrani burada modellemedik)
    sonuc["standartlar"]["ftse_msci"] = {
        "payda": "toplam_varliklar",
        "faizli_borc": esik_degerlendir(yuzde(borc, a.toplam_varliklar), 33.33),
        "faiz_getirili": esik_degerlendir(yuzde(fgv, a.toplam_varliklar), 33.33),
        "uygunsuz_gelir": esik_degerlendir(gelir_orani, 5.0),
    }
    # DJIM / S&P (2023 sonrasi) — tek kaldirac ekrani; payda: ORTALAMA piyasa degeri.
    # Girilen piyasa degeri anlik ise bunu ciktida not ederiz.
    sonuc["standartlar"]["djim_sp"] = {
        "payda": "24-36 ay ortalama piyasa degeri (girilen deger anlik ise yaklasiktir)",
        "faizli_borc": esik_degerlendir(yuzde(borc, a.ort_piyasa_degeri or a.piyasa_degeri), 33.0),
        "uygunsuz_gelir_faiz_dahil": esik_degerlendir(gelir_orani, 5.0),
    }

    def genel(std):
        alanlar = [v for k, v in std.items() if isinstance(v, dict) and "sonuc" in v]
        if any(x["sonuc"] == "KALDI" for x in alanlar):
            return "UYGUN DEGIL"
        if any(x["sonuc"] == "VERI_YOK" for x in alanlar):
            return "EKSIK VERI"
        if any(x["sonuc"] == "TOLERANS_BANDI" for x in alanlar):
            return "TOLERANS BANDINDA"
        return "UYGUN (finansal oranlar)"

    sonuc["ozet"] = {k: genel(v) for k, v in sonuc["standartlar"].items()}
    sonuc["not"] = ("Bu cikti yalnizca FINANSAL oran ekranidir; faaliyet/sektor "
                    "taramasi ve istirak kontrolu ayrica yapilmalidir.")
    print(json.dumps(sonuc, ensure_ascii=False, indent=2))


def cmd_arindirma(a):
    if a.yontem == "a":
        if a.temettu is None or a.uygunsuz_oran is None:
            sys.exit("Yontem A icin --temettu ve --uygunsuz-oran gerekli.")
        tutar = a.temettu * a.uygunsuz_oran / 100.0
        out = {"yontem": "A (temettu arindirmasi)",
               "formul": "temettu x (uygunsuz gelir / toplam gelir)",
               "temettu": a.temettu, "uygunsuz_gelir_orani_%": a.uygunsuz_oran,
               "arindirma_tutari": round(tutar, 2)}
    else:
        if a.hisse_basina is None or a.adet is None:
            sys.exit("Yontem B icin --hisse-basina ve --adet gerekli.")
        pay = a.gun / a.donem_gun if a.gun else 1.0
        katsayi = a.enflasyon_ayari if a.enflasyon_ayari is not None else 1.0
        tutar = a.hisse_basina * a.adet * pay * katsayi
        out = {"yontem": "B (kapsamli / hisse basina — AAOIFI & TKBB md.3.6)",
               "formul": "hisse_basina_uygunsuz_gelir x adet x (gun/donem) x katsayi",
               "hisse_basina_uygunsuz_gelir": a.hisse_basina, "adet": a.adet,
               "elde_tutma_orani": round(pay, 4),
               "enflasyon_ayar_katsayisi": katsayi,
               "not": ("TKBB md.3.6.2: faiz gelirinde yalnizca enflasyonu ASAN kisim "
                       "arindirilir; katsayi bu ayari temsil eder (1.0 = ayarsiz)."),
               "arindirma_tutari": round(tutar, 2)}
    out["hatirlatma"] = "Arindirma zekat degildir; sevap beklemeden hayra verilir."
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_hisse_matrah(a):
    if a.yontem in ("ticaret", "ihtiyat"):
        matrah = a.deger
        aciklama = "Piyasa degerinin tamami (ticaret niyeti / ihtiyat)."
    elif a.yontem == "temettu":
        if a.kar_payi is None:
            sys.exit("--yontem temettu icin --kar-payi gerekli.")
        matrah = a.kar_payi
        aciklama = ("Diyanet yontemi: zekat yillik alinan kar payi uzerinden; "
                    "hisse degerine ayrica zekat gerekmez.")
    elif a.yontem == "donen":
        if a.donen_oran is None:
            sys.exit("--yontem donen icin --donen-oran (yuzde) gerekli.")
        matrah = a.deger * a.donen_oran / 100.0
        aciklama = "Hisse degeri x sirketin zekata tabi (donen) varlik orani."
    else:
        sys.exit("yontem: ticaret | temettu | donen | ihtiyat")
    print(json.dumps({"yontem": a.yontem, "matrah": round(matrah, 2),
                      "aciklama": aciklama}, ensure_ascii=False, indent=2))


def cmd_zekat(a):
    kalemler = {}
    for v in a.varlik or []:
        try:
            ad, tutar = v.rsplit(":", 1)
            kalemler[ad] = kalemler.get(ad, 0) + float(tutar)
        except ValueError:
            sys.exit(f"--varlik bicimi 'ad:tutar' olmali: {v!r}")
    toplam_varlik = sum(kalemler.values())
    matrah = toplam_varlik - (a.borc or 0.0)
    nisap_gram = a.nisap_gram
    nisap_tl = nisap_gram * a.gram_fiyat if a.gram_fiyat else None
    oran = 2.577 if a.miladi else a.oran
    out = {"kalemler": kalemler, "toplam_varlik": round(toplam_varlik, 2),
           "dusulen_borc": a.borc or 0.0, "matrah": round(matrah, 2),
           "nisap": {"gram": nisap_gram, "gram_fiyat": a.gram_fiyat,
                     "nisap_tutari": round(nisap_tl, 2) if nisap_tl else None},
           "oran_%": oran}
    if nisap_tl is None:
        out["sonuc"] = "NISAP_KONTROLU_YAPILAMADI (--gram-fiyat verilmedi)"
    elif matrah < nisap_tl:
        out["sonuc"] = "NISAP_ALTINDA — zekat gerekmez"
        out["zekat_tutari"] = 0.0
    else:
        out["sonuc"] = "NISAP_USTUNDE"
        out["zekat_tutari"] = round(matrah * oran / 100.0, 2)
    out["hatirlatma"] = ("Havelan-i havl (kameri yil) sarti kullanicinin kendi zekat "
                         "tarihine goredir; arindirma bu hesaptan ayridir.")
    print(json.dumps(out, ensure_ascii=False, indent=2))


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("tarama", help="Finansal oran taramasi (4 standart)")
    t.add_argument("--toplam-varliklar", type=float, required=True)
    t.add_argument("--piyasa-degeri", type=float, required=True)
    t.add_argument("--ort-piyasa-degeri", type=float,
                   help="DJIM/S&P icin 24-36 ay ortalama (varsa)")
    t.add_argument("--faizli-borc", type=float, required=True)
    t.add_argument("--faiz-getirili", type=float, required=True,
                   help="Faiz getirili nakit + menkul kiymetler")
    t.add_argument("--uygunsuz-gelir", type=float, required=True)
    t.add_argument("--toplam-gelir", type=float, required=True)
    t.set_defaults(func=cmd_tarama)

    r = sub.add_parser("arindirma", help="Arindirma hesabi")
    r.add_argument("--yontem", choices=["a", "b"], required=True)
    r.add_argument("--temettu", type=float, help="Yontem A: brut temettu")
    r.add_argument("--uygunsuz-oran", type=float, help="Yontem A: uygunsuz gelir %%")
    r.add_argument("--hisse-basina", type=float, help="Yontem B: hisse basina uygunsuz gelir")
    r.add_argument("--adet", type=float, help="Yontem B: hisse adedi")
    r.add_argument("--gun", type=float, help="Yontem B: elde tutulan gun")
    r.add_argument("--donem-gun", type=float, default=365.0)
    r.add_argument("--enflasyon-ayari", type=float,
                   help="TKBB md.3.6.2 katsayisi (0-1): faizin enflasyonu asan payi")
    r.set_defaults(func=cmd_arindirma)

    h = sub.add_parser("hisse-matrah", help="Zekat icin hisse matrahi")
    h.add_argument("--deger", type=float, required=True, help="Guncel piyasa degeri")
    h.add_argument("--yontem", choices=["ticaret", "temettu", "donen", "ihtiyat"],
                   required=True)
    h.add_argument("--kar-payi", type=float, help="temettu yontemi: yillik kar payi")
    h.add_argument("--donen-oran", type=float, help="donen yontemi: zekata tabi varlik %%")
    h.set_defaults(func=cmd_hisse_matrah)

    z = sub.add_parser("zekat", help="Matrah + nisap + zekat")
    z.add_argument("--varlik", action="append", metavar="AD:TUTAR",
                   help="Tekrarlanabilir; hisse icin once hisse-matrah calistir")
    z.add_argument("--borc", type=float, help="1 yil icinde vadesi gelen borclar")
    z.add_argument("--gram-fiyat", type=float, help="Altin gram ALIS fiyati (TL)")
    z.add_argument("--nisap-gram", type=float, default=G_NISAP_DIYANET,
                   help=f"Varsayilan {G_NISAP_DIYANET} (Diyanet); klasik {G_NISAP_KLASIK}")
    z.add_argument("--oran", type=float, default=2.5)
    z.add_argument("--miladi", action="store_true", help="Miladi yil: %%2,577 kullan")
    z.set_defaults(func=cmd_zekat)

    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()

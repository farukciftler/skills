#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
deger_hesapla.py — Coklu yontemle startup deger araligi hesaplar.

Elle carpma yapma; bunu kullan ki hesap izlenebilir olsun ve her rapor ayni
yontemle uretilsin. Yontemlerin gerekcesi: references/degerleme-yontemleri.md

Kullanim:
    python3 deger_hesapla.py girdi.json
    python3 deger_hesapla.py --ornek > girdi.json   # sablonu uret, doldur, calistir

Girdi JSON alanlari (bilinmeyeni null birak; script o yontemi atlar ve neden
atladigini soyler -- uydurma deger uretmez):

{
  "ad": "Ornek",
  "kur_usdtry": 42.5,
  "kur_tarihi": "2026-08-27",
  "aylik_gelir_tl": 0,
  "aylik_gider_tl": {"bulut": 40000, "yazilim": 70000, "personel": 0, "pazarlama": 0},
  "nakit_tl": null,
  "mau": 1500,
  "toplam_indirme": 4000,
  "kullanici_basi_usd": [0.5, 3.0],
  "rebuild": {"gelistirici_ay": 18, "aylik_maliyet_tl": 120000,
              "tasarim_tl": 150000, "devralinabilirlik": 0.6},
  "ekip_kisi": 2, "acquihire_kisi_basi_usd": [30000, 120000],
  "ekip_gecer_mi": false,
  "sde_yillik_tl": null, "sde_carpan": [2.0, 4.0],
  "arr_tl": null, "arr_carpan": [1.5, 4.0],
  "senaryolar": [
    {"ad": "Kotu", "deger_usd": 15000, "olasilik": 0.45, "varsayim": "..."},
    {"ad": "Baz",  "deger_usd": 45000, "olasilik": 0.40, "varsayim": "..."},
    {"ad": "Iyi",  "deger_usd": 150000, "olasilik": 0.15, "varsayim": "..."}
  ]
}
"""

import argparse
import json
import sys

ORNEK = {
    "ad": "Ornek Startup",
    "kur_usdtry": None,
    "kur_tarihi": None,
    "aylik_gelir_tl": 0,
    "aylik_gider_tl": {"bulut": 0, "yazilim": 0, "personel": 0, "pazarlama": 0, "diger": 0},
    "nakit_tl": None,
    "mau": None,
    "toplam_indirme": None,
    "kullanici_basi_usd": [0.5, 3.0],
    "rebuild": {"gelistirici_ay": None, "aylik_maliyet_tl": 120000,
                "tasarim_tl": 0, "devralinabilirlik": 0.6},
    "ekip_kisi": None,
    "acquihire_kisi_basi_usd": [30000, 120000],
    "ekip_gecer_mi": False,
    "sde_yillik_tl": None,
    "sde_carpan": [2.0, 4.0],
    "arr_tl": None,
    "arr_carpan": [1.5, 4.0],
    "senaryolar": [],
}


def usd(tl, kur):
    return None if (tl is None or not kur) else tl / kur


def fmt(v, birim="USD"):
    if v is None:
        return "—"
    return f"{v:,.0f} {birim}".replace(",", ".")


def hesapla(g):
    kur = g.get("kur_usdtry")
    if not kur:
        print("UYARI: kur_usdtry verilmedi. TL sonuclari USD'ye cevrilemeyecek.\n",
              file=sys.stderr)

    yontemler = []   # (ad, alt_usd, ust_usd, not)
    atlanan = []

    gider = g.get("aylik_gider_tl") or {}
    aylik_gider = sum(v for v in gider.values() if isinstance(v, (int, float)))
    aylik_gelir = g.get("aylik_gelir_tl") or 0
    yakim = aylik_gider - aylik_gelir
    nakit = g.get("nakit_tl")
    pist = (nakit / yakim) if (nakit and yakim > 0) else None

    # --- A. Yeniden yapim maliyeti
    rb = g.get("rebuild") or {}
    if rb.get("gelistirici_ay") and rb.get("aylik_maliyet_tl"):
        ham = rb["gelistirici_ay"] * rb["aylik_maliyet_tl"] + (rb.get("tasarim_tl") or 0)
        dev = rb.get("devralinabilirlik", 0.6)
        yontemler.append(("Yeniden Yapim Maliyeti",
                          usd(ham * dev * 0.6, kur), usd(ham * dev, kur),
                          f"Ham {fmt(ham,'TL')}, devralinabilirlik x{dev}"))
    else:
        atlanan.append("Yeniden Yapim Maliyeti — gelistirici_ay veya aylik_maliyet_tl yok")

    # --- B. Acquihire
    if g.get("ekip_gecer_mi") and g.get("ekip_kisi"):
        a, b = g.get("acquihire_kisi_basi_usd", [30000, 120000])
        yontemler.append(("Acquihire (ekip degeri)", g["ekip_kisi"] * a, g["ekip_kisi"] * b,
                          f"{g['ekip_kisi']} kisi"))
    else:
        atlanan.append("Acquihire — ekip devirde gecmiyor veya kisi sayisi yok "
                       "(ekip gecmiyorsa bu yontem gecersizdir)")

    # --- C. Kullanici basi
    if g.get("mau"):
        a, b = g.get("kullanici_basi_usd", [0.5, 3.0])
        yontemler.append(("Kullanici Basi Deger (per-MAU)", g["mau"] * a, g["mau"] * b,
                          f"{g['mau']:,} MAU x {a}-{b} USD".replace(",", ".")))
    else:
        atlanan.append("Kullanici Basi Deger — MAU bilinmiyor (aralik bu yuzden genis kalir)")

    # --- D. Gelir carpani
    if g.get("arr_tl"):
        a, b = g.get("arr_carpan", [1.5, 4.0])
        yontemler.append(("Gelir Carpani (ARR x)", usd(g["arr_tl"] * a, kur),
                          usd(g["arr_tl"] * b, kur), f"ARR {fmt(g['arr_tl'],'TL')} x{a}-{b}"))
    else:
        atlanan.append("Gelir Carpani — ARR yok/sifir")

    # --- E. SDE carpani
    if g.get("sde_yillik_tl") and g["sde_yillik_tl"] > 0:
        a, b = g.get("sde_carpan", [2.0, 4.0])
        yontemler.append(("SDE Carpani", usd(g["sde_yillik_tl"] * a, kur),
                          usd(g["sde_yillik_tl"] * b, kur),
                          f"SDE {fmt(g['sde_yillik_tl'],'TL')} x{a}-{b}"))
    else:
        atlanan.append("SDE Carpani — yillik SDE pozitif degil "
                       "(negatif kar carpanla carpilmaz)")

    gecerli = [y for y in yontemler if y[1] is not None and y[2] is not None]

    # --- Yakim baskisi iskontosu
    if pist is None:
        iskonto, iskonto_not = 0.0, "Pist bilinmiyor (nakit verilmedi) — iskonto uygulanmadi"
    elif pist > 12:
        iskonto, iskonto_not = 0.0, f"Pist {pist:.1f} ay — iskonto yok"
    elif pist > 6:
        iskonto, iskonto_not = 0.15, f"Pist {pist:.1f} ay — %15 yakim baskisi iskontosu"
    elif pist > 3:
        iskonto, iskonto_not = 0.32, f"Pist {pist:.1f} ay — %32 yakim baskisi iskontosu"
    else:
        iskonto, iskonto_not = 0.55, f"Pist {pist:.1f} ay — %55 yakim baskisi iskontosu (zorunlu satis)"

    # --- Senaryolar
    beklenen = None
    toplam_olasilik = None
    sen = g.get("senaryolar") or []
    if sen:
        toplam_olasilik = sum(s.get("olasilik", 0) for s in sen)
        beklenen = sum(s.get("deger_usd", 0) * s.get("olasilik", 0) for s in sen)

    return {
        "aylik_gider_tl": aylik_gider, "aylik_gelir_tl": aylik_gelir,
        "aylik_yakim_tl": yakim, "yillik_yakim_tl": yakim * 12,
        "pist_ay": pist, "iskonto": iskonto, "iskonto_not": iskonto_not,
        "yontemler": gecerli, "atlanan": atlanan,
        "beklenen_usd": beklenen, "toplam_olasilik": toplam_olasilik,
        "kur": kur,
    }


def rapor_bas(g, r):
    kur = r["kur"]
    print("=" * 74)
    print(f"  {g.get('ad','(isimsiz)')} — Deger Hesabi")
    if kur:
        print(f"  Kur: 1 USD = {kur} TL ({g.get('kur_tarihi','tarih yok')})")
    print("=" * 74)

    print("\n[ NAKIT AKISI ]")
    print(f"  Aylik gider   : {fmt(r['aylik_gider_tl'],'TL')}"
          + (f"  ({fmt(usd(r['aylik_gider_tl'],kur))})" if kur else ""))
    print(f"  Aylik gelir   : {fmt(r['aylik_gelir_tl'],'TL')}")
    print(f"  Aylik net yakim: {fmt(r['aylik_yakim_tl'],'TL')}"
          + (f"  ({fmt(usd(r['aylik_yakim_tl'],kur))})" if kur else ""))
    print(f"  Yillik yakim  : {fmt(r['yillik_yakim_tl'],'TL')}"
          + (f"  ({fmt(usd(r['yillik_yakim_tl'],kur))})" if kur else ""))
    print(f"  Pist          : {r['pist_ay']:.1f} ay" if r["pist_ay"] else
          "  Pist          : bilinmiyor (nakit verilmedi)")

    print("\n[ YONTEMLER ]  (iskonto oncesi, USD)")
    if not r["yontemler"]:
        print("  Hicbir yontem uygulanamadi — girdiler yetersiz.")
    for ad, alt, ust, notu in r["yontemler"]:
        print(f"  {ad:<32} {fmt(alt):>14} – {fmt(ust):<14}  {notu}")

    if r["atlanan"]:
        print("\n[ ATLANAN YONTEMLER ]  (bunlar raporda 'veri yok' olarak yazilmali)")
        for a in r["atlanan"]:
            print(f"  - {a}")

    if r["yontemler"]:
        alt = min(y[1] for y in r["yontemler"])
        ust = max(y[2] for y in r["yontemler"])
        ort_alt = sum(y[1] for y in r["yontemler"]) / len(r["yontemler"])
        ort_ust = sum(y[2] for y in r["yontemler"]) / len(r["yontemler"])
        i = r["iskonto"]
        print("\n[ BIRLESIK ARALIK ]")
        print(f"  Yontemlerin uc noktalari : {fmt(alt)} – {fmt(ust)}")
        print(f"  Yontem ortalamasi        : {fmt(ort_alt)} – {fmt(ort_ust)}")
        print(f"  {r['iskonto_not']}")
        print(f"  ISKONTO SONRASI          : {fmt(ort_alt*(1-i))} – {fmt(ort_ust*(1-i))}")
        if kur:
            print(f"                             ({fmt(ort_alt*(1-i)*kur,'TL')} – "
                  f"{fmt(ort_ust*(1-i)*kur,'TL')})")
        yayilma = (ust / alt) if alt else 0
        if yayilma > 6:
            print(f"  ! Yontemler arasi {yayilma:.0f} kat fark var. Bu, degerin hangi "
                  "hikayeye\n    inandigina bagli oldugunu gosterir — raporda acikca yaz.")

    if r["beklenen_usd"] is not None:
        print("\n[ SENARYOLAR ]")
        for s in g.get("senaryolar", []):
            print(f"  {s.get('ad',''):<8} {fmt(s.get('deger_usd')):>14}  "
                  f"%{s.get('olasilik',0)*100:.0f}   {s.get('varsayim','')}")
        print(f"  {'BEKLENEN':<8} {fmt(r['beklenen_usd']):>14}")
        if abs((r["toplam_olasilik"] or 0) - 1.0) > 0.001:
            print(f"  ! Olasiliklar toplami {r['toplam_olasilik']:.2f} — 1.00 olmali.")
        if kur:
            print(f"  Beklenen deger TL: {fmt(r['beklenen_usd']*kur,'TL')}")
    print()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("girdi", nargs="?")
    p.add_argument("--ornek", action="store_true", help="Bos sablon JSON bas")
    p.add_argument("--json", action="store_true", help="Sonucu JSON olarak bas")
    a = p.parse_args()

    if a.ornek:
        print(json.dumps(ORNEK, ensure_ascii=False, indent=2))
        return
    if not a.girdi:
        p.error("girdi JSON dosyasi gerekli (veya --ornek)")

    with open(a.girdi, encoding="utf-8") as f:
        g = json.load(f)
    r = hesapla(g)
    if a.json:
        r["yontemler"] = [{"ad": y[0], "alt_usd": y[1], "ust_usd": y[2], "not": y[3]}
                          for y in r["yontemler"]]
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        rapor_bas(g, r)


if __name__ == "__main__":
    main()

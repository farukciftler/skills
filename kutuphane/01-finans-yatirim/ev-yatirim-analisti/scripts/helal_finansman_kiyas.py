#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
helal_finansman_kiyas.py — Faizsiz konut edinme kanallarını yan yana koyar.

Kullanım:
    python3 helal_finansman_kiyas.py --sablon > fin.json
    python3 helal_finansman_kiyas.py fin.json
    python3 helal_finansman_kiyas.py fin.json --json

Desteklenen kanallar: nakit_bekle, katilim_murabaha, tasarruf_finansman,
toki_kooperatif, karz_hasen. Faizli kredi bilinçli olarak desteklenmez.

Her kanal için üretir: nakit çıkışlarının bugünkü değeri, efektif yıllık maliyet,
teslim tarihi, ve gecikmeli teslimde "satın alma gücü açığı" (sözleşme tutarının
teslim anındaki konut fiyatını karşılayıp karşılamadığı).
"""

import json
import sys

SABLON = {
    "konut_fiyati": 5_000_000,
    "eldeki_nakit": 2_000_000,
    "aylik_birikim_kapasitesi": 60_000,
    "yillik_konut_fiyat_artisi": 0.28,
    "enflasyon": 0.25,
    "alternatif_yillik_getiri": 0.30,   # helal alternatif (katılım fonu, sukuk, altın vb.)
    "ufuk_ay": 240,
    "secenekler": [
        {"tip": "nakit_bekle", "ad": "Biriktir, peşin al"},
        {"tip": "katilim_murabaha", "ad": "Katılım bankası konut finansmanı",
         "finansman_tutari": 3_000_000, "aylik_kar_payi_orani": 0.0287, "vade_ay": 120,
         "tahsis_ucreti": 25_000, "diger_masraf": 20_000},
        {"tip": "tasarruf_finansman", "ad": "Tasarruf finansman (evim sistemi)",
         "sozlesme_tutari": 5_000_000, "pesinat_orani": 0.40,
         "organizasyon_ucreti_orani": 0.10, "teslim_ay": 36, "vade_ay": 120},
        {"tip": "toki_kooperatif", "ad": "TOKİ / kooperatif",
         "konut_bedeli": 2_500_000, "pesinat_orani": 0.10, "vade_ay": 240,
         "yillik_taksit_artisi": 0.25, "teslim_ay": 24},
    ],
}


def aylik(oran_yillik):
    return (1 + oran_yillik) ** (1 / 12) - 1


def taksit(anapara, r, n):
    if anapara <= 0 or n <= 0:
        return 0.0
    if r == 0:
        return anapara / n
    q = (1 + r) ** n
    return anapara * r * q / (q - 1)


def irr_aylik(akis, alt=-0.9, ust=1.0):
    def npv(r):
        return sum(cf / (1 + r) ** i for i, cf in enumerate(akis))
    fa, fu = npv(alt), npv(ust)
    if fa * fu > 0:
        return None
    for _ in range(300):
        o = (alt + ust) / 2
        f = npv(o)
        if abs(f) < 1e-6:
            return o
        if fa * f < 0:
            ust, fu = o, f
        else:
            alt, fa = o, f
    return (alt + ust) / 2


def bd(akis, r_ay):
    """Ödeme akışının bugünkü değeri (alternatif getiri oranıyla iskonto)."""
    return sum(cf / (1 + r_ay) ** i for i, cf in enumerate(akis))


def _ay_serisi(n):
    return [0.0] * (n + 1)


def degerlendir(g, s):
    P = g["konut_fiyati"]
    r_alt = aylik(g["alternatif_yillik_getiri"])
    r_ev = aylik(g["yillik_konut_fiyat_artisi"])
    ufuk = int(g["ufuk_ay"])
    tip = s["tip"]
    odemeler = _ay_serisi(ufuk)     # pozitif = cepten çıkan
    teslim_ay = 0
    notlar = []

    if tip == "nakit_bekle":
        nakit = g["eldeki_nakit"]
        birikim = g.get("aylik_birikim_kapasitesi", 0.0)
        ay = 0
        while ay <= ufuk:
            fiyat = P * (1 + r_ev) ** ay
            if nakit >= fiyat:
                break
            nakit = nakit * (1 + r_alt) + birikim
            if ay <= ufuk:
                odemeler[min(ay, ufuk)] += birikim
            ay += 1
        teslim_ay = ay
        if ay > ufuk:
            notlar.append(f"Ufuk içinde ({ufuk} ay) peşin alıma yetişilemiyor: "
                          f"konut fiyatı birikimden hızlı büyüyor.")
        odemeler[0] += g["eldeki_nakit"]
        satin_alma_gucu_acigi = 0.0

    elif tip == "katilim_murabaha":
        F = s["finansman_tutari"]
        r = s["aylik_kar_payi_orani"]
        n = int(s["vade_ay"])
        t = taksit(F, r, n)
        pesinat = max(0.0, P - F)
        odemeler[0] += pesinat + s.get("tahsis_ucreti", 0) + s.get("diger_masraf", 0)
        for ay in range(1, min(n, ufuk) + 1):
            odemeler[ay] += t
        teslim_ay = 0
        satin_alma_gucu_acigi = 0.0
        fin_akis = [F - s.get("tahsis_ucreti", 0) - s.get("diger_masraf", 0)] + [-t] * n
        fin_r = irr_aylik(fin_akis)
        notlar.append(f"Aylık taksit {t:,.0f}".replace(",", ".") +
                      f" · toplam geri ödeme {t*n:,.0f}".replace(",", ".") +
                      f" · murabaha kâr payı toplamı {t*n-F:,.0f}".replace(",", "."))

    elif tip == "tasarruf_finansman":
        S = s["sozlesme_tutari"]
        pes = S * s["pesinat_orani"]
        org = S * s["organizasyon_ucreti_orani"]
        teslim_ay = int(s["teslim_ay"])
        n_son = int(s["vade_ay"])
        odemeler[0] += org
        if teslim_ay > 0:
            aylik_tasarruf = pes / teslim_ay
            for ay in range(1, min(teslim_ay, ufuk) + 1):
                odemeler[ay] += aylik_tasarruf
        else:
            odemeler[0] += pes
        kalan = S - pes
        t = kalan / n_son if n_son else 0.0
        for ay in range(teslim_ay + 1, min(teslim_ay + n_son, ufuk) + 1):
            odemeler[ay] += t
        fiyat_teslimde = P * (1 + r_ev) ** teslim_ay
        satin_alma_gucu_acigi = max(0.0, fiyat_teslimde - S)
        if satin_alma_gucu_acigi > 0 and teslim_ay <= ufuk:
            odemeler[teslim_ay] += satin_alma_gucu_acigi  # farkı cepten kapatma varsayımı
        notlar.append(f"Organizasyon ücreti {org:,.0f} (iade edilmez)".replace(",", ".") +
                      f" · teslim sonrası aylık taksit {t:,.0f}".replace(",", "."))
        if satin_alma_gucu_acigi > 0:
            notlar.append(f"⚠ Teslim ayında ({teslim_ay}. ay) hedef konut "
                          f"{fiyat_teslimde:,.0f}".replace(",", ".") +
                          f", sözleşme tutarı {S:,.0f}".replace(",", ".") +
                          f" → {satin_alma_gucu_acigi:,.0f} açık.".replace(",", ".") +
                          " Sözleşme tutarı sabitse aradaki farkı cepten kapatman gerekir.")

    elif tip == "toki_kooperatif":
        B = s["konut_bedeli"]
        pes = B * s["pesinat_orani"]
        n = int(s["vade_ay"])
        teslim_ay = int(s.get("teslim_ay", 0))
        odemeler[0] += pes
        taksit0 = (B - pes) / n
        for ay in range(1, min(n, ufuk) + 1):
            yil = (ay - 1) // 12
            odemeler[ay] += taksit0 * (1 + s.get("yillik_taksit_artisi", 0.0)) ** yil
        fiyat_teslimde = s.get("teslimde_piyasa_degeri", B * (1 + r_ev) ** teslim_ay)
        satin_alma_gucu_acigi = 0.0
        edinilen_deger = fiyat_teslimde
        notlar.append("Taksitler endeksli: nominal artar, reel yük teorik olarak sabit kalır.")
        notlar.append(f"Teslim {teslim_ay}. ayda; piyasa muadili o tarihte "
                      f"~{fiyat_teslimde:,.0f}".replace(",", "."))

    elif tip == "karz_hasen":
        F = s["tutar"]
        n = int(s["vade_ay"])
        odemeler[0] += max(0.0, P - F)
        for ay in range(1, min(n, ufuk) + 1):
            odemeler[ay] += F / n
        teslim_ay = 0
        satin_alma_gucu_acigi = 0.0
        notlar.append("Maliyetsiz finansman; tek risk borcun vadesinde kapatılabilmesi.")

    else:
        raise ValueError(f"Bilinmeyen kanal: {tip}. Faizli kredi bu skill'de desteklenmez.")

    edinilen = locals().get("edinilen_deger", P * (1 + r_ev) ** teslim_ay)
    edinilen_bd = edinilen / (1 + r_alt) ** teslim_ay if teslim_ay <= ufuk else 0.0
    odeme_bd = bd(odemeler, r_alt)
    r_ay = locals().get("fin_r") if tip in ("katilim_murabaha",) else (
        0.0 if tip == "karz_hasen" else None)
    return {
        "edinilen_varlik": edinilen,
        "edinilen_varlik_bd": edinilen_bd,
        "net_bugunku_deger": edinilen_bd - odeme_bd,
        "maliyet_carpani": sum(odemeler) / P if P else None,
        "ad": s.get("ad", tip),
        "tip": tip,
        "teslim_ay": teslim_ay,
        "toplam_nominal_odeme": sum(odemeler),
        "odemelerin_bugunku_degeri": odeme_bd,
        "finansman_yillik_maliyeti": ((1 + r_ay) ** 12 - 1) if r_ay is not None else None,
        "satin_alma_gucu_acigi": satin_alma_gucu_acigi,
        "ilk_yil_aylik_ortalama": sum(odemeler[1:13]) / 12,
        "notlar": notlar,
    }


def _t(x):
    return "—" if x is None else f"{x:,.0f}".replace(",", ".")


def _p(x):
    return "—" if x is None else f"%{x*100:,.1f}".replace(",", ".")


def rapor(g, sonuclar):
    L = [f"### Helal konut finansmanı kanal karşılaştırması",
         f"Konut fiyatı {_t(g['konut_fiyati'])} · konut fiyat artışı {_p(g['yillik_konut_fiyat_artisi'])}"
         f" · enflasyon {_p(g['enflasyon'])} · helal alternatif getiri {_p(g['alternatif_yillik_getiri'])}",
         "",
         "| Kanal | Teslim | Toplam nominal ödeme | Ödeme / konut fiyatı | Ödemelerin BD | Edinilen varlığın BD | Net BD | Finansman yıllık maliyeti | 1. yıl aylık ort. |",
         "|---|---|---|---|---|---|---|---|---|"]
    for s in sonuclar:
        L.append(f"| {s['ad']} | {s['teslim_ay']}. ay | {_t(s['toplam_nominal_odeme'])} | "
                 f"{s['maliyet_carpani']:.2f}x | {_t(s['odemelerin_bugunku_degeri'])} | "
                 f"{_t(s['edinilen_varlik_bd'])} | {_t(s['net_bugunku_deger'])} | "
                 f"{_p(s['finansman_yillik_maliyeti'])} | {_t(s['ilk_yil_aylik_ortalama'])} |")
    L.append("")
    L.append("**Nasıl okunur:** *Net BD* = edinilen varlığın bugünkü değeri − ödemelerin bugünkü "
             f"değeri; iskonto oranı helal alternatif getiri ({_p(g['alternatif_yillik_getiri'])}). "
             "Pozitif ve en yüksek olan kanal, aynı parayı alternatifte değerlendirme senaryosuna "
             "göre en avantajlısıdır. *Finansman yıllık maliyeti* yalnızca gerçek bir finansman "
             "akışı olan kanallarda hesaplanır ve konut fiyat artışıyla "
             f"({_p(g['yillik_konut_fiyat_artisi'])}) kıyaslanır: üstündeyse kaldıraç erozyon yaratır.")
    L.append("")
    for s in sonuclar:
        L.append(f"**{s['ad']}**")
        for n in s["notlar"]:
            L.append(f"- {n}")
        if s["satin_alma_gucu_acigi"] > 0:
            L.append(f"- Satın alma gücü açığı: {_t(s['satin_alma_gucu_acigi'])}")
        L.append("")
    L.append("_Bu çıktı maliyet karşılaştırmasıdır; kanalların fıkhî uygunluğu ayrı bir "
             "değerlendirmedir (bkz. references/helal-finansman.md ve `helal-yatirim-uzmani`)._")
    return "\n".join(L)


def main():
    if "--sablon" in sys.argv:
        print(json.dumps(SABLON, ensure_ascii=False, indent=2))
        return
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as fh:
        gelen = json.load(fh)
    g = dict(SABLON)
    g.update(gelen)
    sonuclar = [degerlendir(g, s) for s in g["secenekler"]]
    if "--json" in sys.argv:
        print(json.dumps({"girdi": g, "sonuclar": sonuclar}, ensure_ascii=False, indent=2, default=float))
    else:
        print(rapor(g, sonuclar))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ev_analiz.py — Konut yatırımı nakit akışı ve getiri motoru.

Kullanım:
    python3 ev_analiz.py girdi.json            # metin rapor
    python3 ev_analiz.py girdi.json --json     # makine okunur çıktı
    python3 ev_analiz.py --sablon > girdi.json # boş girdi şablonu

Tüm oranlar ondalık (0.28 = %28). Para birimi girdiyle aynıdır (TL varsayılır).
Motor hiçbir piyasa verisini kendisi bilmez; her sayı girdiden gelir.
"""

import json
import sys
from copy import deepcopy

SABLON = {
    "baslik": "Örnek konut",
    "alim": {
        "ilan_fiyati": 5_000_000,
        "pazarlik_indirimi": 0.05,      # ilan fiyatı üzerinden beklenen indirim
        "tapu_harci_orani": 0.02,       # alıcı payı; tamamını alıcı ödüyorsa 0.04
        "emlakci_komisyon_orani": 0.02,
        "tadilat": 250_000,
        "diger_alim_masrafi": 30_000,   # döner sermaye, ekspertiz, taşınma, mobilya
    },
    "kira": {
        "aylik_kira": 28_000,
        "bos_kalma_orani": 0.04,        # yıllık boşta kalma + tahsil edilemeyen pay
        "yillik_kira_artis": 0.30,
    },
    "giderler": {
        "aylik_aidat_ev_sahibi": 1_500,   # ev sahibine kalan pay (demirbaş/büyük onarım)
        "yillik_emlak_vergisi": 12_000,
        "yillik_sigorta": 6_000,          # DASK + konut poliçesi
        "bakim_rezervi_kira_orani": 0.05, # yıllık kiranın yüzdesi olarak onarım rezervi
        "yonetim_gideri_kira_orani": 0.0, # emlakçı/yönetim; kiracı değişim komisyonu için ~0.04
        "yillik_gider_artis": 0.30,
    },
    "vergi": {
        "gmsi_uygula": True,
        "yontem": "goturu",             # "goturu" | "gercek"
        "istisna": 58_000,              # o yılın mesken istisnası; yoksa 0
        "istisna_artis": 0.25,          # istisnanın yıllık güncellenme varsayımı
        "goturu_gider_orani": 0.15,
        "marjinal_vergi_orani": 0.27,
        "deger_artis_istisna_yili": 5,
        "deger_artis_marjinal_oran": 0.35,
    },
    "finansman": {
        "model": "katilim_murabaha",   # katilim_murabaha | tasarruf_finansman | toki_kooperatif
                                       # | karz_hasen | ozkaynak — faizli kredi desteklenmez
        "kredi_tutari": 0,
        "aylik_oran": 0.0287,          # katılım tarafında aylık kâr payı oranı
        "vade_ay": 120,
        "tahsis_ucreti": 0,
        "diger_finansman_masrafi": 0,   # ipotek harcı, ekspertiz, hayat sigortası peşin kısmı
    },
    "beklenti": {
        "yillik_deger_artisi": 0.28,
        "enflasyon": 0.25,
        "elde_tutma_yili": 10,
        "satis_komisyon_orani": 0.02,
        "satis_tapu_harci_orani": 0.02,
    },
    "alternatif": {
        "yillik_getiri": 0.30,          # aynı parayı koyacağın alternatifin nominal getirisi
        "ad": "katılım fonu / alternatif portföy",
    },
}


# ---------------------------------------------------------------- yardımcılar

def _birlestir(sablon, gelen):
    out = deepcopy(sablon)
    for k, v in (gelen or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _birlestir(out[k], v)
        else:
            out[k] = v
    return out


def taksit(anapara, aylik_oran, vade_ay):
    if anapara <= 0 or vade_ay <= 0:
        return 0.0
    if aylik_oran == 0:
        return anapara / vade_ay
    q = (1 + aylik_oran) ** vade_ay
    return anapara * aylik_oran * q / (q - 1)


def kredi_yil_ozeti(anapara, aylik_oran, vade_ay, yil_sayisi):
    """Her yıl için (ödenen taksit, ödenen kâr payı, yıl sonu kalan borç)."""
    t = taksit(anapara, aylik_oran, vade_ay)
    kalan = float(anapara)
    ay = 0
    yillar = []
    for _ in range(yil_sayisi):
        odenen = kar = 0.0
        for _ in range(12):
            if ay >= vade_ay or kalan <= 1e-9:
                break
            k = kalan * aylik_oran
            anapara_payi = t - k
            if anapara_payi > kalan:
                anapara_payi = kalan
            kalan -= anapara_payi
            odenen += anapara_payi + k
            kar += k
            ay += 1
        yillar.append({"odenen": odenen, "kar_payi": kar, "kalan_borc": max(kalan, 0.0)})
    return t, yillar


def irr(akislar, alt=-0.95, ust=10.0, tol=1e-7):
    """Yıllık nakit akışları için IRR (bisection). akislar[0] = t0."""
    def npv(r):
        return sum(cf / (1 + r) ** i for i, cf in enumerate(akislar))
    f_alt, f_ust = npv(alt), npv(ust)
    if f_alt * f_ust > 0:
        return None
    for _ in range(300):
        orta = (alt + ust) / 2
        f = npv(orta)
        if abs(f) < tol:
            return orta
        if f_alt * f < 0:
            ust, f_ust = orta, f
        else:
            alt, f_alt = orta, f
    return (alt + ust) / 2


def gmsi_vergisi(brut_kira, isletme_gideri, kar_payi, iktisap_bedeli, yil_no, v):
    if not v.get("gmsi_uygula"):
        return 0.0
    istisna = v["istisna"] * (1 + v.get("istisna_artis", 0.0)) ** (yil_no - 1)
    if v.get("yontem") == "gercek":
        # Gerçek gider: işletme giderleri + finansman kâr payı + amortisman (%2)
        # + ilk 5 yıl iktisap bedelinin %5'i (GVK 74/4). Yaklaşıktır, SMMM'ye doğrulat.
        indirim = isletme_gideri + kar_payi + iktisap_bedeli * 0.02
        if yil_no <= 5:
            indirim += iktisap_bedeli * 0.05
        matrah = max(0.0, brut_kira - istisna) - indirim
        # istisna kullanılınca gerçek giderin istisnaya isabet eden kısmı indirilemez
        matrah = max(0.0, matrah)
    else:
        kalan = max(0.0, brut_kira - istisna)
        matrah = kalan * (1 - v["goturu_gider_orani"])
    return matrah * v["marjinal_vergi_orani"]


# ------------------------------------------------------------------ ana hesap

IZINLI_MODELLER = {"katilim_murabaha", "tasarruf_finansman", "toki_kooperatif",
                   "karz_hasen", "ozkaynak"}


def model_dogrula(f):
    m = f.get("model", "katilim_murabaha")
    if f.get("kredi_tutari", 0) > 0 and m not in IZINLI_MODELLER:
        raise ValueError(
            f"finansman.model='{m}' desteklenmiyor. Bu skill yalnızca faizsiz kanalları "
            f"modellemektedir: {', '.join(sorted(IZINLI_MODELLER))}. Faizli konut kredisi "
            "senaryosu üretilmez."
        )
    return m


def analiz(g):
    model_dogrula(g["finansman"])
    a, k, gd = g["alim"], g["kira"], g["giderler"]
    v, f, b, alt = g["vergi"], g["finansman"], g["beklenti"], g["alternatif"]
    N = int(b["elde_tutma_yili"])

    fiyat = a["ilan_fiyati"] * (1 - a.get("pazarlik_indirimi", 0.0))
    harc = fiyat * a.get("tapu_harci_orani", 0.0)
    komisyon = fiyat * a.get("emlakci_komisyon_orani", 0.0)
    fin_masraf = f.get("tahsis_ucreti", 0.0) + f.get("diger_finansman_masrafi", 0.0)
    yan_maliyet = harc + komisyon + a.get("tadilat", 0.0) + a.get("diger_alim_masrafi", 0.0) + fin_masraf
    toplam_giris = fiyat + yan_maliyet

    kredi = min(f.get("kredi_tutari", 0.0), fiyat)
    ozkaynak = toplam_giris - kredi
    aylik_taksit, kredi_yillari = kredi_yil_ozeti(kredi, f["aylik_oran"], int(f["vade_ay"]), N)

    # --- yıl 1 statik göstergeler (kaldıraçsız)
    brut_kira_1 = k["aylik_kira"] * 12
    efektif_kira_1 = brut_kira_1 * (1 - k.get("bos_kalma_orani", 0.0))
    isletme_1 = (gd["aylik_aidat_ev_sahibi"] * 12 + gd["yillik_emlak_vergisi"] + gd["yillik_sigorta"]
                 + brut_kira_1 * (gd.get("bakim_rezervi_kira_orani", 0.0) + gd.get("yonetim_gideri_kira_orani", 0.0)))
    vergi_1 = gmsi_vergisi(efektif_kira_1, isletme_1, kredi_yillari[0]["kar_payi"] if kredi_yillari else 0.0,
                           fiyat, 1, v)
    noi_1 = efektif_kira_1 - isletme_1              # vergi öncesi net işletme geliri
    net_1 = noi_1 - vergi_1                          # vergi sonrası, finansman öncesi

    gostergeler = {
        "toplam_giris_maliyeti": toplam_giris,
        "yan_maliyet_orani": yan_maliyet / fiyat if fiyat else 0,
        "ozkaynak": ozkaynak,
        "brut_kira_getirisi": brut_kira_1 / toplam_giris,
        "net_kira_getirisi_cap_rate": noi_1 / toplam_giris,
        "vergi_sonrasi_net_getiri": net_1 / toplam_giris,
        "brut_kira_carpani_yil": fiyat / brut_kira_1 if brut_kira_1 else None,
        "net_kira_carpani_yil": toplam_giris / net_1 if net_1 > 0 else None,
        "aylik_taksit": aylik_taksit,
        "yil1_kaldiracli_nakit_getirisi": ((net_1 - (kredi_yillari[0]["odenen"] if kredi_yillari else 0.0)) / ozkaynak)
                                          if ozkaynak > 0 else None,
        "yil1_aylik_net_cep": (net_1 - (kredi_yillari[0]["odenen"] if kredi_yillari else 0.0)) / 12,
    }

    # --- yıl yıl nakit akışı
    satirlar = []
    akis_ozkaynak = [-ozkaynak]
    for yil in range(1, N + 1):
        art_k = (1 + k["yillik_kira_artis"]) ** (yil - 1)
        art_g = (1 + gd["yillik_gider_artis"]) ** (yil - 1)
        brut = brut_kira_1 * art_k
        efektif = brut * (1 - k.get("bos_kalma_orani", 0.0))
        isletme = ((gd["aylik_aidat_ev_sahibi"] * 12 + gd["yillik_emlak_vergisi"] + gd["yillik_sigorta"]) * art_g
                   + brut * (gd.get("bakim_rezervi_kira_orani", 0.0) + gd.get("yonetim_gideri_kira_orani", 0.0)))
        ky = kredi_yillari[yil - 1] if yil <= len(kredi_yillari) else {"odenen": 0.0, "kar_payi": 0.0, "kalan_borc": 0.0}
        vergi = gmsi_vergisi(efektif, isletme, ky["kar_payi"], fiyat, yil, v)
        noi = efektif - isletme
        nakit = noi - vergi - ky["odenen"]
        satirlar.append({
            "yil": yil,
            "brut_kira": brut,
            "efektif_kira": efektif,
            "isletme_gideri": isletme,
            "gmsi_vergisi": vergi,
            "noi": noi,
            "borc_odemesi": ky["odenen"],
            "net_nakit": nakit,
            "kalan_borc": ky["kalan_borc"],
            "deger": fiyat * (1 + b["yillik_deger_artisi"]) ** yil,
        })
        akis_ozkaynak.append(nakit)

    # --- çıkış
    satis_degeri = fiyat * (1 + b["yillik_deger_artisi"]) ** N
    satis_masrafi = satis_degeri * (b.get("satis_komisyon_orani", 0.0) + b.get("satis_tapu_harci_orani", 0.0))
    dak_vergisi = 0.0
    if N < v.get("deger_artis_istisna_yili", 5):
        endeksli_maliyet = toplam_giris * (1 + b["enflasyon"]) ** N   # ÜFE endekslemesi yaklaşığı
        kazanc = max(0.0, satis_degeri - satis_masrafi - endeksli_maliyet)
        dak_vergisi = kazanc * v.get("deger_artis_marjinal_oran", 0.35)
    kalan_borc = satirlar[-1]["kalan_borc"] if satirlar else 0.0
    net_satis = satis_degeri - satis_masrafi - dak_vergisi - kalan_borc
    akis_ozkaynak[-1] += net_satis

    ozkaynak_irr = irr(akis_ozkaynak)
    reel_irr = ((1 + ozkaynak_irr) / (1 + b["enflasyon"]) - 1) if ozkaynak_irr is not None else None

    # --- alternatif yatırımla adil karşılaştırma (nakit akışları alternatif oranda değerlendirilir)
    r_alt = alt["yillik_getiri"]
    gm_fv = 0.0
    for i, cf in enumerate(akis_ozkaynak[1:], start=1):
        gm_fv += cf * (1 + r_alt) ** (N - i)
    alt_fv = ozkaynak * (1 + r_alt) ** N
    reel_carpan = (1 + b["enflasyon"]) ** N

    def _fv_farki(g_deger):
        gg = deepcopy(g)
        gg["beklenti"]["yillik_deger_artisi"] = g_deger
        r = _hizli_fv(gg)
        return r - alt_fv

    basabas_deger_artisi = _bisect(_fv_farki, -0.5, 3.0)

    return {
        "girdi": g,
        "fiyat": fiyat,
        "gostergeler": gostergeler,
        "yillar": satirlar,
        "cikis": {
            "satis_degeri": satis_degeri,
            "satis_masrafi": satis_masrafi,
            "deger_artis_kazanci_vergisi": dak_vergisi,
            "kapatilan_borc": kalan_borc,
            "net_satis_geliri": net_satis,
        },
        "sonuc": {
            "ozkaynak_irr_nominal": ozkaynak_irr,
            "ozkaynak_irr_reel": reel_irr,
            "gayrimenkul_gelecek_deger": gm_fv,
            "alternatif_gelecek_deger": alt_fv,
            "fark": gm_fv - alt_fv,
            "gayrimenkul_bugunku_alim_gucu": gm_fv / reel_carpan,
            "alternatif_bugunku_alim_gucu": alt_fv / reel_carpan,
            "basabas_yillik_deger_artisi": basabas_deger_artisi,
        },
        "duyarlilik": duyarlilik(g),
    }


def _hizli_fv(g):
    """Sadece nihai FV döndüren hafif tekrar hesap (duyarlılık ve başabaş için)."""
    a, k, gd = g["alim"], g["kira"], g["giderler"]
    v, f, b, alt = g["vergi"], g["finansman"], g["beklenti"], g["alternatif"]
    N = int(b["elde_tutma_yili"])
    fiyat = a["ilan_fiyati"] * (1 - a.get("pazarlik_indirimi", 0.0))
    yan = (fiyat * (a.get("tapu_harci_orani", 0) + a.get("emlakci_komisyon_orani", 0))
           + a.get("tadilat", 0) + a.get("diger_alim_masrafi", 0)
           + f.get("tahsis_ucreti", 0) + f.get("diger_finansman_masrafi", 0))
    toplam = fiyat + yan
    kredi = min(f.get("kredi_tutari", 0.0), fiyat)
    ozkaynak = toplam - kredi
    _, ky = kredi_yil_ozeti(kredi, f["aylik_oran"], int(f["vade_ay"]), N)
    brut1 = k["aylik_kira"] * 12
    r_alt = alt["yillik_getiri"]
    fv = 0.0
    for yil in range(1, N + 1):
        brut = brut1 * (1 + k["yillik_kira_artis"]) ** (yil - 1)
        efektif = brut * (1 - k.get("bos_kalma_orani", 0.0))
        isletme = ((gd["aylik_aidat_ev_sahibi"] * 12 + gd["yillik_emlak_vergisi"] + gd["yillik_sigorta"])
                   * (1 + gd["yillik_gider_artis"]) ** (yil - 1)
                   + brut * (gd.get("bakim_rezervi_kira_orani", 0) + gd.get("yonetim_gideri_kira_orani", 0)))
        y = ky[yil - 1] if yil <= len(ky) else {"odenen": 0.0, "kar_payi": 0.0, "kalan_borc": 0.0}
        vergi = gmsi_vergisi(efektif, isletme, y["kar_payi"], fiyat, yil, v)
        fv += (efektif - isletme - vergi - y["odenen"]) * (1 + r_alt) ** (N - yil)
    satis = fiyat * (1 + b["yillik_deger_artisi"]) ** N
    masraf = satis * (b.get("satis_komisyon_orani", 0) + b.get("satis_tapu_harci_orani", 0))
    dak = 0.0
    if N < v.get("deger_artis_istisna_yili", 5):
        endeksli = toplam * (1 + b["enflasyon"]) ** N
        dak = max(0.0, satis - masraf - endeksli) * v.get("deger_artis_marjinal_oran", 0.35)
    kalan = ky[-1]["kalan_borc"] if ky else 0.0
    return fv + satis - masraf - dak - kalan


def _bisect(fn, alt, ust, tol=1e-6):
    f_alt, f_ust = fn(alt), fn(ust)
    if f_alt * f_ust > 0:
        return None
    for _ in range(200):
        orta = (alt + ust) / 2
        f = fn(orta)
        if abs(f) < 1.0 or (ust - alt) < tol:
            return orta
        if f_alt * f < 0:
            ust, f_ust = orta, f
        else:
            alt, f_alt = orta, f
    return (alt + ust) / 2


def duyarlilik(g):
    """Değer artışı × kira artışı ızgarasında reel özkaynak IRR."""
    b = g["beklenti"]
    g0, k0, enf = b["yillik_deger_artisi"], g["kira"]["yillik_kira_artis"], b["enflasyon"]
    d_ekseni = [round(g0 + d, 4) for d in (-0.10, -0.05, 0.0, 0.05, 0.10)]
    k_ekseni = [round(k0 + d, 4) for d in (-0.05, 0.0, 0.05)]
    izgara = []
    for kd in k_ekseni:
        satir = []
        for dd in d_ekseni:
            gg = deepcopy(g)
            gg["beklenti"]["yillik_deger_artisi"] = dd
            gg["kira"]["yillik_kira_artis"] = kd
            gg["duyarlilik_kapali"] = True
            r = analiz_irr(gg)
            satir.append(None if r is None else (1 + r) / (1 + enf) - 1)
        izgara.append({"kira_artisi": kd, "degerler": satir})
    return {"deger_artisi_ekseni": d_ekseni, "satirlar": izgara}


def analiz_irr(g):
    """Sadece özkaynak IRR (duyarlılık ızgarası için, özyineleme yok)."""
    a, k, gd = g["alim"], g["kira"], g["giderler"]
    v, f, b = g["vergi"], g["finansman"], g["beklenti"]
    N = int(b["elde_tutma_yili"])
    fiyat = a["ilan_fiyati"] * (1 - a.get("pazarlik_indirimi", 0.0))
    yan = (fiyat * (a.get("tapu_harci_orani", 0) + a.get("emlakci_komisyon_orani", 0))
           + a.get("tadilat", 0) + a.get("diger_alim_masrafi", 0)
           + f.get("tahsis_ucreti", 0) + f.get("diger_finansman_masrafi", 0))
    toplam = fiyat + yan
    kredi = min(f.get("kredi_tutari", 0.0), fiyat)
    akis = [-(toplam - kredi)]
    _, ky = kredi_yil_ozeti(kredi, f["aylik_oran"], int(f["vade_ay"]), N)
    brut1 = k["aylik_kira"] * 12
    for yil in range(1, N + 1):
        brut = brut1 * (1 + k["yillik_kira_artis"]) ** (yil - 1)
        efektif = brut * (1 - k.get("bos_kalma_orani", 0.0))
        isletme = ((gd["aylik_aidat_ev_sahibi"] * 12 + gd["yillik_emlak_vergisi"] + gd["yillik_sigorta"])
                   * (1 + gd["yillik_gider_artis"]) ** (yil - 1)
                   + brut * (gd.get("bakim_rezervi_kira_orani", 0) + gd.get("yonetim_gideri_kira_orani", 0)))
        y = ky[yil - 1] if yil <= len(ky) else {"odenen": 0.0, "kar_payi": 0.0, "kalan_borc": 0.0}
        vergi = gmsi_vergisi(efektif, isletme, y["kar_payi"], fiyat, yil, v)
        akis.append(efektif - isletme - vergi - y["odenen"])
    satis = fiyat * (1 + b["yillik_deger_artisi"]) ** N
    masraf = satis * (b.get("satis_komisyon_orani", 0) + b.get("satis_tapu_harci_orani", 0))
    dak = 0.0
    if N < v.get("deger_artis_istisna_yili", 5):
        endeksli = toplam * (1 + b["enflasyon"]) ** N
        dak = max(0.0, satis - masraf - endeksli) * v.get("deger_artis_marjinal_oran", 0.35)
    akis[-1] += satis - masraf - dak - (ky[-1]["kalan_borc"] if ky else 0.0)
    return irr(akis)


# --------------------------------------------------------------------- rapor

def _p(x):
    return "—" if x is None else f"%{x*100:,.1f}".replace(",", ".")


def _t(x):
    return "—" if x is None else f"{x:,.0f}".replace(",", ".")


def rapor(r):
    g = r["girdi"]
    go, so, ci = r["gostergeler"], r["sonuc"], r["cikis"]
    N = int(g["beklenti"]["elde_tutma_yili"])
    L = []
    L.append(f"### {g.get('baslik','Konut')} — {N} yıllık analiz")
    L.append("")
    L.append("**Giriş maliyeti**")
    L.append(f"- Pazarlıklı alım fiyatı: {_t(r['fiyat'])}")
    L.append(f"- Toplam giriş (yan maliyetler dahil): {_t(go['toplam_giris_maliyeti'])}  "
             f"(yan maliyet fiyatın {_p(go['yan_maliyet_orani'])}'i)")
    L.append(f"- Özkaynak: {_t(go['ozkaynak'])} | Kredi/finansman: {_t(g['finansman']['kredi_tutari'])}"
             + (f" | Aylık taksit: {_t(go['aylik_taksit'])}" if g['finansman']['kredi_tutari'] else ""))
    if g["finansman"].get("kredi_tutari"):
        L.append(f"- Finansman modeli: {g['finansman'].get('model','katilim_murabaha')} "
                 f"(aylık kâr payı {_p(g['finansman']['aylik_oran'])})")
    L.append("")
    L.append("**Yıl 1 getiri göstergeleri**")
    L.append(f"- Brüt kira getirisi: {_p(go['brut_kira_getirisi'])} | Net (cap rate): {_p(go['net_kira_getirisi_cap_rate'])}"
             f" | Vergi sonrası: {_p(go['vergi_sonrasi_net_getiri'])}")
    L.append(f"- Brüt kira çarpanı: {go['brut_kira_carpani_yil']:.1f} yıl | "
             f"Net çarpan (vergi sonrası, yan maliyet dahil): "
             + (f"{go['net_kira_carpani_yil']:.1f} yıl" if go['net_kira_carpani_yil'] else "negatif"))
    if g["finansman"]["kredi_tutari"]:
        L.append(f"- Kaldıraçlı nakit getirisi (yıl 1): {_p(go['yil1_kaldiracli_nakit_getirisi'])} | "
                 f"Aylık cebe giren/çıkan: {_t(go['yil1_aylik_net_cep'])}")
    L.append("")
    L.append("**Yıl yıl nakit akışı**")
    L.append("| Yıl | Brüt kira | İşletme gid. | GMSİ vergisi | Borç ödemesi | Net nakit | Değer |")
    L.append("|---|---|---|---|---|---|---|")
    for s in r["yillar"]:
        L.append(f"| {s['yil']} | {_t(s['brut_kira'])} | {_t(s['isletme_gideri'])} | {_t(s['gmsi_vergisi'])} | "
                 f"{_t(s['borc_odemesi'])} | {_t(s['net_nakit'])} | {_t(s['deger'])} |")
    L.append("")
    L.append(f"**Çıkış (yıl {N})**")
    L.append(f"- Satış değeri: {_t(ci['satis_degeri'])} | Satış masrafı: {_t(ci['satis_masrafi'])} | "
             f"Değer artış kazancı vergisi: {_t(ci['deger_artis_kazanci_vergisi'])}")
    L.append(f"- Kapatılan borç: {_t(ci['kapatilan_borc'])} → Net satış geliri: {_t(ci['net_satis_geliri'])}")
    L.append("")
    L.append("**Sonuç**")
    L.append(f"- Özkaynak IRR: nominal {_p(so['ozkaynak_irr_nominal'])} | **reel {_p(so['ozkaynak_irr_reel'])}** "
             f"(enflasyon varsayımı {_p(g['beklenti']['enflasyon'])})")
    L.append(f"- {N} yıl sonunda gayrimenkul: {_t(so['gayrimenkul_gelecek_deger'])} | "
             f"{g['alternatif'].get('ad','alternatif')}: {_t(so['alternatif_gelecek_deger'])} | "
             f"fark: {_t(so['fark'])}")
    L.append(f"- Bugünkü alım gücüyle: gayrimenkul {_t(so['gayrimenkul_bugunku_alim_gucu'])} vs "
             f"alternatif {_t(so['alternatif_bugunku_alim_gucu'])}")
    bb = so["basabas_yillik_deger_artisi"]
    L.append(f"- **Başabaş:** alternatifle eşitlenmek için konutun yılda {_p(bb)} değer kazanması gerekiyor "
             f"(senaryo varsayımı {_p(g['beklenti']['yillik_deger_artisi'])}).")
    L.append("")
    L.append("**Duyarlılık — reel özkaynak IRR (satır: kira artışı, sütun: değer artışı)**")
    d = r["duyarlilik"]
    L.append("| kira ↓ / değer → | " + " | ".join(_p(x) for x in d["deger_artisi_ekseni"]) + " |")
    L.append("|---" * (len(d["deger_artisi_ekseni"]) + 1) + "|")
    for satir in d["satirlar"]:
        L.append(f"| {_p(satir['kira_artisi'])} | " + " | ".join(_p(x) for x in satir["degerler"]) + " |")
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
    g = _birlestir(SABLON, gelen)
    r = analiz(g)
    if "--json" in sys.argv:
        print(json.dumps(r, ensure_ascii=False, indent=2, default=float))
    else:
        print(rapor(r))


if __name__ == "__main__":
    main()

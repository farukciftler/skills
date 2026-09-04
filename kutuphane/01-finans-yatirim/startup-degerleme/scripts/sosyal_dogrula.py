#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sosyal_dogrula.py — Bir sosyal medya hesabinin takipcileri gercek mi, kitle urune
donusuyor mu sorularini sayiya ceviren hesap makinesi.

Neden gerekli: Buyuk takipci sayisi bir startup raporunda en cok yanlis okunan metriktir.
Takipci satin almak ucuzdur (TR'de 1000 takipci ~ 2-5 USD); etkilesim satin almak pahalidir
ve surdurulemez. Bu yuzden **etkilesim orani takipci sayisindan cok daha zor taklit edilir**
ve hesabin gercekligini olcmenin en ucuz yolu odur.

Veri toplama yontemi (giris yapmadan) references/sosyal-dogrulama.md icinde anlatiliyor.
Bu script sadece hesabi yapar; sayilari sen toplayip verirsin.

Kullanim:
    python3 sosyal_dogrula.py --takipci 49300 --begeniler 186,165,165,44,44,23,17,16,15,12,10,9 \
        --yorumlar 0,1,0,0,0,0,0,0,0,0,0,0 --platform instagram \
        --indirme 4300 --gonderi-sayisi 228
"""

import argparse
import statistics

# Saglikli etkilesim orani referanslari (takipci basina begeni+yorum, %), 2026.
# Kaynak: sektor konsensusu; kendi taramalarindan cikan degerlerle
# veri/benchmarkler.md uzerinden guncelle.
SAGLIKLI = {
    "instagram": {"dusuk": 1.0, "iyi": 3.0, "referans": 2.0},
    "tiktok":    {"dusuk": 3.0, "iyi": 9.0, "referans": 5.0},
    "x":         {"dusuk": 0.3, "iyi": 1.5, "referans": 0.8},
    "youtube":   {"dusuk": 1.0, "iyi": 4.0, "referans": 2.0},
    "linkedin":  {"dusuk": 1.0, "iyi": 4.0, "referans": 2.0},
}


def yorumla(er, ref):
    """Etkilesim oranini karara cevir. Esikler referansin katlari olarak tanimli."""
    oran = er / ref["referans"]
    if er >= ref["iyi"]:
        return ("GERCEK VE CANLI", oran,
                "Kitle hem gercek hem ilgili. Bu hesap satilabilir bir medya varligidir.")
    if er >= ref["dusuk"]:
        return ("GERCEK", oran,
                "Etkilesim normal bandin icinde. Kitle gercek kabul edilebilir.")
    if er >= ref["dusuk"] / 3:
        return ("ZAYIF / YORGUN", oran,
                "Kitle muhtemelen gercek ama ilgisini kaybetmis ya da icerik kitleyle "
                "ortusmuyor. Medya degeri ciddi sekilde iskontolanir.")
    if er >= ref["dusuk"] / 15:
        return ("SUPHELI", oran,
                "Bu seviye organik bir hesapta nadiren gorulur. Takipcilerin onemli bir "
                "kismi satin alinmis ya da hesap uzun sure atil kalmis olabilir.")
    return ("BUYUK OLCUDE OLU/SAHTE", oran,
            "Bu etkilesim seviyesi organik bir kitleyle acıklanamaz. Takipci sayisi "
            "raporda varlik olarak fiyatlanmamalidir.")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--takipci", type=int, required=True)
    p.add_argument("--begeniler", required=True,
                   help="Ornekledigin gonderilerin begeni sayilari, virgulle")
    p.add_argument("--yorumlar", help="Ayni sirayla yorum sayilari, virgulle (opsiyonel)")
    p.add_argument("--platform", default="instagram", choices=list(SAGLIKLI))
    p.add_argument("--indirme", type=int, help="Urunun toplam indirme sayisi (donusum icin)")
    p.add_argument("--gonderi-sayisi", type=int, help="Hesaptaki toplam gonderi sayisi")
    p.add_argument("--takip-edilen", type=int, help="Hesabin takip ettigi kisi sayisi")
    a = p.parse_args()

    beg = [int(x) for x in a.begeniler.split(",") if x.strip()]
    yor = [int(x) for x in a.yorumlar.split(",")] if a.yorumlar else []
    ref = SAGLIKLI[a.platform]

    med_beg = statistics.median(beg)
    ort_beg = statistics.mean(beg)
    med_yor = statistics.median(yor) if yor else 0
    etkilesim = med_beg + med_yor
    er = etkilesim / a.takipci * 100

    karar, oran, aciklama = yorumla(er, ref)

    print("=" * 72)
    print(f"  SOSYAL HESAP GERCEKLIK DENETIMI — {a.platform}")
    print("=" * 72)
    print(f"  Takipci                 : {a.takipci:,}".replace(",", "."))
    print(f"  Ornek gonderi sayisi    : {len(beg)}")
    print(f"  Begeni  medyan / ortalama: {med_beg:.0f} / {ort_beg:.0f}")
    print(f"  Begeni  min / maks      : {min(beg)} / {max(beg)}")
    if yor:
        print(f"  Yorum medyan            : {med_yor:.0f}")
    print(f"\n  ETKILESIM ORANI         : %{er:.3f}")
    print(f"  Saglikli bant ({a.platform}) : %{ref['dusuk']}–%{ref['iyi']} "
          f"(referans %{ref['referans']})")
    print(f"  Referansin              : {oran:.3f} kati")
    print(f"\n  >>> KARAR: {karar}")
    print(f"      {aciklama}")

    # Dagilim testi: yeni gonderiler eskilerden cok farkliysa reklam/satin alma sinyali
    if len(beg) >= 6:
        yeni = beg[:max(3, len(beg) // 4)]
        eski = beg[len(beg) // 2:]
        if statistics.median(eski) > 0:
            fark = statistics.median(yeni) / statistics.median(eski)
            if fark >= 4:
                print(f"\n  ! DAGILIM UYARISI: En yeni gonderilerin medyani, eskilerin "
                      f"{fark:.1f} katı.\n    Organik buyume bu kadar ani olmaz. Muhtemel "
                      "sebep: son donemde reklamla\n    one cikarma (paid reach) ya da "
                      "etkilesim satin alma. Ayirt etmek icin\n    yorum/begeni oranina bak: "
                      "reklamda yorum da artar, satin almada artmaz.")
            elif fark <= 0.25:
                print(f"\n  ! DAGILIM UYARISI: Yeni gonderiler eskilerin {fark:.2f} kati "
                      "etkilesim aliyor.\n    Hesap sonuyor ya da algoritma erisimi kesmis.")

    if yor and sum(yor) == 0 and med_beg > 50:
        print("\n  ! YORUM UYARISI: Begeni var ama yorum yok. Gercek kitlelerde yorum, "
              "begeninin\n    %1-5'i kadar olur. Sifir yorum + yuksek begeni satin alinmis "
              "etkilesim imzasidir.")

    if a.takip_edilen and a.takipci and a.takip_edilen > a.takipci * 0.5:
        print("\n  ! TAKIP ORANI UYARISI: Hesap, takipci sayisina yakin sayida hesabi takip "
              "ediyor.\n    Karsilikli takip (follow-for-follow) ile sisirilmis olabilir.")

    # --- Kitle -> urun donusumu
    if a.indirme:
        print("\n" + "-" * 72)
        print("  KITLE → URUN DONUSUMU")
        print("-" * 72)
        oran_ti = a.takipci / a.indirme
        print(f"  Takipci / toplam indirme : {oran_ti:.1f}×  (saglikli bant 0,1–1,0)")
        if oran_ti > 3:
            print("  >>> Kanal urune donusmuyor. Iki acıklamadan biri gecerli ve hangisi\n"
                  "      oldugu ETKILESIM ORANINDAN anlasilir:")
            print("      - Etkilesim de dusukse  -> takipciler gercek degil/olu; "
                  "kanal bir varlik degil.")
            print("      - Etkilesim saglikliysa -> kitle gercek ama urune ilgi duymuyor; "
                  "sorun urunde\n        veya cagri-eylem/onboarding akisinda.")
        # Etkilesen kitle uzerinden indirme donusumu
        if etkilesim > 0:
            print(f"  Gonderi basi etkilesen kisi: ~{etkilesim:.0f}")
            print(f"  Bu hacimle bir gonderiden beklenebilecek indirme: "
                  f"~{etkilesim*0.05:.0f}–{etkilesim*0.2:.0f}")
        if a.gonderi_sayisi:
            print(f"  Toplam {a.gonderi_sayisi} gonderi × ~{etkilesim:.0f} etkilesim = "
                  f"~{a.gonderi_sayisi*etkilesim:,.0f} kumulatif etkilesim".replace(",", "."))

    # --- Medya varligi olarak deger
    print("\n" + "-" * 72)
    print("  HESABIN VARLIK DEGERI")
    print("-" * 72)
    etkin = a.takipci * min(1.0, er / ref["referans"])
    print(f"  Etkilesime gore duzeltilmis 'etkin takipci': {etkin:,.0f}".replace(",", "."))
    print(f"  Medya varlik degeri (1000 etkin takipci basina 25–80 USD):")
    print(f"      {etkin/1000*25:,.0f} – {etkin/1000*80:,.0f} USD".replace(",", "."))
    if etkin < a.takipci * 0.15:
        print("  NOT: Ham takipci sayisi uzerinden hesaplanan deger "
              f"({a.takipci/1000*25:,.0f}–{a.takipci/1000*80:,.0f} USD) bu hesap icin"
              .replace(",", "."))
        print("       GECERSIZDIR. Raporda ham takipci sayisini varlik olarak yazma;")
        print("       yazarsan raporun en buyuk avantaj maddesi denetimde cokecektir.")
    print("  Ayrica: marka/handle/gecmis icerik arsivi ayri bir kalem olarak degerlendirilir;")
    print("  bu hesap takipci degeri sifir olsa bile birkac yuz USD tasiyabilir.")
    print()


if __name__ == "__main__":
    main()

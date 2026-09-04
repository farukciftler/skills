#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fiyat_hesap.py — fiyatlandirma-uzmani skill'inin deterministik hesap araci.

Alt komutlar:
  taban     Maliyet tabani: hedef gelirden minimum gun/saat ucreti
  deger     Deger bazli ucret bandi (%10-20 payi) + ROI tablosu
  proje     Efordan 3 secenekli proje fiyati (taban/tavan kontrollu)
  retainer  Aylik retainer bedeli + taahhut indirimi
  saas      SaaS birim ekonomisi: marj, LTV/CAC, geri odeme
  indirim   Indirimin marj etkisi: ayni kar icin gereken ek hacim
  zam       Zammin tolere edebilecegi musteri kaybi + endeks hesabi

Para birimi agnostiktir; girdiyi hangi birimde verirsen cikti o birimdedir.
"""
import argparse
import sys


def para(x):
    s = f"{x:,.0f}" if abs(x) >= 100 else f"{x:,.2f}"
    return s.replace(",", "_").replace(".", ",").replace("_", ".")


def yuzde(x):
    return f"%{x * 100:,.1f}".replace(".", ",")


def ciz(baslik):
    print("\n" + baslik)
    print("-" * max(28, len(baslik)))


def cmd_taban(a):
    yillik_gider = a.gider_ay * 12
    if not (0 <= a.vergi_pay < 1):
        sys.exit("HATA: --vergi-pay 0 ile 1 arasinda oran olmali (orn. 0.25)")
    gerekli_brut = (a.hedef_net + yillik_gider) / (1 - a.vergi_pay)
    gun_ucret = gerekli_brut / a.gun
    saat_ucret = gun_ucret / a.saat
    ciz("MALIYET TABANI (pazar fiyati DEGIL, alt sinir)")
    print(f"Hedef yillik net gelir : {para(a.hedef_net)}")
    print(f"Yillik isletme gideri  : {para(yillik_gider)}  ({para(a.gider_ay)}/ay)")
    print(f"Vergi+SGK efektif payi : {yuzde(a.vergi_pay)}  (gercek oran icin sahis-vergi-yukumluluk)")
    print(f"Gerekli yillik ciro    : {para(gerekli_brut)}")
    print(f"Faturalanabilir gun    : {a.gun} gun/yil  (solo gercekligi: 100-140)")
    print(f">>> Minimum GUN ucreti : {para(gun_ucret)}")
    print(f">>> Minimum SAAT ucreti: {para(saat_ucret)}  ({a.saat} faturalanabilir saat/gun)")
    print("Not: Hicbir teklif secenegi bu cizginin altina kurgulanmaz.")


def cmd_deger(a):
    etki_adj = a.etki * a.guven * a.yil
    alt = etki_adj * a.pay_min
    ust = etki_adj * a.pay_max
    onerilen = etki_adj * (a.pay_min + a.pay_max) / 2
    ciz("DEGER BAZLI UCRET BANDI")
    print(f"Beyan edilen yillik etki : {para(a.etki)}")
    print(f"Guven katsayisi          : {a.guven}  (gerceklesme/atfedilme olasiligi)")
    print(f"Etki suresi carpani      : {a.yil}")
    print(f"Duzeltilmis etki         : {para(etki_adj)}")
    print(f">>> Ucret bandi          : {para(alt)}  -  {para(ust)}   (pay {yuzde(a.pay_min)}-{yuzde(a.pay_max)})")
    print(f">>> Onerilen nokta       : {para(onerilen)}")
    ciz("MUSTERI GOZUNDEN ROI (sunumda kullan)")
    for f in (alt, onerilen, ust):
        print(f"Ucret {para(f):>14}  ->  ilk yil geri donus ~{etki_adj / f:,.1f}x".replace(".", ","))
    if a.etki < 50000:
        print("UYARI: Etki kucuk (<50K); deger bazli kurgu yerine proje fiyati daha uygun olabilir.")


def cmd_proje(a):
    cekirdek = a.gun * a.gun_ucret * (1 + a.tampon)
    s1, s2, s3 = cekirdek * 0.6, cekirdek, cekirdek * 1.7
    ciz("3 SECENEKLI PROJE FIYATI")
    print(f"Efor: {a.gun} gun x {para(a.gun_ucret)}  + belirsizlik tamponu {yuzde(a.tampon)}")
    print(f"Secenek A  Cekirdek   (~0.6x): {para(s1)}")
    print(f"Secenek B  Onerilen   (1.0x) : {para(s2)}   <- hedeflenen satis")
    print(f"Secenek C  Kapsamli   (1.7x) : {para(s3)}   <- once bu sunulur (capa)")
    print("Odeme onerisi: %30-50 pesin, kalan kilometre taslarinda. Gecerlilik: 14-30 gun.")
    if a.taban_gun and a.gun_ucret < a.taban_gun:
        print(f"UYARI: Gun ucreti ({para(a.gun_ucret)}) taban gun ucretinin ({para(a.taban_gun)}) ALTINDA.")
    if a.deger_tavan:
        oran = s2 / a.deger_tavan
        print(f"Deger tavani kontrolu: onerilen fiyat, tavanin {yuzde(oran)}'i.")
        if s2 > a.deger_tavan:
            print("UYARI: Fiyat deger tavanini asiyor -> kapsami kucult veya degeri yeniden konus.")
        elif oran < 0.1:
            print("NOT: Fiyat degerin %10'unun altinda -> deger bazli kurguya gecmek para birakiyor olabilir.")


def cmd_retainer(a):
    indirimler = {3: 0.0, 6: 0.05, 12: 0.10}
    ind = a.indirim if a.indirim is not None else indirimler.get(a.taahhut, 0.0)
    aylik_liste = a.gun_ay * a.gun_ucret
    aylik = aylik_liste * (1 - ind)
    ciz("RETAINER FIYATI")
    print(f"Kapsam: ayda {a.gun_ay} gun x {para(a.gun_ucret)} = liste {para(aylik_liste)}/ay")
    print(f"Taahhut: {a.taahhut} ay  ->  indirim {yuzde(ind)}")
    print(f">>> Aylik bedel: {para(aylik)}   (donem toplami: {para(aylik * a.taahhut)})")
    print("Sozlesme notlari: kullanilmayan gun devretmez; kapsam disi is ayri teklif;")
    print("30 gun onceden fesih; 6-12 ayda fiyat gozden gecirme; TL ise endeksleme maddesi.")


def cmd_saas(a):
    if a.fiyat <= 0:
        sys.exit("HATA: --fiyat pozitif olmali")
    marj = (a.fiyat - a.cogs) / a.fiyat
    ciz("SAAS BIRIM EKONOMISI")
    print(f"Aylik fiyat: {para(a.fiyat)}   Birim COGS: {para(a.cogs)}   Brut marj: {yuzde(marj)}")
    min_fiyat = a.cogs / (1 - a.hedef_marj) if a.hedef_marj < 1 else float("inf")
    print(f"Hedef marj {yuzde(a.hedef_marj)} icin minimum fiyat: {para(min_fiyat)}")
    print("DURUM: " + ("marj hedefin ALTINDA -> fiyat/kredi kurgusunu gozden gecir." if marj < a.hedef_marj else "marj hedefi saglaniyor."))
    if a.kayip is not None and a.kayip > 0:
        churn = a.kayip / 100.0
        ltv = (a.fiyat * marj) / churn
        print(f"Aylik churn {yuzde(churn)} -> ort. musteri omru {1/churn:,.1f} ay, LTV ~{para(ltv)}".replace(".0 ay", " ay"))
        if a.cac is not None and a.cac > 0:
            oran = ltv / a.cac
            geri = a.cac / (a.fiyat * marj) if marj > 0 else float("inf")
            print(f"CAC {para(a.cac)} -> LTV/CAC = {oran:,.1f} (hedef >=3), geri odeme ~{geri:,.1f} ay (hedef <=12)".replace(".", ","))
    print("Not: AI-yogun urunde en yogun kullanici personasiyla stres testi yap (tavan kullanici hala karli mi?).")


def cmd_indirim(a):
    m, i = a.marj / 100.0, a.oran / 100.0
    ciz("INDIRIMIN MARJ ETKISI")
    print(f"Brut marj {yuzde(m)}, indirim {yuzde(i)}")
    if i >= m:
        print(">>> Indirim marji YUTUYOR: her satis zarar/sifir. Bu indirim verilmez; kapsam kucultulur.")
        return
    ek = i / (m - i)
    print(f">>> Ayni kari korumak icin gereken ek hacim: {yuzde(ek)}")
    print(f"(Hacim ayni kalirsa birim kar {yuzde(i / m)} dusuyor.)")
    print("Kural: indirim ancak karsilik ile (yillik pesin, taahhut, vaka calismasi, hacim).")


def cmd_zam(a):
    m, z = a.marj / 100.0, a.oran / 100.0
    ciz("ZAMMIN DAYANIKLILIGI")
    tolerans = z / (m + z)
    print(f"Brut marj {yuzde(m)}, zam {yuzde(z)}")
    print(f">>> Ayni kari korumak icin tolere edilebilir musteri/hacim kaybi: {yuzde(tolerans)}")
    print("Beklenen churn bu esigin altindaysa zam net kazanctir; 2 fatura donemi izle.")
    if a.enflasyon is not None:
        e = a.enflasyon / 100.0
        print(f"Endeks notu: son zamdan bu yana enflasyon {yuzde(e)} ise sadece reel korunma icin {yuzde(e)} zam gerekir;")
        print(f"{yuzde(z)} zam, reel olarak {yuzde((1 + z) / (1 + e) - 1)} degisim demektir.")


def main():
    p = argparse.ArgumentParser(description="Fiyatlandirma hesap araci (fiyatlandirma-uzmani skill)")
    sub = p.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("taban", help="maliyet tabani")
    t.add_argument("--hedef-net", type=float, required=True, dest="hedef_net", help="hedef yillik net gelir")
    t.add_argument("--gider-ay", type=float, default=0, dest="gider_ay", help="aylik isletme gideri")
    t.add_argument("--vergi-pay", type=float, default=0.25, dest="vergi_pay", help="efektif vergi+SGK orani (0-1)")
    t.add_argument("--gun", type=int, default=120, help="yillik faturalanabilir gun")
    t.add_argument("--saat", type=float, default=6, help="gunluk faturalanabilir saat")
    t.set_defaults(f=cmd_taban)

    d = sub.add_parser("deger", help="deger bazli band")
    d.add_argument("--etki", type=float, required=True, help="yillik parasal etki")
    d.add_argument("--guven", type=float, default=0.7, help="guven katsayisi 0-1")
    d.add_argument("--pay-min", type=float, default=0.10, dest="pay_min")
    d.add_argument("--pay-max", type=float, default=0.20, dest="pay_max")
    d.add_argument("--yil", type=float, default=1.0, help="etki suresi carpani")
    d.set_defaults(f=cmd_deger)

    pr = sub.add_parser("proje", help="3 secenekli proje fiyati")
    pr.add_argument("--gun", type=float, required=True, help="tahmini efor (gun)")
    pr.add_argument("--gun-ucret", type=float, required=True, dest="gun_ucret")
    pr.add_argument("--tampon", type=float, default=0.20, help="belirsizlik tamponu (0.15-0.35)")
    pr.add_argument("--taban-gun", type=float, default=None, dest="taban_gun", help="taban gun ucreti (kontrol)")
    pr.add_argument("--deger-tavan", type=float, default=None, dest="deger_tavan", help="deger tavani (kontrol)")
    pr.set_defaults(f=cmd_proje)

    r = sub.add_parser("retainer", help="retainer bedeli")
    r.add_argument("--gun-ay", type=float, required=True, dest="gun_ay", help="ayda kac gun")
    r.add_argument("--gun-ucret", type=float, required=True, dest="gun_ucret")
    r.add_argument("--taahhut", type=int, default=3, help="taahhut suresi (ay)")
    r.add_argument("--indirim", type=float, default=None, help="ozel indirim orani (0-1); bos: 3ay %%0 / 6ay %%5 / 12ay %%10")
    r.set_defaults(f=cmd_retainer)

    s = sub.add_parser("saas", help="birim ekonomi")
    s.add_argument("--fiyat", type=float, required=True, help="aylik fiyat")
    s.add_argument("--cogs", type=float, default=0, help="birim degisken maliyet (aylik)")
    s.add_argument("--hedef-marj", type=float, default=0.75, dest="hedef_marj")
    s.add_argument("--cac", type=float, default=None, help="musteri edinme maliyeti")
    s.add_argument("--kayip", type=float, default=None, help="aylik churn yuzdesi (orn. 3)")
    s.set_defaults(f=cmd_saas)

    i = sub.add_parser("indirim", help="indirim etkisi")
    i.add_argument("--marj", type=float, required=True, help="brut marj yuzdesi (orn. 70)")
    i.add_argument("--oran", type=float, required=True, help="indirim yuzdesi (orn. 20)")
    i.set_defaults(f=cmd_indirim)

    z = sub.add_parser("zam", help="zam dayanikliligi")
    z.add_argument("--marj", type=float, required=True, help="brut marj yuzdesi")
    z.add_argument("--oran", type=float, required=True, help="zam yuzdesi")
    z.add_argument("--enflasyon", type=float, default=None, help="son zamdan bu yana enflasyon yuzdesi")
    z.set_defaults(f=cmd_zam)

    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()

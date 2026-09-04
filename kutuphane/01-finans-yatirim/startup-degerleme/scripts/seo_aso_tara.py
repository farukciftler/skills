#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seo_aso_tara.py — Bir urunun bulunabilirligini olcer: App Store arama sirasi,
magaza listesi gorunurlugu, site teknik SEO'su ve marka arama talebi.

Neden gerekli: Indirme sayisi "kac kisi geldi" sorusunu cevaplar, bulunabilirlik
"gelmeye devam eder mi" sorusunu. Reklam durdugunda ayakta kalan tek kanal organik
bulunabilirliktir. Bir alici icin bu, satin aldigi seyin kendi kendine kullanici
uretip uretmedigi demektir ve dogrudan fiyattir.

Kullanim:
    python3 seo_aso_tara.py --ios-id 6633421265 --site uniboom.com.tr --marka uniboom \
        --kelimeler "üniversite,kampüs,öğrenci,kampüs sosyal ağ" \
        --rakip-ios-id 6744582219 --rakip-marka kampusify --ulke tr

Sadece standart kutuphane kullanir. Sonuclari [D] ve [T] ayrimiyla raporla:
iTunes arama sonucu gercek App Store siralamasi degil, ona yakin bir vekildir.
"""

import argparse, json, re, sys, urllib.parse, urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/122.0 Safari/537.36"
URUN_IZI = ("uygulama", "app", "üniversite", "kampüs", "kampus", "öğrenci", "ogrenci",
            "nedir", "indir", "giriş", "giris", "yorum")


def getir(url, timeout=20, ham=False):
    r = urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": UA,
                                             "Accept-Language": "tr-TR,tr;q=0.9"}), timeout=timeout)
    d = r.read()
    return (d, r.getcode()) if ham else d.decode("utf-8", errors="replace")


def kelime_sirasi(kelime, ulke, ids):
    """iTunes arama alaka sirasi. App Store siralamasinin vekili, birebir ayni degil."""
    u = ("https://itunes.apple.com/search?term=" + urllib.parse.quote(kelime) +
         f"&country={ulke}&entity=software&limit=100")
    try:
        r = json.loads(getir(u)).get("results", [])
    except Exception:
        return None, {}
    return len(r), {i: next((k + 1 for k, x in enumerate(r) if x.get("trackId") == i), None)
                    for i in ids}


def liste_kontrol(ulke, adlar):
    u = f"https://rss.marketingtools.apple.com/api/v2/{ulke}/apps/top-free/100/apps.json"
    try:
        r = json.loads(getir(u))["feed"]["results"]
    except Exception:
        return None
    return {a: next((i + 1 for i, x in enumerate(r) if a.lower() in x["name"].lower()), None)
            for a in adlar}


def site_seo(alan):
    s = {"alan": alan}
    try:
        ham, kod = getir("https://" + alan + "/", ham=True)
        h = ham.decode("utf-8", errors="replace")
    except Exception as e:
        return {**s, "hata": str(e)}
    metin = re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", h, flags=re.S | re.I)
    s.update({
        "http": kod,
        "byte": len(ham),
        "kelime": len(metin.split()),
        "title": (re.search(r"<title[^>]*>(.*?)</title>", h, re.S | re.I) or [None, None])[1],
        "meta_description": bool(re.search(r'name=["\']description["\']', h, re.I)),
        "open_graph": len(re.findall(r'property=["\']og:', h, re.I)),
        "schema_org": bool(re.search(r"application/ld\+json", h, re.I)),
        "canonical": bool(re.search(r'rel=["\']canonical["\']', h, re.I)),
        "h1": len(re.findall(r"<h1", h, re.I)),
        "ic_link": len(re.findall(r"<a ", h, re.I)),
        "magaza_linki": bool(re.search(r"apps\.apple\.com|play\.google\.com", h, re.I)),
        "hreflang": len(re.findall(r"hreflang=", h, re.I)),
    })
    for yol, ad in (("robots.txt", "robots_txt"), ("sitemap.xml", "sitemap_xml")):
        try:
            _, k = getir(f"https://{alan}/{yol}", ham=True)
            s[ad] = k
        except Exception as e:
            s[ad] = getattr(e, "code", "hata")
    return s


def marka_talebi(marka, ulke):
    """Google otomatik tamamlama, marka arama talebinin ucuz vekilidir.
    Oneri yoksa o marka icin anlamli arama hacmi yok demektir."""
    u = ("https://suggestqueries.google.com/complete/search?client=firefox"
         f"&hl={ulke}&gl={ulke}&q=" + urllib.parse.quote(marka))
    try:
        oneriler = json.loads(getir(u))[1]
    except Exception:
        return None
    urun = [o for o in oneriler if any(w in o.lower() for w in URUN_IZI)]
    return {"oneri_sayisi": len(oneriler), "oneriler": oneriler[:10],
            "urun_ilgili": urun, "sahiplik": len(urun) / len(oneriler) if oneriler else 0}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ios-id", type=int, required=True)
    p.add_argument("--marka", required=True)
    p.add_argument("--site")
    p.add_argument("--kelimeler", required=True, help="Virgulle ayrilmis anahtar kelimeler")
    p.add_argument("--rakip-ios-id", type=int)
    p.add_argument("--rakip-marka")
    p.add_argument("--ulke", default="tr")
    a = p.parse_args()

    ids = [a.ios_id] + ([a.rakip_ios_id] if a.rakip_ios_id else [])
    kelimeler = [k.strip() for k in a.kelimeler.split(",") if k.strip()]

    print("=" * 78)
    print(f"  BULUNABILIRLIK TARAMASI — {a.marka}  ({a.ulke.upper()})")
    print("=" * 78)

    print("\n[ APP STORE ARAMA SIRASI ]  iTunes alaka sirasi, gercek siralamanin vekili [T]")
    basli = 0
    for k in kelimeler:
        n, poz = kelime_sirasi(k, a.ulke, ids)
        if n is None:
            print(f"  {k:26} sorgu basarisiz"); continue
        benim = poz.get(a.ios_id)
        if benim:
            basli += 1
        satir = f"  {k:26} sonuc={n:3}  {a.marka}={str(benim) if benim else 'ilk 100 disi':>12}"
        if a.rakip_ios_id:
            rk = poz.get(a.rakip_ios_id)
            satir += f"   {a.rakip_marka or 'rakip'}={str(rk) if rk else 'yok':>10}"
        print(satir)
    kapsam = basli / len(kelimeler) if kelimeler else 0
    print(f"\n  Kelime kapsami: {basli}/{len(kelimeler)}  (%{kapsam*100:.0f})")
    if kapsam == 0:
        print("  >>> Urun hicbir ticari kelimede bulunmuyor. Organik magaza kesfi sifir.")
    elif kapsam < 0.35:
        print("  >>> Kapsam cok dar. Indirmelerin neredeyse tamami disaridan yonlendirmeyle geliyor;")
        print("      yonlendirme durdugunda buyume de durur.")

    print("\n[ MAGAZA LISTELERI ]")
    liste = liste_kontrol(a.ulke, [a.marka] + ([a.rakip_marka] if a.rakip_marka else []))
    if liste is None:
        print("  Liste verisi alinamadi.")
    else:
        for ad, sira in liste.items():
            print(f"  Genel ucretsiz ilk 100: {ad:16} {sira if sira else 'listede yok'}")
        print("  Not: genel liste yuksek bir esik, ayirt edici degil. Kategori listesi ucretsiz")
        print("       ucla alinamiyor; gerekiyorsa magaza uygulamasindan elle bakilmali.")

    if a.site:
        print("\n[ SITE TEKNIK SEO ]")
        s = site_seo(a.site)
        if "hata" in s:
            print("  " + s["hata"])
        else:
            eksik = []
            print(f"  HTTP {s['http']}  |  {s['byte']} byte  |  {s['kelime']} kelime  |  {s['ic_link']} link")
            print(f"  title            : {s['title']}")
            for alan, ad in [("meta_description", "meta description"), ("schema_org", "schema.org"),
                             ("canonical", "canonical"), ("magaza_linki", "magaza indirme linki")]:
                ok = s[alan]
                print(f"  {ad:17}: {'var' if ok else 'YOK'}")
                if not ok:
                    eksik.append(ad)
            print(f"  open graph etiket: {s['open_graph']}" + ("" if s["open_graph"] else "   (YOK)"))
            if not s["open_graph"]:
                eksik.append("open graph")
            for alan, ad in [("robots_txt", "robots.txt"), ("sitemap_xml", "sitemap.xml")]:
                v = s[alan]
                print(f"  {ad:17}: {'var' if v == 200 else f'YOK ({v})'}")
                if v != 200:
                    eksik.append(ad)
            if s["kelime"] < 300:
                eksik.append("indekslenebilir icerik")
                print(f"  >>> {s['kelime']} kelime, arama motoru icin siralanacak icerik yok.")
            if eksik:
                print(f"\n  Eksik: {', '.join(eksik)}")
                print("  Bunlarin hepsi birkac gunluk is. Eksik olmasi teknik borctan cok")
                print("  organik kanala hic yatirim yapilmadiginin isareti; deger tarafinda")
                print("  'buyume tamamen odemeli ya da elle yonlendirmeye bagli' diye okunur.")

    print("\n[ MARKA ARAMA TALEBI ]  Google otomatik tamamlama, talebin vekili [T]")
    for ad in [a.marka] + ([a.rakip_marka] if a.rakip_marka else []):
        t = marka_talebi(ad, a.ulke)
        if not t:
            print(f"  {ad:16} sorgu basarisiz"); continue
        print(f"  {ad:16} oneri={t['oneri_sayisi']:2}  urun ilgili={len(t['urun_ilgili']):2}  "
              f"marka sahipligi=%{t['sahiplik']*100:.0f}")
        if t["oneriler"]:
            print(f"                   {t['oneriler'][:5]}")
    print("\n  Oneri yoksa ya da onerilerin hicbiri urunle ilgili degilse: marka adi icin")
    print("  anlamli arama talebi yok, ya da marka adi baska bir sektorde daha guclu bir")
    print("  oyuncuya ait. Ikincisi devirde ayrica bir maliyet: alici markayi konumlandirmak")
    print("  icin harcama yapmak zorunda kalir ve bu fiyattan duser.\n")


if __name__ == "__main__":
    main()

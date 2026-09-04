#!/usr/bin/env python3
"""
Trip.com filtreli konaklama arama URL'i ureteci.

Bagimlilik yok. Filtre kodlari references/filtre-kodlari.md ile ayni kaynaktan gelir;
orasi guncellenirse buradaki FILTRELER sozlugunu de guncelle.

Ornek:
  python3 trip_url.py --city 338 --city-name London \
    --checkin 2026-10-01 --checkout 2026-10-06 --adults 1 --rooms 1 \
    --tip hotel --ucretsiz-iptal --ozel-banyo --ozel-tuvalet \
    --poi "51.5194133,-0.1269566,The British Museum,6789940" \
    --sirala yurume --curr TRY --locale tr-TR
"""

import argparse
import datetime as dt
import sys
from urllib.parse import quote

# --- filtre sozlugu: takma ad -> filterID ("type|value") ---------------------

FILTRELER = {
    # politika / odeme
    "ucretsiz-iptal":    "23|10",
    "aninda-onay":       "23|5",
    "otelde-odeme":      "7|1",
    "on-odeme":          "7|2",
    "kartsiz":           "7|6",
    # tesis tipi
    "hotel":             "75|TAG_495",
    "apart":             "75|TAG_513",
    "servisli-apart":    "75|TAG_505",
    "pansiyon":          "75|TAG_503",
    "bnb":               "75|TAG_504",
    "villa":             "75|TAG_507",
    "tatil-evi":         "75|TAG_514",
    "hostel":            "75|TAG_519",
    "kapsul":            "75|TAG_520",
    "han":               "75|TAG_499",
    # oda olanaklari
    "ozel-banyo":        "77|92",
    "ozel-tuvalet":      "77|445",
    "klima":             "77|107",
    "kuvet":             "77|91",
    "mutfak":            "77|198",
    "camasir":           "77|207",
    "sigarasiz":         "77|NoSmoking",
    "balkon":            "77|247",
    "buzdolabi":         "77|87",
    "su-isitici":        "77|80",
    "tv":                "77|183",
    "erisilebilir-oda":  "77|630",
    # tesis olanaklari
    "havuz":             "3|605",
    "otopark":           "3|656",
    "spa":               "3|65",
    # ogun
    "kahvalti":          "5|1",
    "aksam-yemegi":      "86|1",
    "yarim-pansiyon":    "146|1",
    "her-sey-dahil":     "146|4",
    # oda ozellikleri
    "aile-odasi":        "81|1188",
    "suit":              "81|1309",
    "tum-unite":         "78|1",
}

YILDIZ   = {5: "16|5", 4: "16|4", 3: "16|3", 2: "16|2"}
PUAN     = {9: "6|10", 8: "6|9", 7: "6|8", 6: "6|7"}
YORUM    = {500: "25|7", 200: "25|6", 100: "25|5"}
YATAK    = {"cift": "4|1", "iki-yatak": "4|2", "tek": "4|4", "king": "4|3"}

SIRALAMA = {
    "onerilen": "17|1",
    "yurume":   "17|12",   # yurume/surus mesafesi, once en yakin
    "kus":      "17|5",    # kus ucusu mesafe
    "puan":     "17|6",
    "ucuz":     "17|3",
    "pahali":   "17|4",
    "yildiz":   "17|14",
}


def token(filter_id: str) -> str:
    """'type|value' -> 'type~value*type*value' (TAG_ oneki ilk yarida korunur)."""
    parcalar = filter_id.split("|")
    tip = parcalar[0]
    kuyruk = "~".join(parcalar[1:])
    deger = "~".join(p[4:] if p.startswith("TAG_") else p for p in parcalar[1:])
    return "%s~%s*%s*%s" % (tip, kuyruk, tip, deger)


def poi_token(spec: str) -> str:
    """'lat,lon,ad,poiId' -> landmark capasi token'i (tip 50)."""
    alanlar = [p.strip() for p in spec.split(",")]
    if len(alanlar) != 4:
        sys.exit("--poi bicimi: 'lat,lon,ad,poiId' "
                 "(orn: '51.5194133,-0.1269566,The British Museum,6789940')")
    lat, lon, ad, poi_id = alanlar
    return "50~50~%s*50*%s~%s~%s~%s~1" % (poi_id, lat, lon, quote(ad), poi_id)


def bolge_token(spec: str) -> str:
    """'zoneId,lat,lon' -> bolge (zone) capasi token'i.

    DIKKAT: POI'den farkli. Ikinci segment grup numarasi (50) DEGIL, alt tip (8).
    Dogru:  50~8~10788*8*10788~51.5073~-0.1641~1
    Yanlis: 50~8~10788*50*10788~...   -> filtre cipi gorunur ama sonuclar alakasiz gelir.
    """
    alanlar = [p.strip() for p in spec.split(",")]
    if len(alanlar) != 3:
        sys.exit("--bolge bicimi: 'zoneId,lat,lon' "
                 "(orn: '10788,51.50736329950768,-0.1641134586554857')")
    zid, lat, lon = alanlar
    return "50~8~%s*8*%s~%s~%s~1" % (zid, zid, lat, lon)


def fiyat_token(min_f: int, max_f: int) -> str:
    return "15~Range*15*%d~%d" % (min_f, max_f)


def tarih_dogrula(s: str, ad: str) -> str:
    try:
        dt.date.fromisoformat(s)
    except ValueError:
        sys.exit("--%s YYYY-MM-DD biciminde olmali (verilen: %s)" % (ad, s))
    return s


def main() -> None:
    ap = argparse.ArgumentParser(description="Trip.com filtreli arama URL'i uret")
    ap.add_argument("--city", required=True, help="cityId (Londra 338, Istanbul 532...)")
    ap.add_argument("--city-name", default="", help="kozmetik sehir adi")
    ap.add_argument("--checkin", required=True, help="YYYY-MM-DD")
    ap.add_argument("--checkout", required=True, help="YYYY-MM-DD")
    ap.add_argument("--adults", type=int, default=2, help="toplam yetiskin (varsayilan 2)")
    ap.add_argument("--children", type=int, default=0)
    ap.add_argument("--ages", default="", help="cocuk yaslari, virgullu: 8,12")
    ap.add_argument("--rooms", type=int, default=1)
    ap.add_argument("--curr", default="TRY")
    ap.add_argument("--locale", default="tr-TR")
    ap.add_argument("--domain", default="", help="tr.trip.com | www.trip.com (bos: locale'den secilir)")
    ap.add_argument("--tip", action="append", default=[],
                    help="tesis tipi takma adi (hotel, apart, hostel...); birden fazla verilebilir")
    ap.add_argument("--filtre", action="append", default=[],
                    help="serbest filtre takma adi; birden fazla verilebilir")
    ap.add_argument("--yildiz", action="append", type=int, default=[], choices=[2, 3, 4, 5])
    ap.add_argument("--puan", type=int, choices=[6, 7, 8, 9], help="asgari misafir puani")
    ap.add_argument("--yorum", type=int, choices=[100, 200, 500], help="asgari yorum sayisi")
    ap.add_argument("--yatak", choices=sorted(YATAK))
    ap.add_argument("--poi", help="landmark (POI) capasi: 'lat,lon,ad,poiId'")
    ap.add_argument("--bolge", help="bolge/semt capasi: 'zoneId,lat,lon'. "
                                    "POI degil semt ise bunu kullan (bkz. mesafe-ve-konum.md §6)")
    ap.add_argument("--fiyat-min", type=int, help="gecelik, --curr biriminde")
    ap.add_argument("--fiyat-max", type=int, help="gecelik, --curr biriminde")
    ap.add_argument("--sirala", choices=sorted(SIRALAMA), default=None)
    ap.add_argument("--ham", action="append", default=[],
                    help="sozlukte olmayan filterID, 'type|value' biciminde")

    # sik kullanilanlar icin kisayol bayraklari
    for kisayol in ("ucretsiz-iptal", "ozel-banyo", "ozel-tuvalet", "kahvalti",
                    "otelde-odeme", "kartsiz", "sigarasiz", "klima"):
        ap.add_argument("--" + kisayol, action="store_true")

    a = ap.parse_args()

    tarih_dogrula(a.checkin, "checkin")
    tarih_dogrula(a.checkout, "checkout")
    if a.checkout <= a.checkin:
        sys.exit("--checkout, --checkin'den sonra olmali")
    geceler = (dt.date.fromisoformat(a.checkout) - dt.date.fromisoformat(a.checkin)).days

    ids = []

    # siralama: poi verildiyse ve siralama secilmediyse yurume mesafesi mantikli varsayilan
    sirala = a.sirala or ("yurume" if (a.poi or a.bolge) else None)
    if sirala:
        ids.append(SIRALAMA[sirala])

    for ad in a.tip + a.filtre:
        if ad not in FILTRELER:
            sys.exit("bilinmeyen filtre: %s\nmevcutlar: %s"
                     % (ad, ", ".join(sorted(FILTRELER))))
        ids.append(FILTRELER[ad])

    for kisayol in ("ucretsiz_iptal", "ozel_banyo", "ozel_tuvalet", "kahvalti",
                    "otelde_odeme", "kartsiz", "sigarasiz", "klima"):
        if getattr(a, kisayol, False):
            ids.append(FILTRELER[kisayol.replace("_", "-")])

    for y in a.yildiz:
        ids.append(YILDIZ[y])
    if a.puan:
        ids.append(PUAN[a.puan])
    if a.yorum:
        ids.append(YORUM[a.yorum])
    if a.yatak:
        ids.append(YATAK[a.yatak])
    ids.extend(a.ham)

    # tekrarlari sirayi bozmadan at
    gorulen, tekil = set(), []
    for i in ids:
        if i not in gorulen:
            gorulen.add(i)
            tekil.append(i)

    tokenlar = [token(i) for i in tekil]
    if a.poi and a.bolge:
        sys.exit("--poi ve --bolge birlikte kullanilamaz: Trip.com ayni anda tek konum capasi kabul eder")
    if a.poi:
        tokenlar.append(poi_token(a.poi))
    if a.bolge:
        tokenlar.append(bolge_token(a.bolge))
    if a.fiyat_min is not None or a.fiyat_max is not None:
        tokenlar.append(fiyat_token(a.fiyat_min or 0, a.fiyat_max or 999999))

    domain = a.domain or ("tr.trip.com" if a.locale.startswith("tr") else "www.trip.com")

    q = [
        ("cityId", a.city),
        ("cityName", a.city_name or ""),
        ("searchType", "CT"),
        ("checkin", a.checkin),
        ("checkout", a.checkout),
        ("crn", str(a.rooms)),
        ("adult", str(a.adults)),
        ("children", str(a.children)),
    ]
    if a.ages:
        q.append(("ages", a.ages))
    q += [("curr", a.curr), ("locale", a.locale)]

    # listFilters'i quote ETME: virgul, tilde ve yildiz ham kalmali
    qs = "&".join("%s=%s" % (k, quote(str(v), safe="")) for k, v in q if v != "")
    if tokenlar:
        qs += "&listFilters=" + ",".join(tokenlar)

    url = "https://%s/hotels/list?%s" % (domain, qs)

    print(url)
    print(file=sys.stderr)
    print("geceler      : %d (%s -> %s)" % (geceler, a.checkin, a.checkout), file=sys.stderr)
    print("misafir      : %d oda, %d yetiskin, %d cocuk" % (a.rooms, a.adults, a.children),
          file=sys.stderr)
    print("filtreler    : %s" % (", ".join(tekil) or "yok"), file=sys.stderr)
    if a.poi:
        print("landmark     : %s (POI)" % a.poi, file=sys.stderr)
    if a.bolge:
        print("bolge        : %s (semt uyeligi filtresi, yaricap DEGIL)" % a.bolge, file=sys.stderr)
    print("siralama     : %s" % (sirala or "Trip.com onerisi"), file=sys.stderr)
    print(file=sys.stderr)
    print("Sayfayi actiginda filtre ciplerini dogrula: her kisit cip olarak gorunmeli.",
          file=sys.stderr)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
app_store_cek.py — Bir uygulamanin App Store ve Google Play verisini tek komutta ceker.

Sadece standart kutuphane kullanir (urllib), ek paket gerektirmez.

Kullanim:
    python3 app_store_cek.py --ios-id 6633421265 --play-id com.uniboomtr.app --ulke tr
    python3 app_store_cek.py --ios-ara "uniboom" --ulke tr
    python3 app_store_cek.py --ios-id 6633421265 --yorum-sayfa 3 --cikti veri/uniboom.json

Ciktilar JSON olarak stdout'a basilir; --cikti verilirse dosyaya da yazilir.

Play Store'un resmi API'si yoktur; HTML kaziyoruz ve Google sayfa yapisini degistirdiginde
bu kisim bozulabilir. Bozulursa script bunu acikca "play_hata" alaninda soyler --
o durumda tarayiciyla sayfayi acip metnini okumak dogru yoldur, tahmin uretmek degil.
"""

import argparse
import json
import re
import sys
import urllib.request
import urllib.parse
import urllib.error

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0 Safari/537.36")


def _getir(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


# ----------------------------------------------------------------------------- iOS
def ios_lookup(app_id, ulke="tr"):
    url = f"https://itunes.apple.com/lookup?id={app_id}&country={ulke}"
    try:
        veri = json.loads(_getir(url))
    except Exception as e:
        return {"hata": f"iOS lookup basarisiz: {e}"}
    if not veri.get("results"):
        return {"hata": f"iOS id {app_id} icin {ulke} magazasinda sonuc yok"}
    a = veri["results"][0]
    surum_sayisi = None
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)", str(a.get("version", "")))
    if m:
        surum_sayisi = int(m.group(3))  # yama numarasi kaba bir surum sayaci verir
    return {
        "kaynak": url,
        "ad": a.get("trackName"),
        "tuzel_saglayici": a.get("sellerName"),
        "gelistirici": a.get("artistName"),
        "kategori": a.get("primaryGenreName"),
        "kategoriler": a.get("genres"),
        "puan_ortalama": a.get("averageUserRating"),
        "puan_sayisi": a.get("userRatingCount"),
        "puan_ortalama_bu_surum": a.get("averageUserRatingForCurrentVersion"),
        "puan_sayisi_bu_surum": a.get("userRatingCountForCurrentVersion"),
        "fiyat": a.get("formattedPrice"),
        "ilk_yayin": a.get("releaseDate"),
        "surum": a.get("version"),
        "surum_yayin": a.get("currentVersionReleaseDate"),
        "tahmini_yama_sayisi": surum_sayisi,
        "boyut_mb": round(int(a.get("fileSizeBytes", 0)) / 1048576, 1) if a.get("fileSizeBytes") else None,
        "min_os": a.get("minimumOsVersion"),
        "diller": a.get("languageCodesISO2A"),
        "yas_siniri": a.get("contentAdvisoryRating"),
        "destek_url": a.get("sellerUrl"),
        "aciklama": (a.get("description") or "")[:1500],
        "surum_notu": (a.get("releaseNotes") or "")[:800],
        "ekran_goruntusu_sayisi": len(a.get("screenshotUrls") or []),
        "store_url": a.get("trackViewUrl"),
    }


def ios_ara(terim, ulke="tr", limit=8):
    url = ("https://itunes.apple.com/search?term=" + urllib.parse.quote(terim) +
           f"&country={ulke}&entity=software&limit={limit}")
    try:
        veri = json.loads(_getir(url))
    except Exception as e:
        return {"hata": f"iOS arama basarisiz: {e}"}
    return [{"id": r.get("trackId"), "ad": r.get("trackName"),
             "saglayici": r.get("sellerName"), "puan": r.get("averageUserRating"),
             "puan_sayisi": r.get("userRatingCount"), "url": r.get("trackViewUrl")}
            for r in veri.get("results", [])]


def ios_yorumlar(app_id, ulke="tr", sayfa=2):
    """RSS uzerinden tarihli, puanli, tam metinli yorumlar."""
    cikti = []
    for p in range(1, sayfa + 1):
        url = (f"https://itunes.apple.com/{ulke}/rss/customerreviews/page={p}/"
               f"id={app_id}/sortby=mostrecent/json")
        try:
            veri = json.loads(_getir(url))
        except Exception:
            break
        girdiler = veri.get("feed", {}).get("entry", [])
        if isinstance(girdiler, dict):
            girdiler = [girdiler]
        for e in girdiler:
            if "im:rating" not in e:
                continue  # ilk girdi uygulamanin kendisi
            cikti.append({
                "yazar": e.get("author", {}).get("name", {}).get("label"),
                "puan": int(e["im:rating"]["label"]),
                "baslik": e.get("title", {}).get("label"),
                "metin": e.get("content", {}).get("label", "")[:600],
                "surum": e.get("im:version", {}).get("label"),
                "tarih": e.get("updated", {}).get("label"),
            })
        if not girdiler:
            break
    return cikti


# ------------------------------------------------------------------------- Play
_PLAY_DESENLERI = {
    "indirme": [r'>([\d.,]+\s*[KMBTB]?\+)</div><div[^>]*>(?:Downloads|İndirme)',
                r'\[\[\["([\d.,]+[KMB]?\+)"\]\],\[\[',
                r'"([\d.,]+[KMB]?\+)"\s*,\s*"(?:Downloads|İndirme)"'],
    "puan": [r'>([\d.,]+)</div><div[^>]*aria-label="Ortalama[^"]*"',
             r'\[\[\[([\d.]+),\[\[',
             r'"ratingValue"\s*:\s*"?([\d.,]+)"?'],
    "yorum": [r'([\d.,]+[KMB]?)\s*(?:reviews|yorum)',
              r'"reviewCount"\s*:\s*"?([\d.,]+)"?'],
    "guncelleme": [r'(?:Updated on|Güncellenme tarihi)</div><div[^>]*>([^<]+)<',
                   r'"datePublished"\s*:\s*"([^"]+)"'],
    "gelistirici": [r'href="/store/apps/dev(?:eloper)?\?id=[^"]*"[^>]*>(?:<[^>]+>)*([^<]{2,60})<'],
}


def play_cek(paket, ulke="tr", dil="tr"):
    url = f"https://play.google.com/store/apps/details?id={paket}&hl={dil}&gl={ulke.upper()}"
    try:
        html = _getir(url)
    except urllib.error.HTTPError as e:
        return {"kaynak": url, "play_hata": f"HTTP {e.code} — paket adi yanlis olabilir"}
    except Exception as e:
        return {"kaynak": url, "play_hata": str(e)}

    sonuc = {"kaynak": url, "paket": paket}
    for alan, desenler in _PLAY_DESENLERI.items():
        for d in desenler:
            m = re.search(d, html)
            if m:
                sonuc[alan] = m.group(1).strip()
                break
        else:
            sonuc[alan] = None

    if sonuc.get("puan"):
        try:
            sonuc["puan"] = round(float(sonuc["puan"].replace(",", ".")), 2)
        except ValueError:
            pass

    eksik = [k for k, v in sonuc.items() if v is None and k not in ("kaynak", "paket")]
    if eksik:
        sonuc["play_hata"] = ("Su alanlar HTML'den cikarilamadi: " + ", ".join(eksik) +
                              ". Google sayfa yapisini degistirmis olabilir — sayfayi "
                              "tarayiciyla acip metnini oku, tahmin uretme.")
    return sonuc


# --------------------------------------------------------------------- Turetme
def indirme_bandi(play_indirme):
    """Play bandini ('1 B+', '50K+') alt/ust/orta noktaya cevirir."""
    if not play_indirme:
        return None
    s = play_indirme.upper().replace(" ", "").replace("+", "").replace(",", "").replace(".", "")
    carpan = 1
    if s.endswith("B") and "MILY" not in s:      # TR'de "B" = bin
        carpan, s = 1_000, s[:-1]
    elif s.endswith("K"):
        carpan, s = 1_000, s[:-1]
    elif s.endswith("M"):
        carpan, s = 1_000_000, s[:-1]
    try:
        alt = int(s) * carpan
    except ValueError:
        return None
    ust = alt * 5 if str(alt).startswith("1") else alt * 2
    return {"alt": alt, "ust": ust, "orta_muhafazakar": int(alt * 1.6)}


def ios_indirme_tahmini(puan_sayisi):
    """iOS puan sayisindan indirme turetir. Puanlama orani %0.5-2 kabul edilir."""
    if not puan_sayisi:
        return None
    return {"alt": int(puan_sayisi / 0.02), "ust": int(puan_sayisi / 0.005),
            "orta": int(puan_sayisi / 0.01),
            "not": "Puanlama orani %0.5-2 varsayimi. [T] etiketiyle raporlanmali."}


def main():
    p = argparse.ArgumentParser(description="App Store + Google Play veri toplayici")
    p.add_argument("--ios-id")
    p.add_argument("--ios-ara")
    p.add_argument("--play-id")
    p.add_argument("--ulke", default="tr")
    p.add_argument("--yorum-sayfa", type=int, default=2)
    p.add_argument("--cikti")
    a = p.parse_args()

    if not (a.ios_id or a.ios_ara or a.play_id):
        p.error("En az bir kaynak ver: --ios-id, --ios-ara veya --play-id")

    sonuc = {}
    if a.ios_ara:
        sonuc["ios_arama"] = ios_ara(a.ios_ara, a.ulke)
    if a.ios_id:
        sonuc["ios"] = ios_lookup(a.ios_id, a.ulke)
        sonuc["ios_yorumlar"] = ios_yorumlar(a.ios_id, a.ulke, a.yorum_sayfa)
        if isinstance(sonuc["ios"], dict):
            sonuc["ios_indirme_tahmini"] = ios_indirme_tahmini(sonuc["ios"].get("puan_sayisi"))
    if a.play_id:
        sonuc["play"] = play_cek(a.play_id, a.ulke)
        sonuc["play_indirme_bandi"] = indirme_bandi(sonuc["play"].get("indirme"))

    metin = json.dumps(sonuc, ensure_ascii=False, indent=2)
    print(metin)
    if a.cikti:
        with open(a.cikti, "w", encoding="utf-8") as f:
            f.write(metin)
        print(f"\n[kaydedildi] {a.cikti}", file=sys.stderr)


if __name__ == "__main__":
    main()

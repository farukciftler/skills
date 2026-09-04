#!/usr/bin/env python3
"""Yazıyı yayına vermeden önce tarar.

Kullanım:
    python3 denetle.py yazi.md
    python3 denetle.py yazi.md --dil en

Çıktı bir puan değil, düzeltilecek satırların listesidir. Betiğin temiz çıkması metnin iyi
olduğu anlamına gelmez; yalnızca bilinen imzaların kalmadığı anlamına gelir. Son adım hâlâ
metni sesli okumaktır.

Bulgular üç seviyede: DUR (yayına engel), BAK (gözden geçir), NOT (bilgi).
"""

import argparse
import re
import statistics
import sys
from pathlib import Path

# ------------------------------------------------------------------ listeler

# Kaynak: references/yapay-zeka-imzalari.md, Tier 1
YASAK_EN = [
    "delve", "delves", "delving", "tapestry", "testament to", "camaraderie",
    "palpable", "intricate", "intricacies", "underscore", "underscores",
    "showcase", "showcasing", "pivotal", "realm", "navigate the", "meticulous",
    "meticulously", "embark", "unlock the", "elevate your", "seamless",
    "seamlessly", "robust", "leverage", "leveraging", "harness the", "foster",
    "fostering", "amidst", "cacophony", "solace", "unspoken", "fleeting",
    "unravel", "grapple", "myriad", "plethora", "paradigm shift", "synergy",
    "holistic", "multifaceted", "nuanced", "transformative", "game-changer",
    "cutting-edge", "state-of-the-art", "ever-evolving", "ever-changing",
]

# Kaynak: references/yapay-zeka-imzalari.md, Tier 2
KALIP_EN = [
    "it's important to note", "it is important to note", "it's worth noting",
    "in today's fast-paced", "in today's digital", "in an era of", "in the age of",
    "in conclusion", "to sum up", "in summary", "at the end of the day",
    "let's dive", "let's explore", "buckle up", "here's the thing",
    "the bottom line is", "when it comes to", "whether you're a",
    "not only", "as we've seen", "as mentioned earlier", "it goes without saying",
    "needless to say", "that being said", "with that in mind",
    "in this article", "by the end of this article", "stay tuned",
    "imagine a world where", "picture this", "what if i told you",
]

GECIS_EN = [
    "moreover", "furthermore", "additionally", "nevertheless", "nonetheless",
    "consequently", "subsequently", "notably", "importantly", "interestingly",
    "conversely", "likewise", "firstly", "secondly", "thirdly", "lastly",
]

# Kaynak: references/turkce-yazim.md, bölüm 4.2
KALIP_TR = [
    "bu bağlamda", "unutulmamalıdır ki", "önemli bir rol oynamaktadır",
    "önemli bir rol oynuyor", "sonuç olarak", "günümüzde", "hızla gelişen",
    "dikkat çekmektedir", "ön plana çıkmaktadır", "ön plana çıkıyor",
    "kaliteli ve güvenilir", "geniş bir yelpazede", "ihtiyaçlarınıza yönelik",
    "çözümler sunmaktadır", "büyük önem taşımaktadır", "büyük önem taşıyor",
    "göz ardı edilmemelidir", "bilinmektedir ki", "şüphesiz ki",
    "bu makalede", "bu yazıda", "hadi başlayalım", "gelin birlikte",
    "sizin için derledik", "hakkında konuşalım", "ele alacağız",
    "değinmek gerekir", "belirtmek gerekir", "ifade edilebilir",
    "son yıllarda giderek", "her geçen gün", "dünyasında",
]

GECIS_TR = [
    "ayrıca", "bununla birlikte", "dolayısıyla", "bu nedenle", "böylelikle",
    "öte yandan", "diğer taraftan", "kısacası", "özetle", "nitekim",
    "ilk olarak", "ikinci olarak", "son olarak",
]

SESLI = set("aeıioöuüAEIİOÖUÜ")


# ------------------------------------------------------------------ hazırlık

def metni_temizle(ham: str) -> str:
    """Frontmatter, kod bloğu, URL ve markdown işaretlerini çıkarır."""
    m = re.sub(r"^---\n.*?\n---\n", "", ham, flags=re.S)
    m = re.sub(r"```.*?```", " ", m, flags=re.S)
    m = re.sub(r"`[^`]*`", " ", m)
    m = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", m)   # bağlantı metnini bırak
    m = re.sub(r"https?://\S+", " ", m)
    m = re.sub(r"^\s*[|>#*\-+]\s*", "", m, flags=re.M)
    return m


def cumleler(metin: str) -> list:
    parca = re.split(r"(?<=[.!?…])\s+", metin)
    return [c.strip() for c in parca if len(c.split()) >= 2]


def hece_say(kelime: str) -> int:
    """Türkçede hece sayısı sesli harf sayısına eşittir."""
    return sum(1 for h in kelime if h in SESLI)


def atesman(metin: str) -> float:
    """Ateşman (1997) okunabilirlik puanı. 60-75 bandı hedef."""
    c = cumleler(metin)
    k = re.findall(r"[A-Za-zÇĞİÖŞÜçğıöşü]+", metin)
    if not c or not k:
        return 0.0
    hece_ort = sum(hece_say(x) for x in k) / len(k)
    kelime_ort = len(k) / len(c)
    return 198.825 - 40.175 * hece_ort - 2.610 * kelime_ort


# ------------------------------------------------------------------ denetimler

def satir_ara(satirlar: list, kaliplar: list) -> list:
    """Kalıpları satır satır arar, (satır no, kalıp, satır metni) döner."""
    bulgu = []
    for no, satir in enumerate(satirlar, 1):
        kucuk = satir.lower()
        for k in kaliplar:
            if k in kucuk:
                bulgu.append((no, k, satir.strip()[:90]))
    return bulgu


def denetle(yol: Path, dil: str) -> int:
    ham = yol.read_text(encoding="utf-8")
    satirlar = ham.split("\n")
    metin = metni_temizle(ham)
    kelimeler = metin.split()
    cum = cumleler(metin)

    dur, bak, not_ = [], [], []

    # 1. Uzun çizgi
    em = [(no, s.strip()[:90]) for no, s in enumerate(satirlar, 1) if "—" in s]
    if em:
        sayi = sum(s.count("—") for s in satirlar)
        oran = sayi / max(1, len(kelimeler) / 1000)
        seviye = dur if (dil == "tr" or oran > 2) else bak
        seviye.append(
            f"Uzun çizgi ( — ) {sayi} kez geçiyor (1000 kelimede {oran:.1f}). "
            + ("Türkçede uzun çizgi yalnız konuşma çizgisidir." if dil == "tr"
               else "Hedef: 1000 kelimede en fazla 2.")
        )
        for no, s in em[:8]:
            seviye.append(f"    satır {no}: {s}")

    # 2. Yasak kelimeler ve kalıplar
    yasak = YASAK_EN if dil == "en" else []
    kalip = (KALIP_EN if dil == "en" else KALIP_TR)
    gecis = (GECIS_EN if dil == "en" else GECIS_TR)

    for no, k, s in satir_ara(satirlar, yasak):
        dur.append(f"Yasak kelime '{k}' — satır {no}: {s}")
    for no, k, s in satir_ara(satirlar, kalip):
        dur.append(f"Kalıp ifade '{k}' — satır {no}: {s}")

    g = satir_ara(satirlar, gecis)
    if g:
        bin_basi = len(g) / max(1, len(kelimeler) / 1000)
        seviye = dur if bin_basi > 3 else bak
        seviye.append(f"Geçiş ifadesi {len(g)} kez (1000 kelimede {bin_basi:.1f}). Hedef: 3'ten az.")
        for no, k, s in g[:8]:
            seviye.append(f"    satır {no}: '{k}' — {s}")

    # 3. Türkçeye özel ekler
    if dil == "tr":
        mektedir = len(re.findall(r"\w+m(?:ak|ek)tadır\b", metin, re.I))
        if mektedir:
            dur.append(f"'-mektedir/-maktadır' eki {mektedir} kez. Sıfırlanmalı, şimdiki zaman kullan.")
        not_.append("Bağlaç olan de/da ve ki ayrı mı yazılmış, elle kontrol et (betik ayırt edemiyor).")

    # 4. Cümle uzunluğu dağılımı
    uzunluk = [len(c.split()) for c in cum]
    if len(uzunluk) >= 5:
        ort = statistics.mean(uzunluk)
        ss  = statistics.pstdev(uzunluk)
        # Ham sapma yerine değişim katsayısı (sapma / ortalama) kullanıyoruz.
        # Türkçe düzyazıda ortalama cümle 8-12 kelime olabiliyor; orada 6'lık bir
        # sapma zaten çok değişken demek, ama ham eşik bunu yanlış yakalıyordu.
        dk = ss / ort if ort else 0
        satir = (f"Cümle uzunluğu: ortalama {ort:.1f}, en kısa {min(uzunluk)}, "
                 f"en uzun {max(uzunluk)}, sapma {ss:.1f}, değişim katsayısı {dk:.2f}.")
        if dk < 0.45:
            dur.append(satir + " Değişim katsayısı 0,45'in altında, metin düz okunuyor. "
                               "Kısa cümle ekle, uzunları böl.")
        elif dk < 0.55:
            bak.append(satir + " Değişim katsayısı sınırda.")
        else:
            not_.append(satir)
        if min(uzunluk) > 5:
            bak.append(f"En kısa cümle {min(uzunluk)} kelime. 5 kelimeden kısa en az bir cümle olsun.")
        if max(uzunluk) < 30:
            bak.append(f"En uzun cümle {max(uzunluk)} kelime. 30 kelimeden uzun en az bir cümle olsun.")

    # 5. Somutluk
    sayilar = re.findall(r"(?<![\w/])\d[\d.,]*(?![\w/])", metin)
    if kelimeler:
        yogunluk = len(sayilar) / (len(kelimeler) / 500)
        satir = f"Somut sayı: {len(sayilar)} adet (500 kelimede {yogunluk:.1f})."
        if yogunluk >= 3:
            not_.append(satir)
        elif len(kelimeler) < 300:
            # Kısa metinde yoğunluk ölçümü gürültülü, engel saymıyoruz.
            bak.append(satir + " Hedef en az 3, ama metin kısa olduğu için ölçüm oynak.")
        else:
            dur.append(satir + " Hedef en az 3. Metin somut bir şey söylemiyor olabilir.")

    ozel = set(re.findall(r"(?<![.!?]\s)(?<!^)\b[A-ZÇĞİÖŞÜ][a-zçğıöşü]{2,}\b", metin, re.M))
    if len(ozel) < 3:
        bak.append(f"Özel isim sayısı düşük ({len(ozel)}). Kişi, kurum, yer, marka adı geçiyor mu?")

    # 6. Üçlü paralel liste
    uclu = re.findall(r"\b[\wçğıöşüÇĞİÖŞÜ]+,\s+[\wçğıöşüÇĞİÖŞÜ]+\s+(?:ve|and)\s+[\wçğıöşüÇĞİÖŞÜ]+\b", metin)
    if len(uclu) > 1:
        bak.append(f"Üçlü paralel liste {len(uclu)} kez. En fazla 1 olmalı. Örnek: {uclu[0][:60]}")

    # 7. Kalıp cümle yapıları
    for desen, ad in [
        (r"(?:sadece|yalnız(?:ca)?)\s+(?:\w+\s+){1,4}değil,?\s+\w", "'sadece X değil, Y' kalıbı"),
        (r"\b(?:it'?s|they'?re|that'?s)?\s*(?:is|are)?n'?t just\b", "'X isn't just Y' kalıbı"),
        (r"\bisn'?t about\b.{0,40}\bit'?s about\b", "'X isn't about A, it's about B' kalıbı"),
    ]:
        for no, satir in enumerate(satirlar, 1):
            if re.search(desen, satir, re.I):
                dur.append(f"{ad} — satır {no}: {satir.strip()[:90]}")

    # 8. Okunabilirlik (yalnız Türkçe)
    if dil == "tr" and cum:
        puan = atesman(metin)
        satir = f"Ateşman okunabilirlik puanı: {puan:.1f}. Hedef bant 60-75."
        if puan < 55:
            dur.append(satir + " Metin zor. Cümleleri kısalt, uzun kelimeleri sadeleştir.")
        elif puan < 60 or puan > 80:
            bak.append(satir)
        else:
            not_.append(satir)

    # 9. Meta veriler
    if len(kelimeler) < 300:
        not_.append(f"Metin {len(kelimeler)} kelime. Kısa metin sorun değil, hedefe uyduğundan emin ol.")
    else:
        not_.append(f"Metin {len(kelimeler)} kelime, {len(cum)} cümle.")

    # ------------------------------------------------------------ rapor
    print(f"\n\033[1m{yol.name}\033[0m  (dil: {dil})")
    print("=" * 72)

    for baslik, liste, renk in [
        ("DUR", dur, "\033[31m"), ("BAK", bak, "\033[33m"), ("NOT", not_, "\033[2m")
    ]:
        if not liste:
            continue
        print(f"\n{renk}{baslik}\033[0m")
        for s in liste:
            print(f"  {s}" if s.startswith("    ") else f"  · {s}")

    print()
    if dur:
        print(f"\033[31m{len(dur)} engel var, metin yayına hazır değil.\033[0m")
        return 1
    if bak:
        print(f"\033[33m{len(bak)} nokta gözden geçirilmeli. Engel yok.\033[0m")
        return 0
    print("\033[32mBilinen imza bulunamadı. Şimdi metni sesli oku.\033[0m")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Yazıyı yayın öncesi tarar.")
    ap.add_argument("dosya", type=Path, nargs="+")
    ap.add_argument("--dil", choices=["tr", "en"], default="tr")
    a = ap.parse_args()

    cikis = 0
    for yol in a.dosya:
        if not yol.exists():
            print(f"Dosya yok: {yol}", file=sys.stderr)
            cikis = 1
            continue
        cikis |= denetle(yol, a.dil)
    return cikis


if __name__ == "__main__":
    sys.exit(main())

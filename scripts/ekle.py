#!/usr/bin/env python3
"""Bu makinedeki skill'leri mevcut kütüphaneye *ekler* — hiçbir şey silmez.

`topla.py` tek bir makinenin tam taramasını varsayar: manifest'i sıfırdan yazar,
dolayısıyla başka bir bilgisayarda toplanmış girdileri kataloğun dışında bırakır.
Kütüphane birden çok makineden besleniyorsa bunun yerine bu script kullanılır.

Çalışma biçimi — `kutuphane/` içeriği doğruluk kaynağıdır:

  * kaynağın içerik özeti kütüphanede zaten varsa yalnızca yolu manifest'e işler;
  * kütüphanedeki kopyanın gerçek üst kümesiyse (aynı dosyalar + fazlası) o
    girdiyi yerinde tazeler;
  * geri kalan her ayrışmış içerik `<ad>--<etiket>` yeni girdisi olur.

Kullanım:
    python3 scripts/ekle.py            # kuru çalıştırma, planı basar
    python3 scripts/ekle.py --uygula   # kopyalar ve manifest'i günceller
"""
import filecmp
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import topla

KOK = topla.KOK
EV = topla.EV
KUTUPHANE = topla.KUTUPHANE
MANIFEST = os.path.join(topla.KATALOG, "manifest.json")

# Bilinçli olarak atlananlar: yalnızca frontmatter sarımı/son satır sonu ayrışmış,
# içerikçe özdeş kopyalar. Yeni bir girdi açmaları gürültüden ibaret olur.
ATLA = {
    "~/Documents/GitHub/pipsworn/.claude/skills/chibi-character-factory",
    # 9 Ağustos claude.ai anlık görüntüsünde kalmış, kütüphanedeki kopya ileride
    # olan ikisi (ikisi de yalnız bu eski görüntüde duruyor, `en_yeni_cloud`
    # elemesine takılmıyorlar). Elle doğrulandı:
    #   ucuz-bilet-avcisi   cloud'da `from __future__ import annotations` yok
    #   ambient-video-forge cloud'da macOS `sysctl` ve ffmpeg 8.x filtre düzeltmeleri yok
    "~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/2fee50bc-c9a6-43ff-972a-052c82ab1426/f181d07d-d5e3-4bcf-8416-620881ba96e8/skills/ucuz-bilet-avcisi",
    "~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/2fee50bc-c9a6-43ff-972a-052c82ab1426/f181d07d-d5e3-4bcf-8416-620881ba96e8/skills/ambient-video-forge",
}



def dosya_kumesi(dizin):
    """Dizindeki dosyaların dizine göreli yolları (gürültü dosyaları hariç)."""
    kume = set()
    for kok, dizinler, dosyalar in os.walk(dizin):
        dizinler[:] = [d for d in dizinler if d not in (".git", "__pycache__")]
        for dosya in dosyalar:
            if dosya == ".DS_Store":
                continue
            kume.add(os.path.relpath(os.path.join(kok, dosya), dizin))
    return kume


def kapsam(kaynak, hedef):
    """İki kopyadan biri diğerini aynen kapsıyor mu?

    "ust": kaynak, hedef'in her dosyasını aynen içerip üstüne dosya ekliyor —
    kütüphanedeki kopya tazelenmeli. "alt": tersi; kütüphanedeki zaten daha
    dolu, kaynak yeni girdi açmamalı. Ortak dosyalardan biri bile farklıysa
    None: bunlar gerçekten ayrışmış iki sürümdür.
    """
    kd, hd = dosya_kumesi(kaynak), dosya_kumesi(hedef)
    if kd == hd or not (kd < hd or hd < kd):
        return None
    ortak = kd & hd
    if not all(
        filecmp.cmp(os.path.join(kaynak, r), os.path.join(hedef, r), shallow=False)
        for r in ortak
    ):
        return None
    return "ust" if hd < kd else "alt"


def en_yeni_cloud(kayitlar):
    """Eski claude.ai anlık görüntülerinin gereksiz kopyalarını eler.

    Önbellekte birden çok oturum anlık görüntüsü durur ve aynı skill hepsinde
    bulunur. Bir ad en yeni görüntüde varsa eskilerdeki kopyası tanım gereği
    geride kalmıştır — ayrı girdi açması gürültüdür. Yalnız *sadece* eski bir
    görüntüde kalanlar (claude.ai'dan silinmiş skill'ler) aday olarak kalır.
    """
    sira = {yol: i for i, yol in enumerate(topla.cloud_dizinleri())}
    en_iyi = {}
    for kayit in kayitlar:
        if kayit["tur"] != "cloud":
            continue
        kok = os.path.dirname(kayit["dizin"].replace("~", EV, 1))
        en_iyi[kayit["ad"]] = min(en_iyi.get(kayit["ad"], 10**6), sira.get(kok, 10**6))
    elenen = set()
    for kayit in kayitlar:
        if kayit["tur"] != "cloud":
            continue
        kok = os.path.dirname(kayit["dizin"].replace("~", EV, 1))
        if sira.get(kok, 10**6) > en_iyi[kayit["ad"]]:
            elenen.add(kayit["dizin"])
    return elenen


def kutuphane_girdileri():
    """kutuphane/<kategori>/<slug> dizinlerini içerik özetiyle döndürür."""
    girdiler = {}
    for kategori in sorted(os.listdir(KUTUPHANE)):
        kat_yol = os.path.join(KUTUPHANE, kategori)
        if not os.path.isdir(kat_yol):
            continue
        for slug in sorted(os.listdir(kat_yol)):
            yol = os.path.join(kat_yol, slug)
            if os.path.isdir(yol):
                girdiler[(kategori, slug)] = yol
    return girdiler


def main():
    uygula = "--uygula" in sys.argv
    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    kayit_ile = {(m["cat"], m["slug"]): m for m in manifest}
    girdiler = kutuphane_girdileri()
    ozetler = {}
    for anahtar, yol in girdiler.items():
        ozetler.setdefault(topla.dizin_ozeti(yol), []).append(anahtar)
    sluglar = {slug for _, slug in girdiler}
    adlar = {m["name"] for m in manifest}

    ayni, tazele, ekle = [], [], []
    kayitlar = topla.bul()
    bayat_cloud = en_yeni_cloud(kayitlar)
    for kayit in kayitlar:
        if kayit["dizin"] in ATLA or kayit["dizin"] in bayat_cloud:
            continue
        eslesme = ozetler.get(kayit["ozet"])
        if eslesme:
            ayni.append((kayit, eslesme[0]))
            continue
        kaynak = kayit["dizin"].replace("~", EV, 1)
        kapsayan = [
            (anahtar, kapsam(kaynak, yol))
            for anahtar, yol in girdiler.items()
            if kayit_ile.get(anahtar, {}).get("name") == kayit["ad"]
        ]
        alt = next((a for a, y in kapsayan if y == "alt"), None)
        if alt:
            ayni.append((kayit, alt))
            continue
        ust = next((a for a, y in kapsayan if y == "ust"), None)
        if ust:
            tazele.append((kayit, ust))
            continue
        slug = kayit["ad"] if kayit["ad"] not in adlar else f"{kayit['ad']}--{topla.etiket(kayit)}"
        temel, sayac = slug, 1
        while slug in sluglar:
            sayac += 1
            slug = f"{temel}-{sayac}"
        sluglar.add(slug)
        ekle.append((kayit, (topla.KATEGORI_ESLEME.get(kayit["ad"], topla.DIGER), slug)))

    print(f"kütüphanede zaten var : {len(ayni)}")
    for kayit, (kat, slug) in tazele:
        print(f"TAZELE  {kat}/{slug:44} <- {kayit['dizin']}")
    for kayit, (kat, slug) in ekle:
        print(f"EKLE    {kat}/{slug:44} <- {kayit['dizin']}")
    siniflandirilmamis = sorted({s for _, (k, s) in ekle if k == topla.DIGER})
    if siniflandirilmamis:
        print(f"UYARI — kategorisiz: {siniflandirilmamis}")
    if not uygula:
        print("\n[kuru çalıştırma — hiçbir şey değişmedi; --uygula ile uygula]")
        return

    def yola_yaz(kayit, anahtar):
        """Manifest kaydına bu makinedeki kaynağı işler."""
        m = kayit_ile[anahtar]
        if kayit["dizin"] not in m["srcs"]:
            m["srcs"].append(kayit["dizin"])
            m["kinds"].append(kayit["tur"])
            hedef = "linked" if kayit["tur"] == "install" else "mirrored"
            m.setdefault(hedef, []).append(kayit["dizin"])

    for kayit, anahtar in ayni:
        if anahtar in kayit_ile:
            yola_yaz(kayit, anahtar)

    for kayit, anahtar in tazele:
        yol = girdiler[anahtar]
        shutil.rmtree(yol)
        shutil.copytree(
            kayit["dizin"].replace("~", EV, 1),
            yol,
            symlinks=False,
            ignore=shutil.ignore_patterns(".git", "__pycache__", ".DS_Store"),
        )
        m = kayit_ile[anahtar]
        m["hash"] = kayit["ozet"]
        m["bytes"] = kayit["bayt"]
        yola_yaz(kayit, anahtar)

    for kayit, (kat, slug) in ekle:
        hedef = os.path.join(KUTUPHANE, kat, slug)
        os.makedirs(os.path.dirname(hedef), exist_ok=True)
        shutil.copytree(
            kayit["dizin"].replace("~", EV, 1),
            hedef,
            symlinks=False,
            ignore=shutil.ignore_patterns(".git", "__pycache__", ".DS_Store"),
        )
        manifest.append(
            {
                "name": kayit["ad"],
                "slug": slug,
                "cat": kat,
                "hash": kayit["ozet"],
                "variant": 0 if slug == kayit["ad"] else 1,
                "srcs": [kayit["dizin"]],
                "kinds": [kayit["tur"]],
                "bytes": kayit["bayt"],
                "lib": hedef.replace(EV, "~"),
                "linked": [kayit["dizin"]] if kayit["tur"] == "install" else [],
                "mirrored": [] if kayit["tur"] == "install" else [kayit["dizin"]],
            }
        )

    manifest.sort(key=lambda m: (m["name"], m["slug"]))
    json.dump(
        manifest, open(MANIFEST, "w", encoding="utf-8"), ensure_ascii=False, indent=1
    )
    print(f"\n{len(tazele)} girdi tazelendi, {len(ekle)} girdi eklendi.")
    print("sıradaki: python3 scripts/katalog_uret.py")


if __name__ == "__main__":
    main()

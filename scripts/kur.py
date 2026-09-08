#!/usr/bin/env python3
"""Kütüphanedeki skill'leri terminale kurar (`~/.claude/skills/<ad>` → symlink).

`bagla.py` kurulum noktalarını kütüphaneye bağlar; bu script tersini yapar:
kütüphanedeki *her* girdiyi genel kurulum dizinine bağlayarak her projedeki
`claude` oturumunda yüklenir hale getirir. Hedef bir symlink'tir, kopya değil —
kütüphanede yapılan düzenleme anında kuruluma yansır.

Ad çakışması: `~/.claude/skills/<ad>` tek bir dizindir, ayrışmış sürümlerin
hepsi aynı anda kurulamaz. Ad başına tek kazanan seçilir:

  1. slug'ı adın kendisi olan (düz ad) — CLAUDE.md'ye göre daha yeni sürüm;
  2. yoksa `--cloud` ekli olmayan;
  3. yoksa en büyük içerik.

Kurulacak dizin adı, mümkünse SKILL.md frontmatter'ındaki `name` alanıdır —
Claude Code dizin adıyla frontmatter'ın uyuşmasını bekler.

Güvenlik kuralları:
  * Varsayılan kuru çalıştırmadır; `--uygula` demeden hiçbir şey değişmez.
  * Hedefte gerçek bir dizin varsa **yalnız kütüphanedeki kopyayla birebir
    aynıysa** symlink'e dönüştürülür; ayrışmışsa atlanır.
  * Her işlem `katalog/kurulum-kaydi.json`'a yazılır; `--coz` ile geri alınır.

Kullanım:
    python3 scripts/kur.py              # ne olacağını göster
    python3 scripts/kur.py --uygula     # kur
    python3 scripts/kur.py --coz        # geri almayı göster
    python3 scripts/kur.py --coz --uygula
"""
import argparse
import filecmp
import json
import os
import re
import shutil
import sys
from datetime import datetime

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EV = os.path.expanduser("~")
MANIFEST = os.path.join(KOK, "katalog", "manifest.json")
KAYIT = os.path.join(KOK, "katalog", "kurulum-kaydi.json")
KURULUM = os.path.join(EV, ".claude", "skills")
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def ayni_mi(a, b):
    """İki dizin ağacı birebir aynı mı? (bagla.py ile aynı ölçüt)"""
    kiyas = filecmp.dircmp(a, b, ignore=[".DS_Store", ".git", "__pycache__"])

    def gez(k):
        if k.left_only or k.right_only or k.funny_files:
            return False
        _, farkli, hata = filecmp.cmpfiles(k.left, k.right, k.common_files, shallow=False)
        if farkli or hata:
            return False
        return all(gez(alt) for alt in k.subdirs.values())

    return gez(kiyas)


def frontmatter_adi(yol):
    """SKILL.md'deki `name` alanı — geçerli bir slug değilse None."""
    skill = os.path.join(yol, "SKILL.md")
    if not os.path.exists(skill):
        return None
    with open(skill, encoding="utf-8", errors="replace") as f:
        bas = f.read(4000)
    blok = re.search(r"^---\s*\n(.*?)^---\s*$", bas, re.S | re.M)
    if not blok:
        return None
    ad = re.search(r"^name:\s*(.+?)\s*$", blok.group(1), re.M)
    if not ad:
        return None
    ad = ad.group(1).strip().strip("\"'")
    return ad if SLUG.match(ad) else None


def adaylar():
    """Her kurulum adı için (ad, kazanan girdi, elenen girdiler)."""
    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    gruplar = {}
    for girdi in manifest:
        yol = os.path.join(KOK, "kutuphane", girdi["cat"], girdi["slug"])
        girdi["_yol"] = yol
        girdi["_ad"] = frontmatter_adi(yol) or girdi["name"]
        gruplar.setdefault(girdi["_ad"], []).append(girdi)

    for ad, uyeler in sorted(gruplar.items()):
        sirali = sorted(
            uyeler,
            key=lambda g: (
                g["slug"] != ad,             # düz ad önce
                g["slug"].endswith("--cloud"),  # bayat bulut kopyası sonra
                -g["bytes"],                 # sonra en dolu
            ),
        )
        yield ad, sirali[0], sirali[1:]


def kur(uygula):
    os.path.isdir(KURULUM) or sys.exit(f"kurulum dizini yok: {KURULUM}")
    kurulacak, donusecek, hazir, atlanan, elenen = [], [], [], [], []

    for ad, kazanan, kaybedenler in adaylar():
        elenen += [(ad, g["slug"]) for g in kaybedenler]
        hedef = os.path.join(KURULUM, ad)
        kaynak = kazanan["_yol"]
        if os.path.islink(hedef):
            (hazir if os.path.realpath(hedef) == kaynak else atlanan).append(
                (ad, kazanan["slug"])
                if os.path.realpath(hedef) == kaynak
                else (ad, f"başka bir symlink → {os.path.realpath(hedef)}")
            )
        elif os.path.isdir(hedef):
            if ayni_mi(hedef, kaynak):
                donusecek.append((ad, hedef, kaynak, kazanan["slug"]))
            else:
                atlanan.append((ad, "kurulu dizin İÇERİK AYRIŞMIŞ — önce ekle.py"))
        elif os.path.exists(hedef):
            atlanan.append((ad, "hedefte dizin olmayan bir şey var"))
        else:
            kurulacak.append((ad, hedef, kaynak, kazanan["slug"]))

    print(f"kurulacak        : {len(kurulacak)}")
    print(f"symlink'e dönecek: {len(donusecek)}")
    print(f"zaten bağlı      : {len(hazir)}")
    print(f"atlanan          : {len(atlanan)}")
    print(f"ad çakışmasından elenen sürüm: {len(elenen)}")
    for ad, sebep in atlanan:
        print(f"  ATLA    {ad}\n          → {sebep}")
    for ad, _, _, slug in donusecek:
        print(f"  DÖNÜŞTÜR {ad:38} → kutuphane/…/{slug}")
    for ad, slug in elenen:
        print(f"  ELENDİ  {ad:38} ↛ {slug}")

    if not uygula:
        print("\n[kuru çalıştırma — hiçbir şey değişmedi; --uygula ile kur]")
        return

    gecmis = json.load(open(KAYIT, encoding="utf-8")) if os.path.exists(KAYIT) else []
    for ad, hedef, kaynak, slug in donusecek:
        shutil.rmtree(hedef)
        os.symlink(kaynak, hedef)
        gecmis.append({"ad": ad, "hedef": hedef.replace(EV, "~"),
                       "kaynak": kaynak.replace(EV, "~"), "slug": slug,
                       "onceki": "dizin",
                       "tarih": datetime.now().isoformat(timespec="seconds")})
    for ad, hedef, kaynak, slug in kurulacak:
        os.symlink(kaynak, hedef)
        gecmis.append({"ad": ad, "hedef": hedef.replace(EV, "~"),
                       "kaynak": kaynak.replace(EV, "~"), "slug": slug,
                       "onceki": "yok",
                       "tarih": datetime.now().isoformat(timespec="seconds")})
    json.dump(gecmis, open(KAYIT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n{len(kurulacak) + len(donusecek)} skill kuruldu. Kayıt: katalog/kurulum-kaydi.json")
    print("geri almak için: python3 scripts/kur.py --coz --uygula")


def coz(uygula):
    if not os.path.exists(KAYIT):
        sys.exit("katalog/kurulum-kaydi.json yok — kurulmuş bir şey görünmüyor.")
    gecmis = json.load(open(KAYIT, encoding="utf-8"))
    isler, atlanan = [], []
    for kayit in gecmis:
        hedef = kayit["hedef"].replace("~", EV)
        if not os.path.islink(hedef):
            atlanan.append((kayit["ad"], "artık symlink değil — elle değişmiş"))
        else:
            isler.append(kayit)

    print(f"çözülecek: {len(isler)}   atlanan: {len(atlanan)}")
    for ad, sebep in atlanan:
        print(f"  ATLA  {ad} → {sebep}")
    for kayit in isler:
        geri = "gerçek kopya geri konur" if kayit["onceki"] == "dizin" else "symlink silinir"
        print(f"  ÇÖZ   {kayit['ad']:38} ({geri})")
    if not uygula:
        print("\n[kuru çalıştırma — hiçbir şey değişmedi; --uygula ile çöz]")
        return

    for kayit in isler:
        hedef = kayit["hedef"].replace("~", EV)
        kaynak = kayit["kaynak"].replace("~", EV)
        os.unlink(hedef)
        if kayit["onceki"] == "dizin":
            shutil.copytree(kaynak, hedef, symlinks=False,
                            ignore=shutil.ignore_patterns(".git", "__pycache__", ".DS_Store"))
    kalan = [k for k in gecmis if k not in isler]
    json.dump(kalan, open(KAYIT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n{len(isler)} kurulum çözüldü.")


def main():
    a = argparse.ArgumentParser(add_help=True)
    a.add_argument("--coz", action="store_true", help="kurulumu geri al")
    a.add_argument("--uygula", action="store_true", help="gerçekten uygula")
    args = a.parse_args()
    (coz if args.coz else kur)(args.uygula)


if __name__ == "__main__":
    main()

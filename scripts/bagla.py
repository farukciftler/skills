#!/usr/bin/env python3
"""Kaynak kurulum noktalarını kütüphaneye bağlar (dizin → symlink).

Bu, merkezileştirmenin geri dönüşü zor adımıdır. Bir kurulum noktası
(`<proje>/.claude/skills/<ad>` veya `~/.claude/skills/<ad>`) silinip yerine
`kutuphane/` içindeki karşılığına symlink konur. Bundan sonra skill'i tek
yerden düzenlersin.

Güvenlik kuralları:
  * Varsayılan kuru çalıştırmadır; `--uygula` demeden hiçbir şey değişmez.
  * Kaynak, kütüphanedeki kopyayla **birebir aynı değilse atlanır** — manifest
    yazıldıktan sonra sürüklenmiş bir dizin sessizce ezilmez.
  * Her işlem `katalog/baglanti-kaydi.json`'a yazılır; `scripts/coz.py` ile
    geri alınır.
  * Git deposundaki bir kurulum noktası symlink'e dönüşünce repo'da
    silme+symlink olarak görünür. Depo başına ilerle: `--proje <ad>`.

Kullanım:
    python3 scripts/bagla.py                      # ne olacağını göster
    python3 scripts/bagla.py --proje weftrecords  # tek depoyu süz
    python3 scripts/bagla.py --proje weftrecords --uygula
"""
import argparse
import filecmp
import json
import os
import shutil
import sys
from datetime import datetime

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EV = os.path.expanduser("~")
MANIFEST = os.path.join(KOK, "katalog", "manifest.json")
KAYIT = os.path.join(KOK, "katalog", "baglanti-kaydi.json")


def ayni_mi(a, b):
    """İki dizin ağacı birebir aynı mı?"""
    kiyas = filecmp.dircmp(a, b, ignore=[".DS_Store", ".git", "__pycache__"])

    def gez(k):
        if k.left_only or k.right_only or k.funny_files:
            return False
        _, farkli, hata = filecmp.cmpfiles(
            k.left, k.right, k.common_files, shallow=False
        )
        if farkli or hata:
            return False
        return all(gez(alt) for alt in k.subdirs.values())

    return gez(kiyas)


def main():
    ayristirici = argparse.ArgumentParser(add_help=True)
    ayristirici.add_argument("--proje", help="yalnız yolu bu metni içeren kaynaklar")
    ayristirici.add_argument("--uygula", action="store_true", help="gerçekten bağla")
    args = ayristirici.parse_args()

    if not os.path.exists(MANIFEST):
        sys.exit("katalog/manifest.json yok — önce: python3 scripts/topla.py --uygula")
    manifest = json.load(open(MANIFEST, encoding="utf-8"))

    baglanacak, atlanan, hazir = [], [], []
    for girdi in manifest:
        hedef = girdi["lib"].replace("~", EV)
        for kaynak_rel in girdi.get("linked", []):
            if args.proje and args.proje not in kaynak_rel:
                continue
            kaynak = kaynak_rel.replace("~", EV)
            if os.path.islink(kaynak):
                hazir.append(kaynak_rel)
            elif not os.path.isdir(kaynak):
                atlanan.append((kaynak_rel, "kaynak yok"))
            elif not os.path.isdir(hedef):
                atlanan.append((kaynak_rel, "kütüphane karşılığı yok"))
            elif not ayni_mi(kaynak, hedef):
                atlanan.append((kaynak_rel, "İÇERİK AYRIŞMIŞ — önce topla.py"))
            else:
                baglanacak.append((kaynak_rel, kaynak, hedef, girdi["slug"]))

    print(f"bağlanacak : {len(baglanacak)}")
    print(f"zaten bağlı: {len(hazir)}")
    print(f"atlanan    : {len(atlanan)}")
    for rel, sebep in atlanan:
        print(f"  ATLA  {rel}\n        → {sebep}")
    for rel, _, _, slug in baglanacak:
        print(f"  BAĞLA {rel}\n        → kutuphane/…/{slug}")

    if not args.uygula:
        print("\n[kuru çalıştırma — hiçbir şey değişmedi; --uygula ile bağla]")
        return
    if not baglanacak:
        print("\nyapılacak iş yok.")
        return

    gecmis = json.load(open(KAYIT, encoding="utf-8")) if os.path.exists(KAYIT) else []
    yapilan = 0
    for rel, kaynak, hedef, slug in baglanacak:
        shutil.rmtree(kaynak)
        os.symlink(hedef, kaynak)
        gecmis.append(
            {
                "kaynak": rel,
                "hedef": hedef.replace(EV, "~"),
                "slug": slug,
                "tarih": datetime.now().isoformat(timespec="seconds"),
            }
        )
        yapilan += 1
    json.dump(gecmis, open(KAYIT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n{yapilan} kurulum noktası bağlandı. Kayıt: katalog/baglanti-kaydi.json")
    print("geri almak için: python3 scripts/coz.py --uygula")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""`scripts/bagla.py` ile kurulan symlink'leri geri alır.

Her symlink silinir ve yerine kütüphanedeki içeriğin gerçek bir kopyası konur —
yani depo, bağlanmadan önceki haline döner. Kütüphanedeki dosya bu arada
düzenlendiyse geri dönen kopya o güncel hali taşır (istenen davranış budur:
merkezde yapılan iyileştirme kaybolmaz).

Kullanım:
    python3 scripts/coz.py                       # ne olacağını göster
    python3 scripts/coz.py --proje weftrecords   # tek depoyu süz
    python3 scripts/coz.py --uygula
"""
import argparse
import json
import os
import shutil
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EV = os.path.expanduser("~")
KAYIT = os.path.join(KOK, "katalog", "baglanti-kaydi.json")


def main():
    ayristirici = argparse.ArgumentParser(add_help=True)
    ayristirici.add_argument("--proje", help="yalnız yolu bu metni içeren kayıtlar")
    ayristirici.add_argument("--uygula", action="store_true", help="gerçekten çöz")
    args = ayristirici.parse_args()

    if not os.path.exists(KAYIT):
        sys.exit("katalog/baglanti-kaydi.json yok — bağlanmış bir şey görünmüyor.")
    gecmis = json.load(open(KAYIT, encoding="utf-8"))

    cozulecek, atlanan, kalan = [], [], []
    for kayit in gecmis:
        if args.proje and args.proje not in kayit["kaynak"]:
            kalan.append(kayit)
            continue
        kaynak = kayit["kaynak"].replace("~", EV)
        hedef = kayit["hedef"].replace("~", EV)
        if not os.path.islink(kaynak):
            atlanan.append((kayit["kaynak"], "symlink değil — elle değişmiş olabilir"))
            kalan.append(kayit)
        elif not os.path.isdir(hedef):
            atlanan.append((kayit["kaynak"], "kütüphane karşılığı yok"))
            kalan.append(kayit)
        else:
            cozulecek.append((kayit, kaynak, hedef))

    print(f"çözülecek: {len(cozulecek)}")
    print(f"atlanan  : {len(atlanan)}")
    for rel, sebep in atlanan:
        print(f"  ATLA {rel}\n       → {sebep}")
    for kayit, _, _ in cozulecek:
        print(f"  ÇÖZ  {kayit['kaynak']}")

    if not args.uygula:
        print("\n[kuru çalıştırma — hiçbir şey değişmedi; --uygula ile çöz]")
        return
    if not cozulecek:
        print("\nyapılacak iş yok.")
        return

    for _, kaynak, hedef in cozulecek:
        os.unlink(kaynak)
        shutil.copytree(
            hedef,
            kaynak,
            symlinks=False,
            ignore=shutil.ignore_patterns(".git", "__pycache__", ".DS_Store"),
        )
    json.dump(kalan, open(KAYIT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n{len(cozulecek)} symlink gerçek dizine döndürüldü.")


if __name__ == "__main__":
    main()

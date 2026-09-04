#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kartela Klinik OS — denetim oncesi/sonrasi karsilastirma.

Duzeltmelerden once alinan olcumle sonra alinani yan yana koyar; hangi ekranda
neyin duzeldigini, neyin bozuldugunu tabloya doker. Duzeltme yaptigini iddia
etmeden once bunu calistir.

Kullanim:
    # once
    python3 ... denetim_ss.py --cikti denetim/once
    # duzeltmeler + yeniden derleme
    # sonra
    python3 ... denetim_ss.py --cikti denetim/sonra
    python3 ... karsilastir.py denetim/once/olcum.json denetim/sonra/olcum.json
"""

import json
import sys
from pathlib import Path

ALANLAR = [
    ("yatayTasma", "yatay taşma px", False),
    ("kucukHedef", "<44px hedef", True),
    ("etiketsizAlan", "etiketsiz alan", True),
    ("adsizButon", "adsız buton", True),
    ("kucukGirdi", "16px altı girdi", True),
    ("kontrast", "AA altı metin", True),
    ("konsol", "konsol hatası", True),
]


def anahtar(k: dict) -> str:
    return f"{k.get('rol')}/{k.get('rota')}/{k.get('gorunum')}/{k.get('tema','acik')}"


def deger(kayit: dict, alan: str, sayilir: bool):
    ham = kayit.get(alan)
    if sayilir:
        return len(ham) if isinstance(ham, list) else 0
    return ham if isinstance(ham, (int, float)) else 0


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    once = {anahtar(k): k for k in json.loads(Path(sys.argv[1]).read_text())}
    sonra = {anahtar(k): k for k in json.loads(Path(sys.argv[2]).read_text())}

    toplam_o = {a: 0 for a, _, _ in ALANLAR}
    toplam_s = {a: 0 for a, _, _ in ALANLAR}
    bozulan, duzelen = [], []

    for ek in sorted(set(once) | set(sonra)):
        o, s = once.get(ek), sonra.get(ek)
        if not o or not s:
            print(f"! yalnız bir tarafta: {ek}")
            continue
        for alan, etiket, sayilir in ALANLAR:
            a, b = deger(o, alan, sayilir), deger(s, alan, sayilir)
            toplam_o[alan] += a
            toplam_s[alan] += b
            if b > a:
                bozulan.append(f"{ek} · {etiket}: {a} → {b}")
            elif b < a:
                duzelen.append(f"{ek} · {etiket}: {a} → {b}")

    print(f"\n{'ölçüt':<22}{'önce':>8}{'sonra':>8}{'fark':>8}")
    print("─" * 46)
    for alan, etiket, _ in ALANLAR:
        fark = toplam_s[alan] - toplam_o[alan]
        isaret = "" if fark == 0 else ("↑" if fark > 0 else "↓")
        print(f"{etiket:<22}{toplam_o[alan]:>8}{toplam_s[alan]:>8}{fark:>7}{isaret}")

    if duzelen:
        print(f"\n── düzelen ({len(duzelen)}) ──")
        for s in duzelen:
            print("  ✓", s)
    if bozulan:
        print(f"\n── BOZULAN ({len(bozulan)}) ──")
        for s in bozulan:
            print("  ✗", s)
        return 1
    print("\nGerileme yok.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

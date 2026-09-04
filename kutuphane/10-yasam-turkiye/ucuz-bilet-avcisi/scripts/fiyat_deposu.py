#!/usr/bin/env python3
"""
fiyat_deposu.py — Uçuş fiyatı gözlem deposu ve ampirik fırsat skorlaması.

Neden var: statik fiyat bantları tahmindir ve zamanla kayar. Kendi gözlemlerini
biriktirdiğinde "bu fiyat fırsat mı?" sorusu tahminden ölçüme döner: aynı rota + aynı
sezon için gördüğün fiyatların yüzdelik dilimine bakarsın.

Bağımlılık yok — sadece standart kütüphane.

Kullanım:
    python fiyat_deposu.py kaydet --rota IST-SKP --gidis 2026-08-13 --donus 2026-08-16 \
        --fiyat 1850 --para TRY --tasiyici PC --kaynak google_flights
    python fiyat_deposu.py skor --rota IST-SKP --fiyat 1850 --para TRY
    python fiyat_deposu.py ozet --rota IST-SKP
    python fiyat_deposu.py firsatlar --esik 0.6
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import statistics
from datetime import date, datetime, timezone
from pathlib import Path

VARSAYILAN_DB = Path.home() / ".ucuz-bilet" / "fiyatlar.db"

# Sezon çarpanları — firsat-skorlama.md ile aynı mantık.
# Kendi geçmişin yeterince zenginleştiğinde bunlara ihtiyaç azalır, çünkü
# karşılaştırma zaten aynı sezon içinde yapılır.
YUKSEK_SEZON_AYLAR = {7, 8, 12}
OLU_SEZON_AYLAR = {2, 3, 11}


def sezon_etiketi(gidis_tarihi: str) -> str:
    ay = datetime.strptime(gidis_tarihi, "%Y-%m-%d").month
    if ay in YUKSEK_SEZON_AYLAR:
        return "yuksek"
    if ay in OLU_SEZON_AYLAR:
        return "olu"
    return "orta"


def baglan(db_yolu: Path) -> sqlite3.Connection:
    db_yolu.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db_yolu)
    con.row_factory = sqlite3.Row
    con.executescript(
        """
        CREATE TABLE IF NOT EXISTS gozlem (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            rota         TEXT NOT NULL,      -- IST-SKP  (açık çene: MED-JED gibi de olabilir)
            gidis        TEXT NOT NULL,      -- YYYY-MM-DD
            donus        TEXT,               -- YYYY-MM-DD veya NULL (tek yön)
            fiyat        REAL NOT NULL,
            para         TEXT NOT NULL,
            tasiyici     TEXT,
            aktarma      INTEGER,            -- aktarma sayısı
            bagaj_dahil  INTEGER,            -- 0/1
            kaynak       TEXT NOT NULL,      -- google_flights | kampanya | skyscanner | kullanici
            kanit        TEXT,               -- URL veya kampanya adı
            sezon        TEXT NOT NULL,
            gozlem_ts    TEXT NOT NULL,      -- ISO 8601 UTC
            kalkisa_gun  INTEGER             -- gözlem anında kalkışa kalan gün
        );
        CREATE INDEX IF NOT EXISTS ix_rota_sezon ON gozlem(rota, sezon);
        CREATE INDEX IF NOT EXISTS ix_ts ON gozlem(gozlem_ts);
        """
    )
    return con


def kaydet(con, **kw) -> int:
    gidis = kw["gidis"]
    kalkisa_gun = (datetime.strptime(gidis, "%Y-%m-%d").date() - date.today()).days
    cur = con.execute(
        """INSERT INTO gozlem
           (rota,gidis,donus,fiyat,para,tasiyici,aktarma,bagaj_dahil,
            kaynak,kanit,sezon,gozlem_ts,kalkisa_gun)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            kw["rota"].upper(), gidis, kw.get("donus"), float(kw["fiyat"]),
            kw.get("para", "TRY").upper(), kw.get("tasiyici"), kw.get("aktarma"),
            1 if kw.get("bagaj_dahil") else 0, kw["kaynak"], kw.get("kanit"),
            sezon_etiketi(gidis),
            datetime.now(timezone.utc).isoformat(timespec="seconds"),
            kalkisa_gun,
        ),
    )
    con.commit()
    return cur.lastrowid


def yuzdelik(degerler, q: float) -> float:
    """Basit doğrusal interpolasyonlu yüzdelik. n=1 olsa bile patlamaz."""
    s = sorted(degerler)
    if not s:
        raise ValueError("boş seri")
    if len(s) == 1:
        return s[0]
    k = (len(s) - 1) * q
    alt, ust = int(k), min(int(k) + 1, len(s) - 1)
    return s[alt] + (s[ust] - s[alt]) * (k - alt)


def taban_bul(con, rota: str, para: str, sezon: str | None):
    """Ampirik taban = gözlemlerin 20. yüzdeliği. Aynı sezonda yeterli veri yoksa
    tüm sezonlara düşer ve bunu bildirir."""
    rota = rota.upper()
    para = para.upper()

    def cek(sezon_filtre):
        if sezon_filtre:
            q = "SELECT fiyat FROM gozlem WHERE rota=? AND para=? AND sezon=?"
            return [r["fiyat"] for r in con.execute(q, (rota, para, sezon_filtre))]
        q = "SELECT fiyat FROM gozlem WHERE rota=? AND para=?"
        return [r["fiyat"] for r in con.execute(q, (rota, para))]

    kapsam = f"sezon={sezon}"
    seri = cek(sezon) if sezon else []
    if len(seri) < 5:
        genis = cek(None)
        if len(genis) > len(seri):
            seri, kapsam = genis, "tüm sezonlar (sezon içi veri az)"
    if not seri:
        return None
    return {
        "taban_p20": round(yuzdelik(seri, 0.20), 2),
        "medyan": round(statistics.median(seri), 2),
        "min": round(min(seri), 2),
        "maks": round(max(seri), 2),
        "n": len(seri),
        "kapsam": kapsam,
    }


def etiketle(skor: float) -> str:
    if skor < 0.40:
        return "HATA_FIYATI_OLABILIR"
    if skor < 0.60:
        return "GERCEK_FIRSAT"
    if skor < 0.85:
        return "IYI"
    return "NORMAL"


def skorla(con, rota: str, fiyat: float, para: str, gidis: str | None):
    sezon = sezon_etiketi(gidis) if gidis else None
    ist = taban_bul(con, rota, para, sezon)
    if ist is None:
        return {
            "durum": "veri_yok",
            "mesaj": "Bu rota için hiç gözlem yok. Statik bandı kullan "
                     "(references/firsat-skorlama.md) ve bu fiyatı kaydet.",
        }
    guven = "yuksek" if ist["n"] >= 20 else "orta" if ist["n"] >= 8 else "zayif"
    skor = round(fiyat / ist["taban_p20"], 3)
    return {
        "durum": "ok",
        "skor": skor,
        "etiket": etiketle(skor),
        "guven": guven,
        "gozlem_sayisi": ist["n"],
        "taban_p20": ist["taban_p20"],
        "medyan": ist["medyan"],
        "gorulen_min": ist["min"],
        "kapsam": ist["kapsam"],
        "not": None if guven != "zayif" else
               "Gözlem sayısı az; skoru statik bantla çapraz kontrol et.",
    }


def ozet(con, rota: str):
    rows = list(con.execute(
        """SELECT gidis,donus,fiyat,para,tasiyici,aktarma,kaynak,gozlem_ts,kalkisa_gun
           FROM gozlem WHERE rota=? ORDER BY gozlem_ts DESC LIMIT 40""",
        (rota.upper(),),
    ))
    return [dict(r) for r in rows]


def firsatlar(con, esik: float):
    """Depodaki her rota-tarih için en güncel gözlemi skorlar, eşiğin altını döndürür."""
    son = con.execute(
        """SELECT g.* FROM gozlem g
           JOIN (SELECT rota,gidis,MAX(id) mid FROM gozlem GROUP BY rota,gidis) s
             ON g.id = s.mid"""
    )
    out = []
    for r in son:
        s = skorla(con, r["rota"], r["fiyat"], r["para"], r["gidis"])
        if s["durum"] == "ok" and s["skor"] <= esik:
            out.append({
                "rota": r["rota"], "gidis": r["gidis"], "donus": r["donus"],
                "fiyat": r["fiyat"], "para": r["para"], "tasiyici": r["tasiyici"],
                "skor": s["skor"], "etiket": s["etiket"], "guven": s["guven"],
                "kanit": r["kanit"],
            })
    return sorted(out, key=lambda x: x["skor"])


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--db", type=Path, default=VARSAYILAN_DB)
    alt = p.add_subparsers(dest="komut", required=True)

    k = alt.add_parser("kaydet")
    k.add_argument("--rota", required=True)
    k.add_argument("--gidis", required=True)
    k.add_argument("--donus")
    k.add_argument("--fiyat", required=True, type=float)
    k.add_argument("--para", default="TRY")
    k.add_argument("--tasiyici")
    k.add_argument("--aktarma", type=int)
    k.add_argument("--bagaj-dahil", action="store_true")
    k.add_argument("--kaynak", required=True)
    k.add_argument("--kanit")

    s = alt.add_parser("skor")
    s.add_argument("--rota", required=True)
    s.add_argument("--fiyat", required=True, type=float)
    s.add_argument("--para", default="TRY")
    s.add_argument("--gidis")

    o = alt.add_parser("ozet")
    o.add_argument("--rota", required=True)

    f = alt.add_parser("firsatlar")
    f.add_argument("--esik", type=float, default=0.60)

    a = p.parse_args()
    con = baglan(a.db)

    if a.komut == "kaydet":
        yeni = kaydet(con, rota=a.rota, gidis=a.gidis, donus=a.donus, fiyat=a.fiyat,
                      para=a.para, tasiyici=a.tasiyici, aktarma=a.aktarma,
                      bagaj_dahil=a.bagaj_dahil, kaynak=a.kaynak, kanit=a.kanit)
        print(json.dumps({"kaydedildi": yeni}, ensure_ascii=False))
    elif a.komut == "skor":
        print(json.dumps(skorla(con, a.rota, a.fiyat, a.para, a.gidis),
                         ensure_ascii=False, indent=2))
    elif a.komut == "ozet":
        print(json.dumps(ozet(con, a.rota), ensure_ascii=False, indent=2))
    elif a.komut == "firsatlar":
        print(json.dumps(firsatlar(con, a.esik), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

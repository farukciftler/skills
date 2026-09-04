"""channel_report kova mantiginin regresyon testleri.

Calistir:  python3 .claude/skills/weft-channel/scripts/test_channel_report.py

Buradaki her test bir kez GERCEKTEN yanlis olmus bir davranisi kilitliyor.
"""
import datetime as dt
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from channel_report import (DISPLAY_BUCKETS, TODO_BUCKETS, bucket_of,  # noqa: E402
                            bucket_tol)

D = dt.date


def check(name, got, want):
    if got != want:
        print(f"  BASARISIZ  {name}\n             beklenen {want!r}, gelen {got!r}")
        return 1
    print(f"  ok  {name}")
    return 0


def test_early_ages_do_not_collapse():
    """2026-08-09 auditinde 14 yayinin HEPSI 'gun-2' kovasina dusmustu.

    Sabit BUCKET_TOL=2, gun-2 kovasini [0,4] araligina aciyordu; yas 0, 1 ve 2
    ayni kovaya giriyor, tablo bugun cikmis yayinla iki gunluk yayini yan yana
    koyuyordu. Kovalarin var olma sebebi tam olarak bunu engellemek.
    """
    pub = D(2026, 8, 9)
    fails = 0
    fails += check("yas 0 -> gun-0", bucket_of(D(2026, 8, 9), pub), 0)
    fails += check("yas 1 -> gun-1", bucket_of(D(2026, 8, 10), pub), 1)
    fails += check("yas 2 -> gun-2", bucket_of(D(2026, 8, 11), pub), 2)
    fails += check("yas 3 hicbir kovaya girmez", bucket_of(D(2026, 8, 12), pub), None)
    return fails


def test_tolerance_grows_with_bucket():
    """Erken kovada bir gun fark buyuk, gec kovada degil."""
    fails = 0
    fails += check("gun-0 toleransi 0", bucket_tol(0), 0)
    fails += check("gun-2 toleransi 0", bucket_tol(2), 0)
    fails += check("gun-7 toleransi 1", bucket_tol(7), 1)
    fails += check("gun-30 toleransi 4", bucket_tol(30), 4)
    fails += check("gun-90 toleransi 12", bucket_tol(90), 12)
    return fails


def test_nearest_bucket_not_first_match():
    """Gec kovalarda araliklar ortusur; ilk uyani secmek yanlis cevap verir."""
    pub = D(2026, 1, 1)
    # yas 78: gun-90'in araligi [78,102]; gun-30'unki [26,34] — sadece 90 uyar.
    fails = check("yas 78 -> gun-90", bucket_of(pub + dt.timedelta(days=78), pub), 90)
    # yas 8: gun-7 (±1) uyar, gun-14 (±2 -> [12,16]) uymaz.
    fails += check("yas 8 -> gun-7", bucket_of(pub + dt.timedelta(days=8), pub), 7)
    return fails


def test_todo_starts_at_day_7():
    """CLAUDE.md: 'Ilk 48 saatte karar yok, ilk okuma gun-7.'

    Olcum BORCU gun-7'de baslar. Gun-0/1/2 tabloda gorunur ama borc degildir —
    yoksa rapor asla alinmayacak gecmis okumalari surekli eksik gosterir.
    """
    fails = check("borc listesi gun-7'de baslar", TODO_BUCKETS[0], 7)
    fails += check("gun-2 borc listesinde yok", 2 in TODO_BUCKETS, False)
    fails += check("gun-2 goruntu listesinde var", 2 in DISPLAY_BUCKETS, True)
    return fails


def test_missing_dates_are_none():
    fails = check("yayin gunu yok -> None", bucket_of(D(2026, 8, 9), None), None)
    fails += check("olcum gunu yok -> None", bucket_of(None, D(2026, 8, 9)), None)
    return fails


def main():
    tests = [test_early_ages_do_not_collapse, test_tolerance_grows_with_bucket,
             test_nearest_bucket_not_first_match, test_todo_starts_at_day_7,
             test_missing_dates_are_none]
    total = 0
    for t in tests:
        print(f"\n{t.__name__}")
        total += t()
    print("\n" + ("TUMU GECTI" if total == 0 else f"{total} BASARISIZ"))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""YouTube Studio sayılarını catalog/analytics.csv'ye yazar.

İki yol var, ikisi de aynı satırı üretir:

  import  — Studio → Analitik → Gelişmiş mod → Dışa aktar (CSV) çıktısını okur.
            İndirilen .zip veya açılmış klasör verilir. Sütun adları dilden
            dile değişiyor; eşleşmeyen sütun UYDURULMAZ, ekrana yazılıp durulur.

  add     — ekrandan okunan tek bir yayının sayılarını elle geçirir. Tarayıcıda
            gelişmiş moda inmeye değmeyen tek video ölçümleri için.

    python3 yt_import.py import --export ~/Downloads/Analytics.zip --period 28d
    python3 yt_import.py add --release WR-015 --views 412 --impressions 8200 \
            --ctr 5.0 --avd 14:22 --watch-hours 98 --period lifetime
    python3 yt_import.py add --scope channel --views 1840 --subs 12 --period 28d

Varsayılan olarak yazar; ne yazacağını görmek için --dry-run.
Sistem python3 ile çalışır (stdlib).
"""
import argparse
import csv
import io
import re
import sys
import zipfile
from datetime import date, datetime
from pathlib import Path

FIELDS = ["snap_id", "date", "scope", "release_id", "video_id", "period",
          "impressions", "ctr_pct", "views", "avg_view_duration_sec",
          "watch_hours", "subs_gained", "likes", "comments",
          "top_traffic_source", "top_query", "source", "notes"]

# Studio dışa aktarımının sütun adları — İngilizce ve Türkçe arayüz.
# Sayaç sütunlarında ayırıcı binlik, oran sütunlarında ondalık kabul edilir.
COUNT_COLS = {
    "views": ["views", "görüntüleme", "görüntülemeler", "görüntüleme sayısı"],
    "impressions": ["impressions", "gösterim", "gösterimler", "gösterim sayısı"],
    "subs_gained": ["subscribers", "subscribers gained", "abone", "aboneler",
                    "kazanılan abone", "abone sayısı"],
    "likes": ["likes", "likes (vs. dislikes)", "beğeni", "beğeniler"],
    "comments": ["comments", "comments added", "yorum", "yorumlar", "eklenen yorumlar"],
}
RATE_COLS = {
    "ctr_pct": ["impressions click-through rate (%)", "click-through rate (%)",
                "gösterim tıklama oranı (%)", "tıklama oranı (%)"],
    "watch_hours": ["watch time (hours)", "izlenme süresi (saat)",
                    "izleme süresi (saat)"],
}
DURATION_COLS = {
    "avg_view_duration_sec": ["average view duration", "ortalama görüntülenme süresi",
                              "ortalama izlenme süresi"],
}
KEY_COLS = ["content", "video", "içerik", "video kimliği"]
TITLE_COLS = ["video title", "video başlığı", "başlık"]


def repo_root(explicit=None):
    if explicit:
        return Path(explicit).resolve()
    here = Path(__file__).resolve()
    for cand in [here, *here.parents]:
        if (cand / "catalog" / "publishing.csv").exists():
            return cand
    return Path.cwd()


def norm(text):
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def parse_count(raw):
    """Sayaç: her ayırıcı binliktir. '1.234' = 1234, '12,405' = 12405."""
    s = re.sub(r"[^\d]", "", (raw or ""))
    return s or ""


def parse_rate(raw):
    """Oran: son ayırıcı ondalıktır. '4,7' = 4.7, '1.234,5' = 1234.5."""
    s = (raw or "").replace("%", "").replace(" ", "").strip()
    if not s or s in {"-", "—"}:
        return ""
    cut = max(s.rfind(","), s.rfind("."))
    if cut == -1:
        return s if s.isdigit() else ""
    whole = re.sub(r"[^\d]", "", s[:cut])
    frac = re.sub(r"[^\d]", "", s[cut + 1:])
    if not frac:
        return whole
    return "%s.%s" % (whole or "0", frac)


def parse_duration(raw):
    """'0:03:21' · '3:21' · '201' → saniye."""
    s = (raw or "").strip()
    if not s:
        return ""
    if s.isdigit():
        return s
    parts = s.split(":")
    if not all(p.strip().isdigit() for p in parts):
        return ""
    total = 0
    for p in parts:
        total = total * 60 + int(p)
    return str(total)


def find_col(header, names):
    lookup = {norm(h): i for i, h in enumerate(header)}
    for n in names:
        if n in lookup:
            return lookup[n]
    # Studio bazen sütuna ek parantez koyuyor: "Views (kanal)"
    for key, i in lookup.items():
        for n in names:
            if key.startswith(n):
                return i
    return None


def load_export(path):
    """zip veya klasör → [(dosya adı, satır listesi)]"""
    path = Path(path).expanduser()
    tables = []
    if path.is_dir():
        for f in sorted(path.glob("*.csv")):
            with open(f, newline="", encoding="utf-8-sig") as fh:
                tables.append((f.name, list(csv.reader(fh))))
    elif path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as z:
            for name in sorted(z.namelist()):
                if not name.lower().endswith(".csv"):
                    continue
                data = z.read(name).decode("utf-8-sig", errors="replace")
                tables.append((Path(name).name, list(csv.reader(io.StringIO(data)))))
    elif path.suffix.lower() == ".csv":
        with open(path, newline="", encoding="utf-8-sig") as fh:
            tables.append((path.name, list(csv.reader(fh))))
    else:
        sys.exit("okunamadı (zip/klasör/csv bekleniyor): %s" % path)
    return [(n, rows) for n, rows in tables if rows and len(rows) > 1]


def release_map(root):
    """video_id → release_id, publishing.csv'den."""
    out = {}
    pub = root / "catalog" / "publishing.csv"
    if not pub.exists():
        return out
    with open(pub, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            m = re.search(r"(?:youtu\.be/|[?&]v=|/shorts/|/embed/)([A-Za-z0-9_-]{6,})",
                          row.get("url") or "")
            if m:
                out[m.group(1)] = row.get("release_id", "").strip()
    return out


def next_ids(root, count):
    path = root / "catalog" / "analytics.csv"
    top = 0
    if path.exists():
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                m = re.match(r"AN-(\d+)$", (row.get("snap_id") or "").strip())
                if m:
                    top = max(top, int(m.group(1)))
    return ["AN-%04d" % (top + i + 1) for i in range(count)]


def append(root, rows, dry_run):
    path = root / "catalog" / "analytics.csv"
    if not path.exists():
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(FIELDS)
    with open(path, newline="", encoding="utf-8") as f:
        header = next(csv.reader(f))
    if header != FIELDS:
        sys.exit("analytics.csv başlığı beklenenden farklı — elle bak:\n  %s" % header)

    for r, sid in zip(rows, next_ids(root, len(rows))):
        r["snap_id"] = sid
    for r in rows:
        print("  %s  %-7s %-10s views=%-7s ctr=%-5s imp=%-8s watch=%s" % (
            r["snap_id"], r.get("release_id") or r.get("scope"), r.get("period", ""),
            r.get("views", "—"), r.get("ctr_pct", "—"),
            r.get("impressions", "—"), r.get("watch_hours", "—")))
    if dry_run:
        print("\n--dry-run: hiçbir şey yazılmadı")
        return
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})
    print("\nyazıldı: %s (%d satır)" % (path.relative_to(root), len(rows)))


def cmd_import(args):
    root = repo_root(args.root)
    when = args.date or date.today().isoformat()
    vid2rel = release_map(root)
    tables = load_export(args.export)
    if not tables:
        sys.exit("dışa aktarımda okunabilir CSV yok: %s" % args.export)

    rows, used_table = [], None
    for name, table in tables:
        header, body = table[0], table[1:]
        key_i = find_col(header, KEY_COLS)
        views_i = find_col(header, COUNT_COLS["views"])
        if views_i is None:
            continue
        used_table = name
        cols = {}
        for field, names in COUNT_COLS.items():
            cols[field] = ("count", find_col(header, names))
        for field, names in RATE_COLS.items():
            cols[field] = ("rate", find_col(header, names))
        for field, names in DURATION_COLS.items():
            cols[field] = ("dur", find_col(header, names))
        title_i = find_col(header, TITLE_COLS)

        missing = [f for f, (_, i) in cols.items() if i is None]
        if missing:
            print("! %s içinde bulunamayan sütunlar: %s" % (name, ", ".join(missing)))
            print("  görülen başlıklar: %s" % ", ".join(header))

        for raw in body:
            if not any(c.strip() for c in raw):
                continue
            key = raw[key_i].strip() if key_i is not None and key_i < len(raw) else ""
            is_total = key.lower() in {"total", "toplam", ""}
            rec = {"date": when, "period": args.period,
                   "source": "studio-export:%s" % name,
                   "notes": args.note or ""}
            if is_total and args.scope != "video":
                rec["scope"] = "channel"
            else:
                rec["scope"] = "video"
                rec["video_id"] = key
                rec["release_id"] = vid2rel.get(key, "")
                if not rec["release_id"]:
                    title = raw[title_i].strip() if title_i is not None and title_i < len(raw) else ""
                    print("! %s publishing.csv'de yok%s — release_id boş bırakıldı"
                          % (key, (" (%s)" % title) if title else ""))
            for field, (kind, i) in cols.items():
                if i is None or i >= len(raw):
                    continue
                val = raw[i]
                rec[field] = (parse_count(val) if kind == "count"
                              else parse_rate(val) if kind == "rate"
                              else parse_duration(val))
            if rec.get("views") or rec.get("impressions"):
                rows.append(rec)
        break

    if not rows:
        sys.exit("sayı çıkarılamadı. Okunan dosyalar: %s"
                 % ", ".join(n for n, _ in tables))
    print("kaynak tablo: %s · %d satır" % (used_table, len(rows)))
    append(root, rows, args.dry_run)


def cmd_add(args):
    root = repo_root(args.root)
    when = args.date or date.today().isoformat()
    vid = args.video_id or ""
    rel = args.release or ""
    if rel and not vid:
        for v, r in release_map(root).items():
            if r == rel:
                vid = v
                break
    rec = {
        "date": when,
        "scope": args.scope,
        "release_id": rel,
        "video_id": vid,
        "period": args.period,
        "impressions": parse_count(args.impressions) if args.impressions else "",
        "ctr_pct": parse_rate(args.ctr) if args.ctr else "",
        "views": parse_count(args.views) if args.views else "",
        "avg_view_duration_sec": parse_duration(args.avd) if args.avd else "",
        "watch_hours": parse_rate(args.watch_hours) if args.watch_hours else "",
        "subs_gained": parse_count(args.subs) if args.subs else "",
        "likes": parse_count(args.likes) if args.likes else "",
        "comments": parse_count(args.comments) if args.comments else "",
        "top_traffic_source": args.traffic or "",
        "top_query": args.query or "",
        "source": args.source,
        "notes": args.note or "",
    }
    if rec["scope"] == "video" and not (rel or vid):
        sys.exit("video ölçümü için --release ya da --video-id gerekli")
    append(root, [rec], args.dry_run)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("import", help="Studio CSV dışa aktarımını oku")
    p.add_argument("--export", required=True, help="indirilen .zip, klasör veya .csv")
    p.add_argument("--period", default="28d", help="lifetime · 90d · 28d · 7d · 48h")
    p.add_argument("--date", help="anlık görüntü tarihi (varsayılan: bugün)")
    p.add_argument("--scope", default="auto", choices=["auto", "video"])
    p.add_argument("--note")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_import)

    a = sub.add_parser("add", help="ekrandan okunan sayıları elle gir")
    a.add_argument("--release", help="WR-NNN")
    a.add_argument("--video-id")
    a.add_argument("--scope", default="video", choices=["video", "channel"])
    a.add_argument("--period", default="lifetime")
    a.add_argument("--date")
    a.add_argument("--views")
    a.add_argument("--impressions")
    a.add_argument("--ctr", help="yüzde, ör. 4.7")
    a.add_argument("--avd", help="ortalama görüntülenme süresi, ör. 14:22")
    a.add_argument("--watch-hours")
    a.add_argument("--subs")
    a.add_argument("--likes")
    a.add_argument("--comments")
    a.add_argument("--traffic", help="en büyük trafik kaynağı")
    a.add_argument("--query", help="en büyük arama sorgusu")
    a.add_argument("--source", default="studio-ui")
    a.add_argument("--note")
    a.add_argument("--dry-run", action="store_true")
    a.set_defaults(func=cmd_add)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

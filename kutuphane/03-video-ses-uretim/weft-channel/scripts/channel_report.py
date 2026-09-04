#!/usr/bin/env python3
"""Kanal durum raporu — yüklemeden SONRAKİ işin tek bakışta hâli.

publishing.csv + releases.csv + analytics.csv + channel_log.csv okur; hangi
yayının ölçüm borcu var, hangi kayıt tutarsız, hangi kanal işi gecikti — hepsini
tek çıktıda gösterir. Hiçbir şeyi yazmaz, sadece okur.

    python3 .claude/skills/weft-channel/scripts/channel_report.py
    python3 .claude/skills/weft-channel/scripts/channel_report.py --json
    python3 .claude/skills/weft-channel/scripts/channel_report.py --today 2026-09-08

Çıkış kodu: FAIL varsa 1, yoksa 0. Sistem python3 ile çalışır (stdlib).
"""
import argparse
import csv
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# publishing.csv'de fiilen kullanılan durumlar. `published` conventions.md'de
# yok — orada yayın durumu `released`. İkisi de veride var, script uyarıyor.
CANONICAL_STATUS = {"beklemede", "hazır", "scheduled", "released", "cancelled", "superseded"}
STATUS_FIX = {"published": "released", "yayında": "released"}
LIVE_STATUS = {"released", "published", "yayında"}

# Gün-N karşılaştırması bu kovalarla yapılır: aynı yaştaki yayınlar yan yana.
#
# İki ayrı liste, çünkü iki ayrı iş yapıyorlar:
#   TODO_BUCKETS   — "hangi ölçüm borcu var" listesi. CLAUDE.md § weft-channel:
#                    "İlk 48 saatte karar yok, ilk okuma gün-7." Borç gün-7'de başlar.
#   DISPLAY_BUCKETS — tabloda okumayı GERÇEK yaşında gösterir. Gün-0 ve gün-1
#                    okumaları borç değil ama veri; kovaya sığmadıkları için
#                    sessizce düşmemeleri gerekiyor.
#
# TOLERANS ORANTILI, SABİT DEĞİL. Sabit ±2 gün, gün-2 kovasını [0,4] aralığına
# açıyordu: yaş 0, 1 ve 2 aynı kovaya düşüyor, tablo bugün çıkmış yayınla iki
# günlük yayını "aynı yaşta" diye yan yana koyuyordu — kovaların var olma
# sebebinin tam tersi. Erken kovada bir gün fark büyük, geç kovada değil.
TODO_BUCKETS = (7, 14, 30, 90)
DISPLAY_BUCKETS = (0, 1, 2, 7, 14, 30, 90)


def bucket_tol(b):
    """Kovanın toleransı: gün-0/1/2 tam gün, gün-7 ±1, gün-30 ±4, gün-90 ±12."""
    return b // 7
COMMUNITY_GAP_DAYS = 14  # bundan uzun sessizlik iş listesine düşer

#: Bir yayin cikinca yapilmasi gereken kapanis isleri. Anahtar
#: channel_log.csv'deki `type`, deger raporda gorunecek ad.
#: Bunlar yapilmadan yayin BITMIS sayilmaz; eksikleri rapor gosterir.
CLOSING_WORK = {
    'pinned_comment': 'sabitlenmiş yorum',
    'end_screen': 'bitiş ekranı',
    'playlist': 'oynatma listesi',
}


def repo_root(explicit=None):
    if explicit:
        return Path(explicit).resolve()
    here = Path(__file__).resolve()
    for cand in [here, *here.parents]:
        if (cand / "catalog" / "publishing.csv").exists():
            return cand
    return Path.cwd()


def read_rows(path):
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_date(value):
    value = (value or "").strip()
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def video_id(url):
    """youtu.be/ID · watch?v=ID · /shorts/ID — hepsinden ID çıkarır."""
    url = (url or "").strip()
    if not url:
        return ""
    m = re.search(r"(?:youtu\.be/|[?&]v=|/shorts/|/embed/)([A-Za-z0-9_-]{6,})", url)
    return m.group(1) if m else ""


def to_int(value):
    value = (value or "").strip().replace(".", "").replace(",", "").replace(" ", "")
    return int(value) if value.isdigit() else None


def to_float(value):
    value = (value or "").strip().replace("%", "").replace(",", ".")
    try:
        return float(value)
    except ValueError:
        return None


def collect(root, today):
    pubs = read_rows(root / "catalog" / "publishing.csv")
    rels = {r["release_id"]: r for r in read_rows(root / "catalog" / "releases.csv")}
    snaps = read_rows(root / "catalog" / "analytics.csv")
    log = read_rows(root / "catalog" / "channel_log.csv")

    by_release = {}
    by_video = {}
    channel_snaps = []
    for s in snaps:
        if (s.get("scope") or "video").strip() == "channel":
            channel_snaps.append(s)
            continue
        if s.get("release_id"):
            by_release.setdefault(s["release_id"].strip(), []).append(s)
        if s.get("video_id"):
            by_video.setdefault(s["video_id"].strip(), []).append(s)

    # Yayin KAPANIS islerinin kaydi. Bir video yayinlanip bunlar yapilmazsa
    # borc birikiyor ve rapor "temiz" diyerek yalan soyluyor — 2026-08-09'da
    # on bes yayinin hicbirinde sabitlenmis yorum, bitis ekrani ya da oynatma
    # listesi yoktu ve rapor bunu hic gostermiyordu.
    kapanis = {}
    for e in log:
        t = (e.get("type") or "").strip()
        if t in CLOSING_WORK:
            tgt = (e.get("target") or "").strip()
            if t == "playlist":
                # playlist satirinin hedefi listenin ADI; hangi yayinlari
                # kapsadigi notta duruyor, o yuzden yayin bazinda esleme
                # notes alanindan yapiliyor.
                blob = (e.get("notes") or "") + " " + (e.get("action") or "")
                for m in re.findall(r"WR-\d{3}", blob):
                    kapanis.setdefault(m, set()).add(t)
            elif tgt:
                kapanis.setdefault(tgt, set()).add(t)

    items, issues = [], []

    def flag(level, publish_id, text):
        issues.append({"level": level, "publish_id": publish_id, "text": text})

    for p in pubs:
        pid = p.get("publish_id", "").strip()
        rid = p.get("release_id", "").strip()
        status = (p.get("status") or "").strip()
        url = (p.get("url") or "").strip()
        vid = video_id(url)
        pub_date = parse_date(p.get("published_date"))
        check_date = parse_date(p.get("views_check_date"))
        views_field = to_int(p.get("views"))
        age = (today - pub_date).days if pub_date else None

        mine = by_release.get(rid, []) + [
            s for s in by_video.get(vid, []) if s.get("release_id", "").strip() != rid
        ]
        mine = sorted(mine, key=lambda s: (s.get("date") or ""))
        last = mine[-1] if mine else None

        items.append({
            "publish_id": pid,
            "release_id": rid,
            "title": (rels.get(rid, {}).get("title") or p.get("title") or "").strip(),
            "series": rels.get(rid, {}).get("series", ""),
            "status": status,
            "url": url,
            "video_id": vid,
            "published_date": pub_date.isoformat() if pub_date else "",
            "age_days": age,
            "views_check_date": check_date.isoformat() if check_date else "",
            "snapshots": len(mine),
            "last_snapshot_date": (last or {}).get("date", ""),
            "last_views": to_int((last or {}).get("views")),
            "last_ctr": to_float((last or {}).get("ctr_pct")),
        })

        if status in STATUS_FIX:
            flag("UYAR", pid, "status '%s' → conventions.md '%s' diyor"
                 % (status, STATUS_FIX[status]))
        elif status and status not in CANONICAL_STATUS:
            flag("UYAR", pid, "tanımsız status: '%s'" % status)

        if status in LIVE_STATUS and not url:
            flag("FAIL", pid, "yayında görünüyor ama URL yok")
        if url and not vid:
            flag("FAIL", pid, "URL'den video kimliği çıkmıyor: %s" % url)
        # superseded = yayinlanmisti, YERINE yeni bir yapim gecti ve videosu gizlendi.
        # URL tarihsel kayit olarak duruyor; bu bir eksik degil, bir gecmis.
        if url and status not in LIVE_STATUS and status != "superseded":
            flag("UYAR", pid, "URL var ama status '%s' — yayınlandıysa güncelle" % status)
        if status in LIVE_STATUS and not pub_date:
            flag("UYAR", pid, "yayında ama published_date boş")

        # KAPANIS BORCU. Yayin cikinca bu ucu de yapilir; yapilmadiysa borctur
        # ve burada gorunur. "Sonra yaparim" diye biriken is, birikince
        # on bes videoluk bir temizlik gunune donusuyor.
        if status in LIVE_STATUS and rid:
            eksik = [CLOSING_WORK[k] for k in CLOSING_WORK
                     if k not in kapanis.get(rid, set())]
            if eksik:
                flag("İŞ", pid, "kapanış eksik: %s (channel_log.csv'ye yazılır)"
                     % ", ".join(eksik))

        if pub_date and not check_date:
            flag("İŞ", pid, "views_check_date boş — öneri %s (+30 gün)"
                 % (pub_date + timedelta(days=30)).isoformat())
        if check_date and check_date <= today and views_field is None:
            flag("İŞ", pid, "ölçüm günü geldi (%s) — publishing.csv views boş"
                 % check_date.isoformat())
        if age is not None and age >= 2 and not mine:
            flag("İŞ", pid, "%d günlük, hiç analytics anlık görüntüsü yok" % age)
        elif age is not None and mine:
            covered = {bucket_of(parse_date(s.get("date")), pub_date, TODO_BUCKETS)
                       for s in mine}
            missing = [b for b in TODO_BUCKETS if b <= age and b not in covered]
            if missing:
                flag("İŞ", pid, "gün-%s ölçümü eksik" % ", gün-".join(str(m) for m in missing))

    return {
        "items": items,
        "issues": issues,
        "channel_snaps": sorted(channel_snaps, key=lambda s: s.get("date") or ""),
        "log": sorted(log, key=lambda e: e.get("date") or ""),
    }


def bucket_of(snap_date, pub_date, buckets=DISPLAY_BUCKETS):
    """Anlık görüntünün yaşını EN YAKIN kovaya oturtur; hiçbirine değilse None.

    İlk uyanı değil en yakını seçer — aralıklar örtüşürse (geç kovalarda olur)
    ilk uyan yanlış cevap verir.
    """
    if not snap_date or not pub_date:
        return None
    age = (snap_date - pub_date).days
    fits = [b for b in buckets if abs(age - b) <= bucket_tol(b)]
    return min(fits, key=lambda b: abs(age - b)) if fits else None


def day_n_table(root, data, today):
    """Aynı yaştaki yayınlar yan yana — farklı yaştakileri karşılaştırmak yanlış."""
    snaps = read_rows(root / "catalog" / "analytics.csv")
    pub_by_release = {}
    for item in data["items"]:
        if item["published_date"]:
            pub_by_release[item["release_id"]] = parse_date(item["published_date"])

    grid, dropped = {}, []
    for s in snaps:
        if (s.get("scope") or "video").strip() == "channel":
            continue
        rid = (s.get("release_id") or "").strip()
        pub = pub_by_release.get(rid)
        b = bucket_of(parse_date(s.get("date")), pub)
        views = to_int(s.get("views"))
        if b is None or views is None:
            # Sessizce düşürme yok: kovaya girmeyen okuma da bir veri, sayısı
            # raporda görünür. Görünmeyen eksik, "her şey kapsandı" diye okunur.
            snap_d = parse_date(s.get("date"))
            age = (snap_d - pub).days if (snap_d and pub) else None
            dropped.append({"release_id": rid or "—", "date": s.get("date") or "—",
                            "age_days": age,
                            "why": "views boş" if views is None else "kovaya girmiyor"})
            continue
        grid.setdefault(rid, {})[b] = views
    return grid, dropped


def render(data, grid, today, root, dropped=()):
    out = []
    add = out.append
    add("WEFT KANAL RAPORU — %s" % today.isoformat())
    add("")

    add("YAYINLAR")
    add("%-8s %-7s %-10s %-11s %5s %8s %7s  %s"
        % ("publish", "yayın", "durum", "yayın günü", "yaş", "son ölç.", "views", "başlık"))
    for it in sorted(data["items"], key=lambda x: x["publish_id"]):
        add("%-8s %-7s %-10s %-11s %5s %8s %7s  %s" % (
            it["publish_id"], it["release_id"], it["status"][:10],
            it["published_date"] or "—",
            it["age_days"] if it["age_days"] is not None else "—",
            it["last_snapshot_date"] or "—",
            it["last_views"] if it["last_views"] is not None else "—",
            it["title"][:44]))
    add("")

    if grid:
        cols = [b for b in DISPLAY_BUCKETS if any(b in v for v in grid.values())]
        add("GÜN-N GÖRÜNTÜLEME — aynı yaşta karşılaştır, farklı yaşta değil")
        add("%-8s %s" % ("yayın", " ".join("gün-%-3d" % b for b in cols)))
        for rid in sorted(grid):
            cells = " ".join("%-7s" % (grid[rid].get(b, "—")) for b in cols)
            add("%-8s %s" % (rid, cells))
        if len(cols) > 1:
            add("  ↑ SÜTUNLAR ARASI OKUMA YOK. Bir sütun içinde karşılaştırılır;")
            add("    gün-0 ile gün-2 yan yana durur ama aynı şeyi ölçmezler.")
        add("")

    if dropped:
        add("TABLOYA GİRMEYEN OKUMA — %d tane (sessizce düşürülmedi)" % len(dropped))
        for d in dropped[:8]:
            add("  %-8s %s  yaş %s  — %s"
                % (d["release_id"], d["date"],
                   d["age_days"] if d["age_days"] is not None else "—", d["why"]))
        if len(dropped) > 8:
            add("  … +%d tane daha" % (len(dropped) - 8))
        add("")

    if data["channel_snaps"]:
        last = data["channel_snaps"][-1]
        add("KANAL — son anlık görüntü %s (%s): views %s · abone +%s · gösterim %s · CTR %s"
            % (last.get("date", "—"), last.get("period", "—"), last.get("views", "—"),
               last.get("subs_gained", "—"), last.get("impressions", "—"),
               last.get("ctr_pct", "—")))
        add("")
    else:
        add("KANAL — hiç kanal düzeyi anlık görüntü yok")
        add("")

    community = [e for e in data["log"] if (e.get("type") or "").strip() == "community"]
    if community:
        last_c = parse_date(community[-1].get("date"))
        gap = (today - last_c).days if last_c else None
        add("TOPLULUK — son gönderi %s (%s gün önce), toplam %d"
            % (community[-1].get("date", "—"), gap, len(community)))
    else:
        add("TOPLULUK — hiç gönderi loglanmamış")
    add("")

    fails = [i for i in data["issues"] if i["level"] == "FAIL"]
    warns = [i for i in data["issues"] if i["level"] == "UYAR"]
    jobs = [i for i in data["issues"] if i["level"] == "İŞ"]

    if community:
        last_c = parse_date(community[-1].get("date"))
        if last_c and (today - last_c).days > COMMUNITY_GAP_DAYS:
            jobs.append({"level": "İŞ", "publish_id": "—",
                         "text": "topluluk gönderisi %d gündür yok" % (today - last_c).days})

    add("YAPILACAKLAR")
    if not (fails or warns or jobs):
        add("  temiz — açık iş yok")
    for group, label in ((fails, "FAIL"), (jobs, "İŞ  "), (warns, "UYAR")):
        for i in group:
            add("  %s  %-8s %s" % (label, i["publish_id"], i["text"]))
    add("")
    add("özet: %d FAIL · %d iş · %d uyarı" % (len(fails), len(jobs), len(warns)))
    return "\n".join(out), len(fails)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", help="repo kökü (varsayılan: otomatik bulunur)")
    ap.add_argument("--today", help="YYYY-MM-DD — ölçüm gününü sabitlemek için")
    ap.add_argument("--json", action="store_true", help="ham veriyi JSON bas")
    args = ap.parse_args()

    root = repo_root(args.root)
    today = parse_date(args.today) or date.today()
    data = collect(root, today)
    grid, dropped = day_n_table(root, data, today)

    if args.json:
        print(json.dumps({"today": today.isoformat(), "root": str(root),
                          "day_n": grid, "day_n_dropped": dropped, **data},
                         ensure_ascii=False, indent=2))
        return 1 if any(i["level"] == "FAIL" for i in data["issues"]) else 0

    text, fails = render(data, grid, today, root, dropped)
    print(text)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

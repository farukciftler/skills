#!/usr/bin/env python3
"""arXiv radar — kayitli sorgulari calistirir, sadece YENI makaleleri raporlar.

Kullanim:
  python arxiv_radar.py --config radar.json --state seen.json --out digest.md
  python arxiv_radar.py --config radar.json --dry-run     # state'i guncelleme

Cron (arXiv duyurusu ~22:30 ET oldugu icin sabah calistir):
  0 8 * * * cd /opt/arxiv-radar && python scripts/arxiv_radar.py \\
            --config radar.json --state seen.json --out digest-$(date +\\%F).md

Konfig ornegi: assets/radar.example.json
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arxiv_query import MIN_DELAY, authors_line, search  # noqa: E402


def load_state(path):
    if path and os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {"seen": {}, "last_run": None}


def save_state(path, state):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def run(config, state, days, max_per_topic, delay, include_updates):
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    seen = state.setdefault("seen", {})
    report = []

    for i, topic in enumerate(config["topics"]):
        name, query = topic["name"], topic["query"]
        sys.stderr.write(f"\n[{name}] {query}\n")

        if i:
            time.sleep(delay)

        try:
            records, _ = search(
                query=query.replace(" ", "+"),
                max_results=topic.get("max", max_per_topic),
                since=topic.get("since", since),
                sort_by="submittedDate",
                sort_order="descending",
                delay=delay,
            )
        except SystemExit as e:
            sys.stderr.write(f"  ATLANDI: {e}\n")
            continue

        fresh, revised = [], []
        for r in records:
            prev = seen.get(r["id"])
            if prev is None:
                fresh.append(r)
            elif include_updates and prev != r["version_id"]:
                revised.append(r)
            seen[r["id"]] = r["version_id"]

        report.append({"name": name, "query": query, "new": fresh, "revised": revised})
        sys.stderr.write(f"  {len(fresh)} yeni, {len(revised)} revizyon "
                         f"({len(records)} tarandi)\n")
    return report


def render(report, days):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(len(t["new"]) for t in report)
    lines = [f"# arXiv radar — {now}", "",
             f"Son {days} gun · **{total} yeni makale** · {len(report)} konu", ""]

    if not total and not any(t["revised"] for t in report):
        lines.append("_Yeni bir sey yok._")
        return "\n".join(lines)

    for t in report:
        if not t["new"] and not t["revised"]:
            continue
        lines += [f"## {t['name']}", ""]

        for r in t["new"]:
            lines += [
                f"### {r['title']}",
                f"`arXiv:{r['version_id']}` · {r['published'][:10]} · "
                f"**{r['primary_category']}**  ",
                f"{authors_line(r['authors'])}",
                "",
                r["abstract"][:350] + ("…" if len(r["abstract"]) > 350 else ""),
            ]
            if r["comment"]:
                lines.append(f"> {r['comment']}")
            lines += [f"<{r['abs_url']}>", ""]

        if t["revised"]:
            lines += ["**Guncellenen versiyonlar:**", ""]
            for r in t["revised"]:
                lines.append(f"- {r['title']} — `{r['version_id']}` <{r['abs_url']}>")
            lines.append("")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="arXiv radar")
    p.add_argument("--config", required=True, help="konu/sorgu JSON dosyasi")
    p.add_argument("--state", default="seen.json")
    p.add_argument("--out", help="markdown digest dosyasi (varsayilan stdout)")
    p.add_argument("--days", type=int, default=7, help="geriye donuk tarama penceresi")
    p.add_argument("--max", type=int, default=50, dest="max_per_topic")
    p.add_argument("--delay", type=float, default=MIN_DELAY)
    p.add_argument("--updates", action="store_true", help="revizyonlari da raporla")
    p.add_argument("--dry-run", action="store_true", help="state'i yazma")
    a = p.parse_args()

    with open(a.config, encoding="utf-8") as f:
        config = json.load(f)
    if not config.get("topics"):
        raise SystemExit("Konfigde 'topics' listesi yok.")

    state = load_state(a.state)
    report = run(config, state, a.days, a.max_per_topic, a.delay, a.updates)
    text = render(report, a.days)

    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text)
        sys.stderr.write(f"\n-> {a.out}\n")
    else:
        print(text)

    if not a.dry_run:
        state["last_run"] = datetime.now(timezone.utc).isoformat()
        save_state(a.state, state)


if __name__ == "__main__":
    main()

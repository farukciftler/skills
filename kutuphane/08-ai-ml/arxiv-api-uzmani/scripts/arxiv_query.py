#!/usr/bin/env python3
"""arXiv Query API istemcisi — rate-limit'e uyan, sayfalamalı, bağımlılıksız.

Kullanım:
  python arxiv_query.py --query 'cat:cs.LG AND abs:"mixture of experts"' --max 100
  python arxiv_query.py --query 'cat:cs.CL' --since 2026-09-01 --format json
  python arxiv_query.py --id 2509.01234,2412.09876v2

arXiv ToU: 1 istek / 3 saniye, tek bağlantı. Bu script buna uyar; --delay ile
düşürme.
"""

import argparse
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

API = "http://export.arxiv.org/api/query"
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "opensearch": "http://a9.com/-/spec/opensearch/1.1/",
    "arxiv": "http://arxiv.org/schemas/atom",
}
USER_AGENT = "arxiv-api-uzmani/1.0 (kisisel arastirma; +https://arxiv.org/help/api)"
MIN_DELAY = 3.0
MAX_PAGE = 2000
MAX_START = 30000

ID_RE = re.compile(r"(?:(\d{4}\.\d{4,5})|([a-zA-Z\-]+(?:\.[A-Z]{2})?/\d{7}))(v\d+)?")


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #
def fetch(params, delay=MIN_DELAY, retries=4):
    """Tek bir API çağrısı; 429/503'te exponential backoff."""
    url = API + "?" + urllib.parse.urlencode(params, safe=':+[]"()')
    backoff = delay
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and attempt < retries:
                wait = float(e.headers.get("Retry-After") or backoff)
                sys.stderr.write(f"[{e.code}] {wait:.0f}s bekleniyor…\n")
                time.sleep(wait)
                backoff *= 2
                continue
            if e.code == 400:
                raise SystemExit(f"HTTP 400 — parametre hatasi: {url}")
            raise
        except urllib.error.URLError as e:
            if attempt < retries:
                sys.stderr.write(f"[ag hatasi] {e.reason} — {backoff:.0f}s…\n")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise
    raise SystemExit("Istek tekrar tekrar basarisiz oldu.")


# --------------------------------------------------------------------------- #
# Parse
# --------------------------------------------------------------------------- #
def _text(el, path):
    return " ".join((el.findtext(path, "", NS) or "").split())


def split_id(abs_url):
    """abs URL'den (base_id, version_id) cikar. Eski format ID'leri de destekler."""
    tail = abs_url.rsplit("/abs/", 1)[-1]
    m = ID_RE.match(tail)
    if not m:
        return tail, tail
    base = m.group(1) or m.group(2)
    return base, tail


def parse_feed(xml_bytes):
    """(kayitlar, toplam_sonuc) dondurur. Atom hata feed'ini yakalar."""
    root = ET.fromstring(xml_bytes)
    entries = root.findall("atom:entry", NS)

    if len(entries) == 1 and _text(entries[0], "atom:title") == "Error":
        raise SystemExit("arXiv API hatasi: " + _text(entries[0], "atom:summary"))

    total_txt = root.findtext("opensearch:totalResults", "0", NS) or "0"
    try:
        total = int(total_txt.strip())
    except ValueError:
        total = 0

    out = []
    for e in entries:
        base_id, ver_id = split_id(_text(e, "atom:id"))
        prim = e.find("arxiv:primary_category", NS)
        pdf = ""
        for ln in e.findall("atom:link", NS):
            if ln.get("title") == "pdf":
                pdf = ln.get("href", "")
        out.append(
            {
                "id": base_id,
                "version_id": ver_id,
                "title": _text(e, "atom:title"),
                "abstract": _text(e, "atom:summary"),
                "authors": [
                    " ".join((a.findtext("atom:name", "", NS) or "").split())
                    for a in e.findall("atom:author", NS)
                ],
                "published": _text(e, "atom:published"),
                "updated": _text(e, "atom:updated"),
                "primary_category": prim.get("term") if prim is not None else "",
                "categories": [c.get("term") for c in e.findall("atom:category", NS)],
                "comment": _text(e, "arxiv:comment"),
                "journal_ref": _text(e, "arxiv:journal_ref"),
                "doi": _text(e, "arxiv:doi"),
                "abs_url": f"https://arxiv.org/abs/{base_id}",
                "pdf_url": pdf,
            }
        )
    return out, total


# --------------------------------------------------------------------------- #
# Search
# --------------------------------------------------------------------------- #
def date_range(since=None, until=None):
    """YYYY-MM-DD -> submittedDate:[YYYYMMDD0000+TO+YYYYMMDD2359] parcasi."""
    if not since and not until:
        return None
    fmt = lambda d, t: datetime.strptime(d, "%Y-%m-%d").strftime("%Y%m%d") + t
    lo = fmt(since, "0000") if since else "199101010000"
    hi = fmt(until, "2359") if until else datetime.now(timezone.utc).strftime("%Y%m%d2359")
    return f"submittedDate:[{lo}+TO+{hi}]"


def search(query=None, ids=None, max_results=100, page_size=100,
           sort_by="submittedDate", sort_order="descending",
           since=None, until=None, delay=MIN_DELAY, verbose=True):
    """Sayfalamali arama. Versiyonsuz base ID uzerinden dedupe eder."""
    if since or until:
        rng = date_range(since, until)
        query = f"({query})+AND+{rng}" if query else rng

    page_size = min(page_size, MAX_PAGE, max_results)
    seen, results, start, total = set(), [], 0, None

    while len(results) < max_results:
        if start > MAX_START:
            sys.stderr.write(
                "start=30000 sinirina gelindi. Sorguyu tarih araliklarina bol.\n"
            )
            break

        params = {"start": start, "max_results": min(page_size, max_results - len(results))}
        if query:
            params["search_query"] = query
        if ids:
            params["id_list"] = ids
        if sort_by:
            params["sortBy"] = sort_by
            params["sortOrder"] = sort_order

        page, total = parse_feed(fetch(params, delay=delay))
        if not page:
            break

        for r in page:
            if r["id"] not in seen:
                seen.add(r["id"])
                results.append(r)

        if verbose:
            sys.stderr.write(f"  {len(results)}/{min(max_results, total or max_results)} …\n")

        start += len(page)
        if ids or (total is not None and start >= total):
            break
        if len(results) < max_results:
            time.sleep(delay)

    return results[:max_results], total


# --------------------------------------------------------------------------- #
# Output
# --------------------------------------------------------------------------- #
def authors_line(a, limit=3):
    if not a:
        return "—"
    return ", ".join(a[:limit]) + (f" +{len(a) - limit}" if len(a) > limit else "")


def to_markdown(records, title="arXiv sonuclari"):
    lines = [f"# {title}", "", f"{len(records)} makale · {datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]
    for r in records:
        lines += [
            f"### {r['title']}",
            f"`arXiv:{r['version_id']}` · {r['published'][:10]} · **{r['primary_category']}**",
            f"{authors_line(r['authors'])}",
            "",
            r["abstract"][:400] + ("…" if len(r["abstract"]) > 400 else ""),
        ]
        if r["comment"]:
            lines.append(f"> {r['comment']}")
        lines += [f"<{r['abs_url']}>", ""]
    return "\n".join(lines)


def to_csv(records, fh):
    cols = ["id", "version_id", "title", "published", "updated",
            "primary_category", "categories", "authors", "comment",
            "journal_ref", "doi", "abs_url"]
    w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    for r in records:
        row = dict(r)
        row["authors"] = "; ".join(r["authors"])
        row["categories"] = " ".join(r["categories"])
        w.writerow(row)


def main():
    p = argparse.ArgumentParser(description="arXiv Query API istemcisi")
    p.add_argument("--query", help='search_query, or. \'cat:cs.LG AND abs:"moe"\'')
    p.add_argument("--id", dest="ids", help="virgullu arXiv ID listesi")
    p.add_argument("--max", type=int, default=50, dest="max_results")
    p.add_argument("--page-size", type=int, default=100)
    p.add_argument("--since", help="YYYY-MM-DD (submittedDate alt sinir)")
    p.add_argument("--until", help="YYYY-MM-DD (submittedDate ust sinir)")
    p.add_argument("--sort", default="submittedDate",
                   choices=["relevance", "lastUpdatedDate", "submittedDate"])
    p.add_argument("--order", default="descending", choices=["ascending", "descending"])
    p.add_argument("--format", default="md", choices=["md", "json", "csv"])
    p.add_argument("--delay", type=float, default=MIN_DELAY)
    p.add_argument("--out", help="dosyaya yaz (varsayilan stdout)")
    a = p.parse_args()

    if not a.query and not a.ids:
        p.error("--query veya --id gerekli")
    if a.delay < MIN_DELAY:
        sys.stderr.write(f"UYARI: {MIN_DELAY}s altina inmek arXiv ToU ihlalidir.\n")

    q = a.query.replace(" ", "+") if a.query else None
    records, total = search(query=q, ids=a.ids, max_results=a.max_results,
                            page_size=a.page_size, sort_by=a.sort,
                            sort_order=a.order, since=a.since, until=a.until,
                            delay=a.delay)

    sys.stderr.write(f"\n{len(records)} kayit (toplam eslesme: {total})\n")

    fh = open(a.out, "w", encoding="utf-8") if a.out else sys.stdout
    try:
        if a.format == "json":
            json.dump(records, fh, ensure_ascii=False, indent=2)
        elif a.format == "csv":
            to_csv(records, fh)
        else:
            fh.write(to_markdown(records, a.query or a.ids))
    finally:
        if a.out:
            fh.close()
            sys.stderr.write(f"-> {a.out}\n")


if __name__ == "__main__":
    main()

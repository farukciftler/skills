#!/usr/bin/env python3
"""arXiv OAI-PMH hasatcisi — resumptionToken'li, checkpoint'li, JSONL cikti.

Kullanim:
  python arxiv_oai.py --set cs:cs:AI --from 2026-09-01 --out cs_ai.jsonl
  python arxiv_oai.py --sets                      # mevcut setleri listele
  python arxiv_oai.py --identify                  # depo bilgisi
  python arxiv_oai.py --set math:math:NA --resume  # checkpoint'ten devam

Notlar:
  * Base URL Mart 2025'te degisti: https://oaipmh.arxiv.org/oai
  * datestamp = son degisiklik tarihi, gonderim tarihi DEGIL. Gonderim
    tarihine gore secim gerekiyorsa Query API + submittedDate kullan.
  * resumptionToken gunluk expire olur; kesilen hasat token ile degil,
    son datestamp + --from ile devam ettirilir.
  * 1 istek / 3 saniye, tek baglanti.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

BASE = "https://oaipmh.arxiv.org/oai"
USER_AGENT = "arxiv-api-uzmani/1.0 (kisisel arastirma; +https://arxiv.org/help/oa)"
MIN_DELAY = 3.0

OAI = "{http://www.openarchives.org/OAI/2.0/}"
ARXIV = "{http://arxiv.org/OAI/arXiv/}"


def fetch(params, delay=MIN_DELAY, retries=5):
    url = BASE + "?" + urllib.parse.urlencode(params)
    backoff = delay
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            # OAI-PMH'de 503 normal akis kontrolu, hata degil.
            if e.code in (429, 503) and attempt < retries:
                wait = float(e.headers.get("Retry-After") or backoff)
                sys.stderr.write(f"[{e.code}] {wait:.0f}s bekleniyor…\n")
                time.sleep(wait)
                backoff = min(backoff * 2, 300)
                continue
            raise
        except urllib.error.URLError as e:
            if attempt < retries:
                sys.stderr.write(f"[ag] {e.reason} — {backoff:.0f}s…\n")
                time.sleep(backoff)
                backoff = min(backoff * 2, 300)
                continue
            raise
    raise SystemExit("Istek tekrar tekrar basarisiz oldu.")


def check_error(root):
    err = root.find(OAI + "error")
    if err is not None:
        code = err.get("code", "")
        if code == "noRecordsMatch":
            return "empty"
        raise SystemExit(f"OAI hatasi [{code}]: {(err.text or '').strip()}")
    return None


def parse_arxiv_record(rec):
    """metadataPrefix=arXiv formatindaki tek kaydi sozluge cevirir."""
    header = rec.find(OAI + "header")
    if header is None:
        return None
    identifier = (header.findtext(OAI + "identifier") or "").strip()
    datestamp = (header.findtext(OAI + "datestamp") or "").strip()
    if header.get("status") == "deleted":
        return {"identifier": identifier, "datestamp": datestamp, "deleted": True}

    md = rec.find(OAI + "metadata")
    body = md.find(ARXIV + "arXiv") if md is not None else None
    if body is None:
        return {"identifier": identifier, "datestamp": datestamp, "raw": True}

    txt = lambda t: " ".join((body.findtext(ARXIV + t) or "").split())
    authors = []
    forenames_path = body.find(ARXIV + "authors")
    if forenames_path is not None:
        for a in forenames_path.findall(ARXIV + "author"):
            name = " ".join(
                filter(None, [
                    " ".join((a.findtext(ARXIV + "forenames") or "").split()),
                    " ".join((a.findtext(ARXIV + "keyname") or "").split()),
                ])
            )
            if name:
                authors.append(name)

    return {
        "identifier": identifier,
        "datestamp": datestamp,
        "id": txt("id"),
        "title": txt("title"),
        "abstract": txt("abstract"),
        "authors": authors,
        "categories": txt("categories").split(),
        "created": txt("created"),
        "updated": txt("updated"),
        "doi": txt("doi"),
        "journal_ref": txt("journal-ref"),
        "license": txt("license"),
        "comments": txt("comments"),
    }


def harvest(setspec=None, frm=None, until=None, prefix="arXiv",
            out_path="records.jsonl", state_path=None, delay=MIN_DELAY,
            limit=None, resume=False):
    state = {}
    if state_path and resume and os.path.exists(state_path):
        with open(state_path, encoding="utf-8") as f:
            state = json.load(f)
        frm = state.get("last_datestamp", frm)
        sys.stderr.write(f"Checkpoint'ten devam: from={frm}\n")

    params = {"verb": "ListRecords", "metadataPrefix": prefix}
    if setspec:
        params["set"] = setspec
    if frm:
        params["from"] = frm
    if until:
        params["until"] = until

    count, token, last_ds = 0, None, state.get("last_datestamp")
    mode = "a" if (resume and os.path.exists(out_path)) else "w"

    with open(out_path, mode, encoding="utf-8") as out:
        while True:
            root = ET.fromstring(fetch(params, delay=delay))
            if check_error(root) == "empty":
                sys.stderr.write("Eslesen kayit yok.\n")
                break

            lr = root.find(OAI + "ListRecords")
            if lr is None:
                break

            for rec in lr.findall(OAI + "record"):
                parsed = parse_arxiv_record(rec)
                if parsed:
                    out.write(json.dumps(parsed, ensure_ascii=False) + "\n")
                    last_ds = parsed.get("datestamp") or last_ds
                    count += 1
            out.flush()

            if state_path:
                with open(state_path, "w", encoding="utf-8") as sf:
                    json.dump({"last_datestamp": last_ds, "count": count}, sf)

            sys.stderr.write(f"  {count} kayit…\n")
            if limit and count >= limit:
                sys.stderr.write("Limite ulasildi.\n")
                break

            tok_el = lr.find(OAI + "resumptionToken")
            token = (tok_el.text or "").strip() if tok_el is not None else ""
            if not token:
                sys.stderr.write("Hasat tamamlandi.\n")
                break

            # resumptionToken ile birlikte baska parametre GONDERILMEZ.
            params = {"verb": "ListRecords", "resumptionToken": token}
            time.sleep(delay)

    sys.stderr.write(f"\nToplam {count} kayit -> {out_path}\n")
    return count


def simple_verb(verb, delay=MIN_DELAY):
    root = ET.fromstring(fetch({"verb": verb}, delay=delay))
    check_error(root)
    if verb == "ListSets":
        for s in root.iter(OAI + "set"):
            spec = s.findtext(OAI + "setSpec") or ""
            name = s.findtext(OAI + "setName") or ""
            print(f"{spec:<28} {name}")
    else:
        ident = root.find(OAI + "Identify")
        if ident is not None:
            for child in ident:
                tag = child.tag.replace(OAI, "")
                if child.text and child.text.strip():
                    print(f"{tag:<22} {child.text.strip()}")


def main():
    p = argparse.ArgumentParser(description="arXiv OAI-PMH hasatcisi")
    p.add_argument("--set", dest="setspec", help="or. cs:cs:AI, physics:hep-th, math")
    p.add_argument("--from", dest="frm", help="YYYY-MM-DD (datestamp alt siniri)")
    p.add_argument("--until", help="YYYY-MM-DD")
    p.add_argument("--prefix", default="arXiv", choices=["arXiv", "arXivRaw", "oai_dc"])
    p.add_argument("--out", default="records.jsonl")
    p.add_argument("--state", default="oai_state.json")
    p.add_argument("--resume", action="store_true", help="checkpoint'ten devam et")
    p.add_argument("--limit", type=int, help="kayit sayisi ust siniri (test icin)")
    p.add_argument("--delay", type=float, default=MIN_DELAY)
    p.add_argument("--sets", action="store_true", help="ListSets")
    p.add_argument("--identify", action="store_true", help="Identify")
    a = p.parse_args()

    if a.delay < MIN_DELAY:
        sys.stderr.write(f"UYARI: {MIN_DELAY}s altina inmek arXiv ToU ihlalidir.\n")

    if a.sets:
        return simple_verb("ListSets", a.delay)
    if a.identify:
        return simple_verb("Identify", a.delay)

    harvest(setspec=a.setspec, frm=a.frm, until=a.until, prefix=a.prefix,
            out_path=a.out, state_path=a.state, delay=a.delay,
            limit=a.limit, resume=a.resume)


if __name__ == "__main__":
    main()

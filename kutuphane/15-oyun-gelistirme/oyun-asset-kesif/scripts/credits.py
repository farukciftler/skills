#!/usr/bin/env python3
"""
Asset ledger + CREDITS.md generator.

  add     --from results.json --id <source:id> [--used-in PATH] [--modified "decimated"]
  manual  --title T --author A --url U --license L [--used-in PATH]
  list
  render  [--out CREDITS.md] [--project NAME]
  check   exit 1 if ledger holds red/unknown licenses (CI gate)

Ledger default: ./asset_ledger.json  (override with --ledger)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from asset_search import classify, license_display, license_url, normalize_license  # noqa: E402


def load(path):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {"assets": []}


def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def upsert(ledger, entry):
    for i, a in enumerate(ledger["assets"]):
        if a["key"] == entry["key"]:
            ledger["assets"][i] = {**a, **entry}
            return "updated"
    ledger["assets"].append(entry)
    return "added"


def cmd_add(a):
    with open(a.from_, encoding="utf-8") as f:
        res = json.load(f)
    rec = next((r for r in res.get("results", []) if r.get("key") == a.id), None)
    if not rec:
        sys.exit(f"{a.id} not found in {a.from_}")
    entry = {
        "key": rec["key"], "title": rec.get("title"), "author": rec.get("author"),
        "source": rec.get("source"), "url": rec.get("page_url"), "license": rec.get("license"),
        "license_raw": rec.get("license_raw"),
        "license_class": rec.get("license_class"), "added": date.today().isoformat(),
        "used_in": a.used_in, "modified": a.modified,
    }
    led = load(a.ledger)
    print(upsert(led, entry), entry["key"])
    save(a.ledger, led)


def cmd_manual(a):
    lic = normalize_license(a.license)
    cls, _ = classify(lic, commercial=True, appstore=a.appstore)
    key = a.key or f"manual:{a.title.lower().replace(' ', '-')}"
    entry = {"key": key, "title": a.title, "author": a.author, "source": a.source or "manual",
             "url": a.url, "license": lic, "license_raw": a.license, "license_class": cls,
             "added": date.today().isoformat(), "used_in": a.used_in, "modified": a.modified}
    led = load(a.ledger)
    print(upsert(led, entry), key, lic, cls)
    save(a.ledger, led)


def cmd_list(a):
    for x in load(a.ledger)["assets"]:
        print(f'{x["license_class"]:8} {x["license"]:10} {x["key"]:40} {x.get("used_in") or ""}')


def line(x):
    label = license_display(x["license"], x.get("license_raw"))
    if x["license"] == "UNKNOWN" and x.get("license_raw"):
        label = x["license_raw"]
    lurl = license_url(x["license"], x.get("license_raw"))
    s = f'- "{x["title"]}" by {x.get("author") or "unknown"} — {x.get("url")} — {label}'
    if lurl:
        s += f" ({lurl})"
    if x.get("modified"):
        s += f" — modified: {x['modified']}"
    return s


def cmd_render(a):
    assets = load(a.ledger)["assets"]
    need = [x for x in assets if x["license_class"] in ("yellow", "orange")]
    cc0 = [x for x in assets if x["license_class"] == "green"]
    bad = [x for x in assets if x["license_class"] in ("red", "unknown")]
    out = [f"# Credits{(' — ' + a.project) if a.project else ''}", ""]
    if need:
        out += ["## Third-party assets (attribution required)", ""] + [line(x) for x in sorted(need, key=lambda x: x["title"] or "")] + [""]
    if cc0:
        out += ["## Public domain / CC0 and royalty-free assets", "",
                "Credit not required; listed with thanks.", ""] + [line(x) for x in sorted(cc0, key=lambda x: x["title"] or "")] + [""]
    if bad:
        out += ["<!-- WARNING: the following entries have red/unknown licenses and should be resolved before release:",
                *[f"     {x['key']} ({x['license']})" for x in bad], "-->", ""]
    text = "\n".join(out)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"wrote {a.out}: {len(need)} attribution, {len(cc0)} cc0/royalty-free, {len(bad)} unresolved")


def cmd_check(a):
    bad = [x for x in load(a.ledger)["assets"] if x["license_class"] in ("red", "unknown")]
    for x in bad:
        print(f'UNRESOLVED {x["key"]} {x["license"]} {x.get("url")}')
    sys.exit(1 if bad else 0)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ledger", default="asset_ledger.json")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("add")
    p.add_argument("--from", dest="from_", required=True)
    p.add_argument("--id", required=True)
    p.add_argument("--used-in")
    p.add_argument("--modified")
    p.set_defaults(fn=cmd_add)

    p = sub.add_parser("manual")
    for k in ("title", "author", "url", "license"):
        p.add_argument(f"--{k}", required=True)
    p.add_argument("--source")
    p.add_argument("--key")
    p.add_argument("--used-in")
    p.add_argument("--modified")
    p.add_argument("--appstore", action="store_true")
    p.set_defaults(fn=cmd_manual)

    sub.add_parser("list").set_defaults(fn=cmd_list)

    p = sub.add_parser("render")
    p.add_argument("--out", default="CREDITS.md")
    p.add_argument("--project")
    p.set_defaults(fn=cmd_render)

    sub.add_parser("check").set_defaults(fn=cmd_check)

    a = ap.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()

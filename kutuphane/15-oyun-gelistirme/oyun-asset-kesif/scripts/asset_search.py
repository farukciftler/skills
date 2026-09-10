#!/usr/bin/env python3
"""
Multi-source free game asset search with license gating.

Sources (API):  polyhaven, ambientcg, sketchfab   -> no key needed for search
                polypizza  (env POLYPIZZA_API_KEY or POLY_PIZZA_API_KEY)
                freesound  (env FREESOUND_API_KEY)

Stdlib only. Every provider is fault-isolated: a failing/missing-key source is
reported in "errors" / "skipped" and the rest still return.

Examples:
  python asset_search.py "wooden barrel" --type model --commercial --appstore
  python asset_search.py "sand" --sources ambientcg,polyhaven --type material --green-only
  python asset_search.py "door creak" --sources freesound --type sfx --out res.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

UA = "OyunAssetKesif/1.0 (+claude-skill)"
TIMEOUT = 25

# --------------------------------------------------------------------------- #
# License normalisation & classification
# --------------------------------------------------------------------------- #

LICENSE_LABELS = {
    "CC0-1.0": "CC0 1.0 (Public Domain)",
    "ROYALTY-FREE": "Royalty-free EULA (no raw-file redistribution)",
    "OGA-BY": "OGA-BY",
    "CC-BY": "CC BY",
    "CC-BY-SA": "CC BY-SA",
    "CC-BY-NC": "CC BY-NC (non-commercial)",
    "CC-BY-ND": "CC BY-ND (no derivatives)",
    "GPL": "GPL",
    "LGPL": "LGPL",
    "EDITORIAL": "Editorial only",
    "STANDARD": "Store/Standard (paid or proprietary)",
    "UNKNOWN": "Unknown - check asset page",
}


def normalize_license(raw) -> str:
    """Map arbitrary license strings / URLs / slugs to a canonical id."""
    if raw is None:
        return "UNKNOWN"
    if isinstance(raw, dict):
        raw = " ".join(str(raw.get(k, "")) for k in ("slug", "label", "fullName", "url", "name"))
    s = str(raw).strip().lower()
    if not s:
        return "UNKNOWN"
    if re.search(r"publicdomain/zero|\bcc0\b|creative commons 0|public ?domain|\bpd\b", s):
        return "CC0-1.0"
    if "oga-by" in s or "oga by" in s:
        return "OGA-BY"
    if re.search(r"noncommercial|non-commercial|\bby-nc|\bnc\b|/by-nc", s):
        return "CC-BY-NC"
    if re.search(r"noderiv|no deriv|\bby-nd|/by-nd|\bnd\b", s):
        return "CC-BY-ND"
    if re.search(r"sharealike|share-alike|share alike|\bby-sa|/by-sa|\bsa\b", s):
        return "CC-BY-SA"
    if re.search(r"\blgpl\b", s):
        return "LGPL"
    if re.search(r"\bgpl\b", s):
        return "GPL"
    if "editorial" in s or s in ("ed",):
        return "EDITORIAL"
    if re.search(r"asset ?store|unity eula|fab standard|\bfab\b|sonniss|mixamo|pixabay|royalty[- ]free", s):
        return "ROYALTY-FREE"
    if s == "st" or re.search(r"\bstandard\b", s):
        return "STANDARD"
    if re.search(r"attribution|\bcc[- ]?by\b|/licenses/by/|^by$", s):
        return "CC-BY"
    return "UNKNOWN"


def classify(lic: str, commercial: bool, appstore: bool) -> tuple[str, list[str]]:
    """Return (class, notes). class in green|yellow|orange|red|unknown."""
    notes: list[str] = []
    if lic == "CC0-1.0":
        return "green", notes
    if lic == "ROYALTY-FREE":
        return "green", ["no raw-file redistribution - keep out of public repos; check pack page for 'restricted' terms"]
    if lic == "OGA-BY":
        return "yellow", ["credit required"]
    if lic == "CC-BY":
        notes.append("credit required")
        if appstore:
            notes.append("CC-BY anti-DRM clause: debated for App Store/Steam - prefer CC0/OGA-BY or artist waiver")
        return "yellow", notes
    if lic == "CC-BY-SA":
        notes.append("credit required; derivatives must stay CC BY-SA")
        if appstore:
            notes.append("DRM clause applies as with CC-BY")
        return "orange", notes
    if lic == "LGPL":
        return "orange", ["credit + modified asset must stay LGPL"]
    if lic == "GPL":
        if appstore:
            return "red", ["GPL generally considered incompatible with App Store terms"]
        return "orange", ["whole project may need GPL"]
    if lic == "CC-BY-NC":
        return ("red", ["non-commercial only"]) if commercial else ("yellow", ["non-commercial only; credit"])
    if lic == "CC-BY-ND":
        return "red", ["no derivatives - embedding/modifying in a game is risky"]
    if lic in ("EDITORIAL", "STANDARD"):
        return "red", ["not a free-use license"]
    return "unknown", ["license not returned by API - open the page and verify before use"]


def license_display(lic: str, raw: str | None) -> str:
    """Canonical label, keeping the version number from the raw string if present."""
    label = LICENSE_LABELS.get(lic, lic)
    if raw and lic in ("CC-BY", "CC-BY-SA", "OGA-BY"):
        m = re.search(r"([1-4]\.0)", str(raw))
        if m:
            label = f"{label} {m.group(1)}"
    return label


def license_url(lic: str, raw: str | None) -> str | None:
    ver = "4.0"
    m = re.search(r"([1-4]\.0)", str(raw or ""))
    if m:
        ver = m.group(1)
    return {
        "CC0-1.0": "https://creativecommons.org/publicdomain/zero/1.0/",
        "CC-BY": f"https://creativecommons.org/licenses/by/{ver}/",
        "CC-BY-SA": f"https://creativecommons.org/licenses/by-sa/{ver}/",
        "OGA-BY": "https://opengameart.org/content/oga-by-40-faq" if ver == "4.0" else "https://opengameart.org/content/oga-by-30-faq",
    }.get(lic)


def credit_line(rec: dict) -> str:
    lic = rec["license"]
    label = license_display(lic, rec.get("license_raw"))
    author = rec.get("author") or "unknown author"
    base = f'"{rec.get("title")}" by {author} ({rec.get("page_url")}) - {label}'
    if lic in ("CC0-1.0", "ROYALTY-FREE"):
        return base + " (credit optional)"
    return base


# --------------------------------------------------------------------------- #
# HTTP helpers
# --------------------------------------------------------------------------- #


def http_json(url: str, headers: dict | None = None):
    h = {"User-Agent": UA, "Accept": "application/json"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8"))


def first_url(obj):
    """Find the first http(s) URL anywhere inside a nested structure."""
    if isinstance(obj, str):
        return obj if obj.startswith("http") else None
    if isinstance(obj, dict):
        for k in ("url", "href", "downloadLink", "fullDownloadPath"):
            if isinstance(obj.get(k), str) and obj[k].startswith("http"):
                return obj[k]
        for v in obj.values():
            u = first_url(v)
            if u:
                return u
    if isinstance(obj, list):
        for v in obj:
            u = first_url(v)
            if u:
                return u
    return None


def pick(d: dict, *keys, default=None):
    for k in keys:
        if isinstance(d, dict) and d.get(k) not in (None, "", []):
            return d[k]
    return default


def tokens(q: str) -> list[str]:
    return [t for t in re.split(r"[\s,]+", q.lower()) if t]


# --------------------------------------------------------------------------- #
# Providers  -> each returns list[dict] of partially-filled records
# --------------------------------------------------------------------------- #

TYPE_MAP = {
    "polyhaven": {"model": "models", "material": "textures", "texture": "textures", "hdri": "hdris"},
    "ambientcg": {"model": "3d-model", "material": "material", "texture": "material",
                  "hdri": "hdri", "decal": "decal"},
}


def p_polyhaven(q, atype, limit, **_):
    t = TYPE_MAP["polyhaven"].get(atype or "", "all")
    data = http_json(f"https://api.polyhaven.com/assets?type={t}")
    toks = tokens(q)
    scored = []
    for aid, a in data.items():
        hay = " ".join([aid, a.get("name", ""), a.get("description", ""),
                        str(a.get("category", "")), " ".join(a.get("categories", []) or []),
                        " ".join(a.get("tags", []) or [])]).lower()
        # loose stem match: "wooden" -> "wood", "barrels" -> "barr"
        hits = sum(1 for tk in toks if (tk[:4] if len(tk) > 4 else tk) in hay)
        if toks and hits < len(toks):
            continue
        scored.append((hits, a.get("download_count", 0), aid, a))
    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    out = []
    kind = {0: "hdri", 1: "material", 2: "model"}
    for _, _, aid, a in scored[:limit]:
        out.append({
            "source": "polyhaven", "id": aid, "title": a.get("name", aid),
            "type": kind.get(a.get("type"), atype or "?"),
            "license_raw": "CC0",
            "author": ", ".join((a.get("authors") or {}).keys()),
            "page_url": f"https://polyhaven.com/a/{aid}",
            "thumbnail": a.get("thumbnail_url"),
            "download": f"https://api.polyhaven.com/files/{aid}  (send a unique User-Agent)",
            "meta": {k: a.get(k) for k in ("polycount", "max_resolution", "dimensions", "lods") if a.get(k) is not None},
        })
    return out


def p_ambientcg(q, atype, limit, **_):
    params = {"q": q, "limit": str(limit), "sort": "popular",
              "include": "title,url,tags,thumbnails,downloads,technique,type"}
    t = TYPE_MAP["ambientcg"].get(atype or "")
    if t:
        params["type"] = t
    data = http_json("https://ambientcg.com/api/v3/assets?" + urllib.parse.urlencode(params))
    out = []
    for a in data.get("assets", [])[:limit]:
        aid = a.get("id")
        dl = a.get("downloads")
        out.append({
            "source": "ambientcg", "id": aid, "title": pick(a, "title", default=aid),
            "type": pick(a, "type", default=atype or "?"),
            "license_raw": "CC0", "author": "ambientCG",
            "page_url": pick(a, "url", default=f"https://ambientcg.com/view?id={aid}"),
            "thumbnail": first_url(a.get("thumbnails")),
            "download": first_url(dl) or f"https://ambientcg.com/view?id={aid}",
            "meta": {"technique": a.get("technique"), "tags": (a.get("tags") or [])[:8]},
        })
    return out


def p_polypizza(q, atype, limit, **_):
    key = os.environ.get("POLYPIZZA_API_KEY") or os.environ.get("POLY_PIZZA_API_KEY")
    if not key:
        raise PermissionError("no POLYPIZZA_API_KEY - get one at poly.pizza/settings/api")
    url = f"https://api.poly.pizza/v1/search/{urllib.parse.quote(q)}?" + urllib.parse.urlencode({"limit": limit})
    data = http_json(url, {"X-Auth-Token": key})
    items = data.get("results") or data.get("models") or (data if isinstance(data, list) else [])
    out = []
    for m in items[:limit]:
        mid = pick(m, "ID", "id", "Id")
        creator = pick(m, "Creator", "creator", default={}) or {}
        out.append({
            "source": "polypizza", "id": mid, "title": pick(m, "Title", "title", "name", default=mid),
            "type": "model",
            "license_raw": pick(m, "Licence", "License", "licence", "license"),
            "author": pick(creator, "Username", "username", "name", default=None) if isinstance(creator, dict) else creator,
            "page_url": f"https://poly.pizza/m/{mid}",
            "thumbnail": pick(m, "Thumbnail", "thumbnail"),
            "download": pick(m, "Download", "download", "DownloadGLB"),
            "meta": {"tris": pick(m, "Tri Count", "TriCount", "TriangleCount", "triCount"),
                     "animated": pick(m, "Animated", "animated")},
        })
    return out


def p_sketchfab(q, atype, limit, **_):
    params = {"type": "models", "q": q, "downloadable": "true", "count": str(min(limit, 24))}
    data = http_json("https://api.sketchfab.com/v3/search?" + urllib.parse.urlencode(params))
    out = []
    for m in data.get("results", [])[:limit]:
        uid = m.get("uid")
        user = m.get("user") or {}
        thumbs = ((m.get("thumbnails") or {}).get("images") or [])
        thumb = None
        if thumbs:
            thumb = sorted(thumbs, key=lambda i: abs((i.get("width") or 0) - 256))[0].get("url")
        out.append({
            "source": "sketchfab", "id": uid, "title": m.get("name"), "type": "model",
            "license_raw": m.get("license"),
            "author": user.get("username"),
            "page_url": m.get("viewerUrl") or f"https://sketchfab.com/3d-models/{uid}",
            "thumbnail": thumb,
            "download": f"GET https://api.sketchfab.com/v3/models/{uid}/download  (Authorization: Token <your token>)",
            "meta": {"faces": m.get("faceCount"), "vertices": m.get("vertexCount"),
                     "animations": m.get("animationCount")},
        })
    return out


def p_freesound(q, atype, limit, green_only=False, **_):
    key = os.environ.get("FREESOUND_API_KEY")
    if not key:
        raise PermissionError("no FREESOUND_API_KEY - apply at freesound.org/apiv2/apply")
    params = {"query": q, "token": key, "page_size": str(limit),
              "fields": "id,name,username,license,duration,previews,url,tags"}
    if green_only:
        params["filter"] = 'license:"Creative Commons 0"'
    data = http_json("https://freesound.org/apiv2/search/?" + urllib.parse.urlencode(params))
    out = []
    for s in data.get("results", [])[:limit]:
        prev = s.get("previews") or {}
        out.append({
            "source": "freesound", "id": s.get("id"), "title": s.get("name"), "type": "sfx",
            "license_raw": s.get("license"), "author": s.get("username"),
            "page_url": s.get("url") or f"https://freesound.org/s/{s.get('id')}/",
            "thumbnail": None,
            "download": prev.get("preview-hq-ogg") or prev.get("preview-hq-mp3"),
            "meta": {"duration_s": s.get("duration"), "tags": (s.get("tags") or [])[:8],
                     "note": "preview only; original quality needs OAuth2 / manual download"},
        })
    return out


PROVIDERS = {
    "polyhaven": p_polyhaven,
    "ambientcg": p_ambientcg,
    "polypizza": p_polypizza,
    "sketchfab": p_sketchfab,
    "freesound": p_freesound,
}

DEFAULT_BY_TYPE = {
    "model": ["polypizza", "polyhaven", "sketchfab"],
    "material": ["ambientcg", "polyhaven"],
    "texture": ["ambientcg", "polyhaven"],
    "hdri": ["polyhaven", "ambientcg"],
    "decal": ["ambientcg"],
    "sfx": ["freesound"],
    None: ["polyhaven", "ambientcg", "polypizza", "sketchfab"],
}

CLASS_ORDER = {"green": 0, "yellow": 1, "orange": 2, "unknown": 3, "red": 4}


def run(args) -> dict:
    sources = [s.strip() for s in args.sources.split(",")] if args.sources else DEFAULT_BY_TYPE.get(args.type, DEFAULT_BY_TYPE[None])
    result = {"query": args.query, "type": args.type, "date": date.today().isoformat(),
              "flags": {"commercial": args.commercial, "appstore": args.appstore, "green_only": args.green_only},
              "results": [], "errors": {}, "skipped": {}, "filtered_out": 0}
    for src in sources:
        fn = PROVIDERS.get(src)
        if not fn:
            result["errors"][src] = "unknown source"
            continue
        try:
            recs = fn(args.query, args.type, args.limit, green_only=args.green_only)
        except PermissionError as e:
            result["skipped"][src] = str(e)
            continue
        except urllib.error.HTTPError as e:
            result["errors"][src] = f"HTTP {e.code}: {e.reason}"
            continue
        except Exception as e:  # network, JSON, schema drift
            result["errors"][src] = f"{type(e).__name__}: {e}"
            continue
        for r in recs:
            raw = r.get("license_raw")
            if isinstance(raw, dict):
                raw = raw.get("label") or raw.get("slug")
            r["license_raw"] = str(raw) if raw else None
            r["license"] = normalize_license(raw)
            r["license_class"], r["license_notes"] = classify(r["license"], args.commercial, args.appstore)
            r["key"] = f'{r["source"]}:{r["id"]}'
            r["credit"] = credit_line(r)
            if args.green_only and r["license_class"] != "green":
                result["filtered_out"] += 1
                continue
            if args.commercial and r["license_class"] == "red":
                result["filtered_out"] += 1
                continue
            result["results"].append(r)
    result["results"].sort(key=lambda r: CLASS_ORDER.get(r["license_class"], 9))
    return result


ICON = {"green": "🟢", "yellow": "🟡", "orange": "🟠", "red": "🔴", "unknown": "⚪"}


def print_summary(res: dict):
    print(f'# "{res["query"]}"  type={res["type"]}  {res["date"]}  results={len(res["results"])}  filtered_out={res["filtered_out"]}')
    for r in res["results"]:
        meta = ", ".join(f"{k}={v}" for k, v in (r.get("meta") or {}).items() if v not in (None, [], ""))
        print(f'{ICON.get(r["license_class"], "?")} [{r["source"]}] {r["title"]}  - {r["license"]}  - {r.get("author") or "?"}')
        print(f'    {r["page_url"]}')
        if meta:
            print(f"    {meta}")
        for n in r["license_notes"]:
            print(f"    ! {n}")
    for k, v in res["skipped"].items():
        print(f"(skipped {k}: {v})")
    for k, v in res["errors"].items():
        print(f"(error {k}: {v})")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query")
    ap.add_argument("--type", choices=["model", "material", "texture", "hdri", "decal", "sfx"])
    ap.add_argument("--sources", help="comma list: " + ",".join(PROVIDERS))
    ap.add_argument("--limit", type=int, default=8)
    ap.add_argument("--commercial", action="store_true", help="drop red (NC/ND/editorial/GPL-on-appstore)")
    ap.add_argument("--appstore", action="store_true", help="add DRM warnings for CC-BY family")
    ap.add_argument("--green-only", action="store_true", help="CC0 / public domain only")
    ap.add_argument("--out", help="write full JSON here")
    ap.add_argument("--json", action="store_true", help="print JSON instead of summary")
    args = ap.parse_args(argv)
    res = run(args)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print_summary(res)
    return 0 if res["results"] or not res["errors"] else 2


if __name__ == "__main__":
    sys.exit(main())

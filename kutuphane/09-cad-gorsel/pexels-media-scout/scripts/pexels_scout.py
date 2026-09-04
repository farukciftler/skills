#!/usr/bin/env python3
"""
pexels_scout.py — search, score, shortlist and download Pexels media
for music-studio deliverables. Standard library only.

API key resolution order:
  1. PEXELS_API_KEY environment variable
  2. ~/.config/pexels/key   (single line, chmod 600)
The key is never written into output files.

Subcommands
-----------
  search        run one or more queries, score against a preset, emit shortlist
  sheet         build an HTML contact sheet from a shortlist (hotlinked previews)
  download      download chosen candidates + write CREDITS.md / credits.json
  quota         report X-Ratelimit-* headers
  presets       list available deliverable presets

Examples
--------
  python3 pexels_scout.py search --type photo --preset album-cover-3000 \
      -q "vinyl record macro dust" -q "analog mixing console dark" \
      --color "#1c1a17" --out shortlist.json

  python3 pexels_scout.py sheet --shortlist shortlist.json --out sheet.html

  python3 pexels_scout.py download --shortlist shortlist.json \
      --pick 1,4 --out ./assets --project "WEFT-001"
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API_ROOT = "https://api.pexels.com/v1"
CACHE_DIR = Path(os.path.expanduser("~/.cache/pexels_scout"))
CACHE_TTL = 24 * 3600  # Pexels recommends caching responses ~24h
UA = "pexels-media-scout/1.0"

PRESETS_PATH = Path(__file__).with_name("presets.json")

# Heuristic tokens that hint at release/clearance risk. Not a substitute for
# eyeballing the frame — they only decide what gets flagged for human review.
PEOPLE_TOKENS = {
    "man", "woman", "men", "women", "person", "people", "boy", "girl", "guy",
    "lady", "male", "female", "portrait", "face", "faces", "crowd", "audience",
    "singer", "musician", "dj", "band", "performer", "model", "child", "kid",
    "teenager", "couple", "group",
}
BRAND_TOKENS = {
    "logo", "brand", "sign", "signage", "billboard", "label", "poster",
    "artwork", "painting", "mural", "graffiti", "tattoo", "screen", "monitor",
    "laptop", "phone", "iphone", "macbook", "apple", "fender", "gibson",
    "yamaha", "roland", "korg", "moog", "neumann", "shure", "rode", "akai",
    "pioneer", "technics", "spotify", "youtube",
}


# ---------------------------------------------------------------- key + http

def load_key():
    key = os.environ.get("PEXELS_API_KEY", "").strip()
    if key:
        return key
    keyfile = Path(os.path.expanduser("~/.config/pexels/key"))
    if keyfile.is_file():
        key = keyfile.read_text(encoding="utf-8").strip()
        if key:
            return key
    sys.exit(
        "No API key. Set PEXELS_API_KEY, or write the key to "
        "~/.config/pexels/key (chmod 600). Never hardcode it in a file "
        "that gets committed."
    )


def api_get(path, params, key, use_cache=True):
    """GET an API path. Returns (payload, ratelimit_headers)."""
    qs = urllib.parse.urlencode({k: v for k, v in params.items() if v not in (None, "")})
    url = f"{API_ROOT}{path}?{qs}" if qs else f"{API_ROOT}{path}"

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / (hashlib.sha256(url.encode()).hexdigest() + ".json")
    if use_cache and cache_file.is_file():
        if time.time() - cache_file.stat().st_mtime < CACHE_TTL:
            blob = json.loads(cache_file.read_text(encoding="utf-8"))
            return blob["payload"], blob.get("rate", {})

    req = urllib.request.Request(url, headers={"Authorization": key, "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
            rate = {
                "limit": resp.headers.get("X-Ratelimit-Limit"),
                "remaining": resp.headers.get("X-Ratelimit-Remaining"),
                "reset": resp.headers.get("X-Ratelimit-Reset"),
            }
    except urllib.error.HTTPError as e:
        if e.code == 429:
            sys.exit("429 Too Many Requests — hourly (200) or monthly (20k) quota hit. "
                     "Wait for reset or reuse the cache.")
        if e.code in (401, 403):
            sys.exit(f"{e.code} — API key rejected. Check the key is current and not revoked.")
        sys.exit(f"HTTP {e.code} on {path}: {e.read()[:300].decode('utf-8', 'replace')}")
    except urllib.error.URLError as e:
        sys.exit(f"Network error reaching api.pexels.com: {e.reason}")

    cache_file.write_text(json.dumps({"payload": payload, "rate": rate}), encoding="utf-8")
    return payload, rate


# ---------------------------------------------------------------- presets

def load_presets():
    return json.loads(PRESETS_PATH.read_text(encoding="utf-8"))


def get_preset(name):
    presets = load_presets()
    if name not in presets:
        sys.exit(f"Unknown preset '{name}'. Available: {', '.join(sorted(presets))}")
    return presets[name]


# ---------------------------------------------------------------- scoring

def hex_to_rgb(h):
    h = (h or "").lstrip("#")
    if len(h) != 6:
        return None
    try:
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return None


def color_distance(a, b):
    """0.0 = identical, 1.0 = maximally far. Weighted RGB, good enough for mood matching."""
    ra, rb = hex_to_rgb(a), hex_to_rgb(b)
    if not ra or not rb:
        return None
    dr, dg, db = (ra[0] - rb[0]) / 255, (ra[1] - rb[1]) / 255, (ra[2] - rb[2]) / 255
    return min(1.0, (0.30 * dr * dr + 0.59 * dg * dg + 0.11 * db * db) ** 0.5 * 1.6)


def brightness(hex_color):
    rgb = hex_to_rgb(hex_color)
    if not rgb:
        return None
    return (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255


def risk_flags(text, media):
    """Clearance risks that matter when art ships on a commercial release."""
    tokens = set(re.findall(r"[a-z]+", (text or "").lower()))
    flags = []
    if tokens & PEOPLE_TOKENS:
        flags.append("identifiable-person?")
    if tokens & BRAND_TOKENS:
        flags.append("logo/brand/artwork?")
    if media == "video":
        flags.append("audio-track-not-licensed")
    return flags


def score_photo(p, preset, rank, total, brand_color=None):
    tw, th = preset["target_w"], preset["target_h"]
    target_ar = tw / th
    w, h = p.get("width") or 1, p.get("height") or 1
    ar = w / h
    reasons, score = [], 0.0

    # Relevance: Pexels ranks by relevance, so position carries real signal.
    rel = 1.0 - (rank / max(total, 1))
    score += 22 * rel
    reasons.append(f"rank {rank + 1}/{total}")

    # Resolution headroom. Below target is disqualifying-ish; 2x+ is ideal.
    scale = min(w / tw, h / th)
    if scale < 1.0:
        score -= 40
        reasons.append(f"UNDERSIZE {w}x{h} < {tw}x{th}")
    else:
        score += min(28, 14 * scale)
        reasons.append(f"{w}x{h} ({scale:.1f}x target)")

    # Aspect fit: how much of the frame survives the crop.
    keep = min(ar / target_ar, target_ar / ar)
    score += 26 * keep
    if keep < 0.7:
        reasons.append(f"hard crop (keeps {keep * 100:.0f}%)")
    else:
        reasons.append(f"crop-safe ({keep * 100:.0f}%)")

    # Brand palette proximity.
    if brand_color:
        d = color_distance(p.get("avg_color"), brand_color)
        if d is not None:
            score += 16 * (1 - d)
            reasons.append(f"color Δ{d:.2f} vs {brand_color}")

    # Typography headroom: very dark or very bright frames take overlaid text well.
    if preset.get("needs_negative_space"):
        b = brightness(p.get("avg_color"))
        if b is not None:
            if b < 0.30 or b > 0.78:
                score += 8
                reasons.append(f"text-friendly tone (L={b:.2f})")
            else:
                reasons.append(f"midtone, text may fight image (L={b:.2f})")

    flags = risk_flags(p.get("alt", ""), "photo")
    if preset.get("commercial") and "identifiable-person?" in flags:
        score -= 10
    return score, reasons, flags


def score_video(v, preset, rank, total, brand_color=None):
    tw, th = preset["target_w"], preset["target_h"]
    target_ar = tw / th
    w, h = v.get("width") or 1, v.get("height") or 1
    ar = w / h
    dur = v.get("duration") or 0
    reasons, score = [], 0.0

    rel = 1.0 - (rank / max(total, 1))
    score += 20 * rel
    reasons.append(f"rank {rank + 1}/{total}")

    files = [f for f in v.get("video_files", [])
             if f.get("quality") != "hls" and f.get("width")]
    best_w = max((f["width"] for f in files), default=0)
    best_h = max((f["height"] for f in files), default=0)
    scale = min(best_w / tw, best_h / th) if best_w and best_h else 0
    if scale < 1.0:
        score -= 35
        reasons.append(f"UNDERSIZE best file {best_w}x{best_h}")
    else:
        score += min(26, 13 * scale)
        reasons.append(f"best file {best_w}x{best_h} ({scale:.1f}x)")

    keep = min(ar / target_ar, target_ar / ar)
    score += 24 * keep
    reasons.append(f"crop keeps {keep * 100:.0f}%")

    lo = preset.get("min_duration", 0)
    hi = preset.get("max_duration", 10 ** 6)
    if dur < lo:
        score -= 22
        reasons.append(f"too short {dur}s (need ≥{lo}s)")
    elif dur > hi:
        score -= 6
        reasons.append(f"{dur}s — trim to ≤{hi}s")
    else:
        score += 14
        reasons.append(f"{dur}s in range")

    fpss = {round(f.get("fps") or 0, 3) for f in files if f.get("fps")}
    if fpss:
        reasons.append("fps " + "/".join(str(x) for x in sorted(fpss)))
        if preset.get("prefer_fps") and preset["prefer_fps"] in fpss:
            score += 4

    if brand_color:
        d = color_distance(v.get("avg_color"), brand_color)
        if d is not None:
            score += 12 * (1 - d)
            reasons.append(f"color Δ{d:.2f}")

    flags = risk_flags(f"{v.get('url', '')}", "video")
    return score, reasons, flags


# ---------------------------------------------------------------- search

def slug_words(url):
    """Pexels video objects carry no alt text; the slug in the URL is the next best thing."""
    m = re.search(r"/video/([a-z0-9-]+?)-?\d*/?$", url or "")
    return (m.group(1).replace("-", " ") if m else "")


def cmd_search(args):
    key = load_key()
    preset = get_preset(args.preset)
    media = args.type or preset.get("media", "photo")
    if media == "any":
        media = "photo"

    seen, cands, rate = {}, [], {}
    for q in args.query:
        params = {
            "query": q,
            "per_page": args.per_page,
            "page": args.page,
            "orientation": args.orientation or preset.get("orientation"),
            "size": args.size or preset.get("min_size"),
            "locale": args.locale,
        }
        if media == "photo":
            payload, rate = api_get("/search", {**params, "color": args.color_filter}, key,
                                    use_cache=not args.no_cache)
            items = payload.get("photos", [])
        else:
            payload, rate = api_get("/videos/search", params, key, use_cache=not args.no_cache)
            items = payload.get("videos", [])

        total = len(items)
        for i, it in enumerate(items):
            if it["id"] in seen:
                seen[it["id"]]["queries"].append(q)
                continue
            if media == "photo":
                s, reasons, flags = score_photo(it, preset, i, total, args.color)
                author = it.get("photographer")
                author_url = it.get("photographer_url")
                desc = it.get("alt") or ""
                preview = it["src"]["tiny"]
            else:
                s, reasons, flags = score_video(it, preset, i, total, args.color)
                author = (it.get("user") or {}).get("name")
                author_url = (it.get("user") or {}).get("url")
                desc = slug_words(it.get("url"))
                flags = risk_flags(desc, "video")
                preview = it.get("image")

            if args.exclude_people and "identifiable-person?" in flags:
                continue

            rec = {
                "id": it["id"],
                "media": media,
                "score": round(s, 1),
                "why": reasons,
                "flags": flags,
                "description": desc,
                "pexels_url": it.get("url"),
                "author": author,
                "author_url": author_url,
                "width": it.get("width"),
                "height": it.get("height"),
                "duration": it.get("duration"),
                "avg_color": it.get("avg_color"),
                "preview": preview,
                "queries": [q],
                "_raw": it,
            }
            seen[it["id"]] = rec
            cands.append(rec)

    cands.sort(key=lambda r: -r["score"])

    # Variety: cap per contributor so a single shoot can't own the shortlist.
    per_author, kept = {}, []
    for c in cands:
        a = c["author"] or "?"
        if per_author.get(a, 0) >= args.max_per_author:
            continue
        per_author[a] = per_author.get(a, 0) + 1
        kept.append(c)
    kept = kept[: args.limit]

    out = {
        "preset": args.preset,
        "preset_spec": preset,
        "media": media,
        "queries": args.query,
        "brand_color": args.color,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "ratelimit": rate,
        "candidates": kept,
    }
    Path(args.out).write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"{len(kept)} candidates → {args.out}   (quota left: {rate.get('remaining', '?')})")
    for n, c in enumerate(kept, 1):
        dur = f" {c['duration']}s" if c.get("duration") else ""
        print(f"\n{n:2}. [{c['score']:>5}] {c['id']} {c['width']}x{c['height']}{dur}  "
              f"{(c['description'] or '')[:58]}")
        print(f"     {', '.join(c['why'])}")
        if c["flags"]:
            print(f"     ⚠ {', '.join(c['flags'])}")


# ---------------------------------------------------------------- contact sheet

SHEET_CSS = """
body{background:#0e0e10;color:#e8e6e3;font:14px/1.5 -apple-system,BlinkMacSystemFont,
'Segoe UI',sans-serif;margin:0;padding:28px}
h1{font-size:19px;margin:0 0 4px}
.meta{color:#8b8b93;font-size:12px;margin-bottom:22px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:18px}
.card{background:#17171a;border:1px solid #26262b;border-radius:10px;overflow:hidden}
.card img{width:100%;height:170px;object-fit:cover;display:block;background:#222}
.body{padding:10px 12px}
.n{font-weight:600}
.sc{float:right;color:#7fd1a8;font-variant-numeric:tabular-nums}
.why{color:#8b8b93;font-size:11.5px;margin:6px 0 0}
.flag{color:#e0a86b;font-size:11.5px;margin-top:5px}
a{color:#7aa7ff;text-decoration:none;font-size:11.5px}
footer{margin-top:26px;padding-top:14px;border-top:1px solid #26262b;font-size:12px;color:#8b8b93}
"""


def cmd_sheet(args):
    data = json.loads(Path(args.shortlist).read_text(encoding="utf-8"))
    cards = []
    for n, c in enumerate(data["candidates"], 1):
        flags = (f'<div class="flag">⚠ {", ".join(c["flags"])}</div>' if c["flags"] else "")
        dur = f' · {c["duration"]}s' if c.get("duration") else ""
        cards.append(f"""<div class="card">
<a href="{c['pexels_url']}" target="_blank"><img src="{c['preview']}" loading="lazy" alt=""></a>
<div class="body"><span class="sc">{c['score']}</span><span class="n">{n}. {c['id']}</span>
<div class="why">{c['width']}×{c['height']}{dur} · {(c['description'] or '')[:70]}</div>
<div class="why">{'; '.join(c['why'])}</div>{flags}
<div style="margin-top:8px"><a href="{c['pexels_url']}" target="_blank">Pexels ↗</a> ·
<a href="{c['author_url']}" target="_blank">{c['author']}</a></div></div></div>""")

    html = f"""<!doctype html><meta charset="utf-8"><title>Pexels shortlist — {data['preset']}</title>
<style>{SHEET_CSS}</style>
<h1>{data['preset']} — {len(data['candidates'])} candidates</h1>
<div class="meta">{data['media']} · queries: {' | '.join(data['queries'])}
{' · brand ' + data['brand_color'] if data.get('brand_color') else ''} · {data['generated_at']}</div>
<div class="grid">{''.join(cards)}</div>
<footer>Previews are hotlinked and cost no quota.
<a href="https://www.pexels.com">Photos and videos provided by Pexels</a>.</footer>"""
    Path(args.out).write_text(html, encoding="utf-8")
    print(f"contact sheet → {args.out}")


# ---------------------------------------------------------------- download

def pick_photo_url(photo, preset):
    """Prefer 'original' whenever the deliverable needs real pixels; the sized
    variants are capped at 940px wide and will not survive a 3000px cover."""
    tw, th = preset["target_w"], preset["target_h"]
    src = photo["src"]
    if max(tw, th) > 900:
        return src["original"], "original"
    ar = tw / th
    if 0.9 <= ar <= 1.1:
        return src["large2x"], "large2x"
    return (src["landscape"], "landscape") if ar > 1 else (src["portrait"], "portrait")


def pick_video_file(video, preset):
    tw, th = preset["target_w"], preset["target_h"]
    files = [f for f in video.get("video_files", [])
             if f.get("quality") != "hls" and f.get("width") and f.get("height")]
    if not files:
        return None
    ok = [f for f in files if f["width"] >= tw and f["height"] >= th]
    # Smallest file that still clears the target keeps downloads sane.
    return min(ok, key=lambda f: f["width"] * f["height"]) if ok else \
        max(files, key=lambda f: f["width"] * f["height"])


def fetch_binary(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=180) as r, open(dest, "wb") as fh:
        while True:
            chunk = r.read(1 << 16)
            if not chunk:
                break
            fh.write(chunk)
    return dest.stat().st_size


def cmd_download(args):
    data = json.loads(Path(args.shortlist).read_text(encoding="utf-8"))
    preset = data["preset_spec"]
    cands = data["candidates"]
    picks = [int(x) for x in args.pick.split(",")] if args.pick else range(1, len(cands) + 1)

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    project = args.project or data["preset"]
    credits = []

    for n in picks:
        if not 1 <= n <= len(cands):
            print(f"skip {n}: out of range")
            continue
        c = cands[n - 1]
        raw = c["_raw"]
        if c["media"] == "photo":
            url, variant = pick_photo_url(raw, preset)
            ext = ".png" if ".png" in url.split("?")[0] else ".jpg"
        else:
            vf = pick_video_file(raw, preset)
            if not vf:
                print(f"skip {n}: no downloadable file")
                continue
            url, variant = vf["link"], f"{vf['width']}x{vf['height']}-{vf['quality']}"
            ext = ".mp4"

        slug = re.sub(r"[^a-z0-9]+", "-", (c["description"] or "asset").lower()).strip("-")[:40]
        name = f"{project}_{c['id']}_{slug or 'asset'}{ext}"
        dest = outdir / name
        try:
            size = fetch_binary(url, dest)
        except Exception as e:
            print(f"FAIL {n} ({c['id']}): {e}")
            continue

        line = f"{c['media'].capitalize()} by {c['author']} on Pexels — {c['pexels_url']}"
        (outdir / (dest.stem + ".credit.txt")).write_text(line + "\n", encoding="utf-8")
        credits.append({
            "file": name, "id": c["id"], "media": c["media"], "variant": variant,
            "author": c["author"], "author_url": c["author_url"],
            "pexels_url": c["pexels_url"], "flags": c["flags"],
            "attribution": line,
        })
        print(f"✓ {name}  ({size / 1e6:.1f} MB, {variant})")
        if c["flags"]:
            print(f"  ⚠ verify before commercial use: {', '.join(c['flags'])}")

    if not credits:
        return

    # Ayni dizine ikinci bir download yapmak CREDITS.md'yi eziyordu: tekil bir ek
    # indirme, ilk turun kunyelerini siliyor ve kaynagi belirsiz klipler kaliyordu
    # (WR-040'ta yasandi). Once mevcut credits.json okunur, ayni dosya adi
    # tekrarlanmadan birlestirilir.
    existing = outdir / "credits.json"
    if existing.exists():
        try:
            prior = json.loads(existing.read_text(encoding="utf-8"))
        except ValueError:
            prior = []
        fresh = {c["file"] for c in credits}
        credits = [c for c in prior if c.get("file") not in fresh] + credits

    md = [f"# Credits — {project}", "",
          "Assets sourced via the Pexels API. Pexels License: free for commercial and",
          "non-commercial use, no attribution legally required — but the Pexels API",
          "Guidelines require a prominent link back to Pexels wherever these assets appear,",
          "and crediting the creator is expected practice.", "",
          "**Photos and videos provided by [Pexels](https://www.pexels.com).**", ""]
    for c in credits:
        md.append(f"- `{c['file']}` — [{c['author']}]({c['author_url']}) "
                  f"· [source]({c['pexels_url']})"
                  + (f" · ⚠ {', '.join(c['flags'])}" if c["flags"] else ""))
    md += ["", "## Not cleared by the Pexels License",
           "- Recognisable people: no model release is guaranteed. Do not imply endorsement.",
           "- Logos, artwork, tattoos and branded gear visible in frame: separate rights.",
           "- Selling the asset unaltered (print, poster, merch) is prohibited.",
           "- Video: the audio bed of a Pexels clip is **not** cleared — mute and replace it.",
           ]
    (outdir / "CREDITS.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (outdir / "credits.json").write_text(json.dumps(credits, indent=2, ensure_ascii=False),
                                         encoding="utf-8")
    print(f"\nCREDITS.md + credits.json → {outdir}")


# ---------------------------------------------------------------- misc

def cmd_quota(args):
    key = load_key()
    _, rate = api_get("/search", {"query": "test", "per_page": 1}, key, use_cache=False)
    reset = rate.get("reset")
    when = time.strftime("%Y-%m-%d %H:%M", time.localtime(int(reset))) if reset else "?"
    print(f"limit {rate.get('limit')} · remaining {rate.get('remaining')} · resets {when}")


def cmd_presets(args):
    for name, p in sorted(load_presets().items()):
        print(f"{name:22} {p['media']:5} {p['target_w']}x{p['target_h']}  {p.get('note', '')}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search")
    s.add_argument("-q", "--query", action="append", required=True,
                   help="English search query; repeat for variants")
    s.add_argument("--preset", required=True)
    s.add_argument("--type", choices=["photo", "video"])
    s.add_argument("--color", help="brand hex, e.g. #1c1a17 — used for scoring")
    s.add_argument("--color-filter", help="hard Pexels color filter (photos only)")
    s.add_argument("--orientation", choices=["landscape", "portrait", "square"])
    s.add_argument("--size", choices=["large", "medium", "small"])
    s.add_argument("--locale", default="en-US")
    s.add_argument("--per-page", type=int, default=60)
    s.add_argument("--page", type=int, default=1)
    s.add_argument("--limit", type=int, default=12)
    s.add_argument("--max-per-author", type=int, default=2)
    s.add_argument("--exclude-people", action="store_true")
    s.add_argument("--no-cache", action="store_true")
    s.add_argument("--out", default="shortlist.json")
    s.set_defaults(func=cmd_search)

    sh = sub.add_parser("sheet")
    sh.add_argument("--shortlist", required=True)
    sh.add_argument("--out", default="sheet.html")
    sh.set_defaults(func=cmd_sheet)

    d = sub.add_parser("download")
    d.add_argument("--shortlist", required=True)
    d.add_argument("--pick", help="1-based indices, e.g. 1,3,7 (default: all)")
    d.add_argument("--out", default="./assets")
    d.add_argument("--project", help="filename prefix, e.g. WEFT-001")
    d.set_defaults(func=cmd_download)

    q = sub.add_parser("quota")
    q.set_defaults(func=cmd_quota)

    pr = sub.add_parser("presets")
    pr.set_defaults(func=cmd_presets)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

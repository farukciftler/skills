#!/usr/bin/env python3
"""
metadata_audit.py — deterministic gate for functional-audio YouTube metadata.

Checks a title (and optionally description, tags, hashtags, chapters and the
existing catalogue) against the hard field limits, the truncation window, the
health-claim blocklist, duration honesty, and lexical similarity to titles the
channel has already published.

Usage
-----
  python metadata_audit.py --title "432 Hz Sleep Music — 8 Hours of Ney for Deep Rest" \
      --primary-keyword "432 hz sleep music" \
      --duration-seconds 28800 \
      --description-file desc.txt \
      --tags "sleep music, 432 hz, ney music" \
      --hashtags "#sleepmusic #432hz #neyhours" \
      --catalog ../assets/catalog-ledger.csv

  # audit a whole catalogue for templated repetition
  python metadata_audit.py --catalog ledger.csv --audit-catalog

Exit codes: 0 = no FAIL, 1 = at least one FAIL.
Add --json for machine-readable output.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from itertools import combinations
from pathlib import Path

# ---------------------------------------------------------------- limits

TITLE_HARD_MAX = 100
MOBILE_WINDOW = 50          # approx. mobile search truncation
DESKTOP_WINDOW = 70         # approx. desktop search truncation
SHORTS_WINDOW = 40
DESC_BYTE_MAX = 5000
TAGS_CHAR_MAX = 500
HASHTAG_HARD_MAX = 15       # above this, YouTube ignores all hashtags
HASHTAG_SOFT_MAX = 3
ABOVE_FOLD_CHARS = 150
SIM_FAIL = 0.65             # token-set Jaccard against catalogue
SIM_WARN = 0.50
SKELETON_WARN = 3           # same digit-normalised skeleton this many times
DURATION_TOLERANCE = 0.05   # 5% mismatch between claimed and real runtime

# ---------------------------------------------------------------- claim lists
# Tier 1: never. Removal-level risk (treatment claims, discouraging care,
# fabricated clinical authority).
CLAIMS_FAIL = [
    r"\bcures?\b", r"\bcuring\b", r"\bheals? (?:your|the) (?:body|brain|cells|dna|cancer)\b",
    r"\bdna repair\b", r"\bcell(?:ular)? (?:repair|regeneration)\b",
    r"\binstead of (?:medication|therapy|treatment|doctors?|chemo)\b",
    r"\bbetter than (?:medication|therapy|antidepressants|pills)\b",
    r"\bskip the (?:pills|meds|doctor)\b",
    r"\bclinically proven\b", r"\bdoctor[- ](?:recommended|approved)\b",
    r"\bmedically proven\b", r"\bscientifically proven\b",
    r"\bcancer\b", r"\bchemo(?:therapy)?\b",
    r"\btreats? (?:anxiety|depression|insomnia|adhd|autism|dementia|ptsd)\b",
    r"\b(?:anxiety|depression|insomnia|adhd|autism|dementia)\s+(?:cure|treatment|therapy)\b",
]

# Tier 2: avoid. Unqualified physiological outcome claims.
CLAIMS_WARN = [
    r"\bheal(?:s|ing)? (?:you|yourself|trauma|the soul)\b",
    r"\brepairs?\b", r"\bregenerat", r"\bdetox", r"\brewir",
    r"\blowers? (?:your )?(?:blood pressure|heart rate|cortisol)\b",
    r"\bboosts? (?:your )?immun", r"\bbalances? (?:your )?hormones\b",
    r"\bremoves? (?:all )?negative energy\b",
    r"\bactivates? (?:your )?(?:pineal|third eye)\b",
    r"\bmiracle tone\b", r"\bguaranteed\b", r"\bin (?:just )?\d+ (?:minutes|seconds)\b",
    r"\bfall asleep in \d+\b", r"\binstant(?:ly)? (?:relief|calm|sleep)\b",
    r"\bnasa\b", r"\bforbidden frequency\b",
]

STOPWORDS = {
    "a", "an", "and", "at", "for", "from", "in", "of", "on", "or", "the",
    "to", "with", "your", "you", "into", "by",
}

# ---------------------------------------------------------------- helpers


def visible_len(s: str) -> int:
    """Approximate the character count YouTube's counter reports.

    Non-BMP characters (most emoji) commonly count as 2; other non-ASCII
    characters count as 1 but cost extra bytes in the description field.
    """
    n = 0
    for ch in s:
        n += 2 if ord(ch) > 0xFFFF else 1
    return n


def truncate(s: str, n: int) -> str:
    return s if visible_len(s) <= n else s[: max(0, n - 1)].rstrip() + "…"


def normalise(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def tokens(s: str) -> set[str]:
    return {t for t in normalise(s).split() if t and t not in STOPWORDS}


def jaccard(a: str, b: str) -> float:
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def skeleton(s: str) -> str:
    """Digit-normalised shape of a title: catches 'Vol. 12 / 13 / 14'."""
    return re.sub(r"\d+", "#", normalise(s))


def parse_claimed_duration(title: str) -> tuple[int, str] | tuple[None, None]:
    """Return (seconds, matched_text) for a duration token in the title."""
    m = re.search(r"(\d+(?:\.\d+)?)\s*(hours?|hrs?|h\b|minutes?|mins?|min\b|seconds?|secs?)", title, re.I)
    if not m:
        return None, None
    val, unit = float(m.group(1)), m.group(2).lower()
    if unit.startswith(("hour", "hr", "h")):
        return int(val * 3600), m.group(0)
    if unit.startswith(("minute", "min")):
        return int(val * 60), m.group(0)
    return int(val), m.group(0)


def find_claims(text: str, patterns: list[str]) -> list[str]:
    hits = []
    for p in patterns:
        m = re.search(p, text, re.I)
        if m:
            hits.append(m.group(0))
    return hits


def parse_chapters(desc: str) -> list[tuple[int, str]]:
    out = []
    for line in desc.splitlines():
        m = re.match(r"\s*((?:\d{1,2}:)?\d{1,2}:\d{2})\s+(.+)", line)
        if m:
            parts = [int(x) for x in m.group(1).split(":")]
            secs = 0
            for p in parts:
                secs = secs * 60 + p
            out.append((secs, m.group(2).strip()))
    return out


def load_catalog(path: Path) -> list[str]:
    titles: list[str] = []
    if not path.exists():
        return titles
    if path.suffix.lower() in {".csv", ".tsv"}:
        delim = "\t" if path.suffix.lower() == ".tsv" else ","
        with path.open(newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f, delimiter=delim))
        if not rows:
            return titles
        header = [h.strip().lower() for h in rows[0]]
        idx = next((i for i, h in enumerate(header) if "youtube_title" in h or h == "title"), None)
        if idx is None:
            idx = 0
            rows = rows  # treat every row as data
        else:
            rows = rows[1:]
        for r in rows:
            if len(r) > idx and r[idx].strip() and not r[idx].strip().startswith("#"):
                titles.append(r[idx].strip())
    elif path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            for item in data:
                titles.append(item if isinstance(item, str) else str(item.get("youtube_title") or item.get("title", "")))
    else:
        titles = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return [t for t in titles if t]


# ---------------------------------------------------------------- checks


class Report:
    def __init__(self) -> None:
        self.items: list[dict] = []

    def add(self, level: str, check: str, message: str) -> None:
        self.items.append({"level": level, "check": check, "message": message})

    def ok(self, check: str, message: str) -> None:
        self.add("PASS", check, message)

    def warn(self, check: str, message: str) -> None:
        self.add("WARN", check, message)

    def fail(self, check: str, message: str) -> None:
        self.add("FAIL", check, message)

    @property
    def failed(self) -> bool:
        return any(i["level"] == "FAIL" for i in self.items)


def audit_title(r: Report, args, catalog: list[str]) -> None:
    title = args.title
    n = visible_len(title)

    if n > TITLE_HARD_MAX:
        r.fail("title-length", f"{n} chars — over the {TITLE_HARD_MAX} hard cap; YouTube will reject it.")
    elif n > 80:
        r.warn("title-length", f"{n} chars — inside the cap but chars 71–100 are invisible in search.")
    else:
        r.ok("title-length", f"{n} chars.")

    r.ok("truncation-preview",
         f'@{MOBILE_WINDOW}: "{truncate(title, MOBILE_WINDOW)}" | '
         f'@{DESKTOP_WINDOW}: "{truncate(title, DESKTOP_WINDOW)}"'
         + (f' | @{SHORTS_WINDOW}: "{truncate(title, SHORTS_WINDOW)}"' if args.shorts else ""))

    if args.primary_keyword:
        kw = normalise(args.primary_keyword)
        window = MOBILE_WINDOW if not args.shorts else SHORTS_WINDOW
        head = normalise(title[:window])
        full = normalise(title)
        if kw in head:
            r.ok("keyword-position", f'"{args.primary_keyword}" survives the {window}-char window.')
        elif kw in full:
            r.fail("keyword-position",
                   f'"{args.primary_keyword}" appears but is cut off before char {window}. Move it to the front.')
        else:
            r.fail("keyword-position",
                   f'"{args.primary_keyword}" does not appear in the title at all (allowing for word order).')

    emoji = [c for c in title if ord(c) > 0x2100]
    if emoji:
        pre = title.split(emoji[0])[0]
        if len(pre.strip()) == 0:
            r.fail("emoji", f"title opens with {''.join(emoji[:3])} — decoration before the keyword costs the mobile window.")
        elif len(emoji) > 1:
            r.warn("emoji", f"{len(emoji)} emoji ({''.join(emoji[:5])}); one at most, and only if informative.")
        else:
            r.ok("emoji", f"one emoji ({emoji[0]}), not leading.")

    caps = [w for w in re.findall(r"[A-Za-z]{3,}", title) if w.isupper()]
    if len(caps) > 1:
        r.warn("caps", f"ALL-CAPS words: {', '.join(caps)} — reads as clickbait.")

    if len(re.findall(r"[!?]", title)) > 1:
        r.warn("punctuation", "multiple ! or ? — clickbait signal.")

    seps = {s for s in ["—", "|", "·", "-", ":"] if s in title}
    if len(seps) > 2:
        r.warn("separators", f"mixed separators {' '.join(sorted(seps))}; pick one style per channel.")

    # duration honesty
    claimed, matched = parse_claimed_duration(title)
    if args.duration_seconds and claimed:
        diff = abs(claimed - args.duration_seconds) / max(args.duration_seconds, 1)
        if diff > DURATION_TOLERANCE:
            r.fail("duration-promise",
                   f'title says "{matched}" (~{claimed}s) but the file is {args.duration_seconds}s '
                   f"({diff*100:.0f}% off) — misleading metadata and a retention problem.")
        else:
            r.ok("duration-promise", f'"{matched}" matches the {args.duration_seconds}s file.')
    elif args.duration_seconds and not claimed:
        r.warn("duration-promise", "no duration token in the title; duration is a searched keyword in this niche.")
    elif claimed and not args.duration_seconds:
        r.warn("duration-promise", f'title claims "{matched}" — pass --duration-seconds to verify it.')

    # claims
    haystack = title + "\n" + (args.description or "")
    f_hits = find_claims(haystack, CLAIMS_FAIL)
    w_hits = find_claims(haystack, CLAIMS_WARN)
    if f_hits:
        r.fail("claims-tier1", f"{', '.join(repr(h) for h in f_hits)} — treatment/authority claim. See claims-and-policy.md.")
    if w_hits:
        r.warn("claims-tier2", f"{', '.join(repr(h) for h in w_hits)} — body-outcome language; rewrite as design or intent.")
    if not f_hits and not w_hits:
        r.ok("claims", "no blocklisted claim language in title or description.")

    # catalogue similarity
    if catalog:
        scored = sorted(((jaccard(title, t), t) for t in catalog), reverse=True)
        top = scored[0]
        if top[0] >= SIM_FAIL:
            r.fail("duplication", f'{top[0]:.2f} similarity to "{top[1]}" — reads as a template swap.')
        elif top[0] >= SIM_WARN:
            r.warn("duplication", f'{top[0]:.2f} similarity to "{top[1]}" — vary the texture slot further.')
        else:
            r.ok("duplication", f"max similarity {top[0]:.2f} across {len(catalog)} catalogue titles.")

        sk = skeleton(title)
        reps = sum(1 for t in catalog if skeleton(t) == sk)
        if reps >= SKELETON_WARN:
            r.fail("skeleton", f"this exact title shape already used {reps}× (digits ignored) — templated catalogue signal.")
        elif reps:
            r.warn("skeleton", f"title shape already used {reps}× in the catalogue.")


def audit_pack(r: Report, args) -> None:
    if args.description:
        desc = args.description
        b = len(desc.encode("utf-8"))
        if b > DESC_BYTE_MAX:
            r.fail("description-bytes", f"{b} bytes — over the {DESC_BYTE_MAX}-byte limit (non-ASCII costs 2–4 bytes/char).")
        else:
            r.ok("description-bytes", f"{b} bytes of {DESC_BYTE_MAX}.")

        fold = desc[:ABOVE_FOLD_CHARS]
        if args.primary_keyword and normalise(args.primary_keyword) not in normalise(fold):
            r.warn("above-fold", f"primary keyword missing from the first {ABOVE_FOLD_CHARS} chars of the description.")
        else:
            r.ok("above-fold", "primary phrase present above the fold.")

        chapters = parse_chapters(desc)
        if chapters:
            problems = []
            if chapters[0][0] != 0:
                problems.append("first timestamp is not 00:00")
            if len(chapters) < 3:
                problems.append(f"only {len(chapters)} chapters (3 minimum)")
            for (a_s, a_t), (b_s, _) in zip(chapters, chapters[1:]):
                if b_s - a_s < 10:
                    problems.append(f'"{a_t}" runs under 10s')
                if b_s <= a_s:
                    problems.append("timestamps not ascending")
            if problems:
                r.fail("chapters", "; ".join(dict.fromkeys(problems)) + " — chapters will not render.")
            else:
                r.ok("chapters", f"{len(chapters)} valid chapters, first at 00:00.")
        else:
            r.warn("chapters", "no chapters found; named sections are the cheapest curation signal in long-form.")

    if args.hashtags:
        tags_found = re.findall(r"#\w+", args.hashtags)
        if len(tags_found) > HASHTAG_HARD_MAX:
            r.fail("hashtags", f"{len(tags_found)} hashtags — above {HASHTAG_HARD_MAX} YouTube ignores all of them.")
        elif len(tags_found) > HASHTAG_SOFT_MAX:
            r.warn("hashtags", f"{len(tags_found)} hashtags; 2–3 is the working number (first 3 render above the title).")
        else:
            r.ok("hashtags", f"{len(tags_found)} hashtags: {' '.join(tags_found)}")

    if args.tags:
        raw = [t.strip() for t in args.tags.split(",") if t.strip()]
        total = len(", ".join(raw))
        if total > TAGS_CHAR_MAX:
            r.fail("tags", f"{total} chars — over the {TAGS_CHAR_MAX}-char combined budget.")
        elif len(raw) > 20:
            r.warn("tags", f"{len(raw)} tags; tags carry minimal weight now — 5–10 focused ones is enough.")
        else:
            r.ok("tags", f"{len(raw)} tags, {total} of {TAGS_CHAR_MAX} chars.")


def audit_catalog_only(r: Report, catalog: list[str]) -> None:
    if len(catalog) < 2:
        r.warn("catalog", "fewer than two titles; nothing to compare.")
        return
    pairs = sorted(((jaccard(a, b), a, b) for a, b in combinations(catalog, 2)), reverse=True)
    bad = [p for p in pairs if p[0] >= SIM_FAIL]
    mid = [p for p in pairs if SIM_WARN <= p[0] < SIM_FAIL]
    if bad:
        r.fail("catalog-duplication",
               f"{len(bad)} title pairs at or above {SIM_FAIL:.2f} similarity. Worst: "
               + " || ".join(f'{s:.2f} "{a}" ~ "{b}"' for s, a, b in bad[:5]))
    if mid:
        r.warn("catalog-duplication", f"{len(mid)} pairs between {SIM_WARN:.2f} and {SIM_FAIL:.2f}.")
    if not bad and not mid:
        r.ok("catalog-duplication", f"{len(catalog)} titles, max pairwise similarity {pairs[0][0]:.2f}.")

    shapes: dict[str, int] = {}
    for t in catalog:
        shapes[skeleton(t)] = shapes.get(skeleton(t), 0) + 1
    repeated = {k: v for k, v in shapes.items() if v >= SKELETON_WARN}
    if repeated:
        r.fail("catalog-skeleton",
               f"{len(repeated)} title shape(s) repeated {SKELETON_WARN}+ times: "
               + "; ".join(f'"{k}" ×{v}' for k, v in sorted(repeated.items(), key=lambda x: -x[1])[:5]))
    else:
        r.ok("catalog-skeleton", f"{len(shapes)} distinct title shapes across {len(catalog)} titles.")

    claim_rows = [(t, find_claims(t, CLAIMS_FAIL), find_claims(t, CLAIMS_WARN)) for t in catalog]
    t1 = [(t, h) for t, h, _ in claim_rows if h]
    t2 = [(t, h) for t, _, h in claim_rows if h]
    if t1:
        r.fail("catalog-claims", f"{len(t1)} titles carry tier-1 claims. e.g. " +
               "; ".join(f'"{t}" → {h}' for t, h in t1[:4]))
    if t2:
        r.warn("catalog-claims", f"{len(t2)} titles carry tier-2 claims. e.g. " +
               "; ".join(f'"{t}" → {h}' for t, h in t2[:4]))
    if not t1 and not t2:
        r.ok("catalog-claims", "no blocklisted claim language across the catalogue.")


# ---------------------------------------------------------------- main


def main() -> int:
    p = argparse.ArgumentParser(description="Audit functional-audio YouTube metadata.")
    p.add_argument("--title")
    p.add_argument("--primary-keyword")
    p.add_argument("--duration-seconds", type=int)
    p.add_argument("--description")
    p.add_argument("--description-file")
    p.add_argument("--tags")
    p.add_argument("--hashtags")
    p.add_argument("--catalog", help="CSV/JSON/TXT of existing titles (CSV needs a youtube_title or title column)")
    p.add_argument("--audit-catalog", action="store_true", help="audit the whole catalogue instead of one title")
    p.add_argument("--shorts", action="store_true", help="use the ~40-char Shorts truncation window")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    if args.description_file:
        args.description = Path(args.description_file).read_text(encoding="utf-8")

    catalog = load_catalog(Path(args.catalog)) if args.catalog else []
    r = Report()

    if args.audit_catalog:
        if not catalog:
            print("No catalogue titles loaded.", file=sys.stderr)
            return 1
        audit_catalog_only(r, catalog)
    else:
        if not args.title:
            print("--title is required (or use --audit-catalog).", file=sys.stderr)
            return 1
        audit_title(r, args, catalog)
        audit_pack(r, args)

    if args.json:
        print(json.dumps({"failed": r.failed, "items": r.items}, ensure_ascii=False, indent=2))
    else:
        icons = {"PASS": "  ok ", "WARN": "WARN ", "FAIL": "FAIL "}
        width = max(len(i["check"]) for i in r.items)
        for i in r.items:
            print(f'{icons[i["level"]]} {i["check"]:<{width}}  {i["message"]}')
        fails = sum(1 for i in r.items if i["level"] == "FAIL")
        warns = sum(1 for i in r.items if i["level"] == "WARN")
        print(f'\n{"BLOCKED" if fails else "CLEAR"} — {fails} fail, {warns} warn.')
    return 1 if r.failed else 0


if __name__ == "__main__":
    sys.exit(main())

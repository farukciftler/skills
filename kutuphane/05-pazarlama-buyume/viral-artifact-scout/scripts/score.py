#!/usr/bin/env python3
"""Rank viral-artifact candidates on the six-factor rubric.

Usage:
    python3 score.py candidates.json [--explain] [--lang tr|en]

Input: a JSON list of candidate objects. Each factor is scored 1-5.

    [
      {
        "name": "Dizi Fisi",
        "feasibility": 4,   # can you legally get the data today, as a small builder
        "virality": 5,      # how many of the five ingredients it has
        "tr_gap": 5,        # Phase 3 gap-cause quality (5 = cause 6, evidenced)
        "money": 3,         # realistic monetization model fit
        "build": 4,         # cheapness/speed of v1 (5 = a weekend)
        "durability": 3,    # survives policy change + has a recurrence pattern
        "note": "one line"
      }
    ]

Output: a ranked markdown table, ready to paste into the dossier.
"""

import argparse
import json
import sys

WEIGHTS = {
    "feasibility": 3,
    "virality": 3,
    "tr_gap": 2,
    "money": 2,
    "build": 2,
    "durability": 1,
}

MAX_TOTAL = sum(w * 5 for w in WEIGHTS.values())  # 65

LABELS = {
    "en": {
        "feasibility": "Feasibility",
        "virality": "Virality",
        "tr_gap": "TR gap",
        "money": "Money path",
        "build": "Build cost",
        "durability": "Durability",
        "name": "Candidate",
        "total": "Score",
        "verdict": "Verdict",
        "note": "Note",
        "bands": [
            (50, "build it"),
            (40, "prototype"),
            (35, "maybe"),
            (0, "eliminate"),
        ],
        "veto": "ELIMINATE — no data path",
    },
    "tr": {
        "feasibility": "Yapılabilirlik",
        "virality": "Viralite",
        "tr_gap": "TR boşluğu",
        "money": "Para yolu",
        "build": "Yapım maliyeti",
        "durability": "Dayanıklılık",
        "name": "Aday",
        "total": "Skor",
        "verdict": "Karar",
        "note": "Not",
        "bands": [
            (50, "yap"),
            (40, "prototip"),
            (35, "belki"),
            (0, "ele"),
        ],
        "veto": "ELENDİ — veri yolu yok",
    },
}


def verdict(candidate, total, lang):
    # Hard gate: a candidate with no legal data path is dead no matter how
    # good the artifact would have been. This is the modal cause of death in
    # this category, so it overrides the weighted score rather than being
    # averaged away by it.
    if candidate["feasibility"] <= 1:
        return lang["veto"]
    for threshold, label in lang["bands"]:
        if total >= threshold:
            return label
    return lang["bands"][-1][1]


def validate(candidate, index):
    problems = []
    if not candidate.get("name"):
        problems.append(f"candidate #{index}: missing 'name'")
    for factor in WEIGHTS:
        value = candidate.get(factor)
        if value is None:
            problems.append(f"{candidate.get('name', f'#{index}')}: missing '{factor}'")
        elif not isinstance(value, (int, float)) or not 1 <= value <= 5:
            problems.append(
                f"{candidate.get('name', f'#{index}')}: '{factor}' must be 1-5, got {value!r}"
            )
    return problems


def score(candidate):
    return sum(WEIGHTS[f] * candidate[f] for f in WEIGHTS)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="JSON file with the candidate list")
    parser.add_argument(
        "--explain",
        action="store_true",
        help="show per-factor weighted contributions",
    )
    parser.add_argument("--lang", choices=["tr", "en"], default="tr")
    args = parser.parse_args()

    try:
        with open(args.path, encoding="utf-8") as fh:
            candidates = json.load(fh)
    except FileNotFoundError:
        sys.exit(f"File not found: {args.path}")
    except json.JSONDecodeError as exc:
        sys.exit(f"Invalid JSON in {args.path}: {exc}")

    if not isinstance(candidates, list) or not candidates:
        sys.exit("Expected a non-empty JSON list of candidate objects.")

    problems = []
    for i, candidate in enumerate(candidates, 1):
        if not isinstance(candidate, dict):
            problems.append(f"candidate #{i} is not an object")
            continue
        problems.extend(validate(candidate, i))
    if problems:
        sys.exit("Input problems:\n  " + "\n  ".join(problems))

    lang = LABELS[args.lang]
    ranked = sorted(candidates, key=score, reverse=True)

    headers = [lang["name"]] + [lang[f] for f in WEIGHTS] + [lang["total"], lang["verdict"]]
    print("| " + " | ".join(headers) + " |")
    print("|" + "|".join(["---"] * len(headers)) + "|")

    for candidate in ranked:
        total = score(candidate)
        cells = [candidate["name"]]
        for factor in WEIGHTS:
            if args.explain:
                cells.append(f"{candidate[factor]} (×{WEIGHTS[factor]}={WEIGHTS[factor] * candidate[factor]})")
            else:
                cells.append(str(candidate[factor]))
        cells.append(f"**{total}**/{MAX_TOTAL}")
        cells.append(verdict(candidate, total, lang))
        print("| " + " | ".join(cells) + " |")

    notes = [c for c in ranked if c.get("note")]
    if notes:
        print()
        for candidate in notes:
            print(f"- **{candidate['name']}** — {candidate['note']}")


if __name__ == "__main__":
    main()

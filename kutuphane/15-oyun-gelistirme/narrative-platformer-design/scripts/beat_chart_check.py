#!/usr/bin/env python3
"""
beat_chart_check.py - validate pacing of a platformer beat chart and draw an
ASCII intensity / story-tension curve.

CSV columns (see assets/beat-chart-template.csv):
  id, chapter, location, kishotenketsu, mechanic, new_mechanic, intensity,
  story_tension, story_beat, delivery, control_loss_sec, checkpoint,
  est_minutes, music, notes

delivery values: none | bark | bubble | dialogue | cutscene | environment | collectible

Usage:
  python3 beat_chart_check.py beats.csv [--peak 7] [--max-run 3] [--max-control 45]
"""
import argparse
import csv
import sys
from collections import defaultdict

HEAVY = {"dialogue", "cutscene"}


def num(v, default=0.0):
    try:
        return float(str(v).strip())
    except (TypeError, ValueError):
        return default


def yes(v):
    return str(v).strip().lower() in {"yes", "y", "true", "1", "evet"}


def load(path):
    with open(path, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["_i"] = int(num(r.get("intensity")))
        r["_t"] = int(num(r.get("story_tension")))
        r["_d"] = (r.get("delivery") or "none").strip().lower()
        r["_c"] = num(r.get("control_loss_sec"))
        r["_m"] = num(r.get("est_minutes"))
        r["_ch"] = str(r.get("chapter", "")).strip()
    return rows


def check(rows, peak=7, max_run=3, max_control=45):
    issues = []

    def add(sev, rid, rule, fix):
        issues.append((sev, rid, rule, fix))

    run = 0
    for idx, r in enumerate(rows):
        rid = r.get("id", f"row{idx + 2}")
        nxt = rows[idx + 1:idx + 3]
        # story on a peak
        if r["_d"] in HEAVY and r["_i"] >= peak:
            add("HIGH", rid, f"{r['_d']} at intensity {r['_i']} (momentum break)",
                "move words to the valley after this segment; keep peaks wordless")
        # consecutive peaks
        run = run + 1 if r["_i"] >= peak else 0
        if run == max_run + 1:
            add("MED", rid, f"{run} high-intensity segments in a row (no breather)",
                "insert a low-intensity breather / story valley")
        # missing release after a spike
        if r["_i"] >= peak + 1 and nxt and not any(n["_i"] <= 4 for n in nxt):
            add("MED", rid, f"spike {r['_i']} with no release in next {len(nxt)} rows",
                "follow spikes with intensity <= 4 within two segments")
        # unsafe new mechanic
        if yes(r.get("new_mechanic")) and r["_i"] >= 6:
            add("HIGH", rid, f"new mechanic '{r.get('mechanic', '')}' introduced at intensity {r['_i']}",
                "add a safe Ki segment first (no death risk)")
        # long control loss
        if r["_c"] > max_control:
            add("MED", rid, f"control loss {r['_c']:.0f}s",
                f"trim below {max_control}s, split, or make semi-interactive")
        # retry punishes story
        if r["_d"] in HEAVY and r["_c"] > 0:
            following = rows[idx + 1] if idx + 1 < len(rows) else None
            if following is not None and not yes(following.get("checkpoint")):
                add("HIGH", following.get("id", "?"),
                    "no checkpoint after unskippable story",
                    "checkpoint after the scene or make it skippable on repeat")
        # high tension with no delivery
        if r["_t"] >= 8 and r["_d"] == "none":
            add("MED", rid, f"story tension {r['_t']} but delivery=none",
                "deliver via environment/bark/animation, or lower the tension value")
        # beat with no delivery
        if (r.get("story_beat") or "").strip() and r["_d"] == "none":
            add("LOW", rid, "story_beat written but delivery=none", "say how the player receives it")

    # chapter-level
    chapters = defaultdict(list)
    for r in rows:
        chapters[r["_ch"]].append(r)
    for ch, rs in chapters.items():
        last = rs[-1]
        if last["_i"] <= 3 and last["_t"] <= 3 and "epilogue" not in (last.get("notes") or "").lower():
            add("MED", last.get("id", "?"), f"chapter {ch} ends flat",
                "end on a question, a reveal, or a peak followed by a short valley")
        ctrl = sum(r["_c"] for r in rs)
        mins = sum(r["_m"] for r in rs) or 0
        if mins and ctrl / (mins * 60) > 0.10:
            add("MED", f"ch{ch}", f"control loss {ctrl:.0f}s = {100 * ctrl / (mins * 60):.0f}% of chapter time",
                "light story platformer target: <= 10%")
        if not any(r.get("kishotenketsu", "").strip().lower() == "ten" for r in rs):
            add("LOW", f"ch{ch}", f"chapter {ch} has no 'ten' (twist) segment",
                "twist the chapter mechanic before the mastery test")
        if not any(r["_d"] != "none" for r in rs):
            add("LOW", f"ch{ch}", f"chapter {ch} delivers no story at all", "fine only if intentional")
    return issues


def chart(rows):
    out = ["id        intensity   (T = story tension position)"]
    for r in rows:
        i, t = max(0, min(10, r["_i"])), max(0, min(10, r["_t"]))
        cells = ["\u2588" if k < i else " " for k in range(10)]
        if 1 <= t <= 10:
            cells[t - 1] = "T" if cells[t - 1] == " " else "\u25c6"
        tag = r["_d"] if r["_d"] != "none" else ""
        if r["_d"] in HEAVY:
            tag = tag.upper()
        out.append(f"{r.get('id', ''):<9} |{''.join(cells)}| {i:>2}/{t:<2} {tag}")
    out.append("legend: \u2588 intensity, T tension, \u25c6 tension inside bar, CAPS = control-taking delivery")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--peak", type=int, default=7)
    ap.add_argument("--max-run", type=int, default=3)
    ap.add_argument("--max-control", type=float, default=45)
    a = ap.parse_args()
    rows = load(a.path)
    if not rows:
        print("Empty beat chart.")
        sys.exit(2)
    print(chart(rows))
    issues = check(rows, a.peak, a.max_run, a.max_control)
    total_min = sum(r["_m"] for r in rows)
    ctrl = sum(r["_c"] for r in rows)
    print(f"\nRows: {len(rows)} | est. time: {total_min:.0f} min | control loss: {ctrl:.0f}s")
    if not issues:
        print("No pacing flags.")
        return
    order = {"HIGH": 0, "MED": 1, "LOW": 2}
    for sev, rid, rule, fix in sorted(issues, key=lambda x: order[x[0]]):
        print(f"[{sev}] {rid}: {rule}\n        -> {fix}")


if __name__ == "__main__":
    main()

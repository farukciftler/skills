#!/usr/bin/env python3
"""ASO arithmetic: funnel diagnosis, A/B test sizing, keyword prioritization.

These three calculations show up in every engagement and all three are easy to get
subtly wrong by hand -- particularly the test sizing, where an underpowered test that
"loses" is worse than no test because teams treat it as evidence.

Commands
--------
  funnel     Split an ASO problem into visibility / first-impression / page conversion
  sample     Required sample per variant, and how long the app's traffic will take
  priority   Score and rank keywords on volume x relevance x achievability x headroom

Examples
--------
  python3 aso_calc.py funnel --impressions 480000 --page-views 42000 --downloads 9800
  python3 aso_calc.py sample --baseline-cvr 0.28 --mde 0.10 --daily-traffic 6000 --variants 2
  python3 aso_calc.py priority --csv keywords.csv
"""

import argparse
import csv
import math
import sys

# Normal quantiles, so the module stays dependency-free.
_Z = {0.80: 0.8416, 0.90: 1.2816, 0.95: 1.6449, 0.98: 2.0537, 0.99: 2.3263}


_Z_TWO_SIDED = {0.90: 1.6449, 0.95: 1.9600, 0.98: 2.3263, 0.99: 2.5758}


def z_two_sided(confidence):
    return _Z_TWO_SIDED.get(confidence, 1.9600)


# ---------------------------------------------------------------- funnel

def cmd_funnel(a):
    imp, pv, dl = int(a.impressions), int(a.page_views), int(a.downloads)
    if imp <= 0:
        sys.exit("impressions must be > 0")

    tap_through = pv / imp
    page_cvr = dl / pv if pv else 0.0
    apple_cvr = dl / imp

    print("\n=== ASO funnel ===")
    print(f"Impressions (unique devices) : {imp:,}")
    print(f"Product page views           : {pv:,}   ({tap_through:.2%} of impressions)")
    print(f"First-time downloads         : {dl:,}   ({page_cvr:.2%} of page views)")
    print(f"Store-reported CVR           : {apple_cvr:.2%}   (downloads / impressions)")

    print("\nNote: Apple counts product page views *inside* impressions, so tap-through is "
          "a ratio, not a disjoint split. A large share of installs happen straight from "
          "the search card with no page view at all.")

    print("\n--- Where the problem is ---")
    if imp < a.impression_floor:
        print(f"• VISIBILITY. {imp:,} impressions is below the {a.impression_floor:,} floor for "
              "this analysis to say anything about conversion. Work keywords, category, "
              "browse surfaces and tags first — conversion work on thin traffic is unmeasurable.")
    if tap_through < 0.10:
        print(f"• FIRST IMPRESSION ({tap_through:.1%} tap-through). The search-results card is "
              "losing people: icon, app name, subtitle, star rating, and the first 1–3 "
              "screenshots or the autoplaying preview. This is where icon and hero-frame wins "
              "show up — not in page conversion.")
    elif tap_through > 0.35:
        print(f"• Tap-through is strong ({tap_through:.1%}). The card is doing its job.")
    if pv and page_cvr < 0.20:
        print(f"• PAGE CONVERSION ({page_cvr:.1%}). People arrive and don't install: full "
              "screenshot set, video, rating and review content, description, price. Check the "
              "rating first — below 4.0 is a hard ceiling and a featuring disqualifier.")
    elif pv and page_cvr > 0.40:
        print(f"• Page conversion is strong ({page_cvr:.1%}). The bottleneck is upstream — "
              "you need more qualified impressions, not a better page.")

    print("\nBefore concluding: check for a recent release, price change, seasonality, a "
          "competitor launch, store featuring, or an inventory change (e.g. more paid slots "
          "in search results compressing organic impressions). Most 'mysterious' movements "
          "are an unlogged event.\n")


# ---------------------------------------------------------------- sample size

def cmd_sample(a):
    p = a.baseline_cvr
    if not 0 < p < 1:
        sys.exit("--baseline-cvr must be a proportion between 0 and 1 (e.g. 0.28)")
    rel = a.mde
    p2 = p * (1 + rel)
    if p2 >= 1:
        sys.exit("baseline x (1 + mde) exceeds 100%")

    z_a = z_two_sided(a.confidence)
    z_b = _Z.get(a.power, _Z[0.80])
    pbar = (p + p2) / 2

    n = ((z_a * math.sqrt(2 * pbar * (1 - pbar)) + z_b * math.sqrt(p * (1 - p) + p2 * (1 - p2))) ** 2
         / (p2 - p) ** 2)
    n = math.ceil(n)

    total = n * a.variants
    print("\n=== A/B test sizing ===")
    print(f"Baseline conversion   : {p:.2%}")
    print(f"Target relative lift  : {rel:+.1%}  (→ {p2:.2%})")
    print(f"Confidence / power    : {a.confidence:.0%} two-sided / {a.power:.0%}")
    print(f"Arms (control + treat): {a.variants}")
    print(f"\nRequired per arm      : {n:,}")
    print(f"Required total        : {total:,}")

    if a.daily_traffic:
        share = a.traffic_share
        daily_in_test = a.daily_traffic * share
        days = math.ceil(total / daily_in_test) if daily_in_test else 0
        weeks = math.ceil(days / 7)
        print(f"\nAt {a.daily_traffic:,}/day × {share:.0%} allocated → {daily_in_test:,.0f}/day in test")
        weeks = max(weeks, 1)  # never call a creative test on less than a full week
        print(f"Duration              : ~{days} days of traffic → run {weeks * 7} days "
              f"({weeks} whole week{'s' if weeks > 1 else ''})")
        if days > 90:
            print("\n⚠️  Over Apple's 90-day PPO cap. Options: raise the traffic proportion, cut "
                  "to a single treatment, test a bigger swing, or ship the change on judgment "
                  "and measure with a geo holdout instead.")
        elif days > 28:
            print("\n⚠️  Long test. Seasonality and competitor moves will contaminate it. Prefer "
                  "a bolder variant with a larger expected effect.")
    print("\nAlways run whole weeks — day-of-week effects on store traffic are large. Set "
          "confidence and MDE before launch and don't stop early; peeking inflates false "
          "positives. Apple's PPO fixes confidence at 90%, which is roughly double the "
          "false-positive rate of the 95% standard.\n")


# ---------------------------------------------------------------- priority

def cmd_priority(a):
    rows = []
    with open(a.csv, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    if not rows:
        sys.exit("no rows found")

    def num(r, *names, default=0.0):
        for n in names:
            if n in r and str(r[n]).strip():
                try:
                    return float(str(r[n]).strip())
                except ValueError:
                    pass
        return default

    vols = [num(r, "volume", "popularity", "search_volume") for r in rows]
    vmax = max(vols) or 1.0

    scored = []
    for r in rows:
        kw = (r.get("keyword") or r.get("term") or "").strip()
        vol = num(r, "volume", "popularity", "search_volume")
        rel = num(r, "relevance", "relevancy", default=50.0)
        chance = num(r, "chance", "achievability", default=50.0)
        rank = num(r, "rank", "current_rank", default=0.0)

        # Headroom: ranks 4-15 are the highest-ROI band -- close enough to move, far
        # enough from the top that there is real traffic to win.
        if rank <= 0 or rank > 50:
            gap = 1.0
        elif rank <= 3:
            gap = 0.3
        elif rank <= 15:
            gap = 2.0
        else:
            gap = 1.5

        score = ((vol / vmax) ** a.w_volume
                 * (rel / 100) ** a.w_relevance
                 * (chance / 100) ** a.w_chance
                 * gap)
        scored.append((score, kw, vol, rel, chance, int(rank), gap))

    scored.sort(reverse=True)
    print("\n=== Keyword priority ===")
    print(f"weights: volume^{a.w_volume} × relevance^{a.w_relevance} × chance^{a.w_chance} × rank headroom")
    print("relevance is deliberately over-weighted — volume without relevance is traffic that "
          "doesn't convert.\n")
    print(f"{'#':>3}  {'score':>6}  {'keyword':<28} {'vol':>6} {'rel':>5} {'chnc':>5} {'rank':>5} {'gap':>4}")
    print("-" * 76)
    for i, (s, kw, v, rel, c, rank, gap) in enumerate(scored[:a.top], 1):
        print(f"{i:>3}  {s:>6.3f}  {kw:<28} {v:>6.0f} {rel:>5.0f} {c:>5.0f} "
              f"{(rank or '-'):>5} {gap:>4.1f}")
    print(f"\n{len(scored)} keywords scored. Explain the weights in the deliverable — a "
          "black-box priority number is not a recommendation.\n")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("funnel", help="Diagnose which funnel stage is the problem")
    f.add_argument("--impressions", type=float, required=True)
    f.add_argument("--page-views", type=float, required=True)
    f.add_argument("--downloads", type=float, required=True)
    f.add_argument("--impression-floor", type=int, default=20000)
    f.set_defaults(func=cmd_funnel)

    s = sub.add_parser("sample", help="Sample size and duration for a creative A/B test")
    s.add_argument("--baseline-cvr", type=float, required=True, help="e.g. 0.28")
    s.add_argument("--mde", type=float, default=0.10, help="minimum detectable RELATIVE lift, e.g. 0.10")
    s.add_argument("--confidence", type=float, default=0.95, choices=[0.90, 0.95, 0.98, 0.99])
    s.add_argument("--power", type=float, default=0.80, choices=[0.80, 0.90])
    s.add_argument("--variants", type=int, default=2, help="total arms incl. control")
    s.add_argument("--daily-traffic", type=float, default=0)
    s.add_argument("--traffic-share", type=float, default=1.0, help="share of traffic in the test")
    s.set_defaults(func=cmd_sample)

    k = sub.add_parser("priority", help="Rank keywords from a CSV")
    k.add_argument("--csv", required=True,
                   help="columns: keyword, volume, relevance, chance, rank (see assets/keyword-matrix-template.csv)")
    k.add_argument("--top", type=int, default=40)
    k.add_argument("--w-volume", type=float, default=1.0)
    k.add_argument("--w-relevance", type=float, default=1.5)
    k.add_argument("--w-chance", type=float, default=1.0)
    k.set_defaults(func=cmd_priority)

    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    sys.exit(main())

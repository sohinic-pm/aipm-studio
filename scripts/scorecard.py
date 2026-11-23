#!/usr/bin/env python3
"""Scorecard for aipm.decoded, computed from data/tracker.csv.

Agents quote numbers from this output, never from memory.

  python3 scripts/scorecard.py              full report
  python3 scripts/scorecard.py --since 2026-11-23
  python3 scripts/scorecard.py --reel "Tokenmaxxing"
  python3 scripts/scorecard.py --rows       list logged rows
  python3 scripts/scorecard.py --followers 24   adds the North Star estimate
"""
import argparse
import csv
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACKER = ROOT / "data" / "tracker.csv"

# Keep in step with playbook/pass-lines.md
PASS_LINES = [
    ("skip_rate_pct", "Skip rate", lambda v: v <= 50, "<= 50%"),
    ("avg_watch_pct", "Avg watch", lambda v: v >= 35, ">= 35%"),
    ("non_follower_pct", "Non-follower views", lambda v: v >= 85, ">= 85%"),
    ("shares", "Shares", lambda v: v > 0, "> 0"),
    ("saves", "Saves", lambda v: v >= 2, ">= 2"),
    ("profile_visits", "Profile visits", lambda v: v >= 3, ">= 3"),
    ("follows", "Follows", lambda v: v >= 1, ">= 1"),
]
NUMERIC = ["views", "non_follower_pct", "likes", "saves", "shares",
           "profile_visits", "follows", "skip_rate_pct", "avg_watch_pct"]


def load(since=None):
    rows = []
    with TRACKER.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            for k in NUMERIC:
                r[k] = float(r[k]) if r.get(k, "").strip() else None
            if since and r["date"] < since:
                continue
            rows.append(r)
    return rows


def n(v, pct=False):
    if v is None:
        return "MISSING"
    s = f"{v:,.1f}" if v != int(v) else f"{int(v):,}"
    return s + ("%" if pct else "")


def total(rows, k):
    return sum(r[k] or 0 for r in rows)


def report(rows, followers=None):
    # Judge only reels with at least a day of data
    reels = [r for r in rows if r["format"] == "reel" and "needs 24h" not in r["notes"]]
    cars = [r for r in rows if r["format"] == "carousel"]
    print(f"Posts in range: {len(rows)} ({len(reels)} reviewable reels, {len(cars)} carousels)\n")
    if not reels:
        print("No reviewable reels yet.")
        return

    views = total(reels, "views")
    nf = sum((r["views"] or 0) * (r["non_follower_pct"] or 0) / 100 for r in reels)
    inter = total(reels, "likes") + total(reels, "saves") + total(reels, "shares")
    print("REEL FUNNEL")
    for label, v in [("Views", views), ("From non-followers", round(nf)),
                     ("Likes + saves + shares", inter),
                     ("Profile visits", total(reels, "profile_visits")),
                     ("Follows", total(reels, "follows"))]:
        print(f"  {label:<24}{n(v):>8}")
    print(f"  Non-follower share      {nf / views * 100:>7.1f}%")
    print(f"  Interactions per view   {inter / views * 100:>7.2f}%\n")

    vs = sorted((r["views"] for r in reels), reverse=True)
    print("SHAPE")
    print(f"  Median reel views       {n(statistics.median(vs)):>8}")
    print(f"  Mean reel views         {views / len(reels):>8.0f}")
    if len(vs) >= 2:
        print(f"  Top 2 reels' share      {sum(vs[:2]) / views * 100:>7.1f}%")
    print()

    print("FORMAT          posts   avg views   non-follower share")
    for name, grp in [("reel", reels), ("carousel", cars)]:
        if grp:
            v = total(grp, "views")
            share = sum((r["views"] or 0) * (r["non_follower_pct"] or 0) / 100 for r in grp) / v * 100 if v else 0
            print(f"  {name:<14}{len(grp):>5}{v / len(grp):>12.0f}{share:>19.0f}%")
    print()

    print("PILLAR (reels)  reels   median views   interactions/view")
    for p in sorted({r["pillar"] for r in reels}):
        grp = [r for r in reels if r["pillar"] == p]
        v = total(grp, "views")
        i = total(grp, "likes") + total(grp, "saves") + total(grp, "shares")
        print(f"  {p:<14}{len(grp):>5}{statistics.median(r['views'] for r in grp):>15.0f}{i / v * 100:>19.2f}%")
    print()

    if followers is not None:
        print("NORTH STAR (estimate)")
        print(f"  Followers now           {followers:>8}")
        print(f"  Per 100 reel views      {followers / views * 100:>8.2f}  (target 2.00)")
        print("  Estimate only: Instagram doesn't credit follows to most posts.\n")

    print("PASS LINES (reels; MISSING = not logged yet)")
    for r in reels[-7:]:
        print(f"  {r['date']}  {r['title'][:44]}")
        print("    " + "  ".join(f"{lbl}: {pass_fail(r[k], test)}" for k, lbl, test, _ in PASS_LINES))


def pass_fail(v, test):
    if v is None:
        return "MISSING"
    return "PASS" if test(v) else "FAIL"


def one_reel(rows, query):
    hits = [r for r in rows if query.lower() in r["title"].lower()]
    if not hits:
        print(f"No row matches '{query}'.")
        return
    r = hits[-1]
    print(f"{r['date']}  {r['title']}  ({r['format']}, {r['pillar']})")
    print(f"  Views {n(r['views'])}\n")
    print(f"  {'Metric':<20}{'Value':>10}  {'Pass line':<10}Result")
    for k, lbl, test, line in PASS_LINES:
        pct = k.endswith("_pct")
        print(f"  {lbl:<20}{n(r[k], pct):>10}  {line:<10}{pass_fail(r[k], test)}")
    if r["notes"]:
        print(f"\n  Notes: {r['notes']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--since", help="only rows on or after YYYY-MM-DD")
    ap.add_argument("--reel", help="pass/fail for one reel (title match)")
    ap.add_argument("--rows", action="store_true", help="list logged rows")
    ap.add_argument("--followers", type=int, help="current follower count")
    a = ap.parse_args()
    rows = load(a.since)
    if a.rows:
        for r in rows:
            print(f"{r['date']}  {r['format']:<8} {n(r['views']):>6}  {r['title']}")
    elif a.reel:
        one_reel(rows, a.reel)
    else:
        report(rows, a.followers)


if __name__ == "__main__":
    main()

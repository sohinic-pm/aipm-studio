#!/usr/bin/env python3
"""Score the reel-reviewer's hook predictions against real outcomes.

  python3 scripts/score_eval.py --make-blind          write evals/blind-hooks.csv
  python3 scripts/score_eval.py evals/results/X.csv   score a results file

Results file columns: id,predicted,reason  (predicted: won | average | lost)
"""
import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GOLD = ROOT / "evals" / "hook-eval-set.csv"
BLIND = ROOT / "evals" / "blind-hooks.csv"
LABELS = ["won", "average", "lost"]


def read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def make_blind():
    rows = read(GOLD)
    with BLIND.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "first_frame"])
        for r in rows:
            w.writerow([r["id"], r["first_frame"]])
    print(f"Wrote {BLIND.relative_to(ROOT)} ({len(rows)} hooks, outcomes removed)")


def score(path):
    gold = {r["id"]: r for r in read(GOLD)}
    preds = {r["id"]: r["predicted"].strip().lower() for r in read(path)}
    bad = sorted(set(preds) - set(gold)) + [i for i, p in preds.items() if p not in LABELS]
    if bad:
        sys.exit(f"Unknown ids or labels in results: {bad}")
    missing = sorted(set(gold) - set(preds))

    pairs = [(gold[i]["label"], preds[i]) for i in gold if i in preds]
    exact = sum(g == p for g, p in pairs)
    print(f"Scored {len(pairs)} of {len(gold)} hooks" + (f" (missing: {', '.join(missing)})" if missing else ""))
    print(f"Exact agreement: {exact}/{len(pairs)} = {exact / len(pairs) * 100:.0f}%")
    print("(Always guessing 'average' would score "
          f"{sum(g == 'average' for g, _ in pairs)}/{len(pairs)}: beat that.)\n")

    print("Confusion (rows = real result, columns = reviewer's prediction)")
    print(f"  {'':<9}" + "".join(f"{l:>9}" for l in LABELS))
    for g in LABELS:
        print(f"  {g:<9}" + "".join(f"{sum(1 for a, b in pairs if a == g and b == p):>9}" for p in LABELS))

    won = [i for i in gold if gold[i]["label"] == "won" and i in preds]
    found = [i for i in won if preds[i] == "won"]
    print(f"\nWinners found: {len(found)}/{len(won)}")
    false_wins = [i for i in gold if i in preds and preds[i] == "won" and gold[i]["label"] == "lost"]
    if false_wins:
        print("Rated 'won' but actually lost:")
        for i in false_wins:
            print(f"  {i}  {gold[i]['first_frame']}  ({gold[i]['views']} views)")
    print("\nMisses:")
    for i in gold:
        if i in preds and preds[i] != gold[i]["label"]:
            print(f"  {i}  predicted {preds[i]:<8} real {gold[i]['label']:<8} {gold[i]['first_frame']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("results", nargs="?")
    ap.add_argument("--make-blind", action="store_true")
    a = ap.parse_args()
    if a.make_blind:
        make_blind()
    elif a.results:
        score(a.results)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()

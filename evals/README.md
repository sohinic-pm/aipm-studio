# Hook eval

**Question:** can the reel-reviewer tell, from the first frame alone, which hooks
actually won?

**Set:** all 17 reels from 22 Oct to 17 Nov 2026, with their real views.
Labels use one rule: **won** ≥ 500 views, **average** 200-499, **lost** < 200.

**Blind by design, only partly enforced:** the reviewer is given only
`blind-hooks.csv` (id + first frame) and instructed not to open `data/tracker.csv`
or any other outcome data. Only one side of that is a technical control:
`.claude/settings.json` hard-blocks Claude's read access to `hook-eval-set.csv`
itself, so the answer key can't leak in. `tracker.csv` is **not** blocked —
other agents (insights-analyst, strategist, `scorecard.py`) need to read it —
so blindness to it rests on the reviewer following its instructions, not on a
permission the system enforces. Only `scripts/score_eval.py` reads `hook-eval-set.csv`.

**Run:** `/eval-hooks` in Claude Code. Results go in `results/<date>.csv`.

**Read the result with care:** 17 hooks is a small set and only 2 are winners. Use
it to catch a reviewer that's clearly miscalibrated (for example, it rates the
jargon and "FREE" hooks as winners), not to claim precision. Grow the set every
week: each reviewed reel becomes a new row.

## Limits
This set is also the data the playbook's hook rules were built from — running
the reviewer against it is an **in-sample check, not a validation**.

- On the 7 hooks the playbook already names or builds a rule on (the winners
  and losing patterns in `hook-formulas.md`), the reviewer got **6/7**.
- On the other 10, novel to those rules, it got **4/10** — worse than the
  **7/10** you'd get by always guessing "average".
- Of its 4 "won" calls, **2 were wrong**.

The real test is forward prediction: does the reviewer's call, made before a
reel posts and recorded in that reel's `review.md`, match the real result
logged 24 hours later? `/review-24h` now logs every one of those as a new row
in `hook-eval-set.csv`, marked `forward` in a `source` column. Only that
growing set can tell us whether the reviewer generalizes.

## Results log
| Date | Reviewer version | Exact agreement | Winners found | Notes |
|---|---|---|---|---|
| 2026-11-23 | reel-reviewer v1 | 59% (10/17) | 2/2 | In-sample baseline, not a validation (see Limits): 6/7 on playbook-derived hooks, 4/10 on the rest |

# Hook eval

**Question:** can the reel-reviewer tell, from the first frame alone, which hooks
actually won?

**Set:** all 17 reels from 22 Oct to 17 Nov 2026, with their real views.
Labels use one rule: **won** ≥ 500 views, **average** 200-499, **lost** < 200.

**Blind by design:** the reviewer sees only `blind-hooks.csv` (id + first frame).
`.claude/settings.json` denies Claude read access to `hook-eval-set.csv`, so the
outcomes can't leak into its predictions. Only `scripts/score_eval.py` reads them.

**Run:** `/eval-hooks` in Claude Code. Results go in `results/<date>.csv`.

**Read the result with care:** 17 hooks is a small set and only 2 are winners. Use
it to catch a reviewer that's clearly miscalibrated (for example, it rates the
jargon and "FREE" hooks as winners), not to claim precision. Grow the set every
week: each reviewed reel becomes a new row.

## Results log
| Date | Reviewer version | Exact agreement | Winners found | Notes |
|---|---|---|---|---|
| 2026-11-23 | reel-reviewer v1 | 59% (10/17) | 2/2 | Missed average-tier hooks most (4/8); every miss on an actual "lost" hook was an over-rating, never under |

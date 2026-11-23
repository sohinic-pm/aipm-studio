---
description: Test whether the reel-reviewer can tell winning hooks from losing ones
---

Run the hook eval.

1. Run `python3 scripts/score_eval.py --make-blind`. This writes
   `evals/blind-hooks.csv`: id and first-frame text only, no results.
2. Use the **reel-reviewer** agent in hook-only mode. Give it only
   `evals/blind-hooks.csv`. Ask it to write `evals/results/<yyyy-mm-dd>.csv`
   with columns `id,predicted,reason` (predicted is won, average or lost).
3. Run `python3 scripts/score_eval.py evals/results/<yyyy-mm-dd>.csv` and show
   the output.
4. Summarise in 3 lines: overall agreement, which kind of hook the reviewer
   misjudged most, and one change to the checklist or hook rules worth testing.
   Don't edit the checklist or playbook. Sohini decides.

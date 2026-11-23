---
description: 24-hour review of a posted reel against the pass lines
argument-hint: <reel title or posted/ folder name>
---

Review this reel about 24 hours after posting: $ARGUMENTS

1. Use the **insights-analyst** agent to read this one reel's Insights and update
   its row in `data/tracker.csv`.
2. Ask Sohini for skip rate and average watch time from the app. Add them.
3. Run `python3 scripts/scorecard.py --reel "<title>"` and show the pass/fail table.
4. Apply the decision rules in `playbook/pass-lines.md` and say which one fits.
   Suggest one next step; Sohini decides.
5. If the reel had a reviewer prediction (in its `review.md`), compare it with
   the real result and say whether the reviewer was right.
6. Either way, label the real result (won ≥500 views, average 200-499,
   lost <200) and add it as a new row in `evals/hook-eval-set.csv`: same
   columns as the existing rows, `source` set to `forward`, and `predicted`
   copied from the "Predicted hook result" the reviewer recorded in this
   reel's `review.md` (leave `predicted` empty if the reel had no reviewer
   prediction). This is what turns the hook eval from in-sample into a real,
   growing forward test — see `evals/README.md`.
7. Add one row to the review log in `playbook/reel-learnings.md`:
   `| date | reel | passed | failed | lesson |`. Keep the lesson to one line and
   mark it "early signal" unless 3 or more reels show the same thing.

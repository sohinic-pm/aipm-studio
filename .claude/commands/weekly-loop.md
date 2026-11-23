---
description: Run the weekly aipm.decoded loop (analyse, plan, then stop for Gate 1)
---

Run the weekly content loop. Today is the start of the planning week.

1. Use the **insights-analyst** agent to update `data/tracker.csv` for the last
   7 days and return its report.
2. Show Sohini the report. List anything under "Needs Sohini" (skip rate and
   watch time from the app) and ask her to paste those numbers. Add them to the
   tracker when she does.
3. Use the **strategist** agent to draft next week's plan in `data/weekly-plan.md`.
4. **STOP. Gate 1.** Show Sohini the draft plan as a table and ask her to approve,
   edit or swap items. Do not write any scripts until she says the plan is approved.
5. When she approves, change the heading from `(DRAFT)` to `(APPROVED <date>)`,
   then ask whether to start scripting now. If yes, run `/new-reel` for each
   approved item, one at a time.

Never post or schedule anything. Drafts end at Gate 2 with Sohini.

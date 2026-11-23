---
description: Script, review and fact-check one reel, then stop for Gate 2
argument-hint: <plan item, e.g. "Mon 23 Nov: Replit agent deleted a database">
---

Make one reel draft for: $ARGUMENTS

1. Check the item is in an `(APPROVED ...)` section of `data/weekly-plan.md`.
   If it isn't, stop and ask Sohini whether to go ahead anyway.
2. Create `drafts/<yyyy-mm-dd>-<slug>/`.
3. Use the **script-writer** agent to write `script.md`.
4. Use the **reel-reviewer** agent to write `review.md`.
   - FAIL: send the required fixes back to script-writer and review again.
     After 2 failed rewrites, stop and show Sohini the latest review.
5. Use the **fact-checker** agent to write `sources.md`.
   - Any NEEDS CHANGE: have script-writer apply the sourced number, then
     re-run the fact-checker on the changed claims only.
6. **STOP. Gate 2.** Give Sohini a short summary:
   - First frame and the reviewer's predicted result
   - Checklist score
   - Fact check: X verified, Y unverified (list the unverified ones)
   - The `[FIRST-PERSON]` slot and its hint, which she needs to fill
   - The 6-7 voiceover lines to record

She builds, records and posts. When she has posted, she moves the folder to
`posted/` herself and asks for `/review-24h` the next day.

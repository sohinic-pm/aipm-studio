# Pass lines: the 24-hour scorecard

Checked 24 hours after each reel is posted. Skip rate and average watch time
come from the mobile app (desktop Insights doesn't show them).

| Metric | Column in tracker | Pass line | Tells us |
|---|---|---|---|
| Skip rate | `skip_rate_pct` | 50 or lower | Whether the first frame works |
| Average watch time | `avg_watch_pct` | 35 or more (% of length) | Whether the middle holds |
| Views from non-followers | `non_follower_pct` | 85 or more | Whether Instagram is testing it widely |
| Shares | `shares` | above 0 | Whether the share line lands |
| Saves | `saves` | 2 or more | Whether the PM takeaway is useful |
| Profile visits | `profile_visits` | 3 or more | Whether the who-it's-for line creates curiosity |
| Follows | `follows` | 1 or more | Whether the profile closes the deal |

## North Star
**Follows per 100 weekly viewers.** Today: about 0.5 per 100 viewers (audit estimate;
`scorecard.py --followers 19` gives 0.34 per 100 reel *views*, which count repeat views). Target: 2.
Goal: 40+ followers by 6 Dec 2026, on the way to 100.

## Decision rules
1. Profile visits rise but follows don't: fix the profile (pins, bio, highlights).
2. Skip rate passes but profile visits stay at 0: the reel isn't saying who
   it's for. Strengthen the who-it's-for line.
3. Skip rate fails: the first frame is the problem. Re-test it with a trial reel.
4. Non-follower share below 85%: Instagram didn't test it widely. Check the
   format (carousel?) and posting time before blaming the topic.

These rules suggest a next step. Sohini decides.

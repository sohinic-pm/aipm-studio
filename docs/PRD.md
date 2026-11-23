# PRD: aipm.decoded studio

**Owner:** Sohini Chakraborty · **Status:** v1 built, first run from the week of 23 Nov · **Last updated:** 23 Nov 2026

## 1. Problem
I run a 5-reels-a-week Instagram page alone. Each reel involves research,
scripting, fact-checking, building, posting and a 24-hour review. In the first
30 days:
- Quality checks depended on what I remembered to do that day. The
  follow-conversion rules in my own playbook (the who-it's-for line, an author
  line) didn't make it into a single posted reel.
- Analysis was ad hoc. It took a one-off audit to see that 23 posts had earned
  5,615 reel views and **0 follows credited to any post**.
- Decisions lived in chat history, so I couldn't trace why I'd changed something.

## 2. User
Me: a solo creator-PM who wants a repeatable weekly loop, so each week's content
is decided from data and checked against written rules before it ships.

## 3. Goals
1. Every reel passes the same written checklist before it is built.
2. Every news claim carries a source before I see the draft.
3. Every reel gets a 24-hour review logged in one place, and the next week's plan
   is drafted from those logs.
4. I keep every decision: what to make, what to stop, what goes live.

## 4. Non-goals
- Auto-posting, scheduling, comment replies or DMs. Agents never touch the account.
- Making the video files end to end (that's the `aipm-concept-walkthrough-reel` skill,
  run separately).
- Growth hacks: follow/unfollow, engagement pods, bought reach.

## 5. Solution
A Claude Code project with:
- **Written rules:** `CLAUDE.md` and the `playbook/` files, read by every agent
- **Five specialist subagents:** analyst, strategist, script writer, reviewer, fact-checker
- **Commands** that chain them: `/weekly-loop`, `/new-reel`, `/review-24h`, `/eval-hooks`
- **Two human gates:** the plan (Gate 1) and verify-voice-post (Gate 2)
- **A guardrail hook** that blocks any agent from writing to `posted/`
- **A tracker and a scorecard script**, so numbers come from data, not the model's memory
- **An eval set** of 17 real first frames with known outcomes, to test whether the
  reviewer's judgement matches what actually happened

See `docs/architecture.md`.

## 6. Success metrics
| Metric | Target | How measured |
|---|---|---|
| Page North Star: follows per 100 weekly viewers | 2 (from ~0.5) | Tracker + follower count |
| Followers | 40+ by 6 Dec 2026 | Profile |
| Reels that passed the checklist before build | 100% | Reviewer report in each draft folder |
| News claims with a source at Gate 2 | 100% | Fact-checker report |
| Reels with a logged 24-hour review | 100% | `data/tracker.csv` |
| Reviewer agreement with real outcomes | Baseline first, then improve | `scripts/score_eval.py` |
| My hours per reel | Baseline in week 1, then reduce | Self-logged in `data/weekly-plan.md` |

## 7. Risks
| Risk | Mitigation |
|---|---|
| Agent states a wrong fact confidently | Fact-checker attaches sources; `UNVERIFIED` claims can't be hooks; I read the sources at Gate 2 |
| Agent invents metrics | Agents quote only from `tracker.csv`; anything missing is written `MISSING` |
| Agent posts or edits published work | No posting tools are given; hook blocks writes to `posted/` |
| Reviewer approves hooks that flop | Eval set against real outcomes; recalibrate the checklist when agreement is low |
| Employer details leak into a script | Hard rule in `CLAUDE.md`; reviewer checks the author line is method only |
| Small sample (23 posts) misleads | Lessons are labelled with counts; patterns are re-checked each week |

## 8. Open questions
- One brand name or two? (handle vs end card)
- Does the who-it's-for line move profile visits? (first test, week of 23 Nov)
- When follower count passes ~300, bring carousels back as a second format?

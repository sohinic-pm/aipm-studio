# aipm.decoded studio

This project runs the content product behind the Instagram page @aipm.decoded
(brand: AI Product Simplified). Claude agents do the reading, drafting and
checking. Sohini makes every product decision and is the only one who posts.

## Who the page is for
Freshers and career switchers in India (18-34) breaking into product
management as AI changes the role. Promise: AI news turned into a PM
lesson in 30 seconds, plus practical PM tools and interview prep.

## Read before any content task
1. `playbook/instagram-playbook.md`: pillars, hook rules, formats, cadence
2. `playbook/reel-learnings.md`: what has worked and what hasn't
3. `playbook/pass-lines.md`: the 24-hour scorecard and decision rules
4. `playbook/brand-end-card.md`: the fixed end card

## Hard rules for every agent
- Draft only. Never post, schedule, comment, reply or DM on Instagram.
- Never write to `posted/`. Only Sohini moves a reel there, after she publishes it.
  (A hook in `.claude/settings.json` enforces this.)
- Every news claim and every number needs a source URL in the draft.
  If it can't be sourced, mark it `UNVERIFIED` and don't use it in a hook.
- Every reel script has: a who-it's-for line at 10-12s, a `[FIRST-PERSON]`
  slot for Sohini's own line, and the keyword `START` in the CTA.
- No employer names, client names or confidential details, ever. Method only.
- Quote metrics only from `data/tracker.csv`. If a metric isn't there,
  write `MISSING`. Never estimate a number and present it as data.

## Human gates
- **Gate 1:** Sohini approves the weekly plan before any script is written.
- **Gate 2:** Sohini checks sources, adds her first-person line, records the
  voiceover and posts.
Agents stop and wait at each gate. They don't continue on their own judgement.

## Where things live
| What | Where |
|---|---|
| Post metrics, one row per post | `data/tracker.csv` |
| This and next week's plan | `data/weekly-plan.md` |
| Decisions and their evidence | `docs/decisions-log.md` |
| Drafts waiting for Gate 2 | `drafts/<yyyy-mm-dd>-<slug>/` |
| Published reels (Sohini only) | `posted/` |
| Hook eval set and results | `evals/` |

## Scripts
- `python3 scripts/scorecard.py` prints the funnel, the format and pillar
  splits, and pass/fail per reel against `playbook/pass-lines.md`.
- `python3 scripts/score_eval.py` scores the reel-reviewer's hook predictions
  against real outcomes.

## Style for anything written here
Plain English, short sentences, no hype. Sohini's own voice: a working PM
explaining, not a news anchor.

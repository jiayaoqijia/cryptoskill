---
name: design-a-first-week-onboarding-plan
description: Use when a new engineer or agent starts on a team. Maps day-by-day outcomes with a first merged change by day two, a named buddy, and an environment that runs on day one, so the week ends with a contribution not just orientation.
---

# Design a First-Week Onboarding Plan

A new joiner who spends week one reading and watching ends the week unable to build. A plan that puts a merged change on day two converts reading into working knowledge while motivation is still high.

## Procedure

1. Day 1 outcome: local environment runs. Give one command and the expected tail of output, e.g. `./scripts/bootstrap.sh && make test` ending in `"412 passed"`.
2. Day 1 also: a named buddy with a 30-minute booking, not a channel to ask into the void.
3. Day 2 outcome: one small merged change — a doc fix, a typo, a test. Route it through the real review flow.
4. Day 3: read one slice of the system along its data path, not the whole tree; record three questions.
5. Day 4: pair with the buddy on a real ticket; the newcomer drives and thinks aloud.
6. Day 5: ship the second change and write a half-page "what surprised me" note back to the team.
7. Track each day as a checklist item with an owner, and review the list at the end of the week.
8. Provision access before day 1; a first morning lost to waiting sets the tone.
9. Keep the first two tasks pre-scoped so the newcomer chooses between known-good options, not from scratch.
10. Book a 20-minute end-of-week check-in where the newcomer proposes one fix to the onboarding itself.
11. Give the newcomer a named escalation for day one ('if the build fails, ping @x'), not a general channel.
12. Put the buddy check-ins on the calendar, not left to chance.
13. End day five with the newcomer adding the missing step they hit back into the onboarding doc.
14. Assign an owner to each checklist row, so nothing waits on 'someone'.
15. Include one deliberately social moment, since isolation stalls new joiners.
16. Keep the plan in the repo so the newcomer can tick rows themselves.

## Pitfalls

- A week of access provisioning and reading, with nothing merged, so motivation drops.
- A buddy named but never scheduled; the newcomer waits instead of asking.
- "Read the codebase" with no slice named, which stalls by the afternoon.
- First task is a hard bug, so the first week is a failure instead of a win.
- Onboarding that lives in someone's head, so every joiner gets a different week.
- No day-1 environment check, so the first real task is blocked on a broken build.
- Onboarding blocked on a laptop or account that takes a week to arrive.
- A plan that assumes the newcomer already knows the team's vocabulary.
- No written record, so the plan is reinvented for every hire.
- Rows with no owner that quietly stall.
- A purely technical week with no human contact beyond the buddy.
- A plan kept in a doc nobody opens.

## Verification

    git log --author="<new-hire>" --since="7 days ago" --oneline | wc -l
    # passes when at least 2 commits from the newcomer are on main within the first week

Report to the user: each day's outcome, the day-2 change that merged, and the buddy's scheduled slot.

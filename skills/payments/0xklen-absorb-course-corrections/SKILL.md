---
name: absorb-course-corrections
description: Use when the user corrects, redirects, or rejects work in progress (stop, no, actually, wrong file). Halts the current path, isolates the wrong assumption, and re-plans before continuing.
---

# Absorb Course Corrections

A correction is data about a wrong premise, not an interruption to route around. Stop the current action, find which assumption broke, and change it before doing more of anything.

## Procedure

1. Stop immediately when the correction arrives. Do not finish the in-flight step "since you're already here" — the step may be exactly what the user is rejecting.
2. Restate the correction in one sentence in your own words and check it against the user's words. If your restatement is broader or narrower than theirs, you have it wrong.
3. Identify the broken assumption by asking: which claim was I acting on that the user is now contradicting? Write it down as `assumed: <X>; corrected: <Y>`.
4. Trace the blast radius: list every artefact already produced that rests on the broken assumption (files written, commits made, messages sent, drafts shared).
5. Decide for each artefact: keep, revise, or revert. Revert via the undo path from `rollback-first-planning`; do not hand-patch a wrong premise into shape.
6. Re-plan from the corrected premise, not from the old plan minus one step. If the correction changes the goal, the decomposition may change too.
7. Confirm the new direction in one line before executing: "Corrected to Y; I'll redo the tests then the doc, confirm?" For a small correction, state it and proceed.
8. If the correction reveals a pattern (the user has corrected the same class of thing twice), record a rule in your handoff capsule so it does not recur.
9. Check whether the correction invalidates an earlier statement you already reported and fix the record.
10. Distinguish a preference change ("I prefer tabs") from a factual correction ("that file is the wrong one") — they need different responses.
11. After re-planning, re-run reconciliation because a revert may have left the tree in a new state.

## Pitfalls

- Defending the original choice before acknowledging the correction — the transcript shows it and it costs trust.
- Applying the correction only to the newest artefact and leaving older ones inconsistent.
- Rephrasing the user's correction so it matches what you already built, rather than what they said.
- Continuing to spend on the rejected path while "planning" the new one.
- Treating "use the other file" as a cosmetic swap when it changes the data model downstream.
- Replying with a plan before acknowledging the correction, reading as if you did not hear it.
- Applying the correction to new work while the old, wrong artefact is still shipped or published.

## Verification

    git log --oneline -5 && git status --porcelain
    # passes when reverted artefacts show as reverted and the tree matches the corrected premise

Report to the user: the broken assumption, the artefacts you kept/revised/reverted, and the first step of the re-planned path.

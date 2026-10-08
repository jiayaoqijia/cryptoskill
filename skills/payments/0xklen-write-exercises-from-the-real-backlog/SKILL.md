---
name: write-exercises-from-the-real-backlog
description: Use when a learner needs practice that transfers to real work. Turns a sanitised good-first-issue from the actual backlog into a graded exercise with acceptance checks, so practice maps to the work they will do.
---

# Write Exercises from the Real Backlog

Toy exercises teach a toy idiom. A real, small issue from your own backlog, sanitised and given acceptance checks, practices exactly the work the learner will be paid to do.

## Procedure

1. Pull a genuine small issue: `gh issue list --label good-first-issue --limit 10`, or `git log --grep='good-first-issue' --oneline -10` for merged ones.
2. Sanitise: strip customer names, internal hostnames, and any secret to a placeholder before sharing.
3. Restate the issue as a task with acceptance criteria the learner can self-check, e.g. "a request with an unknown token id returns 404, not 500" and "the existing suite still passes".
4. Provide the smallest failing test that encodes the acceptance criteria.
5. Remove the original solution from the history the learner will read; `git log -- path/to/file` reveals it otherwise.
6. Cap the scope so it fits a 90-minute session; split anything larger into parts.
7. After the learner solves it, diff their patch against the one that actually merged.
8. Archive the exercise with the issue link so the next learner gets the same starting point.
9. Note the concept the issue teaches, so exercises map to a curriculum rather than piling up randomly.
10. Store the exercise next to the issue number so the trail is traceable.
11. Rotate which subsystem the exercises cover, so practice stays broad.
12. Retire an exercise once its answer appears in open PRs.
13. Keep the original issue link in the exercise so context is one click away.
14. Have a second person confirm the acceptance test fails before the fix.
15. Note the expected runtime so learners can plan the session.

## Pitfalls

- Leaving secrets or customer identifiers in the pasted issue.
- Choosing an issue whose solution is in the git history the learner has access to.
- A task with no acceptance check, so "done" is a judgement call.
- Picking an issue so large it becomes a week-long slog.
- Shipping the exercise without the failing test, so the learner cannot tell when they are done.
- Reusing the same issue twice, so the answer is already circulating.
- Choosing a closed issue whose discussion gives away the fix.
- A task whose flakiness makes success random.
- Bundling three fixes into one exercise, so none is practised cleanly.
- An exercise detached from its issue, losing the why.
- An acceptance test that passes on the unfixed code.
- An open-ended runtime that discourages starting.

## Verification

    grep -rniE 'password|token|internal\.corp|@customer' exercises/<name>/ && echo LEAK || echo clean
    # passes when the leak scan prints "clean" and a failing test encodes each acceptance criterion

Report to the user: the source issue, the acceptance criteria, and the sanitise-scan result.

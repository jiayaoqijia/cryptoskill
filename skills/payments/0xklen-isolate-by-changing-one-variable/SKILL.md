---
name: isolate-by-changing-one-variable
description: Use when a test, request, or build behaves differently in two settings and you need the cause. Holds everything constant and flips exactly one factor per run.
---

# Isolate by Changing One Variable

When two environments disagree, the difference is a specific field, flag, or ordering — not "it's flaky". Vary one thing per run and the cause falls out; vary many and you learn nothing.

## Procedure

1. Write down both configurations in full: versions, env vars, flags, hardware, data. Side by side, not from memory.
2. Enumerate the candidate differences. A quick way: `diff <(env | sort) <(ssh other 'env | sort')` and `diff requirements-a.txt requirements-b.txt`.
3. Rank candidates by plausibility given the symptom, then test the most likely first to save runs.
4. Flip exactly one candidate toward the failing configuration, re-run the *same* test, and record pass/fail plus the raw output.
5. Keep a toggle table: variable name, value, outcome. One row per run.
6. When a flip changes the outcome, confirm by flipping it back — the change must be reversible to count as causal.
7. Then bisect the winning variable itself if it is a range or list (see `bisect-a-config-or-data-difference`).
8. Stop as soon as a single variable flips the outcome; do not keep flipping others "for completeness".
9. Record the deciding variable and both values in the bug note so the result survives the session.
10. If no single flip moves the outcome after testing every candidate, the cause is an interaction — escalate to testing ordered pairs rather than looping the singles.

## Pitfalls

- Changing the input and the code in the same run, then crediting whichever change you suspected.
- Confusing correlation with cause: the failing machine also runs a different OS, but the OS is a passenger.
- A non-reversible change (deleted cache, advanced migration) that hides whether the original flip mattered.
- Testing variables in a fixed order every time, so a rare-but-causal variable stays untested for hours.
- Ignoring interaction effects: two variables together cause the bug but neither alone does. If nothing single-flips, test pairs.
- Re-running more than twice when a flip is unstable — that is a flaky variable masquerading as a cause.

## Verification

    ./run.sh --config a >/dev/null; echo "a=$?"
    ./run.sh --config b >/dev/null; echo "b=$?"
    ./run.sh --config a --the-one-difference >/dev/null; echo "a+flip=$?"
    # passes when a+flip reproduces b's outcome and removing the flag returns to a's

Report to the user: the one variable whose value decides the outcome, the three exit codes, and any suspected interaction if no single variable flipped it.

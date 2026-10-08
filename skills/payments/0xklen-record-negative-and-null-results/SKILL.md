---
name: record-negative-and-null-results
description: Use when an experiment, fix, or hypothesis fails or has no effect. Write down what was tried, said the result, and offer the next alternative so the dead end is never re-run blindly.
---

# Record negative and null results

Failures are data, but only if filed. This skill captures dead ends so the next attempt starts informed instead of burning the same budget on the same wall.

## Procedure

1. Add an entry to `NEGATIVE.md` for every attempt that did not work — a hypothesis, a patch, or a configuration change.

2. Record five fields per entry: what was tried, the exact command or diff, the observed result, the interpretation, and the next alternative.

3. Capture the raw failure: `pytest -q 2>&1 | tail -20`, the exit code, and the error string. Never compress it to "didn't work".

4. Distinguish `failed` (the result contradicted the goal) from `null` (no measurable effect). A null needs a control to mean anything: state what changed and what did not.

5. Record the search space covered, so a future pass does not repeat the same corner: "tested timeouts 5s and 30s; 5s rejects, 30s passes but breaks the SLA".

6. Before a new attempt, `grep -i <subsystem> NEGATIVE.md` to avoid repeating a known dead end.

7. If the alternative you name is later tried, append a follow-up line linking the two entries, so the chain of attempts is readable as one thread.

## Pitfalls

- A fix that "didn't help" with no metric recorded is unlogged; always record the measure and its value.
- Confusing a null result with a broken test: verify the test can detect a real effect before trusting its silence.
- Deleting a failed branch loses the reason; keep the note even after the code is reverted.
- Logging only successes turns the file into a marketing sheet rather than evidence.
- Reverting without recording the rationale guarantees someone retries the same idea next quarter.
- A negative result with no date is hard to age against changed inputs; stamp every entry.

## Verification

    grep -c "^## " NEGATIVE.md; grep -l "next alternative" NEGATIVE.md   # every entry carries the field

Report the number of attempts logged and the leading alternative for the next pass.

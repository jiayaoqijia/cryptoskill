---
name: disambiguate-a-vague-request
description: Use when a request could mean several things — "make it faster", "clean this up", "fix the bug". Restate the interpretation you will act on and confirm before doing the work.
---

# Disambiguate a vague request

"The bug" that you guess wrong costs a whole build. Reading the request broadly and stating your reading lets a one-line correction save the work.

## Procedure

1. List two or three plausible readings of the request, each phrased as a concrete action.

2. Pick the reading with the smallest reversible scope as your default.

3. Restate it in one line: "I will do X, which means Y and not Z."

4. Do the cheap disambiguation first: read the code with `rg -n "faster"`, the ticket, or the metric before deciding.

5. If the readings diverge widely, ask with options rather than guess.

6. State what you are deliberately not doing under this reading.

7. If you must proceed, mark the work provisional and flag the assumption you took.

## Pitfalls

- Guessing the largest-scope reading when a small one fits burns the budget.
- "Clean this up" can mean formatting or a rewrite; confirm which before touching files.
- Proceeding on a silent assumption hides a scope decision the user should own.
- Over-asking on trivia wastes round-trips; disambiguate only where readings diverge.
- Restating the request verbatim is not disambiguation; it adds nothing.

## Verification

    grep -nE "^Reading:" request.md   # the chosen interpretation and what it excludes

Restate the interpretation and its exclusions before starting, or ask when the readings diverge.

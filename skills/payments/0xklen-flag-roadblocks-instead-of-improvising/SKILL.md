---
name: flag-roadblocks-instead-of-improvising
description: Use when a blocker stops the agreed path — missing access, a broken dependency, an ambiguous instruction. Surface it with options instead of silently improvising past it.
---

# Flag roadblocks instead of improvising

Silent workarounds look like progress and land as surprises. This skill stops at the wall, names it with evidence, and offers a choice rather than clambering over it.

## Procedure

1. Confirm it is a real blocker, not difficulty: run the failing step once more and capture the exact error. A blocker gives a stable error, not an intermittent slowness.

2. Classify it as one of `missing access`, `broken dependency`, `ambiguous requirement`, or `contradictory instruction`.

3. State the blocked step, the error, and what you already tried — in that order, three lines at most.

4. Offer two or three concrete options with cost and consequence, e.g. "A) supply a token, unblocks now; B) I stub the call and mark it untested; C) skip this and finish the rest".

5. Do not choose the option that changes scope silently. Default to surfacing rather than deciding.

6. If you must proceed to stay unblocked, mark the improvised path `provisional` in the output and in your report so no one treats it as verified.

7. Log the blocker to `STATUS.md` under a `BLOCKED` heading before the progress list, so it is read first.

## Pitfalls

- Improvising credentials or access is never acceptable; ask for a token, never guess one.
- A workaround that works locally can be wrong in production; label it unverified explicitly.
- Waiting silently for the user while the budget drains is also a failure; flag early, not last.
- Burying the blocker at the end of a long report means it is missed; put it at the top.
- Reclassifying an ambiguous instruction as clear, without saying so, hides a scope decision.

## Verification

    grep -n "BLOCKED" STATUS.md   # blocker named with error and options, above the progress list

Report the blocker first, then the options and a recommendation, then stop for the decision.

---
name: layer-hints-in-an-exercise
description: Use when writing an exercise whose learner will get stuck. Provides three hint tiers (nudge, approach, spoiler) gated so escalation happens only after a real attempt, with the solution kept out of the starter tree.
---

# Layer Hints in an Exercise

An exercise with no hints blocks; an exercise with the answer inline teaches nothing. Three gated tiers let a stuck learner escalate by degrees instead of giving up or peeking wholesale.

## Procedure

1. Lay out `exercises/<name>/` with `README.md`, `starter.py`, and `tests/`.
2. Write the failing test first: `pytest exercises/<name>/tests -x` must fail on the intended assertion, not on `ImportError`.
3. Fix the scaffold until the failure is the right one; a learner debugging your scaffold is not learning the concept.
4. Author three tiers in `HINTS.md`:
   - Tier 1, nudge: names the missing concept in one sentence, no code.
   - Tier 2, approach: the shape of the solution in prose plus a function signature.
   - Tier 3, spoiler: the diff, inside a `<details>` block so it is folded by default.
5. Gate escalation in the README: spend 20 minutes and one search attempt before opening Tier 2; one debugging session before Tier 3.
6. Keep `solution/` in a sibling directory excluded from the starter archive, never inside the learner's tree.
7. Prove each tier covers a real blocker: delete one needed line, confirm the tier that references it is sufficient.
8. Re-check the tiers after any starter change, since a moved function makes a hint stale.
9. Run the exercise yourself cold and note where you reached for a hint; those spots are the ones that teach.
10. Number the tiers so a learner can say which one they needed, e.g. 'stuck at tier 2'.
11. Keep `HINTS.md` out of the starter README so a glance does not reveal the spoiler tier.
12. Hand the exercise to someone who has not seen it and record where they escalate; that calibrates the gates.
13. State the exercise's one learning objective at the top so the hints stay on target.
14. Keep the starter runnable so the learner can make progress before the fix.
15. Link each hint back to the concept section, so a hint teaches the rule not the instance.

## Pitfalls

- Tier 1 that is already the answer in disguise ("use a dict keyed by id").
- A starter that fails with `ModuleNotFoundError`, so the learner debugs the scaffold, not the concept.
- Shipping `solution/` inside the tarball and calling the hints pointless.
- Hints ordered by convenience instead of by how much they give away.
- No gate wording, so learners open Tier 3 immediately and skip the struggle that teaches.
- A hint that was true last term but refers to a function you since renamed.
- A tier that only restates the exercise prompt in different words.
- Hints that assume tooling the learner may not have installed.
- Leaving the spoiler expanded by default because the `<details>` tag was mistyped.
- An objective phrased so broadly that any solution counts.
- Starter code that does not run, so the first step is unrelated debugging.
- Hints with no link to the concept, so they patch one instance only.

## Verification

    pytest exercises/<name>/tests -q ; test -d exercises/<name>/solution && echo "solution-separate"
    # passes when tests fail only on the intended assertion and solution/ is outside the starter zip

Report to the user: the exercise name, the intended failing assertion, and the three tier headers in HINTS.md.

---
name: design-a-graded-exercise-set
description: Use when building a practice set for a topic. Lays out recall, apply, and transfer tiers with an explicit pass threshold between tiers, so a learner cannot advance on recognition alone.
---

# Design a Graded Exercise Set

Recognition is not ability. A set that only asks the learner to recall lets them pass without solving anything; a ladder that forces application and transfer exposes the gap while it is still cheap to fix.

## Procedure

1. Split the topic into three tiers and cap each:
   - Tier A recall: 5 items, one right answer, no reasoning required.
   - Tier B apply: 3 items, the rule used in a worked-like setting.
   - Tier C transfer: 1 item, the rule used in a domain the learner has not seen.
2. Set the gate: 4 of 5 on Tier A to attempt B; 2 of 3 on B to attempt C. Below the gate, revisit the tier.
3. Write each item with a runnable check where possible, e.g. `pytest exercises/set1/test_tier_b.py -q` expecting `3 passed`.
4. For non-code items, give a one-line model answer the learner can self-mark against.
5. Order items by increasing distance from the teaching example, not by subjective difficulty.
6. Record for each Tier C item the transfer axis (new data shape, new language, new scale) so you can audit coverage.
7. Cap the whole set at nine items; more than that and the learner stops at Tier B.
8. Re-tune the gates after the first learner: if everyone clears Tier B, the items were too easy.
9. Keep the model answers in `_answers/`, separate from the learner copy.
10. Time the set on yourself; if it takes over an hour, cut items rather than adding pressure.
11. Print a score per tier so the learner sees which rung they are on, not a single pass/fail.
12. Version the set against the topic commit it was written for, so drift is visible.
13. Record how long each tier takes you, so the set fits the session it is used in.
14. Print the tier next to each item so grading is unambiguous.
15. Keep one worked example per tier visible, so the learner sees the standard expected.
16. Store items as data (e.g. YAML) so gates and counts are adjustable without editing prose.

## Pitfalls

- Ten Tier A items and no Tier C, so the set rewards memorisation.
- A Tier C item that is really Tier B with new variable names; transfer means new context.
- Making the gate a hard wall with no route back to re-study.
- Self-marking Tier B items with a vague model answer no learner can match.
- Publishing the answer key in the same directory the learner works in.
- Letting the tiers drift so a "recall" item needs reasoning and an "apply" item does not.
- Tier B items that can be answered by copying a Tier A answer.
- A set with no retry, so one bad tier ends the whole session.
- Gates set by feel rather than by watching the first learner attempt them.
- Requirements that mix tiers, so the grader cannot tell what is being tested.
- A worked example that reveals the Tier C answer.
- Gates hard-coded in several places that drift out of sync.

## Verification

    pytest exercises/set1 -q
    # passes when 5 tier_a, 3 tier_b, 1 tier_c collect and the golden run reports 9 passed

Report to the user: the tier counts, each gate value, and the transfer axis named for the Tier C item.

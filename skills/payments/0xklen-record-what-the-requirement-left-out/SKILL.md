---
name: record-what-the-requirement-left-out
description: Use when a requirement defines what a feature does but not its boundaries. Logs the excluded non-goals, assumptions, and open questions with the spec so gaps cannot resurface as scope surprises.
---

# Record what the requirement left out

A spec is defined as much by what it excludes as by what it states. This skill records the non-goals, the assumptions, and the unresolved questions beside the spec, so nothing is silently assumed.

## Procedure

1. Read the requirement and list three categories in `boundaries.md`: `non-goals` (deliberately excluded), `assumptions` (believed true but unverified), and `open questions` (undecided).
2. For each non-goal name who asked for it and why it was excluded, so a future reader sees the reasoning, not just a veto.
3. For each assumption write the evidence (or `none`) and the impact if it is false; an assumption with no evidence and high impact is an open question in disguise.
4. For each open question name the decider and the date by which it must be answered, or it will be answered by accident during the build.
5. Cross-check assumptions against the acceptance criteria; a criterion resting on an unverified assumption is fragile and should be flagged.
6. Review the boundary list with the requester before freezing the spec, since people catch omissions better than incorrect statements.
7. Version the file with the spec so boundaries travel with the requirements, not in a chat thread.
8. Revisit before each review; a resolved open question moves to non-goals or into the spec, and the list stays current.
9. Distinguish a deliberate non-goal from a forgotten one by naming who decided and when.
10. Add a section for constraints imposed from outside the team, such as platform limits or contracts.

11. Link each assumption to the evidence file or ticket so it can be rechecked when it expires.

## Pitfalls

- Leaving the non-goals implicit, so every reviewer assumes a different boundary.
- Recording an assumption without its impact, which hides the ones that matter.
- Open questions with no owner or deadline, which is how a decision gets made by whoever codes first.
- Writing boundaries in a separate doc that nobody opens with the spec.
- Treating "we'll decide later" as a non-goal; it is an open question with a deadline missing.
- Listing open questions without dates, which quietly become the build team's problem.
- Treating the boundaries doc as a one-time artefact instead of a living companion to the spec.

- Merging a non-goal back into scope without updating the boundary file.

## Verification

    grep -c '^non-goal\|^assumption\|^open question' boundaries.md; grep -c 'owner:\|date:' boundaries.md

Report the non-goal count, every assumption lacking evidence, and each open question's owner and deadline.

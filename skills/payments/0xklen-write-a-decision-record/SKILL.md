---
name: write-a-decision-record
description: Use when you choose between two or more viable approaches. Record the options, the deciding constraint, and the reversal cost in a dated, numbered file.
---

# Write a decision record

A choice with no record gets re-litigated by the next agent, or by you an hour later. This skill captures the reasoning while the alternatives and constraints are still in your head.

## Procedure

1. Find the next number: `ls decisions/ADR-*.md | sort -V | tail -1`. Create `decisions/ADR-<n>-<slug>.md`.

2. Fill the header with date (`date -u +%F`), status (`proposed`/`accepted`/`superseded`), and the decider.

3. List at least two options, one line each. A record with a single option is a plan, not a decision, and cannot be reviewed.

4. State the deciding constraint as a measurable fact, not a preference: "build must finish under 120s on CI" beats "faster is better".

5. Write the consequence section: what becomes hard or impossible once this option is chosen.

6. Give the reversal cost in effort and in units: `trivial (<10 min)`, `moderate (hours)`, `severe (rewrite)`, and note whether any data migration is involved.

7. Only after the record exists do you begin implementing, so the reasoning is not back-filled.

8. To change course later, write a NEW record that links the old one via a `Supersedes: ADR-3` line and mark the old status `superseded`. Never edit a past record's decision.

## Pitfalls

- Hindsight rewrites the record; capture the constraint you actually felt at the time.
- An `accepted` record with no named decider cannot be challenged or owned by anyone.
- Recording a decision you were merely told to make hides the instruction — quote it as the constraint.
- Numbers age: put the measured value and the command that produced it, not just the conclusion.
- Two records disagreeing with no supersede link leaves the reader with no truth; always link.

## Verification

    ls decisions/ | wc -l; grep -L "Reversal cost" decisions/ADR-*.md   # second command prints nothing

Report the ADR path and the one constraint that decided the choice, in a single sentence.

---
name: write-a-scope-agreement
description: Use when starting work with a client, team, or another agent and the boundaries are verbal. Put deliverables, exclusions, acceptance, and change control in one page both sides confirm.
---

# Write a scope agreement

A verbal scope lives only in memory, and two memories of the same call rarely match. One page, written before the build, is the cheapest dispute resolution there is.

## Procedure

1. Draft a single page with five headings: Deliverables, Out of scope, Acceptance, Change control, Assumptions.

2. Under Deliverables, list numbered, testable items with a definition of done each (`D1..Dn`).

3. Under Out of scope, name what a reasonable reader assumes is included but is not: docs, staging, migration, mobile.

4. Under Acceptance, state how completion is judged: the exact command, test suite, or named signer.

5. Under Change control, give the threshold that triggers a written change order.

6. Send for confirmation and record who confirmed and when, not merely that they were told.

7. Store it beside the work in the repo as `SCOPE.md` so it survives the session, not in a chat thread.

## Pitfalls

- An agreement that lives only in a chat scroll, unfindable when the argument starts.

- No acceptance definition, so "done" becomes a matter of opinion.

- Exclusions missing, so every omission is later read as a defect.

- Treating a silent reader as agreement without a stated deadline for objection.

- Letting the document rot as scope changes instead of versioning it.

## Verification

```
    grep -cE '^## (Deliverables|Out of scope|Acceptance|Change control)' SCOPE.md   # all four -> 4
```

Report the four section headings and the name of the person who confirmed the scope.

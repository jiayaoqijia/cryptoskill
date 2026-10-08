---
name: write-falsifiable-acceptance-criteria
description: Use when turning a requirement into build-or-reject criteria. Writes each criterion as a pass/fail observation a stranger could run, not a sentiment.
---

# Write falsifiable acceptance criteria

Acceptance criteria decide whether work ships. If a criterion cannot fail, it gates nothing; this skill forces every line into a check someone else can execute.

## Procedure

1. Write one criterion per line in `AC.md`, each with an identifier `AC-01`, `AC-02`, ... so tests and reviews can cite them.
2. Give each criterion the shape `given <state>, when <action>, then <observable result>`; the `then` clause must name a value, a count, a status, or a visible string.
3. Ban unfalsifiable verbs: "works", "fast", "intuitive", "robust", "user-friendly". Replace each with the measurement that would make it true (`grep -inE 'fast|robust|intuitive|user-friendly' AC.md`).
4. Put a number or an exact string where the eye would otherwise interpret; "under 500 ms at p95" beats "responsive".
5. Add the negative case beside each positive one: what must NOT happen (no duplicate row, no charge on retry, no PII in the response).
6. Mark each criterion with the layer it is checked at — `unit`, `integration`, `e2e`, or `manual` — so verification effort is planned, not assumed.
7. Reject any criterion you cannot imagine failing; if you cannot describe the broken state, you do not understand the requirement yet.
8. Freeze the file before build and version it; later edits are spec drift and must be logged (see `detect-spec-drift-against-the-build`).
9. Give each criterion an owner and a review date so an idling requirement is visible rather than assumed met.
10. Store the criteria in the repository beside the code, not a ticket tracker that closes and hides them.

11. Number criteria so no gaps appear when one is removed; a missing `AC-04` should be visible, not silently absorbed.

## Pitfalls

- A criterion that restates the feature ("the button works") duplicates the spec without adding a gate.
- Combining two behaviours in one line hides the half that passes; keep one assertion per criterion.
- Thresholds without a unit or population ("fast") are unmeasurable; always say p50/p95 and at what load.
- Criteria written after the code tend to describe what was built, not what was wanted.
- Omitting the failure path leaves error handling untested and shipped broken.
- A criterion copied from a template without adapting its values to this feature.
- Acceptance criteria that silently change after review with no version bump.

- Acceptance criteria that never mention what the user sees, only internal state.

## Verification

    grep -cE '^AC-[0-9]+' AC.md; grep -inE '\b(fast|robust|intuitive|user-friendly|works)\b' AC.md || echo clean

Passes when every `AC-` line has a `then` with a value and the vague-word grep prints `clean`. Report any criterion with no negative case.

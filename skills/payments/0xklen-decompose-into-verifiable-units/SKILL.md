---
name: decompose-into-verifiable-units
description: Use when a task is too large to do or check in one motion. Splits it into units that each have an observable pass/fail, ordered by dependency, so progress is provable step by step.
---

# Decompose into Verifiable Units

A step you cannot check is a step you cannot trust. Cut the task until every unit has an input, an action, and an observable result, and complete them in dependency order.

## Procedure

1. Restate the end state as a single checkable condition: "the endpoint returns 200 with a `total` field for a valid query". If the end state has no check, it is not the end state.
2. List the units needed to reach it. Each unit must satisfy: one input, one action, one observable output you can test.
3. Reject any unit whose result you cannot observe — split it again, or admit you do not know how to verify it.
4. Order units by dependency, not by the order they were mentioned. Draw the edges: unit B needs A's output before it can start.
5. Mark units that are independent and can be done in parallel; do not interleave them if one's failure would contaminate the other's evidence.
6. Size each unit to finish in one short pass (roughly under ten minutes of work). Oversized units hide failures; undersized ones waste calls.
7. Execute in order, and check each unit's observable before starting the next. A failed check stops the chain until fixed.
8. Keep a checklist in the workspace: `notes/plan.md` with `- [x] unit` / `- [ ] unit` lines, updated as you go.
9. When the whole chain passes, run the end-state check from step 1 as the final verification.
10. Write each unit's observable as a command with an expected output before implementing it, so the check is not shaped around whatever the code happens to produce.
11. Keep a "not yet decomposed" scratch list; anything still unverifiable stays there rather than entering the plan.
12. Estimate each unit's cost; any unit over the time-box gets split again.

## Pitfalls

- A "unit" that is really the whole task ("build the feature"), offering no intermediate proof.
- Ordering by narrative rather than dependency, so a later unit needs output that does not exist yet.
- Verifying only at the end, so a fault in unit one surfaces after units two through eight are built on it.
- Units so small they are just tool calls, adding bookkeeping with no verification value.
- Marking a unit done because the command ran, not because its observable result was checked.
- Defining the verification after seeing the output, so it always passes.
- Units that each need the full test suite to check, serializing the whole plan for no reason.

## Verification

    cat notes/plan.md
    # passes when every unit has a checkable result and all boxes are ticked by an observed pass

Report to the user: the unit list with each unit's observable result, and the final end-state check output.

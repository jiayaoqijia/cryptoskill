---
name: handle-a-moving-target-request
description: Use when requirements change faster than they can be built, a new "actually" every meeting. Freeze a baseline, batch changes into a cadence, and re-baseline deliberately.
---

# Handle a moving-target request

When the target moves faster than the build cadence, nothing can ever be finished. The fix is not to chase harder but to freeze a baseline and adopt changes as a deliberate, batched decision.

## Procedure

1. Recognise the pattern: more than two requirement changes since the last build step, each contradicting the previous.

2. Freeze the current understanding as a dated baseline in `SCOPE.md`, and say so out loud.

3. Stop building toward undelivered changes; work only the frozen baseline until the next gate.

4. Batch incoming changes: collect them and review as a set at a fixed point, such as daily, or per milestone.

5. At each gate, re-baseline deliberately: adopt the changes that clear the change-order threshold, defer the rest.

6. Price each adopted change (see `price-a-change-request`) before folding it into the baseline.

7. If changes keep arriving between gates, raise it: a target moving faster than the cadence cannot be hit, and that is a scope conversation, not an execution one.

## Pitfalls

- Chasing each new instruction immediately, so nothing is ever finished.

- Freezing a baseline and refusing all change, blocking legitimate new information.

- Re-baselining so often it is indistinguishable from chasing.

- Batching changes but never re-baselining, so the freeze becomes a permanent stalemate.

- Absorbing every change's cost silently until the schedule breaks.

## Verification

```
    grep -c '^baseline' SCOPE.md   # dated baselines exist; more than a few a week means the cadence is wrong
```

Report the current baseline date, the changes queued since it, and the next re-baseline gate.

---
name: stop-work-when-conditions-become-unsafe
description: Use when work in progress uncovers a hazard such as wrong environment, live data, or a destructive step. Halt rather than continue carefully.
---

# Stop work when conditions become unsafe

"Being more careful" still executes the dangerous action, only slower. When a hazard surfaces mid-task, the correct move is to halt, revert to known good, and verify the condition before resuming.

## Procedure

1. On discovering a hazard mid-task (writes hitting prod, a delete against shared storage, a secret in a public repo), stop the current command before it completes.

2. Assess the blast radius: what has already changed, and is any of it irreversible?

3. If reversible, revert to the last known good state before doing anything else; do not build on the contaminated state.

4. Freeze the work, causing no further side effects, until the environment is confirmed safe.

5. Notify the owner with the hazard, the exposed surface, and what you reverted; escalate if the owner is unreachable.

6. Before resuming, prove the condition is fixed. Point the command at the intended target and re-read it with `echo "$DATABASE_URL"`, rather than trusting a reassurance.

7. Record the halt and the condition that cleared it in the task or incident log.

## Pitfalls

- "Being more careful" instead of stopping, which continues the exposure at a slower rate.

- Continuing to produce output that builds on the contaminated state, multiplying the rework.

- Fixing forward under time pressure instead of reverting to known good.

- Resuming on an assurance that the target is correct without re-reading it yourself.

- Halting but telling nobody, so the hazard persists for the next run.

## Verification

```
    grep -nE 'halt|reverted to' incident.md   # halt recorded with the reverted state named
```

Report the hazard found, what you reverted, and the check that cleared it before resuming.

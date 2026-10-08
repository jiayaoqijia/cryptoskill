---
name: guard-against-scope-creep
description: Use when a task is quietly growing while you execute it. Classify each new piece of work as in-scope, adjacent, or new, and route it before doing it.
---

# Guard against scope creep

Creep is rarely one big overreach; it is ten small "while I'm here" additions. This skill turns every addition into a visible, priced item rather than an absorbed cost of the deliverable.

## Procedure

1. Keep the frozen requirement list open beside the work so you can test each impulse against it.

2. Classify everything you are tempted to add:
   - `in-scope` — directly required by an existing criterion; just do it.
   - `adjacent` — needed to make a criterion pass but not itself listed; do it and log it.
   - `new` — valuable but unrequested; do NOT do it, queue it.

3. Log every `adjacent` and `new` item to `SCOPE.md` with an estimate in minutes and the criterion that spawned it.

4. Before starting a `new` item, check the time budget: once elapsed exceeds 80% of the box, stop adding work and start reporting.

5. Surface `new` items to the user as a labelled list at the next report, never as a finished fait accompli.

6. When a discovered bug blocks a criterion, it is `adjacent` and belongs in the log; when it does not, it is `new` and belongs in the queue.

7. Count deltas at the end: `grep -cE "^(adjacent|new)" SCOPE.md`, and reconcile against what you actually did.

## Pitfalls

- Refactoring en route feels free but invalidates prior test runs and re-opens finished work.
- "It's only two lines" ignores the review, test, and rollback cost those two lines carry.
- A `new` item completed silently makes the deliverable differ from what was agreed.
- Renaming cleanups (typos, formatting) still produce a diff someone must review; log them.
- An `adjacent` item that keeps growing into a subsystem is really a `new` project; reclassify.

## Verification

    grep -cE "^(in-scope|adjacent|new)" SCOPE.md; grep '^new' SCOPE.md   # queue shown, none executed

Report the added-item count and every deferred item with its estimate, one line each.

---
name: plan-in-vertical-slices
description: Use when a plan is organized by layer (all schema, then all API, then all UI) and delivers value only at the very end. Reorders work into thin end-to-end slices so each finishes something real and cheap to estimate.
---

# Plan in vertical slices

A layered plan hides all the integration risk until the end, and the estimate is a single all-or-nothing bet. Slicing vertically — one thin path through every layer — produces shippable increments, earlier feedback, and estimates that can be checked slice by slice.

## Procedure

1. Take the smallest user-visible outcome: "a logged-in user sees their own name on the dashboard." That is slice one.
2. Implement every layer needed for that one outcome — a real row in the DB, one endpoint, one rendered component. Resist stubbing layers you "will need anyway."
3. Ship the slice (behind a flag if needed) and observe it. Deploy it, do not just merge it.
4. Estimate the *next* slice now, using the first as a reference class. Slice N is usually cheaper than slice 1 because the plumbing exists.
5. Add slices one at a time, each end-to-end. A slice that only touches one layer is horizontal and does not count.
6. Keep a walking-skeleton slice zero: the thinnest possible path (health check through deploy through UI) to prove the pipeline works before features pile on.
7. Track slices as checkboxes in `notes/slices.md`, so partial delivery is visible:

       - [x] slice 1: show own name
       - [ ] slice 2: edit own name
       - [ ] slice 3: avatar upload

## Pitfalls

- Calling a layer-complete milestone a slice; "all the models are done" ships nothing a user can touch.
- Slices so thin they are chores (a whole slice for a single field) — merge them.
- Deferring the walking skeleton, so integration surprises arrive after most of the estimate is spent.
- Building a layer "properly for the future" inside slice one, which re-creates the big up-front risk.
- Estimating all slices up front to the same precision; later slices should be estimated more loosely and refined as you go.
- A slice that cannot be demoed on its own; if you cannot show it, it is not vertical yet.

## Verification

    grep -c '\[x\] slice' notes/plan.md
    # passes when at least one slice is checked and every slice spans the full stack

Report the slice list, which slices are shipped and observable, and the re-estimate of the next slice from slice one's actual cost.

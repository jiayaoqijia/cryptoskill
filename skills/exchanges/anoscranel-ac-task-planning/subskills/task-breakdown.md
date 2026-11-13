---
name: task-breakdown
domain: software-engineering/task-breakdown
trigger: "\"Break this into tasks\", \"slice this feature\", \"what order should we build this in\", \"make a task list from the spec\", \"split this epic\"."
anti_trigger: "Estimating cost or choosing cadence (subskills/planning.md); deciding what to build; step size while coding."
scope: "Slicing a spec into ordered, vertical, independently shippable tasks"
status: "seedling"
---

# Task Breakdown

## Standard

- **Vertical slice**: the smallest end-to-end change that delivers user value through every layer it needs.
- **INVEST** (Bill Wake) applies to each task: Independent, Negotiable, Valuable, Estimable, Small, Testable.
- **Small batches** cut review load and integration cost. DORA ties small batches and short-lived branches to delivery performance (https://dora.dev/capabilities/trunk-based-development/).

## Decision rules

1. Slice vertically (UI + API + storage for one behaviour), not horizontally ("all tables first").
2. Each task ends in a state that builds, passes tests and can merge to main. Unfinished user-facing work hides behind a flag.
3. Size: one task fits in one reviewable PR. Aim for about 100 changed lines; treat 1000 as too large (Google "Small CLs": https://google.github.io/eng-practices/review/developer/small-cls.html). ⚠️ "Fits in one day" is house convention.
4. Order: riskiest unknown first, then the walking skeleton, then value in priority order, then polish.
5. A task needing a research answer first becomes a spike task with a time box.
6. Dependencies are explicit. A task that blocks three others moves up.
7. Every task traces to at least one requirement ID or names itself enabling work.
8. Split patterns, in order of preference: by workflow step, by business rule, by data variation, by happy path then edge cases, by interface, by operation (create/read/update/delete).

## Procedure

1. Read the approved spec. List every behaviour and every requirement ID.
2. Find the riskiest assumption. Make it task 1 (a spike or a thin proof).
3. Define the walking skeleton: the thinnest path through all layers, deployed. Make it task 2.
4. Slice the rest with rule 8. Write each task in this shape:
   ```markdown
   ### T-07 Reject expired coupons at checkout
   Traces: REQ-014
   Depends on: T-03
   Done when: Gherkin scenario "expired coupon" passes in CI; flag `coupon_v2` off by default
   Out of scope: coupon admin UI
   Size: S
   ```
5. Check each task against INVEST. Too big → split again. Not valuable alone → merge it into a neighbour or mark it enabling.
6. Order by rule 4. Draw the dependency list. Remove cycles by splitting.
7. Mark tasks that can run in parallel.
8. Save as `docs/specs/NNNN-tasks.md` next to the spec.

## Anti-patterns

- Layer tasks ("build the database", "build the UI").
- Tasks with no done condition.
- "Refactor everything" as one task.
- Hidden integration task left to the end.
- Tasks sized by hours guessed under pressure.
- Agent-generated task lists accepted without a dependency check.

## Done checklist

- [ ] Riskiest unknown is task 1.
- [ ] Walking skeleton is an early task.
- [ ] Every task is vertical, mergeable and has a done condition.
- [ ] Every task traces to a requirement or is marked enabling.
- [ ] Dependencies listed; no cycles.
- [ ] No task exceeds one reviewable PR.

## Sources

- <https://github.blog/developer-skills/github/write-better-commits-build-better-projects/>
- https://google.github.io/eng-practices/review/developer/small-cls.html 
- https://dora.dev/capabilities/trunk-based-development/

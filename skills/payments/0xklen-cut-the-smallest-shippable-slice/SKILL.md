---
name: cut-the-smallest-shippable-slice
description: Use when a feature is scoped as one big release. Cuts it to the smallest slice a real user can use end-to-end this week, with the rest explicitly deferred.
---

# Cut the smallest shippable slice

The first release should be the thinnest thing that delivers value to one real user, so feedback arrives before the design hardens. This skill carves that slice and records what was deferred.

## Procedure

1. Write the full feature as a flow of user steps in `slice.md`, e.g. `sign up -> add item -> pay -> receive confirmation`.
2. Mark each step `must-have-now`, `can-fake`, or `later`. A step is `can-fake` if a manual or stubbed version still lets a user finish the flow.
3. For each `can-fake`, name the manual substitute: a spreadsheet, an operator, a hard-coded value, a queue drained by hand. Fakes must be visible in the plan, not hidden in the code.
4. Define the slice as the shortest prefix of steps that still reaches a value moment — typically ending at the first point the user gets something back.
5. Check the slice is still end-to-end: every dependency it needs (auth, storage, a payment path) must be present or faked. A slice that stops before the return value teaches nothing.
6. Estimate the slice in days, not weeks; if it is over about five engineer-days, cut another step.
7. List the deferred steps under `deferred:` with the reason and the trigger that will pull each back in.
8. Say the slice in one sentence to the requester: "first version: X only, done when Y".
9. Name the metric that will tell you the slice worked, so the cut has a hypothesis and not just a size.
10. Confirm the slice can be demoed to one real user end-to-end before you write the estimate down.

11. Write the out-of-scope list before the in-scope list; the boundary is what keeps the slice thin.

## Pitfalls

- Slicing by component (all the backend, then all the frontend) instead of by user journey; no user can use a component.
- Faking something quietly so the demo works, then shipping the fake to production.
- A slice so small it never reaches a value moment, so the feedback is meaningless.
- Deferring the hard risk (the integration most likely to fail) to the very end instead of front-loading it.
- Leaving `deferred:` empty; if nothing is deferred, the slice was not a slice.
- Building the full data model for the eventual feature and calling that the slice, which is neither small nor shippable.
- Deferring the demo, so nothing validates the slice until it is already large.

- Adding a step back to the slice because it is easy, not because the value moment needs it.

## Verification

    grep -c 'must-have-now\|can-fake\|later' slice.md; grep -c '^deferred:' slice.md

Report the slice in one sentence, its day estimate, and the first deferred item with its trigger.

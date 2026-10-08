---
name: enumerate-user-visible-states
description: Use when specifying a screen, component, or flow. Lists every state a user can see — loading, empty, partial, error, offline — before the happy path is built.
---

# Enumerate user-visible states

Designs default to the happy path and ship the rest by accident. This skill enumerates every state a user can actually observe, so none is improvised in production.

## Procedure

1. Name the entity and the screen in `states.md`, e.g. `orders list`.
2. List the states from the data's point of view: `loading` (request in flight), `empty` (zero results, not an error), `partial` (some pages loaded), `populated`, `stale` (cached while revalidating), `error` (request failed), `offline` (no network), `permission-denied`, and `disabled` (feature gated).
3. For zero results, separate `no data yet` from `no data matches your filter`; they need different copy and a different call to action.
4. For each state specify the visible text, the primary action, and what the user can do next. A state with no next action is a dead end (see `audit-a-flow-for-dead-ends`).
5. Mark which states can appear simultaneously, e.g. `stale` plus `partial`; test the combinations users actually hit, not every permutation.
6. Note the transition that leaves the state and its trigger: retry, refresh, next page, back.
7. Check each message against the rules in `write-actionable-error-copy`.
8. Confirm no state can persist indefinitely: every `loading` and `stale` needs a timeout and a fallback.
9. Add the zero-width and very-long-content cases: an empty string, a 5000-character name, an emoji in a title.
10. Note the slow-network state separately from offline; a request that takes 30 seconds is its own experience.

11. Give the error state its own error code visible to support, so a screenshot identifies the failure precisely.

## Pitfalls

- Treating an empty list as an error; users see a red banner where a friendly nudge belongs.
- A `loading` state with no timeout, so a hung request spins forever.
- Copy that says "something went wrong" with no path forward.
- Forgetting `permission-denied`, so the screen renders as `empty` and looks like lost data.
- Designing from the API's shape rather than the user's; a 200 with an empty array is still `empty`.
- Specifying the loading skeleton but never the failure state it resolves to.
- Forgetting the state after a successful action, such as the post-submit confirmation.

- Naming states after components rather than after what the user perceives.

## Verification

    grep -cEi '^state:|loading|empty|partial|error|offline|denied' states.md

Report the state list and any state with no defined next action or no exit transition.

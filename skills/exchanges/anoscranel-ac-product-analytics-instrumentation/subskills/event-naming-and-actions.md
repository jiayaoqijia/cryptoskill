---
name: event-naming-and-actions
domain: software-engineering/event-naming-and-actions
trigger: "Naming events so they stay queryable and unambiguous."
anti_trigger: "Not for property design, and not for governance process."
scope: "Naming events after user-visible actions, not implementation."
status: seedling
---

# Event naming and actions

## Standard

The naming convention is the first line of defence against the taxonomy rotting: name events after what the user did or saw, not what the code did. Song played, playlist created, file shared — the vocabulary is the product's, and a new engineer can guess the event name from the user-facing action. Signup flow completed beats Form_handler_2_fired.

The convention applies at both ends: no click-tracking of everything interactive without a reason for the question, and no user-action named by its implementation (auto_save_triggered is a jobs queue, not a user event). Alongside the convention sits the family hierarchy: event names groupable by their object rather than their verb, so object populations can be checked after the fact without wrangling a grep over string concatenations.

Primary sources: <https://en.wikipedia.org/wiki/Clickstream> and <https://developer.mozilla.org/en-US/docs/Web/API/Beacon_API>.

## Decision rules

- Name events as object followed by action, or the converse, but commit to one and stay.
- The name must be guessable from the user-facing action alone.
- Never name an event after the component or handler that triggered it.
- Every new event must be distinct from existing ones at the same level: similar-action existing names rejected at proposal.
- The set of allowed verbs is a fixed list; new verbs are governance changes.
- All-caps, camelCase, and snake_case are all fine; mixed cases in one taxonomy are not.

## Procedure

1. Fix the ordering principle: object-then-action or the reverse.
2. Draft the allowed verbs list.
3. Write the initial names against the user-facing journey map.
4. Check each name for guessability: a new engineer tries to guess it cold.
5. Review the initial set for near-duplicates and merge before adoption.
6. Record naming decisions in the taxonomy so future proposals don't relitigate them.

## Anti-patterns

- event named for the component, the class, or the developer who added it.
- The same user action named differently on web and mobile.
- A new doc-saved event alongside an existing file_saved event because the team never read the taxonomy.
- A verb list that keeps growing (form_a, form_b... form_z).
- One-time or time-stamped names: signup_2024_02 becomes the same event 600 times.

## Done checklist

- [ ] Ordering principle fixed and documented.
- [ ] Allowed-verbs list written.
- [ ] Names checked for guessability.
- [ ] Near-duplicate check done.
- [ ] Naming rationale recorded.
- [ ] Platform parity verified per name.

## Sources

- Background on clickstream event quality and naming: <https://en.wikipedia.org/wiki/Clickstream>
- The client-side delivery context every event exists inside: <https://developer.mozilla.org/en-US/docs/Web/API/Beacon_API>
- Source listing for common web event names: <https://developer.mozilla.org/en-US/docs/Web/Events>

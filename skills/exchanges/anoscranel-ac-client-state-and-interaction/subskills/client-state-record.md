---
name: client-state-record
domain: software-engineering/client-state-record
trigger: "Writing the record of the client data layer and its promises."
anti_trigger: "Not for the changelog, and not for API documentation."
scope: "The written record: layer choices, promises made, failure paths."
status: seedling
---

# Client state record

## Standard

The client-state record says what the client promises the user and what happens when each promise breaks. Every optimistic update is a promise with a rollback; every cached read is a promise with a freshness bound; every offline write is a promise with a sync outcome; every undo is a promise with a scope and a depth. The record lists these as decisions with their failure paths, so that when behaviour surprises a user, the answer is either "as designed, here is the design" or "the design was silent here, and that is the bug".

The record also fixes architecture facts that otherwise live only in folklore: the data layer and its keys, the state machine representations, the cache classes, the queue, the virtualization thresholds. A new engineer reading it should predict the app's behaviour on a flaky network without reading the source. Where the record and the code disagree, one of them is wrong and the record review says which.

Primary sources: <https://tanstack.com/query/latest/docs/framework/react/overview> and <https://localfirstweb.dev/>.

## Decision rules

- List every promise the client makes: optimistic paths, freshness bounds, offline surfaces, undo scope.
- For each promise, record the failure path and what the user sees when it fires.
- Record the layer facts: query keys, machine representations, cache classes, queue, thresholds.
- State the refetch policy and the concurrency rules per contested key.
- Record quota budgets and update-flow behaviour.
- Review the record when behaviour changes, not when the calendar says so.

## Procedure

1. Enumerate the user-visible promises the client makes.
2. Pair each with its failure path and user-visible outcome.
3. Document the data layer: keys, staleness, invalidation map.
4. Document the machines, cache classes, queue, and virtualization thresholds.
5. State refetch policy and concurrency rules.
6. Schedule the record's review against behaviour changes.

## Anti-patterns

- Architecture docs that describe intent with no failure paths.
- A rollback implemented but never written down, so the next rewrite omits it.
- Records that describe the happy path in glowing detail.
- Cache policies that exist in code with no policy statement.
- Records reviewed quarterly regardless of what changed.

## Done checklist

- [ ] Promises enumerated.
- [ ] Failure paths per promise recorded.
- [ ] Layer facts documented.
- [ ] Refetch and concurrency rules stated.
- [ ] Quota and update flow recorded.
- [ ] Review tied to behaviour changes.

## Sources

- Data-layer reference: <https://tanstack.com/query/latest/docs/framework/react/overview>
- Local-first principles: <https://localfirstweb.dev/>
- Statecharts: <https://xstate.js.org/docs/>

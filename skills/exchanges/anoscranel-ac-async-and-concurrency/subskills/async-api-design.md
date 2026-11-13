---
name: async-api-design
domain: software-engineering/async-api-design
trigger: "Designing an async interface that states its semantics."
anti_trigger: "Not for HTTP API contracts, and not for recommending a runtime."
scope: "Futures, callbacks, and the semantics an async interface must state."
status: seedling
---

# Async API design

## Standard

An async interface is a promise about when and whether code runs, and most async bugs are contract gaps: the caller assumed exactly-once, the interface delivers at-least-once; the caller assumed the callback runs on the original context, the interface runs it on a worker; the caller assumed cancellation stops work, the interface ignores the signal. The design's job is to state these semantics, not to make them ambient.

The choices are concrete: future-or-callback as the surface; once, at-least-once, or at-most-once as the delivery; which context the continuation runs on and what happens if that context is gone; what error delivery looks like when the failure happens after the caller has moved on; and what cancellation does to the task, to already-delivered partial results, and to the caller's obligations. A client library that hides these choices behind "it just works" has simply chosen for its users, silently, and its users will discover the choices one incident at a time.

Primary sources: <https://martinfowler.com/> and <https://clig.dev/>.

## Decision rules

- State the surface — future, callback, or both — and the reason for the choice.
- State delivery semantics: once, at-least-once, or at-most-once, of results and of errors.
- State the execution context of callbacks, and the behaviour when that context is gone.
- State what cancellation does to the task, after partial results have already been observed.
- State backpressure: what happens when a caller submits work faster than it completes.
- State the caller's lifecycle duties: what the caller must await or close before releasing resources.

## Procedure

1. Choose the surface and document the reason.
2. Write the semantics table: delivery, context, cancellation, errors, backpressure.
3. Review each entry against how a naive caller would read the signature alone.
4. Provide the minimal safe wrapper so misuse is hard, not merely discouraged.
5. State the lifecycle obligations in the type or the docs, not in tribal memory.
6. Test the boundary cases: cancel mid-flight, error after partial results, context gone.

## Anti-patterns

- Sync and async variants of one operation with divergent cancellation semantics, undocumented.
- Callbacks onto a pool without saying so, letting callers touch thread-unsafe state.
- Errors delivered to a context the caller has already released.
- Cancellation offered in a signature with no explanation of what gets skipped.
- No backpressure statement in an interface whose callers can submit unboundedly.

## Done checklist

- [ ] Surface chosen and justified.
- [ ] Semantics table written.
- [ ] Naive-caller reading checked.
- [ ] Safe wrapper provided.
- [ ] Lifecycle obligations stated.
- [ ] Boundary cases tested.

## Sources

- Async API patterns: <https://martinfowler.com/>
- Interface convention guidance: <https://clig.dev/>
- Concurrency API literature: <https://dl.acm.org/>

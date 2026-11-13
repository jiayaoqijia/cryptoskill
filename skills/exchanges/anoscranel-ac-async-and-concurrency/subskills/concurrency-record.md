---
name: concurrency-record
domain: software-engineering/concurrency-record
trigger: "Writing a concurrency design so a reviewer can check it."
anti_trigger: "Not for recommending a runtime, and not for a PR description."
scope: "The written record: shared state, orderings, cancellation, and blast radius."
status: seedling
---

# Concurrency record

## Standard

The concurrency record documents the design's shared state, its orderings, its cancellation policy, and its testing evidence — the artefact a reviewer needs to find a race by reading instead of by reproducing. It is small, because a well-designed concurrent module has little to say: a list of shared items with their guards, the lock order, the cancellation checkpoints, and the tests that exercise the risky interleavings.

Its most useful entry is the blast radius per shared structure: what breaks, and for which users, when this invariant is violated. A reviewer triaging a report can then map "this symptom" to "this invariant" from the record rather than from a week of archaeology, and a future maintainer can know which invariant cannot be safely traded away under load pressure — the exact trade a stressed engineer is tempted to make.

Primary sources: <https://martinfowler.com/> and <https://osf.io/prereg/>.

## Decision rules

- The record lists shared mutable items, their guarding mechanism, and the invariant sentence.
- The record lists the global lock order and every nested acquisition.
- The record lists cancellation checkpoints and the work skipped between them.
- The record lists the tests that exercise the risky interleavings, with their schedules.
- Each invariant carries its blast radius: what breaks when it is violated.
- The record is rewritten to expose any intended invariant relaxations, never edited quietly.

## Procedure

1. Write the shared-state list with guards and invariants.
2. Write the lock order and nested acquisition list.
3. Write the cancellation checkpoints and skipped work.
4. Attach the schedule tests by name.
5. Add the blast radius per invariant.
6. Amend with dates; an invariant relaxation is a change, and it is recorded as one.

## Anti-patterns

- Prose about the design's elegance with no list of shared items.
- A lock order known by convention, written nowhere.
- Cancellation described as "handled" with no checkpoints named.
- No blast radius, so a pressure-release decision trades an unknown invariant.
- Invariants relaxed under load without any record entry.

## Done checklist

- [ ] Shared items, guards, and invariants listed.
- [ ] Lock order and nested acquisitions listed.
- [ ] Cancellation checkpoints listed.
- [ ] Schedule tests named.
- [ ] Blast radius per invariant.
- [ ] Relaxations amended with dates.

The record also settles the review question that costs the most time: when a reviewer cannot tell whether a change is safe under concurrency, the change waits on an archaeological read of the code. A record that answers "which structures does this touch, what is blast radius if it races" from a single file turns that review from a week of guessing into an afternoon, which is the actual product of writing it down.

## Sources

- Concurrency design documentation: <https://martinfowler.com/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Concurrency literature: <https://dl.acm.org/>

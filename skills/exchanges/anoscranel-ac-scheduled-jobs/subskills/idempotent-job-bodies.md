---
name: idempotent-job-bodies
domain: software-engineering/idempotent-job-bodies
trigger: "Making a job body safe to run twice, late, or in the wrong order."
anti_trigger: "Not for the delivery semantics themselves (that is missed-run-semantics)."
scope: "Writing a job body that is safe to run twice, in order, at the wrong time."
status: seedling
---

# Idempotent job bodies

## Standard

Schedule delivery in practice is at-least-once: retried runs, catch-up replays, and lock edge cases mean the same instance may execute more than once. A job body is safe when the second execution of the same instance produces the state the first one should have — no duplicate rows, no double sends, no twice-charged accounts. Idempotency is a property of the body, not of the scheduler's promises.

The reliable technique is an instance key: a stable identifier for "this run of this job for this period", derived from the schedule time, not from execution time. Every effect the body produces checks the key first — a ledger row exists, an export file exists, a flag is set — and skips work already done. Where effects span multiple systems, the key must be shared across them, or the two systems can disagree about what happened.

## Decision rules

- Derive the instance key from the scheduled period, not from wall-clock execution time.
- Record the key at the start of the run so partial failures are diagnosable.
- Make every external effect check the key before acting.
- Where multiple systems are touched, use the same key across all of them.
- Decide whether a partial run leaves state that marks the whole instance done; usually it must not.
- Test the double-run case explicitly: run the same instance twice, compare the state.

## Procedure

1. Define the instance key from the job and the scheduled period.
2. Identify every external effect the body produces.
3. Add key-checked guards to each effect.
4. Ensure failure mid-run does not mark the instance complete.
5. Run the same instance twice in a test and compare the resulting state.
6. Record the key scheme in the job's definition.

## Anti-patterns

- Deriving the key from the execution timestamp, so a retried run counts as new work.
- Guarding the database write but not the outbound message.
- Marking the instance done before the last effect completes.
- Idempotency by "we will just be careful".
- Testing only the happy path once.

## Done checklist

- [ ] Instance key defined from the period.
- [ ] Every external effect guarded by the key.
- [ ] Same key across all touched systems.
- [ ] Partial failure does not mark completion.
- [ ] Double-run test executed and compared.
- [ ] Key scheme recorded.

## Sources

- Idempotency in messaging: <https://martinfowler.com/articles/patterns-of-distributed-systems/idempotent-receiver.html>
- At-least-once delivery semantics: <https://learn.microsoft.com/en-us/azure/architecture/>
- Exactly-once discussion and its cost: <https://www.confluent.io/blog/>

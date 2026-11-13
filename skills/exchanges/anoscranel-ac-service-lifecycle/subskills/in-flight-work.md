---
name: in-flight-work
domain: software-engineering/in-flight-work
trigger: "Deciding what happens to work that is running at termination."
anti_trigger: "Not for retry and timeout budgets, and not for workflow engines."
scope: "Requests, jobs, and transactions that are running when termination arrives."
status: seedling
---

# In-flight work

## Standard

At termination, the service holds three kinds of work: an HTTP request it is answering, a longer job it is mid-way through, and a transaction or outward call that is half-committed. Each disposes differently. The request can finish within the drain window and return cleanly. The job cannot, and must either checkpoint, or be idempotent enough for a restart to resume it, or be moved to a durable queue so the next instance owns it. The half-committed outward call is the dangerous one: the service dies either before or after the peer received the effect, and the design must assume both possibilities.

The disposition must exist per work type, written before it is needed. A drain window covers seconds; a checkpoint covers restarts; a durable queue covers instance replacement; and a compensating action or an idempotency key covers the outward call that may or may not have landed. "The platform will restart it" is a disposition only if the work is resumable, and most work is not resumable by default.

Primary sources: <https://sre.google/> and <https://martinfowler.com/>.

## Decision rules

- Classify each work type the service performs: request, long job, outward effect.
- Record the disposition per type: complete in drain, checkpoint-resume, queue-handoff, or idempotent-effect.
- Record the idempotency key on outward effects that may have landed before death.
- Record which requests may be safely retried by their caller and which must not.
- Record the checkpoint interval for long jobs and the work lost per checkpoint gap.
- Test termination at the worst moment: mid-transaction, mid-job, mid-request.

## Procedure

1. List work types and their durations.
2. Assign a disposition per type, with the reason.
3. Add idempotency keys to outward effects.
4. Mark caller-retriable requests.
5. Set checkpoint intervals and record the lost-work window.
6. Terminate the service at each boundary moment and observe the outcome.

## Anti-patterns

- One disposition for all work, usually "just let it die".
- Outward calls with no idempotency key, double-charging on the unlucky restart.
- Checkpoints so rare that a termination loses an hour of a long job.
- Requests assumed retriable by the caller when the operation is not idempotent.
- No test of any termination path, so the first kill is production's.

## Done checklist

- [ ] Work types classified.
- [ ] Disposition per type with reason.
- [ ] Idempotency keys on outward effects.
- [ ] Retriability marked per request type.
- [ ] Checkpoint interval recorded.
- [ ] Boundary-moment termination tested.

## Sources

- Reliability and lifecycle practice: <https://sre.google/>
- Idempotency and messaging patterns: <https://martinfowler.com/>
- Distributed systems references: <https://www.distributed-systems.net/>

---
name: ordering-guarantees
domain: software-engineering/ordering-guarantees
trigger: "Deciding what order webhook deliveries arrive in and what the receiver must do."
anti_trigger: "Not for queue partitioning, and not for database ordering."
scope: "Sequence numbers, out-of-order arrival, and what a receiver must do."
status: seedling
---

# Ordering guarantees

## Standard

Retries and parallel delivery destroy ordering. An event that failed and is retried arrives after a later event that succeeded on its first attempt, so the receiver sees a creation after an update. Whether that matters depends on what the events represent: independent notifications tolerate reordering, while a state machine does not.

The mechanism that lets a receiver cope is a sequence number in the envelope, monotonically increasing per stream. With it, a receiver can discard an event older than one it has already applied, or buffer briefly and apply in order. Without it, the receiver has no basis to decide and must either accept the reordering or query the sender for current state.

Primary sources: <https://www.rfc-editor.org/rfc/rfc9110> and <https://csrc.nist.gov/>.

## Decision rules

- Record whether ordering is guaranteed, and if so per what stream.
- Record the sequence number or version field the receiver can use.
- Record the receiver's strategy: apply in arrival order, buffer, or discard stale.
- Record the maximum reordering a receiver should expect, since a retry horizon bounds it.
- Record the events for which ordering matters, since guaranteeing it globally is expensive.
- Record the reconciliation path when the receiver detects a gap.

## Procedure

1. Record the ordering property per event type.
2. Record the sequence field and its scope.
3. Record the receiver's ordering strategy.
4. Record the expected reordering bound.
5. Record gap detection and reconciliation.
6. Write the guarantee with its stream definition.

## Anti-patterns

- Claiming global ordering while retrying in parallel.
- A sequence number scoped globally when delivery is partitioned.
- A receiver that buffers without a bound, waiting for a missing event.
- Assuming ordering implies completeness, when events can also be lost past the horizon.
- No reconciliation path, so a detected gap cannot be resolved.

## Done checklist

- [ ] Ordering property recorded per event type.
- [ ] Sequence field and scope recorded.
- [ ] Receiver strategy recorded.
- [ ] Reordering bound recorded.
- [ ] Gap detection recorded.
- [ ] Reconciliation recorded.

The receiver's stale-event rule also needs a bound: discarding every event older than the last applied sequence protects against reordering but silently drops a legitimate late event that carried a correction, so the rule should distinguish a retry from a new event with an older version rather than treating both the same way.


## Sources

- HTTP delivery semantics: <https://www.rfc-editor.org/rfc/rfc9110>
- Integrity and ordering controls: <https://csrc.nist.gov/>
- Messaging practice: <https://www.enterpriseintegrationpatterns.com/>

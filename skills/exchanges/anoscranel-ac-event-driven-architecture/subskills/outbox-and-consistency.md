---
name: outbox-and-consistency
domain: software-engineering/outbox-and-consistency
trigger: "Publishing an event atomically with the state change that caused it."
anti_trigger: "Not for broker selection, and not for two-phase commit design."
scope: "Publishing an event atomically with the state change that caused it."
status: seedling
---

# Outbox and consistency

## Standard

A service that writes to its database and then publishes an event has a window in which one succeeded and the other did not. Writing first and publishing second loses events when the publish fails; publishing first and writing second produces events for changes that never happened. Neither ordering is safe without a mechanism that makes the pair atomic.

The transactional outbox makes that mechanism local: the event is written to an outbox table inside the same database transaction as the state change, and a separate relay reads the table and publishes. The database's transaction provides atomicity, and the relay provides at-least-once delivery, which the consumer already handles.

Primary sources: <https://martinfowler.com/> and <https://www.enterpriseintegrationpatterns.com/>.

## Decision rules

- Record whether the state change and the event are written in one transaction.
- Record the outbox table's schema, including the event payload and its ordering key.
- Record the relay's mechanism and its polling or change-capture approach.
- Record the delivery guarantee the relay provides and where duplicates can occur.
- Record the outbox table's retention and how it is pruned without losing unpublished rows.
- Record the ordering guarantee the relay preserves, which depends on how it claims rows.

## Procedure

1. Record the state change and the event it must produce.
2. Write both in one transaction into the outbox.
3. Implement the relay with a claim mechanism and record its guarantee.
4. Record ordering: whether the relay publishes in insert order per key.
5. Record pruning that cannot remove an unpublished row.
6. Test the failure of the publish step and verify the event arrives later.

## Anti-patterns

- Publishing after commit with no retry, which loses events.
- Publishing before commit, which emits events for rolled-back work.
- A relay with no claim mechanism, so two instances publish the same row.
- Pruning the outbox by age without checking publication.
- Assuming the relay preserves global order.

## Done checklist

- [ ] Atomicity mechanism recorded.
- [ ] Outbox schema recorded.
- [ ] Relay mechanism and guarantee recorded.
- [ ] Ordering guarantee recorded.
- [ ] Pruning rule recorded.
- [ ] Publish failure tested.

The relay's claim mechanism deserves the same scrutiny as the consumer's deduplication: two relay instances that both read an unclaimed row will publish duplicates, which the consumer absorbs, so the outbox is safe by delegating the problem rather than solving it. Saying that explicitly keeps the guarantee chain visible.


## Sources

- Integration pattern reference: <https://www.enterpriseintegrationpatterns.com/>
- Distributed systems practice: <https://martinfowler.com/>
- Cloud native data guidance: <https://www.cncf.io/>

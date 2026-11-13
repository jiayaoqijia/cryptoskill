---
name: at-least-once-and-dedup
domain: software-engineering/at-least-once-and-dedup
trigger: "Handling duplicate webhook deliveries."
anti_trigger: "Not for exactly-once claims, and not for queue acknowledgement semantics."
scope: "Why retries imply duplicates, and the key that makes them harmless."
status: seedling
---

# At-least-once and deduplication

## Standard

Retrying a delivery whose response was lost produces a duplicate: the sender cannot distinguish a request that never arrived from one that arrived and whose acknowledgement failed. Every webhook system is therefore at-least-once, and the receiver carries the obligation to make duplicates harmless through an idempotency key and a record of what it has processed.

The key must be supplied by the sender and stable across retries. An event identifier in the envelope serves this purpose; a hash of the payload does not, because two legitimate events can carry identical payloads. The receiver's record of processed identifiers must be durable enough to survive its own restart, since a duplicate arriving after a restart is the most likely case.

Primary sources: <https://csrc.nist.gov/> and <https://www.rfc-editor.org/rfc/rfc9110>.

## Decision rules

- Record the deduplication key and confirm it is stable across retries.
- Record the receiver's store of processed keys and its durability.
- Record the retention window for processed keys, which must exceed the retry horizon.
- Record the response for a duplicate: the original success, or an explicit acknowledgement.
- Record what happens when the key store is unavailable, since failing open processes duplicates.
- Record the ordering interaction, since deduplication does not imply ordering.

## Procedure

1. Record the event identifier and its stability.
2. Record the receiver's key store and durability.
3. Set the retention window above the retry horizon.
4. Record the duplicate response.
5. Record behaviour when the store is unavailable.
6. Write the deduplication model from the receiver's side.

## Anti-patterns

- Deriving the key from payload content.
- A key store in memory, which loses its record on restart.
- Retention shorter than the retry horizon, so a late duplicate is processed.
- Returning an error on a duplicate, which invites further retries.
- Assuming deduplication also orders the events.

## Done checklist

- [ ] Key and stability recorded.
- [ ] Key store and durability recorded.
- [ ] Retention window recorded.
- [ ] Duplicate response recorded.
- [ ] Store-unavailable behaviour recorded.
- [ ] Ordering noted separately.

The deduplication key also has to survive the receiver's own scaling: two instances processing the same event concurrently will both find it unprocessed unless the key write is atomic, so the store needs a unique constraint rather than a read-then-write check, which is the race that produces a duplicate despite the design.


## Sources

- Security and integrity controls: <https://csrc.nist.gov/>
- HTTP retry semantics: <https://www.rfc-editor.org/rfc/rfc9110>
- Distributed delivery practice: <https://aws.amazon.com/builders-library/>

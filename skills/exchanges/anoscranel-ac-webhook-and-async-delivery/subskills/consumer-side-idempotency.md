---
name: consumer-side-idempotency
domain: software-engineering/consumer-side-idempotency
trigger: "Making a webhook receiver safe to call more than once."
anti_trigger: "Not for sender retry policy, and not for queue acknowledgement."
scope: "The receiver's obligation, and how it records what it has processed."
status: seedling
---

# Consumer-side idempotency

## Standard

The receiver is the party that can make at-least-once delivery harmless, and it does so by recording which events it has applied before applying them. The record must be written transactionally with the effect, or a crash between the two either loses the event or applies it twice — which is the same choice the sender faced, moved one hop downstream.

The design decision is what counts as processed. Recording the event identifier before performing the effect means a crash mid-effect leaves the event marked done but unapplied, which is worse than a duplicate. Recording after the effect means a crash between them causes the duplicate. The correct arrangement is to write the identifier and the effect in one transaction where the store allows it, and to design the effect itself to tolerate repetition where it does not.

Primary sources: <https://csrc.nist.gov/> and <https://aws.amazon.com/builders-library/>.

## Decision rules

- Record the transaction boundary: identifier and effect written together or separately.
- Record the effect's own tolerance for repetition, which is what covers a non-transactional store.
- Record the acknowledgement timing, which should be after the effect is durable.
- Record the behaviour on a duplicate: acknowledge success without reapplying.
- Record the store's retention and whether a very late duplicate can slip through.
- Record the dead-letter path for events the receiver cannot process.

## Procedure

1. Record the transaction boundary for identifier and effect.
2. Record whether the effect is naturally idempotent.
3. Time the acknowledgement after durability.
4. Record duplicate handling.
5. Record retention and the late-duplicate case.
6. Write the receiver's model with its acknowledgement point.

## Anti-patterns

- Acknowledging before the effect is durable.
- Marking processed before applying, which loses events on a crash.
- A non-idempotent effect with no transaction covering both writes.
- Retrying an unprocessable event forever instead of dead-lettering it.
- Assuming the sender will not retry because the response looked successful.

## Done checklist

- [ ] Transaction boundary recorded.
- [ ] Effect idempotency recorded.
- [ ] Acknowledgement timing recorded.
- [ ] Duplicate handling recorded.
- [ ] Retention recorded.
- [ ] Dead-letter path recorded.

The unprocessable event is worth a separate decision: a payload that the receiver cannot parse will never succeed on retry, so it belongs in a dead-letter store with the reason recorded, rather than consuming the retry schedule until the sender disables the endpoint for a reason nobody can diagnose.


## Sources

- Distributed delivery practice: <https://aws.amazon.com/builders-library/>
- Security and integrity controls: <https://csrc.nist.gov/>
- Messaging patterns: <https://www.enterpriseintegrationpatterns.com/>

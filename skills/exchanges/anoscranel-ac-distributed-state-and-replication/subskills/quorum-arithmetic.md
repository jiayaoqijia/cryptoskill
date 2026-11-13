---
name: quorum-arithmetic
domain: software-engineering/quorum-arithmetic
trigger: "Computing whether quorum reads and writes must overlap."
anti_trigger: "Not for consensus protocol internals, and not for recommending a store."
scope: "Read and write quorums, the overlap that makes them intersect, and the arithmetic of staleness."
status: seedling
---

# Quorum arithmetic

## Standard

In a leaderless store, a read quorum and a write quorum intersect when the sum of their sizes exceeds the number of replicas. With five replicas, writes to three and reads from three always share a node, so a read sees the latest write; writes to three and reads from two do not guarantee the intersection, and reads can return stale data by design. The arithmetic is the whole decision: the guarantee is bought with the quorum sizes, and their sum is the price.

The same arithmetic bounds staleness and failure tolerance. A store configured with a write quorum of all replicas stops accepting writes when any one fails; a store with a majority quorum keeps writing and accepts that a minority of replicas holds older data until read repair or anti-entropy catches up. Reading at a lower quorum than the writes is the classic self-deception: the numbers pass, the intersection never happens, and the data is stale while everything reports healthy.

Primary sources: <https://jepsen.io/> and <https://www.allthingsdistributed.com/>.

## Decision rules

- Record the replica count and the read and write quorum sizes.
- Verify the sum of read and write quorum sizes exceeds the replica count.
- Compute the fault tolerance: how many failures still allow reads, writes, both.
- Compute the staleness case when the quorums do not intersect and record its likelihood.
- Record the repair mechanism: read repair, anti-entropy, or both, and its cadence.
- Record the behaviour when a quorum cannot be met.

## Procedure

1. Fix the replica count.
2. Choose read and write quorum sizes per operation class.
3. Check the intersection arithmetic for each pairing.
4. Compute fault tolerance for reads and for writes separately.
5. Choose and record the repair mechanism and cadence.
6. Write the degraded-mode behaviour when a quorum is unavailable.

## Anti-patterns

- Read and write quorum sizes that do not sum past the replica count.
- Reading at a lower quorum than the writes that must be seen.
- Assuming a quorum read returns the newest value without version comparison.
- Ignoring writes that landed on nodes outside the read quorum.
- No answer for the no-quorum case beyond an error.

## Done checklist

- [ ] Replica count recorded.
- [ ] Quorum sizes per operation recorded.
- [ ] Intersection arithmetic checked.
- [ ] Fault tolerance computed for reads and writes.
- [ ] Repair mechanism and cadence recorded.
- [ ] No-quorum behaviour written.

## Sources

- Quorum and consistency analysis: <https://jepsen.io/>
- Distributed computing notes: <https://www.allthingsdistributed.com/>
- Dynamo-style replication papers: <https://www.distributed-systems.net/>

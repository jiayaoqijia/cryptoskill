---
name: quorum-intersection
domain: software-engineering/quorum-intersection
trigger: "Working out why a committed entry is safe and what a read quorum proves."
anti_trigger: "Not for placement and load distribution, and not for client session logic."
scope: "Why majorities overlap, what a write quorum proves, and read quorum subtleties."
status: seedling
---

# Quorum intersection

## Standard

The safety argument of consensus is overlap. Any two majorities of the same configuration share at least one member, so a new leader, which must have a majority, cannot have missed an entry that the old leader, which also had a majority, committed. Quorum intersection is the property that turns counting into correctness: every ack was on a majority, every election is by a majority, and majorities cannot be disjoint.

Writing reads correctly is the subtle half. A majority is reachable does not mean the responding member is current; a stale member can answer a read with old data while a majority elsewhere holds newer entries. The safe patterns are reading through the leader with a lease, verifying the read index on a quorum, or accepting unlinearizable reads and labelling them honestly. The dangerous pattern is assuming majority reachability implies freshness for the specific member that answered.

Primary sources: <https://raft.github.io/raft.pdf> and <https://en.wikipedia.org/wiki/Quorum_(distributed_systems)>.

## Decision rules

- Record the cluster size and the quorum sizes for writes, elections, and reads.
- Record the read path: through-leader, quorum-verified, or stale-allowed, and label it.
- Record what happens at the size boundary, such as losing the majority and service.
- Record the intersection argument in the deployment's terms as a statement someone could check.
- Record tie-breaking counts, sparse clusters, and zone failures.
- Record witness or learner roles in arithmetic, noting that they cannot vote.

## Procedure

1. Write out the quorum arithmetic for the deployment's exact sizes.
2. Classify every read API offered by the consistency it returns.
3. Test the minority case: what a surviving minority serves, if anything.
4. Write the intersection argument as an auditable sentence.
5. Check that voters are what fail independently, not witnessed rumor.
6. Record the read classification in the consensus record.

## Anti-patterns

- Assuming majority reachability equals majority freshness on a given read.
- Offering a consistent read API the mechanism does not actually implement.
- Counting a witness as voting.
- Losing a majority and expecting any member to take writes.
- Partitioning voters so that correlated failures take both halves of an intersection.

## Done checklist

- [ ] Quorum arithmetic recorded.
- [ ] Every read API classified.
- [ ] Minority behaviour tested.
- [ ] Intersection argument written.
- [ ] Voter independence checked.
- [ ] Read classification recorded.

## Sources

- Raft and quorums: <https://raft.github.io/raft.pdf>
- Quorum systems reference: <https://en.wikipedia.org/wiki/Quorum_(distributed_systems)>
- Consistency models discussion: <https://dataintensive.net/>

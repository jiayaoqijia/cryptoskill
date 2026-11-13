---
name: learners-and-witnesses
domain: software-engineering/learners-and-witnesses
trigger: "Reading non-voting members and their role in the protocol."
anti_trigger: "Not for membership changes, and not for read replicas outside the protocol."
scope: "Non-voting members, cross-region learners, and the cost of full copies."
status: seedling
---

# Learners and witnesses

## Standard

Not every member carries a full vote and a full copy. A learner receives the log without voting, which makes it a catch-up mechanism — a proposed voter that learns the history before being granted a say — and, in a cross-region deployment, a local read presence whose staleness is bounded by the leader's forwarding pace. A witness holds a vote's paperwork without the data: it participates in the quorum arithmetic while storing only the metadata needed to vote, and nothing serves a read from it.

The two roles answer different costs. Learners answer the cost of full replication where a full voter is not needed to survive failures; witnesses answer the cost of quorum breadth where storing the data itself would be the expense. Both rely on the same honesty as an operator question: does the deployment's failure arithmetic actually work, and does the role as deployed do what its name claims.

Primary sources: <https://raft.github.io/raft.pdf> and <https://en.wikipedia.org/wiki/Paxos_(computer_science)>.

## Decision rules

- Record each member's role: voter, learner, or witness, and what the deployment's arithmetic requires.
- Record a learner's promotion path and the catch-up condition required before a vote.
- Record what a learner's read actually serves, with its staleness bound.
- Record why the witness is needed rather than a learner or a voter.
- Record whether the absence of full copies on a witness leaves any hazard, such as serving no recovery role.
- Record which members can seed a new member and how a historical snapshot is transported.

## Procedure

1. Enumerate the roles of all members, including non-voting ones.
2. Write the promotion path for a learner with the catch-up condition.
3. Test a learner's served read against the committed state.
4. Verify the witness participates only in voting, not read service.
5. Check the quorum arithmetic with and without witnesses.
6. Record seeding and snapshot transport in the record.

## Anti-patterns

- Counting a learner as voting in the arithmetic.
- Serving reads from a witness that holds no data.
- Promoting a lagging learner without a catch-up verification.
- Assuming a cross-region learner is current; it follows at leader pace.
- Storing a witness's vote without counting what it costs in metadata.

## Done checklist

- [ ] Roles enumerated.
- [ ] Promotion path written.
- [ ] Learner read staleness bounded.
- [ ] Witness read-hazard checked.
- [ ] Arithmetic verified with roles.
- [ ] Seeding and snapshots recorded.

## Sources

- Raft roles and membership: <https://raft.github.io/raft.pdf>
- Paxos learner roles: <https://en.wikipedia.org/wiki/Paxos_(computer_science)>
- Distributed patterns: <https://martinfowler.com/articles/patterns-of-distributed-systems/>

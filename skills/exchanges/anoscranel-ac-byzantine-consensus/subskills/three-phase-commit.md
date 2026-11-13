---
name: three-phase-commit
domain: software-engineering/three-phase-commit
trigger: "Reading why Byzantine agreement runs a three-phase structure."
anti_trigger: "Not for two-phase database commit, and not for protocol selection."
scope: "Pre-prepare, prepare, and commit, and what each round eliminates."
status: seedling
---

# Three-phase commit

## Standard

Byzantine agreement runs three rounds because each eliminates one class of disagreement. In pre-prepare, the primary assigns a sequence number to a request and broadcasts it. In prepare, replicas exchange their acceptance so that all honest nodes know that all honest nodes saw the same assignment. In commit, they exchange that knowledge again, which guarantees that a value is finalized for every honest node even if the primary disappears before the next request.

What each round buys is the elimination of a scenario. Without prepare, a faulty primary could tell different replicas different sequence numbers. Without commit, two honest replicas could disagree about whether a later value was finalized while a view change replaced the primary mid-flight. The rounds are not redundancy; they are each doing distinct work, and the cost is the latency — three message exchanges before a client sees its reply.

Primary sources: <https://pmg.csail.mit.edu/papers/osdi99.pdf> and <https://en.wikipedia.org/wiki/PBFT>.

## Decision rules

- Record the three phases and the message each replica sends per phase.
- Record the quorum each phase requires and what happens short of it.
- Record what a prepared value means and its role in a later view change.
- Record the latency cost: three exchanges before the client's reply.
- Record how batch processing amortizes the cost.
- Record what the protocol does when the primary sends two values for one sequence number.

## Procedure

1. Trace one client request through pre-prepare, prepare, and commit.
2. Note the quorum that must sign each phase.
3. Record the meaning of prepared and its guarantee.
4. Trace a request that stalls in prepare and meets a view change.
5. Count the message exchanges in the steady-state path.
6. Write the three-phase description with each round's elimination stated.

## Anti-patterns

- Treating the three phases as redundant safety.
- Assuring a client at prepare rather than commit.
- Forgetting that prepared values are the anchors of a view change.
- Assuming the primary is honest and skipping the pre-prepare check.
- Compounding latency without batching when throughput matters.

## Done checklist

- [ ] Request traced through all phases.
- [ ] Phase quorums recorded.
- [ ] Prepared meaning recorded.
- [ ] Stall-into-view-change traced.
- [ ] Exchange count measured.
- [ ] Each round's elimination stated.

A further note on the primary's checkpoint: the three rounds presuppose that the primary assigns sequence numbers honestly, so the checkpoint mechanism that bounds how far a faulty primary can reorder history is part of the same structure and belongs beside it in the record.

## Sources

- PBFT phases: <https://pmg.csail.mit.edu/papers/osdi99.pdf>
- Phase structure reference: <https://en.wikipedia.org/wiki/PBFT>
- Distributed systems patterns: <https://martinfowler.com/articles/patterns-of-distributed-systems/>

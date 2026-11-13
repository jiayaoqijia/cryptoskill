---
name: replica-arithmetic
domain: software-engineering/replica-arithmetic
trigger: "Working out how many replicas a Byzantine deployment needs."
anti_trigger: "Not for crash-fault quorums, and not for placements and load."
scope: "Why 3f+1 is the minimum, and the quorum sizes it produces."
status: seedling
---

# Replica arithmetic

## Standard

Crash tolerance needs 2f+1 replicas because a truthful majority suffices. Byzantine tolerance needs 3f+1 because the witnesses themselves may lie: to outvote f liars, the system needs enough honest nodes that the honest nodes alone form a majority of every quorum. With n = 3f+1, a quorum of 2f+1 contains at least f+1 honest nodes, and any two such quorums overlap in at least f+1 nodes — enough honest overlap to catch a contradiction, since f liars cannot impersonate f+1.

The quorum sizes follow: prepare and commit quorums are 2f+1 of 3f+1, and a client's reply is trusted at f+1 matching responses. The arithmetic is unforgiving in both directions — four replicas tolerate exactly one fault, and losing two of four leaves the system unable to progress, which is a smaller margin than a crash-tolerant cluster of the same size enjoys.

Primary sources: <https://pmg.csail.mit.edu/papers/osdi99.pdf> and <https://en.wikipedia.org/wiki/PBFT>.

## Decision rules

- Record f, the fault tolerance, and n = 3f+1, the replica count.
- Record the quorum sizes the protocol uses for each phase.
- Record the size at which the system loses progress: n minus f.
- Record what f+1 honest overlap makes detectable in one sentence.
- Record the minimum deployment and whether it tolerates one fault or none.
- Record how membership growth changes f and the quorum arithmetic.

## Procedure

1. State f and the derived replica count.
2. Compute the quorum per phase from the protocol.
3. Compute the stop-progress point for the deployment.
4. Write the f+1 honest overlap sentence.
5. Check the smallest deployment against its fault budget.
6. Write the arithmetic with the margin stated.

## Anti-patterns

- Running 3f+1 arithmetic while tolerating no faults in practice.
- Assuming quorums can be relaxed under load.
- Forgetting the margin is thinner than a crash cluster of the same size.
- Growing membership without growing quorums.
- Treating f as a tuning knob; it is the load-bearing number.

## Done checklist

- [ ] f and replica count stated.
- [ ] Phase quorums computed.
- [ ] Stop-progress point computed.
- [ ] Honest overlap sentence written.
- [ ] Smallest deployment checked.
- [ ] Growth behaviour recorded.

The arithmetic also deserves a stated worst case for the deployment's own size: at four replicas tolerating one fault, a second failure halts progress entirely, and an operator who has not rehearsed that arithmetic will add a fifth replica in the middle of an incident and change the quorum mid-flight.

## Sources

- PBFT paper with the 3f+1 derivation: <https://pmg.csail.mit.edu/papers/osdi99.pdf>
- PBFT reference: <https://en.wikipedia.org/wiki/PBFT>
- Byzantine generals problem: <https://en.wikipedia.org/wiki/Byzantine_fault>

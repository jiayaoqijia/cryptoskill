---
name: consistent-hashing
domain: software-engineering/consistent-hashing
trigger: "Reading a hash ring, virtual nodes, or rendezvous placement."
anti_trigger: "Not for hash partitioning in general, and not for consensus protocols."
scope: "Rings, virtual nodes, rendezvous hashing, and movement proportional to change."
status: seedling
---

# Consistent hashing

## Standard

Consistent hashing fixes the rehash cost. Keys and nodes are both placed on a ring by hash; a key belongs to the first node found walking clockwise. When a node joins or leaves, only the keys whose arc passed through that node's position move — typically a fraction proportional to the change, not the whole keyspace — so cluster resize becomes an incremental operation instead of a rewrite.

The refinement that makes rings work at realistic node counts is the virtual node: each physical node claims many scattered positions, which both smooths the load distribution and limits the damage any one node's failure causes. Rendezvous hashing reaches the same destination from another direction — compute a score per key-node pair and take the highest — trading the ring's incremental machinery for a stateless computation that is easy to reason about and verify.

Primary sources: <https://en.wikipedia.org/wiki/Consistent_hashing> and <https://en.wikipedia.org/wiki/Rendezvous_hashing>.

## Decision rules

- Record the ring construction: hash, ordering, and how a key's owner is found.
- Record the virtual node count and the load variance it produces.
- Record the movement fraction on a single node join and a single failure.
- Record whether node weight maps to virtual node count.
- Record whether the scheme is ring or rendezvous, and why.
- Record how replicas are chosen: successive ring positions, distinct failure domains, or both.

## Procedure

1. Write the placement rule in one sentence a reader can execute.
2. Measure load variance across nodes at the chosen virtual node count.
3. Compute the fraction of keys moving on one join and one departure.
4. Check replica placement for failure-domain collision.
5. Compare ring versus rendezvous for the system's size and staleness needs.
6. Write the scheme with the measured variance and movement stated.

## Anti-patterns

- Too few virtual nodes, producing visible load imbalance.
- Replicas on successive ring positions that share a rack.
- Treating consistent hashing as fixing hot keys; it distributes nodes, not popularity.
- Mixing hash functions between clients, splitting ownership.
- Ignoring the nonuniform-capacity case; weight belongs in the design.

## Done checklist

- [ ] Placement rule stated executably.
- [ ] Virtual node count and variance recorded.
- [ ] Movement fractions computed.
- [ ] Weighting scheme recorded.
- [ ] Ring-versus-rendezvous decided.
- [ ] Replica failure domains verified.

## Sources

- Consistent hashing reference: <https://en.wikipedia.org/wiki/Consistent_hashing>
- Rendezvous hashing reference: <https://en.wikipedia.org/wiki/Rendezvous_hashing>
- Consistent hashing in distributed systems: <https://martinfowler.com/articles/patterns-of-distributed-systems/>

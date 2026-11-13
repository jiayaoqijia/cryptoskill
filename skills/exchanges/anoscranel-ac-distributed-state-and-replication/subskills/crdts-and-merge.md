---
name: crdts-and-merge
domain: software-engineering/crdts-and-merge
trigger: "Choosing data types whose merges cannot conflict."
anti_trigger: "Not for recommending a store or library, and not for cache coherency."
scope: "Data types whose merges cannot conflict, and their limits."
status: seedling
---

# CRDTs and merge

## Standard

A conflict-free replicated data type is a structure — a counter, a set, a register, a sequence — with a merge operation that is commutative, associative, and idempotent. Merge any two replica states in any order and any number of times, and the result is the same. That property is what removes conflict resolution from the application's path: there is no conflict to resolve because the merge is defined for all cases.

The cost is that the type decides the semantics. A grow-only set can never remove an element; observed-remove sets remove by observing a tag and lose true re-adds; a counter can only add and subtract through a per-node component that grows forever; a sequence CRDT carries metadata that grows with concurrent edits. Rich CRDTs exist for maps and documents, and they all trade state size and metadata for the no-conflict guarantee. Choosing a CRDT is choosing the operation set you will allow, and the choice must be explicit.

Primary sources: <https://martinfowler.com/> and <https://jepsen.io/>.

## Decision rules

- Record the operation set the application needs and match it to what the type supports.
- Record the merge semantics in the application's terms, not the implementation's.
- Record state growth: per-node components, tombstones, and metadata that accumulate.
- Record the bounds on tombstone retention and the consequence of early collection.
- Record the causality the type preserves and what it loses, such as true re-adds.
- Test merge with genuinely concurrent edits from independent nodes.

## Procedure

1. Enumerate the operations the application performs on the shared value.
2. Match them to a type family and record the mismatches.
3. State the merge semantics in application terms.
4. Model state growth over the retention period.
5. Bound tombstones and record the visibility consequence.
6. Test concurrent edits across nodes without a coordination step.

## Anti-patterns

- Choosing a CRDT because conflicts are annoying, without matching the operation set.
- A grow-only structure where removal is required.
- Unbounded per-node metadata on high-cardinality keys.
- Tombstones collected while offline replicas could resurrect the removed value.
- Treating merge convergence as the application's expected ordering.

## Done checklist

- [ ] Operation set matched to the type.
- [ ] Merges stated in application terms.
- [ ] State growth modelled.
- [ ] Tombstone bound and consequence recorded.
- [ ] Causality limits recorded.
- [ ] Concurrent-edit test executed.

## Sources

- CRDT design and usage: <https://martinfowler.com/>
- Consistency verification under partitions: <https://jepsen.io/>
- Distributed data structures primer: <https://www.distributed-systems.net/>

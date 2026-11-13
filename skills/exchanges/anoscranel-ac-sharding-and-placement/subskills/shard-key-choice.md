---
name: shard-key-choice
domain: software-engineering/shard-key-choice
trigger: "Choosing the key that decides where each record lives."
anti_trigger: "Not for replication of the copies, and not for query tuning after the fact."
scope: "The key as the load balancer, and the analysis that precedes choosing it."
status: seedling
---

# Shard key choice

## Standard

The shard key is the load balancer. Every request whose key lands on shard three is served by shard three, so the distribution of key values in real traffic — not the distribution in theory — decides the distribution of load. A key with high cardinality and even access frequency balances; a key whose values repeat unevenly concentrates; a key absent from the query forces every node to answer.

Choice follows from the query shapes the system must serve. Point lookups want the key the lookup arrives with; range scans want a key whose order matches the scan's order; joins prefer co-locating the join key; time-series traffic wants time in the key or out of it, depending on whether old partitions should rest. Most real systems rank these and accept losses on the weaker ones.

Primary sources: <https://martinfowler.com/articles/patterns-of-distributed-systems/> and <https://en.wikipedia.org/wiki/Shard_(database_architecture)>.

## Decision rules

- Record every query shape the datasets must serve, with its frequency.
- Record the candidate keys and what each does to each query shape.
- Record the key's cardinality and the access frequency per value.
- Record whether any single value can exceed one shard's capacity.
- Record what the key does to co-location of related records.
- Record the escape hatch: is the key changeable, and at what cost.

## Procedure

1. Enumerate query shapes with frequencies.
2. Score candidate keys against each shape.
3. Measure the value distribution of the leading candidate.
4. Test the largest tenant or celebrity key against a single shard's capacity.
5. Decide what co-location is preserved or sacrificed.
6. Write the choice with the losses named, not only the gains.

## Anti-patterns

- Choosing the key for the query the team likes rather than the traffic's mode.
- Ignoring cardinality and assuming any key spreads.
- Choosing a key a thundering tenant can dominate.
- Forgetting that absent keys become scatter-gather.
- Pretending the choice is permanent; state the re-key cost.

## Done checklist

- [ ] Query shapes and frequencies recorded.
- [ ] Candidate keys scored.
- [ ] Value distribution measured.
- [ ] Celebrity capacity tested.
- [ ] Co-location trade-off stated.
- [ ] Re-key cost stated.

A useful discipline is to write the query that must not become a scatter-gather before choosing the key: if the system's defining query arrives without the candidate key, no amount of clever placement repairs it afterwards, and the key choice should fail early rather than be regretted later.

## Sources

- Sharding patterns overview: <https://martinfowler.com/articles/patterns-of-distributed-systems/>
- Shard architecture reference: <https://en.wikipedia.org/wiki/Shard_(database_architecture)>
- Distributed data placement background: <https://dataintensive.net/>

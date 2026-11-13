---
name: replication-topologies
domain: software-engineering/replication-topologies
trigger: "Choosing how copies of data are organised and who may accept writes."
anti_trigger: "Not for cache topology, and not for recommending a product."
scope: "Primary-replica, multi-leader, and leaderless; what each can promise."
status: seedling
---

# Replication topologies

## Standard

Three topologies cover most deployed systems. Primary-replica routes all writes to one node and ships changes to replicas; it is simple to reason about and its failure mode is the failover. Multi-leader lets several nodes accept writes and resolves conflicts after the fact; it buys availability and locality and pays in conflict handling. Leaderless (or peer-to-peer) lets any node accept any operation and uses quorums to make reads and writes intersect; it accepts partitions gracefully and pays in read repair and anti-entropy traffic.

The honest comparison is by what each guarantees. Primary-replica gives a single ordering of writes and a clear point of truth; multi-leader gives none of that by default and requires conflict handling at read or write time; leaderless gives tunable consistency whose arithmetic you must do yourself. Choosing by familiarity rather than by the guarantee an operation needs is the commonest expensive mistake.

Primary sources: <https://jepsen.io/> and <https://martinfowler.com/>.

## Decision rules

- State which operations need which consistency guarantee before choosing a topology.
- Record who may accept writes, and what happens when a writer is unreachable.
- Record the ordering guarantee: single order per key, or none.
- Record the conflict story for any topology with more than one writer.
- Record the failover plan and the window during which writes cannot be accepted.
- Record the replication transport and whether it is synchronous or asynchronous.

## Procedure

1. List the operations with their consistency and latency requirements.
2. Match the requirements against what each topology can promise.
3. Choose the write set and the ordering story.
4. Design the conflict handling if there is more than one writer.
5. Write the failover plan with its detection time and promotion step.
6. Record the transport and its synchrony, and the resulting staleness bound.

## Anti-patterns

- Choosing a topology before stating the guarantees needed.
- Multi-leader with no conflict policy, resolved by "whatever lands last".
- Treating an asynchronous replica as a backup of committed data.
- No written failover plan, so failover is invented during the failure.
- Synchronous replication everywhere, paying the latency on operations that do not need it.

## Done checklist

- [ ] Operations listed with their guarantees.
- [ ] Write set and ordering recorded.
- [ ] Conflict story recorded.
- [ ] Failover plan written with timings.
- [ ] Transport synchrony recorded.
- [ ] Staleness bound recorded.

## Sources

- Consistency analysis of distributed databases: <https://jepsen.io/>
- Patterns of replicated data: <https://martinfowler.com/>
- Distributed systems primer: <https://www.distributed-systems.net/>

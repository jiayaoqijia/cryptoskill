---
name: ordering-and-partitioning
domain: software-engineering/ordering-and-partitioning
trigger: "Working out where message ordering is guaranteed."
anti_trigger: "Not for broker selection, and not for database ordering."
scope: "Where ordering is guaranteed, and what the partition key decides."
status: seedling
---

# Ordering and partitioning

## Standard

Ordering is guaranteed within a partition and not across partitions, so the partition key decides which messages can be reordered. Two events about the same entity must share a key or they may arrive in either order; two events about different entities need not, and forcing them to share a key serialises work that could proceed in parallel.

Choosing the key is therefore a correctness decision, not a performance one. Keying by user identifier preserves per-user order and distributes load; keying by tenant preserves tenant order at the cost of hot partitions; keying by a random identifier distributes perfectly and guarantees no order at all. The record should state the key and the ordering guarantee it buys.

Primary sources: <https://www.cncf.io/> and <https://www.enterpriseintegrationpatterns.com/>.

## Decision rules

- Record the partition key and the ordering guarantee it produces.
- Record which events must be ordered relative to each other, and which need not.
- Record the hot-partition risk of the chosen key and its mitigation.
- Record the consumer's assumption about ordering, since a consumer that assumes global order will break.
- Record what happens to ordering during a rebalance or a partition change.
- Record the key's stability, since a changed key breaks the guarantee for in-flight messages.

## Procedure

1. Record the events that must be ordered and their shared entity.
2. Choose a key that groups them and record the guarantee.
3. Assess hot-partition risk and record the mitigation.
4. Record the consumer's ordering assumption explicitly.
5. Record rebalance behaviour and its effect on in-flight ordering.
6. Record the key's stability across changes.

## Anti-patterns

- Assuming a topic guarantees global ordering.
- Keying by a random value and then expecting per-entity order.
- Keying by tenant and creating a partition that carries most of the traffic.
- Changing the key without thinking about in-flight messages.
- A consumer that assumes order the producer does not provide.

## Done checklist

- [ ] Partition key and guarantee recorded.
- [ ] Events requiring order identified.
- [ ] Hot-partition risk recorded.
- [ ] Consumer assumption recorded.
- [ ] Rebalance behaviour recorded.
- [ ] Key stability recorded.

The key's effect on latency is worth recording alongside its ordering guarantee: a key that concentrates traffic gives correct ordering and a hot partition, and the consumer for that partition becomes the throughput ceiling for the whole topic, which is a cost the ordering guarantee paid for.


## Sources

- Messaging and streaming standards: <https://www.cncf.io/>
- Integration pattern reference: <https://www.enterpriseintegrationpatterns.com/>
- Distributed systems reference: <https://martinfowler.com/>

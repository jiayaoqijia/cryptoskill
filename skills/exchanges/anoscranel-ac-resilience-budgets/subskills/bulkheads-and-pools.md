---
name: bulkheads-and-pools
domain: software-engineering/bulkheads-and-pools
trigger: "Stopping one dependency from consuming all of a service's capacity."
anti_trigger: "Not for load balancing policy, and not for capacity planning."
scope: "Isolating a failing dependency's resource use from everything else."
status: seedling
---

# Bulkheads and pools

## Standard

A bulkhead partitions a resource so that exhaustion in one partition cannot exhaust the whole. The ship analogy is exact: a hull breach floods one compartment, not the vessel. In software the compartments are connection pools, thread pools, and concurrency limits, and the partition is per dependency or per workload class rather than shared.

The design question is where to divide. Partitioning by dependency protects one slow dependency's callers from another's, which is usually the right split because dependencies fail independently. Partitioning by endpoint protects a latency-sensitive path from a batch path, which is the right split when the two have different tolerance. Both are valid, and the record should state which dimension was chosen and why.

Primary sources: <https://aws.amazon.com/builders-library/> and <https://sre.google/>.

## Decision rules

- Record each pool and what it is partitioned by: dependency, workload class, or tenant.
- Record the size of each partition and the total across partitions.
- Record the queue behaviour when a partition is full: reject, wait, or block.
- Record whether a request can hold capacity in more than one partition, which creates a deadlock risk.
- Record the monitoring that shows per-partition saturation rather than aggregate.
- Record the partition that would saturate first under the expected load.

## Procedure

1. Record the shared resources and their current sharing.
2. Choose the partition dimension and record the reason.
3. Size each partition and record the total.
4. Record the behaviour at saturation.
5. Record deadlock risk where a request spans partitions.
6. Write the design with the first-to-saturate partition named.

## Anti-patterns

- Partitioning by a dimension along which failures are correlated anyway.
- Partition sizes summing to more than the backing resource can serve.
- A blocking wait when a partition is full, which converts isolation into a stall.
- A request holding one partition while waiting on another.
- Aggregate dashboards that hide one partition's saturation.

## Done checklist

- [ ] Partition dimension recorded.
- [ ] Sizes recorded per partition.
- [ ] Saturation behaviour recorded.
- [ ] Cross-partition holding recorded.
- [ ] Per-partition monitoring recorded.
- [ ] First-to-saturate named.

The partition count is its own cost: every partition reserves capacity even when idle, so a system split into twenty pools is a system with twenty minimums, and the arithmetic should show the aggregate reservation against the backing resource. A partition scheme that reserves more than the database can serve is isolation that guarantees contention.


## Sources

- Bulkhead and isolation patterns: <https://aws.amazon.com/builders-library/>
- Reliability guidance: <https://sre.google/>
- Capacity context: <https://sre.google/workbook/table-of-contents/>

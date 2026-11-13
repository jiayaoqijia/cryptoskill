---
name: hot-keys-and-skew
domain: software-engineering/hot-keys-and-skew
trigger: "Measuring and mitigating a load imbalance that no placement fixes."
anti_trigger: "Not for choosing a shard key, and not for queue backpressure policy."
scope: "Measuring skew, the celebrity-key problem, and mitigation that does not fragment the data."
status: seedling
---

# Hot keys and skew

## Standard

Skew is an empirical property of traffic, not of the placement scheme. A perfectly even partition of the key space is still unevenly loaded when one key receives a tenth of all requests: every shard is a quarter full, and one shard is on fire. The celebrity-key problem is the canonical case — one popular item, one owning partition, no spreading without changing what the key means or how it is cached.

Measurement comes before mitigation. The honest metric is a request distribution per key over a representative window: percentile counts per key, the top keys' share of total load, and whether the top keys rotate or persist. Mitigation then chooses among splitting the hot key by a salt, caching the hot item ahead of the shard, or replicating the hot partition — each moving the bottleneck somewhere observably different.

Primary sources: <https://dataintensive.net/> and <https://martinfowler.com/articles/patterns-of-distributed-systems/>.

## Decision rules

- Record the per-key request distribution over a stated window.
- Record the top keys' aggregate share of load, and whether they persist across windows.
- Record the hottest shard's load relative to the mean shard.
- Record any salting scheme and what it does to point reads of the hot key.
- Record cache layers that absorb hot reads, and their hit behaviour under failure.
- Record the point at which skew triggers action rather than discussion.

## Procedure

1. Collect a per-key request histogram for a representative window.
2. Compute top-keys' load share and hottest-shard ratio.
3. Determine whether hot keys rotate or persist.
4. Evaluate salting: what assembling a salted key's views costs.
5. Evaluate caching: where reads offload and what a cold cache does to the shard.
6. Write the skew assessment with the chosen mitigation and its trade.

## Anti-patterns

- Declaring hash placement sufficient and never measuring per key.
- Salting everything, fragmenting unrelated cold data along with the hot.
- Caching without deciding what a cache-miss storm does to the owning shard.
- Averaging the hot shard into a fleet mean and calling it healthy.
- Mitigating in an outage without a measured prior.

## Done checklist

- [ ] Per-key histogram collected.
- [ ] Top-key share and hottest-ratio computed.
- [ ] Rotation behaviour recorded.
- [ ] Salt cost evaluated.
- [ ] Cache failure behaviour evaluated.
- [ ] Action threshold stated in the record.

## Sources

- Skewed partitioning and hot spots: <https://dataintensive.net/>
- Distributed systems patterns: <https://martinfowler.com/articles/patterns-of-distributed-systems/>
- Load balancing reference: <https://en.wikipedia.org/wiki/Load_(computing)>

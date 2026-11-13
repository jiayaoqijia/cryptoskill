---
name: vector-clocks-and-conflicts
domain: software-engineering/vector-clocks-and-conflicts
trigger: "Detecting whether two writes happened concurrently."
anti_trigger: "Not for time synchronisation, and not for recommending a store."
scope: "Detecting concurrent writes and what the detection costs."
status: seedling
---

# Vector clocks and conflicts

## Standard

Two writes are concurrent when neither happened before the other, and a wall-clock timestamp cannot establish that — clocks skew, and two nodes can assign later timestamps to earlier events. A vector clock keeps a counter per node, and comparing two versions' clocks establishes one of three relations: one causally precedes the other, or they are concurrent. Concurrency is the signal that a conflict exists and no ordering is justified.

The cost is what the design must state. Clock entries grow with the number of writers, and a store that keeps every version until resolution, or forever, accumulates them without bound. Most deployments bound the damage by pruning, by keeping a fixed number of siblings, or by resolving quickly — and pruning trades correctness for space in ways the application must know about. Conflict *detection* is the honest limit of the tool: deciding what the merged value should be is the application's work.

Primary sources: <https://jepsen.io/> and <https://www.distributed-systems.net/>.

## Decision rules

- Record how versions are stamped and by what: vector clock, version vector, or hybrid logical clock.
- Record what a concurrent comparison triggers: siblings retained, merge invoked, or last-writer-wins.
- Record the bound on retained versions and the correctness consequence of pruning.
- Record where conflict resolution executes: client, coordinator, or application-defined merge.
- Record the case where the clock must be reset — node replacement, counter overflow.
- Test the conflict path with a genuine partition, not with sequential writes from one client.

## Procedure

1. Choose the versioning mechanism.
2. Define what a concurrent detection produces.
3. Bound version retention and record the consequence.
4. Define the resolution path and where it runs.
5. Define clock reset and node-replacement behaviour.
6. Test conflict detection under a real partition.

## Anti-patterns

- Conflict detection by timestamp comparison on skewed clocks.
- Unbounded sibling retention that turns hot keys into memory failures.
- Silent last-writer-wins presented to the application as causal ordering.
- Conflict resolution code that has never run under a real conflict.
- Clock state lost on node restart, merging unrelated histories.

## Done checklist

- [ ] Versioning mechanism recorded.
- [ ] Concurrent-detection outcome defined.
- [ ] Retention bound and consequence recorded.
- [ ] Resolution path and location recorded.
- [ ] Clock reset behaviour recorded.
- [ ] Partition test executed.

## Sources

- Versioning and consistency analysis: <https://jepsen.io/>
- Distributed systems primer: <https://www.distributed-systems.net/>
- Logical clock literature hub: <https://dataintensive.net/>

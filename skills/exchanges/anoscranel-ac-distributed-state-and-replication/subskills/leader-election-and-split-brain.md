---
name: leader-election-and-split-brain
domain: software-engineering/leader-election-and-split-brain
trigger: "Designing failover and preventing two primaries at once."
anti_trigger: "Not for recommending a coordination service, and not for cache failover."
scope: "Choosing a leader, fencing old ones, and the failure that is two."
status: seedling
---

# Leader election and split brain

## Standard

A primary-replica system needs a way to replace a failed primary, and the replacement mechanism decides whether the system can end up with two. A naive election — promote the replica that first notices the primary is gone — fails precisely when the network is degraded, because different nodes notice different things, and the honest verdict is that any election that relies on a failure detector without a quorum can elect two primaries.

Split brain is prevented, when it is prevented, by arithmetic and by fencing. The arithmetic is a quorum: a candidate needs agreement from a majority of nodes, so two majorities cannot exist. The fencing is a lease or an epoch number: an old primary that keeps accepting writes must have its writes rejected by replicas and by clients, and a new primary's term must be visible wherever a write could land. Both mechanisms have failure windows, and the design must state what happens inside them.

Primary sources: <https://raft.github.io/> and <https://jepsen.io/>.

## Decision rules

- Record the election mechanism and whether a candidate needs a majority quorum.
- Record the failure detector's timeout and its false-positive behaviour under load.
- Record the fencing mechanism and who enforces it against an old primary.
- Record the promotion time from detection to the new primary accepting writes.
- Record what happens to writes accepted by the old primary in the window.
- State the residual window in which two primaries can exist and what is lost if it does.

## Procedure

1. Write the detection step and its timeout.
2. Write the election step and its quorum requirement.
3. Write the fencing: epoch, lease, or a majority's rejection of a stale term.
4. Test the failover under a network partition and time it.
5. Record the outcome for writes in flight across promotion.
6. Record the residual dual-primary window and its recovery path.

## Anti-patterns

- Election by first-detects-wins, with no quorum.
- A failure detector timeout shorter than the network's worst latency.
- No fencing, on the assumption promotion is atomic.
- Untested failover whose first execution is in production.
- Ignoring writes accepted by the deposed primary, losing committed data.

## Done checklist

- [ ] Election mechanism and quorum recorded.
- [ ] Failure detector timeout recorded.
- [ ] Fencing mechanism recorded.
- [ ] Promotion time measured.
- [ ] In-flight write outcome recorded.
- [ ] Dual-primary window and recovery stated.

## Sources

- Consensus and election protocols: <https://raft.github.io/>
- Partition and failure analysis: <https://jepsen.io/>
- Distributed coordination primer: <https://www.distributed-systems.net/>

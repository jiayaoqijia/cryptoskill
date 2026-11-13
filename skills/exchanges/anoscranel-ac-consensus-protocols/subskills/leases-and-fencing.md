---
name: leases-and-fencing
domain: software-engineering/leases-and-fencing
trigger: "Deciding how a stale leader is stopped from acting."
anti_trigger: "Not for choosing a protocol, and not for authentication tokens."
scope: "Leader leases versus fencing tokens, and the clock question."
status: seedling
---

# Leases and fencing

## Standard

Every leader-based system eventually answers one question: when an old leader does not yet know it is old, what stops it from acting? The two mechanisms in production are leases and fencing. A lease grants authority for a bounded time: the leader promises not to act after expiry without renewal, and correctness then depends on clock assumptions — if a lease expires in one second of real time, a scheduler's pause or a clock jump can break that promise silently.

Fencing removes the clock. Every act carries a monotonically increasing token — commonly the term and index — and the receiving side refuses tokens older than the highest it has seen. A stale leader's writes arrive with a stale token and are rejected without needing any timing assumption. The trade is that fencing must be checked at every act's destination, which is trivial for a log append and impossible for a side effect the protocol cannot see.

Primary sources: <https://martinfowler.com/articles/patterns-of-distributed-systems/> and <https://raft.github.io/raft.pdf>.

## Decision rules

- Record whether design relies on leases, fencing, or both.
- Record the lease duration and the clock assumptions behind it.
- Record what a clock jump does to the safety of the lease's interval.
- Record the fencing token's composition and the checked enforcement point.
- Record side effects that bypass the fencing check, such as writes to external systems.
- Record the clock sync service, and what losing it does to safety.

## Procedure

1. State the authority mechanism in one sentence.
2. If leases: derive the duration and the assumption in writing.
3. If fencing: write the token's structure and where it is checked.
4. Enumerate every side effect and ask whether its destination checks anything.
5. Trace the stale-leader scenario through the mechanism.
6. Write the result with the clock assumption named or its absence stated.

## Anti-patterns

- Using a lease for a side effect that no second party can check.
- Assuming an NTP-synced clock cannot jump; it can, and leases then lie.
- Fencing log appends but not downstream effects.
- Grace periods that let an old leader act just a little longer.
- Renewing a lease on a paused process's behalf.

## Done checklist

- [ ] Authority mechanism stated.
- [ ] Lease assumptions written or fencing token defined.
- [ ] Clock failure behaviour classified.
- [ ] Enforcement points enumerated.
- [ ] Side effects outside the check named.
- [ ] Stale-leader scenario traced.

## Sources

- Fencing and lease patterns: <https://martinfowler.com/articles/patterns-of-distributed-systems/>
- Raft leadership: <https://raft.github.io/raft.pdf>
- Clock synchronisation limits: <https://en.wikipedia.org/wiki/Network_Time_Protocol>

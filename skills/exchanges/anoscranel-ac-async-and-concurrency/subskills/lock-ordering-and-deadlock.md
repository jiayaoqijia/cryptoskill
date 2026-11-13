---
name: lock-ordering-and-deadlock
domain: software-engineering/lock-ordering-and-deadlock
trigger: "Preventing the interleaving where everyone waits forever."
anti_trigger: "Not for distributed locks, and not for runtime tuning."
scope: "Acquiring in order, timing out, and why deadlock is a design error."
status: seedling
---

# Lock ordering and deadlock

## Standard

Deadlock requires four conditions, but in practice it reduces to one design question: can two threads acquire overlapping sets of locks in different orders? If every path acquires the same set of locks in the same global order, the cycle cannot form; if any two paths disagree about order, the cycle forms whenever the schedule is unlucky — which it will be, once, in production.

The design rules follow. Impose a global lock order and verify it mechanically, by inspection or by a runtime checker, because the order violations are invisible until the schedule reveals them. Prefer acquiring one lock at a time: release before taking the next whenever the invariant allows, because two locks held are one order requirement and ten locks held are forty-five. And wrap every acquisition that might wait with a timeout, not because the timeout fixes anything, but because it converts an unreproducible hang into a diagnosable failure you can log and fix.

Primary sources: <https://dl.acm.org/> and <https://martinfowler.com/>.

## Decision rules

- List every lock and assign it a position in a global order; record the order.
- Verify every acquisition path takes locks in ascending order, by inspection or tooling.
- Minimise locks held simultaneously; release before the next acquisition where the invariant allows.
- Wrap cross-task waits with timeouts, and treat a timeout as a defect with a name.
- Record every place one lock is held while acquiring another — the exact deadlock surface.
- Record the deadlock detection story: runtime detection, watchdog, or nothing.

## Procedure

1. Enumerate the locks and their guards.
2. Assign a global order and write it down.
3. Rewrite acquisition paths to follow the order.
4. Reduce simultaneous holdings where possible.
5. Add timeouts with logged failures.
6. Add a retry-under-load test that exercises concurrent mixed-order workloads.

## Anti-patterns

- Lock order implicit in the functions' call structure, never written.
- Holding a branch's lock while acquiring the root's, in some code path only.
- An untimed wait that turns a bug into a permanent hang.
- A "fix" that retries the same order — reordering is the fix; retry prolongs the hang.
- Nested acquisitions spread so wide that the global order is unverifiable by a human.

## Done checklist

- [ ] Global lock order written.
- [ ] Acquisition paths verified against it.
- [ ] Simultaneous holdings minimised.
- [ ] Timeouts wrapping cross-task waits.
- [ ] Nested acquisitions listed.
- [ ] Concurrency stress test executed.

## Sources

- Deadlock theory and practice: <https://dl.acm.org/>
- Concurrency patterns: <https://martinfowler.com/>
- Systems references: <https://www.distributed-systems.net/>

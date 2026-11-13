---
name: shared-state-and-primitives
domain: software-engineering/shared-state-and-primitives
trigger: "Identifying shared mutable state and choosing what protects it."
anti_trigger: "Not for distributed consensus, and not for recommending a runtime."
scope: "What shared mutable state is, and what locks and atomics actually provide."
status: seedling
---

# Shared state and primitives

## Standard

Shared mutable state exists the moment two threads of execution can reach the same data with at least one of them writing. The first design move is not choosing a primitive — it is reducing the sharing: make state immutable and share copies, confine it to one task and pass messages, or partition it so each partition has exactly one writer. Whatever sharing remains needs an explicit mechanism, chosen for the actual requirement: an atomic for a single counter or flag, a lock for a multi-step invariant across fields, a compare-and-swap loop for lock-free update of a pointer-sized value.

The primitives guarantee less than their names suggest. An atomic update is atomic — it does not tear — but two atomic updates in sequence are not atomic together, and a check-then-act built from separate atomic reads and writes still races. A mutual-exclusion lock provides exclusion, not correctness: the invariant it protects must actually be restored before release, and the lock guards exactly the fields it was written to guard, nothing more. Choosing locks as the default rather than the last resort multiplies the surface for the classic ordering failures.

Primary sources: <https://martinfowler.com/> and <https://dl.acm.org/>.

## Decision rules

- List every piece of mutable state and every task that can reach it.
- Prefer removing sharing — immutability, confinement, message passing — before adding synchronisation.
- Record the chosen mechanism per shared item and the reason it suffices.
- Record the invariant each lock protects, as a sentence.
- Record memory-ordering requirements explicitly when using atomics across fields.
- Record any check-then-act sequence and the mechanism that makes it one step.

## Procedure

1. Enumerate mutable state and its reachability from each task.
2. Remove sharing where possible by restructuring.
3. For each remaining shared item, choose the weakest sufficient mechanism.
4. Write the invariant per lock and the ordering requirement per atomic.
5. Mark every check-then-act and give it a single atomic step.
6. Review the list against every new task added later.

## Anti-patterns

- A lock pasted onto shared state without a stated invariant.
- Two sequential atomics assumed atomic together.
- Check-then-act on a shared flag, racy by construction.
- Sharing chosen for convenience where a copy would remove the problem.
- A lock that grew to guard everything, serialising the whole program.

## Done checklist

- [ ] Shared state enumerated with reachability.
- [ ] Sharing reduced before synchronising.
- [ ] Mechanism per item with reason.
- [ ] Invariant sentence per lock.
- [ ] Ordering requirements recorded.
- [ ] Check-then-act sequences eliminated or made atomic.

## Sources

- Concurrency design patterns: <https://martinfowler.com/>
- Concurrency research literature: <https://dl.acm.org/>
- Systems programming references: <https://www.distributed-systems.net/>

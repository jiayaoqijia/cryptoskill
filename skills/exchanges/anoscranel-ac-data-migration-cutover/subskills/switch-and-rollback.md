---
name: switch-and-rollback
domain: software-engineering/switch-and-rollback
trigger: "Flipping traffic and knowing the way back."
anti_trigger: "Not for code rollback mechanics, and not for a tool choice."
scope: "The cutover trigger, the reverse path, and what rollback restores."
status: seedling
---

# Switch and rollback

## Standard

The switch is the moment the new store becomes authoritative, and it needs three things written before it happens: what triggers it, who can pull it, and the way back. The trigger is a measured criterion — shadow quiet for N days, reconciliation divergence zero for M — never a calendar date. The way back is the design decision most often skipped, and it must state what a rollback restores: the old store, which has kept receiving writes if dual writes continued, and which therefore requires either that dual writes never stopped, or a reverse-copy plan nobody wants to execute at 3 a.m.

Two properties make rollback real. Reversibility in a stated time: if the way back takes eight hours of reverse copying, the rollback is not an emergency measure and the system must survive on the new store until it completes. Learnability: after the rollback, the divergence that forced it must be reconcilable — writes that went only to the new store during the failed period need a path back or a deliberate decision to lose them, written in advance.

Primary sources: <https://martinfowler.com/> and <https://sre.google/>.

## Decision rules

- Record the trigger as a measured criterion with numbers, not a date.
- Record who may switch and who may roll back, by name or on-call role.
- Record whether dual writes continue after the switch, for how long, and why that makes rollback cheap or expensive.
- Record the rollback duration honestly: minutes if writes continued, a reverse copy otherwise.
- Record the disposition of writes that exist only in the new store after a rollback.
- Rehearse the rollback once under controlled conditions.

## Procedure

1. Define the trigger, the roles, and the announce protocol.
2. Decide the post-switch dual-write continuation window.
3. Write the rollback plan with its measured duration.
4. Write the new-store-only writes disposition.
5. Rehearse the rollback.
6. After the real switch, keep dual writes until the retention window closes.

## Anti-patterns

- A switch scheduled by date with the criteria "probably fine by then".
- Stopping dual writes at the moment of switch, making rollback a reverse migration.
- A rollback plan whose duration has never been measured.
- New-store-only writes with no stated disposition after rollback.
- No rehearsal, so the rollback's first execution is during the incident.

## Done checklist

- [ ] Trigger stated in numbers.
- [ ] Roles named.
- [ ] Dual-write continuation window set.
- [ ] Rollback duration measured.
- [ ] Write disposition after rollback written.
- [ ] Rollback rehearsed.

## Sources

- Migration patterns: <https://martinfowler.com/>
- Release and rollback practice: <https://sre.google/>
- Distributed systems references: <https://www.distributed-systems.net/>

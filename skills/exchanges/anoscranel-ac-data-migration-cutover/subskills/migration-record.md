---
name: migration-record
domain: software-engineering/migration-record
trigger: "Writing down the migration before running it."
anti_trigger: "Not for a tool recommendation, and not for a ticket dump."
scope: "The written record: strategy, phases, triggers, and the numbers compared."
status: seedling
---

# Migration record

## Standard

The migration record states the strategy and its accepted failure, the phases with their gates, the triggers and roles, the rollback with its measured duration, and the numbers the comparison produced. It is written before the migration begins, because a migration's correctness is a sequence of criteria, and criteria written during the event become negotiations.

Its most useful page is the timeline plan: what phase begins when the previous phase's gate is met — never when a calendar date arrives — and what measurement constitutes each gate. The second most useful page is the divergence history: every reconciliation pass with its counts. A migration that ends with a page of zeros is documented; one that ends with optimism is not.

Primary sources: <https://martinfowler.com/> and <https://osf.io/prereg/>.

## Decision rules

- The record names the strategy and the failure it accepts.
- Each phase carries a gate stated as a measurement, and the next phase depends on the gate.
- The record names the truth store for every period of overlap.
- The rollback duration is measured and recorded, with the rehearsal date.
- The divergence history is appended for every reconciliation pass.
- The record closes with the zero-divergence date and the sign-off.

## Procedure

1. Write the strategy, accepted failure, and phase list.
2. State each phase's gate as a measurement.
3. Name truth per period of overlap.
4. Measure and record the rollback duration and rehearsal.
5. Append every reconciliation result with its date.
6. Close with the zero-divergence date.

## Anti-patterns

- Phases gated on dates because the business wanted a deadline.
- The record begun after the migration, reconstructed from chat.
- No divergence history, so the quiet-period claim has no evidence.
- Truth named once for the whole plan while the overlap had two periods with different truths.
- A rollback duration copied from another migration.

## Done checklist

- [ ] Strategy and accepted failure recorded.
- [ ] Phase gates as measurements.
- [ ] Truth store per overlap period.
- [ ] Rollback measured with rehearsal date.
- [ ] Divergence history appended per pass.
- [ ] Zero-divergence close recorded.

One final entry deserves its own line: the cost of the migration's complexity, counted in the engineers' hours spent on comparison tooling, reconciliation passes, and the retention window. The zero-downtime strategies are not free — they trade an outage for weeks of dual-write attention — and a record that states both prices lets the next migration choose with its eyes open rather than by reflex toward whichever strategy the last team survived.

## Sources

- Migration documentation patterns: <https://martinfowler.com/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Data engineering references: <https://www.distributed-systems.net/>

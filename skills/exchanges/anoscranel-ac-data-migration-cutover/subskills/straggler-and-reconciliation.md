---
name: straggler-and-reconciliation
domain: software-engineering/straggler-and-reconciliation
trigger: "Catching rows written late and making both stores agree forever."
anti_trigger: "Not for one-time data repair, and not for audit tooling in general."
scope: "Rows written late, counted after, and reconciled into truth."
status: seedling
---

# Straggler and reconciliation

## Standard

A migration is not complete when the switch happens, because writes arrive at the old store for a while longer: clients that cached a connection, jobs that held a session, a queue message processed from a stale consumer. Those stragglers must be written to the new store, and the reconciliation pass that catches them must state which store is truth during the period — the quiet week after cutover, both stores receive writes from different sources, and an unguided merge corrupts.

The reconciliation design has three parts: a detection pass that compares the stores by primary key and version, a resolution rule that takes fresher or truth-designated rows, and an anomaly bucket for pairs that both changed in conflicting ways, which get held for human review rather than auto-resolved. After the retention window — the period in which straggler writes are still possible — a final pass must find zero divergence, and that zero is the migration's actual completion certificate.

Primary sources: <https://www.postgresql.org/> and <https://martinfowler.com/>.

## Decision rules

- Record the sources of straggler writes and how long each can persist.
- Record the retention window and what closes it: drained queues, retired writers, revoked credentials.
- Record the truth store during the reconciliation period.
- Run the detection pass on a schedule until it finds zero twice in a row.
- Route conflicting pairs to an anomaly bucket with human review, not silent resolution.
- Record the final zero-divergence pass as the migration's end date.

## Procedure

1. List the straggler sources and their lifetimes.
2. Set the retention window and its closure conditions.
3. Name the truth store and the resolution rule.
4. Schedule the detection pass and its report.
5. Build the anomaly bucket and its review path.
6. Keep passing until zero twice, then close.

## Anti-patterns

- Reconciliation ended when divergence looked low, while a stale consumer still wrote.
- Conflicting pairs auto-resolved by newest-write, silently discarding truth.
- No truth store named during the overlap, so both stores claim authority.
- The final pass never run because the migration was "obviously done".
- Straggler lifetime guessed rather than measured from the logs.

## Done checklist

- [ ] Straggler sources and lifetimes recorded.
- [ ] Retention window and closure set.
- [ ] Truth store and rule recorded.
- [ ] Scheduled passes run to zero twice.
- [ ] Anomaly bucket built with review path.
- [ ] Final zero recorded with a date.

## Sources

- Comparison and merge mechanics: <https://www.postgresql.org/docs/>
- Data migration patterns: <https://martinfowler.com/>
- Data engineering references: <https://www.distributed-systems.net/>

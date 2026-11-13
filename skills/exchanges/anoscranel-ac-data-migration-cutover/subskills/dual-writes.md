---
name: dual-writes
domain: software-engineering/dual-writes
trigger: "Writing two stores at once and keeping them agreeing."
anti_trigger: "Not for event delivery between services, and not for cache invalidation."
scope: "Writing both stores at once, and how they silently diverge."
status: seedling
---

# Dual writes

## Standard

A dual write sends every mutation to both the old and the new store, and its correctness depends on a property the two stores do not have: atomicity across both. A write that succeeds in one and fails in the other leaves them disagreeing, and unless something detects it the disagreement is permanent — the new store hosts the switch, the switch happens, and the divergence becomes the system of record.

The mitigations are known and must be chosen explicitly. Write to a transactional log or queue first, with both stores consuming from it, so a consumer failure is a retryable lag rather than a lost write. Version or timestamp rows so a late backfill or a delayed consumer cannot overwrite fresher data with stale. Reconcile continuously during the whole window, so divergence is measured daily rather than discovered at cutover. And define which store is truth when they disagree, because "the new one, because we are migrating to it" is not an answer the old store's readers agreed to.

Primary sources: <https://martinfowler.com/> and <https://www.postgresql.org/>.

## Decision rules

- Record the write path: dual synchronous, log-first with consumers, or outbox-fed.
- Record the atomicity expectation honestly: none, unless a shared log provides it.
- Record the truth store during the transition and how disagreements resolve.
- Version or timestamp rows so stale overwrites are detectable and refused.
- Reconcile periodically during the entire window and record the divergence count per pass.
- Record the failure path when one store accepts and the other rejects.

## Procedure

1. Choose the write path and its atomicity story.
2. Name the truth store and the disagreement rule.
3. Add version or timestamp columns to both stores.
4. Build the reconciliation job and its divergence report.
5. Define the partial-failure path and its alert.
6. Run the dual-write window with daily divergence counts until the gate passes.

## Anti-patterns

- Two synchronous writes with no reconciliation, hoping nothing fails halfway.
- The backfill overwriting a newer dual-written row with an older copied value.
- No truth store named, so disagreements are resolved by whoever notices them.
- Reconciliation at cutover only, after weeks of accumulated divergence.
- A partial-failure path that logs and continues, losing one side permanently.

## Done checklist

- [ ] Write path and atomicity recorded.
- [ ] Truth store and disagreement rule named.
- [ ] Version or timestamp columns added.
- [ ] Reconciliation built with divergence counts.
- [ ] Partial-failure path defined with alert.
- [ ] Daily divergence measured through the window.

## Sources

- Data migration patterns: <https://martinfowler.com/>
- Transactional replication: <https://www.postgresql.org/docs/>
- Distributed data references: <https://www.distributed-systems.net/>

---
name: backfills
domain: software-engineering/backfills
trigger: "Rerunning history — a new column, a fixed bug, a late source."
anti_trigger: "Not for today's failed run, and not for stream replay alone."
scope: "Rerunning history safely: window declaration, catch-up control, resource shaping."
status: seedling
---

# Backfills

## Standard

A backfill reruns a pipeline over a historical window: a bug was fixed and the outputs must be regenerated; a new column must be computed for the past; a source published files years late. The safe backfill is declared as a window — from date A to date B, for these datasets, under these upgraded transformations — while the pipeline's normal schedule is paused or fenced so daily runs and the backfill never write the same partitions concurrently.

The wrong backfill is the quiet one: a catch-up flag left on, or a paused schedule silently resuming, pouring historical runs onto production resources while consumers read the partitions it is overwriting. Every real backfill has a stated window, a priority ordering (usually newest-first, so recent partitions recover their freshness first), a resource envelope so it does not starve serving, and an end state that is verifiable: which partitions, of which datasets, at which transformation version.

Primary sources: <https://airflow.apache.org/docs/> and <https://docs.getdbt.com/>.

## Decision rules

- Declare the backfill window explicitly: datasets, dates, transformation version.
- Fence the affected partitions from the daily schedule until the backfill completes.
- Choose a partition ordering that serves the consumer: usually newest-first.
- Shape resources separately from daily runs; a backfill is not the daily schedule with more anger.
- Record the idempotency contract each backfill relies on — it must hold at historical volumes.
- Verify completion as a checkable end state: all backfilled partitions at the new version, freshness recovered.

## Procedure

1. State the reason, datasets, and window of the backfill.
2. Freeze or re-route the daily schedule for the affected partitions.
3. Set the transformation version for the backfill runs.
4. Run in declared order with a resource envelope.
5. Verify the end state per partition: version, completeness, spot checks.
6. Record the window, the outcome, and any data corrections the backfill forced.

## Anti-patterns

- Catch-up left enabled as a standing "backfill" mechanism.
- Backfill and daily runs writing the same partition concurrently.
- Oldest-first ordering that leaves the most-consumed recent partitions stale the longest.
- A backfill whose completion is a feeling rather than a per-partition check.
- Massive historical reruns to add a column nobody asked to backfill — compute the cost first.

## Done checklist

- [ ] Window, datasets, and version declared.
- [ ] Daily schedule fenced for the window.
- [ ] Ordering chosen for the consumer.
- [ ] Resource envelope set.
- [ ] Per-partition completion verified.
- [ ] Backfill recorded with outcome.

## Sources

- Airflow catchup and backfill behaviour: <https://airflow.apache.org/docs/>
- dbt full-refresh and on-schema-change semantics: <https://docs.getdbt.com/>
- AWS Glue job orchestration: <https://docs.aws.amazon.com/glue/latest/dg/welcome.html>

---
name: pipeline-record
domain: software-engineering/pipeline-record
trigger: "Writing the record of a pipeline before it breaks at 3am."
anti_trigger: "Not for the data contract, and not for the run history alone."
scope: "The written record: DAG, keys, SLAs, failure paths, backfill history."
status: seedling
---

# Pipeline record

## Standard

The pipeline record is the document that answers, in advance, the questions an incident asks: which dependency should have run first, against what key is a rerun safe, what freshness promise did we make and to whom, what does a failed assertion do (fail, quarantine, alert), and where is the last known-good partition to fall back to. Like every record in this pack it is append-only, and the incident that revealed a missing line adds the line.

Because pipelines fail in their semantics rather than in their code more often than anyone admits, the record is semantic: the DAG as declared (not as drawn in someone's head), the idempotency key per task, the partition layout with reasons, the late-data policy and its keys, the backfill history with windows and outcomes, and the freshness targets with their breach paths. A run falls back to the record; a record that matches the drawings in one person's memory is not a record.

Primary sources: <https://openlineage.io/docs/> and <https://osf.io/prereg/>.

## Decision rules

- Record the declared DAG, sensors, and timeouts as submitted to the platform.
- Record the idempotency key and write pattern per task, and the partition layout with reasons.
- Record the late-data policy: accept/hold/wait, cutoff, merge key, revision columns.
- Record the freshness targets and breach paths, and which consumers rely on each.
- Record every backfill: window, datasets, version, ordering, outcome, corrections forced.
- Post-incident, the record gains what the incident taught: the failure path taken, the partition restored, the gap closed.

## Procedure

1. Assemble the sections from the leaves as the pipeline is designed, not after it runs.
2. Add the backfill history as each backfill completes.
3. Add the incident lines with dates within the incident's week.
4. Tie the record to the operational metadata: a reader can get from any section to the runs.
5. Re-read the record at every pipeline design change; outdated sections are corrected by amendment.
6. Name the person who owns the record and its amendment process.

## Anti-patterns

- A record written after the first outage from memory.
- Run history standing in for a stated design.
- Backfills with no recorded window or outcome.
- Amending silently after an incident instead of appending.
- No owner: the record drifts from the platform and nobody knows which is wrong.

## Done checklist

- [ ] DAG, keys, layout, policy, and targets recorded.
- [ ] Backfill history complete.
- [ ] Incident lines appended with dates.
- [ ] Record cross-linked to operational metadata.
- [ ] Re-read at every design change.
- [ ] Owner and amendment process named.

## Sources

- OpenLineage dataset and run metadata: <https://openlineage.io/docs/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Airflow pipeline-as-code: <https://airflow.apache.org/docs/>

---
name: lineage-and-observability
domain: software-engineering/lineage-and-observability
trigger: "Answering: what does this failure touch, and who reads what I write?"
anti_trigger: "Not for service telemetry, and not for the contract schema itself."
scope: "Column-level lineage, run metadata, and finding what a failure touched."
status: seedling
---

# Lineage and observability

## Standard

When a number looks wrong downstream, the question is what produced it: which upstream partitions, which transformation version, which task runs. Run-level lineage (this task, this run, these input partitions, this code version) answers the operational half. Column-level lineage (this output column derives from these input columns through this expression) answers the analytical half: the wrong number traces to the expressions that produced it, and the fix traces to every other consumer column that expression feeds.

The observability that matters is failure-shaped. A pipeline's telemetry must answer: which partitions did this run write, which did it read, how long did each task take, what did it quarantined, what assertions fired. Dashboards with average task durations answer none of those; the incident questions are per-partition and per-run, and the run metadata must be queryable at that granularity.

Primary sources: <https://openlineage.io/docs/> and <https://airflow.apache.org/docs/>.

## Decision rules

- Emit run metadata per task run: inputs, outputs, code version, start/end, status, quarantine counts.
- Maintain column-level lineage for every consumer-facing output column.
- Make lineage queryable in both directions: from output column to sources, from source partition to dependents.
- Record assertion results in the run metadata, not in a separate log only.
- Test the lineage paths deliberately: a wrong lineage map is worse than none.
- Publish the lineage of any consumer-facing dataset so its consumers can trace their inputs.

## Procedure

1. Instrument each task with OpenLineage-style run events (inputs, outputs, version, counts).
2. Build or adopt column-level lineage for the transformation layer.
3. Verify lineage on a known column change: the map should point to exactly the touched expressions.
4. Route assertion results into the run metadata.
5. On the next incident, answer "what did this failure touch" from the metadata alone, and note gaps.
6. Publish lineage for consumer-facing datasets.

## Anti-patterns

- Lineage at table level only, when the question is about one column.
- Run metadata that cannot answer per-partition questions.
- A lineage map that was never verified against a real change.
- Assertion results stored where nobody queries during an incident.
- Dashboards of averages standing in for per-run records.

## Done checklist

- [ ] Run metadata per task run with inputs, outputs, version, counts.
- [ ] Column-level lineage on consumer-facing outputs.
- [ ] Bidirectional lineage queries.
- [ ] Assertions in the run metadata.
- [ ] Lineage verified against a real change.
- [ ] Incident question answered from metadata.

## Sources

- OpenLineage specification: <https://openlineage.io/docs/>
- Airflow run metadata: <https://airflow.apache.org/docs/>
- Great Expectations results as data: <https://docs.greatexpectations.io/>

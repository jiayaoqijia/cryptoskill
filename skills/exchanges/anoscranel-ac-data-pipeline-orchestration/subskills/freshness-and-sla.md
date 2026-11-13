---
name: freshness-and-sla
domain: software-engineering/freshness-and-sla
trigger: "Setting and monitoring how current a dataset is."
anti_trigger: "Not for the data contract itself, and not for stream lag alone."
scope: "Freshness measured against a reference, monitored, and honestly reported."
status: seedling
---

# Freshness and SLA

## Standard

Freshness is a comparison, not a timestamp: the age of the newest complete record in a dataset, measured against a reference that means something to the consumer. "Updated at 03:00" is not freshness. "Currency rates present for the 02:45 fixing cycle, which the risk report runs against" is freshness — it states what a downstream job needs to be true and lets the measurement prove it true or false.

The error class this kills is the silently stale dataset: a source stopped publishing, an upstream task is yellow in the scheduler but nobody looks, and every downstream consumer runs to completion against six-day-old data because the pipeline never asserts what "current" means. Monitoring against a declared reference makes staleness loud at the point where it would otherwise be silent for weeks.

Primary sources: <https://openlineage.io/docs/> and <https://airflow.apache.org/docs/>.

## Decision rules

- Define freshness as (newest complete partition, reference event) with the reference's meaning stated.
- Publish a target per dataset and an alert on breach; state the breach path (who is told, what they do).
- Alert against the platform consumer: a pipeline that is last-partition-complete and still beyond target needs a different alert than an incomplete one.
- Handle day-boundary periods explicitly: a daily partition is not a daily count of events.
- When freshness must be violated, mark and publish the violation rather than extending the target quietly.
- Review the targets when source lateness profiles change (late-data monitoring feeds this leaf).

## Procedure

1. Identify each dataset's consumers and the event reference each needs.
2. State the target as a measurable comparator on the newest complete partition.
3. Wire the check into the platform so it runs at the consumer's time of use, not just at pipeline end.
4. Set the breach path: notify, page, or block the consumer; make the choice explicit.
5. Mark any known violation in the dataset metadata for consumers to see.
6. Review targets against the published lateness profile at every source change.

## Anti-patterns

- Freshness defined by "updated within 24 hours" with no reference to the events inside.
- Alerting only when the pipeline fails: silent staleness is the target of this leaf.
- Quietly widening a target to keep the alert quiet.
- Measuring the newest raw record but claiming freshness for the complete partition.
- One freshness definition for all datasets regardless of consumer needs.

## Done checklist

- [ ] Targets stated as comparators against a reference.
- [ ] Checks run at the consumer's time of use.
- [ ] Breach path explicit per dataset.
- [ ] Violations marked in metadata.
- [ ] Targets reviewed on source-profile changes.
- [ ] Staleness loud at the consumer.

## Sources

- OpenLineage run and dataset metadata: <https://openlineage.io/docs/>
- Airflow monitoring and alerting: <https://airflow.apache.org/docs/>
- Great Expectations data quality checks: <https://docs.greatexpectations.io/>

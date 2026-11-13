---
name: schema-and-indexing
domain: software-engineering/schema-and-indexing
trigger: "Designing the label index and controlling cardinality."
anti_trigger: "Not for application schema in general, and not for relational indexing."
scope: "The label index, matching, and cardinality as the design constraint."
status: seedling
---

# Schema and indexing

## Standard

A metric schema is the set of metric names and labels in production, and the index is the inverted table that lets a query find matching series efficiently: given the label matchers, which series exist. That index's size is the cardinality, and every query traverses the matchers against the indexed series. The classic failure is a single series explosion that makes the index the query bottleneck, because label matching is proportional to the series matching even when the time range is small.

Controlling cardinality is an engineering discipline, not a rule of total abstinence. Techniques exist: bound the labels, aggregate high-cardinality detail into pre-reduced series at write time, split per-object detail into an event or log stream and keep the metric as a rollup, or use exemplars that carry the rare detail as attached traces. The design question is which detail belongs in the burned path label-space, and which belongs somewhere else entirely.

Primary sources: <https://prometheus.io/docs/prometheus/latest/storage/> and <https://prometheus.io/docs/prometheus/latest/querying/examples/>.

## Decision rules

- Keep the high-frequency query dimensions as labels; push the rest to logs, traces, or exemplars.
- Bound every label to a declared distinct-value set; treat an unbounded label as a defect to remove.
- Aggregate at write time when detail per object is not a question operators ask in a graph but is a number in a log.
- Set an active-series ceiling for the deployment, and alert on the trend that approaches it.
- Prefer thresholds-and-alert queries being evaluated against a stable index than a rich index whose counts thrash as objects churn.
- Review label changes as application code review, because the metric schema is defined in application code.

## Procedure

1. List the dimensions that operators slice by, and confirm each against a real question.
2. For each high-cardinality candidate dimension, decide metric-label, pre-aggregated rollup, or non-metric channel, and record why.
3. Set the active-series ceiling and a trend alert against it.
4. Add an exemplar or trace link when operators need per-occurrence detail without per-occurrence series.
5. Put label-set changes in the deployment checklist so a feature release cannot silently multiply series.
6. Record the schema — metric names, labels, per-label distinct estimates — with the review dates.

## Anti-patterns

- Per-request success labels — user, path variable, session — consulted by nobody, paid for by everybody.
- A metric whose labels track an ephemeral pod identity, so series counts churn with every deploy.
- Discovering a series explosion from a memory alert three weeks after the feature that caused it.
- Assuming the label-problem will show up in review when no reviewer ever sees the deploy size.
- Micro-aggregating everything at write time, then losing the anomaly signal that raw series carried.

## Done checklist

- [ ] Query dimensions confirmed against real questions.
- [ ] Every label bounded and justified.
- [ ] Active-series ceiling set with a trend alert.
- [ ] Per-occurrence detail channeled to logs, traces, or exemplars.
- [ ] Label changes in the deployment checklist.
- [ ] Schema recorded with estimates and dates.

## Sources

- Storage and index overview: <https://prometheus.io/docs/prometheus/latest/storage/>
- Label matching in queries: <https://prometheus.io/docs/prometheus/latest/querying/examples/>
- Time-series database overview: <https://en.wikipedia.org/wiki/Time_series_database>

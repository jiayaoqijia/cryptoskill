---
name: tsdb-record
domain: software-engineering/tsdb-record
trigger: "Writing the record of a metrics deployment's schema and capacity state."
anti_trigger: "Not for SLO target-setting semantics, and not for alert-rule management."
scope: "The written record: series inventory, capacity, and policy state."
status: seedling
---

# TSDB record

## Standard

The time-series record captures the state a future responder needs when the metrics system itself is the incident: the schema in force — metric names, label sets, and their cardinality estimates — the capacity numbers — active-series count, head memory, ingest rate, compression ratio — and the policy state — retention windows, rollup semantics, and deletion. Each is stated with its measured date, because all of them drift with the application that defines the schema.

Its second job is reconciliation. Every metric schema drift begins as an application change, so the record ties series-count reviews to deployment cadence, and the recorded ceiling — the active-series budget — is what turns an accidental explosion into a caught one. When a query becomes slow or ingest stalls, the record answers the question that the dashboard itself cannot: what did the healthy state look like, and when.

Primary sources: <https://prometheus.io/docs/prometheus/latest/storage/> and <https://prometheus.io/docs/introduction/overview/>.

## Decision rules

- Record the schema: metric names, label sets, distinct-value estimates per label, with the review dates.
- Record the capacity numbers on a cadence: active series, head memory, ingest rate, compression ratio, compaction times — each with its date.
- Record the active-series ceiling as policy, with a trend alert against it.
- Record retention windows and rollup semantics as policies with rationale, not as inherited defaults.
- Record every schema drift as a dated entry tied to the change that caused it.
- Reconcile the series count against the ceiling after every deploy that touches instrumented code.

## Procedure

1. Assemble the schema inventory with estimates and the application areas that define each metric.
2. Record baseline capacity numbers from steady-state measurement, with dates.
3. Set the active-series ceiling and wire the trend alert to it.
4. Write retention and rollup policies with their rationale.
5. Add a dated entry for every schema change, including the reverted ones.
6. On any metrics incident, first read the record: the last healthy reconciliation narrows the search before any other check.

## Anti-patterns

- A dashboard answering from a system whose schema state exists only in the code that emitted it.
- Capacity numbers recorded once at launch, then cited years later without a re-measurement date.
- A ceiling nobody remembers setting, so the trend alert reads as noise.
- Schema changes that never enter the record until an incident demands history.
- A record consulted only in incidents, so steady-state baselines are exactly what is missing.

## Done checklist

- [ ] Schema inventory with estimates and review dates.
- [ ] Capacity numbers with measurement dates.
- [ ] Active-series ceiling as policy with a trend alert.
- [ ] Retention and rollup policies with rationale.
- [ ] Dated schema-drift entries.
- [ ] Post-deploy series reconciliation scheduled.

## Sources

- Storage lifecycle: <https://prometheus.io/docs/prometheus/latest/storage/>
- Overview: <https://prometheus.io/docs/introduction/overview/>
- Time-series database systems overview: <https://en.wikipedia.org/wiki/Time_series_database>

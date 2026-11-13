---
name: aggregates-and-summaries
domain: software-engineering/aggregates-and-summaries
trigger: "Pre-computing rolls and accepting their refresh and drift cost."
anti_trigger: "Not for engine-level materialized views of a specific store, and not for cache TTLs."
scope: "Pre-computed rolls, their refresh windows, and their drift risk."
status: seedling
---

# Aggregates and summaries

## Standard

An aggregate table stores the answer to a common aggregation: revenue by day and region, users by week. It trades write-time and storage for read-time, on the bet that the question is asked many more times than the data changes. The two costs that decide whether the bet wins are the refresh window — the interval during which the aggregate is behind its source — and the fan-out maintainability problem of aggregate definitions that drift apart from each other.

The failure mode is drift between aggregates built from the same base. Two teams each build a daily-active-user roll, one over events from the raw table and one over the deduplicated stream, and the enterprise has two official numbers. A defined derivation for the aggregate — its input fact, its grain, its filters, its owner — is what lets two implementations be recognised as the same number or as deliberately different ones.

Primary sources: <https://www.kimballgroup.com/> and <https://martinfowler.com/>.

## Decision rules

- Record the aggregate's grain sentence and the base fact it derives from.
- Record the refresh mechanism and the window during which the aggregate lags.
- Record the downgrade behaviour when the refresh fails: serve stale, or serve nothing.
- Record the queries that are permitted to use it and the ones that must not.
- Derive new aggregates from the same conformed base, not from each other.
- Record the point at which the aggregate should be dropped: its read-to-refresh cost ratio.

## Procedure

1. Confirm the question's repetition rate justifies any pre-computation.
2. Write the derivation: input, grain, filters, and deviating rules.
3. Choose the refresh mechanism and schedule.
4. Define the stale-failure behaviour.
5. Register the aggregate with its owner and its intended consumers.
6. Re-measure after the first month: reads served versus refresh cost.

## Anti-patterns

- Aggregates built from other aggregates, compounding their drift.
- Two rolls of the same metric with different filters, both labelled "daily revenue".
- Serving stale automatically, with no staleness indicator to the reader.
- Pre-computing for a report run once a year.
- No owner, so the definition nobody can change is also nobody's to fix.

## Done checklist

- [ ] Grain sentence and base fact recorded.
- [ ] Refresh window recorded.
- [ ] Stale-failure behaviour defined.
- [ ] Permitted queries listed.
- [ ] Derivation chain single-source.
- [ ] Cost review scheduled.

## Sources

- Aggregate design techniques: <https://www.kimballgroup.com/>
- Reporting and aggregation patterns: <https://martinfowler.com/>
- Data warehousing references: <https://clickhouse.com/docs/>

---
name: alert-on-pipeline-freshness-slo
description: Use when a table can go stale or empty without any job reporting failure. Monitors freshness, volume, and schema so a silent stall is caught before a consumer notices.
---

# Alert on Pipeline Freshness SLO

A pipeline can succeed while producing nothing: the source is empty, the filter matched zero rows, the job ran but loaded a stale partition. Monitor the data, not just the exit code.

## Procedure

1. Define freshness: the maximum allowed age of the newest row, for example `now() - max(event_ts) < 1h`. This is the SLO.
2. Monitor volume: the row count per partition within an expected band (plus or minus k sigma of the trailing baseline, or a floor like >0 and >10% of yesterday).
3. Monitor the max event time actually present, not just the job's finish time. A job finishing at 06:00 that wrote yesterday's partition is stale.
4. Test with the tool you already run:
   - dbt: `dbt source freshness` with `warn_after` / `error_after`.
   - Airflow: a `SQLCheckOperator` or a freshness sensor.
   - Standalone: `soda` / `monte_carlo`, or a query in the scheduler.
5. Alert on the data, naming the table, partition, and measured lag, and route to the owning team.
6. Distinguish empty-from-source (upstream), empty-from-filter (logic bug), and not-yet-run (scheduler): they page different people.
7. Alert on the absence of a partition too, which is different from a stale one and often means the scheduler dropped the run.
8. Two-sided: alert on too-old (stale) and on anomalous-too-new (a clock bug, future timestamps).
9. Baseline the volume on a rolling window that accounts for weekly seasonality, so Mondays do not page every weekend.
10. Make the check tolerant of the pipeline's own commit delay so it fires on real stalls, not normal jitter.

## Pitfalls

- Monitoring job exit status catches crashes but not a job that ran and wrote zero rows.
- Freshness measured on `loaded_at` (processing time) hides a stale source; measure the event time.
- A volume alert with a fixed threshold fires on every legitimate seasonal drop.
- Alerts with no owner page everyone and get muted.
- Testing freshness on a table scoped to today misses a partition that never arrived.
- Alert thresholds tighter than the pipeline's normal jitter cause constant noise.
- A check that only runs on the scheduler's success path never runs when the scheduler itself is down.
- Alerting on row count without a floor lets a partial load of one row pass as healthy.

## Verification

```sh
dbt source freshness --select source:orders   # expect a warning/error when the loader is stopped
psql -c "SELECT now()-max(event_ts) AS lag FROM events"
```

Lag is under the SLO in steady state; when the loader is stopped, the check fires within the expected window. Report the SLO, measured lag, and the last alert.
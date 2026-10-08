---
name: handle-late-arriving-data
description: Use when events arrive after their event-time window has closed. Sets an allowed-lateness policy and republishes corrected windows instead of dropping or misfiling records.
---

# Handle Late-Arriving Data

Event time and processing time differ: a mobile event stamped 09:58 may reach the pipeline at 10:07. Decide how late is acceptable, and make the pipeline emit corrections rather than silently dropping or misfiling.

## Procedure

1. Partition output by event time (`DATE(event_ts)`), never by ingestion time, so a late row lands in the partition it belongs to.
2. Set an explicit allowed lateness and record it in config, not a comment. Typical: 2 hours clickstream, 24 hours mobile, 7 days for batch reconciliation.
3. Streaming: attach a watermark with bounded out-of-orderness and a side output for records past the horizon.
   - Flink: `WatermarkStrategy.forBoundedOutOfOrderness(Duration.ofMinutes(30)).withAllowedLateness(Duration.ofHours(2))`.
   - Spark Structured Streaming: `withWatermark("event_ts", "2 hours")` before the aggregation.
4. Batch: reprocess the trailing lateness horizon each run, not just yesterday. A 7-day horizon re-merges the last week every night.
5. Route records later than the horizon to a late-data table or side output; alert on its growth.
6. When a late record lands in a closed window, republish the corrected aggregate for that window so downstream sees the fix.
7. Make consumers read current state for a window, not an append-only running sum, so a correction replaces rather than double-counts.
8. Measure the lateness distribution first (`percentile(event_ts - ingest_ts, 0.99)`) and set the horizon from the p99, not a guess.
9. For batch reconciliation, schedule a weekly wider-horizon pass to pick up the extreme tail beyond the daily horizon.
10. Tag corrected rows with an `updated_at` and a revision count so downstream can tell a correction from the first load.

## Pitfalls

- A watermark allowed-lateness of zero drops every out-of-order record silently.
- Partitioning by ingestion date shelves a late row in the wrong day; queries for the true day never see it.
- Dropping late records as acceptable loses the tail of every burst.
- Emitting a corrected aggregate as an addition double-counts; downstream must replace, not add.
- Setting the horizon at exactly the max observed lateness means the next outlier falls off the edge.
- Republishing corrections without a version or `updated_at` makes the current value unidentifiable.
- Computing p99 on a quiet week sets the horizon too tight for a burst week.
- A late-data side table nobody reads becomes a silent graveyard for the records you most needed.

## Verification

```sh
psql -c "SELECT event_date, count(*) FROM late_events GROUP BY 1 ORDER BY 1 DESC LIMIT 7"
psql -c "SELECT sum(v) FROM events WHERE event_date='2026-09-30'"
```

The late table's daily volume is under threshold, and the window aggregate matches a from-scratch recompute. Report the lateness horizon, the late-record rate, and any windows corrected this run.
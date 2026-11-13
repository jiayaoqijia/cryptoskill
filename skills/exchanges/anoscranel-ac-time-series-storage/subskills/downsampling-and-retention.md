---
name: downsampling-and-retention
domain: software-engineering/downsampling-and-retention
trigger: "Deciding rollups, retention windows, and value-selection semantics."
anti_trigger: "Not for backup policy, and not for log retention compliance."
scope: "Rollups, value-selection semantics, and retention as a policy."
status: seedling
---

# Downsampling and retention

## Standard

Retention is a policy per timeframe with a stated rationale: how long raw samples stay queryable, what is rolled up, and when data is deleted. Downsampling creates a second stream — the rollup — by re-aggregating each window into fewer points, and the semantics matter more than the cadence: a rolled-up gauge needs max, min, and average to retain meaning, and a rolled-up counter is a pre-computed rate over the window, which summarises behaviour differently than the raw series did.

The reason to downsample is cost distinction between the fresh and the old. Recent samples are asked precise questions — a spike, a deploy, a regression — so they are kept raw. Old samples are asked coarse questions — a trend, a capacity plan, a comparison — so they can be kept coarse. The honest design says which queries each tier serves and where the boundary sits in time, because the boundary is a decision about what evidence the operator has later, and pretending everything is kept raw is usually a billing surprise.

Primary sources: <https://prometheus.io/docs/prometheus/latest/storage/> and <https://en.wikipedia.org/wiki/Time_series_database>.

## Decision rules

- State the retention horizon for raw and rolled-up data separately, each with the questions it serves.
- Declare rollup value-selection per metric type: gauges keep the distribution summary, counters become rates over the window.
- Record what is lost in rollup: burst shape, brief spikes, and per-instance identity are common casualties.
- Treat every retention window — including deletion — as a policy in the record, not an engine default inherited silently.
- Keep the raw window long enough to cover a routine investigation: if on-call queries span a week, raw data spans at least that.
- Deleting old blocks is not backup; if the data matters after retention, a separate archive with its own policy exists.

## Procedure

1. List what questions are asked of recent versus historical data, and where the transition sits.
2. Choose the raw-retention window to cover the routine investigation span, on stated grounds.
3. Define the rollup windows and the aggregation semantics per metric type, and document the loss each implies.
4. Compute the storage saved from measured compression, not from advertised ratios, and record it.
5. Implement or schedule deletion, and record it as policy with a rationale, including any archive tier.
6. Verify a query across the boundary: results above and below the rollup point must not silently differ in meaning.

## Anti-patterns

- Rolling up to average-only gauges and detecting no spikes ever again, because the average erased them.
- A retention number chosen from the storage bill rather than from the investigation cadence.
- Treating the engine's default retention as if a decision had been made.
- Assuming deletion covers the compliance question; retention policies and deletion policies are not the same instrument.
- A dashboard that straddles the raw/rollup boundary without its author knowing.

## Done checklist

- [ ] Raw and rollup horizons stated with served-question rationale.
- [ ] Rollup semantics per metric type documented.
- [ ] Rollup losses named.
- [ ] Storage savings measured, not assumed.
- [ ] Retention and deletion written as policy with an archive tier if needed.
- [ ] Boundary-semantic query verified.

## Sources

- Storage tiers and retention mechanics: <https://prometheus.io/docs/prometheus/latest/storage/>
- Time-series storage systems context: <https://en.wikipedia.org/wiki/Time_series_database>
- Overview of long-term-patterns context: <https://prometheus.io/docs/introduction/overview/>

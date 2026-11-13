---
name: query-path
domain: software-engineering/query-path
trigger: "Constructing range queries honestly against the sampled data."
anti_trigger: "Not for alert-rule semantics, and not for dashboard product choice."
scope: "Range selectors, aggregation, and the scrape-interval floor."
status: seedling
---

# Query path

## Standard

A time-series query selects series by label, then reads a range of samples for each, and the engine returns the series the labels match over the time the range covers. The aggregation layer then combines: sum or average across label groups, rate over counters, quantiles from histograms. Each operation has a semantic floor that the underlying sampling sets: a rate computed from samples a minute apart can resolve minute-scale changes and nothing faster, and an average across five series is a claim about those five, not about the service unless they are all its instances.

The honest construction states the claim. Queries interpolate — they connect points, and graph renderers make data look more continuous than the sampling warrants — and the sample interval is the finest detail any conclusion can carry. Reading a single spike's shape at a resolution the samples never had, or averaging away the variance that was the finding, are construction errors the record should catch, because the graph looks equally convincing either way.

Primary sources: <https://prometheus.io/docs/prometheus/latest/querying/examples/> and <https://prometheus.io/docs/prometheus/latest/configuration/configuration/>.

## Decision rules

- State the scrape interval and treat it as the resolution floor of every conclusion drawn from the chart.
- Sum as aggregation across a label, group by what the claim is about — remembering that sum over a code path is a service claim only if all its instances are present.
- State the counter-rate window: a rate over one minute differs from a rate over five, and the claim of the wording should name the interval.
- Histograms: pre-bucketed, with bucket-boundary errors-as-claims; a quantile is an estimate from a bucket, never the exact measurement.
- Avoid range queries that span retention-tier boundaries without acknowledging that the source data changes character at the boundary.
- On rendered charts, remember that continuity is a rendering artefact of interpolation, not evidence about the sub-interval.

## Procedure

1. Write the claim as a question the data will answer, before writing the query.
2. Confirm the label matchers select the series the claim is about, no more and no fewer.
3. Confirm the range and consider dynamic points: the scrape-interval floor bounds any duration resolution.
4. Select the aggregation that preserves the claim; test with a known answer, such as an inject instrumented on purpose.
5. Name the interval in any rate or quantile wording, with the value recorded.
6. Record the query with its claim in the record when it becomes a dashboard or alert basis.

## Anti-patterns

- Minute-scale reasoning about a single loud event, from samples taken every minute.
- An alert threshold that presumes a resolution the interval does not sample.
- Summing across one label axis and forgetting the fan-out that double-counts.
- Reading a quantile estimate as an exact percentile because the renderer labelled it so.
- A pane that quietly crosses the rollup boundary with no annotation.

## Done checklist

- [ ] Claim written before query.
- [ ] Label selection equals the claim's subject.
- [ ] Interval and window widths named in wording.
- [ ] Aggregation verified with a known answer.
- [ ] Rate window stated with the number.
- [ ] Consistent-semantics check across any tier boundary.

## Sources

- Query examples and operators: <https://prometheus.io/docs/prometheus/latest/querying/examples/>
- Configuration and intervals: <https://prometheus.io/docs/prometheus/latest/configuration/configuration/>
- Overview: <https://prometheus.io/docs/introduction/overview/>

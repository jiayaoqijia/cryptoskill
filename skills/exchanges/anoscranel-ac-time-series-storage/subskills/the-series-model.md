---
name: the-series-model
domain: software-engineering/the-series-model
trigger: "Understanding what a time series is and what cardinality measures."
anti_trigger: "Not for query language syntax, and not for alerting semantics."
scope: "Series, samples, labels, and what cardinality means."
status: seedling
---

# The series model

## Standard

A time series is a named stream of samples: a metric name, a set of key-value labels, and a sequence of timestamp-value pairs. The name and labels together identify the series — `http_requests_total` with `method=GET, handler=/login` is one series; the same name with a different handler is another. Every distinct combination is a separate series that the system tracks, stores, and indexes independently.

That independence is the double edge. Labels give queries their power — slice by method, by handler, by instance — and every added label multiplies the series count by its distinct values. A label like `user_id` on a metric with ten thousand users turns one series into ten thousand, and the multiplication compounds across labels. Cardinality is the count of active series, and it, not sample volume, is the number that decides memory, index size, and query cost.

Primary sources: <https://prometheus.io/docs/introduction/overview/> and <https://prometheus.io/docs/prometheus/latest/querying/examples/>.

## Decision rules

- Decide labels by the questions the on-call will ask, not by the fields the object happens to have.
- Bound every label: a label whose distinct values grow without limit is a schema defect, not a feature.
- Never label with anything per-request or per-user on a service metric; aggregate those dimensions when they are needed at all.
- Prefer a small number of stable, low-cardinality labels; add one only with an estimate of the series multiply it causes.
- Count the expected cardinality of a new metric before deploy: distinct values per label, multiplied, times the instances.
- Check the active-series count after deploy against the estimate; reconcile any gap before it hardens.

## Procedure

1. Name the metric and the unit it counts, and state who will use it.
2. List the questions the labels must answer and derive the minimal label set from them.
3. Enumerate distinct values per label and multiply to estimate series count per instance.
4. Multiply by instance count and compare against the active-series budget.
5. If over budget, drop or bound labels, or pre-aggregate, and revisit questions the labels can no longer answer.
6. Record the metric, label set, and cardinality estimate in the storage record.

## Anti-patterns

- Per-object labels — user, session, request — that turn a counter into a fan-out.
- Labels added by reflex because the data existed in the application object.
- Cardinality estimated after the page, from the dashboard that will not load.
- A sparse many-None label set that mostly tracks combinations no one queries.
- Assuming sample count is the capacity driver and ignoring the index the series count grows.

## Done checklist

- [ ] Label set derived from stated questions.
- [ ] Every label bounded with a distinct-value estimate.
- [ ] Cardinality arithmetic done before deploy.
- [ ] Estimate against the active-series budget reconciled.
- [ ] Post-deploy series count checked against estimate.
- [ ] Metric and estimate recorded.

## Sources

- Data-model overview: <https://prometheus.io/docs/introduction/overview/>
- Query-by-label examples: <https://prometheus.io/docs/prometheus/latest/querying/examples/>
- Time-series database background (the Gorilla system among them): <https://en.wikipedia.org/wiki/Time_series_database>

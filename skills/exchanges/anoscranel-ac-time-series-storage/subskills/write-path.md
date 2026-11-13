---
name: write-path
domain: software-engineering/write-path
trigger: "Designing the ingest path and its timing assumptions."
anti_trigger: "Not for the query engine, and not for pipeline scheduling generally."
scope: "Ingest, scrape intervals, timestamp assignment, and out-of-order arrival."
status: seedling
---

# Write path

## Standard

Most metric systems pull on an interval: a scrape or poll walks the targets and appends the samples it finds. The interval is therefore a design decision with query consequences — a 60-second scrape cannot support a claim about a 30-second event, and an interval chosen for resource comfort quietly sets the resolution floor for every question asked later. Push-based ingest shifts who decides the timestamp, but not the constraint: the rate, the timestamp source, and a stated order policy must be decided either way.

Timestamps are trustworthy or the window arithmetic is not. When the scraper stamps arrival, long scrapes skew samples late; when the source stamps its own clock, clock skew between sources shifts alignment, and late samples arrive out of order. Engines define an acceptance window and a policy — accept-head, reject-late, or rewrite-stale — and the honest design states which it assumes rather than discovering it when a counter resets oddly after a network partition.

Primary sources: <https://prometheus.io/docs/introduction/overview/> and <https://en.wikipedia.org/wiki/Time_series_database>.

## Decision rules

- Choose the scrape or emit interval from the fastest event the queries must resolve, then reconsider for cost.
- State the timestamp authority — scraper or source — and the clock assumption that goes with it.
- State the out-of-order policy the engine enforces and the window it allows; late data outside the window is decided, not mysterious.
- Size the ingest for the projected active-series count times the rate, with the multiplication shown in the record.
- Distinguish a missed scrape from a zero: absence of samples and a sample of zero are different facts.
- On push-based ingest, require per-source backpressure or spill so one stuck emitter cannot block the rest.

## Procedure

1. Set the interval from the fastest query resolution, then verify the sample count the fleet produces.
2. Fix the timestamp authority and document the clock-skew assumption.
3. Read the engine's late-sample policy and record which window it enforces.
4. Load-test ingest at the projected active-series count, not at a single-series stand-in.
5. Verify gap handling in a query: an absent sample must not read as a zero value.
6. Record interval, timestamp authority, late policy, and capacity numbers with dates.

## Anti-patterns

- An interval chosen to make the storage bill small, followed by observability questions the samples cannot answer.
- Late samples silently dropped, discovered when a chart disagrees with a log.
- Reading absence as zero, and concluding a service's error rate fell when its reporting died.
- Load tests that replay few series fast, then production with many series slow.
- A push path with no backpressure, where one emitter wedges ingest for a fleet.

## Done checklist

- [ ] Interval derived from fastest event to resolve.
- [ ] Timestamp authority and skew assumption stated.
- [ ] Late-sample policy known and recorded.
- [ ] Ingest sized from active-series times rate.
- [ ] Absence-versus-zero verified in a query.
- [ ] Numbers and dates in the record.

## Sources

- Ingest and data-model overview: <https://prometheus.io/docs/introduction/overview/>
- Gorilla write-path design: <https://en.wikipedia.org/wiki/Time_series_database>
- Storage-engine overview: <https://prometheus.io/docs/prometheus/latest/storage/>

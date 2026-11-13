---
name: freshness-and-completeness
domain: software-engineering/freshness-and-completeness
trigger: "Committing to how current and how complete a dataset will be."
anti_trigger: "Not for pipeline scheduling, and not for latency optimisation."
scope: "Delivery time, coverage, and the guarantees a producer can keep."
status: seedling
---

# Freshness and completeness

## Standard

Freshness is a promise about time: by when a record of a given event will be available. Completeness is a promise about coverage: which population the dataset includes and what it excludes. Both are usually assumed rather than stated, and both fail silently, because a dataset that is late or partial looks exactly like a dataset that is current and whole.

The guarantee must be measurable by the producer. A commitment to "within an hour" requires the producer to measure the age of the newest record and to alert when the threshold is crossed; without that measurement the promise is an aspiration. Completeness is harder because the missing population is invisible in the data, so it usually requires a comparison against an independent count.

Primary sources: <https://csrc.nist.gov/> and <https://sre.google/>.

## Decision rules

- Record the freshness commitment and the percentile it applies to, since a median hides the tail.
- Record how the producer measures age and where the measurement is exposed.
- Record the completeness definition: which population, and what is excluded.
- Record the source of truth for the population count, since it cannot be derived from the dataset itself.
- Record the expected variance, such as weekend or month-end effects, so a normal cycle is not treated as a breach.
- Record the alert threshold and who receives it.

## Procedure

1. Record the freshness commitment and the percentile.
2. Record the age measurement and its source.
3. Define completeness and record the reference count.
4. Record expected variance by period.
5. Record alert thresholds and recipients.
6. Write the guarantees with their measurement.

## Anti-patterns

- A median freshness figure presented as the guarantee.
- Completeness defined as "all records", which is unmeasurable.
- A threshold that fires on every weekend.
- Measuring age at the wrong point, such as ingest rather than availability.
- A commitment with no alert, which is discovered by a consumer instead.

## Done checklist

- [ ] Freshness commitment and percentile recorded.
- [ ] Age measurement recorded.
- [ ] Completeness definition recorded.
- [ ] Reference count recorded.
- [ ] Expected variance recorded.
- [ ] Alert thresholds recorded.

The completeness reference deserves its own line because it usually comes from a different system than the dataset: an orders table compared against a payment processor's count, or a census against a population register. Recording where the reference comes from, and its own reliability, prevents a completeness check from inheriting an unexamined assumption.


## Sources

- Reliability measurement practice: <https://sre.google/>
- Data governance guidance: <https://csrc.nist.gov/>
- Service level context: <https://sre.google/workbook/table-of-contents/>

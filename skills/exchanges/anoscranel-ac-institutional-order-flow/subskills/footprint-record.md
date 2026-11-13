---
name: footprint-record
domain: investing/footprint-record
trigger: "Writing the record of a tape observation and what it supports."
anti_trigger: "Not for recommending a position, and not for attributing intent."
scope: "The written record: observation, method, confidence, and the alternative explanation."
status: seedling
---

# Footprint record

## Standard

The footprint record states what was observed in the tape, how it was measured, what it is consistent with, and what else could have produced it. The last field is the one that separates analysis from storytelling: a cluster of large prints is consistent with accumulation and also with a seller working into demand, and a record that names only the first explanation has chosen a narrative rather than read the data.

The record also carries the limits of the measurement. Trade direction relies on the venue's classification, which is an inference rather than a fact; block timestamps may be published with a delay; and the sampling of a book captures only what was displayed. Writing those limits beside the conclusion is what keeps a later reader from treating an inference as an observation.

Primary sources: <https://www.finra.org/> and <https://osf.io/prereg/>.

## Decision rules

- The record states the observation in one sentence, with the instrument, window, and data source.
- The measurement method is stated, including any classification the data provider performed.
- The confidence is labelled and tied to the method's limits.
- At least one alternative explanation is recorded.
- The record states what would confirm or refute the reading.
- Entries are dated; later observations are appended, not substituted.

## Procedure

1. Write the observation and the data source.
2. Record the method and any provider classifications used.
3. Label the confidence with its basis.
4. Record the alternative explanation.
5. Record the confirming or refuting observation to look for.
6. File and date the entry.

## Anti-patterns

- Stating a reading without the method.
- Naming one explanation and omitting the other.
- Treating the provider's trade classification as ground truth.
- Writing a conclusion that no observation could refute.
- Rewriting an entry after the price resolved it.

## Done checklist

- [ ] Observation and source recorded.
- [ ] Method stated.
- [ ] Confidence labelled with basis.
- [ ] Alternative recorded.
- [ ] Confirmer named.
- [ ] Entry dated.

The record's value compounds across entries in a way a single observation cannot: three entries describing the same pattern on successive days are a stronger statement than any one of them, and three entries describing the same pattern with the price moving against it are a reason to discard the reading. Keeping the series is what allows the distinction.


## Sources

- Trading and reporting guidance: <https://www.finra.org/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Market structure context: <https://www.sec.gov/investor>

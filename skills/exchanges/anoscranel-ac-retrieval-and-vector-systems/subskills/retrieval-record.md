---
name: retrieval-record
domain: software-engineering/retrieval-record
trigger: "Writing the record of a retrieval system and its measured quality."
anti_trigger: "Not for prompt records, and not for vendor evaluation."
scope: "The written record: chunking, model, index, freshness, and metrics."
status: seedling
---

# Retrieval record

## Standard

The retrieval record states the chunking parameters, the embedding model and its dimensions, the index type and operating parameters, the freshness contract, and the measured metrics with their golden set. Those six items are what make a retrieval system reproducible, and each of them changes the answer in ways that are invisible from the outside.

Its second function is to preserve the measurement. A retrieval system's quality is a number relative to a fixed set, and the set changes as queries change. Recording the metric, the set's size, and the date means a later comparison is between comparable things rather than between two impressions of quality remembered from different months.

Primary sources: <https://www.nist.gov/> and <https://osf.io/prereg/>.

## Decision rules

- The record states chunk size, overlap, and boundary rule.
- The embedding model, version, and dimensionality are recorded.
- The index type and operating parameters are recorded with measured recall.
- The freshness contract records the maximum lag and the deletion path.
- Metrics are recorded with the golden set's size and date.
- Review triggers are dated: model change, corpus growth, metric regression, freshness breach.

## Procedure

1. Record the chunking parameters.
2. Record the model and dimensions.
3. Record the index and its measured recall and latency.
4. Record the freshness contract.
5. Record the metrics and the golden set.
6. Set review triggers and amend at each.

## Anti-patterns

- Recording the model without its version.
- Omitting measured recall, which makes the index choice unevidenced.
- Recording metrics without the set they were measured on.
- Leaving the deletion path undocumented.
- No triggers, so the record describes a system that has since changed.

## Done checklist

- [ ] Chunking parameters recorded.
- [ ] Model and dimensions recorded.
- [ ] Index and recall recorded.
- [ ] Freshness contract recorded.
- [ ] Metrics and golden set recorded.
- [ ] Triggers dated.

The record should also state what the system does when retrieval returns nothing, since that path is rarely exercised in testing and is the one users meet most often: an empty result with no fallback reads as a broken product, and the behaviour should be a decision rather than an accident.


The record should also note the query distribution it was tuned against, since retrieval quality is relative to the questions asked: a system tuned for short keyword queries and then used with long conversational ones is being measured against the wrong set, and the mismatch is invisible in the metrics until someone reads the queries.

## Sources

- Retrieval evaluation methodology: <https://www.nist.gov/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Information retrieval foundations: <https://nlp.stanford.edu/IR-book/>

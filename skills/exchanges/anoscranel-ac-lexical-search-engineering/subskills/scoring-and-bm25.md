---
name: scoring-and-bm25
domain: software-engineering/scoring-and-bm25
trigger: "Understanding and tuning the score that orders results."
anti_trigger: "Not for analyzer choices, and not for learning-to-rank models."
scope: "Term frequency, inverse document frequency, field length, and the knobs."
status: seedling
---

# Scoring and BM25

## Standard

BM25 orders documents by a formula with three instincts: a term matters more the rarer it is across the corpus (inverse document frequency); a document matches harder when the term appears more often, but with diminishing returns (term frequency saturation); and a long field dilutes a match that a short field would make look strong (field-length normalization). The shocking majority of relevance surprises trace to one of those three, most often the third: a two-word title matches harder than a forty-paragraph body containing the same two words, and unless that consequence is wanted, the field-length norm needs adjusting.

The formula's knobs are saturations and norms, and tuning them is corpus-specific work with a safety rule: keep an untuned baseline, change one knob at a time, and record each change on a frozen query set. A tuned system whose tuning rationale is lost is indistinguishable from a broken one at the next debugging session. Guards belong outside scoring — filters express what must be true, boosts express what should rank higher — and putting mandatory conditions into boosts is the classic way to produce results that violate the requirements.
Primary sources: <https://nlp.stanford.edu/IR-book/> and <https://elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html>.

## Decision rules

- The three instincts are named in the system's documentation with the consequence each has for the corpus.
- Field-length norms are a recorded decision per field, because the title-beats-body effect is sometimes a bug wanted and sometimes unwanted.
- Boosts adjust ordering among qualifying results; mandatory conditions go in filters, never in boosts.
- Tuning happens on a frozen query set with an untuned baseline; one knob at a time.
- Every tuning change is recorded with its query set, the numbers, and the reason.
- Score computation changes on an engine upgrade are treated as a re-tuning event, not as a silent behaviour continuation.

## Procedure

1. Assemble the query set from real production queries, frozen and versioned.
2. Run the untuned baseline; record the result.
3. Change one knob; re-run; diff the ordering; record why the change helped.
4. Repeat per knob, never compounding unexamined changes.
5. Verify filters still exclude; boosts only reorder.
6. Store the final parameters, the baseline, and the query-set version in the search record.

## Anti-patterns

- Tuning three knobs at once and shipping whatever the aggregate looked like.
- Mandatory conditions expressed as boosts; the result ordering contains violations.
- Accepting the default norm with no idea that short fields win by construction.
- Boost hoping to fix an analyzer mismatch; the terms were never the same on both sides.
- An upgrade shifting scores with no baseline to compare against.

## Done checklist

- [ ] Frozen query set assembled and versioned.
- [ ] Untuned baseline recorded.
- [ ] One-knob-at-a-time change log with reasons.
- [ ] Filters verified after tuning.
- [ ] Parameters and reasoning in the search record.
- [ ] Upgrade treated as a re-tuning event.

## Sources

- Introduction to Information Retrieval: <https://nlp.stanford.edu/IR-book/>
- Elasticsearch query DSL: <https://elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html>
- Lucene project: <https://lucene.apache.org/core/corenews.html>

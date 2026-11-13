---
name: relevance-evaluation
domain: software-engineering/relevance-evaluation
trigger: "Measuring whether a retrieval change actually improved results."
anti_trigger: "Not for model benchmark selection, and not for prompt evaluation."
scope: "Golden sets, recall at k, and measuring a change honestly."
status: seedling
---

# Relevance evaluation

## Standard

A retrieval change is a hypothesis, and testing it requires a fixed set of queries with judged relevant documents. Without that set, every change is evaluated by inspecting a handful of results and concluding they look better, which is how an index accumulates improvements that do not improve anything.

The metric should match the question. Recall at k measures whether the relevant document appears in the top k, which is the right question when a downstream model consumes the results. Precision at k measures how much of the result set is relevant, which matters when a human reads the list. Mean reciprocal rank and normalised discounted cumulative gain weight position, which matters when ordering is the product. Recording which metric was chosen and why is part of the evaluation, not a formality.

Primary sources: <https://www.nist.gov/> and <https://nlp.stanford.edu/IR-book/>.

## Decision rules

- Record the golden set's size, how it was built, and who judged it.
- Record the metric used and the reason it matches the downstream use.
- Record recall at the candidate depth the reranker receives.
- Record the baseline results before any change.
- Record the test's statistical treatment, since a difference on fifty queries may be noise.
- Record the golden set's refresh policy, since a set that never changes stops detecting regressions.

## Procedure

1. Build a golden set of queries with judged relevant documents.
2. Record its size, provenance, and judging process.
3. Choose the metric that matches the downstream use.
4. Measure the baseline and record it.
5. Apply the change and measure again against the same set.
6. Record the difference and whether it is distinguishable from noise.

## Anti-patterns

- Judging a change by looking at a few results.
- Using precision when a downstream model needs recall.
- Comparing scores across two different golden sets.
- Reporting an improvement without the baseline.
- Never refreshing the set, so it stops representing real queries.

## Done checklist

- [ ] Golden set size and provenance recorded.
- [ ] Judging process recorded.
- [ ] Metric chosen with reason.
- [ ] Baseline measured.
- [ ] Change measured against the same set.
- [ ] Significance treatment recorded.

The set's coverage matters as much as its size: fifty queries drawn from one product area will detect regressions there and miss them everywhere else, so recording which areas the set covers, and which it does not, prevents a green result from being read as a general one.


## Sources

- Retrieval evaluation methodology: <https://www.nist.gov/>
- Information retrieval foundations: <https://nlp.stanford.edu/IR-book/>
- Pre-registration practice for stated tests: <https://osf.io/prereg/>

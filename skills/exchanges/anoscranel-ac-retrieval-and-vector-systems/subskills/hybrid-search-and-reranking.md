---
name: hybrid-search-and-reranking
domain: software-engineering/hybrid-search-and-reranking
trigger: "Combining keyword and vector search, and adding a reranking stage."
anti_trigger: "Not for index parameter tuning, and not for embedding model choice."
scope: "Sparse plus dense fusion, and the second stage that fixes ranking."
status: seedling
---

# Hybrid search and reranking

## Standard

Dense retrieval matches meaning and loses exact strings; sparse retrieval matches terms and misses paraphrase. Combining them covers both failure modes, and the combination is usually stronger than either alone because the two make uncorrelated mistakes. The fusion method matters less than the fact of having both, though reciprocal rank fusion is a common default because it needs no score calibration.

Reranking is a second stage that takes the combined candidate set and reorders it with a more expensive model. Its value depends on the first stage's recall: a reranker cannot recover a document the retrieval stage never returned, so the two are sequential rather than alternative, and the record should state the candidate depth the reranker receives.

Primary sources: <https://nlp.stanford.edu/IR-book/> and <https://www.nist.gov/>.

## Decision rules

- Record the retrieval methods combined and the fusion rule.
- Record the candidate depth passed to the reranker.
- Record the first stage's recall at that depth, since it bounds the final result.
- Record the reranker's latency and whether it fits the request budget.
- Record the evaluation showing the combination beats each method alone.
- Record the fallback when the reranker is unavailable.

## Procedure

1. Record the methods and the fusion rule.
2. Measure recall at the candidate depth.
3. Add the reranker and measure the final ranking improvement.
4. Record reranker latency within the request budget.
5. Record the fallback path.
6. Write the pipeline with its depth and recall stated.

## Anti-patterns

- Adding a reranker before measuring first-stage recall.
- Fusing scores from incomparable scales without normalisation.
- Assuming hybrid always wins without measuring it on the corpus.
- Setting a candidate depth so shallow that recall suffers.
- Reranking with a model whose latency exceeds the request budget.

## Done checklist

- [ ] Methods and fusion rule recorded.
- [ ] Candidate depth recorded.
- [ ] First-stage recall measured.
- [ ] Reranker improvement measured.
- [ ] Latency recorded.
- [ ] Fallback recorded.

The reranker's value also depends on what it was trained for: a model trained on general relevance may reorder technical content poorly, and its improvement on a generic benchmark is not evidence about this corpus. Measuring it against the golden set, rather than adopting it on reputation, is the only test that applies to the system being built.


## Sources

- Information retrieval foundations: <https://nlp.stanford.edu/IR-book/>
- Evaluation methodology: <https://www.nist.gov/>
- Open model documentation: <https://huggingface.co/docs/transformers/>

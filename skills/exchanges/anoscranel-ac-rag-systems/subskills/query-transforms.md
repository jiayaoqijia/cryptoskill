---
name: query-transforms
domain: prompt-engineering/query-transforms
trigger: "Turning the question as asked into the query the index should receive."
anti_trigger: "Not for index mechanics, and not for prompt writing."
scope: "Rewriting the question into what the index should be asked."
status: seedling
---

# Query transforms

## Standard

The question a user asks is optimized for a human conversational partner, and the query an index serves is optimized for term matching in a vector space or a lexical index. The two shapes differ: the question carries pronouns and references from earlier turns, assumed context, and the vocabulary of the user, while the index carries the vocabulary of the documents. A transform stage converts one into the other, and skipping it sends the index a query that cannot reach the passages that hold the answer.

The transforms worth having are few and each earns its latency. Reference resolution rewrites pronouns and elliptical questions into self-contained queries — necessary in any conversation beyond the first turn. Vocabulary alignment moves user terms toward corpus terms without discarding the originals. Expansion adds the phrasings the answer's sources plausibly use. Each transform is a published stage with a stated purpose; a transform that cannot say what failure it fixes is latency, not quality.

Primary sources: <https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview> and <https://python.langchain.com/docs/concepts/rag/>.

## Decision rules

- Resolve conversational references into a self-contained query before any retrieval.
- Record each transform stage with the failure it exists to fix.
- Test transforms on real question logs, not on invented examples.
- Measure end-to-end: a transform that improves retrieval metrics but not final answers is not an improvement.
- Keep the original question alongside every transform; some answers need the user's phrasing back.
- One transform passes its output to the next; a stack where stages cannot say their order is unauditable.

## Procedure

1. Sample real questions from production logs, including follow-ups.
2. Classify the failure modes: unresolved reference, vocabulary mismatch, missing phrasing.
3. Implement only the transforms that address a classified failure.
4. Measure retrieval quality and end-answer quality before and after, on the same set.
5. Keep the raw question in the record for answer phrasing and for later analysis.
6. Publish the stage order in the RAG record.

## Anti-patterns

- Deploying a transform because a framework ships one.
- Testing on invented questions that mirror the transform's assumption.
- Measuring retrieval metrics while answers stay flat.
- A transform stack whose order is undocumented.
- Discarding the original question once a transform has run.

## Done checklist

- [ ] References resolved for follow-up turns.
- [ ] Each transform tied to a classified failure.
- [ ] Real-log test set used.
- [ ] End-to-end change measured, not just retrieval metrics.
- [ ] Original question retained.
- [ ] Stage order published.

## Sources

- RAG architecture overview: <https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview>
- LangChain RAG concepts: <https://python.langchain.com/docs/concepts/rag/>
- The original RAG paper: <https://arxiv.org/abs/2005.11401>

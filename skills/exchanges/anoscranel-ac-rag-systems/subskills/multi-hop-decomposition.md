---
name: multi-hop-decomposition
domain: prompt-engineering/multi-hop-decomposition
trigger: "Splitting a question whose answer needs more than one retrieval round."
anti_trigger: "Not for single-query retrieval, and not for index mechanics."
scope: "Splitting questions whose answer needs more than one retrieval."
status: seedling
---

# Multi-hop decomposition

## Standard

Some questions cannot be answered by one retrieval because the answer needs the output of one retrieval to form the next query: which standards cite another standard, who reports to whom through an intermediate, what a term means in a document that must be found before it can be read. These are multi-hop questions — the second retrieval depends on what the first returned, so no single query, however well transformed, can reach the answer.

The engineering choice is between three shapes: decompose up front into a fixed list of sub-queries (works only when the hops are visible in the question itself); iterate retrieve-then-re-query until a condition is met (works when hops are discovered, but needs a stop rule); and retrieve broadly over the union of plausible sub-queries and let generation assemble (works when hops are shallow and recall is cheap). The choice is recorded per question type, with the failure that each shape handles.

Primary sources: <https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview> and <https://arxiv.org/abs/2005.11401>.

## Decision rules

- Classify questions by hop structure before choosing a decomposition shape.
- Iterative decomposition carries a stop condition stated in advance; open-ended loops drift.
- Each sub-query inherits the citation discipline — the final answer cites every passage it used, across all hops.
- Cap the hop count in a loop; some questions look multi-hop and are actually unanswerable in the corpus.
- Record which question types route to which shape, and measure very honestly: multi-hop costs multiply latency.
- Test with questions whose hops are known, so skip-counting is measurable.

## Procedure

1. Classify the incoming question: single-hop, fixed multi-hop, or discovered multi-hop.
2. Route to the matching shape; do not run iterative decomposition on single-hop questions.
3. For iterative shapes, state the stop condition and the hop cap before execution.
4. Collect passages from every hop in one evidence pool with hop numbers attached.
5. Generate the answer over the pool with citations across all hops.
6. Record the hop count and skip count per question for tuning.

## Anti-patterns

- Running every question through multi-hop machinery to catch the few that need it.
- An iterative loop with no stated stop condition.
- Citing only the last hop's passages.
- No hop cap: unanswerable questions become latency black holes.
- Measuring only final-answer accuracy; skip counts and latency are part of the honest result.

## Done checklist

- [ ] Questions classified by hop structure.
- [ ] Decomposition shape routed per class.
- [ ] Stop condition and hop cap stated for loops.
- [ ] Passage pool carries hop numbers.
- [ ] Citations span all hops.
- [ ] Hop and skip counts measured.

## Sources

- RAG architecture overview: <https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview>
- Original RAG formulation: <https://arxiv.org/abs/2005.11401>
- Retrieval concepts: <https://docs.llamaindex.ai/en/stable/understanding/rag/>

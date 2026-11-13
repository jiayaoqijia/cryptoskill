---
name: rag-prompts
domain: prompt-engineering/rag-prompts
trigger: "When a prompt must answer strictly from retrieved documents, cite them, and refuse cleanly when they are silent."
anti_trigger: "The model may use its own training knowledge freely."
scope: "Prompting grounded question-answering over retrieved documents: grounding clauses, citation demands, abstain behavior, and source-first ordering."
status: "seedling"
---

# RAG prompts: grounded answers

## Standard

The pattern has one goal: the answer must come from the retrieved context, and the
model must say so when it does not. Google's Gemini guide supplies the grounding clause
template: instruct the model to rely only on the provided user context, and to treat
anything not mentioned there as unavailable (<https://ai.google.dev/gemini-api/docs/prompting-strategies>). Give an explicit
license to abstain, because the highest-probability continuation of a question is an
invented answer. Put retrieved material in an explicit data envelope at
the tail of the context; never let its text redefine policy (<https://model-spec.openai.com/2026-08-18.html>).
Retrieved content is untrusted data, so the rules compose with injection defenses; this
leaf owns only the faithfulness contract.

Primary sources: <https://ai.google.dev/gemini-api/docs/prompting-strategies> and <https://www.braintrust.dev>.

## Decision rules

| Need | Prompt rule |
|---|---|
| Answers must come from the documents only | Grounding clause naming the context block as the only source |
| The right answer is often "not covered" | A named abstain output, for example "NOT IN DOCUMENTS" |
| Traceability | Require citation of the source ID for every claim |
| Long documents | Put the question and rules near the end; retrieval fills the middle |
| Fresh data | A current-date clause so the model does not reason from stale dates |

## Procedure

1. Define the context block format the retriever emits: IDs, titles, spans.
2. Write the grounding clause naming that block as the exclusive source.
3. Add the abstain token and show one example of it used correctly.
4. Demand citations by source ID, and check them in code after generation.
5. Test with documents that do not answer the question; the abstain path must fire.
6. Test with a document whose text tries to steer the model; the envelope must hold.

## Anti-patterns

- Asking for faithfulness without an abstain path; the model invents to comply.
- Burying the question above thousands of tokens of retrieval; restate it near the end.
- Citation requests without a check; models cite IDs that do not exist if unverified.
- Mixing the grounding clause with "also use your knowledge"; pick one contract.
- Trusting delimiter tags against hostile retrieved text; delimiters are formatting,
 not a security boundary (see the enforcement order in this skill's injection leaf).

## Done checklist

- [ ] The grounding clause names the exclusive source block.
- [ ] A named abstain output exists and is tested.
- [ ] Citations resolve to real source IDs under a code check.
- [ ] Steer-text-in-document tests pass without policy drift.

## Sources

- <https://ai.google.dev/gemini-api/docs/prompting-strategies>
- <https://www.braintrust.dev>

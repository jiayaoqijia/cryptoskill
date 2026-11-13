---
name: refusal-behaviour
domain: prompt-engineering/refusal-behaviour
trigger: "Answering honestly when the corpus does not contain the answer."
anti_trigger: "Not for prompt phrasing alone, and not for index mechanics."
scope: "Answering honestly when the corpus does not contain the answer."
status: seedling
---

# Refusal behaviour

## Standard

The corpus is finite and the questions are not; between the two lies a region where retrieval returns passages, none of which answer the question, and the model faces a choice it must be designed for: answer anyway from what it retrieved, answer from what its parameters remember, or say that the corpus does not appear to contain the answer. Without design, the default is the worst of the three — a fluent answer that cites passages which do not support it, because generation is rewarded for fluency and the gap is invisible to the user.

Refusal is a designed behaviour, not a temperament. The system's refusal gets a stated threshold: how little retrieved relevance is acceptable before answering gives way to saying the corpus is silent. The refusal text itself is designed — what the system did search, what it did and did not find, and what the user can do next — because a refusal that names the gap is diagnostic while a bare refusal is indistinguishable from failure.

Primary sources: <https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview> and <https://docs.anthropic.com/en/docs/build-with-claude/citations>.

## Decision rules

- State the relevance threshold beneath which answering gives way to refusing.
- The refusal reports the queries tried and the gap found; a bare refusal is indistinguishable from an outage.
- Distinguish corpus-silence from retrieval-failure: a weak result on a known-included topic is a retrieval bug, not a refusal case.
- Refusals on high-traffic questions are a corpus roadmap, not a metric to minimize.
- The mode matters: an assistant at a search interface refuses differently from a pipeline that must never fabricate.
- Measure refusal rate by query class; changes signal corpus or retrieval shifts, not model morality.

## Procedure

1. Set the relevance threshold from retrieval scores or graded judgments.
2. Design the refusal text: queries tried, result, one next step.
3. Separate the handling of retrieval failures from genuine corpus silence.
4. Log refusals with their query classes.
5. Review refusal logs against corpus coverage plans.
6. Adjust the threshold only with measured grounds, and record the change.

## Anti-patterns

- Optimizing to reduce refusal rate as if it were an error rate.
- A refusal with no content pretending to be politeness.
- Treating retrieval failure as corpus silence.
- A single refusal mode for every application context.
- Changing threshold after one embarrassing miss, with no measurement.

## Done checklist

- [ ] Relevance threshold stated.
- [ ] Refusal names the queries and the gap.
- [ ] Retrieval failure distinguished from silence.
- [ ] Refusals logged by query class.
- [ ] Logs feed corpus coverage.
- [ ] Threshold changes measured and recorded.

## Sources

- RAG architecture overview: <https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview>
- Citation mechanics for sourced answers: <https://docs.anthropic.com/en/docs/build-with-claude/citations>
- Original RAG paper: <https://arxiv.org/abs/2005.11401>

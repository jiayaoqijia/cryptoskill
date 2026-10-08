---
name: abstain-when-context-is-insufficient
description: Use when a retrieval answer is fluent even when the chunks do not contain the fact. Requires the answer to abstain or flag gaps instead of filling them from model memory.
---

# Abstain When Context Is Insufficient

A RAG system that always answers will answer past its evidence. The safe behaviour is to answer only from the retrieved chunks and, when they do not cover the question, say so and ask for what is missing.

## Procedure

1. State the contract in the prompt: answer using only the provided chunks; if they do not contain the answer, reply `INSUFFICIENT_CONTEXT`.
2. Require a citation per claim; a claim with no supporting chunk is disallowed by construction.
3. After generation, check each sentence against its cited chunk — a sentence with no citation is a candidate fabrication (`verify-answer-claims-against-chunks`).
4. Handle the zero-chunk case explicitly: if retrieval returns nothing above the score floor, abstain before calling the generator.
5. Distinguish "not in the corpus" from "not retrieved": an empty result may mean a missing document, which is a data gap to report, not a confident "no".
6. Offer the nearest partial answer with its limits: "the docs cover refund timing but not the EU-specific window."
7. Log every abstention with the query and retrieved ids; a spike in abstentions is an ingest regression.
8. Never let the model's pretraining fill a gap silently — if it answers from memory, mark it `UNVERIFIED`.
9. Test with off-corpus questions on purpose; an eval with only answerable questions cannot detect over-answering.
10. Report abstention rate as a first-class metric, not a failure to hide.

11. Log the query alongside the flag so a wave of abstentions can be traced to an ingest gap or a prompt change.

## Pitfalls

- A system prompt that says "be helpful", which the model reads as licence to guess.
- Grader evals that penalise every abstention, training the system to always invent an answer.
- Treating the model's own confidence prose as evidence of coverage.
- Abstaining on a question the corpus answers because retrieval was too tight, not because the fact is absent.
- Returning "I don't know" with no information about what was searched, leaving the user stuck.
- Allowing a partial answer without flagging which sub-question is unanswered.

- A temperature or sampling change that quietly raises over-answering without touching retrieval.
- Abstaining on the whole answer when only one sub-question is uncovered, discarding the parts that are supported.

## Verification

    python3 eval.py --set evals/offcorpus.jsonl
    # passes when 0 off-corpus questions are answered as fact and every gap is flagged INSUFFICIENT_CONTEXT

Report to the user: abstention rate on answerable vs off-corpus sets, and the flags emitted for partial answers.

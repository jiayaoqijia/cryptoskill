---
name: ask-a-decision-ready-question
description: Use when you need a human decision or missing input. Ask with the options, the tradeoffs, your default, and what happens if nobody answers.
---

# Ask a decision-ready question

A bare "what should I do?" offloads the analysis back to the reader. A decision-ready ask brings options, costs, and a default so one reply can close it.

## Procedure

1. Confirm it is genuinely unanswerable by you: search the repo and docs first with `rg -n "API_KEY|endpoint|config" .`.

2. State the decision in one line: what must be chosen, and why now.

3. Give two or three options, each labelled with cost, risk, and reversibility.

4. Mark your recommended default and the reason for it.

5. Give the consequence of silence: "absent an answer I will ship option B on Friday".

6. Ask exactly one question. Several questions in one message get partially answered.

7. Put the question at the top, never after a page of context.

## Pitfalls

- "What should I do?" without options pushes the work back uphill.
- Bundling five decisions into one message guarantees a partial reply.
- No default means the task stalls silently waiting for an answer that never comes.
- Asking for facts you could have looked up spends trust for nothing.
- A question buried at the end of a status report is routinely missed.

## Verification

    grep -c "?" question.md   # exactly one question mark in the ask block

Ask one question, with options, a recommendation, and a default action on silence.

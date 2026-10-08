---
name: summarize-a-thread-faithfully
description: Use when condensing a long conversation, ticket, or log into a summary. Preserve who said what, keep dissent visible, and list open questions without editorialising.
---

# Summarize a thread faithfully

A summary that flattens dissent into consensus becomes the record people cite. Carry attribution, unresolved disagreement, and open questions intact.

## Procedure

1. Read the whole thread before writing a line; a summary built from the top misrepresents the end.

2. Capture each distinct position, attributed: "A argued X; B proposed Y because Z."

3. Preserve unresolved disagreement explicitly; never average it into false consensus.

4. List decisions made, each with the message that made it.

5. List open questions and who owes the answer.

6. Mark your own additions as `[summary author: ...]` so they are not read as thread content.

7. Keep quotations short and verbatim; paraphrase can invert meaning.

## Pitfalls

- Dropping minority dissent produces a summary the thread itself would reject.
- Attributing a paraphrase to someone who did not say it misrepresents them.
- Picking a side without flagging it hides the decision from the reader.
- Omitting open questions makes the thread look closed when it is not.
- Summarising from memory rather than the log loses the exact wording that matters.

## Verification

    grep -cE "^(Decision|Open|Disagreement):" summary.md   # each class present when it exists

Summarise positions, decisions, dissent, and open questions, each with attribution.

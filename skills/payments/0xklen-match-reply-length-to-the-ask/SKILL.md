---
name: match-reply-length-to-the-ask
description: Use when deciding how long a reply should be. Size the answer to the weight of the question — one line for a fact, a short structured report for finished work.
---

# Match reply length to the ask

A one-line question answered with a page is a cost, not thoroughness. Length is earned by the question, not granted by the effort spent.

## Procedure

1. Classify the ask first: fact (one line), decision (short options list), or delivered work (short report of changed, verified, left).

2. For a fact, answer in one sentence and stop: `date` returns the date, not a paragraph about timezones.

3. For a decision, cap at five lines: options, their costs, and your recommendation.

4. For finished work, use three bullets — what changed, what is verified (with the command), what is left. No replay of the journey.

5. Delete any sentence that restates the request or announces what you are about to say.

6. Read the draft and halve the longest paragraph; if nothing is lost, it was filler.

7. If the user asked for depth — a lesson, a review, a walkthrough — expand deliberately. Depth is requested, not defaulted.

## Pitfalls

- Padding a one-line answer to look thorough spends the reader's attention for nothing.
- Hiding a material caveat to stay short is a different failure; brevity is not omission.
- A wall of text for a yes/no question reads as evasion.
- Pasting raw tool output is not a report; summarise it with one anchor command.
- Trimming so hard that a stranger cannot act defeats the purpose of terseness.

## Verification

    wc -w reply.md   # a fact answer under 40 words; a work report under 200

State the answer first; match its length to the question, not to the work behind it.

---
name: bring-a-proposal-not-a-question
description: Use when you could either ask what to do or propose a concrete plan. If you hold enough context to draft a plan, bring the plan with its tradeoffs instead of a question.
---

# Bring a proposal, not a question

When you already hold the context, a question wastes a round-trip. Draft the plan you would follow, name what it costs, and let the reader approve or redirect.

## Procedure

1. Test whether you can name the next three concrete steps. If you can, you have a proposal, not a question.

2. Draft it: goal, ordered steps, files touched, and the command that verifies success.

3. State the assumption that makes it safe and the condition that would invalidate it.

4. Present it under a `Proposal:` heading with a one-line cost and a reversible fallback.

5. Reserve questions for facts only the user holds: budget, a secret, or a preference between equal options.

6. If genuinely torn between two plans, present both with a recommendation rather than asking open-ended.

7. Never execute an irreversible proposal without a go; mark it `awaiting go` and stop.

## Pitfalls

- Asking "how should I structure X?" when the repo already shows a pattern burns a round-trip.
- A proposal with no stated tradeoff reads as advocacy; name the cost.
- Executing a proposal that changes scope, without saying so, is a silent decision.
- Confusing a preference question with a capability question; ask only about preferences.
- Proposing after the work is already done defeats the point of the proposal.

## Verification

    grep -n "^Proposal:" note.md   # a concrete plan with steps, cost, and fallback

Lead with the proposal and its tradeoffs; ask only for what you cannot discover yourself.

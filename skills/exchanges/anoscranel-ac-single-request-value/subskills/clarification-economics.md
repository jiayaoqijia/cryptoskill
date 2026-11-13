---
name: clarification-economics
domain: prompt-engineering/clarification-economics
trigger: "Deciding whether a clarifying question earns its round trip."
anti_trigger: "Not for prompt style alone, and not for interactive chat."
scope: "When a clarifying question is worth a round trip, and when a staged-response contract is better."
status: seedling
---

# Clarification economics

## Standard

The clarifying question is the classic hidden cost under a request cap. In an unmetered chat, asking "do you mean the 2023 or the 2024 filing?" is free; under a cap it is a full request — and one that produces no work, only a disambiguation. The request-hungry habit burns a round trip on the question and a second on the re-run that uses the answer, when a single well-contracted request could have carried both branches.

The core move is the conditional contract: instead of asking which condition holds, write the request to say "if the condition holds, do X; otherwise do Y, and state which branch was taken." One request, both branches, a stated disambiguation. The clarification that cannot be contracted away — a genuinely missing fact the responder cannot infer or retrieve — is the only kind that earns its round trip, and even then the question should carry the next step with it so the answer runs work forward rather than stopping to await number two.

Primary sources: <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering> and <https://12factor.net/>.

## Decision rules

- Before asking a clarifying question, ask whether a conditional contract can carry both branches.
- Write conditional requests as "if X then A; if not-X then B; state the branch taken."
- When clarification is genuinely needed, pack the follow-up work into the same request.
- Budget the whole work session in requests at planning time, including any expected clarifications.
- Prefer assumptions stated in the request ("assume the 2024 filing; note if this distorts") over questions where an error is cheap to detect.
- Record each spent clarification in the ledger with what it changed, to retrain the habit.

## Procedure

1. At the moment a clarifying question arises, write down what the answer changes.
2. Test whether a conditional contract can cover both cases in one request.
3. If yes, write the conditional and send; if no, keep the question but attach the contingent work.
4. State the assumption path explicitly in the request so the response shows which branch ran.
5. Log the decision: clarified, contracted, or assumed, with the cost.
6. Review the ledger's clarification entries per session and eliminate the repeat patterns.

## Anti-patterns

- Burning a request purely to ask and a second to act on the answer.
- Asking a question whose answer the material in the request already contains.
- A conditional contract that leaves the branch unstated in the response.
- A clarifying question about preference where either branch would have been adequate.
- Session planning that treats clarifications as free.

## Done checklist

- [ ] Clarification need written down with what it changes.
- [ ] Conditional-contract alternative tested first.
- [ ] Genuinely needed questions carry their follow-up work.
- [ ] Assumption path stated in the request.
- [ ] Decision logged in the ledger with cost.
- [ ] Repeat clarification patterns eliminated at review.

## Sources

- Prompt engineering guidance, Anthropic: <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering>
- The twelve-factor app: <https://12factor.net/>
- Provider limits documentation, Google: <https://ai.google.dev/gemini-api/docs/rate-limits>

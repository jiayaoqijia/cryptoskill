---
name: instruction-form
domain: prompt-engineering/instruction-form
trigger: "When writing, tightening, or reviewing any single instruction line in a prompt."
anti_trigger: "Choosing among named techniques (few-shot, chain-of-thought, role lines) — that is the patterns decision, not line form."
scope: "Writing a single instruction line that adds information: the information test, positive checkable constraints, placement, and the instruction budget."
status: "seedling"
---

# Instruction form

## Standard

Every prompt technique does one of two things: it adds **information** the model could
not infer, or it tries to **elicit** a better answer from what the model already knows.
Information lines survive model generations; elicitation lines get absorbed into
training (<https://ai.google.dev/gemini-api/docs/prompting-strategies>). The
test for any line: **what could a competent person not do without it?** "The schema
version is 4.2" passes. "Be thorough" fails, because thoroughness was implied by asking.
State constraints positively and checkably: "reply with: approve / reject / escalate"
can be enforced with an `in` test; "do not be vague" enforces nothing. Give
the model an explicit license to abstain ("if the document does not say, answer: NOT IN
DOCUMENT"), because the highest-probability continuation of a question is an answer.
The 2026 OpenAI structure is Identity, Instructions, Examples, Context,
with private data positioned near the end
(https://platform.openai.com/docs/guides/prompt-engineering, fetched 2026-10-21).

Primary sources: <https://www.anthropic.com/engineering/building-effective-agents> and <https://ai.google.dev/gemini-api/docs/prompting-strategies>.

## Decision rules

| Line type | Verdict |
|---|---|
| Fact, constraint, or contract the model cannot know | Keep |
| Quality adjective ("careful", "world-class expert") | Delete; zero measured lift |
| Threat, tip, or plea ("my career depends on it") | Delete; 2023-era folklore |
| Format description in prose | Replace with one exemplar of the exact output |
| Negative rule ("never do X") | Pair it with the positive action to take instead |

Shorter beats longer for single-task prompts: in a 28K-prompt study, prompts under 50
words scored 80.1 versus 66.9 for prompts over 300 words, and 62% of the long prompts
held contradictory constraints (corpus study, <https://arxiv.org/html/2511.00751v2>).
Contradictions between a user's own sections are a leading failure cause (OpenAI,
https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide).

## Procedure

1. Draft the line. Apply the information test; delete on a fail.
2. Convert every negative into a positive plus an exception path.
3. Make every rule checkable in code or by a reviewer at a glance.
4. Order the prompt: identity line first, instructions, examples, context and pasted
 documents last.
5. Add the abstain license wherever the model must not invent.
6. Read the whole draft for self-contradiction before shipping.

## Anti-patterns

- Kitchen-sink anticipation of rare failures; move rare content out on demand.
- Vibe constraints ("be careful") that nothing can check.
- Role inflation openings ("Act as a world-class expert"); zero measured lift
 (Deep-Dive, 28K corpus).
- Buried critical rules in the middle of long prompts; restate them at the end.

## Done checklist

- [ ] Every line passes the information test.
- [ ] Every constraint is positive and checkable.
- [ ] An abstain path exists wherever invention is dangerous.
- [ ] No two lines demand conflicting behavior.

## Sources

- <https://www.anthropic.com/engineering/building-effective-agents>
- <https://ai.google.dev/gemini-api/docs/prompting-strategies>

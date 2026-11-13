---
name: prompt-patterns
domain: prompt-engineering/prompt-patterns
trigger: When deciding whether to add few-shot examples, a persona, chain-of-thought wording, or a structured-output schema to a prompt.
anti_trigger: Wording a single instruction line, or choosing model and sampler settings.
scope: Picking named prompt text techniques and knowing which are dead, absorbed, or conditional in 2026.
status: seedling
---

# Prompt patterns: which named techniques still work

## Standard

Evidence sources: <https://ai.google.dev/gemini-api/docs/prompting-strategies> and the arXiv papers cited
per row below.

| Technique | 2026 status | Receipt |
|---|---|---|
| Persona / role lines | Dead for accuracy | 162 personas tested, no reliable gain over none (Zheng et al. 2024). Keep a one-line identity only for voice and scope |
| "Think step by step" | Dead to harmful on reasoning models | OpenAI guidance: it can interfere with internal reasoning; reasoning models do it unprompted |
| Chain-of-thought on fast models | Conditional | On GPT-class instruction models, explicit steps still help (OpenAI junior-coworker analogy) |
| Few-shot examples | Alive, but as shape exemplars | One example of the exact output beats describing it; use varied canonical examples, identical formatting (Google Vertex: include few-shot; too many overfit) |
| Self-consistency (sample-and-vote) | Conditional | ~0.4-1.6% at 15-20x token cost on Gemini 2.5 (arXiv:2511.00751); use only far below ceiling |
| Tree-of-thought, ReAct loops | Absorbed | Reasoning models explore internally; tool calling is native |
| Reflection / self-critique loops | Harmful in excess | Parallel attempts beat sequential rethink by up to 20% at equal budget (NeurIPS 2025, per Deep-Dive) |
| Structured output (JSON schema) | Alive and first-choice | Schema as an API parameter, not format prose (OpenAI structured outputs guide) |

## Decision rules

1. Need a fixed output shape? Use the schema parameter. Add one exemplar only if the
 schema cannot express the shape.
2. Need judgment quality on a reasoning model? Give the goal and constraints, no
 reasoning instructions. On a fast instruction model, short explicit steps still pay.
3. Need a voice or a narrow behavior band? One identity line with scope and refusal
 boundary. Skip personas-as-performance.
4. Considering ensembling? Price it first; buy it only when single-pass accuracy is
 measurably below the ceiling the task needs.

## Procedure

1. Name the failure you are treating (wrong format, wrong reasoning, wrong tone).
2. Map it to the roster: format -> schema + exemplar; reasoning -> goal-plus-constraints;
 tone -> identity line.
3. Apply at most one new technique per change, so the eval can attribute the effect.
4. Re-run the golden set before and after; keep only measured wins.

## Anti-patterns

- Stacking five techniques on one prompt; interactions are untraceable.
- "You are an expert..." plus "think step by step" on a reasoning model: two dead lines.
- Ten near-duplicate few-shot examples; overfit and burn budget.
- Reflection loops as a default; they overthink (Deep-Dive Part I).

## Done checklist

- [ ] Each added technique maps to a named failure mode.
- [ ] No dead technique ships (persona-for-accuracy, CoT on reasoning models).
- [ ] The change was measured on the golden set, not eyeballed.

## Sources

- Prompt-engineering corpus: <https://ai.google.dev/gemini-api/docs/prompting-strategies>; "Deep-Dive" = <https://arxiv.org/html/2511.00751v2>.

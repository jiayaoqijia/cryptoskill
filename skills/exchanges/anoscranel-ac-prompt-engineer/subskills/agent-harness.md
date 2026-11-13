---
name: agent-harness
domain: prompt-engineering/agent-harness
trigger: "When writing or restructuring the standing instructions an agent runs under (the root developer message), its tool rules, memory rules, or handoff format."
anti_trigger: "A one-shot user prompt, or securing against hostile content in the input."
scope: "The anatomy of an agent's root instructions: the identity-first skeleton, tool contracts, memory lifecycle, handoff contracts, and refusal handling."
status: "seedling"
---

# Harness and agent prompt mechanics

## Standard

Production agents converge on one skeleton, seen across a 30-prompt audit of shipping
products: **identity, then behavior rules, then tool usage, then output format, then
safety last** (<https://arxiv.org/html/2511.00751v2>
Part II). The identity line is load-bearing and goes on line one. Sections are marked
with XML-style tags or Markdown headers so the model can navigate long documents.
Negative rules ("never X") dominate agentic prompts; each is a changelog of a past bug,
so pair every negative with the positive action to take instead. Refusals are named
constants, not improvised prose; apologies are forbidden in production teardowns.
Load-bearing rules get restated at the end of long prompts (recency pinning).

Message roles carry authority: OpenAI's Model Spec orders platform and developer
messages above user messages, though production models do not fully reflect the chain,
so never treat ordering as armor (OpenAI Model Spec).
Assemble context in authority order: immutable authority and policy first; task, goal,
and stop conditions; typed tools and permissions; examples; then retrieved, user, and
memory material last (<https://model-spec.openai.com/2026-08-18.html>).

Primary sources: <https://www.anthropic.com/engineering/building-effective-agents> and <https://modelcontextprotocol.io>.

## Decision rules

| Component | Rule |
|---|---|
| Identity | One line: what the agent is, its scope, its refusal boundary |
| Tools | State intent in prose; enforce arguments in JSON Schema; enforce permissions and side effects in code, never in prose alone |
| Memory | Writes require authorization; records carry provenance, TTL, and a supersedes link |
| Handoffs between agents | Pass typed fields (goal, constraints, evidence, next action), not transcript summaries |
| Refusals | One named constant message; a documented fallback path |

## Procedure

1. Write the identity line first.
2. Add behavior rules, each positive-plus-checkable, each with its failure
 counterpart.
3. Document each tool: when to call it, when not to, what its errors mean.
4. Specify the output contract and the abstain path.
5. Put safety and escalation last, restated near the end if the document is long.
6. Version the whole artifact in code with its eval fixtures.

## Anti-patterns

- Kitchen-sink bloat; prompts under 50 words beat 300-plus-word prompts on quality in
 the large-corpus study (Deep-Dive).
- Tool permissions enforced by instructions only; enforce in deterministic code.
- Transcript-summary handoffs that drop boundary markers and constraints.
- Secrets in the instruction text; keep credentials out-of-band.

## Done checklist

- [ ] The skeleton order is identity, behavior, tools, format, safety.
- [ ] Every negative rule names the positive alternative.
- [ ] Tool permissions are enforced in code, not prose.
- [ ] Refusals use the named constant with the fallback documented.

## Sources

- <https://www.anthropic.com/engineering/building-effective-agents>
- <https://modelcontextprotocol.io>

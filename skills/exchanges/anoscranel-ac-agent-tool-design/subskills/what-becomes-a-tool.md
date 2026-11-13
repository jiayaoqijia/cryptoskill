---
name: what-becomes-a-tool
domain: prompt-engineering/what-becomes-a-tool
trigger: "Deciding whether a capability should become a tool at all."
anti_trigger: "Not for protocol wiring, and not for the client loop."
scope: "Capabilities that earn tool status, and those that should stay prompt or workflow."
status: seedling
---

# What becomes a tool

## Standard

Tools are for things the model cannot do by generating text: act on the world, retrieve what it cannot see, or verify a claim against a source. Reading a file, querying a database, sending a message — these are actions and observations, and generation cannot substitute for either. Conversely, a task the model can do directly — summarise, restructure, plan — is only degraded by wrapping it in a tool that calls the model again.

The second filter is epistemic safety. A capability becomes a tool only when its misuse is either recoverable or bounded: a read-only lookup misfires cheaply and teaches the model something; a destructive action misfires expensively and teaches nothing because the damage stands. Structuring access so the harmful calls cannot be trivially made is the point of this leaf — the model should not be able to destroy state in a single moment of confusion that was caused by our own bad tool naming or a too-broad capability.

Primary sources: <https://docs.anthropic.com/en/docs/agents-and-tools/tool-use> and <https://modelcontextprotocol.io/docs/concepts/architecture>.

## Decision rules

- Act-on-world or observe-world capabilities are tool candidates; pure-generation tasks are not.
- One capability per tool; a tool that does two related but different things reads as unclear to its only reader.
- Irreversible actions get their own separate tool, never bundled with benign reads.
- Reserve destructive tools for a narrower, precisely described surface with required confirmation parameters.
- Nothing that feeds the model's own reasoning (synthesis, summarisation of context it already has) earns a tool.
- Default to fewer tools; remove tools nobody calls or the model rarely uses.

## Procedure

1. List every capability a plan implies the agent needs.
2. Split into: generate-directly / act-on-world / observe-world.
3. Mark each act as reversible or irreversible.
4. Tool the observers; split the irreversible acts out as separate, minimal tools.
5. Leave generate-directly tasks in prompts where they already belonged.
6. Record the rejected candidates with reasons in the tool-surface record.

## Anti-patterns

- Tools that wrap a model call inside an agent's model call.
- One do-everything tool because wiring fewer functions was easier.
- A delete-or-modify parameter buried inside a benign read tool.
- Tools "just in case" — unused surface still costs selection accuracy.
- Giving a capability tool status when a good prompt answer exists.

## Done checklist

- [ ] Capabilities split by generate / act / observe.
- [ ] Irreversible acts isolated and narrowed.
- [ ] Rejected candidates recorded with a reason.
- [ ] Reversibility of every action stated in its description.
- [ ] Anything the model can already do left as a non-tool.
- [ ] Default direction was subtraction, not addition.

## Sources

- Tool-use design framing: <https://docs.anthropic.com/en/docs/agents-and-tools/tool-use>
- Function calling overview: <https://platform.openai.com/docs/guides/function-calling>
- Capability layering context: <https://modelcontextprotocol.io/docs/concepts/architecture>

---
name: reading-descriptions
domain: prompt-engineering/reading-descriptions
trigger: "Writing tool names and descriptions a model reads correctly."
anti_trigger: "Not for the client loop, and not for MCP transport."
scope: "Descriptions and names written for a model reader."
status: seedling
---

# Reading descriptions

## Standard

The model selects a tool from its description alone, in a menu of competitors, without the benefit of a demo or a tooltip. The description is therefore the entire discoverability surface, and it earns its length: what the tool does, when to use it, and when not to use it. The third part is the one most often omitted, and its omission is why agents pick a near-miss tool with misplaced confidence — a description without boundaries reads as matching more tasks than it should.

Names are the second read. A model matches the request's words against the tool's name and description; a name like `run` or `process_data` matches nothing in particular, while a name built from the verb and object of its real use matches the requests it is for. The name answers "what does this do" at a glance; the description answers "is this the right one for this request" — and both should be tested against real misfire examples, not written from a wish.

Primary sources: <https://docs.anthropic.com/en/docs/agents-and-tools/tool-use> and <https://platform.openai.com/docs/guides/function-calling>.

## Decision rules

- Description states: what it does, when to use it, when NOT to use it.
- Name carries verb and object; verbs match what a real user would say.
- Where two tools are adjacent, each description names the other as its boundary.
- Test the description against real requests that should NOT select it, before shipping.
- Rewrite on misfire: the fix for a wrong-tool problem is usually a description fix, not more tools.
- Keep descriptions truthful against implementation drift — a stale description is a worse default than a sparse one.

## Procedure

1. Draft the description as what / when / when-not.
2. Name the tool from its verb-plus-object.
3. Read the description against the neighbouring tools; add explicit boundaries where the menu confuses close capabilities.
4. Test with a sample of real, non-matching requests; any false selection is a boundary gap.
5. Rewrite after misfires found in the log; the misfire's text tells you the missing boundary.
6. Re-verify the description after any implementation change to the tool itself.

## Anti-patterns

- A description that is only a positive claim with no when-not.
- Marketing tone ("powerful", "intelligent") — words that match no real request.
- Vague names where the verb is missing (`data`, `handle`, `process`).
- Descriptions that went stale after the tool's behaviour changed.
- Fixing wrong-tool misfires by adding yet another adjacent tool instead of better boundaries.

## Done checklist

- [ ] Description = what / when / when-not.
- [ ] Name carries verb and object.
- [ ] Neighbour boundaries explicit.
- [ ] Negative sample tested with zero false selections.
- [ ] Implementation and description verified in sync.
- [ ] Misfire-driven rewrites recorded in the log.

## Sources

- Tool-use with structured descriptions: <https://docs.anthropic.com/en/docs/agents-and-tools/tool-use>
- Function definitions the model reads: <https://platform.openai.com/docs/guides/function-calling>
- Architecture of the tool layer: <https://modelcontextprotocol.io/docs/concepts/architecture>

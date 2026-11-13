---
name: result-payloads
domain: prompt-engineering/result-payloads
trigger: "Shaping what a tool returns into the context window."
anti_trigger: "Not for the transport layer, and not for UI rendering."
scope: "What a tool returns to a context window, and what it omits."
status: seedling
---

# Result payloads

## Standard

A tool result lands in the same context window as everything else the model is juggling, and unlike a person skimming a dashboard, the model cannot skim: every token in the result is read, billed, and can crowd out what matters. The payload shape is therefore an information-design problem with a budget — return the fields the next decision needs, in a structure that makes the important facts impossible to miss, and leave the rest retrievable on demand rather than inline.

The common failure is the faithful dump: an entire JSON record, a full HTML page, raw database rows, returned because the tool's author sought fidelity rather than usefulness. Fidelity is a person's virtue; the model reader needs density. A second pass on the result shape — dense summary fields first, detail behind an explicit follow-up — often does more for agent accuracy than any prompt change, because it removes the step where the model must find the needle before using it.

Primary sources: <https://docs.anthropic.com/en/docs/agents-and-tools/tool-use> and <https://platform.openai.com/docs/guides/function-calling>.

## Decision rules

- Bound every result: caps on records returned, characters per field, total tokens.
- Lead with the fields next decisions use; order is meaning to a sequential reader.
- Distinct status field first — success, empty, partial, not-found — so the model's next step is determined before it reads detail.
- Where results need a second look, return a reference (an ID, a link) the model can pass to a detail tool.
- Return errors as structured data, close to the same shape as success, never as prose paragraphs.
- Empty is a result: "no records matched" with the query echoed beats silence or a null.

## Procedure

1. List the decisions the model makes right after this tool returns.
2. Trim the payload to the fields those decisions consume.
3. Add a distinct status field and place it first in structure, not in prose.
4. Cap the result; provide a pagination or detail-retrieval path for the rest.
5. Test the shape on real conversations before shipping the tool.
6. Record the payload contract in the tool-surface record.

## Anti-patterns

- The faithful dump — an entire API response or database row.
- Results whose status is expressed in prose the model has to parse.
- Nested objects five levels deep where a flat list would be read reliably.
- Truncating silently at an arbitrary limit without a status field saying so.
- Returning raw HTML/markup where a plain structure would serve the model.

## Done checklist

- [ ] Decisions-after-return listed.
- [ ] Payload fields match decisions only.
- [ ] Status field first and structured.
- [ ] Caps and completion status explicit.
- [ ] Detail retrieval path exists for second looks.
- [ ] Empty case designed, not defaulted.

## Sources

- Tool result handling: <https://docs.anthropic.com/en/docs/agents-and-tools/tool-use>
- Function result submission: <https://platform.openai.com/docs/guides/function-calling>
- Tool layer architecture: <https://modelcontextprotocol.io/docs/concepts/architecture>

---
name: tool-menu-design
domain: prompt-engineering/tool-menu-design
trigger: "Designing the whole tool menu rather than one tool."
anti_trigger: "Not for a single tool's schema, and not for transport."
scope: "Menu size, near-duplicates, grouping, and the confusion cost of breadth."
status: seedling
---

# Tool menu design

## Standard

Every tool added to the menu taxes every selection the model makes: the more entries, the more confusion surface, and the worse the odds that any given request picks the right one. Provider guidance is consistent — keep the toolset small and focused; where an application needs many functions, newer mechanisms such as tool search exist to defer loading rarely used tools. Menu size is a design constraint, not an accumulation problem.

The confusion cost is dominated by near-duplicates: two or more tools whose descriptions overlap in stated purpose but differ in scope, recency, or permission. The model cannot see the difference an implementer sees, so it selects on whichever word matched best. Grouping tools the way a person would look for them — one area, one subject, one action set — matters more than completeness, because a menu the model cannot navigate is a menu that behaves like noise.

Primary sources: <https://platform.openai.com/docs/guides/function-calling> and <https://modelcontextprotocol.io/docs/concepts/architecture>.

## Decision rules

- Keep the active menu small; move rarely used tools to a deferred mechanism where the provider offers one.
- Merge near-duplicates: two overlapping tools usually indicate one tool with an extra parameter, not two tools.
- Prefer grouped, fewer interfaces over more complete ones — completeness is a person's value.
- When a menu exceeds a working set (often around two dozen), audit for tools whose descriptions only differ in adjective.
- Group tools by the model's task flow, not by internal service boundaries the model cannot see.
- Every tool earns its place by observed selection frequency; the log decides, not the author.

## Procedure

1. Inventory the menu; count selection frequency per tool from logs.
2. Mark zero/low-frequency tools for removal or deferral.
3. Identify near-duplicates by pairwise description overlap; merge or explicitly bound them.
4. Re-group what remains by task flow.
5. Test the reduced menu against a fixed sample of real requests.
6. Record the reduction and its selection-accuracy effect.

## Anti-patterns

- Accreting tools per feature without ever removing one.
- Menu mirroring internal microservice structure instead of tasks.
- Near-duplicates kept "just in case" — the model's confusion stays priced-in.
- Assuming more tools is more capable; more menu is more confusion.
- Deferring the audit until the agent visibly misfires on a daily basis.

## Done checklist

- [ ] Frequency audit completed from logs.
- [ ] Rare tools removed or deferred.
- [ ] Near-duplicates merged or bounded.
- [ ] Menu grouped by task flow.
- [ ] Fixed-sample selection test re-run after reduction.
- [ ] Reduction effect recorded.

## Sources

- Menu size and tool-search guidance: <https://platform.openai.com/docs/guides/function-calling>
- Tool layer architecture: <https://modelcontextprotocol.io/docs/concepts/architecture>
- Tool-use guidance: <https://docs.anthropic.com/en/docs/agents-and-tools/tool-use>

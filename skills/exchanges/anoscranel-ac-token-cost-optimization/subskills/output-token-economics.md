---
name: output-token-economics
domain: prompt-engineering/output-token-economics
trigger: "Controlling the expensive half of the bill: what the model writes back."
anti_trigger: "Not for prompt-packing, and not for streaming mechanics."
scope: "The expensive half of the bill: caps, format, and reasoning tokens."
status: seedling
---

# Output token economics

## Standard

Output tokens bill at a multiple of input — commonly several times the input rate — so every generated token is the most expensive token in the request. Three controls govern the total: the requested format's verbosity, any reasoning or tool-loop tokens the tier generates before the visible answer, and the hard cap set on the response. A workload that asks for a paragraph and gets an essay, or that runs long internal reasoning on a tier that bills for it, pays the output multiple on all of it.

The controls are explicit in the request. Output caps bound the worst case; format instructions ("answer in at most five bullets", "return JSON only") shape the working case; and tier selection changes whether internal reasoning bills as visible output. The saving is measured as output tokens per completed task before and after the change, at the dated output rate.

Primary sources: <https://docs.anthropic.com/en/docs/about-claude/pricing> and <https://platform.openai.com/docs/models>.

## Decision rules

- Set an explicit output cap whenever the task does not require long generations.
- Ask for the format the consumer actually parses — needless prose bills at the output rate.
- Check whether the tier bills internal reasoning tokens; if so, count them in the cost of the tier choice.
- Measure output tokens per completed task, not per request sent.
- Compare terse-output instructions against cut output at equal outcome quality.
- Beware of caps so tight they truncate and force retries: a truncated retry doubles spend.

## Procedure

1. Measure current output tokens per completed task from usage data.
2. Identify the consumer's true need: format, length, and parseability.
3. Rewrite the output instruction to the minimal sufficient form.
4. Set the cap above the working case so it never truncates normal work.
5. Re-measure output tokens per task at equal quality.
6. Record the before-and-after dollars per task.

## Anti-patterns

- No output instruction at all; defaults drift long.
- Caps at the working case's upper edge: retries caused by truncation obliterate savings.
- Measuring output tokens per request while ignoring the retry rate.
- Forget which tiers bill reasoning tokens.
- Cutting verbosity where the prose itself is the value delivered — brief must not mean worse.

## Done checklist

- [ ] Output tokens per completed task measured.
- [ ] Output instruction rewritten to minimal-sufficient form.
- [ ] Cap set safely above the working case.
- [ ] Retry rate unchanged.
- [ ] Reasoning-token treatment checked on the chosen tier.
- [ ] Dollars per task before and after recorded.

## Sources

- Output rate basis: <https://docs.anthropic.com/en/docs/about-claude/pricing>
- Tier capabilities and reasoning: <https://platform.openai.com/docs/models>
- Model overviews: <https://docs.anthropic.com/en/docs/about-claude/models/overview>

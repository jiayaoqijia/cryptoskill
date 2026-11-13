---
name: tokens-capacity
domain: prompt-engineering/tokens-capacity
trigger: "When a prompt is long, costs too much, forgets earlier content, or needs caching or compaction designed."
anti_trigger: "Choosing techniques for output quality, or hardening against hostile input."
scope: "Budgeting the context window: attention economics, stable-prefix caching, placement rules, compaction, and just-in-time retrieval."
status: "seedling"
---

# Tokens and capacity

## Standard

Treat the context window as a finite attention budget. Seek the minimal set of
high-signal tokens; recall degrades as context grows ("context rot")
(Anthropic, https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents,
via <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>). Order prompts for
caching: stable prefix first, dynamic tail last. Anthropic caches explicit breakpoint
prefixes (5-minute default TTL, 1-hour option; minimum 1,024-4,096 tokens by model);
OpenAI caches automatically above 1,024 tokens at a 50% input discount; Gemini 2.5+
has implicit caching on by default (per-provider specifics: <https://claude.com/blog/best-practices-for-prompt-engineering> and the Gemini prompting-strategies guide). For long-context models: Gemini guidance places context
first and instructions last (<https://ai.google.dev/gemini-api/docs/prompting-strategies>), and production
prompts restate load-bearing rules at the end where attention is highest ("recency
pinning", Part II of <https://arxiv.org/html/2511.00751v2>).

Primary sources: <https://developers.openai.com/> and <https://www.anthropic.com/engineering/building-effective-agents>.

## Decision rules

| Symptom | Lever |
|---|---|
| High input cost on repeated long prompts | Stable-prefix order; measure cache-read token share |
| Model forgets an early rule in a long prompt | Restate that rule near the end |
| Context window nearing full mid-task | Compact: summarize, restart; clear old tool results first |
| Huge reference corpus the model rarely needs | Just-in-time retrieval: hand paths and queries, not pasted docs |
| Slow, expensive tool chatter | Budget by content kind: reserve task and evidence space, cap examples and memory |

## Procedure

1. Measure first: log input tokens, cache-read share, and where the output degrades as
 length grows.
2. Split the prompt into stable (identity, rules, schemas) and dynamic (request data).
 Put stable first.
3. For agent loops, plan compaction before the wall: summarize summarized state, keep
 artifacts outside the window with IDs and hashes.
4. Prefer references over preload: give the agent grep-style handles and let it pull
 what it needs (Anthropic context engineering).
5. Track the cache numbers after every layout change; layout is a cost lever now.

## Anti-patterns

- Preloading whole documents "just in case"; preloading pays once, retrieval pays per
 need.
- Editing the stable prefix casually; every edit invalidates the cache.
- Growing the prompt to fix failures that missing information actually caused.
- Compacting by deleting the newest tool results; clear the oldest, largest ones first.

## Done checklist

- [ ] Stable and dynamic sections are separated and ordered correctly.
- [ ] Cache-read token share is logged and trending up on repeated traffic.
- [ ] A compaction plan exists before the context wall, not after it.
- [ ] Rarely needed reference material is reachable, not pasted.

## Sources

- <https://developers.openai.com/>
- <https://www.anthropic.com/engineering/building-effective-agents>

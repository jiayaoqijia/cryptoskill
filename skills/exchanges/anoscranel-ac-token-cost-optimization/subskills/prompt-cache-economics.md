---
name: prompt-cache-economics
domain: prompt-engineering/prompt-cache-economics
trigger: "Deciding whether and how to arrange prompts for cache discounts."
anti_trigger: "Not for cache endpoint mechanics, and not for HTTP wiring."
scope: "Cache hits, cache writes, and arranging prompts so prefixes repeat."
status: seedling
---

# Prompt cache economics

## Standard

Prompt caching charges a discounted rate when a request repeats a prefix the provider has already processed — per provider documentation, discounts reach substantial fractions of the input price. But caching is not free money: many providers price cache writes above base input, so the first request pays extra, and every hit is discounted input, not zero. The economics work when a prefix repeats enough that the hit-rate savings exceed the write overhead — which is a design property of the workload.

That design property is arrangeable: put the stable parts of the prompt — instructions, tools, reference documents — at the front, and the volatile parts — the specific question, the current turn — at the end. A prompt whose order flips per request defeats its own cache. The meter that matters is the hit rate: what fraction of input tokens were charged at the cache rate, visible in the usage object.

Primary sources: <https://platform.openai.com/docs/guides/prompt-caching> and <https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching>.

## Decision rules

- Measure the cache hit rate from the usage object, not from latency hints.
- Put stable content first and volatile content last; the cache is a prefix.
- Account for cache-write costs above base input before declaring a saving.
- Confirm the lifetime of cache entries against the gaps between your requests.
- Compute the break-even: N hits at the discounted rate against the write overhead.
- Re-check hit rates after any prompt change; reordering can silently zero the cache.

## Procedure

1. Identify the stable and volatile parts of the workload's prompts.
2. Restructure so stability is a strict prefix.
3. Read the usage object's cache fields across a representative window.
4. Compute hit rate and dollars saved at the dated rates.
5. Compare against the write overhead the same window paid.
6. Record the break-even and re-check after prompt changes.

## Anti-patterns

- Assuming a cache hit because latency felt lower.
- Timestamps or unique IDs at the top of the prompt, defeating the prefix.
- Caching prompts that never repeat; the write overhead is pure loss.
- Quoting the headline discount without the local hit rate.
- Forgetting that a model or provider change resets cache behaviour entirely.

## Done checklist

- [ ] Stable-first restructuring done.
- [ ] Hit rate measured from usage fields.
- [ ] Write overhead recorded in dollars.
- [ ] Break-even computed.
- [ ] Entry lifetime checked against request gaps.
- [ ] Prompt-change re-check in place.

## Sources

- Prompt caching guide: <https://platform.openai.com/docs/guides/prompt-caching>
- Prompt caching mechanics: <https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching>
- Pricing table with cache rates: <https://docs.anthropic.com/en/docs/about-claude/pricing>

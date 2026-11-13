---
name: pricing-anatomy
domain: prompt-engineering/pricing-anatomy
trigger: "Reading a model API pricing page as a design input."
anti_trigger: "Not for recommending a provider, and not for request-packing."
scope: "Reading a pricing page: input, cached input, output, and the shape of a request."
status: seedling
---

# Pricing anatomy

## Standard

A pricing page is a table of three separate meters. Input tokens are priced per million consumed; output tokens are priced per million generated, typically at a multiple of input; and cached input tokens carry a heavily discounted rate that applies only when a prefix is reused. Some providers add cache-write rates that sit slightly above base input, making the first write cost more and every later hit cost far less.

The design consequence is that a request's cost is its shape, not its size. A short prompt with a long answer costs more than a long prompt with a short one at the same total token count, because output is the expensive meter. Reading a pricing page ends with three numbers recorded per model tier: input rate, cached rate, and the output-to-input ratio — and every later decision uses those ratios rather than headline prices.

Primary sources: <https://docs.anthropic.com/en/docs/about-claude/pricing> and <https://openai.com/api/pricing/>.

## Decision rules

- Record input, cached-input, and output rates per model tier, with the date read.
- Compute the output-to-input ratio per tier; it drives format decisions.
- Treat any quoted price as evidence with a date, never as a constant.
- Compare tiers by ratio (tier B costs n times tier A), not by absolute dollars.
- Check for cache-write pricing above base input before assuming caching always wins.
- Note per-tier context limits alongside prices: cost and capacity are one table.

## Procedure

1. Fetch the provider's pricing page and record the date.
2. Tabulate input, cached-input, cache-write, and output rates per tier.
3. Compute the output-to-input ratio per tier.
4. Note which tiers support caching and batching at all.
5. Record context windows beside prices.
6. Store the table as the dated input to every later leaf's arithmetic.

## Anti-patterns

- Quoting a price from memory as if current.
- Comparing models by input rate alone when output dominates the bill.
- Assuming cache hits are free; they are discounted input, not zero.
- Mixing tiers in one average; ratios matter per tier.
- Ignoring that some features are priced outside the table (tools, attachments).

## Done checklist

- [ ] Rates tabulated per tier with date.
- [ ] Output-to-input ratio computed.
- [ ] Cache and batch support noted per tier.
- [ ] Context limits recorded beside prices.
- [ ] Prices marked as dated evidence.
- [ ] Table stored as the reference input.

## Sources

- Model pricing tables: <https://docs.anthropic.com/en/docs/about-claude/pricing>
- API pricing overview: <https://openai.com/api/pricing/>
- Feature pricing context: <https://docs.anthropic.com/en/docs/about-claude/models/overview>

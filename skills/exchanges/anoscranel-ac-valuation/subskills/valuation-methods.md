---
name: valuation-methods
domain: investing/valuation-methods
trigger: "Choosing which valuation method the business actually supports."
anti_trigger: "Not for computing the valuation itself, and not for comparing methods as a score."
scope: "Discounted cash flow, multiples, asset-based, and sum-of-parts, and when each is the honest choice."
status: seedling
---

# Valuation methods

## Standard

Four methods cover most businesses, and each assumes something different. Discounted cash flow assumes the business has forecastable cash flows. Multiples assume a comparable set exists and is priced correctly. Asset-based valuation assumes the value is in what the company owns. Sum-of-parts assumes the segments are worth more separately than together.

The honest choice follows from the business, not from preference. A pre-revenue biotech has no cash flows to discount and no useful multiple; its value sits in pipeline assets and probabilities. A mature utility is well served by cash flow. A conglomerate demands sum-of-parts because its average multiple hides both good and bad segments.

Primary sources: <https://pages.stern.nyu.edu/~adamodar/> and <https://www.sec.gov/edgar/search/>.

## Decision rules

- State which method fits and why the others do not, before computing anything.
- Where two methods are defensible, compute both and explain the divergence.
- Asset-based valuation is used when the business is asset-heavy or in liquidation; not as a floor for a going concern without justification.
- Sum-of-parts requires segment disclosure; without it, record the method as unavailable.
- Never average two methods into a single number to hide the disagreement.
- A method that requires assumptions you cannot defend is the wrong method.

## Procedure

1. Classify the business: cash-generating, asset-heavy, segment-diverse, or pre-revenue.
2. Match the class to a primary method and a secondary check.
3. Record why the remaining methods were rejected.
4. Compute the primary and the secondary.
5. Write the divergence and what it implies.
6. Record the method choice in the valuation record.

## Anti-patterns

- Using DCF for a business with no forecastable revenue because it looks rigorous.
- Choosing comparables after seeing which set flatters the answer.
- Treating asset value as a floor for a business that is burning cash.
- Averaging methods to produce false confidence.
- Applying a method because a template exists.

## Done checklist

- [ ] Business classified.
- [ ] Primary and secondary methods chosen with reasons.
- [ ] Rejected methods recorded.
- [ ] Both methods computed.
- [ ] Divergence explained.
- [ ] Method choice recorded.

## Sources

- Valuation reference material and data sets: <https://pages.stern.nyu.edu/~adamodar/>
- Full-text filing search for segment and asset data: <https://www.sec.gov/edgar/search/>
- Investor education on valuation concepts: <https://www.investor.gov/introduction-investing>

Method choice is itself an assumption, and it deserves the same scrutiny as a growth rate. Write down what would have to be true for the rejected method to be the better one; if that condition is easy to state, the choice is not obvious and the record should say so.


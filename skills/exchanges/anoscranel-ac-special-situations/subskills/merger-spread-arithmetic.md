---
name: merger-spread-arithmetic
domain: investing/merger-spread-arithmetic
trigger: "Computing a merger spread and what it pays for the risk taken."
anti_trigger: "Not for predicting whether a deal closes, and not for the investment case."
scope: "Gross and net spread, annualisation, and the break scenario."
status: seedling
---

# Merger spread arithmetic

## Standard

A merger spread is the difference between the target's current price and the value of the consideration offered, expressed as a percentage of the target price. For a cash deal, the consideration is a number and the spread is the discount to it; for a stock deal, the consideration moves with the acquirer's price, so the spread is a relationship between two securities rather than a discount to a fixed amount.

Annualising the spread is what makes it comparable: a five percent spread over three months is a different proposition from the same spread over a year. The break case is the essential companion, because a deal that fails typically returns the target to its pre-announcement price, and the loss in that scenario is usually several times the spread being earned.

Primary sources: <https://www.sec.gov/edgar/search/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the consideration, its form, and whether it is cash, stock, or a combination.
- Record the target price and the gross spread as a percentage.
- Record the expected closing date and annualise the spread over that period.
- Record the pre-announcement price and the loss in the break case.
- Record the break-even probability implied by the spread and the break loss.
- For a stock deal, record the hedge ratio and the acquirer's price exposure.

## Procedure

1. Record the offer terms from the filing.
2. Compute the gross spread and its annualisation.
3. Record the pre-announcement price.
4. Compute the break-case loss.
5. Derive the implied probability of completion.
6. Write the spread with its break case beside it.

## Anti-patterns

- Quoting a spread without annualising it.
- Ignoring the break-case loss, which is usually larger than the spread.
- Treating a stock deal's spread as fixed when the acquirer moves.
- Using the announcement price when the pre-announcement price drives the break.
- Assuming the implied probability is the market's forecast rather than a price.

## Done checklist

- [ ] Consideration and form recorded.
- [ ] Gross spread and annualisation recorded.
- [ ] Pre-announcement price recorded.
- [ ] Break-case loss computed.
- [ ] Implied probability derived.
- [ ] Hedge ratio recorded for stock deals.

The implied probability deserves a caution of its own: it assumes the break case is a single known number, and in practice the target after a failed deal can trade above or below its pre-announcement price depending on what emerged during the process, so the derived probability is a summary of the market's pricing rather than a measurement of the deal's prospects.


## Sources

- Merger filings and deal terms: <https://www.sec.gov/edgar/search/>
- Disclosure framework: <https://www.sec.gov/investor>
- Investor education on event risk: <https://www.investor.gov/introduction-investing>

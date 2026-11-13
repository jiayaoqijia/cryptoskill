---
name: cost-stack
domain: investing/cost-stack
trigger: "Computing the total cost of holding a fund, not just its expense ratio."
anti_trigger: "Not for predicting returns, and not for fund recommendations."
scope: "Expense ratio plus spreads, commissions, and taxes: the total cost of holding a fund."
status: seedling
---

# Cost stack

## Standard

The expense ratio is the advertised cost, and it is rarely the whole cost. Holding a fund also costs the bid-ask spread at purchase and sale, any commission the platform charges, the tax on distributions, and — for funds trading at a premium or discount — the difference between the price paid and the value of the underlying assets.

The total cost matters because it compounds against the investor and because it is the most predictable thing about a fund. Two funds with the same exposure and a twenty-basis-point difference in total cost diverge by a fifth of a percent per year, which over decades is a meaningful share of the outcome and requires no forecast to compare.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://www.sec.gov/investor>.

## Decision rules

- Record the expense ratio with its date and whether it includes waivers.
- Add the observed spread, expressed in basis points, at a stated trade size.
- Add any platform commission or custody fee.
- Note the tax treatment of distributions, and the drag it implies.
- Sum the components into a total cost figure with the assumptions stated.
- Compare funds on the total, not on the headline expense ratio alone.

## Procedure

1. Pull the expense ratio and note any waiver and its expiry.
2. Measure or look up the typical spread at the intended trade size.
3. Add platform and custody costs where applicable.
4. Estimate the tax drag from distribution history.
5. Sum into a total cost, stated in basis points per year.
6. Record every component with its date and source.

## Anti-patterns

- Comparing expense ratios alone.
- Using a spread measured at a size you will never trade.
- Ignoring waiver expiries.
- Treating tax as outside the fund decision.
- Quoting costs without dates.

## Done checklist

- [ ] Expense ratio recorded with waiver status and date.
- [ ] Spread measured or looked up at the intended size.
- [ ] Platform and custody costs added where relevant.
- [ ] Tax drag estimated.
- [ ] Total cost summed with assumptions.
- [ ] Comparison made on the total.

## Sources

- Investor education on fund costs: <https://www.investor.gov/introduction-investing>
- Fund disclosure context: <https://www.sec.gov/investor>
- Market data for spreads: <https://fred.stlouisfed.org/>

The comparison is most useful when it is put in years: a twenty-basis-point difference in total cost, compounded over a twenty-year holding period, is a visible fraction of the ending balance, and it requires no forecast to state. Writing the arithmetic makes the otherwise abstract basis points into a decision.

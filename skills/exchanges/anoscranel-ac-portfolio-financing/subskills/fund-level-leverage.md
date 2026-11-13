---
name: fund-level-leverage
domain: investing/fund-level-leverage
trigger: "Measuring the leverage inside a fund and what it costs."
anti_trigger: "Not for the allocation decision, and not for predicting returns."
scope: "Leverage at the vehicle, its cost, and its covenant."
status: seedling
---

# Fund-level leverage

## Standard

Leverage at the fund level is borrowing by the vehicle rather than by the assets it owns. It appears as a subscription line, a NAV facility, or debt at a holding company, and its effect is to raise the fund's exposure without changing the investor's commitment. The investor's return is levered whether or not the investor chose leverage.

Measuring it means looking through the structure to the borrowings at each layer. A fund that reports asset-level leverage but omits a facility at the holding company is reporting a partial figure, and the difference matters most in a decline, when the covenant bites at the level nobody was watching.

Primary sources: <https://www.federalreserve.gov/> and <https://www.sec.gov/investor>.

## Decision rules

- Record every borrowing at the fund and holding-company level.
- Record the ratio of total debt to net asset value at each layer.
- Record the covenants, their metrics, and their test frequency.
- Record the cost of each facility and its maturity.
- Record the priority of each claim in the waterfall.
- Compute the combined leverage and the decline that would breach the tightest covenant.

## Procedure

1. Map the structure and the borrowing entities.
2. Record debt at each layer and the ratios.
3. Record covenants and their metrics.
4. Record cost and maturity.
5. Compute combined leverage.
6. Test the decline that breaches the tightest covenant.

## Anti-patterns

- Reporting leverage at one layer and calling it the fund's.
- Ignoring a holding-company facility.
- Assuming a covenant is tested on the reported NAV.
- Overlooking maturity concentration across facilities.
- Comparing funds on reported leverage without the look-through.

## Done checklist

- [ ] Borrowing entities mapped.
- [ ] Debt and ratios recorded.
- [ ] Covenants recorded.
- [ ] Cost and maturity recorded.
- [ ] Combined leverage computed.
- [ ] Breach decline tested.

The maturity profile is the constraint that binds in practice: several facilities maturing in the same period across different funds turns a set of individually manageable borrowings into a collective refinancing need, and refinancing appetite at that moment depends on markets rather than on the assets. Recording maturities by year across the programme is what exposes the concentration.


The waterfall position of each facility decides who absorbs a shortfall: senior debt at the holding company ranks ahead of the fund's own obligations, so a decline that impairs the vehicle reaches the investor before it reaches the lender, and the order rather than the total is what determines the recovery.


## Sources

- Fund leverage disclosure: <https://www.sec.gov/investor>
- Credit conditions and leverage: <https://www.federalreserve.gov/>
- Analysis standards: <https://www.cfainstitute.org/>

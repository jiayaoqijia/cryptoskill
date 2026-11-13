---
name: dcf-construction
domain: investing/dcf-construction
trigger: "Building a discounted cash-flow model with defensible assumptions."
anti_trigger: "Not for picking the discount rate in isolation, and not for terminal-value debate."
scope: "Forecast horizon, cash-flow definition, discount rate, and terminal value, built with assumption discipline."
status: seedling
---

# DCF construction

## Standard

A discounted cash-flow model is five decisions and a spreadsheet. The decisions are the forecast horizon, the cash-flow definition, the growth path within the horizon, the discount rate, and the terminal value. Everything else is arithmetic. Models fail when the decisions are implicit — when the horizon is whatever the template said, the cash flow is "free cash flow" undefined, and the terminal value is a growth rate chosen to make the answer look reasonable.

The discipline is to write the five decisions down before building, and to keep the model simple enough that a reader can trace every cell back to an assumption.

Primary sources: <https://pages.stern.nyu.edu/~adamodar/> and <https://www.sec.gov/edgar/search/>.

## Decision rules

- Horizon matches the period over which the business has a competitive advantage; beyond that, terminal assumptions dominate anyway.
- Cash flow is defined explicitly: operating cash flow less capex, adjusted for working capital, with the adjustment stated.
- Revenue growth in the horizon is anchored to history and to a stated market view, not to a round number.
- Margins converge toward a level the competitive analysis supports, not toward the current peak.
- Every assumption is a named cell with a source or a stated judgement.
- If the model needs more than a dozen assumptions to work, the business is not understood well enough.

## Procedure

1. Write the five decisions in one paragraph before opening a spreadsheet.
2. Build the revenue path from a stated driver (volume, price, or segment growth).
3. Build margins from the cost structure, converging to a stated steady state.
4. Derive cash flow with the stated definition.
5. Discount at the rate from the discount-rate leaf, with the basis recorded.
6. Add the terminal value with its assumption stated separately.
7. Record every assumption in a table with source or judgement.

## Anti-patterns

- Using a template's defaults as assumptions.
- Letting margins expand every year to reach a desired answer.
- Defining free cash flow differently from the source statements without saying so.
- Hiding the terminal value inside the forecast.
- Building a model too complex to audit.

## Done checklist

- [ ] Five decisions written before modelling.
- [ ] Revenue path built from named drivers.
- [ ] Margins converge to a supported steady state.
- [ ] Cash-flow definition stated.
- [ ] Discount rate basis recorded.
- [ ] Terminal value stated separately with its assumption.
- [ ] Assumption table with source or judgement.

## Sources

- Valuation reference material and data sets: <https://pages.stern.nyu.edu/~adamodar/>
- Full-text filing search for historical financials: <https://www.sec.gov/edgar/search/>
- Investor education on cash-flow analysis: <https://www.investor.gov/introduction-investing>

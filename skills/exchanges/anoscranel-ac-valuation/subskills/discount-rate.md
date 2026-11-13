---
name: discount-rate
domain: investing/discount-rate
trigger: "Estimating the cost of capital used to discount a valuation."
anti_trigger: "Not for choosing a terminal growth rate, and not for market timing."
scope: "Cost of capital, risk-free rate, equity premium, and the sensitivity that follows from beta."
status: seedling
---

# Discount rate

## Standard

The discount rate is the return the capital could earn elsewhere at comparable risk. Get it wrong and every downstream number moves: a two-percentage-point difference in the discount rate changes a long-duration valuation by a third or more. The honest construction is a risk-free rate plus a risk premium scaled by the company's sensitivity to the market, with explicit adjustments for size, leverage, and country where they are justified.

The rate is not a place for false precision. A range with a stated midpoint tells the reader what the analysis knows; a single number to two decimal places tells them the analyst has mistaken arithmetic for evidence.

Primary sources: <https://pages.stern.nyu.edu/~adamodar/> and <https://fred.stlouisfed.org/>.

## Decision rules

- The risk-free rate matches the currency and the duration of the cash flows; a long-duration valuation uses a long-duration government rate.
- The equity risk premium is taken from a stated source and date, not from memory.
- Beta comes from a stated estimation window; where the company's history is short, a peer or industry beta is used and labelled.
- Leverage adjustments use the target capital structure, not the current one, where they differ materially.
- Country risk is added only when the cash flows are exposed to it, and the amount is stated.
- The rate is reported as a range with a midpoint; the sensitivity of the value to the rate is shown.

## Procedure

1. Select the risk-free rate with the currency and duration matched, and record the source and date.
2. Select the equity risk premium with its source and date.
3. Estimate beta with a stated window and method, or borrow an industry beta and label it.
4. Adjust for size, leverage, and country only with stated reasons.
5. Compute the range and midpoint.
6. Show the value sensitivity to the rate plus or minus one percentage point.
7. Record every input with source and date.

## Anti-patterns

- Using a short-duration rate for long-duration cash flows.
- Taking the equity premium from an old memory or a presentation.
- Reporting beta without the estimation window.
- Adding country risk to a company with no exposure to the country.
- Hiding a high discount rate to make a valuation conservative by construction.

## Done checklist

- [ ] Risk-free rate matched to currency and duration, with source and date.
- [ ] Equity risk premium sourced and dated.
- [ ] Beta estimated with window and method, or industry beta labelled.
- [ ] Size, leverage, and country adjustments justified or omitted.
- [ ] Range and midpoint reported.
- [ ] Sensitivity to the rate shown.

## Sources

- Cost-of-capital reference material and data: <https://pages.stern.nyu.edu/~adamodar/>
- Interest-rate data: <https://fred.stlouisfed.org/>
- Full-text filing search for capital structure: <https://www.sec.gov/edgar/search/>

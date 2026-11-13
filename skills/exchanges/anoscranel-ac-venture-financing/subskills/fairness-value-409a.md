---
name: fairness-value-409a
domain: investing/fairness-value-409a
trigger: "Understanding the internal valuation of common stock and option strikes."
anti_trigger: "Not for tax advice, and not for the company's enterprise valuation."
scope: "The internal valuation of common stock and option strike prices."
status: seedling
---

# Fairness value and 409A

## Standard

A 409A valuation is the independent appraisal of a private company's common stock that sets the price employees pay when they exercise options. In the United States, granting options at a strike below the appraised fair market value creates an immediate tax event on the discount — a penalty-laden event the appraisal exists to prevent. The appraisal therefore prices the option, and the option's economics for every future employee rest on it.

The method matters because common stock in a venture-backed company has no market price, so the appraisal deducts the value of the preference stack and the likelihood-weighted effects of the other classes' superior rights from the enterprise value. As rounds progress, each new preferred class adds to the deductions, which is why successive 409A appraisals can show common prices that move less than the round valuations suggest — the preferred stack's claims grow alongside the headline. An appraisal is a dated opinion with assumptions, not a market fact, and its method is as visible in its assumptions as in its output.

Primary sources: <https://www.irs.gov/> and <https://en.wikipedia.org/wiki/Business_valuation>.

## Decision rules

- Record the appraisal's date, provider, and the common price per share it set.
- Record the method and its key assumptions: comparable companies, hypothesis of sale, or an income approach.
- Record how each class's rights — preference, participation, control — entered the deduction from enterprise value.
- Note whether subsequent rounds occurring after the appraisal date require a fresh valuation before new grants.
- Track how the appraisal's common price relates to the preferred price in each round.
- Record the allocation of the enterprise value across classes in the appraisal and the assumptions behind it.

## Procedure

1. Obtain the current appraisal with its date and price per share.
2. Extract the method and the discount/option-pricing assumptions applied to common.
3. Trace how the preference stack entered the value determination.
4. Compare with the prior appraisal and with the round valuations between.
5. Verify whether any material event since the appraisal requires a refresh before new grants.
6. Write the summary with the price, its basis, and its date.

## Anti-patterns

- Treating the appraised price as a stable fact rather than a dated, assumption-laden opinion.
- Using the 409A price as the company's enterprise valuation read sideways.
- Assuming the common price scales with headline valuations.
- Ignoring the obligations created by granting below fair market value.
- Treating an expired or stale appraisal as sufficient for new grants.

## Done checklist

- [ ] Price, provider, and date recorded.
- [ ] Method and assumptions extracted.
- [ ] Class-rights treatment in the deduction traced.
- [ ] Compared with the prior appraisal and round prices.
- [ ] Refresh triggers checked.
- [ ] Summary written with the basis visible.

## Sources

- Tax administration guidance on equity valuation: <https://www.irs.gov/>
- Valuation standards and methodology: <https://www.nacva.com/>
- Stock-based compensation accounting: <https://www.fasb.org/>

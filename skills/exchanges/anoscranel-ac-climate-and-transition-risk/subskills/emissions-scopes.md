---
name: emissions-scopes
domain: investing/emissions-scopes
trigger: "Reading an emissions figure and knowing what it counts."
anti_trigger: "Not for scoring a company's climate performance, and not for valuation."
scope: "Scope 1, 2, and 3, what each counts, and where double counting lives."
status: seedling
---

# Emissions scopes

## Standard

Scope 1 counts emissions a company produces directly: combustion on site, process emissions, and its own vehicles. Scope 2 counts the emissions embodied in purchased electricity and heat, and it can be computed on a location basis, using the grid average, or a market basis, using the contracts the company has signed. Scope 3 counts everything else in the value chain, upstream and downstream, and it is usually the largest and least certain of the three.

The scopes are not additive across companies. A tonne emitted by a supplier appears in that supplier's scope 1 and in its customer's scope 3, so summing scope 1, 2 and 3 across a portfolio double counts the same tonne many times. Any aggregate that does so is measuring economic activity through an emissions lens rather than measuring emissions, and the distinction matters whenever a total is quoted.

Primary sources: <https://www.sec.gov/investor> and <https://www.bis.org/>.

## Decision rules

- Record which scopes are reported, on which basis, and for which year.
- For scope 2, record whether the figure is location-based or market-based.
- For scope 3, record which of the categories are included and which are estimated.
- Record the estimation method and the vendor or model behind any modelled figure.
- Record the intensity denominator, since per-revenue and per-unit figures rank differently.
- Never sum scopes across companies without stating the double counting.

## Procedure

1. Record the reporting year and the scopes covered.
2. Record the scope 2 basis.
3. Record scope 3 categories and their estimation status.
4. Record the intensity denominator used.
5. Note any restatement from a prior year.
6. Write the emissions summary with the comparability limits.

## Anti-patterns

- Summing scopes across a portfolio as if they were additive.
- Comparing a location-based figure with a market-based one.
- Treating a modelled scope 3 estimate as measured data.
- Comparing companies on different intensity denominators.
- Ignoring a restatement that changed the baseline.

## Done checklist

- [ ] Year and scopes recorded.
- [ ] Scope 2 basis recorded.
- [ ] Scope 3 categories and estimation recorded.
- [ ] Intensity denominator recorded.
- [ ] Restatements noted.
- [ ] Comparability limits stated.

The intensity denominator decides most comparisons: a per-revenue figure favours high-margin businesses and a per-unit figure favours those with small output, so two companies can rank in opposite orders depending on which is used. Recording both, rather than choosing one, is what prevents an intensity comparison from becoming an argument about the denominator.


## Sources

- Climate disclosure requirements: <https://www.sec.gov/investor>
- Financial stability analysis of climate risk: <https://www.bis.org/>
- Emissions accounting standards: <https://www.cfainstitute.org/>

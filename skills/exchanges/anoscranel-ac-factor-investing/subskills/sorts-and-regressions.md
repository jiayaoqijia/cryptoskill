---
name: sorts-and-regressions
domain: investing/sorts-and-regressions
trigger: "Choosing between a portfolio sort and a cross-sectional regression."
anti_trigger: "Not for predicting returns, and not for backtest validation."
scope: "Portfolio sorts versus cross-sectional regression, and what each shows."
status: seedling
---

# Sorts and regressions

## Standard

A portfolio sort builds groups from the factor and measures the returns of those groups, which produces a return series that can be traded and evaluated. A cross-sectional regression estimates the relationship between the factor score and returns across securities, which produces a coefficient and a t-statistic rather than a portfolio.

The two answer different questions. The sort answers what a portfolio built on the factor would have returned, including the effect of the weighting and the rebalancing, and it is the closer approximation to an implementable strategy. The regression answers whether the characteristic is priced across the cross-section, controlling for other characteristics, and it is the closer approximation to a test of the hypothesis. Reporting one and describing it as the other is a common error.

Primary sources: <https://www.nber.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record which method is used and which question it answers.
- For a sort, record the number of groups, the breakpoints, and the weighting.
- For a regression, record the specification, the controls, and the standard errors.
- Record whether the regression includes other factors, which changes the coefficient's meaning.
- Record the period and the rebalancing used in either method.
- Record the results of both where the conclusion depends on the pairing.

## Procedure

1. State the question the test is answering.
2. Choose the method matching the question.
3. Record the parameters: groups or specification.
4. Run the test and record the output.
5. Where possible, run the other method as a check.
6. Write the result with the method named.

## Anti-patterns

- Reporting a regression coefficient as if it were a portfolio return.
- Running a sort without recording the breakpoints.
- A regression without controls, interpreting the coefficient as a pure factor effect.
- Using overlapping periods without adjusting the standard errors.
- Presenting one method's result as confirmation of the other's.

## Done checklist

- [ ] Question stated.
- [ ] Method chosen and justified.
- [ ] Parameters recorded.
- [ ] Output recorded.
- [ ] Cross-check run where feasible.
- [ ] Result labelled with its method.

The breakpoints deserve particular attention because they determine the factor's identity at the extremes: a decile sort whose top group contains twenty names is a concentrated portfolio rather than a broad exposure, and a quintile sort of the same universe is a different strategy with a different capacity, so the number of groups is a choice about how much idiosyncratic risk the factor carries.


## Sources

- Asset pricing research methods: <https://www.nber.org/>
- Investor education on factor evidence: <https://www.investor.gov/introduction-investing>
- Data sources for cross-sectional tests: <https://fred.stlouisfed.org/>

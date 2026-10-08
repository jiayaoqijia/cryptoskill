---
name: attribute-a-kpi-change-without-a-control
description: Use when no randomised control exists and a change must be attributed. Builds a comparison series and checks parallel pre-trends before claiming an effect.
---

# Attribute a KPI Change Without a Control

No experiment means no randomisation, so attribution rests on an assumption you must state and test. Without a control series, "the launch caused the jump" is a correlation with a graph attached.

## Procedure

1. Build a control: a comparable region, cohort, or product that did not get the change, or a synthetic control from donor units.
2. Test the identifying assumption — parallel trends. Plot treated and control before the change; they must move together in the pre-period.
3. Estimate a difference-in-differences with time and group fixed effects, and cluster the standard errors at the level of treatment assignment:
   ```python
   import statsmodels.formula.api as smf
   m = smf.ols('y ~ treat*post + C(unit) + C(period)', data=df).fit(
           cov_type='cluster', cov_kwds={'groups': df['unit']})
   print(m.params['treat:post'], m.pvalues['treat:post'])
   ```
4. Run placebo tests: move the change date earlier and confirm the effect disappears; use untreated units as fake treated.
5. Check for coincident events in the same window (a marketing push, a competitor outage, a price change) that could carry the effect.
6. Report the estimate with the assumption attached and a link to the pre-trend plot.

## Pitfalls

- Without a pre-trend check, a DiD estimate is a number shaped by whatever else moved.
- Choosing the control after seeing the result ("the one region with the pattern") invalidates the comparison.
- A treated unit that is also the biggest ad buyer makes the launch and the spend indistinguishable.
- Clustering at the wrong level understates the interval; cluster where treatment was assigned.
- A four-week post window is too short to rule out a seasonal explanation for a calendar-linked KPI.

## Verification

    python3 -c "import statsmodels.formula.api as smf; print('pre-trend: regress y on time per group; slopes must agree within their CIs')"
    # summarise treated vs control pre-period before quoting any post effect

Report: "DiD +2.3 users/day (95% CI 0.9 to 3.7, clustered by region); pre-trend parallel over 8 pre-weeks; placebo date shows no effect; marketing spend flat in the window."

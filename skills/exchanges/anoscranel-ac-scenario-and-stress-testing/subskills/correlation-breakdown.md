---
name: correlation-breakdown
domain: investing/correlation-breakdown
trigger: "Testing what happens when diversification stops working."
anti_trigger: "Not for predicting correlations, and not for portfolio construction."
scope: "Diversification that disappears exactly when it is needed."
status: seedling
---

# Correlation breakdown

## Standard

Correlations estimated over normal periods understate dependence in stress. Assets that usually move independently can converge when a common factor dominates: a liquidity event, a funding squeeze, or a broad risk-off move in which every holding is sold for the same reason. The diversification that the portfolio relied on then disappears at the moment it was meant to help.

The test is to revalue the portfolio under a correlation assumption of one for the assets that would plausibly converge, and to ask which holdings remain genuinely independent. The answer is usually a shorter list than the calm-period analysis suggests, and the assets that remain independent tend to be those with a different holder base or a different mechanism, rather than those with a low historical correlation.

Primary sources: <https://www.bis.org/> and <https://fred.stlouisfed.org/>.

## Decision rules

- Record the correlation matrix used in the base case and its estimation window.
- Identify the groupings that would plausibly converge under stress.
- Revalue with correlation set to one within each grouping.
- Record which holdings remain independent and why.
- Record the historical episodes where the convergence occurred.
- Record the effect on the portfolio's largest loss.

## Procedure

1. Record the base correlation matrix.
2. Identify convergence groupings by mechanism.
3. Revalue with within-group correlation at one.
4. Identify the survivors of the test.
5. Reference historical episodes.
6. Write the result and the assumption.

## Anti-patterns

- Using a correlation matrix estimated through a calm window as the stress case.
- Assuming all assets converge, which makes the test uninformative.
- Ignoring the mechanism that would cause convergence.
- Treating low historical correlation as structural independence.
- Reporting the stressed loss without the grouping assumption.

## Done checklist

- [ ] Base matrix recorded.
- [ ] Groupings identified with mechanism.
- [ ] Stressed revaluation done.
- [ ] Independents identified.
- [ ] Episodes referenced.
- [ ] Assumption recorded with the result.

A useful discipline is to name the common factor that would drive the convergence: a funding squeeze makes every leveraged holder a seller at once, a broad risk-off move makes every risk asset correlate, and a sector-specific shock makes only that sector converge. The grouping should follow the mechanism, since grouping by correlation alone reproduces the calm-period matrix the test exists to challenge.


Recording which holdings survived the test is the finding that matters, because the survivors are the portfolio's real diversifiers and the rest are, in stress, one position described several ways.


## Sources

- Correlation and stability analysis: <https://www.bis.org/>
- Correlation series: <https://fred.stlouisfed.org/>
- Investor education on diversification: <https://www.investor.gov/introduction-investing>

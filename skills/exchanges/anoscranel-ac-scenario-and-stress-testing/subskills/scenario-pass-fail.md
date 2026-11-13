---
name: scenario-pass-fail
domain: investing/scenario-pass-fail
trigger: "Setting the criterion a stress test is judged against."
anti_trigger: "Not for predicting outcomes, and not for portfolio construction."
scope: "The criterion set before the test, and what failure triggers."
status: seedling
---

# Scenario pass and fail

## Standard

A stress test without a pre-set criterion is a description rather than a test. The criterion states what result would constitute failure — a loss beyond a threshold, a collateral shortfall, a breach of a liquidity bucket — and it is set before the scenario is run, so that the result cannot be accommodated after the fact.

The criterion also determines what happens on failure. A test that fails and produces no action is a test that has been run for its own sake; connecting each failure to a specific response, decided in advance, is what makes the exercise operational. Where the response is discretionary, the record should name who decides and by when.

Primary sources: <https://www.bis.org/> and <https://osf.io/prereg/>.

## Decision rules

- Record the failure criterion in a specific metric with a number.
- Record the criterion's source: policy limit, contractual requirement, or internal tolerance.
- Set the criterion before running the scenario and date it.
- Record the response attached to failure: reduce, hedge, raise buffer, or escalate.
- Record who decides and the deadline for the decision.
- Record a pass as evidence about the assumptions as well as the portfolio.

## Procedure

1. State the criterion and its source.
2. Date it before the run.
3. Run the scenario.
4. Record pass or fail against the criterion.
5. Record the action attached to the result.
6. Name the decision owner and deadline.

## Anti-patterns

- Setting the threshold after seeing the result.
- A criterion expressed as a sentiment rather than a number.
- Failing a test without a defined action.
- Treating a pass as proof of safety rather than as evidence.
- Changing the criterion between reviews without recording the change.

## Done checklist

- [ ] Criterion stated with a number.
- [ ] Source recorded.
- [ ] Criterion dated before the run.
- [ ] Result recorded against it.
- [ ] Action attached.
- [ ] Owner and deadline named.

The criterion also needs a comparison set: a threshold expressed as an absolute loss says little without the portfolio's capital base, and the same currency figure is a pass for one balance sheet and a failure for another, so the criterion should be stated as a ratio as well as an amount.


## Sources

- Stress testing and governance standards: <https://www.bis.org/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Investor education on risk policy: <https://www.investor.gov/introduction-investing>

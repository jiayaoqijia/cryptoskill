---
name: reverse-stress-testing
domain: investing/reverse-stress-testing
trigger: "Identifying what would have to happen for the portfolio to fail."
anti_trigger: "Not for predicting the event, and not for portfolio construction."
scope: "Starting from failure and solving for the shock that causes it."
status: seedling
---

# Reverse stress testing

## Standard

A conventional stress test applies a shock and measures the outcome. A reverse stress test starts from an outcome the portfolio could not survive — a loss that breaches a threshold, a collateral shortfall, a redemption that cannot be met — and solves for the combination of moves that produces it. The output is a set of conditions rather than a loss figure.

The technique's value is that it cannot flatter. A forward test with a mild scenario will produce a survival, and the choice of scenario is where the flattery enters. A reverse test asks what would break the portfolio and then asks whether that combination is plausible, which puts the judgement where it belongs: on the plausibility of the breaking scenario rather than on the severity of an assumed shock.

Primary sources: <https://www.bis.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Define failure first: the threshold that constitutes it, in currency and in a specific metric.
- Record the solvers used: which variables were free and which were held fixed.
- Record the solution: the combination of moves that produces failure.
- Record the plausibility assessment of that combination, with historical references.
- Record the distance from current conditions to the breaking combination.
- Record the actions that would move the distance further away.

## Procedure

1. Define failure in a specific metric.
2. Choose the variables to solve over.
3. Solve for the combination producing failure.
4. Assess plausibility against history and mechanism.
5. Measure the distance from today.
6. Record the actions that increase the distance.

## Anti-patterns

- Applying a scenario and calling the result a reverse test.
- Defining failure vaguely, so no solution is identifiable.
- Solving over variables that cannot move independently.
- Assessing plausibility by intuition rather than reference.
- Treating an implausible solution as reassurance.

## Done checklist

- [ ] Failure defined in a metric.
- [ ] Variables recorded.
- [ ] Solution recorded.
- [ ] Plausibility assessed.
- [ ] Distance measured.
- [ ] Actions recorded.

The plausibility assessment is where the exercise either produces a finding or produces comfort: a breaking combination that requires several independent extremes to coincide is different from one that requires a single common move, and the number of independent conditions is a useful measure of how close the failure actually is.


## Sources

- Stress testing principles and practice: <https://www.bis.org/>
- Investor education on risk management: <https://www.investor.gov/introduction-investing>
- Market data for historical reference: <https://fred.stlouisfed.org/>

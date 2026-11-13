---
name: derisking-glide-path
domain: investing/derisking-glide-path
trigger: "Designing the path from a risky portfolio to a matched one."
anti_trigger: "Not for predicting funding improvements, and not for actuarial advice."
scope: "Glide-path design, funding triggers, and the cost of de-risking late."
status: seedling
---

# De-risking glide path

## Standard

A glide path is a schedule of allocation changes written in advance, moving the portfolio from return-seeking assets toward liability-matching assets as the funding ratio improves. Its value is that it removes the decision from the moment: a scheme that decides to de-risk after a good year tends to do so after the gain has already been given back, because the decision is taken emotionally and late.

Triggers make the path conditional rather than calendar-based. A funding-ratio trigger acts when the ratio crosses a level, which ties the de-risking to the outcome that justifies it. The design question is where to place the triggers and how much to move at each: too coarse and the improvement is not captured, too fine and the scheme de-risks on noise and pays transaction costs repeatedly.

Primary sources: <https://www.cfainstitute.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the current funding ratio and the target.
- Record each trigger level and the allocation change it causes.
- Record whether triggers are one-way or reversible.
- Record the transaction cost of each step.
- Record the liability-side assumption that the glide path depends on.
- Record what happens if the ratio falls after a step has been taken.

## Procedure

1. Record the starting ratio and the target.
2. Set trigger levels and the allocation step for each.
3. Decide whether steps are reversible.
4. Estimate the cost of each step.
5. Record the liability assumptions behind the path.
6. Write the path with its triggers and reversibility.

## Anti-patterns

- Setting a calendar-based path that ignores the funding ratio.
- Making triggers so fine that noise causes repeated de-risking.
- Assuming a step can be reversed at the same cost.
- Leaving the liability assumption implicit.
- Failing to revisit the path when the liability basis changes.

## Done checklist

- [ ] Starting ratio and target recorded.
- [ ] Triggers and steps recorded.
- [ ] Reversibility decided.
- [ ] Costs estimated.
- [ ] Liability assumptions recorded.
- [ ] Review trigger set.

A further design choice is what to do at the target: a glide path that ends at a fully matched portfolio leaves no return-seeking assets to close a residual deficit, so most paths stop short of full matching and hold a residual allocation, and the size of that residual is a decision about how much risk to keep rather than a technical default.

## Sources

- Investment management standards: <https://www.cfainstitute.org/>
- Interest-rate and policy data: <https://www.federalreserve.gov/>
- Rate series for scenario testing: <https://fred.stlouisfed.org/>

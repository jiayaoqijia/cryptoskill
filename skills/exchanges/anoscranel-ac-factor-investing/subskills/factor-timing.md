---
name: factor-timing
domain: investing/factor-timing
trigger: "Considering whether to change factor exposure based on conditions."
anti_trigger: "Not for forecasting factor returns, and not for allocation policy."
scope: "Why timing has a poor record, and what would be required to change that."
status: seedling
---

# Factor timing

## Standard

Factor timing means varying exposure to a factor based on a forecast of its relative return. The record of doing so is poor, and the reason is structural: the signals used to time factors are the same observable characteristics everyone else can see, so the forecast must add information beyond what is already priced. Valuation spreads and momentum are the two most-studied signals, and both have produced weak and unstable timing results.

The honest position is that timing requires a specific, testable reason why the signal predicts the factor's return, and that most reasons offered are narratives fitted after the fact. A position that states its timing signal, the evidence for it, and the conditions under which it would be abandoned is at least reviewable; one that changes exposure because the factor has underperformed is a form of performance chasing.

Primary sources: <https://www.nber.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the timing signal, its construction, and the data it uses.
- Record the evidence for the signal, including out-of-sample performance.
- Record the conditions under which the timing rule would be abandoned.
- Record the turnover the rule implies and its cost.
- Record whether the signal is already visible to other participants.
- Record the difference between a timing rule and a discretion to change exposure.

## Procedure

1. State the timing signal and its rationale.
2. Collect its evidence, separating in-sample from out-of-sample.
3. Assess the turnover and cost.
4. State the abandonment condition.
5. Compare the rule with a fixed exposure.
6. Write the case with its required evidence.

## Anti-patterns

- Changing exposure after underperformance and calling it timing.
- Presenting in-sample evidence as support.
- Ignoring the turnover cost of frequent changes.
- Using a signal everyone can compute and expecting it to add information.
- Abandoning the rule during the period it was designed for.

## Done checklist

- [ ] Signal and rationale recorded.
- [ ] Evidence separated by sample.
- [ ] Turnover and cost recorded.
- [ ] Abandonment condition stated.
- [ ] Compared with fixed exposure.
- [ ] Rule distinguished from discretion.

The comparison that keeps a timing decision honest is against the fixed exposure held through the same period: without it, a change that coincided with a recovery looks like skill, and the only way to distinguish the two is to have recorded what the unchanged portfolio would have done, which is the benchmark a timing rule must beat to justify its turnover.


## Sources

- Research on factor timing and predictability: <https://www.nber.org/>
- Investor education on factor strategies: <https://www.investor.gov/introduction-investing>
- Market data for signal construction: <https://fred.stlouisfed.org/>

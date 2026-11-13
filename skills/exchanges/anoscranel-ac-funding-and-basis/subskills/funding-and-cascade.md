---
name: funding-and-cascade
domain: crypto-trading/funding-and-cascade
trigger: "Examine the empirical relationship between funding rate settlement and liquidation cascades."
anti_trigger: "Assume funding settlement timestamps act as primary triggers for major market liquidations."
scope: "Evaluates empirical evidence on funding settlement non-clustering, branching ratios, and funding flips."
status: seedling
---

## Standard
A widespread misconception in crypto derivatives trading asserts that funding settlement timestamps trigger massive liquidation cascades due to abrupt margin balance deductions. Empirical analysis of large-scale execution datasets contradicts this folklore. Measured data across millions of liquidation events over extended observation windows demonstrates that liquidations do not cluster at funding settlement times; liquidation density shows a mild uniform distribution around funding intervals (approximately 1.038x baseline), whereas hourly peaks concentrate heavily during active trading session overlaps, particularly around 08:00 to 16:00 UTC and peak hourly concentrations near 18:00 UTC.

Cascades operate as subcritical cascading processes characterized by measured branching ratios (lambda hat) between 0.1 and 0.2 in flight. This subcritical dynamic means that liquidation events taper off rather than exploding exponentially from internal mechanics alone. Consequently, funding rate flips observed immediately following major liquidations are downstream consequences of forced position closures and collateral redistribution, not precursors or causes of the cascade itself. Analysts must separate mechanical folklore from empirically verified microstructure facts.

Primary sources for the claims in this step: <https://www.sciencedirect.com/science/article/pii/S154461232200183X> and <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3898231>.

## Decision rules
- Reject trading strategies predicated on the assumption that funding settlement hours spark liquidation cascades.
- Recognize post-cascade funding rate reversals as lagging consequences of position clearing rather than predictive signals.
- Evaluate liquidation risk based on order book depth, leverage concentration, and volatility rather than funding timers.
- Ground cascade forensic analysis in measured branching ratios and time-of-day volume distributions rather than market myths.
- Account for active trading session hours (such as UTC overlap windows) when assessing structural cascade vulnerability.

## Procedure
1. Review historical liquidation timestamps relative to upcoming and past funding settlement intervals.
2. Verify that liquidation clustering aligns with active trading hours rather than funding boundaries.
3. Measure the branching ratio and cascade propagation metrics during volatility spikes.
4. Assess funding rate sign and magnitude changes following large liquidation clearance events.
5. Record empirical findings in research logs, maintaining strict adherence to measured microstructure facts.

## Anti-patterns
- Timing stop-loss or entry executions around funding settlement hours under the belief of scheduled cascade triggers.
- Attributing sudden market crashes to funding payment deductions rather than forced deleveraging and spot selling.
- Treating post-cascade funding flips as leading indicators for secondary trend reversals.
- Relying on unverified folklore regarding derivative settlement mechanics instead of empirical research datasets.

## Done checklist
- [ ] Liquidation timing checked against funding settlement intervals.
- [ ] Time-of-day concentration and session overlap patterns evaluated.
- [ ] Branching ratio and cascade subcriticality confirmed from data.
- [ ] Funding rate flips analyzed as post-cascade consequences.
- [ ] Empirical findings documented without relying on market myths.

## Sources
- Academic Research on Cryptocurrency Liquidation Cascades and Market Microstructure: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3898231
- Empirical Study on Derivative Funding Settlements and Volatility Dynamics: https://www.sciencedirect.com/science/article/pii/S154461232200183X

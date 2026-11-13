---
name: risk-budget
domain: crypto-trading/risk-budget
trigger: "Setting account-level risk limits, maximum decision risk fraction, aggregate open risk cap, and drawdown reserve"
anti_trigger: "Adjusting risk limits during active drawdowns; trading without a pre-committed capital preservation ceiling"
scope: "The account-level budget: maximum fraction per decision, aggregate cap across correlated risk, and drawdown reserve"
status: seedling
---

# Risk Budget

## Standard

- **Kelly, "A New Interpretation of Information Rate" (1956)**: optimal long-term growth requires strict bounds on wager size relative to bankroll. <https://www.bell-labs.com/institute/about/history-bell-labs/bell-system-technical-journal/>
- **Bachelier, _Theory of Speculation_ (1900)**: price fluctuations follow probabilistic distributions where unconstrained variance leads to ruin. <https://archive.org/details/theoriadelaspecu00bach>
- **Markowitz, "Portfolio Selection" (1952)**: risk must be managed at the aggregate portfolio level by accounting for covariance. <https://www.jstor.org/stable/2975931>
- **Thorp, "The Kelly Criterion" (2008)**: practitioners must fractionalize theoretical bets to absorb estimation error. <https://www.e-m-h.org/Thorp08.pdf>
- ⚠️ Practitioner heuristic: desks set per-decision risk at 1% of total capital and aggregate open risk at 5%.

## Decision rules

1. The maximum fraction of capital risked on a single decision must be defined in writing before trading begins.
2. Aggregate open risk across active positions must be capped at a pre-committed multiple of single-decision risk.
3. A capital preservation reserve must be maintained untouched; breaching it halts trading.
4. Risk parameters are static constants during active cycles and can only be reviewed during scheduled audits.
5. Invalidation distance determines position size against the fixed risk dollar amount.
6. Correlated assets must be grouped into single risk buckets with aggregate caps.
7. ⚠️ House: exceeding the risk budget voids the session record.

## Procedure

1. Calculate total liquid capital available at the start of the period.
2. Multiply capital by the per-decision risk fraction to establish maximum dollar loss.
3. Establish the aggregate open risk cap by multiplying single-trade risk by maximum positions.
4. Segregate the drawdown reserve percentage into a separate accounting ledger.
5. Record all risk parameters in desk configuration files before opening positions.
6. Verify prior to every entry that calculated dollar risk matches the budget.
7. Conduct weekly audits comparing actual drawdowns against preservation reserves.

## Anti-patterns

- **Risk escalation after losses.** Increasing risk budget after losses to recover faster. Fix: reduce risk or halt trading.
- **Uncapped correlation.** Treating correlated positions as independent. Fix: group correlated assets and cap exposure.
- **Dynamic risk adjustment.** Altering risk parameters mid-trade. Fix: treat risk limits as inviolable.
- **Ignoring drawdown reserves.** Deploying reserves during high volatility. Fix: lock reserves behind separate administrative controls.

## Done checklist

- [ ] Per-decision risk fraction is defined in writing.
- [ ] Aggregate open risk cap is established and recorded.
- [ ] Drawdown reserve is segregated from active trading capital.
- [ ] Correlation groupings are defined for all active assets.
- [ ] Risk parameters remain static throughout the trading cycle.

## Sources

- Kelly, "A New Interpretation of Information Rate": <https://www.bell-labs.com/institute/about/history-bell-labs/bell-system-technical-journal/>
- Markowitz, "Portfolio Selection": <https://www.jstor.org/stable/2975931>
- Thorp, "The Kelly Criterion": <https://www.e-m-h.org/Thorp08.pdf>

⚠️ Gaps: non-linear liquidation risks in crypto markets require continuous dynamic adjustment of the risk fraction.

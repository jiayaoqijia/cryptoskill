---
name: drawdown-budgeting
domain: crypto-trading/drawdown-budgeting
trigger: "drawdown budget, recovery arithmetic, maximum drawdown, portfolio breach"
anti_trigger: "capital allocation, rebalancing, correlation regime"
scope: Managing maximum drawdown budgets, strategy combination, and recovery arithmetic.
status: seedling
---

# Drawdown Budgeting

## Standard

Drawdown budgeting establishes hard thresholds for acceptable capital contraction at both the individual strategy and total portfolio levels. Because recovery arithmetic is non-linear—recovering from a 50 percent portfolio drawdown requires a 100 percent gain, while recovering from an 80 percent drawdown requires a 400 percent gain—drawdown limits must be strictly enforced. Portfolio construction requires aggregating strategy-level drawdown potentials while accounting for simultaneous strategy failures driven by common market shocks. Maintaining strict drawdown boundaries prevents cumulative capital erosion and ensures that trading operations can survive severe market contractions without facing total account liquidation or irreversible capital impairment. Proper drawdown allocation safeguards long-term trading survivability.

Primary sources for the claims here: <https://www.cfainstitute.org/> and <https://www.iosco.org/>.

## Decision rules

- A maximum allowable portfolio drawdown limit must be defined prior to deploying capital, with mandatory risk reduction triggered upon approaching the limit.
- Individual strategies must operate within assigned drawdown sub-budgets that sum to less than or equal to the total portfolio drawdown limit.
- Hitting a strategy-level drawdown stop forces an immediate freeze and capital withdrawal from that strategy until a thorough structural review is completed.
- Position sizing and leverage across all active strategies must scale down dynamically as aggregate portfolio drawdown deepens toward critical thresholds.

## Procedure

1. Define the absolute maximum portfolio drawdown threshold compatible with risk tolerance mandates and capital preservation goals.
2. Allocate strategy drawdown sub-budgets based on historical strategy variance, expected tail behavior, and maximum historical loss profiles.
3. Compute recovery gain requirements for each drawdown milestone to ensure mathematical feasibility under realistic market return conditions.
4. Implement automated monitoring and alerting systems to track cumulative drawdowns in real time across all active accounts and trading venues.
5. Execute pre-planned risk curtailment protocols immediately upon breaching any strategy or portfolio drawdown threshold without discretionary delay.

## Anti-patterns

- Continuing to trade at full size after breaching soft drawdown limits in anticipation of an immediate market rebound.
- Failing to account for non-linear recovery arithmetic when sizing risk for high-volatility, leveraged crypto strategies.
- Setting strategy drawdown limits independently without evaluating cumulative portfolio impact during correlated stress events.

## Done checklist

- [ ] Maximum portfolio drawdown limit and strategy sub-budgets are formally established and documented.
- [ ] Automated monitoring and risk curtailment triggers are active across all trading accounts.
- [ ] Recovery gain requirements are documented for all potential drawdown tiers and risk brackets.

## Sources

- CFA Institute: https://www.cfainstitute.org/
- Financial Stability Board (FSB): https://www.fsb.org/
- International Organization of Securities Commissions (IOSCO): https://www.iosco.org/
- Bank for International Settlements (BIS): https://www.bis.org/

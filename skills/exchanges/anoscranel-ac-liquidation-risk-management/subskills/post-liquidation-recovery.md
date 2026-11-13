---
name: post-liquidation-recovery
domain: crypto-trading/post-liquidation-recovery
trigger: Use when executing post-liquidation forensic reviews, incident record creation, cooling-off periods, and restart protocols.
anti_trigger: Not for real-time margin monitoring, pre-trade leverage selection, or managing active hedge legs.
scope: What a liquidation did mechanically, the record it must produce, restart rules, and the prohibition on averaging down into a liquidation.
status: seedling
---

## Standard
A liquidation is a catastrophic mechanical failure of risk controls, resulting in forced position closure, liquidation penalty fees, and potential account wipeout. When a liquidation occurs, the risk engine automatically cancels open orders, liquidates remaining collateral at market rates through the bankruptcy engine, and charges liquidation clearance fees that exacerbate account drawdown. Post-liquidation recovery requires an immediate, objective forensic audit to document the exact mechanical failure sequence (price trigger, slippage, fee impact, collateral depletion). Strict restart rules must be enforced, including a mandatory cooling-off period and an absolute prohibition against averaging down or revenge trading immediately following a liquidation event. The incident must produce a formal trading record that updates risk parameters before any capital is redeployed.

Primary sources for the claims here: <https://www.binance.com/en/support/faq/futures-trading-fee-structure-360033544232> and <https://www.bybit.com/en/help-center/article/Liquidation-Process-Linear>.

## Decision rules
1. Impose a mandatory 24-hour trading freeze on any account that experiences a forced liquidation event to eliminate emotional revenge trading.
2. Prohibit averaging down, adding margin to a losing position, or reopening the same directional trade within 48 hours of liquidation.
3. Conduct a comprehensive forensic audit documenting exact slippage, maintenance margin failures, and trigger prices within 6 hours of the event.
4. Reduce baseline position sizing by 50% for the first ten trades executed following a post-liquidation restart.

## Procedure
1. Extract exchange execution logs, trade history, and liquidation penalty records immediately following the event.
2. Calculate the exact total financial loss, including position delta, funding fees, and liquidation clearance penalties.
3. Complete the post-liquidation forensic report detailing root causes (e.g., inadequate stop distance, sudden volatility spike, ignored margin warning).
4. Initiate the mandatory cooling-off period and lock trading permissions on the account.
5. Review and update risk management parameters and leverage limits in the trading playbook before restarting operations with reduced capital.

## Anti-patterns
- Attempting immediate revenge trading or averaging down into the same market direction to "win back" liquidated funds.
- Failing to conduct a forensic audit, dismissing the liquidation as "bad luck" rather than a mechanical risk failure.
- Restarting trading immediately at full size without a cooling-off period or parameter adjustments.
- Ignoring liquidation clearance fees when calculating actual trading capital depletion.

## Done checklist
- [ ] Mandatory cooling-off trading freeze initiated immediately upon liquidation.
- [ ] Exchange execution logs and liquidation clearance fees audited.
- [ ] Formal forensic report completed detailing mechanical failure root causes.
- [ ] Trading playbook risk parameters and leverage caps updated.
- [ ] Capital redeployment restricted to 50% reduced sizing for initial restart trades.

## Sources
- Binance Futures Liquidation Fee and Bankruptcy Rules: https://www.binance.com/en/support/faq/futures-trading-fee-structure-360033544232
- Bybit Liquidation Clearance and Insurance Fund Procedures: https://www.bybit.com/en/help-center/article/Liquidation-Process-Linear

---
name: rebalancing-and-drift
domain: crypto-trading/rebalancing-and-drift
trigger: "rebalancing rules, drift tolerance, rebalancing cost, slippage, funding fees"
anti_trigger: "capital allocation, concentration risk, portfolio review"
scope: Defining drift tolerances, rebalancing rules, and transaction cost impacts.
status: seedling
---

# Rebalancing And Drift

## Standard

Portfolio drift occurs when market price movements alter asset weights and strategy allocations away from their target parameters. While periodic rebalancing restores target risk profiles, executing rebalancing transactions in crypto markets incurs substantial friction costs, including exchange fees, slippage, and adverse funding rate impacts. Rebalancing rules must balance the necessity of maintaining risk discipline against the explicit transaction costs of trading out of drifted positions. Ignoring drift allows high-performing or volatile strategies to consume an unearned share of the risk budget, whereas excessive rebalancing degrades performance through constant fee attrition and market impact. Finding the optimal rebalancing frequency is vital for long-term portfolio efficiency and adherence to structural risk mandates across all operating venues. Consistent monitoring prevents silent risk creep and unbudgeted risk exposures across all accounts.

Primary sources for the claims here: <https://www.cfainstitute.org/> and <https://www.iosco.org/>.

## Decision rules

- Rebalancing must be triggered only when asset or strategy weights breach pre-defined percentage drift tolerance bands rather than on a rigid calendar schedule.
- Transaction costs, expected slippage, and immediate funding fee impacts must be calculated before executing any portfolio rebalancing trade.
- Rebalancing flows should prioritize natural rebalancing—directing new capital inflows toward underweight strategies—before executing direct liquidations.
- Emergency rebalancing is mandatory if a sudden market shock invalidates the baseline correlation or risk allocation structure across active venues.

## Procedure

1. Establish target weightings and allowable drift percentage bands for all portfolio strategies and underlying assets.
2. Monitor ongoing portfolio weight drift against established tolerance thresholds continuously in real time across all venues.
3. Evaluate rebalancing cost efficiency by comparing potential risk reduction against projected exchange fees, gas costs, and slippage.
4. Execute natural rebalancing using incoming deposits, fee accruals, or routine cash flows where feasible without market impact.
5. Execute direct rebalancing trades during high-liquidity market windows to minimize price impact if drift exceeds emergency limits.

## Anti-patterns

- Rebalancing too frequently, eroding portfolio returns through cumulative transaction fees and adverse market impact.
- Ignoring transaction costs, gas fees, and funding rate penalties during high-volatility rebalancing actions.
- Allowing extreme drift to persist past tolerance limits without intervention during calm market periods.

## Done checklist

- [ ] Target weightings and drift tolerance bands are established for all allocations.
- [ ] Cost-benefit analysis protocols are defined for executing rebalancing trades.
- [ ] Natural rebalancing procedures are prioritized over direct liquidation.

## Sources

- CFA Institute: https://www.cfainstitute.org/
- Bank for International Settlements (BIS): https://www.bis.org/
- Financial Stability Board (FSB): https://www.fsb.org/
- International Organization of Securities Commissions (IOSCO): https://www.iosco.org/

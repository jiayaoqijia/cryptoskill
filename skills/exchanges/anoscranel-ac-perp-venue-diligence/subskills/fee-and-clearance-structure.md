---
name: "fee-and-clearance-structure"
domain: "crypto-trading/fee-and-clearance-structure"
trigger: "When asked about exchange fees, maker/taker schedules, funding rates, liquidation penalties, or tax cost wrappers"
anti_trigger: "When evaluating raw order book depth or API endpoint latency"
scope: "Maker/taker fees, funding mechanics, liquidation clearance penalties, and statutory tax cost wrappers."
status: "seedling"
---

# Fee and Clearance Structure

## Standard

- **Bybit V5 API & Fee Documentation**: Perpetual swap execution costs depend on tiered maker/taker schedules, periodic funding payments exchanged between longs and shorts every 8 hours (or hourly), and liquidation clearance penalties assessed upon forced closure. <https://www.bybit.com/en/help-center/article/Bybit-Fee-Structureen/help-center/article/Bybit-Fee-Structure>
- **Delta Exchange India & Tax Compliance Framework**: Derivatives trading costs must incorporate statutory tax wrappers, such as Goods and Services Tax (GST) applied to platform fees (e.g., 18% GST on exchange fees raising effective taker costs from 0.05% to 0.059%), alongside jurisdictional income characterization (e.g., business income or capital gains under statutory frameworks rather than flat TDS withholding). <https://www.delta.exchange/>
- ⚠️ House standard: liquidation clearance fees charged directly to the liquidated account act as severe cascade amplifiers, transferring margin balances to the insurance fund or liquidator pool and accelerating adjacent position failures.

## Decision rules

1. Aggregate the complete cost stack into an all-in percentage drag: base taker fee + expected funding rate drag over holding horizon + liquidation clearance penalty probability-weighted.
2. Verify whether liquidation clearance fees are rebated to the insurance fund or captured as platform revenue, noting that aggressive penalty structures (>50 bps) intensify cascading liquidations during high volatility.
3. Incorporate statutory tax wrappers and jurisdictional indirect taxes (such as GST on brokerage fees) into the net P&L model before establishing position sizing limits.
4. Check funding rate historical volatility and skew across bullish and bearish market phases; avoid venues with chronic one-sided funding drains exceeding 0.1% per 8-hour interval unless hedged.
5. If fee schedules are opaque or subject to arbitrary discretionary adjustment by venue operators, assign an unverified ⚠️ warning flag.

## Procedure

1. Retrieve the official maker and taker fee schedules from exchange developer portals (e.g., Bybit fee structure: <https://www.bybit.com/en/help-center/article/Bybit-Fee-Structureen/help-center/article/Bybit-Fee-Structure>).
2. Query historical funding rate APRs across the top five perpetual markets for the past 90 days.
3. Review liquidation engine clearance rules to identify penalty percentages applied upon maintenance margin breach.
4. Calculate net effective cost per round-trip trade including statutory indirect taxes (GST, VAT) applicable in the operating jurisdiction.
5. Record all fee components in the venue diligence scorecard.

## Anti-patterns

- Evaluating venues solely on headline maker rebates while ignoring onerous taker fees and hidden liquidation penalties.
- Disregarding funding rate accumulation during extended trend phases, which can erode trading capital faster than base commissions.
- Failing to account for indirect taxes on exchange fees, leading to margin calculation errors over high-frequency execution cycles.

## Done checklist

- [ ] Maker and taker fee tiers documented and verified against official schedules.
- [ ] Historical funding rate distributions analyzed for sustained directional skew.
- [ ] Liquidation clearance penalty rules and insurance fund allocations reviewed.
- [ ] Statutory tax wrappers and indirect fee taxes incorporated into cost models (<https://www.bybit.com/en/help-center/article/Bybit-Fee-Structure>).
- [ ] All-in cost stack logged in the venue diligence scorecard.

## Sources

- Bybit Exchange Fee Structure and Trading Rules. <https://www.bybit.com/en/help-center/article/Bybit-Fee-Structureen/help-center/article/Bybit-Fee-Structure>
- Bybit V5 API Documentation for Derivatives Trading. <https://www.bybit.com/en/help-center/article/Bybit-Fee-Structureen/help-center/article/Bybit-Fee-Structure>
- Delta Exchange Official Documentation and Tax Compliance Notices. <https://www.delta.exchange/>
- Binance Futures Fee Schedule and Insurance Fund Rules. <https://www.binance.com/en/fee/futuresFee>
- CFTC Financial Data and Derivatives Clearinghouse Standards. <https://www.cftc.gov/PressRoom/PressReleases/9241-26>

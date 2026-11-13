---
name: cross-collateral-contagion
domain: crypto-trading/cross-collateral-contagion
trigger: analyzing cross-margin risk, evaluating mixed collateral portfolios, checking asset correlation during liquidations, auditing portfolio leverage
anti_trigger: stablecoin issuer audits, custody architecture review, peg monitoring setup, depeg playbook execution
scope: Mixed collateral under cross margin; correlation and contagion; why the same asset on both legs is not diversification.
status: seedling
---

## Standard
Cross-margin systems aggregate all account collateral and unrealized profits to support open positions across multiple trading pairs, creating efficiency at the cost of systemic contagion risk. When a portfolio holds mixed collateral types—such as pairing volatile crypto assets with stablecoins—a sharp price drop in one asset devalues the total account collateral pool, automatically endangering positions in entirely unrelated markets. Furthermore, utilizing the same digital asset as both trading collateral and margin backing creates a false sense of diversification; if that asset experiences a severe price correction or depeg, both the collateral backing value and the position equity decline simultaneously in a compounding feedback loop. Correlation between collateral assets and traded instruments tends toward one during systemic market panics, negating diversification assumptions built on historical normal-regime data. Academic research on financial contagion, systemic risk propagation, and portfolio correlation breakdowns is published by economic research centers such as the National Bureau of Economic Research at https://www.nber.org/ and monetary analysis groups at https://www.bis.org/. Analyzing cross-collateral structures requires stress-testing portfolio equity against simultaneous shocks to both collateral valuations and position legs to prevent catastrophic margin wipeouts.

## Decision rules
- Rule 1: Never treat holding different tokens within the same cross-margin account as genuine diversification during systemic market stress.
- Rule 2: Avoid using a volatile asset as margin collateral for perpetual contracts denominated or settled in that same underlying asset.
- Rule 3: Assume that asset correlations approach unity during liquidity crises, rendering multi-asset portfolio risk models temporarily ineffective.
- Rule 4: Isolate high-risk leveraged positions into separate sub-accounts to prevent cross-contamination of stable collateral pools.
- Rule 5: Calculate maximum potential portfolio drawdown assuming simultaneous maximum historical haircuts on all collateral holdings.

## Procedure
1. Audit the composition of all assets held within the cross-margin account across venues such as Kraken Pro available at https://www.kraken.com/features/pro.
2. Identify any overlap between the assets used as collateral and the underlying instruments of open perpetual futures positions.
3. Calculate portfolio leverage under worst-case collateral haircut scenarios where all held assets experience simultaneous price dislocation.
4. Review exchange cross-margin liquidation waterfall rules to understand the exact order in which collateral assets are liquidated during deficits.
5. Reallocate positions into isolated margin modes or separate sub-accounts to decouple unrelated risk exposures.

## Anti-patterns
- Assuming that holding a mix of altcoins and stablecoins in a cross-margin account protects against individual asset depegs.
- Using self-issued or highly correlated ecosystem tokens as margin collateral for leveraged directional bets on the same ecosystem.
- Ignoring the contagion effect where a liquidation in one illiquid pair drains the entire multi-asset collateral pool.
- Failing to monitor aggregate account leverage when volatility spikes across correlated market sectors.

## Done checklist
- [ ] Cross-margin collateral composition and asset overlaps audited.
- [ ] Correlation assumptions tested against historical systemic stress episodes.
- [ ] Portfolio leverage recalculated under worst-case haircut scenarios.
- [ ] Isolated margin allocations established for high-risk positions.
- [ ] Contagion pathways documented and mitigated across trading accounts.

## Sources
- National Bureau of Economic Research Contagion Studies: https://www.nber.org/
- Bank for International Settlements Systemic Risk Reports: https://www.bis.org/
- Kraken Pro Trading Features and Margin Documentation: https://www.kraken.com/features/pro

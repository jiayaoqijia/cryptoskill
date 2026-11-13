---
name: depeg-mechanics
domain: crypto-trading/depeg-mechanics
trigger: "investigating stablecoin depeg events, analyzing reserve runs, studying redemption gate mechanics, checking chain congestion during stress"
anti_trigger: "managing position leverage, calculating individual stop losses, executing arbitrage trades, selecting trading venues"
scope: "How a peg breaks: reserve runs, redemption gates, chain congestion, market-depth failure; the recurrent pattern from public episodes."
status: seedling
---

## Standard
A stablecoin depeg represents the divergence of an asset's market price from its nominal fiat peg, typically triggered by a loss of confidence in the underlying reserves or sudden liquidity demands that exceed immediate redemption capacity. The mechanics of a peg break follow a recurring pattern across historical episodes: initial panic leads to concentrated selling on secondary market liquidity pools, compressing order book depth and driving the market price below par. As arbitrageurs attempt to redeem tokens with the issuer for underlying fiat or cash equivalents, issuers may experience reserve runs where liquid assets are exhausted, forcing the activation of redemption gates or the suspension of creation and redemption mechanisms. Simultaneously, heightened transaction volume causes severe network congestion on host blockchains, delaying settlement and trapping margin collateral inside smart contracts or exchange deposit queues. This creates a feedback loop where cascading liquidations on derivative venues coincide with failing collateral values, compounding the downward pressure. Detailed analysis of historical depeg events, such as the TerraUSD collapse documented by researchers at https://www.nber.org/ and historical market stress reports available via https://www.bis.org/, demonstrates that liquidity evaporation precedes formal issuer insolvency declarations. Understanding these sequential failure modes enables traders to recognize early warning signals before secondary market liquidity completely vanishes.

## Decision rules
- Rule 1: Assume that any sudden widening of stablecoin spreads beyond historical norms indicates an active stress event requiring immediate margin re-evaluation.
- Rule 2: Never rely on secondary market depth during a depeg; order books thin out exponentially once arbitrageurs exhaust capital.
- Rule 3: Monitor blockchain gas prices and transaction pool congestion as primary indicators of operational stress during collateral movement.
- Rule 4: Treat redemption gate announcements as permanent cessation of direct liquidity access for the duration of the crisis.
- Rule 5: Avoid attempting complex multi-hop swaps across decentralized exchanges when network congestion spikes and oracle staleness risks mispricing.

## Procedure
1. Monitor real-time price feeds across multiple decentralized and centralized exchanges to detect sustained deviations from the 1:1 parity threshold.
2. Check on-chain transaction metrics and mempool congestion levels via public explorers such as Etherscan at https://etherscan.io/.
3. Review issuer official communication channels and status pages for announcements regarding redemption halts or banking partner updates.
4. Assess the depth of liquidity pools for the depegged asset on automated market makers as detailed in analytics dashboards like Uniswap info at https://info.uniswap.org/.
5. Calculate the effective collateral haircut resulting from the observed price discount and determine necessary position reductions.

## Anti-patterns
- Assuming that a depeg is a temporary pricing anomaly that will revert automatically without verifying underlying reserve liquidity.
- Submitting market sell orders into thinned-out order books during peak panic without calculating slippage impact.
- Ignoring network gas spikes when attempting urgent collateral transfers between self-custody wallets and exchange margin accounts.
- Waiting for official issuer confirmation of insolvency before reducing exposure to compromised collateral assets.

## Done checklist
- [ ] Peg deviation metrics and secondary market spreads evaluated.
- [ ] Network congestion and on-chain settlement delays assessed.
- [ ] Issuer redemption status and official disclosures verified.
- [ ] Liquidity pool depth checked across major exchange venues.
- [ ] Depeg mechanics factored into immediate collateral risk management.

## Sources
- National Bureau of Economic Research Working Papers: https://www.nber.org/
- Bank for International Settlements Market Reports: https://www.bis.org/
- Etherscan Blockchain Explorer and Gas Tracking: https://etherscan.io/
- Uniswap Protocol Analytics and Pool Depth: https://info.uniswap.org/

---
name: depeg-playbook
domain: crypto-trading/depeg-playbook
trigger: "responding to an active depeg event, reducing exposure during peg breaks, swapping compromised collateral, executing emergency venue migration"
anti_trigger: "normal market trading, routine portfolio rebalancing, historical research, setting up passive alerts"
scope: "During a depeg: the decision order (reduce exposure, swap collateral, move venue), and what never to do (market orders into a gapped book)."
status: seedling
---

## Standard
When a stablecoin collateral asset experiences an active depeg, disciplined execution of a predefined emergency playbook is mandatory to prevent catastrophic capital loss. The decision order during a peg break follows a strict hierarchical sequence: first, immediately reduce open perpetual futures position leverage and exposure to minimize liquidation vulnerability; second, swap compromised collateral assets into proven fiat-backed alternatives or native cash equivalents through deep liquidity pools; third, migrate remaining collateral balances away from vulnerable venue omnibus wallets or congested networks. Crucially, traders must never submit aggressive market sell orders directly into thinned-out, gapped secondary market order books, as doing so exacerbates slippage and locks in devastating execution losses. Emergency protocols and crisis management frameworks for financial markets are documented by regulatory bodies such as the U.S. Securities and Exchange Commission at https://www.sec.gov/ and professional trading standards organizations like the Futures Industry Association at https://www.fia.org/. Following a rigorous, emotion-free decision order ensures orderly capital preservation during high-stress liquidity crunches.

## Decision rules
- Rule 1: Execute risk reduction in strict hierarchical order: reduce leverage first, swap collateral second, migrate venue third.
- Rule 2: Never submit large market orders into illiquid, gapped order books during a depeg event; utilize timed limit orders or OTC pathways.
- Rule 3: Avoid attempting multi-hop decentralized exchange swaps when gas fees spike and price impact calculations become unreliable.
- Rule 4: Cease all new position openings on venues experiencing collateral settlement delays or administrative withdrawal freezes.
- Rule 5: Preserve an emergency cash reserve in native tier-one assets completely independent of secondary stablecoin collateral pools.

## Procedure
1. Trigger immediate position deleveraging across all active trading accounts upon confirmation of a sustained structural depeg.
2. Calculate the optimal exit path for compromised collateral using aggregated depth charts from major aggregators like CoinGecko at https://www.coingecko.com/.
3. Execute phased limit orders or utilize direct issuer redemption channels if available to exchange depegged tokens for par value.
4. Transfer successfully converted tier-one assets out of exchange omnibus wallets into self-custody storage.
5. Document the crisis response execution, noting slippage costs, execution speeds, and operational bottlenecks for post-mortem review.

## Anti-patterns
- Panicking and dumping depegged collateral via aggressive market orders into empty order books, maximizing execution loss.
- Attempting to trade the volatility of the depegged asset with leveraged perpetual positions while holding the same asset as margin.
- Waiting for official exchange confirmation or news announcements before initiating defensive leverage reduction.
- Leaving collateral on a venue that has paused withdrawals under the assumption that the freeze is temporary.

## Done checklist
- [ ] Emergency decision order hierarchy activated immediately upon depeg confirmation.
- [ ] Open leverage and position exposure reduced safely without severe market impact.
- [ ] Collateral swapped via liquid pathways avoiding gapped book slippage.
- [ ] Assets migrated successfully out of vulnerable exchange custody.
- [ ] Post-incident review documented covering execution performance and losses.

## Sources
- U.S. Securities and Exchange Commission Regulatory Guidelines: https://www.sec.gov/
- Futures Industry Association Trading Standards: https://www.fia.org/
- CoinGecko Cryptocurrency Data and Liquidity Metrics: https://www.coingecko.com/

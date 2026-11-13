---
name: "liquidity-realism"
domain: "crypto-trading/liquidity-realism"
trigger: "When asked to evaluate exchange depth, order book realism, traded turnover, or liquidity spoofing"
anti_trigger: "When analyzing macro regulatory policy or calculating funding fee stacks"
scope: "Quoted depth vs traded turnover, flat slippage red flags, and small-order testing protocols."
status: "seedling"
---

# Liquidity Realism

## Standard

- **Kyle, A. S. (1985), "Continuous Auctions and Insider Trading", _Econometrica_**: Market depth and price impact are fundamentally governed by order flow resilience and adverse selection costs, establishing that advertised top-of-book depth without matching volume is an illusion. <https://www.jstor.org/stable/1913210>
- **Cont, R., Stoikov, S., & Talreja, R. (2010), "A Market Order Book Model", _Operations Research_**: Order book liquidity must be measured by volume resilience across price levels rather than static resting quotes subject to cancellation. <https://pubsonline.informs.org/doi/10.1287/opre.1090.0785>
- **Theta Desk Research (2026), Delta Exchange Diligence**: Quoted top-of-book depth of $12.6M against $971,156 of 24h turnover and $341,944 open interest represents a ~2,900× discrepancy; flat 0.030 bps slippage across $10K to $500K is the empirical signature of an inactive book rather than genuine liquidity. <https://www.delta.exchange/>
- ⚠️ House standard: any venue where quoted book depth exceeds daily turnover by more than 100× while exhibiting flat linear slippage must be classified as illiquid and unsuited for size execution.

## Decision rules

1. Compute the ratio of total resting order book depth within 1% of mid-price to 24-hour traded turnover; ratios exceeding 50× require immediate small-order slippage testing.
2. If execution testing with a $1,000 equivalent order yields identical percentage slippage to a $100,000 order across multiple price increments, reject the book's quoted depth as algorithmic spoofing or phantom liquidity.
3. Verify that open interest represents at least 10% of daily volume; illiquid books with high open interest relative to turnover indicate severe trap risk during liquidation cascades.
4. Never rely on exchange-provided liquidity scores or resting depth metrics without independent WebSocket order book reconstruction and trade tape validation.
5. In case of unverified resting liquidity or missing public trade APIs, apply a mandatory ⚠️ warning flag and restrict capital deployment to zero.

## Procedure

1. Extract the order book snapshot via public REST or WebSocket endpoints (e.g., Binance API docs: <https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info>).
2. Calculate cumulative resting liquidity across 0.1%, 0.5%, and 1.0% depth bands for both bid and ask sides.
3. Query 24-hour rolling traded turnover and current open interest from exchange data feeds.
4. Execute empirical probing tests using incremental micro-orders (or simulate execution against historical depth snapshots) to measure true price impact.
5. Compare observed price impact against theoretical Kyle lambda estimates; document discrepancies in the venue scorecard.

## Anti-patterns

- Trusting exchange front-end UI depth charts that display dense resting walls without verifying recent trade execution frequency.
- Assuming high quoted depth on minor altcoin perpetual pairs translates to execution capacity during high-volatility liquidation events.
- Failing to cross-reference open interest with daily turnover, leading to exposure in dead markets where position exit is mechanically impossible.

## Done checklist

- [ ] Order book depth vs 24h turnover ratio calculated and verified.
- [ ] Slippage consistency across order sizes tested or evaluated.
- [ ] Open interest compared against daily volume benchmarks.
- [ ] Public API documentation reviewed for depth feed accuracy (<https://www.binance.com/en/fee/futuresFee>).
- [ ] Findings logged in the venue diligence scorecard.

## Sources

- Kyle, A. S. (1985). Continuous Auctions and Insider Trading. *Econometrica*, 53(6), 1315-1335. <https://www.jstor.org/stable/1913210>
- Cont, R., Stoikov, S., & Talreja, R. (2010). A Market Order Book Model and its Empirical Validation. *Operations Research*, 58(3), 549-563. <https://pubsonline.informs.org/doi/10.1287/opre.1090.0785>
- Binance API Documentation. Market Data Endpoints and Order Book Mechanics. <https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info>
- Delta Exchange Official Portal. Exchange Specifications and Contract Metrics. <https://www.delta.exchange/>
- CFTC Guidance on Digital Asset Derivatives and Market Integrity. <https://www.cftc.gov/PressRoom/PressReleases/9241-26>

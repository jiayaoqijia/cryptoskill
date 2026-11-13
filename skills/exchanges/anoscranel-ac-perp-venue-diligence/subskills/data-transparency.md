---
name: "data-transparency"
domain: "crypto-trading/data-transparency"
trigger: "When asked about data transparency, public API endpoints, liquidation feeds, order book streams, or historical data"
anti_trigger: "When evaluating tax laws or internal exchange insurance fund capitalization"
scope: "Transparency ladder, public API endpoints for liquidations, order books, and historical trade feeds."
status: "seedling"
---

# Data Transparency

## Standard

- **Hyperliquid Developer API Documentation**: Institutional-grade derivatives venues provide comprehensive, rate-limit-friendly public APIs (e.g., `POST /info` endpoints) delivering real-time L2 order book snapshots, historical trade executions, and atomic liquidation event streams without authentication barriers. <https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpointhyperliquid-docs/for-developers/api>
- **Bybit V5 Public Data Feeds**: Robust venues maintain granular WebSocket channels for liquidation feeds (`publicTrade`, `liquidation.{symbol}`), open interest time series, and funding rate histories, enabling independent verification of market mechanics. <https://bybit-exchange.github.io/docs/v5/websocket/public/liquidation>
- ⚠️ House standard: any exchange that omits public liquidation streams or returns 404/401 errors on core analytics endpoints is operating a black-box execution venue and must be restricted from automated strategy integration.

## Decision rules

1. Verify that the exchange provides open, unauthenticated public REST and WebSocket endpoints for order book depth, trade history, and forced liquidation events.
2. Check endpoint reliability, rate limit thresholds, and historical data accessibility; missing historical liquidation logs prevent rigorous backtesting and cascade forensics.
3. Test public liquidation feeds against actual market wicks to ensure events are broadcast atomically without artificial filtering or delayed batching.
4. If an exchange restricts critical data feeds behind VIP tiers or requires proprietary SDKs without open REST documentation, apply a transparency penalty in the venue scorecard.
5. Never execute automated strategies on venues lacking transparent, auditable websocket data streams.

## Procedure

1. Query public API documentation to locate liquidation stream endpoints (e.g., Hyperliquid API: <https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpointhyperliquid-docs/>).
2. Establish a test WebSocket connection to subscribe to ticker, order book, and liquidation channels.
3. Measure message latency, payload completeness, and heartbeat stability over a 24-hour monitoring window.
4. Cross-reference broadcast liquidation totals against independent blockchain analytics or aggregate venue trackers.
5. Record transparency ratings in the venue diligence scorecard.

## Anti-patterns

- Assuming exchange-advertised trading volumes are accurate without verifying public trade execution streams.
- Relying on aggregated third-party charting frontends that smooth or interpolate missing exchange API data feeds.
- Ignoring rate limit restrictions during high-volatility events when data consumption spikes.

## Done checklist

- [ ] Public API documentation reviewed for endpoint coverage.
- [ ] WebSocket liquidation and order book feeds successfully tested.
- [ ] Historical data availability verified for backtesting.
- [ ] API reliability and rate limit thresholds documented (<https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint>).
- [ ] Transparency score logged in the venue diligence scorecard.

## Sources

- Hyperliquid Developer Documentation and API Endpoints. <https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpointhyperliquid-docs/for-developers/api>
- Bybit V5 API Developer Guide and WebSocket Feeds. <https://bybit-exchange.github.io/docs/v5/websocket/public/liquidation>
- Binance API Developer Portal for Market Data and Liquidation Streams. <https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info>
- GitHub Open Source Cryptocurrency Data Connectors and Protocols. <⚠️ cited without URL.>
- CFTC Market Transparency and Trade Reporting Standards. <https://www.cftc.gov/PressRoom/PressReleases/9241-26>

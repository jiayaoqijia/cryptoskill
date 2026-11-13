---
name: fill-log-reading
domain: crypto-trading/fill-log-reading
trigger: "Reconstructing a cascade timeline from a transparent venue's fill log: required fields, ordering, dedup, gaps; what a fill log proves vs what it merely suggests."
anti_trigger: "Interpreting aggregated third-party feeds without raw execution records (subskills/proxies-and-tape.md); assuming account categories without verification (subskills/participation-and-anatomy.md)."
scope: "Reconstructing a cascade timeline from a transparent venue's fill log: required fields, ordering, dedup, gaps; what a fill log proves vs what it merely suggests."
status: seedling
---

# Fill Log Reading

## Standard

- **Binance API Documentation (2026)**: Historical trade and liquidation stream specifications, defining required fields such as symbol, price, quantity, timestamp, and liquidation status. <https://binance-docs.github.io/apidocs/futures/en/>
- **Hyperliquid Documentation (2026)**: On-chain and transparent websocket fill-log specifications for decentralized perpetual derivative exchanges, detailing event sequencing and clearing mechanisms. <https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint>
- **Hasbrouck, S. (2007)**: *Empirical Market Microstructure: The Institutions, Prices, and Econometrics of Securities Markets*. Oxford University Press. Establishes the necessity of timestamp sequencing and trade deduping. <https://global.oup.com/academic/product/empirical-market-microstructure-9780195301646>

## Decision rules

- **Rule 1 (Field completeness)**: Every reconstructed event must contain timestamp, price, size, and execution side; missing fields invalidate the sequence.
- **Rule 2 (Chronological sorting)**: Fills must be ordered by exchange-assigned transaction IDs or microsecond exchange timestamps, never client arrival time.
- **Rule 3 (Deduplication boundary)**: Duplicate websocket frames must be filtered using unique trade IDs ( or uid=10321(u0_a321) gid=10321(u0_a321) groups=10321(u0_a321),1007(log),1079(ext_obb_rw),3003(inet),9997(everybody),20321(u0_a321_cache),50321(all_a321),99909997 fields) before calculating cumulative volume.
- **Rule 4 (Proven vs suggested)**: A fill log strictly proves execution price and quantity; it merely suggests order-book depth depletion unless matched with L2/L3 snapshots.

## Procedure

1. Ingest raw websocket or historical CSV fill logs from a transparent derivatives venue (e.g., Binance Futures or Hyperliquid).
2. Extract mandatory fields: timestamp (UTC), trade ID, symbol, execution price, executed quantity, and liquidation marker.
3. Sort records chronologically by exchange transaction ID to resolve millisecond timestamp collisions.
4. Run a duplicate-removal pass using trade ID hashes to eliminate dropped-connection replay artifacts.
5. Identify network latency gaps or missing sequence numbers by checking transaction ID continuity.
6. Match execution timestamps against historical order book depth snapshots to correlate price impact with liquidity exhaustion.
7. Compile the validated execution timeline into a structured tabular format for branching-ratio analysis.

## Anti-patterns

- Relying on local client-receive timestamps instead of exchange-native execution timestamps.
- Treating aggregated 1-minute candlestick volume as individual liquidation fills.
- Failing to deduplicate overlapping websocket message payloads during high-volatility spikes.
- Concluding that a high volume of liquidations proves coordinated market manipulation without order book depth analysis.

## Done checklist

- [ ] Raw fill logs ingested from transparent venue API.
- [ ] Mandatory fields (timestamp, price, size, side) verified.
- [ ] Chronological sorting applied via transaction IDs.
- [ ] Duplicate frames removed using trade ID hashing.
- [ ] Sequence gaps identified and documented.
- [ ] Execution timeline formatted and ready for analysis.
- [ ] Word count and URL counts verified (>=2 public URLs in body, >=2 in Sources).

## Sources

- Binance Futures API documentation. <https://binance-docs.github.io/apidocs/futures/en/>
- Hyperliquid perpetual protocol documentation. <https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint>
- Hasbrouck, J. (2007). *Empirical Market Microstructure*. Oxford University Press. <https://global.oup.com/academic/product/empirical-market-microstructure-9780195301646>
- Campbell, J. Y., Lo, A. W., & MacKinlay, A. C. (1997). *The Econometrics of Financial Markets*. Princeton University Press. <https://press.princeton.edu/books/hardcover/9780691043014/the-econometrics-of-financial-markets>

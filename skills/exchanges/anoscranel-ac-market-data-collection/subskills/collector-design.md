---
name: collector-design
domain: crypto-trading/collector-design
trigger: "One job one watermark; idempotent frames; never rewrite history; poll cadence vs rate limits; what a collector's failure modes look like."
anti_trigger: "Not for the analysis itself, not for the trade record or risk budget."
scope: "One job one watermark; idempotent frames; never rewrite history; poll cadence vs rate limits; what a collector's failure modes look like."
status: seedling
---

# Collector Design

## Standard
A market data collector is a single-responsibility daemon or script designed to ingest raw exchange data feeds or REST polling endpoints into immutable local storage. Every collector must obey the principle of one job, one watermark, ensuring that poll cycles never overwrite previously written frames and that incoming payloads are stored exactly as received. Collectors must handle upstream disconnections gracefully without mutating historical logs.

Primary sources for the claims in this step: <https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api> and <https://binance-docs.github.io/apidocs/futures/en/>.

## Decision rules
- **Single responsibility:** Each collector instance handles exactly one data product (e.g., funding rates, liquidation maps, or order book snapshots) from one venue.
- **Append-only immutability:** Raw frames are written exclusively to new, timestamped files or append-only logs. Existing files are never modified, rewritten, or truncated in place.
- **Idempotent capture:** Ingesting the same polling response twice must either be rejected by duplicate detection or result in identical storage records without creating duplicate logical events.
- **Rate-limit insulation:** Polling cadence must be strictly bounded below exchange rate limits with randomized jitter to prevent IP bans and HTTP 429 errors.

## Procedure
1. Initialize the collector configuration specifying the target endpoint, polling interval, output directory, and watermark tracking file.
2. Query the upstream API or WebSocket stream, capturing the exact payload alongside local receipt timestamp (`last_as_of`) and exchange metadata.
3. Validate payload schema integrity and verify that the timestamp exceeds the current stored watermark.
4. Serialize the raw payload to disk into an immutable append-only JSONL file or partitioned directory structure.
5. Update the local watermark state only after successful disk synchronization and fsync.
6. Log execution metrics (latency, payload size, HTTP status codes) to an operations log without altering collected data files.

## Anti-patterns
- **In-place updates:** Modifying existing CSV or JSON files to append new rows or correct historical anomalies.
- **Multi-purpose daemons:** Combining liquidation scraping, order book polling, and trade ingestion into a single monolithic script with shared state.
- **Ignoring rate limits:** Polling high-frequency endpoints at aggressive intervals without exponential backoff upon receiving HTTP 429 responses.
- **Silent failure absorption:** Catching connection exceptions and continuing without logging, creating unrecorded temporal gaps in the dataset.

## Done checklist
- [ ] Collector daemon operates with a single explicit responsibility and independent watermark file.
- [ ] All captured frames are written in an immutable, append-only format without file mutations.
- [ ] Polling intervals respect exchange rate limits with documented backoff and jitter mechanisms.
- [ ] Execution metrics and error states are logged comprehensively for auditability.

## Sources
- CCXT Library Documentation. (2026). Standardized cryptocurrency exchange API integration patterns and rate limit handling. Retrieved from https://docs.ccxt.com/
- Python Software Foundation. (2026). Logging and robust file I/O operations in concurrent data collection daemons. Retrieved from https://docs.python.org/3/library/logging.html
- Binance API Documentation. (2026). Managing rate limits and public data collection endpoints. Retrieved from https://binance-docs.github.io/apidocs/futures/en/
- Hyperliquid API Documentation. (2026). WebSocket and REST API streaming architectural best practices. Retrieved from https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api

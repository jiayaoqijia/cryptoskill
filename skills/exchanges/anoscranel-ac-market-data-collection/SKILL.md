---
name: ac-market-data-collection
description: "Build robust, repeatable crypto and financial market data collection pipelines, historical datasets, and robust scraping pipelines with strict watermarking, idempotency, gap detection, survivorship-and-universe tracking, and study-readiness validation. Not for running the downstream statistical analysis or forensic hypothesis testing on the collected corpus (ac-cascade-forensics, ac-liquidation-hunt-analysis), not for general enterprise data engineering outside financial time-series markets, and not for recording individual live trade executions or position sizing records (ac-crypto-trading-discipline). Use when asking \"collect market data\", \"build a data pipeline for trading\", \"watermark\", \"backfill\", \"survivorship bias\", \"data series for backtesting\", \"scrape exchange data\"."
license: MIT
metadata:
  domain: crypto-trading
  status: "seedling"
---

# Market Data Collection

ac-market-data-collection establishes the engineering standard and operating procedure for building robust, append-only financial and crypto market data pipelines. Reliable empirical market research, cascade forensics, and quantitative strategy design depend entirely upon pristine data ingestion architectures that eliminate survivorship bias, enforce strict watermark continuity, handle upstream API rate limits, and maintain exact point-in-time universe records.

## When to use

- Designing append-only market data collection daemons for continuous exchange WebSocket or REST ingestion.
- Building historical data series for backtesting, liquidation hunts, or market structure research.
- Enforcing strict watermark tracking, idempotency, and automated gap detection in time-series pipelines.
- Preserving historical point-in-time exchange universes and handling delisted instruments without survivorship bias.
- Validating study readiness, window arithmetic, and pre-registered statistical test parameters before quantitative ingestion runs.

## When NOT to use

- Running downstream statistical tests, Bonferroni corrections, or forensic hypothesis analysis on already collected corpuses (use ac-cascade-forensics or ac-liquidation-hunt-analysis).
- Managing enterprise data warehousing, general business ETL pipelines, or non-financial web scraping tasks outside financial markets.
- Recording individual live trade execution journals, risk budgets, or discretionary position sizing parameters (use ac-crypto-trading-discipline).

## Subskills Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| [collector-design](subskills/collector-design.md) | crypto-trading/collector-design | One job one watermark; idempotent frames; never rewrite history; poll cadence vs rate limits; what a collector's failure modes look like. |
| [watermarks-and-gaps](subskills/watermarks-and-gaps.md) | crypto-trading/watermarks-and-gaps | Watermarking on max(last_as_of); gap detection; backfill policy; how a silent gap corrupts a study (and how to prove a series is gap-free). |
| [survivorship-and-universe](subskills/survivorship-and-universe.md) | crypto-trading/survivorship-and-universe | Point-in-time universe: the instruments and venues that existed THEN, not now; delisting and renaming; why survivorship bias kills cascade studies. |
| [series-design](subskills/series-design.md) | crypto-trading/series-design | What makes a usable series: the 168-cell dowxhour notional example (one daily call, ~20 min/month); pre-registering the analysis BEFORE collecting; UTC discipline; units and aggregation rules. |
| [source-tiering](subskills/source-tiering.md) | crypto-trading/source-tiering | Free vs paid (vendor tiering example: a data vendor with $29-$699 monthly tiers and no free API); rate limits; terms-of-service boundaries; when the only source is a web page that must be scraped - and how to record that provenance. |
| [storage-and-integrity](subskills/storage-and-integrity.md) | crypto-trading/storage-and-integrity | Append-only raw frames, checksums, schema versioning, a second copy on a different medium, and the rule that collected evidence is committed/persisted before any analysis reads it. |
| [study-readiness](subskills/study-readiness.md) | crypto-trading/study-readiness | The checklist before a study runs: window arithmetic (e.g. 31 days of print history -> earliest valid date), the pre-registered test (42 cells, Bonferroni, placebo), and the rule that a collector is finished when the study can run without you. |

## Status and honest limits

This skill operates as a seedling framework. Data collection pipelines are vulnerable to silent upstream schema drift, unannounced exchange rate-limiting changes, and IP bans. Every ingested dataset must be audited independently for gaps before analysis commences. Point-in-time universe reconstructions require diligent historical record-keeping across venue API deprecations.

## Sources

- Hyperliquid API Documentation. (2026). REST and WebSocket API endpoints for historical funding and mid prices. Retrieved from https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api
- Bybit Exchange. (2026). Bybit V5 Public Data and Liquidation WebSocket Streams. Retrieved from https://bybit-exchange.github.io/docs/v5/intro
- CoinGlass Analytics. (2026). Liquidation map data structures and historical aggregation tiers. Retrieved from https://www.coinglass.com/
- Binance API Documentation. (2026). Binance Futures API specifications for public market data and liquidation streams. Retrieved from https://binance-docs.github.io/apidocs/futures/en/

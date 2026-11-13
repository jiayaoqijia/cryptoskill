---
name: "measurement-layer"
domain: "crypto-trading/measurement-layer"
trigger: "When asked about measurement layer in liquidation analysis"
anti_trigger: "When conducting unrelated trading tasks or general market research"
scope: "measurement layer analysis for derivative liquidation events"
status: "seedling"
---

# Measurement Layer

## Standard

Measurement layer specifies the rigorous technical workflow required to collect, parse, and analyze liquidation data from public exchange endpoints and commercial vendor platforms. To conduct empirical research on cascade mechanics without relying on unverified third-party dashboards, analysts must construct deterministic data collection pipelines. This leaf details public API endpoints (such as Hyperliquid `POST /info`, Bybit V5 `liquidation.{symbol}`, and Binance USDⓈ-M futures `fapi` endpoints), commercial vendor pricing structures (ranging from CoinGlass hobbyist tiers to professional $699/mo subscriptions), and the operational rule that custom collection scripts consistently outperform passive web searches.

Building an audit-grade measurement pipeline requires structuring data ingestion into standardized time-series partitions. Because commercial heatmap vendors often gate granular historical liquidation sweeps behind expensive professional tiers (e.g., $699/mo), analysts must implement custom scraper collectors or utilize direct WebSocket feeds to capture raw liquidation events before aggregation artifacts distort the record.

Primary sources for the claims here: <https://bybit-exchange.github.io/docs/linear/> and <https://hyperliquid.gitbook.io/>.

## Decision rules

- Rule 1: Prioritize direct public API ingestion over consumer-facing graphical dashboards for primary empirical research. Utilize Hyperliquid `POST /info`, Bybit V5 WebSocket/REST liquidation streams, and Binance `fapi/v1/allForceOrders`.
- Rule 2: Account for commercial vendor pricing tiers and data gating realities. Recognize that consumer tiers ($29–$299/mo) omit granular liquidation sweep data, requiring custom page-scraping or direct exchange log ingestion for rigorous studies.
- Rule 3: Enforce the empirical collection rule: a systematic, automated local collection project collecting raw prints over 30+ days supersedes any ad-hoc web search or vendor summary report.
- Rule 4: Reject any measurement setup that fails to record sample timestamps, exchange identifiers, and data source lineage alongside raw liquidation figures.

## Procedure

1. Configure asynchronous API polling workers to query exchange endpoint REST archives at standardized minute intervals.
2. Establish persistent WebSocket connections to capture real-time `liquidation` push events and order book depth updates.
3. Store raw incoming JSON payloads in immutable local storage partitions (e.g., partitioned parquet files or compressed CSV logs).
4. Run automated validation scripts to check for dropped websocket frames, timestamp gaps, and exchange formatting anomalies.
5. Compile structured time-series datasets ready for branching ratio estimation and temporal volume clustering analysis.

## Anti-patterns

- Anti-pattern: Relying exclusively on screenshot summaries or curated vendor charts without inspecting raw underlying database records.
- Anti-pattern: Assuming that commercial API endpoints provide unlimited historical depth without rate limiting or pagination caps.
- Anti-pattern: Failing to maintain continuous data collection windows, resulting in survivorship bias and incomplete cascade logs.

## Done checklist

- [ ] Public API endpoints (Hyperliquid, Bybit V5, Binance fapi) documented.
- [ ] Vendor pricing tier constraints ($29 to $699/mo) and scrape requirements noted.
- [ ] Empirical collection rule (custom collector beats ad-hoc search) established.
- [ ] Data validation and raw storage procedures outlined.
- [ ] Zero predictive or trading recommendations included.

## Sources

- Hyperliquid Documentation. (2026). *API Info Endpoints and Historical Data Access*. Hyperliquid GitBook. https://hyperliquid.gitbook.io/
- Bybit API Reference. (2026). *V5 Linear Derivative Liquidation Public Endpoints*. Bybit Fintech. https://bybit-exchange.github.io/docs/linear/

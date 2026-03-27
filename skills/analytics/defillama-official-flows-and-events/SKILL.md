---
name: flows-and-events
description: Guide for querying DeFi flow data and events using DefiLlama MCP tools. Covers bridge flows, ETF inflows/outflows, stablecoin supply, institutional/DAT holdings with mNAV ratios, hacks and exploits, fundraising rounds, CEX volumes, open interest, and protocol treasuries. Use when users ask about bridge volume, ETF flows, stablecoin supply, MicroStrategy holdings, DeFi hacks, funding rounds, exchange volume, or treasury data.
---

# DeFi Flows and Events

## Bridge Flows

Tool: `defillama:get_bridge_flows`

- Two-way bridge deduplication is applied automatically when aggregating
- Grain: bridge x chain (one row per bridge per chain)
- `inflows = deposit_amount - withdraw_amount` (pre-computed, positive = net inflow)
- Params: `bridge`, `chain`, `period`, `start_date`, `end_date`, `sort_by`, `limit`

## ETF Flows

Tool: `defillama:get_etf_flows`

- `flow_usd` is **signed**: positive = inflow, negative = outflow
- Filter by underlying: `token: "bitcoin"` for all BTC ETFs, `token: "ethereum"` for ETH ETFs
- Use `etf` param to filter specific ETF (e.g., `"ibit"`, `"fbtc"`)
- Current view shows latest day only. Use `period: "30d"` for historical.

## Stablecoin Supply

Tool: `defillama:get_stablecoin_supply`

- Supply = **issuance** on each chain, NOT DeFi deposits
- Grain: stablecoin x chain (one row per stablecoin per chain)
- Use `circulating_supply` (not `total_supply`) for supply queries
- Filter by `peg_type` (usd, eur)
- Params: `stablecoin`, `chain`, `peg_type`, `period`, `sort_by`, `limit`

## Institutional Holdings (DAT)

Tool: `defillama:get_dat_holdings`

- Tokens are automatically prefixed with `coingecko:` if not already (e.g., `token: "bitcoin"` works)
- Base response: institution overview (total value, cost, mNAV ratios)
- `include_history: true` adds historical holding snapshots
- `include_mnav: true` adds mNAV time series
- `transaction_type` filters history by transaction type (e.g., `"purchase"`, `"sale"`)

**mNAV** (multiple of Net Asset Value) -- measures crypto exposure relative to market cap:

- `realized_mnav`: conservative estimate
- `realistic_mnav`: expected dilution
- `max_mnav`: maximum dilution
- mNAV > 1 means crypto holdings exceed the company's market cap attribution

## Hacks and Exploits

Tool: `defillama:get_events` with `event_type: "hacks"`

- Filter by `protocol` (victim slug), `chain` (uses `= ANY(chains)` for array column), `min_amount`
- `returned_funds` shows how much was recovered after the hack
- Use `sort_by: "amount desc"` for biggest hacks

## Fundraising Rounds

Tool: `defillama:get_events` with `event_type: "raises"`

- Filter by `protocol`, `chain` (uses `= ANY(chains)` for array column), `min_amount`
- Use `sort_by: "amount desc"` for largest rounds

## Protocol Events

Tool: `defillama:get_events` with `event_type: "protocol_events"`

- Governance votes, upgrades, launches, and other protocol milestones
- Additional filters: `target_type` (filter by target type), `sub_protocol` (filter by sub-protocol slug)

## CEX Volumes

Tool: `defillama:get_cex_volumes`

- CEX slugs differ from common names: binance -> `binance-cex`, huobi -> `htx`, gate.io -> `gate-io`
- Params: `cex`, `period`, `sort_by`, `limit`

## Open Interest

Tool: `defillama:get_open_interest`

- Aggregates with SUM/GROUP BY for proper protocol-level totals
- Params: `protocol`, `chain`, `period`, `start_date`, `end_date`, `sort_by`, `limit`

## Treasury

Tool: `defillama:get_treasury`

- Aggregates with SUM/GROUP BY for proper protocol-level totals
- `treasury_excl_own_token` is the realistic value (excludes inflation of protocol's own token)
- `treasury_total` includes own token (inflated value)
- Params: `treasury`, `chain` (for per-chain breakdown), `period`, `start_date`, `end_date`, `sort_by`, `limit`

## Examples

**Example 1:**
User: "Bitcoin ETF flows this month"
Tool call: `defillama:get_etf_flows(token: "bitcoin", period: "30d")`

**Example 2:**
User: "MicroStrategy bitcoin holdings"
Tool call: `defillama:get_dat_holdings(institution: "microstrategy", token: "coingecko:bitcoin", include_history: true)`

**Example 3:**
User: "Biggest DeFi hacks in 2024"
Tool call: `defillama:get_events(event_type: "hacks", sort_by: "amount desc", limit: 10, start_date: "2024-01-01", end_date: "2024-12-31")`

**Example 4:**
User: "USDT supply across chains"
Tool call: `defillama:get_stablecoin_supply(stablecoin: "coingecko:tether", sort_by: "circulating_supply desc")`

**Example 5:**
User: "Top bridge volume this week"
Tool call: `defillama:get_bridge_flows(period: "7d", sort_by: "volume desc", limit: 10)`

**Example 6:**
User: "Largest crypto fundraises this year"
Tool call: `defillama:get_events(event_type: "raises", period: "365d", sort_by: "amount desc", limit: 20)`

**Example 7:**
User: "Binance trading volume"
Tool call: `defillama:get_cex_volumes(cex: "binance-cex")`

**Example 8:**
User: "Uniswap treasury breakdown"
Tool call: `defillama:get_treasury(treasury: "uniswap")`

**Example 9:**
User: "ETF flows in February 2025"
Tool call: `defillama:get_etf_flows(token: "bitcoin", start_date: "2025-02-01", end_date: "2025-02-28")`

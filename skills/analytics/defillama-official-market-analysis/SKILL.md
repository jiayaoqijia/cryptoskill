---
name: market-analysis
description: Patterns for DeFi market analysis, screening, and comparison using DefiLlama MCP tools. Covers valuation ratios (P/S, P/F), growth screening with pct_change columns, multi-metric protocol comparison, category comparison, and cross-entity analysis. Use when users ask to compare protocols, screen for undervalued projects, analyze growth trends, or do sector analysis.
---

# DeFi Market Analysis

## Valuation Ratios

Pre-computed in `defillama:get_protocol_metrics` and `defillama:get_category_metrics`:

- `ps_ratio` = mcap / annualised revenue. Lower = potentially undervalued relative to revenue.
- `pf_ratio` = mcap / annualised fees. Lower = more fee-efficient valuation.

## Growth Screening

Use `*_pct_change` columns for momentum analysis. Values are **decimals** (0.35 = +35%, -0.13 = -13%).

Available windows: `*_7d_pct_change`, `*_30d_pct_change`, `*_90d_pct_change`

Metrics with pct_change: `tvl_base`, `fees_1d`, `revenue_1d`, `price`, `volume_dexs_1d`

Sort by any pct_change column to find fastest movers.

## Protocol Comparison

Use array params for side-by-side comparison in a single call:

```
defillama:get_protocol_metrics(
  protocol: ["aave", "compound-v3", "morpho"],
  metrics: ["tvl_base", "fees_1d", "revenue_1d", "ps_ratio"]
)
```

This returns one row per protocol, which is more efficient than calling once per protocol.

## Category Comparison

Use `defillama:get_category_metrics` to compare DeFi sectors:

```
defillama:get_category_metrics(
  category: "Lending",
  metrics: ["tvl_base", "fees_1d", "protocol_count"]
)
```

Call once per category in parallel for side-by-side comparison.

## Token Sector Screening

Use `defillama:get_token_prices` for token-level analysis:

```
defillama:get_token_prices(token: "coingecko:ethereum", period: "30d")
```

## Historical Trends

Use `period` for trend analysis:

- Short-term: `7d` or `30d`
- Medium-term: `90d` or `180d`
- Long-term: `365d`
- Custom range: `start_date` / `end_date` (YYYY-MM-DD) overrides `period`

Historical queries return daily data points with a `date` column.

## Cross-Entity Analysis

Compare across entity types using parallel tool calls:

- "ETH price vs Ethereum TVL" -> `defillama:get_token_prices` + `defillama:get_chain_metrics`
- "Aave TVL vs AAVE token price" -> `defillama:get_protocol_metrics` + `defillama:get_token_prices`
- "Lending vs DEX category" -> two `defillama:get_category_metrics` calls in parallel

## Examples

**Example 1:**
User: "Most undervalued DeFi protocols by P/S ratio"
Tool call: `defillama:get_protocol_metrics(sort_by: "ps_ratio asc", limit: 20, metrics: ["tvl_base", "revenue_1d", "ps_ratio", "mcap"])`

**Example 2:**
User: "Which protocols grew TVL most in last 30 days?"
Tool call: `defillama:get_protocol_metrics(sort_by: "tvl_base_30d_pct_change desc", limit: 10, metrics: ["tvl_base", "tvl_base_30d_pct_change"])`

**Example 3:**
User: "Compare Aave and Compound fees"
Tool call: `defillama:get_protocol_metrics(protocol: ["aave", "compound-v3"], metrics: ["tvl_base", "fees_1d", "revenue_1d"])`

**Example 4:**
User: "Compare Lending vs DEX fees and TVL"
Tool call: `defillama:get_category_metrics(category: ["Lending", "DEX"], metrics: ["tvl_base", "fees_1d", "revenue_1d"])`

**Example 5:**
User: "Aave TVL trend over 90 days"
Tool call: `defillama:get_protocol_metrics(protocol: "aave", metrics: ["tvl_base"], period: "90d")`

**Example 6:**
User: "Aave fees in Q1 2025"
Tool call: `defillama:get_protocol_metrics(protocol: "aave", metrics: ["fees_1d"], start_date: "2025-01-01", end_date: "2025-03-31")`

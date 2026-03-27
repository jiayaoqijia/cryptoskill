---
name: defi-data
description: Core reference for DefiLlama MCP tools. Maps DeFi questions to the correct tool call with proper parameters. Covers entity conventions, metric interpretation, stock vs flow distinctions, percentage formatting, and error recovery. Use whenever querying DeFi data — protocol TVL, token prices, chain metrics, fees, revenue, yields, stablecoins, bridges, ETFs, hacks, raises, treasuries, or institutional holdings.
---

# DefiLlama MCP Data Reference

## Tool Quick Reference

| Question | Tool | Key Params |
|----------|------|------------|
| Total DeFi TVL, global volumes | `defillama:get_market_totals` | `metrics` (tvl_base, volume_dexs_1d, etc.) |
| Protocol TVL, fees, revenue | `defillama:get_protocol_metrics` | `protocol`, `metrics` |
| Chain TVL, gas fees, REV | `defillama:get_chain_metrics` | `chain`, `metrics` |
| Token price, mcap, ATH | `defillama:get_token_prices` | `token` |
| Category rankings | `defillama:get_category_metrics` | `category` |
| Pool APY, lending rates | `defillama:get_yield_pools` | `token`, `chain`, `category` |
| Stablecoin supply | `defillama:get_stablecoin_supply` | `stablecoin`, `chain` |
| ETF inflows/outflows | `defillama:get_etf_flows` | `token` (bitcoin/ethereum) |
| Bridge volume | `defillama:get_bridge_flows` | `bridge`, `chain` |
| CEX volume | `defillama:get_cex_volumes` | `cex` |
| Open interest | `defillama:get_open_interest` | `protocol`, `chain` |
| Hacks/exploits | `defillama:get_events` | `event_type: "hacks"` |
| Fundraising | `defillama:get_events` | `event_type: "raises"` |
| Protocol events | `defillama:get_events` | `event_type: "protocol_events"` |
| Protocol treasury | `defillama:get_treasury` | `treasury` |
| Institutional holdings | `defillama:get_dat_holdings` | `institution`, `token` |
| Token unlocks | `defillama:get_token_unlocks` | `token`, `query_type` (chart, window, day, window_all, ratio, market_window) |
| Token TVL in protocols | `defillama:get_token_tvl` | `token`, `protocol` |
| Oracle coverage | `defillama:get_oracle_metrics` | `oracle` |
| User activity | `defillama:get_user_activity` | `protocol`, `chain` |
| Income statement | `defillama:get_income_statement` | `protocol` |
| Protocol metadata, URLs, audit | `defillama:get_protocol_info` | `protocol`, `category`, `tag`, `has_token`, `chain` |
| Chain metadata, type, L2 parent | `defillama:get_chain_info` | `chain`, `chain_type` |
| List valid categories | `defillama:list_categories` | `type` (protocol, token, chain) |
| Unknown entity slug | `defillama:resolve_entity` | `name` |

## Entity Conventions

- **Protocols**: lowercase-hyphenated slugs (`aave`, `uniswap`, `compound-v3`)
- **Chains**: lowercase (`ethereum`, `solana`, `arbitrum`)
- **Tokens**: `coingecko:` prefix (`coingecko:ethereum`, `coingecko:bitcoin`, `coingecko:usd-coin`)
- **CEX**: slug includes suffix (`binance-cex`, `coinbase-cex`, `htx`, `gate-io`)
- **Categories**: Title case (`Lending`, `DEX`, `Derivatives`)

## Protocol vs Sub-Protocol

Many protocols have multiple versions. The database tracks both:
- **Parent protocol** (e.g., `aave`) — used in `get_protocol_metrics`, aggregates all versions
- **Sub-protocol** (e.g., `aave-v3`) — individual versions, used in sub_protocol views

`resolve_entity` returns both `slug` (sub-protocol) and `parent_protocol`. Use `parent_protocol` for `get_protocol_metrics`. Use `slug` when you need a specific version.

Example: resolve_entity({name: "compound"}) returns:
- slug: compound-v2, parent_protocol: compound
- slug: compound-v3, parent_protocol: compound
→ Use `protocol: "compound"` in get_protocol_metrics for the aggregate.

## Array Support

All entity params accept single values or arrays for comparison:
- `protocol: "aave"` or `protocol: ["aave", "lido", "compound"]`
- `chain: "ethereum"` or `chain: ["ethereum", "solana"]`
- `token: "coingecko:ethereum"` or `token: ["coingecko:ethereum", "coingecko:bitcoin"]`

## Entity Resolution

Try tools directly for well-known entities — works 80%+ of the time. Use `defillama:resolve_entity` only when:

- Unsure of exact slug
- Tool returns 0 rows
- Need to disambiguate (e.g., "compound" → compound-v2, compound-v3)
- Need to find the parent_protocol slug

## Period Parameter

All tools accept `period` (NOT `time_range`):

- `current` (default) -- latest snapshot
- `7d`, `30d`, `90d`, `180d`, `365d` -- rolling windows

For custom date ranges, use `start_date` and `end_date` (YYYY-MM-DD format) instead of `period`. If `start_date` is set without `end_date`, it defaults to today.

## Critical Conventions

### Stock vs Flow

Different aggregation rules -- getting this wrong produces nonsensical results:

- **Stock** (point-in-time snapshots): `tvl`, `price`, `mcap` -- NEVER sum across dates
- **Flow** (cumulative over period): `fees_1d`, `revenue_1d`, `volume` -- CAN sum across dates

### Percentage Formatting

Two different conventions in the data:

- `*_pct_change` columns = **decimals** (e.g., -0.13 = -13%, 0.35 = +35%). Multiply by 100 for display.
- `apy` columns = **already percentages** (e.g., 2.32 = 2.32%). Do NOT multiply by 100.

### TVL Components

Components are mutually exclusive -- never double-add:

- `tvl_base` = default TVL (excludes liquid staking and double-counted)
- `tvl_ls_only` = liquid staking portion not in tvl_base
- `tvl_dc_only` = double-counted portion not in tvl_base
- `tvl_ls_and_dc` = both LS and DC
- Total with LS+DC = `tvl_base + tvl_ls_only + tvl_dc_only + tvl_ls_and_dc`

### Fee and Revenue

- `fees` = gross payments by users
- `revenue` = protocol's cut (fees - payments to LPs/stakers)
- `holder_revenue` = buybacks + dividends to token holders
- Chain-level: `chain_fees` (gas), `chain_revenue`, `chain_mev`, `app_fees` (protocol fees on chain), `app_revenue`

### Metric Name Patterns

Protocol metrics follow these patterns:
- **TVL**: `tvl_base`, `tvl_staking`, `tvl_borrowed`, `tvl_pool2`, `tvl_treasury`, `tvl_vesting`
- **Flows** (with suffixes `_1d/_7d/_30d/_90d/_180d/_365d/_ytd/_alltime/_annualised`): `fees`, `revenue`, `holder_revenue`, `incentive`
- **Volume** (same suffixes): `volume_dexs`, `volume_aggregators`, `volume_derivatives`, `volume_aggr_derivatives`, `volume_options`
- **Market**: `price`, `mcap`, `fdv`, `fdv_outstanding`, `token_volume`, `ps_ratio`, `pf_ratio`
- **pct_change** variants only available on `_current` views

Chain metrics use `chain_fees`, `chain_revenue`, `chain_mev`, `app_fees`, `app_revenue` instead of `fees`, `revenue`.

Daily views only have the `_1d` suffix for flows/volumes.

### Important Gotchas

- **Category column**: `get_protocol_metrics` has NO category column. Use `get_category_metrics` for category-level data.
- **FDV**: Never sort by FDV -- unreliable `total_supply` data produces junk rankings. Sort by `mcap` instead.
- **Valuation**: `ps_ratio` = mcap / annualised revenue. `pf_ratio` = mcap / annualised fees. Lower = potentially undervalued.
- **Metric validation**: Protocol/chain/category metrics are validated against actual DB columns. Invalid metrics return a suggestion for the closest match.
- **NULL values**: NULL means data unavailable, NOT $0. Do not report NULL as zero.
- **Params accept string or array**: `protocol: "aave"` or `protocol: ["aave", "lido"]`. Param names are singular (`protocol` not `protocols`).
- **sort_by format**: String like `"tvl_base desc"` or `"fees_1d desc"`.

## Examples

**Example 1:**
User: "What is Aave's TVL?"
Tool call: `defillama:get_protocol_metrics(protocol: "aave", metrics: ["tvl_base"])`

**Example 2:**
User: "Top 5 chains by fees"
Tool call: `defillama:get_chain_metrics(sort_by: "chain_fees_1d desc", limit: 5)`

**Example 3:**
User: "ETH price history over 90 days"
Tool call: `defillama:get_token_prices(token: "coingecko:ethereum", period: "90d")`

**Example 4:**
User: "Compare ETH price and Ethereum chain TVL"
Tool calls in parallel:
- `defillama:get_token_prices(token: "coingecko:ethereum")`
- `defillama:get_chain_metrics(chain: "ethereum")`

**Example 5:**
User: "Biggest DeFi hacks this year"
Tool call: `defillama:get_events(event_type: "hacks", sort_by: "amount desc", limit: 10, period: "365d")`

**Example 6:**
User: "Aave TVL from Jan to Mar 2025"
Tool call: `defillama:get_protocol_metrics(protocol: "aave", metrics: ["tvl_base"], start_date: "2025-01-01", end_date: "2025-03-31")`

## Error Recovery

1. **0 rows returned** -> call `defillama:resolve_entity(name: "...")` -> retry with the correct slug
2. **Wrong data** -> verify you're using the right tool (protocol vs chain vs category)
3. **Ambiguous entity** -> call `resolve_entity` to see all matching slugs, then pick the right one

---
name: defi-market-overview
description: >
  Broad DeFi market overview combining category rankings, chain comparison,
  total TVL trends, top protocols, and market events. Use when the user asks
  for a market summary, "what's happening in DeFi", weekly recap, overall
  market state, DeFi dashboard, or wants a high-level snapshot of the
  ecosystem.
---

# DeFi Market Overview

Produce a high-level snapshot of the entire DeFi ecosystem by pulling
data across categories, chains, protocols, events, stablecoins, and
institutional flows.

## Workflow

### Step 1 - Global market totals

Get the aggregate DeFi TVL, total DEX volume, and derivatives volume.

```
defillama:get_market_totals
  metrics: ["tvl_base", "tvl_base_7d_pct_change", "volume_dexs_1d", "volume_derivatives_1d"]
```

This is a single-row global snapshot. NO fees/revenue here — those come from category/chain views.

### Step 2 - Category metrics

Get the top DeFi categories ranked by TVL and fees.

```
defillama:get_category_metrics
```

This shows which sectors (DEXes, lending, liquid staking, etc.) are
leading the market.

### Step 3 - Top chains

Fetch the leading chains by TVL.

```
defillama:get_chain_metrics
  limit: 10
```

### Step 4 - Top protocols

Fetch the leading protocols by TVL.

```
defillama:get_protocol_metrics
  limit: 10
```

### Step 5 - Recent security incidents

Check for recent hacks or exploits.

```
defillama:get_events
  event_type: "hacks"
```

### Step 6 - Recent fundraises

Check for recent funding rounds and investments.

```
defillama:get_events
  event_type: "raises"
```

### Step 7 - Stablecoin supply

Get total stablecoin market and top stablecoins.

```
defillama:get_stablecoin_supply
```

Stablecoin supply growth is a proxy for capital entering the crypto
ecosystem.

### Step 8 - ETF flows

Check recent institutional activity through ETFs.

```
defillama:get_etf_flows
```

## Output Format

Present the report with these sections in order:

1. **Market Snapshot** - Two to three sentence summary of the current
   DeFi market state: total TVL direction, dominant narrative, and
   sentiment signal.
2. **Category Breakdown** - Top 5-7 categories by TVL with fees and
   percentage changes. Note which categories are gaining or losing share.
3. **Top Chains** - Top 10 chains by TVL with percentage changes.
   Highlight chains with the strongest momentum.
4. **Top Protocols** - Top 10 protocols by TVL with category, chain,
   and recent trend.
5. **Recent Events** - Split into Security Incidents and Fundraises.
   Summarize the most notable items from each.
6. **Capital Flows** - Stablecoin supply trend and ETF flow direction.
   These together indicate whether capital is entering or leaving crypto.

## Tips

- If total stablecoin supply is growing + ETF flows are positive +
  TVL is rising, this is a strong bull signal.
- Categories gaining TVL share indicate where market attention is
  rotating.
- Multiple hacks in a short period may dampen overall market sentiment.
- Large fundraises signal where VCs see future growth.
- Compare chain TVL rankings to previous periods to spot chains that
  are rising or falling in the rankings.
- Use `start_date` / `end_date` params for custom time windows (e.g.,
  weekly or monthly recaps) instead of fixed periods.

---
name: chain-ecosystem
description: >
  Full blockchain ecosystem analysis covering TVL, top protocols, bridge flows,
  stablecoin supply, DEX volume, fees, and user activity on a chain. Use when
  the user asks about a blockchain's ecosystem, "what's happening on Solana",
  chain health, or a chain-level overview.
---

# Chain Ecosystem Analysis

Produce a comprehensive overview of a blockchain ecosystem by combining
chain-level metrics with protocol, bridge, stablecoin, and user data.

## Workflow

### Step 1 - Resolve the chain entity

If the chain slug is unknown or ambiguous, resolve it first.

```
defillama:resolve_entity
  entity_type: "chain"
  name: "<user-provided name>"
```

### Step 2 - Chain-level metrics

Fetch aggregate TVL, fees, revenue, DEX volume, and trends.

```
defillama:get_chain_metrics
  chain: "<slug>"
```

Key fields: `tvl_base`, `chain_fees_1d`, `chain_revenue_1d`, `app_fees_1d`,
`volume_dexs_1d`, `tvl_base_7d_pct_change`, `tvl_base_30d_pct_change`.

### Step 3 - Top protocols on the chain

Identify the largest protocols by TVL on this chain.

```
defillama:get_protocol_metrics
  chain: "<slug>"
```

### Step 4 - Bridge flows

Measure capital entering and leaving the chain.

```
defillama:get_bridge_flows
  chain: "<slug>"
```

Positive net flow = capital inflow (bullish). Negative = outflow.

### Step 5 - Stablecoin supply

Assess stablecoin liquidity available on the chain.

```
defillama:get_stablecoin_supply
  chain: "<slug>"
```

### Step 6 - User activity

Fetch active addresses and transaction counts.

```
defillama:get_user_activity
  chain: "<slug>"
```

## Output Format

Present the report with these sections in order:

1. **Chain Overview** - Summary paragraph: what the chain is known for,
   current positioning in the market.
2. **Key Metrics** - Table of TVL, fees, revenue, DEX volume, and
   percentage changes.
3. **Top Protocols** - Top 5-10 protocols by TVL with category and TVL.
4. **Bridge Activity** - Net flows, top bridges, inflow vs outflow breakdown.
5. **Stablecoin Liquidity** - Total stablecoin supply on chain, top
   stablecoins, and trend direction.
6. **User Activity** - Active addresses, transaction counts, growth trends.

## Tips

- Rising stablecoin supply + positive bridge flows = capital accumulating
  on chain (bullish signal).
- Compare chain metrics to the previous period to identify momentum.
- If a single protocol dominates TVL (>50%), note the concentration risk.
- DEX volume relative to TVL indicates capital efficiency.
- Use `start_date` / `end_date` for custom date ranges when analyzing
  specific periods (e.g., `start_date: "2025-01-01", end_date: "2025-03-31"`).

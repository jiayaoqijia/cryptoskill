---
name: token-research
description: >
  Comprehensive token analysis combining price, market cap, unlock schedule,
  DeFi deposits, and yield opportunities. Use when the user asks to analyze a
  token, research a token, check token fundamentals, or wants full token
  intelligence including vesting and DeFi usage.
---

# Token Research

Perform end-to-end token analysis by combining price data, unlock schedules,
DeFi deposit tracking, yield opportunities, and protocol fundamentals.

## Workflow

### Step 1 - Resolve the token entity

Get the canonical token identifier (coingecko:xxx format).

```
defillama:resolve_entity
  entity_type: "token"
  name: "<user-provided name>"
```

### Step 2 - Price and market data

Fetch current price, market cap, volume, and ATH.

```
defillama:get_token_prices
  token: "<coingecko:token_id>"
```

Key fields: `price`, `mcap`, `volume`, `price_ath`. Distance from ATH can be computed as `(price_ath - price) / price_ath`.

### Step 3 - Unlock schedule

Check vesting and upcoming token unlocks that may create sell pressure.

```
defillama:get_token_unlocks
  token: "<token_name>"
```

Flag any large unlocks in the next 30 days as potential sell pressure.

### Step 4 - DeFi deposits

See where the token is deposited across DeFi protocols.

```
defillama:get_token_tvl
  token: "<coingecko:token_id>"
```

Uses `dim.token_set()` for family resolution (e.g., `coingecko:ethereum`
matches ETH, wETH, stETH, etc.). The `component` param filters by TVL
type (base, borrowed, staking, pool2, treasury, vesting). Quality
filters (`is_distressed`, `has_misrepresented_tokens`) are applied.

This shows which protocols hold the most of this token, indicating
DeFi demand and utility.

### Step 5 - Yield opportunities

Find pools where users can earn yield on this token.

```
defillama:get_yield_pools
  token: "<coingecko:token_id>"
```

The `token` param expects canonical keys (e.g., `coingecko:ethereum`).
Uses `dim.pool_set()` for family matching.

### Step 6 - Protocol fundamentals (if applicable)

If the token belongs to a DeFi protocol, fetch protocol metrics.

```
defillama:get_protocol_metrics
  protocol: "<protocol_slug>"
```

## Output Format

Present the report with these sections in order:

1. **Price & Market** - Current price, market cap, 24h volume, distance
   from ATH, and recent trend.
2. **Unlock Schedule** - Upcoming unlocks with dates, amounts, and
   percentage of circulating supply. Highlight any cliff unlocks.
3. **DeFi Deposits** - Top protocols holding this token, total value
   deposited, and what this implies about utility.
4. **Yield Opportunities** - Top 3-5 pools by APY and TVL where users
   can deploy this token.
5. **Protocol Fundamentals** - If the token is a protocol governance or
   utility token, include TVL, fees, revenue, and valuation ratios.

## Tips

- Large unlocks (>2% of circulating supply) within 30 days are a
  material risk factor.
- High DeFi deposits relative to circulating supply indicate strong
  holder conviction and reduced liquid supply.
- Compare yield APY sources: base APY from fees is sustainable, reward
  APY from token emissions is not.
- If the token has no unlock data, it may be fully unlocked or the data
  may not be tracked - note this to the user.
- Use `start_date` / `end_date` for custom date ranges on price and TVL
  queries.

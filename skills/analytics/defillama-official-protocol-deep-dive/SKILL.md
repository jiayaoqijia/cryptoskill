---
name: protocol-deep-dive
description: >
  Comprehensive single-protocol analysis combining TVL, fees, revenue, yields,
  events, income, and user activity. Produces a full protocol report. Use when
  the user asks for a complete overview, deep dive, "tell me everything about"
  a protocol, or a protocol research report.
---

# Protocol Deep Dive

Perform a thorough analysis of a single DeFi protocol by combining multiple
data sources into one structured report.

## Workflow

### Step 1 - Resolve the protocol entity

If the protocol slug is unknown or ambiguous, resolve it first.

```
defillama:resolve_entity
  entity_type: "protocol"
  name: "<user-provided name>"
```

### Step 2 - Core protocol metrics

Fetch TVL, fees, revenue, market cap, ratios, and trend data.

```
defillama:get_protocol_metrics
  protocol: "<slug>"
```

Key fields to surface: `tvl_base`, `fees_1d`, `revenue_1d`, `mcap`,
`ps_ratio`, `pf_ratio`, `tvl_base_7d_pct_change`, `tvl_base_30d_pct_change`.

### Step 3 - Top yield pools

Retrieve the protocol's highest-TVL pools to show yield opportunities.

```
defillama:get_yield_pools
  protocol: "<slug>"
```

Highlight pools with the highest TVL and APY. Note any pools where the
base APY is very low and rewards dominate (sustainability signal).

### Step 4 - Recent events

Check for hacks, fundraises, or other notable events.

```
defillama:get_events
  protocol: "<slug>"
  event_type: "hacks"
```

Also check for fundraising activity:

```
defillama:get_events
  protocol: "<slug>"
  event_type: "raises"
```

### Step 5 - Income statement

Get the revenue breakdown to understand where income comes from.

```
defillama:get_income_statement
  protocol: "<slug>"
```

Use the `metric` param to filter by specific income line items if needed.

### Step 6 - User activity

Fetch daily active users and transaction counts.

```
defillama:get_user_activity
  protocol: "<slug>"
```

### Step 7 - Token price (if applicable)

If the protocol has a native token, fetch current price context.

```
defillama:get_token_prices
  token: "<coingecko:token_id>"
```

## Output Format

Present the report with these sections in order:

1. **Overview** - One-paragraph summary: what the protocol does, which
   chain(s) it operates on, its category.
2. **Key Metrics** - Table of TVL, fees, revenue, mcap, P/S, P/F, and
   percentage changes (7d, 30d).
3. **Yield Opportunities** - Top 3-5 pools by TVL with chain, APY, and TVL.
4. **Revenue Breakdown** - Where income comes from (supply-side vs protocol).
5. **User Growth** - Active users trend, transaction volume.
6. **Recent Events** - Hacks, raises, governance events.
7. **Token Performance** - Price, market cap, volume, ATH distance.

## Tips

- If `get_income_statement` returns no data, skip the Revenue Breakdown
  section rather than showing empty results.
- Compare P/S and P/F ratios to category averages when possible.
- Flag declining TVL + declining users as a bearish signal.
- Flag growing TVL + growing users + growing revenue as strong fundamentals.
- Use `start_date` / `end_date` for custom date ranges when analyzing
  specific periods.

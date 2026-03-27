---
name: institutional-crypto
description: >
  Institutional and TradFi crypto exposure analysis covering public company
  holdings (MicroStrategy, Tesla, etc.), Bitcoin and Ethereum ETF flows, and
  institutional accumulation patterns. Use when the user asks about
  institutional adoption, ETF flows, corporate treasuries, what institutions
  are buying, or MicroStrategy holdings.
---

# Institutional Crypto Analysis

Analyze institutional and TradFi exposure to crypto by combining corporate
holdings data, ETF flow data, and price context.

## Workflow

### Step 1 - Corporate and institutional holdings

Fetch public companies and institutions that hold crypto on their balance
sheets, including market-to-NAV ratios.

```
defillama:get_dat_holdings
  include_mnav: true
```

Key fields: `institution_slug`, `token`, `amount`, `holding_usd_value`, `mNAV`.

Sort by value to show the largest holders. Note any entities trading at
a significant premium or discount to NAV (mNAV far from 1.0).

### Step 2 - Bitcoin ETF flows

Get recent BTC ETF inflow and outflow data.

```
defillama:get_etf_flows
  token: "bitcoin"
```

Positive flows = net buying. Negative flows = net selling.

### Step 3 - Ethereum ETF flows

Get recent ETH ETF inflow and outflow data.

```
defillama:get_etf_flows
  token: "ethereum"
```

### Step 4 - Price context

Fetch current BTC and ETH prices to contextualize the flows.

```
defillama:get_token_prices
  token: ["coingecko:bitcoin", "coingecko:ethereum"]
```

## Output Format

Present the report with these sections in order:

1. **Institutional Holdings** - Top holders ranked by USD value. Include
   entity name, token held, amount, value, and mNAV. Call out any
   notable changes or premium/discount to NAV.
2. **Bitcoin ETF Flows** - Recent daily/weekly flows, cumulative AUM,
   and trend direction. Name the top ETFs by flow.
3. **Ethereum ETF Flows** - Same structure as BTC ETFs.
4. **Price Context** - Current BTC and ETH prices, helping the user
   understand the dollar magnitude of flows.
5. **Key Takeaways** - Summarize whether institutional appetite is
   growing or shrinking, and any notable patterns.

## Tips

- Sustained positive ETF flows alongside rising price = strong
  institutional demand.
- An entity with mNAV >> 1 is trading at a premium to its crypto
  holdings (e.g., MicroStrategy often trades above NAV).
- Compare weekly ETF flows to previous weeks to identify acceleration
  or deceleration in institutional buying.
- Negative ETF flows during price dips may indicate profit-taking
  rather than loss of conviction if flows resume quickly.
- Use `start_date` / `end_date` for custom date ranges when analyzing
  specific periods (e.g., `start_date: "2025-01-01", end_date: "2025-03-31"`).

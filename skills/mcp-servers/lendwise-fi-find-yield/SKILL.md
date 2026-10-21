---
description: Find and compare DeFi lending yields and optimize an allocation using the Lendwise tools. Use when the user asks where to place stablecoins or crypto for yield, which lending market has the best APY, how stable a market's rate is over months, or how to split an amount across markets — across Aave, Morpho, Compound and Blend (Stellar).
---

# Finding DeFi yield with Lendwise

The `lendwise` MCP server exposes five read-only tools over live Aave / Morpho / Compound / Blend data. It compares markets; it never signs a transaction. Every answer is informational, **not financial advice** — say so.

Work in this order, and never invent a filter value.

1. **`list_market_universe`** first. It returns the assets, chains and protocols that actually exist, with counts. Take every filter value (asset symbol, `chainId`, protocol) from here — not from memory. An asset that isn't listed won't return anything.
2. **`find_best_markets`** with the user's asset (e.g. `USDC`). Returns the current top markets ranked by net APY, filtered and sorted server-side. It defaults to markets with ≥ $1M TVL; keep that floor unless the user explicitly wants thinner markets — a thin market's headline APY is mostly noise, and steering someone into one is the main real-world harm here.
3. **`get_market_history`** on the top 3–5 candidates, `range: "180d"` for a multi-month horizon. Compare mean against stddev: a durable 6% beats a 12% that's a reward programme ending next week. This is the number a long-horizon decision actually turns on.
4. **`optimize_allocation`** with `amountUsd` and the chosen `productIds` to get per-market dollar amounts, the blended APY and a projected yield. Higher `diversification` (default 80) spreads risk; 0 concentrates in the top yield.

Always report the snapshot freshness (`asOf`) and flag any row marked `reliable: false` rather than presenting it as fact. Close with a brief not-financial-advice note: APYs are variable and past yields don't predict future returns.

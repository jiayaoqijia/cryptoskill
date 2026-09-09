---
name: hyperliquid
description: "Read live Hyperliquid mainnet data via the ChainGPT plugin. Markets / mids / orderbook / wallet account state / fills / funding-rate history. Use for perp position monitoring, market scanning, account auditing, and funding-rate analysis. Read-only in v1.6 — signed order placement (EIP-712 L1 actions) is a follow-up. Triggers: hyperliquid, hl, perps, perpetual, funding rate, orderbook, my positions on hyperliquid, leverage trading, BTC perp, ETH perp."
---

# ChainGPT Hyperliquid Skill

You read live Hyperliquid data on behalf of the user. **v1.6 is read-only.** Signed order placement (post `POST /exchange` with EIP-712 L1-actions signatures) is intentionally deferred to a follow-up release.

## What this skill can do today

| Tool | Purpose |
|---|---|
| `chaingpt_hl_markets` | Enumerate the perp or spot universe (asset, max leverage, decimals) |
| `chaingpt_hl_mids` | Get live mid prices for all assets in one call |
| `chaingpt_hl_orderbook` | L2 orderbook for a specific asset |
| `chaingpt_hl_account` | Full account state for a wallet — value / margin / positions / leverage / liquidation prices |
| `chaingpt_hl_fills` | Recent fill history with side / size / price / PnL per fill |
| `chaingpt_hl_funding` | Funding-rate history (hourly) for a perp, with auto-annualized rate at the bottom |

## Common workflows

### "How are my Hyperliquid positions doing?"

```text
chaingpt_hl_account  user="0x…"
```

Returns account value, total margin used, every open position with side/size/entry/unrealized-PnL/leverage/liquidation price.

### "Is the BTC funding rate elevated?"

```text
chaingpt_hl_funding  coin="BTC" hours=24
```

Last 24 hours of hourly funding. Look at the trend and the annualized rate at the bottom. Above ~50% annualized signals overheated long bias; below 0 signals shorts pay.

### "What's the spread on SOL right now?"

```text
chaingpt_hl_orderbook  coin="SOL" depth=10
```

Top 10 levels each side. Compare top-bid vs top-ask for spread; top-bid-size + top-ask-size for liquidity at the touch.

### "Show me everything trading on Hyperliquid"

```text
chaingpt_hl_markets type="perp"
chaingpt_hl_mids
```

Combine: take the asset list from `_markets`, the prices from `_mids`. The two calls cover the whole universe with minimal payload.

## What this skill does NOT do (yet)

- **Place orders** — coming in a follow-up. Will use the custody-free pattern: plugin returns the action payload + EIP-712 typed data; user signs externally and submits via a separate `chaingpt_hl_submit_signed_action` tool.
- **Cancel orders** — same constraint as place.
- **Modify leverage** or transfer between perp / spot / vault — same constraint.
- **Subaccount management** — Hyperliquid supports vault-style subaccounts; not exposed in v1.6.

## When to use this skill vs. the others

- For research / monitoring on Hyperliquid specifically — use this skill.
- For DEX swaps on EVM mainnets — use `chaingpt-trade`.
- For lending / staking — use `chaingpt-defi`.
- For market-data research outside Hyperliquid (token prices on Ethereum / Solana / etc.) — use `chaingpt-research`.

## Credit accounting

All Hyperliquid reads cost 0 ChainGPT credits — the API is free. The credit funnel comes from upstream calls (research, news, signals, audit) the user makes around Hyperliquid trading decisions.

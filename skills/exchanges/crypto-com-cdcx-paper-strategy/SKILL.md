---
name: cdcx-paper-strategy
description: Local paper trading — test strategies against live market prices without risking real funds. CLI-only, no auth, no MCP tools.
---

# Paper Trading

## When to Use

- Validate a strategy before going live
- Experiment with order sizing and timing
- Teach/demo cdcx without risking funds
- Regression-test an agent's trading behaviour

**CLI-only.** Paper trading has no MCP tools — agents that need to paper trade must shell out to `cdcx paper` directly.

## Engine

The paper engine is local (no API calls for order state — only for market prices). State lives in `~/.local/share/cdcx/paper/paper_account.json`.

Fills use live mark prices fetched from the REST API at the moment the order is evaluated:
- MARKET orders fill immediately at the current ticker price
- LIMIT orders sit and fill when the market crosses the limit

## Commands

| Command | Purpose |
|---------|---------|
| `cdcx paper init --balance <n>` | Create a new paper account (default 10000 USDT) |
| `cdcx paper buy <INSTRUMENT> --quantity <q> [--price <p>]` | Buy (market if no price) |
| `cdcx paper sell <INSTRUMENT> --quantity <q> [--price <p>]` | Sell |
| `cdcx paper positions` | Open positions with unrealized P&L |
| `cdcx paper balance` | Cash balance + realized P&L |
| `cdcx paper history` | Fills log |
| `cdcx paper reset --balance <n>` | Wipe state and start fresh |

All commands support `-o json`, `-o table`, `-o ndjson`.

## Workflow

### Bootstrap

```
cdcx paper init --balance 50000
cdcx paper balance -o json
```

### Market Trade (round trip)

```
# 1. Check current price
cdcx market ticker BTC_USDT -o json

# 2. Paper buy
cdcx paper buy BTC_USDT --quantity 0.01 -o json

# 3. Inspect open position
cdcx paper positions -o json

# 4. Close
cdcx paper sell BTC_USDT --quantity 0.01 -o json

# 5. Realized P&L shows up in balance
cdcx paper balance -o json
```

### Limit Order (patient entry)

```
cdcx paper buy BTC_USDT --quantity 0.1 --price 49000 -o json
```

The limit sits in the paper engine until the market ticker crosses 49000. Check back with `cdcx paper positions` — until filled, the cash is reserved.

### Strategy Backtest Loop

```
# Bootstrap
cdcx paper init --balance 100000

# Loop (external script / agent):
#   1. Read signal from cdcx market ticker / candlestick
#   2. Issue cdcx paper buy or cdcx paper sell accordingly
#   3. Call cdcx paper positions -o json to track running P&L

# Review
cdcx paper history -o json
cdcx paper balance -o json
```

### Reset Between Runs

```
cdcx paper reset --balance 100000
```

Wipes all positions, trades, and P&L; starts fresh with the specified balance.

## Notes

- Paper state persists across `cdcx` invocations — use `reset` to start fresh
- No fees are deducted by default — add them in your strategy if you want realism
- Live streaming ticker is not wired into the paper engine; orders are evaluated on subsequent `cdcx paper` invocations using the then-current REST ticker
- For an interactive paper experience use `cdcx tui` and press `p` to toggle LIVE/PAPER mode

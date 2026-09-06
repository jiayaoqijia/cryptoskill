---
name: crypto-com-exchange
description: Trade on Crypto.com Exchange — market data, spot/derivatives orders, portfolio management, wallet operations. Uses cdcx CLI for execution with built-in auth, safety tiers, and dry-run.
metadata:
  version: 2.0.0
  author: Crypto.com
  openclaw:
    requires:
      bins: [cdcx]
    install:
      - kind: node
        package: '@cryptocom/cdcx-cli'
        bins: [cdcx]
        label: Install cdcx CLI (npm)
license: MIT
---

# Crypto.com Exchange Skill

Trade on Crypto.com Exchange using the `cdcx` CLI. Covers spot, derivatives, advanced orders, portfolio, and wallet operations.

## Prerequisites

1. Install: `npx @cryptocom/cdcx-cli@latest` or see [references/install.md](./references/install.md)
2. Authenticate: run `cdcx auth login --oauth` — opens browser for OAuth, no manual key entry needed
3. Verify: `cdcx account summary -o json`

If `cdcx account summary` fails with "No credentials found", immediately execute `cdcx auth login --oauth` via Bash (with ~120s timeout for browser callback).


## Capabilities

| Domain | CLI Group | What It Does |
|--------|-----------|--------------|
| Market Data | `cdcx market` | Prices, orderbook, candles, trades, instruments — no auth needed |
| Order Execution | `cdcx trade` | Place/amend/cancel LIMIT and MARKET orders |
| Advanced Orders | `cdcx advanced` | OCO, OTO, OTOCO bracket orders with trigger logic |
| Portfolio | `cdcx account` | Balances, positions, sub-accounts, P&L |
| History | `cdcx history` | Order history, fills, transactions |
| Wallet | `cdcx wallet` | Deposits, withdrawals, network info |
| Margin | `cdcx margin` | Isolated margin transfers, leverage |
| Staking | `cdcx staking` | Stake/unstake, conversion, reward history |
| Fiat | `cdcx fiat` | Fiat deposit/withdrawal, bank accounts |
| Paper Trading | `cdcx paper` | Local simulation with live prices, no auth |
| Streaming | `cdcx stream` | Real-time WebSocket data (NDJSON) |

## Safety Model

Every command has a safety tier. The CLI enforces these automatically:

| Tier | Behavior | Examples |
|------|----------|----------|
| `read` | Runs freely | `cdcx market ticker`, `cdcx market book` |
| `sensitive_read` | Runs freely (auth required) | `cdcx account summary`, `cdcx trade open-orders` |
| `mutate` | Requires `--yes` or MCP `acknowledged=true` | `cdcx trade order`, `cdcx trade amend` |
| `dangerous` | Requires `--allow-dangerous` on MCP server | `cdcx trade cancel-all`, `cdcx wallet withdraw` |

Always use `--dry-run` before live orders to preview the request.

## Quick Start

### Check Balance

```
cdcx account summary -o json
```

### Get Market Price

```
cdcx market ticker BTC_USDT -o json
```

### Place a Limit Order

```
# Preview first
cdcx trade order BUY BTC_USDT 0.01 --type LIMIT --price 50000 --dry-run -o json

# Execute
cdcx trade order BUY BTC_USDT 0.01 --type LIMIT --price 50000 --client-oid my-buy-001 -o json
```

### Place a Market Order

```
cdcx trade order BUY BTC_USDT 0.01 --type MARKET -o json
```

### Cancel an Order

```
cdcx trade cancel --order-id 123456789 -o json
cdcx trade cancel --client-oid my-buy-001 -o json
```

### Amend an Order

```
cdcx trade amend --order-id 123456789 --new-price 51000 --new-quantity 0.01 -o json
```

Both `--new-price` and `--new-quantity` are required — re-submit the original value for the field you don't want to change.

## Market Data (No Auth)

```
cdcx market ticker BTC_USDT -o json          # Current price
cdcx market ticker -o json                    # All instruments
cdcx market book BTC_USDT --depth 10 -o json  # Orderbook
cdcx market candlestick BTC_USDT --timeframe 1h --count 24 -o json  # OHLCV
cdcx market trades BTC_USDT -o json           # Recent prints
cdcx market instruments -o json               # All tradable pairs + tick sizes
```

Supported timeframes: `1m, 5m, 15m, 30m, 1h, 4h, 6h, 12h, 1D, 7D, 14D, 1M`

### Streaming (real-time)

```
cdcx stream ticker BTC_USDT ETH_USDT   # NDJSON to stdout
cdcx stream book BTC_USDT
cdcx stream trades BTC_USDT
```

## Order Execution

Positional args: `<side> <instrument> <quantity>`. Side is `BUY` or `SELL`.

```
# Limit order
cdcx trade order BUY BTC_USDT 0.01 --type LIMIT --price 50000 -o json

# Market order (buy by notional)
cdcx trade order BUY BTC_USDT --type MARKET --notional 500 -o json

# Batch (up to 10)
cdcx trade order-list --order-list '[
    {"instrument_name":"BTC_USDT","side":"BUY","type":"LIMIT","price":"49000","quantity":"0.01"},
    {"instrument_name":"BTC_USDT","side":"BUY","type":"LIMIT","price":"48000","quantity":"0.01"}
]' -o json

# List open orders
cdcx trade open-orders BTC_USDT -o json

# Close a position
cdcx trade close-position BTCUSD-PERP --type MARKET -o json
```

### Order Options

| Flag | Purpose |
|------|---------|
| `--type` | `LIMIT` or `MARKET` |
| `--price` | Limit price (string) |
| `--notional` | Spend amount in quote currency (MARKET BUY) |
| `--client-oid` | Your correlation ID (max 36 chars) |
| `--time-in-force` | `GOOD_TILL_CANCEL`, `FILL_OR_KILL`, `IMMEDIATE_OR_CANCEL` |
| `--exec-inst` | `POST_ONLY`, `SMART_POST_ONLY`, `REDUCE_ONLY`, `ISOLATED_MARGIN` |
| `--dry-run` | Preview without executing |

## Advanced Orders (OCO / OTO / OTOCO)

### OTOCO Bracket (entry + stop-loss + take-profit)

```
cdcx advanced create-otoco '[
    {"instrument_name":"BTC_USDT","side":"BUY","type":"LIMIT","price":"50000","quantity":"0.01"},
    {"instrument_name":"BTC_USDT","side":"SELL","type":"STOP_LOSS","trigger_price":"48000","quantity":"0.01","ref_price_type":"MARK_PRICE"},
    {"instrument_name":"BTC_USDT","side":"SELL","type":"TAKE_PROFIT","trigger_price":"55000","quantity":"0.01","ref_price_type":"MARK_PRICE"}
]' --dry-run -o json
```

### OTO (entry + protection)

```
cdcx advanced create-oto '[
    {"instrument_name":"BTC_USDT","side":"BUY","type":"LIMIT","price":"50000","quantity":"0.01"},
    {"instrument_name":"BTC_USDT","side":"SELL","type":"STOP_LOSS","trigger_price":"48000","quantity":"0.01","ref_price_type":"MARK_PRICE"}
]' -o json
```

### OCO (two-sided exit for existing position)

```
cdcx advanced oco '[
    {"instrument_name":"BTC_USDT","side":"SELL","type":"LIMIT","price":"55000","quantity":"0.01"},
    {"instrument_name":"BTC_USDT","side":"SELL","type":"STOP_LOSS","trigger_price":"48000","quantity":"0.01","ref_price_type":"MARK_PRICE"}
]' -o json
```

### Single Trigger Order

```
cdcx advanced order BTCUSD-PERP --side SELL --type STOP_LOSS --quantity 0.01 --trigger-price 48000 --ref-price-type MARK_PRICE -o json
```

### Manage Advanced Orders

```
cdcx advanced open-orders BTC_USDT -o json
cdcx advanced order-detail --order-id <id> -o json
cdcx advanced cancel-otoco --list-id <list_id> -o json
cdcx advanced cancel-oco --list-id <list_id> -o json
cdcx advanced cancel-oto --list-id <list_id> -o json
```

## Portfolio & Account

```
cdcx account summary -o json                # Cash balances
cdcx account positions -o json              # Open positions + unrealized P&L
cdcx account info -o json                   # Master + sub-accounts
cdcx account subaccount-balances -o json    # Per-sub-account
cdcx account balance-history --timeframe D1 -o json  # Equity curve

# Fee rates
cdcx trade fee-rate -o json
cdcx trade instrument-fee-rate --instrument-name BTC_USDT -o json

# History
cdcx history orders BTC_USDT --limit 50 -o json
cdcx history trades BTC_USDT --limit 50 -o json
cdcx history transactions --limit 100 -o json
```

## Wallet Operations

```
# Deposit
cdcx wallet networks -o json                        # Supported networks
cdcx wallet deposit-address BTC -o json             # Get address
cdcx wallet deposit-history -o json                 # Track arrivals

# Withdraw (dangerous tier)
cdcx wallet withdraw BTC 0.1 <ADDRESS> --network-id BITCOIN --dry-run -o json
cdcx wallet withdraw BTC 0.1 <ADDRESS> --network-id BITCOIN --client-wid my-wd-001 -o json
cdcx wallet withdrawal-history -o json
```

Withdrawals require whitelisted addresses (configured in Exchange web GUI).

## Isolated Margin

For instruments that require isolated margin (e.g. `SPYUSD-PERP`, `NVDAUSD-PERP`):

```
cdcx trade order BUY SPYUSD-PERP 0.001 --type LIMIT --price 710.25 --exec-inst ISOLATED_MARGIN -o json

# Fund/withdraw margin
cdcx margin transfer --direction IN --amount 100 <ISOLATION_ID>
cdcx margin transfer --direction OUT --amount 50 <ISOLATION_ID>

# Adjust leverage
cdcx margin leverage --leverage 5 <ISOLATION_ID>
```

Get `isolation_id` from `cdcx account positions -o json`.

## Paper Trading (No Auth)

```
cdcx paper init --balance 50000
cdcx paper buy BTC_USDT --quantity 0.01 -o json
cdcx paper sell BTC_USDT --quantity 0.01 -o json
cdcx paper positions -o json
cdcx paper balance -o json
cdcx paper history -o json
cdcx paper reset --balance 100000
```

## Recipes

### Morning Brief

```
cdcx market ticker -o json                          # Market snapshot
cdcx account summary -o json                        # Cash
cdcx account positions -o json                      # Open positions
cdcx trade open-orders -o json                      # Pending orders
cdcx advanced open-orders -o json                   # Advanced orders
cdcx history trades --start-time $(date -v-1d +%s)000 -o json  # Yesterday's fills
```

### Emergency Flatten

**Requires explicit user CONFIRM before execution — this cancels all orders and closes all positions at market.**

```
cdcx trade cancel-all --yes -o json                 # Cancel all orders
cdcx advanced cancel-all --yes -o json              # Cancel all advanced
cdcx account positions -o json | \
    jq -r '.data[].instrument_name' | \
    while read i; do cdcx trade close-position "$i" --type MARKET --yes; done
cdcx account positions -o json                      # Verify flat
```

## Important Notes

- Instrument names are case-sensitive: `BTC_USDT` not `btc_usd`. Spot uses `_` (e.g. `BTC_USDT`), perps use `-PERP` (e.g. `BTC-PERP`)
- Prices in the API are strings — cast to float/decimal before arithmetic
- `c` in ticker response is a ratio, not percentage: `0.0257` means +2.57%
- Always supply `--client-oid` for order correlation
- `close-position` is async — verify with `cdcx account positions` afterwards
- Advanced orders live in their own namespace — not visible in `cdcx trade open-orders`
- Batch max is 10 orders per call
- OTOCO structure: Leg 1 = entry LIMIT, Leg 2 = stop-loss trigger, Leg 3 = take-profit trigger
- OTO second leg must be a trigger type (STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT)
- `get-open-orders` has no pagination — returns ALL open orders
- Withdrawal amount is gross (fee deducted from it)
- For memo coins (XRP, XLM, EOS), always include `--address-tag`

## Agent Behavior

1. Always `--dry-run` before live orders on new strategies
2. Confirm with user before any `mutate` tier action in production — ask for "CONFIRM"
3. Never display full API secrets — mask credentials (first 5 + last 4 for key, last 5 only for secret)
4. Default to `--output json` for programmatic consumption
5. Use `cdcx market instruments` to verify tick sizes before placing orders
6. Check `cdcx account summary` for available balance before order placement
7. For streaming data, prefer `cdcx stream` over polling

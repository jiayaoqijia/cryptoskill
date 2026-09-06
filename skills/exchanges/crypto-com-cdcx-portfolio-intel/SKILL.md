---
name: cdcx-portfolio-intel
description: Read-only portfolio analysis — balances, positions, P&L, sub-accounts, fee rates, transaction history
---

# Portfolio Intelligence

## When to Use

- User asks "what's my balance" / "what do I hold" / "how much PnL"
- Portfolio report or daily wrap-up
- Sub-account overview
- Fee tier or transaction history lookup

Requires authentication (`CDCX_API_KEY`/`CDCX_API_SECRET` or a configured profile).

## Tools Used

| Tool                              | Purpose                                | Tier           |
|-----------------------------------|----------------------------------------|----------------|
| cdcx_account_summary              | Wallet balances (cash per currency)    | sensitive_read |
| cdcx_account_balance_history      | Historical balance snapshots           | sensitive_read |
| cdcx_account_positions            | Open positions with unrealized P&L     | sensitive_read |
| cdcx_account_info                 | Master account + sub-accounts          | sensitive_read |
| cdcx_account_subaccount_balances  | Per-sub-account balances               | sensitive_read |
| cdcx_trade_fee_rate               | Account fee tier                       | sensitive_read |
| cdcx_trade_instrument_fee_rate    | Instrument-specific fee rate           | sensitive_read |
| cdcx_account_orders               | Historical orders                      | sensitive_read |
| cdcx_account_trades               | Historical fills                       | sensitive_read |
| cdcx_account_transactions         | All transactions (fills, funding, etc) | sensitive_read |
| cdcx_market_ticker                | Mark prices for P&L valuation          | read           |

**Note:** MCP tool names beginning with `cdcx_account_orders`/`cdcx_account_trades`/`cdcx_account_transactions` correspond to the `history` schema group which the `account` MCP service group also exposes.

## Workflow

### Quick Balance Check

```
cdcx account summary -o json
```

Returns per-currency balance with `balance`, `available`, `reserved_qty`, `collateral_amount`.

### Full Portfolio Report

```
# 1. Cash
cdcx account summary -o json

# 2. Open positions (derivatives + margin)
cdcx account positions -o json

# 3. Mark prices for valuation
cdcx market ticker -o json
```

Combine: total equity = cash + Σ (position size × mark price) + Σ unrealized P&L. Break down by instrument; call out largest winners/losers.

### Position Detail for One Instrument

```
cdcx account positions BTCUSD-PERP -o json
```

### Historical Trades and Orders

```
cdcx history orders BTC_USDT --limit 50 -o json
cdcx history trades BTC_USDT --limit 50 -o json
cdcx history transactions --limit 100 -o json
```

Time windows via `--start-time` / `--end-time` (ms since epoch).

### Fee Analysis

```
cdcx trade fee-rate -o json                      # Account tier
cdcx trade instrument-fee-rate --instrument-name BTC_USDT -o json
```

Note: fee-rate commands live under `trade`, not `account`.

### Sub-Account Management

```
cdcx account info -o json                        # List master + sub-accounts
cdcx account subaccount-balances -o json         # Balances per sub-account
cdcx account subaccount-transfer \
    --from <sub_uuid_a> --to <sub_uuid_b> \
    --currency USDT --amount 1000                # Transfer (mutate)
```

`subaccount-transfer` is tier `mutate` — requires `acknowledged=true` in MCP mode.

### Balance History (Equity Curve)

```
cdcx account balance-history --timeframe D1 -o json
```

Returns daily snapshots for building an equity curve chart.

## Notes

- `account summary` shows cash; `account positions` shows open derivatives/margin positions — both are needed for a full equity view
- All read endpoints are safe to call repeatedly; no write effects
- `subaccount-transfer` moves real funds — treat as a mutate
- Fee-rate commands were moved to the `trade` group by the upstream API; don't expect them under `account`

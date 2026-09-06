---
name: cdcx-check-balance
description: Verify credentials and inspect account balance — the first action an agent takes before trading.
---

# Check Balance

## When to Use

- Confirm credentials work before any trading workflow
- Report current wallet balance to the user
- Script gating: "only trade if available USDT > X"

Requires authentication.

## Preflight

```
# Are credentials resolvable?
cdcx account info -o json > /dev/null 2>&1 && echo ok || echo "auth not configured"
```

If this fails, redirect the user to `cdcx setup` or the `cdcx-auth-setup` skill.

## Full Balance Snapshot

```
cdcx account summary -o json
```

Response shape (trimmed):

```json
{
  "data": {
    "total_available_balance": "10000.00",
    "total_margin_balance": "12500.00",
    "position_balances": [
      {
        "instrument_name": "USD_Stablecoin",
        "quantity": "12500.00",
        "market_value": "12500.00",
        "total_available_balance": "10000.00",
        "total_margin_balance": "12500.00",
        "total_position_value": "0.00"
      }
    ]
  }
}
```

The top-level `total_available_balance` and `total_margin_balance` are account-wide. Per-asset detail lives in `position_balances[]`.

## One-Currency Check

```
cdcx account summary -o json | \
    jq -r '.data.position_balances[] | select(.instrument_name=="BTC") | .quantity'
```

## Ergonomic Scripts

### Gate a trade on available USDT

```bash
available=$(cdcx account summary -o json | \
    jq -r '.data.total_available_balance // 0')

if awk -v a="$available" 'BEGIN{exit !(a+0 > 500)}'; then
    cdcx trade order BUY BTC_USDT 0.001 --type MARKET -o json
else
    echo "Insufficient USDT: $available"
fi
```

### Summary line

```bash
cdcx account summary -o json | jq -r '
    "Margin: \(.data.total_margin_balance) USD · Available: \(.data.total_available_balance) USD"'
```

### All currencies, one per line

```bash
cdcx account summary -o json | \
    jq -r '.data.position_balances[] | "\(.instrument_name): \(.quantity)"'
```

## Sub-Account Balances

```
cdcx account subaccount-balances -o json
```

Returns balances for every sub-account under the master — useful for multi-account ops.

## Notes

- `total_margin_balance` and `total_available_balance` are valued in USD; `position_balances[].quantity` is in the native currency
- The API schema uses `position_balances` for the per-currency breakdown even though the user-facing concept is "balances" — do not confuse this with derivatives *positions* (that's `cdcx account positions`)
- `cdcx account summary` is tier `sensitive_read` — no acknowledgement required in MCP mode

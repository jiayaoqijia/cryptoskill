---
name: cdcx-wallet-ops
description: Crypto wallet operations — deposits, withdrawals, network management. Withdrawal is tier-dangerous and requires extra gating.
---

# Wallet Operations

## When to Use

- Get a deposit address for a currency/network
- Initiate a withdrawal to a whitelisted address
- Query deposit or withdrawal history
- Look up supported networks for a currency

Requires authentication. Your API key must have **withdrawal permissions enabled** for `wallet withdraw` to work.

## Tools Used

| Tool                             | Purpose                               | Tier      |
|----------------------------------|---------------------------------------|-----------|
| cdcx_funding_deposit_address     | Generate/fetch deposit address        | sensitive_read |
| cdcx_funding_networks            | List supported networks per currency  | read      |
| cdcx_funding_deposit_history     | Past deposits                         | sensitive_read |
| cdcx_funding_withdrawal_history  | Past withdrawals                      | sensitive_read |
| cdcx_funding_withdraw            | Create a withdrawal request           | dangerous |
| cdcx_account_summary             | Available balance for a currency      | sensitive_read |

MCP service group name is **`funding`** (maps to CLI `wallet` group).

## Workflow

### Deposit (receive funds)

```
# 1. Find supported networks
cdcx wallet networks -o json

# 2. Get the deposit address
cdcx wallet deposit-address BTC -o json

# 3. Share the address + network with the sender
# 4. Poll for arrival
cdcx wallet deposit-history -o json
```

Always display both the address *and* the network to the user — sending on the wrong network loses the funds.

### Withdraw (send funds — dangerous)

```
# 1. Confirm available balance
cdcx account summary -o json

# 2. Confirm destination is whitelisted (done in Exchange GUI)

# 3. Confirm supported network
cdcx wallet networks -o json

# 4. Preview the request
cdcx wallet withdraw BTC 0.1 <ADDRESS> \
    --network-id BITCOIN \
    --client-wid my-withdraw-001 \
    --dry-run -o json

# 5. Execute
cdcx wallet withdraw BTC 0.1 <ADDRESS> \
    --network-id BITCOIN \
    --client-wid my-withdraw-001 \
    -o json

# 6. Track settlement
cdcx wallet withdrawal-history -o json
```

Positional args: `<currency> <amount> <address>`.

Tier `dangerous`: MCP server refuses the call unless started with `--allow-dangerous`. In the CLI, `cdcx` prompts for confirmation unless `--yes` is passed.

### Memo / Tag Coins (XRP, XLM, EOS, etc.)

```
cdcx wallet withdraw XRP 100 rXRPaddress... \
    --address-tag 12345 \
    --network-id RIPPLE \
    -o json
```

Omitting `--address-tag` on a memo coin routes funds to the exchange's omnibus address without tagging them to the recipient — they will be **lost**.

### History Queries

```
cdcx wallet deposit-history --currency USDT -o json
cdcx wallet withdrawal-history --currency USDT -o json
```

Use `--start-time` / `--end-time` (ms since epoch) to narrow the window.

## Notes

- Withdrawals only go to whitelisted addresses. Whitelist management is done in the Exchange web GUI, not via CLI
- `--client-wid` is your correlation ID — store it so you can cross-reference with `withdrawal-history`
- The `wallet withdraw` command requires all three positional args (currency, amount, address) plus `--network-id`; CLI will error otherwise
- Withdrawal fees are deducted from the received amount on the receiving side — preview with `--dry-run` to see the exchange's fee estimate

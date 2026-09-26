# Earn

USDC yield. `amount_usdc` is a number of USDC, not smallest units.

```
fere_earn_enable    {amount_usdc}                 # first position only
fere_earn_deposit   {amount_usdc}                 # add; REST also requires position_id
fere_earn_positions                               # positions[] + history[]
fere_earn_withdraw  {position_id, amount_usdc}
fere_earn_info                                    # vault and current rate, no auth args
```

REST: `GET /v1/earn/vault`, `POST /v1/earn/enable`, `POST /v1/earn/deposit`, `POST /v1/earn/withdraw`, `GET /v1/earn/positions`, `GET /v1/earn`. All six accept the `agt_` bearer.

## Rules the schema does not state

- `*_percent` fields are fractions. `0.0624` is 6.24% APY. `performance_fee_percent: 0.05` is a 5% fee. Multiply by 100 before showing a number. Read the live rate from `fere_earn_info`. Do not cache it in this file.
- Deposits are USDC on Base or Arbitrum. The vault is on Base (`0xbeeff7ae5e00aae3db302e4b0d8c883810a58100`).
- The floor is $100 to deposit and $100 to withdraw. Under the floor the error is `BELOW_MINIMUM`, and it runs before the balance check. A $100 position can only be closed whole. A wallet under $100 cannot use Earn.
- REST `deposit` requires `position_id` (`422`, loc `["body","position_id"]`) even when OpenAPI marks it optional and the MCP schema omits it. Read `positions[].id`. `enable` is the call that has none.
- Withdrawals land in the Fere wallet, not an outside address.

## Positions

`positions[]`: `id`, `status`, `vault_chain_name`, `current_apy`, `amount_deposited_usdc`, `current_value_usdc`, `unrealized_yield_usdc`, `created_at`.

`history[]`: `action` (`deposit` or `withdraw`), `status`, `shares_delta`, `vault_address`, `vault_apy_at_action`, `tx_hash`, `error_message`.

Accounting follows on-chain shares, not the deposit you sent. If shares leave by any path other than `fere_earn_withdraw`, Fere closes the position:

```jsonc
{ "status": "withdrawn", "current_value_usdc": 0, "unrealized_yield_usdc": -100,
  "history": [{ "action": "withdraw", "status": "reconciled", "tx_hash": null,
    "error_message": "Auto-closed: 0 shares owned on-chain, no withdrawal executed. Position synced to chain state." }] }
```

`unrealized_yield_usdc` is not a P&L to show a user. Keep your own ledger from `amount_deposited_usdc`, `shares_delta`, and `tx_hash`. A `reconciled` row with a null `tx_hash` is an event to investigate, not a withdrawal that happened.

# Earn — the USDC yield vault

`fere_earn_info` (no auth args) → the vault and the current rate. Everything on this
page was read live from `fere_earn_info` and `fere_earn_positions` on **2026-09-09**
against a funded account; the rest of our Fere notes list Earn as untested, and this
is the only record of a real deposit through it.

```jsonc
{ "product":"Fere Earn", "current_apy_percent":0.0607, "net_apy_percent":0.0624,
  "vault": {"chain":"base","chain_id":8453,"asset":"USDC",
            "total_assets_usd":"25147445.68",
            "performance_fee_percent":"0.05000000","management_fee_percent":"0"} }
```

**The `*_percent` fields are fractions, not percents.** `0.0624` is **6.24 % APY**, and
`performance_fee_percent: 0.05` is a **5 % performance fee**. Multiply by 100 before
you show a user a number. Deposits are USDC on Base or Arbitrum; the vault itself is on
Base (`0xbeeff7ae5e00aae3db302e4b0d8c883810a58100`).

```
fere_earn_enable    {amount_usdc}                 # first position only
fere_earn_deposit   {amount_usdc}                 # add to an existing one
fere_earn_positions                               # positions[] + history[]
fere_earn_withdraw  {position_id, amount_usdc}
```

`amount_usdc` is a **number in USDC**, not smallest units — the odd one out in an API
where everything else is a wei string.

REST has the same six ops under `/v1/earn/*` (`GET /v1/earn/vault`, `POST /v1/earn/enable`,
`POST /v1/earn/deposit`, `POST /v1/earn/withdraw`, `GET /v1/earn/positions`, `GET /v1/earn`).
All six answer an `agt_` bearer (sweep of 2026-09-11, fresh agent); the reads match the
shapes above, and the writes taught us three things no doc or tool schema says:

- **The floor is $100, both ways.** `enable {amount_usdc: 5}` → `400 upstream_error`
  wrapping `{'error_code': 'BELOW_MINIMUM', 'error_message': 'Minimum yield amount is
  $100.00 USDC (requested: $5.0)'}`; `withdraw` → the same code, `'Minimum yield
  withdrawal is $100.00 USDC'`. The check runs *before* the balance check, so an
  under-$100 request never reaches your wallet. A $100 position can only be closed
  whole, and a wallet under $100 cannot use Earn at all.
- **REST `deposit` requires `position_id`** (`422 … loc: ["body", "position_id"]`) even
  though the gateway's openapi marks it optional and the MCP `fere_earn_deposit` schema
  omits it. Read it from `positions[].id` first; `enable` is the call that has none.
- Withdrawals land in the Fere wallet, not outside it — Earn is not an exit either.

The position and history shapes below came through MCP on our own account; no deposit
has gone through an `agt_` bearer.

Positions carry `id, status, vault_chain_name, current_apy, amount_deposited_usdc,
current_value_usdc, unrealized_yield_usdc, created_at`; `history[]` rows carry
`action` (`deposit`/`withdraw`), `status`, `shares_delta`, `vault_address`,
`vault_apy_at_action`, `tx_hash`, `error_message`.

## Earn accounting follows on-chain shares, not your deposit

The position rows are a view over the vault's share balance, and they reconcile to it.
Take the shares out by any path other than `fere_earn_withdraw` — selling the vault
token on-chain, say — and Fere closes the position against chain state:

```jsonc
{ "status": "withdrawn", "current_value_usdc": 0, "unrealized_yield_usdc": -100,
  "history": [{ "action": "withdraw", "status": "reconciled", "tx_hash": null,
    "error_message": "Auto-closed: 0 shares owned on-chain, no withdrawal executed.
                      Position synced to chain state." }] }
```

That is what happened to the one $100 position in our account (the share token was sold
directly), so the `-100` is an artifact of the reconcile, not a loss. It is still worth
knowing, because the same row shape would appear if shares ever went missing for a
reason nobody chose: **`unrealized_yield_usdc` is not a P&L you can show a user.** Keep
your own ledger from `amount_deposited_usdc`, `shares_delta` and the `tx_hash` on each
deposit and withdrawal, and treat a `reconciled` history row with a null `tx_hash` as an
event to investigate rather than a withdrawal that happened.

Otherwise untested by us end to end: deposit small first, and check the share balance on
the vault contract on Base before putting size in.

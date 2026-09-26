# Spot

`POST /v1/swap` (MCP `fere_swap`) does same-chain swaps, cross-chain bridges, and EVM↔Solana in one body, and takes a stop-loss and take-profit inline.

## Chains, sentinels, units

| Chain | `chain_id` | Native | Quote asset |
|---|---|---|---|
| Solana | 7565164 | SOL (9) | USDC `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` (6) |
| Base | 8453 | ETH (18) | USDC `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` (6) |
| Robinhood Chain | 4663 | ETH (18) | USDG `0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168` (6) |
| Ethereum | 1 | ETH (18) | USDC `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` (6) |
| Arbitrum | 42161 | ETH (18) | USDC `0xaf88d065e77c8cC2239327C5EDb3A432268e5831` (6) |
| Polygon | 137 | POL (18) | USDC `0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359` (6) |
| BNB | 56 | BNB (18) | pass the token address |
| Hyperliquid | 999 | HYPE | USDC. Perp and HL spot only. No `swap`. |

Solana's id is Fere's `7565164`, not `1399811149`. `GET /v1/chains` (no auth) is the live list, including `explorer_url`. `/capabilities` still says five chains. Ignore it.

```
EVM native sentinel:  0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
Solana native:        So11111111111111111111111111111111111111112
```

The sentinel is `0x` plus exactly 40 `e`/`E` characters. Assert that length before sending. `fere.py` does. The zero address passes dryrun and fails live, because dryrun checks balance and not the route. Do not send `"native"` first.

`amount` is a string of smallest units. Use integer or `Decimal` math. Solana mints are case-sensitive. Keep the wire address's case.

Budget 60–100 bps per same-chain leg. `platform_fee_amount` can be `"0"` while the route still tolls.

## The swap body

```jsonc
POST /v1/swap?wait=true&timeout=90
{
  "chain_id_in": 8453, "chain_id_out": 8453,
  "token_in":  "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  "token_out": "0x<token>",
  "amount": "10000000",
  "slippage_bps": 300,                               // the API default (50) is too tight; use 300
  "take_profit": {"price_percentage": 1.0, "sell_percentage": 0.5},
  "stop_loss":   {"price_percentage": 0.3, "sell_percentage": 1.0},
  "cancel_conditional_orders": false,
  "idempotency_key": "<uuid>",
  "dryrun": false
}
```

`message` is a constant and sits next to failures. `poll_url` is null on a rejected task. `timeout` above 90 returns 422. Wait, then poll. Do not block the user on the wait.

`GET /v1/tasks/{id}` uses uppercase `PENDING|STARTED|SUCCESS|FAILURE|REVOKED`. The swap response is lowercase. Compare case-insensitively. An id that was never issued returns `200 {"status":"PENDING"}` forever. Cap the poll. A timeout is unknown, not failed.

`idempotency_key` is accepted and not enforced. One key can fill more than once. A timed-out write is unknown: read, do not re-send.

`cancel_conditional_orders: true` on a sell clears every hook on that token, not the matching pair. Re-arm afterwards if some should remain.

## Confirming a fill

```
snapshot = GET /v1/holdings?event=wallet-refresh
POST /v1/swap?wait=true&timeout=90
poll GET /v1/tasks/{id} until terminal or deadline
re-read holdings 3× over ~15 s and diff token_in and token_out
```

- Delta > 0 means filled, whatever `status` said.
- `"Balance validation failed"` or a 4xx means nothing ran.
- Anything else with delta 0 is unconfirmed. Show pending. Do not auto-retry.

`fere.py` takes a per-wallet lock and waits 3 seconds after a terminal task. Parallel sends cause nonce errors. A notification `amount_out` can disagree with the holdings delta. Trade on the delta.

## Holdings

`GET /v1/holdings`. MCP `fere_holdings` takes no arguments. REST `?chain_type=` is an integer: `0` EVM, `1` Solana. `"evm"` is a 422.

| Call | Result |
|---|---|
| `GET /v1/holdings` | Saved answer. An empty wallet's answer is kept up to 45 minutes. |
| `GET /v1/holdings?event=wallet-refresh` | Drops the saved answer and reads the wallet. |
| `?event=<anything else>` | Ignored. You get the saved answer. |

Refresh on a user refresh, while waiting for a deposit, and on every fill diff. A display poll can stay plain. Funding and swaps validate against the chain, not this list. (`_status` in `fere.py` output is the CLI's HTTP envelope, not a Fere field.)

```jsonc
{ "chain": "robinhood", "chain_id": 4663, "token_name": "FATCOIN",
  "base_address": "0x12d5…",
  "decimals": 18,
  "tokens_bought": "2246.0004677",
  "amount_in_wei_or_lamports": "2246000467727542208998",
  "curr_price_usd": 0.0162, "value_usd": 36.43, "verified": true,
  "protocol": null,
  "outstanding_orders": [ { "id":"…", "webhookType":"PRICE_EVENT", "status":"ACTIVE" } ] }
```

- There is no `symbol` field. `buying_price_usd` and `profit_*` are 0 on chain rows. Compute P&L yourself.
- `amount_in_wei_or_lamports` is null on Hyperliquid rows. Parse `tokens_bought` with `Decimal`. Values can be scientific notation (`"2.065E-15"`).
- A 502 from one upstream blanks the whole body. Retry 3 times. Keep the last good snapshot for display only.
- Render rows that are `verified: true` or already in your ledger. Do not auto-act on an unknown token.

## Exits

| | Hooks (`take_profit` / `stop_loss`, or `POST /v1/hooks`) | Limit orders (`POST /v1/limit-orders`) |
|---|---|---|
| Trigger | Percentage off Fere's price at registration | Absolute USD |
| List / cancel | `GET` / `DELETE /wallet/outstanding-orders` | `GET /v1/limit-orders[?status=]` / `DELETE /v1/limit-orders/{id}` |
| Use | Arm at buy time | Anything you may replace |

Hooks re-base on Fere's mark, not your entry. Arm them inline, then re-arm with limit orders priced off your own entry. Hooks can disappear. Reconcile `holdings[].outstanding_orders` on every poll and re-arm what is missing.

`POST /v1/hooks` and `POST /v1/limit-orders` succeed on a zero balance. A successful call is not evidence you hold the token.

Limit-order status on creation is `active`. `?status=pending` returns `[]` while the order exists. Unknown id on delete is `404 not_found`. A failed read is not "no orders". Do not re-arm unless the last read succeeded.

Cancel hooks with `DELETE /wallet/outstanding-orders` and body `{"outstanding_order_ids":[…]}`. An empty body is a 422.

## Security check

`POST /v1/security/check {tokens:[{chain_id, token_address}]}`, at most 50 tokens.

Gate on `status`, not on `allowed` alone. Robinhood Chain returns `status:"unsupported_chain"` with `allowed:true`. Treat `passed` as pass. Treat `unsupported_chain`, `api_unavailable`, and `skipped` as not checked. Block everything else.

## Bridging

Different `chain_id_out` on the same call. Do not bridge on the buy path. Cross-chain tolls vary from well under 1% to several percent and are not quoted in advance. Deposit on the destination chain. If you bridge, make it its own step and show the toll after it lands.

## Notifications

`GET /v1/notifications` returns `{events, total_count, limit, offset}`. `GET /v1/notifications/stream` is SSE: it replays recent events on connect, then `event:`/`data:` frames with a `: ping` every 15 seconds. `EventSource` cannot set `Authorization`. Use a streaming fetch.

Known types: `events.onchain.swap.success`, `events.onchain.swap.failure`, `events.hooks.pt.setup.success`, `events.hooks.pt.delete.success`, `events.onchain.limit_order.setup.success`, `events.onchain.limit_order.cancel.success`, `events.hyperliquid.{fund,setup,withdraw}.success`, `events.onchain.perp.{open,close}.success`, `events.onchain.spot.buy.failure`, `events.polymarket.{setup,fund,order}.success`. Swap success carries `txn_hash`, `amount_out`, `volume_usd`, `explorer_url`. Do not drive an exit off a hook-fire event. That type is not part of this list.

# Spot — swap, bridge, and exits that fire while you sleep

One endpoint (`POST /v1/swap`, MCP `fere_swap`) does same-chain swaps, cross-chain
bridges and EVM↔Solana in the same body, and takes a stop-loss and take-profit inline.
None of the wallet vendors or aggregators we compared (Privy, Turnkey, CDP, Crossmint,
Dynamic, Jupiter, 0x, 1inch) puts `stop_loss` in the swap body — it is the reason to be here.

## Chains, sentinels, units

| Chain | Fere `chain_id` | Native | Quote asset | Notes |
|---|---|---|---|---|
| Solana | **7565164** | SOL (9) | USDC `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` (6) | Fere's own id, **not** Codex's `1399811149` |
| Base | 8453 | ETH (18) | USDC `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` (6) | `cdp_network_name: base` |
| Robinhood Chain | 4663 | ETH (18) | **USDG** `0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168` (6) | not a CDP network |
| Ethereum / Arbitrum / Polygon | 1 / 42161 / 137 | ETH / ETH / POL | native USDC (`0xA0b8…eB48`, `0xaf88…5831`, `0x3c49…3359`, all 6 dp) | swap + bridge |
| BNB | 56 | BNB | **none we have verified** — pass the token address | swap + bridge |
| Hyperliquid | 999 | HYPE | USDC | **perp + HL spot only**, no `swap` |

Quote-asset addresses are checked against Circle's contract-address page (and Base +
Solana USDC against live holdings rows); RH USDG comes from our own live trades. The
CLI's chain table carries exactly these and nothing unverified.

`GET /v1/chains` (no auth) is the truth and returns 8 with `explorer_url` for building
tx links. `/capabilities` still says 5 — schema drift, ignore it.

```
EVM native sentinel:  0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE   ← 0x + exactly 40 e/E
Solana native:        So11111111111111111111111111111111111111112
```

**The most expensive typo we ever made was a 41-character, one-`e`-short sentinel.**
(On an unfunded wallet a dryrun with that sentinel, or the zero address, or a $1
notional, all fail identically on balance — the balance check runs first, so none of
those rules are testable without funds. The $5 floor is from live runs, not the sweep.)
Every order failed with a contradictory body until Fere's own dev read the task ids.
Assert it at module load (`fere.py` does, and `test_fere.py` pins it) so a shortened
string fails the build instead of a live order. The zero address `0x000…0` **passes
dryrun and fails live** — dryrun validates balance, never the route. `"native"` is
accepted as a chain-agnostic fallback; never send it first.

`amount` is always a **string in smallest units**. Compute it in integer/Decimal math,
never floats. Solana mints are base58 and **case-sensitive** — lowercasing an address
(a habit from EVM) corrupts every Solana order. Key your own ledger by a lowercased id
if you like, but keep the wire address's case.

## The swap body

```jsonc
POST /v1/swap?wait=true&timeout=90
{
  "chain_id_in": 8453, "chain_id_out": 8453,          // differ => bridge, in one call
  "token_in":  "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  "token_out": "0x<token>",
  "amount": "10000000",                                // $10 USDC, 6 dp
  "slippage_bps": 300,                                 // default 50 is too tight for memecoins
  "take_profit": {"price_percentage": 1.0, "sell_percentage": 0.5},   // +100%, sell half
  "stop_loss":   {"price_percentage": 0.3, "sell_percentage": 1.0},   // -30%, sell all
  "cancel_conditional_orders": false,
  "idempotency_key": "<uuid>",                         // accepted, NOT deduped: 1 key = 3 fills
  "dryrun": false
}
→ {task_id, status:"success"|"failure", message:"Swap task queued successfully", poll_url, notification_stream}
```

`message` is the hardcoded default and appears next to failures. `poll_url` comes back
**null** on a rejected task. `wait=true&timeout=90` is the cap (`120` → 422, the edge
cuts ~100 s), so always wait *then* poll — never block a user request on it.

`GET /v1/tasks/{id}` → `status` in `PENDING|STARTED|SUCCESS|FAILURE|REVOKED`
(**UPPERCASE**, while the swap response is lowercase — compare case-insensitively).
Success carries `result.tx_hash`; failure carries `result.error`, e.g.
`"Balance validation failed: No holdings found for wallet 0x… on Base."`.

**Poll with a deadline.** An id that was never issued — a typo, a truncated copy, the
all-zero uuid — returns `200 {"status": "PENDING", "result": null}` **forever**, never a
404. "Poll until terminal" does not terminate on a bad id; `fere.py` caps at 120 s and
reports `TIMEOUT`. Note that some tasks legitimately take longer than 90 s (HL setup
did), so a timeout is "unknown", not "failed".

## Confirming a fill (the only correct way)

```
snapshot = GET /v1/holdings
POST /v1/swap?wait=true&timeout=90
poll GET /v1/tasks/{id} to terminal
re-read holdings 3× over ~15 s, diff token_in and token_out in units
```

- delta > 0 → **filled**, whatever the status said.
- `"Balance validation failed"` or a 4xx → **definitively failed**, nothing ran.
- Anything else with delta == 0 → **unconfirmed**: show pending, re-check next poll,
  **never auto-retry**. A sell once returned `failure` twice plus a silent no-op and
  the position cleared anyway.

`fere.py buy/sell/swap` implements exactly this, takes a per-wallet lock (one action in
flight, 3 s gap after terminal — parallel sends cause mempool nonce errors), and exits
non-zero unless it saw the delta.

## Holdings — the portfolio, all venues

`GET /v1/holdings` (MCP `fere_holdings` takes no arguments; REST takes
`?chain_type=0|1`, an **integer**: 0 = EVM, 1 = Solana — `"evm"` gives 422). Rows now
span on-chain tokens **and** Hyperliquid **and** the Polymarket safe.

**It is a cached read unless you ask for a fresh one** (Fere's RCA, 2026-09-23):

| Call | What you get |
|---|---|
| `GET /v1/holdings` | Fere's **saved answer** when it has one. An **empty** wallet's answer is kept up to **45 min** and not re-checked, so a deposit that lands just after one empty read stays invisible for that long. Measured: ~0.18 s once saved. |
| `GET /v1/holdings?event=wallet-refresh` | Drops the saved answer and **reads the wallet again** — the same action as the app's Refresh button. ~0.45 s on an empty agent. |
| `?event=<anything else>` | Silently ignored: 200, saved answer. Spell it exactly. |

Fere's own app refreshes only on the Refresh button and right after a fund or
withdraw; leaving a page open never does. So: **refresh** on a user's Refresh, while
waiting for a deposit, and on **every read of a fill diff** (rule 1); a background
display poll can stay plain. Funding and swaps are **not** affected — they validate
against the chain, not this list (on 2026-09-23 `perp/fund` moved $100 first try while
~100 plain polls still said `[]`). The `_status` key in the envelope is our CLI's, not
Fere's. Row shape:

```jsonc
{ "chain": "robinhood", "chain_id": 4663, "token_name": "FATCOIN",   // no `symbol` field
  "base_address": "0x12d5…",            // "native" for the gas token; EVM rows come back lowercased
  "decimals": 18,
  "tokens_bought": "2246.0004677",      // decimal string — CAN be "2.065E-15", parse as Decimal
  "amount_in_wei_or_lamports": "2246000467727542208998",  // **null** on Hyperliquid rows
  "curr_price_usd": 0.0162, "value_usd": 36.43, "verified": true,
  "buying_price_usd": 0, "profit_abs_usd": 0,   // 0 on chain rows; populated on HL rows
  "protocol": null,                     // "Hyperliquid" | "Polymarket" on venue rows
  "redeemable": null, "condition_id": null, "negative_risk": null,   // Polymarket only
  "leverage": null, "collateral_usd": null, "liquidation_price_usd": null,  // perp only
  "outstanding_orders": [ { "id":"…", "priceUsd":{"gte":0.00031}, "networkId":8453,
      "tokenAddress":"0x…", "webhookType":"PRICE_EVENT", "status":"ACTIVE",
      "bucketSortKey":"tp-0.5" } ] }
```

Traps, all seen live:
- **P&L is yours to compute.** `buying_price_usd` and every `profit_*` field are `0` on
  chain rows. Keep your own ledger keyed by entry.
- **Never parse `amount_in_wei_or_lamports` blind.** It comes back **null** on
  Hyperliquid rows (seen live 2026-09-09), and it is a *risk* for large balances in JS:
  if Fere ever sends it as a number ≥ 1e21 it stringifies as `"1e+21"`, `BigInt()`
  throws, and the bag renders empty. Fere sends strings today — that one is unresolved,
  not fixed. Prefer `tokens_bought` through a `Decimal`, which handles both (and the
  sci-notation values Fere already sends, e.g. `"2.065E-15"`).
- 0.35–0.45 s empty, ~2 s funded. A **502 from one upstream** (`zerion_solana`,
  `hyperliquid`) blanks the entire response: retry 3× (2/4/6 s), keep the last-good
  snapshot for **display only**, never trade on a stale one.
- Unsolicited airdrops show up. Render only rows that are `verified:true` or in your own
  ledger, and never auto-act on an unknown token.

## Exits: hooks vs limit orders

| | **Hooks** (`take_profit`/`stop_loss` inline, or `POST /v1/hooks`) | **Limit orders** (`POST /v1/limit-orders`) |
|---|---|---|
| Trigger | **percentage** off Fere's price **at registration** | **absolute USD** you choose |
| CRUD | none under `/v1` — list/cancel only via `GET\|DELETE /wallet/outstanding-orders` | full CRUD: `GET[?status=]`, `GET /{id}`, `DELETE /{id}` (all verified; unknown id → `404 not_found`) |
| Good for | fire-and-forget at buy time | anything you may need to cancel or replace |

Both are server-side Codex `PRICE_EVENT` webhooks and both fire while you are offline
(verified live on Solana and Robinhood Chain).

- **Hooks re-base on Fere's price at registration, not your entry.** +50 %/−30 % on a
  `0.02371` mark became `gte 0.03556` / `lte 0.01659` regardless of what you paid. Arm
  hooks inline at buy for speed, then **re-arm with absolute limit orders priced off
  your own entry**.
- **Hooks decay.** Two positions' TP+SL vanished overnight while another chain fired a
  hook correctly the same day — order loss, not a chain limitation. Reconcile
  `holdings[].outstanding_orders` against your expected-exits table on every poll and
  re-arm what's missing.
- `POST /v1/hooks` registers **even with a zero balance** (the task result says so:
  `token_balance: "0"`, `hooks_registered: 2`), so a successful call is not evidence
  you hold anything. **So does `POST /v1/limit-orders`** — `SUCCESS`,
  `webhook_registered: true`, on an empty wallet.
- Limit-order `status` values seen live: **`active`** on creation, `cancelled` after
  `DELETE`. Not `pending` — `?status=pending` returns `[]` while the order exists;
  `?status=active` finds it. The executed/failed spellings are unobserved.
- **A failed read is not "no orders".** Gate auto re-arm on "the last read succeeded",
  or one 502 stacks a duplicate sell every cooldown.
- Cancelling: `DELETE /wallet/outstanding-orders` with body
  `{"outstanding_order_ids":[…]}` → `{count:n}`. An empty body is a 422.

## Security check

`POST /v1/security/check {tokens:[{chain_id, token_address}]}`, ≤50 per request.
Honeypot.is for EVM (~0.4 s), RugCheck for Solana (~1.7 s).

**Gate on `status`, never on `allowed` alone.** Robinhood Chain returns
`status:"unsupported_chain"` *with* `allowed:true` — an uncovered chain looks like a
pass. Treat `passed` as pass, `unsupported_chain`/`api_unavailable`/`skipped` as
"not checked, decide anyway", and everything else as a block.

## Bridging

Same call, different `chain_id_out`. But **don't bridge on the buy path**: Base→RH
tolled 2.3 %, 5.8 % and once failed silently on a route that had worked an hour
earlier. Deposit per chain, and if you must bridge, make it an explicit labelled step
with the toll shown. Measured all-in cost same-chain is ~80–100 bps (a Base exit
measured 82 bps; a cross-chain entry 97 bps — so the bridge itself was only ~15 bps
that time, and 2–8 % other times).

## Notifications

`GET /v1/notifications` → `{events:[{id,type,data,created_at,task_id,agent_id}],
total_count, limit:10, offset}`. `GET /v1/notifications/stream` is SSE: it replays
recent events on connect, then `event:`/`data:` frames with a `: ping` every 15 s.
`EventSource` can't set an Authorization header, so read it with a streaming fetch.
Types confirmed: `events.onchain.swap.failure`, `events.hooks.pt.setup.success`.
**Hook-fire and swap-success event types are unverified — do not build an exit
notification on them without checking.**

## Verified live, 2026-09-12

- **Cost, measured:** Base USDC↔WETH ran **57–70 bps per leg**, 120 bps round trip, with
  `platform_fee_amount "0"`. Budget 60–100 bps a leg same-chain, not the 80–100 we used to quote.
- **`cancel_conditional_orders: true` on a sell clears EVERY hook on that token**, not just
  the matching pair — 6 → 0, with `events.hooks.pt.delete.success "Cancelled 6"`. Use it
  deliberately; re-arm afterwards if you meant to keep some.
- **Notification types now confirmed:** `events.onchain.swap.success` (carries `txn_hash`,
  `amount_out`, `volume_usd`, `explorer_url`), `events.hooks.pt.setup.success`,
  `events.hooks.pt.delete.success`, `events.onchain.limit_order.setup.success` and
  `.cancel.success`, `events.hyperliquid.{fund,setup,withdraw}.success`,
  `events.onchain.perp.{open,close}.success`, `events.onchain.spot.buy.failure`,
  `events.polymarket.{setup,fund,order}.success`. **Hook-*fire* is still unverified** — we
  never had a hook trigger.
- **The success event's `amount_out` is not the truth either.** It came back 0.000966 USDC
  *under* the holdings delta. Holdings remain the only number to trade on.

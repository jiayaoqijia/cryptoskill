# Polymarket — per agent, not per account

> **Fills verified 2026-09-12**: two FOK orders through the REST
> route with the MCP field names — BUY $5 → 16.129 shares @0.31, then SELL 16.12 @0.30,
> both `status: "MATCHED"`, position visible in `activity` and `/v1/holdings`. Two
> surprises: the CLOB **accepted a $4.84 SELL**, so the "$5 floor blocks small exits"
> worry is dead; and a sports market charged **3.45 % taker fee per leg**
> (`taker_base_fee 1000`) — price that in before calling an edge. The result echoes a
> `price` 1–3 ticks off what you sent, so read the fill from `activity`, not the echo.
>
> **Exit verified 2026-09-13.** `POST /polymarket/withdraw
> {"amount_usdc":"9.404696","destination_chain_id":8453}` emptied the Safe: task
> `SUCCESS` in 8 s, **9.394675 USDC in the agent's own Base wallet within 40 s**, cost
> $0.010021 (10.7 bps, no flat fee, no minimum tripped at $9.40). `amount_usdc` is a
> **decimal** string — the opposite of `fund-safe`'s smallest-unit `amount`. Money can
> enter and leave every venue we funded except HL spot (which cannot be entered).

**Every key-registered agent gets its own Polymarket Safe.** This was wrong in earlier notes
(including `FERE.md`'s "MCP only") and it matters: it is what makes a prediction-market
product with a wallet per end user possible.

Verified 2026-09-09 on an agent registered from nothing but a keypair minutes earlier:

```bash
python3 scripts/fere.py poly setup alice     # POST /polymarket/setup with alice's bearer
# -> SUCCESS in ~5 s:
#    safe_address        0x37A1E4eCD682d233E54626d071B0007695f5F59A
#    deposit_address_evm 0xA036879890B8c82f7994Cd669DFCf6513B21abdD
#    deposit_address_svm ARTHf4MGkpzgNeVDre3NH6HgPz2Tg3sYo2eLDnDGVHrk
#    setup_complete true, v2_complete true, min_fund_usd 5.0
python3 scripts/fere.py poly status alice
```

Verified: the setup, and (2026-09-11) that a REST order from a fresh, unfunded Safe
gets all the way to the CLOB's cash check — `"Insufficient Polymarket cash balance:
order requires $5.00 USDC but only $0.00 USDC is available on Polymarket (free of
open-order reservations)…"`. Not verified: a fill.

## Two doors, different surfaces

The `/polymarket/*` routes are tagged `webapp-polymarket` rather than living under `/v1`,
which is why they were assumed private — but they **accept a keypair auth `agt_*` bearer
and scope every response to that agent** (unauthenticated: `401 unauthorized`).

| | MCP (`fere_polymarket_*`, 12 tools) | REST (`/polymarket/*`, 12 ops) |
|---|---|---|
| Who | one human's own account | **one Safe per agent → per end user** |
| Discovery + live prices | ✅ `markets`, `markets_for_event`, `prices`, `whale_data` | ❌ **no equivalent — use Polymarket's own public APIs** |
| Setup / fund / order / cancel / redeem / withdraw | ✅ | ✅ |
| Documented request bodies | ✅ in the tool schema | ❌ openapi carries no body schema — the required fields below were recovered from 422s |

Mapping, for porting an MCP flow to per-user REST:

| MCP tool | REST |
|---|---|
| `fere_polymarket_setup` | `POST /polymarket/setup` ← **call this one**; `/setup/v2` alone fails with *"Cannot run v2 migration: v1 setup not complete"* on a fresh agent, and returns `502 upstream_error` (`Upstream error: {'raw': 'Internal Server Error'}`) once v1 has already completed the migration |
| `fere_polymarket_account` | `GET /polymarket/setup/status` + `/polymarket/orders/open` + `/polymarket/activity` + `GET /v1/holdings` (the MCP tool just aggregates these) |
| `fere_polymarket_fund` | `POST /polymarket/fund-safe` — **`amount` is SMALLEST UNITS on REST** (`"10000000"` = $10.000000, verified through to a landed Safe balance 2026-09-12; the bridge tolled ~90 bps). The MCP tool takes a human decimal string instead. |
| `fere_polymarket_order` / `_order_cancel` | `POST /polymarket/order` — **the MCP field names work as-is** (`{side, price, amount, order_type, token_id}` reached the CLOB; `token_id` is the one required field) / `/polymarket/order/cancel` — one of `order_id`, `market_id`, or `cancel_all: true` (the MCP `mode` field is not the REST shape) |
| `fere_polymarket_orders_open` | `GET /polymarket/orders/open` |
| `fere_polymarket_redeem` | `POST /polymarket/redeem` — requires `condition_id` (no `event_slug` resolution on REST, so pass `negative_risk` too — see below) |
| `fere_polymarket_withdraw` | `POST /polymarket/withdraw` — **`{"amount_usdc": "<decimal>", "destination_chain_id": <int>}`**, verified through to a landed balance 2026-09-13. `amount_usdc` is a decimal string (`"9.404696"`), NOT smallest units like `fund-safe`; `destination_chain_id` is required and is not in any schema (the MCP `chain`/`token` names are ignored, not mapped — a body with them still 422s `Field required: destination_chain_id`). Fee comes out of the amount (10.7 bps on $9.40), so pasting the holdings `units` string withdraws everything. Lands in **your Fere wallet** on that chain, not an outside address |
| `fere_polymarket_markets` / `_markets_for_event` / `_prices` / `_whale_data` | **none** — read `gamma-api.polymarket.com` and `clob.polymarket.com` directly (free, no auth, and fresher than anything Fere caches) |
| — | `GET /polymarket/meta`, `POST /polymarket/disclaimer/acknowledge` (no MCP tool) |

Because the write bodies have no published schema, `fere.py poly` takes them as explicit
JSON (`--body '{"side":"BUY",…}'`). The order body is verified through to the CLOB;
`fund-safe` and `withdraw` are verified through to a landed balance (in and out of the
Safe, $10 → 9.910456 pUSD → 9.394675 USDC back on Base); `redeem` only as far as its
required-field 422. Every write answers **HTTP 200 + `task_id` and fails in the task** (a bogus
`token_id` → `PolyApiException[status_code=404, error_message={'error': 'market not
found'}]`), so the task is the verdict. Ship a funded smoke test through your own path
before you trust it with a user's money.

The upstream is **flaky**: mid-session these routes returned
`502 upstream_error {"error":"All connection attempts failed"}` for several minutes and
then recovered. Treat a Polymarket 502 as "try again shortly", never as "not set up".

## The 12 MCP tools

| Tool | What it does || Tool | What it does |
|---|---|
| `fere_polymarket_account` | one-call snapshot: setup state, Safe deposit addresses, open orders, positions (token_id, condition_id, shares, avg_cost, current_price, uPnL, `redeemable`), cash, realized PnL, volume. **Auto-runs setup** if `v2_complete` is false — that's infrastructure, not a user decision |
| `fere_polymarket_setup` | explicit setup (POSTs `/setup/v2`) — on a fresh agent call the REST `/polymarket/setup` instead, or just let `fere_polymarket_account` run it |
| `fere_polymarket_fund` | bridge into the Safe from your Fere wallet. Prefer telling the user to deposit to `account.deposit_addresses` directly |
| `fere_polymarket_markets` | discovery feeds: `trending`, `closing`, `easy_wins`, `arbitrage`, `public` (+ `categories`, `text_query`, `sort_by`, `limit`) |
| `fere_polymarket_markets_for_event` | the markets under one event |
| `fere_polymarket_prices` | **live, uncached** best_bid / best_ask / midpoint / spread / min_tick_size, ≤20 token_ids |
| `fere_polymarket_order` | place a CLOB order |
| `fere_polymarket_orders_open` / `_order_cancel` | manage resting orders |
| `fere_polymarket_redeem` | claim resolved positions |
| `fere_polymarket_withdraw` | Safe → **your Fere wallet** on a chain you name — not an external address (confirm amount + chain with the user first). Fast and cheap on REST: 8 s task, ~40 s to land, ~11 bps |
| `fere_polymarket_whale_data` | large-holder flow — **stale, and it has no predictive edge** (see below) |

## Prices: refresh before every decision

Discovery feeds and the account snapshot carry **batch-cached prices, recomputed
hourly** — 60+ minutes stale in a moving market. We called positions wrong off them
more than once. Use them to *find* markets, then always
`fere_polymarket_prices(token_ids)` before deciding or ordering.

## Ordering, exactly

```jsonc
fere_polymarket_order {
  side: "BUY"|"SELL",             // exits a position; independent of outcome_token
  outcome_token: "YES"|"NO",      // which leg of the market
  token_id: "…",                  // or event_slug + outcome (multi-outcome events)
  price: "0.42",                  // 0.01–0.99, the WORST price you accept
  order_type: "GTC"|"GTD"|"FOK"|"FAK",
  size: "25",                     // shares — GTC/GTD
  amount: "10",                   // FOK/FAK: USD for BUY, shares for SELL
  expiration_seconds: 3600,       // GTD only
  take_profit_price: "0.80"       // BUY only: auto-places a GTC SELL after the fill
}
```

- **`price` is a limit, not the fill price.** A marketable order fills at the resting
  counter-order's price, which can be *better* than your limit — $10 at a 0.17 ceiling
  filled 59 shares at 0.168.
- **There is no market order.** Emulate one by pricing aggressively inside the book
  (SELL at 0.90 when the bid is 0.95), not at the 0.01/0.99 floor.
- **Min notional $5, enforced on BUY only.** SELLs are not pre-checked by Fere, but the
  CLOB rejects tiny notional (`shares × price`), so a price near 0.01 collapses the
  notional and the order dies silently. To exit, price a few cents inside the bid.
  **This is a behaviour change.** Through 2026-07 the MCP order tool pre-checked
  `shares × price ≥ $5` on sells too and rejected small marketable exits, so the
  standing advice was "cut small positions in the web UI, not through the tool"
  (older notes of ours still carry that advice). The live tool
  contract as of **2026-09-09** says the check is BUY-only. Re-read the tool
  description before you rely on either behaviour.
- GTC that crosses the spread fills immediately and never rests.

## Redeeming

`fere_polymarket_redeem {event_slug, outcome?}` is the safe form — the gateway resolves
both `condition_id` and the neg-risk flag. If you pass a raw `condition_id` you **must**
also pass `negative_risk`, because it cannot be inferred from the id and getting it
wrong routes the redeem to the wrong adapter. Redeem lags settlement: if it times out
the market is probably still settling — verify resolution on Gamma/CLOB
(`outcomePrices == [1,0]`), not on a Fere flag, and retry once final.

## Positions show up in `/v1/holdings` too

Safe cash appears as a `pUSD` row on Polygon (`chain_id 137`, `protocol:"Polymarket"`,
token `0xC011a7E12a19f7B1f670d46F03B03f3342E82DFB`), and outcome positions carry
`condition_id`, `negative_risk` and `redeemable`. Filter `avgPrice == 0` rows out of any
whale/leaderboard analysis — they faked a $1.6B holder in ours.

## Two findings worth more than the tooling

- **Copying whales or experts is not +EV out of sample.** We ranked 18,949 wallets over
  the 2026 World Cup and backtested the follow strategy: no edge survives.
- **These markets are near-efficient at every level we could attack** — match, bracket,
  futures, props. Our +77 % headline was ~$31 of a single in-play punt; strip it and the
  system is breakeven. "No bet" is the honest default. If you ship a Polymarket product,
  sell the *tooling* (fast book reads, one-tap exits, redeem hygiene), not alpha.

## Fees and floors, measured

- **Taker fees are real and large on sports markets.** `taker_base_fee: 1000` on
  `clob.polymarket.com/markets/{conditionId}` means `0.05 × p × (1−p)` per share — we paid
  **3.45 % on the buy and 3.5 % on the sell**. Read the market's fee fields before sizing;
  an edge under ~7 % round trip does not survive. `value_usd` in `activity` includes the fee.
- **The small-exit floor is lower than we thought.** A **$4.84 FOK SELL** priced 3¢ inside
  the bid filled. Keep pricing inside the bid, but stop treating $5 as a hard exit floor —
  the real one is somewhere below $3.87 at the echoed price, and we have not found it.

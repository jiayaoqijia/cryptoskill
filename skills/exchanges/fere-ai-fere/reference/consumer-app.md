# Consumer product integration pattern — a page that moves real money

One product has taken this end to end: **The Desk** (`strategy-marketplace/` in the
repo this skill grew up in — `desk_fere.py`, the `/api/*` routes in `server.py`,
`web/desk.js`). Browser-held key, stateless passthrough, Hyperliquid perps, live
fills on the owner's money. Everything below is what it shipped, with the file and
function that owns each rule. Copy the shape; the numbers are measured, not guessed.

Companion reading: `wallets.md` (custody, the key string, no-CORS) ·
`hyperliquid.md` (the venue's own floors and fees) · `fere-multitenant`'s
`reference/onboarding.md` §7 (the browser keypair as an account, and what users
made of it).

## 1. The passthrough: stateless, allowlisted, no key server-side

Fere sends no `Access-Control-Allow-Origin`, so the browser cannot call it. The
answer is *not* a backend that holds keys — it is a dumb forwarder, so that the
sentence "this server holds no key, no session and no user row, so it cannot trade
for anyone, including itself" stays literally true (`server.py:fere_passthrough`).

**The allowlist that shipped** (`desk_fere.py:ALLOWLIST`, method + `fullmatch` on the
normalised path — `desk_fere.py:norm_path` collapses `//` and strips the edges):

```
POST v1/auth/(register|verify|token)
GET  v1/(wallets|holdings)
GET  v1/perp/(setup|orders|markets)
POST v1/perp/(setup|fund|open|close)
POST v1/perp/orders/cancel
POST v1/swap
GET  v1/tasks/[A-Za-z0-9_:.-]{1,128}        # anchored on the id SHAPE, not "anything but /"
```

Everything else is **403 with no socket opened** — and each exclusion is a decision:

- **`v1/chat` is denied by prefix** (`DENY_PREFIXES`), not merely absent: 15 credits a
  query is the one endpoint known to cost money to *call*, and a public page must not
  be able to spend.
- **`v1/perp/withdraw` is deliberately out.** Moving a balance is not part of taking
  or exiting a trade; an endpoint that moves money has no business on a public page's
  allowlist until the product actually uses it.
- **Hooks, limit orders, Polymarket, Earn, notifications: out.** Not because they are
  dangerous — because an allowlist is only worth having if it is the set you use.
- **`v1/swap` is the one addition**, and only for funding (§5): a deposit lands on any
  chain in any token, and the only verified way to HL margin is USDC-on-Base first.

Timeouts by path (`desk_fere.timeout_for`): **20 s default, 130 s** on
`perp/(setup|fund|open|close)` and `v1/swap` — a fund bridges (19 s observed, setup
running behind it) and Fere's gateway holds `?wait=true&timeout=90` connections open.

## 2. Header hygiene, rate limits, logging

- **Forward exactly three request headers**: `authorization`, `content-type`,
  `accept` (`desk_fere.FORWARD_REQ_HEADERS` / `upstream_headers`). Nothing else —
  no cookies, no forwarded-for, no origin.
- **Return `content-type`, `retry-after`, `x-request-id`** plus any `x-ratelimit*`,
  and strip every hop-by-hop / framing header (`desk_fere.response_headers`,
  `HOP_BY_HOP`): your client already de-chunked and decoded the body, so a copied
  `content-length` or `content-encoding` is a lie that breaks the response.
- **Re-quote the path, forward the query verbatim** (`desk_fere.upstream_url`): a
  decoded `?` or `#` inside a segment must stay in the path instead of becoming a
  query Fere reads.
- **Cap the body at 64 KiB → 413** (`MAX_BODY`), checked on the declared
  `content-length` first so an oversize body is dropped before it is read.
- **Per-IP token bucket, 5/s burst 30** (`server.py:_take_bucket`), keyed on the
  **last** `X-Forwarded-For` hop (`_client_key`) — the first hop is whatever the
  client chose to send. Create-account is 4 calls in ~2.5 s, hence the burst.
  Any *unauthenticated* endpoint that does real work needs its own bucket too: the
  Desk's `/api/trade/prepare` runs sync in the threadpool and blocks a worker on a
  Hyperliquid round trip, so 25 concurrent callers starved every other route until
  it got one (`server.py:trade_prepare`, review HIGH 1).
- **Log `method path status ms` and nothing else** (`server.py:_fere_log`). Not the
  bearer, not the body, not the query. The token is a one-hour licence to trade a
  wallet with money in it.
- **`X-Content-Type-Options: nosniff` on every response, refusals included** — one
  middleware, so no error branch can forget it.
- **Retry the agent-proxy JIT-cert race on GETs only** (`desk_fere.is_jit_cert_error`):
  a POST that may already have reached Fere is never re-sent.

## 3. CSP for a page that holds a key

The seed lives in the browser, and browser storage is readable by any script that
gets to run on that origin — so **no script runs unless it came from this origin as
a file** (`server.py:DESK_CSP`):

```
default-src 'none'; script-src 'self';
style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
font-src https://fonts.gstatic.com; img-src 'self' data:;
connect-src 'self' https://api.hyperliquid.xyz;
base-uri 'none'; form-action 'none'; frame-ancestors 'none'; object-src 'none'
```

Plus `nosniff` and `Referrer-Policy: no-referrer`. Three things learned paying for it:

1. **Stamp the header where the bytes come off disk, not on a matching request path.**
   The first cut matched paths, and `/%2e/desk.html`, `/desk.html/` and `/%2e/desk.js`
   all served the page with **no policy at all** through the static mount's own
   normalisation (`server.py:DeskStatic.file_response` fixed it). A policy with a
   bypass is not a policy.
2. **`script-src 'self'` means no inline `<script>` and no charting library.** Ed25519
   comes from WebCrypto with nothing to load (`desk.js:newSeed`); the price chart is
   ~150 lines of hand-drawn `<canvas>`. Budget for that, or pick a different custody
   model. Assert it in a test: one `<script` tag, and it has a `src`.
3. **`style-src 'unsafe-inline'` is fine and is not the gate** — CSS cannot read
   storage. Don't burn a week on it.

## 4. Writes: idempotency, retries, and what counts as a fill

**`idempotency_key` is accepted and NOT enforced** (one key, three filled swaps,
2026-09-12 — `API_FEEDBACK.md` P0-1). So:

- One key per user tap, generated client-side (`desk.js:tapNonce` → `crypto.randomUUID`),
  passed through `prepare` into the order body — **a courtesy, never a safety net**.
- The actual safety is **the page never re-sends a write**. A 401 on a non-GET
  re-mints the bearer and *throws*; only a GET gets the one retry on a fresh token
  (`desk.js:fere()`). A read timeout is UNKNOWN — reconcile by reading the position.
- The funding legs carry **no** idempotency key at all (`desk_fere.fund_plan`, the
  comment block): `perp/fund` does not document the field, and an unenforced key
  reads like "retry is safe" when the measured behaviour is three fills.

**The fill rule, as implemented** (`desk.js:confirmTrade`) — three conditions, all of
them, or the screen says *unconfirmed*:

1. **Positions diff, not presence.** Snapshot `positionFor(coin)` *before* sending;
   a fill is `size` grown beyond a rounding wobble (`× 1.000001 + 1e-9`) or a side
   flip. Without the before-snapshot, a rejected order on a coin already held
   congratulates the user on someone else's position.
2. **AND the task says `SUCCESS`**, polled *with a deadline* (`desk.js:pollTask`,
   90 s) — an id that was never issued answers `200 PENDING` forever.
3. **AND the brackets are read back from the venue**, `frontendOpenOrders` filtered
   on `isTrigger` + coin (`desk.js:readBrackets`), because `tp_oids`/`sl_oids` come
   back **empty from Fere even while both triggers rest**. Only then may the page
   claim a stop exists — and "no stop attached, nothing will close this for you" is a
   sentence it can print, because it can be true.

`SUCCESS` without growth, or growth without `SUCCESS`, is neither a fill nor a
rejection: say so, and send the person to a screen that reads the venue directly.

**Reads come from Hyperliquid, writes from Fere.** Positions, fills, brackets and
balances are public, address-keyed, free and CORS-open, and they work when Fere does
not (`desk.js:hl()`, with `/api/hl/info` as the fallback for a blocked network —
`type`-allowlisted, read-only, `server.py:hl_info`). Key them on
**`GET /v1/perp/setup` → `eoa_address`**, the agent's own HL account — *not* the Fere
EVM wallet address, which is a labelled fallback and is not promised to be the same
(`desk.js:refreshHlAddress`).

## 5. `prepare`: the server builds the order, the client never composes a price

One endpoint turns "$25 at 3× on this card" into the exact `POST /v1/perp/open` body
(`server.py:trade_prepare`). It places nothing and needs no auth — it is arithmetic —
but it is the only place an order body exists.

- **The mark is the venue's, read at prepare time** (`server.py:_live_mid` → HL
  `allMids`, no cache, 6 s, one attempt; `{"dex": …}` for HIP-3 coins, and both the
  prefixed and bare spellings are looked up). The first real fill landed **0.56 %
  away** from a 60 s-cached card mark, and the client's own drift check could not see
  it because both sides came from that same cache. **No live price → 409, never a
  stale one.**
- **Size rounds DOWN to the market's `szDecimals`** (`desk_fere.round_size` on
  `Decimal`, `ROUND_DOWN`): the only rounding that cannot turn "$25 of ETH" into an
  order for more money than was asked for. `szDecimals 0` means integer contracts
  (AERO), and `0.7 → 0.0` is a real answer the caller must then reject.
  `size = amount × leverage / price` (`desk_fere.size_for`) — HL sizes in the base
  token, never in dollars.
- **Order prices round to what HL will accept** (`server.py:_hl_price`): ≤5
  significant figures and ≤ `MAX_DECIMALS − szDecimals` decimals, nearest, integers
  always allowed (BTC 123456.7 → 123457, not 123460). Observed prices — entry, mark —
  are **not** put through it: they are facts, not orders.
- **Min notional $10, refused with the arithmetic in words**
  (`desk_fere.min_notional_error`): *"That comes to $7.30 — under Hyperliquid's $10
  minimum. Try a bigger amount or more leverage."* Size ≤ 0 gets its own sentence.
- **Leverage is clamped to the market's own cap** (`desk_fere.clamp_leverage`,
  fallback 10) and the clamp is reported as a warning, not swallowed.
- **`is_cross: false` — isolated, always.** The sheet promises a bounded "if it hits
  stop" figure, and that promise is only true on isolated margin, where the most the
  trade can lose is the margin posted. Cross backs the position with the whole HL
  balance: a better carry trade and a worse consumer product.
- **`prepare` hands back what the client must agree with** before it sends: `side`,
  `mark_live`, `mark_card`, `drift_pct`, `tp`, `sl`, and the barriers re-measured from
  the live mid. The sheet compares them against what it *printed* and re-renders
  instead of sending when the side flipped or price moved > 0.5 %
  (`desk.js:tradeChanged`). It also 409s a card the price has already run through,
  and one with no barriers left to arm. **The trade you confirm is the trade you read.**

## 6. HIP-3 builder dexes: the gap to design around

Fere's `GET /v1/perp/markets` answers **178 tokens, all `hl:perp:<COIN>` on the main
dex**; Hyperliquid's own table is **519 markets across 11 dexes**
(`{"type":"perpDexs"}` — the `null` row IS the main dex; `server.py:_hl_dex_names`,
`_hl_meta_fetch`, which fetches every dex best-effort so one failure cannot cost you
BTC's 40×). Two independent blockers, both tested live on a funded account
(`API_FEEDBACK.md` **P1-18**):

1. **Five namings, five rejections.** `xyz:NVDA`, `NVDA`, `hl:perp:xyz:NVDA`,
   `hl:perp:NVDA`, `xyz:nvda` — each HTTP 200 + `task_id`, then task `FAILURE` in
   ~4 s: `"Unknown Hyperliquid perp asset: <name>"`, echoed verbatim. `perp/open`
   resolves `asset` against the same main-dex table the catalogue serves, so the
   index gap *is* the routing gap.
2. **Each builder dex has its own perp clearinghouse.** Same wallet, same second:
   main `accountValue` 96.768082, `{"dex":"xyz"}` **0.0**. Collateral reaches it by
   HL's `perpDexClassTransfer`, which Fere exposes no route for — so indexing the
   names would still leave the orders failing for margin.

**So mark them unroutable up front and say why.** `desk_fere.market_row` sets
`fere_routable = false` for any dex-prefixed or delisted coin with a
`routable_reason` in plain words, the page refines it from Fere's own list once there
is a bearer (a server-side default, never a claim), and the card says *"can't be
placed from here"* **before** the tap instead of failing after it. On the Desk that
is 7 of 20 cards — all tradfi, all HIP-3.

## 7. The funding journey (and the swap-pin rule)

Money must be at the venue before an order exists. The whole path, one step at a
time, bodies built server-side (`desk_fere.fund_plan`, `server.py:fund_prepare`):

| Step | Call | Cost | Wait |
|---|---|---|---|
| Deposit | none — the wallet's one EVM address (or its Solana one), any liquid token, no gas coin | — | chain time |
| Convert, only if it is not USDC on Base | `POST /v1/swap {chain_id_in, chain_id_out: 8453, token_in, token_out: USDC-Base, amount (smallest units, string), slippage_bps: 300}` | **57–70 bps** same chain; **0.2–8 %** cross-chain (a measured range, not a quote) | < 1 min / minutes |
| Onto Hyperliquid | `POST /v1/perp/fund {amount, source_chain_id: 8453, source_token: USDC-Base}` | **53–56 bps** measured | ~20 s |
| Confirm | HL `clearinghouseState.marginSummary.accountValue` on the `eoa_address` | free | polled 5 s, 3 min deadline |

`perp/fund` **runs HL setup itself** (its task carries a `setup_task_id`;
`account_activated` flipped 9 s later) — never call `perp/setup` first, which fails
`HYPERLIQUID_NOT_FUNDED` after >90 s on an empty account.

**One swap per balance, ever.** The expensive failure is not a failed transfer, it is
a *second swap*: the fund leg times out, the person taps again, and the original token
is converted twice while the first lot of USDC sits unused. So
(`desk.js:pinFundLeg` / `clearFundLeg` / `swapAlreadyDone`):

- the moment a swap is **sent**, the step is pinned to the USDC-on-Base row, in
  memory *and* `sessionStorage`, so a reload resumes at the fund leg;
- a retry checks the balance itself and skips the swap if the USDC is already there;
- only a deliberate source change, a **definitive** rejection (nothing moved), or a
  completed deposit releases the pin;
- and the second leg is sized on **what actually landed** (a holdings diff), never on
  a number predicted before the swap ran.

**Holdings reads are cached unless the page asks for a fresh one.** A plain `GET
/v1/holdings` can return Fere's saved answer, and an empty wallet's is kept up to
45 min — so a user who deposits into a brand-new wallet and watches the page sees
"nothing here" for that long (2026-09-23, Fere RCA). The passthrough forwards the query
string verbatim (`desk_fere.py:upstream_url`), so send
`GET /api/fere/v1/holdings?event=wallet-refresh` from the **Refresh balances** tap,
from every read inside a deposit-arrival or fill-diff wait, and once on the Account
screen's first render; background re-renders can stay plain.

**Both legs are confirmed by reading a balance, bounded by route**: `GET /v1/holdings`
(**with `?event=wallet-refresh`**) diffed on the USDC-Base row, **60 s same-chain / 5 min cross-chain**
(`desk.js:waitForUsdc`), then HL's own account value (`waitForHl`, 3 min). A wait that
gives up early makes a working transfer look failed — which is what makes someone send
it twice. Every unconfirmed branch says *"nothing was re-sent, and we will not swap
that balance again"* in so many words.

**The $60 floor, and why it is not $50.** Hyperliquid's own `min_fund_usd` is 50.0
(read per account off `GET /v1/perp/setup`; use the larger of it and yours —
`desk.js:hlMin`/`fundFloor`). After the ~55 bps toll a $50 deposit lands at $49.7, and
HL will not take an order under **$10 of position** — so $60 is the smallest deposit
that leaves a person an actual trade (`desk_fere.DESK_FUND_MIN`). Print both numbers
and the reason: `fund_floor_error` says *"$60 is the least you can move. Hyperliquid
needs $50 to switch your account on, and the $60 leaves enough after the bridge fee to
actually take a trade."* A bare minimum with no reason is the kind of line people
retype three times before giving up.

Offer **only chains this skill verifies** (`desk_fere.FUND_CHAINS`: Base — marked the
cheap way in — Arbitrum, Ethereum, Polygon, BNB, Solana, and Robinhood Chain with its
untested-gasless caveat printed), and never name one that is not in the table.
Amounts on the wire are smallest-units strings computed with `Decimal`, rounded **down**
(`desk_fere.token_units` / `usdc_units`) — Fere returns balances as strings,
`"2.065E-15"` included.

## 8. Measured live, end to end (2026-09-15, owner's account, through the product)

Fund **$97.35 USDC-Base → $96.83 landed** (53.4 bps, 15.8 s) · top routable card ARB
LONG, `prepare` → 166.6 ARB isolated 1×, `perp/open` **filled in 7.0 s at 5.5 bps
fee** · `frontendOpenOrders` showed the card's TP 0.1695 / SL 0.1399 resting as
**reduce-only triggers** · `perp/close` in **4.6 s**, position gone and **both
triggers cancelled with it** (which is why Exit is one button). **Whole run cost 0.59
USDC** — bridge 0.52, venue fees 0.03, the move 0.04. One POST per action, no retries,
credits 200.0 → 200.0.

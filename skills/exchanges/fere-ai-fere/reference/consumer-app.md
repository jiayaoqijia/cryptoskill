# Consumer app

A browser cannot call Fere. The page holds the key. The server is a stateless forwarder: no key, no session, no user row. It cannot trade for anyone, including itself.

## Passthrough

Allowlist method plus path with a full match. Collapse `//` and strip edges before matching. Anything else is 403 and does not open a socket.

```
POST v1/auth/(register|verify|token)
GET  v1/(wallets|holdings)
GET  v1/perp/(setup|orders|markets)
POST v1/perp/(setup|fund|open|close)
POST v1/perp/orders/cancel
POST v1/swap
GET  v1/tasks/[A-Za-z0-9_:.-]{1,128}
```

- Deny `v1/chat` by prefix. It costs 15 credits per query.
- Leave `v1/perp/withdraw` off a public page until the product uses it.
- Add hooks, limit orders, Polymarket, Earn, or notifications only when the product calls them.
- `v1/swap` is on the list so a deposit in any token can become USDC on Base before `perp/fund`.

Timeouts: 20 seconds by default, 130 seconds on `perp/(setup|fund|open|close)` and `v1/swap`. The gateway holds `?wait=true&timeout=90` open, and a fund can run longer than that.

## Headers, limits, logs

- Forward only `authorization`, `content-type`, and `accept`.
- Return `content-type`, `retry-after`, `x-request-id`, and `x-ratelimit*`. Strip hop-by-hop and framing headers, including `content-length` and `content-encoding`.
- Re-quote the path. Forward the query string unchanged, so `?event=wallet-refresh` survives.
- Cap the body at 64 KiB and return 413. Check `Content-Length` before reading.
- Rate-limit per IP on the last `X-Forwarded-For` hop. The first hop is client-supplied.
- Give any unauthenticated endpoint that does real work its own limit. A sync prepare that calls Hyperliquid will block a worker.
- Log `method path status ms`. Never log the bearer, the body, or the query.
- Send `X-Content-Type-Options: nosniff` on every response, including refusals.
- Retry a JIT certificate error on GET only. Never re-send a POST that may have reached Fere.

## CSP

The seed is in the browser. No script runs unless it came from this origin as a file.

```
default-src 'none'; script-src 'self';
style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
font-src https://fonts.gstatic.com; img-src 'self' data:;
connect-src 'self' https://api.hyperliquid.xyz;
base-uri 'none'; form-action 'none'; frame-ancestors 'none'; object-src 'none'
```

Also send `Referrer-Policy: no-referrer`.

Stamp the CSP where the bytes leave disk, not on a path match. Encoded or trailing-slash paths such as `/%2e/app.html` and `/app.html/` otherwise skip the policy. `script-src 'self'` means no inline script and no third-party chart library. `style-src 'unsafe-inline'` is acceptable. CSS cannot read storage.

## Writes

`idempotency_key` is accepted and not enforced. One key per tap, generated in the client, is a label. It is not a lock.

- Never re-send a write. On 401, re-mint the bearer and retry a GET once. A non-GET throws.
- A read timeout is unknown. Reconcile by reading the position.
- Do not put an idempotency key on `perp/fund`. The field is undocumented there, and an unenforced key looks like a safe retry.

A fill is all three of these, or the screen says unconfirmed:

1. A positions diff, not presence. Snapshot the position before sending. Growth past rounding, or a side flip, is the fill.
2. The task says `SUCCESS`, polled with a deadline. An unknown id stays `200 PENDING` forever.
3. The brackets are read back from the venue. `tp_oids` and `sl_oids` come back empty while the triggers are resting.

`SUCCESS` without growth, or growth without `SUCCESS`, is neither a fill nor a rejection. Say so.

Read positions, fills, brackets, and balances from Hyperliquid. They are public and work when Fere does not. Key them on `GET /v1/perp/setup` → `eoa_address`, not on the Fere EVM address. Those two are not promised to match. Send writes through Fere.

## Prepare

The server turns "$25 at 3×" into the `POST /v1/perp/open` body. Prepare places nothing and needs no auth.

- Read the mark from Hyperliquid `allMids` at prepare time. No cache. No live price means 409, not a stale price.
- Round size down to `szDecimals` with `Decimal`. `szDecimals` 0 means integer contracts. A size that rounds to 0 is a rejection. Size is base token, not dollars.
- Round order prices to at most 5 significant figures and at most `6 − szDecimals` decimals (Hyperliquid's perp price rule). Do not round observed prices.
- Refuse notional under $10 and say the arithmetic. Clamp leverage to the market cap and report the clamp.
- Use isolated margin (`is_cross: false`) when the UI promises a bounded loss. Cross backs the position with the whole balance.
- Return `side`, the live mark, the card mark, drift, TP, and SL. If the side flipped or price moved more than 0.5%, re-render. Do not send.

## HIP-3

`GET /v1/perp/markets` is the main dex only. Hyperliquid has more markets on builder dexes. `perp/open` rejects prefixed names (`xyz:NVDA` and the other spellings) with `Unknown Hyperliquid perp asset`. Each builder dex has its own clearinghouse, and Fere has no transfer into it.

Mark those markets unroutable, with the reason, before the user can tap.

## Funding

Get USDC on Base, then fund Hyperliquid. One step at a time.

| Step | Call |
|---|---|
| Deposit | The wallet's EVM or Solana address. Any liquid token. No gas coin. |
| Convert, if it is not USDC on Base | `POST /v1/swap` to USDC on chain 8453, `slippage_bps` 300 |
| Onto Hyperliquid | `POST /v1/perp/fund` with `source_chain_id` 8453 |
| Confirm | Hyperliquid `clearinghouseState.marginSummary.accountValue` on `eoa_address` |

`perp/fund` runs setup. Do not call `perp/setup` first.

Pin the swap the moment it is sent, including across a reload. A retry skips the swap if USDC is already on Base. Size the fund leg on what landed, not on the amount you asked to swap. Release the pin only on a source change, a definitive rejection, or a completed deposit.

Confirm both legs by reading a balance, with `?event=wallet-refresh` on holdings. A wait that gives up early makes a working transfer look failed, and that is what makes someone send it twice. Say that nothing was re-sent.

`min_fund_usd` is 50. After the bridge toll a $50 deposit can land under $50, and an order under $10 is rejected. Fund at least $60 and say why.

Amounts on the wire are smallest-unit strings, rounded down. Balances come back as strings, including scientific notation.

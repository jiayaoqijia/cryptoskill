---
name: avee-data-api
description: Query avee's keyless REST API (/api/v1) for DEX market data — liquidity pairs, tokens, token safety briefs and signed scam verdicts, OHLCV candles, trades, holders, wallet PnL and trader rankings, chain and protocol leaderboards, trending and new pairs, launchpad launches, and perpetual markets. Use when the user asks for on-chain DEX data (Robinhood Chain, HyperEVM, TON, Hyperliquid and other chains avee indexes), wants to look up a token by symbol or address, check whether a token is safe, or write code that calls the avee API. Covers the base URL, keyless rate limits and backoff, pagination, error codes, and paying per call with x402 when the user supplies a payer.
license: MIT
metadata:
  author: avee
  version: "0.1.0"
---

# avee data API

Read-only DEX market data over plain HTTPS. **No key and no sign-up**: every route answers an
anonymous request.

- Base URL: `https://api.preview.avee.tech/api/v1` (the preview environment; it serves the current contract).
- The live contract: `GET /openapi.yml` (OpenAPI 3.1) and `GET /llms.txt` on the same base. When this
  skill and the served document disagree, the served document wins.
- Docs: https://docs.preview.avee.tech

## Rules that prevent wrong answers

1. **A target is a chain plus an address.** If the user gives a name or symbol, resolve it first
   (next section). Never guess an address.
2. **Chains** are a slug (`robinhood`) or a numeric id (`4663`). The set grows: read `GET /chains`,
   never hardcode it.
3. **Addresses:** on EVM chains `0x` is optional and case does not matter; responses come back
   lower-case. TON, Solana and Hyperliquid addresses are used exactly as given.
4. **Safety questions go to the brief**, not to price or liquidity alone:
   `GET /chains/{chain}/tokens/{address}/brief`. Read `verdict.status`: `blocked` means avee holds a
   block, `watch` means evidence short of a block, `ok` means nothing is recorded (**not** a
   clearance), `unknown` means nobody has evaluated it (**never** read it as "not blocked").
   A block that is absent from the brief (`holders`, `deployer`) was not measured; it is not zero.
5. **Liquidity has two figures:** `liquidity_usd` includes uncollected LP fees,
   `liquidity_onchain_usd` is the withdrawable principal.
6. **Numbers are USD unless the field name says otherwise;** timestamps are UTC.

## Find a token by symbol first

```bash
curl 'https://api.preview.avee.tech/api/v1/search?q=WETH&chains=robinhood&limit=5'
```

The answer has `tokens[]` (`address`, `network`, `symbol`, `price_usd`) and `pairs[]`
(`pair_address`, `network`, `ticker`, `liquidity_usd`). Several tokens can share a symbol: prefer
the one with the deepest liquidity, and tell the user when the match is ambiguous. For a ranked
list with market figures, use `GET /tokens?q=WETH`.

## The routes you will use most

```bash
B='https://api.preview.avee.tech/api/v1'
curl "$B/chains"                                                        # what is live, and chain lag
curl "$B/pairs?chains=robinhood&sort=volume&timeframe=24h&limit=10"     # pair screener
curl "$B/chains/robinhood/pairs/{pair}"                                 # one pair
curl "$B/chains/robinhood/pairs/{pair}/candles?res=1H&from=$(($(date +%s)-86400))&to=$(date +%s)"  # OHLCV, from and to required
curl "$B/chains/robinhood/pairs/{pair}/trades?limit=50"                 # trade tape
curl "$B/chains/robinhood/tokens/{token}"                               # token in full
curl "$B/chains/robinhood/tokens/{token}/brief"                         # safety decision in one call
curl "$B/tokens?chains=robinhood&sort=market_cap&limit=20"              # token market list
curl "$B/wallets?chain=robinhood&window=7d&sort=realized_pnl&exclude_bots=true&limit=20"  # top traders
curl "$B/chains/robinhood/wallets/{wallet}/positions?state=open"        # a wallet's positions
curl "$B/leaderboard?scope=protocols&chain=robinhood"                   # DEX and launchpad board
```

Every route, with its cost and keyless pace, is in [references/routes.md](references/routes.md).
Useful enums: `sort` on `/pairs` = `liquidity, volume, transactions, price_change, score, apr,
created_at, popular, hottest, trending`; `timeframe` = `5m, 1h, 6h, 24h`; candle `res` = `1, 5, 15,
30, 1H, 4H, 12H, 1D, 1W, …`; wallet `window` = `1d, 7d, 30d, 1y, all`.

**Recently added routes** (trending, new pairs, launchpads, holders, token traders, perps, deployers,
wallet funding, oracle prices, pair batch) may answer `404` with code `not_found` and the detail
"no operation is served at this path" on a host that has not been upgraded yet. That is not a
missing token. Fall back: trending → `/pairs?sort=trending`, new pairs →
`/pairs?chains=X&sort=created_at` or `max_age_seconds`, perps →
`/pairs?chains=hyperliquid&market_type=perp`.

## Pagination

Lists return `{items, next_cursor, prev_cursor}`. Pass `next_cursor` back unchanged as `cursor` and
stop when it is absent. Never build or decode a cursor. An empty `items` with a cursor still present
can happen under a sparse filter: keep going. There is no total count. The keyless page ceiling is
**50**; a larger `limit` is `400 invalid_param`, not a shorter page.

## Limits and backoff

Keyless: one budget per client address, **5 calls per second, burst 20**, shared by every route.
Heavier routes spend more of it (a pair lookup is 2 units, wallet rankings 5, a token batch 10), so
wallet analytics run at about one call per second.

- Read `RateLimit` / `X-RateLimit-Remaining` on every answer and slow down before you hit zero.
- On `429`, wait the `Retry-After` seconds, then retry. Retry repeated `429`s with exponential
  backoff plus jitter. Never retry in a tight loop, and never run wallet calls in parallel.
- `503 upstream_unavailable` and `504 upstream_timeout` are safe to retry with backoff.
- Poll with `If-None-Match: <etag>`: an unchanged answer is `304` with no body and costs you nothing
  to parse.

Details, the error table and header semantics: [references/limits-and-errors.md](references/limits-and-errors.md).

## Errors

Every non-2xx is `application/problem+json` with a stable `code`. **Branch on `code`, never on
`detail`.** Codes: `invalid_param` (read `param`), `key_in_query`, `invalid_api_key`,
`plan_required`, `chain_not_found` (read `GET /chains`), `not_found`, `rate_limited`, `internal`
(quote `request_id`), `upstream_unavailable`, `upstream_timeout`.

## Paying past the keyless limit (x402)

Only when x402 is enabled on the host **and** the user has given you a payer (a wallet or an x402
client they control). Never pay, sign or move funds on your own initiative. Otherwise treat a `429`
as "wait". How it works: [references/x402.md](references/x402.md).

# MEXC Spot WebSocket Streams

Source basis: official Spot V3 docs checked 2026-05-30.

## Bases

- Public: `wss://wbs-api.mexc.com/ws`
- Private: `wss://wbs-api.mexc.com/ws?listenKey=<listenKey>`
- Listen-key REST: `https://api.mexc.com`

## Lifecycle

```json
{"method":"SUBSCRIPTION","params":["spot@public.aggre.deals.v3.api.pb@100ms@BTCUSDT"]}
{"method":"UNSUBSCRIPTION","params":["spot@public.aggre.deals.v3.api.pb@100ms@BTCUSDT"]}
{"method":"PING"}
```

## Public Channels

- Trades: `spot@public.aggre.deals.v3.api.pb@(100ms|10ms)@<symbol>`
- Diff depth: `spot@public.aggre.depth.v3.api.pb@(100ms|10ms)@<symbol>`
- Partial depth: `spot@public.limit.depth.v3.api.pb@<symbol>@(5|10|20)`
- Book ticker: `spot@public.aggre.bookTicker.v3.api.pb@(100ms|10ms)@<symbol>`
- Batch book ticker: `spot@public.bookTicker.batch.v3.api.pb@<symbol>`
- K-lines: use documented `spot@...v3.api.pb` channel for the interval.

Symbols are uppercase, e.g. `BTCUSDT`. Current public pushes use protobuf: `https://github.com/mexcdevelop/websocket-proto`.

## Local Order Book

Subscribe to diff depth, fetch REST snapshot `GET /api/v3/depth?symbol=<symbol>&limit=1000`, ignore older updates, require `fromVersion == previous toVersion + 1`, apply absolute quantities, and reinitialize on any gap.

## Private Streams

Listen-key endpoints: `POST|GET|PUT|DELETE /api/v3/userDataStream` through the Spot REST helper with `--signed`. Extend every 30 minutes; listen keys last 60 minutes.

Private channels: `spot@private.account.v3.api.pb`, account orders, and account deals. Treat listen keys as temporary secrets.

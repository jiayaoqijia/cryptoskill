# MEXC Futures WebSocket Streams

Source basis: official Futures docs checked 2026-05-30.

## Base

`wss://contract.mexc.com/edge`

## Use

- Public channels: trades/deals, tickers, klines, depth, funding, fair/index price where documented.
- Private channels: balances, positions, orders, and fills after current official login/auth flow.
- Order books: REST snapshot plus WebSocket increments; reinitialize on sequence gaps.

## Private Requirements

Read `MEXC_API_KEY` and `MEXC_API_SECRET` from env vars, sign login/auth payloads according to the current official Futures WebSocket page, redact `ApiKey`, signatures, and account data in logs, and resubscribe idempotently after reconnect.

## Connection Handling

Handle ping/pong, reconnect with exponential backoff, resubscribe after reconnect, and expect documented payload compression for deal/depth streams.

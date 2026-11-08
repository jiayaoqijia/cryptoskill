---
name: mexc-spot-websocket
description: MEXC Spot WebSocket workflows for public streams, protobuf handling, depth maintenance, listen keys, and private streams without exposing API keys.
---

# MEXC Spot WebSocket

## Workflow

Use this skill for streaming, not one-off REST queries. Open `references/streams.md` only for exact stream names and lifecycle details.

1. Use public REST endpoints for snapshots and WebSocket streams for increments.
2. Use `wss://wbs-api.mexc.com/ws` for public Spot streams.
3. For private streams, use `/mexc-spot-rest` to create a signed listen key, then connect to `/ws?listenKey=...`.
4. Do not print or persist listen keys except in local process memory needed for the connection.
5. Reconnect before the 24-hour connection limit and extend listen keys every 30 minutes.
6. Decode current public pushes with MEXC protobuf files.
7. Use REST for initial balances/order books; private streams and depth streams are updates after snapshots.
8. For balance/account snapshots, use `/mexc-spot-rest` quick commands and the REST skill lookup helper before opening REST or stream references.

## Safety Rules

- Do not request API keys in chat. Use the Spot REST skill for listen-key creation.
- Treat listen keys as temporary secrets.
- Implement exponential backoff on reconnects.
- Respect 100 messages per second and 30 streams per connection.
- For local order books, restart from a REST snapshot when sequence versions gap.

## Verification

Before production code, verify subscription shape, protobuf channel suffixes, depth sequence continuity, and listen-key extension.

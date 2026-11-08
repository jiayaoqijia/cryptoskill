---
name: mexc-futures-websocket
description: MEXC Futures WebSocket workflows for public streams, private account/order/position streams, ping/pong, subscriptions, and depth maintenance.
---

# MEXC Futures WebSocket

## Workflow

Use this skill for streaming contract data and private futures events. Open `references/streams.md` only for exact stream names and lifecycle details.

1. Use `wss://contract.mexc.com/edge`.
2. Use public channels for market data and private channels only when the user has configured environment-variable credentials.
3. For private auth code, use Futures REST signing rules and redact `ApiKey`, `Signature`, and the secret.
4. Handle ping/pong and reconnects explicitly.
5. Use REST snapshots plus WebSocket increments for order book maintenance.
6. Treat compressed payload behavior as current-default for deal and depth streams.
7. Use REST for initial assets/order books; private streams and depth streams are updates after snapshots.
8. For balance/account snapshots, use `/mexc-futures-rest` quick commands and the REST skill lookup helper before opening REST or stream references.

## Safety Rules

- Do not request API keys in chat. Use env vars and redact signed login payloads.
- Do not persist private stream auth tokens, signatures, or account event payloads to logs unless redacted.
- Reconnect with backoff and resubscribe idempotently.
- Rebuild order books from snapshot on any sequence gap.
- Respect endpoint and stream rate limits from the official docs.

## Verification

Before production code, verify base URL, public auth requirements, current private login flow, and order-book gap recovery.

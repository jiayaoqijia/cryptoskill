# perp-cli/ws — live market, funding and account streams (library)

`perp-cli/ws` is a composable WebSocket library inside the `perp-cli` npm package. Use it to build a
custom live dashboard, funding comparison or price/account feed for **hyperliquid** (native + HIP-3),
**pacifica**, **lighter**, **lighter-rh**, **aster** and **arcus**, in the browser or in Node.

> **Stability:** 0.14.x is **@experimental** — breaking changes only in a minor bump (CHANGELOG
> callouts); every event carries `schema: 1`. Stable from **0.15.0**.

Runnable examples: `examples/ws-funding-compare-browser`, `examples/ws-next-smoke`,
`examples/ws-node-stream` in the perp-cli repository.

## 1. Install and import

```sh
npm install perp-cli
```

| Runtime | Import | Transport |
|---|---|---|
| Browser (any bundler, Next.js, Vite, static page) | `perp-cli/ws` | the page's native `WebSocket` and `fetch` |
| Node 20+ | `perp-cli/ws/node` | `ws` (Node 20 has no global `WebSocket`); same API |

- ESM only, ES2020, no side effects, no top-level await, touches no global at module load (safe in
  SSR / prerendering). Next.js 13.5+: `transpilePackages: ["perp-cli"]`.
- TypeScript: `moduleResolution` `"bundler"`, `"node16"` / `"nodenext"`, or `"node"` (via `typesVersions`).
- Only `perp-cli/ws`, `perp-cli/ws/node` and `perp-cli/package.json` are importable (no deep imports).
- `perp-cli/ws` in Node 20 without a `transport` throws `INVALID_PARAMS` ("import from perp-cli/ws/node or
  pass transport").

## 2. Minimal examples

All-market state for one venue (Node):

```ts
import { createVenueStream, hyperliquid, toApr } from "perp-cli/ws/node";

const stream = createVenueStream(hyperliquid, { hip3Dexes: ["xyz"] }); // HIP-3 dexes are opt-in
stream.onState((s) => console.log("state", s.status));
const sub = stream.subscribe({ kind: "allMarkets", symbols: ["BTC", "ETH", "xyz:TSLA"] });
sub.on((e) => {
  if (e.type === "market") {
    console.log(e.symbol, e.mark, e.funding.rate, e.funding.rateKind, toApr(e.funding.rate, e.funding.rateIntervalHours));
  } else if (e.type === "error") {
    console.error(e.code, e.message, e.remediation);
  }
});
await sub.ready; // rejects with a WsError (code + remediation)
// …later
await stream.close();
```

Async iteration instead of callbacks:

```ts
import { createVenueStream, pacifica } from "perp-cli/ws/node";

const stream = createVenueStream(pacifica);
for await (const e of stream.subscribe({ kind: "market", symbol: "BTC", channels: ["market", "bbo"] })) {
  if (e.type === "bbo") console.log(e.bid, e.bidSize, e.ask, e.askSize);
  if (e.type === "market") break; // break → unsubscribes
}
await stream.close();
```

Funding comparison across venues (browser):

```ts
import {
  arcus, aster, createFundingComparator, createVenueStream, hyperliquid, lighter, lighterRh, pacifica, toHourly,
} from "perp-cli/ws";

const streams = [hyperliquid, pacifica, lighter, lighterRh, aster, arcus].map((c) => createVenueStream(c));
const cmp = createFundingComparator({ streams, kind: "next", minVenues: 2 });
const off = cmp.subscribe((rows) => {
  for (const row of rows) {
    const hourly = row.legs
      .filter((l) => !l.stale && l.rate !== null)
      .map((l) => ({ venue: l.venue, kind: l.rateKind, h: toHourly(l.rate, l.funding.rateIntervalHours) }));
    console.log(row.canonical, row.mixedKinds, hourly);
  }
});
// …later
off();
cmp.close();
await Promise.all(streams.map((s) => s.close()));
```

## 3. Streams, subscriptions, connection state

- `createVenueStream(codec, opts)` — one socket per venue, opened lazily on the first subscription, closed
  (`idle`) when the last one leaves. The market directory is loaded once over REST (`stream.markets()`).
- `subscribe(target)`:
  - `{ kind: "allMarkets", symbols? }` → `MarketUpdate` for every (or the listed) market;
  - `{ kind: "market", symbol, channels: ["market" | "bbo"] }` (`book`, `trades` arrive in 0.14.5);
  - `{ kind: "user", channels: ["account" | "positions" | "orders" | "fills"] }` (needs `credentials`).
  Unknown symbols reject with `INVALID_PARAMS` before anything is sent.
- `Subscription`: `on(cb)` (unbuffered), `for await` (bounded buffer, `opts.buffer.size`, default 1024),
  `ready` (resolves when every wire channel is acknowledged; rejects with a `WsError`), `status`,
  `unsubscribe()`. Wire channels are ref-counted: two subscriptions on one venue channel = one wire
  subscription.
- Connection state (`stream.state`, `stream.onState(cb)`, and `{type:"state"}` events):
  `idle → connecting → live ⇄ stale → reconnecting → … → closed`. `stale` = no message on a channel for
  `staleAfterMs` (from message timestamps, re-checked when a hidden tab becomes visible); 2× → forced
  reconnect. Reconnect backoff 1 s → 30 s with jitter, a per-venue new-connection budget, then
  resubscribe; the first frame after a (re)subscribe has `source: "snapshot"`.
- `closed` is terminal: a later `subscribe` rejects with the close reason. A handshake failure before
  open = `EXCHANGE_UNREACHABLE` ("network, venue outage, or Origin/CORS block").
- Ack timeout: no acknowledgement and no data within the channel's stale threshold → a **pending**
  subscription fails with `WS_PROTOCOL_ERROR`.
- Iterator buffer: market/bbo/account/positions/orders events are **state** and coalesce by key (never
  fatal). Fills and control events are not coalesced; a full buffer → fatal `STREAM_OVERFLOW` and the
  subscription closes. Before the iterator exists, state/error controls are kept in a ring of the last
  `size` (the iterator first gets a non-fatal `STREAM_OVERFLOW` with the discarded count); fills and
  gaps are never evicted.

## 4. Event fields and nullability

Rules: **unknown = `null`, never `0`**. A field the venue never sent is `null`; a field the latest frame
did not carry keeps its last value, with `asOf[field]` = receive time. `Dec` = the venue's decimal string
(exact; parse it yourself). Check `null` before arithmetic — `null` is not zero.

`MarketUpdate`: `venue, dex, symbol, venueSymbol, quote, canonical, mark, index, bestBid, bestAsk, last,
funding{ rate, rateKind, rateSource, rateIntervalHours, settlementIntervalHours, intervalSource,
nextFundingTime, predictedRate, marketClosed }, openInterest{ value, unit: "base"|"usd"|null, sides },
volume24hNotional, venueTs, recvTs, source, changed[], asOf{}`.

Funding:
- `rate` is **raw per `rateIntervalHours`** — never pre-annualized. Use `toHourly(rate, h)` to compare and
  `toApr(rate, h)` only for display (both return `null` for `null` input).
- `rateKind`: `"lastSettled"` (the last payment), `"accruing"` (the current period so far, the "if it
  settled now" rate), `"predicted"` (the venue's estimate of the next payment). `predictedRate` is always
  kind `"predicted"`.

| Venue | `rate` kind | `predictedRate` | interval | OI | notes |
|---|---|---|---|---|---|
| hyperliquid | accruing | null | 1 h | base, one side | bid/ask/last null → `bbo` channel |
| pacifica | lastSettled | next_funding | 1 h | base | bid/ask/last/nextFundingTime null |
| lighter / lighter-rh | lastSettled | current_funding_rate | 1 h | **usd** | wire values are percent/h, emitted as fractions/h |
| aster | accruing | null | per market (`rest:/fapi/v3/fundingInfo`, null if missing) | null | all quotes (USDT, USD1, …) with `quote` set |
| arcus | lastSettled | nextFundingRate | 1 h | base, one side | bid/ask null → `bbo` channel |

`stream.capabilities` carries the full matrix: `browser`, `networks`, `channels`, `fields` (false = always
null) and `notes` (why). lighter-rh has no testnet (`CAPABILITY_UNSUPPORTED`).

`BboUpdate`: `bid, bidSize, ask, askSize` (null = that side of the book is empty), `venueTs, recvTs`.
Venue sequence numbers only drop out-of-order frames (they are not contiguous; bbo never emits gaps).
Pacifica allows ≤ 20 bbo channels per connection (`SUBSCRIPTION_LIMIT` beyond).

## 5. Funding comparator

```ts
import { createFundingComparator, type FundingRow, type VenueStream } from "perp-cli/ws";

declare const streams: VenueStream[];
const cmp = createFundingComparator({ streams, kind: "next", include: ["BTC", "ETH"], minVenues: 2 });
const rows: FundingRow[] = cmp.rows();
```

- `kind`: `"current"` (default; each leg's `rate`, `mixedKinds` flags rows mixing kinds), `"predicted"`,
  `"lastSettled"`, `"accruing"`, and **`"next"`** — per venue the accruing rate when published, else the
  predicted one. A leg without the requested kind has `rate: null, kindUnavailable: true` (never
  substituted).
- A leg is `stale` when its stream is not `live` or its rate is older than 2 × the venue's
  `staleAfterMs` (Arcus 3×). Skip stale legs.
- `canonical`: `defaultCanonicalize` maps HIP-3 to `"<dex>:<BASE>"` and USD-like quotes (USDT, USD1,
  USDC, USD, USDG) to `"<BASE>"`; any other quote → `null` (not compared). Pass `canonicalize` to change it.
- `onControl` receives the streams' `state` / `error` events and `{type:"listener-error"}`.

## 6. User (account) channels

```ts
import { createVenueStream, lighter, type CredentialProvider } from "perp-cli/ws";

const credentials: CredentialProvider = {
  user: async () => ({ venue: "lighter", accountIndex: 12345 }),
  // Only Lighter's orders channel needs a token. Your backend mints it; the page never sees the key.
  authToken: async ({ purpose, maxTtlSec }) => {
    const res = await fetch(`/api/lighter-token?purpose=${purpose}&ttl=${maxTtlSec}`);
    return (await res.json()) as { token: string; expiresAt: number }; // expiresAt: epoch ms
  },
};
const stream = createVenueStream(lighter, { credentials });
const sub = stream.subscribe({ kind: "user", channels: ["account", "positions", "orders", "fills"] });
sub.on((e) => {
  switch (e.type) {
    case "account": console.log(e.equity, e.available); break;
    case "positions": console.log(e.positions.length, e.snapshot); break;
    case "orders": console.log(e.orders.length, e.complete); break;
    case "fills": console.log("snapshot batch", e.fills.length); break;
    case "fill": console.log(e.fillId, e.fill.side, e.fill.size, e.fill.price, e.fill.clientId); break;
    case "gap": console.log("refetch over REST:", e.channel); break;
    default: break;
  }
});
```

- **The library never holds keys.** `CredentialProvider` is async callbacks: `user()` (the account
  identity), `authToken({ purpose, maxTtlSec })` (Lighter `account_all_orders`; re-called at 80 % of the
  TTL with backoff retries; a read-only `ro:` token is recommended in browsers), `hmacSha256` /
  `signTypedData` (reserved for 0.14.5 venues). Tokens handed in are redacted from every error, log and
  raw excerpt.
- `allowInPageSecrets: true` is required for venues whose auth needs a signing secret in the page
  (Aster / Ondo / QFEX, 0.14.5). Without it they reject `CAPABILITY_UNSUPPORTED` in a browser.
- `UserRef` per venue: hyperliquid `{ address }` (no auth), pacifica `{ account }` (Solana address, no
  auth), lighter / lighter-rh `{ accountIndex }`, arcus `{ address, subaccount }` (`null` = account 0, no auth).
- **KNOWN GAP (0.14.4): Aster user channels are not implemented** — `kind: "user"` on aster rejects
  `CAPABILITY_UNSUPPORTED` (no parity; 0.14.5).

Events:
- `account` — `equity, available, marginUsed, unrealizedPnl` (+ `dex` on hyperliquid, one per perp dex);
  `source: "snapshot"` when the frame was a full snapshot.
- `positions` / `orders` — always the **full current set** (snapshot + merged deltas).
  `orders.complete` = every part of the set came from a venue snapshot. **Pacifica sends no order
  snapshot: `complete` stays `false` — refetch open orders over REST.**
- `fills` (`snapshot: true`) — ONE event per venue fill snapshot (HL / Arcus replay recent fills on every
  (re)subscribe; up to 2000), only fills not seen before. `fill` (`snapshot: false`) — one live fill.
  De-duplicated in-library by `fillId` + side + order id (both legs of a self-trade are kept).
- `gap { channel, action: "refetch-required" }` — the library cannot give a complete picture; refetch
  over REST: after a reconnect on non-replayable channels (Pacifica fills + orders, Lighter fills), at
  subscribe for Pacifica orders, and when a replayed fill snapshot does not reach back to the fills seen
  before (outage longer than the replay window).

`clientId`, fees and liquidation price per venue:

| Venue | `OrderRow.clientId` | `FillRow.clientId` | `FillRow.fee` | `PositionRow.liquidationPrice` |
|---|---|---|---|---|
| hyperliquid | cloid (null if none) | cloid only when the frame carries one (not documented) → join by `orderId` | fee in `feeToken` | liquidationPx (null when none) |
| pacifica | `I` | `I` | `f` (feeToken null) | `l` (null when not applicable) |
| lighter / lighter-rh | client_order_id (0 = none → null) | ask/bid client id of your side (0 → null) | usd_amount × rate × 1e-6 (rate in 1e-6, omitted when 0) | liquidation_price; "0" (none) → null |
| arcus | clientId | clientId | `fee` (feeToken null) | always null (not published) |

Mark price in `PositionRow` is null except on Arcus — join the `MarketUpdate` by symbol.

## 7. Errors

`StreamControl { type: "error", code, message, remediation, raw (redacted ≤ 200 chars), fatal }` — always
check `fatal`: a fatal error ended that subscription, a non-fatal one is informational (it keeps running);
`ready` rejects with a `WsError` whose `structured = { code, message, status, retryable, remediation? }`.

| Code | Meaning / what to do |
|---|---|
| `WS_PROTOCOL_ERROR` | malformed / unrecognised frame, or no ack — reported, never silently dropped |
| `WS_AUTH_FAILED` | credentials problem. **Check `fatal`:** non-fatal = a token refresh failed and is being retried (the channel still works with the current token); fatal = no / expired / definitively rejected credentials, the subscription ended |
| `SUBSCRIPTION_LIMIT` | venue or `budget` limit (`details.needed` / `allowed`) — narrow the subscription |
| `STREAM_OVERFLOW` | iterator buffer full — consume faster, use `on()`, raise `buffer.size` |
| `CAPABILITY_UNSUPPORTED` | channel / network not available for the venue (see `capabilities.notes`) |
| `EXCHANGE_UNREACHABLE` | network / outage / handshake refused (reconnects automatically) |
| `INVALID_PARAMS` | bad symbol, dex, channel or option |
| `RATE_LIMITED`, `EXCHANGE_ERROR` | REST bootstrap failures |

## 8. Budgets and limits

- `budget: { maxSubscriptions, newConnectionsPerMin }` caps below the venue limits (checked before sending).
- **Per-IP limits are shared by every tab and app on one IP** (HL: 10 connections, 1000 subscriptions,
  30 new connections/min, 10 users). Several tabs of one dashboard share them — keep one stream per venue
  per page.
- HL `allMarkets` is a single `allDexsAssetCtxs` subscription; `hip3Dexes: "all"` adds every HIP-3 dex.

## 9. Do / don't

- **Do** treat every field as nullable; `null ≠ 0`. Don't default missing data to 0.
- **Do** compare funding per hour (`toHourly`) and like-for-like kinds (comparator `kind`); **don't**
  annualize in your data layer (`toApr` is for display).
- **Do** check `quote` before comparing (Aster lists USDT, USD1 and other quotes per base).
- **Don't** add a REST fallback when a field is null or a channel is unsupported — the capability matrix
  says why; show it as unknown.
- **Do** handle `gap → refetch-required` (refetch fills / open orders over REST) and `orders.complete`.
- **Do** respect `SUBSCRIPTION_LIMIT` and the per-IP note above; coalesce UI updates (~1/s).
- **Don't** pass private keys to the library; return short-lived tokens from `authToken()`.

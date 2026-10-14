# perp-cli/ws — live market, funding and account streams (library)

`perp-cli/ws` is a composable WebSocket library inside the `perp-cli` npm package. Use it to build a
custom live dashboard, funding comparison or price/account feed for **hyperliquid** (native + HIP-3),
**pacifica**, **lighter**, **lighter-rh**, **aster** and **arcus**, in the browser or in Node.

> **Stability:** ships in **0.15.0** and is **@experimental** through 0.15.x — breaking changes only in a
> minor bump (CHANGELOG callouts); every event carries `schema: 1`. **@stable from 0.16.0** after consumer
> sign-off. Planned for **0.15.1**: Aster user channels, Ondo / QFEX, `book` / `trades`, `perp stream`.
> The `VenueId` type already includes `"ondo"` and `"qfex"`, but there are no codecs for them until 0.15.1.

Runnable examples: `examples/ws-funding-compare-browser`, `examples/ws-next-smoke`,
`examples/ws-node-stream` in the perp-cli repository.

## 1. Install and import

Two packages, **the same code and API** (built from one source):

| Package | Install | When |
|---|---|---|
| **`@hypurrquant/perp-ws`** (recommended for integrators) | `npm install @hypurrquant/perp-ws` (+ `ws` for the Node entry) | apps, dashboards, bots — **no dependencies** (~100 KB ESM) |
| `perp-cli/ws` | `npm install perp-cli` | perp-cli is already installed (the CLI pulls ~140 MB of CLI deps) |

| Runtime | `@hypurrquant/perp-ws` | `perp-cli` | Transport |
|---|---|---|---|
| Browser (any bundler, Next.js, Vite, static page), Node ≥ 22 without `ws` | `@hypurrquant/perp-ws` | `perp-cli/ws` | the runtime's native `WebSocket` and `fetch` |
| Node 20+ | `@hypurrquant/perp-ws/node` | `perp-cli/ws/node` | `ws` (16 MiB message cap, protocol ping/pong); same API |

- **`ws` for the Node entry:** `@hypurrquant/perp-ws` declares `ws` (`^8.21.0`) as an **optional peer
  dependency** — `npm install @hypurrquant/perp-ws ws`. Importing `/node` never fails; creating a stream
  or transport without `ws` throws `INVALID_PARAMS` ("npm install ws@^8.21.0"). The Node entry uses `ws`
  even on Node ≥ 22 (which has a global `WebSocket`) for the inbound size cap and ping/pong handling; on
  Node ≥ 22 you may use the browser entry instead (global `WebSocket`, no `ws`, no size cap of ours).
  `perp-cli` ships `ws` as a regular dependency.
- ESM only, ES2020, no side effects, no top-level await, touches no global at module load (safe in
  SSR / prerendering). Next.js 13.5+: `transpilePackages: ["@hypurrquant/perp-ws"]` (or `["perp-cli"]`).
- TypeScript: `moduleResolution` `"bundler"`, `"node16"` / `"nodenext"`, or `"node"` (via `typesVersions`).
- Only the entries above (and `<package>/package.json`) are importable (no deep imports).
- The examples below import `@hypurrquant/perp-ws`; with perp-cli, replace it by `perp-cli/ws`
  (`@hypurrquant/perp-ws/node` → `perp-cli/ws/node`). Everything else is identical.
- The Node entry caps one inbound message at 16 MiB (`DEFAULT_MAX_PAYLOAD`; real frames are ≤ ~150 KB).
  An oversized message closes the socket (`reconnecting` reason `WS_PROTOCOL_ERROR`, naming
  `WS_ERR_UNSUPPORTED_MESSAGE_LENGTH`); 3 within 10 min fail the subscriptions with `WS_PROTOCOL_ERROR`.
  Raise the cap with `createVenueStream(codec, { transport: createNodeTransport({ maxPayload }) })`.
- The browser entry in Node 20 without a `transport` throws `INVALID_PARAMS` ("import from the /node
  entry … or pass transport").

### Static page without a bundler

`dist/index.js` of `@hypurrquant/perp-ws` (`dist/ws/index.js` of perp-cli) is one self-contained ESM
file with **no bare imports**, so a plain HTML page can load it through an import map. The map points the
public specifier at the file; your code still imports `"@hypurrquant/perp-ws"` (that is the "no deep
imports" rule: never write `.../dist/...` in JS — the file path lives only in the map, which is the
page's job, like a bundler's resolver):

```html
<script type="importmap">
  { "imports": { "@hypurrquant/perp-ws": "/node_modules/@hypurrquant/perp-ws/dist/index.js" } }
</script>
<script type="module">
  import { createVenueStream, hyperliquid } from "@hypurrquant/perp-ws";
  const stream = createVenueStream(hyperliquid);
  stream.subscribe({ kind: "allMarkets", symbols: ["BTC"] }).on((e) => {
    if (e.type === "market") document.title = `BTC ${e.mark ?? "—"}`;
  });
</script>
```

Serve the page and `node_modules` from the same static server (any origin works: the venues do not check
Origin and their REST CORS is `*`). Do the same with a CDN that serves npm files (e.g.
`https://cdn.jsdelivr.net/npm/@hypurrquant/perp-ws@0.15.0/dist/index.js`). The `/node` entry is
Node-only (it loads `ws`); never map it in a browser.

## 2. Minimal examples

All-market state for one venue (Node):

```ts
import { createVenueStream, hyperliquid, toApr } from "@hypurrquant/perp-ws/node";

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
import { createVenueStream, pacifica } from "@hypurrquant/perp-ws/node";

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
} from "@hypurrquant/perp-ws";

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
  - `{ kind: "market", symbol, channels: ["market" | "bbo"] }`. `"book"` and `"trades"` are already in
    the types but **reject with `CAPABILITY_UNSUPPORTED` until 0.15.1** — don't ship UI that needs them.
    Any other channel name (e.g. `"ticker"`) or an empty `channels` rejects with `INVALID_PARAMS`;
  - `{ kind: "user", channels: ["account" | "positions" | "orders" | "fills"] }` (needs `credentials`).
- **Symbols are the venue's directory symbols, case-sensitive** — not canonical names. `BTC` is `"BTC"` on
  hyperliquid / pacifica / lighter, `"BTC-USD"` on arcus and `"BTCUSDT"` / `"BTCUSD1"` on aster. Pass
  `MarketUpdate.symbol` / `FundingLeg.symbol`, or look them up in `stream.markets()`. Unknown symbols reject
  with `INVALID_PARAMS` before anything is sent; the message carries a "did you mean …" hint
  (`details.suggestions`) when a directory symbol matches case-insensitively or by canonical / base name.
- `Subscription`: `on(cb)` (unbuffered; a listener that throws is isolated — the other listeners and the
  stream keep running — and reported to `opts.logger` as `{ event: "listener-error" }`, not as a stream
  event), `for await` (bounded buffer, `opts.buffer.size`, default 1024),
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
| pacifica | lastSettled | next_funding | 1 h | base, `sides` null | bid/ask/last/nextFundingTime null |
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
import { createFundingComparator, type FundingRow, type VenueStream } from "@hypurrquant/perp-ws";

declare const streams: VenueStream[];
const cmp = createFundingComparator({ streams, kind: "next", include: ["BTC", "ETH"], minVenues: 2 });
const rows: FundingRow[] = cmp.rows();
```

Options and defaults:

| Option | Default | Meaning |
|---|---|---|
| `kind` | `"current"` | which rate each leg contributes (below) |
| `minVenues` | `2` | rows need ≥ this many **distinct venues with a non-null rate** |
| `staleAfterMs` | 2 × the venue's `stream.staleAfterMs` (Arcus 3×) | a leg is `stale` when its stream is not `live` or its rate is older than this. Venue defaults: hyperliquid 30 s (all markets), pacifica 10 s, lighter / lighter-rh 10 s, aster 5 s, arcus 15 s |
| `include` | all | allowlist of canonical symbols |
| `canonicalize` | `defaultCanonicalize` | HIP-3 → `"<dex>:<BASE>"`; USD-like quotes (USDT, USD1, USDC, USD, USDG) → `"<BASE>"`; any other quote → `null` (not compared) |
| `onControl` | none | the streams' `state` / `error` events and `{type:"listener-error"}` |

- `kind`: `"current"` (each leg's `rate`), `"predicted"`, `"lastSettled"`, `"accruing"`, and **`"next"`** —
  per venue the accruing rate when published, else the predicted one. A leg without the requested kind
  has `rate: null, kindUnavailable: true` (never substituted).
- **`mixedKinds`** is true when a row's legs with a rate use different kinds. With `kind: "next"` it is
  **true by design** whenever an accruing venue (hyperliquid, aster: the current period so far) meets a
  predicted one (pacifica, lighter, lighter-rh, arcus: the venue's estimate of the next payment). Both
  are forward-looking estimates of the coming payment, so the row is usable for ranking; care when you
  need exact like-for-like numbers (e.g. P&L attribution, or an accruing rate early in its period that
  can still move a lot) — then use `kind: "accruing"` or `"predicted"` and accept fewer legs.
- **Several legs per venue:** one venue can contribute more than one leg to a row. Aster lists BTC as
  `BTCUSDT` (quote USDT) and `BTCUSD1` (quote USD1); both canonicalize to `"BTC"`. Pick one per venue
  before ranking — by `quote`, or by the most liquid market (below) — or pass a `canonicalize` that
  returns `null` for the quotes you don't want.
- **`fundingVerified`** (per leg): the CLI's verdict that the venue's funding unit and which published
  rate actually settles were confirmed against its funding payments. All six venues in 0.15.0 are
  `true`; a `false` leg (a future venue) is indicative only — the CLI keeps such venues out of funding
  comparison and refuses them as funding-arb legs, so do the same.
- **Filter illiquid outliers before ranking spreads.** Tiny or newly listed markets often show extreme
  rates (hundreds of % APR) that cannot be traded at size. Require a minimum 24 h notional and/or open
  interest per leg; the comparator legs carry no volume, so read it from the same streams:

```ts
import {
  createFundingComparator, createVenueStream, aster, hyperliquid, lighter, toHourly,
  type FundingLeg, type FundingRow, type MarketUpdate,
} from "@hypurrquant/perp-ws";

const streams = [hyperliquid, lighter, aster].map((c) => createVenueStream(c));
// Same wire channel as the comparator's own subscription (ref-counted): no extra venue traffic.
const notional = new Map<string, number>(); // "<venue>|<symbol>" → 24 h notional
for (const s of streams) {
  s.subscribe({ kind: "allMarkets" }).on((e) => {
    if (e.type !== "market") return;
    const u: MarketUpdate = e;
    if (u.volume24hNotional !== null) notional.set(`${u.venue}|${u.symbol}`, Number(u.volume24hNotional));
  });
}

const MIN_NOTIONAL = 1_000_000;
/** One leg per venue: the most liquid market that passes the filter (null volume = unknown → skipped). */
function pickLegs(row: FundingRow): FundingLeg[] {
  const best = new Map<string, { leg: FundingLeg; vol: number }>();
  for (const leg of row.legs) {
    if (leg.rate === null || leg.stale || !leg.fundingVerified) continue;
    const vol = notional.get(`${leg.venue}|${leg.symbol}`);
    if (vol === undefined || vol < MIN_NOTIONAL) continue;
    const cur = best.get(leg.venue);
    if (cur === undefined || vol > cur.vol) best.set(leg.venue, { leg, vol });
  }
  return Array.from(best.values(), (b) => b.leg);
}

const cmp = createFundingComparator({ streams, kind: "next" });
cmp.subscribe((rows) => {
  for (const row of rows) {
    const legs = pickLegs(row)
      .map((l) => ({ venue: l.venue, h: toHourly(l.rate, l.funding.rateIntervalHours) }))
      .filter((x): x is { venue: typeof x.venue; h: number } => x.h !== null)
      .sort((a, b) => a.h - b.h);
    const lo = legs[0];
    const hi = legs[legs.length - 1];
    if (lo !== undefined && hi !== undefined && legs.length >= 2) console.log(row.canonical, lo.venue, hi.venue);
  }
});
```

## 6. User (account) channels

```ts
import { createVenueStream, lighter, type CredentialProvider } from "@hypurrquant/perp-ws";

const credentials: CredentialProvider = {
  user: async () => ({ venue: "lighter", accountIndex: 12345 }),
  // Only Lighter's orders channel needs a token. Your backend mints it; the page never sees the key.
  authToken: async ({ purpose, maxTtlSec }) => {
    const qs = `purpose=${encodeURIComponent(purpose)}&ttl=${encodeURIComponent(String(maxTtlSec))}`;
    // Same-origin request carrying the user's session cookie: the endpoint must authenticate the caller.
    const res = await fetch(`/api/lighter-token?${qs}`, { credentials: "same-origin" });
    if (!res.ok) throw new Error(`lighter-token: HTTP ${res.status}`);
    const body = (await res.json()) as { token: string; expiresAt: number }; // expiresAt: epoch ms
    // Only accept a READ-ONLY auth token in the page; a full token could be used to trade.
    if (typeof body.token !== "string" || !body.token.startsWith("ro:")) throw new Error("lighter-token: expected a read-only ro: token");
    return body;
  },
};

// Server side (sketch of the /api/lighter-token handler; your framework and session store will differ).
interface Session { accountIndex: number }
declare function getSession(req: Request): Promise<Session | null>; // your auth (cookie → session)
declare function mintLighterReadOnlyToken(accountIndex: number, ttlSec: number): Promise<string>; // "ro:…"
const MAX_TOKEN_TTL_SEC = 600; // server-side cap: never trust the client's ttl
export async function handleLighterToken(req: Request): Promise<Response> {
  const session = await getSession(req);
  if (session === null) return new Response("unauthorized", { status: 401 });
  const url = new URL(req.url);
  // purpose is "<venue>:account_all_orders" (lighter or lighter-rh); refresh follows the expiresAt you return.
  if (!/^lighter(-rh)?:account_all_orders$/.test(url.searchParams.get("purpose") ?? "")) return new Response("bad purpose", { status: 400 });
  const asked = Number(url.searchParams.get("ttl"));
  const ttlSec = Math.min(Number.isFinite(asked) && asked > 0 ? Math.floor(asked) : MAX_TOKEN_TTL_SEC, MAX_TOKEN_TTL_SEC);
  const token = await mintLighterReadOnlyToken(session.accountIndex, ttlSec); // the session's own account only
  return Response.json({ token, expiresAt: Date.now() + ttlSec * 1000 });
}
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
  `signTypedData` (reserved for 0.15.1 venues). Tokens handed in are redacted from every error, log and
  raw excerpt.
- `allowInPageSecrets: true` is required for venues whose auth needs a signing secret in the page
  (Aster / Ondo / QFEX, 0.15.1). Without it they reject `CAPABILITY_UNSUPPORTED` in a browser.
- `UserRef` per venue: hyperliquid `{ address }` (no auth), pacifica `{ account }` (Solana address, no
  auth), lighter / lighter-rh `{ accountIndex }`, arcus `{ address, subaccount }` (`null` = account 0, no auth).
- **KNOWN GAP (0.15.0): Aster user channels are not implemented** — `kind: "user"` on aster rejects
  `CAPABILITY_UNSUPPORTED` (no parity; 0.15.1).

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

Where an error surfaces:
- **Thrown synchronously** (`WsError`, `INVALID_PARAMS`) — bad options, before anything starts:
  `createVenueStream` (codec not a codec export, unknown `network`, bad `buffer.size`, no `WebSocket` /
  `fetch` in the runtime and none passed) and `createFundingComparator` (unknown `kind`, bad `streams`,
  `minVenues`, `include`, `staleAfterMs`, or a non-function `canonicalize` / `onControl` / `clock`).
- **`ready` rejects** (and the subscription ends with a fatal error event) — per-subscription problems:
  unknown symbol / channel, `book` / `trades` or an unsupported network (`CAPABILITY_UNSUPPORTED`), budget
  limits, credentials, REST bootstrap failures, ack timeout, a closed stream.
- **Error events** (`{ type: "error" }` via `on()` / the iterator / comparator `onControl`) — everything
  after `ready`: malformed frames, token-refresh retries, reconnects, overflow.

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

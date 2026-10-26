# perp-cli/ws — live market, funding and account streams (library)

`perp-cli/ws` is a composable WebSocket library inside the `perp-cli` npm package. Use it to build a
custom live dashboard, funding comparison or price/account feed for **hyperliquid** (native + HIP-3),
**pacifica**, **lighter**, **lighter-rh**, **aster** and **arcus**, in the browser or in Node.

> **Stability:** shipped since **0.15.0** and **@experimental** through 0.15.x — breaking changes only in a
> minor bump (CHANGELOG callouts); every event carries `schema: 1`. **@stable from 0.16.0** after consumer
> sign-off. Planned, not yet available: Aster user channels, Ondo / QFEX, `book` / `trades`, `perp stream`.
> The `VenueId` type already includes `"ondo"` and `"qfex"`, but there are no codecs for them yet.
> **GRVT** (CLI venue, market data only) has no codec: its public WS has per-instrument selectors only (no
> all-markets stream) and a 150-stream cap below its 184 perpetuals, so `allMarkets` cannot be served.
> **Extended** (CLI venue `extended`, market data only) has no codec: its public streams are one socket
> per stream URL (`wss://api.starknet.extended.exchange/stream.extended.exchange/v1/prices/mark`,
> `/orderbooks/<m>?depth=1`, `/funding`, …) pushed on connect with no subscribe frame (the bare root
> answers HTTP 404), while a codec here is one `url(network)` plus subscribe / unsubscribe frames. Its
> accruing funding rate is REST-only (`/info/markets`); the `/funding` stream is documented as applied
> rates only. Use the CLI (`perp -e extended market …`) for Extended.

Runnable examples: `examples/ws-funding-compare-browser`, `examples/ws-next-smoke`,
`examples/ws-node-stream` in the perp-cli repository.

## 1. Install and import

Two packages, **the same code and API** (built from one source):

| Package | Install | When |
|---|---|---|
| **`@hypurrquant/perp-ws`** (recommended for integrators) | `npm install @hypurrquant/perp-ws` (+ `ws` for the Node entry) | apps, dashboards, bots — **no dependencies** (~170 KB ESM, ~41 KB gzip; 0.16.0 build) |
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
  `WS_ERR_UNSUPPORTED_MESSAGE_LENGTH`); 3 within 10 min on one socket fail the subscriptions on it with `WS_PROTOCOL_ERROR`.
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
  stream.subscribe({ kind: "allMarkets", canonicals: ["BTC"] }).on((e) => {
    if (e.type === "market") document.title = `BTC ${e.mark ?? "—"}`;
  });
</script>
```

Serve the page and `node_modules` from the same static server (any origin works: the venues do not check
Origin and their REST CORS is `*`). Do the same with a CDN that serves npm files (e.g.
`https://cdn.jsdelivr.net/npm/@hypurrquant/perp-ws@<version>/dist/index.js`). The `/node` entry is
Node-only (it loads `ws`); never map it in a browser.

## 2. Minimal examples

All-market state for one venue (Node):

```ts
import { createVenueStream, hyperliquid, toApr } from "@hypurrquant/perp-ws/node";

const stream = createVenueStream(hyperliquid, { hip3Dexes: ["xyz"] }); // HIP-3 dexes are opt-in
stream.onState((s) => console.log("state", s.status));
const sub = stream.subscribe({ kind: "allMarkets", canonicals: ["BTC", "ETH", "xyz:TSLA"] });
sub.on((e) => {
  if (e.type === "market") {
    console.log(e.symbol, e.mark, e.funding.rate, e.funding.rateKind, toApr(e.funding.rate, e.funding.rateIntervalHours));
  } else if (e.type === "error") {
    console.error(e.fatal ? "FATAL" : "warn", e.code, e.message, e.remediation); // fatal = this subscription ended
  }
});
await sub.ready; // rejects with a WsError (code + remediation) — let it throw, or catch and show it
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

The same markets on several venues (browser) — **`canonicals`, and every rejection made visible**:

```ts
import { arcus, aster, createVenueStream, hyperliquid, lighter, pacifica, type VenueStream } from "@hypurrquant/perp-ws";

declare function show(venue: string, text: string): void; // your UI: one status cell per venue

const streams: VenueStream[] = [hyperliquid, pacifica, lighter, aster, arcus].map((c) => createVenueStream(c));
for (const stream of streams) {
  // canonicals: "BTC" → hyperliquid/pacifica/lighter BTC, aster BTCUSDT, arcus BTC-USD (Aster's
  // BTCUSD1 / BTCU listings are canonical null — only the USDT listing is matchable, as in the CLI).
  // (symbols would need each venue's directory symbols; ["BTC"] rejects on aster and arcus.)
  // A canonical this venue does not list (e.g. SOL somewhere) is skipped with a non-fatal warning;
  // ready rejects only when the venue lists none of them.
  const sub = stream.subscribe({ kind: "allMarkets", canonicals: ["BTC", "ETH", "SOL"] });
  sub.ready.then(
    () => show(stream.venue, "live"),
    (err: unknown) => show(stream.venue, `FAILED: ${err instanceof Error ? err.message : String(err)}`),
  );
  sub.on((e) => {
    if (e.type === "market") show(stream.venue, `${e.symbol} ${e.mark ?? "—"}`);
    else if (e.type === "error" && e.code === "SYMBOL_NOT_FOUND") {
      show(stream.venue, `not listed here: ${e.details?.missing?.join(", ")}`); // non-fatal: the rest stream
    } else if (e.type === "error" && e.fatal) show(stream.venue, `FAILED: ${e.code} ${e.message}`);
  });
  stream.onState((st) => { if (st.status === "closed") show(stream.venue, `closed: ${st.reason.message}`); });
}
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
  - `{ kind: "allMarkets", canonicals? | symbols? }` → `MarketUpdate` for every market, or a subset:
    **`canonicals`** (recommended across venues) selects every directory market whose `canonical` matches
    — `["BTC"]` is `BTC` on hyperliquid / pacifica / lighter / lighter-rh (USDG), `BTCUSDT` on
    aster and `BTC-USD` on arcus; HIP-3 markets are `"<dex>:<BASE>"` (`"xyz:TSLA"`, with `hip3Dexes`) and
    `"BTC"` never pulls them in. Canonicals come from `opts.canonicalize` (default: USD-like quotes
    collapse; an ambiguous ticker — SPX6900 on Hyperliquid / Aster / Lighter / Pacifica, Pacifica BP /
    CHIP, Lighter BB / BOT / WEN / QNT, an unclassified Lighter RH market — and a non-USDT Aster listing
    are null, never grouped: the CLI's rule) — see `MarketDirectoryEntry.canonical` in `stream.markets()`. Canonicals the venue does
    not list are **skipped and reported once** as a non-fatal control
    `{ type: "error", code: "SYMBOL_NOT_FOUND", fatal: false, details: { missing: string[], suggestions:
    Record<string, string[]> } }` (suggestions e.g. `"xyz:TSLA"` for `"TSLA"`; the others are subscribed and
    `ready` resolves). Only when the venue lists **none** of them does `ready` reject `INVALID_PARAMS`.
    **`symbols`** are this venue's exact directory symbols. Pass **one or the other** — both together
    reject `INVALID_PARAMS`. Same wire subscription and budget either way (filtering is client-side);
  - `{ kind: "market", symbol, channels: ["market" | "bbo"] }`. `"book"` and `"trades"` are already in
    the types but **reject with `CAPABILITY_UNSUPPORTED`** (planned, not yet available) — don't ship UI that needs them.
    Any other channel name (e.g. `"ticker"`) or an empty `channels` rejects with `INVALID_PARAMS`;
  - `{ kind: "user", channels: ["account" | "positions" | "orders" | "fills"] }` (needs `credentials`).
- **`symbols` / `symbol` mean the venue's directory symbols, case-sensitive** — not canonical names. `BTC` is `"BTC"` on
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
- Several sockets (Pacifica, > 20 channels of one kind): each socket reconnects and resubscribes only
  its own channels (gaps only for channels on it). `reconnect.maxAttempts` counts per socket, but **one
  socket exhausting it closes the whole stream** (every subscription ends with that reason). The state is
  the aggregate, worst first: `closed` > `reconnecting` > `stale` > `connecting` (of a socket that was
  open before) > `live`. A socket opening for the first time (just added, waiting on the
  new-connection budget, or retrying a failed first handshake) does not turn a live stream into
  `connecting` / `reconnecting`: it stays `live` with
  `sockets` = open sockets and `pending` = sockets still opening — the channels on those are not ready
  yet (their `ready` resolves when they open). `pending` is present only on multi-socket streams.
- `closed` is terminal: a later `subscribe` rejects with the close reason (e.g. the code that exhausted
  the reconnects). After your own `close()` the reason is `CLIENT_CLOSE`, which is not an error code: the
  rejection is `INVALID_PARAMS` "stream is closed" with `details.closeReason: "CLIENT_CLOSE"`. A handshake failure before
  open = `EXCHANGE_UNREACHABLE` ("network, venue outage, or Origin/CORS block").
- Ack timeout: no acknowledgement and no data within the channel's stale threshold → a **pending**
  subscription fails with `WS_PROTOCOL_ERROR`.
- Iterator buffer: market/bbo/account/positions/orders events are **state** and coalesce by key (never
  fatal). Fills and control events are not coalesced; a full buffer → fatal `STREAM_OVERFLOW` and the
  subscription closes. Before the iterator exists, state/error controls are kept in a ring of the last
  `size` (the iterator first gets a non-fatal `STREAM_OVERFLOW` with the discarded count); fills,
  gaps and the one-time `SYMBOL_NOT_FOUND` warning are never evicted.

## 4. Event fields and nullability

Rules: **unknown = `null`, never `0`**. A field the venue never sent is `null`; a field the latest frame
did not carry keeps its last value, with `asOf[field]` = receive time. `Dec` = the venue's decimal string
(exact; parse it yourself). Check `null` before arithmetic — `null` is not zero.

`MarketUpdate`: `venue, dex, symbol, venueSymbol, quote, canonical, mark, index, bestBid, bestAsk, last,
funding{ rate, rateKind, rateSource, rateIntervalHours, settlementIntervalHours, intervalSource,
nextFundingTime, predictedRate, marketClosed }, openInterest{ value, unit: "base"|"usd"|null, sides },
volume24hNotional, venueTs, recvTs, source, changed[], asOf{}`.

- **Aster `volume24hNotional` can stay `null` for minutes after subscribing:** the venue's `!ticker@arr`
  pushes only the tickers that changed, so a quiet market's first ticker (and its 24 h notional) arrives
  late. `null` there means "not received yet", not "no volume" — a volume filter must not treat it as 0
  (see the example in §5, which keeps such legs out explicitly and says so).

Funding:
- `rate` is **raw per `rateIntervalHours`** — never pre-annualized. Use `toHourly(rate, h)` to compare and
  `toApr(rate, h)` only for display (both return `null` for `null` input).
- **Units:** `toHourly` and `toApr` return **fractions** (`toApr` 0.1095 = 10.95 % a year, simple ×24×365).
  The CLI's `annualizedPct` (`perp --json arb scan --rates`, MCP `get_funding_rates`) is the same figure in
  **percent** (10.95). Multiply `toApr` by 100 before comparing it with `annualizedPct` or printing a "%".
- `rateKind`: `"lastSettled"` (the last payment), `"accruing"` (the current period so far, the "if it
  settled now" rate), `"predicted"` (the venue's estimate of the next payment). `predictedRate` is always
  kind `"predicted"`.

| Venue | `rate` kind | `predictedRate` | interval | OI | notes |
|---|---|---|---|---|---|
| hyperliquid | accruing | null | 1 h | base, one side | bid/ask/last null → `bbo` channel |
| pacifica | lastSettled | next_funding | 1 h | base, `sides` null | bid/ask/last/nextFundingTime null |
| lighter / lighter-rh | lastSettled | current_funding_rate | 1 h | **usd**, one side (inferred, not documented by the venue) | wire values are percent/h, emitted as fractions/h; REST `market info` OI is the same side in base units — convert before comparing; inactive / frozen markets are not streamed (same set as `market list`) |
| aster | accruing | null | per market (`rest:/fapi/v3/fundingInfo`, null if missing) | null | all quotes (USDT, USD1, …) with `quote` set |
| arcus | lastSettled | nextFundingRate | 1 h | base, one side | bid/ask null → `bbo` channel |

`stream.capabilities` carries the full matrix: `browser`, `networks`, `channels`, `fields` (false = always
null) and `notes` (why). lighter-rh has no testnet (`CAPABILITY_UNSUPPORTED`).

`BboUpdate`: `bid, bidSize, ask, askSize` (null = that side of the book is empty), `venueTs, recvTs`.
Venue sequence numbers only drop out-of-order frames (they are not contiguous; bbo never emits gaps).
Pacifica allows ≤ 20 subscriptions per channel per connection: the stream spreads further `bbo` channels
over more sockets (≤ 50 per stream; `budget.maxSockets` lowers it; `SUBSCRIPTION_LIMIT` beyond).
`live.sockets` counts the open ones.

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
- **One leg per venue by default:** Aster lists BTC as `BTCUSDT` (quote USDT) and `BTCUSD1` (quote
  USD1); the default canonicalization keeps only the USDT listing matchable and gives every other
  quote `canonical: null`, as the CLI does. A custom `canonicalize` that
  returns a key for both brings back several legs per venue — pick one before ranking.
- **`fundingVerified`** (per leg): the CLI's verdict that the venue's funding unit and which published
  rate actually settles were confirmed against its funding payments. All six WS venues are
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
/**
 * One leg per venue: the most liquid market that passes the filter. A leg whose 24 h notional is not
 * known yet (Aster sends a ticker only when it changes — minutes on quiet markets) is skipped, never
 * read as 0; `unknownVolume` counts them so a dashboard can show "N legs waiting for volume".
 */
let unknownVolume = 0;
function pickLegs(row: FundingRow): FundingLeg[] {
  const best = new Map<string, { leg: FundingLeg; vol: number }>();
  for (const leg of row.legs) {
    if (leg.rate === null || leg.stale || !leg.fundingVerified) continue;
    const vol = notional.get(`${leg.venue}|${leg.symbol}`);
    if (vol === undefined) { unknownVolume++; continue; } // not received yet — unknown, not 0
    if (vol < MIN_NOTIONAL) continue;
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
  `signTypedData` (reserved for planned venues). Tokens handed in are redacted from every error, log and
  raw excerpt.
- `allowInPageSecrets: true` is required for venues whose auth needs a signing secret in the page
  (Aster / Ondo / QFEX — planned, not yet available). Without it they reject `CAPABILITY_UNSUPPORTED` in a browser.
- `UserRef` per venue: hyperliquid `{ address }` (no auth), pacifica `{ account }` (Solana address, no
  auth), lighter / lighter-rh `{ accountIndex }`, arcus `{ address, subaccount }` (`null` = account 0, no auth).
- **Any account, keyless:** the Hyperliquid (`{ address }`) and Pacifica (`{ account }`) user channels
  need no auth, so `user()` may return ANY public address — a live positions / fills feed of someone
  else's account. The REST counterpart (one snapshot, also Lighter / Lighter RH / RISEx) is
  `perp --json -e <venue> account positions --address <addr>` / MCP `get_positions_by_address`.
- **KNOWN GAP: Aster user channels are not implemented** — `kind: "user"` on aster rejects
  `CAPABILITY_UNSUPPORTED` (no parity; planned, not yet available).

Events:
- `account` — `equity, available, marginUsed, unrealizedPnl` (+ `dex` on hyperliquid, one per perp dex);
  `source: "snapshot"` when the frame was a full snapshot. `unrealizedPnl` per venue:
  hyperliquid = the exact sum of that dex's position `unrealizedPnl` in the same `clearinghouseState`
  frame (`"0"` with no position; `null` if a position lacks it — the frame has no account-level field);
  pacifica = `null` (`account_info` publishes none, and the position stream carries no unrealized PnL
  either); lighter / lighter-rh = `null` on `account` (`user_stats` publishes none) — per position it is
  `PositionRow.unrealizedPnl` (`unrealized_pnl` on the positions channel); arcus = `null` on `account`,
  per position on `PositionRow`.
- `positions` / `orders` — always the **full current set** (snapshot + merged deltas). Pacifica
  `account_positions` snapshots older than the last applied one (envelope `li`) are dropped.
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
`ready` rejects with a `WsError` whose `structured = { code, message, status, retryable, remediation? }`;
`err.code` and `err.remediation` (null when none) mirror `structured`, so one handler reads `code` the same
way on error events (`e.code`) and on rejections (`err.code`).

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
| `SYMBOL_NOT_FOUND` | non-fatal: requested `canonicals` this venue does not list (`details.missing`, `details.suggestions`); the rest stream |
| `RATE_LIMITED`, `EXCHANGE_ERROR` | REST bootstrap failures |

## 8. Budgets and limits

- `budget: { maxSubscriptions, maxSockets, newConnectionsPerMin }` caps below the venue limits (checked
  before sending). One socket per stream, except venues whose caps are per connection (Pacifica: 20 per
  channel per connection, 100 connections per IP → up to 50 sockets per stream). The new-connection
  budget is per stream (a socket waiting on it is `pending`; it never opens once its channels are
  released); one socket exhausting its reconnects closes the stream.
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
- **Do** use `canonicals` for the same markets on several venues; `symbols` are per-venue directory symbols
  (`["BTC"]` rejects on aster and arcus). Show the `SYMBOL_NOT_FOUND` warning (which canonicals a venue
  lacks) instead of an empty cell.
- **Do** surface every `ready` rejection and every `fatal` error event per venue (see the price-wall
  pattern in §2). **Never treat `idle` (or a venue with no data) as fine**: `idle` means the stream has no
  active subscription — usually because a subscribe was rejected — not "connected and quiet".

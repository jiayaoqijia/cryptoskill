# @realized-lp/core

**Advertised LP APR is fee income, annualized. It has no price term — so it is positive by
construction and cannot tell you that you lost money.**

This package computes the other number: **realized return = fees + impermanent loss**, from
The Graph's historical `poolDayData`.

```bash
npm i @realized-lp/core
```

## Three lines

```js
import { gatewayUrl, fetchPoolFrom, positionRealized } from '@realized-lp/core';

const pool = await fetchPoolFrom(gatewayUrl(process.env.GRAPH_API_KEY), poolId, entryTs);
const r = positionRealized(pool, 2); // range width: +/-2x

r.realizedReturnPct;    // -14.2  <- what you actually made
r.advertisedAprPct;     // +1.7   <- what the DEX UI showed you
r.impermanentLossPct;   // -16.3
r.outOfRange;           // true -> price left your band, this loss is locked in
```

## No API key? The math is still yours

`impermanentLossPct` and `concentratedIlPct` are pure functions — no network, no key, no
dependencies. Use them anywhere.

```js
import { impermanentLossPct, concentratedIlPct } from '@realized-lp/core';

impermanentLossPct(2);      // -5.7191  full-range, price doubled
concentratedIlPct(2, 2);    // -19.5262 same move, but ranged +/-2x
```

Concentration multiplies both the fees **and** the loss. That second number is why "just go
tighter for more APR" quietly costs people money.

## Audit a whole corpus

```js
import { fetchTopPools, scorePool, summarize, isLive } from '@realized-lp/core';

const pools  = await fetchTopPools(url, { first: 250, minTvlUsd: 250_000 });
const scored = pools.map(scorePool).filter((s) => isLive(s));
summarize(scored); // median advertised vs median realized, % of pools advertising a lie
```

## Multi-venue

```js
import { subgraphId, venueList } from '@realized-lp/core';

venueList();                              // uniswap-v3, aerodrome, ... x chains
subgraphId('aerodrome', 'base');          // -> deployment id
gatewayUrl(key, subgraphId('aerodrome', 'base'));
```

The IL math is venue-agnostic: it takes a price ratio and a range width, not a pool ABI.

## API

| export | what it does | network? |
|---|---|---|
| `impermanentLossPct(r)` | full-range IL for price ratio `r` | no |
| `concentratedIlPct(r, w)` | IL for a position ranged `+/-w` | no |
| `outOfRange(r, w)` | did price leave the band | no |
| `positionRealized(pool, w)` | fees + IL + verdict for one position | no (takes fetched pool) |
| `scorePool(pool)` | advertised vs realized for one pool | no |
| `byRange(...)` | same pool across range widths | no |
| `gatewayUrl(key, subgraphId?)` | build a Graph gateway URL | no |
| `fetchPool(url, id, days)` | last N days of `poolDayData` | yes |
| `fetchPoolFrom(url, id, ts)` | days since an entry timestamp | yes |
| `fetchTopPools(url, opts)` | corpus by TVL | yes |
| `summarize` / `sensitivity` | corpus aggregates, multi-gate | no |
| `isLive` / `priceCollapsed` | liveness + dead-pool filters | no |
| `scoreWindow` / `summarizeWindow` | walk-forward windows | no |

## Why The Graph, specifically

Per-day fee totals in USD are **derived aggregates produced by the indexer**. They do not
exist on-chain. There is no RPC path to this dataset — you would have to replay every swap in
the pool and price each one yourself. The Graph isn't decoration here; remove it and there is
no product.

## Honesty

`positionRealized` refuses a 1-day window rather than dividing by nothing, and returns
`measurable: false` with a reason instead of a confident wrong number. The corpus summary
carries a **canary**: if the worst stable-pair |IL| exceeds 1%, the math is considered broken
and the aggregate refuses to render.

The negative control is a real position our own stack once scored `+1.7% WIN` when the true
outcome was about **−14%** — because resolution was fee-only and arithmetically could not
lose. It is pinned in `test/canary.test.js`.

MIT.

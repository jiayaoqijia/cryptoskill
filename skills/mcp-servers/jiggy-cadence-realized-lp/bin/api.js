#!/usr/bin/env node
/**
 * api.js — the actual HTTP service behind realized.drainfun.xyz.
 *
 * This exists because a static JSON file and an .html page on a subpath do not read as "a
 * tool for agents" — a real API answers live queries, not just the 202 pools we pre-fetched.
 * Every route below either serves the cached corpus (instant) or calls The Graph live
 * (find/query/audit), same code paths as the MCP server in bin/mcp-server.js -- one
 * implementation of the math, two transports.
 *
 * Routes:
 *   GET  /health
 *   GET  /api/pools                      cached corpus, same shape as data/pools.json
 *   GET  /api/find?q=WETH/USDC           live lookup by symbol, ranked by TVL
 *   GET  /api/pool/:id?range=2&days=30   live realized_return for one pool
 *   GET  /api/position/:id?entry=...     live position_realized: YOUR entry date + YOUR range
 *   GET  /api/audit?limit=250            live corpus-wide sweep + canary
 *   GET  /                               the search UI (index.html)
 *   GET  /report.html, /llms.txt         static passthrough
 *
 * No auth (read-only, GET-only, backed by our own paid Graph key -- same trust model as
 * tape's public API). Rate-limited at the nginx layer, not here.
 */
import { createServer } from 'http';
import { readFileSync, existsSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
import {
  gatewayUrl, query, fetchPool, fetchPoolFrom, fetchTopPools, scorePool, positionRealized, simulateExit, summarize, sensitivity, DEFAULT_LIVENESS,
} from '../lib/realized.js';
import { concentratedIlPct, outOfRange } from '../lib/concentrated.js';
import { VENUES, subgraphId, venueList } from '../lib/venues.js';
import { fetchWalletPositions, describePosition, WALLET_LIMITS } from '../packages/core/src/wallet.js';
import { walletV4 } from '../packages/core/src/v4.js';
import { crossCheckPrice, exitGasCost } from '../packages/core/src/oneinch.js';

// 1inch key is optional. Present -> position responses carry an independent price cross-check.
// Absent -> the field says so honestly. Same on-disk pattern as the Graph key.
let ONEINCH_KEY = process.env.ONEINCH_API_KEY || null;
if (!ONEINCH_KEY) {
  try { ONEINCH_KEY = JSON.parse(readFileSync('/home/ubuntu/.config/cadence-secure/1inch.json', 'utf8')).api_key; } catch { /* no key yet */ }
}

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const PORT = process.env.PORT || 3221;
const API_KEY = process.env.GRAPH_API_KEY;

const POOLS = JSON.parse(readFileSync(join(ROOT, 'data/pools.json'), 'utf8'));

const GATES = [
  { label: 'loose', gate: { minActiveDays: 20, minRecent7dVolumeUsd: 10_000, minTvlUsd: 100_000 } },
  { label: 'mid', gate: DEFAULT_LIVENESS },
  { label: 'strict', gate: { minActiveDays: 28, minRecent7dVolumeUsd: 250_000, minTvlUsd: 1_000_000 } },
];

// ---- TTL cache for LIVE Graph lookups -------------------------------------------------
// /api/pools is served from the pre-built corpus and costs nothing. /api/pool/{id},
// /api/find (live fallback) and /api/audit hit The Graph gateway on EVERY request against
// a free-tier key. A judging panel or a demo link making repeat calls can exhaust that key
// mid-evaluation, and the failure is the bad kind: the endpoint starts erroring while the
// cached pages keep working, so the site looks alive but the live features are dead.
//
// Pool-day data only changes once per day, so a short TTL costs correctness nothing and
// collapses N identical judge requests into one upstream call. Deliberately in-memory:
// no dependency, no disk state to go stale across a deploy, and a restart is a clean slate.
const TTL_MS = { pool: 10 * 60_000, find: 30 * 60_000, audit: 15 * 60_000 };
const CACHE_MAX = 500;
const cache = new Map(); // key -> { value, expires }
let cacheHits = 0, cacheMisses = 0;

async function cached(bucket, key, fn) {
  const k = `${bucket}:${key}`;
  const hit = cache.get(k);
  if (hit && hit.expires > Date.now()) { cacheHits++; return hit.value; }
  cacheMisses++;
  const value = await fn();
  // Never cache an error shape -- a transient gateway failure must not be pinned for
  // 10 minutes, or one blip during judging becomes a persistent outage.
  if (!value || value.error) return value;
  if (cache.size >= CACHE_MAX) cache.delete(cache.keys().next().value);
  cache.set(k, { value, expires: Date.now() + (TTL_MS[bucket] ?? 600_000) });
  return value;
}

const json = (res, code, obj) => {
  const body = JSON.stringify(obj, null, 2);
  res.writeHead(code, {
    'content-type': 'application/json; charset=utf-8',
    'access-control-allow-origin': '*',
    'cache-control': code === 200 ? 'public, max-age=60' : 'no-store',
  });
  res.end(body);
};

const CONTENT_TYPES = { '.html': 'text/html', '.json': 'application/json', '.txt': 'text/plain', '.js': 'application/javascript' };
function serveFile(res, path, code = 200) {
  const ext = path.slice(path.lastIndexOf('.'));
  res.writeHead(code, { 'content-type': (CONTENT_TYPES[ext] || 'application/octet-stream') + '; charset=utf-8', 'cache-control': 'public, max-age=300' });
  res.end(readFileSync(path));
}

// Two-tier find: instant match against the cached 202-pool corpus first (covers the vast
// majority of real queries -- these are the top pools by volume on every venue we index).
// Falls back to a bounded LIVE fetch of ONE venue at a time only when nothing cached matches,
// so a query for an obscure pair still works without making every request pay a 5-venue,
// 2500-pool sequential fetch that was timing out at 20s+ before this fix.
function cachedFind(q, limit) {
  const terms = q.toUpperCase().split(/[/\s-]+/).filter(Boolean);
  const results = POOLS.pools
    .filter((p) => { const up = p.pair.toUpperCase(); return terms.every((t) => up.includes(t)); })
    .sort((a, b) => b.tvl - a.tvl)
    .slice(0, limit)
    .map((p) => ({ poolId: p.id, pair: p.pair, dex: p.dex, chain: p.chain, feeTierPct: p.fee, tvlUsd: p.tvl }));
  return results;
}

async function liveFind(q, limit = 5, { venues = [{ dex: 'uniswap-v3', chain: 'mainnet' }] } = {}) {
  const terms = q.toUpperCase().split(/[/\s-]+/).filter(Boolean);
  const results = [];
  for (const { dex, chain } of venues) {
    const id = subgraphId(dex, chain);
    if (!id) continue;
    let pools;
    try { pools = await fetchTopPools(gatewayUrl(API_KEY, id), { first: 300, minTvlUsd: 10_000 }); }
    catch { continue; }
    for (const p of pools) {
      const sym0 = (p.token0?.symbol || '').toUpperCase(), sym1 = (p.token1?.symbol || '').toUpperCase();
      if (terms.every((t) => sym0.includes(t) || sym1.includes(t))) {
        results.push({ poolId: p.id, pair: `${sym0}/${sym1}`, dex, chain, feeTierPct: Number(p.feeTier) / 10_000, tvlUsd: Math.round(Number(p.totalValueLockedUSD)) });
      }
    }
  }
  results.sort((a, b) => b.tvlUsd - a.tvlUsd);
  return results.slice(0, limit);
}

async function livePool(poolId, { days = 30, range } = {}, dex = 'uniswap-v3', chain = 'mainnet') {
  const id = subgraphId(dex, chain);
  if (!id) return { error: `unknown venue ${dex}/${chain}` };
  const pool = await fetchPool(gatewayUrl(API_KEY, id), poolId, days);
  if (!pool) return { error: `pool ${poolId} not found on ${dex}/${chain}` };
  const scored = scorePool(pool);
  if (!scored.measurable || !(range > 1)) return scored;
  const il = concentratedIlPct(scored.priceRatio, range);
  const realizedPct = scored.feeReturnPct + il;
  return {
    ...scored,
    yourRange: {
      rangeWidthX: range,
      impermanentLossPct: il,
      realizedReturnPct: realizedPct,
      realizedAprPct: (realizedPct / scored.windowDays) * 365,
      outOfRange: outOfRange(scored.priceRatio, range),
    },
  };
}

/**
 * livePosition — the HTTP twin of the MCP `position_realized` tool.
 *
 * Deliberately calls the SAME fetchPoolFrom + positionRealized pair the MCP server calls,
 * rather than re-deriving anything here: one implementation of the math, three transports
 * (MCP, HTTP, UI). If this ever disagrees with the MCP tool, that is a bug, not a variant.
 */
async function livePosition(poolId, { entry, range = 2 } = {}, dex = 'uniswap-v3', chain = 'mainnet') {
  const id = subgraphId(dex, chain);
  if (!id) return { error: `unknown venue ${dex}/${chain}` };
  if (!entry) return { error: 'entry is required, e.g. ?entry=2026-08-01 (ISO date or unix timestamp)' };

  let ts;
  if (/^\d+$/.test(String(entry))) {
    ts = Number(entry);
  } else {
    const d = new Date(entry);
    if (Number.isNaN(d.getTime())) return { error: `could not parse entry "${entry}" as an ISO date or unix timestamp` };
    ts = Math.floor(d.getTime() / 1000);
  }
  // A future entry date yields an empty series, which positionRealized would report as
  // "need at least 2 days" -- true but confusing. Name the real cause instead.
  if (ts > Math.floor(Date.now() / 1000)) return { error: 'entry date is in the future' };

  const pool = await fetchPoolFrom(gatewayUrl(API_KEY, id), poolId, ts);
  if (!pool) return { error: `pool ${poolId} not found on ${dex}/${chain}` };
  const pos = positionRealized(pool, range);
  if (!pos.measurable) return pos;
  // Independent price second-opinion from 1inch. Non-load-bearing and non-blocking: if the
  // key is absent or 1inch is down, priceCheck.available is false and the realized number is
  // unchanged. The subgraph remains the source of truth; this only says whether an unrelated
  // aggregator vouches for the current price our IL leg depends on.
  const priceCheck = await crossCheckPrice({
    token0: pool.token0?.id,
    token1: pool.token1?.id,
    subgraphPrice: pos.currentPrice,
    chain,
    apiKey: ONEINCH_KEY,
  });
  return {
    ...pos,
    priceCheck,
    verdict: pos.outOfRange
      ? `Price left your +/-${range}x range: realized ${pos.realizedAprPct.toFixed(1)}% annualized, and this loss is LOCKED IN, not impermanent.`
      : `In-range the whole time: realized ${pos.realizedAprPct.toFixed(1)}% annualized (fees ${pos.feeReturnPct.toFixed(2)}% + IL ${pos.impermanentLossPct.toFixed(2)}%).`,
  };
}

/**
 * liveWallet — an address's open positions, with each one's REAL tick range resolved.
 *
 * The upgrade this unlocks: every realized number on the site so far assumed a +/-2x band,
 * because a pool-level dataset cannot know your position. A connected wallet does know, so
 * we read the actual ticks and report the range width the IL math should use. We do NOT
 * silently compute a portfolio P&L from fields that don't support one -- see the route
 * comment and WALLET-CONNECT-NOTES.md.
 */
async function liveWallet(owner, { dex = 'uniswap-v3', chain = 'mainnet', includeClosed = false } = {}) {
  const id = subgraphId(dex, chain);
  if (!id) return { error: `unknown venue ${dex}/${chain}` };

  // Address shape is validated HERE, before any venue branch, because each branch used to own
  // its own guard and only one of them had it. fetchWalletPositions (v3) rejected malformed
  // input with a 400; walletV4 had no check, so the same garbage address was interpolated
  // straight into a GraphQL `where` and came back as a subgraph 500:
  // "Failed to decode `Bytes` value: `Odd number of digits`". Measured 2026-09-11 against the
  // live API with "0x996d...": v3 => 400 with a readable message, v4 => 500 leaking subgraph
  // internals. Same malformed input, two different contracts, and the one an agent is most
  // likely to hit was the one that failed worst. A validator that lives on one path is not a
  // validator, it is a coincidence -- so it moves up to the dispatch point both paths cross.
  const addr = String(owner || '').toLowerCase();
  if (!/^0x[0-9a-f]{40}$/.test(addr)) {
    return { error: `"${owner}" is not a 0x-prefixed 40-hex-character address` };
  }

  // v4 answers through event reconstruction, not a Position-state read. Different evidence
  // class, different code path, and it reports ranges WITHOUT realized return on purpose.
  if (dex === 'uniswap-v4') {
    return await walletV4(query, gatewayUrl(API_KEY, id), addr);
  }

  // Aerodrome's subgraph does not expose the same Position entity, so say so rather than
  // returning a confusing empty list that reads as "you have no positions".
  if (dex !== 'uniswap-v3') {
    return { error: `wallet positions are only available for uniswap-v3 and uniswap-v4; ${dex} does not expose a comparable Position entity` };
  }
  const r = await fetchWalletPositions(gatewayUrl(API_KEY, id), owner, { includeClosed });
  if (!r.ok) return { error: r.error };

  const positions = r.positions.map(describePosition);
  const feesMeasurable = positions.filter((x) => x.fees.measurable).length;
  const uncollected = positions.filter((x) => x.fees.basis === 'earned-but-uncollected').length;

  return {
    owner: String(owner).toLowerCase(),
    dex,
    chain,
    openPositions: positions.length,
    pools: [...new Set(positions.map((x) => x.pair))],
    positions,
    feeReporting: {
      measurable: feesMeasurable,
      earnedButUncollected: uncollected,
      note: uncollected
        ? `${uncollected} of ${positions.length} position(s) have accrued fees that were never collected. We report those as unmeasurable rather than $0 -- the subgraph exposes no accrued-fee balance.`
        : 'No positions with uncollected accrued fees in this set.',
    },
    limits: WALLET_LIMITS,
    next: 'Feed a position\'s range.widthX into /api/position/{poolId}?entry=YYYY-MM-DD&range={widthX} for realized return at YOUR actual range instead of an assumed +/-2x.',
  };
}

/**
 * liveSimulateExit — same fetch + venue handling as livePosition, different question:
 * "if I closed this position today, what would I walk away with?" Not a new data path --
 * calls the SAME fetchPoolFrom this file already uses, then simulateExit instead of
 * positionRealized. One fetch, two framings of the same verified numbers.
 */
async function liveSimulateExit(poolId, { entry, range = 2, stake = 10_000, consolidate = false } = {}, dex = 'uniswap-v3', chain = 'mainnet') {
  const id = subgraphId(dex, chain);
  if (!id) return { error: `unknown venue ${dex}/${chain}` };
  if (!entry) return { error: 'entry is required, e.g. ?entry=2026-08-01 (ISO date or unix timestamp)' };
  let ts;
  if (/^\d+$/.test(String(entry))) {
    ts = Number(entry);
  } else {
    const d = new Date(entry);
    if (Number.isNaN(d.getTime())) return { error: `could not parse entry "${entry}" as an ISO date or unix timestamp` };
    ts = Math.floor(d.getTime() / 1000);
  }
  if (ts > Math.floor(Date.now() / 1000)) return { error: 'entry date is in the future' };
  const stakeUsd = Number(stake);
  if (!(stakeUsd > 0)) return { error: 'stake must be a positive number of USD' };

  const pool = await fetchPoolFrom(gatewayUrl(API_KEY, id), poolId, ts);
  if (!pool) return { error: `pool ${poolId} not found on ${dex}/${chain}` };
  // Live gas, fetched server-side. 1inch blocks direct curl/python clients at the Cloudflare
  // layer (error 1010), so this is the only path that actually reaches the endpoint -- and it
  // degrades honestly to { available:false, reason } rather than guessing a cost.
  const gas = await exitGasCost({ chain, apiKey: ONEINCH_KEY });
  return simulateExit(pool, range, stakeUsd, { gas, consolidate });
}

async function liveAudit({ limit = 250, days = 30, dex = 'uniswap-v3', chain = 'mainnet' } = {}) {
  const id = subgraphId(dex, chain);
  if (!id) return { error: `unknown venue ${dex}/${chain}` };
  const pools = await fetchTopPools(gatewayUrl(API_KEY, id), { first: limit, days });
  const scored = pools.map(scorePool);
  const s = summarize(scored);
  return { ...s, sensitivity: sensitivity(scored, GATES) };
}

const server = createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const p = url.pathname;

  try {
    if (req.method === 'OPTIONS') { res.writeHead(204, { 'access-control-allow-origin': '*', 'access-control-allow-methods': 'GET, OPTIONS' }); return res.end(); }
    if (req.method !== 'GET') return json(res, 405, { error: 'GET only' });

    if (p === '/health') {
      return json(res, 200, {
        ok: true,
        pools: POOLS.pools.length,
        generatedAt: POOLS.generatedAt,
        // Surfaced so the cache is observable rather than a silent optimisation --
        // if a demo starts failing, the first question is whether upstream is being hit.
        cache: {
          entries: cache.size,
          hits: cacheHits,
          misses: cacheMisses,
          hitRatePct: cacheHits + cacheMisses ? Number(((cacheHits / (cacheHits + cacheMisses)) * 100).toFixed(1)) : null,
          ttlSeconds: Object.fromEntries(Object.entries(TTL_MS).map(([k, v]) => [k, v / 1000])),
        },
      });
    }

    if (p === '/api/pools') {
      // 2026-09-10: this schema/formula was a THIRD independent copy of the same contract
      // (build-app.js's static api/pools.json had a second, richer one nothing actually
      // served -- bin/api.js intercepts /api/pools before nginx ever reaches the static
      // file). Caught by an agent review that correctly flagged the formula-as-prose
      // problem; fixed here where it's actually live, with a real test vector instead of
      // words, and the fields realizedAprPct/gapPts/misleading already precomputed on
      // each pool object by build-pools.js -- so an agent should rarely need the formula
      // at all except to double-check a different range width.
      const worked = POOLS.pools.find((x) => x.realizedAprPct !== null) || POOLS.pools[0];
      return json(res, 200, {
        ...POOLS,
        schema: {
          pair: 'token0/token1 symbols', dex: 'uniswap-v3 | aerodrome', chain: 'mainnet | arbitrum | polygon | base',
          fee: 'pool fee tier, percent', tvl: 'current TVL, USD', r: 'price ratio over window (exit/entry)',
          fees: 'fee income over window, % of entry TVL', adv: 'advertised APR % (fees-only, cannot be negative)', days: 'window length',
          realizedAprPct: 'precomputed realized return (fees + IL), annualized, at MODERATE (+/-2x) range. null if unmeasurable.',
          gapPts: 'adv - realizedAprPct at moderate range. Positive = advertised overstated reality.',
          misleading: 'true if adv > 0 and realizedAprPct < 0 at moderate range. null if unmeasurable.',
        },
        testVector: {
          note: 'Real pool, real inputs, real output from THIS server right now. Implement the '
            + 'formula, run it on these inputs, check you get realizedAprPct before trusting your '
            + 'own math on any other pool.',
          input: { pair: worked.pair, r: worked.r, feesPct: worked.fees, advertisedAprPct: worked.adv, windowDays: worked.days, rangeWidthX: 2 },
          expectedOutput: { realizedAprPct: worked.realizedAprPct, gapPts: worked.gapPts, misleading: worked.misleading },
          formula:
            'realizedReturnPct = fees + impermanentLossPct(r, rangeWidthX). IL closed form: let sa=sqrt(1/w), '
            + 'sb=sqrt(w); if r<=1/w: pos=(1/sa-1/sb)*r; elif r>=w: pos=sb-sa; else: pos=2*sqrt(r)-sa-r/sb; '
            + 'hodl=(1-sa)+(1-1/sb)*r; IL=(pos/hodl-1)*100. w=rangeWidthX (2 for moderate; 1e8 ~ full-range). '
            + 'realizedAprPct = realizedReturnPct/windowDays*365.',
        },
        liveEndpoints: { find: '/api/find?q=WETH/USDC', pool: '/api/pool/{poolId}?range=2', audit: '/api/audit?limit=250' },
      });
    }

    if (p === '/api/find') {
      const q = url.searchParams.get('q');
      if (!q) return json(res, 400, { error: 'q parameter required, e.g. /api/find?q=WETH/USDC' });
      const limit = Number(url.searchParams.get('limit') || 5);
      let matches = cachedFind(q, limit);
      let source = 'cache';
      if (!matches.length && url.searchParams.get('live') !== '0') {
        matches = await cached('find', `${q.toUpperCase()}|${limit}`, () => liveFind(q, limit));
        source = 'live:uniswap-v3/mainnet';
      }
      return json(res, 200, {
        query: q, source, matches,
        note: matches.length ? 'pass matches[].poolId to /api/pool/{poolId}' : 'no match in the 202-pool cache or a live mainnet lookup',
      });
    }

    if (p.startsWith('/api/pool/')) {
      const poolId = decodeURIComponent(p.slice('/api/pool/'.length));
      const range = url.searchParams.get('range') ? Number(url.searchParams.get('range')) : undefined;
      const days = Number(url.searchParams.get('days') || 30);
      const dex = url.searchParams.get('dex') || 'uniswap-v3';
      const chain = url.searchParams.get('chain') || 'mainnet';
      const out = await cached('pool', `${dex}|${chain}|${poolId.toLowerCase()}|${days}|${range ?? 'none'}`,
        () => livePool(poolId, { days, range }, dex, chain));
      return json(res, out.error ? 404 : 200, out);
    }

    if (p.startsWith('/api/position/')) {
      const poolId = decodeURIComponent(p.slice('/api/position/'.length));
      const entry = url.searchParams.get('entry') || '';
      const range = Number(url.searchParams.get('range') || 2);
      const dex = url.searchParams.get('dex') || 'uniswap-v3';
      const chain = url.searchParams.get('chain') || 'mainnet';
      const out = await cached('pool', `pos|${dex}|${chain}|${poolId.toLowerCase()}|${entry}|${range}`,
        () => livePosition(poolId, { entry, range }, dex, chain));
      return json(res, out.error ? 400 : 200, out);
    }

    // /api/simulate-exit/{poolId} -- decision support for closing a position TODAY. Same
    // fetch + math as /api/position/, reframed around dollars on a stake and an explicit
    // gas/slippage `unavailable` rather than a number from an endpoint we have not verified.
    if (p.startsWith('/api/simulate-exit/')) {
      const poolId = decodeURIComponent(p.slice('/api/simulate-exit/'.length));
      const entry = url.searchParams.get('entry') || '';
      const range = Number(url.searchParams.get('range') || 2);
      const stake = Number(url.searchParams.get('stake') || 10_000);
      const consolidate = url.searchParams.get('consolidate') === 'true';
      const dex = url.searchParams.get('dex') || 'uniswap-v3';
      const chain = url.searchParams.get('chain') || 'mainnet';
      const out = await cached('pool', `exit|${dex}|${chain}|${poolId.toLowerCase()}|${entry}|${range}|${stake}|${consolidate}`,
        () => liveSimulateExit(poolId, { entry, range, stake, consolidate }, dex, chain));
      return json(res, out.error ? 400 : 200, out);
    }

    // /api/wallet/{address} — which pools does this address actually hold, and at what range.
    //
    // This is position DISCOVERY, not per-position P&L, and that is a measured decision rather
    // than a missing feature. The Position entity's collectedFees fields are a withdrawal
    // record, not an earnings record (of 150 sampled positions with collectedFeesToken0 == 0,
    // 71 had non-zero feeGrowthInside0LastX128 -- earned, never collected), and the
    // deposited/withdrawn fields are lifetime cumulative rather than entry state. Deriving a
    // fee figure or an entry value from those would reproduce the advertised-APR defect this
    // project exists to expose. See WALLET-CONNECT-NOTES.md. The `limits` block ships in every
    // response so the caller cannot miss it.
    if (p.startsWith('/api/wallet/')) {
      const owner = decodeURIComponent(p.slice('/api/wallet/'.length)).trim();
      const dexParam = url.searchParams.get('dex');
      const chain = url.searchParams.get('chain') || 'mainnet';
      const includeClosed = url.searchParams.get('includeClosed') === 'true';

      // No explicit ?dex= -> look in BOTH v3 and v4 and return whatever the wallet actually
      // holds. Defaulting to v3 alone is what made a wallet with 8 live v4 ranges read as
      // "no positions" -- an absence of evidence rendered as evidence of absence. Each venue
      // is reported with its own source/limits so the two are never silently merged: they are
      // different evidence classes (state read vs event reconstruction), not one list.
      if (!dexParam && chain === 'mainnet') {
        const [v3, v4] = await Promise.all([
          cached('pool', `wallet|uniswap-v3|${chain}|${owner.toLowerCase()}|${includeClosed}`,
            () => liveWallet(owner, { dex: 'uniswap-v3', chain, includeClosed })).catch((e) => ({ error: String(e?.message || e) })),
          cached('pool', `wallet|uniswap-v4|${chain}|${owner.toLowerCase()}|${includeClosed}`,
            () => liveWallet(owner, { dex: 'uniswap-v4', chain, includeClosed })).catch((e) => ({ error: String(e?.message || e) })),
        ]);

        const found = [];
        if (!v3?.error && v3?.openPositions > 0) found.push('uniswap-v3');
        if (!v4?.error && v4?.openPositions > 0) found.push('uniswap-v4');

        return json(res, 200, {
          owner: String(owner).toLowerCase(),
          chain,
          searched: ['uniswap-v3', 'uniswap-v4'],
          foundIn: found,
          openPositions: (v3?.openPositions || 0) + (v4?.openPositions || 0),
          venues: { 'uniswap-v3': v3, 'uniswap-v4': v4 },
          note: found.length === 0
            ? 'No open positions in Uniswap v3 or v4 on mainnet. We searched both; this does not cover v2, other chains, or other DEXes.'
            : `Open positions found in: ${found.join(' and ')}. v3 supports realized return; v4 reports ranges only (reconstructed from events).`,
        });
      }

      const dex = dexParam || 'uniswap-v3';
      const out = await cached('pool', `wallet|${dex}|${chain}|${owner.toLowerCase()}|${includeClosed}`,
        () => liveWallet(owner, { dex, chain, includeClosed }));
      return json(res, out.error ? 400 : 200, out);
    }

    if (p === '/api/audit') {
      const limit = Number(url.searchParams.get('limit') || 250);
      const days = Number(url.searchParams.get('days') || 30);
      const dex = url.searchParams.get('dex') || 'uniswap-v3';
      const chain = url.searchParams.get('chain') || 'mainnet';
      const out = await cached('audit', `${dex}|${chain}|${limit}|${days}`,
        () => liveAudit({ limit, days, dex, chain }));
      return json(res, out.error ? 400 : 200, out);
    }

    // The actionable question, answered honestly. NOT a prediction of which pool will pay
    // best next month -- we tested that (spike-hunt3 found +1.64pp, then five walk-forward
    // re-runs came back -0.11/+0.04/+0.26pp against a pre-registered >=0.5pp bar and all
    // failed). This is TRACK RECORD: whose advertised number has actually matched reality.
    if (p === '/api/rank') {
      const top = Math.min(Number(url.searchParams.get('top') || 25), 200);
      const trust = url.searchParams.get('trust') || '';       // filter by label
      const sort = url.searchParams.get('sort') || 'realized'; // realized | gap | tvl
      let rows = POOLS.pools.filter((x) => x.realizedAprPct !== null);
      if (trust) rows = rows.filter((x) => x.trustLabel === trust);
      const sorters = {
        realized: (a, b) => b.realizedAprPct - a.realizedAprPct,
        gap: (a, b) => (b.gapPts ?? -1e9) - (a.gapPts ?? -1e9),
        tvl: (a, b) => b.tvl - a.tvl,
      };
      rows = [...rows].sort(sorters[sort] || sorters.realized).slice(0, top);
      const all = POOLS.pools.filter((x) => x.realizedAprPct !== null);
      const counts = all.reduce((acc, x) => { acc[x.trustLabel] = (acc[x.trustLabel] || 0) + 1; return acc; }, {});
      return json(res, 200, {
        generatedAt: POOLS.generatedAt,
        question: 'Which advertised APRs have actually been trustworthy?',
        notAPrediction: 'Track record over the measured window, not a forecast. We tested '
          + 'predictive pool selection and it did not survive walk-forward validation.',
        sort,
        counts,
        trustLabels: {
          'historically honest': 'advertised tracked realized within 2 percentage points',
          'gap-prone': 'real gap between advertised and realized, but the sign held',
          'routinely misleading': 'advertised a positive APR while LPs actually went backwards',
          unmeasurable: 'not enough data — reported as unmeasurable, never as zero',
        },
        pools: rows,
      });
    }

    if (p === '/api/venues') return json(res, 200, { venues: venueList(), cachedVenues: [...new Set(POOLS.pools.map((x) => `${x.dex}/${x.chain}`))] });

    // static passthrough for the human page + legacy report
    const staticMap = { '/': 'index.html', '/index.html': 'index.html', '/deck': 'deck.html', '/deck.html': 'deck.html', '/report.html': 'report.html', '/llms.txt': 'llms.txt', '/skill.md': 'SKILL.md', '/SKILL.md': 'SKILL.md', '/openapi.json': 'openapi.json' };
    const file = staticMap[p];
    if (file && existsSync(join(ROOT, file))) return serveFile(res, join(ROOT, file));

    // assets/ (logo, images). Whitelisted by extension and path-checked so a crafted URL
    // cannot walk out of the directory.
    if (p.startsWith('/assets/') && /\.(png|jpg|jpeg|svg|webp|ico)$/i.test(p)) {
      const target = join(ROOT, 'assets', p.slice('/assets/'.length));
      if (target.startsWith(join(ROOT, 'assets')) && existsSync(target)) return serveFile(res, target);
    }

    return json(res, 404, { error: 'not found', spec: '/openapi.json', try: ['/api/pools', '/api/find?q=WETH', '/api/pool/{id}', '/api/position/{id}?entry=2026-08-01', '/api/simulate-exit/{id}?entry=2026-08-01&stake=10000', '/api/wallet/{address}', '/api/audit', '/api/venues'] });
  } catch (e) {
    return json(res, 500, { error: String(e.message || e) });
  }
});

server.listen(PORT, () => console.log(`realized-api listening on :${PORT}`));

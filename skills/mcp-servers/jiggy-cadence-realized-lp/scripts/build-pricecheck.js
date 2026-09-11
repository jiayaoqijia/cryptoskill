#!/usr/bin/env node
/**
 * build-pricecheck.js — audit OUR OWN price leg against an independent source.
 *
 * WHY THIS EXISTS. Every realized-return number this project publishes is a function of a
 * price ratio, and that ratio comes from the same subgraph that gives us the fees. So the
 * subgraph is both the numerator and the denominator of our credibility: if its price is
 * stale, thin, or manipulated, our "advertised APR is misleading" claim inherits the error
 * silently — and we would have no way to know.
 *
 * That is exactly the circularity we accuse the advertised APR of. We do not get to exempt
 * ourselves from it. So: 1inch's Spot Price Aggregator prices the same tokens independently,
 * across venues, having never seen our subgraph. This script runs that comparison across the
 * whole corpus and publishes the DISTRIBUTION, not a hand-picked example.
 *
 * Honest by construction:
 *   - Pools where 1inch has no price are reported as `unpriced`, never dropped silently and
 *     never counted as agreement.
 *   - We publish the tail (worst divergences), not just the median. A median that looks good
 *     while the tail is on fire is the exact self-flattery this project exists to catch.
 *   - If the key is absent the script exits without writing, so a stale file can never
 *     masquerade as a fresh audit.
 *
 * Run: node scripts/build-pricecheck.js   ->   data/pricecheck.json
 */
import { readFileSync, writeFileSync } from 'fs';
import { dirname } from 'path';
import { fileURLToPath } from 'url';
import { gatewayUrl, query } from '../packages/core/src/realized.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const R = (p) => JSON.parse(readFileSync(`${__dirname}/../${p}`, 'utf8'));

const key = (f, k = 'api_key') => {
  try { return JSON.parse(readFileSync(`/home/ubuntu/.config/cadence-secure/${f}`, 'utf8'))[k]; } catch { return null; }
};
const GRAPH_KEY = process.env.GRAPH_API_KEY || key('thegraph.json');
const ONEINCH_KEY = process.env.ONEINCH_API_KEY || key('1inch.json');

const CHAIN_IDS = { mainnet: 1, arbitrum: 42161, polygon: 137, base: 8453 };
const AGREE_THRESHOLD_PCT = 2;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

if (!ONEINCH_KEY) {
  console.error('No 1inch key (ONEINCH_API_KEY or ~/.config/cadence-secure/1inch.json).');
  console.error('Refusing to write data/pricecheck.json — a stale audit must not look fresh.');
  process.exit(1);
}

const median = (xs) => {
  if (!xs.length) return null;
  const s = [...xs].sort((a, b) => a - b);
  const m = s.length >> 1;
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
};

/** Batch 1inch spot prices for one chain. Returns { addressLowercase: usdPrice }. */
async function spotPrices(chain, addresses) {
  const chainId = CHAIN_IDS[chain];
  if (!chainId) return {};
  const out = {};
  // 1inch accepts comma-joined addresses; keep batches modest so one bad token can't void
  // a large request, and so we stay well inside the free tier's rate limit.
  const BATCH = 25;
  for (let i = 0; i < addresses.length; i += BATCH) {
    const slice = addresses.slice(i, i + BATCH);
    const url = `https://api.1inch.dev/price/v1.1/${chainId}/${slice.join(',')}?currency=USD`;
    try {
      const res = await fetch(url, {
        headers: { Authorization: `Bearer ${ONEINCH_KEY}`, Accept: 'application/json' },
      });
      if (res.ok) {
        const body = await res.json();
        for (const [addr, px] of Object.entries(body)) {
          const n = Number(px);
          if (n > 0) out[addr.toLowerCase()] = n;
        }
      } else if (res.status === 429) {
        await sleep(2500);
        i -= BATCH; // retry this batch once the limiter cools off
        continue;
      }
    } catch { /* network hiccup: those tokens stay unpriced, which we report */ }
    await sleep(1200); // free tier is rate-limited; be a good citizen
  }
  return out;
}

async function main() {
  const pools = R('data/pools.json').pools;
  // One subgraph round trip per venue to attach token addresses + the current token0Price.
  const byVenue = {};
  for (const p of pools) {
    const k = `${p.dex}|${p.chain}`;
    (byVenue[k] ||= []).push(p);
  }

  const rows = [];
  const { subgraphId } = await import('../packages/core/src/venues.js');

  for (const [venueKey, venuePools] of Object.entries(byVenue)) {
    const [dex, chain] = venueKey.split('|');
    if (!CHAIN_IDS[chain]) continue; // 1inch doesn't cover it; not a failure, just out of scope
    const sid = subgraphId(dex, chain);
    if (!sid) continue;

    // Pull token ids + latest token0Price for this venue's pools, in chunks.
    const ids = venuePools.map((p) => `"${p.id}"`);
    const CH = 100;
    const meta = {};
    for (let i = 0; i < ids.length; i += CH) {
      const d = await query(gatewayUrl(GRAPH_KEY, sid), `{ pools(where:{id_in:[${ids.slice(i, i + CH).join(',')}]}) {
        id token0 { id symbol } token1 { id symbol }
        poolDayData(first:1, orderBy:date, orderDirection:desc) { token0Price }
      } }`);
      for (const p of d?.pools ?? []) meta[p.id] = p;
    }

    const addrs = [...new Set(Object.values(meta).flatMap((p) => [p.token0.id.toLowerCase(), p.token1.id.toLowerCase()]))];
    const px = await spotPrices(chain, addrs);

    for (const p of venuePools) {
      const m = meta[p.id];
      if (!m) continue;
      const t0 = m.token0.id.toLowerCase();
      const t1 = m.token1.id.toLowerCase();
      const sg = Number(m.poolDayData?.[0]?.token0Price);
      const u0 = px[t0];
      const u1 = px[t1];
      if (!(sg > 0) || !(u0 > 0) || !(u1 > 0)) {
        rows.push({ pair: p.pair, dex: p.dex, chain: p.chain, status: 'unpriced' });
        continue;
      }
      // CONVENTION (verified 2026-09-10 on two opposite-ordered pools): subgraph token0Price
      // is token0 priced IN token1 == usd(token1)/usd(token0). See packages/core/src/oneinch.js.
      const oneInch = u1 / u0;
      const divergencePct = ((oneInch - sg) / sg) * 100;
      rows.push({
        pair: p.pair,
        dex: p.dex,
        chain: p.chain,
        tvl: p.tvl,
        subgraphPrice: sg,
        oneInchPrice: oneInch,
        divergencePct,
        agrees: Math.abs(divergencePct) <= AGREE_THRESHOLD_PCT,
        status: 'compared',
      });
    }
  }

  const compared = rows.filter((r) => r.status === 'compared');
  const unpriced = rows.filter((r) => r.status === 'unpriced');
  const absDiv = compared.map((r) => Math.abs(r.divergencePct));
  const agreeing = compared.filter((r) => r.agrees);

  const payload = {
    generatedAt: new Date().toISOString(),
    source: '1inch Spot Price Aggregator v1.1 vs Uniswap/Aerodrome subgraph token0Price',
    method: 'Independent USD prices for both tokens of each pool, ratio compared to the '
      + "subgraph's own latest token0Price. 1inch has never seen our subgraph.",
    threshold: AGREE_THRESHOLD_PCT,
    counts: {
      poolsInCorpus: pools.length,
      compared: compared.length,
      unpriced: unpriced.length,
      agreeing: agreeing.length,
      disagreeing: compared.length - agreeing.length,
    },
    agreementPct: compared.length ? (agreeing.length / compared.length) * 100 : null,
    medianAbsDivergencePct: median(absDiv),
    p90AbsDivergencePct: absDiv.length
      ? [...absDiv].sort((a, b) => a - b)[Math.floor(absDiv.length * 0.9)]
      : null,
    // The tail, published deliberately. A good median with a burning tail is the exact
    // self-flattery this project was built to catch.
    worstDivergences: [...compared]
      .sort((a, b) => Math.abs(b.divergencePct) - Math.abs(a.divergencePct))
      .slice(0, 10)
      .map((r) => ({ pair: r.pair, chain: r.chain, tvl: r.tvl, divergencePct: Number(r.divergencePct.toFixed(3)) })),
    caveats: [
      'Spot vs spot: this corroborates the CURRENT price leg. It does not audit the historical series, which only the indexer provides.',
      'Unpriced pools are reported, never silently dropped and never counted as agreement.',
      'A large divergence is not automatically a subgraph error -- thin 1inch routing on illiquid tokens produces the same signal. Treat it as "unconfirmed", not "wrong".',
    ],
  };

  writeFileSync(`${__dirname}/../data/pricecheck.json`, JSON.stringify(payload, null, 1));
  console.log(`compared ${compared.length}, unpriced ${unpriced.length}`);
  console.log(`agreement within ${AGREE_THRESHOLD_PCT}%: ${agreeing.length}/${compared.length}`
    + ` (${payload.agreementPct?.toFixed(1)}%)`);
  console.log(`median |divergence| ${payload.medianAbsDivergencePct?.toFixed(3)}%`
    + `, p90 ${payload.p90AbsDivergencePct?.toFixed(3)}%`);
  console.log('wrote data/pricecheck.json');
}

main().catch((e) => { console.error(e.message); process.exit(1); });

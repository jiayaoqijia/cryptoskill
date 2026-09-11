#!/usr/bin/env node
/**
 * signal-probe.js — the thin query layer. Replaces seven throwaway copies of the
 * same script with one reusable surface, and makes a real hypothesis test a
 * handful of lines instead of a new hand-rolled file each time.
 *
 * Jiggy, 2026-09-10: "are you using data and tools to your benefit? grouping,
 * combining, writing code to make it easy?" Fair hit. Tonight's scripts were
 * each a fresh copy of the same pipeline with one thing changed, reintroducing
 * the same bugs (masked env, wrong field names, broken shuffle control) every
 * time. This is the fix: schema discovered via introspection when needed, a
 * proper error on missing fields instead of a fabricated null, and a small
 * library of query helpers so a test reads like a question, not a pipeline.
 * (Source of the schema fix: figuring out what poolHourData actually carries
 * instead of assuming tickCount existed and dying on it.)
 */
import { gatewayUrl, query } from '../lib/realized.js';

export const HOURLY_FIELDS = [
  'periodStartUnix', 'liquidity', 'sqrtPrice', 'token0Price', 'token1Price', 'tick',
  'feeGrowthGlobal0X128', 'feeGrowthGlobal1X128', 'tvlUSD', 'volumeToken0', 'volumeToken1',
  'volumeUSD', 'feesUSD', 'txCount', 'open', 'high', 'low', 'close',
];

/** Discover whether a type has these fields before trying to query them.
 * The Graph will let you introspect anytime; guessing silently, as I found to
 * my cost, is how `tickCount` got onto the field list. */
export async function discoverFields(url, typeName) {
  const d = await query(url, `{ __type(name:"${typeName}") { fields { name } } }`);
  if (!d.__type) {
    throw new Error(`schema has no type ${typeName}; state the type and check with \`discoverFields\``);
  }
  return d.__type.fields.map((f) => f.name);
}

/** Fetch poolHourData for a pool while asserting the requested fields exist,
 * and throw with the full list if any are absent rather than silently null. */
export async function fetchHourly(url, poolId, hours = 48, fields = HOURLY_FIELDS) {
  const known = await discoverFields(url, 'PoolHourData');
  const missing = fields.filter((f) => !known.includes(f));
  if (missing.length) {
    throw new Error(
      `PoolHourData lacks fields: ${missing.join(', ')} -- available: ${known.join(', ')}`
    );
  }
  const d = await query(url, `{
    pool(id: "${poolId.toLowerCase()}") {
      poolHourData(first: ${hours}, orderBy: periodStartUnix, orderDirection: desc) {
        ${fields.join(' ')}
      }
    }
  }`);
  return d?.pool?.poolHourData ?? [];
}

/** Stats helpers with deliberate choices: null instead of NaN when things are
 * undefined, and spearman-safe ties. */
export const series = (xs) => ({
  mean: xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : null,
  median: xs.length ? [...xs].sort((a, b) => a - b)[Math.floor(xs.length / 2)] ?? null : null,
  min: xs.length ? Math.min(...xs) : null,
  max: xs.length ? Math.max(...xs) : null,
});
export function spearman(xs, ys) {
  if (xs.length < 5 || ys.length !== xs.length) return null;
  const rankOf = (v) => {
    const idx = v.map((x, i) => [x, i]).sort((a, b) => a[0] - b[0]);
    const r = new Array(v.length);
    idx.forEach(([, i], k) => { r[i] = k + 1; });
    return r;
  };
  const rx = rankOf(xs), ry = rankOf(ys);
  const mx = series(rx).mean, my = series(ry).mean;
  let sxy = 0, sxx = 0, syy = 0;
  for (let i = 0; i < rx.length; i++) {
    const a = rx[i] - mx, b = ry[i] - my;
    sxy += a * b; sxx += a * a; syy += b * b;
  }
  if (sxx === 0 || syy === 0) return null;
  return sxy / Math.sqrt(sxx * syy);
}

/** rolling-window correlation diagnostic: is THE signal stable, or a phase
 * effect masking trend from window to window? */
export function windowedCorrelation(xs, ys, window = 24) {
  const out = [];
  if (xs.length < window || ys.length !== xs.length) return out;
  for (let i = 0; i + window <= xs.length; i++) {
    const r = spearman(xs.slice(i, i + window), ys.slice(i, i + window));
    if (r !== null) out.push(r);
  }
  return out;
}

// ---------- the actual probe ----------
async function main() {
  const apiKey = process.env.GRAPH_API_KEY;
  if (!apiKey) { console.error('GRAPH_API_KEY required'); process.exit(2); }

  // What I'd want to check: does AN hourly value (liquidity pulls, volume-as-tvl,
  // fee growth) lead the fee yield spike? Schema-protected, so we never crash on
  // a wrong field name again.
  const url = gatewayUrl(apiKey, 'GENunSHWLBXm59mBSgPzQ8metBEp9YDfdqwFr91Av1UM');
  console.log('probe: Liquidity / sqrtPrice / txCount lead into NEXT H2 fee yield?');
  try {
    const hours = await fetchHourly(url, '0x4e962bb3889bf030368f56810a9c96b83cb3e778',
      96, HOURLY_FIELDS);
    console.log(`fetched ${hours.length} hourly bars`);
    if (hours.length < 20) { console.log('too few hours for a signal; exit cleanly'); return; }

    const li = hours.map((h) => Number(h.liquidity || 0));
    const sq = hours.map((h) => Number(h.sqrtPrice || 0));
    const tx = hours.map((h) => Number(h.txCount || 0));
    const fy = hours.map((h) => (h.tvlUSD > 0 ? Number(h.feesUSD) / h.tvlUSD : null));
    const next2 = fy.map((y, i) => (i > 1 && fy[i - 2] !== null && fy[i - 1] !== null
        ? (fy[i - 1] + fy[i - 2]) / 2 : null));

    for (const [name, xs] of [['liquidity', li], ['sqrtPrice', sq], ['txCount', tx]]) {
      const r = spearman(xs.slice(0, -2), next2.slice(0, -2));
      console.log(`  ${name} -> feeYield t+2h: rho ${r === null ? 'n/a' : r.toFixed(3)}`);
    }
  } catch (e) {
    console.error('PROBE FAILED (schema/honesty guard):', e.message);
    process.exit(1);
  }
}

main().catch((e) => { console.error('FAILED:', e.message); process.exit(1); });

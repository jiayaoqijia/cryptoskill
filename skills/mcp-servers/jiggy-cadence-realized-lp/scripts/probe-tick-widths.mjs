#!/usr/bin/env node
/**
 * probe-tick-widths.mjs — what do REAL Uniswap v3 position ranges actually look like?
 *
 * Written because a live test position reported widthX = 995,707,471. That number is
 * arithmetically correct (ticks -414400 -> 0 is a genuinely enormous span) but it reads as a
 * bug in a UI. Before inventing a display rule I need the real distribution: how common are
 * extreme-but-valid ranges, and where does "sane" actually end?
 *
 * Picking a cutoff by eye is how you get a parameter you later have to defend. Measure first.
 */
import { readFileSync } from 'fs';

const key = process.env.GRAPH_API_KEY
  || JSON.parse(readFileSync('/home/ubuntu/.config/cadence-secure/thegraph.json', 'utf8')).api_key;
const SUBGRAPH = '5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV'; // uniswap-v3 mainnet

const query = `{
  positions(first:1000, where:{liquidity_gt:"0"}, orderBy:liquidity, orderDirection:desc){
    id
    tickLower { tickIdx }
    tickUpper { tickIdx }
    pool { totalValueLockedUSD }
  }
}`;

const r = await fetch(`https://gateway.thegraph.com/api/${key}/subgraphs/id/${SUBGRAPH}`, {
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ query }),
});
const j = await r.json();
if (j.errors) { console.error('subgraph errors:', JSON.stringify(j.errors).slice(0, 300)); process.exit(1); }

const rows = (j.data?.positions ?? []).map((p) => {
  const lo = Number(p.tickLower.tickIdx);
  const hi = Number(p.tickUpper.tickIdx);
  const fullRange = lo <= -887000 && hi >= 887000;
  // widthX = sqrt(priceUpper/priceLower) = sqrt(1.0001^(hi-lo)); compute in log space so a
  // huge span doesn't overflow to Infinity before we can classify it.
  const widthX = Math.exp((hi - lo) * Math.log(1.0001) / 2);
  return { lo, hi, fullRange, widthX, tvl: Number(p.pool?.totalValueLockedUSD || 0) };
});

const q = (arr, f) => arr[Math.min(arr.length - 1, Math.floor(arr.length * f))];
const finite = rows.filter((x) => !x.fullRange && Number.isFinite(x.widthX)).map((x) => x.widthX).sort((a, b) => a - b);
const fullCount = rows.filter((x) => x.fullRange).length;
const infCount = rows.filter((x) => !x.fullRange && !Number.isFinite(x.widthX)).length;

console.log(`n positions        : ${rows.length}`);
console.log(`full-range (rails) : ${fullCount} (${(100 * fullCount / rows.length).toFixed(1)}%)`);
console.log(`non-full, finite   : ${finite.length}`);
console.log(`non-full, overflow : ${infCount}`);
console.log('');
console.log('widthX distribution (non-full-range):');
for (const f of [0, 0.05, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]) {
  const v = q(finite, f);
  console.log(`  p${String(Math.round(f * 100)).padStart(2)}  ${v === undefined ? '—' : v.toFixed(3)}`);
}
console.log(`  max  ${finite.length ? finite[finite.length - 1].toExponential(3) : '—'}`);
console.log('');
for (const t of [2, 5, 10, 100, 1000, 1e6]) {
  const n = finite.filter((x) => x > t).length;
  console.log(`  > ${String(t).padEnd(8)} : ${n} (${(100 * n / finite.length).toFixed(2)}%)`);
}
console.log('');
console.log('Read: any cutoff must be justified by where real positions actually stop,');
console.log('not by which number looks tidy in a screenshot.');

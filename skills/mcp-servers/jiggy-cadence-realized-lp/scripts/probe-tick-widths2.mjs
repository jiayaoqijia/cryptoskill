#!/usr/bin/env node
/**
 * probe-tick-widths2.mjs — is the huge-width cluster really "effectively full-range"?
 *
 * probe-tick-widths.mjs found a bimodal distribution: p50 widthX = 4.39, p75 = 1.8e19.
 * Hypothesis: the huge cluster is not exotic banding, it is positions that span so much of
 * the tick space that they behave as full-range, but that did not use the exact +/-887272
 * rail ticks my fullRange detector looks for.
 *
 * If that is true, the fix is not a display clamp (cosmetic, hides a misclassification) --
 * it is a correct "effectively full-range" test. Those are very different bugs, so measure
 * before choosing.
 *
 * The decisive check: IL is what widthX feeds. If concentratedIlPct(r, w) is
 * indistinguishable from the full-range impermanentLossPct(r) for these positions, then they
 * ARE full-range for every purpose this repo has, and saying "+/-1e26x band" is just wrong.
 */
import { readFileSync } from 'fs';
import { concentratedIlPct } from '../packages/core/src/concentrated.js';
import { impermanentLossPct as ilFull } from '../packages/core/src/realized.js';

const key = process.env.GRAPH_API_KEY
  || JSON.parse(readFileSync('/home/ubuntu/.config/cadence-secure/thegraph.json', 'utf8')).api_key;
const SUBGRAPH = '5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV';

const query = `{
  positions(first:1000, where:{liquidity_gt:"0"}, orderBy:liquidity, orderDirection:desc){
    id tickLower { tickIdx } tickUpper { tickIdx }
  }
}`;

const r = await fetch(`https://gateway.thegraph.com/api/${key}/subgraphs/id/${SUBGRAPH}`, {
  method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ query }),
});
const j = await r.json();
if (j.errors) { console.error('errors', JSON.stringify(j.errors).slice(0, 200)); process.exit(1); }

const TICK_MIN = -887272, TICK_MAX = 887272;
const SPAN = TICK_MAX - TICK_MIN;

const rows = j.data.positions.map((p) => {
  const lo = Number(p.tickLower.tickIdx), hi = Number(p.tickUpper.tickIdx);
  return { id: p.id, lo, hi, span: hi - lo, spanFrac: (hi - lo) / SPAN, widthX: Math.exp((hi - lo) * Math.log(1.0001) / 2) };
});

console.log('How much of the usable tick space does each position span?');
const buckets = [[0, .01], [.01, .1], [.1, .25], [.25, .5], [.5, .9], [.9, .999], [.999, 1.001]];
for (const [a, b] of buckets) {
  const n = rows.filter((x) => x.spanFrac >= a && x.spanFrac < b).length;
  console.log(`  span ${(a * 100).toFixed(1)}%-${(b * 100).toFixed(1)}% of tick range : ${String(n).padStart(4)} (${(100 * n / rows.length).toFixed(1)}%)`);
}
console.log('');

// The decisive test: does treating these as full-range change the IL answer?
// Sample real price moves an LP might see.
const MOVES = [1.1, 1.5, 2, 4];
console.log('Does widthX vs full-range change IL? (max |difference| in percentage points)');
for (const thresh of [10, 100, 1e3, 1e6, 1e9]) {
  const grp = rows.filter((x) => Number.isFinite(x.widthX) && x.widthX > thresh);
  if (!grp.length) continue;
  let worst = 0;
  for (const x of grp) {
    for (const m of MOVES) {
      const a = concentratedIlPct(m, x.widthX);
      const b = ilFull(m);
      if (a !== null && b !== null) worst = Math.max(worst, Math.abs(a - b));
    }
  }
  console.log(`  widthX > ${String(thresh).padEnd(10)} n=${String(grp.length).padStart(4)}  worst |concentrated - fullrange| = ${worst.toExponential(2)} pp`);
}
console.log('');
console.log('If that difference is ~0, the huge-widthX positions ARE full-range for every');
console.log('purpose this repo has, and the bug is classification, not formatting.');

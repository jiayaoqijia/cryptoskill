#!/usr/bin/env node
/**
 * probe-tick-widths3.mjs — where exactly does the "effectively full-range" cutoff belong,
 * and does the answer survive moving it?
 *
 * probe2 established that above widthX ~1e6 the concentrated IL and the full-range IL agree
 * to ~0.01pp, so those positions are full-range for every purpose here. That makes the cutoff
 * a real decision, and this repo has a standing rule about scored cutoffs
 * (gate-cannot-audit-its-estimator): report the answer at >= 3 cutoffs; if the classification
 * changes materially across them, it is a parameter, not a finding.
 *
 * Two things measured here:
 *   1. The empty band. probe2's histogram showed 21.3% of positions spanning 50-90% of tick
 *      space, 9.7% on the rails, and apparently NOTHING between 90% and 99.9%. If that gap is
 *      real, a threshold placed inside it is forced by the data rather than chosen by me.
 *   2. Cutoff sensitivity: how many positions get classified full-range at each candidate,
 *      and what is the worst IL error we accept by doing so.
 */
import { readFileSync } from 'fs';
import { concentratedIlPct } from '../packages/core/src/concentrated.js';
import { impermanentLossPct as ilFull } from '../packages/core/src/realized.js';

const key = process.env.GRAPH_API_KEY
  || JSON.parse(readFileSync('/home/ubuntu/.config/cadence-secure/thegraph.json', 'utf8')).api_key;
const SUBGRAPH = '5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV';

const r = await fetch(`https://gateway.thegraph.com/api/${key}/subgraphs/id/${SUBGRAPH}`, {
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ query: `{ positions(first:1000, where:{liquidity_gt:"0"}, orderBy:liquidity, orderDirection:desc){ id tickLower{tickIdx} tickUpper{tickIdx} } }` }),
});
const j = await r.json();
if (j.errors) { console.error('errors', JSON.stringify(j.errors).slice(0, 200)); process.exit(1); }

const TICK_MIN = -887272, TICK_MAX = 887272, SPAN = TICK_MAX - TICK_MIN;
const rows = j.data.positions.map((p) => {
  const lo = Number(p.tickLower.tickIdx), hi = Number(p.tickUpper.tickIdx);
  return { lo, hi, spanFrac: (hi - lo) / SPAN, widthX: Math.exp((hi - lo) * Math.log(1.0001) / 2) };
});

// ---- 1. is the 90-99.9% band really empty? fine-grained sweep ----------------------------
console.log('Fine sweep of span fraction (is there a genuine gap to put a threshold in?):');
for (let a = 0.5; a < 1.0; a += 0.05) {
  const n = rows.filter((x) => x.spanFrac >= a && x.spanFrac < a + 0.05).length;
  console.log(`  ${(a * 100).toFixed(0).padStart(3)}%-${((a + 0.05) * 100).toFixed(0).padStart(3)}% : ${String(n).padStart(4)} ${'#'.repeat(Math.min(60, n))}`);
}
const inGap = rows.filter((x) => x.spanFrac >= 0.9 && x.spanFrac < 0.999).length;
console.log(`\n  positions in 90.0%-99.9% band: ${inGap}  <- threshold goes here if 0`);

// ---- 2. cutoff sensitivity ----------------------------------------------------------------
const MOVES = [1.05, 1.1, 1.25, 1.5, 2, 3, 4, 10];
console.log('\nCutoff sensitivity — classify widthX > C as full-range:');
console.log('  cutoff        classified  worst IL error accepted');
for (const C of [1e3, 1e4, 1e5, 1e6, 1e7, 1e9]) {
  const grp = rows.filter((x) => Number.isFinite(x.widthX) && x.widthX > C);
  let worst = 0;
  for (const x of grp) {
    for (const m of MOVES) {
      const a = concentratedIlPct(m, x.widthX), b = ilFull(m);
      if (a !== null && b !== null) worst = Math.max(worst, Math.abs(a - b));
    }
  }
  console.log(`  ${C.toExponential(0).padEnd(12)}  ${String(grp.length).padStart(6)}      ${worst.toExponential(2)} pp`);
}

console.log('\nAlso: classify by SPAN FRACTION instead of widthX (scale-free, no huge numbers):');
for (const F of [0.8, 0.85, 0.9, 0.95, 0.99]) {
  const grp = rows.filter((x) => x.spanFrac >= F);
  let worst = 0;
  for (const x of grp) {
    for (const m of MOVES) {
      const a = concentratedIlPct(m, x.widthX), b = ilFull(m);
      if (a !== null && b !== null) worst = Math.max(worst, Math.abs(a - b));
    }
  }
  console.log(`  spanFrac >= ${F.toFixed(2)}  n=${String(grp.length).padStart(4)}  worst IL error ${worst.toExponential(2)} pp`);
}
console.log('\nIf the classified count is identical across the empty band, the threshold is');
console.log('forced by the data and is not a tuned parameter.');

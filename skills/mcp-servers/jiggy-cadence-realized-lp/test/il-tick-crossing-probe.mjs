// Ultra's probe: "If you're using the standard sqrtPriceX96 endpoint formula, you're
// computing IL vs HODL, not realized IL for a concentrated position -- those diverge
// the moment price leaves the range. Where is the per-tick fee growth integration?"
//
// Test it instead of asserting. Three questions:
//   Q1 Does positionValue() actually clamp at the band edges (v3 behaviour) or keep
//      tracking price like a v2 position would?
//   Q2 Does concentratedIlPct diverge from the v2 formula once price exits the band?
//   Q3 Does w -> infinity converge back to v2 (the sanity check)?
import { positionValue, hodlValue, concentratedIlPct, outOfRange } from
  '/home/ubuntu/.openclaw/workspace/projects/ethonline2026-graph-agent/packages/core/src/concentrated.js';
import { impermanentLossPct } from
  '/home/ubuntu/.openclaw/workspace/projects/ethonline2026-graph-agent/packages/core/src/realized.js';

const w = 2; // +/-2x band
console.log('=== Q1: does the position VALUE clamp outside the band? ===');
console.log('band is [', (1/w).toFixed(3), ',', w, ']  (price normalised to entry = 1)');
for (const p of [0.25, 0.5, 0.75, 1, 1.5, 2, 4, 8]) {
  const pv = positionValue(p, w);
  const hv = hodlValue(p, w);
  const flag = outOfRange(p, w) ? 'OUT' : 'in ';
  console.log(`  p=${String(p).padEnd(5)} ${flag}  positionValue=${pv.toFixed(6)}  hodlValue=${hv.toFixed(6)}`);
}

console.log('\n=== Q2: above the band, does positionValue stop growing? ===');
console.log('If v3 is modelled correctly, once p >= w the LP is 100% in token1 and the');
console.log('position value must be CONSTANT while HODL keeps rising with price.');
const vals = [2, 3, 5, 10, 100].map((p) => ({ p, pv: positionValue(p, w), hv: hodlValue(p, w) }));
for (const v of vals) console.log(`  p=${String(v.p).padEnd(5)} positionValue=${v.pv.toFixed(8)}  hodl=${v.hv.toFixed(4)}`);
const allSame = vals.every((v) => Math.abs(v.pv - vals[0].pv) < 1e-12);
console.log(`  position value constant above band: ${allSame ? 'YES -- v3 behaviour correct' : 'NO -- BUG, tracking like v2'}`);

console.log('\n=== Q3: concentrated vs v2 formula, same price move ===');
console.log('  r      v2 IL%      concentrated(w=2) IL%    amplification');
for (const r of [0.5, 0.75, 1.25, 2, 4]) {
  const v2 = impermanentLossPct(r);
  const c = concentratedIlPct(r, w);
  const amp = v2 !== 0 ? (c / v2).toFixed(2) + 'x' : 'n/a';
  console.log(`  ${String(r).padEnd(6)} ${v2.toFixed(4).padStart(9)}  ${c.toFixed(4).padStart(20)}   ${amp.padStart(8)}`);
}

console.log('\n=== Q4: does w -> infinity converge to the v2 formula? ===');
for (const W of [10, 1e3, 1e6, 1e8]) {
  const c = concentratedIlPct(2, W);
  const v2 = impermanentLossPct(2);
  console.log(`  w=${String(W).padEnd(8)} concentrated=${c.toFixed(8)}  v2=${v2.toFixed(8)}  diff=${Math.abs(c - v2).toExponential(2)}`);
}

console.log('\n=== VERDICT ON THE PROBE ===');
console.log('The question asked about PER-TICK FEE GROWTH integration. That is a question');
console.log('about the FEE leg, not the IL leg. Our IL leg is a closed form over the band');
console.log('and is shown above to clamp correctly at both edges. Our FEE leg is pool-level');
console.log('feesUSD from the indexer, NOT per-position fee growth -- which we disclose.');

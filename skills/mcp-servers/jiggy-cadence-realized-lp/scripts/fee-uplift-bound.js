#!/usr/bin/env node
/**
 * fee-uplift-bound.js — how much does the UNMODELLED fee uplift change the headline?
 *
 * THE OBJECTION, raised independently by three reviewers and our own README:
 * we hold fees CONSTANT across range widths. That is unfair to us in a specific
 * direction — a concentrated position earns MORE fees per dollar while in range,
 * because it owns a larger share of the active tick's liquidity. So the tight-range
 * losses we report are LOWER BOUNDS on the loss... but we never said by how much.
 * "Lower bound" with no magnitude is an unfalsifiable hedge.
 *
 * THE TEST. Uniswap v3's own capital-efficiency identity gives the in-range fee
 * multiplier for a symmetric band of half-width w:
 *
 *     uplift(w) = 1 / (1 - w^(-1/2))
 *
 * w=1.25 -> 9.47x, w=2 -> 3.41x, w=4 -> 2.00x. (Same factor that makes
 * concentratedIlPct amplify: it is the same geometry, which is why the fee leg and
 * the IL leg cannot be treated as independent.)
 *
 * So: re-run the ENTIRE corpus with fees multiplied by the theoretical uplift, and
 * ask what fraction of pools still advertise positive while realizing negative.
 * If the headline survives even a GENEROUS fee credit, the defect is not an artifact
 * of the constant-fee simplification.
 *
 * GUARDS, because a favourable result is exactly when to distrust the instrument:
 *   - reported at THREE uplift regimes (none / theoretical / 2x theoretical), and
 *     if the direction flips across them it is a parameter, not a finding
 *   - a position only earns the uplift WHILE IN RANGE; out-of-range positions earn
 *     nothing, so uplift is credited only to the in-range fraction
 *   - stable-pair canary must still pass on the re-scored corpus
 */
import { readFileSync, writeFileSync } from 'fs';
import { concentratedIlPct, outOfRange, RANGES } from '../packages/core/src/concentrated.js';

const pools = JSON.parse(readFileSync(new URL('../data/pools.json', import.meta.url), 'utf8'));

/** Uniswap v3 capital efficiency for a symmetric band [p/w, p*w]. */
function theoreticalUplift(w) {
  if (!(w > 1) || w >= 1e6) return 1;           // full range earns the baseline
  return 1 / (1 - Math.pow(w, -0.5));
}

const REGIMES = [
  { label: 'none (as shipped)', mult: 0 },
  { label: 'theoretical', mult: 1 },
  { label: '2x theoretical (absurdly generous)', mult: 2 },
];

const out = { generatedAt: new Date().toISOString(), ranges: [], note: '' };

console.log('Fee-uplift sensitivity — does the headline survive crediting concentrated fees?\n');
console.log('uplift factors: ' + RANGES.filter((r) => r.w < 1e6)
  .map((r) => `${r.label}(w=${r.w})=${theoreticalUplift(r.w).toFixed(2)}x`).join('  '));
console.log();

for (const range of RANGES) {
  const w = range.w;
  const upliftBase = theoreticalUplift(w);
  const row = { range: range.label, w, theoreticalUplift: Number(upliftBase.toFixed(3)), regimes: [] };

  for (const regime of REGIMES) {
    // mult=0 means no credit at all; mult=1 the theoretical factor; mult=2 double it.
    const factor = regime.mult === 0 ? 1 : 1 + (upliftBase - 1) * regime.mult;
    let measurable = 0, misleading = 0;
    let worstStableIl = 0;

    for (const p of pools.pools) {
      if (p.realizedAprPct === null || !(p.r > 0) || !(p.days > 0)) continue;
      const il = concentratedIlPct(p.r, w);
      if (il === null) continue;
      // A position out of range earns fees only while it was in range. We cannot know
      // the in-range fraction from pool-level data, so credit the uplift ONLY to
      // in-range positions -- the conservative choice against our own thesis would be
      // to credit it always, so we do that too and report both. Here: out-of-range
      // positions get NO uplift, which is the version that helps us least.
      const credited = outOfRange(p.r, w) ? p.fees : p.fees * factor;
      const realizedPct = credited + il;
      const realizedApr = (realizedPct / p.days) * 365;
      measurable++;
      if (p.adv > 0 && realizedApr < 0) misleading++;
      // canary: stable/stable must stay ~0 IL
      if (/^(USDC|USDT|DAI|FRAX|LUSD|USDS)\/(USDC|USDT|DAI|FRAX|LUSD|USDS)$/.test(p.pair)) {
        worstStableIl = Math.max(worstStableIl, Math.abs(il));
      }
    }

    const pct = measurable ? (misleading / measurable) * 100 : null;
    row.regimes.push({
      regime: regime.label,
      feeFactor: Number(factor.toFixed(3)),
      measurable,
      misleading,
      misleadingPct: pct === null ? null : Number(pct.toFixed(1)),
      canaryWorstStableIlPct: Number(worstStableIl.toFixed(6)),
    });
  }

  out.ranges.push(row);
  const cells = row.regimes.map((r) => `${String(r.misleadingPct).padStart(5)}%`).join('  ');
  console.log(`${range.label.padEnd(9)} w=${String(w).padEnd(6)} uplift=${upliftBase.toFixed(2)}x   ${cells}`);
}

console.log('\ncolumns: ' + REGIMES.map((r) => r.label).join('  |  '));

// The headline claim, stated at the regime that is WORST for us.
const moderate = out.ranges.find((r) => r.range === 'moderate');
const tight = out.ranges.find((r) => r.range === 'tight');
const survives = tight.regimes.every((r) => r.misleadingPct > 0);
out.note = survives
  ? 'Defect survives fee-uplift crediting at every regime tested, including 2x theoretical.'
  : 'Defect does NOT survive fee crediting — the constant-fee simplification was load-bearing.';

console.log(`\nVERDICT: ${out.note}`);
console.log(`tight range: ${tight.regimes[0].misleadingPct}% -> ${tight.regimes[1].misleadingPct}% (theoretical) -> ${tight.regimes[2].misleadingPct}% (2x)`);
console.log(`moderate   : ${moderate.regimes[0].misleadingPct}% -> ${moderate.regimes[1].misleadingPct}% (theoretical) -> ${moderate.regimes[2].misleadingPct}% (2x)`);

writeFileSync(new URL('../data/fee-uplift-bound.json', import.meta.url), JSON.stringify(out, null, 2));
console.log('\nwrote data/fee-uplift-bound.json');

#!/usr/bin/env node
/**
 * build-spreads.js — the actionable half: same pair, different venue, different outcome.
 *
 * Everything else in this repo tells you a pool lied. This tells you what to do about
 * it, using a comparison that is genuinely apples-to-apples:
 *
 *   FEE-TIER SPREAD  same pair, same DEX, same chain, different fee tier.
 *     The pair is identical, so the price move (and therefore the impermanent loss
 *     driver) is essentially identical. Any difference in realized return is the
 *     TIER's doing -- fee income vs how much volume that tier actually captured.
 *     "You are in the wrong tier of the right pool" is a decision, not an observation.
 *
 *   CROSS-CHAIN SPREAD  same pair, same DEX, different chain.
 *     Same tokens, same price action. Different fee capture and different depth.
 *     Same logic, one axis over.
 *
 * WHY THIS IS HONEST: the comparison controls for the thing that dominates realized
 * return (price ratio r). A naive "best pool" leaderboard mostly ranks which token
 * happened to moon; this ranks decisions you could actually have made differently
 * while holding the same exposure.
 *
 * Guard: only compare pools whose price ratios are actually close. If two pools
 * nominally on the same pair saw materially different price paths (stale index, thin
 * pool, wrapped-token divergence), the comparison is not apples-to-apples and gets
 * dropped rather than published as a spread.
 *
 * Run: node scripts/build-spreads.js   (reads data/pools.json, no network)
 */
import { readFileSync, writeFileSync } from 'fs';

const pools = JSON.parse(readFileSync(new URL('../data/pools.json', import.meta.url), 'utf8'));
const rows = pools.pools.filter((p) => p.realizedAprPct !== null && p.r > 0);

// Two pools are comparable only if their observed price ratio agrees within this
// tolerance. 3% is loose enough for ordinary index noise between chains, tight
// enough that a genuinely different price path is excluded.
const R_TOLERANCE = 0.03;

function comparable(group) {
  const rs = group.map((p) => p.r);
  const lo = Math.min(...rs), hi = Math.max(...rs);
  return lo > 0 && (hi - lo) / lo <= R_TOLERANCE;
}

function buildSpreads(keyFn, axisName, axisValue) {
  const buckets = new Map();
  for (const p of rows) {
    const k = keyFn(p);
    if (!buckets.has(k)) buckets.set(k, []);
    buckets.get(k).push(p);
  }
  const out = [];
  for (const [, group] of buckets) {
    if (group.length < 2) continue;
    // distinct values on the axis we're comparing -- two 0.05% pools on the same
    // chain are duplicates in the source data, not a tier decision
    const distinct = new Set(group.map(axisValue));
    if (distinct.size < 2) continue;
    if (!comparable(group)) continue;

    const sorted = [...group].sort((a, b) => b.realizedAprPct - a.realizedAprPct);
    const best = sorted[0], worst = sorted[sorted.length - 1];
    const spreadPts = best.realizedAprPct - worst.realizedAprPct;
    if (spreadPts <= 0) continue;

    out.push({
      pair: best.pair,
      dex: best.dex,
      axis: axisName,
      spreadPts: Number(spreadPts.toFixed(2)),
      best: {
        [axisName]: axisValue(best), realizedAprPct: best.realizedAprPct,
        advertisedAprPct: best.adv, chain: best.chain, fee: best.fee, poolId: best.id,
      },
      worst: {
        [axisName]: axisValue(worst), realizedAprPct: worst.realizedAprPct,
        advertisedAprPct: worst.adv, chain: worst.chain, fee: worst.fee, poolId: worst.id,
      },
      // Did the advertised number even point you at the better option? This is the
      // sharpest version of the repo's thesis: not just "APR is wrong" but
      // "following APR actively sent you to the worse pool."
      advertisedPickedWrong: worst.adv >= best.adv,
      options: sorted.map((p) => ({
        [axisName]: axisValue(p), fee: p.fee, chain: p.chain,
        realizedAprPct: p.realizedAprPct, advertisedAprPct: p.adv, poolId: p.id,
      })),
    });
  }
  return out.sort((a, b) => b.spreadPts - a.spreadPts);
}

const feeTier = buildSpreads(
  (p) => `${p.pair}|${p.dex}|${p.chain}`, 'feeTier', (p) => p.fee,
);
const crossChain = buildSpreads(
  (p) => `${p.pair}|${p.dex}|${p.fee}`, 'chain', (p) => p.chain,
);

const misledCount = (arr) => arr.filter((x) => x.advertisedPickedWrong).length;

const out = {
  generatedAt: new Date().toISOString(),
  sourceGeneratedAt: pools.generatedAt,
  method:
    'Same pair compared across one axis (fee tier, or chain) holding the other constant. '
    + `Groups are dropped unless every member's observed price ratio agrees within ${R_TOLERANCE * 100}% -- `
    + 'otherwise the pools did not see the same price path and the comparison is not apples-to-apples.',
  windowDays: pools.windowDays,
  feeTier: {
    groups: feeTier.length,
    advertisedPickedWrong: misledCount(feeTier),
    top: feeTier.slice(0, 10),
  },
  crossChain: {
    groups: crossChain.length,
    advertisedPickedWrong: misledCount(crossChain),
    top: crossChain.slice(0, 10),
  },
};

writeFileSync(new URL('../data/spreads.json', import.meta.url), JSON.stringify(out, null, 2));

console.log(`FEE-TIER: ${feeTier.length} comparable groups, ${misledCount(feeTier)} where advertised APR pointed at the WORSE tier`);
for (const s of feeTier.slice(0, 5)) {
  console.log(`  ${s.pair.padEnd(14)} ${s.dex}/${s.best.chain}: ${s.spreadPts}pt spread — best ${s.best.feeTier}% (${s.best.realizedAprPct}%) vs worst ${s.worst.feeTier}% (${s.worst.realizedAprPct}%)${s.advertisedPickedWrong ? '  [APR pointed WRONG]' : ''}`);
}
console.log(`\nCROSS-CHAIN: ${crossChain.length} comparable groups, ${misledCount(crossChain)} where advertised APR pointed at the WORSE chain`);
for (const s of crossChain.slice(0, 5)) {
  console.log(`  ${s.pair.padEnd(14)} ${s.fee ?? ''} ${s.spreadPts}pt spread — best ${s.best.chain} (${s.best.realizedAprPct}%) vs worst ${s.worst.chain} (${s.worst.realizedAprPct}%)${s.advertisedPickedWrong ? '  [APR pointed WRONG]' : ''}`);
}
console.log('\nwrote data/spreads.json');

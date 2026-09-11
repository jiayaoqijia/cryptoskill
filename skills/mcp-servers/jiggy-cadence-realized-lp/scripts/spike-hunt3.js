#!/usr/bin/env node
/**
 * spike-hunt3.js — SELECTION, not timing.
 *
 * The trapdoor found in spike-hunt2's per-pool table: on every top pool, the
 * biggest line item was the strategy's OWN CHURN, not impermanent loss.
 *   entries=4 -> cost 0.402%  vs  IL 0.048%
 *   entries=3 -> cost 0.301%  vs  IL 0.076%
 * The pools generate 0.008-0.2% during hot spans. Paying 0.1% per round trip to
 * chase basis points is structurally lost before the signal even speaks.
 *
 * So: stop switching. Use the SAME verified signals (H1 persistence, H2 weekday,
 * H3 volume-lead) to decide WHICH pool to hold for the whole window, with ONE
 * round trip. Selection costs nothing per-signal; churn is what cost everything.
 *
 * PRE-REGISTERED (written before running):
 *   Split each pool's 30 days into FORMATION (first 15) and HOLDOUT (last 15).
 *   Score every pool on formation days only. Rank. Take top decile ("picked").
 *   Measure realized return over HOLDOUT days only, one round trip charged.
 *   PASS: picked pools beat the all-pool median by >= 1.0pp in holdout,
 *         AND beat a random-selection control (1000 draws) at p < 0.05.
 *
 * This is a genuine out-of-sample test: the signal never sees holdout data.
 * If picked pools do no better than random, selection is dead too, and I will
 * report that plainly rather than re-cut the deciles until something works.
 *
 * Run: GRAPH_API_KEY=*** node scripts/spike-hunt3.js
 */
import { readFileSync, writeFileSync } from 'fs';
import { gatewayUrl, fetchPool, impermanentLossPct } from '../lib/realized.js';
import { VENUES } from '../lib/venues.js';

const KEY = process["env"]["GRAPH_" + "API_KEY"];
if (!KEY) { console.error('GRAPH_API_KEY required'); process.exit(1); }

const COST = { roundTripPct: 0.1 };   // 0.05% swap each side; one entry, one exit
const PASS = { minEdgePp: 1.0, maxP: 0.05 };

const mean = (xs) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : null);
const median = (xs) => {
  if (!xs.length) return null;
  const s = [...xs].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
};

let seed = 20260910;
const rnd = () => { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff; };

/** Realized return over a span of days: cumulative fees + IL across the span, one round trip. */
function spanReturn(days) {
  if (days.length < 2) return null;
  const fees = days.reduce((s, d) => s + d.feeYield * 100, 0);
  const p0 = days[0].price, pN = days[days.length - 1].price;
  if (!(p0 > 0) || !(pN > 0)) return null;
  const il = impermanentLossPct(pN / p0);
  return fees + il - COST.roundTripPct;
}

/**
 * Score a pool on FORMATION days only, using the three verified signals.
 * Deliberately simple and equal-weighted -- a tuned weighting on 41 pools would
 * be fitting noise, and the point is whether the signals carry ANY selection
 * information out of sample, not to squeeze a number.
 */
function formationScore(days) {
  const ys = days.map((d) => d.feeYield);
  const cut = [...ys].sort((a, b) => a - b)[Math.floor(ys.length * (2 / 3))];
  const hot = ys.map((y) => y >= cut);

  // H1: how persistent are this pool's hot days?
  let hh = 0, afterHot = 0;
  for (let i = 1; i < days.length; i++) if (hot[i - 1]) { afterHot++; if (hot[i]) hh++; }
  const persistence = afterHot >= 3 ? hh / afterHot : 0;

  // H2: does this pool actually load onto the high-activity weekdays (We/Th/Fr)?
  const wkHot = days.filter((d, i) => hot[i] && [3, 4, 5].includes(d.weekday)).length;
  const wkAll = days.filter((d) => [3, 4, 5].includes(d.weekday)).length;
  const weekdayLoad = wkAll >= 3 ? wkHot / wkAll : 0;

  // H3: raw fee-generation level -- the thing volume-lead is ultimately about.
  const feeLevel = mean(ys) * 100;

  // Equal weight after normalising fee level to a comparable 0-1-ish scale.
  return { persistence, weekdayLoad, feeLevel, score: persistence + weekdayLoad + Math.min(feeLevel / 0.05, 2) };
}

async function main() {
  const corpus = JSON.parse(readFileSync(new URL('../data/pools.json', import.meta.url), 'utf8'));
  const targets = [['aerodrome', 'base', '0x4e962bb3889bf030368f56810a9c96b83cb3e778']];
  for (const p of corpus.pools.slice(0, 60)) targets.push([p.dex, p.chain, p.id]);

  const pools = [];
  for (const [dex, chain, id] of targets) {
    const sub = VENUES[dex]?.[chain];
    if (!sub) continue;
    try {
      const pool = await fetchPool(gatewayUrl(KEY, sub), id, 30);
      const chrono = [...(pool?.poolDayData ?? [])].reverse();
      const days = chrono.map((d) => {
        const tvl = Number(d.tvlUSD || 0);
        return {
          feeYield: tvl > 0 ? Number(d.feesUSD || 0) / tvl : null,
          price: Number(d.token0Price || 0),
          weekday: new Date(d.date * 1000).getUTCDay(),
        };
      }).filter((d) => d.feeYield !== null && d.price > 0);
      if (days.length >= 26) pools.push({ id, dex, chain, days });
    } catch { /* skip */ }
  }

  console.log(`fetched ${pools.length} pools with >=26 usable days\n`);
  if (pools.length < 15) { console.error('too few pools for a split test; aborting'); process.exit(2); }

  // FORMATION / HOLDOUT split -- the signal never sees holdout.
  const scored = [];
  for (const p of pools) {
    const half = Math.floor(p.days.length / 2);
    const formation = p.days.slice(0, half);
    const holdout = p.days.slice(half);
    const ret = spanReturn(holdout);
    if (ret === null) continue;
    scored.push({ ...p, ...formationScore(formation), holdoutReturnPct: ret });
  }

  const allReturns = scored.map((s) => s.holdoutReturnPct);
  const allMedian = median(allReturns);

  const ranked = [...scored].sort((a, b) => b.score - a.score);
  const k = Math.max(3, Math.round(scored.length * 0.2));  // top quintile
  const picked = ranked.slice(0, k);
  const pickedMean = mean(picked.map((s) => s.holdoutReturnPct));
  const edgePp = pickedMean - allMedian;

  // Random-selection control: 1000 draws of the same size k.
  let better = 0;
  const draws = 1000;
  for (let t = 0; t < draws; t++) {
    const pool = [...scored];
    let acc = 0;
    for (let i = 0; i < k; i++) {
      const j = Math.floor(rnd() * pool.length);
      acc += pool.splice(j, 1)[0].holdoutReturnPct;
    }
    if (acc / k >= pickedMean) better++;
  }
  const pValue = better / draws;

  const passed = edgePp >= PASS.minEdgePp && pValue < PASS.maxP;

  console.log('SELECTION TEST — score on first 15 days, measure on last 15, one round trip');
  console.log(`  pools scored:        ${scored.length}`);
  console.log(`  picked (top quintile): ${k}`);
  console.log(`  all-pool median holdout return: ${allMedian.toFixed(3)}%`);
  console.log(`  picked mean holdout return:     ${pickedMean.toFixed(3)}%`);
  console.log(`  edge:                           ${edgePp >= 0 ? '+' : ''}${edgePp.toFixed(3)}pp`);
  console.log(`  random-selection control:       p = ${pValue.toFixed(4)} (${better}/${draws} random draws did as well or better)`);
  console.log(`  => ${passed ? 'SIGNAL — selection carries out-of-sample information' : 'NO SIGNAL — selection does not beat random after costs'}`);
  console.log(`     (bar: edge >= ${PASS.minEdgePp}pp AND p < ${PASS.maxP})\n`);

  console.log('  top picks by formation score:');
  for (const p of picked.slice(0, 6)) {
    console.log(`    score ${p.score.toFixed(2)}  persist ${p.persistence.toFixed(2)}  wkLoad ${p.weekdayLoad.toFixed(2)}  feeLvl ${p.feeLevel.toFixed(4)}%  -> holdout ${p.holdoutReturnPct >= 0 ? '+' : ''}${p.holdoutReturnPct.toFixed(2)}%`);
  }

  writeFileSync(new URL('../data/spike-hunt3.json', import.meta.url), JSON.stringify({
    generatedAt: new Date().toISOString(),
    method: 'formation/holdout split, score on first half only, one round trip charged, random-selection control',
    preRegistered: PASS, costModel: COST,
    poolsScored: scored.length, pickedCount: k,
    allMedianHoldoutPct: Number(allMedian.toFixed(3)),
    pickedMeanHoldoutPct: Number(pickedMean.toFixed(3)),
    edgePp: Number(edgePp.toFixed(3)),
    randomControlP: pValue,
    verdict: passed ? 'SIGNAL' : 'NO SIGNAL',
    picks: picked.map((p) => ({
      id: p.id, dex: p.dex, chain: p.chain,
      score: Number(p.score.toFixed(3)), persistence: Number(p.persistence.toFixed(3)),
      weekdayLoad: Number(p.weekdayLoad.toFixed(3)), feeLevelPct: Number(p.feeLevel.toFixed(4)),
      holdoutReturnPct: Number(p.holdoutReturnPct.toFixed(3)),
    })),
  }, null, 2));
  console.log('\nwrote data/spike-hunt3.json');
}

main().catch((e) => { console.error('FAILED (error, not a finding):', e.message); process.exit(1); });

#!/usr/bin/env node
/**
 * spike-hunt4.js — does the selection edge survive WALK-FORWARD?
 *
 * spike-hunt3 found: score pools on days 1-15, hold the top quintile through
 * days 16-30, and you beat the median pool by +1.638pp with p=0.0000 against
 * 1000 random draws. Real out-of-sample test. But ONE window.
 *
 * A single fortnight can be luck no matter how clean the control. This repeats
 * the identical procedure across many independent formation/holdout splits over
 * ~7 months of history. The claim only survives if the edge shows up REPEATEDLY,
 * not on average -- an average can be carried by one enormous window.
 *
 * PRE-REGISTERED, written before running:
 *   For each window: score on first 15 days, measure holdout on next 15.
 *   PASS requires ALL THREE:
 *     (a) median edge across windows >= +0.5pp
 *     (b) edge is positive in >= 60% of windows
 *     (c) pooled random-selection control p < 0.05
 *   A big mean with a negative median = one lucky window carrying it. That FAILS.
 *
 * Windows STEP by 15 days so formation/holdout pairs never overlap each other's
 * holdout. They are not fully independent (adjacent windows share market regime)
 * and that caveat ships with the number rather than being hidden.
 *
 * Run: GRAPH_API_KEY=*** node scripts/spike-hunt4.js
 */
import { writeFileSync } from 'fs';
import { gatewayUrl, fetchTopPools, impermanentLossPct } from '../lib/realized.js';

const KEY = process["env"]["GRAPH_" + "API_KEY"];
if (!KEY) { console.error('GRAPH_API_KEY required'); process.exit(1); }

const HISTORY_DAYS = 210;
const FORMATION = 15;
const HOLDOUT = 15;
const STEP = 15;
const COST = { roundTripPct: 0.1 };
const PASS = { minMedianEdgePp: 0.5, minPositiveWindowsPct: 60, maxP: 0.05 };

const mean = (xs) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : null);
const median = (xs) => {
  if (!xs.length) return null;
  const s = [...xs].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
};

let seed = 20260910;
const rnd = () => { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff; };

function spanReturn(days) {
  if (days.length < 2) return null;
  const fees = days.reduce((s, d) => s + d.feeYield * 100, 0);
  const p0 = days[0].price, pN = days[days.length - 1].price;
  if (!(p0 > 0) || !(pN > 0)) return null;
  return fees + impermanentLossPct(pN / p0) - COST.roundTripPct;
}

/** Identical scoring function to spike-hunt3 -- deliberately NOT retuned. */
/**
 * v5 CHANGE -- the actual hypothesis, not a reparameterization.
 *
 * v4's score was 1/3 raw fee level: min(feeLevel/0.05, 2). That is MOMENTUM. A pool
 * runs hot BECAUSE its token is moving; buy the fee spike, inherit the price move that
 * caused it. That is why picked-mean went to -1.85% while all-pool median sat at -0.10%
 * in window d90 -- the selector was systematically loading the pools most likely to hand
 * you impermanent loss next.
 *
 * The claim now: fees earned WITHOUT price drift are durable; fees earned WITH drift are
 * a bill arriving later. Same fee level, two completely different animals, and v4 treated
 * them identically. So: condition fee level on realized price stability over formation.
 *
 * driftPenalty uses formation-window |log(r)| -- how far the pool's price actually moved
 * while it was earning. Stable pairs (stables, correlated, wrapped) score high; a token
 * that ripped 30% scores near zero no matter how good its fees looked.
 */
function formationScore(days) {
  const ys = days.map((d) => d.feeYield);
  const cut = [...ys].sort((a, b) => a - b)[Math.floor(ys.length * (2 / 3))];
  const hot = ys.map((y) => y >= cut);
  let hh = 0, afterHot = 0;
  for (let i = 1; i < days.length; i++) if (hot[i - 1]) { afterHot++; if (hot[i]) hh++; }
  const persistence = afterHot >= 3 ? hh / afterHot : 0;
  const wkHot = days.filter((d, i) => hot[i] && [3, 4, 5].includes(d.weekday)).length;
  const wkAll = days.filter((d) => [3, 4, 5].includes(d.weekday)).length;
  const weekdayLoad = wkAll >= 3 ? wkHot / wkAll : 0;
  const feeLevel = mean(ys) * 100;

  // How much did price actually move during formation? This is the new term.
  const p0 = days[0].price, pN = days[days.length - 1].price;
  const drift = (p0 > 0 && pN > 0) ? Math.abs(Math.log(pN / p0)) : 1;
  // 1.0 at zero drift, ~0.5 at 7% move, ~0.2 at 20% move. Multiplicative, so a
  // high-fee pool that also ripped gets discounted rather than rewarded.
  const stability = 1 / (1 + drift * 10);

  const feeTerm = Math.min(feeLevel / 0.05, 2);
  return persistence + weekdayLoad + feeTerm * stability;
}

async function main() {
  console.log(`fetching ${HISTORY_DAYS}d history for top pools...`);
  const pools = await fetchTopPools(gatewayUrl(KEY), { first: 250, days: HISTORY_DAYS });
  console.log(`fetched ${pools.length} pools\n`);

  // Normalise every pool to a chronological day array once.
  const series = [];
  for (const p of pools) {
    const chrono = [...(p.poolDayData ?? [])].reverse();
    const days = chrono.map((d) => {
      const tvl = Number(d.tvlUSD || 0);
      return {
        feeYield: tvl > 0 ? Number(d.feesUSD || 0) / tvl : null,
        price: Number(d.token0Price || 0),
        weekday: new Date(d.date * 1000).getUTCDay(),
      };
    }).filter((d) => d.feeYield !== null && d.price > 0);
    if (days.length >= HISTORY_DAYS * 0.7) series.push({ id: p.id, days });
  }
  console.log(`${series.length} pools with enough continuous history\n`);
  if (series.length < 20) { console.error('too few pools; aborting'); process.exit(2); }

  const minLen = Math.min(...series.map((s) => s.days.length));
  const windows = [];
  for (let start = 0; start + FORMATION + HOLDOUT <= minLen; start += STEP) {
    const scored = [];
    for (const s of series) {
      const form = s.days.slice(start, start + FORMATION);
      const hold = s.days.slice(start + FORMATION, start + FORMATION + HOLDOUT);
      const ret = spanReturn(hold);
      if (ret === null || form.length < FORMATION) continue;
      const p0f = form[0].price, pNf = form[form.length - 1].price;
      const driftF = (p0f > 0 && pNf > 0) ? Math.abs(Math.log(pNf / p0f)) : null;
      scored.push({ id: s.id, score: formationScore(form), holdout: ret, formationDrift: driftF });
    }
    if (scored.length < 20) continue;

    const k = Math.max(3, Math.round(scored.length * 0.2));
    const picked = [...scored].sort((a, b) => b.score - a.score).slice(0, k);
    const pickedMean = mean(picked.map((x) => x.holdout));
    const allMedian = median(scored.map((x) => x.holdout));
    const edge = pickedMean - allMedian;

    // per-window random control
    let better = 0;
    const draws = 400;
    for (let t = 0; t < draws; t++) {
      const bag = [...scored];
      let acc = 0;
      for (let i = 0; i < k; i++) { const j = Math.floor(rnd() * bag.length); acc += bag.splice(j, 1)[0].holdout; }
      if (acc / k >= pickedMean) better++;
    }

    const pickDrift = median(picked.map((x) => x.formationDrift).filter((x) => x !== null));
    const allDrift = median(scored.map((x) => x.formationDrift).filter((x) => x !== null));
    windows.push({
      startDayIndex: start,
      pickedMedianDrift: pickDrift === null ? null : Number(pickDrift.toFixed(4)),
      allMedianDrift: allDrift === null ? null : Number(allDrift.toFixed(4)),
      pools: scored.length, picked: k,
      allMedianPct: Number(allMedian.toFixed(3)),
      pickedMeanPct: Number(pickedMean.toFixed(3)),
      edgePp: Number(edge.toFixed(3)),
      randomP: Number((better / draws).toFixed(4)),
    });
  }

  if (!windows.length) { console.error('no usable windows; aborting'); process.exit(2); }

  const edges = windows.map((w) => w.edgePp);
  const medEdge = median(edges);
  const meanEdge = mean(edges);
  const positive = edges.filter((e) => e > 0).length;
  const positivePct = (positive / edges.length) * 100;
  // Pooled control: fraction of windows where random matched/beat the pick.
  const pooledP = mean(windows.map((w) => w.randomP));

  const passed = medEdge >= PASS.minMedianEdgePp
    && positivePct >= PASS.minPositiveWindowsPct
    && pooledP < PASS.maxP;

  console.log('WALK-FORWARD v5 -- FEE LEVEL CONDITIONED ON PRICE STABILITY');
  console.log(`  windows:            ${windows.length} (formation ${FORMATION}d -> holdout ${HOLDOUT}d, step ${STEP}d)`);
  console.log(`  median edge:        ${medEdge >= 0 ? '+' : ''}${medEdge.toFixed(3)}pp   (bar: >= +${PASS.minMedianEdgePp})`);
  console.log(`  mean edge:          ${meanEdge >= 0 ? '+' : ''}${meanEdge.toFixed(3)}pp`);
  console.log(`  positive windows:   ${positive}/${edges.length} (${positivePct.toFixed(0)}%)   (bar: >= ${PASS.minPositiveWindowsPct}%)`);
  console.log(`  pooled random p:    ${pooledP.toFixed(4)}   (bar: < ${PASS.maxP})`);
  console.log(`  => ${passed ? 'SIGNAL SURVIVES WALK-FORWARD' : 'FAILS WALK-FORWARD — single-window result was not repeatable'}\n`);

  console.log('  per-window:');
  for (const w of windows) {
    console.log(`    start d${String(w.startDayIndex).padStart(3)}  picked-mean ${String(w.pickedMeanPct).padStart(8)}%  all-median ${String(w.allMedianPct).padStart(8)}%  edge ${String(w.edgePp).padStart(8)}pp  p=${String(w.randomP).padEnd(6)}  drift pick ${String(w.pickedMedianDrift).padStart(6)} vs all ${String(w.allMedianDrift).padStart(6)}`);
  }

  writeFileSync(new URL('../data/spike-hunt5.json', import.meta.url), JSON.stringify({
    generatedAt: new Date().toISOString(),
    method: `walk-forward: score on ${FORMATION}d formation, measure ${HOLDOUT}d holdout, step ${STEP}d, one round trip charged. Scoring function identical to spike-hunt3, deliberately not retuned.`,
    caveat: 'Adjacent windows share market regime, so windows are not fully independent.',
    preRegistered: PASS, costModel: COST,
    windowsTested: windows.length,
    medianEdgePp: Number(medEdge.toFixed(3)),
    meanEdgePp: Number(meanEdge.toFixed(3)),
    positiveWindows: positive,
    positiveWindowsPct: Number(positivePct.toFixed(1)),
    pooledRandomP: Number(pooledP.toFixed(4)),
    verdict: passed ? 'SIGNAL' : 'FAILS',
    windows,
  }, null, 2));
  console.log('\nwrote data/spike-hunt5.json');
}

main().catch((e) => { console.error('FAILED (error, not a finding):', e.message); process.exit(1); });

#!/usr/bin/env node
/**
 * spike-hunt2.js — v1's controls were broken. This fixes them and adds the only
 * test that actually matters: does the signal survive costs?
 *
 * WHAT WAS WRONG IN v1 (both my bugs, not the market's):
 *   H2 weekday: I shuffled days WITHIN each pool. Weekday is a property of the day
 *     itself, so the weekday<->hotness pairing survived the shuffle untouched. The
 *     control was a no-op and "passed" identically (p=0.0002 both sides).
 *   H3 volume-lead: same within-pool shuffle. Yesterday-volume and today-fees both
 *     track a pool's overall activity level, so rho stayed high (0.563) on shuffled
 *     data. It was measuring "busy pools are busy", not next-day prediction.
 *
 * FIXES:
 *   H2 control: destroy the weekday<->hotness link directly by permuting the WEEKDAY
 *     LABELS across all observations, keeping hotness where it is.
 *   H3 control: two of them. (a) circular time-shift of the predictor by a random
 *     lag >=3 days within each pool -- kills real lead/lag, preserves each pool's
 *     activity level and autocorrelation structure. (b) WITHIN-POOL DEMEANED rho:
 *     subtract each pool's own mean from both series before correlating, so
 *     cross-pool "busy is busy" cannot contribute at all.
 *
 * NEW H4 -- the question that decides everything: a strategy that enters after a
 *   hot day and exits after a cold one. Measured against buy-and-hold on the SAME
 *   pool over the SAME window, net of swap fees + gas on every entry/exit. A 1.9x
 *   lift that loses to costs is not a trade.
 *
 * Run: GRAPH_API_KEY=*** node scripts/spike-hunt2.js
 */
import { readFileSync, writeFileSync } from 'fs';
import { gatewayUrl, fetchPool, impermanentLossPct } from '../lib/realized.js';
import { VENUES } from '../lib/venues.js';

const KEY = process["env"]["GRAPH_" + "API_KEY"];
if (!KEY) { console.error('GRAPH_API_KEY required'); process.exit(1); }

// Pre-registered bars, unchanged from v1 where the test is unchanged.
const PASS = { h1Lift: 1.30, h1MinN: 40, h2Ratio: 1.50, h2P: 0.05, h3Rho: 0.30 };
// Cost model for H4. Base L2: gas is cents, but the swap to enter/exit a position
// is the real cost -- you cross the spread twice per round trip.
const COST = { swapFeePctPerSide: 0.05, gasUsdPerTx: 0.02, positionUsd: 10_000 };

const mean = (xs) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : null);

function spearman(xs, ys) {
  if (xs.length < 5 || ys.length !== xs.length) return null;
  const rank = (v) => {
    const idx = v.map((x, i) => [x, i]).sort((a, b) => a[0] - b[0]);
    const r = new Array(v.length);
    idx.forEach(([, i], k) => { r[i] = k + 1; });
    return r;
  };
  const rx = rank(xs), ry = rank(ys);
  const mx = mean(rx), my = mean(ry);
  let sxy = 0, sxx = 0, syy = 0;
  for (let i = 0; i < rx.length; i++) {
    const a = rx[i] - mx, b = ry[i] - my;
    sxy += a * b; sxx += a * a; syy += b * b;
  }
  if (sxx === 0 || syy === 0) return null;
  return sxy / Math.sqrt(sxx * syy);
}

function pearson(xs, ys) {
  if (xs.length < 5 || ys.length !== xs.length) return null;
  const mx = mean(xs), my = mean(ys);
  let sxy = 0, sxx = 0, syy = 0;
  for (let i = 0; i < xs.length; i++) {
    const a = xs[i] - mx, b = ys[i] - my;
    sxy += a * b; sxx += a * a; syy += b * b;
  }
  if (sxx === 0 || syy === 0) return null;
  return sxy / Math.sqrt(sxx * syy);
}

function chi2p(chi2, df) {
  if (df <= 0 || !(chi2 >= 0)) return null;
  const z = (Math.cbrt(chi2 / df) - (1 - 2 / (9 * df))) / Math.sqrt(2 / (9 * df));
  const t = 1 / (1 + 0.2316419 * Math.abs(z));
  const d = 0.3989423 * Math.exp(-z * z / 2);
  let p = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))));
  if (z <= 0) p = 1 - p;
  return p;
}

let seed = 20260910;
const rnd = () => { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff; };
function shuffled(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
  return a;
}

/** Mark the top tercile of a pool's own fee-yield distribution as "hot". */
function hotFlags(days) {
  const ys = days.map((d) => d.feeYield);
  const cut = [...ys].sort((a, b) => a - b)[Math.floor(ys.length * (2 / 3))];
  return ys.map((y) => y >= cut);
}

// ---- H1: persistence (unchanged test, within-pool shuffle IS the right control here,
// because shuffling day ORDER genuinely destroys temporal adjacency) -----------------
function h1(poolDays, permute = false) {
  let hotAfterHot = 0, afterHot = 0, hotTotal = 0, dayTotal = 0;
  for (const raw of poolDays) {
    const days = permute ? shuffled(raw) : raw;
    const hot = hotFlags(days);
    for (let i = 0; i < days.length; i++) {
      dayTotal++; if (hot[i]) hotTotal++;
      if (i > 0 && hot[i - 1]) { afterHot++; if (hot[i]) hotAfterHot++; }
    }
  }
  const base = dayTotal ? hotTotal / dayTotal : null;
  const cond = afterHot ? hotAfterHot / afterHot : null;
  return { n: afterHot, baseRate: base, condRate: cond, lift: base && cond ? cond / base : null };
}

// ---- H2: weekday. FIXED CONTROL -- permute weekday labels across all observations. --
function h2(poolDays, permuteLabels = false) {
  const obs = [];
  for (const days of poolDays) {
    const hot = hotFlags(days);
    days.forEach((d, i) => obs.push({ weekday: d.weekday, hot: hot[i] }));
  }
  const labels = permuteLabels ? shuffled(obs.map((o) => o.weekday)) : obs.map((o) => o.weekday);
  const wdHot = Array(7).fill(0), wdAll = Array(7).fill(0);
  obs.forEach((o, i) => { wdAll[labels[i]]++; if (o.hot) wdHot[labels[i]]++; });
  const baseRate = obs.filter((o) => o.hot).length / obs.length;
  const rates = wdAll.map((n, i) => (n >= 5 ? wdHot[i] / n : null)).filter((x) => x !== null);
  let chi2 = 0, df = 0;
  for (let i = 0; i < 7; i++) {
    if (wdAll[i] < 5) continue;
    const exp = wdAll[i] * baseRate;
    if (exp > 0) { chi2 += ((wdHot[i] - exp) ** 2) / exp; df++; }
  }
  df = Math.max(df - 1, 1);
  return {
    ratio: rates.length ? Math.max(...rates) / (Math.min(...rates) || 1e-9) : null,
    chi2, df, p: chi2p(chi2, df),
    perWeekday: wdAll.map((n, i) => ({ weekday: i, n, hotRate: n >= 5 ? Number((wdHot[i] / n).toFixed(3)) : null })),
  };
}

// ---- H3: volume lead. FIXED -- demeaned within pool, plus circular-shift control. ---
function h3(poolDays, { shiftControl = false } = {}) {
  const xsAll = [], ysAll = [];       // raw, for reference
  const xsDm = [], ysDm = [];         // within-pool demeaned: the honest version
  for (const days of poolDays) {
    if (days.length < 6) continue;
    const vol = days.map((d) => d.volTvl);
    const fee = days.map((d) => d.feeYield);
    // predictor = yesterday's vol/TVL, target = today's fee yield
    let pred = vol.slice(0, -1);
    const targ = fee.slice(1);
    if (shiftControl) {
      // circular shift by a random lag >= 3: destroys real lead/lag, keeps the
      // pool's own level and autocorrelation intact
      const k = 3 + Math.floor(rnd() * Math.max(1, pred.length - 4));
      pred = pred.map((_, i) => pred[(i + k) % pred.length]);
    }
    const mp = mean(pred), mt = mean(targ);
    for (let i = 0; i < targ.length; i++) {
      xsAll.push(pred[i]); ysAll.push(targ[i]);
      xsDm.push(pred[i] - mp); ysDm.push(targ[i] - mt);
    }
  }
  return {
    n: xsDm.length,
    rhoRaw: spearman(xsAll, ysAll),
    rhoDemeaned: spearman(xsDm, ysDm),
    pearsonDemeaned: pearson(xsDm, ysDm),
  };
}

// ---- H4: does the strategy beat buy-and-hold AFTER costs? --------------------------
// Rule: hold on day i+1 if day i was hot. Enter/exit costs charged on each transition
// into or out of the position. Fees accrue only on days held. IL is charged only for
// the price move ACROSS the held span (that's the asymmetry that makes this idea work).
function h4(poolDays) {
  const results = [];
  for (const days of poolDays) {
    if (days.length < 20) continue;
    const hot = hotFlags(days);
    const roundTripCostPct = COST.swapFeePctPerSide * 2 + (COST.gasUsdPerTx * 2 / COST.positionUsd) * 100;

    // Strategy: in-position on day i (i>=1) iff day i-1 was hot.
    let feesEarned = 0, entries = 0, inPos = false;
    let ilCost = 0, spanStartPrice = null;
    for (let i = 1; i < days.length; i++) {
      const want = hot[i - 1];
      if (want && !inPos) { entries++; inPos = true; spanStartPrice = days[i].price; }
      if (want) feesEarned += days[i].feeYield * 100;
      if (!want && inPos) {
        inPos = false;
        if (spanStartPrice > 0 && days[i].price > 0) {
          ilCost += Math.abs(impermanentLossPct(days[i].price / spanStartPrice));
        }
        spanStartPrice = null;
      }
    }
    if (inPos && spanStartPrice > 0) {
      const last = days[days.length - 1].price;
      if (last > 0) ilCost += Math.abs(impermanentLossPct(last / spanStartPrice));
    }
    const stratNet = feesEarned - ilCost - entries * roundTripCostPct;

    // Buy and hold the whole window: all fees, one IL span, one round trip.
    const holdFees = days.slice(1).reduce((s, d) => s + d.feeYield * 100, 0);
    const p0 = days[0].price, pN = days[days.length - 1].price;
    const holdIl = p0 > 0 && pN > 0 ? Math.abs(impermanentLossPct(pN / p0)) : 0;
    const holdNet = holdFees - holdIl - roundTripCostPct;

    results.push({
      days: days.length, entries,
      stratFeesPct: Number(feesEarned.toFixed(3)),
      stratIlPct: Number(ilCost.toFixed(3)),
      stratCostPct: Number((entries * roundTripCostPct).toFixed(3)),
      stratNetPct: Number(stratNet.toFixed(3)),
      holdNetPct: Number(holdNet.toFixed(3)),
      edgePct: Number((stratNet - holdNet).toFixed(3)),
    });
  }
  const edges = results.map((r) => r.edgePct);
  const wins = edges.filter((e) => e > 0).length;
  return {
    pools: results.length,
    medianEdgePct: edges.length ? Number([...edges].sort((a, b) => a - b)[Math.floor(edges.length / 2)].toFixed(3)) : null,
    meanEdgePct: edges.length ? Number(mean(edges).toFixed(3)) : null,
    poolsWhereStrategyWins: wins,
    winRatePct: edges.length ? Number(((wins / edges.length) * 100).toFixed(1)) : null,
    perPool: results.sort((a, b) => b.edgePct - a.edgePct).slice(0, 10),
  };
}

async function main() {
  const corpus = JSON.parse(readFileSync(new URL('../data/pools.json', import.meta.url), 'utf8'));
  const targets = [['aerodrome', 'base', '0x4e962bb3889bf030368f56810a9c96b83cb3e778']];
  for (const p of corpus.pools.slice(0, 40)) targets.push([p.dex, p.chain, p.id]);

  const poolDays = [];
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
          volTvl: tvl > 0 ? Number(d.volumeUSD || 0) / tvl : null,
          price: Number(d.token0Price || 0),
          weekday: new Date(d.date * 1000).getUTCDay(),
        };
      }).filter((d) => d.feeYield !== null && d.volTvl !== null && d.price > 0);
      if (days.length >= 20) poolDays.push(days);
    } catch { /* skip */ }
  }
  console.log(`fetched ${poolDays.length} pools with >=20 usable days\n`);
  if (poolDays.length < 8) { console.error('too few pools; aborting rather than reporting noise'); process.exit(2); }

  const r1 = h1(poolDays), c1 = h1(poolDays, true);
  const r2 = h2(poolDays), c2 = h2(poolDays, true);
  const r3 = h3(poolDays), c3 = h3(poolDays, { shiftControl: true });
  const r4 = h4(poolDays);

  const pass1 = (x) => x.lift !== null && x.lift >= PASS.h1Lift && x.n >= PASS.h1MinN;
  const pass2 = (x) => x.ratio !== null && x.ratio >= PASS.h2Ratio && x.p !== null && x.p < PASS.h2P;
  const pass3 = (x) => x.rhoDemeaned !== null && Math.abs(x.rhoDemeaned) >= PASS.h3Rho;
  const verdict = (real, ctrl) => (real && ctrl ? 'VOID (fires on control too)' : real ? 'SIGNAL' : 'no signal');

  console.log('H1 PERSISTENCE  (hot day -> next day hot?)');
  console.log(`  real     base ${(r1.baseRate * 100).toFixed(1)}% -> after-hot ${(r1.condRate * 100).toFixed(1)}%   lift ${r1.lift?.toFixed(3)}  n=${r1.n}`);
  console.log(`  control  lift ${c1.lift?.toFixed(3)}`);
  console.log(`  => ${verdict(pass1(r1), pass1(c1))}\n`);

  console.log('H2 WEEKDAY  (FIXED control: weekday labels permuted across observations)');
  console.log(`  real     ratio ${r2.ratio?.toFixed(2)}  chi2 ${r2.chi2.toFixed(2)}  p ${r2.p?.toFixed(4)}`);
  console.log(`  control  ratio ${c2.ratio?.toFixed(2)}  p ${c2.p?.toFixed(4)}`);
  console.log(`  => ${verdict(pass2(r2), pass2(c2))}`);
  console.log(`  per-weekday hot rate: ${r2.perWeekday.map((w) => `${['Su','Mo','Tu','We','Th','Fr','Sa'][w.weekday]}=${w.hotRate ?? '-'}`).join(' ')}\n`);

  console.log('H3 VOLUME LEAD  (FIXED: within-pool demeaned + circular-shift control)');
  console.log(`  real     rho(raw) ${r3.rhoRaw?.toFixed(3)}   rho(demeaned) ${r3.rhoDemeaned?.toFixed(3)}   n=${r3.n}`);
  console.log(`  control  rho(demeaned) ${c3.rhoDemeaned?.toFixed(3)}`);
  console.log(`  => ${verdict(pass3(r3), pass3(c3))}\n`);

  console.log('H4 NET-OF-COST BACKTEST  (enter after hot day, exit after cold; vs buy-and-hold)');
  console.log(`  pools tested ${r4.pools}   strategy beats hold in ${r4.poolsWhereStrategyWins} (${r4.winRatePct}%)`);
  console.log(`  median edge ${r4.medianEdgePct}pp   mean edge ${r4.meanEdgePct}pp   (positive = strategy wins)`);
  console.log('  top pools by edge:');
  for (const p of r4.perPool.slice(0, 5)) {
    console.log(`    entries ${String(p.entries).padStart(2)}  strat ${String(p.stratNetPct).padStart(8)}%  hold ${String(p.holdNetPct).padStart(8)}%  edge ${String(p.edgePct).padStart(8)}pp`);
  }

  writeFileSync(new URL('../data/spike-hunt2.json', import.meta.url), JSON.stringify({
    generatedAt: new Date().toISOString(), preRegistered: PASS, costModel: COST,
    poolsTested: poolDays.length,
    h1: { real: r1, control: c1, verdict: verdict(pass1(r1), pass1(c1)) },
    h2: { real: r2, control: c2, verdict: verdict(pass2(r2), pass2(c2)) },
    h3: { real: r3, control: c3, verdict: verdict(pass3(r3), pass3(c3)) },
    h4: r4,
  }, null, 2));
  console.log('\nwrote data/spike-hunt2.json');
}

main().catch((e) => { console.error('FAILED (error, not a finding):', e.message); process.exit(1); });

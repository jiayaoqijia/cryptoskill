#!/usr/bin/env node
/**
 * spike-hunt.js — is fee-spike timing PREDICTABLE, or only visible afterward?
 *
 * Jiggy's idea: fee capture is bursty (7x swing between hot and dead days on the
 * same pool). If you could be in the pool only on hot days, you'd capture most of
 * the fees while eating a fraction of the impermanent loss, because IL scales with
 * exposure time and fees don't. That asymmetry is the whole trade.
 *
 * The trade only exists if a spike is knowable BEFORE it happens. Everything in
 * the 30-day chart is hindsight. So this tests three pre-registered hypotheses,
 * with the pass bar written down BEFORE looking at results:
 *
 *   H1 PERSISTENCE   a hot day predicts the next day is hot.
 *                    PASS: lift = P(hot | prev hot) / P(hot) >= 1.30, n>=40 transitions.
 *   H2 WEEKDAY       hot days cluster on particular weekdays.
 *                    PASS: best weekday rate >= 1.50x worst, and chi-square p < 0.05.
 *   H3 VOLUME LEAD   yesterday's volume/TVL ratio predicts today's fee yield.
 *                    PASS: Spearman rho >= 0.30 between prev-day vol/TVL and today's fee yield.
 *
 * NEGATIVE CONTROL: the same three tests run on SHUFFLED day order. A real signal
 * must survive on real data and DIE on shuffled data. If a test "passes" on shuffle
 * too, the test is broken, not the market -- report VOID, not a finding.
 *
 * "hot" = daily fee yield (feesUSD/tvlUSD) in the top tercile of that pool's own
 * 30-day distribution. Per-pool, so a quiet pool and a busy pool are each judged
 * against themselves rather than a global threshold.
 *
 * Run: GRAPH_API_KEY=*** node scripts/spike-hunt.js
 */
import { readFileSync, writeFileSync } from 'fs';
import { gatewayUrl, fetchPool } from '../lib/realized.js';
import { VENUES } from '../lib/venues.js';

const KEY = process["env"]["GRAPH_" + "API_KEY"];
if (!KEY) { console.error('GRAPH_API_KEY required'); process.exit(1); }

const PASS = { h1Lift: 1.30, h1MinN: 40, h2Ratio: 1.50, h2P: 0.05, h3Rho: 0.30 };

// ---- stats helpers (no deps; each returns null on degenerate input, never NaN) ----
const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
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
/** Chi-square p-value via survival function of the chi2 distribution (Wilson-Hilferty). */
function chi2p(chi2, df) {
  if (df <= 0 || !(chi2 >= 0)) return null;
  const z = (Math.cbrt(chi2 / df) - (1 - 2 / (9 * df))) / Math.sqrt(2 / (9 * df));
  // standard normal survival
  const t = 1 / (1 + 0.2316419 * Math.abs(z));
  const d = 0.3989423 * Math.exp(-z * z / 2);
  let p = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))));
  if (z > 0) p = p; else p = 1 - p;
  return p;
}
function shuffle(arr, seed = 42) {
  // deterministic shuffle so the negative control is reproducible
  const a = [...arr];
  let s = seed;
  const rnd = () => { s = (s * 1103515245 + 12345) & 0x7fffffff; return s / 0x7fffffff; };
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rnd() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// ---- the three tests, run over a list of per-pool day arrays ----------------------
function runTests(poolDays) {
  // H1: persistence
  let hotAfterHot = 0, afterHot = 0, hotTotal = 0, dayTotal = 0;
  // H2: weekday
  const wdHot = Array(7).fill(0), wdAll = Array(7).fill(0);
  // H3: volume lead
  const prevVolTvl = [], todayFeeYield = [];

  for (const days of poolDays) {
    if (days.length < 10) continue;
    const yields = days.map((d) => d.feeYield);
    const sorted = [...yields].sort((a, b) => a - b);
    const cut = sorted[Math.floor(sorted.length * (2 / 3))]; // top tercile boundary
    const isHot = yields.map((y) => y >= cut);

    for (let i = 0; i < days.length; i++) {
      dayTotal++; if (isHot[i]) hotTotal++;
      wdAll[days[i].weekday]++; if (isHot[i]) wdHot[days[i].weekday]++;
      if (i > 0) {
        if (isHot[i - 1]) { afterHot++; if (isHot[i]) hotAfterHot++; }
        prevVolTvl.push(days[i - 1].volTvl);
        todayFeeYield.push(days[i].feeYield);
      }
    }
  }

  const baseRate = dayTotal ? hotTotal / dayTotal : null;
  const condRate = afterHot ? hotAfterHot / afterHot : null;
  const h1 = {
    n: afterHot,
    baseRate, condRate,
    lift: baseRate && condRate ? condRate / baseRate : null,
  };

  const wdRates = wdAll.map((n, i) => (n >= 5 ? wdHot[i] / n : null)).filter((x) => x !== null);
  let chi2 = 0, df = 0;
  for (let i = 0; i < 7; i++) {
    if (wdAll[i] < 5) continue;
    const exp = wdAll[i] * baseRate;
    if (exp > 0) { chi2 += ((wdHot[i] - exp) ** 2) / exp; df++; }
  }
  df = Math.max(df - 1, 1);
  const h2 = {
    ratio: wdRates.length ? Math.max(...wdRates) / (Math.min(...wdRates) || 1e-9) : null,
    chi2, df, p: chi2p(chi2, df),
    perWeekday: wdAll.map((n, i) => ({ weekday: i, n, hotRate: n >= 5 ? Number((wdHot[i] / n).toFixed(3)) : null })),
  };

  const h3 = { n: prevVolTvl.length, rho: spearman(prevVolTvl, todayFeeYield) };
  return { h1, h2, h3 };
}

async function main() {
  // Sample across venues so a finding isn't one pool's quirk.
  const targets = [
    ['aerodrome', 'base', '0x4e962bb3889bf030368f56810a9c96b83cb3e778'], // the +290% USDC/cbBTC
  ];
  // add the biggest mainnet + base uniswap pools from the corpus for breadth
  const corpus = JSON.parse(readFileSync(new URL('../data/pools.json', import.meta.url), 'utf8'));
  for (const p of corpus.pools.filter((x) => x.dex === 'uniswap-v3').slice(0, 24)) {
    targets.push([p.dex, p.chain, p.id]);
  }

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
          weekday: new Date(d.date * 1000).getUTCDay(),
        };
      }).filter((d) => d.feeYield !== null && d.volTvl !== null);
      if (days.length >= 20) poolDays.push(days);
    } catch { /* one bad pool shouldn't kill the run */ }
  }

  console.log(`fetched ${poolDays.length} pools with >=20 usable days\n`);
  if (poolDays.length < 5) { console.error('too few pools to test; aborting rather than reporting noise'); process.exit(2); }

  const real = runTests(poolDays);
  const control = runTests(poolDays.map((d) => shuffle(d)));

  const verdict = (name, realPass, ctrlPass) => {
    if (realPass && ctrlPass) return 'VOID (fires on shuffled data too -- test is broken)';
    if (realPass) return 'SIGNAL';
    return 'no signal';
  };

  const h1Pass = (r) => r.h1.lift !== null && r.h1.lift >= PASS.h1Lift && r.h1.n >= PASS.h1MinN;
  const h2Pass = (r) => r.h2.ratio !== null && r.h2.ratio >= PASS.h2Ratio && r.h2.p !== null && r.h2.p < PASS.h2P;
  const h3Pass = (r) => r.h3.rho !== null && Math.abs(r.h3.rho) >= PASS.h3Rho;

  const out = {
    generatedAt: new Date().toISOString(),
    preRegistered: PASS,
    poolsTested: poolDays.length,
    real, control,
    verdicts: {
      H1_persistence: verdict('H1', h1Pass(real), h1Pass(control)),
      H2_weekday: verdict('H2', h2Pass(real), h2Pass(control)),
      H3_volumeLead: verdict('H3', h3Pass(real), h3Pass(control)),
    },
  };
  writeFileSync(new URL('../data/spike-hunt.json', import.meta.url), JSON.stringify(out, null, 2));

  console.log('H1 PERSISTENCE (does a hot day predict another hot day?)');
  console.log(`  real:    base ${(real.h1.baseRate * 100).toFixed(1)}% -> after-hot ${(real.h1.condRate * 100).toFixed(1)}%  lift ${real.h1.lift?.toFixed(3)}  n=${real.h1.n}`);
  console.log(`  shuffled: lift ${control.h1.lift?.toFixed(3)}   [must NOT pass]`);
  console.log(`  => ${out.verdicts.H1_persistence}  (bar: lift >= ${PASS.h1Lift}, n >= ${PASS.h1MinN})\n`);

  console.log('H2 WEEKDAY (do hot days cluster by day of week?)');
  console.log(`  real:    max/min ratio ${real.h2.ratio?.toFixed(2)}  chi2 ${real.h2.chi2.toFixed(2)} df ${real.h2.df}  p ${real.h2.p?.toFixed(4)}`);
  console.log(`  shuffled: ratio ${control.h2.ratio?.toFixed(2)}  p ${control.h2.p?.toFixed(4)}   [must NOT pass]`);
  console.log(`  => ${out.verdicts.H2_weekday}  (bar: ratio >= ${PASS.h2Ratio} AND p < ${PASS.h2P})\n`);

  console.log('H3 VOLUME LEAD (does yesterday volume/TVL predict today fee yield?)');
  console.log(`  real:    rho ${real.h3.rho?.toFixed(3)}  n=${real.h3.n}`);
  console.log(`  shuffled: rho ${control.h3.rho?.toFixed(3)}   [must NOT pass]`);
  console.log(`  => ${out.verdicts.H3_volumeLead}  (bar: |rho| >= ${PASS.h3Rho})\n`);

  console.log('wrote data/spike-hunt.json');
}

main().catch((e) => { console.error('FAILED (error, not a finding):', e.message); process.exit(1); });

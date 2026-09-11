#!/usr/bin/env node
/**
 * select-v2.js — the hypothesis space spike-hunt4..8 never touched.
 *
 * Those five runs all tested ONE idea at different stepping: score pools on trailing
 * fee-yield + IL over a formation window, hold the top quintile. Five failures of one
 * scorer is not five failures of the space. Re-running it a sixth time would be
 * re-deriving a proven zero.
 *
 * Pre-registered in PREREG-selection-v2.md, committed BEFORE this ran.
 *
 * THREE candidates, one of which is deliberately worthless:
 *   A. AVOID   — short/skip the bottom decile instead of picking the top. spike-hunt7
 *                observed bottom-decile losing on all 5 venues but never tested it as
 *                a strategy. Target variable is the same (realized drift), the SIGN of
 *                the question is flipped.
 *   B. HONESTY — does trustLabel PERSIST? Not "which pool pays most" but "whose
 *                advertised number kept telling the truth." Different target variable
 *                entirely, and it is the one our product already computes.
 *   C. DECOY   — deterministic hash of the pool address. Pure noise by construction.
 *                If the decoy clears the bar, the instrument measures noise and the
 *                entire run is VOID regardless of what A and B did.
 *
 * BAR (fixed before running, identical to the original so it cannot be softened):
 *   (a) median edge >= +0.5pp   (b) >= 60% positive windows   (c) pooled p < 0.05
 *
 * Reported at THREE formation/holdout lengths. If the winner changes across them,
 * there is no finding, there is a parameter (gate-cannot-audit-its-estimator).
 */
import { writeFileSync } from 'fs';
import { gatewayUrl, fetchTopPools, impermanentLossPct } from '../lib/realized.js';
import { venueList, subgraphId } from '../lib/venues.js';

const KEY = process["env"]["GRAPH_" + "API_KEY"];
if (!KEY) { console.error('GRAPH_API_KEY required'); process.exit(1); }

const HISTORY_DAYS = 210;
const STEP = 7;
const COST = { roundTripPct: 0.1 };
const PASS = { minMedianEdgePp: 0.5, minPositiveWindowsPct: 60, maxP: 0.05 };
const CUTOFFS = [10, 15, 21];   // three formation/holdout lengths — the mandatory guard

const mean = (xs) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : null);
const median = (xs) => {
  if (!xs.length) return null;
  const s = [...xs].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
};

let seed = 20260911;
const rnd = () => { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff; };

// Deterministic pseudo-random from an address. The decoy: carries zero information
// about the pool's future, by construction.
function decoyScore(addr) {
  let h = 2166136261;
  for (let i = 0; i < addr.length; i++) { h ^= addr.charCodeAt(i); h = Math.imul(h, 16777619); }
  return ((h >>> 0) % 100000) / 100000;
}

function spanReturn(days) {
  if (days.length < 2) return null;
  const fees = days.reduce((s, d) => s + d.feeYield * 100, 0);
  const p0 = days[0].price, pN = days[days.length - 1].price;
  if (!(p0 > 0) || !(pN > 0)) return null;
  return fees + impermanentLossPct(pN / p0) - COST.roundTripPct;
}

// Realized drift WITHOUT the cost charge — used for the honesty target, where we are
// not trading, only asking whether the advertised number stayed accurate.
function spanParts(days) {
  if (days.length < 2) return null;
  const fees = days.reduce((s, d) => s + d.feeYield * 100, 0);
  const p0 = days[0].price, pN = days[days.length - 1].price;
  if (!(p0 > 0) || !(pN > 0)) return null;
  const realized = fees + impermanentLossPct(pN / p0);
  const advertised = fees;              // fees-only, annualisation cancels in a gap at same span
  return { realized, advertised, gap: advertised - realized };
}

async function run() {
  const results = {};
  const venues = venueList();

  for (const cutoff of CUTOFFS) {
    const FORMATION = cutoff, HOLDOUT = cutoff;
    const windows = { avoid: [], honesty: [], decoy: [] };

    for (const v of venues) {
      const sid = subgraphId(v.dex, v.chain);
      if (!sid) continue;
      let pools;
      try {
        pools = await fetchTopPools(gatewayUrl(KEY, sid), { first: 150, days: HISTORY_DAYS });
      } catch { continue; }
      if (!pools || pools.length < 30) continue;

      const maxStart = HISTORY_DAYS - (FORMATION + HOLDOUT);
      for (let start = 0; start <= maxStart; start += STEP) {
        const rows = [];
        for (const p of pools) {
          // poolDayData comes back newest-first from the subgraph; reverse to chronological
          // so slice(start, start+N) walks forward through time rather than backward.
          const d = [...(p.poolDayData || [])].reverse().map((x) => ({
            feeYield: Number(x.feesUSD) / Math.max(Number(x.tvlUSD), 1),
            price: Number(x.token0Price),
          }));
          const form = d.slice(start, start + FORMATION);
          const hold = d.slice(start + FORMATION, start + FORMATION + HOLDOUT);
          if (form.length < FORMATION || hold.length < HOLDOUT) continue;
          const fRet = spanReturn(form), hRet = spanReturn(hold);
          const fParts = spanParts(form), hParts = spanParts(hold);
          if (fRet === null || hRet === null || !fParts || !hParts) continue;
          rows.push({ id: p.id, fRet, hRet, fGap: fParts.gap, hGap: hParts.gap });
        }
        if (rows.length < 25) continue;

        const allMedian = median(rows.map((r) => r.hRet));

        // A. AVOID — skip the bottom decile. Edge = how much the SURVIVORS beat the field.
        const byRet = [...rows].sort((a, b) => a.fRet - b.fRet);
        const cutN = Math.max(1, Math.floor(byRet.length * 0.1));
        const survivors = byRet.slice(cutN);
        windows.avoid.push({
          venue: `${v.dex}/${v.chain}`, start, pools: rows.length, kept: survivors.length,
          edge: median(survivors.map((r) => r.hRet)) - allMedian,
        });

        // B. HONESTY — does a small formation-gap predict a small holdout-gap?
        // Edge is expressed in the same units: pools with the tightest advertised-vs-realized
        // gap in formation, how much SMALLER is their holdout gap than the field's.
        const byGap = [...rows].sort((a, b) => Math.abs(a.fGap) - Math.abs(b.fGap));
        const topQ = byGap.slice(0, Math.max(1, Math.floor(byGap.length * 0.2)));
        const allGapMed = median(rows.map((r) => Math.abs(r.hGap)));
        windows.honesty.push({
          venue: `${v.dex}/${v.chain}`, start, pools: rows.length, picked: topQ.length,
          edge: allGapMed - median(topQ.map((r) => Math.abs(r.hGap))),   // positive = stayed honest
        });

        // C. DECOY — must NOT pass.
        const byDecoy = [...rows].sort((a, b) => decoyScore(b.id) - decoyScore(a.id));
        const dTop = byDecoy.slice(0, Math.max(1, Math.floor(byDecoy.length * 0.2)));
        windows.decoy.push({
          venue: `${v.dex}/${v.chain}`, start, pools: rows.length, picked: dTop.length,
          edge: median(dTop.map((r) => r.hRet)) - allMedian,
        });
      }
    }

    // Pooled random control, per candidate.
    const score = (ws) => {
      const edges = ws.map((w) => w.edge).filter((x) => Number.isFinite(x));
      if (!edges.length) return null;
      const med = median(edges), mn = mean(edges);
      const pos = edges.filter((e) => e > 0).length;
      let worse = 0;
      const TRIALS = 2000;
      for (let t = 0; t < TRIALS; t++) {
        const shuffled = edges.map(() => (rnd() < 0.5 ? -1 : 1));
        const rm = median(edges.map((e, i) => e * shuffled[i]));
        if (rm >= med) worse++;
      }
      return {
        windows: edges.length,
        medianEdgePp: Number(med.toFixed(4)),
        meanEdgePp: Number(mn.toFixed(4)),
        positiveWindows: pos,
        positiveWindowsPct: Number(((pos / edges.length) * 100).toFixed(1)),
        pooledP: Number((worse / TRIALS).toFixed(4)),
        verdict: (med >= PASS.minMedianEdgePp && (pos / edges.length) * 100 >= PASS.minPositiveWindowsPct && worse / TRIALS < PASS.maxP) ? 'PASSES' : 'FAILS',
      };
    };

    results[cutoff] = {
      avoid: score(windows.avoid),
      honesty: score(windows.honesty),
      decoy: score(windows.decoy),
    };
    console.log(`\n=== cutoff ${cutoff}d formation / ${cutoff}d holdout ===`);
    for (const k of ['avoid', 'honesty', 'decoy']) {
      const r = results[cutoff][k];
      if (!r) { console.log(`  ${k.padEnd(8)} no data`); continue; }
      console.log(`  ${k.padEnd(8)} n=${String(r.windows).padEnd(4)} median=${String(r.medianEdgePp).padEnd(9)} mean=${String(r.meanEdgePp).padEnd(9)} pos=${String(r.positiveWindowsPct + '%').padEnd(7)} p=${String(r.pooledP).padEnd(7)} ${r.verdict}`);
    }
  }

  const out = {
    generatedAt: new Date().toISOString(),
    preRegistered: PASS,
    prereg: 'PREREG-selection-v2.md, committed before this ran',
    cutoffs: CUTOFFS,
    costModel: COST,
    candidates: {
      avoid: 'skip bottom decile by formation return; edge = survivors vs field median',
      honesty: 'pick tightest advertised-vs-realized gap in formation; edge = how much smaller their holdout gap is vs field',
      decoy: 'deterministic hash of pool address — pure noise, MUST fail or the run is void',
    },
    results,
    caveat: 'Adjacent windows share market regime, so windows are not fully independent.',
  };
  writeFileSync('data/select-v2.json', JSON.stringify(out, null, 2));

  // The guard that decides whether any of this is reportable.
  const decoyPassed = CUTOFFS.some((c) => results[c].decoy?.verdict === 'PASSES');
  console.log('\n=== VERDICT ===');
  if (decoyPassed) {
    console.log('VOID — the decoy cleared the bar. The instrument is measuring noise.');
  } else {
    console.log('Decoy failed at every cutoff, as required. Instrument is not trivially fooled.');
    for (const k of ['avoid', 'honesty']) {
      const verdicts = CUTOFFS.map((c) => results[c][k]?.verdict);
      const allPass = verdicts.every((v) => v === 'PASSES');
      const anyPass = verdicts.some((v) => v === 'PASSES');
      console.log(`  ${k}: ${verdicts.join(' / ')} -> ${allPass ? 'SURVIVES all cutoffs' : anyPass ? 'CUTOFF-DEPENDENT = parameter, not finding' : 'FAILS'}`);
    }
  }
  console.log('\nwrote data/select-v2.json');
}

run().catch((e) => { console.error(String(e.message || e)); process.exit(1); });

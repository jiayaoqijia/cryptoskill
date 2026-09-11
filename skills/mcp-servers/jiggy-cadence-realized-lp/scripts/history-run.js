#!/usr/bin/env node
/**
 * history-run.js — the defect across 5 chains and ~33 INDEPENDENT monthly windows.
 *
 * TWO UPGRADES OVER walk-forward.js:
 *
 * 1. NON-OVERLAPPING WINDOWS. walk-forward stepped 15d across a 30d span, so adjacent windows
 *    shared half their data and could not be counted as independent samples. These are strict
 *    30-day tiles: no shared days, so "the defect appears in N of M months" is a real count.
 *
 * 2. NO WAYBACK MACHINE NEEDED. We nearly rebuilt history by scraping archived DeFi dashboards.
 *    Checked first: poolDayData on the Uniswap v3 subgraph goes back to 2021-05-05 (1,952 days
 *    for USDC/WETH). The primary source has the history natively, at full fidelity, with no
 *    archive gaps and no HTML parsing. Wayback would have been a worse copy of data we can
 *    already query. Checking the primary source cost one query and saved a subsystem.
 *
 * THE VOLATILITY TEST IS A FALSIFICATION TEST, NOT A DISCOVERY.
 * Impermanent loss is mathematically a function of price divergence. So the defect MUST get
 * worse in volatile months. That is not a market insight — it is a prediction our own theory
 * makes, and if the data did not show it, our instrument would be broken. We run it to try to
 * break ourselves. Reporting "IL rises with volatility" as a finding would be dressing up an
 * identity as a discovery.
 *
 * Run: GRAPH_API_KEY=*** node scripts/history-run.js
 */
import { writeFileSync, mkdirSync, readFileSync } from 'fs';
import { dirname } from 'path';
import { fileURLToPath } from 'url';
import { pearson, spearman, DEFAULT_LIVENESS, STABLES } from '../lib/realized.js';
import { scoreWindow, summarizeWindow } from '../lib/walkforward.js';
import { RANGES } from '../lib/concentrated.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUT = `${__dirname}/../data/history.json`;

// Verified live 2026-09-07: these 5 answer. BNB/Celo/Avalanche v3 subgraphs return
// "bad indexers" / "no allocations" on the decentralized network and are excluded as
// UNAVAILABLE rather than silently dropped — absence of an indexer is not absence of a defect.
const CHAINS = {
  mainnet: '5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV',
  arbitrum: 'FbCGRftH4a3yZugY7TnbYgPJVEv2LvMT6oF1fxPe9aJM',
  polygon: '3hCPRGf4z88VC5rsBKU5AA9FBBq5nF3jbKJG7VZCbhjm',
  optimism: 'Cghf4LfVqPiFw6fp6Y5X5Ubc8UpmUhSfJL82zwiBFLaj',
  base: '43Hwfi3dJSoGpyas9VwNoDAv55yjgGrPpNSmbQZArzMG',
};
const UNAVAILABLE = ['bnb (bad indexers)', 'celo (indexer timeout)', 'avalanche (no allocations)'];

const HISTORY = 900;
const WINDOW = 30;
const POOLS = 80;

const key = process.env.GRAPH_API_KEY || readFileSync('/tmp/gk.txt', 'utf8').trim();
const gql = async (id, query) => {
  const r = await fetch(`https://gateway.thegraph.com/api/${key}/subgraphs/id/${id}`, {
    method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ query }),
  });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  const j = await r.json();
  if (j.errors) throw new Error(JSON.stringify(j.errors).slice(0, 200));
  return j.data;
};

/** Annualized realized volatility from daily log returns of token0Price inside the window. */
function realizedVol(slice) {
  const p = slice.map((d) => Number(d.token0Price || 0)).filter((x) => x > 0).reverse();
  if (p.length < 10) return null;
  const rets = [];
  for (let i = 1; i < p.length; i++) rets.push(Math.log(p[i] / p[i - 1]));
  const m = rets.reduce((a, b) => a + b, 0) / rets.length;
  const v = rets.reduce((a, b) => a + (b - m) ** 2, 0) / (rets.length - 1);
  return Math.sqrt(v) * Math.sqrt(365) * 100;
}

async function main() {
  const perChain = {};
  const allWindows = [];

  for (const [chain, id] of Object.entries(CHAINS)) {
    process.stdout.write(`${chain}: fetching ${POOLS} pools x ${HISTORY}d... `);
    let pools;
    try {
      const FIELDS = `id feeTier totalValueLockedUSD token0{symbol} token1{symbol}
        poolDayData(first:${HISTORY},orderBy:date,orderDirection:desc){date volumeUSD feesUSD tvlUSD token0Price}`;
      const d = await gql(id, `{pools(first:${POOLS},orderBy:volumeUSD,orderDirection:desc,where:{totalValueLockedUSD_gt:"250000"}){${FIELDS}}}`);
      pools = d.pools || [];

      // CANARY SUPPLEMENT. The stable-pair canary needs stable/stable pools to be PRESENT.
      // On Base the top-80-by-volume contained none, so every window came back untrusted --
      // the canary correctly refusing to certify rather than reporting a confident number from
      // an unvalidated instrument. The fix is to give the canary its reference signal, NOT to
      // weaken the canary. These pools are fetched for validation only; they are excluded from
      // the headline anyway because summarizeWindow() filters out stablePair rows.
      const haveStable = pools.some((p) => STABLES.has(p.token0?.symbol) && STABLES.has(p.token1?.symbol));
      if (!haveStable) {
        const seen = new Set(pools.map((p) => p.id));
        for (const [a, b] of [['USDC', 'USDT'], ['USDC', 'DAI'], ['USDT', 'DAI'], ['USDC', 'USDS']]) {
          try {
            const sd = await gql(id, `{pools(first:4,orderBy:volumeUSD,orderDirection:desc,where:{
              token0_:{symbol_in:["${a}","${b}"]}, token1_:{symbol_in:["${a}","${b}"]},
              totalValueLockedUSD_gt:"100000"}){${FIELDS}}}`);
            for (const p of sd.pools || []) {
              if (!seen.has(p.id) && STABLES.has(p.token0?.symbol) && STABLES.has(p.token1?.symbol)) {
                pools.push(p); seen.add(p.id);
              }
            }
          } catch { /* a missing stable pair is a real answer; leave the canary unproven */ }
        }
        const added = pools.length - POOLS;
        if (added > 0) process.stdout.write(`(+${added} stable for canary) `);
      }
    } catch (e) {
      console.log(`FAILED (${e.message.slice(0, 60)})`);
      perChain[chain] = { error: e.message.slice(0, 200) };
      continue;
    }
    const maxLen = Math.max(...pools.map((p) => (p.poolDayData || []).length));
    console.log(`${pools.length} pools, deepest history ${maxLen}d`);

    const rows = [];
    for (let off = 0; off + WINDOW <= maxLen; off += WINDOW) {   // NON-OVERLAPPING tiles
      const scored = pools.map((p) => scoreWindow(p, p.poolDayData ?? [], off, WINDOW));
      const any = scored.find((s) => s.measurable);
      if (!any) continue;
      const byRange = {};
      for (const { label, w } of RANGES) byRange[label] = summarizeWindow(scored, DEFAULT_LIVENESS, w === 1e8 ? null : w);
      if (!byRange.full.trusted) { rows.push({ chain, offsetDaysAgo: off, endDate: any.endDate, trusted: false, byRange }); continue; }

      const vols = pools.map((p) => realizedVol((p.poolDayData ?? []).slice(off, off + WINDOW))).filter((v) => v !== null);
      const medVol = vols.length ? [...vols].sort((a, b) => a - b)[Math.floor(vols.length / 2)] : null;

      const row = { chain, offsetDaysAgo: off, endDate: any.endDate, trusted: true, medianRealizedVolPct: medVol, byRange };
      rows.push(row);
      allWindows.push(row);
    }
    perChain[chain] = {
      poolsFetched: pools.length,
      windowsTotal: rows.length,
      windowsTrusted: rows.filter((r) => r.trusted).length,
      oldestWindowEnd: rows.length ? rows[rows.length - 1].endDate : null,
      windows: rows,
    };
  }

  // Stability per chain per range
  const stability = {};
  for (const [chain, d] of Object.entries(perChain)) {
    if (d.error) continue;
    stability[chain] = {};
    for (const { label } of RANGES) {
      const vals = d.windows.filter((w) => w.trusted).map((w) => w.byRange[label].misleadingPct).filter((v) => v !== null);
      if (!vals.length) { stability[chain][label] = null; continue; }
      const s = [...vals].sort((a, b) => a - b);
      stability[chain][label] = {
        windows: vals.length, min: s[0], max: s[s.length - 1],
        median: s.length % 2 ? s[(s.length - 1) / 2] : (s[s.length / 2 - 1] + s[s.length / 2]) / 2,
        windowsWithDefect: vals.filter((v) => v > 0).length,
      };
    }
  }

  // FALSIFICATION TEST: IL is a function of price divergence, so misleading% MUST track
  // volatility. If it does not, the instrument is suspect. This is a self-check, not a finding.
  const vt = {};
  for (const { label } of RANGES) {
    const rows = allWindows.filter((w) => w.medianRealizedVolPct !== null && w.byRange[label].misleadingPct !== null);
    vt[label] = {
      n: rows.length,
      pearson: pearson(rows.map((r) => r.medianRealizedVolPct), rows.map((r) => r.byRange[label].misleadingPct)),
      spearman: spearman(rows.map((r) => r.medianRealizedVolPct), rows.map((r) => r.byRange[label].misleadingPct)),
    };
  }

  const out = {
    generatedAt: new Date().toISOString(),
    method: `${WINDOW}-day NON-OVERLAPPING windows, top ${POOLS} pools/chain by volume, up to ${HISTORY}d of poolDayData`,
    chainsMeasured: Object.keys(CHAINS),
    chainsUnavailable: UNAVAILABLE,
    wideNote: 'poolDayData reaches 2021-05-05 on mainnet. No Wayback Machine or archive scraping '
      + 'is required: the primary source carries the history natively.',
    volatilityTest: {
      note: 'FALSIFICATION TEST, NOT A FINDING. Impermanent loss is mathematically a function of '
        + 'price divergence, so the defect MUST worsen with volatility. We run it to try to break '
        + 'the instrument. A null or negative result would mean our own measurement is broken. '
        + 'It is NOT evidence about macro, equities, or crypto beta -- we did not test those, and '
        + 'with this many candidate series we could find a "relationship" to anything.',
      rows: vt,
    },
    stability,
    perChain,
  };
  mkdirSync(dirname(OUT), { recursive: true });
  writeFileSync(OUT, JSON.stringify(out, null, 2));

  console.log(`\nwrote ${OUT}\n`);
  console.log('chain      windows  oldest       tight        moderate     full');
  for (const [chain, s] of Object.entries(stability)) {
    if (!s.tight) { console.log(`${chain.padEnd(10)} no trusted windows`); continue; }
    const f = (x) => `${x.min.toFixed(0)}-${x.max.toFixed(0)}% (med ${x.median.toFixed(0)}%)`;
    console.log(`${chain.padEnd(10)} ${String(s.tight.windows).padStart(3)}     ${perChain[chain].oldestWindowEnd}   ${f(s.tight).padEnd(12)} ${f(s.moderate).padEnd(12)} ${f(s.full)}`);
  }
  console.log('\nfalsification test — misleading% vs realized volatility (must be POSITIVE):');
  for (const [label, r] of Object.entries(vt)) {
    console.log(`  ${label.padEnd(9)} n=${String(r.n).padStart(3)}  pearson=${r.pearson?.toFixed(3)}  spearman=${r.spearman?.toFixed(3)}`);
  }
}

main().catch((e) => { console.error(e); process.exit(1); });

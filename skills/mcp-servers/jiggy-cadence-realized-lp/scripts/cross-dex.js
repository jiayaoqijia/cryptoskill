#!/usr/bin/env node
/**
 * cross-dex.js — is this a Uniswap artifact, or how concentrated liquidity works?
 *
 * Everything measured so far was Uniswap v3. If the defect only exists there, the honest
 * headline is "Uniswap's advertised APR is broken", which is a much smaller claim than the one
 * we want to make. So we run the SAME instrument, unchanged, on two independent DEXes that
 * fork the v3 schema:
 *
 *   Aerodrome Slipstream (Base)  — different team, different incentive model (veAERO emissions)
 *   SushiSwap v3 (Ethereum)      — different team, same chain as our mainnet baseline
 *
 * Probed 6 candidates (scripts/dex-probe.mjs); these 2 answer on the decentralized network.
 * PancakeSwap v3 (bsc + eth), QuickSwap v3, Camelot v3 return bad indexers / subgraph not
 * found and are recorded as UNAVAILABLE, never as venues without the defect.
 *
 * Run: GRAPH_API_KEY=*** node scripts/cross-dex.js
 */
import { writeFileSync, mkdirSync, readFileSync } from 'fs';
import { dirname } from 'path';
import { fileURLToPath } from 'url';
import { DEFAULT_LIVENESS, STABLES } from '../lib/realized.js';
import { scoreWindow, summarizeWindow } from '../lib/walkforward.js';
import { RANGES } from '../lib/concentrated.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUT = `${__dirname}/../data/cross-dex.json`;

const VENUES = {
  'aerodrome-slipstream': { id: 'GENunSHWLBXm59mBSgPzQ8metBEp9YDfdqwFr91Av1UM', chain: 'base', team: 'Aerodrome' },
  'sushiswap-v3': { id: '5nnoU1nUFeWqtXgbpC54L9PWdpgo7Y9HYinR3uTMsfzs', chain: 'mainnet', team: 'SushiSwap' },
};
const UNAVAILABLE = [
  'pancakeswap-v3-bsc (bad indexers)',
  'pancakeswap-v3-eth (subgraph not found)',
  'quickswap-v3-polygon (indexer timeout)',
  'camelot-v3-arbitrum (subgraph not found)',
];

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

const FIELDS = `id feeTier totalValueLockedUSD token0{symbol} token1{symbol}
  poolDayData(first:${HISTORY},orderBy:date,orderDirection:desc){date volumeUSD feesUSD tvlUSD token0Price}`;

async function main() {
  const perVenue = {};

  for (const [venue, meta] of Object.entries(VENUES)) {
    process.stdout.write(`${venue}: `);
    let pools;
    try {
      const d = await gql(meta.id, `{pools(first:${POOLS},orderBy:volumeUSD,orderDirection:desc,where:{totalValueLockedUSD_gt:"250000"}){${FIELDS}}}`);
      pools = d.pools || [];

      // Same canary supplement as history-run.js: the stable-pair reference must be PRESENT
      // for the instrument to prove it measures IL correctly. Validation-only; excluded from
      // every headline because summarizeWindow() filters stablePair rows out of the sample.
      if (!pools.some((p) => STABLES.has(p.token0?.symbol) && STABLES.has(p.token1?.symbol))) {
        const seen = new Set(pools.map((p) => p.id));
        for (const [a, b] of [['USDC', 'USDT'], ['USDC', 'DAI'], ['USDT', 'DAI']]) {
          try {
            const sd = await gql(meta.id, `{pools(first:4,orderBy:volumeUSD,orderDirection:desc,where:{
              token0_:{symbol_in:["${a}","${b}"]}, token1_:{symbol_in:["${a}","${b}"]},
              totalValueLockedUSD_gt:"100000"}){${FIELDS}}}`);
            for (const p of sd.pools || []) {
              if (!seen.has(p.id) && STABLES.has(p.token0?.symbol) && STABLES.has(p.token1?.symbol)) { pools.push(p); seen.add(p.id); }
            }
          } catch { /* absent stable pair is a real answer: leave the canary unproven */ }
        }
      }
    } catch (e) {
      console.log(`FAILED (${e.message.slice(0, 60)})`);
      perVenue[venue] = { ...meta, error: e.message.slice(0, 200) };
      continue;
    }

    const maxLen = Math.max(...pools.map((p) => (p.poolDayData || []).length));
    const rows = [];
    for (let off = 0; off + WINDOW <= maxLen; off += WINDOW) {
      const scored = pools.map((p) => scoreWindow(p, p.poolDayData ?? [], off, WINDOW));
      const any = scored.find((s) => s.measurable);
      if (!any) continue;
      const byRange = {};
      for (const { label, w } of RANGES) byRange[label] = summarizeWindow(scored, DEFAULT_LIVENESS, w === 1e8 ? null : w);
      rows.push({ offsetDaysAgo: off, endDate: any.endDate, trusted: byRange.full.trusted, byRange });
    }

    const stability = {};
    for (const { label } of RANGES) {
      const vals = rows.filter((r) => r.trusted).map((r) => r.byRange[label].misleadingPct).filter((v) => v !== null);
      if (!vals.length) { stability[label] = null; continue; }
      const s = [...vals].sort((a, b) => a - b);
      stability[label] = {
        windows: vals.length, min: s[0], max: s[s.length - 1],
        median: s.length % 2 ? s[(s.length - 1) / 2] : (s[s.length / 2 - 1] + s[s.length / 2]) / 2,
      };
    }

    perVenue[venue] = {
      ...meta,
      poolsFetched: pools.length,
      windowsTotal: rows.length,
      windowsTrusted: rows.filter((r) => r.trusted).length,
      oldestWindowEnd: rows.length ? rows[rows.length - 1].endDate : null,
      stability,
      windows: rows,
    };
    console.log(`${pools.length} pools, ${rows.filter((r) => r.trusted).length}/${rows.length} trusted windows`);
  }

  const out = {
    generatedAt: new Date().toISOString(),
    question: 'Is the advertised-APR defect a Uniswap artifact, or a property of concentrated liquidity?',
    method: `${WINDOW}-day non-overlapping windows, top ${POOLS} pools by volume, same instrument as history-run.js, unchanged`,
    venuesUnavailable: UNAVAILABLE,
    perVenue,
  };
  mkdirSync(dirname(OUT), { recursive: true });
  writeFileSync(OUT, JSON.stringify(out, null, 2));

  console.log(`\nwrote ${OUT}\n`);
  console.log('venue                  chain     months  oldest       tight            moderate         full');
  for (const [venue, d] of Object.entries(perVenue)) {
    if (d.error) { console.log(`${venue.padEnd(22)} ${d.chain.padEnd(9)} ERROR ${d.error.slice(0, 40)}`); continue; }
    if (!d.stability.tight) { console.log(`${venue.padEnd(22)} ${d.chain.padEnd(9)} no trusted windows`); continue; }
    const f = (x) => `${x.min.toFixed(0)}-${x.max.toFixed(0)}% (med ${x.median.toFixed(0)}%)`;
    console.log(`${venue.padEnd(22)} ${d.chain.padEnd(9)} ${String(d.stability.tight.windows).padStart(4)}    ${d.oldestWindowEnd}   ${f(d.stability.tight).padEnd(16)} ${f(d.stability.moderate).padEnd(16)} ${f(d.stability.full)}`);
  }
}

main().catch((e) => { console.error(e); process.exit(1); });

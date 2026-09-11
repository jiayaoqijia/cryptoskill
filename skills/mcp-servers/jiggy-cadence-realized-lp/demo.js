#!/usr/bin/env node
/**
 * demo.js — the ENTIRE pitch, one command, no setup beyond a Graph API key.
 *
 * A judge should not need to know this repo has three build scripts, an MCP
 * server, and a static site. They run one thing and get the finding, fetched
 * live from The Graph right now — no pre-built JSON, no server process.
 *
 *   GRAPH_API_KEY=... node demo.js
 *
 * 2026-09-09: first version of this file called scorePool(url, id, opts) and
 * invented field names (.full.ilPct, .advertisedAprPct at top level) that do
 * not exist on lib/realized.js's real API. It failed its own canary on the
 * first live run -- correctly, since a wrong contract IS broken, and the
 * canary's whole job is to refuse a number rather than print one blind. Fixed
 * by reading lib/realized.js's actual exports instead of guessing them, and
 * by reusing its own summarize()/canary logic instead of hand-rolling a
 * second, weaker one.
 */
import { gatewayUrl, query, fetchTopPools, scorePool, summarize, DEFAULT_LIVENESS } from './lib/realized.js';

const KEY = process.env.GRAPH_API_KEY;
if (!KEY) {
  console.error(
    '\nGRAPH_API_KEY is not set.\n\n' +
    'Get a free key: https://thegraph.com/studio (Subgraph Studio -> create API key)\n' +
    'Then run:\n\n  GRAPH_API_KEY=your-key node demo.js\n'
  );
  process.exit(1);
}

const url = gatewayUrl(KEY);
const bar = '─'.repeat(64);
const pct = (x, d = 2) => (x === null || x === undefined ? 'n/a' : `${x >= 0 ? '+' : ''}${x.toFixed(d)}%`);

async function main() {
  console.log(bar);
  console.log('REALIZED — what did you actually make as an LP?');
  console.log(bar);
  console.log(
    '\nAdvertised LP APR is fee income, annualized. It has no price term.\n' +
    'So it is positive by construction: a pool CANNOT advertise a loss.\n'
  );

  console.log(`${bar}\nFetching a live sample from The Graph (Uniswap v3 mainnet)...\n${bar}`);
  const pools = await fetchTopPools(url, { first: 20, minTvlUsd: 250_000 });
  if (!pools.length) {
    console.error('No pools returned — Gateway or subgraph issue. Not a finding, a fetch failure.');
    process.exit(2);
  }
  const scored = pools.map((p) => scorePool(p));

  // ── The canary lives inside summarize() itself: it separately tracks any
  // stable/stable pair in the sample and requires |IL| < 1%, and marks the
  // whole result UNPROVEN if no stable pair showed up at all. ──────────────
  const summary = summarize(scored, DEFAULT_LIVENESS);
  console.log(`${bar}\nSTEP 1 — CANARY (does the instrument actually work?)\n${bar}`);
  console.log(summary.canary.note);
  if (!summary.canary.passed) {
    console.error(`\nCANARY ${summary.canary.stablePairsFound ? 'FAILED' : 'UNPROVEN'} —`,
      summary.canary.stablePairsFound
        ? `worst stable-pair |IL| = ${pct(summary.canary.worstAbsIlPct, 4)}, expected <1%`
        : 'no stable/stable pair in this 20-pool sample.');
    console.error('Refusing to print a headline number on an unproven instrument. Re-run for a larger sample.');
    process.exit(2);
  }
  console.log(`CANARY PASS — worst stable-pair |IL| = ${pct(summary.canary.worstAbsIlPct, 4)}`);
  console.log('The math finds a known-zero signal correctly. Numbers below can be trusted.\n');

  // ── One concrete pool, all four concentration ranges. ──────────────────
  console.log(`${bar}\nSTEP 2 — ONE REAL POOL, RIGHT NOW\n${bar}`);
  const example = scored.find((s) => s.measurable && !s.stablePair) ?? scored[0];
  if (example?.measurable) {
    console.log(`Pool: ${example.pair}  (${example.windowDays}-day live window, fetched just now)`);
    console.log(`Advertised APR (fee-only, annualized): ${pct(example.advertisedAprPct, 1)} — always positive.\n`);
    console.log('  range        IL          realized      out of range?');
    for (const [label, r] of Object.entries(example.byRange)) {
      if (!r.measurable) { console.log(`  ${label.padEnd(11)} unmeasurable`); continue; }
      console.log(
        `  ${label.padEnd(11)} ${pct(r.impermanentLossPct).padEnd(11)} ${pct(r.realizedReturnPct).padEnd(13)} ${r.outOfRange ? 'YES' : 'no'}`
      );
    }
    console.log(
      example.misleading
        ? '\n  This pool is MISLEADING: advertised APR is positive, full-range realized return is negative.\n'
        : "\n  This pool isn't misleading at full range — the defect isn't universal, it's a rate. See step 3.\n"
    );
  } else {
    console.log('(sample pool unmeasurable this run — the field IS present as `measurable: false`, never a fabricated 0)\n');
  }

  // ── Is it one pool, or a pattern? ───────────────────────────────────────
  console.log(`${bar}\nSTEP 3 — IS THIS ONE POOL, OR A PATTERN?\n${bar}`);
  console.log(`Live sample: ${summary.counts.fetched} fetched, ${summary.counts.measurable} measurable, ${summary.counts.liveVolatile} pass the liveness gate.`);
  if (summary.counts.liveVolatile > 0) {
    console.log(`${summary.misleadingCount}/${summary.counts.liveVolatile} (${summary.misleadingPct.toFixed(0)}%) advertised a positive APR while realized return was negative, full-range.`);
    console.log(`Median advertised APR: ${pct(summary.medianAdvertisedAprPct, 1)}   Median realized APR: ${pct(summary.medianRealizedAprPct, 1)}`);
  } else {
    console.log('No pool cleared the liveness gate in this small sample — re-run, or see the full 250-pool corpus below.');
  }

  console.log(`\n${bar}`);
  console.log('This is a 20-pool live spot-check. The full evidence base is much larger:');
  console.log('  110 independent monthly windows, 4 chains, cross-DEX check on Aerodrome,');
  console.log('  a graded, backdated audit of DefiLlama\'s own yield predictions.');
  console.log('README.md has the numbers. Full site + agent API: https://realized.drainfun.xyz');
  console.log(bar);
}

main().catch((err) => {
  console.error('\nDEMO FAILED (an error, not a finding):', err.message);
  process.exit(1);
});

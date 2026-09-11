#!/usr/bin/env node
/**
 * walk-forward.js — re-run the entire instrument in every 30-day window of the last ~6 months.
 *
 * The question this answers: is "advertised APR cannot tell you that you lost money" a fact
 * about DeFi, or a fact about the one month we happened to measure? Until now the repo could
 * not tell the difference. Every published number came from a single window ending on the day
 * the script was run.
 *
 * Output: data/walkforward.json
 * Run: GRAPH_API_KEY=*** node scripts/walk-forward.js
 */
import { writeFileSync, mkdirSync } from 'fs';
import { dirname } from 'path';
import { fileURLToPath } from 'url';
import { gatewayUrl, fetchTopPools, DEFAULT_LIVENESS, pearson, spearman } from '../lib/realized.js';
import { scoreWindow, summarizeWindow } from '../lib/walkforward.js';
import { RANGES } from '../lib/concentrated.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUT = `${__dirname}/../data/walkforward.json`;

const HISTORY_DAYS = 210;   // ~7 months of poolDayData
const WINDOW = 30;
const STEP = 15;            // new window every 15 days (overlapping, so windows are NOT independent)

async function main() {
  const apiKey = process.env.GRAPH_API_KEY;
  if (!apiKey) { console.error('GRAPH_API_KEY is required'); process.exit(2); }
  const url = gatewayUrl(apiKey);

  console.log(`fetching ${HISTORY_DAYS}d of history for top pools...`);
  const pools = await fetchTopPools(url, { first: 250, days: HISTORY_DAYS });
  console.log(`fetched ${pools.length} pools`);

  const offsets = [];
  for (let o = 0; o + WINDOW <= HISTORY_DAYS; o += STEP) offsets.push(o);

  const windows = [];
  for (const offset of offsets) {
    const scored = pools.map((p) => scoreWindow(p, p.poolDayData ?? [], offset, WINDOW));
    const anyMeasurable = scored.find((s) => s.measurable);
    if (!anyMeasurable) continue;

    const row = {
      offsetDaysAgo: offset,
      endDate: anyMeasurable.endDate,
      byRange: {},
    };
    for (const { label, w } of RANGES) {
      row.byRange[label] = summarizeWindow(scored, DEFAULT_LIVENESS, w === 1e8 ? null : w);
    }
    // correlation in this window, full-range basis
    const live = scored.filter((s) => s.measurable && !s.stablePair && !s.collapsed
      && s.liveness.activeDays >= DEFAULT_LIVENESS.minActiveDays
      && s.liveness.recent7dVolumeUsd > DEFAULT_LIVENESS.minRecent7dVolumeUsd
      && s.currentTvlUsd > DEFAULT_LIVENESS.minTvlUsd);
    row.correlation = {
      n: live.length,
      pearson: pearson(live.map((s) => s.advertisedAprPct), live.map((s) => s.realizedAprPct)),
      spearman: spearman(live.map((s) => s.advertisedAprPct), live.map((s) => s.realizedAprPct)),
    };
    windows.push(row);
  }

  const trusted = windows.filter((w) => w.byRange.full.trusted);
  const untrusted = windows.length - trusted.length;

  // Stability of the headline across windows, per range.
  const stability = {};
  for (const { label } of RANGES) {
    const vals = trusted.map((w) => w.byRange[label].misleadingPct).filter((v) => v !== null);
    if (!vals.length) { stability[label] = null; continue; }
    const s = [...vals].sort((a, b) => a - b);
    const mean = vals.reduce((a, b) => a + b, 0) / vals.length;
    stability[label] = {
      windows: vals.length,
      min: s[0],
      median: s.length % 2 ? s[(s.length - 1) / 2] : (s[s.length / 2 - 1] + s[s.length / 2]) / 2,
      max: s[s.length - 1],
      mean,
      everyWindowAbove50: s[0] > 50,
      everyWindowAbove33: s[0] > 33,
    };
  }

  const out = {
    generatedAt: new Date().toISOString(),
    method: `${WINDOW}-day windows stepped every ${STEP} days across ${HISTORY_DAYS} days of poolDayData, `
      + 'same pools, same gates, instrument re-run independently in each window',
    caveats: [
      'OVERLAPPING WINDOWS: step 15d < window 30d, so adjacent windows share half their data. '
        + 'They are NOT independent samples and must not be treated as n=13 for significance.',
      'SURVIVORSHIP BIAS: pools are ranked by CURRENT volume, so pools that died are absent from '
        + 'historical windows. This makes the past look better than it was, which works AGAINST '
        + 'our thesis rather than for it. The subgraph does not expose point-in-time ranking.',
      'Each window carries its own stable-pair canary. Untrusted windows are reported, not dropped.',
    ],
    windowsTotal: windows.length,
    windowsTrusted: trusted.length,
    windowsUntrusted: untrusted,
    stability,
    windows,
  };

  mkdirSync(dirname(OUT), { recursive: true });
  writeFileSync(OUT, JSON.stringify(out, null, 2));

  console.log(`\nwrote ${OUT}`);
  console.log(`windows: ${windows.length} total, ${trusted.length} trusted, ${untrusted} untrusted\n`);
  console.log('end date    n    tight   moderate   wide    full    canary');
  for (const w of windows) {
    const f = w.byRange.full;
    const pct = (r) => (r.misleadingPct === null ? '  --' : `${r.misleadingPct.toFixed(0).padStart(3)}%`);
    console.log(`${w.endDate}  ${String(f.n).padStart(3)}   ${pct(w.byRange.tight)}    ${pct(w.byRange.moderate)}     ${pct(w.byRange.wide)}   ${pct(w.byRange.full)}    ${f.canary.passed ? 'PASS' : 'FAIL'}${f.trusted ? '' : ' UNTRUSTED'}`);
  }
  console.log('\nstability of "advertised positive while realized negative":');
  for (const [label, s] of Object.entries(stability)) {
    if (!s) { console.log(`  ${label}: no trusted windows`); continue; }
    console.log(`  ${label.padEnd(9)} min=${s.min.toFixed(0)}%  median=${s.median.toFixed(0)}%  max=${s.max.toFixed(0)}%  (${s.windows} windows)`);
  }
}

main().catch((e) => { console.error(e); process.exit(1); });

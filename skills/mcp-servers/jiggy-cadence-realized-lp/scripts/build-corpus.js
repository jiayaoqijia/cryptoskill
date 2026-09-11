#!/usr/bin/env node
/**
 * build-corpus.js — regenerate the public ground-truth corpus.
 *
 * This IS the differentiator, not the MCP server. Anyone can wrap a subgraph in
 * natural language. Nobody else publishes a falsifiable, canary-gated table of
 * which live pools actually paid LPs vs which ones only look like they did.
 *
 * Output: data/corpus.json — judges (or anyone) can diff this against the live
 * subgraph themselves. Run: GRAPH_API_KEY=... node scripts/build-corpus.js
 */
import { writeFileSync, mkdirSync } from 'fs';
import { dirname } from 'path';
import { fileURLToPath } from 'url';
import { gatewayUrl, fetchTopPools, scorePool, summarize, sensitivity, DEFAULT_LIVENESS, pearson, spearman, RANGES } from '../lib/realized.js';
import { concentratedIlPct, outOfRange } from '../lib/concentrated.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUT = `${__dirname}/../data/corpus.json`;

const GATES = [
  { label: 'loose', gate: { minActiveDays: 20, minRecent7dVolumeUsd: 10_000, minTvlUsd: 100_000 } },
  { label: 'mid', gate: DEFAULT_LIVENESS },
  { label: 'strict', gate: { minActiveDays: 28, minRecent7dVolumeUsd: 250_000, minTvlUsd: 1_000_000 } },
];

async function main() {
  const apiKey = process.env.GRAPH_API_KEY;
  if (!apiKey) {
    console.error('GRAPH_API_KEY is required');
    process.exit(2);
  }
  const url = gatewayUrl(apiKey);
  console.log('fetching pools from The Graph (Uniswap v3 mainnet)...');
  const pools = await fetchTopPools(url, { first: 250, days: 30 });
  console.log(`fetched ${pools.length} pools`);

  const scored = pools.map(scorePool);
  const s = summarize(scored);
  const sens = sensitivity(scored, GATES);

  // Correlation, computed here so it is REPRODUCIBLE. A previous README quoted
  // corr = 0.06 that existed in no committed code and does not regenerate; it is
  // retracted rather than restated. Both Pearson and Spearman are reported because
  // Pearson alone chases the fat tail of advertised APR.
  const measurable = scored.filter((p) => p.measurable);
  const corrRows = GATES.map(({ label, gate }) => {
    const live = measurable.filter((p) => !p.stablePair && !p.collapsed
      && p.liveness.activeDays >= gate.minActiveDays
      && p.liveness.recent7dVolumeUsd > gate.minRecent7dVolumeUsd
      && p.currentTvlUsd > gate.minTvlUsd);
    const x = live.map((p) => p.advertisedAprPct);
    const y = live.map((p) => p.realizedAprPct);
    // Trimmed variant: drop top/bottom 2% of advertised APR.
    const sortedIdx = live.map((_, i) => i).sort((a, b) => x[a] - x[b]);
    const k = Math.floor(live.length * 0.02);
    const keep = new Set(sortedIdx.slice(k, sortedIdx.length - k));
    const xt = x.filter((_, i) => keep.has(i));
    const yt = y.filter((_, i) => keep.has(i));
    return {
      label, n: live.length,
      pearson: pearson(x, y), spearman: spearman(x, y),
      pearsonTrimmed: pearson(xt, yt), spearmanTrimmed: spearman(xt, yt),
    };
  });

  // CANARY for the correlation code itself: advertised APR and fee return are both
  // fee-derived, so they MUST correlate strongly. If this is weak the estimator is broken
  // and every correlation below is untrusted.
  const corrCanaryValue = pearson(measurable.map((p) => p.advertisedAprPct), measurable.map((p) => p.feeReturnPct));
  const corrCanary = {
    value: corrCanaryValue,
    passed: corrCanaryValue !== null && corrCanaryValue > 0.3,
    note: 'corr(advertised APR, fee return) must be clearly positive — both are fee-derived. A weak value means the estimator is broken, not that the market is odd.',
  };

  // Headline at every concentration range. Full-range is the v2-equivalent baseline.
  const rangeRows = RANGES.map(({ label, w, note }) => {
    const live = measurable.filter((p) => !p.stablePair && !p.collapsed
      && p.liveness.activeDays >= DEFAULT_LIVENESS.minActiveDays
      && p.liveness.recent7dVolumeUsd > DEFAULT_LIVENESS.minRecent7dVolumeUsd
      && p.currentTvlUsd > DEFAULT_LIVENESS.minTvlUsd);
    const ils = live.map((p) => concentratedIlPct(p.priceRatio, w));
    const rz = live.map((p, i) => p.feeReturnPct + ils[i]);
    const mis = live.filter((p, i) => p.advertisedAprPct > 0 && rz[i] < 0).length;
    const oor = live.filter((p) => outOfRange(p.priceRatio, w)).length;
    const med = (xs) => { const q = [...xs].sort((a, b) => a - b); return q.length ? (q.length % 2 ? q[(q.length - 1) / 2] : (q[q.length / 2 - 1] + q[q.length / 2]) / 2) : null; };
    return {
      label, rangeWidthX: w, note, n: live.length,
      medianIlPct: med(ils), medianRealizedPct: med(rz),
      outOfRangeCount: oor,
      misleadingPct: live.length ? (mis / live.length) * 100 : null,
    };
  });

  if (!s.canary.passed) {
    console.error('CANARY FAILED — refusing to publish an untrusted corpus.');
    console.error(JSON.stringify(s.canary, null, 2));
    process.exit(1);
  }
  if (!corrCanary.passed) {
    console.error('CORRELATION CANARY FAILED — refusing to publish. The estimator could not find a signal known to be present.');
    console.error(JSON.stringify(corrCanary, null, 2));
    process.exit(1);
  }

  const corpus = {
    generatedAt: new Date().toISOString(),
    source: 'The Graph — Uniswap v3 mainnet subgraph (5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV)',
    method: 'realized = fee income - impermanent loss over a 30-day poolDayData window; ' +
      'advertised = most recent day fees, annualized on current TVL (the standard DEX-UI formula)',
    canary: s.canary,
    counts: s.counts,
    headline: {
      medianAdvertisedAprPct: s.medianAdvertisedAprPct,
      medianRealizedAprPct: s.medianRealizedAprPct,
      medianGapPts: s.medianGapPts,
      misleadingCount: s.misleadingCount,
      misleadingPct: s.misleadingPct,
    },
    sensitivity: sens,
    correlation: {
      canary: corrCanary,
      note: 'advertised vs realized APR. Reported at 3 liveness gates x {raw, 2% trimmed} x {pearson, spearman} because the value moves a lot across those choices — see README honesty box.',
      rows: corrRows,
    },
    byRange: {
      note: 'Uniswap v3 LPs concentrate. The v2/full-range formula is the MOST GENEROUS case for the pool. Reported at 4 ranges; the defect must survive all of them or it is a parameter.',
      rows: rangeRows,
    },
    worstOffenders: s.worstOffenders,
    allScoredPools: scored.filter((p) => p.measurable),
  };

  mkdirSync(dirname(OUT), { recursive: true });
  writeFileSync(OUT, JSON.stringify(corpus, null, 2));
  console.log(`\nwrote ${OUT}`);
  console.log(`canary: ${s.canary.passed ? 'PASS' : 'FAIL'} (worst stable |IL| = ${s.canary.worstAbsIlPct?.toFixed(4)}%)`);
  console.log(`headline: ${s.misleadingCount}/${s.counts.liveVolatile} live pools mislead (${s.misleadingPct?.toFixed(0)}%)`);
  console.log('sensitivity:');
  for (const row of sens) console.log(`  ${row.label.padEnd(8)} n=${row.n}  misleading=${row.misleadingPct?.toFixed(0)}%  medGap=${row.medianGapPts?.toFixed(2)}`);
  console.log(`correlation canary: ${corrCanary.passed ? 'PASS' : 'FAIL'} (corr(advertised, feeReturn) = ${corrCanaryValue?.toFixed(3)})`);
  console.log('corr(advertised APR, realized APR):');
  for (const r of corrRows) {
    console.log(`  ${r.label.padEnd(8)} n=${String(r.n).padStart(3)}  pearson=${r.pearson?.toFixed(3)}  spearman=${r.spearman?.toFixed(3)}  (trimmed: ${r.pearsonTrimmed?.toFixed(3)} / ${r.spearmanTrimmed?.toFixed(3)})`);
  }
  console.log('by concentration range:');
  for (const r of rangeRows) {
    console.log(`  ${r.label.padEnd(9)} medIL=${r.medianIlPct?.toFixed(2)}%  medRealized=${r.medianRealizedPct?.toFixed(2)}%  outOfRange=${r.outOfRangeCount}/${r.n}  misleading=${r.misleadingPct?.toFixed(0)}%`);
  }
}

main().catch((e) => { console.error(e); process.exit(1); });

#!/usr/bin/env node
/**
 * build-llama-layer.js — the correction layer on the site people actually use.
 *
 * DefiLlama is where nearly everyone shops for yield. It ships a machine-learning
 * yield prediction on ~11k pools (predictedClass + predictedProbability). What
 * nobody publishes is whether those predictions were RIGHT. We graded them
 * retrospectively (scripts/grade-llama-backdated.py, 26 Wayback snapshots of
 * yields.llama.fi/pools, 8,092 graded instances across 459 pools) and the
 * answer has two halves that point opposite directions:
 *
 *   1. Raw accuracy is a MIRAGE. The edge over a naive baseline flips sign with
 *      the tolerance band: strict 0% = -1.4pp (WORSE than guessing), mid 5% =
 *      +4.5pp, loose 10% = +1.5pp. A number that changes sign when you move an
 *      arbitrary knob is a parameter, not a finding.
 *
 *   2. Their CONFIDENCE is genuinely calibrated, and that survives the same
 *      knob. Sorted by DefiLlama's own predictedProbability tier:
 *          bin1 n=1987  edge -0.3pp
 *          bin2 n=2639  edge +3.1pp
 *          bin3 n=3466  edge +8.3pp
 *      Monotonic, wide spread, large n. When DefiLlama says it's confident, it
 *      has earned it. When it isn't, its prediction is worth nothing.
 *
 * So the useful product is NOT "DefiLlama is wrong." It's: use their high-
 * confidence predictions, ignore their low-confidence ones, and in every case
 * check the fee-only APR against realized return -- because the target variable
 * they predict (fee APR) is near-orthogonal to what an LP actually takes home.
 *
 * This script emits data/llama-layer.json for the site + API. It performs no
 * new measurement; it reshapes an existing graded result into guidance.
 *
 * Run: node scripts/build-llama-layer.js
 */
import { readFileSync, writeFileSync } from 'fs';

const __dir = new URL('.', import.meta.url);
const R = (p) => JSON.parse(readFileSync(new URL(`../${p}`, import.meta.url), 'utf8'));

const grade = R('data/llama-grade-backdated.json');

// ── Canary first: the grader must prove it can tell right from wrong. ──────
// oracle (a perfect predictor) must score 100, inverted (always wrong) must
// score 0, coinflip must land near 50. If these drift, every number below is
// void -- refuse to write rather than publish guidance from a broken grader.
const c = grade.canary;
const canaryOk = c && c.oracle === 100 && c.inverted === 0 && Math.abs(c.coinflip - 50) < 5;
if (!canaryOk) {
  console.error('CANARY FAILED -- grader cannot distinguish a perfect predictor from an inverted one.');
  console.error(JSON.stringify(c));
  console.error('Refusing to write llama-layer.json. Guidance from an unproven grader is worse than none.');
  process.exit(2);
}

const bands = Object.entries(grade.byBand).map(([label, v]) => ({
  band: label,
  n: v.n,
  accuracyPct: v.accuracy,
  baselinePct: v.baseline,
  edgePp: v.edge,
}));

const conf = Object.entries(grade.byConfidence)
  .map(([tier, v]) => ({
    tier: Number(tier),
    n: v.n,
    accuracyPct: v.accuracy,
    baselinePct: v.baseline,
    edgePp: v.accuracy - v.baseline,
  }))
  .sort((a, b) => a.tier - b.tier);

// Is the calibration claim actually monotonic? Assert it rather than assume it --
// if a future re-grade breaks monotonicity, the headline claim is dead and the
// file should say so instead of quietly shipping a stale story.
const monotonic = conf.every((x, i) => i === 0 || x.edgePp > conf[i - 1].edgePp);

// Does the raw-accuracy edge flip sign across bands? That's the "mirage" claim.
const edgeSigns = new Set(bands.map((b) => Math.sign(b.edgePp)));
const flipsSign = edgeSigns.size > 1;

const out = {
  generatedAt: new Date().toISOString(),
  source: {
    what: 'DefiLlama yield predictions (predictedClass / predictedProbability), graded retrospectively',
    how: grade.method,
    snapshots: grade.snapshots?.length ?? null,
    nInstances: grade.nInstances,
    nPools: grade.nPools,
    gradedAt: grade.gradedAt,
  },
  canary: { ...c, passed: true, note: 'oracle must score 100, inverted 0, coinflip ~50' },

  headline: {
    rawAccuracyIsAMirage: flipsSign,
    rawAccuracyNote: flipsSign
      ? 'Edge over baseline FLIPS SIGN across tolerance bands -- it is a parameter, not a finding.'
      : 'Edge did not flip sign across bands in this grade; the mirage claim does NOT currently hold.',
    confidenceIsCalibrated: monotonic,
    confidenceNote: monotonic
      ? 'Edge rises monotonically with DefiLlama\'s own stated confidence tier. Their uncertainty is honest even when their point estimate is not.'
      : 'Confidence tiers are NOT monotonic in this grade -- the calibration claim does not hold and must not be published as if it does.',
  },

  byBand: bands,
  byConfidence: conf,

  howToUseThis: [
    'Trust DefiLlama\'s prediction ONLY in its top confidence tier -- that is where the edge is real (+8.3pp over baseline, n=3466).',
    'Treat its low-confidence predictions as noise (-0.3pp, i.e. no better than the base rate).',
    'In every tier, remember what is being predicted: fee-only APY. That target is near-orthogonal to what an LP actually takes home, because it has no impermanent-loss term.',
    'Use /api/pools or the realized_return MCP tool to get the realized figure for the specific pool before acting on any advertised or predicted APR.',
  ],
};

writeFileSync(new URL('../data/llama-layer.json', import.meta.url), JSON.stringify(out, null, 2));

console.log('canary PASS (oracle 100 / inverted 0 / coinflip ~50)');
console.log(`raw accuracy flips sign across bands: ${flipsSign}`);
console.log(`confidence tiers monotonic: ${monotonic}`);
for (const t of conf) console.log(`  bin${t.tier}: n=${t.n} edge ${t.edgePp >= 0 ? '+' : ''}${t.edgePp.toFixed(1)}pp`);
console.log('\nwrote data/llama-layer.json');

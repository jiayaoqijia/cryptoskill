/**
 * concentrated.js — impermanent loss for CONCENTRATED liquidity (Uniswap v3).
 *
 * WHY THIS EXISTS. lib/realized.js shipped `impermanentLossPct(r)`, the constant-product
 * (v2) formula. It is correct only for a FULL-RANGE position. Uniswap v3's entire premise
 * is that LPs concentrate into a band, and inside a band IL is amplified; once price leaves
 * the band the position is 100% converted into the losing asset and the loss stops being
 * "impermanent" at all. Measuring a v3 venue with the v2 formula reports the most generous
 * possible outcome for the pool — which understates the exact defect this project claims to
 * expose. Found 2026-09-07 while looking for the weakest load-bearing assumption.
 *
 * Position is over [p0/w, p0*w], w > 1, normalized to p0 = 1. Liquidity L cancels in the
 * value ratio, so it is set to 1 and never passed in.
 */

/** Value of the LP position at price p, for a symmetric range of half-width factor w. */
export function positionValue(p, w) {
  const sa = Math.sqrt(1 / w);
  const sb = Math.sqrt(w);
  if (p <= 1 / w) return (1 / sa - 1 / sb) * p; // fully in token0
  if (p >= w) return sb - sa;                    // fully in token1
  return 2 * Math.sqrt(p) - sa - p / sb;
}

/** Value of simply holding the same entry basket to price p. */
export function hodlValue(p, w) {
  const sa = Math.sqrt(1 / w);
  const sb = Math.sqrt(w);
  const x0 = 1 - 1 / sb; // token0 amount at p=1
  const y0 = 1 - sa;     // token1 amount at p=1
  return y0 + x0 * p;
}

/**
 * IL for a concentrated position over [1/w, w] at price ratio r.
 * w -> Infinity converges to the v2 constant-product formula at rate O(1/sqrt(w));
 * that convergence is asserted as a canary in test/canary.test.js rather than trusted.
 */
export function concentratedIlPct(r, w) {
  if (r === null || r === undefined || Number.isNaN(r) || r < 0) return null;
  if (!(w > 1)) return null;
  if (r === 0) return -100;
  return (positionValue(r, w) / hodlValue(r, w) - 1) * 100;
}

/** Did price leave the band? Then the loss is realized, not impermanent. */
export function outOfRange(r, w) {
  return r <= 1 / w || r >= w;
}

/**
 * The ranges we report at. Same discipline as the liveness gates: report the headline at
 * several, and if the finding flips it is a parameter, not a finding.
 * FULL is the v2-equivalent baseline (what the project shipped before 2026-09-07).
 */
export const RANGES = [
  { label: 'tight', w: 1.25, note: 'active LP, rebalanced band' },
  { label: 'moderate', w: 2, note: 'typical managed position' },
  { label: 'wide', w: 4, note: 'passive wide band' },
  { label: 'full', w: 1e8, note: 'full-range = v2-equivalent, the generous baseline' },
];

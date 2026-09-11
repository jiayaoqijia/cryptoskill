/**
 * wallet.js — read an address's Uniswap v3 positions from The Graph.
 *
 * WHY THIS FILE IS SMALLER THAN YOU EXPECT, AND DELIBERATELY SO
 *
 * The obvious version of "connect your wallet" shows a per-position P&L. We measured the
 * Position entity before writing it (WALLET-CONNECT-NOTES.md, live mainnet, 2026-09-11) and
 * two of its fields do not mean what their names say:
 *
 *   collectedFeesToken0/1 — populates ONLY when the LP calls collect(). Measured: of 150
 *     positions with collectedFeesToken0 == 0, SEVENTY-ONE had feeGrowthInside0LastX128 != 0.
 *     They earned fees and never collected. The field is a WITHDRAWAL record wearing an
 *     EARNINGS name. Using it as fee income tells ~47% of uncollected wallets "you earned $0"
 *     while the chain disagrees.
 *
 *   depositedToken0/1, withdrawnToken0/1 — LIFETIME CUMULATIVE, not entry state. Measured:
 *     75% of live positions look "one-sided" (exactly one token zero), which is not exotic LP
 *     behaviour, it is what a running counter looks like after a withdraw/re-deposit cycle.
 *     So deposited* cannot be read as "position value at entry".
 *
 * Shipping a fee number off collectedFees* would reproduce, inside our own product and pointed
 * at the user's own money, the exact defect this project exists to expose: a metric whose label
 * has drifted from the thing it measures. So we don't.
 *
 * WHAT WE DO SHIP, because these fields ARE reliable:
 *   owner, pool, tickLower/tickUpper, liquidity.
 *
 * Those answer the question that actually upgrades the product: WHICH pools is this wallet in,
 * and AT WHAT RANGE. Every number on the site until now assumed a +/-2x band. A connected
 * wallet doesn't have to assume — we read the real ticks and feed the real range into the
 * existing, tested positionRealized path.
 */

/** Uniswap v3 tick -> price multiplier. price = 1.0001^tick. */
export function tickToPrice(tick) {
  return Math.pow(1.0001, Number(tick));
}

// Uniswap v3's usable tick bounds. A position sitting on both rails is literally full-range.
export const TICK_MIN = -887272;
export const TICK_MAX = 887272;
const TICK_SPAN = TICK_MAX - TICK_MIN;

/**
 * EFFECTIVELY_FULL_RANGE_SPAN -- the fraction of usable tick space above which a position is
 * full-range for every purpose this repo has.
 *
 * NOT a tuned number. Measured (scripts/probe-tick-widths3.mjs, n=1000 live mainnet positions):
 *
 *   spanFrac cutoff | positions classified | worst IL error accepted
 *   0.80            | 98                   | 0.00pp
 *   0.85            | 98                   | 0.00pp
 *   0.90            | 97                   | 0.00pp
 *   0.95            | 97                   | 0.00pp
 *   0.99            | 97                   | 0.00pp
 *
 * The classification is flat across the whole sweep and the IL error is exactly zero, because
 * the underlying distribution has a hole: successive 5% bins from 80% to 95% hold 0, 1, and 0
 * positions. The threshold lives inside that hole, so moving it anywhere sensible changes
 * nothing. That is the repo's gate-cannot-audit-its-estimator rule satisfied: reported at five
 * cutoffs, the winner does not change, therefore a finding rather than a parameter.
 *
 * Why span fraction and not widthX: widthX for these positions reaches 1e26+, which (a) reads
 * as a bug in a UI even when arithmetically correct and (b) is a WORSE classifier -- sweeping
 * widthX cutoffs moved the count 374->370 AND carried non-zero IL error. Span fraction is
 * scale-free and exact.
 */
export const EFFECTIVELY_FULL_RANGE_SPAN = 0.9;

/**
 * Convert a position's tick bounds to the symmetric range-width multiplier the rest of the
 * repo speaks (the "w" in concentratedIlPct(r, w), where the band is [1/w, w] around entry).
 *
 * A real position is rarely symmetric around the current price, so collapsing it to one
 * number loses information. We therefore return BOTH: the true bounds, and the symmetric
 * width that is the position's geometric-mean-equivalent. The caller gets to see the
 * approximation rather than have it hidden.
 *
 * Full-range positions (the v2-equivalent min/max ticks) report widthX = Infinity, which the
 * existing math already handles via its >= 1e6 branch.
 */
export function tickRangeToWidth(tickLower, tickUpper) {
  const lo = Number(tickLower);
  const hi = Number(tickUpper);
  if (!Number.isFinite(lo) || !Number.isFinite(hi) || hi <= lo) return null;

  // Compute widthX in LOG SPACE. Math.pow(1.0001, 887272) overflows to Infinity, so deriving
  // widthX from two separate tickToPrice() calls loses the position before we can classify it.
  const spanFrac = (hi - lo) / TICK_SPAN;
  const widthX = Math.exp((hi - lo) * Math.log(1.0001) / 2);

  // Two distinct things, deliberately kept apart:
  //   onRails      -- the position literally uses the min/max ticks.
  //   fullRange    -- it behaves as full-range, which is what the MATH cares about.
  // An earlier version only tested the rails and so classified 9.7% of positions as
  // full-range while labelling the rest as absurd finite bands (widthX up to 1e26). Measured:
  // above this span threshold the concentrated IL and the full-range IL agree to 0.00pp.
  const onRails = lo <= -887000 && hi >= 887000;
  const fullRange = spanFrac >= EFFECTIVELY_FULL_RANGE_SPAN;

  const pLo = tickToPrice(lo);
  const pHi = tickToPrice(hi);
  // Geometric mean is the right centre for a multiplicative band: sqrt(pLo*pHi) sits exactly
  // halfway between them in log-price, which is the space IL actually lives in. Only
  // meaningful for bands narrow enough to avoid overflow; null when it is not.
  const centre = Number.isFinite(pLo) && Number.isFinite(pHi) && pLo > 0 ? Math.sqrt(pLo * pHi) : null;

  return {
    tickLower: lo,
    tickUpper: hi,
    priceLower: Number.isFinite(pLo) ? pLo : null,
    priceUpper: Number.isFinite(pHi) ? pHi : null,
    centre,
    spanFrac,
    widthX: fullRange ? Infinity : widthX,
    fullRange,
    onRails,
  };
}

const POSITION_FIELDS = `
  id
  owner
  liquidity
  tickLower { tickIdx }
  tickUpper { tickIdx }
  collectedFeesToken0
  collectedFeesToken1
  feeGrowthInside0LastX128
  feeGrowthInside1LastX128
  depositedToken0
  depositedToken1
  withdrawnToken0
  withdrawnToken1
  pool { id feeTier totalValueLockedUSD token0Price }
  token0 { symbol decimals }
  token1 { symbol decimals }
`;

/**
 * Fetch open positions for an owner address.
 *
 * Only liquidity > 0 by default: a closed position has no range to reason about and would
 * just be noise in a "what am I exposed to" view. Pass includeClosed to see everything.
 */
export async function fetchWalletPositions(url, owner, { first = 100, includeClosed = false } = {}) {
  const addr = String(owner || '').toLowerCase();
  if (!/^0x[0-9a-f]{40}$/.test(addr)) {
    return { ok: false, error: `"${owner}" is not a 0x-prefixed 40-hex-character address` };
  }
  const where = includeClosed ? `{owner:"${addr}"}` : `{owner:"${addr}", liquidity_gt:"0"}`;
  const query = `{ positions(first:${Math.min(Number(first) || 100, 500)}, where:${where}, orderBy:liquidity, orderDirection:desc){${POSITION_FIELDS}} }`;

  const r = await fetch(url, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ query }),
  });
  if (!r.ok) return { ok: false, error: `subgraph HTTP ${r.status}` };
  const j = await r.json();
  if (j.errors) return { ok: false, error: String(JSON.stringify(j.errors)).slice(0, 200) };
  return { ok: true, positions: j.data?.positions ?? [] };
}

/**
 * Normalise one raw Position into what we are willing to say about it.
 *
 * The `fees` block is the honest part. We report collected fees as COLLECTED (a withdrawal
 * that definitely happened), and when the fee-growth accumulator is non-zero while collected
 * is zero we say "earned but uncollected, not measurable from this data" -- never $0.
 * `measurable: false` with a reason is the repo-wide rule for "we don't know"; a fabricated
 * zero is the thing we exist to complain about.
 */
export function describePosition(p) {
  const range = tickRangeToWidth(p.tickLower?.tickIdx, p.tickUpper?.tickIdx);
  const collected0 = Number(p.collectedFeesToken0 || 0);
  const collected1 = Number(p.collectedFeesToken1 || 0);
  const growth0 = String(p.feeGrowthInside0LastX128 || '0');
  const growth1 = String(p.feeGrowthInside1LastX128 || '0');
  const anyCollected = collected0 > 0 || collected1 > 0;
  const anyGrowth = growth0 !== '0' || growth1 !== '0';

  const fees = anyCollected
    ? {
        measurable: true,
        basis: 'collected',
        collectedToken0: collected0,
        collectedToken1: collected1,
        note: 'Fees the position has actually collected on-chain. Any fees accrued since the last collect() are NOT included -- the subgraph does not expose them as a balance.',
      }
    : {
        measurable: false,
        basis: anyGrowth ? 'earned-but-uncollected' : 'none-recorded',
        reason: anyGrowth
          ? 'This position has accrued fees (feeGrowthInside != 0) but has never called collect(), so no collected-fee figure exists. Reporting $0 here would be false.'
          : 'No collected fees and no fee growth recorded for this position.',
      };

  return {
    id: p.id,
    owner: p.owner,
    pair: `${p.token0?.symbol ?? '?'}/${p.token1?.symbol ?? '?'}`,
    poolId: p.pool?.id,
    // Token decimals travel WITH the amounts. collectedFees* are raw integer strings; without
    // the scale a routine fee renders as 1,382,961,847,474,539,500,000 -- unreadable and wrong
    // by 18 orders of magnitude. Any consumer formatting these needs the divisor in the same
    // payload, or it will guess.
    token0Decimals: p.token0?.decimals != null ? Number(p.token0.decimals) : null,
    token1Decimals: p.token1?.decimals != null ? Number(p.token1.decimals) : null,
    feeTierPct: p.pool?.feeTier ? Number(p.pool.feeTier) / 10_000 : null,
    poolTvlUsd: p.pool?.totalValueLockedUSD ? Number(p.pool.totalValueLockedUSD) : null,
    liquidity: p.liquidity,
    range: range
      ? {
          tickLower: range.tickLower,
          tickUpper: range.tickUpper,
          widthX: range.fullRange ? null : Number(range.widthX.toFixed(4)),
          fullRange: range.fullRange,
          note: range.fullRange
            ? 'Full-range position (v2-equivalent).'
            : `Position spans a factor of ${(range.widthX * range.widthX).toFixed(2)}x low-to-high; widthX is the symmetric +/-${range.widthX.toFixed(2)}x equivalent used by the IL math.`,
        }
      : null,
    fees,
    // Named so nobody mistakes these for entry state. See the file header.
    cumulative: {
      depositedToken0: Number(p.depositedToken0 || 0),
      depositedToken1: Number(p.depositedToken1 || 0),
      withdrawnToken0: Number(p.withdrawnToken0 || 0),
      withdrawnToken1: Number(p.withdrawnToken1 || 0),
      note: 'LIFETIME CUMULATIVE totals, not a snapshot of the position at entry. A deposit/withdraw/re-deposit cycle produces totals that were never simultaneously true, so these must not be read as position value.',
    },
  };
}

/** The disclosure the UI and the API both surface, so neither can quietly drop it. */
export const WALLET_LIMITS = {
  measured: '2026-09-11, Uniswap v3 mainnet subgraph, n=200 live positions',
  weReport: ['which pools the wallet holds', 'the real tick range of each position', 'realized return at THAT range instead of an assumed one'],
  weDoNotReport: ['per-position fee income when fees are uncollected', 'position value at entry'],
  why: 'collectedFees* is a withdrawal record, not an earnings record: of 150 sampled positions with collectedFeesToken0 == 0, 71 had non-zero feeGrowthInside0LastX128 -- they earned fees and never collected. deposited*/withdrawn* are lifetime cumulative, so 75% of positions read as one-sided. Reporting $0 fees or an entry value from these fields would reproduce the advertised-APR defect this project exists to expose.',
};

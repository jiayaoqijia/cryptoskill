/**
 * walkforward.js — is the finding a fact, or one lucky month?
 *
 * WHY THIS EXISTS. Every number this project published came from ONE 30-day window ending
 * on the day we ran it. That is a single draw. "34-62% of pools mislead" could be a property
 * of DeFi or a property of August 2026, and nothing in the repo could tell the difference.
 * A result measured once is an anecdote with a canary attached.
 *
 * This slices the SAME pools into many overlapping 30-day windows going back ~6 months and
 * re-runs the whole instrument in each one. Every window carries its own stable-pair canary,
 * so a window whose data is bad is marked untrusted instead of quietly averaged in.
 *
 * KNOWN BIAS, STATED NOT HIDDEN: pools are selected by CURRENT volume rank, so the sample is
 * survivorship-biased toward pools that still exist and still trade today. That bias makes
 * historical windows look BETTER than they were (the pools that died are absent), so it works
 * against our own thesis. We report it rather than correct it, because correcting it would
 * require a point-in-time pool ranking the subgraph does not expose.
 */

import { impermanentLossPct, STABLES } from './realized.js';
import { concentratedIlPct, outOfRange } from './concentrated.js';

/**
 * Score one 30-day window out of a longer poolDayData series.
 * `days` is DESC (index 0 = most recent). Window is days[offset .. offset+len-1].
 */
export function scoreWindow(pool, days, offset, len = 30) {
  const slice = days.slice(offset, offset + len);
  if (slice.length < len) return { measurable: false, reason: 'window extends past available history' };

  const entry = slice[slice.length - 1];
  const exit = slice[0];
  const entryTvl = Number(entry.tvlUSD || 0);
  const nowTvl = Number(exit.tvlUSD || 0);
  const pEntry = Number(entry.token0Price || 0);
  const pExit = Number(exit.token0Price || 0);

  if (entryTvl <= 0 || nowTvl <= 0) return { measurable: false, reason: 'zero TVL at a window edge' };
  if (pEntry <= 0 || pExit <= 0) return { measurable: false, reason: 'missing price at a window edge' };

  const ratio = pExit / pEntry;
  if (!(ratio > 0.01 && ratio < 100)) return { measurable: false, reason: 'price ratio outside sane band' };

  const totalFeesUsd = slice.reduce((s, d) => s + Number(d.feesUSD || 0), 0);
  const feeReturnPct = (totalFeesUsd / entryTvl) * 100;
  const ilPct = impermanentLossPct(ratio);
  const realizedPct = feeReturnPct + ilPct;

  const advertisedApr = (Number(exit.feesUSD || 0) / nowTvl) * 365 * 100;
  const realizedApr = (realizedPct / slice.length) * 365;

  const activeDays = slice.filter((d) => Number(d.feesUSD || 0) > 0).length;
  const recent7dVolumeUsd = slice.slice(0, 7).reduce((s, d) => s + Number(d.volumeUSD || 0), 0);

  const sym0 = pool.token0?.symbol ?? '?';
  const sym1 = pool.token1?.symbol ?? '?';

  // Price collapse WITHIN this window only — no lookahead into later data.
  const prices = slice.map((d) => Number(d.token0Price || 0)).filter((p) => p > 0);
  const collapsed = prices.length >= 5 && (prices[0] / Math.max(...prices)) < 0.05;

  return {
    pool: pool.id,
    pair: `${sym0}/${sym1}`,
    measurable: true,
    windowDays: slice.length,
    endDate: new Date(Number(exit.date) * 1000).toISOString().slice(0, 10),
    entryTvlUsd: entryTvl,
    currentTvlUsd: nowTvl,
    priceRatio: ratio,
    feeReturnPct,
    impermanentLossPct: ilPct,
    realizedReturnPct: realizedPct,
    advertisedAprPct: advertisedApr,
    realizedAprPct: realizedApr,
    misleading: advertisedApr > 0 && realizedApr < 0,
    stablePair: STABLES.has(sym0) && STABLES.has(sym1),
    collapsed,
    liveness: { activeDays, recent7dVolumeUsd },
  };
}

/**
 * Aggregate one window across all pools, with its OWN canary. A window that cannot prove its
 * instrument works is returned as untrusted rather than dropped silently — "we could not
 * measure this month" and "this month was fine" must never look the same.
 */
export function summarizeWindow(scored, gate, rangeWidthX) {
  const measurable = scored.filter((s) => s.measurable);
  const stables = measurable.filter((s) => s.stablePair);
  const worstStableIl = stables.length ? Math.max(...stables.map((s) => Math.abs(s.impermanentLossPct))) : null;
  const canaryPassed = worstStableIl !== null && worstStableIl < 1.0;

  const live = measurable.filter((s) => !s.stablePair && !s.collapsed
    && s.liveness.activeDays >= gate.minActiveDays
    && s.liveness.recent7dVolumeUsd > gate.minRecent7dVolumeUsd
    && s.currentTvlUsd > gate.minTvlUsd);

  const withRange = live.map((s) => {
    const il = rangeWidthX ? concentratedIlPct(s.priceRatio, rangeWidthX) : s.impermanentLossPct;
    const rz = s.feeReturnPct + il;
    return { ...s, ilUsed: il, realizedUsed: rz, realizedAprUsed: (rz / s.windowDays) * 365,
      leftBand: rangeWidthX ? outOfRange(s.priceRatio, rangeWidthX) : false };
  });

  const misleading = withRange.filter((s) => s.advertisedAprPct > 0 && s.realizedAprUsed < 0);
  const med = (xs) => {
    if (!xs.length) return null;
    const q = [...xs].sort((a, b) => a - b);
    return q.length % 2 ? q[(q.length - 1) / 2] : (q[q.length / 2 - 1] + q[q.length / 2]) / 2;
  };

  return {
    canary: { stablePairsFound: stables.length, worstAbsIlPct: worstStableIl, passed: canaryPassed },
    trusted: canaryPassed && live.length >= 20,
    n: live.length,
    medianIlPct: med(withRange.map((s) => s.ilUsed)),
    medianRealizedPct: med(withRange.map((s) => s.realizedUsed)),
    medianAdvertisedAprPct: med(withRange.map((s) => s.advertisedAprPct)),
    misleadingCount: misleading.length,
    misleadingPct: withRange.length ? (misleading.length / withRange.length) * 100 : null,
    leftBandCount: withRange.filter((s) => s.leftBand).length,
  };
}

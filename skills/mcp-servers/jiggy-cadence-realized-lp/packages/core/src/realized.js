/**
 * realized.js — the instrument.
 *
 * Advertised LP APR is fees-only and annualized. It has no price term, so it is
 * POSITIVE BY CONSTRUCTION: a pool cannot advertise a loss. That is the defect.
 *
 * Realized return = fee income + impermanent loss (IL is <= 0 always).
 * Both terms come from The Graph's historical poolDayData -- per-day feesUSD and
 * token0Price at each day's close.
 *
 * WHY THE GRAPH AND NOT AN RPC NODE. Not because the data is unreachable -- an earlier
 * version of this comment claimed "there is no RPC path," and that was FALSE. Verified
 * 2026-09-11 against a live archive node: feeGrowthGlobal0X128 is public state, readable
 * at any historical block via eth_call, so a determined engineer CAN reconstruct fee
 * accrual from RPC.
 *
 * What they cannot cheaply do is the rest of it: feeGrowthGlobal is a Q128 accumulator in
 * TOKEN units, so turning it into per-day USD needs (a) an archive node, (b) a block-number
 * lookup for every day boundary, (c) a historical USD price for BOTH tokens at each of
 * those boundaries, and (d) the same again for every pool you want to compare. The Graph
 * publishes that join already computed and consistent across 256 pools and 5 chains.
 *
 * So the honest claim is PRACTICALITY, not impossibility: the indexer is the only route
 * that makes a cross-pool, multi-chain, daily-resolution corpus tractable. Overstating it
 * as "impossible" would be the same defect this file exists to measure -- a claim whose
 * label outruns what was actually checked.
 */

import { concentratedIlPct, outOfRange, RANGES } from './concentrated.js';

const UNISWAP_V3_MAINNET = '5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV';

export { RANGES };

export const STABLES = new Set([
  'USDC', 'USDT', 'DAI', 'FRAX', 'LUSD', 'TUSD', 'USDS', 'USDE',
  'GUSD', 'BUSD', 'PYUSD', 'USDP', 'crvUSD',
]);

/** Default liveness gate. Exported so callers can move it and re-check the finding. */
export const DEFAULT_LIVENESS = { minActiveDays: 25, minRecent7dVolumeUsd: 50_000, minTvlUsd: 250_000 };

export function gatewayUrl(apiKey, subgraphId = UNISWAP_V3_MAINNET) {
  if (!apiKey) throw new Error('GRAPH_API_KEY is required (Subgraph Studio gateway key)');
  return `https://gateway.thegraph.com/api/${apiKey}/subgraphs/id/${subgraphId}`;
}

export async function query(url, graphql, { timeoutMs = 60_000 } = {}) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ query: graphql }),
      signal: ctrl.signal,
    });
    if (!res.ok) throw new Error(`Graph gateway HTTP ${res.status}`);
    const json = await res.json();
    if (json.errors) throw new Error(`Subgraph error: ${JSON.stringify(json.errors).slice(0, 300)}`);
    return json.data;
  } finally {
    clearTimeout(t);
  }
}

/**
 * Constant-product impermanent loss for a price ratio r = price_exit / price_entry.
 * IL(1) = 0, IL(2) = IL(0.5) ≈ -5.72%, IL(0) = -100%. Never positive.
 */
export function impermanentLossPct(r) {
  if (r === null || r === undefined || Number.isNaN(r)) return null;
  if (r < 0) return null;
  if (r === 0) return -100;
  return (2 * Math.sqrt(r) / (1 + r) - 1) * 100;
}

const POOL_FIELDS = `
  id feeTier totalValueLockedUSD
  token0 { id symbol } token1 { id symbol }
  poolDayData(first: $DAYS, orderBy: date, orderDirection: desc) {
    date volumeUSD feesUSD tvlUSD token0Price
  }
`;

export async function fetchPool(url, poolId, days = 30) {
  const data = await query(url, `{ pool(id: "${poolId.toLowerCase()}") {
    ${POOL_FIELDS.replace('$DAYS', String(days))}
  } }`);
  return data?.pool ?? null;
}

/**
 * fetchPoolFrom — poolDayData from a specific entry timestamp forward, not just
 * "the last N days from now." Grok critique #4/Phase 2, 2026-09-10: everything else in
 * this file answers a POOL-level, backward-looking question. A real LP has a specific
 * entry date and a specific range; they want "what have I actually made since then,"
 * not "what did the average LP make in the last 30 days." This is the fetch that
 * question needs -- filtered by date_gte in the subgraph query itself, not sliced
 * client-side out of a fixed-size window that might not reach back far enough.
 */
export async function fetchPoolFrom(url, poolId, entryTimestamp) {
  const data = await query(url, `{ pool(id: "${poolId.toLowerCase()}") {
    id feeTier totalValueLockedUSD
    token0 { id symbol } token1 { id symbol }
    poolDayData(
      first: 1000, orderBy: date, orderDirection: asc,
      where: { date_gte: ${Math.floor(entryTimestamp)} }
    ) { date volumeUSD feesUSD tvlUSD token0Price }
  } }`);
  return data?.pool ?? null;
}

/**
 * positionRealized — the position-level tool. Pool + entry date + your range (+
 * optional current price override for an in-flight position) -> what YOU actually
 * made, not the pool-average headline.
 *
 * Reuses concentratedIlPct/dailyRealizedSeries's own math -- not a second formula --
 * so this can never drift from the pool-level numbers the rest of the site shows.
 * The only new logic here is date-anchoring the fee/price series to the caller's
 * actual entry point instead of "the most recent N days."
 */
/**
 * simulateExit — decision support for a position someone is deciding whether to close TODAY.
 *
 * NOT a new claim. It calls positionRealized (identical math, identical honesty contract:
 * measurable:false rather than a fabricated number, outOfRange rather than silently treating
 * a locked-in loss as still-impermanent) and reframes the SAME figures around the one question
 * a holder actually has at the moment of deciding: "if I closed this right now, what would I
 * actually walk away with, in dollars, on a stake of this size?"
 *
 * WHAT IT DELIBERATELY DOES NOT CLAIM: gas cost and swap slippage on exit. We hold a 1inch
 * SPOT PRICE key, not a verified swap-quote/gas-estimate endpoint -- promising a number from
 * an API surface we have not proven live would be exactly the fabricated-precision defect this
 * project exists to expose, aimed at someone's actual exit decision. So those fields are
 * `unavailable: true` with a stated reason, never a guessed dollar figure. If a swap-quote
 * integration is added later, this is the one place that number would plug in.
 */
function fmtUsd(n) {
  // Sub-dollar amounts keep cents: gas at $0.19 rendered as "$0" reads as free rather than
  // cheap, which is a label drifting from its number in the direction that flatters us.
  const a = Math.abs(n);
  const abs = a > 0 && a < 1 ? a.toFixed(2) : a.toFixed(0);
  return n < 0 ? `-$${abs}` : `$${abs}`;
}

/**
 * exitSlippage -- what consolidating an exited position into ONE token would cost in price impact.
 *
 * THE CONCEPTUAL POINT, which matters more than the arithmetic: closing a v3 position is NOT a
 * swap. decreaseLiquidity + collect hands back BOTH tokens at the current tick -- no trade, no
 * price impact, slippage is exactly zero. Slippage only exists if the holder then CHOOSES to
 * swap one side into the other, which is a separate decision many never make.
 *
 * So a single "exit slippage" number quoted for everyone would be inventing two things at once:
 * the token amounts, and the intent to consolidate. Instead:
 *   - the no-swap path is reported as a measured ZERO, because it genuinely is zero;
 *   - the consolidation path is estimated from the pool's OWN depth, and only when we know the
 *     position's real share of liquidity.
 *
 * Depth estimate: for a constant-product-equivalent slice, price impact of trading size S against
 * reserves R is approximately S / (S + R). We use the pool's current TVL as R, which is
 * conservative for a concentrated pool (real depth at the active tick is thinner than total TVL,
 * so this UNDERSTATES impact) -- stated in the response rather than hidden, and the reason this
 * is labelled an estimate with a bound rather than a quote.
 */
export function exitSlippage({ stakeUsd, poolTvlUsd, feeTierPct = 0.05, consolidate = false } = {}) {
  if (!consolidate) {
    return {
      available: true,
      measured: true,
      slippagePct: 0,
      costUsd: 0,
      note: 'Closing a v3 position returns BOTH tokens at the current tick -- it is not a swap, so price impact is zero. This figure is a measured zero, not an unavailable field.',
    };
  }
  if (!(stakeUsd > 0) || !(poolTvlUsd > 0)) {
    return { available: false, reason: 'need position size and pool TVL to estimate consolidation impact' };
  }
  // Only HALF the position needs swapping to consolidate into one side.
  const swapSize = stakeUsd / 2;
  const impactPct = (swapSize / (swapSize + poolTvlUsd)) * 100;
  const feePct = Number(feeTierPct) || 0;
  const totalPct = impactPct + feePct;
  return {
    available: true,
    measured: false,
    isEstimate: true,
    assumesConsolidationToOneToken: true,
    swapSizeUsd: Number(swapSize.toFixed(2)),
    poolTvlUsd: Number(poolTvlUsd.toFixed(0)),
    priceImpactPct: Number(impactPct.toFixed(4)),
    poolFeePct: feePct,
    slippagePct: Number(totalPct.toFixed(4)),
    costUsd: Number((swapSize * (totalPct / 100)).toFixed(2)),
    note: 'Estimate, and a LOWER BOUND: impact is modelled against total pool TVL, but a concentrated '
      + 'pool\'s depth at the active tick is thinner than its TVL, so real impact is likely higher. '
      + 'Applies only if you choose to swap one side into the other -- closing alone costs zero slippage.',
  };
}

export function simulateExit(pool, rangeWidthX = 2, stakeUsd = 10_000, opts = {}) {
  const pos = positionRealized(pool, rangeWidthX);
  if (!pos.measurable) return pos;
  const feesUsd = stakeUsd * (pos.feeReturnPct / 100);
  const ilUsd = stakeUsd * (pos.impermanentLossPct / 100);
  const netUsd = stakeUsd * (pos.realizedReturnPct / 100);
  const slippage = exitSlippage({
    stakeUsd,
    poolTvlUsd: Number(pool?.totalValueLockedUSD || 0),
    feeTierPct: pool?.feeTier ? Number(pool.feeTier) / 10_000 : 0.05,
    consolidate: Boolean(opts.consolidate),
  });
  const gas = opts.gas ?? { available: false, reason: 'gas not requested; the HTTP and MCP surfaces fetch it live' };
  // Only fold costs into a single number when BOTH are actually known. A partial subtraction
  // (real slippage, missing gas) would read as a complete figure while silently omitting a term
  // -- the same defect this project exists to expose.
  const gasUsd = gas.available ? Number(gas.costUsd) : null;
  const slipUsd = slippage.available ? Number(slippage.costUsd) : null;
  const costsKnown = gasUsd !== null && slipUsd !== null;
  const costTail = costsKnown
    ? `, or ${fmtUsd(netUsd - gasUsd - slipUsd)} after ${fmtUsd(gasUsd)} gas${slipUsd > 0 ? ` and ${fmtUsd(slipUsd)} slippage` : ' (closing alone costs no slippage)'}`
    : '';
  return {
    measurable: true,
    pair: pos.pair,
    entryDate: pos.entryDate,
    asOfDate: pos.latestDate,
    daysHeld: pos.daysHeld,
    rangeWidthX: pos.rangeWidthX,
    stakeUsd,
    feesUsd: Number(feesUsd.toFixed(2)),
    impermanentLossUsd: Number(ilUsd.toFixed(2)),
    netUsd: Number(netUsd.toFixed(2)),
    netPct: pos.realizedReturnPct,
    outOfRange: pos.outOfRange,
    outOfRangeNote: pos.outOfRangeNote,
    gas,
    slippage,
    netAfterCostsUsd: costsKnown ? Number((netUsd - gasUsd - slipUsd).toFixed(2)) : null,
    netAfterCostsNote: costsKnown
      ? `Net of position P&L, ${fmtUsd(gasUsd)} gas, and ${fmtUsd(slipUsd)} slippage.`
      : 'Not computed: gas is unavailable, so subtracting it would invent a number. Use netUsd and add costs yourself.',
    verdict: pos.outOfRange
      ? `Exiting today: ${fmtUsd(netUsd)} net on a $${stakeUsd.toLocaleString()} stake${costTail}. Price already left your range, so this loss is locked in regardless of when you close -- waiting does not un-realize it.`
      : `Exiting today: ${fmtUsd(netUsd)} net on a $${stakeUsd.toLocaleString()} stake (fees ${fmtUsd(feesUsd)}, impermanent loss ${fmtUsd(ilUsd)})${costTail}. Still in range -- this number moves if price moves before you actually close.`,
  };
}

export function positionRealized(pool, rangeWidthX = 2) {
  const days = pool?.poolDayData ?? [];
  // NOTE: fetchPoolFrom returns ASCENDING (oldest first) by construction -- scorePool's
  // days array is DESCENDING. Do not feed one function's array into the other's parser.
  if (days.length < 2) {
    return { measurable: false, reason: `position window has ${days.length} day(s); need at least 2 to bracket entry/now` };
  }
  const entry = days[0];
  const latest = days[days.length - 1];
  const entryTvl = Number(entry.tvlUSD || 0);
  const pEntry = Number(entry.token0Price || 0);
  const pNow = Number(latest.token0Price || 0);
  if (entryTvl <= 0) return { measurable: false, reason: 'zero TVL at entry day' };
  if (!(pEntry > 0) || !(pNow > 0)) return { measurable: false, reason: 'missing price at entry or latest day' };

  const ratio = pNow / pEntry;
  const totalFeesUsd = days.reduce((s, d) => s + Number(d.feesUSD || 0), 0);
  const feeReturnPct = (totalFeesUsd / entryTvl) * 100;
  const il = rangeWidthX >= 1e6
    ? impermanentLossPct(ratio)
    : concentratedIlPct(ratio, rangeWidthX);
  if (il === null) return { measurable: false, reason: `IL unmeasurable at ratio ${ratio.toExponential(2)}` };

  const realizedPct = feeReturnPct + il;
  const n = days.length;
  const realizedAprPct = (realizedPct / n) * 365;
  const out = rangeWidthX < 1e6 && outOfRange(ratio, rangeWidthX);

  return {
    measurable: true,
    pair: `${pool.token0?.symbol ?? '?'}/${pool.token1?.symbol ?? '?'}`,
    entryDate: typeof entry.date === 'number' ? new Date(entry.date * 1000).toISOString().slice(0, 10) : entry.date,
    latestDate: typeof latest.date === 'number' ? new Date(latest.date * 1000).toISOString().slice(0, 10) : latest.date,
    daysHeld: n,
    rangeWidthX,
    entryPrice: pEntry,
    currentPrice: pNow,
    priceRatio: ratio,
    feeReturnPct,
    impermanentLossPct: il,
    realizedReturnPct: realizedPct,
    realizedAprPct,
    outOfRange: out,
    outOfRangeNote: out ? 'Price left this range during the position -- the loss below is REALIZED, not impermanent. Rebalancing would have required active management this instrument does not model.' : null,
    dailySeries: dailyRealizedSeriesFromAscending(days, pEntry),
  };
}

/** Same math as dailyRealizedSeries in scorePool, but takes an ASCENDING array
 * (fetchPoolFrom's native order) instead of reversing a descending one. Kept
 * separate rather than reusing dailyRealizedSeries+reverse to avoid a silent
 * off-by-one if someone "simplifies" this back to one shared helper later
 * without checking which order it expects. */
function dailyRealizedSeriesFromAscending(chrono, pEntry) {
  if (!chrono?.length || !(pEntry > 0)) return null;
  const entryTvl = Number(chrono[0]?.tvlUSD || 0);
  if (entryTvl <= 0) return null;
  let cumFeesUsd = 0;
  const points = [];
  for (const d of chrono) {
    const date = typeof d.date === 'number' ? new Date(d.date * 1000).toISOString().slice(0, 10) : (d.date ?? null);
    cumFeesUsd += Number(d.feesUSD || 0);
    const p = Number(d.token0Price || 0);
    if (p <= 0) { points.push({ date, realizedReturnPct: null }); continue; }
    const ratio = p / pEntry;
    const il = ratio > 0 ? impermanentLossPct(ratio) : null;
    if (il === null) { points.push({ date, realizedReturnPct: null }); continue; }
    points.push({ date, realizedReturnPct: Number(((cumFeesUsd / entryTvl) * 100 + il).toFixed(3)) });
  }
  return points;
}

export async function fetchTopPools(url, { first = 250, minTvlUsd = 250_000, days = 30 } = {}) {
  const data = await query(url, `{ pools(first: ${first}, orderBy: volumeUSD, orderDirection: desc,
      where: { totalValueLockedUSD_gt: "${minTvlUsd}" }) {
    ${POOL_FIELDS.replace('$DAYS', String(days))}
  } }`);
  return data?.pools ?? [];
}

/**
 * Score one pool. Returns null when the window is not measurable — never a
 * fabricated zero. "Unpriceable" must stay distinguishable from "no loss".
 */
export function scorePool(pool) {
  const days = pool?.poolDayData ?? [];
  if (days.length < 25) return { pool: pool?.id, measurable: false, reason: 'window shorter than 25 days' };

  const entry = days[days.length - 1];
  const exit = days[0];
  const entryTvl = Number(entry.tvlUSD || 0);
  const nowTvl = Number(exit.tvlUSD || 0);
  const pEntry = Number(entry.token0Price || 0);
  const pExit = Number(exit.token0Price || 0);

  if (entryTvl <= 0 || nowTvl <= 0) return { pool: pool.id, measurable: false, reason: 'zero TVL at a window edge' };
  if (pEntry <= 0 || pExit <= 0) return { pool: pool.id, measurable: false, reason: 'missing price at a window edge' };

  const ratio = pExit / pEntry;
  if (!(ratio > 0.01 && ratio < 100)) {
    return { pool: pool.id, measurable: false, reason: `price ratio ${ratio.toExponential(2)} outside sane band` };
  }

  const n = days.length;
  const totalFeesUsd = days.reduce((s, d) => s + Number(d.feesUSD || 0), 0);
  const feeReturnPct = (totalFeesUsd / entryTvl) * 100;
  const ilPct = impermanentLossPct(ratio);
  const realizedPct = feeReturnPct + ilPct;

  // What a DEX UI shows: most recent day's fees, annualized on current TVL.
  const advertisedApr = (Number(exit.feesUSD || 0) / nowTvl) * 365 * 100;
  const realizedApr = (realizedPct / n) * 365;

  const activeDays = days.filter((d) => Number(d.feesUSD || 0) > 0).length;
  const recent7dVolumeUsd = days.slice(0, 7).reduce((s, d) => s + Number(d.volumeUSD || 0), 0);

  const sym0 = pool.token0?.symbol ?? '?';
  const sym1 = pool.token1?.symbol ?? '?';

  return {
    pool: pool.id,
    pair: `${sym0}/${sym1}`,
    feeTierPct: Number(pool.feeTier) / 10_000,
    measurable: true,
    windowDays: n,
    entryTvlUsd: entryTvl,
    currentTvlUsd: nowTvl,
    priceRatio: ratio,
    totalFeesUsd,
    feeReturnPct,
    impermanentLossPct: ilPct,
    realizedReturnPct: realizedPct,
    advertisedAprPct: advertisedApr,
    realizedAprPct: realizedApr,
    gapPts: advertisedApr - realizedApr,
    misleading: advertisedApr > 0 && realizedApr < 0,
    stablePair: STABLES.has(sym0) && STABLES.has(sym1),
    liveness: { activeDays, recent7dVolumeUsd },
    collapsed: priceCollapsed(pool),
    byRange: byRange(ratio, feeReturnPct, n, advertisedApr),
    dailySeries: dailyRealizedSeries(days, pEntry),
  };
}

/**
 * Cumulative realized-return series, one point per day, oldest first --
 * for a sparkline. Recomputed from the SAME poolDayData already fetched for
 * the headline number, not a second query. Each point is (fees earned so far
 * / entry TVL) + (impermanent loss AS OF that day's price vs entry price) --
 * so the line can and does go up on a good fee day and down on an adverse
 * price move, same as the headline math, just unrolled day by day.
 *
 * 2026-09-10: independent agent review (kimi-k3, asked to critique the API
 * for agent consumption) correctly called this "chart data wearing an API
 * costume" as shipped -- 30 bare numbers, no dates, silently assumes no
 * missing days. If activeDays < 30 the array still has 30 slots (nulls for
 * missing days) but nothing told the caller WHICH day is which, so an agent
 * computing drawdown or trend has no way to align a spike to a real date.
 * Fixed: each point now carries its own `date` (poolDayData's own YYYY-MM-DD,
 * not back-computed from generatedAt) alongside the value.
 */
function dailyRealizedSeries(daysDesc, pEntry) {
  if (!daysDesc?.length || !(pEntry > 0)) return null;
  const chrono = [...daysDesc].reverse(); // poolDayData arrives desc; sparkline reads oldest->newest
  const entryTvl = Number(chrono[0]?.tvlUSD || 0);
  if (entryTvl <= 0) return null;
  let cumFeesUsd = 0;
  const points = [];
  for (const d of chrono) {
    const date = typeof d.date === 'number'
      ? new Date(d.date * 1000).toISOString().slice(0, 10)
      : (d.date ?? null);
    cumFeesUsd += Number(d.feesUSD || 0);
    const p = Number(d.token0Price || 0);
    if (p <= 0) { points.push({ date, realizedReturnPct: null }); continue; } // missing day: null, never a fabricated 0
    const ratio = p / pEntry;
    const il = ratio > 0 ? impermanentLossPct(ratio) : null;
    if (il === null) { points.push({ date, realizedReturnPct: null }); continue; }
    const feePct = (cumFeesUsd / entryTvl) * 100;
    points.push({ date, realizedReturnPct: Number((feePct + il).toFixed(3)) });
  }
  return points;
}

/**
 * The same pool scored at several concentration ranges. The v2 formula (full-range) is the
 * MOST GENEROUS case for the pool; real v3 LPs concentrate and eat amplified IL. Reporting
 * one range would be picking a parameter, so we report all of them — same discipline as the
 * liveness gates.
 */
export function byRange(ratio, feeReturnPct, windowDays, advertisedApr) {
  const out = {};
  for (const { label, w } of RANGES) {
    const il = concentratedIlPct(ratio, w);
    if (il === null) { out[label] = { measurable: false }; continue; }
    const realizedPct = feeReturnPct + il;
    const realizedApr = (realizedPct / windowDays) * 365;
    out[label] = {
      measurable: true,
      rangeWidthX: w,
      impermanentLossPct: il,
      realizedReturnPct: realizedPct,
      realizedAprPct: realizedApr,
      outOfRange: outOfRange(ratio, w),
      misleading: advertisedApr > 0 && realizedApr < 0,
    };
  }
  return out;
}

/** Pearson correlation. Returns null on a degenerate input rather than NaN. */
export function pearson(xs, ys) {
  const n = xs.length;
  if (n < 3 || ys.length !== n) return null;
  const mx = xs.reduce((a, b) => a + b, 0) / n;
  const my = ys.reduce((a, b) => a + b, 0) / n;
  let sxy = 0, sxx = 0, syy = 0;
  for (let i = 0; i < n; i++) { const a = xs[i] - mx, b = ys[i] - my; sxy += a * b; sxx += a * a; syy += b * b; }
  if (sxx === 0 || syy === 0) return null;
  return sxy / Math.sqrt(sxx * syy);
}

const ranks = (v) => {
  const idx = v.map((x, i) => [x, i]).sort((a, b) => a[0] - b[0]);
  const r = new Array(v.length);
  idx.forEach(([, i], k) => { r[i] = k + 1; });
  return r;
};

/** Spearman = Pearson on ranks. Robust to the fat tail that Pearson chases. */
export function spearman(xs, ys) {
  if (xs.length < 3 || ys.length !== xs.length) return null;
  return pearson(ranks(xs), ranks(ys));
}

/**
 * Price-collapse check. Activity/volume/TVL gates alone let a DEAD TOKEN through:
 * a pool can show 7 active days and real volume for months while the underlying
 * token bleeds to near-zero (UST/WETH survives the activity gate at every
 * cutoff tested 2026-09-06 — this function is the fix). If price fell >99%
 * peak-to-current within the observed window, treat the pool as a collapse,
 * not ordinary volatility: IL alone already prices ordinary moves correctly,
 * this only catches the case a token effectively went to zero.
 */
export function priceCollapsed(pool) {
  const days = pool?.poolDayData ?? [];
  const prices = days.map((d) => Number(d.token0Price || 0)).filter((p) => p > 0);
  if (prices.length < 5) return false;
  const peak = Math.max(...prices);
  const current = prices[0]; // index 0 = most recent (desc order)
  if (peak <= 0) return false;
  // Threshold checked against real depegs, not a guess: UST/USDC on this subgraph
  // bottomed at ~2-6% of peak (2026-09-06 spot check, 5 real pools), never <1%.
  // A <1% cutoff would MISS every one of them. 5% catches all 3 observed depegs
  // in the sample without flagging LINK/WETH-style ordinary volatility (worst
  // ordinary swing seen was ~identical price start/end, ratio ~1).
  return current / peak < 0.05;
}

export function isLive(scored, gate = DEFAULT_LIVENESS) {
  if (!scored?.measurable) return false;
  if (scored.collapsed) return false;
  return scored.liveness.activeDays >= gate.minActiveDays
    && scored.liveness.recent7dVolumeUsd > gate.minRecent7dVolumeUsd
    && scored.currentTvlUsd > gate.minTvlUsd;
}

export function median(xs) {
  if (!xs.length) return null;
  const s = [...xs].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
}

/**
 * Aggregate + SELF-CANARY. Stable/stable pairs must show ~0 IL; if they do not,
 * the instrument is broken and every number here is untrusted. A zero is only
 * evidence if the thing producing it proved it can find a known-present item.
 */
export function summarize(scoredList, gate = DEFAULT_LIVENESS) {
  const measurable = scoredList.filter((s) => s.measurable);
  const stables = measurable.filter((s) => s.stablePair);
  const worstStableIl = stables.length ? Math.max(...stables.map((s) => Math.abs(s.impermanentLossPct))) : null;
  const canary = {
    stablePairsFound: stables.length,
    worstAbsIlPct: worstStableIl,
    passed: worstStableIl !== null && worstStableIl < 1.0,
    note: stables.length
      ? 'stable/stable pairs must show ~0 impermanent loss'
      : 'NO stable/stable pair in sample — canary UNPROVEN, treat results as untrusted',
  };

  const live = measurable.filter((s) => !s.stablePair && isLive(s, gate));
  const misleading = live.filter((s) => s.misleading);

  return {
    canary,
    counts: { fetched: scoredList.length, measurable: measurable.length, liveVolatile: live.length },
    medianAdvertisedAprPct: median(live.map((s) => s.advertisedAprPct)),
    medianRealizedAprPct: median(live.map((s) => s.realizedAprPct)),
    medianGapPts: median(live.map((s) => s.gapPts)),
    misleadingCount: misleading.length,
    misleadingPct: live.length ? (misleading.length / live.length) * 100 : null,
    worstOffenders: [...live].sort((a, b) => b.gapPts - a.gapPts).slice(0, 10),
  };
}

/** Report the headline at several gates. A finding that flips with the knob is a parameter. */
export function sensitivity(scoredList, gates) {
  return gates.map(({ label, gate }) => {
    const s = summarize(scoredList, gate);
    return {
      label,
      n: s.counts.liveVolatile,
      misleadingPct: s.misleadingPct,
      medianGapPts: s.medianGapPts,
    };
  });
}

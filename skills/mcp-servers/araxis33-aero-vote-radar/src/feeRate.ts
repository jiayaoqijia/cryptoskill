import { accruedBetween, type FeeCounter } from "./feeStream.js";

/**
 * What a pool's voters have been earning per day lately, from the continuous fee
 * counters (see feeStream.ts) — the figure the radar will rank by once Aero's
 * Predictive Allocation replaces the weekly epoch on 2026-10-22.
 *
 * Why a trailing 96 hours: an allocation can move every 48 hours under sAERO,
 * so the question is which pools will earn the most over the next 48. Measured
 * on this repo's own counter history (29 reads, 2026-09-27..10-06, fixed
 * prices, ~219 pools with at least 100k votes), the last 96 hours ranked the
 * next 48 hours best: Spearman 0.77 per 10k votes, and a top-10 picked this way
 * collected 78% of what the best possible top-10 did. The last 12 hours did
 * worse (0.72 / 62%) — chasing "where the money is flowing right now" loses to
 * a few days of history. The dollar figure itself is rough (median miss about
 * half), so it is published as an estimate to rank by, not a promise.
 *
 * Fees only. Incentives (bribes) arrive in lumps under the weekly system and
 * will stream per second under Aero; they are added once the new contracts are
 * live rather than modelled now.
 */

/** Hours of history the per-day figure is averaged over. */
export const FEE_RATE_WINDOW_HOURS = 96;
/** Intervals older than this are dropped from the file; a little over the window so a late run still fills it. */
export const FEE_RATE_KEEP_HOURS = 120;
/**
 * The share of the window that must be covered by readable intervals. A CL
 * gauge that collected between two reads leaves that interval unreadable (only
 * the part after the collection is visible), so gaps are normal; the rate is
 * taken over the readable part. Below this coverage there is too little to say.
 */
export const FEE_RATE_MIN_COVERAGE = 0.6;

/** USD that reached one pool's voters between two counter reads; `null` when it could not be read. */
export interface FeeInterval {
  from: string;
  to: string;
  usd: Record<string, number | null>;
}

export interface PoolFeeRate {
  /** Average USD per day that reached this pool's voters over the readable part of the window. */
  usdPerDay: number;
  /** `usdPerDay` for 10,000 votes at the pool's current weight; null when the pool has no votes. */
  usdPerDayPer10k: number | null;
  /** Hours of readable history behind the figure. */
  hours: number;
}

/**
 * On disk the intervals are stored column-wise: pool addresses once in
 * `poolIds`, each interval's USD as an array aligned with it (null = no
 * reading). Keyed by address in every interval the file was ~5x larger, and it
 * is committed four times a day.
 */
export interface FeeRateFile {
  generatedAt: string;
  windowHours: number;
  pools: Record<string, PoolFeeRate>;
  poolIds: string[];
  intervals: { from: string; to: string; usd: (number | null)[] }[];
}

export interface TokenPrice {
  decimals: number;
  /** Zero means the price source had none. */
  priceUsd: number;
}

/**
 * The USD each pool's voters received between two full counter reads. A pool
 * is `null` (unknown, not zero) when its CL gauge collected in between — the
 * part accrued before the collection is invisible — or when a token it earned
 * has no price, since leaving it out would understate the pool. A pool missing
 * from either read is left out entirely.
 */
export function buildFeeInterval(
  prev: readonly FeeCounter[],
  next: readonly FeeCounter[],
  from: string,
  to: string,
  priceOf: (token: string) => TokenPrice | undefined,
): FeeInterval {
  const before = new Map(prev.map((c) => [c.pool, c]));
  const usd: Record<string, number | null> = {};
  for (const c of next) {
    const p = before.get(c.pool);
    if (!p || p.kind !== c.kind) continue;
    if (c.kind === "cl" && p.kind === "cl" && c.gaugeFees.some((v, k) => BigInt(v) < BigInt(p.gaugeFees[k]))) {
      usd[c.pool] = null;
      continue;
    }
    const amounts = accruedBetween(p, c);
    let total = 0;
    let priced = true;
    amounts.forEach((amt, k) => {
      if (amt === 0n) return;
      const price = priceOf(c.tokens[k]);
      if (!price || !(price.priceUsd > 0)) {
        priced = false;
        return;
      }
      total += (Number(amt) / 10 ** price.decimals) * price.priceUsd;
    });
    usd[c.pool] = priced ? total : null;
  }
  return { from, to, usd };
}

/** Keeps the intervals that end within `keepHours` of `now`, oldest first. */
export function pruneFeeIntervals(intervals: readonly FeeInterval[], now: Date, keepHours = FEE_RATE_KEEP_HOURS): FeeInterval[] {
  const cutoff = now.getTime() - keepHours * 3_600_000;
  return intervals.filter((i) => Date.parse(i.to) > cutoff).sort((a, b) => Date.parse(a.from) - Date.parse(b.from));
}

/**
 * One pool's average USD per day over the intervals that end inside the window,
 * skipping the unreadable ones. `null` when the readable part covers less than
 * `FEE_RATE_MIN_COVERAGE` of the window.
 */
export function poolFeeRate(
  intervals: readonly FeeInterval[],
  pool: string,
  now: Date,
  windowHours = FEE_RATE_WINDOW_HOURS,
): { usdPerDay: number; hours: number } | null {
  const start = now.getTime() - windowHours * 3_600_000;
  let usd = 0;
  let ms = 0;
  for (const i of intervals) {
    const from = Date.parse(i.from);
    const to = Date.parse(i.to);
    if (from < start || to > now.getTime()) continue;
    const v = i.usd[pool];
    if (v === null || v === undefined) continue;
    usd += v;
    ms += to - from;
  }
  if (ms < windowHours * 3_600_000 * FEE_RATE_MIN_COVERAGE) return null;
  return { usdPerDay: usd / (ms / 86_400_000), hours: ms / 3_600_000 };
}

/** Per-pool rates for every pool seen in the intervals, with the per-10k figure at the current vote weights. */
export function buildFeeRates(
  intervals: readonly FeeInterval[],
  votes: ReadonlyMap<string, number>,
  now: Date,
): Record<string, PoolFeeRate> {
  const pools = new Set(intervals.flatMap((i) => Object.keys(i.usd)));
  const out: Record<string, PoolFeeRate> = {};
  for (const pool of [...pools].sort()) {
    const r = poolFeeRate(intervals, pool, now);
    if (!r) continue;
    const v = votes.get(pool) ?? 0;
    out[pool] = {
      usdPerDay: round2(r.usdPerDay),
      usdPerDayPer10k: v > 0 ? round4((r.usdPerDay / v) * 10_000) : null,
      hours: Math.round(r.hours * 10) / 10,
    };
  }
  return out;
}

const round2 = (x: number) => Math.round(x * 100) / 100;
const round4 = (x: number) => Math.round(x * 10_000) / 10_000;

/** Packs intervals into the on-disk column form, amounts rounded to cents. */
export function packFeeIntervals(intervals: readonly FeeInterval[]): Pick<FeeRateFile, "poolIds" | "intervals"> {
  const poolIds = [...new Set(intervals.flatMap((i) => Object.keys(i.usd)))].sort();
  return {
    poolIds,
    intervals: intervals.map((i) => ({
      from: i.from,
      to: i.to,
      usd: poolIds.map((p) => {
        const v = i.usd[p];
        return v === null || v === undefined ? null : round2(v);
      }),
    })),
  };
}

/** The inverse of `packFeeIntervals`; tolerates a missing or malformed file by returning nothing. */
export function unpackFeeIntervals(file: Partial<FeeRateFile> | null): FeeInterval[] {
  if (!file || !Array.isArray(file.poolIds) || !Array.isArray(file.intervals)) return [];
  const ids = file.poolIds;
  return file.intervals.map((i) => ({
    from: i.from,
    to: i.to,
    usd: Object.fromEntries(ids.flatMap((p, k) => (i.usd[k] === null || i.usd[k] === undefined ? [] : [[p, i.usd[k]]]))),
  }));
}

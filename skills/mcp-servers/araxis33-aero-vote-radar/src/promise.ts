/**
 * Promise against payout: what the radar said a pool would pay per vote, set
 * beside what the pool actually paid once the epoch closed.
 *
 * `predict.ts` scores the vote weight a pool settles at. This scores the
 * number a reader acts on — dollars per 10,000 veAERO — for the pools the
 * radar ranked highest on the day, which is the claim a post or a vote rests
 * on. Pure functions only: the chain scan lives in `settled.ts`, the printing
 * in `promise-cli.ts`.
 */
import { DEFAULT_MIN_CONSISTENCY } from "./constants.js";
import { WEEKLY_EPOCH, periodStartOf } from "./trend.js";

/** Dollars per this many veAERO — the unit the radar quotes to readers. */
export const PER_VEAERO = 10_000;
/** How many of the day's best-ranked pools are held to their forecast. */
export const TOP_POOLS = 10;
/** A scan counts as "before the vote closed" if it ran at least this long before the epoch ended. */
export const MIN_LEAD_SECONDS = 24 * 3600;

export interface PromiseRow {
  symbol: string;
  pool: string;
  /** What the radar quoted for 10,000 veAERO placed alone in the pool, own vote included (dilution-adjusted basis). */
  forecastUsd: number;
  /** What 10,000 veAERO placed alone in the pool would have earned at the weight it settled at, own vote included. */
  paidUsd: number;
  /** paid ÷ forecast; below 1 means the radar promised too much. */
  ratio: number;
}

export interface EpochPromise {
  epochStart: string;
  scannedAt: string;
  rows: PromiseRow[];
  /** Median of paid ÷ forecast over `rows`. */
  medianRatio: number;
  /** Share of `rows` that paid at least what was forecast. */
  paidAtLeastForecast: number;
  /** Share of `rows` that paid less than half of what was forecast. */
  paidUnderHalf: number;
}

interface SnapshotLike {
  generatedAt?: string;
  pools?: {
    symbol: string;
    pool: string;
    votesVeAero: number;
    consistency: number;
    migrating?: boolean;
    forecastUsd: number;
    dilutionAdjustedValuePerVote: number;
  }[];
}

const median = (xs: number[]): number => {
  const s = [...xs].sort((a, b) => a - b);
  const mid = Math.floor(s.length / 2);
  return s.length % 2 ? s[mid] : (s[mid - 1] + s[mid]) / 2;
};

/**
 * For each settled epoch, the latest scan that still ran at least
 * `MIN_LEAD_SECONDS` before the epoch closed — the last look a voter could
 * have acted on. Snapshots from the epoch still running are dropped.
 */
export function pickScanPerEpoch(
  snapshots: unknown[],
  currentEpochStart: number,
): Map<number, SnapshotLike> {
  const picked = new Map<number, { takenAt: number; snap: SnapshotLike }>();
  for (const raw of snapshots) {
    const snap = raw as SnapshotLike;
    if (!snap.generatedAt || !Array.isArray(snap.pools)) continue;
    const takenAt = Math.floor(Date.parse(snap.generatedAt) / 1000);
    if (!Number.isFinite(takenAt)) continue;
    const epochStart = periodStartOf(takenAt);
    if (epochStart >= currentEpochStart) continue;
    const closesAt = epochStart + WEEKLY_EPOCH.lengthSeconds;
    if (closesAt - takenAt < MIN_LEAD_SECONDS) continue;
    const best = picked.get(epochStart);
    if (!best || takenAt > best.takenAt) picked.set(epochStart, { takenAt, snap });
  }
  return new Map([...picked].map(([k, v]) => [k, v.snap]));
}

/**
 * Holds one scan's best-ranked pools to what they paid. Returns null when the
 * scan has no pool that both qualified (consistent, not migrating) and has a
 * settled answer — an epoch that cannot be scored is left out, not guessed.
 */
export function scoreEpochPromise(
  snap: SnapshotLike,
  epochStart: number,
  settledVotes: Map<string, Map<number, number>>,
  settledUsd: Map<string, Map<number, number>>,
  topPools: number = TOP_POOLS,
  minConsistency: number = DEFAULT_MIN_CONSISTENCY,
): EpochPromise | null {
  // The quote is what PER_VEAERO placed alone in the pool is expected to earn,
  // the voter's own weight included. The per-vote rate on its own is the
  // marginal first vote: a pool with almost no votes shows an enormous one that
  // dilutes to nothing the moment a real vote lands (a first version of this
  // check quoted $3.3M for a pool that paid $20). `dilutionAdjustedValuePerVote`
  // is `forecastUsd` over the weight the pool is expected to settle at, so that
  // weight is recovered by dividing back.
  const candidates = (snap.pools ?? [])
    .filter(
      (p) =>
        !p.migrating &&
        p.consistency >= minConsistency &&
        p.votesVeAero > 0 &&
        p.forecastUsd > 0 &&
        p.dilutionAdjustedValuePerVote > 0,
    )
    .map((p) => {
      const expectedWeight = p.forecastUsd / p.dilutionAdjustedValuePerVote;
      return { p, quote: (p.forecastUsd * PER_VEAERO) / (expectedWeight + PER_VEAERO) };
    })
    .sort((a, b) => b.quote - a.quote);

  const rows: PromiseRow[] = [];
  for (const { p, quote } of candidates) {
    if (rows.length >= topPools) break;
    const address = String(p.pool).toLowerCase();
    const weight = settledVotes.get(address)?.get(epochStart);
    const paid = settledUsd.get(address)?.get(epochStart);
    if (weight === undefined || paid === undefined || weight <= 0) continue;
    const paidUsd = (paid * PER_VEAERO) / (weight + PER_VEAERO);
    rows.push({ symbol: p.symbol, pool: address, forecastUsd: quote, paidUsd, ratio: paidUsd / quote });
  }
  if (rows.length === 0 || !snap.generatedAt) return null;

  return {
    epochStart: new Date(epochStart * 1000).toISOString().slice(0, 10),
    scannedAt: snap.generatedAt,
    rows,
    medianRatio: median(rows.map((r) => r.ratio)),
    paidAtLeastForecast: rows.filter((r) => r.ratio >= 1).length / rows.length,
    paidUnderHalf: rows.filter((r) => r.ratio < 0.5).length / rows.length,
  };
}

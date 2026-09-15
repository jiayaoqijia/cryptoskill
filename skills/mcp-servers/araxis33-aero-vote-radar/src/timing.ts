/**
 * How much of what you are looking at right now survives to the end of the
 * epoch.
 *
 * Every dashboard in this corner of Base, this one included, ranks pools by a
 * per-vote figure computed from the vote weight standing at the moment you
 * load the page. That weight is still moving. So the question a voter actually
 * has — "is this list the list, or will it be someone else's list by Thursday?"
 * — has never been answered with a number, only with a warning that the number
 * is unstable.
 *
 * It can be answered, because the repo has been committing a snapshot of the
 * live tally every six hours since 7 August. Pair each of those scans with the
 * weight its epoch went on to settle at, and the answer falls out: of the ten
 * pools that topped the list at that moment, how many still topped it at close.
 *
 * Two deliberate choices about that measurement:
 *
 * 1. Both rankings use the epoch's *settled* USD. That hands the earlier
 *    ranking perfect foresight about rewards it could not have had, which makes
 *    the survival figure a ceiling: whatever churn is left is caused purely by
 *    votes moving, not by anyone mispredicting fees. A voter reading "6 of 10"
 *    should know the real number is no better than that.
 * 2. Survival is reported separately over three sets of pools, because the
 *    single number over everything is dominated by near-empty gauges where one
 *    voter's arrival halves the rate. Telling a voter their list is worthless
 *    when the part of it they can actually use is fairly stable would be its
 *    own kind of lie.
 */

import { periodStartOf, WEEKLY_EPOCH } from "./trend.js";

/** One pool inside one scan, paired with what its epoch settled at. */
export interface SettledRow {
  address: string;
  symbol: string;
  /** The live vote weight the scan recorded. */
  tally: number;
  /** The weight that epoch closed at. */
  settled: number;
  /** USD the epoch paid voters, at settlement. */
  usd: number;
}

/** One committed scan, placed in the epoch it was taken inside. */
export interface TimingScan {
  takenAt: number;
  epochStart: number;
  /** Hours between the scan and the epoch's close. */
  hoursLeft: number;
  rows: SettledRow[];
}

/**
 * Windows the week is cut into, wide enough that four epochs of six-hourly
 * scans put several readings in each. The labels name the day rather than the
 * hour count because that is how a voter thinks about when they are voting.
 */
export const TRUST_WINDOWS: { label: string; fromHours: number; toHours: number }[] = [
  { label: "Thursday–Friday", fromHours: 120, toHours: 168 },
  { label: "Saturday–Sunday", fromHours: 72, toHours: 120 },
  { label: "Monday–Tuesday", fromHours: 24, toHours: 72 },
  { label: "Wednesday", fromHours: 5, toHours: 24 },
  { label: "final hours", fromHours: 0, toHours: 5 },
];

/** A pool needs this much settled weight to count as more than a near-empty gauge. */
export const THICK_VOTES = 50_000;
/** ...or to have paid this much, which is the other way a pool stops being noise. */
export const RICH_USD = 1_000;
/** Below this many pools a "top ten" is most of the list, and survival is meaningless. */
export const MIN_POOLS_FOR_RANKING = 15;
/** The window a late surge is measured over: the last full day before Wednesday. */
export const SURGE_FROM_HOURS = 24;
export const SURGE_TO_HOURS = 48;
/** Fewer readings than this and one strange week would be the whole signal. */
export const MIN_SURGE_READINGS = 8;
/** Weight change small enough that saying it out loud would be false precision. */
export const SURGE_BADGE_THRESHOLD = 0.25;

export interface RankTrust {
  label: string;
  fromHours: number;
  toHours: number;
  /** Scans that fell in this window. */
  scans: number;
  /** Median of "how many of the top ten were still top ten at close", or null when nothing scorable landed here. */
  keptAll: number | null;
  keptThick: number | null;
  keptRich: number | null;
}

export interface LateMover {
  address: string;
  symbol: string;
  /** Median settled/tally measured a day or two out: +0.8 means the pool ended up 80% heavier. */
  medianSurge: number;
  readings: number;
}

export interface TimingReport {
  generatedAt: string;
  /** ISO dates of the settled epochs the measurement could see. */
  epochs: string[];
  scans: number;
  pools: number;
  observations: number;
  /**
   * Median number of pools a single scan in this measurement could see.
   *
   * Not decoration. Until 2026-09-15 pool discovery dropped every
   * concentrated-liquidity pool, so scans committed before then cover 107 pools
   * where 359 exist. A survival figure measured over those scans is a fact
   * about the third of Aerodrome they contained, while the ranking a visitor
   * reads it beside is drawn from all of it.
   *
   * Publishing the coverage lets the page notice that gap and say so, rather
   * than presenting a number from one universe as a fact about another — the
   * same mistake that kept a 1,000,000 veAERO crossover in this repo for three
   * weeks. It closes on its own as post-fix scans accumulate.
   */
  medianPoolsPerScan: number;
  trust: RankTrust[];
  lateMovers: LateMover[];
}

const median = (values: number[]): number => {
  const sorted = [...values].sort((a, b) => a - b);
  const mid = sorted.length >> 1;
  return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
};

/**
 * Of the ten pools this set ranks highest by USD per vote *now*, how many are
 * still in the top ten once the votes have finished moving.
 *
 * Returns null for a set too small to rank, rather than a flattering number: a
 * "top ten" out of twelve pools would score nine out of ten and mean nothing.
 */
export function topTenSurvivors(rows: SettledRow[]): number | null {
  if (rows.length < MIN_POOLS_FOR_RANKING) return null;
  const byRate = (denominator: (r: SettledRow) => number) =>
    [...rows].sort((a, b) => b.usd / denominator(b) - a.usd / denominator(a)).slice(0, 10);
  const now = byRate((r) => r.tally).map((r) => r.address);
  const atClose = new Set(byRate((r) => r.settled).map((r) => r.address));
  return now.filter((address) => atClose.has(address)).length;
}

/** The window a scan belongs to, or null if it sits outside all of them. */
export function windowFor(hoursLeft: number): (typeof TRUST_WINDOWS)[number] | null {
  return TRUST_WINDOWS.find((w) => hoursLeft >= w.fromHours && hoursLeft < w.toHours) ?? null;
}

/**
 * Turns the scans into the two things the page shows: how much of the ranking
 * holds at each point in the week, and which pools are the ones that move.
 */
export function buildTimingReport(scans: TimingScan[], generatedAt: string = new Date().toISOString()): TimingReport {
  const perWindow = new Map<string, { scans: number; all: number[]; thick: number[]; rich: number[] }>();
  for (const w of TRUST_WINDOWS) perWindow.set(w.label, { scans: 0, all: [], thick: [], rich: [] });

  const surges = new Map<string, { symbol: string; values: number[] }>();
  const epochs = new Set<number>();
  const pools = new Set<string>();
  let observations = 0;

  for (const scan of scans) {
    const w = windowFor(scan.hoursLeft);
    if (!w || scan.rows.length === 0) continue;
    epochs.add(scan.epochStart);
    observations += scan.rows.length;
    for (const r of scan.rows) pools.add(r.address);

    const bucket = perWindow.get(w.label)!;
    bucket.scans++;
    const push = (into: number[], value: number | null) => {
      if (value !== null) into.push(value);
    };
    push(bucket.all, topTenSurvivors(scan.rows));
    push(bucket.thick, topTenSurvivors(scan.rows.filter((r) => r.settled >= THICK_VOTES)));
    push(bucket.rich, topTenSurvivors(scan.rows.filter((r) => r.usd >= RICH_USD)));

    // A surge is only meaningful measured from a fixed distance out. Reading it
    // from every scan would mix "a day before close" with "six days before" and
    // call the difference a property of the pool.
    if (scan.hoursLeft >= SURGE_FROM_HOURS && scan.hoursLeft < SURGE_TO_HOURS) {
      for (const r of scan.rows) {
        const entry = surges.get(r.address) ?? { symbol: r.symbol, values: [] };
        entry.symbol = r.symbol || entry.symbol;
        entry.values.push(r.settled / r.tally);
        surges.set(r.address, entry);
      }
    }
  }

  const trust: RankTrust[] = TRUST_WINDOWS.map((w) => {
    const b = perWindow.get(w.label)!;
    return {
      label: w.label,
      fromHours: w.fromHours,
      toHours: w.toHours,
      scans: b.scans,
      keptAll: b.all.length ? median(b.all) : null,
      keptThick: b.thick.length ? median(b.thick) : null,
      keptRich: b.rich.length ? median(b.rich) : null,
    };
  });

  const lateMovers: LateMover[] = [...surges.entries()]
    .filter(([, v]) => v.values.length >= MIN_SURGE_READINGS)
    .map(([address, v]) => ({ address, symbol: v.symbol, medianSurge: median(v.values) - 1, readings: v.values.length }))
    .filter((m) => Math.abs(m.medianSurge) >= SURGE_BADGE_THRESHOLD)
    .sort((a, b) => b.medianSurge - a.medianSurge);

  return {
    generatedAt,
    epochs: [...epochs].sort((a, b) => a - b).map((t) => new Date(t * 1000).toISOString().slice(0, 10)),
    scans: scans.length,
    pools: pools.size,
    observations,
    // Median rather than mean: one truncated scan should not drag the figure the
    // page compares against today's coverage.
    medianPoolsPerScan: scans.length === 0 ? 0 : Math.round(median(scans.map((s) => s.rows.length))),
    trust,
    lateMovers,
  };
}

/**
 * Places one committed snapshot in the epoch it was taken inside and pairs each
 * pool it recorded with that epoch's settled answer.
 *
 * Returns null when the scan cannot be scored at all — malformed JSON, or one
 * taken inside the epoch still running, which has no answer yet. A pool the
 * chain scan has no settled history for is skipped silently, the same tolerance
 * `observationsFromSnapshot` has and for the same reason: one untracked pool is
 * not a reason to throw away the scan.
 */
export function scanFromSnapshot(
  raw: unknown,
  settledVotes: Map<string, Map<number, number>>,
  settledUsd: Map<string, Map<number, number>>,
  currentEpochStart: number,
): TimingScan | null {
  const snap = raw as { generatedAt?: string; pools?: { pool: string; symbol?: string; votesVeAero: number }[] };
  if (!snap.generatedAt || !Array.isArray(snap.pools)) return null;
  const takenAt = Math.floor(Date.parse(snap.generatedAt) / 1000);
  if (!Number.isFinite(takenAt)) return null;
  const epochStart = periodStartOf(takenAt);
  if (epochStart >= currentEpochStart) return null;

  const rows: SettledRow[] = [];
  for (const p of snap.pools) {
    const address = String(p.pool).toLowerCase();
    const settled = settledVotes.get(address)?.get(epochStart);
    const usd = settledUsd.get(address)?.get(epochStart);
    const tally = p.votesVeAero;
    if (!settled || settled <= 0 || !tally || tally <= 0 || usd === undefined || usd <= 0) continue;
    rows.push({ address, symbol: p.symbol ?? address, tally, settled, usd });
  }

  return { takenAt, epochStart, hoursLeft: (epochStart + WEEKLY_EPOCH.lengthSeconds - takenAt) / 3600, rows };
}

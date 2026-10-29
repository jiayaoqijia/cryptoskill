import type { V3ScanGauge, V3Steadiness } from "./v3.js";

/**
 * Hourly history of what each Aero pool pays, kept so the page can tell a pool
 * that pays steadily from one that spiked once (asked for under the Oct 24
 * post: "some just want steady APRs").
 *
 * Each scan adds one sample per pool with at least V3_HISTORY_MIN_WEIGHT sAERO:
 * fees over the last 24 h plus incentives streaming now, as a daily figure for
 * 10,000 sAERO after it dilutes the pool. The rule for "steady" is the one the
 * pre-launch page used on fee-rate windows: at least 75% of the samples pay
 * half the pool's own average or more, over at least a day of samples.
 */

/** Samples older than this are dropped. */
export const V3_HISTORY_KEEP_HOURS = 168;
/** Pools below this weight are left out, as on the page's ranking. */
export const V3_HISTORY_MIN_WEIGHT = 100_000;
/** Fewer samples than this say too little about a pool. */
export const V3_STEADY_MIN_SAMPLES = 24;
/** Share of samples that must pay at least half the pool's average. */
export const V3_STEADY_SHARE = 0.75;

const PER = 10_000;

/** Columns per pool id ("chain:gauge"), one entry per sample; `null` where the pool wasn't in that scan. */
export interface V3HistoryFile {
  at: string[];
  pools: Record<string, (number | null)[]>;
  /**
   * The radar's own pick at each sample, for its public track record: the pool it
   * ranked first for 10,000 sAERO (96 h of fees plus incentives, after dilution)
   * and what it said that would pay a day. `null` before this was recorded (28.10).
   */
  picks?: (V3Pick | null)[];
}

export interface V3Pick {
  pool: string;
  per10k: number;
}

/** The pool the page ranks first for 10,000 sAERO, the same figures as its table. */
export function topPick(gauges: readonly V3ScanGauge[]): V3Pick | null {
  let best: V3Pick | null = null;
  for (const g of gauges) {
    if (g.weight < V3_HISTORY_MIN_WEIGHT) continue;
    const per10k = ((g.feesUsdPerDay + g.incentivesUsdPerDay) * PER) / (g.weight + PER);
    if (!best || per10k > best.per10k) best = { pool: poolKey(g), per10k: Math.round(per10k * 1e4) / 1e4 };
  }
  return best;
}

export const poolKey = (g: Pick<V3ScanGauge, "chain" | "gauge">) => `${g.chain}:${g.gauge.toLowerCase()}`;

/** What 10,000 sAERO would earn a day in the pool now, after diluting it. */
export function per10kNow(g: Pick<V3ScanGauge, "fees24hUsdPerDay" | "incentivesUsdPerDay" | "weight">): number {
  return ((g.fees24hUsdPerDay + g.incentivesUsdPerDay) * PER) / (g.weight + PER);
}

/** Adds this scan as a sample and drops samples older than `keepHours`. */
export function appendV3Sample(
  file: V3HistoryFile | null,
  gauges: readonly V3ScanGauge[],
  now: Date,
  keepHours = V3_HISTORY_KEEP_HOURS,
): V3HistoryFile {
  const at = [...(file?.at ?? [])];
  const pools: Record<string, (number | null)[]> = {};
  for (const [k, v] of Object.entries(file?.pools ?? {})) pools[k] = [...v];
  const picks = [...(file?.picks ?? [])];
  while (picks.length < at.length) picks.unshift(null);
  at.push(now.toISOString());
  picks.push(topPick(gauges));
  for (const col of Object.values(pools)) col.push(null);
  for (const g of gauges) {
    if (g.weight < V3_HISTORY_MIN_WEIGHT) continue;
    const k = poolKey(g);
    pools[k] ??= Array(at.length).fill(null);
    pools[k][at.length - 1] = Math.round(per10kNow(g) * 1e4) / 1e4;
  }
  const cutoff = now.getTime() - keepHours * 3_600_000;
  const drop = at.findIndex((t) => Date.parse(t) >= cutoff);
  const from = drop < 0 ? at.length : drop;
  const out: V3HistoryFile = { at: at.slice(from), pools: {}, picks: picks.slice(from) };
  for (const [k, v] of Object.entries(pools)) {
    const kept = v.slice(from);
    if (kept.some((x) => x !== null)) out.pools[k] = kept;
  }
  return out;
}

/** The pool's steadiness over the history, or undefined while it has fewer than V3_STEADY_MIN_SAMPLES samples. */
export function steadiness(samples: readonly (number | null)[]): V3Steadiness | undefined {
  const vals = samples.filter((x): x is number => x !== null);
  if (vals.length < V3_STEADY_MIN_SAMPLES) return undefined;
  const avg = vals.reduce((a, x) => a + x, 0) / vals.length;
  return {
    held: vals.filter((x) => x >= 0.5 * avg).length,
    of: vals.length,
    avgPer10k: avg,
    minPer10k: Math.min(...vals),
  };
}

export const isSteady = (s: V3Steadiness | undefined) => !!s && s.avgPer10k > 0 && s.held >= V3_STEADY_SHARE * s.of;

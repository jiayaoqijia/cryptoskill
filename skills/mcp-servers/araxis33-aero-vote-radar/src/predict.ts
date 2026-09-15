/**
 * Scoring for "which way of guessing a pool's settled vote weight is actually
 * the most accurate" — the question that decides `--vote-basis`.
 *
 * This exists because the tool got that answer wrong once by reasoning about it
 * instead of measuring it. A basis was picked because its justification sounded
 * conservative, shipped as the default, and only afterwards measured — at which
 * point it turned out to be the least accurate of the three candidates and
 * biased upward by construction. The point of a permanent command is that the
 * measurement costs one command rather than an afternoon, so there is no excuse
 * to skip it next time.
 *
 * Everything here is pure, including `observationsFromSnapshot` below: it turns
 * one already-parsed snapshot and already-fetched settled history into scorable
 * observations, with no git or chain access of its own. Only the actual
 * fetching — walking the snapshot history in git and reading settled epochs off
 * the chain — lives in `predict-cli.ts`.
 */
import { computeVoteStability, expectedDilutedVotes, previousSettledVotes } from "./dilution.js";
import { WEEKLY_EPOCH, periodStartOf } from "./trend.js";
import { MIN_TRAILING_USD, TREND_EPOCHS } from "./constants.js";

export interface PredictionObservation {
  /** The weight the epoch actually settled at. Must be above zero. */
  actual: number;
  /** Each candidate's guess at `actual`, keyed by basis name. */
  predicted: Record<string, number>;
  /**
   * The pool's live weight when the guess was made. Used only to bucket results
   * by pool size — a predictor can be fine on deep pools and useless on thin
   * ones, and an overall median hides exactly that.
   */
  tally: number;
}

export interface PredictorScore {
  name: string;
  observations: number;
  /**
   * Median absolute error on a log scale, expressed as a ratio: 0.17 means the
   * typical guess is 17% out.
   *
   * Log scale because a pool's payout depends on its weight multiplicatively —
   * `value * yours / (weight + yours)`. Being 2x out matters the same whether
   * the pool holds 10k votes or 10M, which an absolute error in votes would
   * completely misrepresent. Median rather than mean because vote weights are
   * heavy-tailed: a handful of pools that swing by 100x would otherwise decide
   * the figure on their own.
   */
  medianAbsError: number;
  /**
   * Median signed error, same ratio scale. Positive means the predictor sits
   * above the weight that turned up.
   *
   * Reported separately from the error because they fail differently and the
   * distinction is what caught the retired basis: it was not merely noisy, it
   * was systematically high, because it took a maximum and so could only ever
   * revise an estimate upward. A biased estimator is not a cautious one — the
   * allocator divides by it, so the bias is spread across every pool it prices.
   */
  medianBias: number;
  /** How often this predictor was the closest of those being compared. */
  closestOn: number;
}

const median = (values: number[]): number => {
  if (values.length === 0) return NaN;
  const sorted = [...values].sort((a, b) => a - b);
  const mid = sorted.length >> 1;
  return sorted.length % 2 === 1 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
};

/** Converts a log-space error back to the ratio it represents, for display. */
export function asRatio(logError: number): number {
  return Math.exp(logError) - 1;
}

/**
 * Scores every named predictor against what actually settled.
 *
 * An observation is skipped for a predictor that has no finite positive guess
 * for it, rather than being scored as infinitely wrong — "this basis had
 * nothing to say here" and "this basis was badly wrong here" are different
 * findings, and `observations` per predictor says which happened. The
 * closest-of counts only consider observations where every predictor produced a
 * usable number, so that column always compares like with like.
 */
export function scorePredictors(
  observations: PredictionObservation[],
  names: string[],
): PredictorScore[] {
  const usable = (value: number | undefined): value is number =>
    typeof value === "number" && Number.isFinite(value) && value > 0;

  const errors = new Map<string, number[]>(names.map((n) => [n, []]));
  const biases = new Map<string, number[]>(names.map((n) => [n, []]));
  const closest = new Map<string, number>(names.map((n) => [n, 0]));

  for (const o of observations) {
    if (!usable(o.actual)) continue;

    for (const name of names) {
      const p = o.predicted[name];
      if (!usable(p)) continue;
      const logError = Math.log(p / o.actual);
      errors.get(name)!.push(Math.abs(logError));
      biases.get(name)!.push(logError);
    }

    const complete = names.every((n) => usable(o.predicted[n]));
    if (!complete) continue;
    let best: string | null = null;
    let bestError = Infinity;
    for (const name of names) {
      const e = Math.abs(Math.log(o.predicted[name] / o.actual));
      if (e < bestError) {
        bestError = e;
        best = name;
      }
    }
    if (best) closest.set(best, closest.get(best)! + 1);
  }

  return names.map((name) => ({
    name,
    observations: errors.get(name)!.length,
    medianAbsError: median(errors.get(name)!),
    medianBias: median(biases.get(name)!),
    closestOn: closest.get(name)!,
  }));
}

export interface SizeBucket {
  label: string;
  /** Inclusive lower bound on the pool's live weight. */
  from: number;
  /** Exclusive upper bound. */
  to: number;
}

/**
 * The pool-size bands results are broken down by. Thin pools are where vote
 * weight swings hardest and where an overall median is least informative, so
 * they get their own band rather than being averaged into the rest.
 */
export const SIZE_BUCKETS: SizeBucket[] = [
  { label: "under 10k votes", from: 0, to: 10_000 },
  { label: "10k - 100k votes", from: 10_000, to: 100_000 },
  { label: "100k - 1M votes", from: 100_000, to: 1_000_000 },
  { label: "1M+ votes", from: 1_000_000, to: Infinity },
];

export function inBucket(o: PredictionObservation, bucket: SizeBucket): boolean {
  return o.tally >= bucket.from && o.tally < bucket.to;
}

/** One pool's observation, paired with the address it came from — see `observationsFromSnapshot`. */
export interface SnapshotObservation {
  address: string;
  observation: PredictionObservation;
}

/**
 * Turns one committed snapshot into the settled-epoch observations it can
 * supply, pairing the live tally it recorded for each pool with the vote
 * weight and USD value that epoch actually settled at, plus the trailing
 * window the radar would have had at the time — all read from
 * `settledVotes`/`settledUsd`, which `predict-cli.ts` builds once from a live
 * chain scan and reuses across every snapshot.
 *
 * Returns null when the snapshot cannot be used at all: malformed JSON, or one
 * taken inside the epoch still running, which has no settled answer yet. A
 * per-pool skip (no settled history for that address, a trailing window that
 * doesn't reach back far enough, or a trailing average below the noise floor)
 * is silent rather than null, matching how `rankPoolsByEfficiency` excludes a
 * pool from a ranking — one thin or untracked pool isn't a reason to distrust
 * the rest of the snapshot.
 */
export function observationsFromSnapshot(
  raw: unknown,
  settledVotes: Map<string, Map<number, number>>,
  settledUsd: Map<string, Map<number, number>>,
  currentEpochStart: number,
  trendEpochs: number = TREND_EPOCHS,
  minTrailingUsd: number = MIN_TRAILING_USD,
): { epochStart: number; entries: SnapshotObservation[] } | null {
  const snap = raw as { generatedAt?: string; pools?: { pool: string; votesVeAero: number }[] };
  if (!snap.generatedAt || !Array.isArray(snap.pools)) return null;
  const takenAt = Math.floor(Date.parse(snap.generatedAt) / 1000);
  if (!Number.isFinite(takenAt)) return null;
  const epochStart = periodStartOf(takenAt);
  // Only epochs whose answer is known. The running one has no answer yet.
  if (epochStart >= currentEpochStart) return null;

  const entries: SnapshotObservation[] = [];
  for (const p of snap.pools) {
    const address = String(p.pool).toLowerCase();
    const votes = settledVotes.get(address);
    const usd = settledUsd.get(address);
    if (!votes || !usd) continue;

    const actual = votes.get(epochStart);
    const tally = p.votesVeAero;
    if (!actual || actual <= 0 || !tally || tally <= 0) continue;

    // The same trailing window the radar itself would have had, strictly
    // older than the epoch being predicted — nothing here has seen the answer.
    const usdWindow: number[] = [];
    const voteWindow: number[] = [];
    for (let k = 1; k <= trendEpochs; k++) {
      const ts = epochStart - k * WEEKLY_EPOCH.lengthSeconds;
      const u = usd.get(ts);
      const v = votes.get(ts);
      if (u === undefined || v === undefined) break;
      usdWindow.push(u);
      voteWindow.push(v);
    }
    if (usdWindow.length < trendEpochs) continue;
    // Same admission gate the rankings use, so this describes the pools the
    // tool would actually put a vote into rather than the whole long tail.
    const trailingAvg = usdWindow.reduce((a, b) => a + b, 0) / usdWindow.length;
    if (trailingAvg < minTrailingUsd) continue;

    const { expectedVotes } = computeVoteStability(voteWindow, false, tally);
    entries.push({
      address,
      observation: {
        actual,
        tally,
        predicted: {
          // Mid-week, so entry 0 of the series is the running epoch: the series
          // handed over is the settled window, with the tally passed separately.
          previous: previousSettledVotes(voteWindow, false, tally),
          current: tally,
          typical: expectedDilutedVotes(tally, expectedVotes),
        },
      },
    });
  }

  return { epochStart, entries };
}

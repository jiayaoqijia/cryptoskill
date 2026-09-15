import { MIN_TRAILING_USD } from "./constants.js";

/**
 * Weekly epoch length in seconds. Aerodrome's voting epochs are exactly one
 * week long and flip at Thursday 00:00 UTC, which falls out of the arithmetic
 * for free: the Unix epoch itself began on a Thursday, so any timestamp floored
 * to a 604800-second boundary *is* a Thursday 00:00 UTC.
 */
export const EPOCH_SECONDS = 604_800;

/**
 * Fewest completed epochs needed before a momentum figure is reported at all.
 * Momentum compares a recent half against an older half, so four is the
 * smallest history that gives each side two observations. With one observation
 * per side a single one-off bribe reads as a trend, which is exactly the
 * mistake `consistency` already exists to guard against.
 */
export const MOMENTUM_MIN_EPOCHS = 4;

/**
 * The stretch of time a set of rewards is counted over, and the boundary a vote
 * has to beat to count toward it.
 *
 * Everything in this project currently measures in weekly epochs, because that
 * is what Aerodrome pays on today. But "epoch" is two facts wearing one word: a
 * length (one week) and an alignment (Thursday 00:00 UTC), and the code got both
 * for free from a single floor operation. That works only for a period whose
 * length divides evenly into Unix time from zero, which a week does and, for
 * instance, a 48-hour window offset from Thursday does not.
 *
 * Aerodrome has announced Predictive Allocation — continuous, rolling
 * allocation in place of the weekly vote — so the period this tool counts over
 * will stop being a constant of the universe and become a parameter of the
 * protocol. Naming it now, while the only value it takes is the weekly epoch,
 * is what turns that from an architecture change into a configuration change:
 * a different window becomes another `RewardPeriod`, not a rewrite of every
 * function that says "epoch".
 *
 * `anchorSeconds` is any instant at which one period began; boundaries are
 * counted from there in both directions, so it does not have to be the first
 * one ever. For the weekly epoch it is 0 — the Unix epoch itself began on a
 * Thursday, which is why flooring to a 604,800-second boundary lands on
 * Thursday 00:00 UTC without anyone arranging it.
 */
export interface RewardPeriod {
  /** How long one period lasts, in seconds. */
  lengthSeconds: number;
  /** A Unix timestamp at which some period began. Boundaries are counted from here. */
  anchorSeconds: number;
  /** What one of these is called in output: "epoch" today, something else later. */
  name: string;
}

/** Aerodrome's weekly voting epoch: one week, aligned to Thursday 00:00 UTC. */
export const WEEKLY_EPOCH: RewardPeriod = {
  lengthSeconds: EPOCH_SECONDS,
  anchorSeconds: 0,
  name: "epoch",
};

/** Start timestamp of the period that `unixSeconds` falls inside. */
export function periodStartOf(unixSeconds: number, period: RewardPeriod = WEEKLY_EPOCH): number {
  const { lengthSeconds, anchorSeconds } = period;
  const elapsed = unixSeconds - anchorSeconds;
  return anchorSeconds + Math.floor(elapsed / lengthSeconds) * lengthSeconds;
}

/**
 * When the period containing `unixSeconds` flips. The boundary belongs to the
 * period opening there, so this is the first instant of the next one rather
 * than the last instant of this one — a vote cast exactly on the boundary gets
 * a whole period, not zero seconds.
 */
export function periodEndOf(unixSeconds: number, period: RewardPeriod = WEEKLY_EPOCH): number {
  return periodStartOf(unixSeconds, period) + period.lengthSeconds;
}

/** Whether `latestTs` belongs to the period still running as of `asOfUnixSeconds`. */
export function isPeriodInProgress(
  latestTs: number,
  asOfUnixSeconds: number,
  period: RewardPeriod = WEEKLY_EPOCH,
): boolean {
  return latestTs >= periodStartOf(asOfUnixSeconds, period);
}

/** Start timestamp of the epoch that `unixSeconds` falls inside. */
export function epochStartOf(unixSeconds: number): number {
  return periodStartOf(unixSeconds, WEEKLY_EPOCH);
}

/**
 * When the epoch containing `unixSeconds` flips — which is also the deadline
 * for a vote to count toward it. A recommendation is only actionable while the
 * epoch it was computed for is still open, and "Thursday 00:00 UTC" is not
 * something most people can turn into "how long have I got" at a glance.
 *
 * The boundary belongs to the epoch starting there, so this returns the first
 * instant of the next epoch rather than the last instant of this one.
 */
export function epochEndOf(unixSeconds: number): number {
  return periodEndOf(unixSeconds, WEEKLY_EPOCH);
}

/**
 * Seconds rendered as `2d 4h`, `4h 12m` or `9m` — the coarsest two units only.
 *
 * Deliberately not accurate to the second. This describes a weekly deadline
 * derived from block timestamps, and a countdown ticking off single seconds
 * would imply a precision the underlying boundary does not have. Non-positive
 * input reads as `0m` rather than as a negative duration, because the caller
 * that hits that case is past the deadline, not owed time.
 */
export function formatDuration(seconds: number): string {
  if (!Number.isFinite(seconds) || seconds <= 0) return "0m";

  const days = Math.floor(seconds / 86_400);
  const hours = Math.floor((seconds % 86_400) / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);

  if (days > 0) return `${days}d ${hours}h`;
  if (hours > 0) return `${hours}h ${minutes}m`;
  return `${minutes}m`;
}

/**
 * Whether a pool's newest epoch is the one still running.
 *
 * This matters more than it looks. `RewardsSugar.epochsByAddress` returns the
 * *current* epoch at index 0, not the most recently completed one, so on a scan
 * taken mid-week that entry holds a few days of bribes and fees rather than a
 * full week's worth. Charting it next to six finished epochs would draw a cliff
 * on every single pool, and averaging it into a "recent" half would report the
 * whole market as fading every week. So the series is published in full and
 * this flag tells consumers which bar is not comparable to the others yet.
 */
export function isEpochInProgress(latestEpochTs: number, asOfUnixSeconds: number): boolean {
  return isPeriodInProgress(latestEpochTs, asOfUnixSeconds, WEEKLY_EPOCH);
}

export interface Trend {
  /**
   * Recent completed epochs' average value divided by the older ones', minus 1.
   * `0.4` means incentives in the recent half ran 40% above the older half.
   * Null when there is no honest basis for the comparison — see `computeTrend`.
   */
  momentum: number | null;
  /** How many completed epochs the figure was drawn from (the in-progress one excluded). */
  completedEpochs: number;
}

const average = (values: number[]): number => values.reduce((a, b) => a + b, 0) / values.length;

/**
 * Splits a pool's epoch history down the middle and asks whether the recent
 * half paid better than the older half.
 *
 * This answers a question the existing metrics genuinely cannot. `trailingAvgUsd`
 * flattens six epochs into one number, and `consistency` says how *evenly* they
 * were spread — but a pool ramping from $50 to $500 and one decaying from $500
 * to $50 can report an identical average and an identical consistency. Direction
 * was simply not in the published data.
 *
 * `epochUsd` is most-recent-first, matching the contract's own ordering.
 *
 * Null momentum means "no comparable baseline", and there are two ways to get
 * there: too little completed history, or an older half too small to divide by.
 *
 * That second guard is not a rounding detail, it is what makes the figure worth
 * showing. A ratio explodes when its denominator is tiny: measured against real
 * Aerodrome data, an unguarded version put a pool that went from $0.02 to $5.75
 * an epoch at the top of the "ramping up" list at +29,286%, ahead of one that
 * genuinely went from $54 to $417. Neither the cents nor the percentage means
 * anything — it is the same reasoning behind `MIN_TRAILING_USD`, applied to the
 * baseline instead of the average, so the same floor is reused as the default.
 *
 * Only the older half is floored, not the recent one: a pool collapsing from
 * $200 an epoch to $12 has a small recent half and that is precisely the move
 * worth reporting.
 *
 * An odd number of completed epochs drops the middle one rather than assigning
 * it to a side, so both halves always carry equal weight.
 */
export function computeTrend(
  epochUsd: number[],
  currentEpochPartial: boolean,
  minBaselineUsd: number = MIN_TRAILING_USD,
): Trend {
  const completed = currentEpochPartial ? epochUsd.slice(1) : epochUsd.slice();
  if (completed.length < MOMENTUM_MIN_EPOCHS) {
    return { momentum: null, completedEpochs: completed.length };
  }

  const half = Math.floor(completed.length / 2);
  const recentAvg = average(completed.slice(0, half));
  const olderAvg = average(completed.slice(completed.length - half));
  if (olderAvg < minBaselineUsd || olderAvg <= 0) {
    return { momentum: null, completedEpochs: completed.length };
  }

  return { momentum: recentAvg / olderAvg - 1, completedEpochs: completed.length };
}

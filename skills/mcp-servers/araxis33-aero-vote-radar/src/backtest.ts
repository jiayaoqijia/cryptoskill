import { allocateAcrossCandidates, type AllocationCandidate } from "./allocator.js";
import { computeConsistency, epochUsd } from "./efficiency.js";
import { computeVoteStability, expectedDilutedVotes } from "./dilution.js";
import { fetchActivePools, fetchPoolEpochs } from "./pools.js";
import { getTokenPrices, countUnpricedTokens } from "./prices.js";
import { BACKTEST_EPOCHS, MIN_TRAILING_USD, TREND_EPOCHS } from "./constants.js";
import { mapWithConcurrency } from "./util.js";

const VE_DECIMALS = 18;

/** One pool's epoch history, most recent first, with `usd` and `votes` index-aligned. */
export interface PoolHistory {
  address: string;
  symbol: string;
  usd: number[];
  votes: number[];
}

export interface BacktestEpochResult {
  /** 0 = the most recently completed epoch, 1 = the one before it, and so on. */
  epochsAgo: number;
  /** How many pools the allocator actually got to choose between, after every filter. */
  candidatesConsidered: number;
  /**
   * How many pools cleared the trailing-value floor but were dropped by
   * `minConsistency`. Zero when no consistency filter was applied. Reported
   * because "the radar earned less this epoch" and "the filter left it three
   * pools to work with" are different findings, and averaging them together
   * is how a filter gets blamed for a bad week it had nothing to do with.
   */
  candidatesExcludedByConsistency: number;
  /** What this tool's allocation would actually have earned that epoch, judging pools on the last settled vote weight. */
  radarUsd: number;
  /**
   * The same allocation run against the weight each pool *typically* settles at
   * rather than its most recent one — the tool's current default basis.
   *
   * Reported beside `radarUsd` rather than replacing it because the change this
   * measures is a change of denominator, and a backtest that showed only the new
   * figure could not answer the question it exists to answer: did switching help.
   */
  radarTypicalUsd: number;
  /** What "put everything in the highest current $/vote pool" would have earned. */
  naiveUsd: number;
  naiveSymbol: string | null;
}

export interface BacktestReport {
  veAeroBudget: number;
  /**
   * The consistency floor that was applied, echoed back so a report read on its
   * own says which strategy it tested. A backtest of the unfiltered strategy is
   * a different claim from a backtest of the filtered one, and the numbers alone
   * do not say which you are looking at.
   */
  minConsistency: number;
  epochsTested: number;
  radarTotalUsd: number;
  /** Total under the typical-weight basis — see `radarTypicalUsd`. */
  radarTypicalTotalUsd: number;
  naiveTotalUsd: number;
  /** radarTotalUsd / naiveTotalUsd - 1, or null when the baseline earned nothing to compare against. */
  upliftPct: number | null;
  /**
   * radarTypicalTotalUsd / radarTotalUsd - 1: what switching the denominator was
   * worth over these epochs, or null when the current-weight basis earned nothing
   * to divide by. This is the figure the default basis has to justify itself on.
   */
  typicalVsCurrentPct: number | null;
  epochsWonByRadar: number;
  /** How many tested epochs the typical-weight basis beat the current-weight one. */
  epochsWonByTypical: number;
  epochs: BacktestEpochResult[];
}

export interface BacktestOptions {
  testEpochs?: number;
  trendEpochs?: number;
  topK?: number;
  minTrailingUsd?: number;
  /**
   * Same 0..1 consistency floor that `pools` and `recommend` accept. Without it
   * the backtest could only ever test the unfiltered strategy, while the vote
   * actually being cast came from a filtered one — so the one number meant to
   * justify the tool described a strategy nobody was running.
   */
  minConsistency?: number;
}

/**
 * Your realised share of a pool's epoch value if you add `x` votes to the `v`
 * votes everyone else cast: value * x / (v + x) — the same dilution model the
 * allocator optimises against, now scored against what the epoch actually paid.
 *
 * `v === 0` (nobody else voted) collapses to x/x = 1, i.e. you'd have taken the
 * whole pot. That is what the maths says and what would really have happened,
 * so it is left as-is rather than special-cased away.
 */
function realisedUsd(epochValueUsd: number, othersVotes: number, myVotes: number): number {
  if (myVotes <= 0) return 0;
  return (epochValueUsd * myVotes) / (othersVotes + myVotes);
}

/**
 * Replays past epochs to answer the question the README can otherwise only
 * assert: does ranking by trailing-average trend and allocating with
 * self-dilution actually beat the naive "vote wherever $/vote looks highest
 * right now" strategy it argues against?
 *
 * For each tested epoch it rebuilds the view of the world as it stood *before*
 * that epoch resolved — trailing average over the preceding `trendEpochs`, and
 * the vote totals as last seen — picks an allocation from that alone, and only
 * then scores it against what the epoch actually paid out. Nothing from the
 * tested epoch feeds the decision, which is what keeps this a backtest rather
 * than a flattering hindsight fit.
 *
 * Honest limits, because a backtest is easy to oversell:
 *   - It assumes your votes wouldn't have changed anyone else's behaviour. At a
 *     large enough budget relative to a pool's votes that is optimistic.
 *   - It only sees pools that still have a live gauge today, so pools that were
 *     attractive and have since been killed are invisible (survivorship bias).
 *   - A handful of weekly epochs is a small sample; treat a single-digit uplift
 *     as noise rather than proof.
 *   - It cannot tell the "previous" and "current" vote bases apart. Live those
 *     differ — one is last epoch's settled weight, the other the running
 *     mid-week tally — but a closed epoch's mid-week tally is not recoverable
 *     from the chain, so here the previous settled weight stands in for both and
 *     the two bases are literally the same number. Separating them needs a
 *     mid-week vantage point, which only the snapshot history provides; that is
 *     what `predict-check` is for.
 */
export function runBacktest(
  histories: PoolHistory[],
  veAeroBudget: number,
  opts: BacktestOptions = {},
): BacktestReport {
  const {
    testEpochs = BACKTEST_EPOCHS,
    trendEpochs = TREND_EPOCHS,
    topK = 15,
    minTrailingUsd = MIN_TRAILING_USD,
    minConsistency = 0,
  } = opts;

  const empty: BacktestReport = {
    veAeroBudget,
    minConsistency,
    epochsTested: 0,
    radarTotalUsd: 0,
    radarTypicalTotalUsd: 0,
    naiveTotalUsd: 0,
    upliftPct: null,
    typicalVsCurrentPct: null,
    epochsWonByRadar: 0,
    epochsWonByTypical: 0,
    epochs: [],
  };

  if (!Number.isFinite(veAeroBudget) || veAeroBudget <= 0) return empty;

  const epochs: BacktestEpochResult[] = [];

  for (let t = 0; t < testEpochs; t++) {
    const candidates: AllocationCandidate[] = [];
    const typicalCandidates: AllocationCandidate[] = [];
    // Outcome data, kept per pool so scoring can't accidentally reach for a
    // different pool's epoch than the one it allocated to. Populated for every
    // pool either strategy could pick, not just the radar's candidates — see
    // below for why the baseline's reach is deliberately wider.
    const outcomes = new Map<string, { usd: number; votes: number }>();
    let naiveBest: { symbol: string; address: string; valuePerVote: number } | null = null;
    let excludedByConsistency = 0;

    for (const h of histories) {
      // The baseline decides from one epoch and is scored on the next, so those
      // two are all it needs. Its eligibility is deliberately checked *before*
      // any of the radar's own gates below.
      //
      // Letting the radar's filters run first would quietly hand the baseline
      // the radar's judgement: `minTrailingUsd` exists to drop thin, spiky,
      // one-off-bribe pools, and those are exactly the pools that show the
      // highest instantaneous $/vote — the mistake this baseline is supposed to
      // represent. Filtering them out of the comparison too leaves both sides
      // choosing from one pre-vetted set, and the backtest measures the radar
      // against a strategy that already thinks like the radar.
      if (h.usd.length <= t + 1 || h.votes.length <= t + 1) continue;

      const knownVotes = h.votes[t + 1];
      if (knownVotes <= 0) continue;

      outcomes.set(h.address, { usd: h.usd[t], votes: h.votes[t] });

      // The naive strategy looks only at the most recent *known* epoch's $/vote.
      const latestValuePerVote = h.usd[t + 1] / knownVotes;
      if (!naiveBest || latestValuePerVote > naiveBest.valuePerVote) {
        naiveBest = { symbol: h.symbol, address: h.address, valuePerVote: latestValuePerVote };
      }

      // Everything from here down is the radar's own admission criteria: a full
      // trailing window strictly older than the tested epoch (anything shorter
      // would silently shrink the estimate's basis), and an average above the
      // noise floor.
      if (h.usd.length <= t + trendEpochs || h.votes.length <= t + trendEpochs) continue;

      const window = h.usd.slice(t + 1, t + 1 + trendEpochs);
      const trailingAvgUsd = window.reduce((a, b) => a + b, 0) / window.length;
      if (trailingAvgUsd < minTrailingUsd) continue;

      // Consistency as it stood *then*, measured over the same trailing window
      // the estimate came from. Recomputing it here rather than reusing today's
      // figure is the whole point: today's consistency has seen the epoch being
      // tested, and feeding that back into the decision would turn the backtest
      // into a hindsight fit — the exact failure the rest of this loop avoids.
      const { consistency } = computeConsistency(window);
      if (consistency < minConsistency) {
        excludedByConsistency++;
        continue;
      }

      candidates.push({
        address: h.address,
        symbol: h.symbol,
        existingVotes: knownVotes,
        expectedUsd: trailingAvgUsd,
      });

      // The same candidate, judged against the weight this pool has typically
      // settled at instead of the single most recent one. The window is the same
      // trailing window the USD average came from and is strictly older than the
      // epoch being tested, so nothing here has seen the outcome.
      //
      // One structural difference from live use, stated rather than hidden:
      // live, "current votes" is the running mid-week tally and the median is
      // taken over settled epochs beside it. Here the most recent settled epoch
      // plays both roles — it is the best stand-in the chain offers for past
      // weeks, since the running tally of an epoch that has closed is not
      // recoverable. That stand-in is the *kinder* of the two to the
      // current-weight basis: a settled weight is steadier than the mid-week
      // tally, which drifts down as holders re-vote. So an improvement measured
      // here is a floor on the live one, not an exaggeration of it.
      const voteWindow = h.votes.slice(t + 1, t + 1 + trendEpochs);
      const { expectedVotes } = computeVoteStability(voteWindow, false, knownVotes);
      typicalCandidates.push({
        address: h.address,
        symbol: h.symbol,
        existingVotes: expectedDilutedVotes(knownVotes, expectedVotes),
        expectedUsd: trailingAvgUsd,
      });
    }

    if (candidates.length === 0) continue;

    // Each basis shortlists by its own rate. Ranking both by the current-weight
    // rate would hand the typical basis a shortlist chosen by the thing it is
    // being tested against, and it could then only ever match, never differ.
    const scoreAllocation = (set: AllocationCandidate[]): number => {
      const ranked = [...set].sort(
        (x, y) => y.expectedUsd / y.existingVotes - x.expectedUsd / x.existingVotes,
      );
      const allocation = allocateAcrossCandidates(ranked.slice(0, topK), veAeroBudget);
      let total = 0;
      for (const a of allocation) {
        const outcome = outcomes.get(a.pool);
        if (outcome) total += realisedUsd(outcome.usd, outcome.votes, a.veAeroAllocated);
      }
      return total;
    };

    const radarUsd = scoreAllocation(candidates);
    const radarTypicalUsd = scoreAllocation(typicalCandidates);

    let naiveUsd = 0;
    if (naiveBest) {
      const outcome = outcomes.get(naiveBest.address);
      if (outcome) naiveUsd = realisedUsd(outcome.usd, outcome.votes, veAeroBudget);
    }

    epochs.push({
      epochsAgo: t,
      candidatesConsidered: candidates.length,
      candidatesExcludedByConsistency: excludedByConsistency,
      radarUsd,
      radarTypicalUsd,
      naiveUsd,
      naiveSymbol: naiveBest?.symbol ?? null,
    });
  }

  const radarTotalUsd = epochs.reduce((a, e) => a + e.radarUsd, 0);
  const radarTypicalTotalUsd = epochs.reduce((a, e) => a + e.radarTypicalUsd, 0);
  const naiveTotalUsd = epochs.reduce((a, e) => a + e.naiveUsd, 0);

  return {
    veAeroBudget,
    minConsistency,
    epochsTested: epochs.length,
    radarTotalUsd,
    radarTypicalTotalUsd,
    naiveTotalUsd,
    upliftPct: naiveTotalUsd > 0 ? radarTotalUsd / naiveTotalUsd - 1 : null,
    typicalVsCurrentPct: radarTotalUsd > 0 ? radarTypicalTotalUsd / radarTotalUsd - 1 : null,
    epochsWonByRadar: epochs.filter((e) => e.radarUsd > e.naiveUsd).length,
    epochsWonByTypical: epochs.filter((e) => e.radarTypicalUsd > e.radarUsd).length,
    epochs,
  };
}

/** Fetches enough live epoch history off Base to replay `testEpochs` past epochs, then runs the backtest. */
export async function backtestLive(
  veAeroBudget: number,
  testEpochs = BACKTEST_EPOCHS,
  trendEpochs = TREND_EPOCHS,
  minConsistency = 0,
): Promise<BacktestReport> {
  const pools = await fetchActivePools();
  const depth = testEpochs + trendEpochs + 1;

  let epochFetchFailures = 0;
  const epochsByPool = await mapWithConcurrency(pools, 8, (p) =>
    fetchPoolEpochs(p.address, depth).catch(() => {
      epochFetchFailures++;
      return [];
    }),
  );
  if (epochFetchFailures > 0) {
    console.error(`(skipped ${epochFetchFailures} pool(s) whose epoch history failed to load)`);
  }

  const allTokens = epochsByPool.flat().flatMap((e) => [
    ...e.bribes.map((b) => b.token),
    ...e.fees.map((f) => f.token),
  ]);
  const prices = await getTokenPrices(allTokens);
  const unpriced = countUnpricedTokens(prices);
  if (unpriced > 0) {
    console.error(
      `(${unpriced} of ${prices.size} reward token(s) have no USD price and count as $0 — pools paid only in those will look empty)`,
    );
  }

  const histories: PoolHistory[] = pools.map((pool, i) => ({
    address: pool.address,
    symbol: pool.symbol,
    usd: epochsByPool[i].map((e) => epochUsd(e, prices)),
    votes: epochsByPool[i].map((e) => Number(e.votes) / 10 ** VE_DECIMALS),
  }));

  return runBacktest(histories, veAeroBudget, { testEpochs, trendEpochs, minConsistency });
}

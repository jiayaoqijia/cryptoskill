import type { PoolEfficiency } from "./efficiency.js";
import { computeVoteStability, expectedDilutedVotes, previousSettledVotes } from "./dilution.js";
import { isEpochInProgress } from "./trend.js";
import { VOTE_BASIS_CROSSOVER_VEAERO } from "./constants.js";

/**
 * Aerodrome's voting UI accepts whole percentages, so a vote is cast on a
 * 1%-of-your-balance lattice whatever the maths would have preferred. Running
 * the greedy allocator in exactly 100 steps makes each step one castable
 * percentage point, which is why this is the granularity and not a resolution
 * knob to be turned up.
 *
 * Finer steps do not buy accuracy here, they lose it. At 400 steps the
 * allocator hands out quarter-points it cannot vote, and `toWholePercentWeights`
 * then rounds them away: on a 1,000,000 veAERO run against live data the
 * allocator spread the budget across 15 pools of which 9 came back under 0.5%
 * and were dropped, so the table printed an expected total that no castable
 * vote could earn.
 *
 * Nothing is given up by quantising. Each pool's return R*x/(V+x) is concave in
 * x, and for a separable sum of concave functions, handing out identical
 * indivisible units to the best marginal each time is exactly optimal for that
 * lattice — not an approximation of the continuous answer, but the best answer
 * to the question actually being asked.
 */
export const WHOLE_PERCENT_STEPS = 100;

export interface AllocationResult {
  pool: string;
  symbol: string;
  weight: number;
  veAeroAllocated: number;
  /** Your share of the pool's expected epoch value at exactly `veAeroAllocated` votes. */
  expectedUsd: number;
  /** Votes already in the pool from everyone else — the V in R*x/(V+x). */
  existingVotes: number;
  /** The pool's whole expected epoch value, before your dilution — the R. */
  poolExpectedUsd: number;
}

export interface WholePercentWeight {
  pool: string;
  symbol: string;
  percent: number;
}

/**
 * Rewrites fractional allocation weights as whole percentages that sum to
 * exactly 100, which is the form Aerodrome's own voting UI actually accepts.
 *
 * Rounding each weight independently doesn't work: six weights of 16.67% each
 * round to 17% and total 102%, which the UI rejects — so the user ends up
 * hand-fudging the last row and quietly voting something other than what was
 * recommended. This uses the largest-remainder (Hamilton) method instead: floor
 * everything, then hand the leftover percentage points one at a time to whoever
 * lost the most to flooring. Weights are normalised by their own sum first, so
 * the leftover is always between 0 and the number of candidates even if the
 * incoming weights carry floating-point drift.
 *
 * Rows that land on 0% are dropped — you cannot cast a 0% vote — and dropping
 * them is safe precisely because they contribute nothing to the 100 total.
 */
export function toWholePercentWeights(allocation: AllocationResult[]): WholePercentWeight[] {
  const totalWeight = allocation.reduce((a, b) => a + b.weight, 0);
  if (allocation.length === 0 || totalWeight <= 0) return [];

  const rows = allocation.map((a) => {
    const raw = (a.weight / totalWeight) * 100;
    const floor = Math.floor(raw);
    return { pool: a.pool, symbol: a.symbol, percent: floor, remainder: raw - floor };
  });

  let deficit = 100 - rows.reduce((a, b) => a + b.percent, 0);

  // Hand out the leftover points to the largest fractional remainders. Ties fall
  // back to the incoming order, which the allocator already sorted by size, so
  // the result is deterministic rather than dependent on sort stability.
  const byRemainder = rows
    .map((row, index) => ({ row, index }))
    .sort((a, b) => b.row.remainder - a.row.remainder || a.index - b.index);

  for (const { row } of byRemainder) {
    if (deficit <= 0) break;
    row.percent++;
    deficit--;
  }

  return rows
    .filter((r) => r.percent > 0)
    .map(({ pool, symbol, percent }) => ({ pool, symbol, percent }));
}

/**
 * Expected USD from the vote a user can actually cast, rather than from the
 * continuous allocation behind it.
 *
 * These are not the same number, for two reasons that pull in opposite
 * directions. Rows too small to round up to 1% are dropped — you cannot cast a
 * 0% vote — so their value should not be claimed. But the largest-remainder
 * rounding then redistributes those points across the rows that survived, so the
 * whole budget still gets voted, and the surviving pools receive *more* veAERO
 * than the allocator penciled in. Summing `expectedUsd` over the kept rows would
 * be wrong in both directions at once.
 *
 * So each surviving pool's share is recomputed at the veAERO its percentage
 * really puts there, against the same R*x/(V+x) dilution model the allocation
 * was chosen under — which is why `AllocationResult` carries V and R and not
 * only the already-diluted figure.
 */
export function expectedUsdForWholePercentVote(
  allocation: AllocationResult[],
  veAeroBudget: number,
): number {
  if (!Number.isFinite(veAeroBudget) || veAeroBudget <= 0) return 0;

  const byPool = new Map(allocation.map((a) => [a.pool, a]));
  let total = 0;

  for (const { pool, percent } of toWholePercentWeights(allocation)) {
    const row = byPool.get(pool);
    if (!row) continue;
    const votes = (percent / 100) * veAeroBudget;
    if (votes <= 0) continue;
    total += (row.poolExpectedUsd * votes) / (row.existingVotes + votes);
  }

  return total;
}

/**
 * veAERO the allocator could not place — always 0 without a `maxWeight` cap,
 * and positive when the cap times the number of candidates cannot absorb the
 * whole budget (five pools capped at 15% can hold 75% of it).
 *
 * This has to be surfaced rather than swallowed, because `toWholePercentWeights`
 * normalises by the weights it is given: hand it a 75%-spent allocation and it
 * scales the rows back up to 100%, quietly restoring the concentration the cap
 * was asked to prevent. Callers check this first.
 */
export function unallocatedVeAero(allocation: AllocationResult[], veAeroBudget: number): number {
  if (!Number.isFinite(veAeroBudget) || veAeroBudget <= 0) return 0;
  const spent = allocation.reduce((a, b) => a + b.veAeroAllocated, 0);
  const left = veAeroBudget - spent;
  // Floating-point dust from summing 100 slices is not a shortfall.
  return left > veAeroBudget * 1e-9 ? left : 0;
}

/**
 * The minimal shape the allocator actually needs. Stated as its own type so
 * callers that aren't holding a full `PoolEfficiency` — notably the backtester,
 * which reconstructs each historical epoch's view of the world — can run the
 * real allocation algorithm instead of reimplementing it and drifting from it.
 */
export interface AllocationCandidate {
  address: string;
  symbol: string;
  existingVotes: number;
  expectedUsd: number;
}

interface Candidate extends AllocationCandidate {
  allocated: number;
  /** Steps taken, kept alongside `allocated` so a cap can be enforced exactly on the lattice. */
  units: number;
}

/**
 * Greedy marginal-value ("water-filling") allocator. Repeatedly gives the next
 * small slice of the veAERO budget to whichever candidate pool currently has the
 * highest marginal expected return, where a pool's expected epoch value R is held
 * fixed at its trailing-average estimate and other voters' votes V are held fixed
 * at their last-observed snapshot (a stated simplifying assumption — this does not
 * model how other voters might react to your allocation).
 *
 * For a pool, your dollar return if you hold x of its (V + x) total votes is
 * R * x / (V + x); its derivative w.r.t. x is R * V / (V + x)^2, which strictly
 * decreases as you add more of your own votes — this is the self-dilution effect
 * naive "just vote where APR is highest" optimizers ignore.
 */
/**
 * Which vote weight to divide a pool's incentives by. Every one of these is a
 * prediction of the weight the epoch will settle at, and they were chosen by
 * measuring that prediction rather than by argument — see `previousSettledVotes`.
 *
 * `"previous"` (default) uses the weight the pool settled at last epoch: the
 * most accurate of the three and unbiased. `"current"` trusts the live mid-week
 * tally — slightly worse, and what this function did before the option existed.
 * `"typical"` takes the larger of the live tally and the pool's usual weight;
 * it measured clearly worst and is kept only so the finding stays reproducible.
 */
export type VoteBasis = "previous" | "current" | "typical";

/**
 * `asOfUnixSeconds` decides whether each pool's newest epoch counts as finished,
 * which is what keeps the still-running week out of the typical-weight figure.
 * It is a parameter rather than a call to the clock so the result is
 * reproducible and testable, matching how `toSnapshotPool` takes `generatedAt`.
 */
export function recommendAllocation(
  ranked: PoolEfficiency[],
  veAeroBudget: number,
  topK = 15,
  steps = WHOLE_PERCENT_STEPS,
  maxWeight = 1,
  voteBasis: VoteBasis = "previous",
  asOfUnixSeconds: number = Math.floor(Date.now() / 1000),
): AllocationResult[] {
  const withVotes = ranked.map((c) => ({
    pool: c,
    votes: votesToDivideBy(c, voteBasis, asOfUnixSeconds),
  }));

  // Shortlisted by the rate implied by the chosen basis rather than by the
  // order the caller happened to pass. Under "current" this reproduces the
  // conventional ranking (`rankPoolsByEfficiency` sorts by exactly this), so
  // nothing moves; under any other basis the incoming order ranks a quantity
  // that is no longer the one being allocated on, and slicing topK from it
  // would shortlist pools the caller is not being shown.
  //
  // A pool nobody has voted on sorts first, matching `marginalValuePerVeAero`'s
  // view that V = 0 is the best case and not the worst — but only when it has
  // something to pay, so a dead pool cannot consume a topK slot.
  const rate = (x: (typeof withVotes)[number]): number => {
    if (x.pool.trailingAvgUsd <= 0) return 0;
    return x.votes > 0 ? x.pool.trailingAvgUsd / x.votes : Number.POSITIVE_INFINITY;
  };
  withVotes.sort((a, b) => rate(b) - rate(a));

  return allocateAcrossCandidates(
    withVotes.slice(0, topK).map(({ pool, votes }) => ({
      address: pool.pool.address,
      symbol: pool.pool.symbol,
      existingVotes: votes,
      expectedUsd: pool.trailingAvgUsd,
    })),
    veAeroBudget,
    steps,
    maxWeight,
  );
}

/** The vote weight one pool should be judged against under the chosen basis. */
export function votesToDivideBy(
  pool: PoolEfficiency,
  voteBasis: VoteBasis,
  asOfUnixSeconds: number,
): number {
  if (voteBasis === "current") return pool.currentVotesVeAero;

  const partial = isEpochInProgress(pool.latestEpochTs, asOfUnixSeconds);
  if (voteBasis === "previous") {
    return previousSettledVotes(pool.epochVotesSeries, partial, pool.currentVotesVeAero);
  }

  const { expectedVotes } = computeVoteStability(
    pool.epochVotesSeries,
    partial,
    pool.currentVotesVeAero,
  );
  return expectedDilutedVotes(pool.currentVotesVeAero, expectedVotes);
}

/**
 * What the next `stepSize` of budget is worth to this candidate, per veAERO, so
 * candidates on very different scales stay comparable.
 *
 * For a pool that already has V votes from other people, your dollar return at x
 * of your own is R*x/(V+x), whose derivative R*V/(V+x)^2 is the usual answer.
 *
 * That derivative is 0 when V is 0 — and a pool nobody else has voted on is the
 * best case there is, not the worst: your share is R*x/(0+x) = R, the whole
 * epoch value, for any x above zero. Left to the derivative alone such a pool
 * would never receive a single step, no matter how large R was. The entire gain
 * arrives with the first slice and nothing is added by the ones after it, which
 * is what the `allocated === 0` branch says.
 *
 * `backtest.ts`'s `realisedUsd` already scores V = 0 this way ("you'd have taken
 * the whole pot"); this keeps the allocator from contradicting the scorer.
 */
function marginalValuePerVeAero(c: Candidate, stepSize: number): number {
  if (c.expectedUsd <= 0) return 0;
  if (c.existingVotes === 0) return c.allocated === 0 ? c.expectedUsd / stepSize : 0;
  const v = c.existingVotes + c.allocated;
  return (c.expectedUsd * c.existingVotes) / (v * v);
}

/**
 * The allocation algorithm itself, over an already-selected candidate set. See
 * `recommendAllocation` for the maths and the assumptions it rests on.
 */
export function allocateAcrossCandidates(
  input: AllocationCandidate[],
  veAeroBudget: number,
  steps = WHOLE_PERCENT_STEPS,
  maxWeight = 1,
): AllocationResult[] {
  // Reject non-finite budgets (e.g. a caller passing Infinity/NaN through) rather
  // than letting `stepSize` become Infinity/NaN and poisoning every allocation
  // below with NaN weights and expected-USD values.
  if (!Number.isFinite(veAeroBudget) || veAeroBudget <= 0) return [];

  const candidates: Candidate[] = input.map((c) => ({ ...c, allocated: 0, units: 0 }));

  const stepSize = veAeroBudget / steps;
  // The cap counted in steps rather than in veAERO, so it is exact on the same
  // lattice the allocation lives on. A cap below one whole step would silently
  // mean "allocate nothing", so it floors to at least one.
  const maxUnits =
    Number.isFinite(maxWeight) && maxWeight > 0 && maxWeight < 1
      ? Math.max(1, Math.floor(maxWeight * steps))
      : steps;

  for (let s = 0; s < steps; s++) {
    let bestIndex = -1;
    let bestMarginal = 0;

    for (let i = 0; i < candidates.length; i++) {
      // A pool already at the cap is out of the running entirely, not merely
      // ranked lower: the point of the cap is that the next-best pool gets the
      // step even when the capped one still has the higher marginal.
      if (candidates[i].units >= maxUnits) continue;
      const marginal = marginalValuePerVeAero(candidates[i], stepSize);
      if (marginal > bestMarginal) {
        bestMarginal = marginal;
        bestIndex = i;
      }
    }

    // Either nothing has positive expected value left, or every candidate that
    // does has hit the cap. The second case leaves part of the budget unspent,
    // which callers must notice rather than paper over — see
    // `unallocatedVeAero`, and the guard in the CLI that refuses to print a
    // vote that would be renormalised back past the cap.
    if (bestIndex === -1) break;
    candidates[bestIndex].allocated += stepSize;
    candidates[bestIndex].units++;
  }

  return candidates
    .filter((c) => c.allocated > 0)
    .map((c) => ({
      pool: c.address,
      symbol: c.symbol,
      weight: c.allocated / veAeroBudget,
      veAeroAllocated: c.allocated,
      expectedUsd: (c.expectedUsd * c.allocated) / (c.existingVotes + c.allocated),
      existingVotes: c.existingVotes,
      poolExpectedUsd: c.expectedUsd,
    }))
    .sort((a, b) => b.veAeroAllocated - a.veAeroAllocated);
}

/**
 * Whether, at this budget, the basis the allocation was priced on is the one
 * the evidence actually supports — and if not, what the other measurement says.
 *
 * The default (`previous`) is the most accurate predictor of the weight an
 * epoch settles at, which is why it is the default; see `previousSettledVotes`.
 * Accuracy over all pools is not the same question as dollars earned, and for
 * a while the two pointed opposite ways below VOTE_BASIS_CROSSOVER_VEAERO, so
 * every small voter was warned that the basis they were on was the one the
 * money measurement did not favour. Re-measured on 2026-09-15 that gap is
 * gone: the sign alternates between +4% and -11% across budgets, which is no
 * edge. The warning went with it — see VOTE_BASIS_CROSSOVER_VEAERO for the
 * numbers. Telling a voter their setting is wrong when it measures the same as
 * the alternative spends their trust and pays them nothing.
 *
 * What remains is the large-budget case, where the reason is structural rather
 * than a replay that can move: past this size a budget is big enough to move
 * the very weight "typical" assumes will arrive.
 *
 * Returns null when the chosen basis is the one the evidence favours at this
 * size. A caveat printed on every run is a caveat nobody reads.
 *
 * `"current"` is grouped with the default deliberately: a replayed epoch has no
 * mid-week tally, so the backtest scored the two as literally the same column,
 * and the finding applies to whichever of them a voter chose.
 */
export function voteBasisCaveat(veAeroBudget: number, voteBasis: VoteBasis): string | null {
  if (!Number.isFinite(veAeroBudget) || veAeroBudget <= 0) return null;

  const belowCrossover = veAeroBudget < VOTE_BASIS_CROSSOVER_VEAERO;

  if (voteBasis === "typical" && !belowCrossover) {
    return (
      `At your size, replaying the last five epochs, this setting earned less than "last epoch's final ` +
      `weight" — about 4% less at 25,000 veAERO and 24% less at 100,000. Above roughly ` +
      `${VOTE_BASIS_CROSSOVER_VEAERO.toLocaleString("en-US")} veAERO your vote is big enough to move a pool's weight itself, ` +
      `so assuming the weight will arrive anyway starts costing you.`
    );
  }

  return null;
}

import { test } from "node:test";
import assert from "node:assert/strict";
import {
  allocateAcrossCandidates,
  expectedUsdForWholePercentVote,
  recommendAllocation,
  toWholePercentWeights,
  unallocatedVeAero,
  voteBasisCaveat,
  votesToDivideBy,
} from "../src/allocator.js";
import type { AllocationResult } from "../src/allocator.js";
import type { PoolEfficiency } from "../src/efficiency.js";
import { VOTE_BASIS_CROSSOVER_VEAERO } from "../src/constants.js";

function fixture(overrides: Partial<PoolEfficiency> & { address: string; symbol: string }): PoolEfficiency {
  return {
    pool: {
      address: overrides.address,
      symbol: overrides.symbol,
      token0: "0xtoken0",
      token1: "0xtoken1",
      gauge: "0xgauge",
      gaugeAlive: true,
    },
    latestEpochTs: 0,
    currentVotesVeAero: 0,
    latestEpochUsd: 0,
    trailingAvgUsd: 0,
    forecastUsd: overrides.trailingAvgUsd ?? 0,
    epochsObserved: 6,
    epochUsdSeries: [100, 110, 120, 130, 120, 140],
    epochVotesSeries: [0, 0, 0, 0, 0, 0],
    currentValuePerVote: 0,
    predictedValuePerVote: 0,
    predictiveEdge: 0,
    volatility: 0,
    consistency: 1,
    latestEpochBribes: [],
    latestEpochFees: [],
    ...overrides,
  };
}

function alloc(symbol: string, weight: number): AllocationResult {
  return {
    pool: `0x${symbol}`,
    symbol,
    weight,
    veAeroAllocated: weight * 1000,
    expectedUsd: 0,
    existingVotes: 0,
    poolExpectedUsd: 0,
  };
}

test("zero budget returns no allocation", () => {
  const ranked = [fixture({ address: "0xA", symbol: "A", currentVotesVeAero: 1000, trailingAvgUsd: 100 })];
  assert.deepEqual(recommendAllocation(ranked, 0), []);
});

test("a single candidate receives the entire budget", () => {
  const ranked = [fixture({ address: "0xA", symbol: "A", currentVotesVeAero: 1000, trailingAvgUsd: 100 })];
  const result = recommendAllocation(ranked, 5000);

  assert.equal(result.length, 1);
  assert.equal(result[0].pool, "0xA");
  assert.ok(Math.abs(result[0].weight - 1) < 1e-6, `weight should be ~1, got ${result[0].weight}`);
  assert.ok(Math.abs(result[0].veAeroAllocated - 5000) < 1, "should allocate ~the full budget");
});

test("allocated veAERO and weights sum back to the requested budget", () => {
  const ranked = [
    fixture({ address: "0xA", symbol: "A", currentVotesVeAero: 1000, trailingAvgUsd: 500 }),
    fixture({ address: "0xB", symbol: "B", currentVotesVeAero: 4000, trailingAvgUsd: 300 }),
    fixture({ address: "0xC", symbol: "C", currentVotesVeAero: 200, trailingAvgUsd: 50 }),
  ];
  const budget = 25_000;
  const result = recommendAllocation(ranked, budget);

  const totalAllocated = result.reduce((sum, r) => sum + r.veAeroAllocated, 0);
  const totalWeight = result.reduce((sum, r) => sum + r.weight, 0);

  assert.ok(Math.abs(totalAllocated - budget) < budget * 0.01, `total allocated (${totalAllocated}) should be ~= budget`);
  assert.ok(Math.abs(totalWeight - 1) < 0.01, `weights (${totalWeight}) should sum to ~1`);
});

test("self-dilution: two pools with identical incentives but a large enough budget get diversified, not dumped into one", () => {
  // Same trailing USD value, same existing votes -> perfectly symmetric, so a
  // budget much larger than either pool's own votes should split roughly evenly
  // instead of an APR-only optimizer's "put it all in pool A" answer.
  const ranked = [
    fixture({ address: "0xA", symbol: "A", currentVotesVeAero: 1000, trailingAvgUsd: 100 }),
    fixture({ address: "0xB", symbol: "B", currentVotesVeAero: 1000, trailingAvgUsd: 100 }),
  ];
  const result = recommendAllocation(ranked, 50_000);

  assert.equal(result.length, 2, "budget large relative to existing votes should spread across both pools");
  const [first, second] = result;
  assert.ok(Math.abs(first.veAeroAllocated - second.veAeroAllocated) < 50_000 * 0.05, "symmetric pools should get near-equal allocation");
});

test("under-voted pool with equal incentive is prioritized first for a small budget", () => {
  // Pool A has the same expected epoch value as B but far fewer existing votes,
  // so its marginal $-per-vote at the margin starts higher -> should be filled first.
  const ranked = [
    fixture({ address: "0xA", symbol: "A", currentVotesVeAero: 100, trailingAvgUsd: 100 }),
    fixture({ address: "0xB", symbol: "B", currentVotesVeAero: 100_000, trailingAvgUsd: 100 }),
  ];
  const result = recommendAllocation(ranked, 10); // tiny budget relative to either pool

  assert.equal(result.length, 1);
  assert.equal(result[0].pool, "0xA");
});

test("a non-finite budget (Infinity/NaN) returns no allocation instead of NaN weights", () => {
  const ranked = [fixture({ address: "0xA", symbol: "A", currentVotesVeAero: 1000, trailingAvgUsd: 100 })];
  assert.deepEqual(recommendAllocation(ranked, Infinity), []);
  assert.deepEqual(recommendAllocation(ranked, NaN), []);
  assert.deepEqual(recommendAllocation(ranked, -Infinity), []);
});

test("toWholePercentWeights: six equal weights sum to exactly 100, not 102", () => {
  // Rounding 16.666% independently gives 17% six times = 102%, which Aerodrome's
  // voting UI rejects. Largest-remainder must land on exactly 100.
  const result = toWholePercentWeights(Array.from({ length: 6 }, (_, i) => alloc(`P${i}`, 1 / 6)));

  assert.equal(result.length, 6);
  assert.equal(result.reduce((a, b) => a + b.percent, 0), 100);
  // Floors are 16 each = 96, so four leftover points are handed out: 4x17 + 2x16.
  assert.deepEqual(
    result.map((r) => r.percent).sort((a, b) => a - b),
    [16, 16, 17, 17, 17, 17],
  );
});

test("toWholePercentWeights: three equal thirds sum to exactly 100", () => {
  const result = toWholePercentWeights([alloc("A", 1 / 3), alloc("B", 1 / 3), alloc("C", 1 / 3)]);
  assert.equal(result.reduce((a, b) => a + b.percent, 0), 100);
  assert.deepEqual(result.map((r) => r.percent).sort((a, b) => a - b), [33, 33, 34]);
});

test("toWholePercentWeights: leftover points go to the largest fractional remainders", () => {
  // Raw: 50.4 / 30.3 / 19.3 -> floors 50/30/19 = 99, one point left over, and
  // A holds the biggest remainder (.4) so it takes it.
  const result = toWholePercentWeights([alloc("A", 0.504), alloc("B", 0.303), alloc("C", 0.193)]);

  assert.equal(result.reduce((a, b) => a + b.percent, 0), 100);
  assert.deepEqual(result, [
    { pool: "0xA", symbol: "A", percent: 51 },
    { pool: "0xB", symbol: "B", percent: 30 },
    { pool: "0xC", symbol: "C", percent: 19 },
  ]);
});

test("toWholePercentWeights: drops rows that round to 0% while still totalling 100", () => {
  const result = toWholePercentWeights([alloc("A", 0.996), alloc("B", 0.004)]);

  assert.equal(result.reduce((a, b) => a + b.percent, 0), 100);
  assert.deepEqual(result, [{ pool: "0xA", symbol: "A", percent: 100 }]);
});

test("toWholePercentWeights: normalises weights that carry floating-point drift", () => {
  // Weights that sum to 0.999... rather than exactly 1 must still produce 100.
  const drifting = [alloc("A", 0.3333), alloc("B", 0.3333), alloc("C", 0.3333)];
  assert.equal(toWholePercentWeights(drifting).reduce((a, b) => a + b.percent, 0), 100);
});

test("toWholePercentWeights: an empty or zero-weight allocation returns nothing", () => {
  assert.deepEqual(toWholePercentWeights([]), []);
  assert.deepEqual(toWholePercentWeights([alloc("A", 0)]), []);
});

test("toWholePercentWeights: a real recommendAllocation result always totals 100", () => {
  const ranked = [
    fixture({ address: "0xA", symbol: "A", currentVotesVeAero: 1000, trailingAvgUsd: 500 }),
    fixture({ address: "0xB", symbol: "B", currentVotesVeAero: 4000, trailingAvgUsd: 300 }),
    fixture({ address: "0xC", symbol: "C", currentVotesVeAero: 200, trailingAvgUsd: 50 }),
  ];
  const percents = toWholePercentWeights(recommendAllocation(ranked, 25_000));

  assert.ok(percents.length > 0);
  assert.equal(percents.reduce((a, b) => a + b.percent, 0), 100);
  assert.ok(percents.every((p) => Number.isInteger(p.percent) && p.percent > 0));
});

test("topK is a hard bound on how many pools can be funded", () => {
  const ranked = [
    fixture({ address: "0xA", symbol: "A", currentVotesVeAero: 1000, trailingAvgUsd: 500 }),
    fixture({ address: "0xB", symbol: "B", currentVotesVeAero: 1000, trailingAvgUsd: 400 }),
    fixture({ address: "0xC", symbol: "C", currentVotesVeAero: 1000, trailingAvgUsd: 300 }),
  ];
  const result = recommendAllocation(ranked, 50_000, /* topK */ 2);

  assert.equal(result.length, 2);
  assert.deepEqual(result.map((r) => r.pool).sort(), ["0xA", "0xB"]);
});

test("the shortlist follows the basis being allocated on, not the order passed in", () => {
  // recommendAllocation used to slice topK straight off the caller's array,
  // which was only ever correct because that order happened to match the metric
  // it allocates on. Under the typical basis it does not: a pool sitting far
  // below the weight it usually settles at ranks high on current votes and low
  // on the weight it will actually be diluted by. Shortlisting by the incoming
  // order would hand the budget to a pool the caller is not being shown.
  const between = fixture({
    address: "0xBETWEEN",
    symbol: "BETWEEN",
    currentVotesVeAero: 1_000, // looks like $1.00/vote right now...
    trailingAvgUsd: 1_000,
    epochVotesSeries: [1_000, 100_000, 100_000, 100_000], // ...but usually carries 100x that
  });
  const steady = fixture({
    address: "0xSTEADY",
    symbol: "STEADY",
    currentVotesVeAero: 10_000,
    trailingAvgUsd: 500, // a real $0.05/vote, and it stays that way
    epochVotesSeries: [10_000, 10_000, 10_000, 10_000],
  });

  // Passed in the order the current-vote ranking would produce: BETWEEN first.
  const typical = recommendAllocation([between, steady], 1_000, 1, undefined, 1, "typical", 0);
  assert.equal(typical[0].pool, "0xSTEADY", "the pool that survives its weight returning is shortlisted");

  const current = recommendAllocation([between, steady], 1_000, 1, undefined, 1, "current", 0);
  assert.equal(current[0].pool, "0xBETWEEN", "the old behaviour is still available");
});

test("the default basis shortlists and prices pools on last epoch's settled weight", () => {
  // "previous" is the actual default in production — recommend/backtest/the MCP
  // tools all fall back to it — but unlike "typical" (tested above) nothing
  // exercised it end-to-end through recommendAllocation/votesToDivideBy: every
  // other test's epochVotesSeries defaults to all-zero, which only reaches
  // previousSettledVotes' fallback branch, not the "read last epoch" branch that
  // real snapshots hit every time. Same fixtures as the "typical" case above:
  // BETWEEN looks cheap on its live tally but usually settles 100x higher.
  const between = fixture({
    address: "0xBETWEEN",
    symbol: "BETWEEN",
    currentVotesVeAero: 1_000,
    trailingAvgUsd: 1_000,
    epochVotesSeries: [1_000, 100_000, 100_000, 100_000],
  });
  const steady = fixture({
    address: "0xSTEADY",
    symbol: "STEADY",
    currentVotesVeAero: 10_000,
    trailingAvgUsd: 500,
    epochVotesSeries: [10_000, 10_000, 10_000, 10_000],
  });

  const previous = recommendAllocation([between, steady], 1_000, 1, undefined, 1, "previous", 0);
  assert.equal(previous[0].pool, "0xSTEADY", "shortlisted by the weight it actually settles at, not its live tally");

  // votesToDivideBy is what recommendAllocation actually calls to get there;
  // exercised directly here since nothing else in this suite calls it.
  assert.equal(votesToDivideBy(between, "previous", 0), 100_000, "reads last epoch's settled weight, not the live tally of 1,000");
  assert.equal(votesToDivideBy(steady, "previous", 0), 10_000);
});

test("allocateAcrossCandidates funds a pool nobody else has voted on", () => {
  // V = 0 is the best case, not the worst: your share is R*x/(0+x) = R, the
  // whole epoch value. The marginal-value derivative R*V/(V+x)^2 is 0 there, so
  // before this was special-cased such a pool never received a single step no
  // matter how large R was — it was silently skipped in favour of any crowded
  // pool with a sliver of value left.
  const result = allocateAcrossCandidates(
    [
      { address: "0xEMPTY", symbol: "EMPTY", existingVotes: 0, expectedUsd: 500 },
      { address: "0xCROWDED", symbol: "CROWDED", existingVotes: 1_000_000, expectedUsd: 100 },
    ],
    1000,
  );

  const empty = result.find((r) => r.symbol === "EMPTY");
  assert.ok(empty, "the unvoted pool must receive an allocation");
  assert.ok(empty.veAeroAllocated > 0);
  // Holding all of the votes means collecting all of the value.
  assert.ok(Math.abs(empty.expectedUsd - 500) < 1e-6);
});

test("allocateAcrossCandidates gives an unvoted pool one slice, not the whole budget", () => {
  // The entire gain lands with the first slice — R*x/x is R whatever x is — so
  // piling more budget in adds nothing. The rest must stay available for pools
  // that can still pay for it.
  const result = allocateAcrossCandidates(
    [
      { address: "0xEMPTY", symbol: "EMPTY", existingVotes: 0, expectedUsd: 500 },
      { address: "0xREAL", symbol: "REAL", existingVotes: 1000, expectedUsd: 400 },
    ],
    1000,
    400,
  );

  const empty = result.find((r) => r.symbol === "EMPTY");
  const real = result.find((r) => r.symbol === "REAL");
  assert.ok(empty && real);
  // One step of a 1,000 veAERO budget over 400 steps.
  assert.ok(Math.abs(empty.veAeroAllocated - 2.5) < 1e-9);
  assert.ok(real.veAeroAllocated > empty.veAeroAllocated);
});

test("expectedUsdForWholePercentVote scores the rounded vote, not the continuous allocation", () => {
  // One pool, so the whole budget lands there and rounding changes nothing:
  // 100% of 1,000 veAERO against 1,000 existing votes collects half of $200.
  const allocation = allocateAcrossCandidates(
    [{ address: "0xA", symbol: "A", existingVotes: 1000, expectedUsd: 200 }],
    1000,
  );
  assert.ok(Math.abs(expectedUsdForWholePercentVote(allocation, 1000) - 100) < 1e-6);
});

test("expectedUsdForWholePercentVote counts the veAERO that dropped rows hand back", () => {
  // Fifteen pools on very different scales, allocated at a deliberately finer
  // granularity than a vote can express: several round to 0% and their points
  // are redistributed to the survivors, so those survivors end up with more
  // veAERO than the allocator penciled in. Summing `expectedUsd` over the kept
  // rows would miss that and understate the vote; summing over every row would
  // claim value from pools the user is told not to vote for.
  //
  // The default granularity no longer produces this situation at all (see the
  // test below), but the function still has to be right for a caller that asks
  // for finer steps, and for an allocation assembled by hand.
  const candidates = Array.from({ length: 15 }, (_, i) => ({
    address: `0x${i}`,
    symbol: `P${i}`,
    existingVotes: 10 ** (1 + (i % 5)),
    expectedUsd: 50 * (i + 1),
  }));
  const budget = 1_000_000;
  const allocation = allocateAcrossCandidates(candidates, budget, 400);
  const percents = toWholePercentWeights(allocation);

  assert.ok(percents.length < allocation.length, "this case must actually drop rows");

  const forVote = expectedUsdForWholePercentVote(allocation, budget);
  const keptRowsOnly = allocation
    .filter((a) => percents.some((p) => p.pool === a.pool))
    .reduce((sum, a) => sum + a.expectedUsd, 0);

  // Strictly more than the kept rows at their original sizes, because the
  // redistributed points buy real extra share in those same pools.
  assert.ok(forVote > keptRowsOnly, `${forVote} should exceed ${keptRowsOnly}`);

  // Recomputed independently from the percentages themselves.
  const expected = percents.reduce((sum, p) => {
    const row = allocation.find((a) => a.pool === p.pool)!;
    const votes = (p.percent / 100) * budget;
    return sum + (row.poolExpectedUsd * votes) / (row.existingVotes + votes);
  }, 0);
  assert.ok(Math.abs(forVote - expected) < 1e-9);
});

test("expectedUsdForWholePercentVote returns 0 for an empty allocation or a bad budget", () => {
  assert.equal(expectedUsdForWholePercentVote([], 1000), 0);
  const allocation = allocateAcrossCandidates(
    [{ address: "0xA", symbol: "A", existingVotes: 1000, expectedUsd: 200 }],
    1000,
  );
  for (const budget of [0, -1, NaN, Infinity]) {
    assert.equal(expectedUsdForWholePercentVote(allocation, budget), 0);
  }
});

test("the default allocation is castable: every row survives rounding to whole percent", () => {
  // The case that motivated the change: 1,000,000 veAERO across fifteen pools
  // on wildly different scales. At 400 steps the allocator handed nine of them
  // shares under 0.5%, which toWholePercentWeights then rounded to nothing, so
  // the printed table described a vote that could not be cast.
  const candidates = Array.from({ length: 15 }, (_, i) => ({
    address: `0x${i}`,
    symbol: `P${i}`,
    existingVotes: 10 ** (1 + (i % 5)),
    expectedUsd: 50 * (i + 1),
  }));
  const budget = 1_000_000;

  const allocation = allocateAcrossCandidates(candidates, budget);
  const percents = toWholePercentWeights(allocation);

  assert.equal(percents.length, allocation.length, "no row may be rounded away");
  assert.equal(
    percents.reduce((a, p) => a + p.percent, 0),
    100,
  );

  // And the finer granularity really did drop rows, so the guarantee above is
  // the change and not an accident of these particular numbers.
  const fine = allocateAcrossCandidates(candidates, budget, 400);
  assert.ok(toWholePercentWeights(fine).length < fine.length);
});

test("on the default lattice, the quoted total and the castable total are the same number", () => {
  // Two figures that used to disagree: what the table totals, and what the vote
  // you can actually type in is worth. On the 1% lattice there is nothing left
  // to round, so they must agree to the cent.
  const candidates = Array.from({ length: 12 }, (_, i) => ({
    address: `0x${i}`,
    symbol: `P${i}`,
    existingVotes: 500 * (i + 1),
    expectedUsd: 40 * (i + 1),
  }));
  const budget = 250_000;

  const allocation = allocateAcrossCandidates(candidates, budget);
  const quoted = allocation.reduce((a, b) => a + b.expectedUsd, 0);
  const castable = expectedUsdForWholePercentVote(allocation, budget);

  assert.ok(Math.abs(quoted - castable) < 1e-6, `${quoted} vs ${castable}`);
});

test("every allocated amount is a whole percent of the budget", () => {
  // Checked across a spread of budgets and candidate counts rather than one
  // case, because the guarantee is arithmetic, not a property of these inputs.
  for (const budget of [1, 137, 25_000, 1_000_000, 8_432_119]) {
    for (const n of [1, 2, 7, 15]) {
      const candidates = Array.from({ length: n }, (_, i) => ({
        address: `0x${i}`,
        symbol: `P${i}`,
        existingVotes: 100 * (i + 1) ** 2,
        expectedUsd: 25 * (i + 1),
      }));

      const allocation = allocateAcrossCandidates(candidates, budget);
      const unit = budget / 100;

      for (const row of allocation) {
        const units = row.veAeroAllocated / unit;
        assert.ok(
          Math.abs(units - Math.round(units)) < 1e-6,
          `${row.symbol} got ${row.veAeroAllocated} of ${budget}, which is ${units} percentage points`,
        );
      }

      const spent = allocation.reduce((a, b) => a + b.veAeroAllocated, 0);
      assert.ok(Math.abs(spent - budget) < budget * 1e-9, `budget conservation: ${spent} vs ${budget}`);
    }
  }
});

test("maxWeight caps a pool that would otherwise take the whole vote", () => {
  // One pool is strictly better at every margin, so uncapped it takes 100%.
  const candidates = [
    { address: "0xA", symbol: "A", existingVotes: 1000, expectedUsd: 5000 },
    { address: "0xB", symbol: "B", existingVotes: 1000, expectedUsd: 50 },
    { address: "0xC", symbol: "C", existingVotes: 1000, expectedUsd: 40 },
  ];
  const budget = 10_000;

  const uncapped = allocateAcrossCandidates(candidates, budget);
  assert.equal(uncapped[0].symbol, "A");

  const capped = allocateAcrossCandidates(candidates, budget, undefined, 0.4);
  const aRow = capped.find((r) => r.symbol === "A")!;

  assert.ok(aRow.weight <= 0.4 + 1e-9, `A took ${aRow.weight}, cap was 0.4`);
  assert.ok(capped.length > 1, "the capped budget has to go somewhere");
  assert.ok(Math.abs(capped.reduce((a, b) => a + b.veAeroAllocated, 0) - budget) < 1e-6);
});

test("the cap is enforced on the lattice, so it is never exceeded by a rounding step", () => {
  const candidates = Array.from({ length: 6 }, (_, i) => ({
    address: `0x${i}`,
    symbol: `P${i}`,
    existingVotes: 100 * (i + 1),
    expectedUsd: 900 - i * 10,
  }));

  for (const cap of [0.2, 0.25, 0.33, 0.5, 0.75]) {
    const allocation = allocateAcrossCandidates(candidates, 50_000, undefined, cap);
    const percents = toWholePercentWeights(allocation);
    for (const p of percents) {
      assert.ok(p.percent <= Math.floor(cap * 100), `cap ${cap}: ${p.symbol} got ${p.percent}%`);
    }
  }
});

test("a cap too tight for the candidate set leaves veAERO unplaced rather than exceeding it", () => {
  // Three pools capped at 20% can hold 60% of the budget and no more. The
  // allocator must stop, not quietly overshoot — and the caller must be able to
  // see it, because toWholePercentWeights would scale the rows back to 100%.
  const candidates = Array.from({ length: 3 }, (_, i) => ({
    address: `0x${i}`,
    symbol: `P${i}`,
    existingVotes: 1000,
    expectedUsd: 500,
  }));
  const budget = 10_000;

  const allocation = allocateAcrossCandidates(candidates, budget, undefined, 0.2);
  const spent = allocation.reduce((a, b) => a + b.veAeroAllocated, 0);

  assert.ok(Math.abs(spent - budget * 0.6) < 1e-6, `expected 60% placed, got ${spent}`);
  assert.ok(Math.abs(unallocatedVeAero(allocation, budget) - budget * 0.4) < 1e-6);

  // The trap this guards: rounding renormalises and hands back 33/33/34.
  const percents = toWholePercentWeights(allocation);
  assert.equal(percents.reduce((a, p) => a + p.percent, 0), 100);
  assert.ok(percents.some((p) => p.percent > 20), "normalisation really does breach the cap");
});

test("unallocatedVeAero reports nothing for an ordinary uncapped allocation", () => {
  const candidates = [
    { address: "0xA", symbol: "A", existingVotes: 1000, expectedUsd: 500 },
    { address: "0xB", symbol: "B", existingVotes: 2000, expectedUsd: 400 },
  ];
  const allocation = allocateAcrossCandidates(candidates, 25_000);

  assert.equal(unallocatedVeAero(allocation, 25_000), 0);
  assert.equal(unallocatedVeAero([], 0), 0);
});

test("unallocatedVeAero reports the whole budget as unplaced when nothing qualified at all", () => {
  // This is the case a caller must check *before* unallocatedVeAero, not after:
  // an empty allocation with a positive budget always reads as "fully unplaced"
  // here, because nothing was spent — it does not by itself mean a --max-weight
  // cap was too tight (the cap could be untouched at its uncapped default of 1),
  // only that recommendAllocation had zero candidate pools to place anything
  // into (e.g. every pool filtered out by --min-consistency). cli.ts's
  // `allocation.length === 0` branch and the equivalent guard in
  // mcp-server.ts's `recommend_allocation` exist to report that distinct cause
  // instead of blaming the cap.
  assert.equal(unallocatedVeAero([], 25_000), 25_000);
});

test("a cap of 1 or above changes nothing", () => {
  const candidates = [
    { address: "0xA", symbol: "A", existingVotes: 1000, expectedUsd: 5000 },
    { address: "0xB", symbol: "B", existingVotes: 1000, expectedUsd: 50 },
  ];
  const plain = allocateAcrossCandidates(candidates, 10_000);
  const capped = allocateAcrossCandidates(candidates, 10_000, undefined, 1);

  assert.deepEqual(capped, plain);
});

/**
 * The caveat exists because two honest measurements disagree about the vote
 * basis and the disagreement depends on position size. What has to hold is that
 * it appears on exactly the side of the crossover where the chosen basis is the
 * unfavoured one: a caveat that fires on every run is noise, and one that never
 * fires is the silence it was written to break.
 */
// Below the crossover the page's default basis is the one the replay favours
// outright — "typical" won every single epoch at 2,000, 5,000 and 10,000 veAERO
// — so there is nothing to warn a small holder about, whichever basis they pick.
test("voteBasisCaveat says nothing to a position below the crossover, on any basis", () => {
  for (const basis of ["previous", "current", "typical"] as const) {
    for (const budget of [2_000, 5_000, 10_000]) {
      assert.equal(voteBasisCaveat(budget, basis), null, `expected silence for ${basis} at ${budget} veAERO`);
    }
  }
});

test("voteBasisCaveat says nothing to a large position using the default basis", () => {
  assert.equal(voteBasisCaveat(VOTE_BASIS_CROSSOVER_VEAERO, "previous"), null);
  assert.equal(voteBasisCaveat(5_000_000, "current"), null);
});

// The one surviving caveat, kept because its reason is structural rather than a
// replay that can move: past this size the budget is large enough to shift the
// very weight "typical" assumes will arrive.
test("voteBasisCaveat tells a large position what the setting costs, in money", () => {
  const caveat = voteBasisCaveat(2_000_000, "typical");
  assert.ok(caveat);
  assert.match(caveat, /20,000 veAERO/);
  // It has to name the loss, not describe the mechanism: "dilution rather than
  // pool-picking decides the outcome" is true and tells a holder nothing about
  // whether to act on it.
  assert.match(caveat, /24% less at 100,000/);
  assert.match(caveat, /earned less/);
});

test("voteBasisCaveat says nothing to a small position that already chose typical", () => {
  assert.equal(voteBasisCaveat(VOTE_BASIS_CROSSOVER_VEAERO - 1, "typical"), null);
});

// The crossover is a measurement, not decoration: at 25,000 veAERO "typical"
// already loses (-4.4%), and by 100,000 it loses 23.7%. A holder that size on
// that basis has to be told.
test("voteBasisCaveat warns a position at or above the crossover that chose typical", () => {
  for (const budget of [VOTE_BASIS_CROSSOVER_VEAERO, 25_000, 100_000]) {
    assert.ok(voteBasisCaveat(budget, "typical"), `expected a caveat for typical at ${budget} veAERO`);
  }
});

test("voteBasisCaveat is silent rather than wrong on a budget that is not a positive number", () => {
  assert.equal(voteBasisCaveat(0, "previous"), null);
  assert.equal(voteBasisCaveat(-1, "previous"), null);
  assert.equal(voteBasisCaveat(Number.NaN, "previous"), null);
  assert.equal(voteBasisCaveat(Number.POSITIVE_INFINITY, "previous"), null);
});

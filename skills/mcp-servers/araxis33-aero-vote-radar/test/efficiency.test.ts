import { test } from "node:test";
import assert from "node:assert/strict";
import { computeConsistency, computePoolEfficiency, epochUsd } from "../src/efficiency.js";
import type { PoolInfo, EpochData } from "../src/pools.js";
import { MIN_TRAILING_USD } from "../src/constants.js";

const pool: PoolInfo = {
  address: "0xpool",
  symbol: "vAMM-TEST/USDC",
  token0: "0xtoken0",
  token1: "0xtoken1",
  gauge: "0xgauge",
  gaugeAlive: true,
};

const prices = new Map([
  ["0xbribe", { price: 2, decimals: 18 }],
  ["0xfee", { price: 1, decimals: 6 }],
]);

function epoch(overrides: Partial<EpochData>): EpochData {
  return { ts: 0, votes: 0n, bribes: [], fees: [], ...overrides };
}

test("epochUsd sums bribes and fees, converted to USD via the price map", () => {
  const e = epoch({
    bribes: [{ token: "0xbribe", amount: 5_000_000_000_000_000_000n }], // 5 * $2
    fees: [{ token: "0xfee", amount: 3_000_000n }], // 3 * $1 (6 decimals)
  });
  assert.equal(epochUsd(e, prices), 13);
});

test("epochUsd treats unpriced tokens as contributing $0 rather than throwing", () => {
  const e = epoch({ bribes: [{ token: "0xunpriced", amount: 1_000_000_000_000_000_000n }] });
  assert.equal(epochUsd(e, prices), 0);
});

test("computePoolEfficiency returns null when there is no epoch history", () => {
  assert.equal(computePoolEfficiency(pool, [], prices), null);
});

test("computePoolEfficiency returns null when the latest epoch has zero recorded votes", () => {
  const epochs = [epoch({ votes: 0n, fees: [{ token: "0xfee", amount: 100_000_000n }] })];
  assert.equal(computePoolEfficiency(pool, epochs, prices), null);
});

test("computePoolEfficiency returns null when the trailing average is below MIN_TRAILING_USD", () => {
  const tinyFee = 1_000n; // $0.000001, far below the floor
  const epochs = [epoch({ votes: 1_000n * 10n ** 18n, fees: [{ token: "0xfee", amount: tinyFee }] })];
  assert.equal(computePoolEfficiency(pool, epochs, prices), null);
});

test("computePoolEfficiency computes currentVotesVeAero, latest/trailing USD, and $/vote correctly", () => {
  const votes = 100n * 10n ** 18n; // 100 veAERO
  const epochs = [
    epoch({ ts: 200, votes, fees: [{ token: "0xfee", amount: 200_000_000n }] }), // $200 latest
    epoch({ ts: 100, votes, fees: [{ token: "0xfee", amount: 100_000_000n }] }), // $100
  ];
  const result = computePoolEfficiency(pool, epochs, prices);

  assert.ok(result);
  assert.equal(result.currentVotesVeAero, 100);
  assert.equal(result.latestEpochTs, 200);
  assert.equal(result.latestEpochUsd, 200);
  assert.equal(result.trailingAvgUsd, 150); // mean(200, 100)
  assert.equal(result.epochsObserved, 2);
  assert.equal(result.currentValuePerVote, 2); // 200 / 100
  assert.equal(result.predictedValuePerVote, 1.5); // 150 / 100
  assert.ok(Math.abs(result.predictiveEdge - -0.25) < 1e-9); // 1.5 / 2 - 1
});

test("computePoolEfficiency carries the per-epoch USD series through, most recent first", () => {
  const votes = 100n * 10n ** 18n;
  const epochs = [
    epoch({ ts: 300, votes, fees: [{ token: "0xfee", amount: 300_000_000n }] }), // $300
    epoch({ ts: 200, votes, fees: [{ token: "0xfee", amount: 200_000_000n }] }), // $200
    epoch({ ts: 100, votes, fees: [{ token: "0xfee", amount: 100_000_000n }] }), // $100
  ];
  const result = computePoolEfficiency(pool, epochs, prices);

  assert.ok(result);
  assert.deepEqual(result.epochUsdSeries, [300, 200, 100]);
  // The series is the basis of the average, not a separate reading of the chain.
  assert.equal(result.trailingAvgUsd, 200);
});

test("computeConsistency scores a perfectly steady pool as 1 and zero volatility", () => {
  const { volatility, consistency } = computeConsistency([100, 100, 100, 100]);
  assert.equal(volatility, 0);
  assert.equal(consistency, 1);
});

test("computeConsistency scores a one-off spike far below a steady pool with the same average", () => {
  const steady = computeConsistency([100, 100, 100, 100, 100, 100]);
  const spike = computeConsistency([600, 0, 0, 0, 0, 0]);

  // Both average $100/epoch — the trailing average alone cannot tell them apart.
  assert.ok(spike.consistency < steady.consistency);
  // cv of [600,0,0,0,0,0] is sqrt(5)≈2.236, so consistency = 1/(1+2.236) ≈ 0.309
  assert.ok(Math.abs(spike.volatility - Math.sqrt(5)) < 1e-9);
  assert.ok(Math.abs(spike.consistency - 1 / (1 + Math.sqrt(5))) < 1e-9);
});

test("computeConsistency treats a single observed epoch as unproven (0), not perfectly steady", () => {
  assert.deepEqual(computeConsistency([100]), { volatility: 0, consistency: 0 });
  assert.deepEqual(computeConsistency([]), { volatility: 0, consistency: 0 });
});

test("computeConsistency returns 0 rather than NaN when every epoch is worth $0", () => {
  const { volatility, consistency } = computeConsistency([0, 0, 0]);
  assert.equal(volatility, 0);
  assert.equal(consistency, 0);
});

test("computeConsistency is scale-free — same shape at $50/epoch and $50,000/epoch scores identically", () => {
  const small = computeConsistency([50, 100, 150]);
  const large = computeConsistency([50_000, 100_000, 150_000]);
  assert.ok(Math.abs(small.volatility - large.volatility) < 1e-9);
  assert.ok(Math.abs(small.consistency - large.consistency) < 1e-9);
});

test("computePoolEfficiency surfaces volatility/consistency for the epochs it observed", () => {
  const votes = 100n * 10n ** 18n;
  const epochs = [
    epoch({ ts: 200, votes, fees: [{ token: "0xfee", amount: 200_000_000n }] }), // $200
    epoch({ ts: 100, votes, fees: [{ token: "0xfee", amount: 100_000_000n }] }), // $100
  ];
  const result = computePoolEfficiency(pool, epochs, prices);

  assert.ok(result);
  // mean 150, population std dev 50 → cv = 1/3
  assert.ok(Math.abs(result.volatility - 1 / 3) < 1e-9);
  assert.ok(Math.abs(result.consistency - 1 / (1 + 1 / 3)) < 1e-9);
});

test("computePoolEfficiency: predictiveEdge falls back to 0 (not Infinity/NaN) when the latest epoch is worth $0 but the trailing average isn't", () => {
  const votes = 10n * 10n ** 18n;
  const epochs = [
    epoch({ ts: 200, votes, fees: [] }), // latest epoch: $0
    epoch({ ts: 100, votes, fees: [{ token: "0xfee", amount: BigInt(MIN_TRAILING_USD * 2 * 2) * 10n ** 6n }] }),
  ];
  const result = computePoolEfficiency(pool, epochs, prices);

  assert.ok(result);
  assert.equal(result.currentValuePerVote, 0);
  assert.equal(result.predictiveEdge, 0);
});

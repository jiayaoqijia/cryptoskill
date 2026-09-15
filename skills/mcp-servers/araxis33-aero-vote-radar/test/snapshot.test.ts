import { test } from "node:test";
import assert from "node:assert/strict";
import { buildEpochYields, buildRewardTokens, buildSnapshot, toSnapshotPool } from "../src/snapshot.js";
import type { PoolEfficiency } from "../src/efficiency.js";

function ranked(overrides: Partial<PoolEfficiency> & { symbol?: string }): PoolEfficiency {
  const { symbol, ...rest } = overrides;
  return {
    pool: {
      address: "0xpool",
      symbol: symbol ?? "vAMM-TEST/USDC",
      token0: "0xtoken0",
      token1: "0xtoken1",
      gauge: "0xgauge",
      gaugeAlive: true,
    },
    latestEpochTs: 1_000,
    currentVotesVeAero: 500,
    latestEpochUsd: 100,
    trailingAvgUsd: 120,
    epochsObserved: 6,
    epochUsdSeries: [100, 110, 120, 130, 120, 140],
    epochVotesSeries: [500, 500, 500, 500, 500, 500],
    currentValuePerVote: 0.2,
    predictedValuePerVote: 0.24,
    predictiveEdge: 0.2,
    volatility: 0.5,
    consistency: 2 / 3,
    latestEpochBribes: [],
    latestEpochFees: [],
    ...rest,
  };
}

test("toSnapshotPool publishes the allocator's inputs, not just the derived per-vote figures", () => {
  const p = toSnapshotPool(ranked({}), new Date("2026-08-17T00:00:00Z"));
  // The browser re-runs allocateAcrossCandidates, which needs both of these;
  // the CLI's JSON shape carries neither.
  assert.equal(p.votesVeAero, 500);
  assert.equal(p.trailingAvgUsd, 120);
  assert.equal(p.symbol, "vAMM-TEST/USDC");
  assert.equal(p.pool, "0xpool");
});

test("toSnapshotPool publishes the epoch series and the pool's own epoch date", () => {
  const p = toSnapshotPool(
    ranked({ epochUsdSeries: [300, 200, 100, 100, 100, 100], latestEpochTs: 1_786_579_200 }),
    new Date("2026-08-17T00:00:00Z"),
  );
  assert.deepEqual(p.epochUsd, [300, 200, 100, 100, 100, 100]);
  assert.equal(p.latestEpochTs, 1_786_579_200);
});

test("toSnapshotPool flags a mid-week scan's newest epoch as partial and keeps it out of momentum", () => {
  // Epoch opened 2026-08-13, scanned four days later: epochUsd[0] is a part-week.
  const series = [60, 200, 200, 200, 200];
  const midWeek = toSnapshotPool(
    ranked({ epochUsdSeries: series, latestEpochTs: 1_786_579_200 }),
    new Date("2026-08-17T00:00:00Z"),
  );
  assert.equal(midWeek.currentEpochPartial, true);
  assert.equal(midWeek.momentum, 0); // the steady $200 epochs, part-week excluded

  // The same pool data a week on: that epoch has closed, so it now counts.
  const afterRollover = toSnapshotPool(
    ranked({ epochUsdSeries: series, latestEpochTs: 1_786_579_200 }),
    new Date("2026-08-24T00:00:00Z"),
  );
  assert.equal(afterRollover.currentEpochPartial, false);
  assert.ok((afterRollover.momentum as number) < -0.3);
});

test("buildSnapshot judges partial epochs against its own generatedAt, not the wall clock", () => {
  const snap = buildSnapshot(
    [ranked({ latestEpochTs: 1_786_579_200 })],
    new Date("2026-08-17T00:00:00Z"),
  );
  assert.equal(snap.pools[0].currentEpochPartial, true);
});

test("buildSnapshot records the generation time as an ISO string", () => {
  const snap = buildSnapshot([ranked({})], new Date("2026-08-07T12:00:00Z"));
  assert.equal(snap.generatedAt, "2026-08-07T12:00:00.000Z");
});

test("buildSnapshot counts the pools it publishes", () => {
  const snap = buildSnapshot([ranked({ symbol: "A" }), ranked({ symbol: "B" })], new Date());
  assert.equal(snap.poolCount, 2);
  assert.equal(snap.pools.length, 2);
});

test("buildSnapshot takes the newest epoch across pools, not the top-ranked pool's", () => {
  // Pools arrive sorted by predicted value, so the first pool can easily be one
  // whose rewards contract hasn't been touched this week. Taking its epoch would
  // report the site as staler than it is.
  const snap = buildSnapshot(
    [ranked({ symbol: "STALE", latestEpochTs: 1_000 }), ranked({ symbol: "FRESH", latestEpochTs: 9_000 })],
    new Date(),
  );
  assert.equal(snap.latestEpochTs, 9_000);
});

test("buildSnapshot on an empty ranking yields no pools and a zero epoch", () => {
  const snap = buildSnapshot([], new Date());
  assert.equal(snap.poolCount, 0);
  assert.equal(snap.latestEpochTs, 0);
});

test("the snapshot publishes when the epoch it describes stops being actionable", () => {
  // Scanned Saturday 2026-08-22 12:00 UTC, so the vote it recommends has to be
  // cast before Thursday 2026-08-27 00:00 UTC to count.
  const generatedAt = new Date(Date.UTC(2026, 7, 22, 12, 0, 0));
  const snapshot = buildSnapshot([ranked({ latestEpochTs: 1_786_320_000 })], generatedAt);

  assert.equal(new Date(snapshot.epochEndsAt * 1000).toISOString(), "2026-08-27T00:00:00.000Z");
  assert.ok(snapshot.epochEndsAt > Math.floor(generatedAt.getTime() / 1000));
});

test("epochEndsAt follows the scan clock, not a pool's stale latestEpochTs", () => {
  // A pool whose rewards contract has not been touched in weeks reports an old
  // epoch. Deriving the deadline from that would tell a visitor that voting
  // closed long ago, when the epoch they can actually vote in is the current one.
  const generatedAt = new Date(Date.UTC(2026, 7, 22, 12, 0, 0));
  const staleEpochTs = Math.floor(Date.UTC(2026, 6, 2, 0, 0, 0) / 1000);

  const snapshot = buildSnapshot([ranked({ latestEpochTs: staleEpochTs })], generatedAt);

  assert.equal(snapshot.latestEpochTs, staleEpochTs);
  assert.equal(new Date(snapshot.epochEndsAt * 1000).toISOString(), "2026-08-27T00:00:00.000Z");
});

test("toSnapshotPool carries the vote-weight history and what it implies", () => {
  // 5,000 votes now against 40,000 in each completed epoch: the pool is between
  // votes, and its per-vote figure is optimistic by 8x until the weight returns.
  const p = toSnapshotPool(
    ranked({
      currentVotesVeAero: 5_000,
      trailingAvgUsd: 120,
      epochVotesSeries: [5_000, 40_000, 40_000, 40_000, 40_000],
      latestEpochTs: 1_786_579_200,
    }),
    new Date("2026-08-17T00:00:00Z"),
  );

  assert.deepEqual(p.epochVotes, [5_000, 40_000, 40_000, 40_000, 40_000]);
  assert.equal(p.expectedVotes, 40_000);
  assert.equal(p.refillRatio, 8);
  assert.equal(p.voteStability, 1);
  // The headline figure divides by 5,000; the honest one divides by 40,000.
  assert.equal(p.predictedValuePerVote, 0.24);
  assert.equal(p.dilutionAdjustedValuePerVote, 120 / 40_000);
});

test("a pool carrying more than last epoch is allowed to report the lower weight", () => {
  // The defect in the basis this replaced: it took the maximum of the live tally
  // and the pool's usual weight, so it could only ever raise the denominator.
  // Measured against what epochs actually settled at, that upward bias made it
  // the worst of the three predictors — so a tally sitting above last epoch's
  // weight must not pin the estimate to itself.
  const p = toSnapshotPool(
    ranked({
      currentVotesVeAero: 9_000,
      trailingAvgUsd: 90,
      epochVotesSeries: [9_000, 3_000, 3_000, 3_000],
      latestEpochTs: 1_786_579_200,
    }),
    new Date("2026-08-17T00:00:00Z"),
  );

  assert.equal(p.dilutionAdjustedValuePerVote, 90 / 3_000);
  assert.ok((p.refillRatio as number) < 1);
});

test("a pool with no previous epoch falls back to the weight it actually carries", () => {
  // A brand-new pool: nothing behind the running tally to read. It is priced on
  // what it has rather than excluded or handed an invented baseline.
  const p = toSnapshotPool(
    ranked({
      currentVotesVeAero: 5_000,
      trailingAvgUsd: 120,
      predictedValuePerVote: 120 / 5_000, // keep the fixture self-consistent
      epochVotesSeries: [5_000],
      latestEpochTs: 1_786_579_200,
    }),
    new Date("2026-08-17T00:00:00Z"),
  );

  assert.equal(p.expectedVotes, null); // one epoch cannot demonstrate a typical weight
  assert.equal(p.refillRatio, null);
  assert.equal(p.dilutionAdjustedValuePerVote, p.predictedValuePerVote);
});

test("buildEpochYields sums the pot over the weight, keyed by epoch rather than by position", () => {
  // Two pools with different history depths. Index 1 is the same week for both
  // only because their latestEpochTs agree; the third pool's does not.
  const week = 604_800;
  const ts = 1_786_579_200;
  const yields = buildEpochYields(
    [
      ranked({ symbol: "A", latestEpochTs: ts, epochUsdSeries: [10, 20], epochVotesSeries: [100, 200] }),
      ranked({ symbol: "B", latestEpochTs: ts, epochUsdSeries: [30, 60], epochVotesSeries: [300, 600] }),
      ranked({ symbol: "C", latestEpochTs: ts - week, epochUsdSeries: [7], epochVotesSeries: [700] }),
    ],
    new Date("2026-08-17T00:00:00Z"),
  );

  // A and B each carry two epochs (ts and ts-week); C carries one, dated ts-week.
  // So there are exactly two buckets, and C lands in the older one.
  assert.deepEqual(
    yields.map((y) => y.ts),
    [ts, ts - week],
  );

  const current = yields[0];
  assert.equal(current.totalUsd, 40);
  assert.equal(current.totalVotes, 400);
  assert.equal(current.usdPerVote, 0.1);
  assert.equal(current.pools, 2);

  // C's only epoch lands in the middle bucket because it is keyed by date.
  const middle = yields[1];
  assert.equal(middle.pools, 3);
  assert.equal(middle.totalUsd, 20 + 60 + 7);
  assert.equal(middle.totalVotes, 200 + 600 + 700);
});

test("buildEpochYields flags the running epoch, whose totals are a part-week", () => {
  const ts = 1_786_579_200; // opened 2026-08-13
  const yields = buildEpochYields(
    [ranked({ latestEpochTs: ts, epochUsdSeries: [5, 100], epochVotesSeries: [50, 50] })],
    new Date("2026-08-17T00:00:00Z"),
  );

  assert.equal(yields[0].partial, true);
  assert.equal(yields[1].partial, false);
});

test("buildEpochYields reports zero rather than dividing by an epoch with no votes", () => {
  const yields = buildEpochYields(
    [ranked({ latestEpochTs: 1_786_579_200, epochUsdSeries: [10], epochVotesSeries: [0] })],
    new Date("2026-08-17T00:00:00Z"),
  );
  assert.equal(yields[0].usdPerVote, 0);
});

test("buildSnapshot publishes the protocol-wide yield series alongside the pools", () => {
  const snap = buildSnapshot(
    [ranked({ latestEpochTs: 1_786_579_200, epochUsdSeries: [10, 20], epochVotesSeries: [100, 100] })],
    new Date("2026-08-17T00:00:00Z"),
  );
  assert.equal(snap.epochYields.length, 2);
  assert.equal(snap.epochYields[1].usdPerVote, 0.2);
});

const AT = new Date("2026-08-17T00:00:00Z");
const USDC = "0xA0B86991C6218B36C1D19D4A2E9EB0CE3606EB48";
const AERO = "0x940181A94A35A4569E4529A3CDFB74E38FD98631";

test("toSnapshotPool publishes the token amounts behind latestEpochUsd, not just the total", () => {
  const p = toSnapshotPool(
    ranked({
      latestEpochBribes: [{ token: AERO, amount: 5_000_000_000_000_000_000n, decimals: 18, priceUsd: 0.5 }],
      latestEpochFees: [{ token: USDC, amount: 2_500_000n, decimals: 6, priceUsd: 1 }],
    }),
    AT,
  );
  assert.deepEqual(p.latestEpochBribes, [[AERO.toLowerCase(), "5000000000000000000"]]);
  assert.deepEqual(p.latestEpochFees, [[USDC.toLowerCase(), "2500000"]]);
});

test("the published amounts and prices reconstruct the published USD figure", () => {
  // The point of publishing the parts is that they add back up to the whole. If
  // this drifts, a later reader separating accrual from a price move would be
  // working from numbers that never described this scan.
  const r = ranked({
    latestEpochUsd: 5, // 5 AERO at $0.50 plus 2.5 USDC at $1
    latestEpochBribes: [{ token: AERO, amount: 5_000_000_000_000_000_000n, decimals: 18, priceUsd: 0.5 }],
    latestEpochFees: [{ token: USDC, amount: 2_500_000n, decimals: 6, priceUsd: 1 }],
  });
  const snap = buildSnapshot([r], AT);
  const priced = new Map(snap.rewardTokens.map((t) => [t.address, t]));
  const rebuilt = [...snap.pools[0].latestEpochBribes, ...snap.pools[0].latestEpochFees].reduce((sum, [token, amount]) => {
    const t = priced.get(token)!;
    return sum + (Number(amount) / 10 ** t.decimals) * t.priceUsd;
  }, 0);
  assert.equal(rebuilt, snap.pools[0].latestEpochUsd);
});

test("toSnapshotPool drops zero amounts rather than publishing empty rows four times a day", () => {
  const p = toSnapshotPool(
    ranked({
      latestEpochFees: [
        { token: USDC, amount: 0n, decimals: 6, priceUsd: 1 },
        { token: AERO, amount: 1n, decimals: 18, priceUsd: 0.5 },
      ],
    }),
    AT,
  );
  assert.deepEqual(p.latestEpochFees, [[AERO.toLowerCase(), "1"]]);
});

test("buildRewardTokens records each token once, sorted, with the price the scan valued it at", () => {
  const bribe = { token: AERO, amount: 1n, decimals: 18, priceUsd: 0.5 };
  const fee = { token: USDC, amount: 1n, decimals: 6, priceUsd: 1 };
  const tokens = buildRewardTokens([
    ranked({ symbol: "A", latestEpochBribes: [bribe], latestEpochFees: [fee] }),
    ranked({ symbol: "B", latestEpochBribes: [bribe], latestEpochFees: [] }),
  ]);
  assert.deepEqual(
    tokens,
    [
      { address: USDC.toLowerCase(), decimals: 6, priceUsd: 1 },
      { address: AERO.toLowerCase(), decimals: 18, priceUsd: 0.5 },
    ].sort((a, b) => (a.address < b.address ? -1 : 1)),
  );
});

test("an unpriced reward token still gets its amount recorded, so it can be valued later", () => {
  // A token the price source had nothing for counts as $0 in every total here.
  // Dropping its amount too would make that scan permanently unrecoverable.
  const snap = buildSnapshot(
    [ranked({ latestEpochBribes: [{ token: AERO, amount: 7n, decimals: 18, priceUsd: 0 }], latestEpochFees: [] })],
    AT,
  );
  assert.deepEqual(snap.pools[0].latestEpochBribes, [[AERO.toLowerCase(), "7"]]);
  assert.equal(snap.rewardTokens[0].priceUsd, 0);
});

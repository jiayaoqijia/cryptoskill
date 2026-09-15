import { test } from "node:test";
import assert from "node:assert/strict";
import { scoreVotes, type CastVote } from "../src/voted.js";
import type { EpochData } from "../src/pools.js";

const EPOCH = 1788393600;
const PREVIOUS = EPOCH - 604800;
const WEI = 10n ** 18n;

const prices = new Map([["0xaaa", { price: 2, decimals: 18 }]]);

const epoch = (ts: number, votes: bigint, bribeTokens: bigint): EpochData => ({
  ts,
  votes,
  bribes: [{ token: "0xaaa", amount: bribeTokens }],
  fees: [],
});

const history = (entries: [string, string, EpochData[]][]) =>
  new Map(entries.map(([addr, symbol, epochs]) => [addr, { symbol, epochs }]));

test("scoreVotes divides the pool's settled pot by the weight the epoch settled at", () => {
  // Pool paid 100 tokens at $2 = $200, over 1,000 veAERO. This holder had 100.
  const votes: CastVote[] = [{ pool: "0xp", weight: 100n * WEI }];
  const r = scoreVotes(votes, EPOCH, history([["0xp", "vAMM-A/B", [epoch(EPOCH, 1000n * WEI, 100n * WEI)]]]), prices);
  assert.equal(r.rows.length, 1);
  assert.equal(r.rows[0].poolUsd, 200);
  assert.equal(r.rows[0].poolVotes, 1000);
  assert.equal(r.rows[0].myVotes, 100);
  assert.equal(r.earnedUsd, 20);
  assert.equal(r.budget, 100);
});

test("scoreVotes splits the holder's own share across pools by weight, not evenly", () => {
  const votes: CastVote[] = [
    { pool: "0xa", weight: 75n * WEI },
    { pool: "0xb", weight: 25n * WEI },
  ];
  const r = scoreVotes(
    votes,
    EPOCH,
    history([
      ["0xa", "A", [epoch(EPOCH, 1000n * WEI, 100n * WEI)]],
      ["0xb", "B", [epoch(EPOCH, 1000n * WEI, 100n * WEI)]],
    ]),
    prices,
  );
  const byPool = new Map(r.rows.map((x) => [x.pool, x]));
  assert.equal(byPool.get("0xa")?.share, 0.75);
  assert.equal(byPool.get("0xb")?.share, 0.25);
  assert.equal(r.budget, 100);
});

test("scoreVotes scores the epoch asked for, not whichever one the pool's history starts with", () => {
  const votes: CastVote[] = [{ pool: "0xp", weight: 100n * WEI }];
  const epochs = [epoch(EPOCH, 1000n * WEI, 100n * WEI), epoch(PREVIOUS, 1000n * WEI, 999n * WEI)];
  const r = scoreVotes(votes, PREVIOUS, history([["0xp", "P", epochs]]), prices);
  assert.equal(r.epochTs, PREVIOUS);
  assert.equal(r.rows[0].poolUsd, 1998);
});

test("scoreVotes counts a pool with no settled record rather than dropping it silently", () => {
  const votes: CastVote[] = [
    { pool: "0xknown", weight: 50n * WEI },
    { pool: "0xgone", weight: 50n * WEI },
  ];
  const r = scoreVotes(votes, EPOCH, history([["0xknown", "K", [epoch(EPOCH, 1000n * WEI, 100n * WEI)]]]), prices);
  assert.equal(r.rows.length, 1);
  assert.equal(r.unscored, 1);
  // The unscored pool's veAERO still counts toward what this holder committed:
  // it was spent, it just cannot be scored.
  assert.equal(r.budget, 100);
});

test("scoreVotes reports zero rather than dividing by a pool with no recorded weight", () => {
  const votes: CastVote[] = [{ pool: "0xp", weight: 100n * WEI }];
  const r = scoreVotes(votes, EPOCH, history([["0xp", "P", [epoch(EPOCH, 0n, 100n * WEI)]]]), prices);
  assert.equal(r.rows[0].earnedUsd, 0);
  assert.ok(Number.isFinite(r.earnedUsd));
});

test("scoreVotes values a reward token the price map has no entry for at zero, not NaN", () => {
  const votes: CastVote[] = [{ pool: "0xp", weight: 100n * WEI }];
  const epochs = [{ ts: EPOCH, votes: 1000n * WEI, bribes: [{ token: "0xunpriced", amount: 5n * WEI }], fees: [] }];
  const r = scoreVotes(votes, EPOCH, history([["0xp", "P", epochs]]), prices);
  assert.equal(r.rows[0].poolUsd, 0);
  assert.equal(r.earnedUsd, 0);
});

test("scoreVotes puts the biggest earner first, so the report opens on what mattered", () => {
  const votes: CastVote[] = [
    { pool: "0xsmall", weight: 50n * WEI },
    { pool: "0xbig", weight: 50n * WEI },
  ];
  const r = scoreVotes(
    votes,
    EPOCH,
    history([
      ["0xsmall", "SMALL", [epoch(EPOCH, 1000n * WEI, 1n * WEI)]],
      ["0xbig", "BIG", [epoch(EPOCH, 1000n * WEI, 500n * WEI)]],
    ]),
    prices,
  );
  assert.deepEqual(r.rows.map((x) => x.symbol), ["BIG", "SMALL"]);
});

test("scoreVotes handles a lock with no votes at all without dividing by zero", () => {
  const r = scoreVotes([], EPOCH, history([]), prices);
  assert.deepEqual(r.rows, []);
  assert.equal(r.earnedUsd, 0);
  assert.equal(r.budget, 0);
  assert.equal(r.unscored, 0);
});

test("scoreVotes sums several locks on the same pool into one holder's share", () => {
  // Two veNFTs of the same wallet, both on the same pool: the caller passes both
  // votes and the report must read as one position, because that is what the
  // chain paid out on.
  const votes: CastVote[] = [
    { pool: "0xp", weight: 60n * WEI },
    { pool: "0xp", weight: 40n * WEI },
  ];
  const r = scoreVotes(votes, EPOCH, history([["0xp", "P", [epoch(EPOCH, 1000n * WEI, 100n * WEI)]]]), prices);
  assert.equal(r.budget, 100);
  assert.equal(r.earnedUsd, 20);
});

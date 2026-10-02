import { test } from "node:test";
import assert from "node:assert/strict";
import { pickScanPerEpoch, scoreEpochPromise } from "../src/promise.js";
import { WEEKLY_EPOCH, periodStartOf } from "../src/trend.js";

const EPOCH = periodStartOf(1_790_300_000); // some settled epoch
const NEXT = EPOCH + WEEKLY_EPOCH.lengthSeconds;
const iso = (s: number) => new Date(s * 1000).toISOString();
const near = (actual: number, expected: number) => assert.ok(Math.abs(actual - expected) < 1e-9, `${actual} vs ${expected}`);

/** A snapshot pool forecast to earn `forecastUsd` at an expected settled weight of `expectedWeight`. */
const pool = (symbol: string, address: string, forecastUsd: number, expectedWeight: number, extra: object = {}) => ({
  symbol,
  pool: address,
  votesVeAero: 1000,
  consistency: 0.9,
  migrating: false,
  forecastUsd,
  dilutionAdjustedValuePerVote: forecastUsd / expectedWeight,
  ...extra,
});

const settled = (entries: Record<string, [number, number]>) => {
  const votes = new Map<string, Map<number, number>>();
  const usd = new Map<string, Map<number, number>>();
  for (const [addr, [v, u]] of Object.entries(entries)) {
    votes.set(addr, new Map([[EPOCH, v]]));
    usd.set(addr, new Map([[EPOCH, u]]));
  }
  return { votes, usd };
};

test("quoted and paid are both for 10,000 veAERO placed alone in the pool, own vote included", () => {
  // A: forecast $60 at weight 2,000 -> 10,000 of 12,000 -> $50. Paid $90 at weight 2,000 -> $75.
  // B: forecast $20 at weight 10,000 -> half -> $10. Paid $5 at weight 10,000 -> $2.50.
  const { votes, usd } = settled({ "0xa": [2000, 90], "0xb": [10_000, 5] });
  const snap = { generatedAt: iso(EPOCH + 3600), pools: [pool("A", "0xA", 60, 2000), pool("B", "0xb", 20, 10_000)] };
  const result = scoreEpochPromise(snap, EPOCH, votes, usd)!;
  const a = result.rows.find((r) => r.symbol === "A")!;
  near(a.forecastUsd, 50);
  near(a.paidUsd, 75);
  near(a.ratio, 1.5);
  const b = result.rows.find((r) => r.symbol === "B")!;
  near(b.forecastUsd, 10);
  near(b.paidUsd, 2.5);
  near(b.ratio, 0.25);
  assert.equal(result.paidAtLeastForecast, 0.5);
  assert.equal(result.paidUnderHalf, 0.5);
});

test("a pool with almost no votes does not get a huge quote: its own vote dilutes it", () => {
  // $30 over a weight of 3 would be $10 a vote; with 10,000 voted it is $30 * 10000/10003.
  const { votes, usd } = settled({ "0xa": [3, 30] });
  const snap = { generatedAt: iso(EPOCH + 3600), pools: [pool("tiny", "0xa", 30, 3)] };
  const row = scoreEpochPromise(snap, EPOCH, votes, usd)!.rows[0];
  near(row.forecastUsd, (30 * 10_000) / 10_003);
  assert.ok(row.forecastUsd < 30);
});

test("migrating and inconsistent pools are never held to a quote, and unsettled pools are skipped", () => {
  const { votes, usd } = settled({ "0xa": [1000, 5], "0xb": [1000, 5], "0xc": [1000, 5] });
  const snap = {
    generatedAt: iso(EPOCH + 3600),
    pools: [
      pool("moving", "0xa", 900, 1000, { migrating: true }),
      pool("erratic", "0xb", 800, 1000, { consistency: 0.2 }),
      pool("unknown", "0xzzz", 700, 1000),
      pool("ok", "0xc", 100, 1000),
    ],
  };
  const result = scoreEpochPromise(snap, EPOCH, votes, usd)!;
  assert.deepEqual(result.rows.map((r) => r.symbol), ["ok"]);
});

test("only the top pools by quote are scored", () => {
  const entries: Record<string, [number, number]> = {};
  const pools = [];
  for (let i = 0; i < 5; i++) {
    entries[`0x${i}`] = [1000, 10];
    pools.push(pool(`P${i}`, `0x${i}`, 10 * (i + 1), 1000));
  }
  const { votes, usd } = settled(entries);
  const result = scoreEpochPromise({ generatedAt: iso(EPOCH + 3600), pools }, EPOCH, votes, usd, 2)!;
  assert.deepEqual(result.rows.map((r) => r.symbol), ["P4", "P3"]);
});

test("an epoch with nothing scorable returns null rather than an empty promise", () => {
  const { votes, usd } = settled({});
  assert.equal(scoreEpochPromise({ generatedAt: iso(EPOCH), pools: [pool("A", "0xa", 10, 1000)] }, EPOCH, votes, usd), null);
});

test("the scan used is the latest one at least a day before close; the running epoch is ignored", () => {
  const early = { generatedAt: iso(EPOCH + 3600), pools: [] };
  const lastUseful = { generatedAt: iso(NEXT - 25 * 3600), pools: [] };
  const tooLate = { generatedAt: iso(NEXT - 3600), pools: [] };
  const running = { generatedAt: iso(NEXT + 3600), pools: [] };
  const picked = pickScanPerEpoch([early, tooLate, lastUseful, running], NEXT);
  assert.equal(picked.size, 1);
  assert.equal(picked.get(EPOCH), lastUseful);
});

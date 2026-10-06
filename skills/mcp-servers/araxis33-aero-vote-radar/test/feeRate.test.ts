import { test } from "node:test";
import assert from "node:assert/strict";
import type { FeeCounter } from "../src/feeStream.js";
import { buildFeeInterval, buildFeeRates, packFeeIntervals, poolFeeRate, pruneFeeIntervals, unpackFeeIntervals, type FeeInterval } from "../src/feeRate.js";

const tokens: [string, string] = ["0xa", "0xb"];
const cl = (pool: string, a: string, b: string): FeeCounter => ({ pool, kind: "cl", tokens, gaugeFees: [a, b] });
// token a: 18 decimals at $2; token b: 6 decimals at $1.
const prices = (t: string) => (t === "0xa" ? { decimals: 18, priceUsd: 2 } : t === "0xb" ? { decimals: 6, priceUsd: 1 } : undefined);
const e18 = 10n ** 18n;

test("interval: counter growth valued at the given prices", () => {
  const i = buildFeeInterval([cl("0xp", "0", "0")], [cl("0xp", (3n * e18).toString(), "5000000")], "t0", "t1", prices);
  assert.equal(i.usd["0xp"], 3 * 2 + 5);
});

test("interval: a CL gauge that collected in between is unknown, not the small later reading", () => {
  const i = buildFeeInterval([cl("0xp", (9n * e18).toString(), "0")], [cl("0xp", e18.toString(), "0")], "t0", "t1", prices);
  assert.equal(i.usd["0xp"], null);
});

test("interval: an earned token without a price makes the pool unknown rather than understated", () => {
  const priced = (t: string) => (t === "0xa" ? { decimals: 18, priceUsd: 0 } : prices(t));
  const i = buildFeeInterval([cl("0xp", "0", "0")], [cl("0xp", e18.toString(), "1000000")], "t0", "t1", priced);
  assert.equal(i.usd["0xp"], null);
});

test("interval: a pool missing from the earlier read is left out", () => {
  const i = buildFeeInterval([], [cl("0xp", "1", "1")], "t0", "t1", prices);
  assert.deepEqual(i.usd, {});
});

const now = new Date("2026-10-06T00:00:00Z");
const h = (hoursAgo: number) => new Date(now.getTime() - hoursAgo * 3_600_000).toISOString();
// Sixteen 6-hour intervals = the last 96 hours, $60 each -> $240/day.
const steady = (usd: (k: number) => number | null): FeeInterval[] =>
  Array.from({ length: 16 }, (_, k) => ({ from: h(96 - 6 * k), to: h(90 - 6 * k), usd: { "0xp": usd(k) } }));

test("rate: average per day over the window", () => {
  assert.deepEqual(poolFeeRate(steady(() => 60), "0xp", now), { usdPerDay: 240, hours: 96 });
});

test("rate: unreadable intervals are skipped, the rate comes from the readable part", () => {
  const r = poolFeeRate(steady((k) => (k % 4 === 0 ? null : 60)), "0xp", now);
  assert.deepEqual(r, { usdPerDay: 240, hours: 72 });
});

test("rate: below 60% readable coverage there is no figure", () => {
  assert.equal(poolFeeRate(steady((k) => (k < 7 ? null : 60)), "0xp", now), null);
});

test("rate: intervals outside the window do not count", () => {
  const old: FeeInterval = { from: h(130), to: h(124), usd: { "0xp": 1_000_000 } };
  assert.deepEqual(poolFeeRate([old, ...steady(() => 60)], "0xp", now), { usdPerDay: 240, hours: 96 });
});

test("per 10k votes uses the pool's current weight; no votes means no per-vote figure", () => {
  const rates = buildFeeRates(steady(() => 60), new Map([["0xp", 1_000_000]]), now);
  assert.deepEqual(rates["0xp"], { usdPerDay: 240, usdPerDayPer10k: 2.4, hours: 96 });
  assert.equal(buildFeeRates(steady(() => 60), new Map(), now)["0xp"].usdPerDayPer10k, null);
});

test("prune keeps the recent intervals, oldest first", () => {
  const kept = pruneFeeIntervals([{ from: h(6), to: h(0), usd: {} }, { from: h(200), to: h(194), usd: {} }, { from: h(12), to: h(6), usd: {} }], now);
  assert.deepEqual(kept.map((i) => i.to), [h(6), h(0)]);
});

test("pack/unpack round-trips, with missing and unreadable pools both coming back as absent", () => {
  const intervals: FeeInterval[] = [
    { from: h(12), to: h(6), usd: { "0xp": 1.234, "0xq": null } },
    { from: h(6), to: h(0), usd: { "0xq": 5 } },
  ];
  const packed = packFeeIntervals(intervals);
  assert.deepEqual(packed.poolIds, ["0xp", "0xq"]);
  assert.deepEqual(packed.intervals.map((i) => i.usd), [[1.23, null], [null, 5]]);
  assert.deepEqual(unpackFeeIntervals({ ...packed }).map((i) => i.usd), [{ "0xp": 1.23 }, { "0xq": 5 }]);
  assert.deepEqual(unpackFeeIntervals(null), []);
});

import { test } from "node:test";
import assert from "node:assert/strict";
import { appendV3Sample, isSteady, per10kNow, poolKey, steadiness, V3_STEADY_MIN_SAMPLES } from "../src/v3History.js";
import type { V3ScanGauge } from "../src/v3.js";

const gauge = (gauge: string, weight: number, fees24h: number, incentives = 0): V3ScanGauge =>
  ({
    chain: "base",
    gauge: gauge as `0x${string}`,
    pool: "0x0" as `0x${string}`,
    weight,
    fees24hUsdPerDay: fees24h,
    feesUsdPerDay: fees24h,
    incentivesUsdPerDay: incentives,
    usdPerDayPer10k: null,
  }) as V3ScanGauge;

test("per10kNow: 24 h fees plus incentives, diluted by the 10,000 sAERO itself", () => {
  assert.equal(per10kNow(gauge("0xA", 90_000, 80, 20)), 10);
});

test("appendV3Sample: one column per pool, small pools left out, missing scans are null", () => {
  const t = (h: number) => new Date(Date.UTC(2026, 9, 24, h));
  let f = appendV3Sample(null, [gauge("0xA", 90_000, 100), gauge("0xB", 200_000, 210)], t(0));
  assert.deepEqual(Object.keys(f.pools), [poolKey(gauge("0xB", 0, 0))]);
  f = appendV3Sample(f, [gauge("0xC", 490_000, 50)], t(1));
  assert.deepEqual(f.at, [t(0).toISOString(), t(1).toISOString()]);
  assert.deepEqual(f.pools["base:0xb"], [10, null]);
  assert.deepEqual(f.pools["base:0xc"], [null, 1]);
});

test("appendV3Sample: samples past the keep window are dropped, and pools left with none", () => {
  const t = (h: number) => new Date(Date.UTC(2026, 9, 24, h));
  let f = appendV3Sample(null, [gauge("0xB", 200_000, 210)], t(0), 2);
  f = appendV3Sample(f, [gauge("0xC", 490_000, 50)], t(1), 2);
  f = appendV3Sample(f, [gauge("0xC", 490_000, 50)], t(3), 2);
  assert.deepEqual(f.at, [t(1).toISOString(), t(3).toISOString()]);
  assert.equal(f.pools["base:0xb"], undefined);
  assert.deepEqual(f.pools["base:0xc"], [1, 1]);
});

test("steadiness: needs a day of samples; steady when 75% pay half the average or more", () => {
  assert.equal(steadiness(Array(V3_STEADY_MIN_SAMPLES - 1).fill(3)), undefined);
  const even = steadiness([...Array(V3_STEADY_MIN_SAMPLES).fill(3), null]);
  assert.deepEqual(even, { held: 24, of: 24, avgPer10k: 3, minPer10k: 3 });
  assert.ok(isSteady(even));
  // One huge hour lifts the average so the rest fall below half of it.
  const spiky = steadiness([...Array(23).fill(1), 100]);
  assert.equal(spiky!.held, 1);
  assert.ok(!isSteady(spiky));
});

test("appendV3Sample: records the radar's pick for 10,000 sAERO, null for samples from before it was kept", () => {
  const t = (h: number) => new Date(Date.UTC(2026, 9, 24, h));
  const old = { at: [t(0).toISOString()], pools: { "base:0xb": [10] } };
  // 0xA pays more but is under 100,000 sAERO; 0xC pays 50 a day on 490,000: 1 for 10,000.
  const f = appendV3Sample(old, [gauge("0xA", 90_000, 900), gauge("0xB", 200_000, 10), gauge("0xC", 490_000, 50)], t(1));
  assert.deepEqual(f.picks, [null, { pool: "base:0xc", per10k: 1 }]);
  const g = appendV3Sample(f, [], t(2), 1);
  assert.deepEqual(g.picks, [{ pool: "base:0xc", per10k: 1 }, null]);
});

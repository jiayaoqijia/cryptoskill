import { test } from "node:test";
import assert from "node:assert/strict";
import { dilutedPerDay, poolName, rankPools, scanAgeHours, splitAllocation, splitToText, steadyPools, trendOf, MAX_POOLS } from "../src/radar.js";
import type { V3ScanFile, V3ScanGauge } from "../src/v3.js";

const g = (sym: string, weight: number, fees: number, extra: Partial<V3ScanGauge> = {}): V3ScanGauge =>
  ({
    chain: "base", gauge: `0x${sym}`, pool: "0x2", weight, feesUsdPerDay: fees, fees24hUsdPerDay: fees, fees48hUsdPerDay: fees,
    incentivesUsdPerDay: 0, usdPerDayPer10k: null, symbol0: sym, symbol1: "USDC", kind: "CL100", ...extra,
  }) as V3ScanGauge;

const scan = (gauges: V3ScanGauge[], windowHours = 66.4): V3ScanFile => ({
  checkedAt: "2026-10-25T16:47:00.000Z", chain: "all", status: "live", windowHours, gauges,
});

test("dilutedPerDay counts the user's own stake in the pool", () => {
  assert.equal(dilutedPerDay(100, 90_000, 10_000), 10);
  assert.equal(dilutedPerDay(100, 90_000, 0), 0);
});

test("rankPools leaves out pools under 100k sAERO or paying nothing, and ranks after dilution", () => {
  const ranked = rankPools(scan([g("SMALL", 50_000, 1000), g("ZERO", 500_000, 0), g("LOW", 990_000, 100), g("HIGH", 190_000, 100)]), 10_000);
  assert.deepEqual(ranked.map((r) => r.gauge.symbol0), ["HIGH", "LOW"]);
  assert.equal(ranked[0].mine, 5);
});

test("rankPools filters by network", () => {
  const s = scan([g("A", 200_000, 10), g("B", 200_000, 50, { chain: "optimism" })]);
  assert.deepEqual(rankPools(s, 10_000, "optimism").map((r) => r.gauge.symbol0), ["B"]);
  assert.equal(rankPools(s, 10_000).length, 2);
});

test("incentives count toward what a pool pays", () => {
  const ranked = rankPools(scan([g("FEES", 190_000, 100), g("INC", 190_000, 0, { incentivesUsdPerDay: 300 })]), 10_000);
  assert.equal(ranked[0].gauge.symbol0, "INC");
});

test("splitAllocation keeps a small stake in the best pool", () => {
  const s = scan([g("HIGH", 190_000, 100), g("LOW", 990_000, 100)]);
  const split = splitAllocation(rankPools(s, 1_000).map((r) => r.gauge), 1_000);
  assert.equal(split.length, 1);
  assert.equal(split[0].gauge.symbol0, "HIGH");
  assert.equal(split[0].share, 1);
});

test("splitAllocation spreads a large stake, in 5% steps over at most 3 pools, totalling 100%", () => {
  const pools = [g("A", 100_000, 100), g("B", 100_000, 95), g("C", 100_000, 90), g("D", 100_000, 85)];
  const amount = 1_000_000;
  const split = splitAllocation(rankPools(scan(pools), amount).map((r) => r.gauge), amount);
  assert.ok(split.length > 1 && split.length <= MAX_POOLS);
  for (const s of split) assert.equal(Math.round(s.share * 100) % 5, 0);
  assert.equal(Math.round(split.reduce((a, s) => a + s.share, 0) * 100), 100);
  // Spreading beats putting it all in the top pool.
  const all = dilutedPerDay(100, 100_000, amount);
  assert.ok(split.reduce((a, s) => a + s.perDay, 0) > all);
});

test("splitAllocation returns nothing for no amount or no pools", () => {
  assert.deepEqual(splitAllocation([g("A", 200_000, 10)], 0), []);
  assert.deepEqual(splitAllocation([], 10_000), []);
});

test("trendOf says new under 36 h of data, then compares the last 24 h with the window", () => {
  assert.equal(trendOf(g("A", 1, 10, { fees24hUsdPerDay: 20 }), 30).label, "new");
  assert.equal(trendOf(g("A", 1, 10, { fees24hUsdPerDay: 20 }), 66).label, "rising");
  assert.equal(trendOf(g("A", 1, 10, { fees24hUsdPerDay: 5 }), 66).label, "cooling");
  assert.equal(trendOf(g("A", 1, 10, { fees24hUsdPerDay: 10.5 }), 66).label, "steady");
});

test("steadyPools keeps pools that held up and ranks them by the last 24 h", () => {
  const calm = g("CALM", 190_000, 100, { steady: { held: 30, of: 30, avgPer10k: 5.2, minPer10k: 4.1 } });
  const jumpy = g("JUMPY", 190_000, 500, { steady: { held: 10, of: 30, avgPer10k: 9, minPer10k: 0.1 } });
  const none = g("NONE", 190_000, 500);
  assert.deepEqual(steadyPools(scan([calm, jumpy, none]), 10_000).map((r) => r.gauge.symbol0), ["CALM"]);
});

test("poolName falls back to a short address without symbols", () => {
  assert.equal(poolName({ pool: "0x1234567890abcdef1234567890abcdef12345678" }), "0x1234…5678");
});

test("splitToText names pool, type, network and percent per line", () => {
  const split = splitAllocation([g("HIGH", 190_000, 100, { chain: "optimism" })], 1_000);
  assert.equal(splitToText(split), "HIGH/USDC (CL100, OP Mainnet) 100%");
});

test("scanAgeHours measures from checkedAt", () => {
  assert.equal(scanAgeHours({ checkedAt: "2026-10-25T16:00:00.000Z" }, Date.parse("2026-10-25T18:00:00.000Z")), 2);
});

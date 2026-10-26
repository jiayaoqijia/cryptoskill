import { test } from "node:test";
import assert from "node:assert/strict";
import { currentSplitPays, timersByChain, untilText, withoutOwnSAero, type Stake } from "../src/stakes.js";
import type { V3ScanFile, V3ScanGauge } from "../src/v3.js";

const gauge = (chain: string, addr: string, weight: number, fees: number) =>
  ({ chain, gauge: addr, pool: "0x2", weight, feesUsdPerDay: fees, fees24hUsdPerDay: fees, incentivesUsdPerDay: 0, usdPerDayPer10k: null }) as unknown as V3ScanGauge;

const scan: V3ScanFile = {
  checkedAt: "2026-10-25T16:47:00.000Z", chain: "all", status: "live", windowHours: 66,
  gauges: [gauge("base", "0xAAAA", 100_000, 100), gauge("optimism", "0xbbbb", 50_000, 10)],
};

const stake = (chains: Stake["chains"]): Stake => ({ id: 1n, sAero: 20_000, chains });

test("timersByChain keeps the soonest timer per network, skipping networks never allocated on", () => {
  const w = {
    stakes: [
      stake({ base: { lastAllocated: 100, readyAt: 500, allocations: [] }, ink: { lastAllocated: 0, readyAt: 0, allocations: [] } }),
      stake({ base: { lastAllocated: 50, readyAt: 300, allocations: [] } }),
    ],
  };
  assert.deepEqual(timersByChain(w), { base: 300 });
});

test("currentSplitPays matches gauges per network, case-insensitively, and counts unmatched sAERO as placed", () => {
  const w = {
    stakes: [
      stake({
        base: { lastAllocated: 1, readyAt: 2, allocations: [{ gauge: "0xaaaa", amount: 10_000 }] },
        optimism: { lastAllocated: 1, readyAt: 2, allocations: [{ gauge: "0xbbbb", amount: 5_000 }, { gauge: "0xdead", amount: 1_000 }] },
      }),
    ],
  };
  const r = currentSplitPays(w, scan);
  assert.equal(r.placedSAero, 16_000);
  assert.equal(r.usdPerDay, 100 * 0.1 + 10 * 0.1);
});

test("withoutOwnSAero takes the wallet's sAERO out of the pools it sits in, summed over stakes, never below zero", () => {
  const w = {
    stakes: [
      stake({ base: { lastAllocated: 1, readyAt: 2, allocations: [{ gauge: "0xaaaa", amount: 10_000 }] } }),
      stake({ base: { lastAllocated: 1, readyAt: 2, allocations: [{ gauge: "0xaaaa", amount: 5_000 }] }, optimism: { lastAllocated: 1, readyAt: 2, allocations: [{ gauge: "0xbbbb", amount: 60_000 }] } }),
    ],
  };
  const out = withoutOwnSAero(scan, w);
  assert.deepEqual(out.gauges.map((g) => g.weight), [85_000, 0]);
  assert.equal(scan.gauges[0].weight, 100_000);
  assert.equal(withoutOwnSAero(scan, { stakes: [] }), scan);
});

test("untilText rounds up to whole hours and says now once due", () => {
  assert.equal(untilText(1000, 2000), "now");
  assert.equal(untilText(2000 + 3601, 2000), "in 2 h");
});

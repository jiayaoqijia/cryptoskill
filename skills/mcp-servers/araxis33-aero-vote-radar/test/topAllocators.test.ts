import { test } from "node:test";
import assert from "node:assert/strict";
import { buildTopAllocators, pickTop, splitOf, together, type DromosBoard } from "../src/topAllocators.js";
import type { StakeOnChain } from "../src/stakes.js";

const pos = (id: string, rank: number | null, size = 20_000): DromosBoard["positions"][number] => ({
  id,
  owner: "0x" + id.padStart(40, "0"),
  contract: false,
  size,
  p: { "7d": [rank, 100, 0.5, 2] },
});

const on = (lastAllocated: number, ...allocations: [string, number][]): StakeOnChain => ({
  lastAllocated,
  readyAt: lastAllocated + 47 * 3600,
  allocations: allocations.map(([gauge, amount]) => ({ gauge, amount })),
});

test("pickTop: ranked positions only, best rank first, cut to n", () => {
  const board: DromosBoard = { asOf: "", minSize: 10_000, positions: [pos("3", 3), pos("9", null), pos("1", 1), pos("2", 2)] };
  assert.deepEqual(pickTop(board, 2).map((p) => p.id), ["1", "2"]);
});

test("splitOf: shares of what is placed across networks, gauges lower-cased, largest first", () => {
  const s = splitOf({ base: on(1, ["0xAA", 30], ["0xBB", 10]), arbitrum: on(2, ["0xCC", 60]), ink: on(0) });
  assert.deepEqual(s, [
    { chain: "arbitrum", gauge: "0xcc", share: 0.6 },
    { chain: "base", gauge: "0xaa", share: 0.3 },
    { chain: "base", gauge: "0xbb", share: 0.1 },
  ]);
  assert.deepEqual(splitOf({ base: on(0) }), []);
});

test("together: each position weighs the same, whatever its size; unplaced ones left out", () => {
  const t = together([
    { split: [{ chain: "base", gauge: "0xa", share: 1 }] },
    { split: [{ chain: "base", gauge: "0xa", share: 0.5 }, { chain: "base", gauge: "0xb", share: 0.5 }] },
    { split: [] },
  ]);
  assert.deepEqual(t, [
    { chain: "base", gauge: "0xa", share: 0.75 },
    { chain: "base", gauge: "0xb", share: 0.25 },
  ]);
});

test("buildTopAllocators: dromos figures, latest move on any network, split from the reads", () => {
  const board: DromosBoard = { asOf: "2026-10-26T17:39:10Z", minSize: 10_000, positions: [pos("7", 1, 31_000)] };
  const reads = new Map([["7", { base: on(100, ["0xA", 1]), optimism: on(500, ["0xB", 1]) }]]);
  const f = buildTopAllocators(board, reads, new Date(Date.UTC(2026, 9, 26)));
  assert.equal(f.boardAsOf, "2026-10-26T17:39:10Z");
  assert.equal(f.source, "dromos.kitchen");
  assert.deepEqual(
    { ...f.positions[0], split: f.positions[0].split.length },
    { rank: 1, id: "7", owner: pos("7", 1).owner, contract: false, sAero: 31_000, earned7d: 100, apr7d: 0.5, moves7d: 2, lastMoved: 500, split: 2 },
  );
  assert.equal(f.together.length, 2);
});

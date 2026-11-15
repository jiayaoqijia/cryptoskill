import { test, afterEach } from "node:test";
import assert from "node:assert/strict";
import { buildTopAllocators, pickTop, scanTopAllocators, splitOf, together, DROMOS_BOARD_URL, type DromosBoard } from "../src/topAllocators.js";
import type { StakeOnChain } from "../src/stakes.js";
import { CHAIN_NAMES } from "../src/radar.js";

// Selectors from src/stakes.ts, copied here (not exported) so the mocked RPC
// responses below can be routed by which on-chain call they answer.
const SEL_COOLDOWN = "0x6f5aa6ab";
const SEL_TOKEN_STATES = "0xaa9f3eca";
const SEL_REDUCTION = "0xbe8cfed2";
const SEL_GAUGES = "0xd596efe1";

// Mirrors stakes.ts's own word encoding so mocked eth_call results are shaped
// exactly as the real RPC's ABI-encoded return data would be.
const w = (hex: string) => hex.replace(/^0x/, "").toLowerCase().padStart(64, "0");
const wn = (n: number | bigint) => w(BigInt(n).toString(16));
const okResult = (hex: string) => ({ ok: true, json: async () => ({ result: "0x" + hex }) });

/** A no-allocations RPC answer for every LeafVoter selector readCooldown/readStakeOn touch. */
function rpcAnswer(data: string) {
  const sel = data.slice(0, 10);
  if (sel === SEL_COOLDOWN) return okResult(wn(172_800));
  if (sel === SEL_TOKEN_STATES) return okResult(wn(0) + wn(1_000_000) + wn(0) + wn(0));
  if (sel === SEL_REDUCTION) return okResult(wn(0));
  if (sel === SEL_GAUGES) return okResult(wn(0x20) + wn(0)); // empty allocatedGauges array
  throw new Error(`unexpected selector ${sel}`);
}

const originalFetch = global.fetch;
afterEach(() => {
  global.fetch = originalFetch;
});

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

test("pickTop: a position with no `p` field at all (untrusted JSON) is excluded, not a crash", () => {
  const noP = { id: "4", owner: "0x" + "4".padStart(40, "0"), contract: false, size: 20_000 } as unknown as DromosBoard["positions"][number];
  const board: DromosBoard = { asOf: "", minSize: 10_000, positions: [pos("1", 1), noP] };
  assert.deepEqual(pickTop(board).map((p) => p.id), ["1"]);
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

test("scanTopAllocators throws a clear error on a non-ok HTTP response from the leaderboard", async () => {
  global.fetch = (async () => ({ ok: false, status: 503 })) as unknown as typeof fetch;

  await assert.rejects(() => scanTopAllocators(new Date()), /dromos\.kitchen HTTP 503/);
});

test("scanTopAllocators throws when the leaderboard has no positions array", async () => {
  global.fetch = (async () => ({ ok: true, json: async () => ({ asOf: "", minSize: 10_000 }) })) as unknown as typeof fetch;

  await assert.rejects(() => scanTopAllocators(new Date()), /no positions in the leaderboard/);
});

test("scanTopAllocators throws if any network's reads fail, so a partial split never ships", async () => {
  const board: DromosBoard = { asOf: "2026-10-26T00:00:00Z", minSize: 10_000, positions: [pos("1", 1)] };
  global.fetch = (async (url: string, init?: RequestInit) => {
    if (url === DROMOS_BOARD_URL) return { ok: true, json: async () => board };
    if (url.includes("arc.io")) throw new Error("ECONNRESET"); // arc has only this one RPC configured
    const { data } = (JSON.parse(init!.body as string) as { params: [{ data: string }] }).params[0];
    return rpcAnswer(data);
  }) as unknown as typeof fetch;

  await assert.rejects(() => scanTopAllocators(new Date()), /ECONNRESET/);
});

test("scanTopAllocators reads the leaderboard and every network's split into one file", async () => {
  const board: DromosBoard = { asOf: "2026-10-26T00:00:00Z", minSize: 10_000, positions: [pos("1", 1, 31_000), pos("2", 2)] };
  global.fetch = (async (url: string, init?: RequestInit) => {
    if (url === DROMOS_BOARD_URL) return { ok: true, json: async () => board };
    const { data } = (JSON.parse(init!.body as string) as { params: [{ data: string }] }).params[0];
    return rpcAnswer(data);
  }) as unknown as typeof fetch;

  const file = await scanTopAllocators(new Date("2026-10-26T12:00:00Z"), 1);
  assert.equal(file.source, "dromos.kitchen");
  assert.equal(file.boardAsOf, board.asOf);
  assert.equal(file.positions.length, 1, "n=1 keeps only the best-ranked position");
  assert.equal(file.positions[0].id, "1");
  assert.equal(file.positions[0].lastMoved, 1_000_000, "the latest move, read on every network in CHAIN_NAMES");
  assert.equal(Object.keys(CHAIN_NAMES).length > 1, true, "sanity: more than one network was actually read");
});

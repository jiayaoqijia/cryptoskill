import { test, afterEach } from "node:test";
import assert from "node:assert/strict";
import {
  currentSplitPays,
  readCooldown,
  readStakeOn,
  readWalletStakes,
  timersByChain,
  untilText,
  withoutOwnSAero,
  LEAF_VOTER,
  VOTING_ESCROW,
  type Stake,
} from "../src/stakes.js";
import type { V3ScanFile, V3ScanGauge } from "../src/v3.js";

// Selectors from src/stakes.ts, copied here (not exported) so the mocked RPC
// responses below can be routed by which on-chain call they answer.
const SEL_BALANCE_OF = "0x70a08231";
const SEL_TOKEN_OF_OWNER = "0x2f745c59";
const SEL_POWER_OF = "0xe7e242d4";
const SEL_COOLDOWN = "0x6f5aa6ab";
const SEL_TOKEN_STATES = "0xaa9f3eca";
const SEL_REDUCTION = "0xbe8cfed2";
const SEL_GAUGES = "0xd596efe1";
const SEL_ALLOCATION = "0x1c3a964f";

// Mirrors stakes.ts's own word/hexOf encoding so mocked eth_call results are
// shaped exactly as the real RPC's ABI-encoded return data would be.
const w = (hex: string) => hex.replace(/^0x/, "").toLowerCase().padStart(64, "0");
const wn = (n: number | bigint) => w(BigInt(n).toString(16));
const okResult = (hex: string) => ({ ok: true, json: async () => ({ result: "0x" + hex }) });

const originalFetch = global.fetch;
afterEach(() => {
  global.fetch = originalFetch;
});

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

test("readWalletStakes reads a wallet's stakes with bounded concurrency, preserving their order", async () => {
  const STAKE_COUNT = 8;
  const word64 = (n: bigint | number) => BigInt(n).toString(16).padStart(64, "0");
  let inFlight = 0;
  let maxInFlight = 0;

  global.fetch = (async (_url: string, init?: RequestInit) => {
    const { params } = JSON.parse(init!.body as string) as { params: [{ data: string }] };
    const data = params[0].data;
    const selector = data.slice(0, 10);
    inFlight++;
    maxInFlight = Math.max(maxInFlight, inFlight);
    // Resolve out of order, so a naive concurrent-but-unordered implementation
    // would be caught by the order assertions below.
    await new Promise((resolve) => setTimeout(resolve, 5 - (inFlight % 3)));
    inFlight--;

    let result = "0x" + word64(0); // one zero word: enough for every per-network read this test touches
    if (selector === "0x70a08231") result = "0x" + word64(STAKE_COUNT); // balanceOf
    else if (selector === "0x2f745c59") result = "0x" + word64(Number(BigInt("0x" + data.slice(-64))) + 1); // tokenOfOwnerByIndex -> id = index + 1
    else if (selector === "0xe7e242d4") result = "0x" + word64(BigInt("0x" + data.slice(10, 74)) * 10n ** 18n); // balanceOfNFT, scaled

    return { ok: true, json: async () => ({ jsonrpc: "2.0", id: 1, result }) };
  }) as unknown as typeof fetch;

  const wallet = await readWalletStakes("0x1111111111111111111111111111111111111111");

  assert.equal(wallet.count, STAKE_COUNT);
  assert.deepEqual(wallet.stakes.map((s) => s.id), Array.from({ length: STAKE_COUNT }, (_, i) => BigInt(i + 1)));
  assert.deepEqual(wallet.stakes.map((s) => s.sAero), Array.from({ length: STAKE_COUNT }, (_, i) => i + 1));
  assert.equal(wallet.totalSAero, wallet.stakes.reduce((a, s) => a + s.sAero, 0));
  assert.ok(maxInFlight > 1, `expected overlapping stake reads, max in flight was ${maxInFlight}`);
});

test("readCooldown decodes the LeafVoter's answer, trying the chain's next RPC URL after the first fails", async () => {
  let calls = 0;
  global.fetch = (async () => {
    calls++;
    if (calls === 1) throw new Error("ECONNRESET");
    return okResult(wn(172_800));
  }) as unknown as typeof fetch;

  assert.equal(await readCooldown("ethereum"), 172_800);
  assert.equal(calls, 2, "a failed RPC should not be fatal while the chain has another URL configured");
});

test("readStakeOn decodes lastAllocated, derives readyAt from cooldown minus the reduction, and decodes each allocation", async () => {
  const gauge = "0x0000000000000000000000000000000000005678";
  global.fetch = (async (_url: string, init?: RequestInit) => {
    const { data } = (JSON.parse(init!.body as string) as { params: [{ data: string }] }).params[0];
    const sel = data.slice(0, 10);
    if (sel === SEL_TOKEN_STATES) return okResult(wn(0) + wn(1_000_000) + wn(0) + wn(0));
    if (sel === SEL_REDUCTION) return okResult(wn(3_600));
    if (sel === SEL_GAUGES) return okResult(wn(0x20) + wn(1) + w(gauge));
    if (sel === SEL_ALLOCATION) return okResult(wn(999_000_000_000_000_000_000n));
    throw new Error(`unexpected selector ${sel}`);
  }) as unknown as typeof fetch;

  const r = await readStakeOn("optimism", 42n, 172_800);
  assert.equal(r.lastAllocated, 1_000_000);
  assert.equal(r.readyAt, 1_000_000 + 172_800 - 3_600);
  assert.deepEqual(r.allocations, [{ gauge, amount: 999 }]);
});

test("readStakeOn never waits when the stake has not allocated on this network yet", async () => {
  global.fetch = (async (_url: string, init?: RequestInit) => {
    const { data } = (JSON.parse(init!.body as string) as { params: [{ data: string }] }).params[0];
    const sel = data.slice(0, 10);
    if (sel === SEL_TOKEN_STATES) return okResult(wn(0) + wn(0) + wn(0) + wn(0)); // lastAllocated 0: never allocated
    if (sel === SEL_REDUCTION) return okResult(wn(0));
    if (sel === SEL_GAUGES) return okResult(wn(0x20) + wn(0)); // empty array
    throw new Error(`unexpected selector ${sel}`);
  }) as unknown as typeof fetch;

  const r = await readStakeOn("arbitrum", 1n, 172_800);
  assert.equal(r.lastAllocated, 0);
  assert.equal(r.readyAt, 0);
  assert.deepEqual(r.allocations, []);
});

test("readWalletStakes totals sAero across the wallet's stakes and reports a network that never answers, without failing the whole read", async () => {
  const gauge = "0x0000000000000000000000000000000000005678";
  global.fetch = (async (url: string, init?: RequestInit) => {
    if (url.includes("arc.io")) throw new Error("ECONNRESET"); // arc has only this one RPC configured
    const { to, data } = (JSON.parse(init!.body as string) as { params: [{ to: string; data: string }] }).params[0];
    const sel = data.slice(0, 10);
    if (to === VOTING_ESCROW) {
      if (sel === SEL_BALANCE_OF) return okResult(wn(1));
      if (sel === SEL_TOKEN_OF_OWNER) return okResult(wn(777));
      if (sel === SEL_POWER_OF) return okResult(wn(12_345_000_000_000_000_000_000n));
    }
    if (to === LEAF_VOTER) {
      if (sel === SEL_COOLDOWN) return okResult(wn(172_800));
      if (sel === SEL_TOKEN_STATES) return okResult(wn(0) + wn(1_000_000) + wn(0) + wn(0));
      if (sel === SEL_REDUCTION) return okResult(wn(3_600));
      if (sel === SEL_GAUGES) return okResult(wn(0x20) + wn(1) + w(gauge));
      if (sel === SEL_ALLOCATION) return okResult(wn(999_000_000_000_000_000_000n));
    }
    throw new Error(`unexpected eth_call to ${to} ${sel}`);
  }) as unknown as typeof fetch;

  const wallet = await readWalletStakes("0x0000000000000000000000000000000000000001");
  assert.equal(wallet.count, 1);
  assert.equal(wallet.totalSAero, 12_345);
  assert.deepEqual(wallet.failed, ["arc"]);
  assert.equal(wallet.stakes[0].chains.arc, undefined);
  for (const chain of ["base", "ethereum", "optimism", "arbitrum", "ink", "robinhood"]) {
    assert.deepEqual(wallet.stakes[0].chains[chain], {
      lastAllocated: 1_000_000,
      readyAt: 1_000_000 + 172_800 - 3_600,
      allocations: [{ gauge, amount: 999 }],
    });
  }
});

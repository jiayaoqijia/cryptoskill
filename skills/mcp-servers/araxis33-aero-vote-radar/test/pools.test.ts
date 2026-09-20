import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { filterAlivePools, isMigratingFactory, resolvePoolInfo, withoutMigrating } from "../src/pools.js";

test("filterAlivePools drops pools (and their paired gauge) whose gauge is not alive", () => {
  const result = filterAlivePools(
    ["0xpoolA", "0xpoolB", "0xpoolC"],
    ["0xgaugeA", "0xgaugeB", "0xgaugeC"],
    [true, false, true],
  );
  assert.deepEqual(result, {
    alivePools: ["0xpoolA", "0xpoolC"],
    aliveGauges: ["0xgaugeA", "0xgaugeC"],
  });
});

test("filterAlivePools returns empty arrays when no gauge is alive", () => {
  const result = filterAlivePools(["0xpoolA"], ["0xgaugeA"], [false]);
  assert.deepEqual(result, { alivePools: [], aliveGauges: [] });
});

test("resolvePoolInfo resolves a pool whose symbol/token0/token1 calls all succeed", () => {
  const { pools, skipped } = resolvePoolInfo(
    ["0xpoolA"],
    ["0xgaugeA"],
    [{ status: "success", result: "vAMM-A/B" }],
    [{ status: "success", result: "0xtokenA" }],
    [{ status: "success", result: "0xtokenB" }],
  );
  assert.equal(skipped, 0);
  assert.deepEqual(pools, [
    { address: "0xpoolA", symbol: "vAMM-A/B", token0: "0xtokenA", token1: "0xtokenB", gauge: "0xgaugeA", gaugeAlive: true },
  ]);
});

// Slipstream pools have no `symbol()` at all. Requiring one dropped every one
// of them: 107 pools survived where 359 exist, and the epoch of 2026-09-03 read
// as $121,034 of protocol incentives against an actual $2,131,626. These two
// tests are the guard on the half of Aerodrome that used to be invisible.
test("resolvePoolInfo names a pool with no symbol of its own from the pair it holds", () => {
  const { pools, skipped } = resolvePoolInfo(
    ["0xclPool"],
    ["0xgauge"],
    [{ status: "failure" }],
    [{ status: "success", result: "0xWETH" }],
    [{ status: "success", result: "0xcbBTC" }],
    new Map([
      ["0xweth", "WETH"],
      ["0xcbbtc", "cbBTC"],
    ]),
  );
  assert.equal(skipped, 0);
  assert.equal(pools[0].symbol, "CL-WETH/cbBTC");
  assert.equal(pools[0].address, "0xclPool");
});

test("resolvePoolInfo prefers a pool's own symbol over the composed pair name", () => {
  const { pools } = resolvePoolInfo(
    ["0xpool"],
    ["0xgauge"],
    [{ status: "success", result: "vAMM-A/B" }],
    [{ status: "success", result: "0xA" }],
    [{ status: "success", result: "0xB" }],
    new Map([
      ["0xa", "A"],
      ["0xb", "B"],
    ]),
  );
  assert.equal(pools[0].symbol, "vAMM-A/B");
});

test("resolvePoolInfo still skips a symbol-less pool when its tokens cannot be named either", () => {
  const { pools, skipped } = resolvePoolInfo(
    ["0xpool"],
    ["0xgauge"],
    [{ status: "failure" }],
    [{ status: "success", result: "0xA" }],
    [{ status: "success", result: "0xB" }],
    new Map([["0xa", "A"]]),
  );
  assert.equal(skipped, 1);
  assert.deepEqual(pools, []);
});

test("resolvePoolInfo skips a pool whose symbol call failed, without dropping the ones after it", () => {
  const { pools, skipped } = resolvePoolInfo(
    ["0xpoolA", "0xpoolB"],
    ["0xgaugeA", "0xgaugeB"],
    [{ status: "failure" }, { status: "success", result: "vAMM-B/C" }],
    [{ status: "success", result: "0xtokenA" }, { status: "success", result: "0xtokenB" }],
    [{ status: "success", result: "0xtokenA2" }, { status: "success", result: "0xtokenC" }],
  );
  assert.equal(skipped, 1);
  assert.deepEqual(pools, [
    { address: "0xpoolB", symbol: "vAMM-B/C", token0: "0xtokenB", token1: "0xtokenC", gauge: "0xgaugeB", gaugeAlive: true },
  ]);
});

test("resolvePoolInfo skips a pool if either token0 or token1 (not just symbol) fails", () => {
  const { pools: skippedOnToken0, skipped: skipped0 } = resolvePoolInfo(
    ["0xpoolA"],
    ["0xgaugeA"],
    [{ status: "success", result: "vAMM-A/B" }],
    [{ status: "failure" }],
    [{ status: "success", result: "0xtokenB" }],
  );
  assert.equal(skipped0, 1);
  assert.deepEqual(skippedOnToken0, []);

  const { pools: skippedOnToken1, skipped: skipped1 } = resolvePoolInfo(
    ["0xpoolA"],
    ["0xgaugeA"],
    [{ status: "success", result: "vAMM-A/B" }],
    [{ status: "success", result: "0xtokenA" }],
    [{ status: "failure" }],
  );
  assert.equal(skipped1, 1);
  assert.deepEqual(skippedOnToken1, []);
});

// 16.09.2026: a voter could not find the radar's CL-cbBTC/EDGE pick on
// Aerodrome's vote page. Its factory is one Aerodrome is migrating away from,
// and the vote page's default list leaves those pools out. That day they were
// 163 of the 360 ranked pools and 9 of the top 20.
const OLD_SLIPSTREAM = "0x5e7BB104d84c7CB9B682AaC2F3d509f5F406809A";
const NEW_SLIPSTREAM = "0xf8f2eB4940CFE7d13603DDDD87f123820Fc061Ef";

test("isMigratingFactory recognises both migrating factories in any letter case, and nothing else", () => {
  assert.equal(isMigratingFactory(OLD_SLIPSTREAM), true);
  assert.equal(isMigratingFactory(OLD_SLIPSTREAM.toLowerCase()), true);
  assert.equal(isMigratingFactory("0xaDe65c38CD4849aDBA595a4323a8C7DdfE89716a"), true);
  assert.equal(isMigratingFactory(NEW_SLIPSTREAM), false);
  assert.equal(isMigratingFactory(null), false);
  assert.equal(isMigratingFactory(undefined), false);
});

test("resolvePoolInfo marks a pool from a migrating factory, and only that pool", () => {
  const { pools } = resolvePoolInfo(
    ["0xold", "0xnew"],
    ["0xg1", "0xg2"],
    [{ status: "failure" }, { status: "failure" }],
    [{ status: "success", result: "0xcbBTC" }, { status: "success", result: "0xcbBTC" }],
    [{ status: "success", result: "0xEDGE" }, { status: "success", result: "0xEDGE" }],
    new Map([["0xcbbtc", "cbBTC"], ["0xedge", "EDGE"]]),
    [{ status: "success", result: OLD_SLIPSTREAM }, { status: "success", result: NEW_SLIPSTREAM }],
  );
  assert.equal(pools[0].migrating, true);
  assert.equal("migrating" in pools[1], false);
});

test("resolvePoolInfo keeps a pool unmarked when its factory call failed or was not made", () => {
  const { pools } = resolvePoolInfo(
    ["0xpool"],
    ["0xgauge"],
    [{ status: "success", result: "vAMM-A/B" }],
    [{ status: "success", result: "0xA" }],
    [{ status: "success", result: "0xB" }],
    undefined,
    [{ status: "failure" }],
  );
  assert.equal("migrating" in pools[0], false);
});

test("withoutMigrating drops migrating pools and keeps the order of the rest", () => {
  const row = (address: string, migrating?: true) => ({
    pool: { address, symbol: address, token0: "0xa", token1: "0xb", gauge: "0xg", gaugeAlive: true, ...(migrating ? { migrating } : {}) },
  });
  const kept = withoutMigrating([row("0x1"), row("0x2", true), row("0x3"), row("0x4", true)]);
  assert.deepEqual(kept.map((r) => r.pool.address), ["0x1", "0x3"]);
});

test("resolvePoolInfo pairs each resolved pool with its gauge by matching index, not original position", () => {
  const { pools } = resolvePoolInfo(
    ["0xpoolA", "0xpoolB"],
    ["0xgaugeA", "0xgaugeB"],
    [{ status: "success", result: "sym-A" }, { status: "success", result: "sym-B" }],
    [{ status: "success", result: "0xt0A" }, { status: "success", result: "0xt0B" }],
    [{ status: "success", result: "0xt1A" }, { status: "success", result: "0xt1B" }],
  );
  assert.equal(pools[0].gauge, "0xgaugeA");
  assert.equal(pools[1].gauge, "0xgaugeB");
});

/**
 * `fetchActivePools` talks to a shared public RPC, so it has no unit test of its
 * own — and that is exactly where the scan has now broken twice. Overlapping the
 * per-pool multicalls over ~860 pools does not degrade gracefully: the RPC drops
 * the entire burst and every call comes back failed, which reaches the snapshot
 * as "0 pools" and stops the site updating. Measured on 2026-09-20 against the
 * live chain: 0/866 successes on all three rounds run concurrently, 360/865/865
 * on the same three run one after another.
 *
 * On 2026-09-16 the answer was to pull one call out of the concurrent batch; the
 * three that stayed behind failed the same way four days later. So the invariant
 * is not "fewer at once", it is "one at a time", and this test reads the source
 * to hold it — there is no seam to assert it through at runtime.
 */
test("fetchActivePools issues its per-pool multicalls one at a time, never concurrently", () => {
  const source = readFileSync(new URL("../src/pools.ts", import.meta.url), "utf8");
  const start = source.indexOf("export async function fetchActivePools");
  assert.notEqual(start, -1, "fetchActivePools not found in src/pools.ts");
  const end = source.indexOf("\nexport ", start + 1);
  const body = source.slice(start, end === -1 ? undefined : end);

  assert.equal(
    /Promise\.all/.test(body),
    false,
    "fetchActivePools must not run multicalls concurrently — a shared public RPC drops the whole burst",
  );
});

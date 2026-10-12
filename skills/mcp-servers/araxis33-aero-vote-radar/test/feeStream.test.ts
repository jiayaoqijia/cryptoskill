import { test } from "node:test";
import assert from "node:assert/strict";
import { accruedBetween, buildFeeCounters, type FeeCounter } from "../src/feeStream.js";
import type { MulticallOutcome, PoolInfo } from "../src/pools.js";

const tokens: [string, string] = ["0xa", "0xb"];
const cl = (a: string, b: string): FeeCounter => ({ pool: "0xp", kind: "cl", tokens, gaugeFees: [a, b] });
const v2 = (i0: string, i1: string, lp: string): FeeCounter => ({ pool: "0xp", kind: "v2", tokens, index: [i0, i1], gaugeLp: lp });

const ok = (result: unknown): MulticallOutcome => ({ status: "success", result });
const fail: MulticallOutcome = { status: "failure" };

const pool = (address: string, gauge = `${address}-gauge`): PoolInfo => ({
  address,
  symbol: `SYM-${address}`,
  token0: `${address}-t0`,
  token1: `${address}-t1`,
  gauge,
  gaugeAlive: true,
});

test("CL: accrual is the growth of gaugeFees between two reads", () => {
  assert.deepEqual(accruedBetween(cl("100", "5"), cl("250", "9")), [150n, 4n]);
});

test("CL: a drop means the gauge collected in between, so the later reading is what accrued since", () => {
  assert.deepEqual(accruedBetween(cl("900", "40"), cl("30", "2")), [30n, 2n]);
});

test("v2: accrual is index growth times the gauge's LP, at the index's 1e18 scale", () => {
  const e18 = 10n ** 18n;
  // +2 tokens per LP on token0, +0.5 on token1, gauge holds 3 LP.
  const prev = v2((10n * e18).toString(), (1n * e18).toString(), (3n * e18).toString());
  const next = v2((12n * e18).toString(), ((3n * e18) / 2n).toString(), (3n * e18).toString());
  assert.deepEqual(accruedBetween(prev, next), [6n * e18, (3n * e18) / 2n]);
});

test("v2: an unchanged index accrues nothing, even with LP in the gauge", () => {
  assert.deepEqual(accruedBetween(v2("5", "5", "1000"), v2("5", "5", "1000")), [0n, 0n]);
});

test("a pool that switched kind between reads is an error, not a silent zero", () => {
  assert.throws(() => accruedBetween(cl("1", "1"), v2("1", "1", "1")), /changed kind/);
});

test("buildFeeCounters: a pool whose gaugeFees() succeeds is read as CL, tokens lowercased", () => {
  const pools = [pool("0xP1")];
  const out = buildFeeCounters(pools, [ok([10n, 20n])], [], [], []);
  assert.deepEqual(out, [
    { pool: "0xp1", kind: "cl", tokens: ["0xp1-t0", "0xp1-t1"], gaugeFees: ["10", "20"] },
  ]);
});

test("buildFeeCounters: a pool whose gaugeFees() fails is read as classic from index0/index1/balanceOf", () => {
  const pools = [pool("0xP1")];
  const out = buildFeeCounters(pools, [fail], [ok(5n * 10n ** 18n)], [ok(2n * 10n ** 18n)], [ok(3n * 10n ** 18n)]);
  assert.deepEqual(out, [
    { pool: "0xp1", kind: "v2", tokens: ["0xp1-t0", "0xp1-t1"], index: [(5n * 10n ** 18n).toString(), (2n * 10n ** 18n).toString()], gaugeLp: (3n * 10n ** 18n).toString() },
  ]);
});

test("buildFeeCounters: a classic pool missing any one of index0/index1/balanceOf is dropped, not half-filled", () => {
  const pools = [pool("0xP1")];
  assert.deepEqual(buildFeeCounters(pools, [fail], [fail], [ok(1n)], [ok(1n)]), []);
  assert.deepEqual(buildFeeCounters(pools, [fail], [ok(1n)], [fail], [ok(1n)]), []);
  assert.deepEqual(buildFeeCounters(pools, [fail], [ok(1n)], [ok(1n)], [fail]), []);
});

test("buildFeeCounters: CL and classic pools mixed keep their alignment across the filtered classic-only arrays", () => {
  // P1 is CL, P2 and P3 are classic (gaugeFees fails) — so the classic-only
  // arrays have length 2, indexed [P2, P3], not [P1, P2, P3]. A j-vs-i mixup
  // here would silently attach P3's index/balance reads to P2 or vice versa.
  const pools = [pool("0xP1"), pool("0xP2"), pool("0xP3")];
  const cls = [ok([1n, 1n]), fail, fail];
  const index0 = [ok(100n), ok(200n)]; // [P2, P3]
  const index1 = [ok(10n), ok(20n)];
  const gaugeLp = [ok(1n), ok(2n)];

  const out = buildFeeCounters(pools, cls, index0, index1, gaugeLp);

  assert.deepEqual(out, [
    { pool: "0xp1", kind: "cl", tokens: ["0xp1-t0", "0xp1-t1"], gaugeFees: ["1", "1"] },
    { pool: "0xp2", kind: "v2", tokens: ["0xp2-t0", "0xp2-t1"], index: ["100", "10"], gaugeLp: "1" },
    { pool: "0xp3", kind: "v2", tokens: ["0xp3-t0", "0xp3-t1"], index: ["200", "20"], gaugeLp: "2" },
  ]);
});

test("buildFeeCounters: a pool failing on every read (CL and classic alike) is left out entirely", () => {
  const pools = [pool("0xP1")];
  assert.deepEqual(buildFeeCounters(pools, [fail], [fail], [fail], [fail]), []);
});

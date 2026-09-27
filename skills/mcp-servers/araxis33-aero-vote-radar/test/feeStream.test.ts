import { test } from "node:test";
import assert from "node:assert/strict";
import { accruedBetween, type FeeCounter } from "../src/feeStream.js";

const tokens: [string, string] = ["0xa", "0xb"];
const cl = (a: string, b: string): FeeCounter => ({ pool: "0xp", kind: "cl", tokens, gaugeFees: [a, b] });
const v2 = (i0: string, i1: string, lp: string): FeeCounter => ({ pool: "0xp", kind: "v2", tokens, index: [i0, i1], gaugeLp: lp });

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

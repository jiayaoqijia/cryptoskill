import { test } from "node:test";
import assert from "node:assert/strict";
import { formatPromise } from "../src/promise-cli.js";
import type { EpochPromise, PromiseRow } from "../src/promise.js";

const row = (overrides: Partial<PromiseRow> = {}): PromiseRow => ({
  symbol: "WETH/USDC",
  pool: "0xpool",
  forecastUsd: 100,
  paidUsd: 80,
  ratio: 0.8,
  ...overrides,
});

const epoch = (overrides: Partial<EpochPromise> = {}): EpochPromise => ({
  epochStart: "2026-08-28",
  scannedAt: "2026-08-27T12:00:00.000Z",
  rows: [row()],
  medianRatio: 0.8,
  paidAtLeastForecast: 0,
  paidUnderHalf: 0,
  ...overrides,
});

test("formatPromise prints the epoch and scan date, and each row's symbol, quote, and payout", () => {
  const out = formatPromise([epoch()]);
  assert.ok(out.includes("Epoch of 2026-08-28 (scan 2026-08-27T12:00:00.000Z)"));
  assert.ok(out.includes("WETH/USDC"));
  assert.ok(out.includes("$100.00"));
  assert.ok(out.includes("$80.00"));
  assert.ok(out.includes("0.80"));
});

test("formatPromise renders the median ratio and the two coverage percentages as whole numbers", () => {
  const out = formatPromise([epoch({ medianRatio: 0.753, paidAtLeastForecast: 0.5, paidUnderHalf: 0.25 })]);
  assert.ok(out.includes("median paid/quoted 0.75"));
  assert.ok(out.includes("paid at least the quote on 50%"));
  assert.ok(out.includes("under half on 25%"));
});

test("formatPromise lists every epoch passed to it, in order", () => {
  const out = formatPromise([epoch({ epochStart: "2026-08-28" }), epoch({ epochStart: "2026-09-04" })]);
  const first = out.indexOf("Epoch of 2026-08-28");
  const second = out.indexOf("Epoch of 2026-09-04");
  assert.ok(first >= 0 && second > first);
});

test("formatPromise renders nothing for an empty epoch list beyond the trailing basis note", () => {
  const out = formatPromise([]);
  assert.ok(!out.includes("Epoch of"));
  assert.ok(out.includes("USD earned by"));
});

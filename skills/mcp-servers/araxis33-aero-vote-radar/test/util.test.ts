import { test } from "node:test";
import assert from "node:assert/strict";
import { formatError, isValidAddress, mapWithConcurrency, padCol } from "../src/util.js";

test("isValidAddress accepts a well-formed 0x-prefixed 40-hex-character address", () => {
  assert.equal(isValidAddress("0x1234567890abcdef1234567890ABCDEF12345678"), true);
});

test("isValidAddress rejects a missing 0x prefix", () => {
  assert.equal(isValidAddress("1234567890abcdef1234567890abcdef12345678"), false);
});

test("isValidAddress rejects the wrong length", () => {
  assert.equal(isValidAddress("0x1234"), false);
  assert.equal(isValidAddress("0x1234567890abcdef1234567890abcdef123456789"), false);
});

test("isValidAddress rejects non-hex characters", () => {
  assert.equal(isValidAddress("0xzzzz567890abcdef1234567890abcdef12345678"), false);
});

test("mapWithConcurrency preserves input order regardless of completion order", async () => {
  // Earlier items resolve slower than later ones, so this only passes if results
  // are written to their original index rather than in completion order.
  const items = [30, 10, 20, 0];
  const result = await mapWithConcurrency(items, 4, async (delay, i) => {
    await new Promise((resolve) => setTimeout(resolve, delay));
    return i;
  });
  assert.deepEqual(result, [0, 1, 2, 3]);
});

test("mapWithConcurrency never runs more than `concurrency` tasks at once", async () => {
  let inFlight = 0;
  let maxInFlight = 0;
  const items = Array.from({ length: 10 }, (_, i) => i);

  await mapWithConcurrency(items, 3, async (item) => {
    inFlight++;
    maxInFlight = Math.max(maxInFlight, inFlight);
    await new Promise((resolve) => setTimeout(resolve, 5));
    inFlight--;
    return item;
  });

  assert.ok(maxInFlight <= 3, `max concurrent tasks was ${maxInFlight}, expected <= 3`);
});

test("mapWithConcurrency runs every item exactly once and maps values correctly", async () => {
  const items = [1, 2, 3, 4, 5];
  const result = await mapWithConcurrency(items, 2, async (n) => n * 2);
  assert.deepEqual(result, [2, 4, 6, 8, 10]);
});

test("mapWithConcurrency propagates a rejection from any task", async () => {
  const items = [1, 2, 3];
  await assert.rejects(
    () =>
      mapWithConcurrency(items, 2, async (n) => {
        if (n === 2) throw new Error("boom");
        return n;
      }),
    /boom/,
  );
});

test("mapWithConcurrency handles an empty input array", async () => {
  const result = await mapWithConcurrency([], 4, async (n: number) => n);
  assert.deepEqual(result, []);
});

test("mapWithConcurrency works when concurrency exceeds the number of items", async () => {
  const items = [1, 2, 3];
  const result = await mapWithConcurrency(items, 100, async (n) => n + 1);
  assert.deepEqual(result, [2, 3, 4]);
});

test("formatError prefers a viem-style shortMessage over the full multi-paragraph message", () => {
  const err = new Error(
    "HTTP request failed.\n\nDocs: https://viem.sh/docs/x\nDetails: over rate limit\n\nVersion: viem@2.55.2",
  );
  (err as Error & { shortMessage: string }).shortMessage = "HTTP request failed.";
  assert.equal(formatError(err), "HTTP request failed.");
});

test("formatError falls back to the plain message for a regular Error with no shortMessage", () => {
  assert.equal(formatError(new Error("boom")), "boom");
});

test("formatError stringifies a non-Error thrown value", () => {
  assert.equal(formatError("plain string throw"), "plain string throw");
});

test("padCol pads a short value out to the column width", () => {
  assert.equal(padCol("vAMM-WETH/MET", 18), "vAMM-WETH/MET".padEnd(18));
});

test("padCol truncates a value at or past the width and still separates it from the next column", () => {
  const longSymbol = "vAMM-VIRTUAL/cbBTC"; // 18 chars: a real pool symbol, at the column width itself
  const result = padCol(longSymbol, 18);

  assert.equal(result.length, 18);
  assert.ok(result.endsWith(" "), "a truncated value must still leave a separator before the next column");
  assert.ok(result.startsWith(longSymbol.slice(0, 16)), "truncation should keep as much of the original text as fits");
});

test("padCol never grows a column narrower than 1 character wide", () => {
  assert.equal(padCol("toolong", 1).length, 1);
});

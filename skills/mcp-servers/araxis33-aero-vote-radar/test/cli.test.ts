import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import { fmtUsd, parseAmountFlag, parseChainFlag, parsePositiveIntFlag, scanLine, walletToJson } from "../src/cli.js";
import type { V3ScanFile } from "../src/v3.js";

test("parsePositiveIntFlag: fallback when absent, undefined for garbage or a dangling flag", () => {
  assert.equal(parsePositiveIntFlag([], "top", 15), 15);
  assert.equal(parsePositiveIntFlag(["--top", "5"], "top", 15), 5);
  assert.equal(parsePositiveIntFlag(["--top", "abc"], "top", 15), undefined);
  assert.equal(parsePositiveIntFlag(["--top", "-2"], "top", 15), undefined);
  assert.equal(parsePositiveIntFlag(["--top"], "top", 15), undefined);
});

test("parseAmountFlag accepts thousands separators and rejects zero", () => {
  assert.equal(parseAmountFlag([], 10_000), 10_000);
  assert.equal(parseAmountFlag(["--amount", "25,000"], undefined), 25_000);
  assert.equal(parseAmountFlag(["--amount", "0"], 10_000), undefined);
  assert.equal(parseAmountFlag(["--amount"], 10_000), undefined);
});

test("parseChainFlag: known network, any case; null for an unknown or missing value", () => {
  assert.equal(parseChainFlag([]), undefined);
  assert.equal(parseChainFlag(["--chain", "Optimism"]), "optimism");
  assert.equal(parseChainFlag(["--chain", "solana"]), null);
  assert.equal(parseChainFlag(["--chain"]), null);
});

test("fmtUsd keeps cents under $1,000 and four places under $1", () => {
  assert.equal(fmtUsd(1234.6), "$1,235");
  assert.equal(fmtUsd(3.456), "$3.46");
  assert.equal(fmtUsd(0.01234), "$0.0123");
  assert.equal(fmtUsd(0), "$0");
});

test("scanLine flags a scan older than 3 h", () => {
  const scan = { checkedAt: "2026-10-25T10:00:00.000Z", windowHours: 66.4, gauges: [{ chain: "base" }, { chain: "arc" }] } as unknown as V3ScanFile;
  assert.match(scanLine(scan, Date.parse("2026-10-25T10:30:00.000Z")), /on 2 networks under an hour ago; fees from the last 66 h/);
  assert.match(scanLine(scan, Date.parse("2026-10-25T15:00:00.000Z")), /5 h ago — older than usual/);
});

test("walletToJson turns stake ids into strings so JSON.stringify works", () => {
  const out = walletToJson({ address: "0x1", count: 1, totalSAero: 5, failed: [], stakes: [{ id: 619n, sAero: 5, chains: {} }] });
  assert.equal(JSON.parse(JSON.stringify(out)).stakes[0].id, "619");
});

/** Runs the CLI with tsx and returns its exit code and output. No network: these paths stop before any fetch. */
function runCli(args: string[]): Promise<{ code: number | null; stdout: string; stderr: string }> {
  const cli = fileURLToPath(new URL("../src/cli.ts", import.meta.url));
  return new Promise((resolve) => {
    const child = spawn(process.execPath, ["--import", "tsx", cli, ...args]);
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (d) => (stdout += d));
    child.stderr.on("data", (d) => (stderr += d));
    child.on("close", (code) => resolve({ code, stdout, stderr }));
  });
}

test("no command prints usage and exits 0", async () => {
  const r = await runCli([]);
  assert.equal(r.code, 0);
  assert.match(r.stdout, /my-stakes <address>/);
});

test("an unknown or old veAERO command exits 1 with usage", async () => {
  for (const cmd of ["poolz", "backtest", "my-veaero"]) {
    const r = await runCli([cmd]);
    assert.equal(r.code, 1, cmd);
    assert.match(r.stderr, /Unknown command/);
  }
});

test("recommend without --amount or --address exits 1", async () => {
  const r = await runCli(["recommend"]);
  assert.equal(r.code, 1);
  assert.match(r.stderr, /needs --amount <sAERO> or --address/);
});

test("pools with an unknown network exits 1", async () => {
  const r = await runCli(["pools", "--chain", "solana"]);
  assert.equal(r.code, 1);
  assert.match(r.stderr, /--chain must be one of: base, ethereum/);
});

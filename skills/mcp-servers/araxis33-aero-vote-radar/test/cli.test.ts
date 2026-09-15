import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import {
  chooseVoteTokenId,
  epochDeadlineLine,
  parsePositiveIntFlag,
  parseUnitIntervalFlag,
  parseVoteBasisFlag,
  poolEfficiencyToJson,
  resolveBudget,
  veAeroPositionsToJson,
} from "../src/cli.js";
import { EPOCH_SECONDS } from "../src/trend.js";
import type { PoolEfficiency } from "../src/efficiency.js";
import type { VeNftSummary } from "../src/veAero.js";

/** Runs `fn` with console.error silenced, returning its return value and everything logged. */
async function captureStderr<T>(fn: () => Promise<T>): Promise<{ result: T; logged: string[] }> {
  const original = console.error;
  const logged: string[] = [];
  console.error = (...parts: unknown[]) => {
    logged.push(parts.join(" "));
  };
  try {
    const result = await fn();
    return { result, logged };
  } finally {
    console.error = original;
  }
}

test("parsePositiveIntFlag returns the fallback when the flag is absent", () => {
  assert.equal(parsePositiveIntFlag([], "top", 20), 20);
});

test("parsePositiveIntFlag parses a valid positive integer flag", () => {
  assert.equal(parsePositiveIntFlag(["--top", "5"], "top", 20), 5);
});

test("parsePositiveIntFlag rejects a non-numeric value instead of returning NaN", () => {
  assert.equal(parsePositiveIntFlag(["--top", "abc"], "top", 20), undefined);
});

test("parsePositiveIntFlag rejects zero and negative values", () => {
  assert.equal(parsePositiveIntFlag(["--top", "0"], "top", 20), undefined);
  assert.equal(parsePositiveIntFlag(["--top", "-5"], "top", 20), undefined);
});

test("parsePositiveIntFlag rejects non-integer values", () => {
  assert.equal(parsePositiveIntFlag(["--top", "3.5"], "top", 20), undefined);
});

test("parsePositiveIntFlag rejects a dangling flag with no value instead of silently using the fallback", () => {
  assert.equal(parsePositiveIntFlag(["--top"], "top", 20), undefined);
  assert.equal(parsePositiveIntFlag(["--veaero", "25000", "--top"], "top", 20), undefined);
});

test("parsePositiveIntFlag accepts a value at or below the given max", () => {
  assert.equal(parsePositiveIntFlag(["--epochs", "20"], "epochs", 6, 20), 20);
  assert.equal(parsePositiveIntFlag(["--epochs", "6"], "epochs", 6, 20), 6);
});

test("parsePositiveIntFlag rejects a value above the given max instead of silently clamping it", () => {
  assert.equal(parsePositiveIntFlag(["--epochs", "21"], "epochs", 6, 20), undefined);
  assert.equal(parsePositiveIntFlag(["--epochs", "100000"], "epochs", 6, 20), undefined);
});

test("parsePositiveIntFlag ignores max when the flag is absent, still returning the fallback", () => {
  assert.equal(parsePositiveIntFlag([], "epochs", 6, 20), 6);
});

test("parseUnitIntervalFlag returns the fallback when the flag is absent", () => {
  assert.equal(parseUnitIntervalFlag([], "min-consistency", 0), 0);
});

test("parseUnitIntervalFlag accepts both ends of the 0..1 range and a fraction inside it", () => {
  assert.equal(parseUnitIntervalFlag(["--min-consistency", "0"], "min-consistency", 0), 0);
  assert.equal(parseUnitIntervalFlag(["--min-consistency", "1"], "min-consistency", 0), 1);
  assert.equal(parseUnitIntervalFlag(["--min-consistency", "0.55"], "min-consistency", 0), 0.55);
});

test("parseUnitIntervalFlag rejects values outside 0..1 rather than silently clamping", () => {
  assert.equal(parseUnitIntervalFlag(["--min-consistency", "-0.1"], "min-consistency", 0), undefined);
  assert.equal(parseUnitIntervalFlag(["--min-consistency", "1.5"], "min-consistency", 0), undefined);
});

test("parseUnitIntervalFlag rejects non-numeric and dangling flags", () => {
  assert.equal(parseUnitIntervalFlag(["--min-consistency", "abc"], "min-consistency", 0), undefined);
  assert.equal(parseUnitIntervalFlag(["--min-consistency"], "min-consistency", 0), undefined);
  assert.equal(parseUnitIntervalFlag(["--min-consistency", "Infinity"], "min-consistency", 0), undefined);
});

test("poolEfficiencyToJson includes epochsObserved and the consistency fields, matching the MCP list_pool_efficiency shape", () => {
  const p: PoolEfficiency = {
    pool: { address: "0xpool", symbol: "vAMM-TEST/USDC", token0: "0xtoken0", token1: "0xtoken1", gauge: "0xgauge", gaugeAlive: true },
    latestEpochTs: 100,
    currentVotesVeAero: 10,
    latestEpochUsd: 5,
    trailingAvgUsd: 4,
    epochsObserved: 3,
    epochUsdSeries: [5, 4, 3],
    epochVotesSeries: [10, 10, 10],
    currentValuePerVote: 0.5,
    predictedValuePerVote: 0.4,
    predictiveEdge: -0.2,
    volatility: 0.25,
    consistency: 0.8,
    latestEpochBribes: [],
    latestEpochFees: [],
  };

  // Only 3 epochs observed — below MOMENTUM_MIN_EPOCHS, so momentum is null
  // regardless of the "as of" time passed in.
  assert.deepEqual(poolEfficiencyToJson(p, 1000), {
    symbol: "vAMM-TEST/USDC",
    pool: "0xpool",
    votesVeAero: 10,
    currentValuePerVote: 0.5,
    predictedValuePerVote: 0.4,
    predictiveEdge: -0.2,
    epochsObserved: 3,
    volatility: 0.25,
    consistency: 0.8,
    momentum: null,
  });
});

test("poolEfficiencyToJson wires momentum from the pool's epoch series and the given time, matching the MCP tool", () => {
  const p: PoolEfficiency = {
    pool: { address: "0xpool", symbol: "vAMM-TEST/USDC", token0: "0xtoken0", token1: "0xtoken1", gauge: "0xgauge", gaugeAlive: true },
    latestEpochTs: 1_786_579_200, // a Thursday 00:00 UTC epoch boundary
    currentVotesVeAero: 10,
    latestEpochUsd: 400,
    trailingAvgUsd: 250,
    epochsObserved: 4,
    epochUsdSeries: [400, 400, 100, 100],
    epochVotesSeries: [10, 10, 10, 10],
    currentValuePerVote: 40,
    predictedValuePerVote: 25,
    predictiveEdge: -0.375,
    volatility: 0.6,
    consistency: 0.625,
    latestEpochBribes: [],
    latestEpochFees: [],
  };

  // A full epoch after latestEpochTs: that epoch has closed, so all 4 entries
  // are completed history and momentum compares the recent half to the older half.
  const asOfUnixSeconds = p.latestEpochTs + EPOCH_SECONDS;
  assert.equal(poolEfficiencyToJson(p, asOfUnixSeconds).momentum, 3);
});

test("veAeroPositionsToJson sums voting power across locks and matches the MCP get_my_veaero shape", () => {
  const positions: VeNftSummary[] = [
    { id: "6", votingPowerVeAero: 11_362_738.622, expiresAt: 0, isPermanent: true },
    { id: "17324", votingPowerVeAero: 107_871.726, expiresAt: 1_893_456_000, isPermanent: false },
  ];

  assert.deepEqual(veAeroPositionsToJson("0xAccount", positions), {
    address: "0xAccount",
    totalVeAero: 11_362_738.622 + 107_871.726,
    locks: positions,
  });
});

test("veAeroPositionsToJson returns a zero total and empty locks for an account with no veAERO", () => {
  assert.deepEqual(veAeroPositionsToJson("0xEmpty", []), {
    address: "0xEmpty",
    totalVeAero: 0,
    locks: [],
  });
});

// resolveBudget backs both `recommend` and `backtest`'s budget resolution, but
// unlike the rest of this file's flag parsers it had no direct test coverage —
// these cover every branch that doesn't require a live RPC call (a valid
// --address still hits fetchVeAeroPositions, so that branch is exercised live
// via the CLI instead, same as fetchActivePools/fetchVeAeroPositions elsewhere).

test("resolveBudget rejects passing both --veaero and --address", async () => {
  const { result, logged } = await captureStderr(() =>
    resolveBudget(["--veaero", "25000", "--address", "0x1234567890123456789012345678901234567890"], "USAGE"),
  );
  assert.equal(result, null);
  assert.ok(logged.some((l) => l.includes("not both")), `expected a "not both" message, got: ${logged.join(" | ")}`);
});

test("resolveBudget rejects a malformed --address before attempting any RPC call", async () => {
  const { result, logged } = await captureStderr(() => resolveBudget(["--address", "not-an-address"], "USAGE"));
  assert.equal(result, null);
  assert.ok(logged.some((l) => l.includes("40-character hex address")), `expected an address-format message, got: ${logged.join(" | ")}`);
});

test("resolveBudget rejects a missing --veaero/--address entirely", async () => {
  const { result, logged } = await captureStderr(() => resolveBudget([], "USAGE"));
  assert.equal(result, null);
  assert.ok(logged.some((l) => l.includes("finite positive number")), `expected an amount-format message, got: ${logged.join(" | ")}`);
});

test("resolveBudget rejects a non-numeric --veaero", async () => {
  const { result } = await captureStderr(() => resolveBudget(["--veaero", "abc"], "USAGE"));
  assert.equal(result, null);
});

test("resolveBudget rejects zero and negative --veaero amounts", async () => {
  assert.equal((await captureStderr(() => resolveBudget(["--veaero", "0"], "USAGE"))).result, null);
  assert.equal((await captureStderr(() => resolveBudget(["--veaero", "-100"], "USAGE"))).result, null);
});

test("resolveBudget accepts a valid --veaero amount and logs nothing", async () => {
  const { result, logged } = await captureStderr(() => resolveBudget(["--veaero", "25000"], "USAGE"));
  assert.deepEqual(result, { veaero: 25000, positions: [] });
  assert.deepEqual(logged, []);
});

/**
 * Runs the CLI as a real child process. Exit codes are the one part of this
 * program a caller can only observe from outside, and they are what a script
 * wrapping the tool actually branches on — so this spawns rather than importing.
 * Only argument-handling paths are exercised here; none of them touch the chain.
 */
function runCli(args: string[]): Promise<{ code: number; stdout: string; stderr: string }> {
  return new Promise((resolvePromise) => {
    const child = spawn(
      process.execPath,
      ["--import", "tsx", fileURLToPath(new URL("../src/cli.ts", import.meta.url)), ...args],
      { stdio: ["ignore", "pipe", "pipe"] },
    );
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (d) => (stdout += d));
    child.stderr.on("data", (d) => (stderr += d));
    child.on("close", (code) => resolvePromise({ code: code ?? 0, stdout, stderr }));
  });
}

test("the CLI exits 0 and prints usage when asked for help", async () => {
  for (const args of [[], ["--help"], ["-h"], ["help"]]) {
    const { code, stdout } = await runCli(args);
    assert.equal(code, 0, `\`${args.join(" ")}\` should succeed`);
    assert.match(stdout, /Commands:/);
    // --vote-basis is a real, tested recommend flag (see parseVoteBasisFlag
    // tests below) — the top-level help text previously omitted it entirely,
    // leaving it undiscoverable short of reading the README or the source.
    assert.match(stdout, /--vote-basis/);
  }
});

test("the CLI exits non-zero on an unknown command", async () => {
  // Printing usage and reporting success meant a typo in a script — `poolz` for
  // `pools` — was indistinguishable from a completed run.
  const { code, stderr } = await runCli(["poolz"]);
  assert.equal(code, 1);
  assert.match(stderr, /Unknown command: poolz/);
  // Usage still goes out, just on stderr where a failure's output belongs.
  assert.match(stderr, /Commands:/);
});

test("epochDeadlineLine states the deadline in both remaining time and UTC", () => {
  // Saturday 2026-08-22 12:00 UTC — four days and twelve hours before the flip.
  const line = epochDeadlineLine(new Date(Date.UTC(2026, 7, 22, 12, 0, 0)));

  assert.match(line, /closes in 4d 12h/);
  assert.match(line, /2026-08-27 00:00 UTC/);
  assert.match(line, /counts toward the next epoch/);
});

test("epochDeadlineLine does not report a negative countdown at the boundary", () => {
  // The instant of the flip belongs to the epoch opening there, so a full week
  // remains rather than zero or a negative figure.
  const line = epochDeadlineLine(new Date(Date.UTC(2026, 7, 27, 0, 0, 0)));
  assert.match(line, /closes in 7d 0h/);
});

test("parseVoteBasisFlag accepts every basis and rejects anything else", () => {
  assert.equal(parseVoteBasisFlag([]), "previous");
  assert.equal(parseVoteBasisFlag(["--vote-basis", "previous"]), "previous");
  assert.equal(parseVoteBasisFlag(["--vote-basis", "current"]), "current");
  assert.equal(parseVoteBasisFlag(["--vote-basis", "typical"]), "typical");
  // A typo must print usage rather than quietly allocating on a different basis.
  assert.equal(parseVoteBasisFlag(["--vote-basis", "Current"]), undefined);
  assert.equal(parseVoteBasisFlag(["--vote-basis", "median"]), undefined);
  assert.equal(parseVoteBasisFlag(["--vote-basis"]), undefined);
});

/**
 * A wallet with several locks is the case worth testing: `Voter.vote` casts
 * from exactly one veNFT, and locks differ in size and expiry, so there is no
 * default the tool is entitled to pick on someone's behalf.
 */
const LOCK = (id: string, votingPowerVeAero: number): VeNftSummary => ({
  id,
  votingPowerVeAero,
  expiresAt: 0,
  isPermanent: true,
});

test("chooseVoteTokenId takes --nft whenever it is given", () => {
  assert.deepEqual(chooseVoteTokenId("17324", []), { tokenId: "17324" });
  // Even when the wallet's locks would have answered on their own.
  assert.deepEqual(chooseVoteTokenId("6", [LOCK("17324", 100)]), { tokenId: "6" });
});

test("chooseVoteTokenId rejects an --nft that is not a positive whole id", () => {
  for (const bad of ["0", "-4", "17e3", "abc", "", "1.5"]) {
    const chosen = chooseVoteTokenId(bad, []);
    assert.ok("error" in chosen, `expected "${bad}" to be rejected`);
    assert.match(chosen.error, /positive whole veNFT id/);
  }
});

test("chooseVoteTokenId uses a single lock without asking", () => {
  assert.deepEqual(chooseVoteTokenId(undefined, [LOCK("17324", 107_871)]), { tokenId: "17324" });
});

test("chooseVoteTokenId refuses to pick between several locks, and names them", () => {
  const chosen = chooseVoteTokenId(undefined, [LOCK("6", 11_362_738), LOCK("17324", 107_871)]);

  assert.ok("error" in chosen);
  assert.match(chosen.error, /holds 2 locks/);
  assert.match(chosen.error, /#6/);
  assert.match(chosen.error, /#17324/);
  assert.match(chosen.error, /--nft/);
});

test("chooseVoteTokenId asks for one when there is nothing to read", () => {
  const chosen = chooseVoteTokenId(undefined, []);

  assert.ok("error" in chosen);
  assert.match(chosen.error, /--nft <id>/);
});

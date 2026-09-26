#!/usr/bin/env node
import { rankPoolsByEfficiency, type PoolEfficiency } from "./efficiency.js";
import {
  recommendAllocation,
  toWholePercentWeights,
  expectedUsdForWholePercentVote,
  unallocatedVeAero,
  voteBasisCaveat,
  type VoteBasis,
} from "./allocator.js";
import { backtestLive } from "./backtest.js";
import { buildVoteCalldata } from "./calldata.js";
import { fetchVeAeroPositions, type VeNftSummary } from "./veAero.js";
import { fetchVotesFor, fetchLastVoted, fetchPoolSymbols, scoreVotes } from "./voted.js";
import { fetchPoolEpochs, withoutMigrating, type EpochData } from "./pools.js";
import { getTokenPrices } from "./prices.js";
import { mapWithConcurrency } from "./util.js";
import { periodStartOf, WEEKLY_EPOCH } from "./trend.js";
import { BACKTEST_EPOCHS, DEFAULT_MIN_CONSISTENCY, MAX_BACKTEST_EPOCHS } from "./constants.js";
import { formatError, isValidAddress, padCol, wrapText } from "./util.js";
import { computeTrend, epochEndOf, formatDuration, isEpochInProgress } from "./trend.js";

function fmtUsd(n: number): string {
  return `$${n.toLocaleString("en-US", { maximumFractionDigits: 2 })}`;
}

// Per-vote values are often fractions of a cent (a pool's weekly incentives
// split across millions of votes) — fmtUsd alone would just print "$0" for those.
function fmtUsdPerVote(n: number): string {
  if (n === 0) return "$0";
  if (n < 0.01) return `$${n.toFixed(6)}`;
  return fmtUsd(n);
}

function getFlag(args: string[], name: string): string | undefined {
  const i = args.indexOf(`--${name}`);
  return i === -1 ? undefined : args[i + 1];
}

function hasFlag(args: string[], name: string): boolean {
  return args.includes(`--${name}`);
}

/**
 * Shapes a ranked pool for --json output. Kept in parity with the MCP
 * `list_pool_efficiency` tool's response shape, including `epochsObserved` —
 * without it, a --json consumer can't tell a prediction backed by 6 trailing
 * epochs from one backed by a single epoch of a brand-new pool.
 *
 * `momentum` is derived here rather than stored on `PoolEfficiency`, the same
 * way `snapshot.ts`'s `toSnapshotPool` derives it for the web app — it needs
 * to know whether the latest epoch is still in progress, which depends on
 * *when* the caller is asking, not on anything the ranking itself computed.
 * `asOfUnixSeconds` is a parameter (not read from the clock inside) so this
 * stays pure and testable.
 */
export function poolEfficiencyToJson(p: PoolEfficiency, asOfUnixSeconds: number) {
  const currentEpochPartial = isEpochInProgress(p.latestEpochTs, asOfUnixSeconds);
  const { momentum } = computeTrend(p.epochUsdSeries, currentEpochPartial);
  return {
    symbol: p.pool.symbol,
    pool: p.pool.address,
    votesVeAero: p.currentVotesVeAero,
    currentValuePerVote: p.currentValuePerVote,
    predictedValuePerVote: p.predictedValuePerVote,
    predictiveEdge: p.predictiveEdge,
    epochsObserved: p.epochsObserved,
    volatility: p.volatility,
    consistency: p.consistency,
    momentum,
    migrating: !!p.pool.migrating,
  };
}

/**
 * Shapes an account's veAERO positions for --json output, matching the MCP
 * `get_my_veaero` tool's response shape (`{ address, totalVeAero, locks }`).
 */
export function veAeroPositionsToJson(address: string, positions: VeNftSummary[]) {
  const totalVeAero = positions.reduce((a, b) => a + b.votingPowerVeAero, 0);
  return { address, totalVeAero, locks: positions };
}

/**
 * Parses a `--name` flag as a positive integer, falling back to `fallback` if
 * the flag is absent. Returns undefined (rather than NaN or a silently-clamped
 * value) if the flag was given but isn't a positive integer, so callers can
 * print a clear usage error instead of e.g. `Array.slice` quietly treating a
 * garbled `--top abc` as 0 or a negative `--top` as "drop the last N rows".
 *
 * A dangling flag with no value (e.g. `--top` as the last argument) must hit
 * this same error path rather than the fallback: `getFlag` returns undefined
 * for both "flag absent" and "flag present but out of args", so `hasFlag` is
 * checked separately to tell the two apart.
 *
 * `max`, when given, rejects a value above it the same way — callers whose
 * flag drives an on-chain fetch (e.g. `--epochs`) can bound it so a mistyped
 * value can't balloon into a much larger live scan than intended.
 */
export function parsePositiveIntFlag(args: string[], name: string, fallback: number, max?: number): number | undefined {
  const raw = getFlag(args, name);
  if (raw === undefined) return hasFlag(args, name) ? undefined : fallback;
  const n = Number(raw);
  if (!Number.isInteger(n) || n <= 0) return undefined;
  return max !== undefined && n > max ? undefined : n;
}

/**
 * Parses a `--name` flag as a 0..1 fraction (used by `--min-consistency`),
 * following the same "undefined means the caller should print usage" contract
 * as `parsePositiveIntFlag`. 0 and 1 are both accepted: 0 is a meaningful
 * "don't filter at all" and 1 means "only perfectly steady pools".
 */
export function parseUnitIntervalFlag(args: string[], name: string, fallback: number): number | undefined {
  const raw = getFlag(args, name);
  if (raw === undefined) return hasFlag(args, name) ? undefined : fallback;
  const n = Number(raw);
  return Number.isFinite(n) && n >= 0 && n <= 1 ? n : undefined;
}

/**
 * Parses `--vote-basis`, which decides whether a pool is judged against the
 * weight it carries right now or the weight it usually settles at. Follows the
 * same "undefined means print usage" contract as the flags above, so a typo
 * prints help rather than silently falling back to a different strategy than
 * the one asked for.
 */
export function parseVoteBasisFlag(args: string[], fallback: VoteBasis = "previous"): VoteBasis | undefined {
  const raw = getFlag(args, "vote-basis");
  if (raw === undefined) return hasFlag(args, "vote-basis") ? undefined : fallback;
  return raw === "previous" || raw === "current" || raw === "typical" ? raw : undefined;
}

async function cmdPools(args: string[]) {
  const top = parsePositiveIntFlag(args, "top", 20);
  const minConsistency = parseUnitIntervalFlag(args, "min-consistency", 0);
  if (top === undefined || minConsistency === undefined) {
    console.error("Usage: aero-vote-radar pools [--top N] [--min-consistency 0..1] [--json] (N must be a positive integer, min-consistency a number from 0 to 1)");
    process.exitCode = 1;
    return;
  }
  const ranked = await rankPoolsByEfficiency();
  const eligible = ranked.filter((p) => p.consistency >= minConsistency);
  const topRanked = eligible.slice(0, top);

  if (hasFlag(args, "json")) {
    const asOfUnixSeconds = Math.floor(Date.now() / 1000);
    console.log(JSON.stringify(topRanked.map((p) => poolEfficiencyToJson(p, asOfUnixSeconds)), null, 2));
    return;
  }

  const filterNote =
    minConsistency > 0 ? ` (${eligible.length} of ${ranked.length} pass consistency >= ${minConsistency})` : "";
  console.log(`\nTop ${top} Aerodrome pools by predicted $/veAERO vote (of ${ranked.length} live-gauge pools with votes)${filterNote}:\n`);
  console.log(
    ["Symbol", "Votes(veAERO)", "Latest $/vote", "Predicted $/vote", "Edge", "Consistency"]
      .map((h) => h.padEnd(18))
      .join(""),
  );
  for (const p of topRanked) {
    console.log(
      [
        padCol(p.pool.migrating ? `${p.pool.symbol} (migrating)` : p.pool.symbol, 18),
        p.currentVotesVeAero.toLocaleString("en-US", { maximumFractionDigits: 0 }).padEnd(18),
        fmtUsdPerVote(p.currentValuePerVote).padEnd(18),
        fmtUsdPerVote(p.predictedValuePerVote).padEnd(18),
        `${(p.predictiveEdge * 100).toFixed(1)}%`.padEnd(18),
        p.consistency.toFixed(2),
      ].join(""),
    );
  }
  console.log("\nConsistency: 1.00 = identical payout every epoch, lower = spikier. A high predicted $/vote");
  console.log("backed by low consistency is usually one big one-off bribe, not a repeatable opportunity.\n");
}

const RECOMMEND_USAGE =
  "Usage: aero-vote-radar recommend (--veaero <amount> | --address <0x...>) [--top K] [--min-consistency 0..1] [--max-weight 0..1] [--vote-basis previous|current|typical] [--vote-ready] [--calldata [--nft <id>]] [--json]";

const BACKTEST_USAGE = `Usage: aero-vote-radar backtest (--veaero <amount> | --address <0x...>) [--epochs N] [--min-consistency 0..1] [--json] (N must be a positive integer, max ${MAX_BACKTEST_EPOCHS}; min-consistency a number from 0 to 1)`;

export interface ResolvedBudget {
  veaero: number;
  /**
   * The wallet's locks, when the budget came from `--address` — empty for a
   * plain `--veaero` amount. Returned alongside the budget (rather than just
   * the total) so a caller that also needs to pick a veNFT to vote from, like
   * `--calldata`, can reuse this fetch instead of hitting `fetchVeAeroPositions`
   * a second time for the same address.
   */
  positions: VeNftSummary[];
}

/**
 * Resolves the veAERO budget from either an explicit `--veaero` amount or, with
 * `--address`, the wallet's actual on-chain voting power — so the common case
 * stops being "go look up your own balance first, then retype it here". Shared
 * by `recommend` and `backtest`, which take a `usage` string each so a bad
 * `--veaero`/`--address` shows the calling command's own usage (flags, etc.)
 * rather than always printing `recommend`'s.
 * Returns null after printing its own error, so the caller just bails.
 */
export async function resolveBudget(args: string[], usage: string): Promise<ResolvedBudget | null> {
  const rawVeaero = getFlag(args, "veaero");
  const address = getFlag(args, "address");

  if (rawVeaero !== undefined && address !== undefined) {
    console.error(`${usage}\nPass either --veaero or --address, not both.`);
    return null;
  }

  if (address !== undefined) {
    if (!isValidAddress(address)) {
      console.error(`${usage}\n--address must be a 0x-prefixed 40-character hex address.`);
      return null;
    }
    const positions = await fetchVeAeroPositions(address);
    const total = positions.reduce((a, b) => a + b.votingPowerVeAero, 0);
    if (total <= 0) {
      console.error(`No veAERO voting power found for ${address} — nothing to allocate.`);
      return null;
    }
    // stderr, not stdout: this status line runs before cmdRecommend/cmdBacktest
    // get a chance to check --json, so putting it on stdout would prepend
    // human-readable text to what's supposed to be a clean JSON payload for
    // `recommend --address ... --json` / `backtest --address ... --json`.
    console.error(`\nUsing ${total.toLocaleString("en-US", { maximumFractionDigits: 3 })} veAERO of live voting power from ${address} (${positions.length} lock(s)).`);
    return { veaero: total, positions };
  }

  const veaero = Number(rawVeaero);
  if (rawVeaero === undefined || !Number.isFinite(veaero) || veaero <= 0) {
    console.error(`${usage}\nAmount must be a finite positive number.`);
    return null;
  }
  return { veaero, positions: [] };
}

/**
 * Which veNFT a vote should be cast from, given what the user asked for and
 * what they actually hold.
 *
 * Kept pure and separate from the fetch so the awkward part — a wallet with
 * several locks — is testable without a chain. There is no sensible default
 * there: locks differ in size and expiry, `Voter.vote` casts from exactly one,
 * and picking "the biggest" on the user's behalf would be this tool choosing
 * which of someone's positions to commit for a week. Returns an error string
 * rather than throwing, since every caller here prints and bails.
 */
export function chooseVoteTokenId(
  nftFlag: string | undefined,
  positions: VeNftSummary[],
): { tokenId: string } | { error: string } {
  if (nftFlag !== undefined) {
    if (!/^[0-9]+$/.test(nftFlag) || BigInt(nftFlag) <= 0n) {
      return { error: `--nft must be a positive whole veNFT id, got "${nftFlag}".` };
    }
    return { tokenId: nftFlag };
  }

  if (positions.length === 1) return { tokenId: positions[0].id };

  if (positions.length === 0) {
    return { error: "--calldata needs a veNFT to vote from: pass --nft <id>, or --address to read your locks." };
  }

  const ids = positions.map((p) => `#${p.id} (${p.votingPowerVeAero.toLocaleString("en-US", { maximumFractionDigits: 0 })} veAERO)`);
  return {
    error: `That wallet holds ${positions.length} locks — a vote is cast from one of them. Pick with --nft <id>: ${ids.join(", ")}.`,
  };
}

/**
 * One line saying how long this recommendation stays actionable.
 *
 * A vote only counts toward the epoch it is cast in, so a ranking is advice
 * with a deadline attached — and the deadline was previously stated nowhere.
 * Exported for testing, and takes its clock as an argument so the test can pin
 * one instead of racing the real one.
 */
export function epochDeadlineLine(now: Date = new Date()): string {
  const nowSec = Math.floor(now.getTime() / 1000);
  const endsAt = epochEndOf(nowSec);
  const stamp = `${new Date(endsAt * 1000).toISOString().slice(0, 16).replace("T", " ")} UTC`;
  return `Voting for this epoch closes in ${formatDuration(endsAt - nowSec)} (${stamp}) — a vote cast after that counts toward the next epoch.`;
}

/**
 * Prints the vote-basis caveat, if this budget has one, together with the
 * command that settles it for this particular voter rather than in general.
 *
 * The caveat itself is deliberately not a recommendation — see
 * `voteBasisCaveat` — so what is added here is the way to check, not a nudge:
 * `backtest` prints both bases side by side on the epochs available today, and
 * that is a number about the reader's own size rather than about the size the
 * constant was measured at.
 */
function printVoteBasisCaveat(veAeroBudget: number, voteBasis: VoteBasis): void {
  const caveat = voteBasisCaveat(veAeroBudget, voteBasis);
  if (caveat === null) return;

  const amount = Math.round(veAeroBudget).toString();
  console.log(`\n${wrapText(caveat, 92)}`);
  console.log(
    wrapText(
      `Check it at your own size: backtest --veaero ${amount} replays past epochs under both, and npm run predict-check scores their accuracy.`,
      92,
    ),
  );
}

/**
 * Prints the vote as an unsigned transaction, and says plainly what it is.
 *
 * The tone here is deliberate. Everywhere else this tool prints advice; this is
 * the one output someone will paste into a wallet, so it names the contract it
 * targets, restates the weights beside the blob that encodes them, and says who
 * signs — which is never this program.
 *
 * `positions` comes from `resolveBudget`, already fetched for `--address` (or
 * empty for a plain `--veaero` amount) — refetching it here would mean a
 * second live `fetchVeAeroPositions` call for the exact same address on every
 * `recommend --address ... --calldata` run.
 */
function printVoteCalldata(
  args: string[],
  positions: VeNftSummary[],
  votePercents: ReturnType<typeof toWholePercentWeights>,
  expectedUsd: number,
  veAeroBudget: number,
  voteBasis: VoteBasis,
): void {
  const chosen = chooseVoteTokenId(getFlag(args, "nft"), positions);
  if ("error" in chosen) {
    console.error(chosen.error);
    process.exitCode = 1;
    return;
  }

  let tx;
  try {
    tx = buildVoteCalldata(chosen.tokenId, votePercents);
  } catch (err) {
    console.error(formatError(err));
    process.exitCode = 1;
    return;
  }

  if (hasFlag(args, "json")) {
    console.log(JSON.stringify(tx, null, 2));
    return;
  }

  console.log(`\nUnsigned vote from veNFT #${tx.tokenId} — ${tx.functionSignature} on Base (chain ${tx.chainId}):\n`);
  for (let i = 0; i < tx.pools.length; i++) {
    console.log(`  ${tx.weights[i].toString().padStart(3)}%  ${votePercents[i].symbol}  ${tx.pools[i]}`);
  }
  console.log(`\n  to:    ${tx.to}   (Voter)`);
  console.log(`  value: ${tx.value}`);
  console.log(`  data:  ${tx.data}`);
  console.log(`\nExpected next epoch: ${fmtUsd(expectedUsd)}.`);
  console.log(epochDeadlineLine());
  // The same caveat the other two output modes carry: encoding a vote does not
  // make the basis it was priced on any better supported.
  printVoteBasisCaveat(veAeroBudget, voteBasis);
  console.log();
  console.log(
    wrapText(
      "Nothing here is signed or sent. Paste it into your own wallet, check that `to` is the Voter address above and that the pools and weights match the rows, and sign it yourself — only the owner of that veNFT can.",
      92,
    ),
  );
  console.log();
}

async function cmdRecommend(args: string[]) {
  const topK = parsePositiveIntFlag(args, "top", 15);
  const minConsistency = parseUnitIntervalFlag(args, "min-consistency", DEFAULT_MIN_CONSISTENCY);
  const maxWeight = parseUnitIntervalFlag(args, "max-weight", 1);
  const voteBasis = parseVoteBasisFlag(args);
  if (topK === undefined || minConsistency === undefined || maxWeight === undefined || maxWeight === 0 || voteBasis === undefined) {
    console.error(
      `${RECOMMEND_USAGE}\nK must be a positive integer; min-consistency a number from 0 to 1; max-weight a number above 0 and up to 1; vote-basis one of "previous", "current" or "typical".`,
    );
    process.exitCode = 1;
    return;
  }

  const resolved = await resolveBudget(args, RECOMMEND_USAGE);
  if (resolved === null) {
    process.exitCode = 1;
    return;
  }
  const { veaero, positions } = resolved;

  // Pools Aerodrome is migrating still rank in `pools`, but are never recommended:
  // its vote page hides them by default and their liquidity is being told to leave.
  const allRanked = await rankPoolsByEfficiency();
  const ranked = withoutMigrating(allRanked).filter((p) => p.consistency >= minConsistency);
  const migratingLeftOut = allRanked.length - withoutMigrating(allRanked).length;
  if (migratingLeftOut > 0) {
    console.error(`(left out ${migratingLeftOut} pool(s) Aerodrome is migrating to new gauges; they are hidden from its default vote list)`);
  }
  const spikyLeftOut = withoutMigrating(allRanked).length - ranked.length;
  if (spikyLeftOut > 0) {
    console.error(`(left out ${spikyLeftOut} pool(s) with consistency below ${minConsistency}; pass --min-consistency 0 to include them)`);
  }
  const allocation = recommendAllocation(ranked, veaero, topK, undefined, maxWeight, voteBasis);

  // A cap too tight for the candidate set leaves part of the budget unplaced,
  // and every downstream figure would then describe a vote that spends less
  // than the user has. Refusing here is the only honest option: printing the
  // rows anyway means toWholePercentWeights scales them back to 100% and hands
  // back exactly the concentration --max-weight was asked to prevent.
  //
  // Skipped when nothing qualified at all: unallocatedVeAero(allocation=[], ...)
  // returns the *whole* budget (nothing was spent), which would otherwise always
  // read as "unplaced > 0" and blame --max-weight even when it's untouched at its
  // uncapped default of 1 — the real cause (zero candidate pools) is reported by
  // the allocation.length === 0 branch below instead.
  const unplaced = allocation.length > 0 ? unallocatedVeAero(allocation, veaero) : 0;
  if (unplaced > 0) {
    const pct = Math.round((unplaced / veaero) * 100);
    console.error(
      `--max-weight ${maxWeight} is too tight for the ${allocation.length} pool(s) that qualified: ${pct}% of your veAERO has nowhere to go. Raise --max-weight, raise --top, or lower --min-consistency.`,
    );
    process.exitCode = 1;
    return;
  }
  const totalExpectedUsd = allocation.reduce((a, b) => a + b.expectedUsd, 0);
  const votePercents = toWholePercentWeights(allocation);
  // What the rounded, actually-castable vote is worth. Not the sum above — see
  // `expectedUsdForWholePercentVote` for why the two differ in both directions.
  const votePercentsExpectedUsd = expectedUsdForWholePercentVote(allocation, veaero);

  if (hasFlag(args, "json")) {
    console.log(
      JSON.stringify(
        {
          veAeroBudget: veaero,
          maxWeight,
          voteBasis,
          voteBasisCaveat: voteBasisCaveat(veaero, voteBasis),
          allocation,
          votePercents,
          totalExpectedUsd,
          votePercentsExpectedUsd,
        },
        null,
        2,
      ),
    );
    return;
  }

  if (allocation.length === 0) {
    // Without this, --vote-ready would print "whole percentages, summing to
    // exactly 100" followed by zero rows and $0 — actively misleading rather
    // than just empty. Mirrors the "not enough epoch history" guard in
    // cmdBacktest for the same underlying situation: nothing qualified.
    const reason =
      minConsistency > 0
        ? `No live-gauge pool passes --min-consistency ${minConsistency} right now — try a lower value.`
        : "No live-gauge pool with a big enough trailing average is available to allocate to right now.";
    console.log(`\n${reason}\n`);
    return;
  }

  if (hasFlag(args, "calldata")) {
    printVoteCalldata(args, positions, votePercents, votePercentsExpectedUsd, veaero, voteBasis);
    return;
  }

  if (hasFlag(args, "vote-ready")) {
    console.log(`\nVote-ready weights for ${veaero.toLocaleString("en-US", { maximumFractionDigits: 0 })} veAERO — whole percentages, summing to exactly 100:\n`);
    for (const v of votePercents) {
      console.log(`  ${v.percent.toString().padStart(3)}%  ${v.symbol}`);
    }
    const dropped = allocation.length - votePercents.length;
    console.log(`\nEnter these directly on aerodrome.finance. Expected next epoch: ${fmtUsd(votePercentsExpectedUsd)}.`);
    if (dropped > 0) {
      console.log(
        `(${dropped} pool${dropped > 1 ? "s" : ""} received a share too small to round up to 1%; those points went to the rows above.)`,
      );
    }
    console.log(epochDeadlineLine());
    printVoteBasisCaveat(veaero, voteBasis);
    console.log("\nThis tool never touches your wallet or keys.\n");
    return;
  }

  const capNote = maxWeight < 1 ? `, no pool above ${Math.round(maxWeight * 100)}%` : "";
  console.log(`\nRecommended allocation for ${veaero.toLocaleString("en-US", { maximumFractionDigits: 0 })} veAERO (top ${topK} candidates considered${capNote}):\n`);
  console.log(["Symbol", "Weight", "veAERO", "Expected $/epoch"].map((h) => h.padEnd(18)).join(""));
  for (const a of allocation) {
    console.log(
      [
        padCol(a.symbol, 18),
        `${(a.weight * 100).toFixed(1)}%`.padEnd(18),
        a.veAeroAllocated.toLocaleString("en-US", { maximumFractionDigits: 0 }).padEnd(18),
        fmtUsd(a.expectedUsd),
      ].join(""),
    );
  }
  console.log(`\nTotal expected value next epoch (heuristic: trailing average capped at the last completed epoch): ${fmtUsd(totalExpectedUsd)}`);
  console.log(epochDeadlineLine());
  printVoteBasisCaveat(veaero, voteBasis);
  console.log("\nPass --vote-ready for whole percentages you can type straight into Aerodrome's voting UI.");
  console.log("You vote this yourself on aerodrome.finance — this tool never touches your wallet or keys.\n");
}

async function cmdBacktest(args: string[]) {
  const epochs = parsePositiveIntFlag(args, "epochs", BACKTEST_EPOCHS, MAX_BACKTEST_EPOCHS);
  const minConsistency = parseUnitIntervalFlag(args, "min-consistency", DEFAULT_MIN_CONSISTENCY);
  if (epochs === undefined || minConsistency === undefined) {
    console.error(BACKTEST_USAGE);
    process.exitCode = 1;
    return;
  }

  const resolved = await resolveBudget(args, BACKTEST_USAGE);
  if (resolved === null) {
    process.exitCode = 1;
    return;
  }
  const { veaero } = resolved;

  const report = await backtestLive(veaero, epochs, undefined, minConsistency);

  if (hasFlag(args, "json")) {
    console.log(JSON.stringify(report, null, 2));
    return;
  }

  if (report.epochsTested === 0) {
    // Same distinction `recommend` draws: "there is no history" and "your filter
    // rejected all of it" call for different next moves, and one message for
    // both sends you looking for a data problem that isn't there.
    console.log(
      minConsistency > 0
        ? `\nNo epoch had a candidate pool passing --min-consistency ${minConsistency} — try a lower value.\n`
        : "\nNot enough epoch history to backtest — no epoch had a qualifying candidate pool.\n",
    );
    return;
  }

  const filterNote = minConsistency > 0 ? ` (only pools with consistency ≥ ${minConsistency})` : "";
  console.log(`\nBacktest over the last ${report.epochsTested} epoch(s) with ${veaero.toLocaleString("en-US", { maximumFractionDigits: 0 })} veAERO${filterNote}:\n`);
  console.log(
    ["EpochsAgo", "Radar $ (typical)", "Radar $ (current)", "Naive $", "Naive picked"]
      .map((h) => h.padEnd(20))
      .join(""),
  );
  for (const e of report.epochs) {
    console.log(
      [
        String(e.epochsAgo).padEnd(20),
        fmtUsd(e.radarTypicalUsd).padEnd(20),
        fmtUsd(e.radarUsd).padEnd(20),
        fmtUsd(e.naiveUsd).padEnd(20),
        e.naiveSymbol ?? "-",
      ].join(""),
    );
  }

  const uplift = report.upliftPct === null ? "n/a (baseline earned $0)" : `${(report.upliftPct * 100).toFixed(1)}%`;
  console.log(`\nTotal: radar ${fmtUsd(report.radarTotalUsd)} vs naive ${fmtUsd(report.naiveTotalUsd)} — uplift ${uplift}`);
  console.log(`Radar earned more in ${report.epochsWonByRadar} of ${report.epochsTested} epoch(s).`);

  // What the default vote basis is worth, which is the only reason it is the
  // default. Printed as its own line rather than folded into the uplift above,
  // because it answers a different question: not "does the radar beat naive
  // APR-chasing" but "does judging pools on the weight they settle at beat
  // judging them on the weight they are showing".
  const basisDelta =
    report.typicalVsCurrentPct === null
      ? "n/a (the current-weight basis earned $0)"
      : `${report.typicalVsCurrentPct >= 0 ? "+" : ""}${(report.typicalVsCurrentPct * 100).toFixed(1)}%`;
  console.log(
    `Vote basis: typical ${fmtUsd(report.radarTypicalTotalUsd)} vs current ${fmtUsd(report.radarTotalUsd)} — ${basisDelta}, ahead in ${report.epochsWonByTypical} of ${report.epochsTested} epoch(s).`,
  );

  if (minConsistency > 0) {
    // Worth stating plainly: a filter that leaves two pools to choose between
    // has changed the strategy far more than the uplift figure alone suggests.
    const excluded = report.epochs.reduce((a, e) => a + e.candidatesExcludedByConsistency, 0);
    const kept = report.epochs.reduce((a, e) => a + e.candidatesConsidered, 0);
    console.log(
      `The filter dropped ${excluded} pool-epoch(s) and left ${kept} to allocate across. The naive baseline is deliberately left unfiltered, so this uplift is comparable with an unfiltered run.`,
    );
  }
  console.log("\nEpochsAgo 0 is the most recently completed epoch. 'Naive' = put everything in the pool with the");
  console.log("highest $/vote at the time. Decisions use only data available before each epoch resolved, but this");
  console.log("assumes your votes wouldn't have moved anyone else's, and only sees pools whose gauge is still alive.\n");
}

export type ReviewTarget = { kind: "nft"; tokenIds: bigint[] } | { kind: "address"; address: string };

/**
 * Validates `review`'s `--address`/`--nft` flags, including rejecting both at
 * once — the same rule `resolveBudget` already enforces for
 * `--veaero`/`--address`, which this command had silently skipped: passing
 * both here let `--nft` win with no word to the user that `--address` was
 * ignored. Split out from `cmdReview` so the validation is testable without a
 * chain, the way the rest of this file's flag parsers are. Only the `--nft`
 * branch is immediately usable; `--address` still needs
 * `fetchVeAeroPositions` to turn into token ids, which stays in `cmdReview`
 * alongside its other live RPC calls. Returns null after printing its own
 * error, so the caller just bails.
 */
export function resolveReviewTarget(args: string[]): ReviewTarget | null {
  const address = getFlag(args, "address");
  const nftFlag = getFlag(args, "nft");
  const usage = "Usage: aero-vote-radar review (--address 0x... | --nft <id>) [--json]";

  if (!address && !nftFlag) {
    console.error(usage);
    return null;
  }
  if (address !== undefined && nftFlag !== undefined) {
    console.error(`${usage}\nPass either --address or --nft, not both.`);
    return null;
  }
  if (nftFlag !== undefined) {
    if (!/^[0-9]+$/.test(nftFlag)) {
      console.error("--nft must be a whole veNFT id.");
      return null;
    }
    return { kind: "nft", tokenIds: [BigInt(nftFlag)] };
  }

  if (!isValidAddress(address as string)) {
    console.error("--address must be a 0x-prefixed 40-character hex address.");
    return null;
  }
  return { kind: "address", address: address as string };
}

/**
 * `review` — scores the vote already cast, for the epoch that has most recently
 * closed.
 *
 * The rest of this CLI asks a holder to trust a forecast before they have any
 * reason to. This asks for nothing: the epoch is settled, the weights are final,
 * and every figure can be checked against their own wallet. It is the first
 * thing a stranger can run that proves the tool is reading the right chain.
 *
 * Only pools the holder actually voted for are fetched, not the whole protocol,
 * so it is a handful of calls rather than a full scan.
 */
async function cmdReview(args: string[]) {
  const target = resolveReviewTarget(args);
  if (!target) {
    process.exitCode = 1;
    return;
  }

  let tokenIds: bigint[];
  if (target.kind === "nft") {
    tokenIds = target.tokenIds;
  } else {
    const positions = await fetchVeAeroPositions(target.address);
    if (positions.length === 0) {
      console.log(`No veAERO locks found for ${target.address}.`);
      return;
    }
    tokenIds = positions.map((p) => BigInt(p.id));
  }

  // The most recently *closed* epoch. The one in progress has no settled weight
  // to divide by, so scoring it would be a forecast wearing a receipt's clothes.
  const now = Math.floor(Date.now() / 1000);
  const epochTs = periodStartOf(now, WEEKLY_EPOCH) - WEEKLY_EPOCH.lengthSeconds;

  const votes = (await Promise.all(tokenIds.map((id) => fetchVotesFor(id)))).flat();
  if (votes.length === 0) {
    console.log("\nThis lock has no vote recorded on any pool. Nothing to score yet.\n");
    return;
  }
  const lastVoted = Math.max(...(await Promise.all(tokenIds.map((id) => fetchLastVoted(id)))));

  // Only the pools this lock voted for — read directly, never through the
  // active-pool list. That list keeps live gauges only, and a holder can
  // perfectly well have voted for a pool whose gauge has since been killed
  // (measured on a real lock, that is exactly what happened). Going direct also
  // skips a ~1,800-pool scan this command has no use for, which is the
  // difference between a report that takes seconds and one that takes minutes.
  const pools = [...new Set(votes.map((v) => v.pool))];
  const symbols = await fetchPoolSymbols(pools);
  const epochsByPool = new Map<string, { symbol: string; epochs: EpochData[] }>();
  const fetched = await mapWithConcurrency(pools, 8, (p) => fetchPoolEpochs(p, 4).catch(() => [] as EpochData[]));
  pools.forEach((p, i) => epochsByPool.set(p, { symbol: symbols.get(p) ?? p, epochs: fetched[i] }));

  const tokens = [...new Set(fetched.flat().flatMap((e) => [...e.bribes.map((b) => b.token), ...e.fees.map((f) => f.token)]))];
  const prices = await getTokenPrices(tokens);

  const review = scoreVotes(votes, epochTs, epochsByPool, prices);

  if (hasFlag(args, "json")) {
    console.log(JSON.stringify({ ...review, lastVoted, tokenIds: tokenIds.map(String) }, null, 2));
    return;
  }

  const day = new Date(epochTs * 1000).toISOString().slice(0, 10);
  console.log(`
Your vote for the epoch of ${day}, scored against what it settled at:
`);
  if (review.rows.length === 0) {
    console.log("  None of the pools voted for have a settled record for that epoch.\n");
    return;
  }

  const COLS = [24, 8, 14, 14, 14, 12];
  const row = (cells: string[]) => cells.map((c, i) => padCol(c, COLS[i])).join("");
  console.log(row(["Pool", "Your %", "Your veAERO", "Pool total", "Pool paid", "You earned"]));
  for (const r of review.rows) {
    console.log(
      row([
        r.symbol,
        `${Math.round(r.share * 100)}%`,
        r.myVotes.toLocaleString("en-US", { maximumFractionDigits: 2 }),
        r.poolVotes.toLocaleString("en-US", { maximumFractionDigits: 0 }),
        fmtUsd(r.poolUsd),
        // A small lock's share of a pool is routinely fractions of a cent, and
        // fmtUsd rounds those to "$0" — which reads as "this pool paid you
        // nothing" rather than "your share was small". The whole point of the
        // command is that the holder can check the figure, so it has to survive
        // being printed.
        fmtUsdPerVote(r.earnedUsd),
      ]),
    );
  }

  console.log(
    `\nTotal earned: ${fmtUsdPerVote(review.earnedUsd)} on ${review.budget.toLocaleString("en-US", { maximumFractionDigits: 2 })} veAERO.`,
  );
  if (review.budget > 0) {
    console.log(`That is ${fmtUsdPerVote(review.earnedUsd / review.budget)} per veAERO.`);
  }
  if (review.unscored > 0) {
    console.log(`(${review.unscored} pool(s) you voted for have no settled record for that epoch and are not counted above.)`);
  }
  if (lastVoted > 0) {
    console.log(`Last vote cast ${new Date(lastVoted * 1000).toISOString().slice(0, 16).replace("T", " ")} UTC.`);
  }
  console.log(
    `
To compare: backtest --veaero ${Math.max(1, Math.round(review.budget))} --epochs 1 replays the same epoch with this tool's allocation.
`,
  );
}

async function cmdMyVeAero(args: string[]) {
  // Find the first non-flag argument rather than assuming args[0], so
  // `--json` can be passed either before or after the address.
  const address = args.find((a) => !a.startsWith("--"));
  if (!address || !isValidAddress(address)) {
    console.error("Usage: aero-vote-radar my-veaero <wallet address> [--json] (must be a 0x-prefixed 40-character hex address)");
    process.exitCode = 1;
    return;
  }
  const positions = await fetchVeAeroPositions(address);

  if (hasFlag(args, "json")) {
    console.log(JSON.stringify(veAeroPositionsToJson(address, positions), null, 2));
    return;
  }

  if (positions.length === 0) {
    console.log(`No veAERO locks found for ${address}.`);
    return;
  }
  console.log(`\nveAERO locks for ${address}:\n`);
  for (const p of positions) {
    // expiresAt is 0 both for a permanent lock and for a lock with nothing left
    // in it, so read isPermanent rather than treating 0 as Jan 1 1970 or as
    // proof of permanence.
    const expires = p.isPermanent
      ? "never (permanent lock)"
      : p.expiresAt === 0
        ? "no active lock"
        : new Date(p.expiresAt * 1000).toISOString().slice(0, 10);
    console.log(`  NFT #${p.id}: ${p.votingPowerVeAero.toLocaleString("en-US")} veAERO voting power, expires ${expires}`);
  }
  const total = positions.reduce((a, b) => a + b.votingPowerVeAero, 0);
  console.log(`\nTotal voting power: ${total.toLocaleString("en-US")} veAERO\n`);
}

/**
 * Whether `command` is a request for help rather than a mistake — no arguments
 * at all, or an explicit help flag. Both print the same text; only the exit code
 * differs, because a script that runs `aero-vote-radar poolz` and reads $? needs
 * to be told it typed something wrong.
 */
function isHelpRequest(command: string | undefined): boolean {
  return command === undefined || command === "help" || command === "--help" || command === "-h";
}

async function main() {
  const [command, ...rest] = process.argv.slice(2);
  switch (command) {
    case "pools":
      return cmdPools(rest);
    case "recommend":
      return cmdRecommend(rest);
    case "backtest":
      return cmdBacktest(rest);
    case "my-veaero":
      return cmdMyVeAero(rest);
    case "review":
      return cmdReview(rest);
    default: {
      // An unrecognised command exits non-zero: printing usage and reporting
      // success meant a typo in a script looked exactly like a completed run.
      const usage = `aero-vote-radar — Aerodrome (Base) veAERO vote-efficiency tool

Commands:
  pools [--top N] [--min-consistency 0..1] [--json]
      Rank live-gauge pools by current & predicted $/vote, with a consistency score

  recommend (--veaero N | --address 0x...) [--top K] [--min-consistency 0..1] [--max-weight 0..1] [--vote-basis previous|current|typical] [--vote-ready] [--calldata [--nft <id>]] [--json]
      Recommend a self-dilution-aware allocation. --address reads your live voting
      power on-chain instead of you typing the amount; --vote-basis picks which
      vote weight pools are judged against (default: previous, the weight the pool
      settled at last epoch); --vote-ready prints whole percentages that sum to
      100, ready for Aerodrome's voting UI; --calldata prints that same vote as an
      unsigned Voter.vote transaction to paste into your own wallet, cast from the
      veNFT given by --nft (or your only lock, if --address found exactly one).

  backtest (--veaero N | --address 0x...) [--epochs N] [--min-consistency 0..1] [--json]
      Replay past epochs (up to ${MAX_BACKTEST_EPOCHS}) and compare this tool's allocation against the
      naive "vote for the highest current $/vote" strategy. Pass the same
      --min-consistency you vote with, so the backtest tests the strategy you
      actually run; the naive baseline stays unfiltered either way.

  review (--address 0x... | --nft <id>) [--json]
      Score the vote you already cast. Reads which pools your lock chose and what
      share of those pools' settled rewards that bought, for the epoch that has
      closed most recently. Nothing here is a prediction: the epoch is over, so
      every figure can be checked against your own wallet.

  my-veaero <address> [--json]
      Look up an account's veAERO locks and voting power

Pass --json to any command for machine-readable output instead of a table.
`;
      if (isHelpRequest(command)) {
        console.log(usage);
        return;
      }
      console.error(`Unknown command: ${command}
`);
      console.error(usage);
      process.exitCode = 1;
      return;
    }
  }
}

main().catch((err) => {
  console.error(`Error: ${formatError(err)}`);
  process.exitCode = 1;
});

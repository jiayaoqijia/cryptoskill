#!/usr/bin/env node
import { realpathSync } from "node:fs";
import { pathToFileURL } from "node:url";
import {
  ALLOCATE_URL,
  CHAIN_NAMES,
  STALE_HOURS,
  chainName,
  chainOf,
  fetchScan,
  poolName,
  poolToJson,
  rankPools,
  scanAgeHours,
  splitAllocation,
  steadyPools,
  trendOf,
} from "./radar.js";
import { currentSplitPays, readWalletStakes, timersByChain, untilText, withoutOwnSAero, MAX_STAKES, type WalletStakes } from "./stakes.js";
import type { V3ScanFile } from "./v3.js";
import { formatError, isValidAddress, padCol } from "./util.js";

export const DEFAULT_AMOUNT = 10_000;
export const DEFAULT_TOP = 15;

export function fmtUsd(n: number): string {
  if (n === 0) return "$0";
  if (n >= 1000) return `$${Math.round(n).toLocaleString("en-US")}`;
  if (n >= 1) return `$${n.toFixed(2)}`;
  return `$${n.toFixed(4)}`;
}

const fmtNum = (n: number) => n.toLocaleString("en-US", { maximumFractionDigits: 0 });

function getFlag(args: string[], name: string): string | undefined {
  const i = args.indexOf(`--${name}`);
  return i === -1 ? undefined : args[i + 1];
}

function hasFlag(args: string[], name: string): boolean {
  return args.includes(`--${name}`);
}

/**
 * Parses a `--name` flag as a positive integer, falling back to `fallback` if
 * the flag is absent. Returns undefined (rather than NaN or a silently-clamped
 * value) if the flag was given but isn't a positive integer, so callers can
 * print a clear usage error. A dangling flag with no value hits the same error
 * path rather than the fallback.
 */
export function parsePositiveIntFlag(args: string[], name: string, fallback: number): number | undefined {
  const raw = getFlag(args, name);
  if (raw === undefined) return hasFlag(args, name) ? undefined : fallback;
  const n = Number(raw);
  return Number.isInteger(n) && n > 0 ? n : undefined;
}

/** `--amount`: sAERO, any positive number ("25,000" accepted). Same "undefined means print usage" contract. */
export function parseAmountFlag(args: string[], fallback: number | undefined): number | undefined {
  const raw = getFlag(args, "amount");
  if (raw === undefined) return hasFlag(args, "amount") ? undefined : fallback;
  const n = Number(raw.replace(/[,_]/g, ""));
  return Number.isFinite(n) && n > 0 ? n : undefined;
}

/** `--chain`: one of CHAIN_NAMES' keys; absent means every network, `null` a bad value. */
export function parseChainFlag(args: string[]): string | undefined | null {
  const raw = getFlag(args, "chain");
  if (raw === undefined) return hasFlag(args, "chain") ? null : undefined;
  const key = raw.toLowerCase();
  return key in CHAIN_NAMES ? key : null;
}

function usageError(message: string) {
  console.error(`${message}\n\n${USAGE}`);
  process.exitCode = 1;
}

/** One line under every table: how fresh the figures are and what they rest on. */
export function scanLine(scan: V3ScanFile, nowMs: number = Date.now()): string {
  const age = scanAgeHours(scan, nowMs);
  const nets = new Set(scan.gauges.map(chainOf)).size;
  const when = age < 1 ? "under an hour ago" : `${Math.round(age)} h ago`;
  const stale = age > STALE_HOURS ? " — older than usual, the hourly scan may be late" : "";
  return `Scanned from Aero's contracts on ${nets} networks ${when}${stale}; fees from the last ${Math.round(scan.windowHours)} h.`;
}

function poolRow(rank: string, name: string, kind: string, chain: string, cols: string[]) {
  return `${padCol(rank, 4)}${padCol(name, 22)}${padCol(kind, 6)}${padCol(chain, 16)}${cols.map((c) => c.padStart(12)).join("")}`;
}

async function cmdPools(args: string[]) {
  const amount = parseAmountFlag(args, DEFAULT_AMOUNT);
  const top = parsePositiveIntFlag(args, "top", DEFAULT_TOP);
  const chain = parseChainFlag(args);
  if (amount === undefined) return usageError("--amount must be a positive number of sAERO.");
  if (top === undefined) return usageError("--top must be a positive whole number.");
  if (chain === null) return usageError(`--chain must be one of: ${Object.keys(CHAIN_NAMES).join(", ")}.`);
  const steadyOnly = hasFlag(args, "steady");

  const scan = await fetchScan();
  const ranked = (steadyOnly ? steadyPools(scan, amount, chain) : rankPools(scan, amount, chain)).slice(0, top);

  if (hasFlag(args, "json")) {
    const pools = ranked.map((r) => ({ ...poolToJson(r.gauge, scan.windowHours, amount), yourUsdPerDay: r.mine }));
    console.log(JSON.stringify({ checkedAt: scan.checkedAt, windowHours: scan.windowHours, amountSAero: amount, steadyOnly, pools }, null, 2));
    return;
  }

  const title = steadyOnly ? "Steadiest pools" : "Pools";
  console.log(`\n${title} for ${fmtNum(amount)} sAERO${chain ? ` on ${chainName(chain)}` : ""}, per day after your stake dilutes the pool:\n`);
  if (ranked.length === 0) {
    console.log(steadyOnly ? "  No pool has paid steadily for 24 hourly samples yet." : "  No pool with at least 100,000 sAERO allocated is paying right now.");
  } else if (steadyOnly) {
    console.log(poolRow("#", "Pool", "Type", "Network", ["You/day", "Avg/10K", "Low/10K", "Held"]));
    ranked.forEach((r, i) => {
      const s = r.gauge.steady!;
      console.log(poolRow(String(i + 1), poolName(r.gauge), r.gauge.kind ?? "?", chainName(chainOf(r.gauge)), [fmtUsd(r.mine), fmtUsd(s.avgPer10k), fmtUsd(s.minPer10k), `${s.held}/${s.of} h`]));
    });
  } else {
    console.log(poolRow("#", "Pool", "Type", "Network", ["You/day", "Fees/day", "Incent/day", "sAERO", "Trend"]));
    ranked.forEach((r, i) => {
      const g = r.gauge;
      const t = trendOf(g, scan.windowHours);
      const trend = t.change === undefined || t.label === "steady" ? t.label : `${t.label === "rising" ? "+" : ""}${Math.round(t.change * 100)}%`;
      console.log(poolRow(String(i + 1), poolName(g), g.kind ?? "?", chainName(chainOf(g)), [fmtUsd(r.mine), fmtUsd(g.feesUsdPerDay), fmtUsd(g.incentivesUsdPerDay), fmtNum(g.weight), trend]));
    });
  }
  console.log(`\n${scanLine(scan)}\n`);
}

function printTimers(w: WalletStakes, nowSec: number = Date.now() / 1000) {
  const timers = timersByChain(w);
  const keys = Object.keys(CHAIN_NAMES).filter((k) => k in timers);
  if (keys.length) console.log(`Your 47 h timers: ${keys.map((k) => `${chainName(k)} ${untilText(timers[k], nowSec)}`).join(" · ")}`);
  else if (!w.failed.length) console.log("Not allocated yet: the first allocation has no wait.");
  if (w.failed.length) console.log(`Not read (network did not answer): ${w.failed.map(chainName).join(", ")}`);
}

async function cmdRecommend(args: string[]) {
  const address = getFlag(args, "address");
  const amountFlag = parseAmountFlag(args, undefined);
  const chain = parseChainFlag(args);
  if (hasFlag(args, "amount") && amountFlag === undefined) return usageError("--amount must be a positive number of sAERO.");
  if (hasFlag(args, "address") && (address === undefined || !isValidAddress(address))) return usageError("--address must be a 0x… wallet address.");
  if (amountFlag !== undefined && address !== undefined) return usageError("Pass either --amount or --address, not both.");
  if (amountFlag === undefined && address === undefined) return usageError("recommend needs --amount <sAERO> or --address <0x…>.");
  if (chain === null) return usageError(`--chain must be one of: ${Object.keys(CHAIN_NAMES).join(", ")}.`);

  const [scan, wallet] = await Promise.all([fetchScan(), address ? readWalletStakes(address) : Promise.resolve(undefined)]);
  const amount = amountFlag ?? wallet!.totalSAero;
  if (!(amount > 0)) {
    console.log(`\nNo sAERO stake in ${address} on Base — nothing to allocate. Stake AERO on app.aero.xyz first.\n`);
    return;
  }
  const others = wallet ? withoutOwnSAero(scan, wallet) : scan;
  const split = splitAllocation(rankPools(others, amount, chain).map((r) => r.gauge), amount);
  const pays = split.reduce((a, s) => a + s.perDay, 0);
  const current = wallet ? currentSplitPays(wallet, scan) : undefined;

  if (hasFlag(args, "json")) {
    const rows = split.map((s) => ({ ...poolToJson(s.gauge, scan.windowHours, s.amount), percent: Math.round(s.share * 100), sAero: s.amount }));
    console.log(
      JSON.stringify(
        {
          checkedAt: scan.checkedAt,
          amountSAero: amount,
          split: rows,
          splitUsdPerDay: pays,
          current: current ?? null,
          timers: wallet ? timersByChain(wallet) : null,
          notRead: wallet ? wallet.failed : null,
          allocateUrl: ALLOCATE_URL,
        },
        null,
        2,
      ),
    );
    return;
  }

  console.log(`\nSuggested split for ${fmtNum(amount)} sAERO${chain ? ` on ${chainName(chain)}` : ""}:\n`);
  if (split.length === 0) {
    console.log("  No pool with at least 100,000 sAERO allocated is paying right now.\n");
    return;
  }
  console.log(poolRow("%", "Pool", "Type", "Network", ["sAERO", "You/day"]));
  for (const s of split) {
    console.log(poolRow(`${Math.round(s.share * 100)}`, poolName(s.gauge), s.gauge.kind ?? "?", chainName(chainOf(s.gauge)), [fmtNum(s.amount), fmtUsd(s.perDay)]));
  }
  console.log(`\nAbout ${fmtUsd(pays)} a day in total, at today's rates.`);
  if (wallet && current) {
    if (current.placedSAero > 0) console.log(`Your current split pays about ${fmtUsd(current.usdPerDay)} a day.`);
    printTimers(wallet);
  }
  console.log(`\nEnter it on ${ALLOCATE_URL} (Aero has no link that pre-fills a split).`);
  console.log(`\n${scanLine(scan)}\n`);
}

/** Shapes a wallet for --json, matching the MCP `get_my_stakes` tool's response. */
export function walletToJson(w: WalletStakes) {
  return {
    address: w.address,
    stakeCount: w.count,
    totalSAero: w.totalSAero,
    stakes: w.stakes.map((s) => ({ id: s.id.toString(), sAero: s.sAero, chains: s.chains })),
    timers: timersByChain(w),
    notRead: w.failed,
  };
}

async function cmdMyStakes(args: string[]) {
  const address = args.find((a) => !a.startsWith("--"));
  if (address === undefined || !isValidAddress(address)) return usageError("my-stakes needs a 0x… wallet address.");
  const [wallet, scan] = await Promise.all([readWalletStakes(address), fetchScan()]);
  const current = currentSplitPays(wallet, scan);

  if (hasFlag(args, "json")) {
    console.log(JSON.stringify({ ...walletToJson(wallet), currentUsdPerDay: current.usdPerDay }, null, 2));
    return;
  }
  if (wallet.count === 0) {
    console.log(`\nNo sAERO stake in ${address} on Base.\n`);
    return;
  }
  const byGauge = new Map(scan.gauges.map((g) => [`${chainOf(g)}:${g.gauge.toLowerCase()}`, g]));
  console.log(`\n${wallet.count} ${wallet.count === 1 ? "stake" : "stakes"}, ${fmtNum(wallet.totalSAero)} sAERO${wallet.count > MAX_STAKES ? ` (first ${MAX_STAKES} read)` : ""}:\n`);
  for (const st of wallet.stakes) {
    console.log(`  Stake #${st.id}: ${fmtNum(st.sAero)} sAERO`);
    for (const [chain, c] of Object.entries(st.chains)) {
      if (!c.lastAllocated && c.allocations.length === 0) continue;
      const placed = c.allocations.map((a) => {
        const g = byGauge.get(`${chain}:${a.gauge.toLowerCase()}`);
        return `${g ? poolName(g) : a.gauge} ${fmtNum(a.amount)}`;
      });
      console.log(`    ${chainName(chain)}: moves ${untilText(c.readyAt)}${placed.length ? ` — ${placed.join(", ")}` : ""}`);
    }
  }
  console.log(`\nCurrent split pays about ${fmtUsd(current.usdPerDay)} a day at today's rates.`);
  printTimers(wallet);
  console.log(`\nRun \`aero-vote-radar recommend --address ${address}\` for a better split, if there is one.\n`);
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

const USAGE = `aero-vote-radar — where sAERO earns the most on Aero, across its networks

Commands:
  pools [--amount N] [--chain NAME] [--top N] [--steady] [--json]
      Rank pools by what N sAERO (default ${fmtNum(DEFAULT_AMOUNT)}) earns a day after your
      stake dilutes the pool. --steady shows only pools that kept paying hour
      after hour. --chain: ${Object.keys(CHAIN_NAMES).join(", ")}.

  recommend (--amount N | --address 0x...) [--chain NAME] [--json]
      Suggest a split over up to 3 pools in 5% steps, the one that earns the
      most after dilution. --address reads your sAERO on-chain and adds your
      current split and your 47 h timers on each network.

  my-stakes <address> [--json]
      Your stakes, what each has allocated where, the 47 h timer on each
      network and what your current split pays a day.

Figures come from the hourly scan behind aero.deftools.xyz (set
AERO_RADAR_DATA_URL to read another copy). Read-only: no keys, no signing.
Pass --json to any command for machine-readable output.
`;

async function main() {
  const [command, ...rest] = process.argv.slice(2);
  switch (command) {
    case "pools":
      return cmdPools(rest);
    case "recommend":
      return cmdRecommend(rest);
    case "my-stakes":
      return cmdMyStakes(rest);
    default: {
      // An unrecognised command exits non-zero: printing usage and reporting
      // success meant a typo in a script looked exactly like a completed run.
      if (isHelpRequest(command)) {
        console.log(USAGE);
        return;
      }
      usageError(`Unknown command: ${command}`);
    }
  }
}

// Only run when executed directly, not when tests import the parsers. realpath,
// because npx runs the bin through a symlink while import.meta.url is the real file.
const isMainModule = process.argv[1] !== undefined && import.meta.url === pathToFileURL(realpathSync(process.argv[1])).href;
if (isMainModule) {
  main().catch((err) => {
    console.error(`Error: ${formatError(err)}`);
    process.exitCode = 1;
  });
}

/**
 * The two ingredients every measurement in this repo needs: the committed
 * snapshot history (what the radar saw at a moment inside a running epoch) and
 * the settled on-chain answer (what that epoch turned out to be).
 *
 * Both used to live inside `predict-cli.ts`. They moved here when a second
 * measurement — `timing-cli.ts` — needed the same pair, because two copies of a
 * chain scan drift in exactly the way that makes two reports disagree about the
 * same week and leaves no way to tell which one is wrong.
 */
import { execFileSync } from "node:child_process";
import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { fetchActivePools, fetchPoolEpochs, type PoolInfo } from "./pools.js";
import { getTokenPrices } from "./prices.js";
import { epochUsd } from "./efficiency.js";
import { formatError, mapWithConcurrency } from "./util.js";
import { TREND_EPOCHS } from "./constants.js";

const VE_DECIMALS = 18;
export const SNAPSHOT_PATH = "docs/data/snapshot.json";

/**
 * Every committed version of the snapshot, newest first. Empty if git is
 * unavailable — a measurement that cannot read its history should say so and
 * stop, not invent one.
 */
export function snapshotsFromGit(path: string = SNAPSHOT_PATH): unknown[] {
  let shas: string[];
  try {
    shas = execFileSync("git", ["log", "--format=%H", "--", path], { encoding: "utf8" })
      .split("\n")
      .filter(Boolean);
  } catch {
    console.error("Could not read the snapshot history from git. Pass a directory of snapshot JSON files instead.");
    return [];
  }

  const out: unknown[] = [];
  for (const sha of shas) {
    try {
      out.push(JSON.parse(execFileSync("git", ["show", `${sha}:${path}`], { encoding: "utf8", maxBuffer: 64 * 1024 * 1024 })));
    } catch {
      // A commit from before the file existed, or one whose JSON never parsed.
      // Skipping it is right: one unreadable revision is not a reason to refuse
      // to measure anything.
    }
  }
  return out;
}

/**
 * Every `.json` file in `dir`, parsed. Skips a file that can't be read or
 * doesn't parse rather than letting it crash the whole measurement — the same
 * tolerance `snapshotsFromGit` already has for a commit whose JSON never
 * parsed, and for the same reason: one bad file (partial write, an unrelated
 * JSON file that happens to sit in the directory) is not a reason to refuse to
 * measure the rest of it.
 */
export function snapshotsFromDir(dir: string): unknown[] {
  const out: unknown[] = [];
  for (const f of readdirSync(dir).filter((f) => f.endsWith(".json"))) {
    try {
      out.push(JSON.parse(readFileSync(join(dir, f), "utf8")));
    } catch (err) {
      console.error(`(skipping ${f}: ${formatError(err)})`);
    }
  }
  return out;
}

/**
 * What each pool's epochs actually settled at, keyed by address and then by
 * epoch start, so a scan taken at any moment can be paired with the epoch it
 * was taken inside regardless of how deep each pool's own history runs.
 */
export interface SettledHistory {
  pools: PoolInfo[];
  /** address (lowercase) -> epoch start -> vote weight the epoch closed at */
  votes: Map<string, Map<number, number>>;
  /** address (lowercase) -> epoch start -> USD the epoch paid voters */
  usd: Map<string, Map<number, number>>;
}

/**
 * One live scan of Base, turned into the answer key above.
 *
 * `depth` defaults deep enough that a scan from the oldest covered epoch still
 * has a full trailing window strictly older than the epoch it is predicting —
 * the window the radar itself would have had at that moment, with nothing in it
 * that has seen the answer.
 */
export async function loadSettledHistory(depth: number = TREND_EPOCHS + 10): Promise<SettledHistory> {
  const pools = await fetchActivePools();
  const epochsByPool = await mapWithConcurrency(pools, 8, (p) => fetchPoolEpochs(p.address, depth).catch(() => []));
  const allTokens = epochsByPool.flat().flatMap((e) => [
    ...e.bribes.map((b) => b.token),
    ...e.fees.map((f) => f.token),
  ]);
  const prices = await getTokenPrices(allTokens);

  const votes = new Map<string, Map<number, number>>();
  const usd = new Map<string, Map<number, number>>();
  pools.forEach((pool, i) => {
    const v = new Map<number, number>();
    const u = new Map<number, number>();
    for (const e of epochsByPool[i]) {
      v.set(e.ts, Number(e.votes) / 10 ** VE_DECIMALS);
      u.set(e.ts, epochUsd(e, prices));
    }
    votes.set(pool.address.toLowerCase(), v);
    usd.set(pool.address.toLowerCase(), u);
  });

  return { pools, votes, usd };
}

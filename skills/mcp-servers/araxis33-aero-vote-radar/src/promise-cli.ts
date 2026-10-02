#!/usr/bin/env node
/**
 * `npm run promise-check` — writes `docs/data/promise.json`: for every settled
 * epoch the snapshot history covers, the radar's best-ranked pools with what it
 * quoted for them (USD per 10,000 veAERO) beside what they actually paid.
 *
 * Same vantage point as `predict-check` and `timing`: the committed snapshot
 * history supplies what the radar saw before the vote closed, a chain scan
 * supplies what each epoch settled at.
 *
 * Limits, restated rather than left to be discovered: each row is 10,000 veAERO
 * placed alone in one pool (own vote included), not the radar's spread across
 * several, so a bigger vote or a split one earns differently; payouts are
 * valued at today's reward-token prices; and a few epochs are a sanity check,
 * not a track record.
 */
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";
import { pathToFileURL } from "node:url";
import { periodStartOf } from "./trend.js";
import { formatError } from "./util.js";
import { loadSettledHistory, snapshotsFromDir, snapshotsFromGit } from "./settled.js";
import { PER_VEAERO, TOP_POOLS, pickScanPerEpoch, scoreEpochPromise, type EpochPromise } from "./promise.js";

const money = (n: number) => `$${n.toFixed(2)}`;
const pct = (n: number) => `${Math.round(n * 100)}%`;

export function formatPromise(epochs: EpochPromise[]): string {
  const lines: string[] = [];
  for (const e of epochs) {
    lines.push(`\nEpoch of ${e.epochStart} (scan ${e.scannedAt})`);
    lines.push(`  ${"pool".padEnd(24)}${"quoted".padStart(10)}${"paid".padStart(10)}${"paid/quoted".padStart(13)}`);
    for (const r of e.rows) {
      lines.push(
        `  ${r.symbol.padEnd(24)}${money(r.forecastUsd).padStart(10)}${money(r.paidUsd).padStart(10)}${r.ratio.toFixed(2).padStart(13)}`,
      );
    }
    lines.push(
      `  median paid/quoted ${e.medianRatio.toFixed(2)} · paid at least the quote on ${pct(e.paidAtLeastForecast)} · under half on ${pct(e.paidUnderHalf)}`,
    );
  }
  lines.push(
    `\nUSD earned by ${PER_VEAERO.toLocaleString("en-US")} veAERO placed alone in the pool (own vote included), top ${TOP_POOLS} pools by quote.`,
  );
  return lines.join("\n");
}

async function main() {
  const outPath = process.argv[3] ?? "docs/data/promise.json";
  const dir = process.argv[2];
  const snapshots = dir ? snapshotsFromDir(dir) : snapshotsFromGit();
  if (snapshots.length === 0) {
    console.error("No snapshots to measure. This needs the full git history of the snapshot file, not a shallow clone.");
    process.exitCode = 1;
    return;
  }

  const { votes, usd } = await loadSettledHistory();
  const currentEpochStart = periodStartOf(Math.floor(Date.now() / 1000));

  const epochs: EpochPromise[] = [];
  for (const [epochStart, snap] of pickScanPerEpoch(snapshots, currentEpochStart)) {
    const scored = scoreEpochPromise(snap, epochStart, votes, usd);
    if (scored) epochs.push(scored);
  }
  epochs.sort((a, b) => a.epochStart.localeCompare(b.epochStart));

  if (epochs.length === 0) {
    console.error("No epoch could be scored yet — the history has to reach into an epoch that has since settled.");
    process.exitCode = 1;
    return;
  }

  console.log(formatPromise(epochs));
  mkdirSync(dirname(outPath), { recursive: true });
  writeFileSync(outPath, JSON.stringify({ perVeAero: PER_VEAERO, topPools: TOP_POOLS, epochs }, null, 2) + "\n");
  console.error(`wrote ${outPath}: ${epochs.length} settled epoch(s)`);
}

const isMainModule = process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href;
if (isMainModule) {
  main().catch((error) => {
    console.error(`promise-check failed: ${formatError(error)}`);
    process.exitCode = 1;
  });
}

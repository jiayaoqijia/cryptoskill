#!/usr/bin/env node
/**
 * `npm run predict-check` — measures which vote basis actually predicts the
 * weight an epoch settles at.
 *
 * The vantage point is the whole trick. A backtest replaying a closed epoch has
 * no mid-week vote tally to work from, so `previous` and `current` collapse to
 * the same number there and it cannot separate them. But every scan this repo
 * has ever committed to `docs/data/snapshot.json` recorded the live tally at
 * that moment, six-hourly — so each scan taken inside an epoch that has since
 * settled *is* a real mid-week vantage point, with the answer now known.
 *
 * So: walk the git history of the snapshot, keep the scans from settled epochs,
 * and score each basis against what those epochs settled at.
 *
 * Limits, which the report restates rather than leaving to be discovered:
 * observations within one pool are not independent (the same pool appears at
 * every scan time), and only epochs with snapshot coverage can be scored.
 */
import { pathToFileURL } from "node:url";
import { periodStartOf } from "./trend.js";
import { formatError } from "./util.js";
import { loadSettledHistory, snapshotsFromDir, snapshotsFromGit } from "./settled.js";
import {
  asRatio,
  inBucket,
  observationsFromSnapshot,
  scorePredictors,
  SIZE_BUCKETS,
  type PredictionObservation,
} from "./predict.js";

const BASES = ["previous", "current", "typical"];

// Re-exported because the tests import it from here, where it lived before the
// second measurement needed it too. The implementation is in settled.ts.
export { snapshotsFromDir };

async function main() {
  const dir = process.argv[2];
  const snapshots = dir ? snapshotsFromDir(dir) : snapshotsFromGit();
  if (snapshots.length === 0) {
    console.error("No snapshots to measure.");
    process.exitCode = 1;
    return;
  }

  const { votes: settledVotes, usd: settledUsd } = await loadSettledHistory();
  const currentEpochStart = periodStartOf(Math.floor(Date.now() / 1000));
  const observations: PredictionObservation[] = [];
  const epochsCovered = new Set<number>();
  const poolsSeen = new Set<string>();

  for (const raw of snapshots) {
    const result = observationsFromSnapshot(raw, settledVotes, settledUsd, currentEpochStart);
    if (!result) continue;
    for (const { address, observation } of result.entries) {
      observations.push(observation);
      epochsCovered.add(result.epochStart);
      poolsSeen.add(address);
    }
  }

  if (observations.length === 0) {
    console.error(
      "No scorable observations. This needs snapshots taken inside an epoch that has since settled — the history may not reach back that far yet.",
    );
    process.exitCode = 1;
    return;
  }

  const pct = (n: number) => `${(asRatio(n) * 100).toFixed(0)}%`;
  const signed = (n: number) => `${asRatio(n) >= 0 ? "+" : ""}${(asRatio(n) * 100).toFixed(0)}%`;

  const dates = [...epochsCovered]
    .sort((a, b) => a - b)
    .map((t) => new Date(t * 1000).toISOString().slice(0, 10));

  console.log(
    `\nPredicting the vote weight each epoch settled at, from real mid-week vantage points.`,
  );
  console.log(
    `${observations.length.toLocaleString("en-US")} observations · ${poolsSeen.size} pools · ${epochsCovered.size} settled epoch(s): ${dates.join(", ")}\n`,
  );

  const row = (label: string, obs: PredictionObservation[]) => {
    const scores = scorePredictors(obs, BASES);
    console.log(label);
    for (const s of scores) {
      console.log(
        "  " +
          s.name.padEnd(10) +
          String(s.observations).padStart(8) +
          pct(s.medianAbsError).padStart(10) +
          signed(s.medianBias).padStart(10) +
          String(s.closestOn).padStart(12),
      );
    }
  };

  console.log("  basis".padEnd(12) + "n".padStart(8) + "error".padStart(10) + "bias".padStart(10) + "closest on".padStart(12));
  console.log("  " + "-".repeat(48));
  row("  all observations:", observations);

  for (const bucket of SIZE_BUCKETS) {
    const subset = observations.filter((o) => inBucket(o, bucket));
    if (subset.length === 0) continue;
    console.log("");
    row(`  ${bucket.label}:`, subset);
  }

  console.log(
    "\nError is the median absolute miss on a log scale, so 17% means the typical guess is 17% out;" +
      "\npayout depends on weight multiplicatively, which is why it is not measured in votes. Bias is" +
      "\nthe median signed miss: a predictor can be no noisier than another and still be systematically" +
      "\nhigh, and the allocator divides by this figure, so that bias reaches every pool it prices.",
  );
  console.log(
    "\nTreat the count as fewer independent points than it looks: the same pool appears at every scan" +
      "\ntime, so observations within a pool are correlated. Only epochs with snapshot coverage can be" +
      "\nscored at all.",
  );
}

// Only run when this file is executed directly (as `npm run predict-check`),
// not when it's imported — e.g. by tests importing `snapshotsFromDir`. Without
// this, importing the module for its pure helpers would also kick off `main`'s
// live chain scan, the same hazard `mcp-server.ts` guards against for the same
// reason.
const isMainModule = process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href;
if (isMainModule) {
  main().catch((err) => {
    console.error(`Error: ${formatError(err)}`);
    process.exitCode = 1;
  });
}

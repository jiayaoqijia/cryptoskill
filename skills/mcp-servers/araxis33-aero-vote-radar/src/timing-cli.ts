#!/usr/bin/env node
/**
 * `npm run timing` — writes `docs/data/timing.json`, the file that lets the page
 * say how much of itself a visitor should believe.
 *
 * It answers three questions from the same pair of sources (the committed scan
 * history and the settled on-chain answer), because they are three faces of one
 * fact — that the weight behind every per-vote figure is still moving:
 *
 *   1. how much of the ranking on screen survives to the epoch's close;
 *   2. which pools are the ones that move, by name;
 *   3. how far the tally the allocation is built on typically misses, which is
 *      what turns a single expected-dollars figure into an honest range.
 *
 * Unlike the snapshot, this changes only when an epoch settles, so it is built
 * weekly rather than six-hourly — and it needs the full git history of the
 * snapshot file, not a shallow clone.
 */
import { writeFileSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";
import { pathToFileURL } from "node:url";
import { periodStartOf } from "./trend.js";
import { formatError } from "./util.js";
import { loadSettledHistory, snapshotsFromDir, snapshotsFromGit } from "./settled.js";
import { buildTimingReport, scanFromSnapshot, type TimingScan } from "./timing.js";
import {
  asRatio,
  inBucket,
  observationsFromSnapshot,
  scorePredictors,
  SIZE_BUCKETS,
  type PredictionObservation,
} from "./predict.js";

const BASES = ["previous", "current", "typical"];

/**
 * The accuracy figures, in the shape the page reads them: one entry per vote
 * basis, plus the same scores per pool-size bucket.
 *
 * The two bases named here are the two the page offers, so a visitor is shown
 * the error of the basis they actually have selected rather than an average
 * over settings they are not using.
 */
export interface BasisAccuracy {
  name: string;
  observations: number;
  /** Median absolute miss as a ratio: 0.2 means the typical guess is 20% out. */
  medianAbsError: number;
  /** Median signed miss, same scale. */
  medianBias: number;
  /** How often this basis was the closest of the three. */
  closestOn: number;
}

export interface AccuracyReport {
  overall: BasisAccuracy[];
  buckets: { label: string; bases: BasisAccuracy[] }[];
  epochs: string[];
}

const toAccuracy = (observations: PredictionObservation[]): BasisAccuracy[] =>
  scorePredictors(observations, BASES).map((s) => ({
    name: s.name,
    observations: s.observations,
    medianAbsError: asRatio(s.medianAbsError),
    medianBias: asRatio(s.medianBias),
    closestOn: s.closestOn,
  }));

/**
 * Assembles the accuracy section of `docs/data/timing.json` from already-scored
 * observations. Pure and exported so the bucket-filtering behaviour below is
 * unit-testable without a chain scan or the committed snapshot history — the
 * same separation `predict.ts`'s `scorePredictors`/`observationsFromSnapshot`
 * already have from `predict-cli.ts`'s live-fetching `main`.
 *
 * A pool-size bucket with no observations is dropped rather than published
 * empty: `scorePredictors` still returns a row per basis with `observations: 0`
 * and a `NaN` error/bias for an empty input, and shipping that to the page
 * would render as a literal "NaN%" instead of the bucket simply not appearing.
 * Checking `bases[0].observations` is enough because every basis is scored
 * against the same filtered set, so all three always agree on the count.
 */
export function buildAccuracyReport(observations: PredictionObservation[], epochsCovered: Set<number>): AccuracyReport {
  return {
    overall: toAccuracy(observations),
    buckets: SIZE_BUCKETS.map((bucket) => ({
      label: bucket.label,
      bases: toAccuracy(observations.filter((o) => inBucket(o, bucket))),
    })).filter((b) => b.bases.length > 0 && b.bases[0].observations > 0),
    epochs: [...epochsCovered].sort((a, b) => a - b).map((t) => new Date(t * 1000).toISOString().slice(0, 10)),
  };
}

async function main() {
  const outPath = process.argv[3] ?? "docs/data/timing.json";
  const dir = process.argv[2];
  const snapshots = dir ? snapshotsFromDir(dir) : snapshotsFromGit();
  if (snapshots.length === 0) {
    console.error("No snapshots to measure. This needs the full git history of the snapshot file, not a shallow clone.");
    process.exitCode = 1;
    return;
  }

  const { votes, usd } = await loadSettledHistory();
  const currentEpochStart = periodStartOf(Math.floor(Date.now() / 1000));

  const scans: TimingScan[] = [];
  const observations: PredictionObservation[] = [];
  const epochsCovered = new Set<number>();
  for (const raw of snapshots) {
    const scan = scanFromSnapshot(raw, votes, usd, currentEpochStart);
    if (scan && scan.rows.length > 0) scans.push(scan);

    // The same scans, scored the way `predict-check` scores them, so the page's
    // accuracy panel and the command line can never quote different numbers for
    // the same week.
    const scored = observationsFromSnapshot(raw, votes, usd, currentEpochStart);
    if (!scored) continue;
    for (const { observation } of scored.entries) {
      observations.push(observation);
      epochsCovered.add(scored.epochStart);
    }
  }

  if (scans.length === 0 || observations.length === 0) {
    console.error("No scorable scans yet — the snapshot history has to reach back into an epoch that has since settled.");
    process.exitCode = 1;
    return;
  }

  const accuracy = buildAccuracyReport(observations, epochsCovered);

  const report = { ...buildTimingReport(scans), accuracy };

  mkdirSync(dirname(outPath), { recursive: true });
  writeFileSync(outPath, JSON.stringify(report, null, 2) + "\n");
  console.error(
    `wrote ${outPath}: ${report.scans} scans across ${report.epochs.length} settled epoch(s), ` +
      `${report.lateMovers.length} pool(s) that move late`,
  );
}

const isMainModule = process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href;
if (isMainModule) {
  main().catch((err) => {
    console.error(`Error: ${formatError(err)}`);
    process.exitCode = 1;
  });
}

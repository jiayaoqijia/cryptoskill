import { test } from "node:test";
import assert from "node:assert/strict";
import { buildAccuracyReport } from "../src/timing-cli.js";
import type { PredictionObservation } from "../src/predict.js";

const obs = (actual: number, tally: number, predicted: Record<string, number> = {}): PredictionObservation => ({
  actual,
  tally,
  predicted: { previous: actual, current: actual, typical: actual, ...predicted },
});

test("buildAccuracyReport scores the overall set and reports the covered epochs sorted", () => {
  const report = buildAccuracyReport(
    [obs(1_000, 1_000), obs(2_000, 2_000)],
    new Set([2_000_000, 1_000_000]),
  );

  assert.equal(report.overall.length, 3);
  assert.ok(report.overall.every((b) => b.observations === 2));
  assert.deepEqual(report.epochs, [
    new Date(1_000_000 * 1000).toISOString().slice(0, 10),
    new Date(2_000_000 * 1000).toISOString().slice(0, 10),
  ]);
});

test("buildAccuracyReport drops a pool-size bucket with no observations rather than publishing an empty (NaN) one", () => {
  // Both observations fall in the "under 10k votes" bucket; every other bucket
  // (10k-100k, 100k-1M, 1M+) has nothing to score and must not appear at all —
  // scorePredictors would otherwise hand back a row with observations: 0 and a
  // NaN error/bias, which the page would render as a literal "NaN%".
  const report = buildAccuracyReport([obs(500, 500), obs(800, 800)], new Set());

  assert.equal(report.buckets.length, 1);
  assert.equal(report.buckets[0].label, "under 10k votes");
  assert.ok(report.buckets[0].bases.every((b) => b.observations === 2));
});

test("buildAccuracyReport splits observations across every bucket they actually land in", () => {
  const report = buildAccuracyReport(
    [obs(500, 500), obs(50_000, 50_000), obs(500_000, 500_000), obs(5_000_000, 5_000_000)],
    new Set(),
  );

  assert.deepEqual(
    report.buckets.map((b) => b.label),
    ["under 10k votes", "10k - 100k votes", "100k - 1M votes", "1M+ votes"],
  );
  assert.ok(report.buckets.every((b) => b.bases.every((base) => base.observations === 1)));
});

test("buildAccuracyReport returns no buckets and no epochs for an empty input", () => {
  const report = buildAccuracyReport([], new Set());
  assert.deepEqual(report.buckets, []);
  assert.deepEqual(report.epochs, []);
  assert.ok(report.overall.every((b) => b.observations === 0));
});

import { test } from "node:test";
import assert from "node:assert/strict";
import {
  buildTimingReport,
  scanFromSnapshot,
  topTenSurvivors,
  windowFor,
  MIN_POOLS_FOR_RANKING,
  MIN_SURGE_READINGS,
  SURGE_BADGE_THRESHOLD,
  THICK_VOTES,
  type SettledRow,
  type TimingScan,
} from "../src/timing.js";
import { WEEKLY_EPOCH, periodStartOf } from "../src/trend.js";

const row = (i: number, over: Partial<SettledRow> = {}): SettledRow => ({
  address: `0x${String(i).padStart(40, "0")}`,
  symbol: `POOL${i}`,
  tally: 100_000,
  settled: 100_000,
  usd: 1_000,
  ...over,
});

const rows = (n: number, over: (i: number) => Partial<SettledRow> = () => ({})): SettledRow[] =>
  Array.from({ length: n }, (_, i) => row(i, over(i)));

test("topTenSurvivors refuses to score a field too small for a top ten to mean anything", () => {
  assert.equal(topTenSurvivors(rows(MIN_POOLS_FOR_RANKING - 1)), null);
  assert.notEqual(topTenSurvivors(rows(MIN_POOLS_FOR_RANKING)), null);
});

test("topTenSurvivors scores a ranking that does not move at all as ten of ten", () => {
  // Rates differ pool to pool but nothing moves between the scan and the close.
  assert.equal(topTenSurvivors(rows(20, (i) => ({ usd: 1_000 + i * 10 }))), 10);
});

test("topTenSurvivors sees through a top ten built on weight that has not arrived yet", () => {
  // Pools 0-9 look best now only because their gauges are near-empty; by close
  // each has filled up and pools 10-19, whose weight never moved, take over.
  const set = rows(20, (i) =>
    i < 10
      ? { tally: 1_000, settled: 1_000_000, usd: 5_000 }
      : { tally: 100_000, settled: 100_000, usd: 5_000 },
  );
  assert.equal(topTenSurvivors(set), 0);
});

test("windowFor places a scan by hours left, and leaves a settled-epoch overshoot out", () => {
  assert.equal(windowFor(150)?.label, "Thursday–Friday");
  assert.equal(windowFor(100)?.label, "Saturday–Sunday");
  assert.equal(windowFor(30)?.label, "Monday–Tuesday");
  assert.equal(windowFor(6)?.label, "Wednesday");
  assert.equal(windowFor(1)?.label, "final hours");
  assert.equal(windowFor(200), null);
  assert.equal(windowFor(-1), null);
});

const scan = (hoursLeft: number, epochStart: number, r: SettledRow[]): TimingScan => ({
  takenAt: epochStart + WEEKLY_EPOCH.lengthSeconds - hoursLeft * 3600,
  epochStart,
  hoursLeft,
  rows: r,
});

test("buildTimingReport reports survival per window and counts the scans behind it", () => {
  const epoch = periodStartOf(1_760_000_000);
  const stable = rows(20, (i) => ({ usd: 1_000 + i }));
  const report = buildTimingReport([scan(150, epoch, stable), scan(1, epoch, stable)], "2026-09-07T00:00:00.000Z");

  const thursday = report.trust.find((w) => w.label === "Thursday–Friday")!;
  assert.equal(thursday.scans, 1);
  assert.equal(thursday.keptAll, 10);
  const empty = report.trust.find((w) => w.label === "Monday–Tuesday")!;
  assert.equal(empty.scans, 0);
  assert.equal(empty.keptAll, null);
  assert.deepEqual(report.epochs, [new Date(epoch * 1000).toISOString().slice(0, 10)]);
});

test("buildTimingReport scores thin gauges separately from pools with real weight behind them", () => {
  const epoch = periodStartOf(1_760_000_000);
  // Half the field is near-empty and reshuffles completely; the other half is
  // heavy and does not move. Scored together the ranking looks worthless.
  const mixed = [
    // Top of the list now (a tiny tally makes any reward look enormous per
    // vote), bottom of it at close, once the gauge has filled and the modest
    // reward is spread across it.
    ...rows(15, (i) => ({ tally: 500, settled: THICK_VOTES - 1, usd: 100 + i })),
    ...Array.from({ length: 15 }, (_, i) =>
      row(100 + i, { tally: THICK_VOTES * 2, settled: THICK_VOTES * 2, usd: 5_000 + i }),
    ),
  ];
  const report = buildTimingReport([scan(150, epoch, mixed)], "2026-09-07T00:00:00.000Z");
  const thursday = report.trust.find((w) => w.label === "Thursday–Friday")!;
  assert.equal(thursday.keptAll, 0);
  assert.equal(thursday.keptThick, 10);
});

test("buildTimingReport names a pool as a late mover only with enough readings and a move worth stating", () => {
  const epoch = periodStartOf(1_760_000_000);
  const scans: TimingScan[] = [];
  for (let i = 0; i < MIN_SURGE_READINGS; i++) {
    scans.push(
      scan(36, epoch - i * WEEKLY_EPOCH.lengthSeconds, [
        row(1, { symbol: "SURGER", tally: 100_000, settled: 300_000 }),
        row(2, { symbol: "STEADY", tally: 100_000, settled: 100_000 }),
        row(3, { symbol: "RARE", tally: 100_000, settled: 400_000 }),
      ]),
    );
  }
  // RARE only has readings from one week: drop it from the last few scans.
  for (const s of scans.slice(1)) s.rows = s.rows.filter((r) => r.symbol !== "RARE");

  const report = buildTimingReport(scans, "2026-09-07T00:00:00.000Z");
  const named = report.lateMovers.map((m) => m.symbol);
  assert.deepEqual(named, ["SURGER"]);
  assert.equal(report.lateMovers[0].readings, MIN_SURGE_READINGS);
  assert.ok(Math.abs(report.lateMovers[0].medianSurge - 2) < 1e-9);
  assert.ok(SURGE_BADGE_THRESHOLD < 2);
});

test("buildTimingReport ignores a scan taken outside the surge window when naming late movers", () => {
  const epoch = periodStartOf(1_760_000_000);
  const scans = Array.from({ length: MIN_SURGE_READINGS }, (_, i) =>
    // 150 hours out, far from the 48-24h window a surge is measured over.
    scan(150, epoch - i * WEEKLY_EPOCH.lengthSeconds, [row(1, { symbol: "SURGER", tally: 100_000, settled: 300_000 })]),
  );
  assert.deepEqual(buildTimingReport(scans, "2026-09-07T00:00:00.000Z").lateMovers, []);
});

const settledMaps = (epoch: number, votes: number, usd: number) => ({
  votes: new Map([["0xpool", new Map([[epoch, votes]])]]),
  usd: new Map([["0xpool", new Map([[epoch, usd]])]]),
});

test("scanFromSnapshot pairs a scan with the epoch it was taken inside", () => {
  const epoch = periodStartOf(1_760_000_000);
  const takenAt = epoch + 3600; // one hour in, so 167 hours left
  const { votes, usd } = settledMaps(epoch, 250_000, 900);
  const result = scanFromSnapshot(
    { generatedAt: new Date(takenAt * 1000).toISOString(), pools: [{ pool: "0xPOOL", symbol: "P", votesVeAero: 100_000 }] },
    votes,
    usd,
    epoch + WEEKLY_EPOCH.lengthSeconds,
  );
  assert.ok(result);
  assert.equal(result.epochStart, epoch);
  assert.ok(Math.abs(result.hoursLeft - 167) < 0.01);
  assert.deepEqual(result.rows, [{ address: "0xpool", symbol: "P", tally: 100_000, settled: 250_000, usd: 900 }]);
});

test("scanFromSnapshot refuses a scan from the epoch still running, which has no answer yet", () => {
  const epoch = periodStartOf(1_760_000_000);
  const { votes, usd } = settledMaps(epoch, 250_000, 900);
  const result = scanFromSnapshot(
    { generatedAt: new Date((epoch + 3600) * 1000).toISOString(), pools: [{ pool: "0xpool", votesVeAero: 100 }] },
    votes,
    usd,
    epoch, // the epoch being scanned is the current one
  );
  assert.equal(result, null);
});

test("scanFromSnapshot skips a pool with no settled history rather than dropping the scan", () => {
  const epoch = periodStartOf(1_760_000_000);
  const { votes, usd } = settledMaps(epoch, 250_000, 900);
  const result = scanFromSnapshot(
    {
      generatedAt: new Date((epoch + 3600) * 1000).toISOString(),
      pools: [
        { pool: "0xunknown", symbol: "U", votesVeAero: 100 },
        { pool: "0xpool", symbol: "P", votesVeAero: 100_000 },
      ],
    },
    votes,
    usd,
    epoch + WEEKLY_EPOCH.lengthSeconds,
  );
  assert.equal(result?.rows.length, 1);
  assert.equal(result?.rows[0].symbol, "P");
});

test("scanFromSnapshot returns null for malformed input instead of guessing", () => {
  const { votes, usd } = settledMaps(0, 1, 1);
  assert.equal(scanFromSnapshot({}, votes, usd, 1), null);
  assert.equal(scanFromSnapshot({ generatedAt: "not a date", pools: [] }, votes, usd, 1), null);
  assert.equal(scanFromSnapshot({ pools: [] }, votes, usd, 1), null);
});

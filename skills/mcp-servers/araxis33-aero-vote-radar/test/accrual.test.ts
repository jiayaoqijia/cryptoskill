import { test } from "node:test";
import assert from "node:assert/strict";
import {
  buildAccrualReport,
  buildWindows,
  scanFromSnapshot,
  valueAt,
  type AccrualScan,
  type TokenPrice,
} from "../src/accrual.js";

const HOUR = 3600;
const EPOCH = 1788393600;

const prices = (entries: [string, number, number][]): Map<string, TokenPrice> =>
  new Map(entries.map(([a, decimals, priceUsd]) => [a, { decimals, priceUsd }]));

function scan(
  at: number,
  pools: { pool: string; amounts: [string, bigint][]; usd: number; epochTs?: number; symbol?: string }[],
  priceMap: Map<string, TokenPrice>,
): AccrualScan {
  return {
    at,
    prices: priceMap,
    pools: new Map(
      pools.map((p) => [
        p.pool,
        {
          symbol: p.symbol ?? p.pool,
          pool: p.pool,
          epochTs: p.epochTs ?? EPOCH,
          amounts: p.amounts,
          usd: p.usd,
        },
      ]),
    ),
  };
}

test("valueAt prices raw amounts by each token's own decimals", () => {
  const p = prices([
    ["0xaaa", 18, 2],
    ["0xbbb", 6, 1],
  ]);
  assert.equal(valueAt([["0xaaa", 3n * 10n ** 18n]], p), 6);
  assert.equal(valueAt([["0xbbb", 5n * 10n ** 6n]], p), 5);
  assert.equal(valueAt([["0xaaa", 10n ** 18n], ["0xbbb", 10n ** 6n]], p), 3);
});

test("valueAt counts a token the price vector has no entry for as zero, the same way the scan did", () => {
  const p = prices([["0xaaa", 18, 2]]);
  assert.equal(valueAt([["0xunknown", 10n ** 18n]], p), 0);
  assert.equal(valueAt([["0xaaa", 10n ** 18n], ["0xunknown", 999n * 10n ** 18n]], p), 2);
});

test("valueAt treats an explicitly zero price as zero rather than dropping the token's decimals", () => {
  const p = prices([["0xaaa", 18, 0]]);
  assert.equal(valueAt([["0xaaa", 10n ** 18n]], p), 0);
});

test("buildWindows removes the price move by valuing both ends at one vector", () => {
  // Same amounts at both ends, but the scan's own dollar figure doubled: a pure
  // price move, and the accrual figure has to read it as zero.
  const later = prices([["0xaaa", 18, 4]]);
  const scans = [
    scan(0, [{ pool: "0xp", amounts: [["0xaaa", 10n ** 18n]], usd: 2 }], prices([["0xaaa", 18, 2]])),
    scan(48 * HOUR, [{ pool: "0xp", amounts: [["0xaaa", 10n ** 18n]], usd: 4 }], later),
  ];
  const [w] = buildWindows(scans, 48);
  assert.equal(w.naiveUsd, 2);
  assert.equal(w.accrualUsd, 0);
  assert.equal(w.repricingUsd, 2);
  assert.equal(w.amountMoved, false);
});

test("buildWindows reports real accrual at one price even while the price is moving", () => {
  const later = prices([["0xaaa", 18, 4]]);
  const scans = [
    scan(0, [{ pool: "0xp", amounts: [["0xaaa", 10n ** 18n]], usd: 2 }], prices([["0xaaa", 18, 2]])),
    scan(48 * HOUR, [{ pool: "0xp", amounts: [["0xaaa", 3n * 10n ** 18n]], usd: 12 }], later),
  ];
  const [w] = buildWindows(scans, 48);
  assert.equal(w.naiveUsd, 10);
  // Two extra tokens at the later price, and nothing of the repricing of the first.
  assert.equal(w.accrualUsd, 8);
  assert.equal(w.repricingUsd, 2);
  assert.equal(w.amountMoved, true);
  assert.equal(w.amountFell, false);
});

test("buildWindows skips a pair that straddles an epoch boundary rather than reading the reset as a loss", () => {
  const p = prices([["0xaaa", 18, 1]]);
  const scans = [
    scan(0, [{ pool: "0xp", amounts: [["0xaaa", 9n * 10n ** 18n]], usd: 9, epochTs: EPOCH }], p),
    scan(48 * HOUR, [{ pool: "0xp", amounts: [["0xaaa", 10n ** 18n]], usd: 1, epochTs: EPOCH + 604800 }], p),
  ];
  assert.deepEqual(buildWindows(scans, 48), []);
});

test("buildWindows flags an amount that fell inside one epoch instead of reporting it as negative earnings", () => {
  const p = prices([["0xaaa", 18, 1]]);
  const scans = [
    scan(0, [{ pool: "0xp", amounts: [["0xaaa", 5n * 10n ** 18n]], usd: 5 }], p),
    scan(48 * HOUR, [{ pool: "0xp", amounts: [["0xaaa", 2n * 10n ** 18n]], usd: 2 }], p),
  ];
  const [w] = buildWindows(scans, 48);
  assert.equal(w.amountFell, true);
  assert.equal(w.amountMoved, true);
  assert.equal(w.accrualUsd, -3);
});

test("buildWindows picks the scan closest to the requested gap, not merely the first one inside it", () => {
  const p = prices([["0xaaa", 18, 1]]);
  const pool = (usd: number, amount: bigint) => [{ pool: "0xp", amounts: [["0xaaa", amount]] as [string, bigint][], usd }];
  const scans = [
    scan(0, pool(1, 10n ** 18n), p),
    scan(40 * HOUR, pool(2, 2n * 10n ** 18n), p),
    scan(47 * HOUR, pool(3, 3n * 10n ** 18n), p),
    scan(58 * HOUR, pool(4, 4n * 10n ** 18n), p),
  ];
  const windows = buildWindows(scans, 48).filter((w) => w.fromAt === 0);
  assert.equal(windows.length, 1);
  assert.equal(windows[0].toAt, 47 * HOUR);
});

test("buildWindows ignores a pair outside the tolerance entirely", () => {
  const p = prices([["0xaaa", 18, 1]]);
  const scans = [
    scan(0, [{ pool: "0xp", amounts: [["0xaaa", 10n ** 18n]], usd: 1 }], p),
    scan(10 * HOUR, [{ pool: "0xp", amounts: [["0xaaa", 2n * 10n ** 18n]], usd: 2 }], p),
  ];
  assert.deepEqual(buildWindows(scans, 48), []);
});

test("buildWindows counts a token with no price as unpriced on both sides rather than silently", () => {
  const p = prices([["0xaaa", 18, 1]]);
  const scans = [
    scan(0, [{ pool: "0xp", amounts: [["0xaaa", 10n ** 18n], ["0xnope", 5n]], usd: 1 }], p),
    scan(48 * HOUR, [{ pool: "0xp", amounts: [["0xaaa", 2n * 10n ** 18n], ["0xnope", 9n]], usd: 2 }], p),
  ];
  const [w] = buildWindows(scans, 48);
  assert.equal(w.unpricedTokens, 1);
  assert.equal(w.accrualUsd, 1);
});

test("scanFromSnapshot refuses a snapshot from before the raw amounts were published", () => {
  assert.equal(
    scanFromSnapshot({
      generatedAt: "2026-08-01T00:00:00.000Z",
      pools: [{ pool: "0xp", symbol: "x", latestEpochTs: EPOCH, latestEpochUsd: 5 }],
    }),
    null,
  );
});

test("scanFromSnapshot merges bribes and fees and lowercases every address", () => {
  const s = scanFromSnapshot({
    generatedAt: "2026-09-01T00:00:00.000Z",
    rewardTokens: [{ address: "0xAAA", decimals: 18, priceUsd: 2 }],
    pools: [
      {
        pool: "0xPOOL",
        symbol: "vAMM-x/y",
        latestEpochTs: EPOCH,
        latestEpochUsd: 7,
        latestEpochBribes: [["0xAAA", "1000000000000000000"]],
        latestEpochFees: [["0xAAA", "2000000000000000000"]],
      },
    ],
  });
  assert.ok(s);
  assert.ok(s.prices.has("0xaaa"));
  const pool = s.pools.get("0xpool");
  assert.ok(pool);
  assert.equal(pool.amounts.length, 2);
  assert.equal(valueAt(pool.amounts, s.prices), 6);
});

test("scanFromSnapshot drops an amount that is not an integer string rather than calling it zero", () => {
  const s = scanFromSnapshot({
    generatedAt: "2026-09-01T00:00:00.000Z",
    rewardTokens: [{ address: "0xaaa", decimals: 18, priceUsd: 1 }],
    pools: [
      {
        pool: "0xp",
        symbol: "p",
        latestEpochTs: EPOCH,
        latestEpochUsd: 1,
        latestEpochBribes: [["0xaaa", "not-a-number"], ["0xaaa", "1000000000000000000"]],
        latestEpochFees: [],
      },
    ],
  });
  assert.ok(s);
  assert.equal(s.pools.get("0xp")?.amounts.length, 1);
});

test("scanFromSnapshot returns null for a scan whose pools all lack amounts, so it cannot pad the count", () => {
  assert.equal(
    scanFromSnapshot({
      generatedAt: "2026-09-01T00:00:00.000Z",
      rewardTokens: [{ address: "0xaaa", decimals: 18, priceUsd: 1 }],
      pools: [{ pool: "0xp", symbol: "p", latestEpochTs: EPOCH, latestEpochUsd: 0, latestEpochBribes: [], latestEpochFees: [] }],
    }),
    null,
  );
});

test("buildAccrualReport separates the pools that only repriced from the ones that earned", () => {
  const p = prices([["0xaaa", 18, 1]]);
  const amounts = (n: bigint): [string, bigint][] => [["0xaaa", n * 10n ** 18n]];
  const scans = [
    scan(
      0,
      [
        { pool: "0xstill", symbol: "STILL", amounts: amounts(10n), usd: 5 },
        { pool: "0xearns", symbol: "EARNS", amounts: amounts(1n), usd: 1 },
      ],
      p,
    ),
    scan(
      48 * HOUR,
      [
        { pool: "0xstill", symbol: "STILL", amounts: amounts(10n), usd: 30 },
        { pool: "0xearns", symbol: "EARNS", amounts: amounts(4n), usd: 4 },
      ],
      p,
    ),
  ];

  const report = buildAccrualReport(scans, [48], new Date("2026-09-15T00:00:00.000Z"));
  const [w] = report.windows;
  assert.equal(w.observations, 2);
  assert.equal(w.withAccrual, 0.5);
  assert.equal(w.negativeAccrual, 0);
  assert.equal(w.medianAccrualWhenMoved, 3);

  assert.deepEqual(report.pureRepricing.map((r) => r.symbol), ["STILL"]);
  assert.equal(report.pureRepricing[0].repricingUsd, 25);
  assert.deepEqual(report.didAccrue.map((r) => r.symbol), ["EARNS"]);
  assert.equal(report.didAccrue[0].accrualUsd, 3);
});

test("buildAccrualReport keeps one row per pool, not one per overlapping window", () => {
  const p = prices([["0xaaa", 18, 1]]);
  const at = (t: number, n: bigint, usd: number) =>
    scan(t, [{ pool: "0xp", symbol: "P", amounts: [["0xaaa", n * 10n ** 18n]], usd }], p);
  const report = buildAccrualReport([at(0, 1n, 1), at(48 * HOUR, 5n, 5), at(96 * HOUR, 9n, 9)], [48]);
  assert.equal(report.windows[0].observations, 2);
  assert.equal(report.didAccrue.length, 1);
  assert.equal(report.didAccrue[0].accrualUsd, 4);
});

test("buildAccrualReport reports an empty history without throwing or inventing a range", () => {
  const report = buildAccrualReport([], [48]);
  assert.equal(report.scans, 0);
  assert.equal(report.from, "");
  assert.equal(report.windows[0].observations, 0);
  assert.ok(Number.isNaN(report.windows[0].withAccrual));
  assert.deepEqual(report.pureRepricing, []);
  assert.deepEqual(report.didAccrue, []);
});

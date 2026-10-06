import { test } from "node:test";
import assert from "node:assert/strict";
import {
  gaugeWeightAt,
  incentiveRatesNow,
  readFeesCollected,
  readIncentivePrograms,
  readV3Gauges,
  v3GaugeYield,
  V3_PRECISION,
  type V3Client,
} from "../src/v3.js";

const e18 = 10n ** 18n;

test("weight: bias decays by slope per second, never below zero, permanent stake stays", () => {
  const p = { bias: 1000n * e18, slope: e18, ts: 100, permanentStakeBalance: 50n * e18 };
  assert.equal(gaugeWeightAt(p, 100), 1050n * e18);
  assert.equal(gaugeWeightAt(p, 600), 550n * e18);
  assert.equal(gaugeWeightAt(p, 5000), 50n * e18);
});

test("incentives: only programs running now stream, rates of the same token add up", () => {
  const prog = (token: string, perSec: bigint, start: number, end: number) => ({
    token: token as `0x${string}`, amount: 0n, rate: perSec * V3_PRECISION, start, end,
  });
  const r = incentiveRatesNow([prog("0xA", 2n, 0, 1000), prog("0xa", 3n, 50, 200), prog("0xb", 9n, 500, 900), prog("0xc", 7n, 0, 100)], 100);
  assert.deepEqual([...r.entries()], [["0xa", 5]]);
});

test("yield: fees averaged over the window plus incentives at the current rate, per 10k of weight", () => {
  const price = (t: string) => (t === "0xusdc" ? { decimals: 6, priceUsd: 1 } : undefined);
  const y = v3GaugeYield({
    feesCollected: [{ token: "0xUSDC", amount: 96_000_000n }], // $96 over 96 h -> $24/day
    windowHours: 96,
    incentiveRates: new Map([["0xusdc", 1_000_000 / 86_400]]), // $1/day
    weight: 100_000n * e18,
    priceOf: price,
  });
  assert.equal(y.feesUsdPerDay, 24);
  assert.ok(Math.abs(y.incentivesUsdPerDay - 1) < 1e-9);
  assert.ok(Math.abs((y.usdPerDayPer10k ?? 0) - 2.5) < 1e-9);
  assert.equal(y.partial, false);
});

test("yield: an unpriced earned token is flagged rather than silently dropped; zero weight has no per-10k figure", () => {
  const y = v3GaugeYield({ feesCollected: [{ token: "0xNOPE", amount: 5n }], windowHours: 24, incentiveRates: new Map(), weight: 0n, priceOf: () => undefined });
  assert.equal(y.partial, true);
  assert.equal(y.usdPerDayPer10k, null);
});

const fake = (answers: Record<string, unknown>, logs: unknown[] = []): V3Client & { ranges: [bigint, bigint][] } => {
  const ranges: [bigint, bigint][] = [];
  return {
    ranges,
    async readContract({ address, functionName, args }) {
      const key = [address, functionName, ...(args ?? []).map((a) => (Array.isArray(a) ? a.join(",") : String(a)))].join("|");
      if (!(key in answers)) throw new Error(`unexpected call ${key}`);
      return answers[key];
    },
    async getLogs({ fromBlock, toBlock }) {
      ranges.push([fromBlock, toBlock]);
      return logs as never;
    },
  };
};

test("gauges: walked from the registry, empty before launch", async () => {
  const before = fake({ "0xR|leafVoter": "0x0", "0xR|gaugeFactories": [] });
  assert.deepEqual(await readV3Gauges(before, "0xR"), { leafVoter: "0x0", gauges: [] });
  const after = fake({
    "0xR|leafVoter": "0xV",
    "0xR|gaugeFactories": ["0xF"],
    "0xR|factoryToGauges|0xF": ["0xG"],
    "0xR|gaugeToRewards|0xG": "0xM",
    "0xR|gaugeToTarget|0xG": "0xP",
  });
  assert.deepEqual(await readV3Gauges(after, "0xR"), { leafVoter: "0xV", gauges: [{ gauge: "0xG", pool: "0xP", rewards: "0xM" }] });
});

test("programs: ids start at 1, none means no call for the list", async () => {
  assert.deepEqual(await readIncentivePrograms(fake({ "0xM|incentiveCount": 0n }), "0xM"), []);
  const c = fake({
    "0xM|incentiveCount": 2n,
    "0xM|incentives|1,2": [
      { token: "0xT", amount: 10n, rate: 1n, start: 5, end: 9 },
      { token: "0xU", amount: 20n, rate: 2n, start: 6, end: 10 },
    ],
  });
  assert.deepEqual((await readIncentivePrograms(c, "0xM")).map((p) => p.token), ["0xT", "0xU"]);
});

test("FeesCollected: range split into chunks, incomplete logs skipped", async () => {
  const c = fake({}, [
    { address: "0xM", args: { _gauge: "0xG", _token: "0xT", _amount: 7n } },
    { address: "0xM", args: { _gauge: "0xG" } },
  ]);
  const out = await readFeesCollected(c, ["0xM"], 0n, 24_999n);
  assert.deepEqual(c.ranges, [[0n, 9_999n], [10_000n, 19_999n], [20_000n, 24_999n]]);
  assert.equal(out.length, 3);
  assert.deepEqual(out[0], { rewards: "0xM", gauge: "0xG", token: "0xT", amount: 7n });
  assert.deepEqual(await readFeesCollected(c, [], 0n, 10n), []);
});

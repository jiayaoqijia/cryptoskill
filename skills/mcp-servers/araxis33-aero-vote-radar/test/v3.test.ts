import { test } from "node:test";
import assert from "node:assert/strict";
import {
  gaugeWeightAt,
  incentiveRatesNow,
  readFeesCollected,
  readGaugePoint,
  readIncentivePrograms,
  readPoolMeta,
  readV3Gauges,
  v3GaugeYield,
  V3_PRECISION,
  AERO_LAUNCH_TS,
  registryFromDeployment,
  scanV3,
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

test("pool meta: a Slipstream pool's kind is CL<tickSpacing>; token symbols are cached across pools", async () => {
  const symbols = new Map<string, string>();
  const c = fake({
    "0xPool1|token0": "0xTokenA",
    "0xPool1|token1": "0xTokenB",
    "0xPool1|tickSpacing": 100,
    "0xTokenA|symbol": "WETH",
    "0xTokenB|symbol": "USDC",
    "0xPool2|token0": "0xTokenA",
    "0xPool2|token1": "0xTokenC",
    "0xPool2|tickSpacing": 50,
    "0xTokenC|symbol": "AERO",
  });
  let tokenACalls = 0;
  const counting: V3Client = {
    ...c,
    readContract: async (args) => {
      if (args.address === "0xTokenA" && args.functionName === "symbol") tokenACalls++;
      return c.readContract(args);
    },
  };
  assert.deepEqual(await readPoolMeta(counting, "0xPool1", symbols), { symbol0: "WETH", symbol1: "USDC", kind: "CL100" });
  assert.deepEqual(await readPoolMeta(counting, "0xPool2", symbols), { symbol0: "WETH", symbol1: "AERO", kind: "CL50" });
  assert.equal(tokenACalls, 1, "a token symbol already seen must not be read again");
});

test("pool meta: basic pools with no tickSpacing() fall back to symbol() to tell sAMM from vAMM", async () => {
  const symbols = new Map<string, string>();
  const c = fake({
    "0xPoolS|token0": "0xTokenA",
    "0xPoolS|token1": "0xTokenB",
    "0xPoolS|symbol": "sAMM-USDC/USDT",
    "0xTokenA|symbol": "USDC",
    "0xTokenB|symbol": "USDT",
    "0xPoolV|token0": "0xTokenA",
    "0xPoolV|token1": "0xTokenC",
    "0xPoolV|symbol": "vAMMV2-AERO/WETH",
    "0xTokenC|symbol": "AERO",
  });
  assert.equal((await readPoolMeta(c, "0xPoolS", symbols))?.kind, "sAMM");
  assert.equal((await readPoolMeta(c, "0xPoolV", symbols))?.kind, "vAMM");
});

test("pool meta: a token symbol that fails to read is \"?\" rather than failing the whole pool; a pool that answers like neither kind is undefined", async () => {
  const symbols = new Map<string, string>();
  const c = fake({
    "0xPool|token0": "0xTokenX",
    "0xPool|token1": "0xTokenY",
    "0xPool|symbol": "vAMM-X/Y",
    "0xTokenY|symbol": "Y",
    // 0xTokenX's symbol() is missing from the answers, so it throws like an unreadable token.
  });
  assert.deepEqual(await readPoolMeta(c, "0xPool", symbols), { symbol0: "?", symbol1: "Y", kind: "vAMM" });

  const bad = fake({ "0xBad|token1": "0xTokenB" }); // token0() missing -> throws
  assert.equal(await readPoolMeta(bad, "0xBad", new Map()), undefined);
});

test("gauge point: pulled out of the Point struct at the end of gaugeStates' nine-field return", async () => {
  const point = { bias: 500n * e18, slope: 2n * e18, ts: 42, permanentStakeBalance: 10n * e18 };
  // gaugeStates returns (ceiling, claimed, lastSettlement, isRegistered, isActivated,
  // surplus, lastIndex, lastTimeIndex, point) — point is the 9th field (index 8), and
  // readGaugePoint has to pull it out from behind the eight it doesn't use.
  const c = fake({
    "0xV|gaugeStates|0xG": [0n, 0n, 0, true, true, 0n, 0n, 0n, point],
  });
  assert.deepEqual(await readGaugePoint(c, "0xV", "0xG"), point);
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

test("FeesCollected: a refused call is split, range first, then addresses; every log arrives once", async () => {
  const calls: [number, bigint, bigint][] = [];
  const c = {
    readContract: async () => { throw new Error("unused"); },
    // refuses more than 100 blocks, and more than one address below that
    getLogs: async (a: { address: string | string[]; fromBlock: bigint; toBlock: bigint }) => {
      const addrs = [a.address].flat();
      calls.push([addrs.length, a.fromBlock, a.toBlock]);
      if (a.toBlock - a.fromBlock + 1n > 100n || addrs.length > 1) throw new Error("HTTP 403");
      return a.fromBlock === 0n ? [{ address: addrs[0], args: { _gauge: "0xG" + addrs[0], _token: "0xT", _amount: 1n } }] : [];
    },
  } as unknown as V3Client;
  const out = await readFeesCollected(c, ["0xA", "0xB"], 0n, 199n, 200n);
  assert.deepEqual(out.map((x) => x.gauge).sort(), ["0xG0xA", "0xG0xB"]);
  // never asked for one block with a single address more than once
  const single = calls.filter(([n]) => n === 1).map(([, f, t]) => `${f}-${t}`);
  assert.equal(new Set(single).size, single.length / 2);
});

test("FeesCollected: a call refused even at the smallest size is an error", async () => {
  const c = { readContract: async () => 0, getLogs: async () => { throw new Error("HTTP 403"); } } as unknown as V3Client;
  await assert.rejects(readFeesCollected(c, ["0xA"], 0n, 10n), /403/);
});

test("deployment file: factoryRegistry found by name, any case; absent or malformed is undefined", () => {
  assert.equal(registryFromDeployment({ factoryRegistry: "0xCe44907DC45D3BFa3f5f6035B0e6E8B22D780A42", metarouter: "0x1" }), "0xCe44907DC45D3BFa3f5f6035B0e6E8B22D780A42");
  assert.equal(registryFromDeployment({ FactoryRegistry: "0x" + "a".repeat(40) }), "0x" + "a".repeat(40));
  assert.equal(registryFromDeployment({ factoryRegistry: "0x123" }), undefined);
  assert.equal(registryFromDeployment({ voter: "0x" + "b".repeat(40) }), undefined);
});

test("scan: a registry with no voter yet is not live and reads nothing else", async () => {
  const c = Object.assign(fake({ "0xR|leafVoter": "0x0000000000000000000000000000000000000000", "0xR|gaugeFactories": [] }), {
    getBlockNumber: async () => { throw new Error("must not be called"); },
  });
  const r = await scanV3(c, "0xR", { chain: "base", now: new Date(AERO_LAUNCH_TS * 1000 + 3600_000), priceOf: async () => () => undefined });
  assert.equal(r.status, "not-live");
  assert.deepEqual(r.gauges, []);
});

test("scan: fee window cut at launch, gauges ranked by per-10k, fees matched to their gauge", async () => {
  const now = new Date((AERO_LAUNCH_TS + 24 * 3600) * 1000); // one day after launch
  const nowSec = AERO_LAUNCH_TS + 24 * 3600;
  const point = (w: bigint) => [0n, 0n, 0, true, true, 0n, 0n, 0n, { bias: 0n, slope: 0n, ts: nowSec, permanentStakeBalance: w * e18 }];
  const c = Object.assign(
    fake(
      {
        "0xR|leafVoter": "0xV",
        "0xR|gaugeFactories": ["0xF"],
        "0xR|factoryToGauges|0xF": ["0xG1", "0xG2"],
        "0xR|gaugeToRewards|0xG1": "0xM1",
        "0xR|gaugeToTarget|0xG1": "0xP1",
        "0xR|gaugeToRewards|0xG2": "0xM2",
        "0xR|gaugeToTarget|0xG2": "0xP2",
        "0xV|gaugeStates|0xG1": point(100_000n),
        "0xV|gaugeStates|0xG2": point(10_000n),
        "0xM1|incentiveCount": 0n,
        "0xM2|incentiveCount": 0n,
      },
      [
        { address: "0xM1", args: { _gauge: "0xG1", _token: "0xUSDC", _amount: 100_000_000n } }, // $100 in a day
        { address: "0xM2", args: { _gauge: "0xG2", _token: "0xUSDC", _amount: 20_000_000n } }, // $20 in a day
      ],
    ),
    { getBlockNumber: async () => 1_000_000n },
  );
  // the fake answers every getLogs call with the same logs; hand them out on the first chunk only
  const getLogs = c.getLogs.bind(c);
  c.getLogs = async (a) => { const l = await getLogs(a); return c.ranges.length === 1 ? l : []; };
  const r = await scanV3(c, "0xR", {
    chain: "base",
    now,
    priceOf: async () => (t) => (t === "0xusdc" ? { decimals: 6, priceUsd: 1 } : undefined),
  });
  assert.equal(r.status, "live");
  assert.equal(r.windowHours, 24);
  // 24 h of 2 s blocks back from block 1,000,000, in one 100-address chunk
  assert.equal(c.ranges[0][0], 1_000_000n - 43_200n);
  assert.deepEqual(r.gauges.map((g) => g.gauge), ["0xG2", "0xG1"]); // $20 over 10k beats $100 over 100k
  assert.ok(Math.abs((r.gauges[0].usdPerDayPer10k ?? 0) - 20) < 1e-9);
  assert.ok(Math.abs((r.gauges[1].usdPerDayPer10k ?? 0) - 10) < 1e-9);
  assert.equal(r.gauges[1].weight, 100_000);
});

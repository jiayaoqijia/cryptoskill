import { test } from "node:test";
import assert from "node:assert/strict";
import { LLMS_EXAMPLE_VEAERO, LLMS_MIN_CONSISTENCY, LLMS_VOTE_BASIS, renderLlmsTxt } from "../src/llms.js";
import type { PoolEfficiency } from "../src/efficiency.js";

function ranked(address: string, symbol: string, overrides: Partial<PoolEfficiency> = {}): PoolEfficiency {
  return {
    pool: { address, symbol, token0: "0xt0", token1: "0xt1", gauge: "0xg", gaugeAlive: true },
    latestEpochTs: 1_000,
    currentVotesVeAero: 50_000,
    latestEpochUsd: 100,
    trailingAvgUsd: 120,
    epochsObserved: 6,
    epochUsdSeries: [100, 110, 120, 130, 120, 140],
    epochVotesSeries: [50_000, 50_000, 50_000, 50_000, 50_000, 50_000],
    currentValuePerVote: 0.002,
    predictedValuePerVote: 0.0024,
    predictiveEdge: 0.2,
    volatility: 0.5,
    consistency: 2 / 3,
    latestEpochBribes: [],
    latestEpochFees: [],
    ...overrides,
  };
}

const AT = new Date("2026-09-25T10:00:00Z");
const ENDS = Date.parse("2026-10-01T00:00:00Z") / 1000;

test("llms.txt carries this week's suggestion as whole percentages summing to 100, with its deadline", () => {
  const txt = renderLlmsTxt(
    [ranked("0xaaa", "vAMM-A/USDC", { trailingAvgUsd: 900 }), ranked("0xbbb", "CL-B/WETH", { trailingAvgUsd: 600 })],
    AT,
    ENDS,
  );
  const percents = [...txt.matchAll(/^- (\d+)% /gm)].map((m) => Number(m[1]));
  assert.ok(percents.length > 0, "no allocation lines");
  assert.equal(percents.reduce((a, b) => a + b, 0), 100);
  assert.match(txt, /Current epoch closes: 2026-10-01 00:00 UTC/);
  assert.match(txt, new RegExp(`suggestion for ${LLMS_EXAMPLE_VEAERO.toLocaleString("en-US")} veAERO`));
  assert.match(txt, /Scanned from Base mainnet: 2026-09-25T10:00:00.000Z/);
});

test("llms.txt never suggests a pool Aerodrome is migrating, and says how many it left out", () => {
  const txt = renderLlmsTxt(
    [
      ranked("0xmig", "CL-OLD/USDC", { trailingAvgUsd: 99_999, pool: { address: "0xmig", symbol: "CL-OLD/USDC", token0: "0xt0", token1: "0xt1", gauge: "0xg", gaugeAlive: true, migrating: true } }),
      ranked("0xok", "vAMM-OK/USDC"),
    ],
    AT,
    ENDS,
  );
  assert.doesNotMatch(txt, /0xmig/);
  assert.match(txt, /0xok/);
  assert.match(txt, /Left out: 1 pool\(s\) Aerodrome marks "Migrating"/);
});

test("llms.txt drops a spiky pool the page's consistency filter drops, instead of going all-in on it", () => {
  // The 2026-09-25 case: a pool whose weight fell to a twentieth of its usual
  // for one week looks like free money on last week's weight alone.
  const txt = renderLlmsTxt(
    [
      ranked("0xspiky", "vAMM-SPIKY/X", { trailingAvgUsd: 50_000, consistency: 0.49 }),
      ranked("0xsteady", "vAMM-STEADY/USDC", { consistency: 0.8 }),
    ],
    AT,
    ENDS,
  );
  assert.doesNotMatch(txt, /0xspiky/);
  assert.match(txt, /0xsteady/);
});

test("llms.txt uses the same defaults the hosted page opens on", async () => {
  const { readFile } = await import("node:fs/promises");
  const html = await readFile(new URL("../docs/index.html", import.meta.url), "utf8");
  const selected = (id: string) =>
    html.match(new RegExp(`<select id="${id}">[\\s\\S]*?<option value="([^"]+)" selected>`))?.[1];
  assert.equal(Number(selected("mincons")), LLMS_MIN_CONSISTENCY);
  assert.equal(selected("votebasis"), LLMS_VOTE_BASIS);
  assert.equal(Number(html.match(/<input id="veaero"[^>]*value="(\d+)"/)?.[1]), LLMS_EXAMPLE_VEAERO);
});

test("llms.txt says so plainly when nothing qualified instead of printing an empty list", () => {
  const txt = renderLlmsTxt([ranked("0xdead", "vAMM-DEAD/USDC", { trailingAvgUsd: 0 })], AT, ENDS);
  assert.match(txt, /No pool qualified in this scan/);
  assert.doesNotMatch(txt, /^- \d+% /m);
});

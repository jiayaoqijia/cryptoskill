import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
import {
  allocateAcrossCandidates,
  toWholePercentWeights,
  expectedUsdForWholePercentVote,
  voteBasisCaveat,
  type AllocationCandidate,
  type VoteBasis,
} from "../src/allocator.js";
import { epochEndOf, formatDuration } from "../src/trend.js";
import { expectedDilutedVotes, previousSettledVotes } from "../src/dilution.js";
import { VOTE_BASIS_CROSSOVER_VEAERO, VOTER_ADDRESS } from "../src/constants.js";
import { buildVoteCalldata } from "../src/calldata.js";
import type { WholePercentWeight } from "../src/allocator.js";

/**
 * The static site cannot import the TypeScript allocator: `docs/` is served by
 * GitHub Pages with no build step, and the whole point of the snapshot design is
 * that the page re-runs the allocation per keystroke in the browser. So
 * `docs/index.html` carries a hand-port of `src/allocator.ts`, labelled as one.
 *
 * A copy nothing checks is a copy that drifts, and the drift is silent: a fix
 * landed in the TypeScript (the V = 0 branch below is exactly such a fix) leaves
 * the page quietly recommending something else, with 100+ passing tests all
 * still green. This suite closes that gap by running the page's own source
 * against the real implementation on the same inputs.
 */

const here = dirname(fileURLToPath(import.meta.url));
const siteSource = readFileSync(resolve(here, "../docs/index.html"), "utf8");

/**
 * Pulls one `function name(...) { ... }` declaration out of the page by matching
 * braces from its opening one. A regex can't do this safely — the bodies contain
 * braces in object literals and template strings — and depth-counting from a
 * known start is both simple and exact for source this shape.
 */
function extractFunction(source: string, name: string): string {
  const start = source.indexOf(`function ${name}(`);
  assert.notEqual(start, -1, `docs/index.html no longer defines ${name}() — did the page stop porting the allocator?`);

  let depth = 0;
  let seenBrace = false;
  for (let i = start; i < source.length; i++) {
    if (source[i] === "{") {
      depth++;
      seenBrace = true;
    } else if (source[i] === "}") {
      depth--;
      if (seenBrace && depth === 0) return source.slice(start, i + 1);
    }
  }
  throw new Error(`unbalanced braces while extracting ${name}() from docs/index.html`);
}

type SiteAllocate = (input: unknown[], budget: number, steps?: number, maxWeight?: number) => { pool: string; symbol: string; weight: number; veAeroAllocated: number; expectedUsd: number }[];
type SitePercents = (allocation: unknown[]) => Map<string, number>;
type SiteExpected = (allocation: unknown[], budget: number) => number;

// `extractConst` is declared further down, next to the epoch-countdown port
// that first needed it; function declarations hoist, and keeping one copy is
// worth more than declaring it twice in reading order.
const siteModule = new Function(`
  ${extractFunction(siteSource, "marginalValuePerVeAero")}
  ${extractFunction(siteSource, "allocateAcrossCandidates")}
  ${extractFunction(siteSource, "toWholePercentWeights")}
  ${extractFunction(siteSource, "expectedUsdForWholePercentVote")}
  ${extractFunction(siteSource, "votesToExpect")}
  ${extractFunction(siteSource, "typicalVotes")}
  ${extractFunction(siteSource, "votesForBasis")}
  ${extractConst(siteSource, "VOTE_BASIS_CROSSOVER_VEAERO")}
  ${extractFunction(siteSource, "voteBasisCaveat")}
  return { allocateAcrossCandidates, toWholePercentWeights, expectedUsdForWholePercentVote, votesToExpect, typicalVotes, votesForBasis, voteBasisCaveat, VOTE_BASIS_CROSSOVER_VEAERO };
`)() as {
  allocateAcrossCandidates: SiteAllocate;
  toWholePercentWeights: SitePercents;
  expectedUsdForWholePercentVote: SiteExpected;
  votesToExpect: (pool: { votesVeAero: number; epochVotes?: number[]; currentEpochPartial?: boolean }) => number;
  typicalVotes: (pool: { votesVeAero: number; expectedVotes?: number | null }) => number;
  votesForBasis: (
    pool: { votesVeAero: number; expectedVotes?: number | null; epochVotes?: number[]; currentEpochPartial?: boolean },
    basis: string,
  ) => number;
  voteBasisCaveat: (veAeroBudget: number, voteBasis: string) => string | null;
  VOTE_BASIS_CROSSOVER_VEAERO: number;
};

/** Candidate sets chosen to exercise the branches the two copies could disagree on. */
const cases: { name: string; candidates: AllocationCandidate[]; budget: number }[] = [
  {
    name: "two identical pools, budget large enough to force diversification",
    candidates: [
      { address: "0xA", symbol: "A", existingVotes: 1000, expectedUsd: 100 },
      { address: "0xB", symbol: "B", existingVotes: 1000, expectedUsd: 100 },
    ],
    budget: 10_000,
  },
  {
    name: "a pool nobody else has voted on, alongside a crowded one",
    candidates: [
      { address: "0xEMPTY", symbol: "EMPTY", existingVotes: 0, expectedUsd: 500 },
      { address: "0xCROWDED", symbol: "CROWDED", existingVotes: 1_000_000, expectedUsd: 100 },
    ],
    budget: 1000,
  },
  {
    name: "a worthless pool that must never be funded",
    candidates: [
      { address: "0xDEAD", symbol: "DEAD", existingVotes: 500, expectedUsd: 0 },
      { address: "0xLIVE", symbol: "LIVE", existingVotes: 500, expectedUsd: 250 },
    ],
    budget: 5000,
  },
  {
    name: "many pools on wildly different scales, so sub-1% rows appear",
    candidates: Array.from({ length: 15 }, (_, i) => ({
      address: `0x${i}`,
      symbol: `P${i}`,
      existingVotes: 10 ** (1 + (i % 5)),
      expectedUsd: 50 * (i + 1),
    })),
    budget: 1_000_000,
  },
];

for (const { name, candidates, budget } of cases) {
  test(`docs/index.html allocates identically to src/allocator.ts: ${name}`, () => {
    const ours = allocateAcrossCandidates(candidates, budget);
    const theirs = siteModule.allocateAcrossCandidates(candidates, budget);

    assert.equal(theirs.length, ours.length, "different number of funded pools");
    for (let i = 0; i < ours.length; i++) {
      assert.equal(theirs[i].pool, ours[i].pool, `row ${i}: different pool`);
      assert.ok(
        Math.abs(theirs[i].veAeroAllocated - ours[i].veAeroAllocated) < 1e-9,
        `row ${i} (${ours[i].symbol}): veAERO ${theirs[i].veAeroAllocated} vs ${ours[i].veAeroAllocated}`,
      );
      assert.ok(
        Math.abs(theirs[i].expectedUsd - ours[i].expectedUsd) < 1e-9,
        `row ${i} (${ours[i].symbol}): expected $ ${theirs[i].expectedUsd} vs ${ours[i].expectedUsd}`,
      );
    }
  });

  test(`docs/index.html rounds to the same whole percentages: ${name}`, () => {
    const ours = allocateAcrossCandidates(candidates, budget);
    const theirs = siteModule.allocateAcrossCandidates(candidates, budget);

    // The page returns a Map keyed by pool and leaves 0% rows in for its caller
    // to drop; the module returns an array with them already removed. Compare
    // the votable rows, which is what a user actually types into Aerodrome.
    const oursPercents = new Map(toWholePercentWeights(ours).map((p) => [p.pool, p.percent]));
    const theirsPercents = new Map(
      [...siteModule.toWholePercentWeights(theirs)].filter(([, percent]) => percent > 0),
    );

    assert.deepEqual(theirsPercents, oursPercents);
  });
}

for (const { name, candidates, budget } of cases) {
  test(`docs/index.html quotes the same expected $ for the cast vote: ${name}`, () => {
    const ours = expectedUsdForWholePercentVote(allocateAcrossCandidates(candidates, budget), budget);
    const theirs = siteModule.expectedUsdForWholePercentVote(
      siteModule.allocateAcrossCandidates(candidates, budget),
      budget,
    );
    assert.ok(Math.abs(theirs - ours) < 1e-9, `site says $${theirs}, module says $${ours}`);
  });
}

/**
 * The cap is the newest thing both copies have to agree on, and the one most
 * likely to drift: it is enforced inside the greedy loop, not applied to the
 * result afterwards, so a port that skips a single line reads as "cap ignored"
 * rather than as a crash.
 */
for (const cap of [0.5, 0.34, 0.25, 0.2]) {
  test(`docs/index.html honours a ${Math.round(cap * 100)}% cap the same way src/allocator.ts does`, () => {
    const candidates: AllocationCandidate[] = Array.from({ length: 8 }, (_, i) => ({
      address: `0x${i}`,
      symbol: `P${i}`,
      existingVotes: 200 * (i + 1),
      expectedUsd: 800 - i * 40,
    }));
    const budget = 120_000;

    const ours = allocateAcrossCandidates(candidates, budget, undefined, cap);
    const theirs = siteModule.allocateAcrossCandidates(candidates, budget, undefined, cap);

    assert.equal(theirs.length, ours.length, "different number of funded pools under the cap");
    for (let i = 0; i < ours.length; i++) {
      assert.equal(theirs[i].pool, ours[i].pool, `row ${i}: different pool`);
      assert.ok(
        Math.abs(theirs[i].veAeroAllocated - ours[i].veAeroAllocated) < 1e-9,
        `row ${i} (${ours[i].symbol}): veAERO ${theirs[i].veAeroAllocated} vs ${ours[i].veAeroAllocated}`,
      );
      assert.ok(ours[i].weight <= cap + 1e-9, `${ours[i].symbol} breached the cap in src/`);
      assert.ok(theirs[i].weight <= cap + 1e-9, `${ours[i].symbol} breached the cap on the page`);
    }
  });
}

// The allocator isn't the only hand-port on the page: the vote-deadline
// countdown (`epochEndOf`/`formatDuration`, right by the code comment "matching
// epochEndOf/formatDuration in src/trend.ts") is copied the same way, for the
// same reason — `docs/` has no build step, so it cannot import `src/trend.ts`
// directly. Nothing checked that copy against the real one, which is exactly
// the silent-drift risk this file's docstring already describes for the
// allocator: a fix landed in `trend.ts` (say, a rounding correction to
// `formatDuration`) would leave the page quietly showing a different countdown
// to the one thing on this page that must never be stale, with every other
// test still green.

/**
 * `epochEndOf` on the page closes over the page's own `const EPOCH_SECONDS`
 * rather than taking it as a parameter, so extracting the function alone
 * leaves it referencing a name that doesn't exist in the sandboxed `Function`
 * scope. Pulled out the same brace/line-matching way as `extractFunction`,
 * rather than hardcoded here, so a changed value on the page is what this
 * test actually exercises.
 */
function extractConst(source: string, name: string): string {
  const match = source.match(new RegExp(`const ${name} = [^;]+;`));
  assert.notEqual(match, null, `docs/index.html no longer declares const ${name}`);
  return match![0];
}

const siteEpochModule = new Function(`
  ${extractConst(siteSource, "EPOCH_SECONDS")}
  ${extractFunction(siteSource, "epochEndOf")}
  ${extractFunction(siteSource, "formatDuration")}
  return { epochEndOf, formatDuration };
`)() as {
  epochEndOf: (unixSeconds: number) => number;
  formatDuration: (seconds: number) => string;
};

test("docs/index.html's epochEndOf matches src/trend.ts across a range of timestamps", () => {
  const samples = [
    0,
    1, // one second into the Unix epoch, itself a Thursday
    1_786_579_200, // a real Thursday 00:00 UTC boundary
    1_786_579_200 - 1, // the second before a boundary
    1_786_579_200 + 1, // the second after a boundary
    1_756_195_200, // an arbitrary "now" mid-epoch
  ];
  for (const s of samples) {
    assert.equal(siteEpochModule.epochEndOf(s), epochEndOf(s), `epochEndOf(${s})`);
  }
});

test("docs/index.html's formatDuration matches src/trend.ts across a range of durations", () => {
  const samples = [-100, 0, 1, 59, 60, 61, 3599, 3600, 3660, 86_399, 86_400, 86_400 * 2 + 3661, NaN, Infinity];
  for (const s of samples) {
    assert.equal(siteEpochModule.formatDuration(s), formatDuration(s), `formatDuration(${s})`);
  }
});

/**
 * The page picks the allocator's denominator itself, so `votesToExpect` is a
 * second hand-port sitting on the same drift risk as the allocator. It decides
 * which pools the suggestion funds, so a copy that quietly disagreed with
 * `previousSettledVotes` would change real vote weights.
 */
test("docs/index.html's votesToExpect matches src/dilution.ts", () => {
  const cases: { votesVeAero: number; epochVotes?: number[]; currentEpochPartial?: boolean }[] = [
    // Mid-week: entry 0 is the running tally, so last epoch's weight is entry 1.
    { votesVeAero: 452_000, epochVotes: [452_000, 11_600_000, 9_000_000], currentEpochPartial: true },
    { votesVeAero: 9_000, epochVotes: [9_000, 3_000, 3_000], currentEpochPartial: true },
    // A settled series: entry 0 already is the previous epoch.
    { votesVeAero: 5_000, epochVotes: [7_000, 6_000], currentEpochPartial: false },
    // Nothing to read: fall back to what the pool actually carries.
    { votesVeAero: 1_234, epochVotes: [1_234], currentEpochPartial: true },
    { votesVeAero: 1_234, epochVotes: [1_234, 0], currentEpochPartial: true },
    { votesVeAero: 1_234 },
    { votesVeAero: 0, epochVotes: [0, 4_000], currentEpochPartial: true },
  ];

  for (const c of cases) {
    assert.equal(
      siteModule.votesToExpect(c),
      previousSettledVotes(c.epochVotes ?? [], c.currentEpochPartial ?? true, c.votesVeAero),
      `votesToExpect disagreed for ${JSON.stringify(c)}`,
    );
  }
});

/**
 * The caveat is the one place where the page tells a visitor that the number
 * above it rests on a basis the evidence does not support at their size. If the
 * two copies drifted, the page could go on reassuring a voter the CLI would
 * warn — the worst direction for a disagreement to run.
 */
test("docs/index.html's vote-basis crossover is the same number as src/constants.ts", () => {
  assert.equal(siteModule.VOTE_BASIS_CROSSOVER_VEAERO, VOTE_BASIS_CROSSOVER_VEAERO);
});

test("docs/index.html's voteBasisCaveat matches src/allocator.ts word for word", () => {
  const budgets = [
    1,
    25_000,
    VOTE_BASIS_CROSSOVER_VEAERO - 1,
    VOTE_BASIS_CROSSOVER_VEAERO,
    VOTE_BASIS_CROSSOVER_VEAERO + 1,
    5_000_000,
    0,
    -1,
    Number.NaN,
  ];
  const bases: VoteBasis[] = ["previous", "current", "typical"];

  for (const budget of budgets) {
    for (const basis of bases) {
      assert.equal(
        siteModule.voteBasisCaveat(budget, basis),
        voteBasisCaveat(budget, basis),
        `voteBasisCaveat disagreed at ${budget} veAERO on "${basis}"`,
      );
    }
  }
});

/**
 * The calldata builder is the one hand-port whose output someone signs. A page
 * that encoded a different pool order, a wrong offset or another contract than
 * the tested implementation would produce a transaction that looks right in the
 * table above it and votes for something else — so it is held to viem's own
 * encoding, not to a fixture written by the same hand that wrote the port.
 */
const siteCalldata = new Function(`
  ${extractConst(siteSource, "VOTER_ADDRESS")}
  ${extractConst(siteSource, "VOTE_SELECTOR")}
  ${extractFunction(siteSource, "voteCalldata")}
  ${extractConst(siteSource, "CALLDATA_SELF_TEST")}
  ${extractFunction(siteSource, "calldataEncoderIsSound")}
  return { voteCalldata, calldataEncoderIsSound, VOTER_ADDRESS, VOTE_SELECTOR, CALLDATA_SELF_TEST };
`)() as {
  voteCalldata: (tokenId: string, rows: WholePercentWeight[]) => string;
  calldataEncoderIsSound: () => boolean;
  VOTER_ADDRESS: string;
  VOTE_SELECTOR: string;
  CALLDATA_SELF_TEST: { tokenId: string; rows: WholePercentWeight[]; expected: string };
};

const weight = (i: number, percent: number): WholePercentWeight => ({
  pool: `0x${String(i).padStart(40, "0")}`,
  symbol: `P${i}`,
  percent,
});

test("docs/index.html encodes the same vote bytes as src/calldata.ts", () => {
  const cases: { name: string; tokenId: string; rows: WholePercentWeight[] }[] = [
    { name: "everything in one pool", tokenId: "1", rows: [weight(1, 100)] },
    { name: "two pools", tokenId: "118577", rows: [weight(1, 60), weight(2, 40)] },
    {
      name: "a spread across seven pools, the shape the allocation usually takes",
      tokenId: "999999999999999999999",
      rows: [weight(1, 30), weight(2, 25), weight(3, 15), weight(4, 12), weight(5, 8), weight(6, 6), weight(7, 4)],
    },
    {
      name: "a hundred one-percent rows, so the array offsets are exercised",
      tokenId: "42",
      rows: Array.from({ length: 100 }, (_, i) => weight(i + 1, 1)),
    },
  ];

  for (const { name, tokenId, rows } of cases) {
    assert.equal(siteCalldata.voteCalldata(tokenId, rows), buildVoteCalldata(tokenId, rows).data, `disagreed on: ${name}`);
  }
});

test("docs/index.html points the vote at the same contract, with the same selector", () => {
  assert.equal(siteCalldata.VOTER_ADDRESS, VOTER_ADDRESS);
  assert.equal(siteCalldata.VOTE_SELECTOR, buildVoteCalldata("1", [weight(1, 100)]).data.slice(0, 10));
});

test("docs/index.html's calldata self-test vector is the one viem produces", () => {
  const { tokenId, rows, expected } = siteCalldata.CALLDATA_SELF_TEST;
  assert.equal(expected, buildVoteCalldata(tokenId, rows).data);
  assert.equal(siteCalldata.calldataEncoderIsSound(), true);
});

test("docs/index.html refuses the same malformed allocations src/calldata.ts refuses", () => {
  const bad: { name: string; tokenId: string; rows: WholePercentWeight[] }[] = [
    { name: "no rows", tokenId: "1", rows: [] },
    { name: "weights that do not total 100", tokenId: "1", rows: [weight(1, 60), weight(2, 30)] },
    { name: "the same pool twice", tokenId: "1", rows: [weight(1, 50), weight(1, 50)] },
    { name: "a zero weight", tokenId: "1", rows: [weight(1, 100), weight(2, 0)] },
    { name: "a fractional weight", tokenId: "1", rows: [weight(1, 99.5), weight(2, 0.5)] },
    { name: "a token id that is not a number", tokenId: "118577n", rows: [weight(1, 100)] },
    { name: "a zero token id", tokenId: "0", rows: [weight(1, 100)] },
    { name: "an empty token id", tokenId: "", rows: [weight(1, 100)] },
  ];

  for (const { name, tokenId, rows } of bad) {
    assert.throws(() => siteCalldata.voteCalldata(tokenId, rows), `the page accepted ${name}`);
    assert.throws(() => buildVoteCalldata(tokenId, rows), `src/calldata.ts accepted ${name}`);
  }
});

/**
 * The third vote basis reached the page after the first two, and it is the one
 * a visitor picks *because* the caveat pointed them at it — so a page copy that
 * computed it differently from src/dilution.ts would quietly answer a question
 * the tool had just told them to ask.
 */
test("docs/index.html's typicalVotes matches src/dilution.ts", () => {
  const cases: { votesVeAero: number; expectedVotes?: number | null }[] = [
    { votesVeAero: 1_208_915, expectedVotes: 13_423_457 }, // a pool whose weight has drained away
    { votesVeAero: 13_423_457, expectedVotes: 1_208_915 }, // and the same pool, refilled past its usual level
    { votesVeAero: 5_000, expectedVotes: 5_000 },
    { votesVeAero: 5_000, expectedVotes: null },
    { votesVeAero: 5_000 },
    { votesVeAero: 0, expectedVotes: 900 },
    { votesVeAero: 900, expectedVotes: Number.NaN },
  ];

  for (const c of cases) {
    assert.equal(
      siteModule.typicalVotes(c),
      expectedDilutedVotes(c.votesVeAero, c.expectedVotes ?? null),
      `typicalVotes disagreed for ${JSON.stringify(c)}`,
    );
  }
});

test("docs/index.html routes each vote basis to the weight src/ would use", () => {
  const pool = {
    votesVeAero: 1_208_915,
    expectedVotes: 13_423_457,
    epochVotes: [1_208_915, 1_168_143, 15_790_839],
    currentEpochPartial: true,
  };

  assert.equal(siteModule.votesForBasis(pool, "current"), pool.votesVeAero);
  assert.equal(
    siteModule.votesForBasis(pool, "previous"),
    previousSettledVotes(pool.epochVotes, pool.currentEpochPartial, pool.votesVeAero),
  );
  assert.equal(siteModule.votesForBasis(pool, "typical"), expectedDilutedVotes(pool.votesVeAero, pool.expectedVotes));
  // Anything unrecognised must fall back to the default basis, not to the live
  // tally: a stale bookmark carrying an old basis should be conservative.
  assert.equal(siteModule.votesForBasis(pool, "nonsense"), siteModule.votesForBasis(pool, "previous"));
});

/**
 * `keptClass` has no `src/` counterpart — it is the "how much of this page to
 * believe" panel's own severity colouring, not a hand-port — but it is pure
 * and worth pinning directly: `keptTile`'s three tiles (`keptAll`/`keptThick`/
 * `keptRich`) are computed independently in `src/timing.ts`'s
 * `buildTimingReport` and can be `null` (no qualifying pools in that window)
 * even when a sibling tile in the same window is a real number — that's
 * exactly the case `trustWindowNow` tolerates by checking only `keptRich`
 * before picking a window. A naive `kept >= 6 ? ... : kept >= 3 ? ... : "bad"`
 * coerces `null` to `0` for both comparisons and falls through to `"bad"`,
 * the same red used for "fewer than 3 of 10 survived" — painting "no
 * measurement yet" as "worst possible measurement".
 */
const siteKeptClass = new Function(`
  ${extractConst(siteSource, "keptClass")}
  return keptClass;
`)() as (kept: number | null) => string;

test("docs/index.html's keptClass renders 'no data' as neutral, not as the worst score", () => {
  assert.equal(siteKeptClass(null), "", "a null (unmeasured) tile must not be coloured as the worst outcome");
  assert.equal(siteKeptClass(6), "good");
  assert.equal(siteKeptClass(3), "mid");
  assert.equal(siteKeptClass(2.9), "bad");
  assert.equal(siteKeptClass(0), "bad");
});

/**
 * `accuracyClass`/`accuracyText` back the "how accurate was each vote basis"
 * tiles in `renderAccuracy`, fed from `timing.accuracy.overall` — one entry
 * per basis, always present by name (see `buildAccuracyReport`'s `BASES`),
 * even when that basis scored zero usable observations. `scorePredictors` in
 * src/predict.ts medians an empty array to `NaN` rather than fabricating a
 * number for exactly that case (the same reasoning that already excludes an
 * empty pool-size bucket from `report.buckets`), so a basis with
 * `observations: 0` carries a `medianAbsError` of `NaN`. Every `<=` against
 * `NaN` is false, so a naive port of the threshold ternary falls through to
 * "bad" and prints "NaN% out" — the same "no data reads as the worst possible
 * score" bug `keptClass`/`keptTile` were fixed for above, in the tile right
 * next to them.
 */
const siteAccuracy = new Function(`
  ${extractConst(siteSource, "accuracyClass")}
  ${extractConst(siteSource, "accuracyText")}
  return { accuracyClass, accuracyText };
`)() as {
  accuracyClass: (basis: { observations: number; medianAbsError: number }) => string;
  accuracyText: (basis: { observations: number; medianAbsError: number }) => string;
};

test("docs/index.html's accuracyClass/accuracyText render a zero-observation basis as neutral 'no data', not '0% out'/NaN%", () => {
  const noData = { observations: 0, medianAbsError: NaN };
  assert.equal(siteAccuracy.accuracyClass(noData), "", "a basis with no observations must not be coloured as the worst outcome");
  assert.equal(siteAccuracy.accuracyText(noData), "—");

  assert.equal(siteAccuracy.accuracyClass({ observations: 5, medianAbsError: 0.1 }), "good");
  assert.equal(siteAccuracy.accuracyClass({ observations: 5, medianAbsError: 0.2 }), "mid");
  assert.equal(siteAccuracy.accuracyClass({ observations: 5, medianAbsError: 0.3 }), "bad");
  assert.equal(siteAccuracy.accuracyText({ observations: 5, medianAbsError: 0.173 }), "17% out");
});

/**
 * `fetchCastVotes` walks `Voter.poolVote(id, i)` upward until the call fails,
 * using the failure as "no length getter, so the end of the list is however
 * it fails" — the same trick `fetchVotesFor` in src/voted.ts uses on-chain,
 * and the same trap: not every failure means the list ended. `ethCall`
 * already retries a real network problem across all three RPCs in `RPCS`
 * before giving up, so a `catch { break; }` here would read a wallet's vote
 * list as shorter than it is whenever that retry is exhausted — silently
 * under-reporting the "you earned" total this panel exists to make
 * checkable, exactly the bug `isEndOfVoteList` was added to src/voted.ts to
 * fix (see "Stop treating an RPC failure as the end of a wallet's vote
 * list"). This pins the page's port of that fix: `isRevertMessage` must mark
 * a genuine on-chain revert, and `fetchCastVotes` must stop on that but
 * propagate anything else.
 */
test("docs/index.html's fetchCastVotes stops a lock's walk on a genuine revert but propagates a real RPC failure", async () => {
  const buildFetchCastVotes = (ethCallImpl: (data: string, to?: string) => Promise<string>) =>
    new Function(
      "ethCall",
      `
        ${extractConst(siteSource, "word")}
        ${extractConst(siteSource, "hexOf")}
        ${extractConst(siteSource, "VOTER_ADDRESS")}
        ${extractConst(siteSource, "SEL_POOL_VOTE")}
        ${extractConst(siteSource, "SEL_VOTES")}
        async ${extractFunction(siteSource, "fetchCastVotes")}
        return fetchCastVotes;
      `,
    )(ethCallImpl) as (ids: bigint[]) => Promise<{ pool: string; veAero: number }[]>;

  const POOL = "0x" + "1".repeat(40);
  const poolWord = "0x" + "0".repeat(24) + "1".repeat(40); // poolVote's answer, address right-aligned in a 32-byte word
  const oneVeAero = "0x" + (10n ** 18n).toString(16).padStart(64, "0");

  // One real pool at index 0, then the on-chain revert that genuinely marks
  // the end of this lock's list.
  let poolVoteCalls = 0;
  const genuineEnd = async (data: string) => {
    if (data.startsWith("0xa86a366d")) {
      poolVoteCalls++;
      if (poolVoteCalls === 1) return poolWord;
      const err = new Error("execution reverted") as Error & { isRevert: boolean };
      err.isRevert = true;
      throw err;
    }
    return oneVeAero;
  };
  assert.deepEqual(await buildFetchCastVotes(genuineEnd)([1n]), [{ pool: POOL, veAero: 1 }]);

  // Same one real pool at index 0, but the index-1 call fails the way
  // `ethCall` fails when every RPC in `RPCS` is unreachable — a fact about
  // the request, not the list. `isRevert` is left unset, exactly as `ethCall`
  // leaves it for an HTTP error, a timeout, or any other non-revert failure.
  let poolVoteCallsAgain = 0;
  const realFailure = async (data: string) => {
    if (data.startsWith("0xa86a366d")) {
      poolVoteCallsAgain++;
      if (poolVoteCallsAgain === 1) return poolWord;
      throw new Error("all RPC endpoints failed");
    }
    return oneVeAero;
  };
  await assert.rejects(() => buildFetchCastVotes(realFailure)([1n]));
});

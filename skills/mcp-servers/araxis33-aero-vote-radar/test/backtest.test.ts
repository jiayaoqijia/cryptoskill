import { test } from "node:test";
import assert from "node:assert/strict";
import { runBacktest, type PoolHistory } from "../src/backtest.js";

/** Builds a pool whose per-epoch USD/votes are given most-recent-first. */
function history(symbol: string, usd: number[], votes: number[]): PoolHistory {
  return { address: `0x${symbol}`, symbol, usd, votes };
}

/** A pool that pays the same amount, with the same vote total, every epoch. */
function steady(symbol: string, usd: number, votes: number, epochs = 5): PoolHistory {
  return history(symbol, Array(epochs).fill(usd), Array(epochs).fill(votes));
}

const opts = { testEpochs: 2, trendEpochs: 2, minTrailingUsd: 10 };

test("runBacktest rejects a non-positive or non-finite budget", () => {
  const pools = [steady("A", 100, 1000)];
  for (const budget of [0, -5, NaN, Infinity]) {
    const report = runBacktest(pools, budget, opts);
    assert.equal(report.epochsTested, 0);
    assert.equal(report.radarTotalUsd, 0);
    assert.equal(report.upliftPct, null);
  }
});

test("runBacktest scores the dilution model: one pool, budget equal to its votes, earns half the pot", () => {
  // 1,000 existing votes + our 1,000 = we hold half the votes, so we earn half
  // of the epoch's $100.
  const report = runBacktest([steady("A", 100, 1000)], 1000, { ...opts, testEpochs: 1 });

  assert.equal(report.epochsTested, 1);
  assert.ok(Math.abs(report.radarTotalUsd - 50) < 1e-6);
  // The naive strategy picks the same single pool here, so there is nothing to win.
  assert.ok(Math.abs(report.naiveTotalUsd - 50) < 1e-6);
  assert.ok(Math.abs(report.upliftPct ?? NaN) < 1e-9);
});

test("runBacktest: spreading beats the naive all-in when the budget is large relative to pool votes", () => {
  // Two identical pools. Naive dumps the whole 10,000 into one of them and
  // dilutes itself; the allocator splits and collects from both.
  const report = runBacktest([steady("A", 100, 1000), steady("B", 100, 1000)], 10_000, {
    ...opts,
    testEpochs: 1,
  });

  // naive: 100 * 10000/11000 = 90.909...
  assert.ok(Math.abs(report.naiveTotalUsd - (100 * 10_000) / 11_000) < 1e-6);
  // radar: split 5000/5000 -> 2 * (100 * 5000/6000) = 166.67
  assert.ok(Math.abs(report.radarTotalUsd - 2 * ((100 * 5000) / 6000)) < 0.5);
  assert.ok(report.radarTotalUsd > report.naiveTotalUsd);
  assert.equal(report.epochsWonByRadar, 1);
  assert.ok((report.upliftPct ?? 0) > 0.8);
});

test("runBacktest does not peek at the epoch being tested (no lookahead)", () => {
  // "Jackpot" pays $10,000 in the epoch under test but was worth $0 in every
  // epoch before it — the information available at decision time is all zeros,
  // so it must not be picked, and its jackpot must not show up in the result.
  const jackpot = history("JACKPOT", [10_000, 0, 0, 0, 0], Array(5).fill(1000));
  const report = runBacktest([steady("STEADY", 100, 1000), jackpot], 1000, {
    ...opts,
    testEpochs: 1,
  });

  assert.equal(report.epochsTested, 1);
  assert.equal(report.epochs[0].candidatesConsidered, 1, "the jackpot pool must not qualify as a candidate");
  assert.equal(report.epochs[0].naiveSymbol, "STEADY");
  assert.ok(report.radarTotalUsd < 100, `must not capture the unforeseeable jackpot, got ${report.radarTotalUsd}`);
});

test("runBacktest skips pools without a full trailing window instead of shrinking the estimate", () => {
  // Only 2 epochs of history, but a t=0 test with trendEpochs=2 needs 3.
  const tooShort = history("SHORT", [100, 100], [1000, 1000]);
  const report = runBacktest([tooShort], 1000, { ...opts, testEpochs: 1 });

  assert.equal(report.epochsTested, 0, "no candidate qualifies, so the epoch is not scored at all");
});

test("runBacktest excludes pools below the trailing-value floor", () => {
  const dust = steady("DUST", 1, 1000); // $1/epoch, below the $10 floor
  const report = runBacktest([dust], 1000, { ...opts, testEpochs: 1 });
  assert.equal(report.epochsTested, 0);
});

test("runBacktest reports uplift as null rather than dividing by a zero baseline", () => {
  // Trailing window is worth $100/epoch so the pool qualifies, but the epoch
  // under test paid out nothing — both strategies earn $0.
  const driedUp = history("DRY", [0, 100, 100, 100, 100], Array(5).fill(1000));
  const report = runBacktest([driedUp], 1000, { ...opts, testEpochs: 1 });

  assert.equal(report.epochsTested, 1);
  assert.equal(report.radarTotalUsd, 0);
  assert.equal(report.naiveTotalUsd, 0);
  assert.equal(report.upliftPct, null);
  assert.equal(report.epochsWonByRadar, 0);
});

test("runBacktest walks each requested epoch and labels how long ago it was", () => {
  const report = runBacktest([steady("A", 100, 1000), steady("B", 100, 1000)], 5000, opts);

  assert.equal(report.epochsTested, 2);
  assert.deepEqual(report.epochs.map((e) => e.epochsAgo), [0, 1]);
  assert.ok(report.epochs.every((e) => e.candidatesConsidered === 2));
  // Totals are the sum of the per-epoch rows, not recomputed separately.
  assert.ok(
    Math.abs(report.radarTotalUsd - report.epochs.reduce((a, e) => a + e.radarUsd, 0)) < 1e-9,
  );
});

test("runBacktest respects topK, so a strong candidate beyond the cutoff is never allocated to", () => {
  // BEST has by far the highest $/vote; with topK=1 it is the only candidate
  // considered, so the whole budget lands there.
  const best = steady("BEST", 1000, 100);
  const rest = [steady("A", 100, 1000), steady("B", 100, 1000)];
  const report = runBacktest([...rest, best], 100, { ...opts, testEpochs: 1, topK: 1 });

  // 1000 * 100/(100+100) = 500 if everything went to BEST alone.
  assert.ok(Math.abs(report.radarTotalUsd - 500) < 1e-6);
});

test("runBacktest's naive baseline may pick a pool the radar's own filters exclude", () => {
  // The whole point of the comparison is that the baseline chases the highest
  // instantaneous $/vote, including into thin one-off-bribe pools the radar
  // deliberately screens out. If the baseline could only choose from pools that
  // already cleared `minTrailingUsd`, both sides would be picking from one
  // pre-vetted set and the backtest would be measuring the radar against itself.
  //
  // STEADY pays $100 across 1,000 votes — $0.10/vote, and a trailing average
  // well clear of the floor. SPIKE pays $15 into a hundredth of a vote —
  // $1,500/vote, 15,000x higher — but averages $7.50 over the trailing window,
  // below the floor, so it is not a radar candidate.
  const steadyPool = history("STEADY", [100, 100, 100, 100, 100], [1000, 1000, 1000, 1000, 1000]);
  const spikePool = history("SPIKE", [12, 15, 0, 0, 0], [0.01, 0.01, 0.01, 0.01, 0.01]);

  const report = runBacktest([steadyPool, spikePool], 100, {
    testEpochs: 1,
    trendEpochs: 2,
    minTrailingUsd: 10,
  });

  assert.equal(report.epochsTested, 1);
  // Only STEADY clears the trailing-average floor, so the radar sees one candidate...
  assert.equal(report.epochs[0].candidatesConsidered, 1);
  // ...while the baseline is free to chase SPIKE's $1,500/vote, and does.
  assert.equal(report.epochs[0].naiveSymbol, "SPIKE");

  // It is then scored on what SPIKE actually paid the tested epoch, which is the
  // half of this that silently returned $0 while outcomes were only recorded for
  // radar candidates: $12 shared between the 0.01 votes already there and our 100.
  assert.ok(report.epochs[0].naiveUsd > 0);
  assert.ok(Math.abs(report.epochs[0].naiveUsd - (12 * 100) / 100.01) < 1e-6);
});

test("widening the baseline leaves the radar's own candidate set untouched", () => {
  // Guard against the fix over-correcting: pools admitted only so the baseline
  // can see them must not become allocation candidates themselves.
  const steadyPool = history("STEADY", [100, 100, 100, 100, 100], [1000, 1000, 1000, 1000, 1000]);
  const spikePool = history("SPIKE", [12, 15, 0, 0, 0], [0.01, 0.01, 0.01, 0.01, 0.01]);

  const withSpike = runBacktest([steadyPool, spikePool], 100, {
    testEpochs: 1,
    trendEpochs: 2,
    minTrailingUsd: 10,
  });
  const withoutSpike = runBacktest([steadyPool], 100, {
    testEpochs: 1,
    trendEpochs: 2,
    minTrailingUsd: 10,
  });

  assert.equal(withSpike.epochs[0].candidatesConsidered, withoutSpike.epochs[0].candidatesConsidered);
  assert.ok(Math.abs(withSpike.radarTotalUsd - withoutSpike.radarTotalUsd) < 1e-9);
});

test("--min-consistency drops spiky pools from the radar's candidates, and says how many", () => {
  // Same trailing average ($100), same votes, opposite steadiness: STEADY paid
  // 100/100 across the window, SPIKY paid 180 then 20.
  const steadyPool = history("STEADY", [100, 100, 100, 100], [1000, 1000, 1000, 1000]);
  const spikyPool = history("SPIKY", [100, 180, 20, 100], [1000, 1000, 1000, 1000]);
  const shared = { testEpochs: 1, trendEpochs: 2, minTrailingUsd: 10 };

  const unfiltered = runBacktest([steadyPool, spikyPool], 1000, shared);
  assert.equal(unfiltered.epochs[0].candidatesConsidered, 2);
  assert.equal(unfiltered.epochs[0].candidatesExcludedByConsistency, 0);
  assert.equal(unfiltered.minConsistency, 0);

  const filtered = runBacktest([steadyPool, spikyPool], 1000, { ...shared, minConsistency: 0.8 });
  assert.equal(filtered.epochs[0].candidatesConsidered, 1);
  assert.equal(filtered.epochs[0].candidatesExcludedByConsistency, 1);
  assert.equal(filtered.minConsistency, 0.8);
});

test("the naive baseline is not filtered, so uplift stays comparable across runs", () => {
  // SPIKY has the highest last-known $/vote (180/1000 vs 100/1000), so the
  // baseline picks it either way. If the filter leaked into the baseline, the
  // filtered run's naive figure would change and the two uplifts would be
  // measuring different things.
  const steadyPool = history("STEADY", [100, 100, 100, 100], [1000, 1000, 1000, 1000]);
  const spikyPool = history("SPIKY", [100, 180, 20, 100], [1000, 1000, 1000, 1000]);
  const shared = { testEpochs: 1, trendEpochs: 2, minTrailingUsd: 10 };

  const unfiltered = runBacktest([steadyPool, spikyPool], 1000, shared);
  const filtered = runBacktest([steadyPool, spikyPool], 1000, { ...shared, minConsistency: 0.8 });

  assert.equal(filtered.epochs[0].naiveSymbol, "SPIKY");
  assert.equal(unfiltered.epochs[0].naiveSymbol, "SPIKY");
  assert.ok(Math.abs(filtered.naiveTotalUsd - unfiltered.naiveTotalUsd) < 1e-9);
});

test("consistency is measured as of the decision, not from the epoch being tested", () => {
  // The tested epoch (index 0) is a $999 outlier, but the trailing window the
  // decision was made from is flat. Judging it on today's full history would
  // reject the pool using information that did not exist yet — a hindsight fit.
  const pool = history("LATESPIKE", [999, 100, 100, 100], [1000, 1000, 1000, 1000]);

  const report = runBacktest([pool], 1000, {
    testEpochs: 1,
    trendEpochs: 2,
    minTrailingUsd: 10,
    minConsistency: 1,
  });

  assert.equal(report.epochs[0].candidatesConsidered, 1);
  assert.equal(report.epochs[0].candidatesExcludedByConsistency, 0);
});

test("a consistency floor nothing clears leaves no epoch tested rather than a flattering one", () => {
  const spikyPool = history("SPIKY", [100, 180, 20, 100], [1000, 1000, 1000, 1000]);

  const report = runBacktest([spikyPool], 1000, {
    testEpochs: 1,
    trendEpochs: 2,
    minTrailingUsd: 10,
    minConsistency: 0.95,
  });

  assert.equal(report.epochsTested, 0);
  assert.equal(report.radarTotalUsd, 0);
  assert.equal(report.upliftPct, null);
  assert.equal(report.minConsistency, 0.95);
});

test("the typical-weight basis avoids a pool that is merely between votes", () => {
  // TRAP pays the same $500 every epoch and normally carries 100,000 votes, but
  // the most recent settled epoch caught it at 2,000 — and it settles back at
  // 100,000 in the epoch under test. Judged on that last figure it looks like
  // $0.25/vote; judged on what it usually carries, $0.005.
  //
  // Index 0 is the epoch being tested, so the decision may only read index 1 and
  // older. Written most-recent-first:
  //   usd:   [500(tested), 500, 500, 500, 500]
  //   votes: [100_000(tested), 2_000, 100_000, 100_000, 100_000]
  const trap = history(
    "TRAP",
    [500, 500, 500, 500, 500],
    [100_000, 2_000, 100_000, 100_000, 100_000],
  );
  // A dependable alternative: fewer dollars, but the weight is what it looks like.
  const solid = steady("SOLID", 300, 10_000, 5);

  const report = runBacktest([trap, solid], 10_000, {
    testEpochs: 1,
    trendEpochs: 3,
    minTrailingUsd: 10,
  });

  assert.equal(report.epochsTested, 1);
  assert.ok(
    report.radarTypicalTotalUsd > report.radarTotalUsd,
    `typical basis (${report.radarTypicalTotalUsd}) should beat current basis (${report.radarTotalUsd}) when a pool is between votes`,
  );
  assert.ok((report.typicalVsCurrentPct ?? 0) > 0);
  assert.equal(report.epochsWonByTypical, 1);
});

test("the typical-weight basis cannot see the epoch it is tested on", () => {
  // Same pool twice, differing ONLY in the tested epoch's settled weight. The
  // decision is taken from index 1 and older, which are identical, so both runs
  // must allocate identically — any difference in what was *chosen* would mean
  // the outcome leaked into the decision.
  //
  // The realised dollars legitimately differ (you are diluted by what actually
  // turned up), so the invariant is asserted on the allocation, via a second
  // pool that must or must not be funded consistently.
  const shape = (testedVotes: number) =>
    history("P", [400, 400, 400, 400, 400], [testedVotes, 5_000, 50_000, 50_000, 50_000]);
  const other = steady("OTHER", 100, 5_000, 5);

  const cheap = runBacktest([shape(1_000), other], 5_000, {
    testEpochs: 1,
    trendEpochs: 3,
    minTrailingUsd: 10,
  });
  const crowded = runBacktest([shape(900_000), other], 5_000, {
    testEpochs: 1,
    trendEpochs: 3,
    minTrailingUsd: 10,
  });

  assert.equal(cheap.epochs[0].candidatesConsidered, crowded.epochs[0].candidatesConsidered);
  // A lookahead would have made the crowded run avoid P and so earn *more* than
  // the cheap run's diluted share. It must instead earn less: same choice, worse
  // outcome, which is exactly what having no foresight looks like.
  assert.ok(
    crowded.radarTypicalTotalUsd < cheap.radarTypicalTotalUsd,
    "the run whose tested epoch filled up must earn less, not dodge the pool",
  );
});

import { test } from "node:test";
import assert from "node:assert/strict";
import {
  computeTrend,
  epochEndOf,
  epochStartOf,
  formatDuration,
  isEpochInProgress,
  isPeriodInProgress,
  periodEndOf,
  periodStartOf,
  EPOCH_SECONDS,
  WEEKLY_EPOCH,
  type RewardPeriod,
} from "../src/trend.js";

/**
 * The seam these exercise is not a feature yet: every caller still passes the
 * weekly epoch. What has to hold is that naming the period changed nothing for
 * the week — the old functions are now thin wrappers, and a silent shift of an
 * epoch boundary would mis-date every snapshot in the published history — and
 * that a period which is *not* aligned to Unix time zero comes out right, since
 * that is the whole reason the alignment became a parameter instead of a
 * consequence of flooring.
 */
test("the weekly period reproduces the epoch functions exactly", () => {
  const samples = [
    0,
    1,
    EPOCH_SECONDS - 1,
    1_786_579_200, // 2026-08-13T00:00:00Z, a boundary
    1_786_950_908, // mid-epoch
    Math.floor(Date.UTC(2026, 7, 27, 0, 0, 0) / 1000),
  ];

  for (const t of samples) {
    assert.equal(periodStartOf(t, WEEKLY_EPOCH), epochStartOf(t), `start disagreed at ${t}`);
    assert.equal(periodEndOf(t, WEEKLY_EPOCH), epochEndOf(t), `end disagreed at ${t}`);
    assert.equal(periodStartOf(t), epochStartOf(t), "the weekly epoch must be the default period");
  }
});

test("a period anchored away from Unix time zero counts boundaries from its own anchor", () => {
  // A 48-hour window opening at 2026-08-13T09:00:00Z — the shape a continuous
  // allocation schedule would have, and one that flooring alone cannot produce.
  const anchor = Math.floor(Date.UTC(2026, 7, 13, 9, 0, 0) / 1000);
  const window: RewardPeriod = { lengthSeconds: 48 * 3600, anchorSeconds: anchor, name: "window" };

  assert.equal(periodStartOf(anchor, window), anchor, "the anchor itself opens a period");
  assert.equal(periodStartOf(anchor + 3600, window), anchor);
  assert.equal(periodStartOf(anchor + 48 * 3600, window), anchor + 48 * 3600);
  assert.equal(periodEndOf(anchor + 3600, window), anchor + 48 * 3600);

  // Before the anchor is a period like any other, not a negative one.
  assert.equal(periodStartOf(anchor - 1, window), anchor - 48 * 3600);
  assert.equal(periodEndOf(anchor - 1, window), anchor);

  // And the alignment is genuinely the window's, not Thursday's.
  assert.notEqual(periodStartOf(anchor + 3600, window), epochStartOf(anchor + 3600));
});

test("isPeriodInProgress follows the period it is given, not the week", () => {
  const anchor = Math.floor(Date.UTC(2026, 7, 13, 9, 0, 0) / 1000);
  const window: RewardPeriod = { lengthSeconds: 48 * 3600, anchorSeconds: anchor, name: "window" };

  assert.equal(isPeriodInProgress(anchor, anchor + 3600, window), true);
  assert.equal(isPeriodInProgress(anchor, anchor + 48 * 3600, window), false);
  // The same two timestamps read against the weekly epoch are still one epoch.
  assert.equal(isEpochInProgress(anchor, anchor + 48 * 3600), true);
});

test("epoch boundaries land on Thursday 00:00 UTC", () => {
  // 2026-08-17T07:15:08Z (a Monday) sits inside the epoch that opened 2026-08-13.
  const start = epochStartOf(1_786_950_908);
  assert.equal(new Date(start * 1000).toISOString(), "2026-08-13T00:00:00.000Z");
  assert.equal(new Date(start * 1000).getUTCDay(), 4); // 4 = Thursday
});

test("epochStartOf is idempotent on a boundary", () => {
  const boundary = 1_786_579_200;
  assert.equal(epochStartOf(boundary), boundary);
});

test("the newest epoch counts as in progress until the week rolls over", () => {
  const epochStart = 1_786_579_200; // 2026-08-13T00:00:00Z
  const midWeek = epochStart + 4 * 86_400;

  assert.equal(isEpochInProgress(epochStart, midWeek), true);
  // Same pool data seen a week later: that epoch has closed, a newer one is live.
  assert.equal(isEpochInProgress(epochStart, epochStart + EPOCH_SECONDS), false);
});

test("momentum compares the recent half against the older half", () => {
  // Most recent first: recent half averages 400, older half averages 100.
  const { momentum, completedEpochs } = computeTrend([400, 400, 100, 100], false);
  assert.equal(completedEpochs, 4);
  assert.equal(momentum, 3);
});

test("a decaying pool reports negative momentum", () => {
  const { momentum } = computeTrend([50, 50, 200, 200], false);
  assert.equal(momentum, -0.75);
});

test("a flat pool reports no movement", () => {
  const { momentum } = computeTrend([120, 120, 120, 120, 120, 120], false);
  assert.equal(momentum, 0);
});

test("the in-progress epoch is excluded so a part-week cannot fake a decline", () => {
  // A steady $200/epoch pool, scanned three days into the current epoch: the
  // newest entry has only accrued $60 so far. Counting it would report a crash.
  const series = [60, 200, 200, 200, 200];

  assert.equal(computeTrend(series, true).momentum, 0);
  assert.ok((computeTrend(series, false).momentum as number) < -0.3);
});

test("the in-progress epoch also does not count toward the minimum history", () => {
  // Four entries, but one is the part-week: only three completed epochs remain.
  const { momentum, completedEpochs } = computeTrend([60, 200, 200, 200], true);
  assert.equal(completedEpochs, 3);
  assert.equal(momentum, null);
});

test("too little history reports null rather than a guess", () => {
  assert.equal(computeTrend([100, 100, 100], false).momentum, null);
  assert.equal(computeTrend([], false).momentum, null);
});

test("an odd history drops the middle epoch so both halves weigh the same", () => {
  // Recent half [400, 400], middle 999 ignored, older half [100, 100].
  assert.equal(computeTrend([400, 400, 999, 100, 100], false).momentum, 3);
});

test("a zero-paying older half reports null instead of infinite growth", () => {
  const { momentum, completedEpochs } = computeTrend([500, 500, 0, 0], false);
  assert.equal(momentum, null);
  assert.equal(completedEpochs, 4); // history was long enough; the baseline was not usable
});

test("a baseline of loose change reports null rather than a headline percentage", () => {
  // Taken from real snapshot data: $0.02/epoch rising to $5.75 computes to
  // +29,286%, which would outrank every genuine mover on the board.
  assert.equal(computeTrend([5.75, 5.75, 0.02, 0.02], false).momentum, null);
});

test("a real move over a real baseline is still reported", () => {
  // Also from live data: $53.88/epoch to $416.53 is the move the floor must not eat.
  const { momentum } = computeTrend([416.53, 416.53, 53.88, 53.88], false);
  assert.ok(momentum !== null && momentum > 6 && momentum < 8);
});

test("only the older half is floored, so a collapse to near-nothing still reports", () => {
  // $200/epoch decaying to $3: the recent half is tiny, which is the finding.
  const { momentum } = computeTrend([3, 3, 200, 200], false);
  assert.ok(momentum !== null && momentum < -0.95);
});

test("the baseline floor is overridable for callers with a different threshold", () => {
  assert.equal(computeTrend([5.75, 5.75, 0.02, 0.02], false, 0.01).momentum, 286.5);
});

test("epochEndOf lands on the Thursday 00:00 UTC that closes the epoch", () => {
  // Mid-epoch: Saturday 2026-08-22 12:00 UTC closes on Thursday 2026-08-27.
  const midEpoch = Math.floor(Date.UTC(2026, 7, 22, 12, 0, 0) / 1000);
  const end = epochEndOf(midEpoch);
  const endDate = new Date(end * 1000);

  assert.equal(endDate.getUTCDay(), 4, "epochs must close on a Thursday");
  assert.equal(endDate.toISOString(), "2026-08-27T00:00:00.000Z");
  assert.ok(end > midEpoch);
});

test("epochEndOf treats a timestamp exactly on the boundary as the start of the new epoch", () => {
  // A vote at the instant of the flip belongs to the epoch beginning there, so
  // it has a full week left, not zero seconds.
  const boundary = Math.floor(Date.UTC(2026, 7, 27, 0, 0, 0) / 1000);
  assert.equal(epochEndOf(boundary) - boundary, 604800);
});

test("formatDuration shows the two coarsest units, and never a negative one", () => {
  assert.equal(formatDuration(2 * 86400 + 4 * 3600 + 30 * 60), "2d 4h");
  assert.equal(formatDuration(4 * 3600 + 12 * 60), "4h 12m");
  assert.equal(formatDuration(9 * 60 + 59), "9m");
  assert.equal(formatDuration(0), "0m");
  assert.equal(formatDuration(-500), "0m");
  assert.equal(formatDuration(NaN), "0m");
});

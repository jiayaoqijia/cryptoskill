import { test } from "node:test";
import assert from "node:assert/strict";
import { toVeNftRaw, toVeNftSummary } from "../src/veAero.js";

test("toVeNftSummary converts voting_amount from 18-decimal wei into veAERO", () => {
  const summary = toVeNftSummary({ id: 6n, voting_amount: 11_362_738_622_000_000_000_000_000n, expires_at: 0n, is_permanent: true });
  assert.equal(summary.votingPowerVeAero, 11_362_738.622);
});

test("toVeNftSummary keeps expiresAt 0 for a permanently-locked veNFT rather than treating it as Jan 1 1970", () => {
  const summary = toVeNftSummary({ id: 6n, voting_amount: 0n, expires_at: 0n, is_permanent: true });
  assert.equal(summary.expiresAt, 0);
});

test("toVeNftSummary passes through a non-zero expires_at as a unix-seconds number", () => {
  const summary = toVeNftSummary({ id: 1n, voting_amount: 0n, expires_at: 1_893_456_000n, is_permanent: false });
  assert.equal(summary.expiresAt, 1_893_456_000);
});

test("toVeNftSummary stringifies the NFT id without precision loss for ids beyond Number.MAX_SAFE_INTEGER", () => {
  const bigId = 2n ** 60n + 3n; // far beyond 2^53, would lose precision as a plain Number
  const summary = toVeNftSummary({ id: bigId, voting_amount: 0n, expires_at: 0n, is_permanent: false });
  assert.equal(summary.id, bigId.toString());
});

test("toVeNftSummary returns 0 voting power for an NFT with no locked amount", () => {
  const summary = toVeNftSummary({ id: 17324n, voting_amount: 0n, expires_at: 0n, is_permanent: false });
  assert.equal(summary.votingPowerVeAero, 0);
});

// A permanent lock and a withdrawn one both report expires_at 0, so the two
// have to be told apart by the flag. Before this, a spent lock printed as
// "never (permanent lock)" — the most confusing thing it could have said.
test("toVeNftSummary marks a permanent lock as permanent", () => {
  const summary = toVeNftSummary({ id: 6n, voting_amount: 5n * 10n ** 18n, expires_at: 0n, is_permanent: true });
  assert.equal(summary.isPermanent, true);
  assert.equal(summary.expiresAt, 0);
});

test("toVeNftSummary does not call a withdrawn lock permanent just because it expires at 0", () => {
  const summary = toVeNftSummary({ id: 1n, voting_amount: 0n, expires_at: 0n, is_permanent: false });
  assert.equal(summary.isPermanent, false);
  assert.equal(summary.expiresAt, 0);
  assert.equal(summary.votingPowerVeAero, 0);
});

test("toVeNftRaw takes voting power from balanceOfNFT and the terms from locked", () => {
  // locked() answers (amount, end, isPermanent). `amount` is the AERO put in,
  // which is not the voting power — that decays toward expiry and comes from
  // balanceOfNFT — so toVeNftRaw must ignore it.
  const raw = toVeNftRaw(95_000n, 81_435_031_560_257_090_000n, [100n * 10n ** 18n, 1_888_185_600n, false]);
  assert.deepEqual(raw, {
    id: 95_000n,
    voting_amount: 81_435_031_560_257_090_000n,
    expires_at: 1_888_185_600n,
    is_permanent: false,
  });
});

test("toVeNftRaw carries the permanent flag through to the summary", () => {
  const summary = toVeNftSummary(toVeNftRaw(6n, 2n * 10n ** 18n, [2n * 10n ** 18n, 0n, true]));
  assert.equal(summary.isPermanent, true);
  assert.equal(summary.votingPowerVeAero, 2);
});

test("toVeNftRaw handles a fully withdrawn lock, which reads as all zeros", () => {
  const summary = toVeNftSummary(toVeNftRaw(3n, 0n, [0n, 0n, false]));
  assert.deepEqual(summary, { id: "3", votingPowerVeAero: 0, expiresAt: 0, isPermanent: false });
});

import { test } from "node:test";
import assert from "node:assert/strict";
import { decodeFunctionData, toFunctionSelector } from "viem";
import { buildVoteCalldata } from "../src/calldata.js";
import { VOTER_ABI } from "../src/abi.js";
import { BASE_CHAIN_ID, VOTER_ADDRESS } from "../src/constants.js";
import type { WholePercentWeight } from "../src/allocator.js";

const POOL_A = "0x0b3e751fc0e2b0d0c5e28d5b9c4a4d8e0d3f2a11";
const POOL_B = "0x1c4f862fd1f3c1e1d6f39e6cad5b5e9f1e4a3b22";
const POOL_C = "0x2d5a973ae204d2f2e7048f7dbe6c6faf2f5b4c33";

function weights(...rows: [string, number][]): WholePercentWeight[] {
  return rows.map(([pool, percent], i) => ({ pool, symbol: `P${i}`, percent }));
}

/**
 * The point of these is not that viem can encode — it can. It is that the bytes
 * a voter is about to sign say exactly what the table above them said. Every
 * check here decodes the output rather than comparing it to a hex string copied
 * from a previous run, which would only prove the function still does whatever
 * it did last time.
 */
test("the calldata decodes back to the pools and weights it was given", () => {
  const tx = buildVoteCalldata("17324", weights([POOL_A, 60], [POOL_B, 28], [POOL_C, 12]));
  const decoded = decodeFunctionData({ abi: VOTER_ABI, data: tx.data });

  assert.equal(decoded.functionName, "vote");
  const [tokenId, pools, castWeights] = decoded.args as [bigint, readonly string[], readonly bigint[]];

  assert.equal(tokenId, 17_324n);
  assert.deepEqual(
    pools.map((p) => p.toLowerCase()),
    [POOL_A, POOL_B, POOL_C],
  );
  assert.deepEqual(castWeights, [60n, 28n, 12n]);
});

test("the transaction targets the Voter on Base and moves no value", () => {
  const tx = buildVoteCalldata("1", weights([POOL_A, 100]));

  assert.equal(tx.to, VOTER_ADDRESS);
  assert.equal(tx.chainId, BASE_CHAIN_ID);
  assert.equal(tx.value, "0x0");
  assert.equal(tx.data.slice(0, 10), toFunctionSelector("vote(uint256,address[],uint256[])"));
});

test("the echoed pools and weights stay aligned with the encoded ones", () => {
  // The plain fields exist so a voter can check the blob without decoding it;
  // if they could drift from the bytes they would be worse than absent.
  const tx = buildVoteCalldata("42", weights([POOL_A, 70], [POOL_B, 30]));
  const [, pools, castWeights] = decodeFunctionData({ abi: VOTER_ABI, data: tx.data }).args as [
    bigint,
    readonly string[],
    readonly bigint[],
  ];

  assert.deepEqual(tx.pools, [...pools]);
  assert.deepEqual(tx.weights.map(BigInt), [...castWeights]);
});

test("a veNFT id beyond Number.MAX_SAFE_INTEGER survives intact", () => {
  const huge = "115792089237316195423570985008687907853269984665640564039457584007913129639935";
  const tx = buildVoteCalldata(huge, weights([POOL_A, 100]));
  const [tokenId] = decodeFunctionData({ abi: VOTER_ABI, data: tx.data }).args as [bigint];

  assert.equal(tokenId.toString(), huge);
  assert.equal(tx.tokenId, huge);
});

test("pool addresses come back checksummed whatever case they went in as", () => {
  const tx = buildVoteCalldata("1", weights([POOL_A.toUpperCase().replace("0X", "0x"), 100]));
  assert.notEqual(tx.pools[0], tx.pools[0].toLowerCase(), "expected EIP-55 mixed case");
  assert.equal(tx.pools[0].toLowerCase(), POOL_A);
});

test("weights that do not total 100 are refused rather than normalised", () => {
  // The contract would happily normalise 60/30 to 2:1 and cast a vote nobody
  // was shown. A total that is not 100 means an upstream bug, not a preference.
  assert.throws(() => buildVoteCalldata("1", weights([POOL_A, 60], [POOL_B, 30])), /total 100%/);
  assert.throws(() => buildVoteCalldata("1", weights([POOL_A, 60], [POOL_B, 60])), /total 100%/);
});

test("a repeated pool is refused, because the contract would sum the rows", () => {
  assert.throws(
    () => buildVoteCalldata("1", weights([POOL_A, 50], [POOL_A.toUpperCase().replace("0X", "0x"), 50])),
    /appears twice/,
  );
});

test("a fractional or non-positive weight is refused", () => {
  assert.throws(() => buildVoteCalldata("1", weights([POOL_A, 99.5], [POOL_B, 0.5])), /whole number/);
  assert.throws(() => buildVoteCalldata("1", weights([POOL_A, 100], [POOL_B, 0])), /whole number/);
  assert.throws(() => buildVoteCalldata("1", weights([POOL_A, 110], [POOL_B, -10])), /whole number/);
});

test("an empty allocation is refused rather than encoding an empty vote", () => {
  // Voter.vote with empty arrays clears the NFT's votes for the epoch, which is
  // the opposite of what someone asking for a recommendation wants.
  assert.throws(() => buildVoteCalldata("1", []), /Nothing to vote/);
});

test("a bad veNFT id is refused", () => {
  assert.throws(() => buildVoteCalldata("0", weights([POOL_A, 100])), /positive whole number/);
  assert.throws(() => buildVoteCalldata("-1", weights([POOL_A, 100])), /positive whole number/);
  assert.throws(() => buildVoteCalldata("17e3", weights([POOL_A, 100])), /positive whole number/);
  assert.throws(() => buildVoteCalldata("", weights([POOL_A, 100])), /positive whole number/);
});

test("something that is not an address is refused", () => {
  assert.throws(() => buildVoteCalldata("1", weights(["not-an-address", 100])), /is not a pool address/);
  assert.throws(() => buildVoteCalldata("1", weights([POOL_A.slice(0, 20), 100])), /is not a pool address/);
});

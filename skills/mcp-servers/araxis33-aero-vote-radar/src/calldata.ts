import { encodeFunctionData } from "viem";
import { VOTER_ABI } from "./abi.js";
import { BASE_CHAIN_ID, VOTER_ADDRESS } from "./constants.js";
import { isValidAddress, normalizeAddress } from "./util.js";
import type { WholePercentWeight } from "./allocator.js";

/**
 * An unsigned transaction: everything needed to cast the vote except a
 * signature, which stays with whoever holds the keys.
 *
 * The fields are named the way wallets and signing tools expect them (`to`,
 * `data`, `value`, `chainId`), so this can be pasted into one without
 * translation. `pools` and `weights` repeat, in plain form, what the `data`
 * blob encodes — not because a caller needs both, but because a hex string is
 * unreadable and a voter should be able to check that the bytes they are about
 * to sign say what they were told they say.
 */
export interface UnsignedVoteTransaction {
  chainId: number;
  /** The Voter contract. Nothing else should ever appear here. */
  to: `0x${string}`;
  /** Always zero: voting moves no value. */
  value: "0x0";
  data: `0x${string}`;
  /** The veNFT this vote is cast from, as a decimal string (ids exceed Number.MAX_SAFE_INTEGER). */
  tokenId: string;
  /** Pools in the same order as `weights`, checksummed. */
  pools: `0x${string}`[];
  /** Whole percentage points, in the same order as `pools`, summing to 100. */
  weights: number[];
  /** The function being called, spelled out for anyone checking the selector. */
  functionSignature: "vote(uint256,address[],uint256[])";
}

/**
 * Turns a vote-ready allocation into the exact bytes `Voter.vote` expects.
 *
 * This is the last mile the tool was missing. Everything upstream produces a
 * table of percentages that a person then retypes into a web form, one row at a
 * time — which is where an allocation measured to the point loses accuracy, to
 * a mistyped digit or a row skipped because the form scrolled.
 *
 * What it deliberately does not do is sign. No key, no seed phrase and no
 * wallet connection is involved anywhere in this project, and that does not
 * change here: the output is a transaction that anyone can read and only the
 * NFT's owner can execute. A voter pastes it into their own wallet, checks that
 * `to` is the Voter contract and that the pools and weights match what they
 * were shown, and signs it themselves.
 *
 * Aerodrome's `vote` normalises the weights by their own sum, so any
 * proportional set would cast the same vote. Whole percentages summing to 100
 * are required here anyway, because that is what the rest of the tool computed
 * and what the voter was shown — a weight vector that quietly disagreed with
 * the printed table would be the one bug this function exists to prevent.
 *
 * Validation is strict and throws rather than repairing anything. A vote is a
 * financial action taken once a week; guessing what a malformed request meant
 * is not a service to anyone.
 */
export function buildVoteCalldata(tokenId: string, weights: WholePercentWeight[]): UnsignedVoteTransaction {
  if (!/^[0-9]+$/.test(tokenId) || BigInt(tokenId) <= 0n) {
    throw new Error(`veNFT id must be a positive whole number, got "${tokenId}".`);
  }
  if (weights.length === 0) {
    throw new Error("Nothing to vote: the allocation is empty.");
  }

  const seen = new Set<string>();
  for (const w of weights) {
    if (!isValidAddress(w.pool)) {
      throw new Error(`"${w.pool}" is not a pool address.`);
    }
    // A repeated pool is not a harmless duplicate: the two rows would be summed
    // by the contract into a weight nobody chose, and the printed table would
    // no longer describe the vote.
    const key = w.pool.toLowerCase();
    if (seen.has(key)) {
      throw new Error(`Pool ${w.pool} appears twice in the allocation.`);
    }
    seen.add(key);

    if (!Number.isInteger(w.percent) || w.percent <= 0) {
      throw new Error(
        `${w.symbol} has a weight of ${w.percent}, which is not a whole number of percentage points above zero.`,
      );
    }
  }

  const total = weights.reduce((a, w) => a + w.percent, 0);
  if (total !== 100) {
    throw new Error(`Weights must total 100%, got ${total}%.`);
  }

  const pools = weights.map((w) => normalizeAddress(w.pool));
  const percents = weights.map((w) => BigInt(w.percent));

  return {
    chainId: BASE_CHAIN_ID,
    to: VOTER_ADDRESS,
    value: "0x0",
    data: encodeFunctionData({ abi: VOTER_ABI, functionName: "vote", args: [BigInt(tokenId), pools, percents] }),
    tokenId,
    pools,
    weights: weights.map((w) => w.percent),
    functionSignature: "vote(uint256,address[],uint256[])",
  };
}

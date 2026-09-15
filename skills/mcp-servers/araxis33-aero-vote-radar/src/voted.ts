/**
 * What a lock actually voted for last week, and what that turned out to be
 * worth.
 *
 * Every other measurement in this repo is about the vote a holder has not cast
 * yet. This one is about the vote they already cast: which pools their veNFT
 * chose, what weight went to each, and what share of those pools' settled
 * rewards that bought. Nothing here predicts anything — the epoch is closed and
 * the numbers are final, so a holder can check every figure against their own
 * wallet.
 *
 * It exists because the tool had no way to show anyone that it was worth using.
 * "Here is where to vote next week" asks for trust up front; "here is what last
 * Thursday paid you, and here is what this allocation would have paid on the
 * same epoch with the same veAERO" asks for nothing and is checkable on chain.
 *
 * Read through `Voter.poolVote` / `Voter.votes` rather than through event logs.
 * A week of Base is roughly 300,000 blocks and public RPCs cap a `getLogs`
 * range far below that, so the log route needs ~150 chunked requests and cannot
 * run in a browser; these are a handful of plain `eth_call`s that can.
 */
import { VOTER_ADDRESS } from "./constants.js";
import { VOTER_ABI, POOL_ABI } from "./abi.js";
import { client } from "./chain.js";
import { epochUsd } from "./efficiency.js";
import type { EpochData } from "./pools.js";

const VE_DECIMALS = 18;

/** One pool a lock put weight on. */
export interface CastVote {
  /** Lowercased pool address. */
  pool: string;
  /** Raw weight as the Voter recorded it. Shares are ratios, so the unit never has to be named. */
  weight: bigint;
}

/**
 * The pools one veNFT currently has weight on, with that weight.
 *
 * This deployment has no length getter for the per-token pool list, so the
 * index is walked upward until the call reverts — that revert is the length.
 * `maxPools` bounds it so a malformed response cannot spin forever; Aerodrome's
 * UI caps a vote at far fewer pools than this.
 */
export async function fetchVotesFor(tokenId: bigint, maxPools = 60): Promise<CastVote[]> {
  const out: CastVote[] = [];
  for (let i = 0n; i < BigInt(maxPools); i++) {
    let pool: `0x${string}`;
    try {
      pool = (await client.readContract({
        address: VOTER_ADDRESS,
        abi: VOTER_ABI,
        functionName: "poolVote",
        args: [tokenId, i],
      })) as `0x${string}`;
    } catch {
      // Past the end of this token's list. Not an error: it is how the list ends.
      break;
    }
    const weight = (await client.readContract({
      address: VOTER_ADDRESS,
      abi: VOTER_ABI,
      functionName: "votes",
      args: [tokenId, pool],
    })) as bigint;
    // A pool can stay in the list with zero weight after a re-vote. Keeping it
    // would put an empty row in a report about where the vote went.
    if (weight > 0n) out.push({ pool: pool.toLowerCase(), weight });
  }
  return out;
}

/**
 * Each pool's own symbol, read straight off the pool contract.
 *
 * Deliberately not resolved through `fetchActivePools`: that walks the Voter's
 * ~1,800 registered pools and then keeps only the ones with a live gauge, which
 * is both slow and wrong here. A holder can perfectly well have voted for a
 * pool whose gauge has since been killed — measured on a real lock, that is
 * exactly what happened — and a review that silently dropped those rows would
 * under-report what the holder actually did with their vote.
 *
 * A pool that will not answer falls back to its address, because a row with a
 * checkable address is worth more than no row.
 */
export async function fetchPoolSymbols(pools: string[]): Promise<Map<string, string>> {
  const symbolOf = async (address: string): Promise<string | null> => {
    try {
      return (await client.readContract({
        address: address as `0x${string}`,
        abi: POOL_ABI,
        functionName: "symbol",
      })) as string;
    } catch {
      return null;
    }
  };

  const out = new Map<string, string>();
  await Promise.all(
    pools.map(async (pool) => {
      const direct = await symbolOf(pool);
      if (direct) {
        out.set(pool.toLowerCase(), direct);
        return;
      }

      // Slipstream (concentrated-liquidity) pools have no `symbol()` at all, and
      // they are a real destination for votes — measured on a live wallet, both
      // of its pools were this kind. Falling straight through to the address
      // would print a table of raw hex, so the name is composed from the pair
      // the pool actually holds.
      try {
        const [token0, token1] = (await Promise.all([
          client.readContract({ address: pool as `0x${string}`, abi: POOL_ABI, functionName: "token0" }),
          client.readContract({ address: pool as `0x${string}`, abi: POOL_ABI, functionName: "token1" }),
        ])) as [string, string];
        const [a, b] = await Promise.all([symbolOf(token0), symbolOf(token1)]);
        out.set(pool.toLowerCase(), a && b ? `CL-${a}/${b}` : pool);
      } catch {
        out.set(pool.toLowerCase(), pool);
      }
    }),
  );
  return out;
}

/** When this lock last cast a vote, in unix seconds; 0 if it never has. */
export async function fetchLastVoted(tokenId: bigint): Promise<number> {
  const ts = (await client.readContract({
    address: VOTER_ADDRESS,
    abi: VOTER_ABI,
    functionName: "lastVoted",
    args: [tokenId],
  })) as bigint;
  return Number(ts);
}

/** One pool of a scored vote. */
export interface ScoredVote {
  pool: string;
  symbol: string;
  /** Share of this holder's own vote that went here, 0..1. */
  share: number;
  /** veAERO this holder had on the pool. */
  myVotes: number;
  /** Everyone's weight on the pool when the epoch settled. */
  poolVotes: number;
  /** The pool's total bribes + fees for that epoch, in USD. */
  poolUsd: number;
  /** `poolUsd * myVotes / poolVotes` — this holder's realised share. */
  earnedUsd: number;
}

export interface VoteReview {
  /** Unix seconds of the epoch scored. */
  epochTs: number;
  /** Total veAERO this holder had on pools that epoch. */
  budget: number;
  rows: ScoredVote[];
  earnedUsd: number;
  /** Pools the holder voted for that have no settled record for this epoch — counted, never silently dropped. */
  unscored: number;
}

/**
 * What a set of cast votes earned in one settled epoch.
 *
 * Pure: it takes the epoch history the caller already fetched, so the same
 * numbers can be checked in a test without a chain.
 *
 * The share is computed against the pool's *settled* weight, which is the
 * denominator Aerodrome actually divided by — not against the weight any scan
 * happened to see mid-week. That is the whole point of scoring a closed epoch:
 * there is nothing left to estimate.
 */
export function scoreVotes(
  votes: CastVote[],
  epochTs: number,
  epochsByPool: Map<string, { symbol: string; epochs: EpochData[] }>,
  prices: Map<string, { price: number; decimals: number }>,
): VoteReview {
  const rows: ScoredVote[] = [];
  let unscored = 0;
  let budget = 0;

  const total = votes.reduce((a, v) => a + v.weight, 0n);

  for (const v of votes) {
    const myVotes = Number(v.weight) / 10 ** VE_DECIMALS;
    budget += myVotes;

    const entry = epochsByPool.get(v.pool);
    const epoch = entry?.epochs.find((e) => Number(e.ts) === epochTs);
    if (!entry || !epoch) {
      unscored++;
      continue;
    }

    const poolVotes = Number(epoch.votes) / 10 ** VE_DECIMALS;
    const poolUsd = epochUsd(epoch, prices);
    // A pool with no recorded weight cannot have paid a share of anything; it
    // is reported as zero rather than dividing by nothing.
    const earnedUsd = poolVotes > 0 ? (poolUsd * myVotes) / poolVotes : 0;

    rows.push({
      pool: v.pool,
      symbol: entry.symbol,
      share: total > 0n ? Number(v.weight) / Number(total) : 0,
      myVotes,
      poolVotes,
      poolUsd,
      earnedUsd,
    });
  }

  rows.sort((a, b) => b.earnedUsd - a.earnedUsd);
  return {
    epochTs,
    budget,
    rows,
    earnedUsd: rows.reduce((a, r) => a + r.earnedUsd, 0),
    unscored,
  };
}

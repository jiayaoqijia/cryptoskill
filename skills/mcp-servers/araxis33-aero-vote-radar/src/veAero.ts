import { client } from "./chain.js";
import { VOTING_ESCROW_ABI } from "./abi.js";
import { VOTING_ESCROW_ADDRESS } from "./constants.js";
import { normalizeAddress } from "./util.js";

const VE_DECIMALS = 18;

export interface VeNftSummary {
  // string, not bigint/number: NFT IDs must round-trip through JSON (the MCP
  // tool responses are JSON) without precision loss or "cannot serialize BigInt" errors.
  id: string;
  votingPowerVeAero: number;
  /** Unix seconds. 0 both for a permanent lock and for one with nothing locked. */
  expiresAt: number;
  /** True only for a genuine permanent lock, so 0 above is never ambiguous. */
  isPermanent: boolean;
}

interface VeNftRaw {
  id: bigint;
  voting_amount: bigint;
  expires_at: bigint;
  is_permanent: boolean;
}

/** VotingEscrow's `locked` return: (amount, end, isPermanent). */
export type LockedBalance = readonly [bigint, bigint, boolean];

/**
 * Turns one raw veNFT struct into its summary shape. Pure, so it's
 * unit-testable without mocking RPC calls — unlike `fetchVeAeroPositions`,
 * which fetches live.
 */
export function toVeNftSummary(nft: VeNftRaw): VeNftSummary {
  return {
    id: nft.id.toString(),
    votingPowerVeAero: Number(nft.voting_amount) / 10 ** VE_DECIMALS,
    expiresAt: Number(nft.expires_at),
    isPermanent: nft.is_permanent,
  };
}

/**
 * Assembles the three per-NFT VotingEscrow reads into the raw struct shape.
 * Split out from the fetch so the decoding is testable without RPC.
 */
export function toVeNftRaw(id: bigint, votingPower: bigint, locked: LockedBalance): VeNftRaw {
  const [, end, isPermanent] = locked;
  return { id, voting_amount: votingPower, expires_at: end, is_permanent: isPermanent };
}

/**
 * Looks up all veAERO NFTs (locks) owned by an account and their current
 * voting power.
 *
 * Walks VotingEscrow's per-owner index instead of asking VeSugar for the whole
 * lot at once, because VeSugar's `byAccount` reverts on a public RPC for
 * accounts with many locks (see VOTING_ESCROW_ABI in abi.ts). Each read here
 * returns one value, so nothing scales with how much the account has voted.
 *
 * Two multicalls total, regardless of lock count: one to read the id list, one
 * to read voting power and lock terms for every id.
 *
 * The address is checksummed first, so a lowercase address from a CLI argument
 * gets a result rather than a raw "Address ... is invalid" error.
 */
export async function fetchVeAeroPositions(account: string): Promise<VeNftSummary[]> {
  const owner = normalizeAddress(account);

  const lockCount = await client.readContract({
    address: VOTING_ESCROW_ADDRESS,
    abi: VOTING_ESCROW_ABI,
    functionName: "balanceOf",
    args: [owner],
  });

  if (lockCount === 0n) return [];

  const indexes = Array.from({ length: Number(lockCount) }, (_, i) => BigInt(i));
  const ids = await client.multicall({
    allowFailure: false,
    contracts: indexes.map((index) => ({
      address: VOTING_ESCROW_ADDRESS,
      abi: VOTING_ESCROW_ABI,
      functionName: "ownerToNFTokenIdList" as const,
      args: [owner, index] as const,
    })),
  });

  // An out-of-range index answers 0 rather than reverting, so a token id of 0
  // means "no lock here" (id 0 is never minted) and is dropped rather than
  // queried. Guards against a balanceOf that moved between the two calls.
  const ownedIds = ids.filter((id) => id !== 0n);
  if (ownedIds.length === 0) return [];

  const reads = await client.multicall({
    allowFailure: false,
    contracts: ownedIds.flatMap((id) => [
      {
        address: VOTING_ESCROW_ADDRESS,
        abi: VOTING_ESCROW_ABI,
        functionName: "balanceOfNFT" as const,
        args: [id] as const,
      },
      {
        address: VOTING_ESCROW_ADDRESS,
        abi: VOTING_ESCROW_ABI,
        functionName: "locked" as const,
        args: [id] as const,
      },
    ]),
  });

  return ownedIds.map((id, i) =>
    toVeNftSummary(toVeNftRaw(id, reads[i * 2] as bigint, reads[i * 2 + 1] as unknown as LockedBalance)),
  );
}

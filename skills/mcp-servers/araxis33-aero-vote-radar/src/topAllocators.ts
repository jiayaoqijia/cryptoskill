import { CHAIN_NAMES } from "./radar.js";
import { readCooldown, readStakeOn, type StakeOnChain } from "./stakes.js";

/**
 * Where the best sAERO allocators are pointed right now (asked for in a DM on
 * Oct 26: "copy allocating based on the best allocators").
 *
 * The ranking is dromos.kitchen's open leaderboard: per sAERO position of
 * 10,000+, what it earned over the last 7 days per sAERO staked. It doesn't
 * say where a position is allocated, so each of the top ones is read from the
 * LeafVoter on every network, as the wallet lookup does. A position that moved
 * after earning its rank shows a split that hasn't earned anything yet, so the
 * time of the last move goes in the file too.
 */

export const DROMOS_BOARD_URL = "https://dromos.kitchen/aero-analytics/leaderboard.json";
export const TOP_ALLOCATORS = 10;
const FETCH_TIMEOUT_MS = 30_000;

/** dromos.kitchen's leaderboard; `p["7d"]` is [rank or null, USD earned, APR as a fraction, moves]. */
export interface DromosBoard {
  asOf: string;
  minSize: number;
  positions: {
    id: string;
    owner: string;
    contract: boolean;
    size: number;
    p: Record<string, [number | null, number, number, number]>;
  }[];
}

export interface TopSlice {
  chain: string;
  gauge: string;
  /** Share of the sAERO the position has placed, 0–1. */
  share: number;
}

export interface TopPosition {
  rank: number;
  id: string;
  owner: string;
  contract: boolean;
  sAero: number;
  earned7d: number;
  apr7d: number;
  moves7d: number;
  /** Unix seconds of the latest move on any network, 0 if it never allocated. */
  lastMoved: number;
  split: TopSlice[];
}

export interface TopAllocatorsFile {
  checkedAt: string;
  source: string;
  boardAsOf: string;
  positions: TopPosition[];
  /** Every position counted once, whatever its size: the pools the top ones agree on. */
  together: TopSlice[];
}

/** The `n` best-ranked positions over the last 7 days. */
export function pickTop(board: DromosBoard, n = TOP_ALLOCATORS): DromosBoard["positions"] {
  return board.positions
    .filter((p) => p.p["7d"]?.[0] != null)
    .sort((a, b) => (a.p["7d"][0] as number) - (b.p["7d"][0] as number))
    .slice(0, n);
}

/** A position's allocations on every network as shares of what it has placed, largest first. */
export function splitOf(chains: Record<string, StakeOnChain>): TopSlice[] {
  const parts = Object.entries(chains).flatMap(([chain, c]) =>
    c.allocations.filter((a) => a.amount > 0).map((a) => ({ chain, gauge: a.gauge.toLowerCase(), amount: a.amount })),
  );
  const total = parts.reduce((s, x) => s + x.amount, 0);
  if (total <= 0) return [];
  return parts.map(({ chain, gauge, amount }) => ({ chain, gauge, share: amount / total })).sort((a, b) => b.share - a.share);
}

/** Average of the positions' splits, each position weighing the same; positions with no split are left out. */
export function together(positions: readonly Pick<TopPosition, "split">[]): TopSlice[] {
  const placed = positions.filter((p) => p.split.length > 0);
  const sum = new Map<string, TopSlice>();
  for (const p of placed)
    for (const s of p.split) {
      const key = `${s.chain}:${s.gauge}`;
      const cur = sum.get(key) ?? { chain: s.chain, gauge: s.gauge, share: 0 };
      cur.share += s.share / placed.length;
      sum.set(key, cur);
    }
  return [...sum.values()].sort((a, b) => b.share - a.share);
}

export function buildTopAllocators(
  board: DromosBoard,
  reads: ReadonlyMap<string, Record<string, StakeOnChain>>,
  now: Date,
  n = TOP_ALLOCATORS,
): TopAllocatorsFile {
  const positions: TopPosition[] = pickTop(board, n).map((p) => {
    const [rank, earned, apr, moves] = p.p["7d"];
    const chains = reads.get(p.id) ?? {};
    return {
      rank: rank as number,
      id: p.id,
      owner: p.owner,
      contract: p.contract,
      sAero: p.size,
      earned7d: earned,
      apr7d: apr,
      moves7d: moves,
      lastMoved: Math.max(0, ...Object.values(chains).map((c) => c.lastAllocated)),
      split: splitOf(chains),
    };
  });
  return { checkedAt: now.toISOString(), source: "dromos.kitchen", boardAsOf: board.asOf, positions, together: together(positions) };
}

/** Reads the leaderboard and the top positions' splits on every network. Throws if any network fails, so a partial split never ships. */
export async function scanTopAllocators(now: Date, n = TOP_ALLOCATORS): Promise<TopAllocatorsFile> {
  const res = await fetch(DROMOS_BOARD_URL, { signal: AbortSignal.timeout(FETCH_TIMEOUT_MS) });
  if (!res.ok) throw new Error(`dromos.kitchen HTTP ${res.status}`);
  const board = (await res.json()) as DromosBoard;
  if (!Array.isArray(board.positions)) throw new Error("dromos.kitchen: no positions in the leaderboard");
  const top = pickTop(board, n);
  const reads = new Map<string, Record<string, StakeOnChain>>(top.map((p) => [p.id, {}]));
  await Promise.all(
    Object.keys(CHAIN_NAMES).map(async (chain) => {
      const cooldown = await readCooldown(chain);
      for (const p of top) reads.get(p.id)![chain] = await readStakeOn(chain, BigInt(p.id), cooldown);
    }),
  );
  return buildTopAllocators(board, reads, now, n);
}

import { client } from "./chain.js";
import type { PoolInfo } from "./pools.js";

/**
 * Raw, continuously-growing fee counters for every ranked pool, written next to
 * the snapshot on each scheduled run.
 *
 * Why this exists: the snapshot's `latestEpochFees` cannot show how revenue
 * flows WITHIN a week. Voter fees land in the rewards contract as one lump
 * when the epoch flips (measured on 117 snapshots, 2026-08-28..09-27: all of
 * it in the first 12 hours, zero afterwards), so any window shorter than a
 * week measures that lump, not the pool. Aero's Predictive Allocation (from
 * 2026-10-22) streams revenue continuously and lets an allocation move every
 * 48 hours — the question "how long does a pool's revenue hold up?" needs the
 * underlying flow, and that flow is readable straight off the pools:
 *
 * - Slipstream (CL) pools keep `gaugeFees()` — fees owed to the gauge, i.e. to
 *   voters, since the gauge last collected. It grows with every swap and drops
 *   back when the gauge collects at the epoch flip.
 * - Classic v2 pools keep a fee index per token (`index0`/`index1`, fees per LP
 *   token, scaled by 1e18) that only ever grows. The gauge's share between two
 *   reads is the index growth times the LP the gauge holds.
 *
 * Amounts are stored raw (strings, as JSON cannot hold these integers) with the
 * token addresses, so a later analysis can value them at whatever price it
 * chooses — the fixed-price method is what makes the comparison clean.
 */

export type FeeCounter =
  | { pool: string; kind: "cl"; tokens: [string, string]; gaugeFees: [string, string] }
  | { pool: string; kind: "v2"; tokens: [string, string]; index: [string, string]; gaugeLp: string };

export interface FeeStreamFile {
  generatedAt: string;
  pools: FeeCounter[];
}

const FEE_ABI = [
  {
    type: "function",
    name: "gaugeFees",
    stateMutability: "view",
    inputs: [],
    outputs: [{ type: "uint128", name: "token0" }, { type: "uint128", name: "token1" }],
  },
  { type: "function", name: "index0", stateMutability: "view", inputs: [], outputs: [{ type: "uint256" }] },
  { type: "function", name: "index1", stateMutability: "view", inputs: [], outputs: [{ type: "uint256" }] },
  { type: "function", name: "balanceOf", stateMutability: "view", inputs: [{ type: "address" }], outputs: [{ type: "uint256" }] },
] as const;

/**
 * Reads every pool's counters. One multicall at a time, never concurrently —
 * the same rule `fetchActivePools` follows, because the shared public RPC drops
 * whole overlapping bursts. A pool whose reads fail is simply left out.
 */
export async function readFeeCounters(pools: readonly PoolInfo[]): Promise<FeeCounter[]> {
  const addr = (p: PoolInfo) => p.address as `0x${string}`;

  const cl = await client.multicall({
    contracts: pools.map((p) => ({ address: addr(p), abi: FEE_ABI, functionName: "gaugeFees" }) as const),
    allowFailure: true,
  });

  // A pool without gaugeFees() is a classic pool; read its fee index instead.
  const classic = pools.filter((_, i) => cl[i].status !== "success");
  const call = (fn: "index0" | "index1") =>
    client.multicall({
      contracts: classic.map((p) => ({ address: addr(p), abi: FEE_ABI, functionName: fn }) as const),
      allowFailure: true,
    });
  const index0 = await call("index0");
  const index1 = await call("index1");
  const gaugeLp = await client.multicall({
    contracts: classic.map(
      (p) => ({ address: addr(p), abi: FEE_ABI, functionName: "balanceOf", args: [p.gauge as `0x${string}`] }) as const,
    ),
    allowFailure: true,
  });

  const out: FeeCounter[] = [];
  pools.forEach((p, i) => {
    const r = cl[i];
    if (r.status === "success") {
      const [a, b] = r.result as readonly [bigint, bigint];
      out.push({ pool: p.address.toLowerCase(), kind: "cl", tokens: [p.token0.toLowerCase(), p.token1.toLowerCase()], gaugeFees: [a.toString(), b.toString()] });
    }
  });
  classic.forEach((p, j) => {
    if (index0[j].status !== "success" || index1[j].status !== "success" || gaugeLp[j].status !== "success") return;
    out.push({
      pool: p.address.toLowerCase(),
      kind: "v2",
      tokens: [p.token0.toLowerCase(), p.token1.toLowerCase()],
      index: [String(index0[j].result), String(index1[j].result)],
      gaugeLp: String(gaugeLp[j].result),
    });
  });
  return out;
}

/**
 * Raw token amounts that reached voters between two reads of the same pool.
 *
 * CL: `gaugeFees` grows until the gauge collects, then restarts from zero, so a
 * drop means a collection happened in between and the later reading is what
 * accrued since (the part accrued just before the collection is not visible).
 * v2: the index never falls; the gauge's share is the growth times the LP it
 * holds at the later read, divided by the index's 1e18 scale.
 */
export function accruedBetween(prev: FeeCounter, next: FeeCounter): [bigint, bigint] {
  if (prev.kind === "cl" && next.kind === "cl") {
    return [0, 1].map((k) => {
      const a = BigInt(prev.gaugeFees[k]);
      const b = BigInt(next.gaugeFees[k]);
      return b >= a ? b - a : b;
    }) as [bigint, bigint];
  }
  if (prev.kind === "v2" && next.kind === "v2") {
    const lp = BigInt(next.gaugeLp);
    return [0, 1].map((k) => {
      const grow = BigInt(next.index[k]) - BigInt(prev.index[k]);
      return grow > 0n ? (grow * lp) / 10n ** 18n : 0n;
    }) as [bigint, bigint];
  }
  throw new Error(`pool ${next.pool} changed kind between reads (${prev.kind} -> ${next.kind})`);
}

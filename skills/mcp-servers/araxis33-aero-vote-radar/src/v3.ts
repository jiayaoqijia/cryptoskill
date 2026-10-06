import { parseAbi, parseAbiItem, type Address } from "viem";

/**
 * Reader for Aero (MetaDEX v3) — the system that replaces weekly veAERO voting
 * on 2026-10-22. Nothing here runs against live data yet: on Arc the
 * FactoryRegistry is deployed but `leafVoter()` is still zero and there are no
 * gauge factories (checked 2026-10-06), and the other chains have no addresses
 * at all. The shapes follow the public source, `dromos-labs/metadex-public` at
 * 2026-10-02, and Dromos Labs' own revenue methodology
 * (`dromos-labs/aerov3_analytics_alpha`, queries/revenue/METHODOLOGY.md):
 *
 * - Revenue to sAERO allocators = fees from staked liquidity, swept to each
 *   gauge's VotingRewardsManager as `FeesCollected(gauge, token, amount)` on no
 *   fixed cadence, plus incentive programs that stream at a constant rate over
 *   `[start, end)` (`rate` is tokens per second scaled by 1e18).
 * - The gauge list comes from the FactoryRegistry: gauge factories → gauges →
 *   rewards contract (`gaugeToRewards`) and pool (`gaugeToTarget`). No log scan.
 * - A gauge's weight is the LeafVoter's decaying point (`bias − slope·Δt`) plus
 *   permanent stake. ASSUMPTION to verify at launch: that this is the weight
 *   allocator revenue is split by (the rewards contract checkpoints the booked
 *   allocation, which should match).
 *
 * Reads go one call at a time over a batching transport rather than through
 * multicall3, which a new chain may not have.
 */

/** PRECISION in metadex V3/src/libraries/ProtocolConstants.sol; incentive `rate` is scaled by it. */
export const V3_PRECISION = 10n ** 18n;

export const REGISTRY_ABI = parseAbi([
  "function leafVoter() view returns (address)",
  "function gaugeFactories() view returns (address[])",
  "function factoryToGauges(address) view returns (address[])",
  "function gaugeToRewards(address) view returns (address)",
  "function gaugeToTarget(address) view returns (address)",
]);

export const LEAF_VOTER_ABI = parseAbi([
  "struct Point { int128 bias; int128 slope; uint48 ts; uint128 permanentStakeBalance; }",
  "function gaugeStates(address) view returns (uint128 ceiling, uint128 claimed, uint48 lastSettlement, bool isRegistered, bool isActivated, uint128 surplus, uint256 lastIndex, uint256 lastTimeIndex, Point point)",
]);

export const REWARDS_ABI = parseAbi([
  "struct IncentiveProgram { address token; uint256 amount; uint256 rate; uint48 start; uint48 end; address creator; }",
  "function incentiveCount() view returns (uint256)",
  "function incentives(uint256[] programIds) view returns (IncentiveProgram[])",
]);

export const FEES_COLLECTED = parseAbiItem("event FeesCollected(address indexed _gauge, address indexed _token, uint256 _amount)");

export interface V3Gauge {
  gauge: Address;
  pool: Address;
  rewards: Address;
}

export interface GaugePoint {
  bias: bigint;
  slope: bigint;
  ts: number;
  permanentStakeBalance: bigint;
}

export interface IncentiveProgram {
  token: Address;
  amount: bigint;
  rate: bigint;
  start: number;
  end: number;
}

/** A gauge's weight at `nowSec`: the decaying part never goes below zero, permanent stake does not decay. */
export function gaugeWeightAt(p: GaugePoint, nowSec: number): bigint {
  const decayed = p.bias - p.slope * BigInt(Math.max(0, nowSec - p.ts));
  return (decayed > 0n ? decayed : 0n) + p.permanentStakeBalance;
}

/**
 * Tokens per second (raw, unscaled) each token is streaming to the gauge's
 * allocators right now: the sum of programs with `start <= now < end`. A
 * program that has not started or has ended streams nothing.
 */
export function incentiveRatesNow(programs: readonly IncentiveProgram[], nowSec: number): Map<string, number> {
  const out = new Map<string, number>();
  for (const p of programs) {
    if (p.start > nowSec || p.end <= nowSec) continue;
    const perSec = Number(p.rate) / Number(V3_PRECISION);
    const key = p.token.toLowerCase();
    out.set(key, (out.get(key) ?? 0) + perSec);
  }
  return out;
}

export interface TokenPrice {
  decimals: number;
  priceUsd: number;
}

export interface V3GaugeYield {
  /** Fees swept to allocators over the window, per day. */
  feesUsdPerDay: number;
  /** Incentives streaming right now, per day. */
  incentivesUsdPerDay: number;
  /** What 10,000 units of allocation would earn per day at the gauge's current weight (marginal, before your own dilution). */
  usdPerDayPer10k: number | null;
  /** True when some earned token had no price, so the figures are understated. */
  partial: boolean;
}

/**
 * The per-day figure for one gauge: realised fees over the window (they are
 * swept in lumps, so a single sweep says little — the window evens that out)
 * plus incentives at their current stream rate, over the gauge's weight.
 */
export function v3GaugeYield(input: {
  feesCollected: readonly { token: string; amount: bigint }[];
  windowHours: number;
  incentiveRates: ReadonlyMap<string, number>;
  weight: bigint;
  priceOf: (token: string) => TokenPrice | undefined;
}): V3GaugeYield {
  let partial = false;
  const usd = (token: string, raw: number) => {
    const p = input.priceOf(token.toLowerCase());
    if (!p || !(p.priceUsd > 0)) {
      if (raw > 0) partial = true;
      return 0;
    }
    return (raw / 10 ** p.decimals) * p.priceUsd;
  };
  let fees = 0;
  for (const f of input.feesCollected) fees += usd(f.token, Number(f.amount));
  const feesUsdPerDay = input.windowHours > 0 ? fees / (input.windowHours / 24) : 0;
  let incentivesUsdPerDay = 0;
  for (const [token, perSec] of input.incentiveRates) incentivesUsdPerDay += usd(token, perSec * 86_400);
  const weight = Number(input.weight) / 1e18;
  return {
    feesUsdPerDay,
    incentivesUsdPerDay,
    usdPerDayPer10k: weight > 0 ? ((feesUsdPerDay + incentivesUsdPerDay) / weight) * 10_000 : null,
    partial,
  };
}

/** The part of a viem public client this module uses, so tests can pass a fake. */
export interface V3Client {
  readContract(args: { address: Address; abi: readonly unknown[]; functionName: string; args?: readonly unknown[] }): Promise<unknown>;
  getLogs(args: { address: Address | Address[]; event: typeof FEES_COLLECTED; fromBlock: bigint; toBlock: bigint }): Promise<
    readonly { address?: Address; args: { _gauge?: Address; _token?: Address; _amount?: bigint } }[]
  >;
}

const read = <T>(c: V3Client, address: Address, abi: readonly unknown[], functionName: string, args?: readonly unknown[]) =>
  c.readContract({ address, abi, functionName, args }) as Promise<T>;

/** Every gauge the registry knows, with its pool and rewards contract. Empty before launch. */
export async function readV3Gauges(c: V3Client, registry: Address): Promise<{ leafVoter: Address; gauges: V3Gauge[] }> {
  const leafVoter = await read<Address>(c, registry, REGISTRY_ABI, "leafVoter");
  const factories = await read<readonly Address[]>(c, registry, REGISTRY_ABI, "gaugeFactories");
  const gauges: V3Gauge[] = [];
  for (const f of factories) {
    for (const gauge of await read<readonly Address[]>(c, registry, REGISTRY_ABI, "factoryToGauges", [f])) {
      const rewards = await read<Address>(c, registry, REGISTRY_ABI, "gaugeToRewards", [gauge]);
      const pool = await read<Address>(c, registry, REGISTRY_ABI, "gaugeToTarget", [gauge]);
      gauges.push({ gauge, pool, rewards });
    }
  }
  return { leafVoter, gauges };
}

/** The LeafVoter's weight point for a gauge. */
export async function readGaugePoint(c: V3Client, leafVoter: Address, gauge: Address): Promise<GaugePoint> {
  const r = await read<readonly unknown[]>(c, leafVoter, LEAF_VOTER_ABI, "gaugeStates", [gauge]);
  const p = r[8] as { bias: bigint; slope: bigint; ts: number; permanentStakeBalance: bigint };
  return { bias: p.bias, slope: p.slope, ts: Number(p.ts), permanentStakeBalance: p.permanentStakeBalance };
}

/** Every incentive program ever created on one rewards contract (ids start at 1). */
export async function readIncentivePrograms(c: V3Client, rewards: Address): Promise<IncentiveProgram[]> {
  const count = Number(await read<bigint>(c, rewards, REWARDS_ABI, "incentiveCount"));
  if (count === 0) return [];
  const ids = Array.from({ length: count }, (_, i) => BigInt(i + 1));
  const progs = await read<readonly { token: Address; amount: bigint; rate: bigint; start: number; end: number }[]>(
    c,
    rewards,
    REWARDS_ABI,
    "incentives",
    [ids],
  );
  return progs.map((p) => ({ token: p.token, amount: p.amount, rate: p.rate, start: Number(p.start), end: Number(p.end) }));
}

/** `FeesCollected` from the given rewards contracts over a block range, in chunks of `step` blocks. */
export async function readFeesCollected(
  c: V3Client,
  rewards: readonly Address[],
  fromBlock: bigint,
  toBlock: bigint,
  step = 10_000n,
): Promise<{ rewards: Address; gauge: Address; token: Address; amount: bigint }[]> {
  if (rewards.length === 0) return [];
  const out: { rewards: Address; gauge: Address; token: Address; amount: bigint }[] = [];
  for (let from = fromBlock; from <= toBlock; from += step) {
    const to = from + step - 1n < toBlock ? from + step - 1n : toBlock;
    const logs = await c.getLogs({ address: [...rewards], event: FEES_COLLECTED, fromBlock: from, toBlock: to });
    for (const l of logs) {
      if (!l.args._gauge || !l.args._token || l.args._amount === undefined) continue;
      out.push({ rewards: (l.address ?? rewards[0]) as Address, gauge: l.args._gauge, token: l.args._token, amount: l.args._amount });
    }
  }
  return out;
}

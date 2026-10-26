import { parseAbi, parseAbiItem, type Address } from "viem";

/**
 * Reader for Aero (MetaDEX v3) — the system that replaced weekly veAERO
 * voting on 2026-10-22. Live on all 7 networks since launch (Arc included:
 * its FactoryRegistry now has gauge factories and a non-zero `leafVoter()`).
 * The shapes follow the public source, `dromos-labs/metadex-public` at
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

export const POOL_META_ABI = parseAbi([
  "function token0() view returns (address)",
  "function token1() view returns (address)",
  "function tickSpacing() view returns (int24)",
  "function stable() view returns (bool)",
  "function symbol() view returns (string)",
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
    readonly { address?: Address; blockNumber?: bigint | null; args: { _gauge?: Address; _token?: Address; _amount?: bigint } }[]
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

export interface PoolMeta {
  symbol0: string;
  symbol1: string;
  /** "CL<tickSpacing>" for Slipstream pools, "sAMM" / "vAMM" for basic stable / volatile pools. */
  kind: string;
}

/** Token symbols and pool type, for display; undefined when the pool does not answer like either pool kind. */
export async function readPoolMeta(c: V3Client, pool: Address, symbols: Map<string, string>): Promise<PoolMeta | undefined> {
  try {
    const [t0, t1, kind] = await Promise.all([
      read<Address>(c, pool, POOL_META_ABI, "token0"),
      read<Address>(c, pool, POOL_META_ABI, "token1"),
      // Aero's basic pools have no `stable()`; their LP symbol starts "sAMM" / "vAMM" ("vAMMV2-AERO/WETH").
      read<number>(c, pool, POOL_META_ABI, "tickSpacing").then(
        (ts) => `CL${ts}`,
        () => read<string>(c, pool, POOL_META_ABI, "symbol").then((s) => (s.startsWith("sAMM") ? "sAMM" : "vAMM")),
      ),
    ]);
    const sym = async (t: Address) => {
      const k = t.toLowerCase();
      if (!symbols.has(k)) symbols.set(k, await read<string>(c, t, POOL_META_ABI, "symbol").catch(() => "?"));
      return symbols.get(k)!;
    };
    const [symbol0, symbol1] = await Promise.all([sym(t0), sym(t1)]);
    return { symbol0, symbol1, kind };
  } catch {
    return undefined;
  }
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

/** Aero goes live at 2026-10-22 00:00 UTC; no allocator fees exist before it, so the fee window starts no earlier. */
export const AERO_LAUNCH_TS = Date.UTC(2026, 9, 22) / 1000;
/** Fee window, the same 96 h the per-day fee figure uses (src/feeRate.ts). */
export const V3_WINDOW_HOURS = 96;
/** Base produces a block every 2 s; used to turn the fee window into a block range. */
export const BASE_BLOCK_TIME_SEC = 2;
/** Rewards contracts per getLogs filter, so a public RPC is not handed hundreds of addresses at once. */
export const V3_LOG_ADDRESS_CHUNK = 100;
/** Gauges whose per-gauge reads run together. */
export const V3_READ_GROUP = 10;
/** Blocks per getLogs call: the cap of the logs RPC (V3_LOGS_RPC_URL). */
export const V3_LOG_BLOCK_STEP = 1_000n;

/** The FactoryRegistry address in one of Aero's deployment files (`deployment-addresses/<chain>.json`). */
export function registryFromDeployment(file: Record<string, unknown>): Address | undefined {
  for (const [k, v] of Object.entries(file)) {
    if (k.toLowerCase() === "factoryregistry" && typeof v === "string" && /^0x[0-9a-fA-F]{40}$/.test(v)) return v as Address;
  }
  return undefined;
}

export interface V3ScanGauge extends V3GaugeYield {
  /** Network the gauge lives on ("base", "optimism", …). */
  chain: string;
  gauge: Address;
  pool: Address;
  /** Allocation weight right now, in sAERO. */
  weight: number;
  /** Fees per day over the last 24 h only, to show whether a pool is cooling or rising against the window. */
  fees24hUsdPerDay: number;
  symbol0?: string;
  symbol1?: string;
  kind?: string;
  /** How steadily the pool has paid over the hourly history (v3History.ts); absent until it has enough hours. */
  steady?: V3Steadiness;
}

/** Hourly samples of what 10,000 sAERO would earn a day in the pool: how many held up, out of how many, their average and low. */
export interface V3Steadiness {
  held: number;
  of: number;
  avgPer10k: number;
  minPer10k: number;
}

/** Smallest block span a refused getLogs call is split down to before splitting its addresses instead. */
export const V3_LOG_MIN_BLOCKS = 50n;

export interface V3ScanFile {
  checkedAt: string;
  chain: string;
  /** no-addresses: no deployment file yet; not-live: registry deployed but no voter; live: gauges read. */
  status: "no-addresses" | "not-live" | "live";
  registry?: Address;
  leafVoter?: Address;
  /** Hours of fees actually behind the figures — shorter than V3_WINDOW_HOURS in the first days after launch. */
  windowHours: number;
  gauges: V3ScanGauge[];
  /** Per network, when several are scanned into one file; `error` is why a network has no rows this time. */
  chains?: Record<string, { status: V3ScanFile["status"] | "error"; windowHours: number; gauges: number; error?: string }>;
}

const ZERO = /^0x0*$/;

/**
 * One pass over a chain's Aero contracts: every gauge's weight, its incentives
 * streaming now, and the fees swept to its allocators over the last
 * V3_WINDOW_HOURS (cut at launch). Sorted by what 10,000 sAERO would earn a day.
 */
export async function scanV3(
  c: V3Client & { getBlockNumber(): Promise<bigint> },
  registry: Address,
  opts: {
    chain: string;
    now: Date;
    priceOf: (tokens: string[]) => Promise<(token: string) => TokenPrice | undefined>;
    /** Seconds per block on this chain (Base 2, Arbitrum ~0.27, Robinhood ~0.1, Ethereum 12). */
    blockTimeSec?: number;
    /** Blocks per getLogs call to start from; refused calls are split further. */
    logStep?: bigint;
  },
): Promise<V3ScanFile> {
  const base = { checkedAt: opts.now.toISOString(), chain: opts.chain, registry };
  const { leafVoter, gauges } = await readV3Gauges(c, registry);
  if (ZERO.test(leafVoter) || gauges.length === 0) return { ...base, status: "not-live", leafVoter, windowHours: 0, gauges: [] };

  const nowSec = Math.floor(opts.now.getTime() / 1000);
  const windowSec = Math.max(0, Math.min(V3_WINDOW_HOURS * 3600, nowSec - AERO_LAUNCH_TS));
  const latest = await c.getBlockNumber();
  const blockTime = opts.blockTimeSec ?? BASE_BLOCK_TIME_SEC;
  const span = BigInt(Math.ceil(windowSec / blockTime));
  const dayBlocks = BigInt(Math.ceil(86_400 / blockTime));
  const fees: Awaited<ReturnType<typeof readFeesCollected>> = [];
  if (windowSec > 0) {
    const rewards = gauges.map((g) => g.rewards);
    for (let i = 0; i < rewards.length; i += V3_LOG_ADDRESS_CHUNK) {
      fees.push(...(await readFeesCollected(c, rewards.slice(i, i + V3_LOG_ADDRESS_CHUNK), latest > span ? latest - span : 0n, latest, opts.logStep ?? V3_LOG_BLOCK_STEP)));
    }
  }

  const rows: { g: V3Gauge; point: GaugePoint; programs: IncentiveProgram[]; meta?: PoolMeta }[] = [];
  const symbols = new Map<string, string>();
  // A few gauges at a time: the batching transport folds their calls into one request.
  for (let i = 0; i < gauges.length; i += V3_READ_GROUP) {
    rows.push(
      ...(await Promise.all(
        gauges.slice(i, i + V3_READ_GROUP).map(async (g) => ({
          g,
          point: await readGaugePoint(c, leafVoter, g.gauge),
          programs: await readIncentivePrograms(c, g.rewards),
          meta: await readPoolMeta(c, g.pool, symbols),
        })),
      )),
    );
  }
  const tokens = [...fees.map((f) => f.token), ...rows.flatMap((r) => r.programs.map((p) => p.token))];
  const priceOf = await opts.priceOf(tokens);

  const dayStart = latest > dayBlocks ? latest - dayBlocks : 0n;
  const out: V3ScanGauge[] = rows.map(({ g, point, programs, meta }) => {
    const weight = gaugeWeightAt(point, nowSec);
    const mine = fees.filter((f) => f.gauge.toLowerCase() === g.gauge.toLowerCase());
    const y = v3GaugeYield({
      feesCollected: mine,
      windowHours: windowSec / 3600,
      incentiveRates: incentiveRatesNow(programs, nowSec),
      weight,
      priceOf,
    });
    const day = v3GaugeYield({
      feesCollected: mine.filter((f) => f.block === undefined || f.block >= dayStart),
      windowHours: Math.min(24, windowSec / 3600),
      incentiveRates: new Map(),
      weight,
      priceOf,
    });
    return { chain: opts.chain, gauge: g.gauge, pool: g.pool, weight: Number(weight / 10n ** 12n) / 1e6, ...y, fees24hUsdPerDay: day.feesUsdPerDay, ...meta };
  });
  out.sort((a, b) => (b.usdPerDayPer10k ?? -1) - (a.usdPerDayPer10k ?? -1));
  return { ...base, status: "live", leafVoter, windowHours: windowSec / 3600, gauges: out };
}

/** `FeesCollected` from the given rewards contracts over a block range, in chunks of `step` blocks. */
export async function readFeesCollected(
  c: V3Client,
  rewards: readonly Address[],
  fromBlock: bigint,
  toBlock: bigint,
  step = 10_000n,
): Promise<{ rewards: Address; gauge: Address; token: Address; amount: bigint; block?: bigint }[]> {
  if (rewards.length === 0) return [];
  const out: { rewards: Address; gauge: Address; token: Address; amount: bigint; block?: bigint }[] = [];
  // Each public node caps getLogs its own way (block span, address count, result
  // count, or a plain 400/403), so a refused call is split in half — the range
  // first, then the address list — until it is accepted or cannot shrink.
  const get = async (addrs: readonly Address[], from: bigint, to: bigint): Promise<Awaited<ReturnType<V3Client["getLogs"]>>> => {
    try {
      return await c.getLogs({ address: [...addrs], event: FEES_COLLECTED, fromBlock: from, toBlock: to });
    } catch (err) {
      if (to - from + 1n > V3_LOG_MIN_BLOCKS) {
        const mid = from + (to - from) / 2n;
        return [...(await get(addrs, from, mid)), ...(await get(addrs, mid + 1n, to))];
      }
      if (addrs.length > 1) {
        const half = Math.ceil(addrs.length / 2);
        return [...(await get(addrs.slice(0, half), from, to)), ...(await get(addrs.slice(half), from, to))];
      }
      throw err;
    }
  };
  for (let from = fromBlock; from <= toBlock; from += step) {
    const to = from + step - 1n < toBlock ? from + step - 1n : toBlock;
    const logs = await get(rewards, from, to);
    for (const l of logs) {
      if (!l.args._gauge || !l.args._token || l.args._amount === undefined) continue;
      out.push({
        rewards: (l.address ?? rewards[0]) as Address,
        gauge: l.args._gauge,
        token: l.args._token,
        amount: l.args._amount,
        ...(l.blockNumber != null ? { block: l.blockNumber } : {}),
      });
    }
  }
  return out;
}

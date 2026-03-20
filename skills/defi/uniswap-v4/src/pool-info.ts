#!/usr/bin/env -S npx tsx
/**
 * pool-info.ts — Read Uniswap V4 pool state (price, tick, liquidity, fees).
 *
 * Read-only, no gas, no private key needed.
 * Uses StateView contract for clean decoded reads.
 */

import { Contract, JsonRpcProvider } from "ethers";
import { parseArgs, fatal, isMain } from "./lib/cli.js";
import {
  type SupportedChain,
  getChainConfig,
  resolveRpcUrl,
  ADDRESS_ZERO,
  FEE_TIERS,
} from "./lib/addresses.js";
import { resolveTokenInput, validateChain } from "./lib/validation.js";
import { computePoolId, makePoolKey, type PoolKey } from "./lib/v4-encoding.js";
import { makeProvider, assertRpcChain, assertHasBytecode } from "./lib/provider.js";

// ── ABI fragments ───────────────────────────────────────────────────
const STATE_VIEW_ABI = [
  "function getSlot0(bytes32 poolId) view returns (uint160 sqrtPriceX96, int24 tick, uint24 protocolFee, uint24 lpFee)",
  "function getLiquidity(bytes32 poolId) view returns (uint128 liquidity)",
];

const ERC20_ABI = [
  "function symbol() view returns (string)",
  "function decimals() view returns (uint8)",
];

// ── Token info helper ───────────────────────────────────────────────
async function getTokenInfo(
  address: string,
  provider: JsonRpcProvider
): Promise<{ symbol: string; decimals: number }> {
  if (address === ADDRESS_ZERO) return { symbol: "ETH", decimals: 18 };
  try {
    const token = new Contract(address, ERC20_ABI, provider);
    const [symbol, decimals] = await Promise.all([
      token.symbol() as Promise<string>,
      token.decimals() as Promise<bigint>,
    ]);
    return { symbol, decimals: Number(decimals) };
  } catch {
    return { symbol: "???", decimals: 18 };
  }
}

// ── Pool discovery ──────────────────────────────────────────────────
interface PoolResult {
  poolId: string;
  key: PoolKey;
  sqrtPriceX96: string;
  tick: number;
  protocolFee: number;
  lpFee: number;
  liquidity: string;
}

async function queryPool(stateView: Contract, key: PoolKey): Promise<PoolResult | null> {
  const poolId = computePoolId(key);
  try {
    const [slot0, liq] = await Promise.all([
      stateView.getSlot0(poolId) as Promise<[bigint, bigint, bigint, bigint]>,
      stateView.getLiquidity(poolId) as Promise<bigint>,
    ]);
    const sqrtPriceX96 = slot0[0];
    if (sqrtPriceX96 === 0n) return null; // pool doesn't exist
    return {
      poolId,
      key,
      sqrtPriceX96: sqrtPriceX96.toString(),
      tick: Number(slot0[1]),
      protocolFee: Number(slot0[2]),
      lpFee: Number(slot0[3]),
      liquidity: liq.toString(),
    };
  } catch {
    return null;
  }
}

/**
 * Find all pools for a token pair, return sorted by liquidity (highest first).
 * Fixes M-01: returns best pool, not first match.
 */
export async function findPools(
  token0: string,
  token1: string,
  chain: SupportedChain,
  rpcUrl: string,
  hooks: string = ADDRESS_ZERO
): Promise<PoolResult[]> {
  const cfg = getChainConfig(chain);
  const provider = makeProvider(chain, rpcUrl);
  await assertRpcChain(provider, chain);
  await assertHasBytecode(provider, cfg.stateView, "StateView");

  const stateView = new Contract(cfg.stateView, STATE_VIEW_ABI, provider);

  // Sort currencies numerically (V4 requirement)
  const [c0, c1] = BigInt(token0) < BigInt(token1) ? [token0, token1] : [token1, token0];

  const results: PoolResult[] = [];

  // Query all fee tiers in parallel
  const queries = FEE_TIERS.map(([fee, ts]) =>
    queryPool(stateView, makePoolKey(c0, c1, fee, ts, hooks))
  );
  const poolResults = await Promise.all(queries);

  for (const r of poolResults) {
    if (r) results.push(r);
  }

  // Sort by liquidity descending — best pool first
  results.sort((a, b) => {
    const liqA = BigInt(a.liquidity);
    const liqB = BigInt(b.liquidity);
    if (liqB > liqA) return 1;
    if (liqB < liqA) return -1;
    return 0;
  });

  return results;
}

// ── CLI ─────────────────────────────────────────────────────────────
const HELP = `pool-info.ts — Read Uniswap V4 pool state

Usage:
  npx tsx src/pool-info.ts --token0 <addr|ETH> --token1 <addr|ETH> [options]

Options:
  --token0 <addr|ETH>     First token address (or ETH)
  --token1 <addr|ETH>     Second token address (or ETH)
  --fee <bps>             Specific fee tier (omit to auto-detect best)
  --tick-spacing <int>    Specific tick spacing (required with --fee)
  --hooks <addr>          Hook contract (default: address(0))
  --chain <name>          base | ethereum | base-sepolia (default: base)
  --rpc <url>             RPC URL (or set BASE_RPC_URL / ETH_RPC_URL env)
  --json                  JSON output (default)
  --help                  Show this help

Env:
  BASE_RPC_URL            Default RPC for Base
  ETH_RPC_URL             Default RPC for Ethereum
  BASE_SEPOLIA_RPC_URL    Default RPC for Base Sepolia`;

async function main() {
  const { flags, booleans } = parseArgs();
  if (booleans.has("help") || booleans.has("h")) {
    console.log(HELP);
    process.exit(0);
  }

  const chainRaw = flags["chain"] ?? "base";
  validateChain(chainRaw);
  const chain = chainRaw as SupportedChain;

  const t0Raw = flags["token0"];
  const t1Raw = flags["token1"];
  if (!t0Raw || !t1Raw) fatal("--token0 and --token1 are required.");

  const t0 = resolveTokenInput(t0Raw, "token0");
  const t1 = resolveTokenInput(t1Raw, "token1");
  const rpcUrl = resolveRpcUrl(chain, flags["rpc"]);
  const hooks = flags["hooks"] ? resolveTokenInput(flags["hooks"], "hooks") : ADDRESS_ZERO;
  const cfg = getChainConfig(chain);

  // Specific fee tier or auto-detect
  if (flags["fee"] && flags["tick-spacing"]) {
    const fee = Number(flags["fee"]);
    const ts = Number(flags["tick-spacing"]);

    const provider = makeProvider(chain, rpcUrl);
    await assertRpcChain(provider, chain);
    await assertHasBytecode(provider, cfg.stateView, "StateView");

    const stateView = new Contract(cfg.stateView, STATE_VIEW_ABI, provider);

    const [c0, c1] = BigInt(t0) < BigInt(t1) ? [t0, t1] : [t1, t0];

    const result = await queryPool(stateView, makePoolKey(c0, c1, fee, ts, hooks));
    if (!result) {
      console.log(JSON.stringify({ success: false, error: "Pool not found or empty" }));
      process.exit(1);
    }

    const [info0, info1] = await Promise.all([
      getTokenInfo(result.key.currency0, provider),
      getTokenInfo(result.key.currency1, provider),
    ]);

    console.log(
      JSON.stringify(
        {
          success: true,
          chain,
          poolId: result.poolId,
          token0: { ...info0, address: result.key.currency0 },
          token1: { ...info1, address: result.key.currency1 },
          fee: result.key.fee,
          tickSpacing: result.key.tickSpacing,
          hooks: result.key.hooks,
          sqrtPriceX96: result.sqrtPriceX96,
          tick: result.tick,
          protocolFee: result.protocolFee,
          lpFee: result.lpFee,
          liquidity: result.liquidity,
        },
        null,
        2
      )
    );
  } else {
    // Auto-detect: find all pools, return best
    const pools = await findPools(t0, t1, chain, rpcUrl, hooks);
    if (pools.length === 0) {
      console.log(JSON.stringify({ success: false, error: "No V4 pool found for this pair" }));
      process.exit(1);
    }

    const best = pools[0];
    const provider = makeProvider(chain, rpcUrl);
    await assertRpcChain(provider, chain);

    const [info0, info1] = await Promise.all([
      getTokenInfo(best.key.currency0, provider),
      getTokenInfo(best.key.currency1, provider),
    ]);

    console.log(
      JSON.stringify(
        {
          success: true,
          chain,
          poolId: best.poolId,
          token0: { ...info0, address: best.key.currency0 },
          token1: { ...info1, address: best.key.currency1 },
          fee: best.key.fee,
          tickSpacing: best.key.tickSpacing,
          hooks: best.key.hooks,
          sqrtPriceX96: best.sqrtPriceX96,
          tick: best.tick,
          protocolFee: best.protocolFee,
          lpFee: best.lpFee,
          liquidity: best.liquidity,
          poolsScanned: pools.length,
        },
        null,
        2
      )
    );
  }
}

if (isMain(import.meta.url)) {
  main().catch((e: Error) => fatal(e.message));
}

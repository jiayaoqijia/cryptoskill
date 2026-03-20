#!/usr/bin/env -S npx tsx
/**
 * quote.ts — Quote swap amounts using V4Quoter (Quoter V2).
 *
 * Calls quoteExactInputSingle via eth_call (no gas, no tx, no private key).
 * Uses the on-chain Quoter contract which simulates the swap and reverts with the result.
 *
 * Fixes C-03 from PhD review: proper quoting in output token units.
 */

import { Contract } from "ethers";
import { parseArgs, log, fatal, isMain } from "./lib/cli.js";
import {
  type SupportedChain,
  getChainConfig,
  resolveRpcUrl,
} from "./lib/addresses.js";
import {
  resolveTokenInput,
  validateChain,
  parseAmount,
  sortCurrencies,
} from "./lib/validation.js";
import { makePoolKey } from "./lib/v4-encoding.js";
import { findPools } from "./pool-info.js";
import { makeProvider, assertRpcChain, assertHasBytecode } from "./lib/provider.js";

// ── V4Quoter ABI fragment ───────────────────────────────────────────
const QUOTER_ABI = [
  "function quoteExactInputSingle((( address,address,uint24,int24,address) poolKey, bool zeroForOne, uint128 exactAmount, bytes hookData)) returns (uint256 amountOut, uint256 gasEstimate)",
];

// ── CLI ─────────────────────────────────────────────────────────────
const HELP = `quote.ts — Quote Uniswap V4 swap amounts

Usage:
  npx tsx src/quote.ts --token-in <addr|ETH> --token-out <addr|ETH> --amount <wei> [options]

Options:
  --token-in <addr|ETH>   Input token
  --token-out <addr|ETH>  Output token
  --amount <wei>          Exact input amount in base units (wei)
  --fee <bps>             Specific fee tier (omit to use best pool)
  --tick-spacing <int>    Tick spacing (required with --fee)
  --chain <name>          base | ethereum | base-sepolia (default: base)
  --rpc <url>             RPC URL
  --json                  JSON output (default)
  --help                  Show this help

  Without --fee/--tick-spacing, auto-discovers the best pool by liquidity.

Env:
  BASE_RPC_URL            Default RPC for Base
  ETH_RPC_URL             Default RPC for Ethereum`;

async function main() {
  const { flags, booleans } = parseArgs();
  if (booleans.has("help") || booleans.has("h")) {
    console.log(HELP);
    process.exit(0);
  }

  const chainRaw = flags["chain"] ?? "base";
  validateChain(chainRaw);
  const chain = chainRaw as SupportedChain;

  const tokenInRaw = flags["token-in"];
  const tokenOutRaw = flags["token-out"];
  const amountRaw = flags["amount"];
  if (!tokenInRaw || !tokenOutRaw || !amountRaw) {
    fatal("--token-in, --token-out, and --amount are required.");
  }

  const tokenIn = resolveTokenInput(tokenInRaw, "token-in");
  const tokenOut = resolveTokenInput(tokenOutRaw, "token-out");
  const amount = parseAmount(amountRaw, "amount");
  const rpcUrl = resolveRpcUrl(chain, flags["rpc"]);
  const cfg = getChainConfig(chain);

  const provider = makeProvider(chain, rpcUrl);
  await assertRpcChain(provider, chain);
  await assertHasBytecode(provider, cfg.quoter, "V4Quoter");

  // Resolve pool
  const { currency0, currency1, zeroForOne } = sortCurrencies(tokenIn, tokenOut);

  let poolFee: number;
  let poolTickSpacing: number;

  if (flags["fee"] && flags["tick-spacing"]) {
    poolFee = Number(flags["fee"]);
    poolTickSpacing = Number(flags["tick-spacing"]);
  } else {
    // Auto-discover best pool
    log("Discovering best pool...");
    const pools = await findPools(tokenIn, tokenOut, chain, rpcUrl);
    if (pools.length === 0) {
      console.log(JSON.stringify({ success: false, error: "No V4 pool found for this pair" }));
      process.exit(1);
    }
    poolFee = pools[0].key.fee;
    poolTickSpacing = pools[0].key.tickSpacing;
    log(
      `Using pool: fee=${poolFee} tickSpacing=${poolTickSpacing} liquidity=${pools[0].liquidity}`
    );
  }

  const key = makePoolKey(currency0, currency1, poolFee, poolTickSpacing);

  // Call Quoter via eth_call (staticCall)
  const quoter = new Contract(cfg.quoter, QUOTER_ABI, provider);
  try {
    const result = await quoter.quoteExactInputSingle.staticCall({
      poolKey: [key.currency0, key.currency1, key.fee, key.tickSpacing, key.hooks],
      zeroForOne,
      exactAmount: amount,
      hookData: "0x",
    });

    const amountOut = result[0] as bigint;
    const gasEstimate = result[1] as bigint;

    console.log(
      JSON.stringify(
        {
          success: true,
          chain,
          tokenIn,
          tokenOut,
          amountIn: amount.toString(),
          amountOut: amountOut.toString(),
          gasEstimate: gasEstimate.toString(),
          pool: {
            currency0,
            currency1,
            fee: poolFee,
            tickSpacing: poolTickSpacing,
            zeroForOne,
          },
        },
        null,
        2
      )
    );
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    console.log(
      JSON.stringify(
        {
          success: false,
          error: `Quote failed: ${msg.slice(0, 200)}`,
          chain,
          tokenIn,
          tokenOut,
          amountIn: amount.toString(),
        },
        null,
        2
      )
    );
    process.exit(1);
  }
}

if (isMain(import.meta.url)) {
  main().catch((e: Error) => fatal(e.message));
}

#!/usr/bin/env -S npx tsx
/**
 * swap.ts — Execute swaps on Uniswap V4 via the Universal Router.
 *
 * Fixes ALL critical bugs from PhD review:
 *   C-01: Uses StateView for pool discovery (not PoolManager.getSlot0)
 *   C-02: Correct action bytes (SETTLE_ALL=0x0c)
 *   C-03: Proper quoting via V4Quoter before swap
 *   C-04: Clean ABI encoding via ethers (not bash/cast)
 * Fixes security issues:
 *   PT-001: No bash arithmetic (TypeScript BigInt)
 *   PT-002: No integer overflow (BigInt is arbitrary precision)
 *   PT-003: Private key from env var only
 */

import { Contract, Wallet } from "ethers";
import { parseArgs, log, fatal, isMain } from "./lib/cli.js";
import {
  type SupportedChain,
  getChainConfig,
  resolveRpcUrl,
  ADDRESS_ZERO,
} from "./lib/addresses.js";
import {
  resolveTokenInput,
  validateChain,
  parseAmount,
  parseSlippage,
  sortCurrencies,
  applySlippage,
  getPrivateKey,
  validateAddress,
} from "./lib/validation.js";
import { makeProvider, assertRpcChain, assertHasBytecode } from "./lib/provider.js";
import { buildExecuteCalldata, makePoolKey } from "./lib/v4-encoding.js";
import { findPools } from "./pool-info.js";

// ── ABI fragments ───────────────────────────────────────────────────
const UNIVERSAL_ROUTER_ABI = [
  "function execute(bytes commands, bytes[] inputs, uint256 deadline) payable",
];

const QUOTER_ABI = [
  "function quoteExactInputSingle(((address,address,uint24,int24,address) poolKey, bool zeroForOne, uint128 exactAmount, bytes hookData)) returns (uint256 amountOut, uint256 gasEstimate)",
];

const ERC20_ABI = [
  "function allowance(address owner, address spender) view returns (uint256)",
  "function approve(address spender, uint256 amount) returns (bool)",
];

const PERMIT2_ABI = [
  "function allowance(address user, address token, address spender) view returns (uint160, uint48, uint48)",
  "function approve(address token, address spender, uint160 amount, uint48 expiration)",
];

// ── CLI ─────────────────────────────────────────────────────────────
const HELP = `swap.ts — Execute a token swap on Uniswap V4 via the Universal Router

Usage:
  PRIVATE_KEY=0x... npx tsx src/swap.ts --token-in <addr|ETH> --token-out <addr|ETH> --amount <wei> [options]

Options:
  --token-in <addr|ETH>   Input token
  --token-out <addr|ETH>  Output token
  --amount <wei>          Input amount in base units (wei)
  --slippage <bps>        Slippage tolerance in basis points (default: 50 = 0.5%)
  --recipient <addr>      Recipient address (default: sender)
  --chain <name>          base | ethereum | base-sepolia (default: base)
  --rpc <url>             RPC URL
  --auto-approve          Auto-approve Permit2 if needed
  --json                  JSON output only
  --help                  Show this help

Env:
  PRIVATE_KEY             Wallet private key (REQUIRED)
  BASE_RPC_URL            Default RPC for Base
  ETH_RPC_URL             Default RPC for Ethereum`;

async function main() {
  const { flags, booleans } = parseArgs();
  if (booleans.has("help") || booleans.has("h")) {
    console.log(HELP);
    process.exit(0);
  }
  const jsonOutput = booleans.has("json");
  const autoApprove = booleans.has("auto-approve");

  // ── Parse & validate inputs ─────────────────────────────────────
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
  const slippageBps = parseSlippage(flags["slippage"] ?? "50");

  const rpcUrl = resolveRpcUrl(chain, flags["rpc"]);
  const cfg = getChainConfig(chain);
  const privateKey = getPrivateKey();

  const provider = makeProvider(chain, rpcUrl);
  await assertRpcChain(provider, chain);

  // Write-path safety: ensure we're talking to real contracts.
  await assertHasBytecode(provider, cfg.universalRouter, "Universal Router");
  await assertHasBytecode(provider, cfg.quoter, "V4Quoter");
  await assertHasBytecode(provider, cfg.permit2, "Permit2");
  if (tokenIn !== ADDRESS_ZERO) await assertHasBytecode(provider, tokenIn, "Token In (ERC20)");
  if (tokenOut !== ADDRESS_ZERO) await assertHasBytecode(provider, tokenOut, "Token Out (ERC20)");

  const wallet = new Wallet(privateKey, provider);
  const sender = wallet.address;

  const recipientFlag = flags["recipient"];
  const recipient = recipientFlag ? validateAddress(recipientFlag, "recipient") : sender;
  const recipientForCalldata = recipientFlag ? recipient : undefined;

  // ── Pool discovery ──────────────────────────────────────────────
  if (!jsonOutput) log("Discovering best pool...");
  const pools = await findPools(tokenIn, tokenOut, chain, rpcUrl);
  if (pools.length === 0) {
    const msg = "No V4 pool found for this token pair.";
    if (jsonOutput) {
      console.log(JSON.stringify({ success: false, error: msg }));
      process.exit(1);
    }
    fatal(msg);
  }

  const bestPool = pools[0];
  const { currency0, currency1, zeroForOne } = sortCurrencies(tokenIn, tokenOut);
  const key = makePoolKey(currency0, currency1, bestPool.key.fee, bestPool.key.tickSpacing);

  if (!jsonOutput) {
    log(`Pool: fee=${key.fee} tickSpacing=${key.tickSpacing} liquidity=${bestPool.liquidity}`);
  }

  // ── Quote expected output (fixes C-03) ──────────────────────────
  if (!jsonOutput) log("Quoting expected output...");
  const quoter = new Contract(cfg.quoter, QUOTER_ABI, provider);
  let expectedOut: bigint;
  try {
    const qResult = await quoter.quoteExactInputSingle.staticCall({
      poolKey: [key.currency0, key.currency1, key.fee, key.tickSpacing, key.hooks],
      zeroForOne,
      exactAmount: amount,
      hookData: "0x",
    });
    expectedOut = qResult[0] as bigint;
  } catch (err) {
    const msg = `Quote failed: ${
      err instanceof Error ? err.message.slice(0, 150) : String(err)
    }`;
    if (jsonOutput) {
      console.log(JSON.stringify({ success: false, error: msg }));
      process.exit(1);
    }
    fatal(msg);
  }

  const amountOutMin = applySlippage(expectedOut, slippageBps);
  if (!jsonOutput) {
    log(`Expected output: ${expectedOut.toString()}`);
    log(`Min output (${slippageBps}bps slippage): ${amountOutMin.toString()}`);
  }

  // ── Auto-approve if needed ──────────────────────────────────────
  if (tokenIn !== ADDRESS_ZERO && autoApprove) {
    const erc20 = new Contract(tokenIn, ERC20_ABI, wallet);
    const permit2Contract = new Contract(cfg.permit2, PERMIT2_ABI, wallet);

    // Check ERC20 → Permit2
    const erc20Allowance = (await erc20.allowance(sender, cfg.permit2)) as bigint;
    if (erc20Allowance < amount) {
      if (!jsonOutput) log("Auto-approving ERC20 → Permit2...");
      const tx = await erc20.approve(cfg.permit2, 2n ** 256n - 1n);
      await tx.wait();
      if (!jsonOutput) log(`  TX: ${tx.hash}`);
    }

    // Check Permit2 → Universal Router
    const [p2Amount, p2Expiry] = (await permit2Contract.allowance(
      sender,
      tokenIn,
      cfg.universalRouter
    )) as [bigint, bigint, bigint];
    const now = BigInt(Math.floor(Date.now() / 1000));
    if (p2Amount < amount || p2Expiry < now + 600n) {
      if (!jsonOutput) log("Auto-approving Permit2 → Universal Router...");
      const MAX_UINT160 = (1n << 160n) - 1n;
      const MAX_UINT48 = (1n << 48n) - 1n;
      const tx = await permit2Contract.approve(tokenIn, cfg.universalRouter, MAX_UINT160, MAX_UINT48);
      await tx.wait();
      if (!jsonOutput) log(`  TX: ${tx.hash}`);
    }
  }

  // ── Build and send swap transaction ─────────────────────────────
  const deadline = BigInt(Math.floor(Date.now() / 1000) + 300); // 5 min
  const { commands, inputs } = buildExecuteCalldata(
    key,
    zeroForOne,
    amount,
    amountOutMin,
    deadline,
    recipientForCalldata
  );

  const router = new Contract(cfg.universalRouter, UNIVERSAL_ROUTER_ABI, wallet);
  const ethValue = tokenIn === ADDRESS_ZERO ? amount : 0n;

  if (!jsonOutput) {
    log("Executing swap...");
    log(`  Chain: ${chain}`);
    log(`  Token In: ${tokenIn}`);
    log(`  Token Out: ${tokenOut}`);
    log(`  Amount: ${amount.toString()} wei`);
    log(`  Router: ${cfg.universalRouter}`);
  }

  try {
    const tx = await router.execute(commands, inputs, deadline, {
      value: ethValue,
    });
    const receipt = await tx.wait();

    const result = {
      success: true,
      txHash: tx.hash,
      chain,
      tokenIn,
      tokenOut,
      recipient,
      amount: amount.toString(),
      expectedOut: expectedOut.toString(),
      amountOutMin: amountOutMin.toString(),
      gasUsed: receipt?.gasUsed?.toString() ?? "unknown",
      explorer: `${cfg.explorerBase}/tx/${tx.hash}`,
    };

    if (jsonOutput) {
      console.log(JSON.stringify(result));
    } else {
      log("✅ Swap submitted!");
      log(`  TX: ${tx.hash}`);
      log(`  Explorer: ${result.explorer}`);
      log(`  Gas used: ${result.gasUsed}`);
    }
  } catch (err) {
    const msg = err instanceof Error ? err.message.slice(0, 300) : String(err);
    if (jsonOutput) {
      console.log(JSON.stringify({ success: false, error: msg }));
      process.exit(1);
    }
    fatal(`Swap failed: ${msg}`);
  }
}

if (isMain(import.meta.url)) {
  main().catch((e: Error) => fatal(e.message));
}

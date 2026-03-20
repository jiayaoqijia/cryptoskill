#!/usr/bin/env -S npx tsx
/**
 * approve.ts — Approve tokens for Permit2 + Universal Router (two-step flow).
 *
 * Step 1: ERC20.approve(Permit2, MAX_UINT256)
 * Step 2: Permit2.approve(token, UniversalRouter, MAX_UINT160, MAX_UINT48)
 *
 * Fixes M-05: uses max uint48 for consistent Permit2 expiry.
 * Fixes PT-003: private key from env var only.
 */

import { Contract, Wallet, MaxUint256 } from "ethers";
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
  getPrivateKey,
} from "./lib/validation.js";
import { makeProvider, assertRpcChain, assertHasBytecode } from "./lib/provider.js";

// ── Constants ───────────────────────────────────────────────────────
const MAX_UINT160 = (1n << 160n) - 1n;
const MAX_UINT48 = (1n << 48n) - 1n;

// ── ABI fragments ───────────────────────────────────────────────────
const ERC20_ABI = [
  "function approve(address spender, uint256 amount) returns (bool)",
  "function allowance(address owner, address spender) view returns (uint256)",
  "function symbol() view returns (string)",
];

const PERMIT2_ABI = [
  "function approve(address token, address spender, uint160 amount, uint48 expiration)",
  "function allowance(address user, address token, address spender) view returns (uint160 amount, uint48 expiration, uint48 nonce)",
];

// ── CLI ─────────────────────────────────────────────────────────────
const HELP = `approve.ts — Set up Permit2 approvals for Uniswap V4 swaps

Usage:
  PRIVATE_KEY=0x... npx tsx src/approve.ts --token <addr> [options]

Options:
  --token <addr>          ERC20 token to approve
  --chain <name>          base | ethereum | base-sepolia (default: base)
  --rpc <url>             RPC URL
  --json                  JSON output only
  --help                  Show this help

Env:
  PRIVATE_KEY             Wallet private key (REQUIRED, never pass on CLI)
  BASE_RPC_URL            Default RPC for Base
  ETH_RPC_URL             Default RPC for Ethereum`;

async function main() {
  const { flags, booleans } = parseArgs();
  if (booleans.has("help") || booleans.has("h")) {
    console.log(HELP);
    process.exit(0);
  }
  const jsonOutput = booleans.has("json");

  const chainRaw = flags["chain"] ?? "base";
  validateChain(chainRaw);
  const chain = chainRaw as SupportedChain;

  const tokenRaw = flags["token"];
  if (!tokenRaw) fatal("--token required.");
  const token = resolveTokenInput(tokenRaw, "token");
  if (token === ADDRESS_ZERO) {
    fatal("Cannot approve ETH (native). Only ERC20 tokens need approval.");
  }

  const rpcUrl = resolveRpcUrl(chain, flags["rpc"]);
  const cfg = getChainConfig(chain);
  const privateKey = getPrivateKey();

  const provider = makeProvider(chain, rpcUrl);
  await assertRpcChain(provider, chain);
  // Write-path safety: ensure we're talking to real contracts.
  await assertHasBytecode(provider, token, "ERC20 token");
  await assertHasBytecode(provider, cfg.permit2, "Permit2");
  await assertHasBytecode(provider, cfg.universalRouter, "Universal Router");

  const wallet = new Wallet(privateKey, provider);
  const sender = wallet.address;

  const erc20 = new Contract(token, ERC20_ABI, wallet);
  const permit2 = new Contract(cfg.permit2, PERMIT2_ABI, wallet);

  let symbol: string;
  try {
    symbol = await (erc20.symbol() as Promise<string>);
  } catch {
    symbol = "???";
  }

  if (!jsonOutput) log(`Setting up Permit2 approvals for ${symbol} (${token})...`);

  // Step 1: ERC20 approve Permit2
  let hash1 = "";
  const currentAllowance = (await erc20.allowance(sender, cfg.permit2)) as bigint;
  if (currentAllowance < MaxUint256 / 2n) {
    if (!jsonOutput) log("Step 1: Approving Permit2 to spend token...");
    const tx1 = await erc20.approve(cfg.permit2, MaxUint256);
    await tx1.wait();
    hash1 = tx1.hash;
    if (!jsonOutput) log(`  TX: ${hash1}`);
  } else {
    if (!jsonOutput) log("Step 1: Permit2 already approved (skipped).");
    hash1 = "already-approved";
  }

  // Step 2: Permit2 approve Universal Router
  let hash2 = "";
  const [currentAmount, currentExpiry] =
    (await permit2.allowance(sender, token, cfg.universalRouter)) as [
      bigint,
      bigint,
      bigint,
    ];
  const now = BigInt(Math.floor(Date.now() / 1000));
  if (currentAmount < MAX_UINT160 / 2n || currentExpiry < now + 86400n * 7n) {
    if (!jsonOutput) log("Step 2: Granting Universal Router allowance on Permit2...");
    const tx2 = await permit2.approve(token, cfg.universalRouter, MAX_UINT160, MAX_UINT48);
    await tx2.wait();
    hash2 = tx2.hash;
    if (!jsonOutput) log(`  TX: ${hash2}`);
  } else {
    if (!jsonOutput) log("Step 2: Universal Router already permitted (skipped).");
    hash2 = "already-approved";
  }

  const result = {
    success: true,
    token,
    symbol,
    chain,
    erc20ApproveTx: hash1,
    permit2ApproveTx: hash2,
  };

  if (jsonOutput) {
    console.log(JSON.stringify(result));
  } else {
    log("");
    log(`✅ Approvals set for ${symbol}`);
    log(`  ERC20 → Permit2: ${hash1}`);
    log(`  Permit2 → Router: ${hash2}`);
  }
}

if (isMain(import.meta.url)) {
  main().catch((e: Error) => fatal(e.message));
}

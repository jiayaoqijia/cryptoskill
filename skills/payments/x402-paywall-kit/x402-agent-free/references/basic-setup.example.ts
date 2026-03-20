/**
 * Example: Basic x402 agent setup (free edition).
 *
 * Uses @x402/fetch directly for simple detect-and-pay functionality.
 * No policy engine or logging — see @x402-kit/agent for the full version.
 *
 * Prerequisites:
 *   npm install @x402/fetch @x402/evm viem
 *
 * Environment:
 *   X402_WALLET_PRIVATE_KEY=0x...  (funded with USDC on Base)
 */

import { createWalletClient, createPublicClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { base } from "viem/chains";
import { wrapFetchWithPayment } from "@x402/fetch";
import { toClientEvmSigner, ExactEvmScheme } from "@x402/evm";

// Load wallet from environment (never hardcode!)
const privateKey = process.env.X402_WALLET_PRIVATE_KEY as `0x${string}`;
if (!privateKey) {
  throw new Error("X402_WALLET_PRIVATE_KEY environment variable is required");
}

const account = privateKeyToAccount(privateKey);

const walletClient = createWalletClient({
  account,
  chain: base,
  transport: http(),
});

const publicClient = createPublicClient({
  chain: base,
  transport: http(),
});

// Create x402 signer from viem wallet
const signer = toClientEvmSigner(
  {
    address: account.address,
    signTypedData: (message) => walletClient.signTypedData(message),
  },
  publicClient,
);

// Wrap fetch with x402 auto-pay
const x402Fetch = wrapFetchWithPayment(fetch, {
  schemes: [new ExactEvmScheme(signer)],
});

// Use it like regular fetch — 402 paywalls are handled automatically
async function main() {
  const response = await x402Fetch("https://api.example.com/premium/data");

  if (response.ok) {
    const data = await response.json();
    console.log("Got premium data:", data);
  } else if (response.status === 402) {
    console.log("Payment failed — check USDC balance on Base");
  } else {
    console.log("Request failed:", response.status);
  }
}

main().catch(console.error);

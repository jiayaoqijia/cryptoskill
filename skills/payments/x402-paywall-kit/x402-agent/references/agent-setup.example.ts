/**
 * Example: Setting up an x402 agent with policy-controlled spending.
 *
 * Prerequisites:
 *   npm install @x402-kit/agent @x402-kit/shared
 *
 * Environment:
 *   X402_WALLET_PRIVATE_KEY=0x...  (funded with USDC on Base)
 */

import { createAgentFetch } from "@x402-kit/agent";
import type { Hex } from "viem";

// Load wallet key from environment (never hardcode!)
const walletPrivateKey = process.env.X402_WALLET_PRIVATE_KEY as Hex;
if (!walletPrivateKey) {
  throw new Error("X402_WALLET_PRIVATE_KEY environment variable is required");
}

// Create a policy-aware fetch wrapper
const agentFetch = createAgentFetch({
  walletPrivateKey,
  network: "eip155:8453", // Base mainnet (use "eip155:84532" for testnet)
  policy: {
    maxPerRequest: "1.00",       // Max 1 USDC per single request
    maxDailySpend: "10.00",      // Max 10 USDC total per day
    allowedNetworks: ["eip155:8453"],
    allowedAssets: [
      "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", // USDC on Base
    ],
    domainAllowlist: ["api.example.com"], // Only pay these domains
    requireHumanApproval: false,
  },
  logFilePath: "./x402-payments.jsonl",   // Payment audit log
  spendFilePath: ".x402/daily-spend.json", // Daily spend tracker
});

// Use agentFetch as a drop-in replacement for fetch
async function main() {
  // This request will auto-pay if the server returns 402 with x402 requirements
  const response = await agentFetch("https://api.example.com/premium/data");

  if (response.ok) {
    const data = await response.json();
    console.log("Got premium data:", data);
  } else if (response.status === 402) {
    console.log("Payment was denied by policy — check limits or domain rules");
  } else {
    console.log("Request failed:", response.status);
  }
}

main().catch(console.error);

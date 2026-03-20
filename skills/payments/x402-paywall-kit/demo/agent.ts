/**
 * Demo: AI agent that auto-pays x402 paywalls.
 *
 * Calls the demo server's /api/joke endpoint, auto-detects the 402 paywall,
 * pays 0.01 USDC on Base Sepolia, and prints the joke.
 *
 * Usage:
 *   export X402_WALLET_PRIVATE_KEY="0xYourPrivateKey"
 *   npx tsx demo/agent.ts
 */

import { createAgentFetch } from "@x402-kit/agent";
import type { Hex } from "viem";

const WALLET_KEY = process.env.X402_WALLET_PRIVATE_KEY as Hex | undefined;
if (!WALLET_KEY) {
  console.error(
    "Error: X402_WALLET_PRIVATE_KEY environment variable is required",
  );
  console.error(
    "Set it to a hex private key (0x...) of a wallet funded with testnet USDC on Base Sepolia.",
  );
  process.exit(1);
}

const SERVER_URL = process.env.DEMO_SERVER_URL ?? "http://localhost:3000";

// Base Sepolia USDC contract address
const USDC_BASE_SEPOLIA = "0x036CbD53842c5426634e7929541eC2318f3dCF7e";

// Create the policy-aware fetch wrapper
const agentFetch = createAgentFetch({
  walletPrivateKey: WALLET_KEY,
  network: "eip155:84532", // Base Sepolia testnet
  policy: {
    maxPerRequest: "0.05", // Max 0.05 USDC per request
    maxDailySpend: "1.00", // Max 1 USDC per day
    allowedNetworks: ["eip155:84532"],
    allowedAssets: [USDC_BASE_SEPOLIA],
    requireHumanApproval: false,
  },
  logFilePath: "./demo/payments-agent.jsonl",
});

async function main() {
  console.log("x402-kit Demo Agent");
  console.log("===================");
  console.log(`Server: ${SERVER_URL}`);
  console.log(`Network: Base Sepolia (eip155:84532)`);
  console.log();

  // Step 1: Check server health (free endpoint)
  console.log("1. Checking server health...");
  const healthResponse = await agentFetch(`${SERVER_URL}/health`);
  if (!healthResponse.ok) {
    console.error(
      `   Server not reachable at ${SERVER_URL}. Is the server running?`,
    );
    process.exit(1);
  }
  console.log("   Server is healthy.");
  console.log();

  // Step 2: Request the paywalled joke
  console.log("2. Requesting joke from paywalled endpoint...");
  console.log(`   GET ${SERVER_URL}/api/joke`);
  console.log();

  const response = await agentFetch(`${SERVER_URL}/api/joke`);

  if (response.ok) {
    const data = await response.json();
    console.log("3. Payment successful! Got a joke:");
    console.log();
    console.log(`   "${data.joke}"`);
    console.log();
    console.log(`   Paid: ${data.price} via ${data.paidWith}`);
    console.log(`   Network: ${data.network}`);
  } else if (response.status === 402) {
    console.log("3. Payment was not made. Possible reasons:");
    console.log("   - Policy denied the payment (check limits/domains)");
    console.log("   - Wallet has insufficient USDC balance");
    console.log("   - Network mismatch between server and agent");
    console.log(`   Response status: ${response.status}`);
  } else {
    console.log(`3. Unexpected response: HTTP ${response.status}`);
    const text = await response.text();
    if (text) console.log(`   Body: ${text}`);
  }

  console.log();
  console.log("Check ./demo/payments-agent.jsonl for the payment log.");
}

main().catch((error) => {
  console.error("Agent error:", error.message ?? error);
  process.exit(1);
});

/**
 * Flaunch + Aegis Integration Example
 *
 * Demonstrates how an AI agent can safely trade tokens launched on Flaunch
 * by running Aegis safety checks before every swap.
 *
 * This example uses the MCP client SDK to connect to a running Aegis server,
 * and the Flaunch SDK for reading token data and executing swaps.
 *
 * Prerequisites:
 *   - Aegis MCP server running (`npx aegis-defi`)
 *   - @flaunch/sdk and @modelcontextprotocol/sdk installed
 *   - A Base RPC endpoint available
 */

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { createFlaunch, type ReadWriteFlaunchSDK } from "@flaunch/sdk";
import { createPublicClient, createWalletClient, http, parseEther, type Address } from "viem";
import { base } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

const BASE_RPC = process.env.BASE_RPC || "https://mainnet.base.org";
const AGENT_PRIVATE_KEY = process.env.AGENT_PRIVATE_KEY as `0x${string}`;
const CHAIN_ID = 8453; // Base mainnet

// ---------------------------------------------------------------------------
// 1. Connect to Aegis MCP server
// ---------------------------------------------------------------------------

async function createAegisClient(): Promise<Client> {
  const transport = new StdioClientTransport({
    command: "npx",
    args: ["aegis-defi"],
  });

  const client = new Client({
    name: "flaunch-agent",
    version: "1.0.0",
  });

  await client.connect(transport);
  console.log("[aegis] Connected to Aegis MCP server");
  return client;
}

// ---------------------------------------------------------------------------
// 2. Set up Flaunch SDK (read + write)
// ---------------------------------------------------------------------------

function createFlaunchClient(): ReadWriteFlaunchSDK {
  const account = privateKeyToAccount(AGENT_PRIVATE_KEY);

  const publicClient = createPublicClient({
    chain: base,
    transport: http(BASE_RPC),
  });

  const walletClient = createWalletClient({
    account,
    chain: base,
    transport: http(BASE_RPC),
  });

  return createFlaunch({ publicClient, walletClient }) as ReadWriteFlaunchSDK;
}

// ---------------------------------------------------------------------------
// 3. Aegis safety check - call assess_risk via MCP
// ---------------------------------------------------------------------------

interface AegisDecision {
  decision: "ALLOW" | "WARN" | "BLOCK";
  overallRiskScore: number;
  riskFactors: string[];
  recommendation: string;
  attestation?: {
    attestationId: string;
    signature: string;
  };
}

async function checkSafetyBeforeSwap(
  aegis: Client,
  agentAddress: Address,
  tokenAddress: Address,
): Promise<AegisDecision> {
  console.log(`[aegis] Running safety check on token ${tokenAddress}...`);

  const result = await aegis.callTool({
    name: "assess_risk",
    arguments: {
      action: "swap",
      targetContract: tokenAddress,
      chainId: CHAIN_ID,
      from: agentAddress,
      tokenAddress: tokenAddress,
    },
  });

  // The MCP tool returns JSON in a text content block
  const textContent = result.content.find(
    (c): c is { type: "text"; text: string } => c.type === "text",
  );

  if (!textContent) {
    throw new Error("Aegis returned no text content");
  }

  const assessment: AegisDecision = JSON.parse(textContent.text);
  console.log(`[aegis] Decision: ${assessment.decision} (risk score: ${assessment.overallRiskScore})`);

  if (assessment.riskFactors.length > 0) {
    console.log(`[aegis] Risk factors: ${assessment.riskFactors.join(", ")}`);
  }

  return assessment;
}

// ---------------------------------------------------------------------------
// 4. Standalone token check - useful for quick honeypot screening
// ---------------------------------------------------------------------------

async function quickTokenCheck(
  aegis: Client,
  tokenAddress: Address,
): Promise<{ safe: boolean; assessment: string }> {
  const result = await aegis.callTool({
    name: "check_token",
    arguments: {
      tokenAddress,
      chainId: CHAIN_ID,
    },
  });

  const textContent = result.content.find(
    (c): c is { type: "text"; text: string } => c.type === "text",
  );

  if (!textContent) {
    throw new Error("Aegis returned no text content");
  }

  const data = JSON.parse(textContent.text);
  return {
    safe: data.overallAssessment === "LIKELY_SAFE",
    assessment: data.overallAssessment,
  };
}

// ---------------------------------------------------------------------------
// 5. Main agent flow: discover token, check safety, trade
// ---------------------------------------------------------------------------

async function agentTradeFlaunchToken(coinAddress: Address, ethAmount: string) {
  // Connect to both services
  const aegis = await createAegisClient();
  const flaunch = createFlaunchClient();
  const account = privateKeyToAccount(AGENT_PRIVATE_KEY);
  const agentAddress = account.address;

  try {
    // Step 1: Read token metadata from Flaunch
    console.log(`\n--- Step 1: Fetching token metadata ---`);
    const metadata = await flaunch.getCoinMetadata(coinAddress);
    console.log(`Token: ${metadata.name} (${metadata.symbol})`);

    // Step 2: Run Aegis safety check
    console.log(`\n--- Step 2: Running Aegis safety check ---`);
    const safety = await checkSafetyBeforeSwap(aegis, agentAddress, coinAddress);

    // Step 3: Act on the decision
    console.log(`\n--- Step 3: Executing decision ---`);

    if (safety.decision === "BLOCK") {
      console.log(`[BLOCKED] Aegis blocked this trade.`);
      console.log(`Reason: ${safety.recommendation}`);
      console.log(`Risk factors: ${safety.riskFactors.join(", ")}`);
      console.log(`The agent will NOT execute this swap.`);
      return {
        executed: false,
        reason: "blocked_by_aegis",
        riskScore: safety.overallRiskScore,
        riskFactors: safety.riskFactors,
      };
    }

    if (safety.decision === "WARN") {
      console.log(`[WARNING] Aegis flagged potential risks.`);
      console.log(`Risk score: ${safety.overallRiskScore}/100`);
      console.log(`Factors: ${safety.riskFactors.join(", ")}`);
      console.log(`Proceeding with caution (reduced position size recommended).`);
      // In production, an agent might reduce the trade size or ask the user
    }

    if (safety.decision === "ALLOW") {
      console.log(`[SAFE] Aegis approved this trade.`);
      console.log(`Risk score: ${safety.overallRiskScore}/100`);
    }

    // Step 4: Execute the swap via Flaunch SDK
    console.log(`\n--- Step 4: Executing swap via Flaunch ---`);
    const txHash = await flaunch.buyCoin({
      coinAddress,
      slippagePercent: 5,
      swapType: "EXACT_IN",
      amountIn: parseEther(ethAmount),
    });

    console.log(`[SUCCESS] Swap executed. TX: ${txHash}`);

    return {
      executed: true,
      txHash,
      riskScore: safety.overallRiskScore,
      decision: safety.decision,
      attestation: safety.attestation,
    };
  } finally {
    // Always clean up the MCP connection
    await aegis.close();
  }
}

// ---------------------------------------------------------------------------
// 6. Sell flow with safety check
// ---------------------------------------------------------------------------

async function agentSellFlaunchToken(coinAddress: Address, tokenAmount: string) {
  const aegis = await createAegisClient();
  const flaunch = createFlaunchClient();
  const account = privateKeyToAccount(AGENT_PRIVATE_KEY);

  try {
    // Before selling, verify the token contract has not been modified
    // (e.g., owner added a transfer blacklist after you bought)
    console.log(`\n--- Pre-sell safety check ---`);
    const tokenCheck = await quickTokenCheck(aegis, coinAddress);

    if (!tokenCheck.safe) {
      console.log(`[WARNING] Token may have issues: ${tokenCheck.assessment}`);
      console.log(`Attempting sell anyway - blocking sells would trap funds.`);
    }

    // Handle Permit2 approval for gasless selling
    const { allowance } = await flaunch.getPermit2AllowanceAndNonce(coinAddress);
    const sellAmount = parseEther(tokenAmount);

    let permitSingle: any;
    let signature: string | undefined;

    if (allowance < sellAmount) {
      console.log(`[permit2] Insufficient allowance - signing Permit2 approval`);
      const permit2Data = await flaunch.getPermit2TypedData(coinAddress);
      permitSingle = permit2Data.permitSingle;

      // In production, the agent's wallet signs this typed data
      // signature = await walletClient.signTypedData(permit2Data.typedData);
      console.log(`[permit2] Typed data prepared for signing`);
    }

    const txHash = await flaunch.sellCoin({
      coinAddress,
      amountIn: sellAmount,
      slippagePercent: 5,
      permitSingle,
      signature,
    });

    console.log(`[SUCCESS] Sell executed. TX: ${txHash}`);

    return { executed: true, txHash };
  } finally {
    await aegis.close();
  }
}

// ---------------------------------------------------------------------------
// 7. Batch screening - scan multiple Flaunch tokens at once
// ---------------------------------------------------------------------------

async function screenFlaunchTokens(tokenAddresses: Address[]): Promise<Map<Address, AegisDecision>> {
  const aegis = await createAegisClient();
  const account = privateKeyToAccount(AGENT_PRIVATE_KEY);
  const results = new Map<Address, AegisDecision>();

  try {
    for (const token of tokenAddresses) {
      try {
        const decision = await checkSafetyBeforeSwap(aegis, account.address, token);
        results.set(token, decision);
      } catch (err) {
        console.error(`[aegis] Failed to check ${token}:`, err);
      }
    }
  } finally {
    await aegis.close();
  }

  // Summary
  const allowed = [...results.values()].filter((d) => d.decision === "ALLOW").length;
  const warned = [...results.values()].filter((d) => d.decision === "WARN").length;
  const blocked = [...results.values()].filter((d) => d.decision === "BLOCK").length;

  console.log(`\n--- Screening Summary ---`);
  console.log(`Total: ${tokenAddresses.length} | ALLOW: ${allowed} | WARN: ${warned} | BLOCK: ${blocked}`);

  return results;
}

// ---------------------------------------------------------------------------
// Run the example
// ---------------------------------------------------------------------------

async function main() {
  // Example: Buy a Flaunch token after safety check
  const EXAMPLE_TOKEN = "0x1234567890abcdef1234567890abcdef12345678" as Address;
  const ETH_AMOUNT = "0.01"; // 0.01 ETH

  console.log("=== Flaunch + Aegis Integration Example ===\n");

  try {
    const result = await agentTradeFlaunchToken(EXAMPLE_TOKEN, ETH_AMOUNT);
    console.log("\n--- Result ---");
    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    console.error("Error:", err);
  }
}

// Uncomment to run:
// main();

export {
  createAegisClient,
  checkSafetyBeforeSwap,
  quickTokenCheck,
  agentTradeFlaunchToken,
  agentSellFlaunchToken,
  screenFlaunchTokens,
};

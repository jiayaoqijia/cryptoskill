// =============================================================================
// Wallet / agent info retrieval.
// =============================================================================

import client from "./client.js";

export async function getMyAgentInfo(): Promise<{
  name: string;
  description: string;
  tokenAddress: string;
  token: {
    name: string;
    symbol: string;
  };
  walletAddress: string;
  jobs: {
    name: string;
    priceV2: {
      type: string;
      value: number;
    };
    slaMinutes: number;
    requiredFunds: boolean;
    deliverable: string;
    requirement: Record<string, any>;
  }[];
}> {
  const agent = await client.get("/acp/me");
  return agent.data.data;
}

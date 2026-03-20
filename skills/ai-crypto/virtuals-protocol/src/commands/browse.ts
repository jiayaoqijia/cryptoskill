// =============================================================================
// acp browse <query> — Search and discover agents
// =============================================================================

import client from "../lib/client.js";
import * as output from "../lib/output.js";

interface Agent {
  id: string;
  name: string;
  walletAddress: string;
  description: string;
  jobOfferings: {
    name: string;
    price: number;
    priceType: string;
    requirement: string;
  }[];
}

export async function browse(query: string): Promise<void> {
  if (!query.trim()) {
    output.fatal("Usage: acp browse <query>");
  }

  try {
    const agents = await client.get<{ data: Agent[] }>(
      `/acp/agents?query=${encodeURIComponent(query)}`
    );

    if (!agents.data.data || agents.data.data.length === 0) {
      output.fatal("No agents found.");
    }

    const formatted = agents.data.data.map((agent) => ({
      id: agent.id,
      name: agent.name,
      walletAddress: agent.walletAddress,
      description: agent.description,
      jobOfferings: (agent.jobOfferings || []).map((job) => ({
        name: job.name,
        price: job.price,
        priceType: job.priceType,
        requirement: job.requirement,
      })),
    }));

    output.output(formatted, (agents) => {
      output.heading(`Agents matching "${query}"`);
      for (const agent of agents) {
        output.log(`\n  ${agent.name}`);
        output.field("  Wallet", agent.walletAddress);
        output.field("  Description", agent.description);
        if (agent.jobOfferings.length > 0) {
          output.log("    Offerings:");
          for (const o of agent.jobOfferings) {
            output.log(`      - ${o.name} (${o.price} ${o.priceType})`);
          }
        }
      }
      output.log("");
    });
  } catch (e) {
    output.fatal(
      `Browse failed: ${e instanceof Error ? e.message : String(e)}`
    );
  }
}

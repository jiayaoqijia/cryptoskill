#!/usr/bin/env node
import {
  agentRegistryId,
  parseArgs,
  readJsonFile,
  resolveNetwork,
  writeJsonFile,
} from "./common.mjs";

async function main() {
  const args = parseArgs(process.argv);
  const network = resolveNetwork(args);
  const agentIdRaw = args.agentId;
  if (!agentIdRaw) throw new Error("Missing --agentId");

  const name = args.name ?? "CEO-1";
  const description = args.description ?? "Autonomous AI agent";
  const image = args.image ?? "https://example.com/agent-image.png";
  const out = args.out ?? `./agent-${agentIdRaw}.json`;

  const base = args.template ? await readJsonFile(args.template) : {};
  const services = Array.isArray(base.services) ? base.services : [];
  const supportedTrust = Array.isArray(base.supportedTrust) ? base.supportedTrust : ["reputation"];

  const card = {
    type: "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
    name,
    description,
    image,
    services,
    x402Support: base.x402Support ?? false,
    active: base.active ?? true,
    registrations: [
      {
        agentId: Number(agentIdRaw),
        agentRegistry: agentRegistryId(network.chainId, network.registry),
      },
    ],
    supportedTrust,
  };

  await writeJsonFile(out, card);
  console.log(
    JSON.stringify(
      {
        status: "ok",
        out,
        agentId: String(agentIdRaw),
        chainId: network.chainId,
        registry: network.registry,
      },
      null,
      2
    )
  );
}

main().catch((err) => {
  const message = err instanceof Error ? err.message : String(err);
  console.error(`build-card.mjs error: ${message}`);
  process.exit(1);
});

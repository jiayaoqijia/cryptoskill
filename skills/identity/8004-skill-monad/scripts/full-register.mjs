#!/usr/bin/env node
import { parseEventLogs } from "viem";
import {
  IDENTITY_ABI,
  agentRegistryId,
  createClients,
  parseArgs,
  readJsonFile,
  resolveNetwork,
  requiredEnv,
  writeJsonFile,
  writeTextFile,
} from "./common.mjs";
import { PinataSDK } from "pinata";

function renderIdentityMarkdown(params) {
  return `# Agent Identity
- **Address**: \`${params.address}\`
- **Agent ID**: \`${params.agentId}\`
- **Agent Registry**: \`${params.agentRegistry}\`
- **Chain ID**: \`${params.chainId}\`
`;
}

async function main() {
  const args = parseArgs(process.argv);
  const network = resolveNetwork(args);
  const { walletClient, publicClient, account } = createClients(network);

  const name = args.name ?? "CEO-1";
  const description = args.description ?? "Autonomous AI agent";
  const image = args.image ?? "https://example.com/agent-image.png";
  const template = args.template ? await readJsonFile(args.template) : {};

  // 1) Register on-chain with empty URI to obtain agentId.
  const registerHash = await walletClient.writeContract({
    address: network.registry,
    abi: IDENTITY_ABI,
    functionName: "register",
    args: [],
    account,
  });
  const registerReceipt = await publicClient.waitForTransactionReceipt({ hash: registerHash });
  const registerLogs = parseEventLogs({
    abi: IDENTITY_ABI,
    logs: registerReceipt.logs,
    eventName: "Registered",
  });
  const agentId = registerLogs[0]?.args?.agentId;
  if (typeof agentId === "undefined") throw new Error("Registered event not found after register().");

  // 2) Build agent card with registrations[].
  const agentRegistry = agentRegistryId(network.chainId, network.registry);
  const card = {
    type: "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
    name,
    description,
    image,
    services: Array.isArray(template.services) ? template.services : [],
    x402Support: template.x402Support ?? false,
    active: template.active ?? true,
    registrations: [{ agentId: Number(agentId), agentRegistry }],
    supportedTrust: Array.isArray(template.supportedTrust) ? template.supportedTrust : ["reputation"],
  };
  const outCardPath = args.outCard ?? `./agent-${agentId.toString()}.json`;
  await writeJsonFile(outCardPath, card);

  // 3) Upload to Pinata.
  const pinataJwt = args.pinataJwt ?? requiredEnv("PINATA_JWT");
  const pinataGateway = args.pinataGateway ?? process.env.PINATA_GATEWAY;
  const pinata = new PinataSDK({
    pinataJwt,
    ...(pinataGateway ? { pinataGateway } : {}),
  });
  const file = new File([JSON.stringify(card, null, 2)], `agent-${agentId.toString()}.json`, {
    type: "application/json",
  });
  const uploadResult = await pinata.upload.public.file(file);
  const tokenUri = `ipfs://${uploadResult.cid}`;

  // 4) Set URI on-chain.
  const setUriHash = await walletClient.writeContract({
    address: network.registry,
    abi: IDENTITY_ABI,
    functionName: "setAgentURI",
    args: [agentId, tokenUri],
    account,
  });
  const setUriReceipt = await publicClient.waitForTransactionReceipt({ hash: setUriHash });

  // 5) Persist identity file for agent memory/workflows.
  const identityFile = args.identityFile ?? "/root/.openclaw/workspace/AGENT_IDENTITY.md";
  await writeTextFile(
    identityFile,
    renderIdentityMarkdown({
      address: account.address,
      agentId: agentId.toString(),
      agentRegistry,
      chainId: network.chainId,
    })
  );

  console.log(
    JSON.stringify(
      {
        status: "ok",
        chainId: network.chainId,
        registry: network.registry,
        address: account.address,
        agentId: agentId.toString(),
        registerTxHash: registerHash,
        outCardPath,
        cid: uploadResult.cid,
        tokenUri,
        setUriTxHash: setUriHash,
        setUriStatus: setUriReceipt.status,
        identityFile,
      },
      null,
      2
    )
  );
}

main().catch((err) => {
  const message = err instanceof Error ? err.message : String(err);
  console.error(`full-register.mjs error: ${message}`);
  process.exit(1);
});

#!/usr/bin/env node
import { getAddress } from "viem";
import { IDENTITY_ABI, createClients, parseArgs, resolveNetwork } from "./common.mjs";

function ipfsToHttp(uri, gatewayHost) {
  if (!uri.startsWith("ipfs://")) return uri;
  const cidPath = uri.replace("ipfs://", "");
  return `https://${gatewayHost}/ipfs/${cidPath}`;
}

async function main() {
  const args = parseArgs(process.argv);
  const network = resolveNetwork(args);
  const agentIdRaw = args.agentId;
  if (!agentIdRaw) throw new Error("Missing --agentId");
  const agentId = BigInt(agentIdRaw);

  const { publicClient } = createClients(network);
  const [owner, tokenUri, wallet] = await Promise.all([
    publicClient.readContract({
      address: network.registry,
      abi: IDENTITY_ABI,
      functionName: "ownerOf",
      args: [agentId],
    }),
    publicClient.readContract({
      address: network.registry,
      abi: IDENTITY_ABI,
      functionName: "tokenURI",
      args: [agentId],
    }),
    publicClient.readContract({
      address: network.registry,
      abi: IDENTITY_ABI,
      functionName: "getAgentWallet",
      args: [agentId],
    }),
  ]);

  const gatewayHost = args.pinataGateway ?? process.env.PINATA_GATEWAY;
  let card = null;
  let registrationMatches = null;
  if (tokenUri && gatewayHost) {
    const url = ipfsToHttp(tokenUri, gatewayHost);
    const res = await fetch(url);
    if (res.ok) {
      card = await res.json();
      const registrations = Array.isArray(card.registrations) ? card.registrations : [];
      const expectedRegistry = `eip155:${network.chainId}:${getAddress(network.registry)}`;
      registrationMatches = registrations.some(
        (entry) => Number(entry?.agentId) === Number(agentIdRaw) && entry?.agentRegistry === expectedRegistry
      );
    }
  }

  console.log(
    JSON.stringify(
      {
        status: "ok",
        chainId: network.chainId,
        registry: network.registry,
        agentId: String(agentId),
        owner,
        tokenUri,
        agentWallet: wallet,
        cardFetched: card !== null,
        registrationMatches,
      },
      null,
      2
    )
  );
}

main().catch((err) => {
  const message = err instanceof Error ? err.message : String(err);
  console.error(`verify.mjs error: ${message}`);
  process.exit(1);
});

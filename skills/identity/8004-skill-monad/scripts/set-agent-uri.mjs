#!/usr/bin/env node
import { IDENTITY_ABI, createClients, parseArgs, resolveNetwork } from "./common.mjs";

async function main() {
  const args = parseArgs(process.argv);
  const network = resolveNetwork(args);
  const agentIdRaw = args.agentId;
  const uri = args.uri ?? args.tokenUri;
  if (!agentIdRaw) throw new Error("Missing --agentId");
  if (!uri) throw new Error("Missing --uri ipfs://...");

  const { walletClient, publicClient, account } = createClients(network);
  const hash = await walletClient.writeContract({
    address: network.registry,
    abi: IDENTITY_ABI,
    functionName: "setAgentURI",
    args: [BigInt(agentIdRaw), uri],
    account,
  });
  const receipt = await publicClient.waitForTransactionReceipt({ hash });

  console.log(
    JSON.stringify(
      {
        status: "ok",
        txHash: hash,
        receiptStatus: receipt.status,
        agentId: String(agentIdRaw),
        tokenUri: uri,
      },
      null,
      2
    )
  );
}

main().catch((err) => {
  const message = err instanceof Error ? err.message : String(err);
  console.error(`set-agent-uri.mjs error: ${message}`);
  process.exit(1);
});

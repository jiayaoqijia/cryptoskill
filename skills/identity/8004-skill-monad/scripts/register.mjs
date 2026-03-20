#!/usr/bin/env node
import { parseEventLogs } from "viem";
import { IDENTITY_ABI, createClients, parseArgs, resolveNetwork } from "./common.mjs";

async function main() {
  const args = parseArgs(process.argv);
  const network = resolveNetwork(args);
  const { walletClient, publicClient, account } = createClients(network);

  const agentUri = typeof args.agentUri === "string" ? args.agentUri : undefined;
  const hash = await walletClient.writeContract({
    address: network.registry,
    abi: IDENTITY_ABI,
    functionName: "register",
    args: agentUri ? [agentUri] : [],
    account,
  });

  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  const logs = parseEventLogs({
    abi: IDENTITY_ABI,
    logs: receipt.logs,
    eventName: "Registered",
  });
  const agentId = logs[0]?.args?.agentId;
  if (typeof agentId === "undefined") {
    throw new Error("Registered event not found in receipt logs.");
  }

  console.log(
    JSON.stringify(
      {
        status: "ok",
        txHash: hash,
        chainId: network.chainId,
        registry: network.registry,
        owner: account.address,
        agentId: agentId.toString(),
        agentUri: agentUri ?? "",
      },
      null,
      2
    )
  );
}

main().catch((err) => {
  const message = err instanceof Error ? err.message : String(err);
  console.error(`register.mjs error: ${message}`);
  process.exit(1);
});

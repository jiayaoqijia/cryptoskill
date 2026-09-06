/**
 * Example: Cast a fortune on-chain and get AI interpretation
 *
 * Steps:
 *   1. Read cast fee from contract
 *   2. Call requestCast() — triggers VRF
 *   3. Poll casts(castId) until ready
 *   4. Look up hexagram data
 *   5. Call Interpret API for AI reading
 *
 * Usage:
 *   PRIVATE_KEY=0x... npx tsx examples/cast-fortune.ts "我的事业运如何？"
 *
 * Environment:
 *   PRIVATE_KEY          — Wallet private key (needs BNB for gas + cast fee)
 *   FORTUNE_CORE_ADDRESS — Contract address (default: BSC mainnet)
 *   RPC_URL              — BSC RPC URL
 *   INTERPRET_API        — Interpret API URL (default: https://qlwy.xyz/api/interpret)
 *   AUTH_TOKEN            — Privy JWT for interpret API
 */

import {
  createPublicClient,
  createWalletClient,
  http,
  parseEventLogs,
  type Address,
} from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { bsc } from "viem/chains";
import fortuneCoreAbi from "../references/QLWYFortuneCore.abi.json";
import hexagramData from "../references/hexagramData.json";

// ─── Config ──────────────────────────────────────────────────────────────────

const PRIVATE_KEY = process.env.PRIVATE_KEY as `0x${string}`;
const FORTUNE_CORE = (process.env.FORTUNE_CORE_ADDRESS ||
  "0xcE6f2F55898050C0D1769164c4Ceb828B4fC54f8") as Address;
const RPC_URL = process.env.RPC_URL || "https://bsc-dataseed1.binance.org";
const INTERPRET_API = process.env.INTERPRET_API || "https://qlwy.xyz/api/interpret";
const AUTH_TOKEN = process.env.AUTH_TOKEN || "";

// ─── Main ────────────────────────────────────────────────────────────────────

async function main() {
  const question = process.argv[2];
  if (!question) {
    console.error('Usage: npx tsx examples/cast-fortune.ts "你的问题"');
    process.exit(1);
  }
  if (!PRIVATE_KEY) {
    console.error("Error: PRIVATE_KEY environment variable required");
    process.exit(1);
  }

  const account = privateKeyToAccount(PRIVATE_KEY);
  const publicClient = createPublicClient({ chain: bsc, transport: http(RPC_URL) });
  const walletClient = createWalletClient({ account, chain: bsc, transport: http(RPC_URL) });

  // Step 1: Read cast fee
  console.log("Step 1: Reading cast fee...");
  const castFee = (await publicClient.readContract({
    address: FORTUNE_CORE,
    abi: fortuneCoreAbi,
    functionName: "castFee",
  })) as bigint;
  console.log(`  Cast fee: ${castFee} wei`);

  // Step 2: Request cast
  console.log("\nStep 2: Requesting cast (VRF)...");
  const tx = await walletClient.writeContract({
    address: FORTUNE_CORE,
    abi: fortuneCoreAbi,
    functionName: "requestCast",
    args: ["0x"],
    value: castFee,
  });
  const receipt = await publicClient.waitForTransactionReceipt({ hash: tx });
  console.log(`  TX: ${tx} (block ${receipt.blockNumber})`);

  // Parse castId from event logs
  const logs = parseEventLogs({ abi: fortuneCoreAbi, logs: receipt.logs });
  const castEvent = logs.find((l: any) => l.eventName === "CastRequested") as any;
  const castId = castEvent?.args?.castId ?? 0n;
  console.log(`  Cast ID: ${castId}`);

  // Step 3: Poll for result
  console.log("\nStep 3: Waiting for VRF result...");
  let ready = false;
  let castResult: any;
  for (let i = 0; i < 30; i++) {
    await new Promise((r) => setTimeout(r, 5000));
    castResult = await publicClient.readContract({
      address: FORTUNE_CORE,
      abi: fortuneCoreAbi,
      functionName: "casts",
      args: [castId],
    });
    ready = (castResult as any)[5]; // ready field
    if (ready) break;
    process.stdout.write(".");
  }
  if (!ready) {
    console.error("\n  Timeout waiting for VRF callback");
    process.exit(1);
  }

  // Step 4: Display hexagram
  const hexId = Number((castResult as any)[3].id) + 1;
  const rarity = Number((castResult as any)[4]);
  const luck = Number((castResult as any)[6]);
  const lines = [...(castResult as any)[3].lines].map(Number);
  const hex = (hexagramData as any[]).find((h) => h.id === hexId);

  console.log(`\n  🎴 卦象: ${hex?.full || `第${hexId}卦`}`);
  console.log(`  爻线: ${lines.join(", ")} (0=阴, 1=阳)`);
  console.log(`  稀有度: ${["普通", "稀有", "史诗", "传奇", "神话"][rarity]}`);
  console.log(`  运气值: ${luck}`);

  // Step 5: Interpret (if auth token available)
  if (AUTH_TOKEN) {
    console.log("\nStep 5: AI interpretation...");
    const res = await fetch(INTERPRET_API, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${AUTH_TOKEN}`,
      },
      body: JSON.stringify({
        castId: castId.toString(),
        question,
        hexagramId: hexId,
        hexagramName: hex?.full,
        hexagramJudgment: hex?.text,
        lines,
        rarity,
        luck,
      }),
    });
    // Read SSE stream
    const reader = res.body?.getReader();
    const decoder = new TextDecoder();
    if (reader) {
      console.log("\n  📖 解读:\n");
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        process.stdout.write(decoder.decode(value));
      }
      console.log();
    }
  } else {
    console.log("\nSkipping AI interpretation (no AUTH_TOKEN set)");
  }

  console.log("\n🎉 Done!");
}

main().catch(console.error);


#!/usr/bin/env node
import { realpathSync } from "node:fs";
import { pathToFileURL } from "node:url";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { createRequire } from "node:module";
import { ALLOCATE_URL, CHAIN_NAMES, fetchScan, poolToJson, rankPools, scanAgeHours, splitAllocation, splitToText, steadyPools } from "./radar.js";
import { currentSplitPays, readWalletStakes, timersByChain, withoutOwnSAero } from "./stakes.js";
import { formatError, isValidAddress } from "./util.js";

/**
 * Resolves an sAERO amount from either an explicit amount or a wallet address,
 * and returns the wallet when one was read so the caller can report its split.
 */
export async function resolveSAero(amount?: number, address?: string) {
  if (amount !== undefined && address !== undefined) throw new Error("Pass either amount or address, not both.");
  if (address !== undefined) {
    if (!isValidAddress(address)) throw new Error(`Not a wallet address: ${address}`);
    const wallet = await readWalletStakes(address);
    if (!(wallet.totalSAero > 0)) throw new Error(`No sAERO stake found for ${address} on Base — nothing to allocate.`);
    return { amount: wallet.totalSAero, wallet };
  }
  if (amount === undefined) throw new Error("Provide either amount (sAERO) or address (a wallet to read it from).");
  return { amount, wallet: undefined };
}

/**
 * Wraps a tool handler so a thrown error (a failed fetch or RPC call, since
 * this server holds one process open across many calls) comes back as a clean
 * one-line `formatError` message instead of the SDK's raw dump.
 */
function withErrorHandling<Args extends unknown[]>(
  handler: (...args: Args) => Promise<{ content: { type: "text"; text: string }[] }>,
) {
  return async (...args: Args) => {
    try {
      return await handler(...args);
    } catch (err) {
      return { content: [{ type: "text" as const, text: formatError(err) }], isError: true };
    }
  };
}

const json = (value: unknown) => ({ content: [{ type: "text" as const, text: JSON.stringify(value, null, 2) }] });

/**
 * Read from package.json rather than repeated here, so the manifest and the
 * handshake can't drift. `../package.json` resolves from both `src/` under tsx
 * and `dist/` when installed.
 */
const { version } = createRequire(import.meta.url)("../package.json") as { version: string };

const server = new McpServer({
  name: "aero-vote-radar",
  version,
});

const chainSchema = z
  .enum(Object.keys(CHAIN_NAMES) as [string, ...string[]])
  .optional()
  .describe("Only pools on this network. Omit for all networks.");

const SCAN_NOTE =
  "Figures are per day at the rates of the latest hourly scan: fees swept to allocators over the scan window plus incentives streaming now, split by the pool's allocated sAERO after the user's own stake joins it. They move hour to hour; they are not a promise.";

server.registerTool(
  "list_pools",
  {
    title: "List Aero pools by what sAERO earns there",
    description:
      "Ranks Aero (formerly Aerodrome) pools on all 7 of its networks by what a given amount of sAERO would earn a day after its own stake dilutes the pool. Reads the hourly scan of Aero's contracts behind aero.deftools.xyz. Pools with under 100,000 sAERO allocated are left out: one stake would move their rate. `steadyOnly` keeps only pools that kept paying hour after hour (at least 75% of 24+ hourly samples at half their own average or more).",
    inputSchema: {
      amount: z.number().positive().default(10_000).describe("sAERO to rank for. Default 10,000."),
      chain: chainSchema,
      top: z.number().int().positive().max(100).default(15).describe("How many pools to return."),
      steadyOnly: z.boolean().default(false).describe("Only pools that paid steadily over the hourly history."),
    },
  },
  withErrorHandling(async ({ amount, chain, top, steadyOnly }) => {
    const scan = await fetchScan();
    const ranked = (steadyOnly ? steadyPools(scan, amount, chain) : rankPools(scan, amount, chain)).slice(0, top);
    return json({
      checkedAt: scan.checkedAt,
      scanAgeHours: Math.round(scanAgeHours(scan) * 10) / 10,
      windowHours: scan.windowHours,
      amountSAero: amount,
      pools: ranked.map((r) => ({ ...poolToJson(r.gauge, scan.windowHours, amount), yourUsdPerDay: r.mine })),
      note: SCAN_NOTE,
    });
  }),
);

server.registerTool(
  "recommend_allocation",
  {
    title: "Recommend how to split sAERO across Aero pools",
    description:
      "Suggests how to allocate sAERO across up to 3 Aero pools in 5% steps: each step goes where it adds the most after dilution, so a large stake spreads out instead of crowding one pool. Pass `amount`, or `address` to read the wallet's sAERO on-chain — then the answer also has what its current split pays and its 47 h timer on each network (a stake can move only 47 h after its last allocation there). Output only: this tool holds no keys and sends nothing. The user enters the split themselves on Aero's Allocate page; Aero has no link that pre-fills it.",
    inputSchema: {
      amount: z.number().positive().optional().describe("sAERO to allocate. Pass this or address."),
      address: z.string().optional().describe("A Base wallet whose sAERO stakes to read. Pass this or amount."),
      chain: chainSchema,
    },
  },
  withErrorHandling(async ({ amount, address, chain }) => {
    const resolved = await resolveSAero(amount, address);
    const scan = await fetchScan();
    const others = resolved.wallet ? withoutOwnSAero(scan, resolved.wallet) : scan;
    const split = splitAllocation(rankPools(others, resolved.amount, chain).map((r) => r.gauge), resolved.amount);
    return json({
      checkedAt: scan.checkedAt,
      amountSAero: resolved.amount,
      split: split.map((s) => ({ ...poolToJson(s.gauge, scan.windowHours, s.amount), percent: Math.round(s.share * 100), sAero: s.amount })),
      splitUsdPerDay: split.reduce((a, s) => a + s.perDay, 0),
      splitText: splitToText(split),
      current: resolved.wallet ? currentSplitPays(resolved.wallet, scan) : null,
      timers: resolved.wallet ? timersByChain(resolved.wallet) : null,
      notRead: resolved.wallet ? resolved.wallet.failed : null,
      allocateUrl: ALLOCATE_URL,
      note: `${SCAN_NOTE} Timers are Unix seconds when a stake may move again on that network. With an address, the wallet's own sAERO is left out of each pool's allocatedSAero, since the split moves it. Do not describe the allocation as done: the user saves it on ${ALLOCATE_URL}.`,
    });
  }),
);

server.registerTool(
  "get_my_stakes",
  {
    title: "Get a wallet's sAERO stakes, timers and current split",
    description:
      "Reads a Base wallet's sAERO stakes from Aero's VotingEscrow, and on each of Aero's 7 networks the stake's 47 h timer and which pools it has allocated to, from that network's LeafVoter. Also what that split pays a day at the latest scan's rates. A network that does not answer is listed in `notRead` rather than failing the call.",
    inputSchema: {
      address: z.string().describe("The Base wallet address (0x…)."),
    },
  },
  withErrorHandling(async ({ address }) => {
    if (!isValidAddress(address)) throw new Error(`Not a wallet address: ${address}`);
    const [wallet, scan] = await Promise.all([readWalletStakes(address), fetchScan()]);
    return json({
      address,
      stakeCount: wallet.count,
      totalSAero: wallet.totalSAero,
      stakes: wallet.stakes.map((s) => ({ id: s.id.toString(), sAero: s.sAero, chains: s.chains })),
      timers: timersByChain(wallet),
      notRead: wallet.failed,
      current: currentSplitPays(wallet, scan),
      note: "readyAt and timers are Unix seconds; 0 means the stake has never allocated on that network and can do so right away.",
    });
  }),
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

// Only run the server when this file is executed directly, not when it's
// imported (e.g. by tests importing `resolveSAero`): `server.connect` never
// resolves for the life of the stdio connection. realpath, because npx runs the
// bin through a symlink while import.meta.url is the real file.
const isMainModule = process.argv[1] !== undefined && import.meta.url === pathToFileURL(realpathSync(process.argv[1])).href;
if (isMainModule) {
  main().catch((err) => {
    console.error("aero-vote-radar MCP server failed to start:", err);
    process.exit(1);
  });
}

#!/usr/bin/env node
import { pathToFileURL } from "node:url";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { createRequire } from "node:module";
import { rankPoolsByEfficiency } from "./efficiency.js";
import {
  recommendAllocation,
  toWholePercentWeights,
  expectedUsdForWholePercentVote,
  unallocatedVeAero,
  voteBasisCaveat,
} from "./allocator.js";
import { backtestLive } from "./backtest.js";
import { buildVoteCalldata } from "./calldata.js";
import { fetchVeAeroPositions } from "./veAero.js";
import { BACKTEST_EPOCHS, MAX_BACKTEST_EPOCHS } from "./constants.js";
import { formatError, isValidAddress } from "./util.js";
import { computeTrend, isEpochInProgress } from "./trend.js";

/**
 * Resolves a veAERO budget from either an explicit amount or a wallet address,
 * shared by the allocation and backtest tools so both accept the same input.
 */
export async function resolveVeAeroBudget(veAero?: number, address?: string): Promise<number> {
  if (veAero !== undefined && address !== undefined) {
    throw new Error("Pass either veAero or address, not both.");
  }
  if (address !== undefined) {
    const positions = await fetchVeAeroPositions(address);
    const total = positions.reduce((a, b) => a + b.votingPowerVeAero, 0);
    if (total <= 0) throw new Error(`No veAERO voting power found for ${address} — nothing to allocate.`);
    return total;
  }
  if (veAero === undefined) throw new Error("Provide either veAero (an amount) or address (a wallet to read it from).");
  return veAero;
}

/**
 * Wraps a tool handler so a thrown error (almost always a failed RPC or
 * price-lookup call, since this server holds one process open across many
 * calls) comes back as a clean one-line `formatError` message instead of the
 * MCP SDK's own catch-all, which surfaces viem's raw `.message` — a
 * multi-paragraph dump of docs links and version info that buries the actual
 * problem for whatever agent is consuming this tool.
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

/**
 * Read from package.json rather than repeated here. The two had already been
 * written twice and would have drifted at the first release, leaving clients
 * told one version by the manifest and another by the handshake.
 *
 * `../package.json` resolves from both `src/` under tsx and `dist/` when
 * installed, since the manifest ships with the package either way.
 */
const { version } = createRequire(import.meta.url)("../package.json") as { version: string };

const server = new McpServer({
  name: "aero-vote-radar",
  version,
});

server.registerTool(
  "list_pool_efficiency",
  {
    title: "List Aerodrome pool vote efficiency",
    description:
      "Ranks all live-gauge Aerodrome (Base) pools by current and trend-predicted USD value per veAERO vote, using live on-chain data from Aerodrome's Sugar contracts plus DefiLlama USD pricing. 'Predicted' is a simple trailing average of recent epochs, not a machine-learning forecast. Each pool also reports `momentum`: the recent completed epochs' average over the older ones', minus 1 (null without enough history) — direction that the trailing average and consistency alone can't show.",
    inputSchema: {
      top: z.number().int().positive().max(100).optional().describe("How many top pools to return (default 20)"),
      minConsistency: z
        .number()
        .min(0)
        .max(1)
        .optional()
        .describe("Only include pools whose consistency score is at least this (0..1). 1.00 = identical payout every epoch; a low score usually means one big one-off bribe rather than a repeatable opportunity."),
    },
  },
  withErrorHandling(async ({ top = 20, minConsistency = 0 }) => {
    const ranked = await rankPoolsByEfficiency();
    const eligible = ranked.filter((p) => p.consistency >= minConsistency);
    const asOfUnixSeconds = Math.floor(Date.now() / 1000);
    const rows = eligible.slice(0, top).map((p) => {
      const currentEpochPartial = isEpochInProgress(p.latestEpochTs, asOfUnixSeconds);
      const { momentum } = computeTrend(p.epochUsdSeries, currentEpochPartial);
      return {
        pool: p.pool.address,
        symbol: p.pool.symbol,
        currentVotesVeAero: p.currentVotesVeAero,
        currentValuePerVoteUsd: p.currentValuePerVote,
        predictedValuePerVoteUsd: p.predictedValuePerVote,
        predictiveEdgePct: p.predictiveEdge * 100,
        epochsObserved: p.epochsObserved,
        volatility: p.volatility,
        consistency: p.consistency,
        momentum,
      };
    });

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({ poolsConsidered: ranked.length, poolsPassingConsistency: eligible.length, top: rows }, null, 2),
        },
      ],
    };
  }),
);

server.registerTool(
  "recommend_allocation",
  {
    title: "Recommend a veAERO vote allocation",
    description:
      "Given a veAERO amount, recommends how to split votes across the current highest-efficiency Aerodrome pools using a greedy marginal-value ('water-filling') algorithm that accounts for self-dilution — voting more of your own veAERO into a pool measurably lowers your own $-per-vote there. Output is weights and expected USD only; this tool never touches a wallet, private key, or sends any transaction. The user reviews the recommendation and votes themselves on aerodrome.finance.",
    inputSchema: {
      veAero: z.number().positive().finite().optional().describe("Amount of veAERO voting power to allocate. Omit this if you pass `address` instead."),
      address: z
        .string()
        .refine(isValidAddress, "Must be a 0x-prefixed 40-character hex address")
        .optional()
        .describe("Base wallet address to read live voting power from, instead of stating an amount. Pass either this or veAero, not both."),
      topCandidates: z.number().int().positive().max(50).optional().describe("How many top-ranked pools to consider as candidates (default 15)"),
      minConsistency: z
        .number()
        .min(0)
        .max(1)
        .optional()
        .describe("Only allocate to pools whose consistency score is at least this (0..1), filtering out pools whose apparent value is one one-off bribe."),
      maxWeight: z
        .number()
        .gt(0)
        .max(1)
        .optional()
        .describe(
          "Cap on any single pool's share of the vote (0..1, default 1 = uncapped). The unconstrained optimum is often one pool at 100%, which is correct arithmetic and more concentration than many voters want. Too tight a cap for the candidate set leaves part of the budget unplaceable and the call fails rather than silently renormalising past the cap.",
        ),
      voteBasis: z
        .enum(["previous", "current", "typical"])
        .optional()
        .describe(
          "Which vote weight to judge each pool against (default 'previous'). Each option is a prediction of the weight the epoch will settle at, chosen by measuring that prediction: 'previous' uses last epoch's settled weight (most accurate, unbiased), 'current' the live mid-week tally (slightly worse), 'typical' the larger of the tally and the pool's usual weight (measured clearly worst; kept only for reproducibility).",
        ),
    },
  },
  withErrorHandling(async ({ veAero, address, topCandidates = 15, minConsistency = 0, maxWeight = 1, voteBasis = "previous" }) => {
    const budget = await resolveVeAeroBudget(veAero, address);
    const ranked = (await rankPoolsByEfficiency()).filter((p) => p.consistency >= minConsistency);
    const allocation = recommendAllocation(ranked, budget, topCandidates, undefined, maxWeight, voteBasis);

    // Zero qualifying pools is a distinct failure from "maxWeight too tight":
    // unallocatedVeAero(allocation=[], ...) returns the *whole* budget (nothing
    // was spent), which would otherwise always read as "unplaced > 0" below and
    // blame maxWeight even when it's untouched at its uncapped default of 1.
    if (allocation.length === 0) {
      throw new Error(
        minConsistency > 0
          ? `No live-gauge pool passes minConsistency ${minConsistency} right now — try a lower value.`
          : "No live-gauge pool with a big enough trailing average is available to allocate to right now.",
      );
    }

    // Same guard the CLI applies: toWholePercentWeights normalises by the
    // weights it is handed, so publishing a part-spent allocation would restore
    // the concentration the cap was asked to prevent.
    const unplaced = unallocatedVeAero(allocation, budget);
    if (unplaced > 0) {
      throw new Error(
        `maxWeight ${maxWeight} is too tight for the ${allocation.length} pool(s) that qualified: ${Math.round((unplaced / budget) * 100)}% of the veAERO has nowhere to go. Raise maxWeight, raise topCandidates, or lower minConsistency.`,
      );
    }
    const totalExpectedUsd = allocation.reduce((a, b) => a + b.expectedUsd, 0);
    const votePercents = toWholePercentWeights(allocation);
    const votePercentsExpectedUsd = expectedUsdForWholePercentVote(allocation, budget);

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(
            {
              veAeroBudget: budget,
              budgetSource: address ? `live on-chain voting power of ${address}` : "caller-supplied amount",
              totalExpectedUsdNextEpoch: totalExpectedUsd,
              votePercentsExpectedUsdNextEpoch: votePercentsExpectedUsd,
              allocation,
              votePercents,
              voteBasis,
              // Null on most calls, by design: it appears only when this
              // budget sits on the side of the measured crossover where the
              // chosen basis is the one the evidence does not favour. An agent
              // relaying a recommendation should relay this with it.
              voteBasisCaveat: voteBasisCaveat(budget, voteBasis),
              note: "Weights and expected $ are a heuristic recommendation based on trailing-epoch trends and current vote snapshots, not a guarantee. `votePercents` are whole percentages summing to exactly 100, ready to enter in Aerodrome's voting UI. Quote `votePercentsExpectedUsdNextEpoch` when telling the user what they would earn: `totalExpectedUsdNextEpoch` belongs to the continuous `allocation`, which includes rows too small to round up to 1% and so cannot be voted as written. If `voteBasisCaveat` is not null, pass it on: at this budget the vote basis used is the one the evidence does not favour, and the user should hear that alongside the numbers it produced. You sign and submit the vote yourself.",
            },
            null,
            2,
          ),
        },
      ],
    };
  }),
);

server.registerTool(
  "backtest_strategy",
  {
    title: "Backtest the vote-allocation strategy against past epochs",
    description:
      "Replays recent completed epochs and compares what this tool's self-dilution-aware allocation would have earned against the naive 'put everything in the pool with the highest current $/vote' strategy. Each epoch's decision uses only data that existed before that epoch resolved, so it is not a hindsight fit. Caveats: it assumes your votes would not have changed other voters' behaviour, only sees pools whose gauge is still alive today (survivorship bias), and a handful of weekly epochs is a small sample.",
    inputSchema: {
      veAero: z.number().positive().finite().optional().describe("Amount of veAERO to simulate voting with. Omit this if you pass `address` instead."),
      address: z
        .string()
        .refine(isValidAddress, "Must be a 0x-prefixed 40-character hex address")
        .optional()
        .describe("Base wallet address to read live voting power from, instead of stating an amount."),
      epochs: z.number().int().positive().max(MAX_BACKTEST_EPOCHS).optional().describe(`How many past epochs to replay (default ${BACKTEST_EPOCHS}, max ${MAX_BACKTEST_EPOCHS})`),
      minConsistency: z
        .number()
        .min(0)
        .max(1)
        .optional()
        .describe(
          "Only allocate to pools whose consistency — measured over the trailing window as it stood before each tested epoch, never today's — was at least this (0..1). Use it to backtest the same filtered strategy you would pass to the allocation tool; without it the report describes the unfiltered strategy instead. The naive baseline stays unfiltered either way, so uplift figures remain comparable.",
        ),
    },
  },
  withErrorHandling(async ({ veAero, address, epochs = BACKTEST_EPOCHS, minConsistency = 0 }) => {
    const budget = await resolveVeAeroBudget(veAero, address);
    const report = await backtestLive(budget, epochs, undefined, minConsistency);

    return {
      content: [{ type: "text", text: JSON.stringify(report, null, 2) }],
    };
  }),
);

server.registerTool(
  "get_my_veaero",
  {
    title: "Get an account's veAERO voting power",
    description: "Looks up all veAERO locks (NFTs) owned by a Base wallet address and their current voting power, read from Aerodrome's VotingEscrow contract.",
    inputSchema: {
      address: z
        .string()
        .refine(isValidAddress, "Must be a 0x-prefixed 40-character hex address")
        .describe("Base wallet address (0x...)"),
    },
  },
  withErrorHandling(async ({ address }) => {
    const positions = await fetchVeAeroPositions(address);
    const totalVeAero = positions.reduce((a, b) => a + b.votingPowerVeAero, 0);

    return {
      content: [{ type: "text", text: JSON.stringify({ address, totalVeAero, locks: positions }, null, 2) }],
    };
  }),
);

server.registerTool(
  "prepare_vote_calldata",
  {
    title: "Build the unsigned transaction that casts a recommended vote",
    description:
      "Turns a vote allocation into the exact bytes Aerodrome's Voter.vote expects, as an unsigned transaction (chainId, to, value, data) for the veNFT owner to review and sign in their own wallet. This server holds no keys, signs nothing and sends nothing — the output is inert until someone signs it. Weights must be whole percentage points totalling 100, which is what `recommend_allocation` returns in `votePercents`; anything else is refused rather than normalised, so the bytes always match the table the user was shown.",
    inputSchema: {
      tokenId: z
        .string()
        .regex(/^[0-9]+$/, "veNFT id must be a positive whole number")
        .describe("The veNFT to cast from, as a decimal string. Ids exceed Number.MAX_SAFE_INTEGER, so pass a string. `get_my_veaero` lists an account's locks; a wallet with several has no default — ask which one."),
      votePercents: z
        .array(
          z.object({
            pool: z.string().refine(isValidAddress, "Must be a 0x-prefixed 40-character hex address"),
            symbol: z.string(),
            percent: z.number().int().positive(),
          }),
        )
        .min(1)
        .describe("The `votePercents` array from `recommend_allocation`, unchanged: pool address, symbol and whole-percent weight, totalling 100."),
    },
  },
  withErrorHandling(async ({ tokenId, votePercents }) => {
    const tx = buildVoteCalldata(tokenId, votePercents);

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(
            {
              ...tx,
              note: "Unsigned and unsent. Show the user the pools, the weights and the `to` address, and tell them plainly that signing it in their own wallet is what casts the vote and that only the owner of that veNFT can. Do not describe the vote as cast, submitted or done. `value` is zero: voting moves no funds, but the transaction does commit that veNFT's voting power for the epoch.",
            },
            null,
            2,
          ),
        },
      ],
    };
  }),
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

// Only run the server when this file is executed directly (as the CLI binary
// or via `npx tsx src/mcp-server.ts`), not when it's imported — e.g. by tests
// importing `resolveVeAeroBudget`. `server.connect` never resolves for the
// life of the stdio connection, so importing this module would otherwise hang
// the importing process forever waiting on stdin.
const isMainModule = process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href;
if (isMainModule) {
  main().catch((err) => {
    console.error("aero-vote-radar MCP server failed to start:", err);
    process.exit(1);
  });
}

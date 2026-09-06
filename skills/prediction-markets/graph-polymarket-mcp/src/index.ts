#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import express from "express";
import { z } from "zod";
import { querySubgraph } from "./graphClient.js";
import { SUBGRAPHS, SUBGRAPH_NAMES } from "./subgraphs.js";
import {
  searchMarkets,
  getMarketBySlug,
  getMarketByConditionId,
  listEvents,
  getEvent,
  getClobPrice,
  getClobPricesBatch,
  getClobMidpoint,
  getClobSpread,
  getClobOrderBook,
  getClobLastTradePrice,
  getClobPriceHistory,
  getClobMarket,
} from "./polymarketApi.js";

const server = new McpServer({
  name: "graph-polymarket-mcp",
  version: "2.1.2",
});

// Helper to format tool responses
function textResult(data: unknown) {
  return {
    content: [{ type: "text" as const, text: JSON.stringify(data, null, 2) }],
  };
}

function errorResult(error: unknown) {
  const message = error instanceof Error ? error.message : String(error);
  return {
    content: [{ type: "text" as const, text: `Error: ${message}` }],
    isError: true,
  };
}

// ---------------------------------------------------------------------------
// Tool 1: list_subgraphs
// ---------------------------------------------------------------------------
server.registerTool(
  "list_subgraphs",
  {
    description: "List all available Polymarket subgraphs with descriptions and key entities",
  },
  async () => {
    const list = Object.entries(SUBGRAPHS).map(([key, cfg]) => ({
      id: key,
      name: cfg.name,
      ipfsHash: cfg.ipfsHash,
      // `era` and `syncWarning` are surfaced, not just stored: this list is what a model reads
      // when it picks a subgraph, and picking a stale one returns data rather than an error.
      era: cfg.era ?? "v1",
      ...(cfg.syncWarning ? { syncWarning: cfg.syncWarning } : {}),
      ...(cfg.availability ? { availability: cfg.availability } : {}),
      description: cfg.description,
      keyEntities: cfg.keyEntities,
    }));
    return textResult({
      subgraphs: list,
      choosing:
        "V1 and V2 are different eras, not old and new. Polymarket migrated to V2 exchange " +
        "contracts on 2026-04-28; the v2_* subgraphs start at block 84902353 and hold NO earlier " +
        "history. All-time or pre-migration questions belong on the V1 entries. Builder-code " +
        "attribution exists only on v2_orderbook. Any entry carrying a syncWarning is behind " +
        "chainhead and will answer with stale data rather than erroring — check its _meta block " +
        "before trusting a 'current' number from it.",
    });
  }
);

// ---------------------------------------------------------------------------
// Tool 2: get_subgraph_schema
// ---------------------------------------------------------------------------
server.registerTool(
  "get_subgraph_schema",
  {
    description: "Get the full GraphQL schema (introspection) for a Polymarket subgraph",
    inputSchema: {
      subgraph: z
        .enum(SUBGRAPH_NAMES)
        .describe("Subgraph identifier: main, beefy_pnl, slimmed_pnl, activity, or orderbook"),
    },
  },
  async ({ subgraph }) => {
    try {
      const cfg = SUBGRAPHS[subgraph];
      const introspectionQuery = `{
        __schema {
          types {
            name
            kind
            fields {
              name
              type { name kind ofType { name kind } }
            }
          }
        }
      }`;
      const data = await querySubgraph(cfg.ipfsHash, introspectionQuery);
      return textResult(data);
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 3: query_subgraph
// ---------------------------------------------------------------------------
server.registerTool(
  "query_subgraph",
  {
    description: "Execute a custom GraphQL query against a Polymarket subgraph",
    inputSchema: {
      subgraph: z
        .enum(SUBGRAPH_NAMES)
        .describe("Subgraph identifier: main, beefy_pnl, slimmed_pnl, activity, or orderbook"),
      query: z.string().describe("GraphQL query string"),
      variables: z
        .record(z.unknown())
        .optional()
        .describe("Optional GraphQL variables as key-value pairs"),
    },
  },
  async ({ subgraph, query, variables }) => {
    try {
      const cfg = SUBGRAPHS[subgraph];
      const data = await querySubgraph(cfg.ipfsHash, query, variables);
      return textResult(data);
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 4: get_market_data
// ---------------------------------------------------------------------------
server.registerTool(
  "get_market_data",
  {
    description: "Get Polymarket market/condition data including outcomes and volumes from the Main subgraph",
    inputSchema: {
      first: z.number().min(1).max(100).default(10).describe("Number of markets to return (1-100)"),
      orderBy: z.string().default("id").describe("Field to order by"),
      orderDirection: z.enum(["asc", "desc"]).default("desc").describe("Sort direction"),
    },
  },
  async ({ first, orderBy, orderDirection }) => {
    try {
      const query = `{
        conditions(first: ${first}, orderBy: ${orderBy}, orderDirection: ${orderDirection}) {
          id
          oracle
          questionId
          outcomeSlotCount
          resolutionTimestamp
          payoutNumerators
          payoutDenominator
        }
      }`;
      const data = await querySubgraph(SUBGRAPHS.main.ipfsHash, query);
      return textResult(data);
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 5: get_account_pnl
// ---------------------------------------------------------------------------
server.registerTool(
  "get_account_pnl",
  {
    description: "Get a trader's P&L and performance metrics from the Beefy P&L subgraph",
    inputSchema: {
      account: z.string().describe("Ethereum address of the trader (lowercase)"),
    },
  },
  async ({ account }) => {
    try {
      const query = `{
        account(id: "${account.toLowerCase()}") {
          id
          creationTimestamp
          lastTradedTimestamp
          isActive
          numTrades
          collateralVolume
          totalRealizedPnl
          totalUnrealizedPnl
          totalFeesPaid
          winRate
          profitFactor
          maxDrawdown
          numWinningPositions
          numLosingPositions
          totalProfitsSum
          totalLossesSum
        }
      }`;
      const data = await querySubgraph(SUBGRAPHS.beefy_pnl.ipfsHash, query);
      return textResult(data);
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 6: get_user_positions
// ---------------------------------------------------------------------------
server.registerTool(
  "get_user_positions",
  {
    description:
      "Get a user's current positions from the Slimmed P&L subgraph. Falls back gracefully if indexers are behind.",
    inputSchema: {
      account: z.string().describe("Ethereum address of the user (lowercase)"),
    },
  },
  async ({ account }) => {
    try {
      const addr = account.toLowerCase();
      const posQuery = `{
        userPositions(where: { user: "${addr}" }, first: 100) {
          id user tokenId amount avgPrice realizedPnl totalBought
        }
      }`;
      const obQuery = `{
        account(id: "${addr}") {
          id totalVolume tradesQuantity totalFees
        }
      }`;
      const [posData, obData] = await Promise.all([
        querySubgraph(SUBGRAPHS.slimmed_pnl.ipfsHash, posQuery),
        querySubgraph(SUBGRAPHS.orderbook.ipfsHash, obQuery).catch(() => null),
      ]);
      const pd = posData as { userPositions?: Array<{ totalBought: string }> };
      const totalBought = (pd.userPositions ?? []).reduce(
        (sum, p) => sum + parseFloat(p.totalBought || "0"), 0
      );
      const od = obData as { account?: { totalVolume?: string; tradesQuantity?: string } } | null;
      const obVolume = parseFloat(od?.account?.totalVolume || "0");
      const obTrades = parseInt(od?.account?.tradesQuantity || "0");
      let reliabilityWarning: string | undefined;
      if (obVolume > 0 && totalBought === 0) {
        reliabilityWarning = `⚠ orderbook-only entry — no split collateral detected. OB volume: $${obVolume.toFixed(2)} across ${obTrades} trades. P&L from totalBought/avgPrice fields is unreliable.`;
      } else if (obVolume > 0 && obVolume > totalBought * 2 && obVolume - totalBought > 1000) {
        reliabilityWarning = `⚠ mixed entry — OB volume ($${obVolume.toFixed(2)}) significantly exceeds split collateral ($${totalBought.toFixed(2)}). Some positions entered via orderbook buys; P&L may be understated.`;
      }
      return textResult({
        positions: pd.userPositions ?? [],
        orderbookAccount: od?.account ?? null,
        ...(reliabilityWarning ? { reliabilityWarning } : {}),
      });
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 7: get_recent_activity
// ---------------------------------------------------------------------------
server.registerTool(
  "get_recent_activity",
  {
    description: "Get recent splits, merges, and redemptions from the Activity subgraph",
    inputSchema: {
      first: z.number().min(1).max(100).default(20).describe("Number of events to return"),
      account: z.string().optional().describe("Optional: filter by Ethereum address"),
    },
  },
  async ({ first, account }) => {
    try {
      const addr = account?.toLowerCase();
      const stakeholderWhere = addr ? `, where: { stakeholder: "${addr}" }` : "";
      const redeemerWhere = addr ? `, where: { redeemer: "${addr}" }` : "";
      const activityQuery = `{
        splits(first: ${first}, orderBy: timestamp, orderDirection: desc${stakeholderWhere}) {
          id stakeholder amount timestamp
        }
        merges(first: ${first}, orderBy: timestamp, orderDirection: desc${stakeholderWhere}) {
          id stakeholder amount timestamp
        }
        redemptions(first: ${first}, orderBy: timestamp, orderDirection: desc${redeemerWhere}) {
          id redeemer payout indexSets timestamp
        }
      }`;
      // Fetch OB fills: if account-filtered, query as maker + taker separately; else recent fills
      const obQuery = addr
        ? `{
            makerFills: orderFilledEvents(first: ${first}, orderBy: timestamp, orderDirection: desc, where: { maker: "${addr}" }) {
              id maker taker price side fee makerAmountFilled takerAmountFilled timestamp
            }
            takerFills: orderFilledEvents(first: ${first}, orderBy: timestamp, orderDirection: desc, where: { taker: "${addr}" }) {
              id maker taker price side fee makerAmountFilled takerAmountFilled timestamp
            }
          }`
        : `{
            orderFilledEvents(first: ${first}, orderBy: timestamp, orderDirection: desc) {
              id maker taker price side fee makerAmountFilled takerAmountFilled timestamp
            }
          }`;
      const [actData, obData] = await Promise.all([
        querySubgraph(SUBGRAPHS.activity.ipfsHash, activityQuery),
        querySubgraph(SUBGRAPHS.orderbook.ipfsHash, obQuery).catch(() => null),
      ]);
      type EventRecord = { eventType: string; timestamp: string; [key: string]: unknown };
      const ad = actData as {
        splits?: Array<{ id: string; stakeholder: string; amount: string; timestamp: string }>;
        merges?: Array<{ id: string; stakeholder: string; amount: string; timestamp: string }>;
        redemptions?: Array<{ id: string; redeemer: string; payout: string; timestamp: string }>;
      };
      const od = obData as {
        orderFilledEvents?: Array<{ id: string; timestamp: string }>;
        makerFills?: Array<{ id: string; timestamp: string }>;
        takerFills?: Array<{ id: string; timestamp: string }>;
      } | null;
      const events: EventRecord[] = [
        ...(ad.splits ?? []).map((e) => ({ eventType: "split", ...e })),
        ...(ad.merges ?? []).map((e) => ({ eventType: "merge", ...e })),
        ...(ad.redemptions ?? []).map((e) => ({ eventType: "redemption", ...e })),
      ];
      const rawFills = od
        ? addr
          ? [
              ...(od.makerFills ?? []).map((e) => ({ eventType: "ob_fill_maker", ...e })),
              ...(od.takerFills ?? []).map((e) => ({ eventType: "ob_fill_taker", ...e })),
            ]
          : (od.orderFilledEvents ?? []).map((e) => ({ eventType: "ob_fill", ...e }))
        : [];
      // Deduplicate fills (same fill can appear as both maker and taker)
      const seen = new Set<string>();
      for (const e of rawFills) {
        if (!seen.has(e.id as string)) {
          seen.add(e.id as string);
          events.push(e as EventRecord);
        }
      }
      events.sort((a, b) => parseInt(b.timestamp) - parseInt(a.timestamp));
      return textResult({ feed: events.slice(0, first * 2) });
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 8: get_orderbook_trades
// ---------------------------------------------------------------------------
server.registerTool(
  "get_orderbook_trades",
  {
    description: "Get recent order fills from the Orderbook subgraph",
    inputSchema: {
      first: z.number().min(1).max(100).default(20).describe("Number of trades to return"),
      maker: z.string().optional().describe("Optional: filter by maker address"),
      taker: z.string().optional().describe("Optional: filter by taker address"),
    },
  },
  async ({ first, maker, taker }) => {
    try {
      const filters: string[] = [];
      if (maker) filters.push(`maker: "${maker.toLowerCase()}"`);
      if (taker) filters.push(`taker: "${taker.toLowerCase()}"`);
      const where = filters.length > 0 ? `, where: { ${filters.join(", ")} }` : "";

      const query = `{
        orderFilledEvents(first: ${first}, orderBy: timestamp, orderDirection: desc${where}) {
          id
          maker
          taker
          makerAssetId
          takerAssetId
          makerAmountFilled
          takerAmountFilled
          fee
          price
          side
          timestamp
        }
      }`;
      const data = await querySubgraph(SUBGRAPHS.orderbook.ipfsHash, query);
      return textResult(data);
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 9: get_global_stats
// ---------------------------------------------------------------------------
server.registerTool(
  "get_global_stats",
  {
    description:
      "Get aggregate Polymarket platform statistics. Combines market counts from the Main subgraph with accurate volume/fee/trade data from the Orderbook subgraph.",
  },
  async () => {
    try {
      // Main subgraph: reliable for condition/trader counts
      const mainQuery = `{
        globals {
          id
          numConditions
          numOpenConditions
          numClosedConditions
          numTraders
        }
      }`;
      // Orderbook subgraph: authoritative source for volume (main Global has zeroed volume fields)
      const orderbookQuery = `{
        ordersMatchedGlobals(first: 1) {
          id
          tradesQuantity
          buysQuantity
          sellsQuantity
          collateralVolume
          scaledCollateralVolume
          collateralBuyVolume
          scaledCollateralBuyVolume
          collateralSellVolume
          scaledCollateralSellVolume
          totalFees
          averageTradeSize
        }
      }`;
      const [mainData, orderbookData] = await Promise.all([
        querySubgraph(SUBGRAPHS.main.ipfsHash, mainQuery),
        querySubgraph(SUBGRAPHS.orderbook.ipfsHash, orderbookQuery),
      ]);
      return textResult({ markets: mainData, volume: orderbookData });
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 10: get_daily_stats
// ---------------------------------------------------------------------------
server.registerTool(
  "get_daily_stats",
  {
    description:
      "Get daily platform statistics from the Beefy P&L subgraph: volume, fees, trader counts, and market activity per day. Use this for trend analysis and historical performance.",
    inputSchema: {
      days: z.number().min(1).max(90).default(7).describe("Number of recent days to return (1-90)"),
    },
  },
  async ({ days }) => {
    try {
      const query = `{
        dailyStats_collection(first: ${days}, orderBy: date, orderDirection: desc) {
          id
          date
          volume
          fees
          numTraders
          numNewMarkets
          numResolvedMarkets
        }
      }`;
      const data = await querySubgraph(SUBGRAPHS.beefy_pnl.ipfsHash, query);
      return textResult(data);
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 11: get_top_traders
// ---------------------------------------------------------------------------
server.registerTool(
  "get_top_traders",
  {
    description:
      "Get the top Polymarket traders ranked by realized P&L, win rate, or volume from the Beefy P&L subgraph.",
    inputSchema: {
      first: z.number().min(1).max(100).default(10).describe("Number of traders to return (1-100)"),
      orderBy: z
        .enum(["totalRealizedPnl", "collateralVolume", "winRate", "profitFactor", "numTrades"])
        .default("totalRealizedPnl")
        .describe("Metric to rank traders by"),
      minTrades: z
        .number()
        .min(1)
        .default(10)
        .describe("Minimum number of trades to filter out inactive accounts"),
    },
  },
  async ({ first, orderBy, minTrades }) => {
    try {
      const beefyQuery = `{
        accounts(
          first: ${first},
          orderBy: ${orderBy},
          orderDirection: desc,
          where: { numTrades_gte: "${minTrades}" }
        ) {
          id numTrades collateralVolume totalRealizedPnl totalUnrealizedPnl
          totalFeesPaid winRate profitFactor maxDrawdown
          numWinningPositions numLosingPositions lastTradedTimestamp
        }
      }`;
      // Fetch top OB-volume accounts to surface OB-only traders absent from Beefy rankings
      const obQuery = `{
        accounts(first: ${first}, orderBy: totalVolume, orderDirection: desc) {
          id totalVolume tradesQuantity
        }
      }`;
      const [beefyData, obData] = await Promise.all([
        querySubgraph(SUBGRAPHS.beefy_pnl.ipfsHash, beefyQuery),
        querySubgraph(SUBGRAPHS.orderbook.ipfsHash, obQuery).catch(() => null),
      ]);
      const bd = beefyData as { accounts?: Array<{ id: string; collateralVolume?: string }> };
      const od = obData as { accounts?: Array<{ id: string; totalVolume: string; tradesQuantity: string }> } | null;
      const beefyIds = new Set((bd.accounts ?? []).map((a) => a.id));
      const obById = new Map((od?.accounts ?? []).map((a) => [a.id, a]));
      // Flag beefy rows where OB-tracked volume significantly exceeds Beefy-tracked volume
      const annotated = (bd.accounts ?? []).map((a) => {
        const ob = obById.get(a.id);
        const beefyVol = parseFloat(a.collateralVolume || "0");
        const obVol = ob ? parseFloat(ob.totalVolume) : null;
        const flag =
          obVol !== null && obVol > beefyVol * 1.5 && obVol - beefyVol > 1000
            ? `⚠ OB volume ($${obVol.toFixed(0)}) exceeds Beefy-tracked volume ($${beefyVol.toFixed(0)}) — P&L ranking may be incomplete`
            : undefined;
        return { ...a, ...(flag ? { reliabilityWarning: flag } : {}) };
      });
      // Surface high-volume OB traders completely absent from Beefy leaderboard
      const obOnlyTraders = (od?.accounts ?? [])
        .filter((a) => !beefyIds.has(a.id))
        .map((a) => ({ address: a.id, obVolume: a.totalVolume, obTrades: a.tradesQuantity, note: "not tracked by Beefy P&L subgraph — P&L unavailable" }));
      return textResult({
        traders: annotated,
        ...(obOnlyTraders.length > 0 ? { obOnlyTradersNotInLeaderboard: obOnlyTraders } : {}),
      });
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 12: get_market_positions
// ---------------------------------------------------------------------------
server.registerTool(
  "get_market_positions",
  {
    description:
      "Get the top positions for a specific market token from the Beefy P&L subgraph. Shows who holds the largest positions and their P&L.",
    inputSchema: {
      tokenId: z
        .string()
        .describe(
          "The outcome token ID — same value as clobTokenIds from search_markets/get_market_info, token_id from get_clob_market, or makerAssetId/takerAssetId from get_orderbook_trades"
        ),
      first: z.number().min(1).max(100).default(20).describe("Number of positions to return"),
      orderBy: z
        .enum(["realizedPnl", "unrealizedPnl", "valueBought"])
        .default("valueBought")
        .describe("Field to sort by"),
    },
  },
  async ({ tokenId, first, orderBy }) => {
    try {
      const query = `{
        marketPositions(
          first: ${first},
          orderBy: ${orderBy},
          orderDirection: desc,
          where: { id_contains: "${tokenId}" }
        ) {
          id
          realizedPnl
          unrealizedPnl
          valueBought
          valueSold
        }
      }`;
      const data = await querySubgraph(SUBGRAPHS.beefy_pnl.ipfsHash, query);
      return textResult(data);
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 13: get_market_open_interest
// ---------------------------------------------------------------------------
server.registerTool(
  "get_market_open_interest",
  {
    description:
      "Get the top Polymarket markets ranked by open interest (USDC locked in outstanding positions). This data is unique to the Open Interest subgraph — no other Polymarket subgraph tracks OI.",
    inputSchema: {
      first: z.number().min(1).max(100).default(10).describe("Number of markets to return (1-100)"),
      orderBy: z
        .enum(["amount", "splitCount", "mergeCount", "lastUpdatedTimestamp"])
        .default("amount")
        .describe("Field to rank markets by"),
      orderDirection: z.enum(["asc", "desc"]).default("desc").describe("Sort direction"),
    },
  },
  async ({ first, orderBy, orderDirection }) => {
    try {
      const oiQuery = `{
        marketOpenInterests(first: ${first}, orderBy: ${orderBy}, orderDirection: ${orderDirection}) {
          id conditionId amount amountRaw splitCount mergeCount redemptionCount
          createdAtTimestamp lastUpdatedTimestamp
        }
      }`;
      const oiData = await querySubgraph(SUBGRAPHS.open_interest.ipfsHash, oiQuery);
      const od = oiData as { marketOpenInterests?: Array<{ conditionId: string; amount: string }> };
      const conditionIds = (od.marketOpenInterests ?? []).map((m) => m.conditionId).filter(Boolean);
      // Cross-ref Main subgraph: payoutDenominator > 0 means market is resolved
      const resolutionMap = new Map<string, boolean>();
      if (conditionIds.length > 0) {
        const ids = conditionIds.map((id) => `"${id}"`).join(", ");
        const mainQuery = `{ conditions(where: { id_in: [${ids}] }) { id payoutDenominator } }`;
        const mainData = await querySubgraph(SUBGRAPHS.main.ipfsHash, mainQuery).catch(() => null);
        if (mainData) {
          const md = mainData as { conditions?: Array<{ id: string; payoutDenominator: string }> };
          for (const c of md.conditions ?? []) {
            resolutionMap.set(c.id, parseInt(c.payoutDenominator || "0") > 0);
          }
        }
      }
      const annotated = (od.marketOpenInterests ?? []).map((m) => {
        if (resolutionMap.get(m.conditionId)) {
          return {
            ...m,
            warning: `⚠ dead money — market resolved. $${parseFloat(m.amount).toFixed(2)} OI represents worthless losing-side tokens that will never be redeemed on-chain.`,
          };
        }
        return m;
      });
      const deadMoneyTotal = (od.marketOpenInterests ?? [])
        .filter((m) => resolutionMap.get(m.conditionId))
        .reduce((sum, m) => sum + parseFloat(m.amount || "0"), 0);
      return textResult({
        markets: annotated,
        ...(deadMoneyTotal > 0
          ? { deadMoneyOI: `$${deadMoneyTotal.toFixed(2)} of displayed OI is from resolved markets (losing tokens — not redeemable on-chain)` }
          : {}),
      });
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 14: get_oi_history
// ---------------------------------------------------------------------------
server.registerTool(
  "get_oi_history",
  {
    description:
      "Get hourly open interest snapshots for a specific Polymarket market. Use this to chart OI trends over time. The conditionId can be obtained from get_market_open_interest or the main subgraph.",
    inputSchema: {
      conditionId: z.string().describe("The conditionId (hex string) of the market"),
      first: z.number().min(1).max(1000).default(168).describe("Number of hourly snapshots to return (default 168 = 1 week)"),
      orderDirection: z.enum(["asc", "desc"]).default("desc").describe("Sort direction by timestamp"),
    },
  },
  async ({ conditionId, first, orderDirection }) => {
    try {
      const query = `{
        oisnapshots(
          first: ${first},
          orderBy: timestamp,
          orderDirection: ${orderDirection},
          where: { market: "${conditionId.toLowerCase()}" }
        ) {
          id
          amount
          amountRaw
          blockNumber
          timestamp
        }
      }`;
      const data = await querySubgraph(SUBGRAPHS.open_interest.ipfsHash, query);
      return textResult(data);
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 15: get_global_open_interest
// ---------------------------------------------------------------------------
server.registerTool(
  "get_global_open_interest",
  {
    description:
      "Get the total open interest across all Polymarket markets — the aggregate USDC locked in outstanding positions platform-wide.",
  },
  async () => {
    try {
      const query = `{
        globalOpenInterests(first: 1) {
          id
          amount
          amountRaw
          marketCount
          lastUpdatedBlock
          lastUpdatedTimestamp
        }
      }`;
      const data = await querySubgraph(SUBGRAPHS.open_interest.ipfsHash, query);
      return textResult(data);
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 16: get_market_resolution
// ---------------------------------------------------------------------------
server.registerTool(
  "get_market_resolution",
  {
    description:
      "Get the UMA oracle resolution status for Polymarket markets. Shows whether a market is initialized, proposed, disputed, or resolved, plus proposed/final prices and dispute history.",
    inputSchema: {
      first: z.number().min(1).max(100).default(10).describe("Number of markets to return (1-100)"),
      status: z
        .enum(["initialized", "proposed", "resolved", "disputed", "challenged", "reproposed"])
        .optional()
        .describe("Optional: filter by resolution status"),
      orderBy: z
        .enum(["lastUpdateTimestamp", "id"])
        .default("lastUpdateTimestamp")
        .describe("Field to sort by"),
      orderDirection: z.enum(["asc", "desc"]).default("desc").describe("Sort direction"),
    },
  },
  async ({ first, status, orderBy, orderDirection }) => {
    try {
      const where = status ? `, where: { status: "${status}" }` : "";
      const query = `{
        marketResolutions(first: ${first}, orderBy: ${orderBy}, orderDirection: ${orderDirection}${where}) {
          id
          status
          flagged
          paused
          wasDisputed
          proposedPrice
          reproposedPrice
          price
          lastUpdateTimestamp
          requestTransactionHash
          resolutionTransactionHash
        }
      }`;
      const data = await querySubgraph(SUBGRAPHS.resolution.ipfsHash, query);
      return textResult(data);
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 17: get_disputed_markets
// ---------------------------------------------------------------------------
server.registerTool(
  "get_disputed_markets",
  {
    description:
      "Get Polymarket markets that were disputed during the UMA oracle resolution process. Disputes happen when someone challenges a proposed outcome — these are high-signal events.",
    inputSchema: {
      first: z.number().min(1).max(100).default(20).describe("Number of disputed markets to return"),
    },
  },
  async ({ first }) => {
    try {
      const query = `{
        marketResolutions(first: ${first}, orderBy: lastUpdateTimestamp, orderDirection: desc, where: { wasDisputed: true }) {
          id
          status
          flagged
          proposedPrice
          reproposedPrice
          price
          wasDisputed
          lastUpdateTimestamp
          requestTransactionHash
          resolutionTransactionHash
        }
      }`;
      const data = await querySubgraph(SUBGRAPHS.resolution.ipfsHash, query);
      return textResult(data);
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 18: get_market_revisions
// ---------------------------------------------------------------------------
server.registerTool(
  "get_market_revisions",
  {
    description:
      "Get moderator revisions/updates for Polymarket markets. Shows when and how moderators intervened in market resolution.",
    inputSchema: {
      questionId: z.string().optional().describe("Optional: filter revisions for a specific market questionId"),
      first: z.number().min(1).max(100).default(20).describe("Number of revisions to return"),
    },
  },
  async ({ questionId, first }) => {
    try {
      const where = questionId ? `, where: { questionId: "${questionId}" }` : "";
      const query = `{
        revisions(first: ${first}, orderBy: timestamp, orderDirection: desc${where}) {
          id
          moderator
          questionId
          timestamp
          update
          transactionHash
        }
      }`;
      const data = await querySubgraph(SUBGRAPHS.resolution.ipfsHash, query);
      return textResult(data);
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 19: get_trader_profile
// ---------------------------------------------------------------------------
server.registerTool(
  "get_trader_profile",
  {
    description:
      "Get a trader's on-chain profile from the Traders subgraph: when they first appeared, their recent CTF events (splits, merges, transfers), and USDC flows.",
    inputSchema: {
      address: z.string().describe("Ethereum address of the trader"),
      eventLimit: z.number().min(1).max(100).default(20).describe("Number of recent events to return"),
    },
  },
  async ({ address, eventLimit }) => {
    try {
      const addr = address.toLowerCase();
      const tradersQuery = `{
        trader(id: "${addr}") {
          id firstSeenBlock firstSeenTimestamp
          ctfEvents(first: ${eventLimit}, orderBy: timestamp, orderDirection: desc) {
            id eventType conditionId amounts blockNumber timestamp
          }
          usdcTransfers(first: ${eventLimit}, orderBy: timestamp, orderDirection: desc) {
            id from to amount isInbound blockNumber timestamp
          }
        }
      }`;
      const obQuery = `{
        makerFills: orderFilledEvents(first: ${eventLimit}, orderBy: timestamp, orderDirection: desc, where: { maker: "${addr}" }) {
          id maker taker price side fee makerAmountFilled takerAmountFilled timestamp
        }
        takerFills: orderFilledEvents(first: ${eventLimit}, orderBy: timestamp, orderDirection: desc, where: { taker: "${addr}" }) {
          id maker taker price side fee makerAmountFilled takerAmountFilled timestamp
        }
        account(id: "${addr}") {
          id collateralVolume numTrades
        }
      }`;
      const [tradersData, obData] = await Promise.all([
        querySubgraph(SUBGRAPHS.traders.ipfsHash, tradersQuery),
        querySubgraph(SUBGRAPHS.orderbook.ipfsHash, obQuery).catch(() => null),
      ]);
      const od = obData as {
        makerFills?: Array<{ id: string; timestamp: string }>;
        takerFills?: Array<{ id: string; timestamp: string }>;
        account?: { id: string; collateralVolume: string; numTrades: string };
      } | null;
      // Deduplicate and merge fills
      const seen = new Set<string>();
      const allFills = [
        ...(od?.makerFills ?? []).map((e) => ({ ...e, role: "maker" })),
        ...(od?.takerFills ?? []).map((e) => ({ ...e, role: "taker" })),
      ]
        .filter((e) => {
          if (seen.has(e.id)) return false;
          seen.add(e.id);
          return true;
        })
        .sort((a, b) => parseInt(b.timestamp) - parseInt(a.timestamp));
      const td = tradersData as { trader?: { ctfEvents?: unknown[] } };
      const hasCTFEvents = (td.trader?.ctfEvents?.length ?? 0) > 0;
      const hasOBFills = allFills.length > 0;
      const obVolume = parseFloat(od?.account?.collateralVolume || "0");
      let entryType: string;
      if (hasCTFEvents && hasOBFills) entryType = "hybrid (split collateral + orderbook buys)";
      else if (!hasCTFEvents && hasOBFills) entryType = "⚠ orderbook-only — no split collateral detected";
      else if (hasCTFEvents && !hasOBFills) entryType = "split-collateral only";
      else entryType = "no activity detected";
      return textResult({
        ...(tradersData as object),
        orderbookFills: allFills,
        orderbookAccount: od?.account ?? null,
        entryType,
        ...(obVolume > 0 && !hasCTFEvents
          ? { pnlWarning: `⚠ wallet entered entirely via orderbook buys ($${obVolume.toFixed(2)} OB volume) — P&L from Slimmed/Beefy subgraphs is unreliable` }
          : {}),
      });
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 20: get_trader_usdc_flows
// ---------------------------------------------------------------------------
server.registerTool(
  "get_trader_usdc_flows",
  {
    description:
      "Get USDC deposit/withdrawal history for a trader. Shows inbound and outbound USDC transfers, useful for tracking when traders fund or withdraw from Polymarket.",
    inputSchema: {
      address: z.string().describe("Ethereum address of the trader"),
      direction: z.enum(["inbound", "outbound", "both"]).default("both").describe("Filter by transfer direction"),
      first: z.number().min(1).max(100).default(50).describe("Number of transfers to return"),
    },
  },
  async ({ address, direction, first }) => {
    try {
      const addr = address.toLowerCase();
      const dirFilter =
        direction === "both"
          ? `trader: "${addr}"`
          : `trader: "${addr}", isInbound: ${direction === "inbound"}`;
      const query = `{
        usdctransfers(first: ${first}, orderBy: timestamp, orderDirection: desc, where: { ${dirFilter} }) {
          id
          from
          to
          amount
          isInbound
          blockNumber
          timestamp
        }
      }`;
      const data = await querySubgraph(SUBGRAPHS.traders.ipfsHash, query);
      return textResult(data);
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ===========================================================================
// Polymarket REST API Tools (Gamma + CLOB) — powered by polymarket-cli APIs
// ===========================================================================

// ---------------------------------------------------------------------------
// Tool 21: search_markets
// ---------------------------------------------------------------------------
server.registerTool(
  "search_markets",
  {
    description:
      "Search Polymarket prediction markets by text query. Returns market metadata including question, prices, volume, liquidity, and CLOB token IDs. Uses the Gamma API for real-time market discovery. Chain with: get_clob_market(conditionId) for live order books, get_live_prices(clobTokenIds) for token-level pricing, get_market_open_interest for capital locked, or get_market_resolution for oracle status.",
    inputSchema: {
      query: z.string().describe("Search text (e.g. 'Trump', 'Bitcoin', 'World Cup')"),
      limit: z.number().min(1).max(100).default(10).describe("Number of results (1-100)"),
      active: z.boolean().optional().describe("Filter: only active markets"),
      closed: z.boolean().optional().describe("Filter: only closed/resolved markets"),
      orderBy: z
        .enum(["volume", "liquidity", "endDate", "startDate", "createdAt"])
        .optional()
        .describe("Sort field"),
      ascending: z.boolean().default(false).describe("Sort ascending (default: descending)"),
    },
  },
  async ({ query, limit, active, closed, orderBy, ascending }) => {
    try {
      const markets = await searchMarkets(query, { limit, active, closed, orderBy, ascending });
      return textResult({
        count: markets.length,
        markets: markets.map((m) => ({
          id: m.id,
          question: m.question,
          slug: m.slug,
          conditionId: m.conditionId,
          active: m.active,
          closed: m.closed,
          outcomePrices: m.outcomePrices,
          outcomes: m.outcomes,
          bestBid: m.bestBid,
          bestAsk: m.bestAsk,
          lastTradePrice: m.lastTradePrice,
          spread: m.spread,
          volume: m.volume,
          liquidity: m.liquidity,
          endDate: m.endDate,
          clobTokenIds: m.clobTokenIds,
          description: m.description,
        })),
      });
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 22: get_market_info
// ---------------------------------------------------------------------------
server.registerTool(
  "get_market_info",
  {
    description:
      "Get detailed Polymarket market info by slug or condition ID. Returns full market metadata from the Gamma API including description, prices, outcomes, and CLOB token IDs. Use the returned conditionId to query get_clob_market for live CLOB data, get_market_open_interest for OI, or get_market_resolution for oracle status.",
    inputSchema: {
      slug: z.string().optional().describe("Market slug (e.g. 'will-trump-win-2024')"),
      conditionId: z.string().optional().describe("Market condition ID (hex string)"),
    },
  },
  async ({ slug, conditionId }) => {
    try {
      if (!slug && !conditionId) {
        return errorResult("Provide either slug or conditionId");
      }
      const markets = slug
        ? await getMarketBySlug(slug)
        : await getMarketByConditionId(conditionId!);
      if (markets.length === 0) {
        return textResult({ error: "Market not found", slug, conditionId });
      }
      return textResult(markets.length === 1 ? markets[0] : markets);
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 23: list_polymarket_events
// ---------------------------------------------------------------------------
server.registerTool(
  "list_polymarket_events",
  {
    description:
      "List Polymarket events (groups of related markets). Events bundle multiple Yes/No markets under one topic (e.g. 'US Presidential Election 2024' contains many candidate markets). Uses the Gamma API.",
    inputSchema: {
      limit: z.number().min(1).max(100).default(10).describe("Number of events (1-100)"),
      active: z.boolean().optional().describe("Filter: only active events"),
      closed: z.boolean().optional().describe("Filter: only closed events"),
      tag: z.string().optional().describe("Filter by tag (e.g. 'politics', 'crypto', 'sports')"),
      orderBy: z
        .enum(["volume", "liquidity", "startDate", "endDate", "createdAt"])
        .optional()
        .describe("Sort field"),
      ascending: z.boolean().default(false).describe("Sort ascending"),
    },
  },
  async ({ limit, active, closed, tag, orderBy, ascending }) => {
    try {
      const events = await listEvents({ limit, active, closed, tag, orderBy, ascending });
      return textResult({
        count: events.length,
        events: events.map((e) => ({
          id: e.id,
          title: e.title,
          slug: e.slug,
          description: e.description,
          startDate: e.startDate,
          endDate: e.endDate,
          marketCount: e.markets?.length ?? 0,
          markets: (e.markets ?? []).map((m) => ({
            id: m.id,
            question: m.question,
            outcomePrices: m.outcomePrices,
            volume: m.volume,
            active: m.active,
          })),
        })),
      });
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 24: get_polymarket_event
// ---------------------------------------------------------------------------
server.registerTool(
  "get_polymarket_event",
  {
    description:
      "Get a single Polymarket event with all its associated markets. An event groups related prediction markets under one topic.",
    inputSchema: {
      eventId: z.string().describe("Event ID or slug"),
    },
  },
  async ({ eventId }) => {
    try {
      const event = await getEvent(eventId);
      return textResult(event);
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 25: get_live_prices
// ---------------------------------------------------------------------------
server.registerTool(
  "get_live_prices",
  {
    description:
      "Get real-time CLOB prices for Polymarket outcome tokens. Returns the current best price for buying or selling. Token IDs come from: clobTokenIds in search_markets/get_market_info, or token_id in get_clob_market.",
    inputSchema: {
      tokenIds: z
        .array(z.string())
        .min(1)
        .max(20)
        .describe("Array of CLOB token IDs (get these from search_markets or get_market_info clobTokenIds field)"),
      side: z.enum(["buy", "sell"]).default("buy").describe("Price side: buy or sell"),
    },
  },
  async ({ tokenIds, side }) => {
    try {
      if (tokenIds.length === 1) {
        const result = await getClobPrice(tokenIds[0], side);
        return textResult({ tokenId: tokenIds[0], side, ...result });
      }
      const result = await getClobPricesBatch(tokenIds, side);
      return textResult({ side, prices: result });
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 26: get_live_spread
// ---------------------------------------------------------------------------
server.registerTool(
  "get_live_spread",
  {
    description:
      "Get the real-time bid-ask spread for a Polymarket outcome token. Returns best bid, best ask, and spread. Useful for assessing market liquidity and trading costs.",
    inputSchema: {
      tokenId: z.string().describe("CLOB token ID"),
    },
  },
  async ({ tokenId }) => {
    try {
      const [spread, midpoint] = await Promise.all([
        getClobSpread(tokenId),
        getClobMidpoint(tokenId),
      ]);
      return textResult({ tokenId, ...spread, midpoint: midpoint.mid });
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 27: get_live_orderbook
// ---------------------------------------------------------------------------
server.registerTool(
  "get_live_orderbook",
  {
    description:
      "Get the full real-time order book (bids and asks) for a Polymarket outcome token from the CLOB. Shows all resting limit orders with prices and sizes.",
    inputSchema: {
      tokenId: z.string().describe("CLOB token ID"),
    },
  },
  async ({ tokenId }) => {
    try {
      const book = await getClobOrderBook(tokenId);
      return textResult({
        tokenId,
        bidCount: book.bids?.length ?? 0,
        askCount: book.asks?.length ?? 0,
        bids: book.bids,
        asks: book.asks,
        timestamp: book.timestamp,
      });
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 28: get_price_history
// ---------------------------------------------------------------------------
server.registerTool(
  "get_price_history",
  {
    description:
      "Get historical price data for a Polymarket outcome token. Returns time-series price points for charting and trend analysis.",
    inputSchema: {
      tokenId: z.string().describe("CLOB token ID"),
      interval: z
        .enum(["1m", "5m", "1h", "6h", "1d", "1w", "max"])
        .default("1d")
        .describe("Time interval: 1m, 5m, 1h, 6h, 1d, 1w, or max"),
      fidelity: z
        .number()
        .min(1)
        .max(500)
        .default(60)
        .describe("Number of data points to return (1-500)"),
    },
  },
  async ({ tokenId, interval, fidelity }) => {
    try {
      const data = await getClobPriceHistory(tokenId, interval, fidelity);
      const history = (data.history ?? []).map((p) => ({
        timestamp: p.t,
        date: new Date(p.t * 1000).toISOString(),
        price: p.p,
      }));
      return textResult({
        tokenId,
        interval,
        pointCount: history.length,
        history,
      });
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 29: get_last_trade
// ---------------------------------------------------------------------------
server.registerTool(
  "get_last_trade",
  {
    description:
      "Get the last trade price for a Polymarket outcome token from the CLOB.",
    inputSchema: {
      tokenId: z.string().describe("CLOB token ID"),
    },
  },
  async ({ tokenId }) => {
    try {
      const result = await getClobLastTradePrice(tokenId);
      return textResult({ tokenId, ...result });
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 30: get_clob_market
// ---------------------------------------------------------------------------
server.registerTool(
  "get_clob_market",
  {
    description:
      "Get CLOB market details by condition ID. Returns token IDs (token_id) with live prices, minimum order/tick sizes, and market status. This is the bridge between on-chain condition IDs and CLOB trading data. Use the returned token_id values with get_live_prices, get_live_spread, get_live_orderbook, get_price_history, or get_market_positions.",
    inputSchema: {
      conditionId: z.string().describe("Market condition ID (hex string)"),
    },
  },
  async ({ conditionId }) => {
    try {
      const market = await getClobMarket(conditionId);
      return textResult(market);
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 31: search_markets_enriched
// ---------------------------------------------------------------------------
server.registerTool(
  "search_markets_enriched",
  {
    description:
      "Power tool: search Polymarket markets then auto-enrich each result with live CLOB prices and on-chain resolution status. Combines Gamma API + CLOB API + The Graph in one call — no need to chain tools manually.",
    inputSchema: {
      query: z.string().describe("Search text (e.g. 'Trump', 'Bitcoin', 'World Cup')"),
      limit: z.number().min(1).max(20).default(5).describe("Number of results (1-20, kept small for enrichment speed)"),
      active: z.boolean().optional().describe("Filter: only active markets"),
      closed: z.boolean().optional().describe("Filter: only closed/resolved markets"),
    },
  },
  async ({ query, limit, active, closed }) => {
    try {
      const markets = await searchMarkets(query, { limit, active, closed, orderBy: "volume" });

      // Enrich each market with CLOB prices and resolution status in parallel
      const enriched = await Promise.all(
        markets.map(async (m) => {
          const base = {
            question: m.question,
            slug: m.slug,
            conditionId: m.conditionId,
            active: m.active,
            closed: m.closed,
            volume: m.volume,
            liquidity: m.liquidity,
            endDate: m.endDate,
            outcomes: m.outcomes,
            outcomePrices: m.outcomePrices,
            clobTokenIds: m.clobTokenIds,
          };

          // Fetch CLOB market data + resolution status in parallel
          const [clobData, resolutionData] = await Promise.all([
            m.conditionId
              ? getClobMarket(m.conditionId).catch(() => null)
              : Promise.resolve(null),
            m.conditionId
              ? querySubgraph(
                  SUBGRAPHS.resolution.ipfsHash,
                  `{ marketResolutions(where: { id: "${m.conditionId.toLowerCase()}" }, first: 1) { status flagged wasDisputed proposedPrice price lastUpdateTimestamp } }`
                ).catch(() => null)
              : Promise.resolve(null),
          ]);

          const cd = clobData as {
            tokens?: Array<{ token_id: string; outcome: string; price: number; winner: boolean }>;
            minimum_tick_size?: string;
            accepting_orders?: boolean;
          } | null;

          const rd = resolutionData as {
            marketResolutions?: Array<{
              status: string;
              flagged: boolean;
              wasDisputed: boolean;
              proposedPrice: string;
              price: string;
              lastUpdateTimestamp: string;
            }>;
          } | null;

          return {
            ...base,
            liveTokens: cd?.tokens ?? null,
            acceptingOrders: cd?.accepting_orders ?? null,
            tickSize: cd?.minimum_tick_size ?? null,
            resolution: rd?.marketResolutions?.[0] ?? null,
          };
        })
      );

      return textResult({ count: enriched.length, markets: enriched });
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// MCP Prompts - guided workflows for agents
// ---------------------------------------------------------------------------
server.registerPrompt(
  "analyze_trader",
  {
    description: "Analyze a Polymarket trader's full profile: P&L, positions, and recent activity",
    argsSchema: { address: z.string().describe("Ethereum address of the trader") },
  },
  ({ address }) => ({
    messages: [
      {
        role: "user" as const,
        content: {
          type: "text" as const,
          text: `Analyze the Polymarket trader at address ${address}. Follow these steps:
1. Use get_account_pnl to get their P&L metrics and performance stats
2. Use get_trader_profile to see their on-chain history (CTF events and USDC flows)
3. Use get_user_positions to see their current open positions
4. Use get_orderbook_trades with the maker parameter to see their recent trades
5. Use get_recent_activity with the account parameter to check splits/merges/redemptions
6. Summarize: overall profitability, win rate, active positions, USDC deposit/withdrawal patterns, and trading behavior`,
        },
      },
    ],
  })
);

server.registerPrompt(
  "market_overview",
  {
    description: "Get a comprehensive overview of Polymarket platform activity",
    argsSchema: {},
  },
  () => ({
    messages: [
      {
        role: "user" as const,
        content: {
          type: "text" as const,
          text: `Give me a comprehensive Polymarket overview. Follow these steps:
1. Use get_global_stats to get platform-wide metrics (market counts from main + real volume from orderbook)
2. Use get_daily_stats with days=7 to see the last week of volume, fees, and trader trends
3. Use search_markets with orderBy=volume to find the hottest markets right now
4. Use get_orderbook_trades with first=10 to see the most recent trades
5. Use get_top_traders with first=5 orderBy=totalRealizedPnl to identify leading traders
6. Summarize: total volume, active markets, trending topics, daily trends, recent trades, and top performers`,
        },
      },
    ],
  })
);

server.registerPrompt(
  "explore_subgraph",
  {
    description: "Explore a specific Polymarket subgraph's schema and sample data",
    argsSchema: {
      subgraph: z.string().describe("Subgraph id: main, beefy_pnl, slimmed_pnl, activity, orderbook, open_interest, resolution, or traders"),
    },
  },
  ({ subgraph }) => ({
    messages: [
      {
        role: "user" as const,
        content: {
          type: "text" as const,
          text: `Help me explore the "${subgraph}" Polymarket subgraph. Follow these steps:
1. Use list_subgraphs to show what this subgraph contains and note any caveats
2. Use query_subgraph with subgraph="${subgraph}" to run this introspection: { __schema { queryType { fields { name } } } }
3. Pick 2-3 of the most interesting query fields and fetch sample data with query_subgraph
4. Explain what kinds of questions this subgraph can answer and any known limitations

Working example queries by subgraph:
- main: { conditions(first: 5, orderBy: id, orderDirection: desc) { id oracle questionId outcomeSlotCount resolutionTimestamp payoutNumerators } }
- beefy_pnl: { accounts(first: 5, orderBy: totalRealizedPnl, orderDirection: desc, where: { numTrades_gte: "10" }) { id winRate profitFactor totalRealizedPnl numTrades } }
- beefy_pnl daily: { dailyStats_collection(first: 7, orderBy: date, orderDirection: desc) { id date volume fees numTraders } }
- orderbook: { ordersMatchedGlobals(first: 1) { tradesQuantity collateralVolume totalFees averageTradeSize } }
- orderbook fills: { orderFilledEvents(first: 5, orderBy: timestamp, orderDirection: desc) { maker taker price side fee timestamp } }
- activity: { splits(first: 5, orderBy: timestamp, orderDirection: desc) { stakeholder amount timestamp } }
- open_interest: { marketOpenInterests(first: 5, orderBy: amount, orderDirection: desc) { id amount splitCount mergeCount lastUpdatedTimestamp } }
- open_interest global: { globalOpenInterests(first: 1) { amount marketCount lastUpdatedTimestamp } }
- open_interest history: { oisnapshots(first: 24, orderBy: timestamp, orderDirection: desc, where: { market: "0x..." }) { amount timestamp } }
- resolution: { marketResolutions(first: 5, orderBy: lastUpdateTimestamp, orderDirection: desc) { id status flagged wasDisputed proposedPrice price lastUpdateTimestamp } }
- resolution disputed: { marketResolutions(first: 5, where: { wasDisputed: true }) { id status proposedPrice reproposedPrice price } }
- traders: { trader(id: "0x...") { id firstSeenBlock firstSeenTimestamp ctfEvents(first: 5) { eventType conditionId amounts timestamp } } }
- traders usdc: { usdctransfers(first: 5, orderBy: timestamp, orderDirection: desc, where: { trader: "0x..." }) { from to amount isInbound timestamp } }`,
        },
      },
    ],
  })
);

server.registerPrompt(
  "daily_trends",
  {
    description: "Analyze Polymarket daily trading trends over a time period",
    argsSchema: {
      days: z.string().default("30").describe("Number of days to analyze (e.g. 7, 30, 90)"),
    },
  },
  ({ days }) => ({
    messages: [
      {
        role: "user" as const,
        content: {
          type: "text" as const,
          text: `Analyze Polymarket trading trends over the last ${days} days. Follow these steps:
1. Use get_daily_stats with days=${days} to get daily volume, fees, trader counts, and market activity
2. Identify: highest and lowest volume days, trend direction (growing/declining), average daily volume
3. Use get_global_stats to compare daily averages against all-time totals
4. Use get_top_traders with orderBy=collateralVolume to see the most active traders driving volume
5. Summarize key trends, anomalies, and what they suggest about platform health`,
        },
      },
    ],
  })
);

server.registerPrompt(
  "oi_analysis",
  {
    description: "Analyze Polymarket open interest — which markets have the most capital locked in and how OI is trending",
    argsSchema: {},
  },
  () => ({
    messages: [
      {
        role: "user" as const,
        content: {
          type: "text" as const,
          text: `Analyze Polymarket open interest. Follow these steps:
1. Use get_global_open_interest to get total platform OI and market count
2. Use get_market_open_interest with first=10 to find the top 10 markets by OI
3. For the top 2-3 markets, use get_oi_history with their conditionIds to see how OI has trended
4. Use get_market_data from the main subgraph to cross-reference conditionIds with market details (oracle, questionId, resolution status)
5. Summarize: total platform OI, top markets by capital locked, OI trends (growing/declining), and any notable patterns`,
        },
      },
    ],
  })
);

server.registerPrompt(
  "market_deep_dive",
  {
    description: "Deep dive into a specific Polymarket market — combining off-chain metadata with on-chain analytics and live CLOB data",
    argsSchema: {
      query: z.string().describe("Market search query or slug"),
    },
  },
  ({ query }) => ({
    messages: [
      {
        role: "user" as const,
        content: {
          type: "text" as const,
          text: `Do a deep dive on the Polymarket market matching "${query}". Follow these steps:
1. Use search_markets to find the market. If multiple results, pick the most relevant one
2. Use get_market_info with the slug to get full metadata (description, resolution source, outcomes)
3. Use get_clob_market with the conditionId to get CLOB token IDs and live prices
4. For each outcome token, use get_live_spread to check liquidity and get_price_history with interval=1w for trend
5. Use get_market_open_interest with the conditionId to see capital locked
6. Use get_oi_history to chart OI trend
7. Use get_market_resolution to check the UMA oracle status
8. Summarize: what the market is about, current prices, price trend, liquidity depth, OI, resolution status, and any notable patterns`,
        },
      },
    ],
  })
);

// ---------------------------------------------------------------------------
// Tools 22-23: builder attribution (CLOB V2 only)
//
// The V2 `OrderFilled` event carries a `builder` code identifying which frontend, bot or
// integrator routed the order. The V1 exchange contracts do not emit it, so these two questions
// are unanswerable on every other subgraph in this registry — this is new capability, not a
// migration of something that already existed.
// ---------------------------------------------------------------------------
server.registerTool(
  "get_builder_leaderboard",
  {
    description:
      "Rank Polymarket CLOB V2 builders by routed volume, order count or fees. A 'builder' is the " +
      "frontend/bot/integrator whose code is attached to a fill — this answers 'who is actually " +
      "routing the flow', which no V1 subgraph can, because the V1 contracts never emitted it. " +
      "V2-era only (from block 84902353, migration 2026-04-28).",
    inputSchema: {
      limit: z.number().int().min(1).max(100).optional().describe("How many builders to return (default 10)"),
      orderBy: z
        .enum(["scaledVolume", "orderCount", "scaledFees"])
        .optional()
        .describe("Ranking metric (default scaledVolume)"),
    },
  },
  async ({ limit, orderBy }) => {
    try {
      const n = limit ?? 10;
      const by = orderBy ?? "scaledVolume";
      const query = `{
        builders(first: ${n}, orderBy: ${by}, orderDirection: desc) {
          id
          orderCount
          volume
          scaledVolume
          fees
          scaledFees
          firstSeenTimestamp
          lastSeenTimestamp
        }
        globalStats_collection(first: 1) {
          buildersCount
          tradesQuantity
          scaledCollateralVolume
        }
      }`;
      const data = (await querySubgraph(SUBGRAPHS.v2_orderbook.ipfsHash, query)) as {
        builders?: Array<{ id: string; scaledVolume: string }>;
        globalStats_collection?: Array<{ buildersCount: string; scaledCollateralVolume: string }>;
      };
      const totals = data.globalStats_collection?.[0];
      // Share is computed here rather than left to the caller: the raw numbers invite comparing a
      // builder's volume against all-time platform volume, which is a V1 number and ~3x larger.
      const builders = (data.builders ?? []).map((b) => ({
        ...b,
        shareOfV2Volume: totals?.scaledCollateralVolume
          ? `${((Number(b.scaledVolume) / Number(totals.scaledCollateralVolume)) * 100).toFixed(2)}%`
          : null,
      }));
      return textResult({
        builders,
        v2Totals: totals ?? null,
        era: "CLOB V2 only — from block 84902353 (2026-04-28 migration). Shares are of V2-era volume, not all-time.",
      });
    } catch (error) {
      return errorResult(error);
    }
  }
);

server.registerTool(
  "get_v2_top_traders",
  {
    description:
      "Top real traders on Polymarket CLOB V2 by volume or trade count, with the exchange contracts " +
      "excluded. Use this rather than querying accounts directly: the V2 exchange is itself the " +
      "`taker` when an order matches the book, so it accumulates an Account row and outranks every " +
      "human by an order of magnitude. V2-era only (from block 84902353).",
    inputSchema: {
      limit: z.number().int().min(1).max(100).optional().describe("How many traders (default 10)"),
      orderBy: z
        .enum(["scaledCollateralVolume", "tradesQuantity"])
        .optional()
        .describe("Ranking metric (default scaledCollateralVolume)"),
    },
  },
  async ({ limit, orderBy }) => {
    try {
      const n = limit ?? 10;
      const by = orderBy ?? "scaledCollateralVolume";
      const cfg = SUBGRAPHS.v2_orderbook;
      const excluded = cfg.excludeAccounts ?? [];
      // Over-fetch by the number of excluded venues so the caller still gets `n` real traders back
      // after filtering, rather than n-2.
      const query = `{
        accounts(
          first: ${n + excluded.length}
          orderBy: ${by}
          orderDirection: desc
          where: { id_not_in: ${JSON.stringify(excluded)} }
        ) {
          id
          tradesQuantity
          buysQuantity
          sellsQuantity
          collateralVolume
          scaledCollateralVolume
          lastTradedTimestamp
        }
      }`;
      const data = (await querySubgraph(cfg.ipfsHash, query)) as {
        accounts?: Array<{ id: string }>;
      };
      const accounts = (data.accounts ?? []).slice(0, n);
      return textResult({
        traders: accounts,
        excludedVenues: excluded,
        note: "Exchange contracts filtered out — they appear as Accounts because the exchange is the taker on a book match. V2-era volume only, not all-time.",
      });
    } catch (error) {
      return errorResult(error);
    }
  }
);

server.registerTool(
  "get_builder_activity",
  {
    description:
      "Recent fills routed by one Polymarket CLOB V2 builder code, with that builder's aggregate " +
      "totals. Use get_builder_leaderboard first to find a builder id. V2-era only.",
    inputSchema: {
      builderId: z.string().describe("The builder code (bytes32 hex, as returned by get_builder_leaderboard)"),
      limit: z.number().int().min(1).max(100).optional().describe("How many recent fills (default 20)"),
    },
  },
  async ({ builderId, limit }) => {
    try {
      const n = limit ?? 20;
      const query = `{
        builder(id: ${JSON.stringify(builderId)}) {
          id
          orderCount
          scaledVolume
          scaledFees
          firstSeenTimestamp
          lastSeenTimestamp
        }
        orderFilledEvents(
          first: ${n}
          orderBy: timestamp
          orderDirection: desc
          where: { builder: ${JSON.stringify(builderId)} }
        ) {
          timestamp
          maker
          taker
          side
          tokenId
          price
          size
          fee
          market { id lastPrice }
        }
      }`;
      const data = (await querySubgraph(SUBGRAPHS.v2_orderbook.ipfsHash, query)) as {
        builder?: unknown;
      };
      if (!data.builder) {
        return textResult({
          builder: null,
          note: `No builder with id ${builderId} in the V2 orderbook subgraph. Builder ids are bytes32 hex — run get_builder_leaderboard to list real ones.`,
        });
      }
      return textResult(data);
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool 24: check_subgraph_freshness
// ---------------------------------------------------------------------------
server.registerTool(
  "check_subgraph_freshness",
  {
    description:
      "Report how far behind chainhead a subgraph is, by reading its _meta block. Worth calling " +
      "before trusting any 'current' or 'latest' number, because a lagging subgraph returns stale " +
      "data rather than an error — it succeeds, it is just answering about the past.",
    inputSchema: {
      subgraph: z.enum(SUBGRAPH_NAMES).describe("Which subgraph to check"),
    },
  },
  async ({ subgraph }) => {
    try {
      const cfg = SUBGRAPHS[subgraph];
      const data = (await querySubgraph(
        cfg.ipfsHash,
        `{ _meta { block { number timestamp } hasIndexingErrors deployment } }`
      )) as { _meta?: { block?: { number: number; timestamp: number }; hasIndexingErrors?: boolean } };
      const block = data._meta?.block;
      const ageSeconds = block?.timestamp ? Math.floor(Date.now() / 1000) - block.timestamp : null;
      const behindHuman =
        ageSeconds === null
          ? null
          : ageSeconds < 300
            ? "at chainhead"
            : ageSeconds < 86400
              ? `${Math.floor(ageSeconds / 3600)}h behind`
              : `${Math.floor(ageSeconds / 86400)} days behind`;
      return textResult({
        subgraph,
        name: cfg.name,
        era: cfg.era ?? "v1",
        headBlock: block?.number ?? null,
        headTimestamp: block?.timestamp ?? null,
        behind: behindHuman,
        hasIndexingErrors: data._meta?.hasIndexingErrors ?? null,
        // The static warning and the live measurement are both reported: the registry text can go
        // out of date, and the live number cannot.
        registryWarning: cfg.syncWarning ?? null,
        trustworthyForCurrentData: ageSeconds !== null && ageSeconds < 3600,
      });
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// HTTP/SSE Transport
// ---------------------------------------------------------------------------
function startHttpTransport(port: number) {
  const app = express();
  const sessions = new Map<string, SSEServerTransport>();

  app.get("/sse", async (req, res) => {
    const transport = new SSEServerTransport("/messages", res);
    sessions.set(transport.sessionId, transport);
    res.on("close", () => {
      sessions.delete(transport.sessionId);
    });
    await server.connect(transport);
  });

  app.post("/messages", async (req, res) => {
    const sessionId = req.query.sessionId as string;
    const transport = sessions.get(sessionId);
    if (!transport) {
      res.status(400).json({ error: "Invalid or expired session" });
      return;
    }
    await transport.handlePostMessage(req, res);
  });

  app.get("/health", (_req, res) => {
    res.json({ status: "ok", server: "graph-polymarket-mcp" });
  });

  app.listen(port, () => {
    console.error(`SSE transport listening on http://localhost:${port}/sse`);
  });
}

// ---------------------------------------------------------------------------
// Start server
// ---------------------------------------------------------------------------
async function main() {
  const httpPort = process.env.MCP_HTTP_PORT || (process.argv.includes("--http") ? "3851" : null);
  const httpOnly = process.argv.includes("--http-only");

  if (httpPort || httpOnly) {
    const port = parseInt(httpPort || "3851", 10);
    startHttpTransport(port);
  }

  if (!httpOnly) {
    const transport = new StdioServerTransport();
    await server.connect(transport);
  }

  console.error("Graph Polymarket MCP server running");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});

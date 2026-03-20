export interface SubgraphConfig {
  name: string;
  ipfsHash: string;
  description: string;
  keyEntities: string[];
}

export const SUBGRAPHS: Record<string, SubgraphConfig> = {
  main: {
    name: "Main",
    ipfsHash: "QmdyCguLEisTtQFveEkvMhTH7UzjyhnrF9kpvhYeG4QX8a",
    description:
      "Core Polymarket subgraph with markets, conditions, and trader counts. Best for: market discovery, condition resolution status, and counting open/closed markets. NOTE: volume/fee fields in Global are zeroed out — use the orderbook subgraph for accurate volume data.",
    keyEntities: [
      "Global (numConditions, numOpenConditions, numClosedConditions, numTraders)",
      "Condition (oracle, questionId, outcomeSlotCount, resolutionTimestamp, payoutNumerators)",
      "Account",
      "MarketData",
      "Transaction",
    ],
  },
  beefy_pnl: {
    name: "Beefy Profit and Loss",
    ipfsHash: "QmbHwcGkumWdyTK2jYWXV3vX4WyinftEGbuwi7hDkhPWqG",
    description:
      "The most comprehensive Polymarket analytics subgraph. UNIQUE FEATURES not available elsewhere: (1) Hedge fund-grade account metrics — winRate, profitFactor, maxDrawdown computed on-chain per trader. (2) Per-position P&L with realizedPnl, unrealizedPnl, cost basis (valueBought/valueSold). (3) Daily time-series — query as dailyStats_collection (NOT dailyStats) for daily volume, fees, numTraders, numNewMarkets, numResolvedMarkets. (4) Market-level analytics — currentPrice, numBuyers, numSellers. Best for: trader performance analysis, portfolio analytics, P&L tracking, and historical trend data.",
    keyEntities: [
      "Account (winRate, profitFactor, maxDrawdown, numWinning/LosingPositions)",
      "MarketPosition (realizedPnl, unrealizedPnl, valueBought, valueSold)",
      "dailyStats_collection (date, volume, fees, numTraders, numNewMarkets, numResolvedMarkets) — use _collection suffix for list queries",
      "Market (currentPrice, numBuyers, numSellers)",
      "MarketProfit",
      "Transaction",
      "TokenPosition",
      "UserStats",
    ],
  },
  slimmed_pnl: {
    name: "Slimmed P&L",
    ipfsHash: "QmZAYiMeZiWC7ZjdWepek7hy1jbcW3ngimBF9ibTiTtwQU",
    description:
      "Lightweight position tracker. Stores user token holdings with amount, avgPrice, realizedPnl, and totalBought. Best for: quick position lookups when you just need current holdings without full analytics. NOTE: indexers on this subgraph can lag; if queries fail with 'too far behind' errors, use the beefy_pnl subgraph instead.",
    keyEntities: ["UserPosition (amount, avgPrice, realizedPnl, totalBought)", "NegRiskEvent", "Condition", "FPMM"],
  },
  activity: {
    name: "Activity",
    ipfsHash: "Qmf3qPUsfQ8et6E3QNBmuXXKqUJi91mo5zbsaTkQrSnMAP",
    description:
      "Event log for position management operations. Tracks splits (minting outcome tokens), merges (combining tokens back to collateral), and redemptions (claiming payouts from resolved markets). Best for: monitoring position lifecycle events, tracking when users enter/exit markets, and auditing collateral flows.",
    keyEntities: [
      "Split (stakeholder, condition, amount, timestamp)",
      "Merge (stakeholder, condition, amount, timestamp)",
      "Redemption (redeemer, condition, payout, indexSets)",
      "NegRiskConversion",
      "NegRiskEvent",
    ],
  },
  orderbook: {
    name: "Orderbook",
    ipfsHash: "QmVGA9vvNZtEquVzDpw8wnTFDxVjB6mavTRMTrKuUBhi4t",
    description:
      "Detailed orderbook trading data and authoritative platform-wide volume. Every order fill with maker/taker, price, side, fee, and asset IDs. IMPORTANT: Use ordersMatchedGlobals for accurate total volume ($72B+), trade counts, and fees — the main subgraph Global entity has zeroed volume fields. Best for: analyzing trading patterns, tracking specific maker/taker activity, order flow analysis, per-market trade statistics, and platform volume metrics.",
    keyEntities: [
      "OrderFilledEvent (maker, taker, price, side, fee, amounts)",
      "OrdersMatchedEvent",
      "Orderbook (per-token trade stats)",
      "Global (platform-wide trade counts)",
      "Account (per-trader volume and activity)",
    ],
  },
  open_interest: {
    name: "Open Interest",
    ipfsHash: "QmbT2MmS2VGbGihiTUmWk6GMc2QYqoT9ZhiupUicYMWt6H",
    description:
      "The only Polymarket subgraph dedicated to open interest. Tracks USDC currently locked in outstanding YES/NO positions per market, with hourly snapshots for time-series analysis. OI is computed from PositionSplit (increases) and PositionsMerge (decreases) events on the ConditionalTokens contract. IMPORTANT: Polymarket does NOT use on-chain PayoutRedemption — winners sell shares on the orderbook or merge positions instead. This means resolved markets will still show residual OI from losing-side tokens that will never be redeemed. High OI on a resolved market = dead money (worthless losing tokens), not unclaimed winnings. Best for: identifying markets with the most capital at risk, charting OI trends over time, and detecting capital flow shifts across markets.",
    keyEntities: [
      "MarketOpenInterest (amount in USDC, splitCount, mergeCount — cross-reference with main subgraph for resolution status)",
      "OISnapshot (hourly bucketed OI per market — amount, timestamp, blockNumber)",
      "GlobalOpenInterest (total OI across all markets, marketCount)",
    ],
  },
  resolution: {
    name: "Market Resolution",
    ipfsHash: "QmZnnrHWCB1Mb8dxxXDxfComjNdaGyRC66W8derjn3XDPg",
    description:
      "Tracks the full UMA oracle resolution lifecycle for every Polymarket question. Each MarketResolution entity captures the current status (initialized → proposed → resolved), whether it was disputed, proposed/reproposed prices, and moderator flags. Revision entities log moderator updates with timestamps. Best for: monitoring market resolution progress, detecting disputed outcomes, auditing oracle activity, and checking if a market was flagged or paused.",
    keyEntities: [
      "MarketResolution (questionId, status, proposedPrice, price, flagged, paused, wasDisputed)",
      "Revision (moderator, questionId, timestamp, update)",
      "Moderator (address, canMod)",
      "AncillaryDataHashToQuestionId (maps ancillary data to questionId)",
    ],
  },
  traders: {
    name: "Traders",
    ipfsHash: "QmfT4YQwFfAi77hrC2JH3JiPF7C4nEn27UQRGNpSpUupqn",
    description:
      "Per-trader event log indexing every CTF interaction and USDC flow. Each Trader has a derived list of CTFEvents (splits, merges, transfers, resolutions, redemptions) and USDCTransfers (inbound/outbound with amounts). Best for: building trader profiles, tracking when a wallet first appeared, reconstructing a trader's full on-chain history, and analyzing USDC deposit/withdrawal patterns.",
    keyEntities: [
      "Trader (address, firstSeenBlock, firstSeenTimestamp)",
      "CTFEvent (eventType, conditionId, amounts, timestamp) — immutable, @derivedFrom trader",
      "USDCTransfer (from, to, amount, isInbound, timestamp) — immutable, @derivedFrom trader",
    ],
  },
};

export const SUBGRAPH_NAMES = Object.keys(SUBGRAPHS) as [string, ...string[]];

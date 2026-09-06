export interface SubgraphConfig {
  name: string;
  ipfsHash: string;
  description: string;
  keyEntities: string[];
  /**
   * Which Polymarket CLOB era this subgraph indexes.
   *
   * Polymarket migrated to V2 exchange contracts on 2026-04-28. The V2 subgraphs start at block
   * 84902353 and therefore hold **no pre-migration history at all** — they are not newer versions
   * of the V1 subgraphs, they are a different window on a different pair of contracts. Anything
   * asking "all time" still belongs on V1.
   */
  era?: "v1" | "v2";
  /**
   * Set when a subgraph is materially behind chainhead, with the measurement date. Present here
   * rather than only in prose because this object is what an LLM reads when it picks a subgraph,
   * and a silently-stale answer is worse than a refusal.
   */
  syncWarning?: string;
  /**
   * Addresses that appear as Accounts but are infrastructure, not traders. Ranking accounts without
   * excluding these puts the venue at the top of every "biggest trader" list.
   */
  excludeAccounts?: string[];
  /**
   * Set when a subgraph is not currently answerable on the network. Distinct from `syncWarning`:
   * a stale subgraph answers with old data, an unavailable one answers not at all. Both belong in
   * the registry so a model can route around them instead of retrying into a wall.
   */
  availability?: string;
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
    availability:
      "NOT SERVED as of 2026-08-08 — no indexer is allocated to this deployment, so every query fails with 'subgraph not found'. The subgraph record still exists (4LkKSgkqijUccYMYMYUPtjXswrdK3xipPMfs3fa7gfef) but is unqueryable by deployment OR subgraph id. Tools depending on it (get_account_pnl, get_top_traders, get_daily_stats, get_market_positions) will error until it is re-deployed or signalled.",
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
    // Already the V2 deployment — this one migrated before the rest and is live at chainhead.
    // It reads ConditionalTokens, which V2 left unchanged, so it has no migration discontinuity.
    era: "v2",
    description:
      "The only Polymarket subgraph dedicated to open interest. Tracks USDC currently locked in outstanding YES/NO positions per market, with hourly snapshots for time-series analysis. OI is computed from PositionSplit (increases) and PositionsMerge (decreases) events on the ConditionalTokens contract. IMPORTANT: Polymarket does NOT use on-chain PayoutRedemption — winners sell shares on the orderbook or merge positions instead. This means resolved markets will still show residual OI from losing-side tokens that will never be redeemed. High OI on a resolved market = dead money (worthless losing tokens), not unclaimed winnings. Best for: identifying markets with the most capital at risk, charting OI trends over time, and detecting capital flow shifts across markets.",
    keyEntities: [
      "MarketOpenInterest (amount in USDC, splitCount, mergeCount — cross-reference with main subgraph for resolution status)",
      "OISnapshot (hourly bucketed OI per market — amount, timestamp, blockNumber)",
      "GlobalOpenInterest (total OI across all markets, marketCount)",
    ],
  },
  resolution: {
    availability:
      "DEGRADED as of 2026-08-08 — indexers are allocated but the gateway reports 'bad indexers' (BadResponse). May be transient; retry before assuming it is gone.",
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
    availability:
      "NOT SERVED as of 2026-08-08 — no indexer is allocated; queries fail with 'subgraph not found'.",
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

  // ── Polymarket CLOB V2 (migration 2026-04-28) ───────────────────────────────────────────────
  //
  // Added, not substituted. V2 indexes the new CTF Exchange contracts from block 84902353, so it
  // holds no pre-migration history — a question about all-time volume or a 2025 market still has to
  // go to the V1 entries above. Choosing between them is an era question, not a freshness one.

  v2_orderbook: {
    name: "V2 Orderbook (CLOB V2)",
    ipfsHash: "QmNtJGxpAjFgoHhMwdijyvbLrpPPiHHX2qct56nTpk42Bs",
    era: "v2",
    description:
      "Order fills on the Polymarket CLOB **V2** exchange contracts (migration 2026-04-28), indexed from block 84902353. Live at chainhead. UNIQUE TO V2 — **builder-code attribution**: every fill carries the `builder` code that routed it, and Builder entities aggregate order count, volume and fees per builder. Nothing in the V1 subgraphs can answer 'which frontend/bot routed this flow', because the V1 contracts do not emit it. Best for: builder/routing analysis, and post-migration trading activity. NOT for all-time totals — it starts at the migration, so its volume is V2-era only ($24B, versus $72B+ all-time on the V1 `orderbook` subgraph). Note the field names differ from V1: `GlobalStats` (not `Global`), queried as `globalStats_collection`, and volume is `collateralVolume` / `scaledCollateralVolume` (not `totalVolume`). ⚠️ TRAP — the two V2 exchange contracts appear as Account rows, because the exchange is the `taker` when an order matches the book. Ranking accounts by volume or trade count returns `0xe111…996b` (CTF Exchange V2, 176M fills) and `0xe222…0f59` (Neg Risk V2, 41M fills) at the top, an order of magnitude above any real trader. Exclude both — they are listed in this entry's `excludeAccounts`.",
    keyEntities: [
      "GlobalStats (tradesQuantity, collateralVolume, scaledCollateralVolume, collateralFees, tradersCount, marketsCount, buildersCount) — query as globalStats_collection",
      "Builder (id = builder code, orderCount, volume, scaledVolume, fees, scaledFees, firstSeenTimestamp, lastSeenTimestamp) — V2 ONLY",
      "OrderFilledEvent (maker, taker, side, tokenId, price, size, fee, builder, metadata, exchange)",
      "Account (tradesQuantity, collateralVolume, scaledCollateralVolume, lastTradedTimestamp) — SEE THE EXCHANGE-ACCOUNT WARNING",
      "Market (tokenId, tradesQuantity, collateralVolume, lastPrice, lastActiveTimestamp)",
    ],
    /**
     * Addresses that are venues, not traders. When an order matches against the book the exchange
     * contract is itself the `taker`, so it accumulates an Account row — and ranking accounts by
     * volume or trade count puts these two on top by an order of magnitude (176M and 41M fills,
     * versus ~10M for the largest real trader). Verified against the live subgraph 2026-08-08.
     */
    excludeAccounts: [
      "0xe111180000d2663c0091e4f400237545b87b996b", // CTF Exchange V2
      "0xe2222d279d744050d28e00520010520000310f59", // Neg Risk CTF Exchange V2
    ],
  },

  v2_pnl: {
    name: "V2 P&L (CLOB V2)",
    ipfsHash: "QmT21E4p8r6FCzW2EPK4NVj1dbcggdvKxZr8uuMcB4P5Cu",
    era: "v2",
    description:
      "Per-trader cost basis and realized P&L computed from **V2** exchange fills only, from block 84902353. Live at chainhead. Deliberately lean — three entities, fills-only. It does NOT carry the hedge-fund metrics the V1 `beefy_pnl` subgraph has (winRate, profitFactor, maxDrawdown, unrealizedPnl) or its daily time-series, so for trader-quality scoring stay on `beefy_pnl`. Use this when you specifically want P&L attributable to V2-era trading, uncontaminated by pre-migration history.",
    keyEntities: [
      "Account (per-trader aggregate: collateralVolume, tradesQuantity)",
      "UserPosition (id = `{address}-{tokenId}`, amount, avgPrice, realizedPnl, totalBought)",
      "Market (per-outcome-token volume and last price)",
    ],
  },

  v2_main: {
    name: "V2 Main (CLOB V2) — SYNCING",
    ipfsHash: "QmTKrqyYg23BjhihmsrRjbV9cVS2piNmnHsr7cjYaTgdWu",
    era: "v2",
    syncWarning:
      "BEHIND CHAINHEAD. Measured 2026-08-08: head block 86.84M against a Polygon chainhead of 91.67M — roughly three months of lag, closing at about 4 blocks/sec. Do not use it for anything current.",
    description:
      "Conditions, resolution status and global counters for CLOB **V2**. ⚠️ STILL SYNCING — as of 2026-08-08 its head is ~4.8M blocks (about three months) behind chainhead and catching up slowly. It answers structural questions about conditions that existed before its head block, but **any question about recent markets, current counts, or 'latest' anything will be silently wrong** — it will return data, just old data. Until it catches up, use the V1 `main` subgraph for market discovery and resolution status. Kept in the registry so it can be queried deliberately, not so it can be picked by default.",
    keyEntities: [
      "Global (numConditions, numOpenConditions, numClosedConditions, numTraders) — as of the head block, NOT current",
      "Condition (oracle, questionId, outcomeSlotCount, resolutionTimestamp, payoutNumerators)",
      "Account, MarketData, MarketPosition, MarketProfit, Transaction",
      "Split / Merge / Redemption",
      "Builder, Orderbook, EnrichedOrderFilled",
    ],
  },
};

/** Subgraphs that are materially behind chainhead, so a caller can warn or route around them. */
export function isStale(key: string): boolean {
  return Boolean(SUBGRAPHS[key]?.syncWarning);
}

export const SUBGRAPH_NAMES = Object.keys(SUBGRAPHS) as [string, ...string[]];

/**
 * @realized-lp/core — public entry point.
 *
 * The whole point of this package: advertised LP APR is fee income annualized. It has no
 * price term, so it is positive by construction and cannot show you a loss. Realized return
 * is fees PLUS impermanent loss (IL <= 0 always). This package computes the second number.
 *
 * Three levels of use, smallest first:
 *
 *   1. Pure math, no network, no API key:
 *        import { impermanentLossPct, concentratedIlPct } from '@realized-lp/core';
 *        impermanentLossPct(2)          // full-range IL at a 2x price move
 *        concentratedIlPct(2, 2)        // same move, position ranged +/-2x
 *
 *   2. One position, live from The Graph:
 *        import { gatewayUrl, fetchPoolFrom, positionRealized } from '@realized-lp/core';
 *        const url  = gatewayUrl(process.env.GRAPH_API_KEY);
 *        const pool = await fetchPoolFrom(url, poolId, entryUnixSeconds);
 *        positionRealized(pool, 2);     // { realizedReturnPct, impermanentLossPct, ... }
 *
 *   3. Corpus-wide audit:
 *        import { fetchTopPools, scorePool, summarize } from '@realized-lp/core';
 *
 * Why The Graph is load-bearing and not decoration: per-day fee totals in USD are derived
 * aggregates produced by the indexer. Reconstructing them from RPC is possible but not
 * practical at corpus scale -- see the note in realized.js. The short version: there is no cheap RPC path to
 * this dataset -- you would have to replay every swap and price it yourself.
 */

// -- Pure math (no network, no key) -------------------------------------------------------
export { impermanentLossPct, positionRealized, byRange, scorePool } from './realized.js';
export { positionValue, hodlValue, concentratedIlPct, outOfRange, RANGES } from './concentrated.js';

// -- The Graph access ---------------------------------------------------------------------
export { gatewayUrl, query, fetchPool, fetchPoolFrom, fetchTopPools } from './realized.js';

// -- Corpus / aggregate analysis ----------------------------------------------------------
export {
  STABLES,
  DEFAULT_LIVENESS,
  pearson,
  spearman,
  priceCollapsed,
  isLive,
  median,
  summarize,
  sensitivity,
} from './realized.js';

// -- Multi-venue (Uniswap v3, Aerodrome, ... across chains) -------------------------------
export { VENUES, subgraphId, venueList } from './venues.js';

// -- Walk-forward / out-of-sample windows -------------------------------------------------
export { scoreWindow, summarizeWindow } from './walkforward.js';

// -- Wallet positions (read an address's real tick ranges) ---------------------------------
// Deliberately does NOT export a per-position fee/P&L number: collectedFees* is a withdrawal
// record, not an earnings record, and deposited* is lifetime cumulative rather than entry
// state. See wallet.js header + WALLET-CONNECT-NOTES.md for the measurements.
export { tickToPrice, tickRangeToWidth, fetchWalletPositions, describePosition, WALLET_LIMITS } from './wallet.js';

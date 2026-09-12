/**
 * venues.js — the one place subgraph IDs live.
 *
 * These were duplicated between scripts/build-pools.js and the API server. Two copies of a
 * source-of-truth map is exactly the drift this repo keeps catching elsewhere: one gets a new
 * chain, the other doesn't, and the corpus silently stops matching what the live API returns.
 */

export const VENUES = {
  'uniswap-v3': {
    mainnet: '5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV',
    arbitrum: 'FbCGRftH4a3yZugY7TnbYgPJVEv2LvMT6oF1fxPe9aJM',
    polygon: '3hCPRGf4z88VC5rsBKU5AA9FBBq5nF3jbKJG7VZCbhjm',
    base: '43Hwfi3dJSoGpyas9VwNoDAv55yjgGrPpNSmbQZArzMG',
  },
  // v4 mainnet only, on purpose. Verified live 2026-09-11 against this subgraph; the other
  // chains are NOT here because each is a separate subgraph id that needs its own probe, and
  // an unverified id in this map is indistinguishable from a verified one at the call site.
  // Adding Arbitrum/Base/Polygon v4 = add the id AND prove it answers, in the same change.
  'uniswap-v4': {
    mainnet: 'DiYPVdygkfjDWhbxGSqAQxwBKmfKnkWQojqeM2rkLb3G',
  },
  aerodrome: {
    base: 'GENunSHWLBXm59mBSgPzQ8metBEp9YDfdqwFr91Av1UM',
  },
};

/**
 * Which venues support which questions.
 *
 * v3 stores position STATE on-chain (tickLower/tickUpper/liquidity on the NFT), so a range is a
 * lookup and realized return is computable. v4 exposes only EVENTS -- the Position entity has no
 * range -- so a range is RECONSTRUCTED by replaying ModifyLiquidity, which is a strictly weaker
 * evidence class. Reconstructed liquidity inherits gaps that a state read never has (a position
 * transferred in has removes with no adds in this wallet's history), so we do not price exits on
 * it. This map is what stops a caller from assuming every venue answers every question.
 */
export const CAPABILITIES = {
  'uniswap-v3': {
    source: 'position-state',
    poolAnalytics: true,
    walletLookup: true,
    realRange: true,
    realizedReturn: true,
    exitSimulation: true,
  },
  'uniswap-v4': {
    source: 'event-reconstruction',
    poolAnalytics: true,
    walletLookup: true,
    realRange: true,
    realizedReturn: false,
    exitSimulation: false,
    why: 'The v4 Position entity carries no tick range; ranges are reconstructed from ModifyLiquidity events. Reconstructed liquidity cannot support exit pricing.',
  },
  // Aerodrome is POOL-LEVEL ONLY. Its pool analytics are real (it ships in the pool table with
  // live TVL and verdicts), but its subgraph exposes no per-owner Position entity, so
  // /api/wallet returns an explicit error for it.
  //
  // CORRECTED 2026-09-11: this entry previously claimed realizedReturn/exitSimulation/realRange
  // true with no walletLookup field at all, which read as "wallet lookup works here" while the
  // code refused it. The capability map and the endpoint contradicted each other and the map was
  // the one lying. Verified by calling ?dex=aerodrome for two addresses: both error.
  aerodrome: {
    source: 'pool-only',
    poolAnalytics: true,
    walletLookup: false,
    realRange: false,
    realizedReturn: false,
    exitSimulation: false,
    why: 'Aerodrome pool analytics are supported, but its subgraph exposes no per-owner Position entity, so wallet-level position lookup is not available.',
  },
};

/** What a given dex can and cannot answer. Unknown dex returns null, not a guess. */
export function capabilities(dex = 'uniswap-v3') {
  return CAPABILITIES[dex] ?? null;
}

/** Resolve dex+chain to a subgraph id, or null when we do not index that pair. */
export function subgraphId(dex = 'uniswap-v3', chain = 'mainnet') {
  return VENUES[dex]?.[chain] ?? null;
}

/** Flat list for discovery endpoints. */
export function venueList() {
  return Object.entries(VENUES).flatMap(([dex, chains]) =>
    Object.keys(chains).map((chain) => ({ dex, chain, ...(CAPABILITIES[dex] ?? {}) })));
}

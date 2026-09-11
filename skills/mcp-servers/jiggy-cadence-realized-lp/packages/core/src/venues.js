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
  aerodrome: {
    base: 'GENunSHWLBXm59mBSgPzQ8metBEp9YDfdqwFr91Av1UM',
  },
};

/** Resolve dex+chain to a subgraph id, or null when we do not index that pair. */
export function subgraphId(dex = 'uniswap-v3', chain = 'mainnet') {
  return VENUES[dex]?.[chain] ?? null;
}

/** Flat list for discovery endpoints. */
export function venueList() {
  return Object.entries(VENUES).flatMap(([dex, chains]) =>
    Object.keys(chains).map((chain) => ({ dex, chain })));
}

import { DEFILLAMA_PRICE_URL, DEFILLAMA_TIMEOUT_MS, PRICE_BATCH_SIZE, PRICE_BATCH_CONCURRENCY, PRICE_CACHE_TTL_MS, PRICE_FAILURE_CACHE_TTL_MS } from "./constants.js";
import { mapWithConcurrency } from "./util.js";

type DefiLlamaResponse = {
  coins: Record<string, { price: number; decimals: number; symbol: string }>;
};

export interface TokenPrice {
  price: number;
  decimals: number;
}

interface CachedPrice extends TokenPrice {
  cachedAt: number;
  /**
   * True for the $0 written when a token came back unpriced or its batch failed
   * outright. Kept because the two expire on very different clocks — see
   * PRICE_FAILURE_CACHE_TTL_MS — and because a $0 price is otherwise
   * indistinguishable from a real one that happens to be zero.
   */
  isFallback: boolean;
}

const cache = new Map<string, CachedPrice>();

function isFresh(entry: CachedPrice | undefined): entry is CachedPrice {
  if (entry === undefined) return false;
  const ttl = entry.isFallback ? PRICE_FAILURE_CACHE_TTL_MS : PRICE_CACHE_TTL_MS;
  return Date.now() - entry.cachedAt < ttl;
}

/**
 * Looks up current USD price + decimals for a batch of Base token addresses via
 * DefiLlama's free, keyless price API. Missing/unpriced tokens (obscure or very
 * new bribe tokens are common) get price 0 rather than throwing, so one unpriced
 * token doesn't blow up a whole pool's calculation — it just contributes $0.
 * That $0 is cached far more briefly than a real price, so a token that failed
 * to price once isn't stuck at zero for the rest of a long-lived process.
 *
 * Requests are chunked into batches of `PRICE_BATCH_SIZE` tokens rather than one
 * request for the whole (potentially hundreds-long) token list, so a single
 * oversized/failed request only zeroes out prices for its own batch instead of
 * every token in the run. Batches are fetched with bounded concurrency rather
 * than one after another — a run touching a few hundred tokens can produce
 * several batches, and awaiting them sequentially means a slow or timed-out
 * batch (up to `DEFILLAMA_TIMEOUT_MS` each) adds its full delay to every batch
 * behind it instead of overlapping.
 */
export async function getTokenPrices(
  tokenAddresses: string[],
): Promise<Map<string, TokenPrice>> {
  const unique = [...new Set(tokenAddresses.map((a) => a.toLowerCase()))];
  const uncached = unique.filter((a) => !isFresh(cache.get(a)));

  const batches: string[][] = [];
  for (let i = 0; i < uncached.length; i += PRICE_BATCH_SIZE) {
    batches.push(uncached.slice(i, i + PRICE_BATCH_SIZE));
  }

  await mapWithConcurrency(batches, PRICE_BATCH_CONCURRENCY, async (batch) => {
    const keys = batch.map((a) => `base:${a}`).join(",");
    try {
      const res = await fetch(`${DEFILLAMA_PRICE_URL}/${keys}`, { signal: AbortSignal.timeout(DEFILLAMA_TIMEOUT_MS) });
      if (res.ok) {
        const data = (await res.json()) as DefiLlamaResponse;
        for (const [key, coin] of Object.entries(data.coins)) {
          const address = key.split(":")[1]?.toLowerCase();
          if (address) cache.set(address, { price: coin.price, decimals: coin.decimals, cachedAt: Date.now(), isFallback: false });
        }
      }
    } catch {
      // Network-level failure (DNS, timeout, connection refused) — fall through to
      // the same $0 fallback used for an HTTP error response, per this function's
      // contract: one pricing outage shouldn't blow up a whole pool's calculation
      // (and, since this is per-batch, doesn't take down other batches' pricing).
    }
    for (const a of batch) {
      if (!isFresh(cache.get(a))) cache.set(a, { price: 0, decimals: 18, cachedAt: Date.now(), isFallback: true });
    }
  });

  const result = new Map<string, TokenPrice>();
  for (const a of unique) {
    const entry = cache.get(a);
    result.set(a, entry ? { price: entry.price, decimals: entry.decimals } : { price: 0, decimals: 18 });
  }
  return result;
}

/**
 * How many of the looked-up tokens ended up with no usable price.
 *
 * An unpriced token silently contributes $0 to every epoch it appears in, which
 * is the right behaviour — one obscure bribe token shouldn't blow up a pool's
 * whole calculation — but it is not a fact worth hiding. A pool incentivised
 * entirely in something DefiLlama doesn't cover reads as $0, falls under
 * MIN_TRAILING_USD, and vanishes from the ranking with nothing said. Callers
 * report this the same way they already report skipped pools and failed epoch
 * fetches, so a thin-looking scan can be recognised as a pricing gap rather
 * than a quiet market.
 */
export function countUnpricedTokens(prices: Map<string, TokenPrice>): number {
  let unpriced = 0;
  for (const { price } of prices.values()) if (price === 0) unpriced++;
  return unpriced;
}

/** Converts a raw on-chain token amount to a USD value using a looked-up price/decimals map. */
export function toUsd(amount: bigint, token: string, prices: Map<string, TokenPrice>): number {
  const info = prices.get(token.toLowerCase());
  if (!info || info.price === 0) return 0;
  return (Number(amount) / 10 ** info.decimals) * info.price;
}

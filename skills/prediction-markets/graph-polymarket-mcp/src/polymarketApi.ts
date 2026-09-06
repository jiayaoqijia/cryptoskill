// Polymarket REST API clients (Gamma + CLOB)
// Gamma API: market discovery, events, tags
// CLOB API: real-time prices, order books, spreads, price history

const GAMMA_BASE = "https://gamma-api.polymarket.com";
const CLOB_BASE = "https://clob.polymarket.com";

export class PolymarketApiError extends Error {
  constructor(
    message: string,
    public readonly statusCode?: number,
    public readonly endpoint?: string
  ) {
    super(message);
    this.name = "PolymarketApiError";
  }
}

async function fetchJson<T>(url: string): Promise<T> {
  const response = await fetch(url, {
    headers: { Accept: "application/json" },
  });
  if (!response.ok) {
    throw new PolymarketApiError(
      `HTTP ${response.status}: ${response.statusText}`,
      response.status,
      url
    );
  }
  return response.json() as Promise<T>;
}

// ---------------------------------------------------------------------------
// Gamma API — Market Discovery
// ---------------------------------------------------------------------------

export interface GammaMarket {
  id: string;
  question: string;
  conditionId: string;
  slug: string;
  resolutionSource: string;
  endDate: string;
  liquidity: string;
  volume: string;
  active: boolean;
  closed: boolean;
  marketMakerAddress: string;
  outcomePrices: string;
  outcomes: string;
  clobTokenIds: string;
  bestBid: string;
  bestAsk: string;
  lastTradePrice: string;
  spread: string;
  description: string;
  [key: string]: unknown;
}

export interface GammaEvent {
  id: string;
  slug: string;
  title: string;
  description: string;
  startDate: string;
  endDate: string;
  markets: GammaMarket[];
  [key: string]: unknown;
}

export async function searchMarkets(
  query: string,
  opts: { limit?: number; active?: boolean; closed?: boolean; orderBy?: string; ascending?: boolean } = {}
): Promise<GammaMarket[]> {
  const params = new URLSearchParams();
  params.set("_limit", String(opts.limit ?? 10));
  if (query) params.set("_q", query);
  if (opts.active !== undefined) params.set("active", String(opts.active));
  if (opts.closed !== undefined) params.set("closed", String(opts.closed));
  if (opts.orderBy) {
    params.set("_sort", opts.orderBy);
    params.set("_order", opts.ascending ? "asc" : "desc");
  }
  return fetchJson<GammaMarket[]>(`${GAMMA_BASE}/markets?${params}`);
}

export async function getMarketBySlug(slug: string): Promise<GammaMarket[]> {
  return fetchJson<GammaMarket[]>(`${GAMMA_BASE}/markets?slug=${encodeURIComponent(slug)}`);
}

export async function getMarketByConditionId(conditionId: string): Promise<GammaMarket[]> {
  return fetchJson<GammaMarket[]>(
    `${GAMMA_BASE}/markets?conditionId=${encodeURIComponent(conditionId)}`
  );
}

export async function listEvents(
  opts: { limit?: number; active?: boolean; closed?: boolean; slug?: string; tag?: string; orderBy?: string; ascending?: boolean } = {}
): Promise<GammaEvent[]> {
  const params = new URLSearchParams();
  params.set("_limit", String(opts.limit ?? 10));
  if (opts.active !== undefined) params.set("active", String(opts.active));
  if (opts.closed !== undefined) params.set("closed", String(opts.closed));
  if (opts.slug) params.set("slug", opts.slug);
  if (opts.tag) params.set("tag", opts.tag);
  if (opts.orderBy) {
    params.set("_sort", opts.orderBy);
    params.set("_order", opts.ascending ? "asc" : "desc");
  }
  return fetchJson<GammaEvent[]>(`${GAMMA_BASE}/events?${params}`);
}

export async function getEvent(eventId: string): Promise<GammaEvent> {
  return fetchJson<GammaEvent>(`${GAMMA_BASE}/events/${encodeURIComponent(eventId)}`);
}

// ---------------------------------------------------------------------------
// CLOB API — Real-Time Prices & Order Books
// ---------------------------------------------------------------------------

export interface ClobPrice {
  price: string;
  size: string;
}

export interface ClobOrderBook {
  market: string;
  asset_id: string;
  bids: ClobPrice[];
  asks: ClobPrice[];
  hash: string;
  timestamp: string;
}

export interface ClobMarket {
  condition_id: string;
  question_id: string;
  tokens: Array<{
    token_id: string;
    outcome: string;
    price: number;
    winner: boolean;
  }>;
  minimum_order_size: string;
  minimum_tick_size: string;
  description: string;
  market_slug: string;
  end_date_iso: string;
  active: boolean;
  closed: boolean;
  accepting_orders: boolean;
  accepting_order_timestamp: string;
  [key: string]: unknown;
}

export async function getClobPrice(
  tokenId: string,
  side: "buy" | "sell" = "buy"
): Promise<{ price: string }> {
  return fetchJson<{ price: string }>(
    `${CLOB_BASE}/price?token_id=${encodeURIComponent(tokenId)}&side=${side}`
  );
}

export async function getClobPricesBatch(
  tokenIds: string[],
  side: "buy" | "sell" = "buy"
): Promise<unknown> {
  const params = tokenIds.map((id) => `token_ids=${encodeURIComponent(id)}`).join("&");
  return fetchJson<unknown>(`${CLOB_BASE}/prices?${params}&side=${side}`);
}

export async function getClobMidpoint(tokenId: string): Promise<{ mid: string }> {
  return fetchJson<{ mid: string }>(
    `${CLOB_BASE}/midpoint?token_id=${encodeURIComponent(tokenId)}`
  );
}

export async function getClobSpread(
  tokenId: string
): Promise<{ spread: string; bid: string; ask: string }> {
  return fetchJson<{ spread: string; bid: string; ask: string }>(
    `${CLOB_BASE}/spread?token_id=${encodeURIComponent(tokenId)}`
  );
}

export async function getClobOrderBook(tokenId: string): Promise<ClobOrderBook> {
  return fetchJson<ClobOrderBook>(
    `${CLOB_BASE}/book?token_id=${encodeURIComponent(tokenId)}`
  );
}

export async function getClobLastTradePrice(
  tokenId: string
): Promise<{ price: string }> {
  return fetchJson<{ price: string }>(
    `${CLOB_BASE}/last-trade-price?token_id=${encodeURIComponent(tokenId)}`
  );
}

export async function getClobPriceHistory(
  tokenId: string,
  interval: string = "1d",
  fidelity: number = 60
): Promise<{ history: Array<{ t: number; p: number }> }> {
  return fetchJson<{ history: Array<{ t: number; p: number }> }>(
    `${CLOB_BASE}/prices-history?market=${encodeURIComponent(tokenId)}&interval=${interval}&fidelity=${fidelity}`
  );
}

export async function getClobMarket(conditionId: string): Promise<ClobMarket> {
  return fetchJson<ClobMarket>(
    `${CLOB_BASE}/markets/${encodeURIComponent(conditionId)}`
  );
}

export async function getClobMarkets(nextCursor?: string): Promise<{
  data: ClobMarket[];
  next_cursor: string;
}> {
  const params = nextCursor ? `?next_cursor=${encodeURIComponent(nextCursor)}` : "";
  return fetchJson<{ data: ClobMarket[]; next_cursor: string }>(
    `${CLOB_BASE}/markets${params}`
  );
}

// Overridable via env var so users with their own Base RPC (Alchemy, Infura, etc.)
// get a much higher rate-limit ceiling than the shared public endpoints.
export const BASE_RPC_URL = process.env.BASE_RPC_URL ?? "https://base-rpc.publicnode.com";

// Logs for the Aero (v3) fee window. publicnode answers 403 to eth_getLogs older
// than ~10,000 blocks (5.5 h); Tenderly's public gateway serves the full 96 h,
// 1,000 blocks per call (measured 2026-10-22).
export const V3_LOGS_RPC_URL = process.env.V3_LOGS_RPC_URL ?? "https://base.gateway.tenderly.co";

export const DEFILLAMA_PRICE_URL = "https://coins.llama.fi/prices/current";

// Bounds how long a single DefiLlama batch request can hang before it's treated
// as a failure. Without this, a stalled connection (no response, no error) never
// resolves or rejects, so a hung request would block a whole ranking run forever
// — and for mcp-server.ts, which holds one process open across many tool calls,
// that wedges every future call too, not just the one that hit it.
export const DEFILLAMA_TIMEOUT_MS = 8000;

// How many extra attempts a DefiLlama batch gets after an initial failure
// (network error, non-ok response, or timeout) before falling back to $0 —
// mirrors chain.ts's retry around the Base RPC client, which exists for the
// same reason: a public, unauthenticated endpoint drops occasional requests
// under load, and that shouldn't cost a whole batch its pricing. Kept lower
// than the RPC's retryCount (6) since a batch request is comma-joined and
// costs real latency to redo, and this runs inside mcp-server.ts's per-call
// budget rather than a single eth_call.
export const DEFILLAMA_RETRY_COUNT = 2;

// Delay between DefiLlama retry attempts. Short relative to DEFILLAMA_TIMEOUT_MS
// since most failures worth retrying (a dropped connection, a transient 5xx)
// clear within a second, not the RPC client's 1500ms (that backs off against
// rate-limiting; this backs off against a blip).
export const DEFILLAMA_RETRY_DELAY_MS = 400;

// Max token addresses per DefiLlama price request. A run can touch bribe/fee
// tokens across hundreds of live-gauge pools, and one comma-joined URL covering
// all of them at once risks tripping URL-length limits on DefiLlama's edge/CDN —
// which would silently zero out pricing for every token in the run, not just the
// ones that were actually the problem. Batching bounds the blast radius of a
// single failed/oversized request to just that batch.
export const PRICE_BATCH_SIZE = 50;

// How many DefiLlama batch requests run at once. Bounded rather than unbounded
// (a run can produce several batches) so a burst of simultaneous requests
// doesn't look like abuse to DefiLlama's edge/CDN.
export const PRICE_BATCH_CONCURRENCY = 4;

// How long a successfully looked-up price stays valid before it's refetched.
// The CLI is a fresh process per invocation so this never matters there, but
// mcp-server.ts holds one process open for the life of a client connection —
// without a TTL, prices would be cached forever for that process and silently
// go stale.
export const PRICE_CACHE_TTL_MS = 5 * 60 * 1000;

// How long the $0 fallback stays valid — much shorter than a real price, and
// deliberately so. The two are not the same kind of fact: a real price is
// information that ages slowly, while a $0 fallback is the absence of one, and
// it is written both for tokens DefiLlama genuinely doesn't price and for a
// batch that merely failed to reach it. Caching those together for five minutes
// meant one timed-out request could value a token at $0 across a whole run of
// mcp-server.ts calls — enough to drop real pools below MIN_TRAILING_USD and
// reorder a ranking, with nothing in the output saying why. At 30s a transient
// failure costs one refetch; a genuinely unpriced token costs a cheap retry per
// batch, since it is looked up alongside the rest of its batch either way.
export const PRICE_FAILURE_CACHE_TTL_MS = 30 * 1000;

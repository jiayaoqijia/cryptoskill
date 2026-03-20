/**
 * @x402-kit/agent — HTTP interceptor for AI agents to auto-pay x402 paywalls.
 *
 * Main export: `createAgentFetch()` — a policy-aware fetch wrapper that
 * auto-detects 402 paywalls, checks spending policy, signs payments,
 * retries, and logs results.
 *
 * Also re-exports from @x402/fetch for users who want bare x402 client
 * without our policy layer.
 */
export { createAgentFetch } from "./interceptor.js";
export type { AgentFetchConfig } from "./interceptor.js";

// Re-exports for convenience
export { wrapFetchWithPayment, wrapFetchWithPaymentFromConfig } from "@x402/fetch";
export type { x402ClientConfig } from "@x402/fetch";

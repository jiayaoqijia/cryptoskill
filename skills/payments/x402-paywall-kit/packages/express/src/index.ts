/**
 * @x402-kit/express — Enhanced Express middleware for x402 crypto paywalls.
 *
 * Main export: `x402EnhancedMiddleware()` — a simplified, logging-enabled
 * wrapper around the upstream `@x402/express` payment middleware.
 *
 * Also re-exports from @x402/express for users who need lower-level control.
 */
export { x402EnhancedMiddleware } from "./middleware.js";
export type {
  EnhancedMiddlewareConfig,
  RoutePaymentConfig,
} from "./middleware.js";

// Re-exports for convenience
export { paymentMiddleware, paymentMiddlewareFromConfig } from "@x402/express";

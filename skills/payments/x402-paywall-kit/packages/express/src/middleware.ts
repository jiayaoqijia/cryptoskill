import type { RequestHandler } from "express";
import { paymentMiddleware, x402ResourceServer } from "@x402/express";
import { HTTPFacilitatorClient } from "@x402/core/server";
import { registerExactEvmScheme } from "@x402/evm/exact/server";
import { createPaymentLogger } from "x402-kit-shared";
import type { Network } from "@x402/core/types";

/**
 * Payment configuration for a single route.
 */
export interface RoutePaymentConfig {
  /** Price for the route (e.g., "$0.10", "0.10", or 0.10). */
  price: string | number;
  /** Recipient wallet address (payTo). */
  recipient: string;
  /** Blockchain network in CAIP-2 format (default: "eip155:8453" for Base). */
  network?: Network;
  /** Human-readable resource description. */
  description?: string;
  /** MIME type of the protected resource. */
  mimeType?: string;
  /** Maximum timeout in seconds for payment settlement. */
  maxTimeoutSeconds?: number;
}

/**
 * Configuration for the enhanced x402 Express middleware.
 */
export interface EnhancedMiddlewareConfig {
  /** Route payment configs — maps route patterns to payment settings.
   *  A single RoutePaymentConfig applies to all routes. */
  routes: Record<string, RoutePaymentConfig> | RoutePaymentConfig;
  /** Path to the payment log file (JSONL format). */
  logFilePath?: string;
  /** Custom facilitator URL (defaults to https://x402.org/facilitator). */
  facilitatorUrl?: string;
  /** Paywall UI configuration passed through to upstream middleware. */
  paywallConfig?: {
    appName?: string;
    appLogo?: string;
    testnet?: boolean;
  };
  /** Whether to sync with facilitator on first request (default: true). */
  syncFacilitatorOnStart?: boolean;
}

const DEFAULT_NETWORK: Network = "eip155:8453";

/**
 * Convert our simplified route config into the upstream RoutesConfig format.
 */
function buildRoutesConfig(
  routes: Record<string, RoutePaymentConfig> | RoutePaymentConfig,
) {
  // Single config → apply to all routes
  if ("price" in routes && "recipient" in routes) {
    const config = routes as RoutePaymentConfig;
    return {
      accepts: {
        scheme: "exact" as const,
        network: config.network ?? DEFAULT_NETWORK,
        payTo: config.recipient,
        price: config.price,
        maxTimeoutSeconds: config.maxTimeoutSeconds ?? 300,
      },
      description: config.description,
      mimeType: config.mimeType,
    };
  }

  // Multi-route config
  const result: Record<string, unknown> = {};
  for (const [pattern, config] of Object.entries(
    routes as Record<string, RoutePaymentConfig>,
  )) {
    result[pattern] = {
      accepts: {
        scheme: "exact" as const,
        network: config.network ?? DEFAULT_NETWORK,
        payTo: config.recipient,
        price: config.price,
        maxTimeoutSeconds: config.maxTimeoutSeconds ?? 300,
      },
      description: config.description,
      mimeType: config.mimeType,
    };
  }
  return result;
}

/**
 * Create an enhanced Express middleware for x402 crypto paywalls.
 *
 * Wraps the upstream `paymentMiddleware` from `@x402/express` with:
 * - Simplified route configuration (price + recipient)
 * - Payment event logging (JSONL via `x402-kit-shared`)
 * - Settlement hooks for observability
 *
 * @example
 * ```ts
 * import express from "express";
 * import { x402EnhancedMiddleware } from "@x402-kit/express";
 *
 * const app = express();
 * app.use(x402EnhancedMiddleware({
 *   routes: {
 *     "GET /api/premium/*": {
 *       price: "$0.10",
 *       recipient: "0xYourAddress",
 *     },
 *   },
 *   logFilePath: "./payments.jsonl",
 * }));
 * ```
 */
export function x402EnhancedMiddleware(
  config: EnhancedMiddlewareConfig,
): RequestHandler {
  const facilitator = new HTTPFacilitatorClient(
    config.facilitatorUrl ? { url: config.facilitatorUrl } : undefined,
  );

  const server = new x402ResourceServer(facilitator);
  registerExactEvmScheme(server);

  // Add logging hooks
  if (config.logFilePath) {
    const logger = createPaymentLogger(config.logFilePath);

    server.onAfterSettle(async (ctx) => {
      const req = ctx.requirements;
      const result = ctx.result;
      const transport = ctx.transportContext as
        | { request?: { url?: string } }
        | undefined;

      logger.log({
        timestamp: new Date().toISOString(),
        url: transport?.request?.url ?? "",
        amount: req.amount,
        asset: req.asset,
        network: req.network,
        facilitator: config.facilitatorUrl ?? "https://x402.org/facilitator",
        txHash: result.transaction,
        success: result.success,
        error: result.success ? undefined : result.errorReason,
        policyDecision: "approved",
      });
    });

    server.onSettleFailure(async (ctx) => {
      const req = ctx.requirements;

      logger.log({
        timestamp: new Date().toISOString(),
        url: "",
        amount: req.amount,
        asset: req.asset,
        network: req.network,
        facilitator: config.facilitatorUrl ?? "https://x402.org/facilitator",
        success: false,
        error: ctx.error.message,
        policyDecision: "approved",
      });
    });
  }

  const routes = buildRoutesConfig(config.routes);

  return paymentMiddleware(
    routes as Parameters<typeof paymentMiddleware>[0],
    server,
    config.paywallConfig,
    undefined,
    config.syncFacilitatorOnStart,
  ) as RequestHandler;
}

/**
 * Exported for testing — converts simplified route config to upstream format.
 * @internal
 */
export { buildRoutesConfig as _buildRoutesConfig };

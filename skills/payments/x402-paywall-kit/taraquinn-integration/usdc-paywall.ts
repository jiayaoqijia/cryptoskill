/**
 * USDC payment endpoint for taraquinn.ai using x402 middleware.
 *
 * Paywalls the x402 Paywall Kit download behind a $29 USDC payment on Base.
 * Uses our own @x402-kit/express middleware — eating our own dogfood!
 *
 * Add to: /api/products/x402-paywall-kit (Next.js API route or Express endpoint)
 *
 * Environment variables:
 *   X402_PAYTO_ADDRESS    — Tara's wallet (0x5b99070C84aB6297F2c1a25490c53eE483C8B499)
 *
 * Note: This endpoint serves as both the paywall and the delivery mechanism.
 * Without payment: returns 402 with x402 requirements.
 * With valid payment: returns the download URL.
 */

/*
 * Example implementation (Express):
 *
 * import express from "express";
 * import { x402EnhancedMiddleware } from "@x402-kit/express";
 *
 * const app = express();
 *
 * // Paywall the product download endpoint
 * app.use(
 *   x402EnhancedMiddleware({
 *     routes: {
 *       "GET /api/products/x402-paywall-kit/download": {
 *         price: "$29.00",
 *         recipient: process.env.X402_PAYTO_ADDRESS!,
 *         network: "eip155:8453", // Base mainnet
 *         description: "x402 Paywall Kit — one-time purchase",
 *         mimeType: "application/json",
 *       },
 *     },
 *     logFilePath: "./logs/x402-sales.jsonl",
 *   }),
 * );
 *
 * // Only reached after successful USDC payment
 * app.get("/api/products/x402-paywall-kit/download", (req, res) => {
 *   res.json({
 *     product: "x402-paywall-kit",
 *     version: "1.0.0",
 *     downloadUrl: "https://github.com/tara-quinn-ai/x402-kit/archive/refs/tags/v1.0.0.tar.gz",
 *     // Or: generate a signed URL for a private download
 *   });
 * });
 */

export const USDC_PAYWALL_CONFIG = {
  price: "$29.00",
  recipient: "0x5b99070C84aB6297F2c1a25490c53eE483C8B499", // Tara's wallet
  network: "eip155:8453" as const, // Base mainnet
  description: "x402 Paywall Kit — one-time purchase",
  mimeType: "application/json",
};

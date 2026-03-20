/**
 * Demo: Paywalled Express API server.
 *
 * GET /api/joke — returns a joke for 0.01 USDC on Base Sepolia.
 * Unauthenticated requests get HTTP 402 with x402 payment requirements.
 *
 * Usage:
 *   export X402_PAYTO_ADDRESS="0xYourAddress"
 *   npx tsx demo/server.ts
 */

import express from "express";
import { x402EnhancedMiddleware } from "@x402-kit/express";

const PAYTO = process.env.X402_PAYTO_ADDRESS;
if (!PAYTO) {
  console.error("Error: X402_PAYTO_ADDRESS environment variable is required");
  console.error("Set it to the wallet address that receives payments.");
  process.exit(1);
}

const PORT = parseInt(process.env.PORT ?? "3000");

const app = express();

// Protect /api/joke with a 0.01 USDC paywall on Base Sepolia
app.use(
  x402EnhancedMiddleware({
    routes: {
      "GET /api/joke": {
        price: "$0.01",
        recipient: PAYTO,
        network: "eip155:84532", // Base Sepolia testnet
        description: "A premium joke",
        mimeType: "application/json",
      },
    },
    logFilePath: "./demo/payments-server.jsonl",
    paywallConfig: {
      appName: "x402-kit Demo",
      testnet: true,
    },
  }),
);

// The protected route — only reached after successful payment
app.get("/api/joke", (_req, res) => {
  const jokes = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "A SQL query walks into a bar, sees two tables, and asks: 'Can I join you?'",
    "Why was the JavaScript developer sad? Because he didn't Node how to Express himself.",
    "What's a blockchain developer's favorite music? Heavy metal — because of all the chains.",
    "Why did the crypto investor break up? There was no trust in the relationship.",
  ];

  const joke = jokes[Math.floor(Math.random() * jokes.length)];

  res.json({
    joke,
    paidWith: "x402 protocol",
    network: "Base Sepolia",
    price: "0.01 USDC",
  });
});

// Health check (free, no paywall)
app.get("/health", (_req, res) => {
  res.json({ status: "ok" });
});

app.listen(PORT, () => {
  console.log(`x402-kit demo server running on http://localhost:${PORT}`);
  console.log(`  Paywalled:  GET http://localhost:${PORT}/api/joke (0.01 USDC)`);
  console.log(`  Free:       GET http://localhost:${PORT}/health`);
  console.log(`  Payments to: ${PAYTO}`);
  console.log(`  Network:    Base Sepolia (eip155:84532)`);
  console.log();
  console.log("Waiting for requests...");
});

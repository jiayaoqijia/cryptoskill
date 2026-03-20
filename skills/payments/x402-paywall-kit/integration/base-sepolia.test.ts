/**
 * Integration test: full x402 payment flow on Base Sepolia.
 *
 * Spins up a local Express server with x402 paywall middleware,
 * then uses the x402 client to detect the 402, sign a payment,
 * and retry the request successfully.
 *
 * Required env vars (test skips if missing):
 *   X402_WALLET_PRIVATE_KEY  — Hex private key of a wallet with testnet USDC
 *   X402_PAYTO_ADDRESS       — Recipient wallet address (any valid 0x address)
 */

import { describe, it, expect, beforeAll, afterAll } from "vitest";
import express from "express";
import type { Server } from "node:http";
import { createWalletClient, createPublicClient, http, type Hex } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { baseSepolia } from "viem/chains";
import { ExactEvmScheme, toClientEvmSigner } from "@x402/evm";
import { ExactEvmScheme as ExactEvmSchemeServer } from "@x402/evm/exact/server";
import { x402Client } from "@x402/core/client";
import { HTTPFacilitatorClient } from "@x402/core/http";
import { wrapFetchWithPayment } from "@x402/fetch";
import {
  paymentMiddleware,
  x402ResourceServer,
} from "@x402/express";

// ─── Config ──────────────────────────────────────────────────────────

const PRIVATE_KEY = process.env.X402_WALLET_PRIVATE_KEY as Hex | undefined;
const PAYTO = process.env.X402_PAYTO_ADDRESS as `0x${string}` | undefined;
const NETWORK = "eip155:84532" as const; // Base Sepolia
const PRICE = "0.001"; // 0.001 USDC — minimal amount for testing
const PORT = 0; // random available port

const canRun = Boolean(PRIVATE_KEY && PAYTO);

// ─── Test suite ──────────────────────────────────────────────────────

describe.skipIf(!canRun)("Base Sepolia integration", () => {
  let server: Server;
  let baseUrl: string;
  let fetchWithPay: typeof fetch;

  beforeAll(async () => {
    // --- Server setup ---
    const app = express();

    const facilitator = new HTTPFacilitatorClient();
    const resourceServer = new x402ResourceServer(facilitator).register(
      NETWORK,
      new ExactEvmSchemeServer(),
    );

    const routes = {
      "/api/joke": {
        accepts: {
          scheme: "exact" as const,
          network: NETWORK,
          payTo: PAYTO!,
          price: PRICE,
        },
      },
    };

    app.use(
      paymentMiddleware(routes, resourceServer, { testnet: true }, undefined, true),
    );

    app.get("/api/joke", (_req, res) => {
      res.json({ joke: "Why did the AI cross the road? To pay the toll." });
    });

    // Start on a random port
    await new Promise<void>((resolve) => {
      server = app.listen(PORT, () => resolve());
    });
    const addr = server.address();
    const port = typeof addr === "object" && addr ? addr.port : PORT;
    baseUrl = `http://localhost:${port}`;

    // --- Client setup ---
    const account = privateKeyToAccount(PRIVATE_KEY!);
    const walletClient = createWalletClient({
      account,
      chain: baseSepolia,
      transport: http(),
    });
    const publicClient = createPublicClient({
      chain: baseSepolia,
      transport: http(),
    });

    const signer = toClientEvmSigner(walletClient, publicClient);
    const client = new x402Client().register(
      NETWORK,
      new ExactEvmScheme(signer),
    );
    fetchWithPay = wrapFetchWithPayment(fetch, client);
  });

  afterAll(async () => {
    if (server) {
      await new Promise<void>((resolve) => server.close(() => resolve()));
    }
  });

  it("gets 402 without payment", async () => {
    const response = await fetch(`${baseUrl}/api/joke`);
    expect(response.status).toBe(402);
  });

  it("completes full flow: 402 → pay → success", async () => {
    const response = await fetchWithPay(`${baseUrl}/api/joke`);
    expect(response.status).toBe(200);

    const data = await response.json();
    expect(data).toHaveProperty("joke");
  });
});

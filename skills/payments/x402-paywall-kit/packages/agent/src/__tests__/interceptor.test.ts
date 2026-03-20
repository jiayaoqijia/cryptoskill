import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { mkdirSync, rmSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { privateKeyToAccount } from "viem/accounts";
import { encodePaymentRequiredHeader } from "@x402/core/http";
import type { PaymentRequired, PaymentRequirements } from "@x402/core/types";
import type { X402Policy } from "x402-kit-shared";
import { createAgentFetch } from "../interceptor.js";

// Deterministic test private key (not real funds — never use on mainnet)
const TEST_PRIVATE_KEY =
  "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80" as const;
const TEST_ACCOUNT = privateKeyToAccount(TEST_PRIVATE_KEY);

const NETWORK = "eip155:84532" as const;
// USDC on Base Sepolia
const USDC_ADDRESS = "0x036CbD53842c5426634e7929541eC2318f3dCF7e";
const PAYTO = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8" as const;

function basePolicy(overrides?: Partial<X402Policy>): X402Policy {
  return {
    maxPerRequest: "1.00",
    maxDailySpend: "10.00",
    allowedNetworks: [NETWORK],
    allowedAssets: [USDC_ADDRESS],
    requireHumanApproval: false,
    ...overrides,
  };
}

function makePaymentRequired(
  amountRaw = "1000",
  network = NETWORK,
  asset = USDC_ADDRESS,
): PaymentRequired {
  return {
    x402Version: 2,
    resource: {
      url: "http://example.com/api/data",
      description: "Test resource",
      mimeType: "application/json",
    },
    accepts: [
      {
        scheme: "exact",
        network,
        asset,
        amount: amountRaw,
        payTo: PAYTO,
        maxTimeoutSeconds: 300,
        extra: {
          // EIP-712 domain parameters required for EIP-3009 signing
          name: "USD Coin",
          version: "2",
        },
      },
    ],
  };
}

function make402Response(paymentRequired: PaymentRequired): Response {
  const encoded = encodePaymentRequiredHeader(paymentRequired);
  return new Response(JSON.stringify(paymentRequired), {
    status: 402,
    headers: {
      "Content-Type": "application/json",
      "PAYMENT-REQUIRED": encoded,
    },
  });
}

function make200Response(data: unknown = { result: "ok" }): Response {
  return new Response(JSON.stringify(data), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
}

describe("createAgentFetch()", () => {
  let tmpDir: string;

  beforeEach(() => {
    tmpDir = join(
      tmpdir(),
      `x402-agent-test-${Date.now()}-${Math.random().toString(36).slice(2)}`,
    );
    mkdirSync(tmpDir, { recursive: true });
  });

  afterEach(() => {
    rmSync(tmpDir, { recursive: true, force: true });
  });

  function makeConfig(
    policyOverrides?: Partial<X402Policy>,
  ) {
    return {
      walletPrivateKey: TEST_PRIVATE_KEY,
      policy: basePolicy(policyOverrides),
      network: NETWORK,
      spendFilePath: join(tmpDir, "spend.json"),
      logFilePath: join(tmpDir, "payments.jsonl"),
      rpcUrl: "http://localhost:1", // dummy — signing is local
    };
  }

  it("passes non-402 responses through unchanged", async () => {
    const mockFetch = vi.fn().mockResolvedValue(make200Response({ hello: "world" }));
    const originalFetch = globalThis.fetch;
    globalThis.fetch = mockFetch;

    try {
      const agentFetch = createAgentFetch(makeConfig());
      const response = await agentFetch("http://example.com/api/free");

      expect(response.status).toBe(200);
      const data = await response.json();
      expect(data).toEqual({ hello: "world" });
      expect(mockFetch).toHaveBeenCalledTimes(1);
    } finally {
      globalThis.fetch = originalFetch;
    }
  });

  it("returns 402 when domain is in denylist", async () => {
    const paymentRequired = makePaymentRequired();
    const mockFetch = vi.fn().mockResolvedValue(make402Response(paymentRequired));
    const originalFetch = globalThis.fetch;
    globalThis.fetch = mockFetch;

    try {
      const agentFetch = createAgentFetch(
        makeConfig({ domainDenylist: ["example.com"] }),
      );
      const response = await agentFetch("http://example.com/api/data");

      expect(response.status).toBe(402);
      // Only one call — no retry
      expect(mockFetch).toHaveBeenCalledTimes(1);

      // Check denial was logged
      const logRaw = readFileSync(join(tmpDir, "payments.jsonl"), "utf-8");
      const logEntry = JSON.parse(logRaw.trim());
      expect(logEntry.policyDecision).toBe("denied");
      expect(logEntry.success).toBe(false);
    } finally {
      globalThis.fetch = originalFetch;
    }
  });

  it("returns 402 when network is not allowed", async () => {
    const paymentRequired = makePaymentRequired();
    const mockFetch = vi.fn().mockResolvedValue(make402Response(paymentRequired));
    const originalFetch = globalThis.fetch;
    globalThis.fetch = mockFetch;

    try {
      const agentFetch = createAgentFetch(
        makeConfig({ allowedNetworks: ["eip155:8453"] }), // mainnet only
      );
      const response = await agentFetch("http://example.com/api/data");

      expect(response.status).toBe(402);
      expect(mockFetch).toHaveBeenCalledTimes(1);
    } finally {
      globalThis.fetch = originalFetch;
    }
  });

  it("returns 402 when asset is not allowed", async () => {
    const paymentRequired = makePaymentRequired();
    const mockFetch = vi.fn().mockResolvedValue(make402Response(paymentRequired));
    const originalFetch = globalThis.fetch;
    globalThis.fetch = mockFetch;

    try {
      const agentFetch = createAgentFetch(
        makeConfig({ allowedAssets: ["0xOTHER"] }),
      );
      const response = await agentFetch("http://example.com/api/data");

      expect(response.status).toBe(402);
      expect(mockFetch).toHaveBeenCalledTimes(1);
    } finally {
      globalThis.fetch = originalFetch;
    }
  });

  it("signs payment and retries when policy approves", async () => {
    const paymentRequired = makePaymentRequired("1000"); // 0.001 USDC
    let callCount = 0;

    const mockFetch = vi.fn().mockImplementation((input: Request) => {
      callCount++;
      if (callCount === 1) {
        return Promise.resolve(make402Response(paymentRequired));
      }
      // Second call should have payment header
      const hasPayment =
        input.headers?.get("X-PAYMENT") || input.headers?.get("PAYMENT-SIGNATURE");
      if (hasPayment) {
        return Promise.resolve(make200Response({ paid: true }));
      }
      return Promise.resolve(make402Response(paymentRequired));
    });

    const originalFetch = globalThis.fetch;
    globalThis.fetch = mockFetch;

    try {
      const agentFetch = createAgentFetch(makeConfig());
      const response = await agentFetch("http://example.com/api/data");

      expect(response.status).toBe(200);
      const data = await response.json();
      expect(data).toEqual({ paid: true });

      // Two calls: initial 402 + retry with payment
      expect(mockFetch).toHaveBeenCalledTimes(2);

      // Check payment was logged as approved
      const logRaw = readFileSync(join(tmpDir, "payments.jsonl"), "utf-8");
      const logEntry = JSON.parse(logRaw.trim());
      expect(logEntry.policyDecision).toBe("approved");
      expect(logEntry.success).toBe(true);
    } finally {
      globalThis.fetch = originalFetch;
    }
  });

  it("tracks cumulative daily spend", async () => {
    const paymentRequired = makePaymentRequired("9500000"); // 9.5 USDC (6 decimals)
    let callCount = 0;

    const mockFetch = vi.fn().mockImplementation(() => {
      callCount++;
      if (callCount % 2 === 1) {
        return Promise.resolve(make402Response(paymentRequired));
      }
      return Promise.resolve(make200Response({ paid: true }));
    });

    const originalFetch = globalThis.fetch;
    globalThis.fetch = mockFetch;

    try {
      // maxDailySpend is 10.00 — first payment of 9.5 is fine, second would exceed
      const agentFetch = createAgentFetch(
        makeConfig({ maxDailySpend: "10.00", maxPerRequest: "10.00" }),
      );

      // First request: should succeed (9.5 < 10.0)
      const r1 = await agentFetch("http://example.com/api/data");
      expect(r1.status).toBe(200);

      // Second request: should be denied (9.5 + 9.5 = 19.0 > 10.0)
      callCount = 0; // reset
      const r2 = await agentFetch("http://example.com/api/data");
      expect(r2.status).toBe(402);

      // Check that the log has 2 entries: one approved, one denied
      const logRaw = readFileSync(join(tmpDir, "payments.jsonl"), "utf-8");
      const entries = logRaw
        .trim()
        .split("\n")
        .map((l) => JSON.parse(l));
      expect(entries).toHaveLength(2);
      expect(entries[0].policyDecision).toBe("approved");
      expect(entries[1].policyDecision).toBe("denied");
    } finally {
      globalThis.fetch = originalFetch;
    }
  });

  it("returns 402 for non-x402 402 responses", async () => {
    // A plain 402 without x402 headers
    const mockFetch = vi.fn().mockResolvedValue(
      new Response("Payment Required", { status: 402 }),
    );
    const originalFetch = globalThis.fetch;
    globalThis.fetch = mockFetch;

    try {
      const agentFetch = createAgentFetch(makeConfig());
      const response = await agentFetch("http://example.com/api/data");

      expect(response.status).toBe(402);
      expect(mockFetch).toHaveBeenCalledTimes(1);
    } finally {
      globalThis.fetch = originalFetch;
    }
  });
});

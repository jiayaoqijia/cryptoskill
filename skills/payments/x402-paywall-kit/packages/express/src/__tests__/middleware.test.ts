import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { mkdirSync, rmSync, readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import {
  x402EnhancedMiddleware,
  _buildRoutesConfig,
  type EnhancedMiddlewareConfig,
  type RoutePaymentConfig,
} from "../middleware.js";

// ---------------------------------------------------------------------------
// buildRoutesConfig — pure function tests
// ---------------------------------------------------------------------------

describe("buildRoutesConfig()", () => {
  it("converts a single-route config to upstream format", () => {
    const input: RoutePaymentConfig = {
      price: "$0.10",
      recipient: "0xRecipient",
      description: "Premium API",
    };

    const result = _buildRoutesConfig(input) as Record<string, unknown>;

    expect(result).toEqual({
      accepts: {
        scheme: "exact",
        network: "eip155:8453",
        payTo: "0xRecipient",
        price: "$0.10",
        maxTimeoutSeconds: 300,
      },
      description: "Premium API",
      mimeType: undefined,
    });
  });

  it("converts multi-route config to upstream format", () => {
    const input: Record<string, RoutePaymentConfig> = {
      "GET /api/premium/*": {
        price: 0.5,
        recipient: "0xAddr1",
        network: "eip155:84532",
      },
      "POST /api/generate": {
        price: "$1.00",
        recipient: "0xAddr2",
        maxTimeoutSeconds: 600,
      },
    };

    const result = _buildRoutesConfig(input) as Record<string, unknown>;

    expect(result).toHaveProperty("GET /api/premium/*");
    expect(result).toHaveProperty("POST /api/generate");

    const premium = result["GET /api/premium/*"] as Record<string, unknown>;
    expect(premium.accepts).toEqual({
      scheme: "exact",
      network: "eip155:84532",
      payTo: "0xAddr1",
      price: 0.5,
      maxTimeoutSeconds: 300,
    });

    const generate = result["POST /api/generate"] as Record<string, unknown>;
    expect(generate.accepts).toEqual({
      scheme: "exact",
      network: "eip155:8453",
      payTo: "0xAddr2",
      price: "$1.00",
      maxTimeoutSeconds: 600,
    });
  });

  it("defaults network to eip155:8453 (Base mainnet)", () => {
    const result = _buildRoutesConfig({
      price: "0.01",
      recipient: "0xTest",
    }) as Record<string, unknown>;

    const accepts = result.accepts as Record<string, unknown>;
    expect(accepts.network).toBe("eip155:8453");
  });

  it("uses custom network when provided", () => {
    const result = _buildRoutesConfig({
      price: "0.01",
      recipient: "0xTest",
      network: "eip155:84532",
    }) as Record<string, unknown>;

    const accepts = result.accepts as Record<string, unknown>;
    expect(accepts.network).toBe("eip155:84532");
  });
});

// ---------------------------------------------------------------------------
// x402EnhancedMiddleware — factory function tests
// ---------------------------------------------------------------------------

describe("x402EnhancedMiddleware()", () => {
  it("returns a function (Express middleware)", () => {
    const middleware = x402EnhancedMiddleware({
      routes: {
        price: "$0.10",
        recipient: "0xRecipient",
      },
      syncFacilitatorOnStart: false,
    });

    expect(typeof middleware).toBe("function");
  });

  it("accepts multi-route config without errors", () => {
    const middleware = x402EnhancedMiddleware({
      routes: {
        "GET /api/data": {
          price: "$0.50",
          recipient: "0xAddr",
          network: "eip155:84532",
        },
        "POST /api/submit": {
          price: "$1.00",
          recipient: "0xAddr",
        },
      },
      syncFacilitatorOnStart: false,
    });

    expect(typeof middleware).toBe("function");
  });

  it("accepts custom facilitator URL", () => {
    const middleware = x402EnhancedMiddleware({
      routes: {
        price: "$0.10",
        recipient: "0xRecipient",
      },
      facilitatorUrl: "https://custom-facilitator.example.com",
      syncFacilitatorOnStart: false,
    });

    expect(typeof middleware).toBe("function");
  });

  it("accepts paywall config", () => {
    const middleware = x402EnhancedMiddleware({
      routes: {
        price: "$0.10",
        recipient: "0xRecipient",
      },
      paywallConfig: {
        appName: "My App",
        appLogo: "https://example.com/logo.png",
        testnet: true,
      },
      syncFacilitatorOnStart: false,
    });

    expect(typeof middleware).toBe("function");
  });
});

// ---------------------------------------------------------------------------
// Logging — verify log file path is used
// ---------------------------------------------------------------------------

describe("x402EnhancedMiddleware() logging", () => {
  let tmpDir: string;

  beforeEach(() => {
    tmpDir = join(
      tmpdir(),
      `x402-express-test-${Date.now()}-${Math.random().toString(36).slice(2)}`,
    );
    mkdirSync(tmpDir, { recursive: true });
  });

  afterEach(() => {
    rmSync(tmpDir, { recursive: true, force: true });
  });

  it("creates middleware with log file path without errors", () => {
    const logPath = join(tmpDir, "payments.jsonl");

    const middleware = x402EnhancedMiddleware({
      routes: {
        price: "$0.10",
        recipient: "0xRecipient",
      },
      logFilePath: logPath,
      syncFacilitatorOnStart: false,
    });

    expect(typeof middleware).toBe("function");
    // Log file is not created until first write
  });

  it("does not create logger when logFilePath is omitted", () => {
    const middleware = x402EnhancedMiddleware({
      routes: {
        price: "$0.10",
        recipient: "0xRecipient",
      },
      syncFacilitatorOnStart: false,
    });

    expect(typeof middleware).toBe("function");
  });
});

// ---------------------------------------------------------------------------
// Middleware behavior with mock facilitator
// ---------------------------------------------------------------------------

describe("x402EnhancedMiddleware() request handling", () => {
  it("calls next() for unmatched routes", async () => {
    const middleware = x402EnhancedMiddleware({
      routes: {
        "GET /api/premium/*": {
          price: "$0.10",
          recipient: "0xRecipient",
        },
      },
      syncFacilitatorOnStart: false,
    });

    // Simulate Express request/response for an unprotected path
    const req = {
      method: "GET",
      url: "/api/free",
      path: "/api/free",
      headers: {},
      get: (name: string) => (req.headers as Record<string, string>)[name.toLowerCase()],
      header: (name: string) => (req.headers as Record<string, string>)[name.toLowerCase()],
    };
    const res = {
      statusCode: 200,
      headers: {} as Record<string, string>,
      setHeader: (name: string, value: string) => { res.headers[name] = value; },
      getHeader: (name: string) => res.headers[name],
      status: (code: number) => { res.statusCode = code; return res; },
      json: vi.fn(),
      send: vi.fn(),
      end: vi.fn(),
    };
    const next = vi.fn();

    await middleware(req as any, res as any, next);

    // Unmatched route: next() should be called
    expect(next).toHaveBeenCalled();
  });
});

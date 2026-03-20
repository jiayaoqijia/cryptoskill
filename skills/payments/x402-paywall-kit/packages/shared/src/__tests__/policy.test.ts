import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { mkdirSync, writeFileSync, rmSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { evaluate, createPolicyEngine } from "../policy/index.js";
import type { X402Policy } from "../types/index.js";

/** A default permissive policy for tests. */
function basePolicy(overrides?: Partial<X402Policy>): X402Policy {
  return {
    maxPerRequest: "1.00",
    maxDailySpend: "10.00",
    allowedNetworks: ["base:mainnet"],
    allowedAssets: ["USDC"],
    requireHumanApproval: false,
    ...overrides,
  };
}

// ---------- evaluate() ----------

describe("evaluate()", () => {
  it("approves when all limits are satisfied", () => {
    const result = evaluate("0.50", "base:mainnet", "USDC", "example.com", basePolicy());
    expect(result.decision).toBe("approved");
    expect(result.reason).toBeUndefined();
  });

  it("denies when domain is in denylist", () => {
    const policy = basePolicy({ domainDenylist: ["evil.com"] });
    const result = evaluate("0.50", "base:mainnet", "USDC", "evil.com", policy);
    expect(result.decision).toBe("denied");
    expect(result.reason).toContain("denylist");
  });

  it("denies when domain is not in allowlist", () => {
    const policy = basePolicy({ domainAllowlist: ["trusted.com"] });
    const result = evaluate("0.50", "base:mainnet", "USDC", "other.com", policy);
    expect(result.decision).toBe("denied");
    expect(result.reason).toContain("allowlist");
  });

  it("approves when domain is in allowlist", () => {
    const policy = basePolicy({ domainAllowlist: ["trusted.com"] });
    const result = evaluate("0.50", "base:mainnet", "USDC", "trusted.com", policy);
    expect(result.decision).toBe("approved");
  });

  it("allows all domains when allowlist is empty", () => {
    const policy = basePolicy({ domainAllowlist: [] });
    const result = evaluate("0.50", "base:mainnet", "USDC", "anything.com", policy);
    expect(result.decision).toBe("approved");
  });

  it("allows all domains when allowlist is undefined", () => {
    const policy = basePolicy({ domainAllowlist: undefined });
    const result = evaluate("0.50", "base:mainnet", "USDC", "anything.com", policy);
    expect(result.decision).toBe("approved");
  });

  it("denies when network is not allowed", () => {
    const result = evaluate("0.50", "ethereum:mainnet", "USDC", "example.com", basePolicy());
    expect(result.decision).toBe("denied");
    expect(result.reason).toContain("Network");
  });

  it("denies when asset is not allowed", () => {
    const result = evaluate("0.50", "base:mainnet", "DAI", "example.com", basePolicy());
    expect(result.decision).toBe("denied");
    expect(result.reason).toContain("Asset");
  });

  it("denies when amount exceeds maxPerRequest", () => {
    const result = evaluate("1.50", "base:mainnet", "USDC", "example.com", basePolicy());
    expect(result.decision).toBe("denied");
    expect(result.reason).toContain("per-request");
  });

  it("returns needs-human-approval when amount exceeds maxPerRequest and requireHumanApproval is true", () => {
    const policy = basePolicy({ requireHumanApproval: true });
    const result = evaluate("1.50", "base:mainnet", "USDC", "example.com", policy);
    expect(result.decision).toBe("needs-human-approval");
    expect(result.reason).toContain("per-request");
  });

  it("denies when daily spend would exceed maxDailySpend", () => {
    const result = evaluate("0.50", "base:mainnet", "USDC", "example.com", basePolicy(), 9.75);
    expect(result.decision).toBe("denied");
    expect(result.reason).toContain("Daily spend");
  });

  it("returns needs-human-approval when daily spend would exceed and requireHumanApproval is true", () => {
    const policy = basePolicy({ requireHumanApproval: true });
    const result = evaluate("0.50", "base:mainnet", "USDC", "example.com", policy, 9.75);
    expect(result.decision).toBe("needs-human-approval");
    expect(result.reason).toContain("Daily spend");
  });

  it("approves when amount is exactly at per-request limit", () => {
    const result = evaluate("1.00", "base:mainnet", "USDC", "example.com", basePolicy());
    expect(result.decision).toBe("approved");
  });

  it("approves when daily spend is exactly at daily limit", () => {
    const result = evaluate("0.50", "base:mainnet", "USDC", "example.com", basePolicy(), 9.50);
    expect(result.decision).toBe("approved");
  });

  it("checks denylist before allowlist", () => {
    const policy = basePolicy({
      domainAllowlist: ["evil.com"],
      domainDenylist: ["evil.com"],
    });
    const result = evaluate("0.50", "base:mainnet", "USDC", "evil.com", policy);
    expect(result.decision).toBe("denied");
    expect(result.reason).toContain("denylist");
  });
});

// ---------- createPolicyEngine() ----------

describe("createPolicyEngine()", () => {
  let tmpDir: string;

  beforeEach(() => {
    tmpDir = join(tmpdir(), `x402-test-${Date.now()}-${Math.random().toString(36).slice(2)}`);
    mkdirSync(tmpDir, { recursive: true });
  });

  afterEach(() => {
    rmSync(tmpDir, { recursive: true, force: true });
  });

  function spendFile(): string {
    return join(tmpDir, "spend.json");
  }

  it("tracks spend across calls", () => {
    const engine = createPolicyEngine(basePolicy(), { spendFilePath: spendFile() });

    const r1 = engine.evaluate("0.50", "base:mainnet", "USDC", "example.com");
    expect(r1.decision).toBe("approved");
    engine.recordSpend("0.50");
    expect(engine.getDailySpend()).toBe(0.5);

    // Second request — still within limits
    const r2 = engine.evaluate("0.50", "base:mainnet", "USDC", "example.com");
    expect(r2.decision).toBe("approved");
    engine.recordSpend("0.50");
    expect(engine.getDailySpend()).toBe(1.0);
  });

  it("denies when cumulative spend exceeds daily limit", () => {
    const engine = createPolicyEngine(basePolicy({ maxDailySpend: "1.00" }), {
      spendFilePath: spendFile(),
    });

    engine.recordSpend("0.80");
    const result = engine.evaluate("0.50", "base:mainnet", "USDC", "example.com");
    expect(result.decision).toBe("denied");
    expect(result.reason).toContain("Daily spend");
  });

  it("persists spend to file", () => {
    const path = spendFile();
    const engine = createPolicyEngine(basePolicy(), { spendFilePath: path });
    engine.recordSpend("3.50");

    const data = JSON.parse(readFileSync(path, "utf-8"));
    expect(data.spent).toBe("3.5");
    expect(data.date).toBe(new Date().toISOString().slice(0, 10));
  });

  it("loads persisted spend on initialization", () => {
    const path = spendFile();
    const today = new Date().toISOString().slice(0, 10);
    writeFileSync(path, JSON.stringify({ date: today, spent: "5.00" }));

    const engine = createPolicyEngine(basePolicy(), { spendFilePath: path });
    expect(engine.getDailySpend()).toBe(5);
  });

  it("ignores persisted spend from a different day", () => {
    const path = spendFile();
    writeFileSync(path, JSON.stringify({ date: "2000-01-01", spent: "9.99" }));

    const engine = createPolicyEngine(basePolicy(), { spendFilePath: path });
    expect(engine.getDailySpend()).toBe(0);
  });

  it("handles corrupted spend file gracefully", () => {
    const path = spendFile();
    writeFileSync(path, "not json!!!");

    const engine = createPolicyEngine(basePolicy(), { spendFilePath: path });
    expect(engine.getDailySpend()).toBe(0);
  });

  it("handles missing spend file gracefully", () => {
    const engine = createPolicyEngine(basePolicy(), {
      spendFilePath: join(tmpDir, "nonexistent", "spend.json"),
    });
    expect(engine.getDailySpend()).toBe(0);
  });
});

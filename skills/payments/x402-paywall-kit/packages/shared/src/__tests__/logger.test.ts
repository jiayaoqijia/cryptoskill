import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { mkdirSync, rmSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { createPaymentLogger } from "../logger/index.js";
import type { X402PaymentLog } from "../types/index.js";

function sampleEntry(overrides?: Partial<X402PaymentLog>): X402PaymentLog {
  return {
    timestamp: "2026-02-27T12:00:00.000Z",
    url: "https://api.example.com/data",
    amount: "0.50",
    asset: "USDC",
    network: "base:mainnet",
    facilitator: "https://x402.org/facilitator",
    success: true,
    policyDecision: "approved",
    ...overrides,
  };
}

describe("createPaymentLogger()", () => {
  let tmpDir: string;

  beforeEach(() => {
    tmpDir = join(
      tmpdir(),
      `x402-logger-test-${Date.now()}-${Math.random().toString(36).slice(2)}`,
    );
    mkdirSync(tmpDir, { recursive: true });
  });

  afterEach(() => {
    rmSync(tmpDir, { recursive: true, force: true });
  });

  function logFile(): string {
    return join(tmpDir, "payments.jsonl");
  }

  it("writes a single entry as JSONL", () => {
    const logger = createPaymentLogger(logFile());
    const entry = sampleEntry();
    logger.log(entry);

    const raw = readFileSync(logFile(), "utf-8");
    const lines = raw.trim().split("\n");
    expect(lines).toHaveLength(1);
    expect(JSON.parse(lines[0])).toEqual(entry);
  });

  it("appends multiple entries on separate lines", () => {
    const logger = createPaymentLogger(logFile());
    const entry1 = sampleEntry({ amount: "0.10" });
    const entry2 = sampleEntry({ amount: "0.20" });
    const entry3 = sampleEntry({ amount: "0.30" });

    logger.log(entry1);
    logger.log(entry2);
    logger.log(entry3);

    const raw = readFileSync(logFile(), "utf-8");
    const lines = raw.trim().split("\n");
    expect(lines).toHaveLength(3);
    expect(JSON.parse(lines[0]).amount).toBe("0.10");
    expect(JSON.parse(lines[1]).amount).toBe("0.20");
    expect(JSON.parse(lines[2]).amount).toBe("0.30");
  });

  it("reads back entries with getEntries()", () => {
    const logger = createPaymentLogger(logFile());
    const entry1 = sampleEntry({ url: "https://a.com" });
    const entry2 = sampleEntry({ url: "https://b.com" });

    logger.log(entry1);
    logger.log(entry2);

    const entries = logger.getEntries();
    expect(entries).toHaveLength(2);
    expect(entries[0].url).toBe("https://a.com");
    expect(entries[1].url).toBe("https://b.com");
  });

  it("returns empty array when file does not exist", () => {
    const logger = createPaymentLogger(join(tmpDir, "nonexistent.jsonl"));
    expect(logger.getEntries()).toEqual([]);
  });

  it("skips malformed lines gracefully", () => {
    const path = logFile();
    const entry = sampleEntry();
    writeFileSync(
      path,
      `${JSON.stringify(entry)}\nNOT VALID JSON\n${JSON.stringify(entry)}\n`,
    );

    const logger = createPaymentLogger(path);
    const entries = logger.getEntries();
    expect(entries).toHaveLength(2);
  });

  it("handles empty file", () => {
    const path = logFile();
    writeFileSync(path, "");

    const logger = createPaymentLogger(path);
    expect(logger.getEntries()).toEqual([]);
  });

  it("creates parent directories if they don't exist", () => {
    const nested = join(tmpDir, "deep", "nested", "payments.jsonl");
    const logger = createPaymentLogger(nested);
    logger.log(sampleEntry());

    const raw = readFileSync(nested, "utf-8");
    expect(raw.trim()).toBeTruthy();
  });

  it("logs failed payment entries", () => {
    const logger = createPaymentLogger(logFile());
    const entry = sampleEntry({
      success: false,
      error: "Facilitator timeout",
      policyDecision: "approved",
    });

    logger.log(entry);

    const entries = logger.getEntries();
    expect(entries).toHaveLength(1);
    expect(entries[0].success).toBe(false);
    expect(entries[0].error).toBe("Facilitator timeout");
  });

  it("logs denied payment entries", () => {
    const logger = createPaymentLogger(logFile());
    const entry = sampleEntry({
      success: false,
      policyDecision: "denied",
    });

    logger.log(entry);

    const entries = logger.getEntries();
    expect(entries[0].policyDecision).toBe("denied");
  });
});

import { readFileSync, appendFileSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";
import type { X402PaymentLog } from "../types/index.js";

export interface PaymentLogger {
  /** Append a payment log entry to the JSONL file. */
  log(entry: X402PaymentLog): void;

  /** Read all log entries from the file. Skips malformed lines. */
  getEntries(): X402PaymentLog[];
}

const DEFAULT_LOG_PATH = "x402-payments.jsonl";

/**
 * Create a payment logger that appends JSON Lines to a file.
 *
 * Each call to `log()` writes one JSON object per line.
 * `getEntries()` reads the file back and parses each line.
 */
export function createPaymentLogger(
  logFilePath: string = DEFAULT_LOG_PATH,
): PaymentLogger {
  function ensureDir(): void {
    mkdirSync(dirname(logFilePath), { recursive: true });
  }

  return {
    log(entry: X402PaymentLog): void {
      ensureDir();
      appendFileSync(logFilePath, JSON.stringify(entry) + "\n", "utf-8");
    },

    getEntries(): X402PaymentLog[] {
      let raw: string;
      try {
        raw = readFileSync(logFilePath, "utf-8");
      } catch {
        return [];
      }

      const entries: X402PaymentLog[] = [];
      for (const line of raw.split("\n")) {
        const trimmed = line.trim();
        if (!trimmed) continue;
        try {
          entries.push(JSON.parse(trimmed) as X402PaymentLog);
        } catch {
          // Skip malformed lines
        }
      }
      return entries;
    },
  };
}

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";
import type { X402Policy, EvaluateResult } from "../types/index.js";

/**
 * Evaluate a payment request against a policy.
 *
 * Pure function — no I/O. The caller provides `currentDailySpend`.
 * Checks are ordered for fast rejection.
 */
export function evaluate(
  amount: string,
  network: string,
  asset: string,
  domain: string,
  policy: X402Policy,
  currentDailySpend: number = 0,
): EvaluateResult {
  // 1. Domain denylist
  if (policy.domainDenylist?.includes(domain)) {
    return { decision: "denied", reason: `Domain "${domain}" is in denylist` };
  }

  // 2. Domain allowlist (non-empty means only those domains are allowed)
  if (
    policy.domainAllowlist &&
    policy.domainAllowlist.length > 0 &&
    !policy.domainAllowlist.includes(domain)
  ) {
    return {
      decision: "denied",
      reason: `Domain "${domain}" is not in allowlist`,
    };
  }

  // 3. Network check
  if (!policy.allowedNetworks.includes(network)) {
    return {
      decision: "denied",
      reason: `Network "${network}" is not allowed`,
    };
  }

  // 4. Asset check
  if (!policy.allowedAssets.includes(asset)) {
    return { decision: "denied", reason: `Asset "${asset}" is not allowed` };
  }

  const amountNum = parseFloat(amount);
  const maxPerRequest = parseFloat(policy.maxPerRequest);
  const maxDailySpend = parseFloat(policy.maxDailySpend);

  // 5. Per-request limit
  if (amountNum > maxPerRequest) {
    if (policy.requireHumanApproval) {
      return {
        decision: "needs-human-approval",
        reason: `Amount ${amount} exceeds per-request limit of ${policy.maxPerRequest}`,
      };
    }
    return {
      decision: "denied",
      reason: `Amount ${amount} exceeds per-request limit of ${policy.maxPerRequest}`,
    };
  }

  // 6. Daily spend limit
  if (currentDailySpend + amountNum > maxDailySpend) {
    if (policy.requireHumanApproval) {
      return {
        decision: "needs-human-approval",
        reason: `Daily spend would be ${currentDailySpend + amountNum}, exceeding limit of ${policy.maxDailySpend}`,
      };
    }
    return {
      decision: "denied",
      reason: `Daily spend would be ${currentDailySpend + amountNum}, exceeding limit of ${policy.maxDailySpend}`,
    };
  }

  // 7. All checks passed
  return { decision: "approved" };
}

/** Shape of the daily spend persistence file. */
interface SpendFile {
  date: string;
  spent: string;
}

/** Returns today's date as YYYY-MM-DD in UTC. */
function todayUTC(): string {
  return new Date().toISOString().slice(0, 10);
}

export interface PolicyEngine {
  /** Evaluate a payment request against the policy. */
  evaluate(
    amount: string,
    network: string,
    asset: string,
    domain: string,
  ): EvaluateResult;

  /** Record that a payment of `amount` was made (updates daily spend). */
  recordSpend(amount: string): void;

  /** Get the current daily spend total. */
  getDailySpend(): number;
}

export interface PolicyEngineOptions {
  /** Path to the JSON file for persisting daily spend. */
  spendFilePath: string;
}

/**
 * Create a stateful policy engine that tracks daily spend in-memory
 * and persists it to a JSON file.
 */
export function createPolicyEngine(
  policy: X402Policy,
  options: PolicyEngineOptions,
): PolicyEngine {
  const { spendFilePath } = options;
  let currentDate = todayUTC();
  let dailySpend = 0;

  // Load persisted spend on initialization
  try {
    const raw = readFileSync(spendFilePath, "utf-8");
    const data: SpendFile = JSON.parse(raw);
    if (data.date === currentDate) {
      dailySpend = parseFloat(data.spent) || 0;
    }
    // If date doesn't match, start fresh (dailySpend stays 0)
  } catch {
    // File doesn't exist or is corrupted — start fresh
  }

  function persist(): void {
    try {
      mkdirSync(dirname(spendFilePath), { recursive: true });
      const data: SpendFile = { date: currentDate, spent: String(dailySpend) };
      writeFileSync(spendFilePath, JSON.stringify(data), "utf-8");
    } catch {
      // Best-effort persistence — don't crash on write failure
    }
  }

  function resetIfNewDay(): void {
    const today = todayUTC();
    if (today !== currentDate) {
      currentDate = today;
      dailySpend = 0;
    }
  }

  return {
    evaluate(
      amount: string,
      network: string,
      asset: string,
      domain: string,
    ): EvaluateResult {
      resetIfNewDay();
      return evaluate(amount, network, asset, domain, policy, dailySpend);
    },

    recordSpend(amount: string): void {
      resetIfNewDay();
      dailySpend += parseFloat(amount);
      persist();
    },

    getDailySpend(): number {
      resetIfNewDay();
      return dailySpend;
    },
  };
}

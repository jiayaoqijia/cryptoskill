/**
 * Re-export upstream x402 types for convenience.
 */
export type {
  PaymentPayload,
  PaymentRequirements,
  PaymentRequired,
  Network,
} from "@x402/core/types";

/**
 * Policy configuration for controlling agent spending behavior.
 */
export interface X402Policy {
  /** Maximum USDC amount per single request (e.g., "1.00") */
  maxPerRequest: string;
  /** Maximum USDC amount per day (e.g., "10.00") */
  maxDailySpend: string;
  /** Allowed blockchain networks (e.g., ["base-sepolia", "base"]) */
  allowedNetworks: string[];
  /** Allowed payment assets (e.g., ["USDC"]) */
  allowedAssets: string[];
  /** If set, only pay these domains */
  domainAllowlist?: string[];
  /** If set, never pay these domains */
  domainDenylist?: string[];
  /** Whether to require human approval for payments above threshold */
  requireHumanApproval: boolean;
}

/**
 * Result of evaluating a payment against a policy.
 */
export type PolicyDecision = "approved" | "denied" | "needs-human-approval";

/**
 * Detailed result from policy evaluation, including denial reason.
 */
export interface EvaluateResult {
  decision: PolicyDecision;
  reason?: string;
}

/**
 * Structured log entry for a payment event.
 */
export interface X402PaymentLog {
  timestamp: string;
  url: string;
  amount: string;
  asset: string;
  network: string;
  facilitator: string;
  txHash?: string;
  success: boolean;
  error?: string;
  policyDecision: PolicyDecision;
}

/**
 * Top-level configuration for x402-kit.
 */
export interface X402KitConfig {
  /** Policy rules for the agent */
  policy: X402Policy;
  /** Path to the payment log file */
  logFilePath?: string;
  /** Facilitator URL (defaults to Coinbase) */
  facilitatorUrl?: string;
}

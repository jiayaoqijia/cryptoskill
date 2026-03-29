import { createHash, randomBytes } from 'crypto';
import { pino, Logger } from 'pino';
import { appendFileSync, existsSync, mkdirSync } from 'fs';
import { dirname } from 'path';
import { getConfig } from './env.js';
import type { NormalizedSwapParams, TransactionData } from './types.js';

// ============================================================================
// Logger Setup
// ============================================================================

let loggerInstance: Logger | null = null;

export function getLogger(): Logger {
  if (loggerInstance) {
    return loggerInstance;
  }

  const config = getConfig();

  loggerInstance = pino({
    level: config.LOG_LEVEL,
  });

  return loggerInstance;
}

// ============================================================================
// Audit Logging
// ============================================================================

export function writeAuditLog(entry: Record<string, unknown>): void {
  const config = getConfig();

  if (!config.ELSA_AUDIT_LOG_PATH) {
    return;
  }

  try {
    const dir = dirname(config.ELSA_AUDIT_LOG_PATH);
    if (!existsSync(dir)) {
      mkdirSync(dir, { recursive: true });
    }

    const line = JSON.stringify({
      ...entry,
      timestamp: new Date().toISOString(),
    }) + '\n';

    appendFileSync(config.ELSA_AUDIT_LOG_PATH, line, 'utf8');
  } catch (error) {
    getLogger().error({ error }, 'Failed to write audit log');
  }
}

// ============================================================================
// Crypto Utilities
// ============================================================================

export function generateToken(): string {
  const bytes = randomBytes(32);
  return bytes.toString('base64url');
}

export function hashParams(params: NormalizedSwapParams): string {
  const json = JSON.stringify(params);
  return createHash('sha256').update(json).digest('hex');
}

// ============================================================================
// Parameter Normalization
// ============================================================================

export function normalizeSwapParams(params: {
  from_chain: string;
  from_token: string;
  from_amount: string;
  to_chain: string;
  to_token: string;
  wallet_address: string;
  slippage: number;
}): NormalizedSwapParams {
  return {
    from_chain: params.from_chain.trim().toLowerCase(),
    from_token: params.from_token.trim().toLowerCase(),
    from_amount: params.from_amount.trim(),
    to_chain: params.to_chain.trim().toLowerCase(),
    to_token: params.to_token.trim().toLowerCase(),
    wallet_address: params.wallet_address.trim().toLowerCase(),
    slippage: params.slippage,
  };
}

// ============================================================================
// Transaction Data Mapping
// ============================================================================

export function mapTransactionData(raw: unknown): TransactionData {
  if (!raw || typeof raw !== 'object') {
    throw new Error('Invalid transaction data: expected object');
  }

  const data = raw as Record<string, unknown>;

  if (!data.to || typeof data.to !== 'string') {
    throw new Error('Invalid transaction data: missing "to" field');
  }

  if (!data.data || typeof data.data !== 'string') {
    throw new Error('Invalid transaction data: missing "data" field');
  }

  const result: TransactionData = {
    to: data.to,
    data: data.data,
  };

  // Optional fields with type coercion
  if (data.value !== undefined) {
    result.value = String(data.value);
  }

  if (data.gas !== undefined) {
    result.gas = String(data.gas);
  }

  if (data.maxFeePerGas !== undefined) {
    result.maxFeePerGas = String(data.maxFeePerGas);
  }

  if (data.maxPriorityFeePerGas !== undefined) {
    result.maxPriorityFeePerGas = String(data.maxPriorityFeePerGas);
  }

  if (data.nonce !== undefined) {
    result.nonce = typeof data.nonce === 'number'
      ? data.nonce
      : parseInt(String(data.nonce), 10);
  }

  if (data.chainId !== undefined) {
    result.chainId = typeof data.chainId === 'number'
      ? data.chainId
      : parseInt(String(data.chainId), 10);
  }

  return result;
}

// ============================================================================
// Timing Utilities
// ============================================================================

export function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export function nowMs(): number {
  return Date.now();
}

// ============================================================================
// Output Helpers
// ============================================================================

export function out(data: unknown): void {
  console.log(JSON.stringify(data, null, 2));
}

export function exitWithError(message: string, code: number = 1): never {
  out({
    ok: false,
    error: {
      code: 'CLI_ERROR',
      message,
    },
  });
  process.exit(code);
}

import { normalizeChainId } from './normalize.js';
import type { AelfscanConfig } from './types.js';

const DEFAULT_TIMEOUT_MS = 10_000;
const DEFAULT_RETRY = 1;
const DEFAULT_API_BASE_URL = 'https://aelfscan.io';
const DEFAULT_RETRY_BASE_MS = 200;
const DEFAULT_RETRY_MAX_MS = 3_000;
const DEFAULT_MAX_CONCURRENT_REQUESTS = 5;
const DEFAULT_CACHE_TTL_MS = 60_000;
const DEFAULT_CACHE_MAX_ENTRIES = 500;
const DEFAULT_MAX_RESULT_COUNT = 200;
const DEFAULT_MCP_MAX_ITEMS = 50;
const DEFAULT_MCP_MAX_CHARS = 60_000;
const DEFAULT_MCP_INCLUDE_RAW = false;

let cachedConfig: AelfscanConfig | null = null;

function toNumber(raw: string | undefined, fallback: number): number {
  if (!raw) {
    return fallback;
  }

  const value = Number(raw);
  return Number.isFinite(value) && value >= 0 ? value : fallback;
}

function toBoolean(raw: string | undefined, fallback: boolean): boolean {
  if (!raw) {
    return fallback;
  }

  const normalized = raw.trim().toLowerCase();
  if (normalized === 'true' || normalized === '1' || normalized === 'yes' || normalized === 'on') {
    return true;
  }

  if (normalized === 'false' || normalized === '0' || normalized === 'no' || normalized === 'off') {
    return false;
  }

  return fallback;
}

function trimSlash(input: string): string {
  return input.replace(/\/+$/, '');
}

export function getConfig(): AelfscanConfig {
  if (cachedConfig) {
    return cachedConfig;
  }

  cachedConfig = {
    apiBaseUrl: trimSlash(process.env.AELFSCAN_API_BASE_URL || DEFAULT_API_BASE_URL),
    defaultChainId: normalizeChainId(process.env.AELFSCAN_DEFAULT_CHAIN_ID || ''),
    timeoutMs: toNumber(process.env.AELFSCAN_TIMEOUT_MS, DEFAULT_TIMEOUT_MS),
    retry: Math.floor(toNumber(process.env.AELFSCAN_RETRY, DEFAULT_RETRY)),
    retryBaseMs: Math.floor(toNumber(process.env.AELFSCAN_RETRY_BASE_MS, DEFAULT_RETRY_BASE_MS)),
    retryMaxMs: Math.floor(toNumber(process.env.AELFSCAN_RETRY_MAX_MS, DEFAULT_RETRY_MAX_MS)),
    maxConcurrentRequests: Math.floor(
      toNumber(process.env.AELFSCAN_MAX_CONCURRENT_REQUESTS, DEFAULT_MAX_CONCURRENT_REQUESTS),
    ),
    cacheTtlMs: Math.floor(toNumber(process.env.AELFSCAN_CACHE_TTL_MS, DEFAULT_CACHE_TTL_MS)),
    cacheMaxEntries: Math.floor(toNumber(process.env.AELFSCAN_CACHE_MAX_ENTRIES, DEFAULT_CACHE_MAX_ENTRIES)),
    maxResultCount: Math.floor(toNumber(process.env.AELFSCAN_MAX_RESULT_COUNT, DEFAULT_MAX_RESULT_COUNT)),
    mcpMaxItems: Math.floor(toNumber(process.env.AELFSCAN_MCP_MAX_ITEMS, DEFAULT_MCP_MAX_ITEMS)),
    mcpMaxChars: Math.floor(toNumber(process.env.AELFSCAN_MCP_MAX_CHARS, DEFAULT_MCP_MAX_CHARS)),
    mcpIncludeRaw: toBoolean(process.env.AELFSCAN_MCP_INCLUDE_RAW, DEFAULT_MCP_INCLUDE_RAW),
  };

  return cachedConfig;
}

export function resetConfigCache(): void {
  cachedConfig = null;
}

import { afterEach, beforeEach, describe, expect, test } from 'bun:test';
import { getConfig, resetConfigCache } from '../../lib/config.js';

const ENV_KEYS = [
  'AELFSCAN_API_BASE_URL',
  'AELFSCAN_DEFAULT_CHAIN_ID',
  'AELFSCAN_TIMEOUT_MS',
  'AELFSCAN_RETRY',
  'AELFSCAN_RETRY_BASE_MS',
  'AELFSCAN_RETRY_MAX_MS',
  'AELFSCAN_MAX_CONCURRENT_REQUESTS',
  'AELFSCAN_CACHE_TTL_MS',
  'AELFSCAN_CACHE_MAX_ENTRIES',
  'AELFSCAN_MAX_RESULT_COUNT',
  'AELFSCAN_MCP_MAX_ITEMS',
  'AELFSCAN_MCP_MAX_CHARS',
  'AELFSCAN_MCP_INCLUDE_RAW',
] as const;

type EnvSnapshot = Record<(typeof ENV_KEYS)[number], string | undefined>;

let snapshot: EnvSnapshot;

function restoreEnv(from: EnvSnapshot): void {
  ENV_KEYS.forEach((key) => {
    const value = from[key];
    if (value === undefined) {
      delete process.env[key];
    } else {
      process.env[key] = value;
    }
  });
}

beforeEach(() => {
  snapshot = {
    AELFSCAN_API_BASE_URL: process.env.AELFSCAN_API_BASE_URL,
    AELFSCAN_DEFAULT_CHAIN_ID: process.env.AELFSCAN_DEFAULT_CHAIN_ID,
    AELFSCAN_TIMEOUT_MS: process.env.AELFSCAN_TIMEOUT_MS,
    AELFSCAN_RETRY: process.env.AELFSCAN_RETRY,
    AELFSCAN_RETRY_BASE_MS: process.env.AELFSCAN_RETRY_BASE_MS,
    AELFSCAN_RETRY_MAX_MS: process.env.AELFSCAN_RETRY_MAX_MS,
    AELFSCAN_MAX_CONCURRENT_REQUESTS: process.env.AELFSCAN_MAX_CONCURRENT_REQUESTS,
    AELFSCAN_CACHE_TTL_MS: process.env.AELFSCAN_CACHE_TTL_MS,
    AELFSCAN_CACHE_MAX_ENTRIES: process.env.AELFSCAN_CACHE_MAX_ENTRIES,
    AELFSCAN_MAX_RESULT_COUNT: process.env.AELFSCAN_MAX_RESULT_COUNT,
    AELFSCAN_MCP_MAX_ITEMS: process.env.AELFSCAN_MCP_MAX_ITEMS,
    AELFSCAN_MCP_MAX_CHARS: process.env.AELFSCAN_MCP_MAX_CHARS,
    AELFSCAN_MCP_INCLUDE_RAW: process.env.AELFSCAN_MCP_INCLUDE_RAW,
  };
  resetConfigCache();
});

afterEach(() => {
  restoreEnv(snapshot);
  resetConfigCache();
});

describe('config', () => {
  test('parses env values and normalizes outputs', () => {
    process.env.AELFSCAN_API_BASE_URL = 'https://example.com///';
    process.env.AELFSCAN_DEFAULT_CHAIN_ID = ' multiChain ';
    process.env.AELFSCAN_TIMEOUT_MS = '1234';
    process.env.AELFSCAN_RETRY = '2.9';
    process.env.AELFSCAN_RETRY_BASE_MS = '300';
    process.env.AELFSCAN_RETRY_MAX_MS = '900';
    process.env.AELFSCAN_MAX_CONCURRENT_REQUESTS = '8';
    process.env.AELFSCAN_CACHE_TTL_MS = '5000';
    process.env.AELFSCAN_CACHE_MAX_ENTRIES = '666';
    process.env.AELFSCAN_MAX_RESULT_COUNT = '300';
    process.env.AELFSCAN_MCP_MAX_ITEMS = '80';
    process.env.AELFSCAN_MCP_MAX_CHARS = '80000';
    process.env.AELFSCAN_MCP_INCLUDE_RAW = 'true';

    const config = getConfig();

    expect(config.apiBaseUrl).toBe('https://example.com');
    expect(config.defaultChainId).toBe('');
    expect(config.timeoutMs).toBe(1234);
    expect(config.retry).toBe(2);
    expect(config.retryBaseMs).toBe(300);
    expect(config.retryMaxMs).toBe(900);
    expect(config.maxConcurrentRequests).toBe(8);
    expect(config.cacheTtlMs).toBe(5000);
    expect(config.cacheMaxEntries).toBe(666);
    expect(config.maxResultCount).toBe(300);
    expect(config.mcpMaxItems).toBe(80);
    expect(config.mcpMaxChars).toBe(80000);
    expect(config.mcpIncludeRaw).toBe(true);
  });

  test('falls back on invalid numeric env values', () => {
    process.env.AELFSCAN_TIMEOUT_MS = 'abc';
    process.env.AELFSCAN_RETRY = '-1';
    process.env.AELFSCAN_RETRY_BASE_MS = '-1';
    process.env.AELFSCAN_RETRY_MAX_MS = 'nan';
    process.env.AELFSCAN_MAX_CONCURRENT_REQUESTS = '-10';
    process.env.AELFSCAN_CACHE_TTL_MS = 'oops';
    process.env.AELFSCAN_CACHE_MAX_ENTRIES = '-1';
    process.env.AELFSCAN_MAX_RESULT_COUNT = '-2';
    process.env.AELFSCAN_MCP_MAX_ITEMS = 'oops';
    process.env.AELFSCAN_MCP_MAX_CHARS = '-1';
    process.env.AELFSCAN_MCP_INCLUDE_RAW = 'invalid';

    const config = getConfig();

    expect(config.timeoutMs).toBe(10000);
    expect(config.retry).toBe(1);
    expect(config.retryBaseMs).toBe(200);
    expect(config.retryMaxMs).toBe(3000);
    expect(config.maxConcurrentRequests).toBe(5);
    expect(config.cacheTtlMs).toBe(60000);
    expect(config.cacheMaxEntries).toBe(500);
    expect(config.maxResultCount).toBe(200);
    expect(config.mcpMaxItems).toBe(50);
    expect(config.mcpMaxChars).toBe(60000);
    expect(config.mcpIncludeRaw).toBe(false);
  });

  test('caches config until reset', () => {
    process.env.AELFSCAN_API_BASE_URL = 'https://cache-1.example.com';
    const first = getConfig();

    process.env.AELFSCAN_API_BASE_URL = 'https://cache-2.example.com';
    const second = getConfig();

    expect(second).toBe(first);
    expect(second.apiBaseUrl).toBe('https://cache-1.example.com');

    resetConfigCache();
    const third = getConfig();
    expect(third.apiBaseUrl).toBe('https://cache-2.example.com');
  });
});

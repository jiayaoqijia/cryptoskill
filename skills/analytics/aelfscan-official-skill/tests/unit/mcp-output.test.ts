import { afterEach, beforeEach, describe, expect, test } from 'bun:test';
import { resetConfigCache } from '../../lib/config.js';
import { asMcpResult } from '../../src/mcp/output.js';

const ENV_KEYS = ['AELFSCAN_MCP_MAX_ITEMS', 'AELFSCAN_MCP_MAX_CHARS', 'AELFSCAN_MCP_INCLUDE_RAW'] as const;
type EnvSnapshot = Record<(typeof ENV_KEYS)[number], string | undefined>;

let snapshot: EnvSnapshot;

function restoreEnv(): void {
  ENV_KEYS.forEach((key) => {
    const value = snapshot[key];
    if (value === undefined) {
      delete process.env[key];
    } else {
      process.env[key] = value;
    }
  });
}

beforeEach(() => {
  snapshot = {
    AELFSCAN_MCP_MAX_ITEMS: process.env.AELFSCAN_MCP_MAX_ITEMS,
    AELFSCAN_MCP_MAX_CHARS: process.env.AELFSCAN_MCP_MAX_CHARS,
    AELFSCAN_MCP_INCLUDE_RAW: process.env.AELFSCAN_MCP_INCLUDE_RAW,
  };
  resetConfigCache();
});

afterEach(() => {
  restoreEnv();
  resetConfigCache();
});

describe('mcp output', () => {
  test('truncates long arrays and strips raw by default', () => {
    process.env.AELFSCAN_MCP_MAX_ITEMS = '3';
    process.env.AELFSCAN_MCP_MAX_CHARS = '20000';
    process.env.AELFSCAN_MCP_INCLUDE_RAW = 'false';
    resetConfigCache();

    const result = asMcpResult(
      {
        success: true,
        traceId: 'trace-1',
        data: {
          total: 100,
          list: Array.from({ length: 10 }).map((_, i) => ({ i })),
        },
        raw: { shouldNotAppear: true },
      },
      'summary',
    );

    const text = result.content[0]?.text || '';
    const parsed = JSON.parse(text) as {
      data?: { list?: Array<unknown> };
      raw?: unknown;
      meta?: { truncated?: boolean };
    };

    expect(parsed.raw).toBeUndefined();
    expect(parsed.data?.list?.length).toBe(3);
    expect(parsed.meta?.truncated).toBe(true);
  });

  test('falls back to compact summary when payload exceeds max chars', () => {
    process.env.AELFSCAN_MCP_MAX_ITEMS = '50';
    process.env.AELFSCAN_MCP_MAX_CHARS = '220';
    resetConfigCache();

    const result = asMcpResult({
      success: true,
      traceId: 'trace-2',
      data: {
        hugeText: 'x'.repeat(5000),
      },
    });

    const text = result.content[0]?.text || '';
    const parsed = JSON.parse(text) as {
      dataSummary?: unknown;
      meta?: { truncated?: boolean; maxChars?: number };
    };

    expect(parsed.meta?.truncated).toBe(true);
    expect(parsed.dataSummary).toBeDefined();
    expect(parsed.meta?.maxChars).toBe(220);
  });
});

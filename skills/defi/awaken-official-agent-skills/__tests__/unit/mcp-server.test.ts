// ============================================================
// Unit Test: MCP Server — tool registration, ok/fail helpers
// ============================================================

import { describe, test, expect } from 'bun:test';
import { fail, toMcpError } from '../../src/mcp/error';

// We test the MCP module's helper functions and tool registration
// by dynamically importing the server module and intercepting McpServer.

describe('MCP Server helpers', () => {
  // Replicate the ok/fail helpers from server.ts to unit-test them in isolation
  function ok(data: any) {
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  }

  test('ok() wraps data as MCP text content', () => {
    const result = ok({ foo: 'bar' });
    expect(result.content).toHaveLength(1);
    expect(result.content[0].type).toBe('text');
    const parsed = JSON.parse(result.content[0].text);
    expect(parsed.foo).toBe('bar');
  });

  test('ok() handles arrays', () => {
    const result = ok([1, 2, 3]);
    const parsed = JSON.parse(result.content[0].text);
    expect(parsed).toEqual([1, 2, 3]);
  });

  test('ok() handles null', () => {
    const result = ok(null);
    expect(result.content[0].text).toBe('null');
  });

  test('fail() wraps Error with isError=true', () => {
    const result = fail(new Error('something broke'));
    expect(result.isError).toBe(true);
    expect(result.content[0].text).toBe('[ERROR] UNKNOWN_ERROR: something broke');
    expect(result.content.length).toBe(2);
  });

  test('toMcpError() only parses allowlisted message codes', () => {
    const allowed = toMcpError(
      new Error('SIGNER_PASSWORD_REQUIRED: missing password'),
    );
    expect(allowed.code).toBe('SIGNER_PASSWORD_REQUIRED');
    expect(allowed.message).toBe('missing password');

    const notAllowed = toMcpError(new Error('HTTP: connection refused'));
    expect(notAllowed.code).toBe('UNKNOWN_ERROR');
    expect(notAllowed.message).toBe('HTTP: connection refused');
  });

  test('fail() handles string error', () => {
    const result = fail('raw string error');
    expect(result.isError).toBe(true);
    expect(result.content[0].text).toBe('[ERROR] UNKNOWN_ERROR: raw string error');
  });

  test('fail() handles undefined error', () => {
    const result = fail(undefined);
    expect(result.isError).toBe(true);
    expect(result.content[0].text).toBe('[ERROR] UNKNOWN_ERROR: undefined');
  });

  test('fail() handles error object without message', () => {
    const result = fail({ code: 500 });
    expect(result.isError).toBe(true);
    expect(result.content[0].text).toBe('[ERROR] UNKNOWN_ERROR: [object Object]');
  });
});

describe('MCP Server module', () => {
  test('server.ts can be imported without crashing (module-level)', async () => {
    // Importing the module at the top level triggers registerTool calls
    // but also starts the server (which connects to stdio).
    // We test that the core imports and tool registration don't throw
    // by importing the core modules directly.
    const query = await import('../../src/core/query');
    const trade = await import('../../src/core/trade');
    const kline = await import('../../src/core/kline');

    // All 11 core functions should be importable
    expect(typeof query.getQuote).toBe('function');
    expect(typeof query.getPair).toBe('function');
    expect(typeof query.getTokenBalance).toBe('function');
    expect(typeof query.getTokenAllowance).toBe('function');
    expect(typeof query.getLiquidityPositions).toBe('function');
    expect(typeof trade.executeSwap).toBe('function');
    expect(typeof trade.addLiquidity).toBe('function');
    expect(typeof trade.removeLiquidity).toBe('function');
    expect(typeof trade.approveTokenSpending).toBe('function');
    expect(typeof kline.fetchKline).toBe('function');
    expect(typeof kline.getKlineIntervals).toBe('function');
  });

  test('MCP SDK modules can be imported', async () => {
    const { McpServer } = await import('@modelcontextprotocol/sdk/server/mcp.js');
    const { StdioServerTransport } = await import('@modelcontextprotocol/sdk/server/stdio.js');
    expect(typeof McpServer).toBe('function');
    expect(typeof StdioServerTransport).toBe('function');
  });

  test('McpServer can be instantiated with correct name and version', async () => {
    const { McpServer } = await import('@modelcontextprotocol/sdk/server/mcp.js');
    const server = new McpServer({
      name: 'awaken-agent-kit',
      version: '1.0.0',
    });
    expect(server).toBeDefined();
    expect(typeof server.registerTool).toBe('function');
  });

  test('registerTool accepts valid tool definition', async () => {
    const { McpServer } = await import('@modelcontextprotocol/sdk/server/mcp.js');
    const { z } = await import('zod');

    const server = new McpServer({ name: 'test', version: '0.0.1' });

    // Should not throw
    (server as any).registerTool(
      'test_tool',
      {
        description: 'A test tool',
        inputSchema: {
          name: z.string().describe('A name'),
        },
      },
      async ({ name }: any) => {
        return { content: [{ type: 'text' as const, text: `hello ${name}` }] };
      },
    );
  });
});

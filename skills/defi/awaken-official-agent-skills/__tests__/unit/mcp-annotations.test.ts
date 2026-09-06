import { describe, expect, test } from 'bun:test';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

const READ_TOOLS = [
  'awaken_quote',
  'awaken_pair',
  'awaken_balance',
  'awaken_allowance',
  'awaken_liquidity',
  'awaken_kline_fetch',
  'awaken_kline_intervals',
];

const WRITE_TOOLS = [
  'awaken_swap',
  'awaken_add_liquidity',
  'awaken_remove_liquidity',
  'awaken_approve',
];

describe('MCP tool annotations', () => {
  test('read and network write tools expose the expected annotations', async () => {
    const transport = new StdioClientTransport({
      command: 'bun',
      args: ['run', 'src/mcp/server.ts'],
      cwd: process.cwd(),
    });
    const client = new Client(
      {
        name: 'awaken-annotations-test',
        version: '1.0.0',
      },
      {
        capabilities: {},
      },
    );

    try {
      await client.connect(transport);
      const result = await client.listTools();

      READ_TOOLS.forEach(name => {
        const tool = result.tools.find(item => item.name === name);
        expect(tool?.annotations?.readOnlyHint).toBe(true);
        expect(tool?.annotations?.destructiveHint).not.toBe(true);
      });

      WRITE_TOOLS.forEach(name => {
        const tool = result.tools.find(item => item.name === name);
        expect(tool?.annotations?.destructiveHint).toBe(true);
        expect(tool?.annotations?.openWorldHint).toBe(true);
      });
    } finally {
      await client.close();
    }
  });
});

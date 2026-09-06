import { describe, expect, test } from 'bun:test';
import {
  IRONCLAW_CONFIG_SCHEMA_VERSION,
  generateIronclawServerEntry,
  mergeIronclawMcpConfig,
  removeIronclawMcpConfig,
} from '../../bin/platforms/ironclaw';

describe('IronClaw MCP config helpers', () => {
  test('generates a stdio MCP server entry with placeholder secrets', () => {
    const entry = generateIronclawServerEntry('/custom/server.ts');

    expect(entry.name).toBe('awaken-agent-kit');
    expect(entry.transport.transport).toBe('stdio');
    expect(entry.transport.command).toBeString();
    expect(entry.transport.args).toEqual(['run', '/custom/server.ts']);
    expect(entry.transport.env).toEqual({
      AELF_PRIVATE_KEY: '<YOUR_PRIVATE_KEY>',
      AWAKEN_NETWORK: 'mainnet',
    });
  });

  test('merges config using schema_version=1 and preserves unrelated servers', () => {
    const existing = {
      schema_version: 1,
      servers: [
        {
          name: 'existing-server',
          url: 'https://example.invalid',
          transport: { transport: 'http' },
          enabled: true,
          headers: {},
        },
      ],
    };

    const { config, action } = mergeIronclawMcpConfig(
      existing,
      generateIronclawServerEntry('/new/server.ts'),
      false,
    );

    expect(action).toBe('created');
    expect(config.schema_version).toBe(IRONCLAW_CONFIG_SCHEMA_VERSION);
    expect(config.servers).toHaveLength(2);
    expect(config.servers.map(server => server.name)).toEqual(
      expect.arrayContaining(['existing-server', 'awaken-agent-kit']),
    );
  });

  test('upserts same-name server instead of duplicating entries', () => {
    const existing = {
      schema_version: 1,
      servers: [generateIronclawServerEntry('/old/server.ts')],
    };

    const { config, action } = mergeIronclawMcpConfig(
      existing,
      generateIronclawServerEntry('/new/server.ts'),
      true,
    );

    expect(action).toBe('updated');
    expect(config.servers).toHaveLength(1);
    expect(config.servers[0]?.transport.args).toEqual(['run', '/new/server.ts']);
  });

  test('removes the configured IronClaw MCP server by name', () => {
    const existing = {
      schema_version: 1,
      servers: [generateIronclawServerEntry('/server.ts')],
    };

    const { config, removed } = removeIronclawMcpConfig(existing, 'awaken-agent-kit');

    expect(removed).toBe(true);
    expect(config.servers).toHaveLength(0);
    expect(config.schema_version).toBe(IRONCLAW_CONFIG_SCHEMA_VERSION);
  });
});

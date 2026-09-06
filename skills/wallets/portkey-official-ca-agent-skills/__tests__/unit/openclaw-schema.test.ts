import { describe, expect, test } from 'bun:test';
import * as fs from 'node:fs';
import * as path from 'node:path';

type OpenClawTool = {
  name: string;
  args: string[];
  inputSchema?: {
    properties?: Record<string, unknown>;
    required?: string[];
  };
};

type OpenClawConfig = {
  tools: OpenClawTool[];
};

const EXACT_SCHEMA_EXPECTATIONS: Record<string, { properties: string[]; required: string[] }> = {
  'portkey-query-check-account': {
    properties: ['email'],
    required: ['email'],
  },
  'portkey-query-guardian-list': {
    properties: ['identifier', 'chain-id'],
    required: ['identifier', 'chain-id'],
  },
  'portkey-query-prepare-auth-flow': {
    properties: ['email', 'chain-id'],
    required: ['email'],
  },
  'portkey-auth-send-code': {
    properties: ['email', 'verifier-id', 'operation', 'chain-id'],
    required: ['email', 'verifier-id', 'operation', 'chain-id'],
  },
  'portkey-auth-verify-code': {
    properties: ['email', 'code', 'verifier-id', 'session-id', 'operation', 'chain-id'],
    required: ['email', 'code', 'verifier-id', 'session-id', 'operation', 'chain-id'],
  },
  'portkey-auth-recover': {
    properties: ['email', 'manager', 'guardians-approved', 'chain-id'],
    required: ['email', 'manager', 'guardians-approved', 'chain-id'],
  },
  'portkey-query-token-list': {
    properties: ['ca-address-infos', 'strategy'],
    required: ['ca-address-infos'],
  },
  'portkey-query-nft-collections': {
    properties: ['ca-address-infos'],
    required: ['ca-address-infos'],
  },
};

function readOpenclaw(): OpenClawConfig {
  const filePath = path.resolve(import.meta.dir, '../../openclaw.json');
  const content = fs.readFileSync(filePath, 'utf8');
  return JSON.parse(content) as OpenClawConfig;
}

function sortedUnique(values: string[]): string[] {
  return [...new Set(values)].sort();
}

function schemaProperties(tool: OpenClawTool): string[] {
  return sortedUnique(Object.keys(tool.inputSchema?.properties || {}));
}

function schemaRequired(tool: OpenClawTool): string[] {
  return sortedUnique((tool.inputSchema?.required || []).map(String));
}

describe('openclaw schema guards', () => {
  test('key tools keep exact inputSchema properties/required', () => {
    const config = readOpenclaw();
    const toolsByName = new Map(config.tools.map((tool) => [tool.name, tool]));

    for (const [toolName, expected] of Object.entries(EXACT_SCHEMA_EXPECTATIONS)) {
      const tool = toolsByName.get(toolName);
      expect(tool).toBeDefined();
      if (!tool) continue;

      expect(schemaProperties(tool)).toEqual(sortedUnique(expected.properties));
      expect(schemaRequired(tool)).toEqual(sortedUnique(expected.required));
    }
  });

  test('inputSchema keys are aligned with tool args', () => {
    const config = readOpenclaw();

    for (const tool of config.tools) {
      const flags = sortedUnique(
        (tool.args || [])
          .filter((arg) => typeof arg === 'string' && arg.startsWith('--'))
          .map((arg) => arg.slice(2)),
      );
      const properties = schemaProperties(tool);
      const required = schemaRequired(tool);

      const unknownProperties = properties.filter((key) => !flags.includes(key));
      expect(unknownProperties).toEqual([]);

      const invalidRequired = required.filter((key) => !properties.includes(key));
      expect(invalidRequired).toEqual([]);
    }
  });
});

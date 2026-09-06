#!/usr/bin/env bun
import * as fs from 'node:fs';
import * as path from 'node:path';

type JsonValue = string | number | boolean | null | JsonValue[] | { [key: string]: JsonValue };

type JsonObject = { [key: string]: JsonValue };

type OpenClawParameter = {
  type?: string;
  required?: boolean;
  description?: string;
  default?: JsonValue;
};

type OpenClawTool = {
  name: string;
  description: string;
  command: string;
  args: string[];
  cwd: string;
  inputSchema: JsonObject;
};

type SchemaExpectation = {
  properties: string[];
  required: string[];
};

const EXACT_SCHEMA_EXPECTATIONS: Record<string, SchemaExpectation> = {
  'portkey-query-check-account': {
    properties: ['email'],
    required: ['email'],
  },
  'portkey-query-guardian-list': {
    properties: ['identifier', 'chain-id'],
    required: ['identifier', 'chain-id'],
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

function readJson(filePath: string): JsonObject {
  const content = fs.readFileSync(filePath, 'utf8');
  return JSON.parse(content) as JsonObject;
}

function buildSchemaFromParameters(parameters: JsonObject | undefined): JsonObject | undefined {
  if (!parameters) return undefined;

  const properties: Record<string, JsonObject> = {};
  const required: string[] = [];

  for (const [key, raw] of Object.entries(parameters)) {
    const param = (raw || {}) as OpenClawParameter;
    const prop: JsonObject = {
      type: typeof param.type === 'string' ? param.type : 'string',
      description:
        typeof param.description === 'string'
          ? param.description
          : `${key} parameter`,
    };

    if (param.default !== undefined) {
      prop.default = param.default;
    }

    properties[key] = prop;

    if (param.required) {
      required.push(key);
    }
  }

  const schema: JsonObject = {
    type: 'object',
    properties,
    additionalProperties: true,
  };

  if (required.length > 0) {
    schema.required = required;
  }

  return schema;
}

function uniqueSorted(values: string[]): string[] {
  return [...new Set(values)].sort();
}

function toStringArray(value: JsonValue | undefined): string[] {
  if (!Array.isArray(value)) return [];
  return uniqueSorted(value.map((item) => String(item)));
}

function toJsonObject(value: JsonValue | undefined): JsonObject | undefined {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return undefined;
  return value as JsonObject;
}

function getSchemaProperties(schema: JsonObject): string[] {
  const properties = toJsonObject(schema.properties);
  if (!properties) return [];
  return uniqueSorted(Object.keys(properties));
}

function getSchemaRequired(schema: JsonObject): string[] {
  return toStringArray(schema.required);
}

function getFlagArgs(args: string[]): string[] {
  return uniqueSorted(args.filter((arg) => arg.startsWith('--')).map((arg) => arg.slice(2)));
}

function sameStringSet(a: string[], b: string[]): boolean {
  if (a.length !== b.length) return false;
  return a.every((value, idx) => value === b[idx]);
}

function formatSet(values: string[]): string {
  if (values.length === 0) return '(none)';
  return values.join(', ');
}

function validateOpenclawSchemas(tools: OpenClawTool[]): void {
  const toolsByName = new Map(tools.map((tool) => [tool.name, tool]));

  for (const [toolName, expected] of Object.entries(EXACT_SCHEMA_EXPECTATIONS)) {
    const tool = toolsByName.get(toolName);
    if (!tool) {
      throw new Error(
        `[ERROR] Missing expected OpenClaw tool "${toolName}".`,
      );
    }

    const expectedProperties = uniqueSorted(expected.properties);
    const expectedRequired = uniqueSorted(expected.required);
    const actualProperties = getSchemaProperties(tool.inputSchema);
    const actualRequired = getSchemaRequired(tool.inputSchema);

    if (!sameStringSet(actualProperties, expectedProperties)) {
      throw new Error(
        `[ERROR] OpenClaw exact schema mismatch for "${toolName}". ` +
        `Expected properties: [${formatSet(expectedProperties)}]; actual: [${formatSet(actualProperties)}].`,
      );
    }
    if (!sameStringSet(actualRequired, expectedRequired)) {
      throw new Error(
        `[ERROR] OpenClaw exact schema mismatch for "${toolName}". ` +
        `Expected required: [${formatSet(expectedRequired)}]; actual: [${formatSet(actualRequired)}].`,
      );
    }
  }

  for (const tool of tools) {
    const properties = getSchemaProperties(tool.inputSchema);
    const required = getSchemaRequired(tool.inputSchema);
    const flagArgs = getFlagArgs(tool.args);
    const argSet = new Set(flagArgs);
    const propertySet = new Set(properties);

    const unknownProperties = properties.filter((key) => !argSet.has(key));
    if (unknownProperties.length > 0) {
      throw new Error(
        `[ERROR] OpenClaw schema keys must be declared in args for "${tool.name}". ` +
        `Unknown properties: [${formatSet(unknownProperties)}]. Declared flag args: [${formatSet(flagArgs)}].`,
      );
    }

    const invalidRequired = required.filter((key) => !propertySet.has(key));
    if (invalidRequired.length > 0) {
      throw new Error(
        `[ERROR] OpenClaw required keys must be included in inputSchema.properties for "${tool.name}". ` +
        `Invalid required: [${formatSet(invalidRequired)}]. Properties: [${formatSet(properties)}].`,
      );
    }
  }
}

function normalizeCommand(tool: JsonObject): { command: string; args: string[] } {
  const rawCommand = tool.command;
  const rawArgs = tool.args;

  if (typeof rawCommand !== 'string' || rawCommand.trim().length === 0) {
    throw new Error(`Tool ${String(tool.name)} missing command`);
  }

  if (Array.isArray(rawArgs)) {
    return {
      command: rawCommand,
      args: rawArgs.map((v) => String(v)),
    };
  }

  if (rawCommand.includes(' ')) {
    return {
      command: 'sh',
      args: ['-lc', rawCommand],
    };
  }

  return {
    command: rawCommand,
    args: [],
  };
}

function normalizeTool(rawTool: JsonObject): OpenClawTool {
  const { command, args } = normalizeCommand(rawTool);
  const inputSchema =
    (rawTool.inputSchema as JsonObject | undefined) ||
    buildSchemaFromParameters(rawTool.parameters as JsonObject | undefined) || {
      type: 'object',
      properties: {},
      additionalProperties: true,
    };

  return {
    name: String(rawTool.name || ''),
    description: String(rawTool.description || ''),
    command,
    args,
    cwd: String(rawTool.cwd || rawTool.working_directory || '.'),
    inputSchema,
  };
}

function normalizeOpenclaw(raw: JsonObject, pkg: JsonObject): JsonObject {
  const rawTools = Array.isArray(raw.tools)
    ? (raw.tools as JsonObject[])
    : Array.isArray(raw.skills)
      ? (raw.skills as JsonObject[])
      : [];

  if (rawTools.length === 0) {
    throw new Error('No tools/skills found in openclaw.json');
  }

  const tools = rawTools.map(normalizeTool);
  validateOpenclawSchemas(tools);

  return {
    name: typeof raw.name === 'string' ? raw.name : String(pkg.name || 'skill-openclaw'),
    description:
      typeof raw.description === 'string'
        ? raw.description
        : String(pkg.description || 'OpenClaw tool config'),
    tools,
  };
}

const packageRoot = path.resolve(import.meta.dir, '..');
const targetPath = path.join(packageRoot, 'openclaw.json');
const packageJsonPath = path.join(packageRoot, 'package.json');

const raw = readJson(targetPath);
const pkg = readJson(packageJsonPath);
const normalized = normalizeOpenclaw(raw, pkg);
const serialized = `${JSON.stringify(normalized, null, 2)}\n`;
const checkMode = process.argv.includes('--check');

if (checkMode) {
  const existing = fs.readFileSync(targetPath, 'utf8');
  if (existing !== serialized) {
    process.stderr.write('[ERROR] openclaw.json is out of date. Run `bun run build:openclaw`\n');
    process.exit(1);
  }

  process.stdout.write('[OK] openclaw.json is up to date\n');
  process.exit(0);
}

fs.writeFileSync(targetPath, serialized, 'utf8');
process.stdout.write(`[OK] Generated ${targetPath} with ${(normalized.tools as JsonObject[]).length} tools\n`);

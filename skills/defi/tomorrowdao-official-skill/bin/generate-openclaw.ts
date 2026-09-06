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

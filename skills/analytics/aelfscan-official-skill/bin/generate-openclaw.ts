#!/usr/bin/env bun
import * as fs from 'node:fs';
import * as path from 'node:path';
import { OPENCLAW_TOOL_DESCRIPTORS } from '../src/tooling/tool-descriptors.js';

const packageRoot = path.resolve(import.meta.dir, '..');
const targetPath = path.join(packageRoot, 'openclaw.json');

const openclaw = {
  name: 'aelfscan-skill',
  description: 'AelfScan explorer tools for search, blockchain, addresses, tokens, NFTs, and statistics.',
  tools: OPENCLAW_TOOL_DESCRIPTORS.map(descriptor => ({
    name: descriptor.mcpName,
    description: descriptor.description,
    command: 'bun',
    args: ['run', 'aelfscan_skill.ts', descriptor.domain, descriptor.action],
    cwd: '.',
    inputSchema: {
      type: 'object',
      properties: {},
      additionalProperties: true,
    },
  })),
};

const serialized = `${JSON.stringify(openclaw, null, 2)}\n`;
const checkMode = process.argv.includes('--check');

if (checkMode) {
  if (!fs.existsSync(targetPath)) {
    process.stderr.write(`[ERROR] ${targetPath} does not exist\n`);
    process.exit(1);
  }

  const existing = fs.readFileSync(targetPath, 'utf-8');
  if (existing !== serialized) {
    process.stderr.write('[ERROR] openclaw.json is out of date. Run `bun run build:openclaw`\n');
    process.exit(1);
  }

  process.stdout.write('[OK] openclaw.json is up to date\n');
  process.exit(0);
}

fs.writeFileSync(targetPath, serialized, 'utf-8');
process.stdout.write(`[OK] Generated ${targetPath} with ${openclaw.tools.length} tools\n`);

import * as fs from 'node:fs';
import * as path from 'node:path';
import { LOG, getPackageRoot, readJsonFile, writeJsonFile } from './utils.js';

interface OpenClawTool {
  name: string;
  description?: string;
  command?: string;
  args?: string[];
  cwd?: string;
  [key: string]: unknown;
}

function getSourceFilePath(): string {
  return path.join(getPackageRoot(), 'openclaw.json');
}

function loadSourceTools(): OpenClawTool[] {
  const sourcePath = getSourceFilePath();
  if (!fs.existsSync(sourcePath)) {
    throw new Error(`openclaw.json not found at ${sourcePath}`);
  }

  const source = readJsonFile(sourcePath);
  const tools = Array.isArray(source.tools) ? source.tools : [];
  if (!tools.length) {
    throw new Error('No tools found in openclaw.json');
  }

  return tools;
}

export function setupOpenClaw(opts: { configPath?: string; cwd?: string; force?: boolean }): boolean {
  let tools: OpenClawTool[];
  try {
    tools = loadSourceTools();
  } catch (error) {
    LOG.error((error as Error).message);
    return false;
  }

  const resolvedCwd = opts.cwd || getPackageRoot();
  const normalizedTools = tools.map(tool => ({
    ...tool,
    cwd: resolvedCwd,
  }));

  if (!opts.configPath) {
    const outputPath = path.join(process.cwd(), 'aelfscan-openclaw.json');
    writeJsonFile(outputPath, { tools: normalizedTools });
    LOG.success(`Generated standalone OpenClaw config: ${outputPath}`);
    LOG.info(`Tools count: ${normalizedTools.length}; cwd=${resolvedCwd}`);
    return true;
  }

  LOG.step(`Merging ${normalizedTools.length} tools into: ${opts.configPath}`);

  const existing = readJsonFile(opts.configPath);
  if (!Array.isArray(existing.tools)) {
    existing.tools = [];
  }

  let added = 0;
  let updated = 0;

  for (const tool of normalizedTools) {
    const index = existing.tools.findIndex((item: OpenClawTool) => item.name === tool.name);
    if (index >= 0) {
      if (opts.force) {
        existing.tools[index] = tool;
        updated += 1;
      }
      continue;
    }

    existing.tools.push(tool);
    added += 1;
  }

  writeJsonFile(opts.configPath, existing);
  LOG.success(`OpenClaw config updated: ${added} added, ${updated} updated.`);
  return true;
}

export function uninstallOpenClaw(opts: { configPath?: string }): boolean {
  if (!opts.configPath) {
    LOG.info('Provide --config-path to remove tools from an existing OpenClaw config.');
    return false;
  }

  let toolNames: Set<string>;
  try {
    toolNames = new Set(loadSourceTools().map(tool => tool.name));
  } catch (error) {
    LOG.error((error as Error).message);
    return false;
  }

  const existing = readJsonFile(opts.configPath);
  if (!Array.isArray(existing.tools)) {
    LOG.info('No tools found in target OpenClaw config.');
    return false;
  }

  const before = existing.tools.length;
  existing.tools = existing.tools.filter((tool: OpenClawTool) => !toolNames.has(tool.name));
  const removed = before - existing.tools.length;

  if (removed <= 0) {
    LOG.info('No aelfscan-skill tools found in target OpenClaw config.');
    return false;
  }

  writeJsonFile(opts.configPath, existing);
  LOG.success(`Removed ${removed} aelfscan-skill tools from OpenClaw config.`);
  return true;
}

// ============================================================
// Setup: OpenClaw — register tools from openclaw.json
// ============================================================

import * as path from 'path';
import * as fs from 'fs';
import { getPackageRoot, readJsonFile, writeJsonFile, LOG } from './utils';

export function setupOpenClaw(opts: {
  configPath?: string;
  cwd?: string;
  force?: boolean;
}): boolean {
  const packageRoot = getPackageRoot();
  const sourceFile = path.join(packageRoot, 'openclaw.json');

  if (!fs.existsSync(sourceFile)) {
    LOG.error(`openclaw.json not found at ${sourceFile}`);
    return false;
  }

  const source = readJsonFile(sourceFile);
  const tools: any[] = source.tools || [];

  if (!tools.length) {
    LOG.error('No tools found in openclaw.json');
    return false;
  }

  // Resolve cwd for all tools — use explicit cwd, or package root
  const resolvedCwd = opts.cwd || packageRoot;

  // Update tools with resolved cwd
  const updatedTools = tools.map((tool: any) => ({
    ...tool,
    cwd: resolvedCwd,
  }));

  // If user specified a target config path, merge into it
  if (opts.configPath) {
    LOG.step(`Merging ${tools.length} tools into: ${opts.configPath}`);

    const existing = readJsonFile(opts.configPath);
    if (!existing.tools) existing.tools = [];

    // Merge: replace existing tools with same name, add new ones
    const existingNames = new Set(existing.tools.map((t: any) => t.name));
    let added = 0;
    let updated = 0;

    for (const tool of updatedTools) {
      const idx = existing.tools.findIndex((t: any) => t.name === tool.name);
      if (idx >= 0) {
        if (opts.force) {
          existing.tools[idx] = tool;
          updated++;
        }
        // skip if not forced
      } else {
        existing.tools.push(tool);
        added++;
      }
    }

    writeJsonFile(opts.configPath, existing);
    LOG.success(`OpenClaw config updated: ${added} added, ${updated} updated.`);
  } else {
    // No target path: generate a standalone config file in current dir
    const outPath = path.join(process.cwd(), 'awaken-openclaw.json');
    LOG.step(`Generating OpenClaw config: ${outPath}`);
    LOG.step(`Tool cwd: ${resolvedCwd}`);

    writeJsonFile(outPath, { tools: updatedTools });
    LOG.success(`OpenClaw config generated: ${outPath}`);
    LOG.info(`Contains ${updatedTools.length} tools with cwd set to: ${resolvedCwd}`);
    LOG.info('Import this file into your OpenClaw configuration.');
  }

  return true;
}

export function uninstallOpenClaw(opts: { configPath?: string }): boolean {
  if (!opts.configPath) {
    LOG.info('OpenClaw: no --config-path specified. Remove tools manually from your OpenClaw config.');
    return false;
  }

  const existing = readJsonFile(opts.configPath);
  if (!existing.tools?.length) {
    LOG.info('No tools found in config.');
    return false;
  }

  const awakenToolNames = new Set([
    'awaken-query-quote', 'awaken-query-pair', 'awaken-query-balance',
    'awaken-query-allowance', 'awaken-query-liquidity',
    'awaken-trade-swap', 'awaken-trade-add-liquidity',
    'awaken-trade-remove-liquidity', 'awaken-trade-approve',
    'awaken-kline-fetch', 'awaken-kline-intervals',
  ]);

  const before = existing.tools.length;
  existing.tools = existing.tools.filter((t: any) => !awakenToolNames.has(t.name));
  const removed = before - existing.tools.length;

  if (removed === 0) {
    LOG.info('No Awaken tools found in config.');
    return false;
  }

  writeJsonFile(opts.configPath, existing);
  LOG.success(`Removed ${removed} Awaken tools from OpenClaw config.`);
  return true;
}

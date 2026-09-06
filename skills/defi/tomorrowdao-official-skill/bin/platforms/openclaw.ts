import * as fs from 'fs';
import * as path from 'path';
import { getPackageRoot, readJsonFile, writeJsonFile } from './utils.js';

export function setupOpenclaw(opts: { configPath?: string; cwd?: string; force?: boolean }) {
  const pkgRoot = getPackageRoot();
  const openclawPath = path.join(pkgRoot, 'openclaw.json');
  if (!fs.existsSync(openclawPath)) {
    console.log('[ERROR] openclaw.json not found in package root');
    return;
  }

  const src = readJsonFile(openclawPath);
  if (opts.cwd && Array.isArray(src.tools)) {
    src.tools.forEach((tool: any) => {
      if (tool.cwd) tool.cwd = opts.cwd;
    });
  }

  if (!opts.configPath) {
    console.log(JSON.stringify(src, null, 2));
    return;
  }

  const target = readJsonFile(opts.configPath);
  if (!Array.isArray(target.tools)) target.tools = [];

  const existingNames = new Set(target.tools.map((t: any) => t.name));
  let added = 0;

  for (const tool of src.tools || []) {
    if (existingNames.has(tool.name) && !opts.force) continue;
    target.tools = target.tools.filter((t: any) => t.name !== tool.name);
    target.tools.push(tool);
    added += 1;
  }

  writeJsonFile(opts.configPath, target);
  console.log(`[DONE] merged ${added} tools into ${opts.configPath}`);
}

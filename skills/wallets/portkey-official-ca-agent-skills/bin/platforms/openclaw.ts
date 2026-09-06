import * as path from 'path';
import * as fs from 'fs';
import { getPackageRoot, readJsonFile, writeJsonFile } from './utils.js';

export interface OpenClawSetupOptions {
  configPath?: string;
  cwd?: string;
  force?: boolean;
}

export function setupOpenClaw(options: OpenClawSetupOptions = {}): void {
  const packageRoot = getPackageRoot();
  const openclawSource = path.join(packageRoot, 'openclaw.json');

  if (!fs.existsSync(openclawSource)) {
    console.log('[ERROR] openclaw.json not found at', openclawSource);
    console.log('        Please create it first.');
    return;
  }

  const sourceConfig = readJsonFile(openclawSource);

  // Replace cwd placeholders if needed
  const cwd = options.cwd || packageRoot;

  if (options.configPath) {
    // Merge into existing config
    const existing = readJsonFile(options.configPath);
    const merged = {
      ...existing,
      tools: [...((existing.tools as unknown[]) || []), ...((sourceConfig.tools as unknown[]) || [])],
    };
    writeJsonFile(options.configPath, merged);
    console.log(`[MERGED] OpenClaw tools into ${options.configPath}`);
  } else {
    // Output to stdout for piping
    console.log(JSON.stringify({ ...sourceConfig, cwd }, null, 2));
  }
}

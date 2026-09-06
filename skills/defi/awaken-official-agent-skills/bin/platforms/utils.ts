// ============================================================
// Setup Utilities — path detection, JSON merge, cross-platform
// ============================================================

import * as os from 'os';
import * as path from 'path';
import * as fs from 'fs';

// ---- Package root detection ----

/** Resolve the absolute path to this package's root directory */
export function getPackageRoot(): string {
  // import.meta.dir points to bin/platforms/ — go up 2 levels
  return path.resolve(import.meta.dir, '..', '..');
}

/** Resolve the absolute path to the MCP server.ts */
export function getMcpServerPath(): string {
  return path.join(getPackageRoot(), 'src', 'mcp', 'server.ts');
}

/** Detect bun executable path */
export function getBunPath(): string {
  const platform = os.platform();
  try {
    const cmd = platform === 'win32' ? 'where bun' : 'which bun';
    const result = Bun.spawnSync(cmd.split(' '));
    const stdout = result.stdout.toString().trim();
    if (stdout) return stdout.split('\n')[0].trim();
  } catch {}
  // Fallback
  return 'bun';
}

// ---- Platform config paths ----

export interface PlatformPaths {
  claude: string;
  cursorGlobal: string;
}

export function getPlatformPaths(): PlatformPaths {
  const home = os.homedir();
  const platform = os.platform();

  let claude: string;
  if (platform === 'darwin') {
    claude = path.join(home, 'Library', 'Application Support', 'Claude', 'claude_desktop_config.json');
  } else if (platform === 'win32') {
    claude = path.join(process.env.APPDATA || path.join(home, 'AppData', 'Roaming'), 'Claude', 'claude_desktop_config.json');
  } else {
    claude = path.join(home, '.config', 'Claude', 'claude_desktop_config.json');
  }

  const cursorGlobal = path.join(home, '.cursor', 'mcp.json');

  return { claude, cursorGlobal };
}

export function getCursorProjectPath(projectDir?: string): string {
  const dir = projectDir || process.cwd();
  return path.join(dir, '.cursor', 'mcp.json');
}

// ---- JSON file operations (safe merge) ----

/** Read a JSON file, return empty object if not exists or invalid */
export function readJsonFile(filePath: string): any {
  try {
    if (!fs.existsSync(filePath)) return {};
    const content = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(content);
  } catch {
    return {};
  }
}

/** Write JSON to file, creating parent dirs if needed */
export function writeJsonFile(filePath: string, data: any): void {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2) + '\n', 'utf-8');
}

// ---- MCP config generation ----

export interface McpServerEntry {
  command: string;
  args: string[];
  env: Record<string, string>;
}

export function generateMcpEntry(customPath?: string): McpServerEntry {
  const serverPath = customPath || getMcpServerPath();
  return {
    command: getBunPath(),
    args: ['run', serverPath],
    env: {
      AELF_PRIVATE_KEY: '<YOUR_PRIVATE_KEY>',
      AWAKEN_NETWORK: 'mainnet',
    },
  };
}

/** Merge our MCP server entry into an existing config, returns { config, action } */
export function mergeMcpConfig(
  existing: any,
  serverName: string,
  entry: McpServerEntry,
  force: boolean = false,
): { config: any; action: 'created' | 'updated' | 'skipped' } {
  const config = { ...existing };
  if (!config.mcpServers) config.mcpServers = {};

  if (config.mcpServers[serverName] && !force) {
    return { config, action: 'skipped' };
  }

  const action = config.mcpServers[serverName] ? 'updated' : 'created';
  config.mcpServers[serverName] = entry;
  return { config, action };
}

/** Remove our MCP server entry from config */
export function removeMcpEntry(existing: any, serverName: string): { config: any; removed: boolean } {
  const config = { ...existing };
  if (!config.mcpServers || !config.mcpServers[serverName]) {
    return { config, removed: false };
  }
  delete config.mcpServers[serverName];
  return { config, removed: true };
}

// ---- Console output helpers ----

export const LOG = {
  success: (msg: string) => console.log(`  ✅ ${msg}`),
  info: (msg: string) => console.log(`  ℹ️  ${msg}`),
  warn: (msg: string) => console.log(`  ⚠️  ${msg}`),
  error: (msg: string) => console.error(`  ❌ ${msg}`),
  step: (msg: string) => console.log(`  → ${msg}`),
};

export const SERVER_NAME = 'awaken-agent-kit';

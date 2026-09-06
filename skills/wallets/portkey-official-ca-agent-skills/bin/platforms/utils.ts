import * as os from 'os';
import * as path from 'path';
import * as fs from 'fs';

// ---------------------------------------------------------------------------
// Package root detection
// ---------------------------------------------------------------------------

/** Get the root of this package (bin/platforms/ → ../..) */
export function getPackageRoot(): string {
  return path.resolve(import.meta.dir, '..', '..');
}

/** Get the absolute path to the MCP server entry point. */
export function getMcpServerPath(): string {
  return path.join(getPackageRoot(), 'src', 'mcp', 'server.ts');
}

// ---------------------------------------------------------------------------
// Bun detection
// ---------------------------------------------------------------------------

/** Detect the bun executable path. */
export function getBunPath(): string {
  try {
    const cmd = os.platform() === 'win32' ? 'where bun' : 'which bun';
    const result = Bun.spawnSync(cmd.split(' '));
    const stdout = result.stdout.toString().trim();
    if (stdout) return stdout.split('\n')[0].trim();
  } catch {
    // fallback
  }
  return 'bun';
}

// ---------------------------------------------------------------------------
// Platform-specific config paths
// ---------------------------------------------------------------------------

export function getPlatformPaths() {
  const home = os.homedir();
  const p = os.platform();

  let claude: string;
  if (p === 'darwin') {
    claude = path.join(home, 'Library', 'Application Support', 'Claude', 'claude_desktop_config.json');
  } else if (p === 'win32') {
    claude = path.join(
      process.env.APPDATA || path.join(home, 'AppData', 'Roaming'),
      'Claude',
      'claude_desktop_config.json',
    );
  } else {
    claude = path.join(home, '.config', 'Claude', 'claude_desktop_config.json');
  }

  return {
    claude,
    cursorGlobal: path.join(home, '.cursor', 'mcp.json'),
    cursorProject: path.join(process.cwd(), '.cursor', 'mcp.json'),
  };
}

// ---------------------------------------------------------------------------
// JSON safe read/write
// ---------------------------------------------------------------------------

export function readJsonFile(filePath: string): Record<string, unknown> {
  try {
    if (fs.existsSync(filePath)) {
      return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    }
  } catch {
    // corrupted file — treat as empty
  }
  return {};
}

/** Restricted system directories that should never be written to. */
const FORBIDDEN_PREFIXES = ['/etc', '/usr', '/bin', '/sbin', '/var', '/boot', '/sys', '/proc'];

export function writeJsonFile(filePath: string, data: unknown): void {
  const resolved = path.resolve(filePath);

  // Guard: only allow .json files
  if (!resolved.endsWith('.json')) {
    throw new Error(`writeJsonFile only writes .json files, got: ${resolved}`);
  }

  // Guard: block system directories
  for (const prefix of FORBIDDEN_PREFIXES) {
    if (resolved.startsWith(prefix + '/') || resolved === prefix) {
      throw new Error(`Refusing to write to system directory: ${resolved}`);
    }
  }

  const dir = path.dirname(resolved);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(resolved, JSON.stringify(data, null, 2) + '\n', 'utf-8');
}

// ---------------------------------------------------------------------------
// MCP config merge (never overwrites other servers)
// ---------------------------------------------------------------------------

export function mergeMcpConfig(
  existing: Record<string, unknown>,
  serverName: string,
  entry: unknown,
  force = false,
): { config: Record<string, unknown>; action: 'created' | 'updated' | 'skipped' } {
  const config = { ...existing };
  if (!config.mcpServers || typeof config.mcpServers !== 'object') {
    config.mcpServers = {};
  }
  const servers = config.mcpServers as Record<string, unknown>;

  if (servers[serverName] && !force) {
    return { config, action: 'skipped' };
  }

  const action = servers[serverName] ? 'updated' : 'created';
  servers[serverName] = entry;
  return { config, action };
}

// ---------------------------------------------------------------------------
// MCP server entry generator
// ---------------------------------------------------------------------------

export function generateMcpEntry(customServerPath?: string) {
  return {
    command: getBunPath(),
    args: ['run', customServerPath || getMcpServerPath()],
    env: {
      PORTKEY_PRIVATE_KEY: '<YOUR_PRIVATE_KEY>',
      PORTKEY_NETWORK: 'mainnet',
    },
  };
}

export const SERVER_NAME = 'ca-agent-skills';

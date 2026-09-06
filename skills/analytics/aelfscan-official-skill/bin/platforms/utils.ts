import * as fs from 'node:fs';
import * as os from 'node:os';
import * as path from 'node:path';

export const SERVER_NAME = 'aelfscan-skill';

export interface PlatformPaths {
  claude: string;
  cursorGlobal: string;
}

export interface McpServerEntry {
  command: string;
  args: string[];
  env: Record<string, string>;
}

export function getPackageRoot(): string {
  return path.resolve(import.meta.dir, '..', '..');
}

export function getMcpServerPath(): string {
  return path.join(getPackageRoot(), 'src', 'mcp', 'server.ts');
}

export function getBunPath(): string {
  try {
    const cmd = os.platform() === 'win32' ? ['where', 'bun'] : ['which', 'bun'];
    const result = Bun.spawnSync(cmd);
    const output = result.stdout.toString().trim();
    if (output) {
      return output.split('\n')[0].trim();
    }
  } catch {
    // ignore and use fallback
  }
  return 'bun';
}

export function getPlatformPaths(): PlatformPaths {
  const home = os.homedir();
  const platform = os.platform();

  let claude: string;
  if (platform === 'darwin') {
    claude = path.join(home, 'Library', 'Application Support', 'Claude', 'claude_desktop_config.json');
  } else if (platform === 'win32') {
    const appData = process.env.APPDATA || path.join(home, 'AppData', 'Roaming');
    claude = path.join(appData, 'Claude', 'claude_desktop_config.json');
  } else {
    claude = path.join(home, '.config', 'Claude', 'claude_desktop_config.json');
  }

  return {
    claude,
    cursorGlobal: path.join(home, '.cursor', 'mcp.json'),
  };
}

export function getCursorProjectPath(projectDir?: string): string {
  const baseDir = projectDir || process.cwd();
  return path.join(baseDir, '.cursor', 'mcp.json');
}

export function readJsonFile(filePath: string): any {
  try {
    if (!fs.existsSync(filePath)) {
      return {};
    }

    const text = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(text);
  } catch {
    return {};
  }
}

export function writeJsonFile(filePath: string, data: any): void {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  fs.writeFileSync(filePath, `${JSON.stringify(data, null, 2)}\n`, 'utf8');
}

export function generateMcpEntry(customServerPath?: string): McpServerEntry {
  return {
    command: getBunPath(),
    args: ['run', customServerPath || getMcpServerPath()],
    env: {
      AELFSCAN_API_BASE_URL: 'https://aelfscan.io',
    },
  };
}

export function mergeMcpConfig(
  existing: any,
  serverName: string,
  entry: McpServerEntry,
  force = false,
): { config: any; action: 'created' | 'updated' | 'skipped' } {
  const config = { ...existing };
  if (!config.mcpServers) {
    config.mcpServers = {};
  }

  if (config.mcpServers[serverName] && !force) {
    return { config, action: 'skipped' };
  }

  const action = config.mcpServers[serverName] ? 'updated' : 'created';
  config.mcpServers[serverName] = entry;
  return { config, action };
}

export function removeMcpEntry(existing: any, serverName: string): { config: any; removed: boolean } {
  const config = { ...existing };
  if (!config.mcpServers || !config.mcpServers[serverName]) {
    return { config, removed: false };
  }

  delete config.mcpServers[serverName];
  return { config, removed: true };
}

export const LOG = {
  step: (message: string) => console.log(`  -> ${message}`),
  info: (message: string) => console.log(`  [INFO] ${message}`),
  success: (message: string) => console.log(`  [OK] ${message}`),
  warn: (message: string) => console.log(`  [WARN] ${message}`),
  error: (message: string) => console.error(`  [ERROR] ${message}`),
};

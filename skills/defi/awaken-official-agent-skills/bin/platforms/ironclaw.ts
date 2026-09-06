import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import {
  SERVER_NAME,
  getBunPath,
  getMcpServerPath,
  getPackageRoot,
  readJsonFile,
  writeJsonFile,
} from './utils';

export const IRONCLAW_CONFIG_SCHEMA_VERSION = 1;

export type IronclawStdioTransport = {
  transport: 'stdio';
  command: string;
  args: string[];
  env: Record<string, string>;
};

export type IronclawMcpServer = {
  name: string;
  url: string;
  transport: IronclawStdioTransport;
  headers: Record<string, string>;
  enabled: boolean;
  description?: string;
};

export type IronclawMcpConfig = {
  schema_version: number;
  servers: IronclawMcpServer[];
};

type MergeAction = 'created' | 'updated' | 'skipped';
type SkillAction = 'created' | 'updated' | 'skipped';
const SKILL_DIR_NAME = 'awaken-agent-skills';

function getIronclawBaseDir(): string {
  return path.join(os.homedir(), '.ironclaw');
}

export function getIronclawMcpConfigPath(): string {
  return path.join(getIronclawBaseDir(), 'mcp-servers.json');
}

export function getIronclawSkillsDir(): string {
  return path.join(getIronclawBaseDir(), 'skills');
}

export function getIronclawSkillInstallPath(skillsDir = getIronclawSkillsDir()): string {
  return path.join(skillsDir, SKILL_DIR_NAME, 'SKILL.md');
}

function getBundledSkillPath(): string {
  return path.join(getPackageRoot(), 'SKILL.md');
}

function normalizeIronclawMcpConfig(existing: any): IronclawMcpConfig {
  return {
    schema_version:
      typeof existing?.schema_version === 'number'
        ? existing.schema_version
        : IRONCLAW_CONFIG_SCHEMA_VERSION,
    servers: Array.isArray(existing?.servers) ? [...existing.servers] : [],
  };
}

export function generateIronclawServerEntry(customServerPath?: string): IronclawMcpServer {
  return {
    name: SERVER_NAME,
    url: '',
    transport: {
      transport: 'stdio',
      command: getBunPath(),
      args: ['run', customServerPath || getMcpServerPath()],
      env: {
        AELF_PRIVATE_KEY: '<YOUR_PRIVATE_KEY>',
        AWAKEN_NETWORK: 'mainnet',
      },
    },
    headers: {},
    enabled: true,
    description: 'Awaken DEX MCP server for IronClaw',
  };
}

export function mergeIronclawMcpConfig(
  existing: any,
  entry: IronclawMcpServer,
  force = false,
): { config: IronclawMcpConfig; action: MergeAction } {
  const config = normalizeIronclawMcpConfig(existing);
  const index = config.servers.findIndex(server => server?.name === entry.name);

  if (index >= 0 && !force) {
    return { config, action: 'skipped' };
  }

  if (index >= 0) {
    const servers = [...config.servers];
    servers[index] = entry;
    return {
      config: { ...config, schema_version: IRONCLAW_CONFIG_SCHEMA_VERSION, servers },
      action: 'updated',
    };
  }

  return {
    config: {
      ...config,
      schema_version: IRONCLAW_CONFIG_SCHEMA_VERSION,
      servers: [...config.servers, entry],
    },
    action: 'created',
  };
}

export function removeIronclawMcpConfig(
  existing: any,
  serverName = SERVER_NAME,
): { config: IronclawMcpConfig; removed: boolean } {
  const config = normalizeIronclawMcpConfig(existing);
  const servers = config.servers.filter(server => server?.name !== serverName);

  return {
    config: {
      ...config,
      schema_version: IRONCLAW_CONFIG_SCHEMA_VERSION,
      servers,
    },
    removed: servers.length !== config.servers.length,
  };
}

function installIronclawSkill(
  skillsDir = getIronclawSkillsDir(),
  force = false,
): { action: SkillAction; skillPath: string } {
  const sourcePath = getBundledSkillPath();
  const targetPath = getIronclawSkillInstallPath(skillsDir);
  const targetDir = path.dirname(targetPath);
  const existedBefore = fs.existsSync(targetPath);

  if (!fs.existsSync(sourcePath)) {
    throw new Error(`Bundled SKILL.md not found at ${sourcePath}`);
  }

  if (existedBefore && !force) {
    return { action: 'skipped', skillPath: targetPath };
  }

  fs.mkdirSync(targetDir, { recursive: true });
  fs.copyFileSync(sourcePath, targetPath);

  return {
    action: existedBefore ? 'updated' : 'created',
    skillPath: targetPath,
  };
}

export function assertSafeIronclawSkillDir(skillsDir: string, skillDir: string): void {
  const resolvedSkillsDir = path.resolve(skillsDir);
  const resolvedSkillDir = path.resolve(skillDir);
  const expectedSkillDir = path.dirname(getIronclawSkillInstallPath(resolvedSkillsDir));
  const relative = path.relative(resolvedSkillsDir, resolvedSkillDir);

  if (
    resolvedSkillDir !== expectedSkillDir ||
    path.isAbsolute(relative) ||
    relative.startsWith('..') ||
    path.basename(resolvedSkillDir) !== SKILL_DIR_NAME
  ) {
    throw new Error(`Refusing to remove unexpected IronClaw skill path: ${resolvedSkillDir}`);
  }
}

function removeIronclawSkill(
  skillsDir = getIronclawSkillsDir(),
): { skillRemoved: boolean; skillPath: string } {
  const skillPath = getIronclawSkillInstallPath(skillsDir);
  const skillDir = path.dirname(skillPath);
  const exists = fs.existsSync(skillDir);

  if (exists) {
    assertSafeIronclawSkillDir(skillsDir, skillDir);
    fs.rmSync(skillDir, { recursive: true, force: true });
  }

  return { skillRemoved: exists, skillPath };
}

export function setupIronclaw(opts: {
  mcpConfigPath?: string;
  skillsDir?: string;
  serverPath?: string;
  force?: boolean;
}) {
  const mcpConfigPath = opts.mcpConfigPath || getIronclawMcpConfigPath();
  const existing = readJsonFile(mcpConfigPath);
  const entry = generateIronclawServerEntry(opts.serverPath);
  const { config, action } = mergeIronclawMcpConfig(existing, entry, opts.force);
  const skill = installIronclawSkill(opts.skillsDir, opts.force);

  if (action !== 'skipped') {
    writeJsonFile(mcpConfigPath, config);
  }

  console.log(`[${action.toUpperCase()}] IronClaw MCP config → ${mcpConfigPath}`);
  console.log(`[${skill.action.toUpperCase()}] Trusted skill → ${skill.skillPath}`);
  console.log('\nRemember to replace <YOUR_PRIVATE_KEY> in the IronClaw MCP config.');

  return {
    mcpAction: action,
    skillAction: skill.action,
    mcpConfigPath,
    skillPath: skill.skillPath,
  };
}

export function uninstallIronclaw(opts: {
  mcpConfigPath?: string;
  skillsDir?: string;
}) {
  const mcpConfigPath = opts.mcpConfigPath || getIronclawMcpConfigPath();
  const existing = readJsonFile(mcpConfigPath);
  const { config, removed } = removeIronclawMcpConfig(existing);
  const skill = removeIronclawSkill(opts.skillsDir);

  if (removed) {
    writeJsonFile(mcpConfigPath, config);
  }

  if (!removed) {
    console.log(`[SKIP] "${SERVER_NAME}" not found in ${mcpConfigPath}`);
  } else {
    console.log(`[REMOVED] "${SERVER_NAME}" from ${mcpConfigPath}`);
  }

  if (!skill.skillRemoved) {
    console.log(`[SKIP] Trusted skill not found at ${skill.skillPath}`);
  } else {
    console.log(`[REMOVED] Trusted skill → ${skill.skillPath}`);
  }

  return {
    mcpRemoved: removed,
    skillRemoved: skill.skillRemoved,
    mcpConfigPath,
    skillPath: skill.skillPath,
  };
}

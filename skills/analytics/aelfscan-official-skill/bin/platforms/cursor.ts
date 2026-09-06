import {
  LOG,
  SERVER_NAME,
  generateMcpEntry,
  getCursorProjectPath,
  getPlatformPaths,
  mergeMcpConfig,
  readJsonFile,
  removeMcpEntry,
  writeJsonFile,
} from './utils.js';

export function setupCursor(opts: {
  global?: boolean;
  configPath?: string;
  serverPath?: string;
  force?: boolean;
  projectDir?: string;
}): boolean {
  let configPath: string;
  let scope: 'global' | 'project' | 'custom';

  if (opts.configPath) {
    configPath = opts.configPath;
    scope = 'custom';
  } else if (opts.global) {
    configPath = getPlatformPaths().cursorGlobal;
    scope = 'global';
  } else {
    configPath = getCursorProjectPath(opts.projectDir);
    scope = 'project';
  }

  const entry = generateMcpEntry(opts.serverPath);

  LOG.step(`Scope: ${scope}`);
  LOG.step(`Config file: ${configPath}`);
  LOG.step(`MCP server: ${entry.args[1]}`);

  const existing = readJsonFile(configPath);
  const { config, action } = mergeMcpConfig(existing, SERVER_NAME, entry, opts.force);

  if (action === 'skipped') {
    LOG.warn(`\"${SERVER_NAME}\" already exists in Cursor ${scope} config.`);
    LOG.info('Use --force to overwrite.');
    return false;
  }

  writeJsonFile(configPath, config);
  LOG.success(`Cursor ${scope} MCP config ${action}: ${configPath}`);
  return true;
}

export function uninstallCursor(opts: { global?: boolean; configPath?: string; projectDir?: string }): boolean {
  let configPath: string;

  if (opts.configPath) {
    configPath = opts.configPath;
  } else if (opts.global) {
    configPath = getPlatformPaths().cursorGlobal;
  } else {
    configPath = getCursorProjectPath(opts.projectDir);
  }

  const existing = readJsonFile(configPath);
  const { config, removed } = removeMcpEntry(existing, SERVER_NAME);

  if (!removed) {
    LOG.info(`\"${SERVER_NAME}\" not found in Cursor config: ${configPath}`);
    return false;
  }

  writeJsonFile(configPath, config);
  LOG.success(`Removed \"${SERVER_NAME}\" from Cursor config: ${configPath}`);
  return true;
}

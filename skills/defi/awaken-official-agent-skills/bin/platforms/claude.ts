// ============================================================
// Setup: Claude Desktop — write MCP config
// ============================================================

import {
  getPlatformPaths,
  readJsonFile,
  writeJsonFile,
  generateMcpEntry,
  mergeMcpConfig,
  removeMcpEntry,
  SERVER_NAME,
  LOG,
} from './utils';

export function setupClaude(opts: { configPath?: string; serverPath?: string; force?: boolean }): boolean {
  const configPath = opts.configPath || getPlatformPaths().claude;
  const entry = generateMcpEntry(opts.serverPath);

  LOG.step(`Config file: ${configPath}`);
  LOG.step(`MCP server: ${entry.args[1]}`);

  const existing = readJsonFile(configPath);
  const { config, action } = mergeMcpConfig(existing, SERVER_NAME, entry, opts.force);

  if (action === 'skipped') {
    LOG.warn(`"${SERVER_NAME}" already exists in Claude Desktop config.`);
    LOG.info('Use --force to overwrite.');
    return false;
  }

  writeJsonFile(configPath, config);
  LOG.success(`Claude Desktop MCP config ${action}: ${configPath}`);
  LOG.info('');
  LOG.warn('IMPORTANT: Edit the config file and replace <YOUR_PRIVATE_KEY> with your actual aelf private key.');
  LOG.info('Then restart Claude Desktop to pick up the new MCP server.');
  return true;
}

export function uninstallClaude(opts: { configPath?: string }): boolean {
  const configPath = opts.configPath || getPlatformPaths().claude;
  const existing = readJsonFile(configPath);
  const { config, removed } = removeMcpEntry(existing, SERVER_NAME);

  if (!removed) {
    LOG.info(`"${SERVER_NAME}" not found in Claude Desktop config.`);
    return false;
  }

  writeJsonFile(configPath, config);
  LOG.success(`Removed "${SERVER_NAME}" from Claude Desktop config.`);
  LOG.info('Restart Claude Desktop to apply changes.');
  return true;
}

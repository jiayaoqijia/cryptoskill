import {
  generateMcpEntry,
  getPlatformPaths,
  mergeMcpConfig,
  readJsonFile,
  removeMcpConfig,
  SERVER_NAME,
  writeJsonFile,
} from './utils.js';

export function setupClaude(opts: { configPath?: string; serverPath?: string; force?: boolean }) {
  const paths = getPlatformPaths();
  const configPath = opts.configPath || paths.claude;
  const existing = readJsonFile(configPath);
  const { config, action } = mergeMcpConfig(existing, SERVER_NAME, generateMcpEntry(opts.serverPath), opts.force);

  if (action === 'skipped') {
    console.log(`[SKIP] ${SERVER_NAME} already exists in ${configPath}. Use --force to overwrite.`);
    return;
  }

  writeJsonFile(configPath, config);
  console.log(`[DONE] ${action} ${SERVER_NAME} in ${configPath}`);
}

export function uninstallClaude(opts: { configPath?: string }) {
  const paths = getPlatformPaths();
  const configPath = opts.configPath || paths.claude;
  const existing = readJsonFile(configPath);
  const { config, removed } = removeMcpConfig(existing, SERVER_NAME);
  if (!removed) {
    console.log(`[INFO] ${SERVER_NAME} not found in ${configPath}`);
    return;
  }
  writeJsonFile(configPath, config);
  console.log(`[DONE] removed ${SERVER_NAME} from ${configPath}`);
}

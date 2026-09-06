import {
  getPlatformPaths,
  readJsonFile,
  writeJsonFile,
  mergeMcpConfig,
  generateMcpEntry,
  SERVER_NAME,
} from './utils.js';

export interface CursorSetupOptions {
  configPath?: string;
  serverPath?: string;
  force?: boolean;
  global?: boolean;
}

export function setupCursor(options: CursorSetupOptions = {}): void {
  const paths = getPlatformPaths();
  const configPath =
    options.configPath || (options.global ? paths.cursorGlobal : paths.cursorProject);

  const existing = readJsonFile(configPath);
  const entry = generateMcpEntry(options.serverPath);
  const { config, action } = mergeMcpConfig(existing, SERVER_NAME, entry, options.force);

  if (action === 'skipped') {
    console.log(`[SKIP] "${SERVER_NAME}" already exists in ${configPath}`);
    console.log('       Use --force to overwrite.');
    return;
  }

  writeJsonFile(configPath, config);
  const scope = options.global ? 'global' : 'project-level';
  console.log(`[${action.toUpperCase()}] ${SERVER_NAME} (${scope}) in ${configPath}`);
  console.log('');
  console.log('Next steps:');
  console.log('  1. Edit the config to replace <YOUR_PRIVATE_KEY> with your actual key');
  console.log('  2. Restart Cursor or reload the MCP servers');
}

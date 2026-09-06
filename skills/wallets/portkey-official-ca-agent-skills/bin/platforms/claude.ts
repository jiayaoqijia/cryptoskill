import {
  getPlatformPaths,
  readJsonFile,
  writeJsonFile,
  mergeMcpConfig,
  generateMcpEntry,
  SERVER_NAME,
} from './utils.js';

export interface ClaudeSetupOptions {
  configPath?: string;
  serverPath?: string;
  force?: boolean;
}

export function setupClaude(options: ClaudeSetupOptions = {}): void {
  const paths = getPlatformPaths();
  const configPath = options.configPath || paths.claude;

  const existing = readJsonFile(configPath);
  const entry = generateMcpEntry(options.serverPath);
  const { config, action } = mergeMcpConfig(existing, SERVER_NAME, entry, options.force);

  if (action === 'skipped') {
    console.log(`[SKIP] "${SERVER_NAME}" already exists in ${configPath}`);
    console.log('       Use --force to overwrite.');
    return;
  }

  writeJsonFile(configPath, config);
  console.log(`[${action.toUpperCase()}] ${SERVER_NAME} in ${configPath}`);
  console.log('');
  console.log('Next steps:');
  console.log('  1. Edit the config to replace <YOUR_PRIVATE_KEY> with your actual key');
  console.log('  2. Restart Claude Desktop');
}

#!/usr/bin/env bun
import { Command } from 'commander';
import * as fs from 'node:fs';
import packageJson from '../package.json';
import {
  LOG,
  SERVER_NAME,
  getBunPath,
  getCursorProjectPath,
  getMcpServerPath,
  getPackageRoot,
  getPlatformPaths,
  readJsonFile,
} from './platforms/utils.js';
import { setupClaude, uninstallClaude } from './platforms/claude.js';
import { setupCursor, uninstallCursor } from './platforms/cursor.js';
import { setupOpenClaw, uninstallOpenClaw } from './platforms/openclaw.js';

const program = new Command();

program
  .name('aelfscan-setup')
  .description('Configure @aelfscan/agent-skills for Claude/Cursor/OpenClaw')
  .version(packageJson.version);

const withCommonMcpOptions = (command: Command) =>
  command
    .option('--server-path <path>', 'Custom path to MCP server.ts')
    .option('--config-path <path>', 'Custom config file path')
    .option('--force', 'Overwrite existing aelfscan-skill entry', false);

withCommonMcpOptions(
  program
    .command('claude')
    .description('Setup MCP server for Claude Desktop'),
).action(opts => {
  console.log('\nConfiguring Claude Desktop...\n');
  setupClaude({
    configPath: opts.configPath,
    serverPath: opts.serverPath,
    force: opts.force,
  });
  console.log('');
});

withCommonMcpOptions(
  program
    .command('cursor')
    .description('Setup MCP server for Cursor')
    .option('--global', 'Write to global ~/.cursor/mcp.json', false),
).action(opts => {
  console.log(`\nConfiguring Cursor (${opts.global ? 'global' : 'project'})...\n`);
  setupCursor({
    global: opts.global,
    configPath: opts.configPath,
    serverPath: opts.serverPath,
    force: opts.force,
  });
  console.log('');
});

program
  .command('openclaw')
  .description('Generate or merge OpenClaw tool configuration')
  .option('--config-path <path>', 'Merge into an existing OpenClaw config file')
  .option('--cwd <dir>', 'Working directory for OpenClaw tools')
  .option('--force', 'Overwrite existing tools with the same name', false)
  .action(opts => {
    console.log('\nConfiguring OpenClaw...\n');
    setupOpenClaw({
      configPath: opts.configPath,
      cwd: opts.cwd,
      force: opts.force,
    });
    console.log('');
  });

program
  .command('list')
  .description('Show detected config paths and setup status')
  .action(() => {
    const pkgRoot = getPackageRoot();
    const serverPath = getMcpServerPath();
    const bunPath = getBunPath();
    const paths = getPlatformPaths();
    const cursorProjectPath = getCursorProjectPath();

    console.log('\nAelfScan Skill setup status\n');
    console.log(`  Package root: ${pkgRoot}`);
    console.log(`  MCP server:   ${serverPath} ${fs.existsSync(serverPath) ? '[OK]' : '[MISSING]'}`);
    console.log(`  Bun path:     ${bunPath}`);
    console.log('');

    const claudeExists = fs.existsSync(paths.claude);
    const claude = claudeExists ? readJsonFile(paths.claude) : null;
    const claudeConfigured = Boolean(claude?.mcpServers?.[SERVER_NAME]);
    console.log(`  Claude Desktop: ${paths.claude}`);
    console.log(
      `    Config file: ${claudeExists ? 'exists' : 'not found'} | ${SERVER_NAME}: ${claudeConfigured ? 'configured' : 'not configured'}`,
    );

    const cursorGlobalExists = fs.existsSync(paths.cursorGlobal);
    const cursorGlobal = cursorGlobalExists ? readJsonFile(paths.cursorGlobal) : null;
    const cursorGlobalConfigured = Boolean(cursorGlobal?.mcpServers?.[SERVER_NAME]);
    console.log(`  Cursor (global): ${paths.cursorGlobal}`);
    console.log(
      `    Config file: ${cursorGlobalExists ? 'exists' : 'not found'} | ${SERVER_NAME}: ${cursorGlobalConfigured ? 'configured' : 'not configured'}`,
    );

    const cursorProjectExists = fs.existsSync(cursorProjectPath);
    const cursorProject = cursorProjectExists ? readJsonFile(cursorProjectPath) : null;
    const cursorProjectConfigured = Boolean(cursorProject?.mcpServers?.[SERVER_NAME]);
    console.log(`  Cursor (project): ${cursorProjectPath}`);
    console.log(
      `    Config file: ${cursorProjectExists ? 'exists' : 'not found'} | ${SERVER_NAME}: ${cursorProjectConfigured ? 'configured' : 'not configured'}`,
    );

    console.log('');
    LOG.info('Use `bun run setup claude|cursor|openclaw` to install.');
    console.log('');
  });

program
  .command('uninstall <platform>')
  .description('Remove aelfscan-skill setup from platform (claude|cursor|openclaw)')
  .option('--global', 'For cursor uninstall global config', false)
  .option('--config-path <path>', 'Custom config file path')
  .action((platform, opts) => {
    console.log(`\nRemoving setup from ${platform}...\n`);

    switch (platform) {
      case 'claude':
        uninstallClaude({ configPath: opts.configPath });
        break;
      case 'cursor':
        uninstallCursor({ global: opts.global, configPath: opts.configPath });
        break;
      case 'openclaw':
        uninstallOpenClaw({ configPath: opts.configPath });
        break;
      default:
        LOG.error(`Unknown platform: ${platform}. Supported: claude, cursor, openclaw.`);
        process.exitCode = 1;
        break;
    }

    console.log('');
  });

program.parse();

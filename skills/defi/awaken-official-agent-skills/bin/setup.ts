#!/usr/bin/env bun
// ============================================================
// Awaken Agent Kit — Setup CLI
// ============================================================
// One-command setup for Claude Desktop, Cursor, OpenClaw, and IronClaw.
//
// Usage:
//   bun run bin/setup.ts claude             # Configure Claude Desktop MCP
//   bun run bin/setup.ts cursor             # Configure Cursor (project)
//   bun run bin/setup.ts cursor --global    # Configure Cursor (global)
//   bun run bin/setup.ts ironclaw           # Configure IronClaw trusted skill + MCP
//   bun run bin/setup.ts openclaw           # Generate OpenClaw config
//   bun run bin/setup.ts list               # Show detected paths & status
//   bun run bin/setup.ts uninstall claude   # Remove from Claude Desktop

import { Command } from 'commander';
import * as fs from 'fs';
import packageJson from '../package.json';
import {
  getPackageRoot,
  getMcpServerPath,
  getBunPath,
  getPlatformPaths,
  getCursorProjectPath,
  readJsonFile,
  SERVER_NAME,
  LOG,
} from './platforms/utils';
import { setupClaude, uninstallClaude } from './platforms/claude';
import { setupCursor, uninstallCursor } from './platforms/cursor';
import {
  getIronclawMcpConfigPath,
  getIronclawSkillInstallPath,
  getIronclawSkillsDir,
  setupIronclaw,
  uninstallIronclaw,
} from './platforms/ironclaw';
import { setupOpenClaw, uninstallOpenClaw } from './platforms/openclaw';

const program = new Command();

program
  .name('awaken-setup')
  .description('Configure @awaken-finance/agent-kit for various AI platforms')
  .version(packageJson.version);

// ---- Shared options ----
const sharedOpts = (cmd: Command) =>
  cmd
    .option('--server-path <path>', 'Custom path to MCP server.ts')
    .option('--config-path <path>', 'Custom config file path (overrides auto-detection)')
    .option('--force', 'Overwrite existing config entry', false);

// ---- claude ----
sharedOpts(
  program
    .command('claude')
    .description('Setup MCP server for Claude Desktop'),
)
  .action((opts) => {
    console.log('\n🔧 Setting up Claude Desktop...\n');
    setupClaude({
      configPath: opts.configPath,
      serverPath: opts.serverPath,
      force: opts.force,
    });
    console.log('');
  });

// ---- cursor ----
sharedOpts(
  program
    .command('cursor')
    .description('Setup MCP server for Cursor IDE')
    .option('--global', 'Write to global ~/.cursor/mcp.json instead of project-level', false),
)
  .action((opts) => {
    const scope = opts.global ? 'global' : 'project';
    console.log(`\n🔧 Setting up Cursor (${scope})...\n`);
    setupCursor({
      global: opts.global,
      configPath: opts.configPath,
      serverPath: opts.serverPath,
      force: opts.force,
    });
    console.log('');
  });

// ---- ironclaw ----
sharedOpts(
  program
    .command('ironclaw')
    .description('Setup trusted skill and MCP server for IronClaw'),
)
  .option('--mcp-config-path <path>', 'Custom IronClaw MCP config path')
  .option('--skills-dir <path>', 'Custom IronClaw trusted skills directory')
  .action((opts) => {
    console.log('\n🔧 Setting up IronClaw...\n');
    setupIronclaw({
      mcpConfigPath: opts.mcpConfigPath,
      skillsDir: opts.skillsDir,
      serverPath: opts.serverPath,
      force: opts.force,
    });
    console.log('');
  });

// ---- openclaw ----
program
  .command('openclaw')
  .description('Generate OpenClaw tool configuration')
  .option('--config-path <path>', 'Merge into existing OpenClaw config file')
  .option('--cwd <dir>', 'Working directory for CLI commands')
  .option('--force', 'Overwrite existing tools in target config', false)
  .action((opts) => {
    console.log('\n🔧 Setting up OpenClaw...\n');
    setupOpenClaw({
      configPath: opts.configPath,
      cwd: opts.cwd,
      force: opts.force,
    });
    console.log('');
  });

// ---- list ----
program
  .command('list')
  .description('Show platform config paths and current status')
  .action(() => {
    console.log('\n📋 Awaken Agent Kit — Configuration Status\n');

    const pkgRoot = getPackageRoot();
    const serverPath = getMcpServerPath();
    const bunPath = getBunPath();
    const paths = getPlatformPaths();
    const cursorProject = getCursorProjectPath();

    console.log('  Package root:', pkgRoot);
    console.log('  MCP server:  ', serverPath, fs.existsSync(serverPath) ? '✅' : '❌ NOT FOUND');
    console.log('  Bun path:    ', bunPath);
    console.log('');

    // Claude Desktop
    const claudeExists = fs.existsSync(paths.claude);
    const claudeConfig = claudeExists ? readJsonFile(paths.claude) : null;
    const claudeHasUs = claudeConfig?.mcpServers?.[SERVER_NAME] ? true : false;
    console.log(`  Claude Desktop: ${paths.claude}`);
    console.log(`    Config exists: ${claudeExists ? '✅' : '—'}  |  ${SERVER_NAME}: ${claudeHasUs ? '✅ configured' : '— not configured'}`);

    // Cursor global
    const cursorGlobalExists = fs.existsSync(paths.cursorGlobal);
    const cursorGlobalConfig = cursorGlobalExists ? readJsonFile(paths.cursorGlobal) : null;
    const cursorGlobalHasUs = cursorGlobalConfig?.mcpServers?.[SERVER_NAME] ? true : false;
    console.log(`  Cursor (global): ${paths.cursorGlobal}`);
    console.log(`    Config exists: ${cursorGlobalExists ? '✅' : '—'}  |  ${SERVER_NAME}: ${cursorGlobalHasUs ? '✅ configured' : '— not configured'}`);

    // Cursor project
    const cursorProjectExists = fs.existsSync(cursorProject);
    const cursorProjectConfig = cursorProjectExists ? readJsonFile(cursorProject) : null;
    const cursorProjectHasUs = cursorProjectConfig?.mcpServers?.[SERVER_NAME] ? true : false;
    console.log(`  Cursor (project): ${cursorProject}`);
    console.log(`    Config exists: ${cursorProjectExists ? '✅' : '—'}  |  ${SERVER_NAME}: ${cursorProjectHasUs ? '✅ configured' : '— not configured'}`);

    const ironclawMcpPath = getIronclawMcpConfigPath();
    const ironclawSkillsDir = getIronclawSkillsDir();
    const ironclawSkillPath = getIronclawSkillInstallPath(ironclawSkillsDir);
    const ironclawMcpExists = fs.existsSync(ironclawMcpPath);
    const ironclawConfig = ironclawMcpExists ? readJsonFile(ironclawMcpPath) : null;
    const ironclawHasUs = Array.isArray(ironclawConfig?.servers)
      ? ironclawConfig.servers.some((server: any) => server?.name === SERVER_NAME)
      : false;
    const ironclawSkillExists = fs.existsSync(ironclawSkillPath);
    console.log(`  IronClaw: ${ironclawMcpPath}`);
    console.log(
      `    MCP entry: ${ironclawHasUs ? '✅ configured' : '— not configured'}  |  trusted skill: ${ironclawSkillExists ? '✅ present' : '— missing'}`,
    );

    console.log('');
  });

// ---- uninstall ----
program
  .command('uninstall <platform>')
  .description('Remove Awaken config from a platform (claude, cursor, ironclaw, openclaw)')
  .option('--global', 'For cursor: target global config', false)
  .option('--config-path <path>', 'Custom config file path')
  .option('--mcp-config-path <path>', 'Custom IronClaw MCP config path')
  .option('--skills-dir <path>', 'Custom IronClaw trusted skills directory')
  .action((platform, opts) => {
    console.log(`\n🗑️  Removing Awaken config from ${platform}...\n`);

    switch (platform) {
      case 'claude':
        uninstallClaude({ configPath: opts.configPath });
        break;
      case 'cursor':
        uninstallCursor({ global: opts.global, configPath: opts.configPath });
        break;
      case 'ironclaw':
        uninstallIronclaw({
          mcpConfigPath: opts.mcpConfigPath,
          skillsDir: opts.skillsDir,
        });
        break;
      case 'openclaw':
        uninstallOpenClaw({ configPath: opts.configPath });
        break;
      default:
        LOG.error(`Unknown platform: ${platform}. Use: claude, cursor, ironclaw, or openclaw.`);
    }
    console.log('');
  });

program.parse();

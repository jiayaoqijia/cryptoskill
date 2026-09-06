#!/usr/bin/env bun
import { Command } from 'commander';
import packageJson from '../package.json';
import { setupClaude, uninstallClaude } from './platforms/claude.js';
import { setupCursor, uninstallCursor } from './platforms/cursor.js';
import {
  getIronclawMcpConfigPath,
  getIronclawSkillInstallPath,
  getIronclawSkillsDir,
  setupIronclaw,
  uninstallIronclaw,
} from './platforms/ironclaw.js';
import { setupOpenclaw } from './platforms/openclaw.js';
import {
  getPackageRoot,
  getPlatformPaths,
  readJsonFile,
  SERVER_NAME,
} from './platforms/utils.js';
import * as fs from 'fs';
import * as path from 'path';

const program = new Command();
program.name('tomorrowdao-setup').description('Configure TomorrowDAO MCP/OpenClaw integration');
program.version(packageJson.version);

program
  .command('claude')
  .option('--config-path <path>')
  .option('--server-path <path>')
  .option('--force')
  .action((opts) => setupClaude(opts));

program
  .command('cursor')
  .option('--global')
  .option('--config-path <path>')
  .option('--server-path <path>')
  .option('--force')
  .action((opts) => setupCursor(opts));

program
  .command('ironclaw')
  .option('--mcp-config-path <path>')
  .option('--skills-dir <path>')
  .option('--server-path <path>')
  .option('--force')
  .action((opts) => {
    setupIronclaw(opts);
  });

program
  .command('openclaw')
  .option('--config-path <path>')
  .option('--cwd <dir>')
  .option('--force')
  .action((opts) => setupOpenclaw(opts));

program
  .command('list')
  .action(() => {
    const paths = getPlatformPaths();

    const claudeConfig = fs.existsSync(paths.claude) ? readJsonFile(paths.claude) : null;
    const cursorGlobalConfig = fs.existsSync(paths.cursorGlobal)
      ? readJsonFile(paths.cursorGlobal)
      : null;
    const cursorProjectConfig = fs.existsSync(paths.cursorProject)
      ? readJsonFile(paths.cursorProject)
      : null;

    const openclawPath = path.join(getPackageRoot(), 'openclaw.json');
    const openclawConfig = fs.existsSync(openclawPath) ? readJsonFile(openclawPath) : null;

    console.log('Platform Configuration Status:\n');
    console.log(
      `  Claude Desktop: ${claudeConfig?.mcpServers?.[SERVER_NAME] ? 'CONFIGURED' : fs.existsSync(paths.claude) ? 'NOT CONFIGURED' : 'CONFIG FILE NOT FOUND'}`,
    );
    console.log(`    Path: ${paths.claude}\n`);

    console.log(
      `  Cursor (global): ${cursorGlobalConfig?.mcpServers?.[SERVER_NAME] ? 'CONFIGURED' : fs.existsSync(paths.cursorGlobal) ? 'NOT CONFIGURED' : 'CONFIG FILE NOT FOUND'}`,
    );
    console.log(`    Path: ${paths.cursorGlobal}\n`);

    console.log(
      `  Cursor (project): ${cursorProjectConfig?.mcpServers?.[SERVER_NAME] ? 'CONFIGURED' : fs.existsSync(paths.cursorProject) ? 'NOT CONFIGURED' : 'CONFIG FILE NOT FOUND'}`,
    );
    console.log(`    Path: ${paths.cursorProject}\n`);

    const ironclawMcpPath = getIronclawMcpConfigPath();
    const ironclawSkillsDir = getIronclawSkillsDir();
    const ironclawSkillPath = getIronclawSkillInstallPath(ironclawSkillsDir);
    const ironclawConfig = fs.existsSync(ironclawMcpPath) ? readJsonFile(ironclawMcpPath) : null;
    const ironclawConfigured = Array.isArray(ironclawConfig?.servers)
      ? ironclawConfig.servers.some((server: any) => server?.name === SERVER_NAME)
      : false;
    console.log(`  IronClaw: ${ironclawConfigured || fs.existsSync(ironclawSkillPath) ? 'CONFIGURED' : 'NOT FOUND'}`);
    console.log(`    MCP: ${ironclawMcpPath}`);
    console.log(`    Trusted skill: ${ironclawSkillPath}\n`);

    console.log(`  OpenClaw: ${openclawConfig ? 'AVAILABLE' : 'NOT FOUND'}`);
    console.log(`    Path: ${openclawPath}`);
  });

program
  .command('uninstall <platform>')
  .option('--global')
  .option('--config-path <path>')
  .option('--mcp-config-path <path>')
  .option('--skills-dir <path>')
  .action((platform, opts) => {
    if (platform === 'claude') {
      uninstallClaude(opts);
      return;
    }
    if (platform === 'cursor') {
      uninstallCursor(opts);
      return;
    }
    if (platform === 'ironclaw') {
      uninstallIronclaw({
        mcpConfigPath: opts.mcpConfigPath,
        skillsDir: opts.skillsDir,
      });
      return;
    }
    if (platform === 'openclaw') {
      console.log('[INFO] For OpenClaw, remove tools with prefix tomorrowdao- from your config file.');
      return;
    }
    console.error(`Unknown platform: ${platform}`);
    process.exit(1);
  });

program.parse();

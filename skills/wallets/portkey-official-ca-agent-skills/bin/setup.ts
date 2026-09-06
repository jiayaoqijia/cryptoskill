#!/usr/bin/env bun
import { Command } from 'commander';
import * as fs from 'fs';
import * as path from 'path';
import packageJson from '../package.json';
import { setupClaude } from './platforms/claude.js';
import { setupCursor } from './platforms/cursor.js';
import {
  getIronclawMcpConfigPath,
  getIronclawSkillInstallPath,
  getIronclawSkillsDir,
  setupIronclaw,
  uninstallIronclaw,
} from './platforms/ironclaw.js';
import { setupOpenClaw } from './platforms/openclaw.js';
import {
  getPackageRoot,
  getPlatformPaths,
  readJsonFile,
  writeJsonFile,
  SERVER_NAME,
} from './platforms/utils.js';

const program = new Command();
program
  .name('portkey-ca-setup')
  .version(packageJson.version)
  .description('Configure Portkey Agent Skills for AI platforms');

// ---------------------------------------------------------------------------
// claude
// ---------------------------------------------------------------------------
program
  .command('claude')
  .description('Setup for Claude Desktop')
  .option('--config-path <path>', 'Custom config file path')
  .option('--server-path <path>', 'Custom MCP server path')
  .option('--force', 'Overwrite existing entry')
  .action((opts) => {
    setupClaude({
      configPath: opts.configPath,
      serverPath: opts.serverPath,
      force: opts.force,
    });
  });

// ---------------------------------------------------------------------------
// cursor
// ---------------------------------------------------------------------------
program
  .command('cursor')
  .description('Setup for Cursor IDE')
  .option('--global', 'Global config instead of project-level')
  .option('--config-path <path>', 'Custom config file path')
  .option('--server-path <path>', 'Custom MCP server path')
  .option('--force', 'Overwrite existing entry')
  .action((opts) => {
    setupCursor({
      configPath: opts.configPath,
      serverPath: opts.serverPath,
      force: opts.force,
      global: opts.global,
    });
  });

// ---------------------------------------------------------------------------
// ironclaw
// ---------------------------------------------------------------------------
program
  .command('ironclaw')
  .description('Setup trusted skill and MCP server for IronClaw')
  .option('--mcp-config-path <path>', 'Custom IronClaw MCP config path')
  .option('--skills-dir <path>', 'Custom IronClaw trusted skills directory')
  .option('--server-path <path>', 'Custom MCP server path')
  .option('--force', 'Overwrite existing entry')
  .action((opts) => {
    setupIronclaw({
      mcpConfigPath: opts.mcpConfigPath,
      skillsDir: opts.skillsDir,
      serverPath: opts.serverPath,
      force: opts.force,
    });
  });

// ---------------------------------------------------------------------------
// openclaw
// ---------------------------------------------------------------------------
program
  .command('openclaw')
  .description('Generate or merge OpenClaw config')
  .option('--config-path <path>', 'Merge into existing OpenClaw config')
  .option('--cwd <dir>', 'Override working directory')
  .option('--force', 'Overwrite existing entries')
  .action((opts) => {
    setupOpenClaw({
      configPath: opts.configPath,
      cwd: opts.cwd,
      force: opts.force,
    });
  });

// ---------------------------------------------------------------------------
// list
// ---------------------------------------------------------------------------
program
  .command('list')
  .description('Check configuration status across platforms')
  .action(() => {
    const paths = getPlatformPaths();

    console.log('Portkey CA Agent Skills — Configuration Status\n');

    // MCP platforms
    const mcpChecks = [
      { name: 'Claude Desktop', path: paths.claude },
      { name: 'Cursor (global)', path: paths.cursorGlobal },
      { name: 'Cursor (project)', path: paths.cursorProject },
    ];

    for (const { name, path: configPath } of mcpChecks) {
      const exists = fs.existsSync(configPath);
      if (!exists) {
        console.log(`  ${name}: [NOT FOUND] ${configPath}`);
        continue;
      }
      const config = readJsonFile(configPath);
      const servers = config.mcpServers as Record<string, unknown> | undefined;
      const hasPortkey = servers && SERVER_NAME in servers;
      console.log(
        `  ${name}: ${hasPortkey ? '[CONFIGURED]' : '[EXISTS, NOT CONFIGURED]'} ${configPath}`,
      );
    }

    // OpenClaw
    const resolvedOpenclawPath = path.join(getPackageRoot(), 'openclaw.json');
    const openclawExists = fs.existsSync(resolvedOpenclawPath);
    if (openclawExists) {
      const oc = readJsonFile(resolvedOpenclawPath);
      const toolCount = Array.isArray(oc.tools) ? oc.tools.length : 0;
      console.log(`  OpenClaw: [AVAILABLE] ${toolCount} tools defined — ${resolvedOpenclawPath}`);
    } else {
      console.log(`  OpenClaw: [NOT FOUND] ${resolvedOpenclawPath}`);
    }

    const ironclawMcpPath = getIronclawMcpConfigPath();
    const ironclawSkillsDir = getIronclawSkillsDir();
    const ironclawSkillPath = getIronclawSkillInstallPath(ironclawSkillsDir);
    const ironclawMcpExists = fs.existsSync(ironclawMcpPath);
    const ironclawConfig = ironclawMcpExists ? readJsonFile(ironclawMcpPath) : null;
    const ironclawHasPortkey = Array.isArray(ironclawConfig?.servers)
      ? ironclawConfig.servers.some((server: any) => server?.name === SERVER_NAME)
      : false;
    const ironclawSkillExists = fs.existsSync(ironclawSkillPath);
    console.log(
      `  IronClaw: ${ironclawHasPortkey || ironclawSkillExists ? '[CONFIGURED]' : '[NOT CONFIGURED]'} MCP=${ironclawMcpPath} skill=${ironclawSkillPath}`,
    );

    console.log('');
  });

// ---------------------------------------------------------------------------
// uninstall
// ---------------------------------------------------------------------------
program
  .command('uninstall <platform>')
  .description('Remove Portkey config from a platform (claude, cursor, ironclaw, openclaw)')
  .option('--global', 'Target global Cursor config')
  .option('--config-path <path>', 'Custom config file path')
  .option('--mcp-config-path <path>', 'Custom IronClaw MCP config path')
  .option('--skills-dir <path>', 'Custom IronClaw trusted skills directory')
  .action((platform, opts) => {
    const paths = getPlatformPaths();

    if (platform === 'ironclaw') {
      uninstallIronclaw({
        mcpConfigPath: opts.mcpConfigPath,
        skillsDir: opts.skillsDir,
      });
      return;
    }

    // --- OpenClaw: remove tools by name prefix from a config file ---
    if (platform === 'openclaw') {
      if (!opts.configPath) {
        console.error('[ERROR] OpenClaw uninstall requires --config-path <path>');
        process.exit(1);
      }
      if (!fs.existsSync(opts.configPath)) {
        console.log(`[SKIP] Config not found: ${opts.configPath}`);
        return;
      }
      const config = readJsonFile(opts.configPath);
      const tools = config.tools as { name?: string }[] | undefined;
      if (!Array.isArray(tools) || tools.length === 0) {
        console.log(`[SKIP] No tools found in ${opts.configPath}`);
        return;
      }
      const before = tools.length;
      config.tools = tools.filter((t) => !t.name?.startsWith('portkey-'));
      const removed = before - (config.tools as unknown[]).length;
      if (removed === 0) {
        console.log(`[SKIP] No Portkey tools found in ${opts.configPath}`);
        return;
      }
      writeJsonFile(opts.configPath, config);
      console.log(`[REMOVED] ${removed} Portkey tools from ${opts.configPath}`);
      return;
    }

    // --- MCP platforms: claude, cursor ---
    let configPath: string;
    if (opts.configPath) {
      configPath = opts.configPath;
    } else if (platform === 'claude') {
      configPath = paths.claude;
    } else if (platform === 'cursor') {
      configPath = opts.global ? paths.cursorGlobal : paths.cursorProject;
    } else {
      console.error(`[ERROR] Unknown platform: ${platform}. Use "claude", "cursor", "ironclaw", or "openclaw".`);
      process.exit(1);
    }

    if (!fs.existsSync(configPath)) {
      console.log(`[SKIP] Config not found: ${configPath}`);
      return;
    }

    const config = readJsonFile(configPath);
    const servers = config.mcpServers as Record<string, unknown> | undefined;

    if (!servers || !(SERVER_NAME in servers)) {
      console.log(`[SKIP] "${SERVER_NAME}" not found in ${configPath}`);
      return;
    }

    delete servers[SERVER_NAME];
    writeJsonFile(configPath, config);
    console.log(`[REMOVED] "${SERVER_NAME}" from ${configPath}`);
  });

program.parse();

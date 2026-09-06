import { afterEach, beforeEach, describe, expect, test } from 'bun:test';
import { existsSync, readFileSync, rmSync } from 'fs';
import { tmpdir } from 'os';
import { join } from 'path';
import {
  assertSafeIronclawSkillDir,
  getIronclawSkillInstallPath,
  setupIronclaw,
  uninstallIronclaw,
} from '../../bin/platforms/ironclaw';

describe('IronClaw setup workflow', () => {
  let testRoot = '';
  let mcpConfigPath = '';
  let skillsDir = '';

  beforeEach(() => {
    testRoot = join(tmpdir(), `awaken-ironclaw-${Date.now()}-${Math.random()}`);
    mcpConfigPath = join(testRoot, '.ironclaw', 'mcp-servers.json');
    skillsDir = join(testRoot, '.ironclaw', 'skills');
  });

  afterEach(() => {
    if (testRoot && existsSync(testRoot)) {
      rmSync(testRoot, { recursive: true, force: true });
    }
  });

  test('setup writes trusted skill and MCP config without creating installed_skills', () => {
    const result = setupIronclaw({
      mcpConfigPath,
      skillsDir,
      serverPath: '/custom/server.ts',
    });

    const installedSkillPath = getIronclawSkillInstallPath(skillsDir);
    expect(result.mcpAction).toBe('created');
    expect(result.skillAction).toBe('created');
    expect(existsSync(mcpConfigPath)).toBeTrue();
    expect(existsSync(installedSkillPath)).toBeTrue();
    expect(existsSync(join(testRoot, '.ironclaw', 'installed_skills'))).toBeFalse();
    expect(readFileSync(installedSkillPath, 'utf8')).toContain('awaken-agent-skills');
  });

  test('re-running setup without force keeps a single MCP entry and skill file', () => {
    setupIronclaw({ mcpConfigPath, skillsDir, serverPath: '/custom/server.ts' });
    const second = setupIronclaw({ mcpConfigPath, skillsDir, serverPath: '/custom/server.ts' });

    const config = JSON.parse(readFileSync(mcpConfigPath, 'utf8')) as {
      servers: Array<{ name: string }>;
    };
    expect(second.mcpAction).toBe('skipped');
    expect(second.skillAction).toBe('skipped');
    expect(config.servers.filter(server => server.name === 'awaken-agent-kit')).toHaveLength(1);
  });

  test('uninstall removes both the trusted skill and MCP entry', () => {
    setupIronclaw({ mcpConfigPath, skillsDir, serverPath: '/custom/server.ts' });

    const result = uninstallIronclaw({ mcpConfigPath, skillsDir });
    const installedSkillPath = getIronclawSkillInstallPath(skillsDir);

    expect(result.mcpRemoved).toBe(true);
    expect(result.skillRemoved).toBe(true);
    expect(existsSync(installedSkillPath)).toBeFalse();
    expect(JSON.parse(readFileSync(mcpConfigPath, 'utf8')).servers).toHaveLength(0);
  });

  test('defensive removal rejects unexpected skill paths', () => {
    const unexpectedSkillDir = join(testRoot, 'unexpected', 'awaken-agent-skills');

    expect(() => assertSafeIronclawSkillDir(skillsDir, unexpectedSkillDir)).toThrow(
      'Refusing to remove unexpected IronClaw skill path',
    );
  });
});

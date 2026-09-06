import { afterEach, describe, expect, test } from 'bun:test';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {
  checkForUpdates,
  compareSemver,
  getVersionDiffLevel,
  isCacheFresh,
  maybePrintUpdateReminder,
  renderHumanSummary,
  renderReminderLines,
} from './update-check.ts';
import type { UpdateCheckResult } from './update-types.ts';

function createTempDir(): string {
  return mkdtempSync(path.join(os.tmpdir(), 'aelf-skills-update-check-'));
}

function createMockFetch(routes: Record<string, { status: number; body: unknown }>): typeof fetch {
  return (async (input: string | URL) => {
    const key = String(input);
    const route = routes[key];
    if (!route) {
      return new Response(JSON.stringify({ error: `unmocked route ${key}` }), { status: 404 });
    }
    return new Response(JSON.stringify(route.body), {
      status: route.status,
      headers: { 'content-type': 'application/json' },
    });
  }) as typeof fetch;
}

function setEnv(name: string, value?: string): void {
  if (value === undefined) {
    delete process.env[name];
    return;
  }
  process.env[name] = value;
}

afterEach(() => {
  delete process.env.AELF_SKILLS_UPDATE_CHECK;
});

describe('update-check semver helpers', () => {
  test('compares semver correctly', () => {
    expect(compareSemver('1.2.3', '1.2.4')).toBeLessThan(0);
    expect(compareSemver('2.0.0', '1.9.9')).toBeGreaterThan(0);
    expect(compareSemver('1.2.3', '1.2.3')).toBe(0);
  });

  test('detects diff level', () => {
    expect(getVersionDiffLevel('1.2.3', '2.0.0')).toBe('major');
    expect(getVersionDiffLevel('1.2.3', '1.3.0')).toBe('minor');
    expect(getVersionDiffLevel('1.2.3', '1.2.4')).toBe('patch');
    expect(getVersionDiffLevel('1.2.3', '1.2.3')).toBe('none');
    expect(getVersionDiffLevel('1.2.3-alpha.1', 'invalid')).toBe('unknown');
  });

  test('cache freshness respects ttl', () => {
    const checkedAt = '2026-03-05T00:00:00.000Z';
    expect(isCacheFresh(checkedAt, 24, new Date('2026-03-05T23:59:59.000Z'))).toBeTrue();
    expect(isCacheFresh(checkedAt, 24, new Date('2026-03-06T00:00:00.001Z'))).toBeFalse();
  });
});

describe('update-check live flow', () => {
  test('uses github compare fallback when release tag is missing', async () => {
    const tempDir = createTempDir();
    try {
      const packageJsonPath = path.join(tempDir, 'package.json');
      const catalogPath = path.join(tempDir, 'skills-catalog.json');
      const cachePath = path.join(tempDir, 'cache.json');

      writeFileSync(
        packageJsonPath,
        JSON.stringify(
          {
            name: '@blockchain-forever/aelf-skills',
            version: '0.1.1',
            repository: { url: 'https://github.com/AElfProject/aelf-skills.git' },
          },
          null,
          2,
        ),
      );

      writeFileSync(
        catalogPath,
        JSON.stringify(
          {
            schemaVersion: '1.3.0',
            generatedAt: '2026-03-05T00:00:00.000Z',
            source: 'test',
            warnings: [],
            skills: [
              {
                id: 'awaken-agent-skills',
                displayName: 'Awaken',
                npm: {
                  name: '@awaken-finance/agent-kit',
                  version: '1.2.3',
                },
                repository: {
                  https: 'https://github.com/Awaken-Finance/awaken-agent-skills',
                },
                description: 'test',
                capabilities: ['swap'],
                artifacts: {
                  skillMd: true,
                  mcpServer: true,
                  openclaw: true,
                },
                setupCommands: {
                  install: 'bun install',
                },
                clientSupport: {
                  openclaw: 'native',
                  cursor: 'native-setup',
                  claude_desktop: 'native-setup',
                  ironclaw: 'native-setup',
                  claude_code: 'manual',
                  codex: 'manual',
                },
                openclawToolCount: 1,
              },
            ],
          },
          null,
          2,
        ),
      );

      const mockFetch = createMockFetch({
        'https://registry.npmjs.org/%40blockchain-forever%2Faelf-skills': {
          status: 200,
          body: { 'dist-tags': { latest: '0.1.2' } },
        },
        'https://registry.npmjs.org/%40awaken-finance%2Fagent-kit': {
          status: 200,
          body: { 'dist-tags': { latest: '2.0.0' } },
        },
        'https://api.github.com/repos/AElfProject/aelf-skills/releases/tags/v0.1.2': {
          status: 404,
          body: {},
        },
        'https://api.github.com/repos/AElfProject/aelf-skills/releases/tags/0.1.2': {
          status: 404,
          body: {},
        },
        'https://api.github.com/repos/Awaken-Finance/awaken-agent-skills/releases/tags/v2.0.0': {
          status: 404,
          body: {},
        },
        'https://api.github.com/repos/Awaken-Finance/awaken-agent-skills/releases/tags/2.0.0': {
          status: 404,
          body: {},
        },
      });

      const result = await checkForUpdates({
        force: true,
        allowWhenDisabled: true,
        packageJsonPath,
        catalogPath,
        cachePath,
        ttlHours: 24,
        now: () => new Date('2026-03-05T01:00:00.000Z'),
        fetchImpl: mockFetch,
      });

      expect(result).not.toBeNull();
      if (!result) return;

      expect(result.hasUpdates).toBeTrue();
      expect(result.hub.outdated).toBeTrue();
      expect(result.hub.latestVersion).toBe('0.1.2');
      expect(result.catalogOutdated.length).toBe(1);
      expect(result.catalogOutdated[0].diffLevel).toBe('major');
      expect(result.catalogOutdated[0].release?.source).toBe('github-compare');
      expect(result.catalogOutdated[0].release?.url).toContain('/compare/v1.2.3...v2.0.0');
    } finally {
      rmSync(tempDir, { recursive: true, force: true });
    }
  });

  test('falls back to cache on catastrophic read failure', async () => {
    const tempDir = createTempDir();
    try {
      const cachePath = path.join(tempDir, 'cache.json');
      const cached: UpdateCheckResult = {
        checkedAt: '2026-03-05T00:00:00.000Z',
        fromCache: false,
        hasUpdates: true,
        hub: {
          packageName: '@blockchain-forever/aelf-skills',
          currentVersion: '0.1.1',
          latestVersion: '0.1.2',
          outdated: true,
          diffLevel: 'minor',
        },
        catalogOutdated: [],
        notesDigest: [],
        sourceStatus: {
          npm: 'ok',
          github: 'ok',
          errors: [],
        },
      };
      writeFileSync(cachePath, JSON.stringify(cached, null, 2));

      const result = await checkForUpdates({
        force: true,
        allowWhenDisabled: true,
        packageJsonPath: path.join(tempDir, 'missing-package.json'),
        cachePath,
      });

      expect(result).not.toBeNull();
      if (!result) return;
      expect(result.fromCache).toBeTrue();
      expect(result.hasUpdates).toBeTrue();
      expect(result.sourceStatus.errors.join('\n')).toContain('fallback to cache');
    } finally {
      rmSync(tempDir, { recursive: true, force: true });
    }
  });

  test('hub up-to-date with mixed catalog versions only returns outdated skills', async () => {
    const tempDir = createTempDir();
    try {
      const packageJsonPath = path.join(tempDir, 'package.json');
      const catalogPath = path.join(tempDir, 'skills-catalog.json');
      const cachePath = path.join(tempDir, 'cache.json');

      writeFileSync(
        packageJsonPath,
        JSON.stringify(
          {
            name: '@blockchain-forever/aelf-skills',
            version: '0.1.1',
            repository: { url: 'https://github.com/AElfProject/aelf-skills.git' },
          },
          null,
          2,
        ),
      );

      writeFileSync(
        catalogPath,
        JSON.stringify(
          {
            schemaVersion: '1.3.0',
            generatedAt: '2026-03-05T00:00:00.000Z',
            source: 'test',
            warnings: [],
            skills: [
              {
                id: 'skill-old',
                displayName: 'Skill Old',
                npm: { name: '@demo/skill-old', version: '1.0.0' },
                repository: { https: 'https://github.com/demo/skill-old' },
                description: 'old',
                capabilities: ['x'],
                artifacts: { skillMd: true, mcpServer: true, openclaw: true },
                setupCommands: { install: 'bun install' },
                clientSupport: {
                  openclaw: 'native',
                  cursor: 'native-setup',
                  claude_desktop: 'native-setup',
                  ironclaw: 'native-setup',
                  claude_code: 'manual',
                  codex: 'manual',
                },
                openclawToolCount: 1,
              },
              {
                id: 'skill-ok',
                displayName: 'Skill Ok',
                npm: { name: '@demo/skill-ok', version: '2.1.0' },
                repository: { https: 'https://github.com/demo/skill-ok' },
                description: 'ok',
                capabilities: ['y'],
                artifacts: { skillMd: true, mcpServer: true, openclaw: true },
                setupCommands: { install: 'bun install' },
                clientSupport: {
                  openclaw: 'native',
                  cursor: 'native-setup',
                  claude_desktop: 'native-setup',
                  ironclaw: 'native-setup',
                  claude_code: 'manual',
                  codex: 'manual',
                },
                openclawToolCount: 1,
              },
            ],
          },
          null,
          2,
        ),
      );

      const mockFetch = createMockFetch({
        'https://registry.npmjs.org/%40blockchain-forever%2Faelf-skills': {
          status: 200,
          body: { 'dist-tags': { latest: '0.1.1' } },
        },
        'https://registry.npmjs.org/%40demo%2Fskill-old': {
          status: 200,
          body: { 'dist-tags': { latest: '1.1.0' } },
        },
        'https://registry.npmjs.org/%40demo%2Fskill-ok': {
          status: 200,
          body: { 'dist-tags': { latest: '2.1.0' } },
        },
        'https://api.github.com/repos/demo/skill-old/releases/tags/v1.1.0': {
          status: 404,
          body: {},
        },
        'https://api.github.com/repos/demo/skill-old/releases/tags/1.1.0': {
          status: 404,
          body: {},
        },
      });

      const result = await checkForUpdates({
        force: true,
        allowWhenDisabled: true,
        packageJsonPath,
        catalogPath,
        cachePath,
        fetchImpl: mockFetch,
      });

      expect(result).not.toBeNull();
      if (!result) return;
      expect(result.hub.outdated).toBeFalse();
      expect(result.hasUpdates).toBeTrue();
      expect(result.catalogOutdated.length).toBe(1);
      expect(result.catalogOutdated[0].id).toBe('skill-old');
    } finally {
      rmSync(tempDir, { recursive: true, force: true });
    }
  });

  test('returns null when update check is disabled by env', async () => {
    const tempDir = createTempDir();
    try {
      const packageJsonPath = path.join(tempDir, 'package.json');
      writeFileSync(
        packageJsonPath,
        JSON.stringify({ name: '@blockchain-forever/aelf-skills', version: '0.1.1' }, null, 2),
      );
      setEnv('AELF_SKILLS_UPDATE_CHECK', '0');

      const result = await checkForUpdates({
        packageJsonPath,
      });

      expect(result).toBeNull();
    } finally {
      rmSync(tempDir, { recursive: true, force: true });
    }
  });
});

describe('update-check rendering', () => {
  test('renders human summary and reminder lines', () => {
    const result: UpdateCheckResult = {
      checkedAt: '2026-03-05T00:00:00.000Z',
      fromCache: false,
      hasUpdates: true,
      hub: {
        packageName: '@blockchain-forever/aelf-skills',
        currentVersion: '0.1.1',
        latestVersion: '0.1.2',
        outdated: true,
        diffLevel: 'minor',
        release: {
          source: 'github-release',
          summary: 'Hub update summary',
          url: 'https://github.com/AElfProject/aelf-skills/releases/tag/v0.1.2',
        },
      },
      catalogOutdated: [
        {
          id: 'awaken-agent-skills',
          packageName: '@awaken-finance/agent-kit',
          currentVersion: '1.2.3',
          latestVersion: '1.5.0',
          diffLevel: 'minor',
          release: {
            source: 'github-compare',
            summary: '1.2.3 -> 1.5.0',
            url: 'https://github.com/Awaken-Finance/awaken-agent-skills/compare/v1.2.3...v1.5.0',
          },
        },
      ],
      notesDigest: [],
      sourceStatus: {
        npm: 'ok',
        github: 'ok',
        errors: [],
      },
    };

    const summary = renderHumanSummary(result);
    expect(summary).toContain('Hub: @blockchain-forever/aelf-skills 0.1.1 -> 0.1.2');
    expect(summary).toContain('Outdated skill packages: 1');
    expect(summary).toContain('awaken-agent-skills');

    const reminder = renderReminderLines(result);
    expect(reminder.length).toBeGreaterThan(0);
    expect(reminder.join('\n')).toContain('aelf-skills hub update available');
    expect(reminder.join('\n')).toContain('./bootstrap.sh --source npm');
  });

  test('suppresses reminder when already notified within ttl window', async () => {
    const tempDir = createTempDir();
    try {
      const cachePath = path.join(tempDir, 'cache.json');
      const cached: UpdateCheckResult = {
        checkedAt: '2026-03-05T00:00:00.000Z',
        fromCache: false,
        hasUpdates: true,
        lastNotifiedAt: '2026-03-05T10:00:00.000Z',
        hub: {
          packageName: '@blockchain-forever/aelf-skills',
          currentVersion: '0.1.1',
          latestVersion: '0.1.2',
          outdated: true,
          diffLevel: 'minor',
        },
        catalogOutdated: [],
        notesDigest: [],
        sourceStatus: {
          npm: 'ok',
          github: 'ok',
          errors: [],
        },
      };
      writeFileSync(cachePath, JSON.stringify(cached, null, 2));

      const logs: string[] = [];
      const rawLog = console.log;
      console.log = (...args: unknown[]) => {
        logs.push(args.map(v => String(v)).join(' '));
      };
      try {
        await maybePrintUpdateReminder({
          allowWhenDisabled: true,
          cachePath,
          ttlHours: 24,
          now: () => new Date('2026-03-05T12:00:00.000Z'),
        });
      } finally {
        console.log = rawLog;
      }

      expect(logs.length).toBe(0);
    } finally {
      rmSync(tempDir, { recursive: true, force: true });
    }
  });

  test('renders reminder when hub is up-to-date but catalog has outdated skills', () => {
    const result: UpdateCheckResult = {
      checkedAt: '2026-03-05T00:00:00.000Z',
      fromCache: false,
      hasUpdates: true,
      hub: {
        packageName: '@blockchain-forever/aelf-skills',
        currentVersion: '0.1.1',
        latestVersion: '0.1.1',
        outdated: false,
        diffLevel: 'none',
      },
      catalogOutdated: [
        {
          id: 'awaken-agent-skills',
          packageName: '@awaken-finance/agent-kit',
          currentVersion: '1.2.3',
          latestVersion: '1.5.0',
          diffLevel: 'minor',
        },
      ],
      notesDigest: [],
      sourceStatus: {
        npm: 'ok',
        github: 'ok',
        errors: [],
      },
    };

    const lines = renderReminderLines(result);
    expect(lines.join('\n')).not.toContain('hub update available');
    expect(lines.join('\n')).toContain('1 skill package update(s)');
    expect(lines.join('\n')).toContain('./bootstrap.sh --source npm');
  });
});

import { afterEach, describe, expect, test } from 'bun:test';
import path from 'node:path';
import { buildCatalog } from './catalog.ts';

const PREVIOUS_SKILLS_BASE = process.env.SKILLS_BASE;
const ROOT_DIR = path.resolve(import.meta.dir, '..', '..');
const FIXTURE_ROOT = path.join(ROOT_DIR, 'testdata');
const FIXTURE_WORKSPACE = path.join(FIXTURE_ROOT, 'workspace.ci.json');

afterEach(() => {
  if (PREVIOUS_SKILLS_BASE === undefined) {
    delete process.env.SKILLS_BASE;
    return;
  }
  process.env.SKILLS_BASE = PREVIOUS_SKILLS_BASE;
});

describe('catalog distribution contract', () => {
  test('buildCatalog emits machine-readable discovery and activation fields', () => {
    process.env.SKILLS_BASE = FIXTURE_ROOT;

    const catalog = buildCatalog({
      workspacePath: FIXTURE_WORKSPACE,
      includeLocalPaths: true,
    });

    const coreSkill = catalog.skills.find(skill => skill.id === 'fixture-core-skill');
    const nodeSkill = catalog.skills.find(skill => skill.id === 'fixture-node-skill');

    expect(coreSkill).toBeDefined();
    expect(nodeSkill).toBeDefined();

    expect(coreSkill?.distributionSources).toEqual(
      expect.objectContaining({
        npmPackage: '@fixture/core-skill',
      }),
    );
    expect(coreSkill?.clientInstall.openclaw).toEqual({
      source: 'npm',
      mode: 'package-setup',
      installCommand: 'bunx -p @fixture/core-skill fixture-core-setup openclaw',
    });
    expect(coreSkill?.clientInstall.ironclaw).toEqual({
      source: 'npm',
      mode: 'trusted-local-install',
      installCommand: 'bunx -p @fixture/core-skill fixture-core-setup ironclaw',
      requiresTrustPromotion: true,
    });

    expect(nodeSkill?.distributionSources).toEqual(
      expect.objectContaining({
        npmPackage: '@fixture/node-skill',
      }),
    );
    expect(nodeSkill?.dependsOn).toEqual(['fixture-core-skill']);
    expect(nodeSkill?.clientInstall.openclaw.installCommand).toBe(
      'bunx -p @fixture/node-skill fixture-node-setup openclaw',
    );
    expect(nodeSkill?.clientInstall.ironclaw.installCommand).toBe(
      'bunx -p @fixture/node-skill fixture-node-setup ironclaw',
    );
  });
});

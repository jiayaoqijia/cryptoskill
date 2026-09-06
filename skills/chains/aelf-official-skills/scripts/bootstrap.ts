import { cpSync, existsSync, mkdirSync, mkdtempSync, rmSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import type { SkillCatalogEntry, SkillsCatalog } from './lib/types.ts';
import { parseCsv, readJsonFile, requireCommand, runCommand } from './lib/utils.ts';
import { buildCatalog, writeCatalogArtifacts } from './lib/catalog.ts';
import { printHealthReport, runHealthCheck } from './lib/health.ts';
import { maybePrintUpdateReminder } from './lib/update-check.ts';

type SourceMode = 'auto' | 'npm' | 'github' | 'local';

interface CliOptions {
  catalogPath?: string;
  dest: string;
  source: SourceMode;
  skipInstall: boolean;
  skipHealth: boolean;
  onlyIds: string[];
}

interface SkillRunResult {
  id: string;
  download: 'ok' | 'failed';
  downloadMethod?: 'npm' | 'github' | 'local';
  install: 'ok' | 'skipped' | 'failed';
  issues: string[];
}

function parseArgs(): CliOptions {
  const args = process.argv.slice(2);

  let catalogPath: string | undefined;
  let dest = path.resolve(process.cwd(), 'downloaded-skills');
  let source: SourceMode = 'auto';
  let skipInstall = false;
  let skipHealth = false;
  let only = '';

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];

    if (arg === '--catalog' && args[i + 1]) {
      catalogPath = path.resolve(process.cwd(), args[i + 1]);
      i += 1;
      continue;
    }

    if (arg === '--dest' && args[i + 1]) {
      dest = path.resolve(process.cwd(), args[i + 1]);
      i += 1;
      continue;
    }

    if (arg === '--source' && args[i + 1]) {
      const next = args[i + 1] as SourceMode;
      if (next === 'auto' || next === 'npm' || next === 'github' || next === 'local') {
        source = next;
      } else {
        throw new Error(`Invalid --source value: ${args[i + 1]}. Use auto|npm|github|local.`);
      }
      i += 1;
      continue;
    }

    if (arg === '--skip-install') {
      skipInstall = true;
      continue;
    }

    if (arg === '--skip-health') {
      skipHealth = true;
      continue;
    }

    if (arg === '--only' && args[i + 1]) {
      only = args[i + 1];
      i += 1;
      continue;
    }
  }

  return {
    catalogPath,
    dest,
    source,
    skipInstall,
    skipHealth,
    onlyIds: parseCsv(only),
  };
}

function ensureCatalogFile(catalogPath?: string): SkillsCatalog {
  const resolvedPath = catalogPath || path.join(process.cwd(), 'skills-catalog.json');

  if (!existsSync(resolvedPath)) {
    if (catalogPath) {
      throw new Error(`[FAIL] Catalog file not found: ${resolvedPath}`);
    }

    console.log('[INFO] skills-catalog.json not found. Generating...');
    const generated = buildCatalog();
    writeCatalogArtifacts(generated, { rootDir: process.cwd() });
  }

  return readJsonFile<SkillsCatalog>(resolvedPath);
}

function selectSkills(catalog: SkillsCatalog, onlyIds: string[]): SkillCatalogEntry[] {
  if (onlyIds.length === 0) return catalog.skills;

  const byId = new Map(catalog.skills.map(skill => [skill.id, skill]));
  const selected = onlyIds.map(id => byId.get(id)).filter((skill): skill is SkillCatalogEntry => Boolean(skill));
  const missing = onlyIds.filter(id => !byId.has(id));

  if (missing.length > 0) {
    console.log(`[WARN] Unknown skill IDs in --only: ${missing.join(', ')}`);
  }

  if (selected.length === 0) {
    return [];
  }

  return resolveDependencyClosure(selected, byId);
}

function resolveDependencyClosure(
  roots: SkillCatalogEntry[],
  byId: Map<string, SkillCatalogEntry>,
): SkillCatalogEntry[] {
  const order: SkillCatalogEntry[] = [];
  const status = new Map<string, 'visiting' | 'visited'>();
  const stack: string[] = [];
  const errors: string[] = [];

  const visit = (skill: SkillCatalogEntry): void => {
    const current = status.get(skill.id);
    if (current === 'visited') return;

    if (current === 'visiting') {
      const cycleStart = stack.indexOf(skill.id);
      const cyclePath = [...stack.slice(cycleStart), skill.id].join(' -> ');
      errors.push(`[FAIL] Dependency cycle detected: ${cyclePath}`);
      return;
    }

    status.set(skill.id, 'visiting');
    stack.push(skill.id);

    for (const depId of skill.dependsOn || []) {
      const depSkill = byId.get(depId);
      if (!depSkill) {
        errors.push(`[FAIL] ${skill.id}: dependsOn references unknown skill id "${depId}"`);
        continue;
      }
      visit(depSkill);
    }

    stack.pop();
    status.set(skill.id, 'visited');

    if (!order.some(item => item.id === skill.id)) {
      order.push(skill);
    }
  };

  for (const root of roots) {
    visit(root);
  }

  if (errors.length > 0) {
    throw new Error(errors.join('\n'));
  }

  return order;
}

function validatePrerequisites(source: SourceMode, skipInstall: boolean): void {
  if (source === 'auto' || source === 'npm') {
    requireCommand('npm');
    requireCommand('tar');
  }

  if (source === 'auto' || source === 'github') {
    requireCommand('git');
  }

  if (!skipInstall) {
    requireCommand('bun');
  }
}

function downloadSkill(skill: SkillCatalogEntry, destRoot: string, source: SourceMode): SkillRunResult {
  const targetDir = path.join(destRoot, skill.id);
  const result: SkillRunResult = {
    id: skill.id,
    download: 'failed',
    install: 'skipped',
    issues: [],
  };

  rmSync(targetDir, { recursive: true, force: true });
  mkdirSync(targetDir, { recursive: true });

  if (source === 'local') {
    const localResult = downloadViaLocal(skill, targetDir);
    if (!localResult.ok) {
      result.issues.push(localResult.message);
      return result;
    }
    result.download = 'ok';
    result.downloadMethod = 'local';
    return result;
  }

  if (source === 'npm') {
    const npmResult = downloadViaNpm(skill, targetDir);
    if (!npmResult.ok) {
      result.issues.push(npmResult.message);
      return result;
    }
    result.download = 'ok';
    result.downloadMethod = 'npm';
    return result;
  }

  if (source === 'github') {
    const gitResult = downloadViaGithub(skill, targetDir);
    if (!gitResult.ok) {
      result.issues.push(gitResult.message);
      return result;
    }
    result.download = 'ok';
    result.downloadMethod = 'github';
    return result;
  }

  const npmResult = downloadViaNpm(skill, targetDir);
  if (npmResult.ok) {
    result.download = 'ok';
    result.downloadMethod = 'npm';
    return result;
  }

  result.issues.push(`npm failed: ${npmResult.message}`);

  rmSync(targetDir, { recursive: true, force: true });
  mkdirSync(targetDir, { recursive: true });

  const gitResult = downloadViaGithub(skill, targetDir);
  if (gitResult.ok) {
    result.download = 'ok';
    result.downloadMethod = 'github';
    return result;
  }

  result.issues.push(`github failed: ${gitResult.message}`);
  return result;
}

function downloadViaLocal(skill: SkillCatalogEntry, targetDir: string): { ok: boolean; message: string } {
  if (!skill.sourcePath) {
    return {
      ok: false,
      message: 'sourcePath is missing; use local-path catalog or choose npm/github source',
    };
  }

  if (!existsSync(skill.sourcePath)) {
    return {
      ok: false,
      message: `sourcePath not found: ${skill.sourcePath}`,
    };
  }

  cpSync(skill.sourcePath, targetDir, { recursive: true });
  return {
    ok: true,
    message: `copied from local source: ${skill.sourcePath}`,
  };
}

function downloadViaNpm(skill: SkillCatalogEntry, targetDir: string): { ok: boolean; message: string } {
  const tmpDir = mkdtempSync(path.join(os.tmpdir(), 'aelf-skills-pack-'));
  const packageRef = `${skill.npm.name}@${skill.npm.version}`;

  const packResult = runCommand('npm', ['pack', packageRef, '--pack-destination', tmpDir]);
  if (!packResult.ok) {
    return {
      ok: false,
      message: packResult.stderr || packResult.stdout || `npm pack failed for ${packageRef}`,
    };
  }

  const lines = packResult.stdout
    .split(/\r?\n/)
    .map(value => value.trim())
    .filter(Boolean);
  const tarballName = lines[lines.length - 1];
  const tarballPath = path.join(tmpDir, tarballName);

  const extractResult = runCommand('tar', ['-xzf', tarballPath, '-C', targetDir, '--strip-components=1']);
  if (!extractResult.ok) {
    return {
      ok: false,
      message: extractResult.stderr || extractResult.stdout || `tar extract failed for ${packageRef}`,
    };
  }

  rmSync(tmpDir, { recursive: true, force: true });

  return {
    ok: true,
    message: `downloaded via npm: ${packageRef}`,
  };
}

function downloadViaGithub(skill: SkillCatalogEntry, targetDir: string): { ok: boolean; message: string } {
  if (!skill.repository.https) {
    return {
      ok: false,
      message: 'repository.https is missing',
    };
  }

  const cloneResult = runCommand('git', ['clone', '--depth', '1', skill.repository.https, targetDir]);
  if (!cloneResult.ok) {
    return {
      ok: false,
      message: cloneResult.stderr || cloneResult.stdout || `git clone failed for ${skill.repository.https}`,
    };
  }

  return {
    ok: true,
    message: `downloaded via github: ${skill.repository.https}`,
  };
}

function installSkillDependencies(skillDir: string): { ok: boolean; message: string } {
  const installResult = runCommand('bun', ['install'], skillDir);
  if (!installResult.ok) {
    return {
      ok: false,
      message: installResult.stderr || installResult.stdout || 'bun install failed',
    };
  }

  return {
    ok: true,
    message: 'bun install completed',
  };
}

function printBootstrapSummary(results: SkillRunResult[]): void {
  console.log('\n[Bootstrap] Result matrix');
  console.log('| Skill ID | Download | Method | Install |');
  console.log('|---|---|---|---|');

  for (const row of results) {
    console.log(
      `| ${row.id} | ${row.download.toUpperCase()} | ${row.downloadMethod || '-'} | ${row.install.toUpperCase()} |`,
    );
  }

  const failed = results.filter(row => row.download === 'failed' || row.install === 'failed');
  if (failed.length > 0) {
    console.log('\n[Bootstrap] Failures');
    for (const row of failed) {
      for (const issue of row.issues) {
        console.log(`  - ${row.id}: ${issue}`);
      }
    }
  }
}

async function main(): Promise<void> {
  try {
    await maybePrintUpdateReminder();

    const options = parseArgs();
    validatePrerequisites(options.source, options.skipInstall);

    const catalog = ensureCatalogFile(options.catalogPath);
    const selectedSkills = selectSkills(catalog, options.onlyIds);

    if (selectedSkills.length === 0) {
      console.log('[INFO] No skills selected. Nothing to do.');
      return;
    }

    mkdirSync(options.dest, { recursive: true });

    console.log(`[INFO] Destination: ${options.dest}`);
    console.log(`[INFO] Source mode: ${options.source}`);
    console.log(`[INFO] Skills selected (with dependencies): ${selectedSkills.length}`);

    const results: SkillRunResult[] = [];

    for (const skill of selectedSkills) {
      console.log(`\n[STEP] Downloading ${skill.id} ...`);
      const row = downloadSkill(skill, options.dest, options.source);

      if (row.download === 'ok' && !options.skipInstall) {
        console.log(`[STEP] Installing dependencies for ${skill.id} ...`);
        const installResult = installSkillDependencies(path.join(options.dest, skill.id));
        if (installResult.ok) {
          row.install = 'ok';
        } else {
          row.install = 'failed';
          row.issues.push(installResult.message);
        }
      }

      results.push(row);
    }

    printBootstrapSummary(results);

    let hasFailure = results.some(row => row.download === 'failed' || row.install === 'failed');

    if (!options.skipHealth) {
      const report = runHealthCheck(catalog, {
        skillsRoot: options.dest,
        onlyIds: selectedSkills.map(skill => skill.id),
      });

      printHealthReport(report);
      if (report.summary.fail > 0) {
        hasFailure = true;
      }
    }

    if (hasFailure) {
      process.exitCode = 1;
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.error(message.startsWith('[FAIL]') ? message : `[FAIL] ${message}`);
    process.exitCode = 1;
  }
}

void main();

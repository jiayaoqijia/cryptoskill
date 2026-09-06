import path from 'node:path';
import { existsSync } from 'node:fs';
import type { SkillCatalogEntry, SkillsCatalog } from './types.ts';
import { commandExists, readJsonFile } from './utils.ts';

interface PackageJsonLike {
  scripts?: Record<string, string>;
  bin?: string | Record<string, string>;
}

export interface SkillHealthResult {
  id: string;
  skillDir: string;
  status: 'pass' | 'warn' | 'fail';
  issues: string[];
  checks: {
    packageJson: boolean;
    setupScript: boolean;
    setupBin: boolean;
    mcpServer: boolean;
    openclawJson: boolean;
    cliScript: boolean;
  };
}

export interface HealthSummary {
  total: number;
  pass: number;
  warn: number;
  fail: number;
}

export interface HealthCheckReport {
  generatedAt: string;
  commandAvailability: Record<string, boolean>;
  summary: HealthSummary;
  results: SkillHealthResult[];
}

export interface RunHealthCheckOptions {
  skillsRoot?: string;
  onlyIds?: string[];
}

export function runHealthCheck(catalog: SkillsCatalog, options: RunHealthCheckOptions = {}): HealthCheckReport {
  const selected = selectSkills(catalog.skills, options.onlyIds || []);

  const commandAvailability: Record<string, boolean> = {
    bun: commandExists('bun'),
    npm: commandExists('npm'),
    git: commandExists('git'),
    tar: commandExists('tar'),
  };

  const results = selected.map(skill => checkSkill(skill, resolveSkillDir(skill, options.skillsRoot)));
  const summary = results.reduce(
    (acc, row) => {
      acc.total += 1;
      acc[row.status] += 1;
      return acc;
    },
    { total: 0, pass: 0, warn: 0, fail: 0 } as HealthSummary,
  );

  return {
    generatedAt: new Date().toISOString(),
    commandAvailability,
    summary,
    results,
  };
}

export function printHealthReport(report: HealthCheckReport): void {
  console.log('\n[Health Check] Command availability');
  for (const [name, ok] of Object.entries(report.commandAvailability)) {
    console.log(`  - ${name}: ${ok ? 'OK' : 'MISSING'}`);
  }

  console.log('\n[Health Check] Skill matrix');
  console.log('| Skill ID | Status | package.json | setup | setup-bin | MCP | OpenClaw | CLI |');
  console.log('|---|---|---:|---:|---:|---:|---:|---:|');

  for (const row of report.results) {
    console.log(
      `| ${row.id} | ${row.status.toUpperCase()} | ${toFlag(row.checks.packageJson)} | ${toFlag(row.checks.setupScript)} | ${toFlag(row.checks.setupBin)} | ${toFlag(row.checks.mcpServer)} | ${toFlag(row.checks.openclawJson)} | ${toFlag(row.checks.cliScript)} |`,
    );
  }

  const summary = report.summary;
  console.log(
    `\n[Health Check] Summary: total=${summary.total}, pass=${summary.pass}, warn=${summary.warn}, fail=${summary.fail}`,
  );

  const hasIssues = report.results.some(row => row.issues.length > 0);
  if (hasIssues) {
    console.log('\n[Health Check] Issues');
    for (const row of report.results) {
      if (row.issues.length === 0) continue;
      for (const issue of row.issues) {
        console.log(`  - ${row.id}: ${issue}`);
      }
    }
  }
}

function checkSkill(skill: SkillCatalogEntry, skillDir: string): SkillHealthResult {
  if (!skillDir) {
    return {
      id: skill.id,
      skillDir: '(unresolved)',
      status: 'fail',
      issues: ['local source path missing; provide --skills-root or use local-path catalog mode'],
      checks: {
        packageJson: false,
        setupScript: false,
        setupBin: false,
        mcpServer: false,
        openclawJson: false,
        cliScript: false,
      },
    };
  }

  const packagePath = path.join(skillDir, 'package.json');
  const mcpPath = path.join(skillDir, 'src', 'mcp', 'server.ts');
  const openclawPath = path.join(skillDir, 'openclaw.json');

  const checks = {
    packageJson: existsSync(packagePath),
    setupScript: false,
    setupBin: false,
    mcpServer: existsSync(mcpPath),
    openclawJson: existsSync(openclawPath),
    cliScript: false,
  };

  const issues: string[] = [];

  let pkgScripts: Record<string, string> = {};
  if (!checks.packageJson) {
    issues.push('package.json missing');
  } else {
    try {
      const pkg = readJsonFile<PackageJsonLike>(packagePath);
      pkgScripts = pkg.scripts || {};
      checks.setupScript =
        Boolean(pkgScripts.setup) ||
        existsSync(path.join(skillDir, 'bin', 'setup.ts')) ||
        existsSync(path.join(skillDir, 'bin', 'setup.js'));
      checks.setupBin = hasSetupBinary(pkg);
      checks.mcpServer = checks.mcpServer || Boolean(pkgScripts.mcp);
      checks.cliScript = Boolean(pkgScripts.cli);
    } catch {
      issues.push('package.json parse failed');
    }
  }

  validateExpectedSupport(skill, checks, issues);

  let status: SkillHealthResult['status'] = 'pass';
  if (issues.length > 0) {
    status = issues.some(
      issue => issue.includes('missing') || issue.includes('not executable'),
    )
      ? 'fail'
      : 'warn';
  }

  return {
    id: skill.id,
    skillDir,
    status,
    issues,
    checks,
  };
}

function validateExpectedSupport(
  skill: SkillCatalogEntry,
  checks: SkillHealthResult['checks'],
  issues: string[],
): void {
  if (skill.clientSupport.openclaw === 'native' && !checks.openclawJson) {
    issues.push('declared openclaw native but openclaw.json missing');
  }

  const needsSetup =
    skill.clientSupport.cursor === 'native-setup' ||
    skill.clientSupport.claude_desktop === 'native-setup' ||
    skill.clientSupport.ironclaw === 'native-setup';
  if (needsSetup && !checks.setupScript) {
    issues.push('declared native-setup but setup command not available');
  }
  if (needsSetup && !checks.setupBin) {
    issues.push('declared native-setup but npm installer bin is missing');
  }

  const needsMcp =
    skill.clientSupport.cursor !== 'unsupported' ||
    skill.clientSupport.claude_desktop !== 'unsupported' ||
    skill.clientSupport.ironclaw !== 'unsupported' ||
    skill.clientSupport.claude_code !== 'unsupported';
  if (needsMcp && !checks.mcpServer) {
    issues.push('MCP support declared but src/mcp/server.ts missing');
  }

  const needsCli = skill.clientSupport.codex === 'manual-cli-or-mcp';
  if (needsCli && !checks.mcpServer && !checks.cliScript) {
    issues.push('codex support declared but neither MCP nor CLI script is available');
  }

  if (skill.clientSupport.ironclaw === 'native-setup') {
    if (skill.clientInstall.ironclaw.mode !== 'trusted-local-install') {
      issues.push('ironclaw native-setup declared but clientInstall.ironclaw is not executable');
    }
    if (!skill.distributionSources.npmPackage) {
      issues.push('ironclaw native-setup declared but distributionSources.npmPackage missing');
    }
    if (!skill.clientInstall.ironclaw.installCommand) {
      issues.push('ironclaw native-setup declared but installCommand missing');
    }
  }

  if (skill.clientSupport.openclaw === 'native') {
    if (skill.clientInstall.openclaw.mode === 'managed-install') {
      if (!skill.distributionSources.clawhubId) {
        issues.push('openclaw managed-install declared but distributionSources.clawhubId missing');
      }
    } else if (skill.clientInstall.openclaw.mode === 'package-setup') {
      if (!skill.distributionSources.npmPackage) {
        issues.push('openclaw package-setup declared but distributionSources.npmPackage missing');
      }
      if (!skill.clientInstall.openclaw.installCommand) {
        issues.push('openclaw package-setup declared but installCommand missing');
      }
    } else {
      issues.push('openclaw native support declared but clientInstall.openclaw is not executable');
    }
  }
}

function hasSetupBinary(pkg: PackageJsonLike): boolean {
  if (!pkg.bin) return false;
  if (typeof pkg.bin === 'string') {
    return isSetupTarget(pkg.bin);
  }
  return Object.values(pkg.bin).some(target => isSetupTarget(target));
}

function isSetupTarget(target: string): boolean {
  const normalized = target.replace(/\\/g, '/').replace(/^\.\//, '');
  return normalized === 'bin/setup.js' || normalized === 'bin/setup.ts';
}

function resolveSkillDir(skill: SkillCatalogEntry, skillsRoot?: string): string {
  if (skillsRoot) return path.join(path.resolve(skillsRoot), skill.id);
  if (skill.sourcePath) return skill.sourcePath;
  return '';
}

function selectSkills(skills: SkillCatalogEntry[], onlyIds: string[]): SkillCatalogEntry[] {
  if (onlyIds.length === 0) return skills;
  const set = new Set(onlyIds);
  return skills.filter(skill => set.has(skill.id));
}

function toFlag(value: boolean): string {
  return value ? 'Y' : 'N';
}

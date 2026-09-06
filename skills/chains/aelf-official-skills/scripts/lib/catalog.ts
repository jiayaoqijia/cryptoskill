import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import {
  expandPathWithEnv,
  extractFirstHeading,
  extractSectionBullets,
  normalizeRepoUrlToHttps,
  parseFrontMatter,
  readJsonFile,
  replaceSection,
  runCommand,
  slugifyId,
  writeJsonFile,
} from './utils.ts';
import type {
  SkillCatalogEntry,
  SkillClientInstall,
  SkillClientInstallEntry,
  SkillsCatalog,
  WorkspaceConfig,
  WorkspaceProject,
} from './types.ts';

const SKILL_TABLE_START = '<!-- SKILL_TABLE_START -->';
const SKILL_TABLE_END = '<!-- SKILL_TABLE_END -->';
const REPOSITORY_HTTPS_OVERRIDES: Record<string, string> = {
  '@tomorrowdao/agent-skills': 'https://github.com/TomorrowDAOProject/tomorrowDAO-skill.git',
};
const DESCRIPTION_ZH_OVERRIDES: Record<string, string> = {
  '@blockchain-forever/aelf-node-skill': 'AElf 节点查询与合约调用技能。',
  '@aelfscan/agent-skills': 'AelfScan 浏览器数据检索与分析技能。',
  '@awaken-finance/agent-kit': 'Awaken DEX 交易与行情数据技能。',
  '@eforest-finance/agent-skills': 'eForest 代币与 NFT 市场操作技能。',
  '@portkey/ca-agent-skills': 'Portkey CA 钱包注册、认证、Guardian 与转账技能。',
  '@portkey/eoa-agent-skills': 'Portkey EOA 钱包与资产操作技能。',
  '@tomorrowdao/agent-skills': 'TomorrowDAO 治理、BP 与资源操作技能。',
};
const CLAWHUB_ID_OVERRIDES: Record<string, string> = {};

interface BuiltSkillCandidate {
  entry: SkillCatalogEntry;
  projectPath: string;
  declaredDependsOn: string[];
}

export interface BuildCatalogOptions {
  workspacePath?: string;
  includeLocalPaths?: boolean;
}

export interface WriteCatalogArtifactsOptions {
  rootDir?: string;
  outputPath?: string;
  syncReadme?: boolean;
}

interface PackageJsonLike {
  name?: string;
  version?: string;
  description?: string;
  scripts?: Record<string, string>;
  bin?: string | Record<string, string>;
  repository?: string | { type?: string; url?: string };
}

export function buildCatalog(options: BuildCatalogOptions = {}): SkillsCatalog {
  const workspacePath = path.resolve(options.workspacePath || path.join(process.cwd(), 'workspace.json'));
  const workspaceDir = path.dirname(workspacePath);
  const workspace = readJsonFile<WorkspaceConfig>(workspacePath);
  const includeLocalPaths = options.includeLocalPaths === true;

  const warnings: string[] = [];
  const candidates: BuiltSkillCandidate[] = [];

  for (const project of workspace.projects) {
    const projectPath = resolveProjectPath(project, workspaceDir);
    const packagePath = path.join(projectPath, 'package.json');
    const skillPath = path.join(projectPath, 'SKILL.md');

    if (!existsSync(packagePath)) {
      pushWarning(warnings, 'SKIP', projectPath, includeLocalPaths, 'package.json not found');
      continue;
    }

    if (!existsSync(skillPath)) {
      pushWarning(warnings, 'WARN', projectPath, includeLocalPaths, 'SKILL.md not found, project skipped');
      continue;
    }

    const entry = buildSkillEntry(projectPath, warnings, includeLocalPaths);
    if (!entry) {
      continue;
    }

    candidates.push({
      entry,
      projectPath,
      declaredDependsOn: normalizeDependsOn(project.dependsOn),
    });
  }

  validateDuplicateIds(candidates);
  const skills = applyAndValidateDependencies(candidates);

  skills.sort((a, b) => a.id.localeCompare(b.id));

  return {
    schemaVersion: '1.3.0',
    generatedAt: new Date().toISOString(),
    source: path.basename(workspacePath),
    skills,
    warnings,
  };
}

export function writeCatalogArtifacts(catalog: SkillsCatalog, options: WriteCatalogArtifactsOptions = {}): void {
  const rootDir = options.rootDir || process.cwd();
  const outputPath = options.outputPath
    ? path.resolve(rootDir, options.outputPath)
    : path.join(rootDir, 'skills-catalog.json');

  writeJsonFile(outputPath, catalog);

  if (options.syncReadme === false) {
    return;
  }

  syncReadmeTable(path.join(rootDir, 'README.md'), renderSkillTable(catalog, 'en'));
  syncReadmeTable(path.join(rootDir, 'README.zh-CN.md'), renderSkillTable(catalog, 'zh'));
}

function resolveProjectPath(project: WorkspaceProject, workspaceDir: string): string {
  const expandedPath = expandPathWithEnv(project.path);
  return path.resolve(workspaceDir, expandedPath);
}

function buildSkillEntry(
  projectPath: string,
  warnings: string[],
  includeLocalPaths: boolean,
): SkillCatalogEntry | null {
  const packagePath = path.join(projectPath, 'package.json');
  const skillPath = path.join(projectPath, 'SKILL.md');
  const openclawPath = path.join(projectPath, 'openclaw.json');
  const mcpServerPath = path.join(projectPath, 'src', 'mcp', 'server.ts');

  const pkg = readJsonFile<PackageJsonLike>(packagePath);
  const skillMd = readFileSync(skillPath, 'utf8');
  const frontMatter = parseFrontMatter(skillMd);
  const zhDescription = frontMatter.description_zh || (pkg.name ? DESCRIPTION_ZH_OVERRIDES[pkg.name] : undefined);

  if (!pkg.name || !pkg.version) {
    pushWarning(warnings, 'SKIP', projectPath, includeLocalPaths, 'package name/version missing');
    return null;
  }

  const setupBase = detectSetupBase(pkg, projectPath);
  const setupBin = detectSetupBin(pkg);
  const capabilities = extractSectionBullets(skillMd, 'Capabilities');
  const description = frontMatter.description || pkg.description || `Agent skill package ${pkg.name}`;

  if (!existsSync(openclawPath)) {
    pushWarning(warnings, 'WARN', projectPath, includeLocalPaths, 'openclaw.json not found');
  }

  const openclawToolCount = getOpenclawToolCount(openclawPath, warnings, projectPath, includeLocalPaths);
  const repositoryHttps = resolveRepositoryHttps(pkg, projectPath);
  const clawhubId = resolveClawhubId(pkg.name);
  const hasMcp = existsSync(mcpServerPath) || Boolean(pkg.scripts?.mcp);
  const hasOpenclaw = existsSync(openclawPath);
  const hasCli = Boolean(pkg.scripts?.cli);
  const hasSetup = Boolean(setupBase);

  return {
    id: frontMatter.name ? slugifyId(frontMatter.name) : slugifyId(pkg.name),
    displayName: extractFirstHeading(skillMd) || pkg.name,
    npm: {
      name: pkg.name,
      version: pkg.version,
    },
    repository: {
      ...(repositoryHttps ? { https: repositoryHttps } : {}),
    },
    distributionSources: {
      ...(repositoryHttps ? { githubRepo: repositoryHttps } : {}),
      npmPackage: pkg.name,
      ...(clawhubId ? { clawhubId } : {}),
    },
    description,
    ...(zhDescription ? { description_zh: zhDescription } : {}),
    capabilities,
    artifacts: {
      skillMd: true,
      mcpServer: hasMcp,
      openclaw: hasOpenclaw,
    },
    setupCommands: buildSetupCommands(setupBase),
    clientSupport: buildClientSupport({
      hasMcp,
      hasOpenclaw,
      hasCli,
      hasSetup,
    }),
    clientInstall: buildClientInstall({
      packageName: pkg.name,
      setupBin,
      clawhubId,
      hasOpenclaw,
      hasIronclaw: hasMcp && hasSetup,
    }),
    openclawToolCount,
    ...(includeLocalPaths ? { sourcePath: projectPath } : {}),
  };
}

function validateDuplicateIds(candidates: BuiltSkillCandidate[]): void {
  const idToPaths = new Map<string, string[]>();

  for (const candidate of candidates) {
    const arr = idToPaths.get(candidate.entry.id) || [];
    arr.push(candidate.projectPath);
    idToPaths.set(candidate.entry.id, arr);
  }

  const duplicates = Array.from(idToPaths.entries()).filter(([, paths]) => paths.length > 1);
  if (duplicates.length === 0) {
    return;
  }

  const detail = duplicates
    .map(([id, paths]) => `- ${id}: ${paths.join(' | ')}`)
    .join('\n');
  throw new Error(`[FAIL] Duplicate skill id detected:\n${detail}`);
}

function applyAndValidateDependencies(candidates: BuiltSkillCandidate[]): SkillCatalogEntry[] {
  const knownIds = new Set(candidates.map(candidate => candidate.entry.id));
  const skills: SkillCatalogEntry[] = [];
  const errors: string[] = [];

  for (const candidate of candidates) {
    const { entry, declaredDependsOn } = candidate;
    if (declaredDependsOn.length > 0) {
      const unknown = declaredDependsOn.filter(depId => !knownIds.has(depId));
      if (unknown.length > 0) {
        errors.push(
          `[FAIL] ${entry.id}: dependsOn references unknown skill id(s): ${unknown.join(', ')} (source: ${candidate.projectPath})`,
        );
      } else {
        entry.dependsOn = declaredDependsOn;
      }
    }

    skills.push(entry);
  }

  if (errors.length > 0) {
    throw new Error(errors.join('\n'));
  }

  return skills;
}

function normalizeDependsOn(dependsOn?: string[]): string[] {
  if (!dependsOn || dependsOn.length === 0) {
    return [];
  }

  const seen = new Set<string>();
  const normalized: string[] = [];

  for (const value of dependsOn) {
    const trimmed = value.trim();
    if (!trimmed || seen.has(trimmed)) {
      continue;
    }
    seen.add(trimmed);
    normalized.push(trimmed);
  }

  return normalized;
}

function getOpenclawToolCount(
  openclawPath: string,
  warnings: string[],
  projectPath: string,
  includeLocalPaths: boolean,
): number {
  if (!existsSync(openclawPath)) return 0;
  try {
    const data = readJsonFile<{ tools?: unknown[] }>(openclawPath);
    return Array.isArray(data.tools) ? data.tools.length : 0;
  } catch {
    pushWarning(warnings, 'WARN', projectPath, includeLocalPaths, 'openclaw.json parse failed');
    return 0;
  }
}

function resolveRepositoryHttps(pkg: PackageJsonLike, projectPath: string): string | undefined {
  if (pkg.name && REPOSITORY_HTTPS_OVERRIDES[pkg.name]) {
    return REPOSITORY_HTTPS_OVERRIDES[pkg.name];
  }

  const fromPkg = normalizeRepoUrlToHttps(extractRepositoryFromPackage(pkg));
  if (fromPkg) return canonicalizeRepositoryHttps(fromPkg);

  const gitResult = runCommand('git', ['-C', projectPath, 'remote', 'get-url', 'origin']);
  if (!gitResult.ok || !gitResult.stdout) return undefined;
  const normalized = normalizeRepoUrlToHttps(gitResult.stdout);
  return canonicalizeRepositoryHttps(normalized);
}

function extractRepositoryFromPackage(pkg: PackageJsonLike): string | undefined {
  if (!pkg.repository) return undefined;
  if (typeof pkg.repository === 'string') return pkg.repository;
  return pkg.repository.url;
}

function detectSetupBase(pkg: PackageJsonLike, projectPath: string): string | undefined {
  const hasSetupScript = Boolean(pkg.scripts?.setup);
  if (hasSetupScript) return 'bun run setup';

  const setupTs = path.join(projectPath, 'bin', 'setup.ts');
  const setupJs = path.join(projectPath, 'bin', 'setup.js');
  if (existsSync(setupTs)) return 'bun run bin/setup.ts';
  if (existsSync(setupJs)) return 'bun run bin/setup.js';
  return undefined;
}

function detectSetupBin(pkg: PackageJsonLike): string | undefined {
  if (!pkg.bin) return undefined;

  if (typeof pkg.bin === 'string') {
    return normalizeSetupTarget(pkg.bin) ? defaultBinName(pkg.name) : undefined;
  }

  for (const [binName, target] of Object.entries(pkg.bin)) {
    if (normalizeSetupTarget(target)) {
      return binName;
    }
  }

  return undefined;
}

function defaultBinName(packageName?: string): string | undefined {
  if (!packageName) return undefined;
  const [, unscoped = packageName] = packageName.split('/');
  return unscoped;
}

function normalizeSetupTarget(target: string): boolean {
  const normalized = target.replace(/\\/g, '/').replace(/^\.\//, '');
  return normalized === 'bin/setup.js' || normalized === 'bin/setup.ts';
}

function resolveClawhubId(packageName?: string): string | undefined {
  if (!packageName) return undefined;
  return CLAWHUB_ID_OVERRIDES[packageName];
}

function buildSetupCommands(setupBase?: string) {
  const install = 'bun install';
  if (!setupBase) return { install };

  return {
    install,
    list: `${setupBase} list`,
    openclaw: `${setupBase} openclaw`,
    cursor: `${setupBase} cursor`,
    claudeDesktop: `${setupBase} claude`,
    ironclaw: `${setupBase} ironclaw`,
  };
}

function buildClientSupport(input: {
  hasMcp: boolean;
  hasOpenclaw: boolean;
  hasCli: boolean;
  hasSetup: boolean;
}) {
  const openclaw = input.hasOpenclaw ? (input.hasSetup ? 'native' : 'manual') : 'unsupported';

  const nativeMcp = input.hasMcp && input.hasSetup ? 'native-setup' : 'manual-mcp';

  return {
    openclaw,
    cursor: input.hasMcp ? nativeMcp : 'unsupported',
    claude_desktop: input.hasMcp ? nativeMcp : 'unsupported',
    ironclaw: input.hasMcp ? nativeMcp : 'unsupported',
    claude_code: input.hasMcp ? 'manual-mcp' : 'unsupported',
    codex: input.hasMcp || input.hasCli ? 'manual-cli-or-mcp' : 'unsupported',
  };
}

function buildClientInstall(input: {
  packageName: string;
  setupBin?: string;
  clawhubId?: string;
  hasOpenclaw: boolean;
  hasIronclaw: boolean;
}): SkillClientInstall {
  return {
    openclaw: buildOpenclawInstall(input),
    ironclaw: buildIronclawInstall(input),
  };
}

function buildOpenclawInstall(input: {
  packageName: string;
  setupBin?: string;
  clawhubId?: string;
  hasOpenclaw: boolean;
}): SkillClientInstallEntry {
  if (!input.hasOpenclaw) {
    return { source: 'none', mode: 'unsupported' };
  }

  if (input.clawhubId) {
    return {
      source: 'clawhub',
      mode: 'managed-install',
    };
  }

  if (!input.setupBin) {
    return { source: 'none', mode: 'unsupported' };
  }

  return {
    source: 'npm',
    mode: 'package-setup',
    installCommand: `bunx -p ${input.packageName} ${input.setupBin} openclaw`,
  };
}

function buildIronclawInstall(input: {
  packageName: string;
  setupBin?: string;
  hasIronclaw: boolean;
}): SkillClientInstallEntry {
  if (!input.hasIronclaw || !input.setupBin) {
    return { source: 'none', mode: 'unsupported' };
  }

  return {
    source: 'npm',
    mode: 'trusted-local-install',
    installCommand: `bunx -p ${input.packageName} ${input.setupBin} ironclaw`,
    requiresTrustPromotion: true,
  };
}

function syncReadmeTable(readmePath: string, tableContent: string): void {
  if (!existsSync(readmePath)) return;
  const original = readFileSync(readmePath, 'utf8');
  const updated = replaceSection(original, SKILL_TABLE_START, SKILL_TABLE_END, tableContent);
  if (updated !== original) {
    writeFileSync(readmePath, updated, 'utf8');
  }
}

function renderSkillTable(catalog: SkillsCatalog, locale: 'en' | 'zh'): string {
  const header =
    locale === 'zh'
      ? '| ID | npm 包名 | 版本 | OpenClaw 工具数 | 描述 |'
      : '| ID | npm Package | Version | OpenClaw Tools | Description |';
  const divider = '|---|---|---:|---:|---|';

  const rows = catalog.skills.map(skill => {
    const description = locale === 'zh' ? skill.description_zh || skill.description : skill.description;
    const desc = description.replace(/\|/g, '\\|');
    return `| ${skill.id} | ${skill.npm.name} | ${skill.npm.version} | ${skill.openclawToolCount} | ${desc} |`;
  });

  return [header, divider, ...rows].join('\n');
}

function pushWarning(
  warnings: string[],
  level: 'WARN' | 'SKIP',
  projectPath: string,
  includeLocalPaths: boolean,
  message: string,
): void {
  warnings.push(`[${level}] ${formatWarningTarget(projectPath, includeLocalPaths)}: ${message}`);
}

function formatWarningTarget(projectPath: string, includeLocalPaths: boolean): string {
  if (includeLocalPaths) return projectPath;
  const normalized = projectPath.replace(/\\/g, '/');
  const workspaceMarker = '/workspace/';
  const markerIndex = normalized.indexOf(workspaceMarker);
  if (markerIndex >= 0) {
    return normalized.slice(markerIndex + workspaceMarker.length);
  }

  const segments = normalized.split('/').filter(Boolean);
  if (segments.length >= 2) {
    return `${segments[segments.length - 2]}/${segments[segments.length - 1]}`;
  }
  return path.basename(projectPath);
}

function canonicalizeRepositoryHttps(raw?: string): string | undefined {
  if (!raw) return undefined;

  try {
    const parsed = new URL(raw);
    if (parsed.hostname === 'tmrwdao.github.com') {
      parsed.hostname = 'github.com';
    }
    return parsed.toString();
  } catch {
    return raw;
  }
}

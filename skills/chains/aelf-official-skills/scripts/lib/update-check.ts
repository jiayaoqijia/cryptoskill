import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import type { SkillsCatalog } from './types.ts';
import { normalizeRepoUrlToHttps, readJsonFile } from './utils.ts';
import type {
  HubUpdateInfo,
  OutdatedSkillItem,
  ReleaseDigest,
  UpdateCheckOptions,
  UpdateCheckResult,
  UpdateSourceStatus,
  VersionDiffLevel,
} from './update-types.ts';

const DEFAULT_TTL_HOURS = 24;
const DEFAULT_CACHE_RELATIVE_PATH = path.join('.aelf-skills', 'update-check-cache.json');
const ENABLE_ENV = 'AELF_SKILLS_UPDATE_CHECK';
const TTL_ENV = 'AELF_SKILLS_UPDATE_TTL_HOURS';
const CACHE_PATH_ENV = 'AELF_SKILLS_UPDATE_CACHE_PATH';

interface LocalPackageInfo {
  name: string;
  version: string;
  repositoryUrl?: string;
}

function getDefaultPackageJsonPath(): string {
  return path.resolve(import.meta.dir, '..', '..', 'package.json');
}

function getDefaultCatalogPath(): string {
  return path.resolve(process.cwd(), 'skills-catalog.json');
}

function getDefaultCachePath(): string {
  return path.resolve(os.homedir(), DEFAULT_CACHE_RELATIVE_PATH);
}

function envToBoolean(raw: string | undefined, defaultValue: boolean): boolean {
  if (!raw) return defaultValue;
  const normalized = raw.trim().toLowerCase();
  if (['0', 'false', 'no', 'off'].includes(normalized)) return false;
  if (['1', 'true', 'yes', 'on'].includes(normalized)) return true;
  return defaultValue;
}

function parseNumber(value: string | undefined, fallback: number): number {
  if (!value) return fallback;
  const n = Number(value);
  if (!Number.isFinite(n) || n <= 0) return fallback;
  return n;
}

function resolveTtlHours(options?: UpdateCheckOptions): number {
  return options?.ttlHours || parseNumber(process.env[TTL_ENV], DEFAULT_TTL_HOURS);
}

function resolveCachePath(options?: UpdateCheckOptions): string {
  return path.resolve(options?.cachePath || process.env[CACHE_PATH_ENV] || getDefaultCachePath());
}

function isEnabled(options?: UpdateCheckOptions): boolean {
  if (options?.allowWhenDisabled) return true;
  return envToBoolean(process.env[ENABLE_ENV], true);
}

function readLocalPackageInfo(packageJsonPath: string): LocalPackageInfo {
  const pkg = readJsonFile<Record<string, unknown>>(packageJsonPath);
  const name = typeof pkg.name === 'string' ? pkg.name : '@blockchain-forever/aelf-skills';
  const version = typeof pkg.version === 'string' ? pkg.version : '0.0.0';
  const repository =
    typeof pkg.repository === 'object' && pkg.repository
      ? (pkg.repository as Record<string, unknown>)
      : {};
  const repositoryUrl = typeof repository.url === 'string' ? repository.url : undefined;
  return { name, version, repositoryUrl };
}

interface SemverCore {
  major: number;
  minor: number;
  patch: number;
}

function parseSemverCore(version: string): SemverCore | null {
  const normalized = version.trim().replace(/^v/, '');
  const match = normalized.match(/^(\d+)\.(\d+)\.(\d+)/);
  if (!match) return null;
  return {
    major: Number(match[1]),
    minor: Number(match[2]),
    patch: Number(match[3]),
  };
}

export function compareSemver(currentVersion: string, latestVersion: string): number {
  const a = parseSemverCore(currentVersion);
  const b = parseSemverCore(latestVersion);
  if (!a || !b) {
    if (currentVersion === latestVersion) return 0;
    return currentVersion < latestVersion ? -1 : 1;
  }

  if (a.major !== b.major) return a.major < b.major ? -1 : 1;
  if (a.minor !== b.minor) return a.minor < b.minor ? -1 : 1;
  if (a.patch !== b.patch) return a.patch < b.patch ? -1 : 1;
  return 0;
}

export function getVersionDiffLevel(currentVersion: string, latestVersion: string): VersionDiffLevel {
  const a = parseSemverCore(currentVersion);
  const b = parseSemverCore(latestVersion);
  if (!a || !b) return 'unknown';
  if (a.major !== b.major) return 'major';
  if (a.minor !== b.minor) return 'minor';
  if (a.patch !== b.patch) return 'patch';
  return 'none';
}

export function isCacheFresh(checkedAt: string, ttlHours: number, now: Date): boolean {
  const checkedAtMs = Date.parse(checkedAt);
  if (!Number.isFinite(checkedAtMs)) return false;
  const maxAgeMs = ttlHours * 60 * 60 * 1000;
  return now.getTime() - checkedAtMs < maxAgeMs;
}

function readCache(cachePath: string): UpdateCheckResult | null {
  if (!existsSync(cachePath)) return null;
  try {
    const cached = readJsonFile<UpdateCheckResult>(cachePath);
    if (!cached || typeof cached.checkedAt !== 'string') return null;
    return cached;
  } catch {
    return null;
  }
}

function writeCache(cachePath: string, result: UpdateCheckResult): void {
  const dir = path.dirname(cachePath);
  mkdirSync(dir, { recursive: true });
  writeFileSync(cachePath, `${JSON.stringify(result, null, 2)}\n`, 'utf8');
}

async function fetchJson(url: string, fetchImpl: typeof fetch): Promise<Record<string, any>> {
  const response = await fetchImpl(url, {
    headers: {
      Accept: 'application/json',
      'User-Agent': 'aelf-skills-update-check',
    },
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status} for ${url}`);
  }
  return (await response.json()) as Record<string, any>;
}

async function fetchNpmLatestVersion(packageName: string, fetchImpl: typeof fetch): Promise<string> {
  const registryUrl = `https://registry.npmjs.org/${encodeURIComponent(packageName)}`;
  const payload = await fetchJson(registryUrl, fetchImpl);
  const latest = payload?.['dist-tags']?.latest;
  if (typeof latest !== 'string' || !latest.trim()) {
    throw new Error(`npm latest version not found for ${packageName}`);
  }
  return latest.trim();
}

function toGitHubRepo(repositoryUrl?: string): { owner: string; repo: string; httpsUrl: string } | null {
  const normalized = normalizeRepoUrlToHttps(repositoryUrl);
  if (!normalized) return null;
  const cleaned = normalized.replace(/\.git$/, '');
  const match = cleaned.match(/^https:\/\/github\.com\/([^/]+)\/([^/]+)$/i);
  if (!match) return null;
  return {
    owner: match[1],
    repo: match[2],
    httpsUrl: `https://github.com/${match[1]}/${match[2]}`,
  };
}

function firstMeaningfulLine(markdown: string): string | null {
  const lines = markdown.split(/\r?\n/).map(v => v.trim());
  for (const line of lines) {
    if (!line) continue;
    if (line.startsWith('#')) continue;
    return line;
  }
  return null;
}

function truncate(text: string, maxChars = 180): string {
  if (text.length <= maxChars) return text;
  return `${text.slice(0, maxChars - 1)}…`;
}

async function fetchGitHubReleaseDigest(
  repositoryUrl: string | undefined,
  currentVersion: string,
  latestVersion: string,
  fetchImpl: typeof fetch,
): Promise<ReleaseDigest> {
  const repo = toGitHubRepo(repositoryUrl);
  if (!repo) {
    return {
      source: 'none',
      summary: `${currentVersion} -> ${latestVersion}`,
    };
  }

  const tagCandidates = [`v${latestVersion}`, latestVersion];

  for (const tag of tagCandidates) {
    const apiUrl = `https://api.github.com/repos/${repo.owner}/${repo.repo}/releases/tags/${encodeURIComponent(tag)}`;
    const response = await fetchImpl(apiUrl, {
      headers: {
        Accept: 'application/vnd.github+json',
        'User-Agent': 'aelf-skills-update-check',
      },
    });

    if (response.status === 404) {
      continue;
    }
    if (!response.ok) {
      throw new Error(`GitHub release API ${response.status} for ${repo.owner}/${repo.repo}`);
    }

    const release = (await response.json()) as Record<string, any>;
    const body = typeof release.body === 'string' ? release.body : '';
    const title = typeof release.name === 'string' ? release.name : '';
    const summary = firstMeaningfulLine(body) || title || `${currentVersion} -> ${latestVersion}`;
    const releaseUrl =
      typeof release.html_url === 'string' && release.html_url
        ? release.html_url
        : `${repo.httpsUrl}/releases/tag/${tag}`;

    return {
      source: 'github-release',
      summary: truncate(summary),
      url: releaseUrl,
    };
  }

  return {
    source: 'github-compare',
    summary: `${currentVersion} -> ${latestVersion}`,
    url: `${repo.httpsUrl}/compare/v${currentVersion}...v${latestVersion}`,
  };
}

function buildEmptyHub(packageName: string, currentVersion: string): HubUpdateInfo {
  return {
    packageName,
    currentVersion,
    latestVersion: currentVersion,
    outdated: false,
    diffLevel: 'none',
  };
}

function buildResultSkeleton(localPackage: LocalPackageInfo, checkedAt: string): UpdateCheckResult {
  return {
    checkedAt,
    fromCache: false,
    hasUpdates: false,
    hub: buildEmptyHub(localPackage.name, localPackage.version),
    catalogOutdated: [],
    notesDigest: [],
    sourceStatus: {
      npm: 'ok',
      github: 'skipped',
      errors: [],
    },
  };
}

function toNotesDigest(result: UpdateCheckResult): ReleaseDigest[] {
  const notes: ReleaseDigest[] = [];
  if (result.hub.outdated && result.hub.release) {
    notes.push(result.hub.release);
  }
  for (const skill of result.catalogOutdated.slice(0, 5)) {
    if (skill.release) {
      notes.push(skill.release);
    }
  }
  return notes;
}

async function buildLiveResult(options: UpdateCheckOptions = {}): Promise<UpdateCheckResult> {
  const fetchImpl = options.fetchImpl || fetch;
  const now = (options.now || (() => new Date()))();
  const packageJsonPath = path.resolve(options.packageJsonPath || getDefaultPackageJsonPath());
  const catalogPath = path.resolve(options.catalogPath || getDefaultCatalogPath());
  const localPackage = readLocalPackageInfo(packageJsonPath);
  const result = buildResultSkeleton(localPackage, now.toISOString());

  try {
    const latestHubVersion = await fetchNpmLatestVersion(localPackage.name, fetchImpl);
    const hubCmp = compareSemver(localPackage.version, latestHubVersion);
    const hubOutdated = hubCmp < 0;
    result.hub = {
      packageName: localPackage.name,
      currentVersion: localPackage.version,
      latestVersion: latestHubVersion,
      outdated: hubOutdated,
      diffLevel: getVersionDiffLevel(localPackage.version, latestHubVersion),
    };
    if (hubOutdated) {
      try {
        result.hub.release = await fetchGitHubReleaseDigest(
          localPackage.repositoryUrl,
          localPackage.version,
          latestHubVersion,
          fetchImpl,
        );
        result.sourceStatus.github = 'ok';
      } catch (error) {
        result.sourceStatus.github = 'error';
        result.sourceStatus.errors.push(
          `hub release digest failed: ${error instanceof Error ? error.message : String(error)}`,
        );
      }
    }
  } catch (error) {
    result.sourceStatus.npm = 'error';
    result.sourceStatus.errors.push(`hub npm check failed: ${error instanceof Error ? error.message : String(error)}`);
  }

  if (!existsSync(catalogPath)) {
    result.sourceStatus.errors.push(`catalog not found: ${catalogPath}`);
    result.hasUpdates = result.hub.outdated;
    result.notesDigest = toNotesDigest(result);
    return result;
  }

  const catalog = readJsonFile<SkillsCatalog>(catalogPath);
  const outdated: OutdatedSkillItem[] = [];

  for (const skill of catalog.skills) {
    try {
      const latestVersion = await fetchNpmLatestVersion(skill.npm.name, fetchImpl);
      if (compareSemver(skill.npm.version, latestVersion) >= 0) {
        continue;
      }

      const item: OutdatedSkillItem = {
        id: skill.id,
        packageName: skill.npm.name,
        currentVersion: skill.npm.version,
        latestVersion,
        diffLevel: getVersionDiffLevel(skill.npm.version, latestVersion),
        repositoryUrl: skill.repository.https,
      };

      try {
        item.release = await fetchGitHubReleaseDigest(
          skill.repository.https,
          skill.npm.version,
          latestVersion,
          fetchImpl,
        );
        if (result.sourceStatus.github !== 'error') {
          result.sourceStatus.github = 'ok';
        }
      } catch (error) {
        if (result.sourceStatus.github !== 'error') {
          result.sourceStatus.github = 'error';
        }
        result.sourceStatus.errors.push(
          `${skill.id} release digest failed: ${error instanceof Error ? error.message : String(error)}`,
        );
      }

      outdated.push(item);
    } catch (error) {
      if (result.sourceStatus.npm !== 'error') {
        result.sourceStatus.npm = 'error';
      }
      result.sourceStatus.errors.push(
        `${skill.id} npm check failed: ${error instanceof Error ? error.message : String(error)}`,
      );
    }
  }

  if (result.sourceStatus.github === 'skipped' && outdated.length > 0) {
    // outdated exists but no github notes were retrieved successfully.
    result.sourceStatus.github = 'error';
  }

  result.catalogOutdated = outdated;
  result.hasUpdates = result.hub.outdated || outdated.length > 0;
  result.notesDigest = toNotesDigest(result);
  return result;
}

function withCacheFlag(result: UpdateCheckResult, fromCache: boolean): UpdateCheckResult {
  return {
    ...result,
    fromCache,
  };
}

export async function checkForUpdates(options: UpdateCheckOptions = {}): Promise<UpdateCheckResult | null> {
  if (!isEnabled(options)) {
    return null;
  }

  const now = (options.now || (() => new Date()))();
  const ttlHours = resolveTtlHours(options);
  const cachePath = resolveCachePath(options);
  const cached = readCache(cachePath);

  if (!options.force && cached && isCacheFresh(cached.checkedAt, ttlHours, now)) {
    return withCacheFlag(cached, true);
  }

  try {
    const live = await buildLiveResult(options);
    if (cached?.lastNotifiedAt) {
      live.lastNotifiedAt = cached.lastNotifiedAt;
    }
    writeCache(cachePath, live);
    return withCacheFlag(live, false);
  } catch (error) {
    if (cached) {
      const fallback = withCacheFlag(cached, true);
      fallback.sourceStatus.errors = [
        ...fallback.sourceStatus.errors,
        `live check failed, fallback to cache: ${error instanceof Error ? error.message : String(error)}`,
      ];
      return fallback;
    }
    throw error;
  }
}

export function renderReminderLines(result: UpdateCheckResult): string[] {
  if (!result.hasUpdates) return [];
  const lines: string[] = [];

  if (result.hub.outdated) {
    lines.push(
      `[UPDATE] aelf-skills hub update available: ${result.hub.currentVersion} -> ${result.hub.latestVersion}`,
    );
  }

  if (result.catalogOutdated.length > 0) {
    const sample = result.catalogOutdated
      .slice(0, 2)
      .map(item => `${item.id} ${item.currentVersion}->${item.latestVersion}`)
      .join(', ');
    lines.push(`[UPDATE] ${result.catalogOutdated.length} skill package update(s): ${sample}`);
  }

  lines.push('[ACTION] Use pinned release flow: ./bootstrap.sh --source npm');
  return lines;
}

export function renderHumanSummary(result: UpdateCheckResult): string {
  const lines: string[] = [];
  const hubCmp = compareSemver(result.hub.currentVersion, result.hub.latestVersion);
  const hubStatus = hubCmp < 0 ? 'outdated' : hubCmp > 0 ? 'ahead' : 'ok';

  lines.push('[Update Check]');
  lines.push(`Checked at: ${result.checkedAt}${result.fromCache ? ' (cache)' : ''}`);
  lines.push(
    `Hub: ${result.hub.packageName} ${result.hub.currentVersion} -> ${result.hub.latestVersion} [${hubStatus}]`,
  );

  if (result.hub.outdated && result.hub.release) {
    lines.push(`Hub notes: ${result.hub.release.summary}`);
    if (result.hub.release.url) {
      lines.push(`  ${result.hub.release.url}`);
    }
  }

  if (result.catalogOutdated.length > 0) {
    lines.push(`Outdated skill packages: ${result.catalogOutdated.length}`);
    for (const item of result.catalogOutdated) {
      lines.push(
        `- ${item.id}: ${item.currentVersion} -> ${item.latestVersion} [${item.diffLevel}]`,
      );
      if (item.release?.summary) {
        lines.push(`  notes: ${item.release.summary}`);
      }
      if (item.release?.url) {
        lines.push(`  ${item.release.url}`);
      }
    }
  } else {
    lines.push('Outdated skill packages: 0');
  }

  if (result.sourceStatus.errors.length > 0) {
    lines.push('Source status: degraded');
    for (const errorLine of result.sourceStatus.errors) {
      lines.push(`- ${errorLine}`);
    }
  }

  if (result.hasUpdates) {
    lines.push('[Action]');
    lines.push(`- Upgrade hub if needed: npm i -g ${result.hub.packageName}@latest`);
    lines.push('- Keep release-locked install: ./bootstrap.sh --source npm');
  } else {
    lines.push('[OK] Hub and catalog pinned versions are up to date.');
  }

  return lines.join('\n');
}

export async function maybePrintUpdateReminder(options: UpdateCheckOptions = {}): Promise<void> {
  try {
    const now = (options.now || (() => new Date()))();
    const ttlHours = resolveTtlHours(options);
    const cachePath = resolveCachePath(options);
    const result = await checkForUpdates(options);
    if (!result || !result.hasUpdates) return;

    const lastNotifiedAt = result.lastNotifiedAt;
    if (lastNotifiedAt && isCacheFresh(lastNotifiedAt, ttlHours, now)) {
      return;
    }

    const lines = renderReminderLines(result);
    if (lines.length === 0) return;
    for (const line of lines) {
      console.log(line);
    }

    writeCache(cachePath, {
      ...result,
      lastNotifiedAt: now.toISOString(),
    });
  } catch {
    // Non-blocking reminder path: swallow all check errors.
  }
}

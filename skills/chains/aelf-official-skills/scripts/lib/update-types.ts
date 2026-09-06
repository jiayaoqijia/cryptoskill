export type VersionDiffLevel = 'major' | 'minor' | 'patch' | 'none' | 'unknown';

export type ReleaseDigestSource = 'github-release' | 'github-compare' | 'none';

export interface ReleaseDigest {
  source: ReleaseDigestSource;
  summary: string;
  url?: string;
}

export interface HubUpdateInfo {
  packageName: string;
  currentVersion: string;
  latestVersion: string;
  outdated: boolean;
  diffLevel: VersionDiffLevel;
  release?: ReleaseDigest;
}

export interface OutdatedSkillItem {
  id: string;
  packageName: string;
  currentVersion: string;
  latestVersion: string;
  diffLevel: VersionDiffLevel;
  repositoryUrl?: string;
  release?: ReleaseDigest;
}

export interface UpdateSourceStatus {
  npm: 'ok' | 'error' | 'skipped';
  github: 'ok' | 'error' | 'skipped';
  errors: string[];
}

export interface UpdateCheckResult {
  checkedAt: string;
  fromCache: boolean;
  hasUpdates: boolean;
  lastNotifiedAt?: string;
  hub: HubUpdateInfo;
  catalogOutdated: OutdatedSkillItem[];
  notesDigest: ReleaseDigest[];
  sourceStatus: UpdateSourceStatus;
}

export interface UpdateCheckOptions {
  force?: boolean;
  quiet?: boolean;
  json?: boolean;
  allowWhenDisabled?: boolean;
  ttlHours?: number;
  cachePath?: string;
  catalogPath?: string;
  packageJsonPath?: string;
  now?: () => Date;
  fetchImpl?: typeof fetch;
}

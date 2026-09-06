import {
  closeSync,
  chmodSync,
  existsSync,
  mkdirSync,
  openSync,
  readFileSync,
  renameSync,
  statSync,
  unlinkSync,
  writeFileSync,
} from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { SIGNER_ERROR_CODES } from './signer-error-codes.js';

export type WalletType = 'EOA' | 'CA';
export type WalletSource = 'eoa-local' | 'ca-keystore' | 'env';
export type SignerMode = 'auto' | 'explicit' | 'context' | 'env' | 'daemon';
export type SignerProvider = 'explicit' | 'context' | 'env' | 'daemon';

export type SignerContextInput = {
  signerMode?: SignerMode;
  walletType?: WalletType;
  address?: string;
  password?: string;
  privateKey?: string;
  caHash?: string;
  caAddress?: string;
  network?: 'mainnet' | 'testnet';
};

export type ActiveWalletProfile = {
  walletType: WalletType;
  source: WalletSource;
  network?: string;
  address?: string;
  caAddress?: string;
  caHash?: string;
  walletFile?: string;
  keystoreFile?: string;
  updatedAt: string;
};

export type WalletContextWriter = {
  skill: string;
  version: string;
};

export type WalletContextFile = {
  version: 1;
  activeProfileId: string;
  profiles: Record<string, ActiveWalletProfile>;
  lastWriter: WalletContextWriter;
};

const CONTEXT_VERSION = 1 as const;
const DEFAULT_PROFILE_ID = 'default';
const LOCK_RETRY_INTERVAL_MS = 50;
const LOCK_MAX_RETRIES = 20;
const LOCK_STALE_MS = 30_000;

function getContextPath(): string {
  const override = process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH;
  if (override) return resolve(override);
  return join(homedir(), '.portkey', 'skill-wallet', 'context.v1.json');
}

function sleepMs(ms: number): void {
  const end = Date.now() + ms;
  while (Date.now() < end) {
    // busy wait for a very short lock retry window
  }
}

function ensureDir(pathname: string): void {
  const dir = dirname(pathname);
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true, mode: 0o700 });
  }
  try {
    chmodSync(dir, 0o700);
  } catch {
    // Ignore permission errors for externally managed parent dirs (e.g. /tmp in tests).
  }
}

function parseProfile(value: unknown): ActiveWalletProfile | null {
  if (!value || typeof value !== 'object') return null;
  const record = value as Record<string, unknown>;
  if (record.walletType !== 'EOA' && record.walletType !== 'CA') return null;
  if (
    record.source !== 'eoa-local' &&
    record.source !== 'ca-keystore' &&
    record.source !== 'env'
  ) {
    return null;
  }
  const updatedAt = typeof record.updatedAt === 'string' ? record.updatedAt : '';
  if (!updatedAt) return null;

  return {
    walletType: record.walletType,
    source: record.source,
    network: typeof record.network === 'string' ? record.network : undefined,
    address: typeof record.address === 'string' ? record.address : undefined,
    caAddress: typeof record.caAddress === 'string' ? record.caAddress : undefined,
    caHash: typeof record.caHash === 'string' ? record.caHash : undefined,
    walletFile: typeof record.walletFile === 'string' ? record.walletFile : undefined,
    keystoreFile: typeof record.keystoreFile === 'string' ? record.keystoreFile : undefined,
    updatedAt,
  };
}

function parseContext(raw: unknown): WalletContextFile | null {
  if (!raw || typeof raw !== 'object') return null;
  const record = raw as Record<string, unknown>;
  if (record.version !== CONTEXT_VERSION) return null;

  const activeProfileId =
    typeof record.activeProfileId === 'string' && record.activeProfileId
      ? record.activeProfileId
      : DEFAULT_PROFILE_ID;
  const profilesInput =
    record.profiles && typeof record.profiles === 'object'
      ? (record.profiles as Record<string, unknown>)
      : {};
  const profiles: Record<string, ActiveWalletProfile> = {};
  for (const [id, candidate] of Object.entries(profilesInput)) {
    const parsed = parseProfile(candidate);
    if (parsed) profiles[id] = parsed;
  }

  const lastWriterInput =
    record.lastWriter && typeof record.lastWriter === 'object'
      ? (record.lastWriter as Record<string, unknown>)
      : {};
  const lastWriter: WalletContextWriter = {
    skill:
      typeof lastWriterInput.skill === 'string'
        ? lastWriterInput.skill
        : 'unknown',
    version:
      typeof lastWriterInput.version === 'string'
        ? lastWriterInput.version
        : '0.0.0',
  };

  return {
    version: CONTEXT_VERSION,
    activeProfileId,
    profiles,
    lastWriter,
  };
}

export function readWalletContext(): WalletContextFile | null {
  const filePath = getContextPath();
  return readWalletContextFromPath(filePath);
}

function readWalletContextFromPath(filePath: string): WalletContextFile | null {
  if (!existsSync(filePath)) return null;

  try {
    const raw = JSON.parse(readFileSync(filePath, 'utf8')) as unknown;
    return parseContext(raw);
  } catch {
    return null;
  }
}

export function writeWalletContext(context: WalletContextFile): void {
  const filePath = getContextPath();
  withContextLock(filePath, () => {
    writeWalletContextFile(filePath, context);
  });
}

function writeWalletContextFile(filePath: string, context: WalletContextFile): void {
  ensureDir(filePath);
  const payload = JSON.stringify(context, null, 2) + '\n';
  const tempPath = `${filePath}.tmp`;
  writeFileSync(tempPath, payload, { encoding: 'utf8', mode: 0o600 });
  chmodSync(tempPath, 0o600);
  renameSync(tempPath, filePath);
  chmodSync(filePath, 0o600);
}

function withContextLock<T>(filePath: string, action: () => T): T {
  ensureDir(filePath);
  const lockPath = `${filePath}.lock`;
  let retries = 0;

  while (retries <= LOCK_MAX_RETRIES) {
    try {
      if (existsSync(lockPath)) {
        const ageMs = Date.now() - statSync(lockPath).mtimeMs;
        if (ageMs > LOCK_STALE_MS) {
          unlinkSync(lockPath);
        }
      }
    } catch {
      // best effort stale lock cleanup
    }

    let fd: number | null = null;
    try {
      fd = openSync(lockPath, 'wx', 0o600);
      const result = action();
      closeSync(fd);
      fd = null;
      unlinkSync(lockPath);
      return result;
    } catch (error) {
      if (fd !== null) {
        try {
          closeSync(fd);
        } catch {
          // noop
        }
      }

      const code = error && typeof error === 'object'
        ? String((error as { code?: unknown }).code || '')
        : '';
      if (code !== 'EEXIST') {
        throw error;
      }

      retries += 1;
      if (retries > LOCK_MAX_RETRIES) {
        throw new Error(
          `${SIGNER_ERROR_CODES.CONTEXT_LOCK_TIMEOUT}: failed to acquire context lock after ${LOCK_MAX_RETRIES} retries`,
        );
      }
      sleepMs(LOCK_RETRY_INTERVAL_MS);
    }
  }

  throw new Error(
    `${SIGNER_ERROR_CODES.CONTEXT_LOCK_TIMEOUT}: failed to acquire context lock after ${LOCK_MAX_RETRIES} retries`,
  );
}

export function setActiveWalletProfile(
  profile: Omit<ActiveWalletProfile, 'updatedAt'> & { profileId?: string },
  writer: WalletContextWriter,
): WalletContextFile {
  const filePath = getContextPath();
  return withContextLock(filePath, () => {
    const profileId = profile.profileId || DEFAULT_PROFILE_ID;
    const current =
      readWalletContextFromPath(filePath) ||
      ({
        version: CONTEXT_VERSION,
        activeProfileId: profileId,
        profiles: {},
        lastWriter: writer,
      } as WalletContextFile);

    current.activeProfileId = profileId;
    current.profiles[profileId] = {
      ...profile,
      updatedAt: new Date().toISOString(),
    };
    current.lastWriter = writer;

    writeWalletContextFile(filePath, current);
    return current;
  });
}

export function getActiveWalletProfile(
  profileId?: string,
): ActiveWalletProfile | null {
  const context = readWalletContext();
  if (!context) return null;
  const id = profileId || context.activeProfileId || DEFAULT_PROFILE_ID;
  return context.profiles[id] || null;
}

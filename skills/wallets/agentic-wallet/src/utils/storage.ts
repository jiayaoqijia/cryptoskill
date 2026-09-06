import { existsSync, mkdirSync, readFileSync, writeFileSync, readdirSync, unlinkSync, openSync, closeSync, constants } from 'fs';
import { homedir } from 'os';
import { join, resolve, normalize } from 'path';
import { createCipheriv, createDecipheriv, randomBytes, scryptSync, timingSafeEqual } from 'crypto';

export interface StoredWallet {
  id: string;
  name: string;
  address: string;
  chainId: number;
  chain: string;
  createdAt: string;
  encrypted: boolean;
  encryptedPrivateKey?: string;
  iv?: string;
  salt?: string;
  authTag?: string;
}

export interface CrossmintWalletRecord {
  id: string;
  name: string;
  address: string;
  chainType: string;
  walletType: string;
  custodyModel: 'custodial' | 'non-custodial';
  createdAt: string;
  crossmintLocator?: string;
}

const WALLET_DIR = join(homedir(), '.agent-arena', 'wallets');

// Scrypt parameters — explicit, not relying on Node defaults
// N=16384 (2^14), r=8, p=1 — secure and compatible across Node.js versions
// maxmem raised to 64MB to avoid memory limit errors on constrained environments
const SCRYPT_PARAMS = { N: 16384, r: 8, p: 1, maxmem: 64 * 1024 * 1024 };

/** Max wallet name length to prevent DoS */
const MAX_NAME_LENGTH = 128;

/** Strict wallet name pattern — prevents path traversal */
const SAFE_NAME_REGEX = /^[a-zA-Z0-9][a-zA-Z0-9._-]*$/;

/**
 * Validate wallet name to prevent path traversal and other attacks.
 * Throws if name is invalid.
 */
export function validateWalletName(name: string): void {
  if (!name || name.length === 0) {
    throw new Error('Wallet name cannot be empty');
  }
  if (name.length > MAX_NAME_LENGTH) {
    throw new Error(`Wallet name too long (max ${MAX_NAME_LENGTH} characters)`);
  }
  if (!SAFE_NAME_REGEX.test(name)) {
    throw new Error('Wallet name can only contain letters, numbers, hyphens, underscores, and dots (must start with alphanumeric)');
  }
  // Double-check: resolved path must stay inside WALLET_DIR
  const resolved = resolve(WALLET_DIR, `${name}.json`);
  if (!resolved.startsWith(resolve(WALLET_DIR))) {
    throw new Error('Invalid wallet name: path traversal detected');
  }
}

export function ensureWalletDir(): void {
  if (!existsSync(WALLET_DIR)) {
    mkdirSync(WALLET_DIR, { recursive: true, mode: 0o700 });
  }
}

export function getWalletPath(name: string): string {
  validateWalletName(name);
  return join(WALLET_DIR, `${name}.json`);
}

export function walletExists(name: string): boolean {
  return existsSync(getWalletPath(name));
}

export function encryptPrivateKey(privateKey: string, password: string): { encrypted: string; iv: string; salt: string; authTag: string } {
  const salt = randomBytes(16);
  const key = scryptSync(password, salt, 32, SCRYPT_PARAMS);
  const iv = randomBytes(16);
  const cipher = createCipheriv('aes-256-gcm', key, iv);

  let encrypted = cipher.update(privateKey, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  const authTag = cipher.getAuthTag();

  return {
    encrypted,
    authTag: authTag.toString('hex'),
    iv: iv.toString('hex'),
    salt: salt.toString('hex')
  };
}

export function decryptPrivateKey(encrypted: string, iv: string, salt: string, password: string, authTag?: string): string {
  const key = scryptSync(password, Buffer.from(salt, 'hex'), 32, SCRYPT_PARAMS);
  const ivBuffer = Buffer.from(iv, 'hex');

  let authTagBuffer: Buffer;
  let encryptedData: string;

  if (authTag) {
    // New format: authTag stored separately
    authTagBuffer = Buffer.from(authTag, 'hex');
    encryptedData = encrypted;
  } else {
    // Legacy format: authTag appended to ciphertext (last 32 hex chars = 16 bytes)
    authTagBuffer = Buffer.from(encrypted.slice(-32), 'hex');
    encryptedData = encrypted.slice(0, -32);
  }

  const decipher = createDecipheriv('aes-256-gcm', key, ivBuffer);
  decipher.setAuthTag(authTagBuffer);

  let decrypted = decipher.update(encryptedData, 'hex', 'utf8');
  decrypted += decipher.final('utf8');

  return decrypted;
}

/** Constant-time password comparison to prevent timing attacks */
export function safePasswordEqual(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  return timingSafeEqual(Buffer.from(a), Buffer.from(b));
}

export function saveWallet(wallet: StoredWallet): void {
  ensureWalletDir();
  const path = getWalletPath(wallet.name);
  // Write with restrictive permissions (owner-only read/write)
  writeFileSync(path, JSON.stringify(wallet, null, 2), { encoding: 'utf8', mode: 0o600 });
}

/**
 * Save wallet atomically — uses exclusive create flag to prevent TOCTOU races.
 * Returns false if the file already exists.
 */
export function saveWalletExclusive(wallet: StoredWallet): boolean {
  ensureWalletDir();
  const path = getWalletPath(wallet.name);
  try {
    // O_CREAT | O_EXCL | O_WRONLY — fails if file already exists (atomic check-and-create)
    const fd = openSync(path, constants.O_CREAT | constants.O_EXCL | constants.O_WRONLY, 0o600);
    const data = JSON.stringify(wallet, null, 2);
    writeFileSync(fd, data, 'utf8');
    closeSync(fd);
    return true;
  } catch (err: any) {
    if (err.code === 'EEXIST') return false;
    throw err;
  }
}

export function loadWallet(name: string): StoredWallet | null {
  const path = getWalletPath(name);
  if (!existsSync(path)) {
    return null;
  }
  const data = readFileSync(path, 'utf8');
  const parsed = JSON.parse(data);
  // Basic schema validation
  if (!parsed.id || !parsed.name || !parsed.address || typeof parsed.chainId !== 'number') {
    throw new Error(`Corrupted wallet file: ${name}`);
  }
  return parsed as StoredWallet;
}

export function listAllWallets(): StoredWallet[] {
  ensureWalletDir();
  const files = readdirSync(WALLET_DIR).filter(f => f.endsWith('.json'));
  const wallets: StoredWallet[] = [];
  for (const f of files) {
    try {
      const data = readFileSync(join(WALLET_DIR, f), 'utf8');
      const parsed = JSON.parse(data);
      if (parsed.id && parsed.name && parsed.address && typeof parsed.chainId === 'number') {
        wallets.push(parsed as StoredWallet);
      }
    } catch {
      // Skip corrupted files
    }
  }
  return wallets;
}

export function deleteWalletFile(name: string): boolean {
  const path = getWalletPath(name);
  if (!existsSync(path)) {
    return false;
  }
  unlinkSync(path);
  return true;
}

// --- Crossmint wallet storage ---

const CROSSMINT_DIR = join(homedir(), '.agent-arena', 'crossmint-wallets');

export function ensureCrossmintDir(): void {
  if (!existsSync(CROSSMINT_DIR)) {
    mkdirSync(CROSSMINT_DIR, { recursive: true, mode: 0o700 });
  }
}

export function getCrossmintWalletPath(name: string): string {
  validateWalletName(name);
  return join(CROSSMINT_DIR, `${name}.json`);
}

export function saveCrossmintWallet(wallet: CrossmintWalletRecord): boolean {
  ensureCrossmintDir();
  const path = getCrossmintWalletPath(wallet.name);
  try {
    const fd = openSync(path, constants.O_CREAT | constants.O_EXCL | constants.O_WRONLY, 0o600);
    const data = JSON.stringify(wallet, null, 2);
    writeFileSync(fd, data, 'utf8');
    closeSync(fd);
    return true;
  } catch (err: any) {
    if (err.code === 'EEXIST') return false;
    throw err;
  }
}

export function loadCrossmintWallet(name: string): CrossmintWalletRecord | null {
  const path = getCrossmintWalletPath(name);
  if (!existsSync(path)) return null;
  const data = readFileSync(path, 'utf8');
  return JSON.parse(data) as CrossmintWalletRecord;
}

export function listCrossmintWallets(): CrossmintWalletRecord[] {
  ensureCrossmintDir();
  const files = readdirSync(CROSSMINT_DIR).filter(f => f.endsWith('.json'));
  const wallets: CrossmintWalletRecord[] = [];
  for (const f of files) {
    try {
      const data = readFileSync(join(CROSSMINT_DIR, f), 'utf8');
      const parsed = JSON.parse(data);
      if (parsed.id && parsed.name && parsed.address && parsed.chainType) {
        wallets.push(parsed as CrossmintWalletRecord);
      }
    } catch {
      // Skip corrupted files
    }
  }
  return wallets;
}

export function crossmintWalletExists(name: string): boolean {
  return existsSync(getCrossmintWalletPath(name));
}

// --- Crossmint supported chain types ---

export const CROSSMINT_CHAIN_TYPES = Object.freeze([
  'evm',
  'solana',
  'aptos',
  'sui',
  'stellar'
] as const);

export type CrossmintChainType = typeof CROSSMINT_CHAIN_TYPES[number];

// --- Standard chain config ---

export const CHAIN_CONFIG: Readonly<Record<string, { chainId: number; name: string; rpcUrl: string }>> = Object.freeze({
  base: Object.freeze({
    chainId: 8453,
    name: 'Base',
    rpcUrl: 'https://mainnet.base.org'
  }),
  ethereum: Object.freeze({
    chainId: 1,
    name: 'Ethereum',
    rpcUrl: 'https://eth.llamarpc.com'
  }),
  arbitrum: Object.freeze({
    chainId: 42161,
    name: 'Arbitrum One',
    rpcUrl: 'https://arb1.arbitrum.io/rpc'
  }),
  optimism: Object.freeze({
    chainId: 10,
    name: 'Optimism',
    rpcUrl: 'https://mainnet.optimism.io'
  }),
  polygon: Object.freeze({
    chainId: 137,
    name: 'Polygon',
    rpcUrl: 'https://polygon-rpc.com'
  })
});

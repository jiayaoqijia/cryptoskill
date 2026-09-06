import { existsSync, readFileSync } from 'node:fs';
import AElf from 'aelf-sdk';
import { unlockKeystore } from 'aelf-sdk/src/util/keyStore.js';
import {
  createCaSigner,
  createEoaSigner,
  createSignerFromEnv,
  type AelfSigner,
} from '@portkey/aelf-signer';
import {
  getActiveWalletProfile,
  type SignerContextInput,
  type SignerProvider,
} from './wallet-context.js';
import { SIGNER_ERROR_CODES } from './signer-error-codes.js';

export class SignerContextError extends Error {
  code: string;
  details?: unknown;

  constructor(code: string, message: string, details?: unknown) {
    super(message);
    this.code = code;
    this.details = details;
  }
}

export type ResolvedSignerContext = {
  signer: AelfSigner;
  provider: SignerProvider;
  warnings: string[];
  identity: {
    walletType: 'EOA' | 'CA';
    address?: string;
    caAddress?: string;
    caHash?: string;
  };
};

function decryptEoaPrivateKey(
  walletFile: string,
  password: string,
): { privateKey: string; address?: string } {
  if (!existsSync(walletFile)) {
    throw new SignerContextError(
      SIGNER_ERROR_CODES.CONTEXT_INVALID,
      `active EOA wallet file not found: ${walletFile}`,
    );
  }
  const raw = JSON.parse(readFileSync(walletFile, 'utf8')) as Record<string, unknown>;
  const encrypted =
    typeof raw.AESEncryptPrivateKey === 'string' ? raw.AESEncryptPrivateKey : '';
  if (!encrypted) {
    throw new SignerContextError(
      SIGNER_ERROR_CODES.CONTEXT_INVALID,
      'active EOA wallet file missing AESEncryptPrivateKey',
    );
  }
  const privateKey = AElf.wallet.AESDecrypt(encrypted, password);
  if (!privateKey) {
    throw new SignerContextError(
      SIGNER_ERROR_CODES.PASSWORD_REQUIRED,
      'failed to decrypt active EOA wallet: wrong password or corrupted file',
    );
  }
  return {
    privateKey,
    address: typeof raw.address === 'string' ? raw.address : undefined,
  };
}

function resolveFromExplicit(input: SignerContextInput): ResolvedSignerContext | null {
  if (!input.privateKey) return null;

  if (
    input.walletType === 'CA' &&
    input.caHash &&
    input.caAddress
  ) {
    return {
      signer: createCaSigner({
        managerPrivateKey: input.privateKey,
        caHash: input.caHash,
        caAddress: input.caAddress,
      }),
      provider: 'explicit',
      warnings: [],
      identity: {
        walletType: 'CA',
        caAddress: input.caAddress,
        caHash: input.caHash,
      },
    };
  }

  return {
    signer: createEoaSigner(input.privateKey),
    provider: 'explicit',
    warnings: [],
    identity: {
      walletType: 'EOA',
    },
  };
}

function resolveFromContext(input: SignerContextInput): ResolvedSignerContext {
  const profile = getActiveWalletProfile();
  if (!profile) {
    throw new SignerContextError(
      SIGNER_ERROR_CODES.CONTEXT_NOT_FOUND,
      'active wallet context not found',
    );
  }

  if (profile.walletType === 'EOA') {
    const password = input.password || process.env.PORTKEY_WALLET_PASSWORD;
    if (!password) {
      throw new SignerContextError(
        SIGNER_ERROR_CODES.PASSWORD_REQUIRED,
        'password required for active EOA wallet (set PORTKEY_WALLET_PASSWORD or pass signer.password)',
      );
    }
    const walletFile = profile.walletFile;
    if (!walletFile) {
      throw new SignerContextError(
        SIGNER_ERROR_CODES.CONTEXT_INVALID,
        'active EOA profile missing walletFile',
      );
    }
    const { privateKey, address } = decryptEoaPrivateKey(walletFile, password);
    return {
      signer: createEoaSigner(privateKey),
      provider: 'context',
      warnings: [],
      identity: {
        walletType: 'EOA',
        address,
      },
    };
  }

  const password = input.password || process.env.PORTKEY_CA_KEYSTORE_PASSWORD;
  if (!password) {
    throw new SignerContextError(
      SIGNER_ERROR_CODES.PASSWORD_REQUIRED,
      'password required for active CA keystore (set PORTKEY_CA_KEYSTORE_PASSWORD or pass signer.password)',
    );
  }
  const keystoreFile = profile.keystoreFile;
  if (!keystoreFile || !existsSync(keystoreFile)) {
    throw new SignerContextError(
      SIGNER_ERROR_CODES.CONTEXT_INVALID,
      `active CA profile keystore not found: ${keystoreFile || '<empty>'}`,
    );
  }
  const raw = JSON.parse(readFileSync(keystoreFile, 'utf8')) as Record<string, any>;
  const decrypted = unlockKeystore(raw.keystore, password);
  if (!decrypted?.privateKey) {
    throw new SignerContextError(
      SIGNER_ERROR_CODES.PASSWORD_REQUIRED,
      'failed to decrypt active CA keystore: wrong password or corrupted file',
    );
  }
  const caHash =
    (typeof raw.caHash === 'string' ? raw.caHash : undefined) || profile.caHash;
  const caAddress =
    (typeof raw.caAddress === 'string' ? raw.caAddress : undefined) || profile.caAddress;
  if (!caHash || !caAddress) {
    throw new SignerContextError(
      SIGNER_ERROR_CODES.CONTEXT_INVALID,
      'active CA profile missing caHash/caAddress',
    );
  }
  return {
    signer: createCaSigner({
      managerPrivateKey: decrypted.privateKey,
      caHash,
      caAddress,
    }),
    provider: 'context',
    warnings: [],
    identity: {
      walletType: 'CA',
      caHash,
      caAddress,
      address: profile.address,
    },
  };
}

export function resolveSignerContext(
  input: SignerContextInput = {},
): ResolvedSignerContext {
  const mode = input.signerMode || 'auto';
  const warnings: string[] = [];
  let contextError: unknown = null;

  if (mode === 'daemon') {
    throw new SignerContextError(
      SIGNER_ERROR_CODES.DAEMON_NOT_IMPLEMENTED,
      'daemon signer provider is reserved for future release',
    );
  }

  if (mode === 'explicit' || mode === 'auto') {
    const explicit = resolveFromExplicit(input);
    if (explicit) {
      explicit.warnings = warnings;
      return explicit;
    }
  }

  if (mode === 'context' || mode === 'auto') {
    try {
      const context = resolveFromContext(input);
      context.warnings = warnings;
      return context;
    } catch (error) {
      contextError = error;
      if (mode === 'context') throw error;
    }
  }

  if (mode === 'env' || mode === 'auto') {
    try {
      const signer = createSignerFromEnv();
      return {
        signer,
        provider: 'env',
        warnings,
        identity: {
          walletType:
            process.env.PORTKEY_CA_HASH && process.env.PORTKEY_CA_ADDRESS
              ? 'CA'
              : 'EOA',
          address: signer.address,
          caHash: process.env.PORTKEY_CA_HASH,
          caAddress: process.env.PORTKEY_CA_ADDRESS,
        },
      };
    } catch (error) {
      if (mode === 'env') throw error;
    }
  }

  if (contextError) {
    throw contextError;
  }

  throw new SignerContextError(
    SIGNER_ERROR_CODES.CONTEXT_NOT_FOUND,
    'no signer available from explicit/context/env',
  );
}

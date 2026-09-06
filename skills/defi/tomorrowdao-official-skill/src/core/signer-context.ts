import { existsSync, readFileSync } from 'node:fs';
import AElf from 'aelf-sdk';
import { unlockKeystore } from 'aelf-sdk/src/util/keyStore.js';
import { SkillError } from './errors.js';
import { SIGNER_ERROR_CODES } from './signer-error-codes.js';
import {
  getActiveWalletProfile,
  type SignerContextInput,
  type SignerProvider,
} from './wallet-context.js';

export type ResolvedPrivateKeyContext = {
  privateKey: string;
  provider: SignerProvider;
  warnings: string[];
  identity: {
    walletType: 'EOA' | 'CA';
    address?: string;
    caAddress?: string;
    caHash?: string;
  };
};

function resolveExplicit(input: SignerContextInput): ResolvedPrivateKeyContext | null {
  if (!input.privateKey) return null;
  return {
    privateKey: input.privateKey,
    provider: 'explicit',
    warnings: [],
    identity: {
      walletType: input.walletType || 'EOA',
      address: input.address,
      caAddress: input.caAddress,
      caHash: input.caHash,
    },
  };
}

function resolveContext(input: SignerContextInput): ResolvedPrivateKeyContext {
  const profile = getActiveWalletProfile();
  if (!profile) {
    throw new SkillError(
      SIGNER_ERROR_CODES.CONTEXT_NOT_FOUND,
      'active wallet context not found',
    );
  }

  if (profile.walletType === 'EOA') {
    const password = input.password || process.env.PORTKEY_WALLET_PASSWORD;
    if (!password) {
      throw new SkillError(
        SIGNER_ERROR_CODES.PASSWORD_REQUIRED,
        'password required for active EOA wallet (set PORTKEY_WALLET_PASSWORD or pass signerContext.password)',
      );
    }
    if (!profile.walletFile || !existsSync(profile.walletFile)) {
      throw new SkillError(
        SIGNER_ERROR_CODES.CONTEXT_INVALID,
        `active EOA wallet file not found: ${profile.walletFile || '<empty>'}`,
      );
    }
    const raw = JSON.parse(readFileSync(profile.walletFile, 'utf8')) as Record<string, unknown>;
    const encrypted =
      typeof raw.AESEncryptPrivateKey === 'string' ? raw.AESEncryptPrivateKey : '';
    if (!encrypted) {
      throw new SkillError(
        SIGNER_ERROR_CODES.CONTEXT_INVALID,
        'active EOA wallet file missing AESEncryptPrivateKey',
      );
    }
    const privateKey = AElf.wallet.AESDecrypt(encrypted, password);
    if (!privateKey) {
      throw new SkillError(
        SIGNER_ERROR_CODES.PASSWORD_REQUIRED,
        'failed to decrypt active EOA wallet: wrong password or corrupted file',
      );
    }
    return {
      privateKey,
      provider: 'context',
      warnings: [],
      identity: {
        walletType: 'EOA',
        address: profile.address || (typeof raw.address === 'string' ? raw.address : undefined),
      },
    };
  }

  const password = input.password || process.env.PORTKEY_CA_KEYSTORE_PASSWORD;
  if (!password) {
    throw new SkillError(
      SIGNER_ERROR_CODES.PASSWORD_REQUIRED,
      'password required for active CA keystore (set PORTKEY_CA_KEYSTORE_PASSWORD or pass signerContext.password)',
    );
  }
  if (!profile.keystoreFile || !existsSync(profile.keystoreFile)) {
    throw new SkillError(
      SIGNER_ERROR_CODES.CONTEXT_INVALID,
      `active CA keystore not found: ${profile.keystoreFile || '<empty>'}`,
    );
  }

  const raw = JSON.parse(readFileSync(profile.keystoreFile, 'utf8')) as Record<string, any>;
  const decrypted = unlockKeystore(raw.keystore, password);
  if (!decrypted?.privateKey) {
    throw new SkillError(
      SIGNER_ERROR_CODES.PASSWORD_REQUIRED,
      'failed to decrypt active CA keystore: wrong password or corrupted file',
    );
  }
  return {
    privateKey: decrypted.privateKey,
    provider: 'context',
    warnings: [],
    identity: {
      walletType: 'CA',
      address: profile.address,
      caHash: profile.caHash || (typeof raw.caHash === 'string' ? raw.caHash : undefined),
      caAddress:
        profile.caAddress || (typeof raw.caAddress === 'string' ? raw.caAddress : undefined),
    },
  };
}

export function resolvePrivateKeyContext(
  input: SignerContextInput = {},
): ResolvedPrivateKeyContext {
  const mode = input.signerMode || 'auto';
  let contextError: unknown = null;

  if (mode === 'daemon') {
    throw new SkillError(
      SIGNER_ERROR_CODES.DAEMON_NOT_IMPLEMENTED,
      'daemon signer provider is reserved for future release',
    );
  }

  if (mode === 'explicit' || mode === 'auto') {
    const explicit = resolveExplicit(input);
    if (explicit) return explicit;
  }

  if (mode === 'context' || mode === 'auto') {
    try {
      return resolveContext(input);
    } catch (error) {
      contextError = error;
      if (mode === 'context') throw error;
    }
  }

  if (mode === 'env' || mode === 'auto') {
    const privateKey =
      input.privateKey ||
      process.env.TMRW_PRIVATE_KEY ||
      process.env.AELF_PRIVATE_KEY ||
      process.env.PORTKEY_PRIVATE_KEY;
    if (privateKey) {
      return {
        privateKey,
        provider: 'env',
        warnings: [],
        identity: {
          walletType:
            process.env.PORTKEY_CA_HASH && process.env.PORTKEY_CA_ADDRESS
              ? 'CA'
              : 'EOA',
          caHash: process.env.PORTKEY_CA_HASH,
          caAddress: process.env.PORTKEY_CA_ADDRESS,
        },
      };
    }
    if (mode === 'env') {
      throw new SkillError(
        SIGNER_ERROR_CODES.CONTEXT_NOT_FOUND,
        'no private key available from env',
      );
    }
  }

  if (contextError) {
    throw contextError;
  }

  throw new SkillError(
    SIGNER_ERROR_CODES.CONTEXT_NOT_FOUND,
    'no signer available from explicit/context/env',
  );
}

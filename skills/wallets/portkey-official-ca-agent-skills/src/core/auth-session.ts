import { createWallet } from '../../lib/aelf-client.js';
import type {
  PortkeyConfig,
  RecoverAndSaveWalletParams,
  RecoverAndSaveWalletResult,
} from '../../lib/types.js';
import {
  recoverWallet,
  checkRegisterOrRecoveryStatus,
} from './auth.js';
import { saveKeystore } from './keystore.js';

const DEFAULT_MAX_STATUS_CHECKS = 15;
const DEFAULT_STATUS_CHECK_DELAY_MS = 2000;

export async function recoverAndSaveWallet(
  config: PortkeyConfig,
  params: RecoverAndSaveWalletParams,
): Promise<RecoverAndSaveWalletResult> {
  if (!params.email) throw new Error('email is required');
  if (!params.password) throw new Error('password is required');
  if (!params.chainId) throw new Error('chainId is required');
  if (!params.network) throw new Error('network is required');
  if (!Array.isArray(params.guardiansApproved) || params.guardiansApproved.length === 0) {
    throw new Error('guardiansApproved is required');
  }

  const managerWallet = createWallet();
  if (!managerWallet.privateKey) throw new Error('createWallet did not return a privateKey');
  if (!managerWallet.mnemonic) throw new Error('createWallet did not return a mnemonic');

  const recovery = await recoverWallet(config, {
    email: params.email,
    manager: managerWallet.address,
    guardiansApproved: params.guardiansApproved,
    chainId: params.chainId,
    extraData: params.extraData,
  });

  const status = await waitForRecoveryPass(config, {
    sessionId: recovery.sessionId,
    maxChecks: params.maxStatusChecks,
    delayMs: params.statusCheckDelayMs,
  });

  const saved = saveKeystore({
    password: params.password,
    privateKey: managerWallet.privateKey,
    mnemonic: managerWallet.mnemonic,
    caHash: status.caHash,
    caAddress: status.caAddress,
    loginEmail: params.loginEmail || params.email,
    originChainId: params.chainId,
    network: params.network,
  });

  return {
    sessionId: recovery.sessionId,
    status: 'pass',
    caAddress: status.caAddress,
    caHash: status.caHash,
    keystorePath: saved.keystorePath,
    managerAddress: saved.managerAddress,
    originChainId: params.chainId,
    loginEmail: params.loginEmail || params.email,
  };
}

async function waitForRecoveryPass(
  config: PortkeyConfig,
  params: {
    sessionId: string;
    maxChecks?: number;
    delayMs?: number;
  },
): Promise<{ caAddress: string; caHash: string }> {
  const maxChecks = params.maxChecks ?? DEFAULT_MAX_STATUS_CHECKS;
  const delayMs = params.delayMs ?? DEFAULT_STATUS_CHECK_DELAY_MS;

  for (let attempt = 0; attempt < maxChecks; attempt += 1) {
    const status = await checkRegisterOrRecoveryStatus(config, {
      sessionId: params.sessionId,
      type: 'recovery',
    });
    if (status.status === 'pass' && status.caAddress && status.caHash) {
      return {
        caAddress: status.caAddress,
        caHash: status.caHash,
      };
    }
    if (status.status === 'fail') {
      throw new Error(status.failMessage || 'Recovery failed');
    }
    await sleep(delayMs);
  }

  throw new Error(
    `Recovery ${params.sessionId} did not reach pass status after ${maxChecks} checks`,
  );
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

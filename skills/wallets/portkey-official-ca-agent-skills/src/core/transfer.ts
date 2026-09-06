import AElf from 'aelf-sdk';
import type {
  PortkeyConfig,
  TransferParams,
  CrossChainTransferParams,
  TransferResult,
  TransactionResultParams,
  TransactionResult,
  ChainId,
  TransactionFeePreview,
} from '../../lib/types.js';
import {
  getTxResult,
  callSendMethod,
  type AElfWallet,
} from '../../lib/aelf-client.js';
import { getChainInfoByChainId } from './account.js';
import { managerForwardCall } from './contract.js';
import { checkManagerSyncState, formatManagerSyncError } from './manager-sync.js';

// ============================================================================
// sameChainTransfer
// ============================================================================

/**
 * Transfer tokens on the same chain via ManagerForwardCall.
 *
 * Flow:
 *   Manager signs → CA contract.ManagerForwardCall → Token contract.Transfer
 *
 * The recipient sees the transfer coming from the CA address.
 */
export async function sameChainTransfer(
  config: PortkeyConfig,
  wallet: AElfWallet,
  params: TransferParams,
): Promise<TransferResult> {
  if (!params.caHash) throw new Error('caHash is required');
  if (!params.tokenContractAddress) throw new Error('tokenContractAddress is required');
  if (!params.symbol) throw new Error('symbol is required');
  if (!params.to) throw new Error('to address is required');
  if (!params.amount) throw new Error('amount is required');
  if (!params.chainId) throw new Error('chainId is required');

  const managerSync = await checkManagerSyncState(config, {
    caHash: params.caHash,
    chainId: params.chainId,
    managerAddress: wallet.address,
  });
  if (!managerSync.isManagerSynced) {
    throw new Error(formatManagerSyncError(managerSync));
  }

  const result = await managerForwardCall(config, wallet, {
    caHash: params.caHash,
    contractAddress: params.tokenContractAddress,
    methodName: 'Transfer',
    args: {
      symbol: params.symbol,
      to: params.to,
      amount: params.amount,
      memo: params.memo || '',
    },
    chainId: params.chainId,
    guardiansApproved: params.guardiansApproved,
    managerSync,
  });

  return {
    transactionId: result.transactionId,
    status: result.data.Status,
    feePreview: normalizeFeePreviewForCa(result.feePreview, result.caAddress),
  };
}

// ============================================================================
// crossChainTransfer
// ============================================================================

/**
 * Transfer tokens cross-chain. This is a two-step process:
 *
 * Step 1: Transfer tokens to the manager address itself (via ManagerForwardCall)
 * Step 2: Manager calls CrossChainTransfer on the token contract directly
 *
 * The cross-chain bridge handles moving the tokens to the target chain.
 */
export async function crossChainTransfer(
  config: PortkeyConfig,
  wallet: AElfWallet,
  params: CrossChainTransferParams,
): Promise<TransferResult> {
  if (!params.caHash) throw new Error('caHash is required');
  if (!params.tokenContractAddress) throw new Error('tokenContractAddress is required');
  if (!params.symbol) throw new Error('symbol is required');
  if (!params.to) throw new Error('to address is required');
  if (!params.amount) throw new Error('amount is required');
  if (!params.chainId) throw new Error('source chainId is required');
  if (!params.toChainId) throw new Error('toChainId is required');

  const managerSync = await checkManagerSyncState(config, {
    caHash: params.caHash,
    chainId: params.chainId,
    managerAddress: wallet.address,
  });
  if (!managerSync.isManagerSynced) {
    throw new Error(formatManagerSyncError(managerSync));
  }

  const chainInfo = await getChainInfoByChainId(config, params.chainId);

  // Step 1: Transfer tokens to manager address (so manager can call CrossChainTransfer)
  const step1Result = await managerForwardCall(config, wallet, {
    caHash: params.caHash,
    contractAddress: params.tokenContractAddress,
    methodName: 'Transfer',
    args: {
      symbol: params.symbol,
      to: wallet.address,
      amount: params.amount,
      memo: params.memo || '',
    },
    chainId: params.chainId,
    guardiansApproved: params.guardiansApproved,
    managerSync,
  });

  if (step1Result.data.Status !== 'MINED') {
    throw new Error(
      `Cross-chain step 1 failed (transfer to manager): ${step1Result.data.Error || step1Result.data.Status}`,
    );
  }

  // Step 2: Call CrossChainTransfer on the token contract directly
  // (manager now has the tokens, so it can call the token contract directly)
  try {
    const crossChainResult = await callSendMethod(
      chainInfo.endPoint,
      params.tokenContractAddress,
      wallet,
      'CrossChainTransfer',
      {
        to: params.to,
        symbol: params.symbol,
        amount: params.amount,
        memo: params.memo || '',
        toChainId: chainIdToNum(params.toChainId),
        issueChainId: params.issueChainId || chainIdToNum(params.chainId),
      },
    );

    return {
      transactionId: crossChainResult.transactionId,
      status: crossChainResult.data.Status,
      feePreview: normalizeFeePreviewForCa(step1Result.feePreview, step1Result.caAddress),
    };
  } catch (step2Err: unknown) {
    // Step 1 succeeded but Step 2 failed — tokens are stuck on the Manager address.
    // Provide detailed recovery info so the caller (or AI) can use recoverStuckTransfer.
    const msg = step2Err instanceof Error ? step2Err.message : String(step2Err);
    throw new Error(
      `Cross-chain step 2 failed: ${msg}\n\n` +
      `⚠ RECOVERY NEEDED: ${params.amount} ${params.symbol} is now on Manager address (${wallet.address}), ` +
      `not the CA wallet. Use the "recoverStuckTransfer" tool to transfer tokens back to the CA, ` +
      `or retry the cross-chain transfer manually.\n` +
      `Recovery params: { managerAddress: "${wallet.address}", tokenContractAddress: "${params.tokenContractAddress}", ` +
      `symbol: "${params.symbol}", amount: "${params.amount}", chainId: "${params.chainId}", ` +
      `caHash: "${params.caHash}", step1TxId: "${step1Result.transactionId}" }`,
    );
  }
}

// ============================================================================
// recoverStuckTransfer
// ============================================================================

export interface RecoverStuckTransferParams {
  /** Token contract address on the chain */
  tokenContractAddress: string;
  /** Token symbol (e.g. ELF) */
  symbol: string;
  /** Amount in smallest unit */
  amount: string;
  /** CA address to transfer tokens back to */
  caAddress: string;
  /** Chain ID */
  chainId: ChainId;
  /** Optional memo */
  memo?: string;
}

/**
 * Recover tokens stuck on the Manager address after a failed cross-chain transfer.
 *
 * When crossChainTransfer Step 1 (CA → Manager) succeeds but Step 2
 * (Manager → CrossChainTransfer) fails, tokens remain on the Manager address.
 * This function transfers them back to the CA address.
 *
 * Flow: Manager signs → Token contract.Transfer → CA address
 */
export async function recoverStuckTransfer(
  config: PortkeyConfig,
  wallet: AElfWallet,
  params: RecoverStuckTransferParams,
): Promise<TransferResult> {
  if (!params.tokenContractAddress) throw new Error('tokenContractAddress is required');
  if (!params.symbol) throw new Error('symbol is required');
  if (!params.amount) throw new Error('amount is required');
  if (!params.caAddress) throw new Error('caAddress is required');
  if (!params.chainId) throw new Error('chainId is required');

  const chainInfo = await getChainInfoByChainId(config, params.chainId);

  // Manager directly calls Transfer to send tokens back to CA
  const result = await callSendMethod(
    chainInfo.endPoint,
    params.tokenContractAddress,
    wallet,
    'Transfer',
    {
      to: params.caAddress,
      symbol: params.symbol,
      amount: params.amount,
      memo: params.memo || 'recover stuck cross-chain transfer',
    },
  );

  return {
    transactionId: result.transactionId,
    status: result.data.Status,
  };
}

// ============================================================================
// getTransactionResult
// ============================================================================

/**
 * Get the result of a transaction by its ID.
 */
export async function getTransactionResult(
  config: PortkeyConfig,
  params: TransactionResultParams,
): Promise<TransactionResult> {
  if (!params.txId) throw new Error('txId is required');
  if (!params.chainId) throw new Error('chainId is required');

  const chainInfo = await getChainInfoByChainId(config, params.chainId);
  return getTxResult(chainInfo.endPoint, params.txId);
}

// ============================================================================
// Helpers
// ============================================================================

/**
 * Convert chain ID string to its numeric representation via base58 decode.
 *
 * 'AELF' → 9992731, 'tDVV' → 1866392
 *
 * Uses aelf-sdk's official `chainIdConvertor.base58ToChainId` which:
 *   1. Base58 decodes the string to 3 bytes
 *   2. Pads to 4 bytes
 *   3. Reads as little-endian int32
 */
function chainIdToNum(chainId: string): number {
  return AElf.utils.chainIdConvertor.base58ToChainId(chainId);
}

function normalizeFeePreviewForCa(
  preview: TransactionFeePreview | null | undefined,
  caAddress: string,
): TransactionFeePreview | undefined {
  if (!preview) return undefined;
  const chargingAddress = preview.chargingAddress || null;
  return {
    ...preview,
    chargingAddress,
    isCaPayingFee: chargingAddress ? chargingAddress === caAddress : null,
  };
}
